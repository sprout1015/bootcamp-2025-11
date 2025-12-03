# analyze_data.py

import pandas as pd
import os

# 데이터 파일 경로 설정
DATA_PATH = "./data/ratings.pkl"

def analyze_ratings_data():
    """
    `ratings.pkl` 파일의 내용을 로드하고 분석하여 주요 통계를 출력합니다.
    """
    print("--- 📊 ratings.pkl 데이터 분석 시작 ---")

    if not os.path.exists(DATA_PATH):
        print(f"❌ 오류: 데이터 파일 '{DATA_PATH}'을(를) 찾을 수 없습니다.")
        print("데이터 파일이 올바른 경로에 있는지 확인해주세요.")
        return

    try:
        # 1. 데이터 로드
        df = pd.read_pickle(DATA_PATH)
        print(f"\n✅ 데이터 파일 '{DATA_PATH}' 로드 성공.")
        print(f"총 데이터 개수: {len(df)}개")

        # 2. 데이터 미리보기 (상위 5개 행)
        print("\n--- 데이터 미리보기 (df.head()) ---")
        print(df.head())

        # 3. 데이터 정보 확인 (컬럼, 데이터 타입, 결측치 등)
        print("\n--- 데이터 정보 (df.info()) ---")
        df.info()

        # 4. 기술 통계 확인 (숫자형 컬럼의 평균, 표준편차, 최소/최대 등)
        print("\n--- 기술 통계 (df.describe()) ---")
        print(df.describe())

        # 5. 고유 사용자 및 영화 수 확인
        unique_users = df['user_id'].nunique()
        unique_movies = df['movie_id'].nunique()
        print(f"\n--- 고유 ID 정보 ---")
        print(f"고유 사용자(user_id) 수: {unique_users}명")
        print(f"고유 영화(movie_id) 수: {unique_movies}개")

        # 6. 평점 분포 확인
        print(f"\n--- 평점 분포 (rating.value_counts())")
        print(df['rating'].value_counts().sort_index())

        print("\n--- 📊 데이터 분석 완료 ---")

    except Exception as e:
        print(f"❌ 데이터 분석 중 오류 발생: {e}")

if __name__ == "__main__":
    analyze_ratings_data()
