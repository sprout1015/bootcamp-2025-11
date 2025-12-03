# train.py

from src.data_loader import prepare_dataloaders
from src.model import MatrixFactorization
from src.trainer import Trainer
import src.config as config

def main():
    """
    전체 모델 학습 파이프라인을 실행합니다.
    """
    # 1. 데이터 준비
    train_loader, test_data, user_id_map, item_id_map = prepare_dataloaders(
        data_path=config.DATA_PATH,
        min_rating=config.MIN_RATING,
        user_count=config.USER_COUNT,
        batch_size=config.BATCH_SIZE,
        test_size=config.TEST_SIZE,
        random_state=config.RANDOM_STATE
    )

    # 2. 모델 초기화
    n_users = len(user_id_map)
    n_items = len(item_id_map)
    model = MatrixFactorization(n_users, n_items, config.VECTOR_DIMENSION)

    # 3. 트레이너 초기화 및 학습 시작
    trainer = Trainer(model, config, user_id_map, item_id_map)
    trainer.train(train_loader, test_data)


if __name__ == "__main__":
    main()
