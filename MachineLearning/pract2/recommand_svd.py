# pickle은 파이썬 객체(변수, 데이터 등)를 파일로 저장하거나 불러올 때 사용하는 라이브러리입니다.
import pickle
# 데이터 분석의 필수 라이브러리 pandas와 numpy를 불러옵니다.
import pandas as pd
import numpy as np

# scikit-learn 라이브러리에서 필요한 기능들을 가져옵니다.
from sklearn.decomposition import TruncatedSVD  # SVD 모델
from sklearn.model_selection import train_test_split  # 데이터 분리 도구
from sklearn.metrics import mean_squared_error, mean_absolute_error  # 모델 성능 평가 도구


# 추천 모델링에 사용할 데이터를 추출하고 정제하는 함수입니다.
def extract_data(df, min_rating=4.0, customer_count=100):
    """
    Args:
        df (pd.DataFrame): 원본 평점 데이터프레임
        min_rating (float, optional): 분석에 포함할 최소 평점. Defaults to 4.0.
        customer_count (int, optional): 분석에 포함할 상위 유저 수. Defaults to 100.

    Returns:
        pd.DataFrame: 정제된 데이터프레임
    """
    # 평점을 가장 많이 남긴 상위 'customer_count'명의 유저 목록을 추출합니다.
    users = df["user_id"].value_counts().reset_index().iloc[:customer_count, :]
    
    # 원본 데이터에서 아래 두 조건을 만족하는 데이터만 필터링합니다.
    data = df[(df['user_id'].isin(users['user_id'])) & (df['rating']>=min_rating)]

    return data

# SVD를 이용해 평점을 예측하는 모델 함수
def svd_predict_model(filtered_data, degree=12):
    """
    SVD를 사용하여 사용자-영화 평점 행렬을 분해하고 다시 복원하여,
    평점이 비어있던 영화들의 평점을 예측합니다.

    Args:
        filtered_data (pd.DataFrame): 분석할 사용자와 영화 평점 데이터
        degree (int, optional): SVD에서 사용할 잠재 요인(Latent Factor)의 수. Defaults to 12.
            이 값은 모델이 사용자-영화 관계를 분석할 때 참고할 '주요 특징'의 개수를 의미합니다.
            예를 들어, 영화를 '액션성', '코미디성' 등 몇 개의 보이지 않는 요인으로 분해해 분석할지 결정합니다.
            적절한 값은 실험을 통해 찾으며, 너무 크거나 작으면 예측 성능이 저하될 수 있습니다.
    """
    # 1. 사용자-영화 평점 행렬(피벗 테이블) 생성
    pivot_df = filtered_data.pivot_table(index="user_id", columns="movie_id", values="rating")

    user_ids = pivot_df.index
    movie_ids = pivot_df.columns

    # 2. 결측치(NaN) 처리: 사용자가 평점을 매기지 않은 영화는 각 영화의 평균 평점으로 채웁니다.
    means = pivot_df.mean(axis=0)
    pivot_df_filled = pivot_df.fillna(means)

    # 3. SVD 모델 생성, 학습, 복원
    svd = TruncatedSVD(n_components=degree)
    transformed_matrix = svd.fit_transform(pivot_df_filled)
    predicted_rating_matrix = svd.inverse_transform(transformed_matrix)
    
    predicted_df = pd.DataFrame(predicted_rating_matrix, index=user_ids, columns=movie_ids)

    # 4. 예측 결과를 보기 좋은 형태로 변환 (Unpivot)
    unpivot_df = predicted_df.stack().reset_index()
    unpivot_df.columns = ['user_id', 'movie_id', 'predicted_rating']
    
    return unpivot_df

# 모델의 성능을 평가하는 함수
def performance_metrics(data, test_size=0.2, random_state=42):
    """
    SVD 모델의 예측 성능을 RMSE와 MAE로 평가합니다.

    Args:
        data (pd.DataFrame): 평가할 전체 데이터
        test_size (float, optional): 테스트 데이터로 사용할 비율. Defaults to 0.2.
            모델의 성능을 공정하게 평가하기 위해, 전체 데이터 중 평가에만 사용할 데이터의 비율을 정합니다.
            8:2 (test_size=0.2) 또는 7:3 (test_size=0.3) 비율이 일반적으로 사용됩니다.
        random_state (int, optional): 데이터 분리 시 재현성을 위한 시드값. Defaults to 42.
            데이터를 무작위로 나눌 때, 이 값을 고정하면 언제나 동일한 방식으로 데이터가 나뉩니다.
            이를 통해 코드를 실행할 때마다 동일한 결과를 얻을 수 있어('재현성'), 모델 개선 작업을 용이하게 합니다.
            숫자 자체는 의미가 없으며, 어떤 정수든 고정된 값을 사용하면 됩니다.

    Returns:
        tuple: (RMSE, MAE) 성능 지표
    """
    # 1. 데이터 분리: 모델 학습용(train)과 평가용(test)으로 데이터를 나눕니다.
    train_data, test_data = train_test_split(data, test_size=test_size, random_state=random_state)
    
    # 2. 모델 학습 및 예측: '학습용' 데이터만으로 SVD 모델을 학습시키고 예측을 수행합니다.
    predict_df = svd_predict_model(train_data)

    # 3. 결과 비교: 모델의 예측값(predict_df)과 실제 정답(test_data)을 합쳐서 비교 준비를 합니다.
    comparison_df = pd.merge(predict_df, test_data, on=["movie_id", "user_id"], how="inner")
    
    actual_ratings = comparison_df['rating']  # 실제 평점
    predicted_ratings = comparison_df['predicted_rating']  # 모델이 예측한 평점

    # 4. 성능 지표 계산
    # RMSE (Root Mean Squared Error): 오차의 제곱에 대한 평균의 제곱근. 큰 오차에 더 큰 페널티를 부여합니다.
    rmse = np.sqrt(mean_squared_error(actual_ratings, predicted_ratings))
    
    # MAE (Mean Absolute Error): 오차의 절대값에 대한 평균. 오차의 크기를 직관적으로 파악하기 좋습니다.
    mae = mean_absolute_error(actual_ratings, predicted_ratings)
    
    return rmse, mae

# 이 파일이 직접 실행될 때만 아래 코드가 동작합니다.
if __name__ == '__main__':
    # pickle 파일로 저장된 평점 데이터('ratings.pkl')를 불러옵니다.
    df = pd.read_pickle('data/ratings.pkl')
    
    # 분석할 데이터 추출 (상위 100명의 유저, 4점 이상 평점)
    data = extract_data(df)

    # 모델의 성능을 평가하고 결과를 받아옵니다.
    rmse_score, mae_score = performance_metrics(data)
    
    print(f"모델 성능 평가 결과 (RMSE): {rmse_score:.4f}")
    print(f"모델 성능 평가 결과 (MAE): {mae_score:.4f}")

    # RMSE, MAE는 0에 가까울수록 모델의 예측이 정확하다는 의미입니다.
    # MAE가 0.33이라면, 모델의 예측이 실제 평점과 평균적으로 약 0.33점 정도 차이난다고 해석할 수 있습니다.
    # RMSE가 MAE보다 약간 더 큰 경향이 있는데, 이는 모델이 가끔씩 실제값과 차이가 큰 예측(큰 오차)을 만들고 있기 때문입니다.
