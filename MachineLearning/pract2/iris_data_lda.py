# 데이터 분석 및 시각화에 필요한 라이브러리들을 불러옵니다.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# scikit-learn 라이브러리에서 필요한 기능들을 가져옵니다.
from sklearn.datasets import load_iris  # 붓꽃 예제 데이터
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA  # 선형 판별 분석(LDA) 모델
from sklearn.preprocessing import StandardScaler  # 데이터 표준화(정규화) 도구


# 이 파일이 직접 실행될 때만 아래 코드가 동작합니다.
if __name__ == '__main__':
    # 붓꽃 데이터를 불러옵니다.
    iris = load_iris()
    X = iris.data  # 측정 데이터 (입력값, 특징)
    y = iris.target  # 붓꽃의 품종 정보 (결과값, 레이블) -> LDA는 이 품종 정보를 사용합니다.

    # --- 데이터 전처리: 표준화(Standardization) ---
    # 각 특징(꽃받침 길이, 꽃잎 너비 등)들의 단위와 크기가 다르기 때문에,
    # 이를 평균 0, 표준편차 1을 갖는 표준 정규분포로 변환해주는 '표준화' 과정을 거칩니다.
    # 이렇게 하면 모든 특징이 동일한 스케일(척도)을 갖게 되어, 모델이 더 안정적으로 학습할 수 있습니다.
    X_normalized = StandardScaler().fit_transform(X)

    # --- LDA 모델 적용 ---
    # LDA 모델을 생성합니다. n_components=2는 데이터를 2차원으로 축소하겠다는 의미입니다.
    lda = LDA(n_components=2)
    
    # fit_transform 함수는 모델을 데이터에 학습(fit)시키고, 그 학습 결과에 따라 데이터를 변환(transform)하는 것을 동시에 수행합니다.
    # LDA는 y, 즉 품종 정보를 함께 사용해서 '어떻게 하면 품종들을 가장 잘 나눌 수 있을까?'를 학습합니다.
    # 그 학습 결과로 X_normalized 데이터를 2차원 데이터(X_lda)로 변환합니다.
    X_lda = lda.fit_transform(X_normalized, y)

    # --- 결과 시각화 ---
    # 그래프 크기를 가로 5, 세로 5로 설정합니다.
    plt.figure(figsize=(5, 5))
    
    # 2차원으로 축소된 데이터(X_lda)를 사용해 산점도를 그립니다.
    # x축은 LDA로 찾은 첫 번째 축(성분), y축은 두 번째 축(성분)입니다.
    # c=y 옵션은 각 점의 색깔을 붓꽃의 품종(y)에 따라 다르게 칠하라는 의미입니다.
    # cmap='viridis'는 사용할 색상 팔레트를 지정합니다.
    plt.scatter(X_lda[:, 0], X_lda[:, 1], c=y, cmap='viridis', edgecolor='k', s=100)
    
    # 그래프의 x축, y축, 제목을 설정합니다.
    plt.xlabel("First Linear Discriminant Component (첫 번째 LDA 축)")
    plt.ylabel("Second Linear Discriminant Component (두 번째 LDA 축)")
    plt.title("LDA on Iris dataset (붓꽃 데이터 LDA 결과)")
    
    # 완성된 그래프를 화면에 보여줍니다.
    plt.show()

# 이 그래프를 보면, 원래 4차원이었던 데이터가 2차원으로 축소되었음에도 불구하고,
# 세 종류의 붓꽃 품종이 색깔별로 잘 구분되어 뭉쳐있는 것을 확인할 수 있습니다.
# 이것이 LDA가 '분류'에 유리한 차원 축소를 수행한다는 의미입니다.
