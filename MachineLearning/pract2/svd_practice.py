import numpy as np
import pandas as pd
import pickle
from sklearn.decomposition import TruncatedSVD
# scipy.sparse.linalg.svds는 대규모 희소 행렬에 사용하기 좋은 SVD 함수입니다.
from scipy.sparse.linalg import svds
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler

# --- 💡 1단계: 원본 데이터 가공 (최초 1회만 실행) ---
# 이 블록은 원본 데이터 파일('ratings.dat')을 읽어서,
# 분석에 필요한 형태로 가공한 후 'ratings.pkl' 파일로 저장하는 과정입니다.
# 한 번 실행해서 .pkl 파일을 만들었다면, 그 다음부터는 주석 처리하고 .pkl 파일을 바로 읽어 사용합니다.
"""
# 데이터 파일은 '::' 기호로 구분되어 있으므로, sep='::' 옵션을 줍니다.
df = pd.read_csv('data/ratings.dat', sep='::', engine='python')
# 열(column) 이름을 지정해줍니다.
df.columns = ['user_id', 'movie_id', 'rating', 'timestamp']
# 분석에 사용하지 않을 'timestamp' 열을 삭제합니다.
df.drop(columns=['timestamp'], inplace=True)
# 가공이 끝난 데이터를 'ratings.pkl' 파일로 저장합니다. pickle은 csv보다 훨씬 빠르게 읽고 쓸 수 있습니다.
df.to_pickle('data/ratings.pkl')
"""

# --- 💡 2단계: 피벗 테이블 생성 (최초 1회만 실행) ---
# 이 블록은 위에서 만든 'ratings.pkl'을 읽어서, SVD에 사용할
# '사용자-영화 평점 행렬(피벗 테이블)'을 만들고 'ratings_pivot.pkl'로 저장하는 과정입니다.
"""
df = pd.read_pickle('data/ratings.pkl')
# 활발한 사용자 200명, 평점 4점 이상을 준 데이터만 필터링합니다. (계산량 감소 목적)
users = df["user_id"].value_counts().reset_index().iloc[:200, :]
data = df[(df['user_id'].isin(users['user_id'])) & (df['rating']>=4)]
# pivot_table 함수로 '사용자-영화 평점 행렬'을 만듭니다.
# index(행)는 user_id, columns(열)은 movie_id, values(내용)는 rating이 됩니다.
pivot_df = pd.pivot_table(data, index='user_id', columns='movie_id', values='rating', aggfunc='mean')
# 완성된 피벗 테이블을 저장합니다.
pivot_df.to_pickle("data/ratings_pivot.pkl")
"""

# --- 💡 3단계: 결측치(NaN) 처리 (최초 1회만 실행) ---
# SVD를 적용하려면 행렬에 비어있는 값(NaN)이 없어야 합니다.
# 이 블록은 피벗 테이블의 비어있는 값들을 각 영화(열)의 평균 평점으로 채워넣는 과정입니다.
"""
df = pd.read_pickle('data/ratings_pivot.pkl')
# 각 영화(열, axis=0)의 평균 평점을 계산합니다.
means = df.mean(axis=0)
# fillna 함수로 비어있는 값을 위에서 구한 평균값으로 채웁니다.
df.fillna(means, inplace=True)
# 최종적으로 SVD에 사용할 준비가 된 행렬을 저장합니다.
df.to_pickle('data/ratings_pivot_means.pkl')
"""

# --- 💡 SVD 원리 탐구 (학습용 코드) ---
# 이 블록은 붓꽃(iris) 데이터를 이용해 SVD의 수학적 원리를 탐구하는 실험입니다.
# 데이터 행렬 X에 대해, X.T @ X 와 X @ X.T의 고유값(eigenvalues)이
# X의 특이값(singular values)과 어떤 관계가 있는지 확인하는 과정입니다.
# 지금 당장 이해하기는 어려울 수 있지만, SVD가 행렬의 공분산과 깊은 관련이 있다는 것을 보여줍니다.
"""
if __name__ == "__main__":
    iris = load_iris()
    X = iris.data
    X_scaled = StandardScaler().fit_transform(X) # 데이터 표준화
    X_col_cov = X_scaled.T @ X_scaled # 특징(column) 기준 공분산 행렬
    X_row_cov = X_scaled @ X_scaled.T # 데이터(row) 기준 공분산 행렬
    col_eigenvalues, _ = np.linalg.eig(X_col_cov)
    row_eigenvalues, _ = np.linalg.eig(X_row_cov)
    # 두 공분산 행렬에서 계산된 0이 아닌 고유값의 개수가 동일하며,
    # 이는 데이터의 실제 차원(또는 랭크)과 관련이 있음을 알 수 있습니다.
    print(sorted(col_eigenvalues, reverse=True))
    print(sorted(row_eigenvalues, reverse=True)[:4])
"""


# --- 💡 4단계: SVD를 이용한 평점 예측 (실행되는 메인 코드) ---
if __name__ == "__main__":
    # 위 1~3단계를 통해 최종적으로 준비된 '사용자-영화 평점 행렬'을 불러옵니다.
    X = pd.read_pickle('data/ratings_pivot_means.pkl').values
    
    # --- 방법 1: scikit-learn의 TruncatedSVD 사용 ---
    # TruncatedSVD는 원본 행렬을 n_components 만큼의 차원으로 축소시켜 줍니다.
    svd = TruncatedSVD(n_components=2)
    A_reduced = svd.fit_transform(X)
    print("scikit-learn의 TruncatedSVD 결과 (축소된 행렬의 크기):")
    print(A_reduced.shape) # (원본 행 수, n_components)
    print("-" * 30)

    # --- 방법 2: scipy의 svds 사용 ---
    # svds는 특이값(S), 특이벡터(U, VT)를 직접 반환하며, k는 상위 몇 개의 특이값을 가져올지 지정합니다.
    # k가 작을수록 원본 행렬을 더 많이 '압축'하고 '단순화'하는 효과가 있습니다.
    U, S, VT = svds(X, k=5)
    
    # S는 특이값들을 1차원 배열로 반환하므로, 행렬 곱셈을 위해 대각 행렬 형태로 변환해줍니다.
    D = np.diag(S)
    
    # --- 핵심: 분해된 행렬들을 다시 곱해서 원본 행렬을 '복원'합니다. ---
    # U @ D @ VT  (참고: @는 행렬 곱셈 연산자)
    # 이 과정이 바로 '평점 예측'에 해당합니다.
    # 원본 행렬의 일부 정보(작은 특이값들)를 의도적으로 버리고 복원했기 때문에,
    # 복원된 행렬 X_new_ratings는 원본과 완전히 같지 않습니다.
    # 비어있던(NaN을 평균으로 채웠던) 부분들이 SVD에 의해 '예측된 평점'으로 채워진 새로운 행렬이 됩니다.
    X_new_ratings = U @ D @ VT
    
    print("SVD로 복원된 예측 평점 행렬:")
    print(X_new_ratings)