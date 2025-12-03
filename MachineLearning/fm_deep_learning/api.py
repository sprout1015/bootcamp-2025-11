# api.py

import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.model import MatrixFactorization
from src.config import MODEL_PATH
from src.evaluator import get_device

# --- App & Global Variables ---

app = FastAPI(title="Movie Recommender API")

# 모델과 관련 메타데이터를 저장할 전역 변수
model_data = {
    "model": None,
    "user_id_map": None,
    "item_id_map": None,
    "device": get_device()
}

# --- Pydantic Models ---

class PredictRequest(BaseModel):
    user_id: int  # 모델 인덱스가 아닌, 실제 user_id를 받습니다.
    movie_id: int # 모델 인덱스가 아닌, 실제 movie_id를 받습니다.


# --- Helper Functions ---

def load_model():
    """
    저장된 모델과 메타데이터(ID 맵)를 불러옵니다.
    """
    try:
        # PyTorch 최신 버전의 보안 정책에 따라, 가중치 외에 다른 객체(ID 맵)가 포함된 파일을 불러오려면
        # weights_only=False 옵션을 명시적으로 추가해야 합니다.
        checkpoint = torch.load(MODEL_PATH, map_location=model_data["device"], weights_only=False)
        
        user_id_map = checkpoint["user_id_map"]
        item_id_map = checkpoint["item_id_map"]
        embedding_dim = checkpoint["embedding_dimension"]

        n_users = len(user_id_map)
        n_items = len(item_id_map)

        model = MatrixFactorization(n_users, n_items, embedding_dim).to(model_data["device"])
        model.load_state_dict(checkpoint["model_state_dict"])
        model.eval()

        print(f"✅ Model loaded on {model_data['device']}")
        return model, user_id_map, item_id_map

    except FileNotFoundError:
        print(f"❌ Model file not found at {MODEL_PATH}")
        return None, None, None
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return None, None, None


# --- FastAPI Events ---

@app.on_event("startup")
async def startup_event():
    """
    API 서버가 시작될 때 모델을 로드합니다.
    """
    model, user_map, item_map = load_model()
    if model is not None:
        model_data["model"] = model
        model_data["user_id_map"] = user_map
        model_data["item_id_map"] = item_map


# --- API Endpoints ---

@app.post("/predict")
async def predict(req: PredictRequest):
    """
    특정 사용자(user_id)와 영화(movie_id)에 대한 평점을 예측합니다.
    """
    if model_data["model"] is None:
        raise HTTPException(status_code=503, detail="Model is not loaded")

    # 입력받은 실제 ID가 학습된 ID 맵에 있는지 확인
    if req.user_id not in model_data["user_id_map"]:
        raise HTTPException(status_code=404, detail=f"User ID {req.user_id} not found in trained data.")
    if req.movie_id not in model_data["item_id_map"]:
        raise HTTPException(status_code=404, detail=f"Movie ID {req.movie_id} not found in trained data.")

    # 실제 ID를 모델이 사용하는 인덱스(idx)로 변환
    user_idx = model_data["user_id_map"][req.user_id]
    movie_idx = model_data["item_id_map"][req.movie_id]

    with torch.no_grad():
        u = torch.LongTensor([user_idx]).to(model_data["device"])
        m = torch.LongTensor([movie_idx]).to(model_data["device"])
        prediction = model_data["model"](u, m).item()

    return {
        "user_id": req.user_id,
        "movie_id": req.movie_id,
        "predicted_rating": f"{prediction:.4f}",
    }


@app.get("/recommend/{user_id}")
async def recommend(user_id: int, top_k: int = 10):
    """
    특정 사용자(user_id)에게 가장 높은 평점이 예상되는 영화 K개를 추천합니다.
    """
    model = model_data["model"]
    user_map = model_data["user_id_map"]
    item_map = model_data["item_id_map"]

    if model is None:
        raise HTTPException(status_code=503, detail="Model is not loaded")

    if user_id not in user_map:
        raise HTTPException(status_code=404, detail=f"User ID {user_id} not found in trained data.")

    user_idx = user_map[user_id]
    n_items = len(item_map)
    device = model_data["device"]

    with torch.no_grad():
        # 모든 영화에 대한 예측 평점을 계산
        all_movie_indices = torch.arange(n_items, dtype=torch.long, device=device)
        user_indices = torch.full((n_items,), user_idx, dtype=torch.long, device=device)
        scores = model(user_indices, all_movie_indices)

        # 점수가 가장 높은 상위 K개를 선택
        top_scores, top_indices = torch.topk(scores, top_k)

    # 모델 인덱스(idx)를 실제 영화 ID로 변환
    # 역방향 맵(idx -> id) 생성
    reversed_item_map = {v: k for k, v in item_map.items()}
    # FastAPI가 JSON으로 변환할 수 있도록, NumPy 숫자 타입을 표준 int 타입으로 캐스팅합니다.
    recommended_movie_ids = [int(reversed_item_map[idx.item()]) for idx in top_indices]

    return {
        "user_id": user_id,
        "top_k": top_k,
        "recommended_movie_ids": recommended_movie_ids,
        "scores": [f"{s.item():.4f}" for s in top_scores],
    }

# FastAPI 서버 실행:
# 터미널에서 uvicorn api:app --reload