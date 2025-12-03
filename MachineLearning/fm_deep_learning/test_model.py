# test_model.py

import torch
import random

from src.model import MatrixFactorization
from src.config import MODEL_PATH

def run_test():
    """
    저장된 모델을 불러와 예측 및 추천 테스트를 수행합니다.
    """
    try:
        # CPU로 모델을 로드합니다. GPU에서 테스트하려면 "cpu"를 "cuda" 등으로 변경
        device = torch.device("cpu") 
        # PyTorch 최신 버전의 보안 정책에 따라, 가중치 외에 다른 객체(ID 맵)가 포함된 파일을 불러오려면
        # weights_only=False 옵션을 명시적으로 추가해야 합니다.
        checkpoint = torch.load(MODEL_PATH, map_location=device, weights_only=False)
        print(f"✅ Checkpoint loaded from {MODEL_PATH}")
    except FileNotFoundError:
        print(f"❌ Model file not found. Please run 'python train.py' first.")
        return

    # --- 1. 모델 및 메타데이터 로드 ---
    user_id_map = checkpoint["user_id_map"]
    item_id_map = checkpoint["item_id_map"]
    embedding_dim = checkpoint["embedding_dimension"]

    n_users = len(user_id_map)
    n_items = len(item_id_map)

    model = MatrixFactorization(n_users, n_items, embedding_dim).to(device)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()

    print("\n=== 모델 로드 완료 ===")
    print(f"총 사용자 수: {n_users}")
    print(f"총 아이템(영화) 수: {n_items}")
    print(f"임베딩 차원: {embedding_dim}")

    # --- 2. 예측(Prediction) 테스트 ---
    # 테스트할 실제 사용자 ID를 랜덤으로 선택
    test_user_id = random.choice(list(user_id_map.keys()))
    test_movie_id = random.choice(list(item_id_map.keys()))

    # 실제 ID를 모델 인덱스로 변환
    test_user_idx = user_id_map[test_user_id]
    test_movie_idx = item_id_map[test_movie_id]

    # 텐서 생성
    u_tensor = torch.LongTensor([test_user_idx]).to(device)
    m_tensor = torch.LongTensor([test_movie_idx]).to(device)

    with torch.no_grad():
        prediction = model(u_tensor, m_tensor).item()

    print("\n=== 개별 예측 테스트 ===")
    print(f"테스트 사용자 ID: {test_user_id} (인덱스: {test_user_idx})")
    print(f"테스트 영화 ID: {test_movie_id} (인덱스: {test_movie_idx})")
    print(f"-> 예측 평점: {prediction:.4f}")

    # --- 3. 추천(Recommendation) 테스트 ---
    top_k = 5
    
    # 역방향 맵 (인덱스 -> 실제 ID) 생성
    reversed_item_map = {v: k for k, v in item_id_map.items()}

    with torch.no_grad():
        all_movie_indices = torch.arange(n_items, dtype=torch.long, device=device)
        user_indices = torch.full((n_items,), test_user_idx, dtype=torch.long, device=device)
        scores = model(user_indices, all_movie_indices)
        top_scores, top_indices = torch.topk(scores, top_k)

    recommended_movie_ids = [reversed_item_map[idx.item()] for idx in top_indices]
    
    print(f"\n=== Top-{top_k} 추천 테스트 ===")
    print(f"사용자 ID {test_user_id}를 위한 추천 영화 목록:")
    for i, movie_id in enumerate(recommended_movie_ids):
        print(f"  {i+1}. 영화 ID: {movie_id} (예상 점수: {top_scores[i]:.4f})")


if __name__ == "__main__":
    run_test()