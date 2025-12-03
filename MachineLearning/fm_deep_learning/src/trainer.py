# src/trainer.py

import os
import torch
from tqdm import tqdm
from src.evaluator import evaluate, get_device

class Trainer:
    """
    모델 학습 과정을 관리하는 클래스
    """
    def __init__(self, model, config, user_id_map, item_id_map):
        self.model = model
        self.config = config
        self.user_id_map = user_id_map
        self.item_id_map = item_id_map
        
        self.device = get_device()
        self.model.to(self.device)
        print(f"PyTorch device check: Using {str(self.device).upper()}")
        
        # 손실 함수와 옵티마이저 정의
        self.loss_fn = torch.nn.MSELoss()
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.config.LEARNING_RATE)

    def train(self, train_loader, test_data):
        """
        주어진 데이터로 모델 학습을 실행합니다.
        """
        print("--- Start Training ---")
        for epoch in range(self.config.EPOCHS):
            self.model.train()  # 학습 모드
            total_loss = 0.0

            # tqdm을 사용한 미니배치 학습 루프
            batch_iterator = tqdm(train_loader, desc=f"Epoch {epoch + 1}/{self.config.EPOCHS}", leave=True)

            for user, item, rating in batch_iterator:
                user, item, rating = user.to(self.device), item.to(self.device), rating.float().to(self.device)

                self.optimizer.zero_grad()
                predicted = self.model(user, item)
                loss = self.loss_fn(predicted, rating)
                loss.backward()
                self.optimizer.step()

                total_loss += loss.item()
                batch_iterator.set_postfix(loss=loss.item())

            avg_loss = total_loss / len(train_loader)
            print(f"Epoch [{epoch + 1}/{self.config.EPOCHS}] - Average Loss: {avg_loss:.4f}")

        print("--- Training Finished ---")
        
        # 학습 완료 후 평가 및 모델 저장
        evaluate(self.model, test_data)
        self._save_model()

    def _save_model(self):
        """
        학습된 모델의 가중치와 메타데이터를 저장합니다.
        """
        model_dir = os.path.dirname(self.config.MODEL_PATH)
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)

        torch.save({
            "model_state_dict": self.model.state_dict(),
            "user_id_map": self.user_id_map,
            "item_id_map": self.item_id_map,
            "embedding_dimension": self.config.VECTOR_DIMENSION,
        }, self.config.MODEL_PATH)
        
        print(f"\nModel saved successfully -> {self.config.MODEL_PATH}")
