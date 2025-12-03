# src/model.py

import torch
from torch import nn

class MatrixFactorization(nn.Module):
    """
    Matrix Factorization 모델 정의
    사용자-아이템 평점 행렬을 두 개의 저차원 행렬(사용자, 아이템 잠재 요인)로 분해합니다.
    """
    def __init__(self, n_users, n_items, embedding_dim):
        """
        Args:
            n_users (int): 총 사용자 수
            n_items (int): 총 아이템 수
            embedding_dim (int): 잠재 요인 벡터의 차원
        """
        super(MatrixFactorization, self).__init__()
        self.users_embedding = nn.Embedding(n_users, embedding_dim)
        self.items_embedding = nn.Embedding(n_items, embedding_dim)

        # 가중치를 작은 랜덤 값으로 초기화하여 안정적인 학습을 돕습니다.
        self.users_embedding.weight.data.uniform_(0, 0.05)
        self.items_embedding.weight.data.uniform_(0, 0.05)

    def forward(self, users, items):
        """
        모델의 순전파 로직. 사용자 벡터와 아이템 벡터의 내적을 통해 평점을 예측합니다.
        
        Args:
            users (torch.Tensor): 사용자 ID 텐서
            items (torch.Tensor): 아이템 ID 텐서
            
        Returns:
            torch.Tensor: 예측된 평점 텐서
        """
        user_vector = self.users_embedding(users)
        item_vector = self.items_embedding(items)
        # 두 잠재 요인 벡터의 내적(dot product) 계산
        predicted_rating = (user_vector * item_vector).sum(1)
        return predicted_rating
