# 데이터 분석 및 시각화에 필요한 라이브러리들을 불러옵니다.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# scikit-learn 라이브러리에서 필요한 기능들을 가져옵니다.
from sklearn.datasets import load_iris  # 붓꽃 예제 데이터
from sklearn.decomposition import PCA  # 주성분 분석(PCA) 모델
from sklearn.preprocessing import StandardScaler  # 데이터 표준화(정규화) 도구


# 이 파일이 직접 실행될 때만 아래 코드가 동작합니다.
if __name__ == '__main__':
    # 붓꽃 데이터를 불러옵니다.
    iris = load_iris()
    X = iris.data  # 측정 데이터 (입력값, 특징)
    y = iris.target  # 붓꽃의 품종 정보 (결과값, 레이블). PCA는 이 정보를 사용하지 않지만, 시각화 때 색상 구분을 위해 사용합니다.

    # --- 데이터 전처리: 표준화(Standardization) ---
    # PCA는 데이터의 분산(퍼짐 정도)에 매우 민감합니다.
    # 특정 특징(feature)의 숫자 크기가 다른 특징보다 월등히 크면, 그 특징이 분산을 지배하게 되어 분석이 왜곡될 수 있습니다.
    # 따라서, 모든 특징을 동일한 척도(평균 0, 표준편차 1)로 맞춰주는 '표준화'가 거의 필수적입니다.
    X_normalized = StandardScaler().fit_transform(X)

    # --- PCA 모델 적용 ---
    # PCA 모델을 생성합니다. n_components=2는 데이터를 2차원으로 축소하겠다는 의미입니다.
    # 즉, 원래 4개였던 특징(꽃받침 길이/너비, 꽃잎 길이/너비)을 가장 중요한 2개의 새로운 특징으로 압축합니다.
    pca = PCA(n_components=2)
    
    # fit_transform 함수로 PCA를 적용합니다.
    # ❗️ 중요: LDA와 달리, fit_transform에 품종 정보인 y가 들어가지 않습니다.
    # PCA는 오직 데이터(X_normalized)의 분포(분산)만을 보고, 데이터의 구조를 가장 잘 설명하는 새로운 축(주성분)을 찾습니다.
    # 이렇게 데이터 자체의 특성만으로 학습하는 방식을 '비지도 학습(Unsupervised Learning)'이라고 합니다.
    X_pca = pca.fit_transform(X_normalized)

    # --- 결과 시각화 ---
    # 그래프 크기를 가로 5, 세로 5로 설정합니다.
    plt.figure(figsize=(5, 5))
    
    # 2차원으로 축소된 데이터(X_pca)를 사용해 산점도를 그립니다.
    # x축은 첫 번째 주성분(PC1), y축은 두 번째 주성분(PC2)입니다.
    # c=y 옵션은 각 점의 색깔을 붓꽃의 품종(y)에 따라 다르게 칠해, PCA가 품종 정보를 사용하지 않았음에도
    # 결과적으로 품종들이 잘 나뉘었는지 시각적으로 확인하기 위해 사용됩니다.
    plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y, cmap='viridis', edgecolor='k', s=100)
    
    # 그래프의 x축, y축, 제목을 설정합니다.
    plt.xlabel("First Principal Component (첫 번째 주성분)")
    plt.ylabel("Second Principal Component (두 번째 주성분)")
    plt.title("PCA on Iris dataset (붓꽃 데이터 PCA 결과)")
    
    # 완성된 그래프를 화면에 보여줍니다.
    plt.show()

# LDA 결과와 비교해보면, PCA도 품종들을 어느 정도 잘 분리해내지만,
# LDA만큼 각 품종의 경계가 명확하게 나누어지지는 않을 수 있습니다.
# 이는 PCA의 목적이 '분류'가 아니라 '분산의 최대화'이기 때문입니다.