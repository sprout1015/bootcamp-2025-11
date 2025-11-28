import pandas as pd
import numpy as np
import matplotlib.pyplot as pyplot

X_Label = "Height(Inches)"
Y_Label = "Weight(Pounds)"

# 데이터 비주얼라이징
def visualize_height_weight(df):
    pyplot.figure(figsize=(5,5))
    # 데이터 라벨(Key) 맞추기
    pyplot.scatter(df[X_Label], df[Y_Label])
    pyplot.ylabel("Height")
    pyplot.ylabel("Weight")
    pyplot.show()


def eigen_values_vectors(df):
    # 데이터프레임에서 키(Key)로 지정한 'Height(Inches)', 'Weight(Pounds)' 열만 추출하여 넘파이 배열로 변환
    X = df[[X_Label, Y_Label]].to_numpy()

    # 공분산 행렬(covariance matrix) 계산 (X.T는 전치행렬로 각 변수 기준으로 계산)
    cov_pivot = np.cov(X.T)

    # 공분산 행렬에 대해 고유값(eigenvalues)과 고유벡터(eigenvectors) 계산
    # 고유값: 데이터 분산의 크기, 고유벡터: 분산이 가장 큰 방향(주성분)
    eigen_values, eigen_vectors = np.linalg.eig(cov_pivot)

    # 계산된 고유값과 고유벡터 반환
    return eigen_values, eigen_vectors

if __name__ == "__main__":
    filename = "data/SOCR-HeightWeight.csv"
    df = pd.read_csv(filename)
    # 비주얼라이징
    visualize_height_weight(df)
    # Weight (Pounds)
    # ↑
    # |                                            ***********
    # |                                   **********************
    # |                           *****************************
    # |                       *********************************
    # |                   *************************************
    # |                *************************************
    # |              *************************************
    # |            *************************************
    # |         **********************************
    # |        **************************
    # |       ********************
    # |      *************
    # |     ****
    # |------------------------------------------------------------→ Height (Inches)

    # 고유값
    # [  2.68350923 136.90940491]
    print(eigen_values_vectors(df)[0]);
    #   Height-Weight 데이터의 고유값(새로운 축에서의 분산 크기) 2개
        #   → 작은 축의 분산: 2.68
        #   → 큰 축의 분산: 136.91 (주성분, 데이터 변동을 가장 많이 설명)

    # 고유벡터
    # [[-0.99651893 -0.08336679]
    #  [ 0.08336679 -0.99651893]]
    print(eigen_values_vectors(df)[1]);
    # 각 고유벡터는 데이터의 분산 방향(데이터의 중심에서 뻗는 방향)을 나타냄
        # 첫 번째 벡터 [-0.9965, 0.0833] ↔ 고유값 2.68에 대응 (작은 분산 방향, 대략 11시 방향)
            # → Height 성분(-0.9965)이 크므로 Height 축에 더 크게 영향을 받은 축
        # 두 번째 벡터 [-0.0833, -0.9965] ↔ 고유값 136.91에 대응 (큰 분산 방향, 주성분, 대략 7시 방향)
            # → Weight 성분(-0.9965)이 크므로 Weight 축에 더 크게 영향을 받은 축
        # 벡터 [a, b]는 중심점에서 (a, b) 좌표로 향하는 방향을 의미하며,
    #    PCA에서는 가장 큰 고유값에 대응하는 벡터(주성분)를 기준으로 데이터를 재구성함

    # 따라서 고유값과 고유벡터는 항상 쌍으로 묶어서 해석해야 함:
        # 고유값 2.68350923, 고유벡터 [-0.99651893  0.08336679] → Height 영향이 큰 축
        # 고유값 136.90940491, 고유벡터 [-0.08336679  -0.99651893] → Weight 영향이 큰 축 (주성분)