# src/config.py

# === 데이터 관련 경로 ===
DATA_PATH = "./data/ratings.pkl"
MODEL_PATH = "./model/fm_model.pt"

# === 데이터 전처리 파라미터 ===
MIN_RATING = 4.0
USER_COUNT = 500

# === 모델 하이퍼파라미터 ===
VECTOR_DIMENSION = 64
EPOCHS = 10
LEARNING_RATE = 0.001
BATCH_SIZE = 64
TEST_SIZE = 0.2
RANDOM_STATE = 42
