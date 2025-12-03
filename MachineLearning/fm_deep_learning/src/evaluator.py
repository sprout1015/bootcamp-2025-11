# src/evaluator.py

import torch
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error

def get_device():
    """Helper function to determine the available device."""
    if torch.backends.mps.is_available():
        return torch.device("mps")
    elif torch.cuda.is_available():
        return torch.device("cuda")
    else:
        return torch.device("cpu")

def evaluate(model, test_data):
    """
    학습된 모델의 성능을 평가합니다.
    
    Args:
        model (nn.Module): 평가할 학습된 모델
        test_data (pd.DataFrame): 평가용 데이터
    """
    device = get_device()
    model.eval()  # 모델을 평가 모드로 설정

    # 기울기 계산을 비활성화하여 메모리 사용량과 계산 속도를 최적화합니다.
    with torch.no_grad():
        test_users = torch.LongTensor(test_data['user_idx'].values).to(device)
        test_items = torch.LongTensor(test_data['movie_idx'].values).to(device)
        
        predicted_tensor = model(test_users, test_items)

    predicted = predicted_tensor.detach().cpu().numpy()
    actual = test_data['rating'].values

    # RMSE와 MAE 계산
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    mae = mean_absolute_error(actual, predicted)

    print("\n--- Model Evaluation ---")
    print(f"RMSE (평균 제곱근 오차): {rmse:.4f}")
    print(f"MAE (평균 절대 오차): {mae:.4f}")
    print("------------------------")
    return rmse, mae
