# numpy는 숫자 계산, 특히 행렬과 같은 배열 계산을 쉽게 하도록 도와주는 라이브러리입니다. 'np'라는 별칭으로 주로 사용합니다.
import numpy as np
# pandas는 표(테이블) 형태의 데이터를 다루는 데 특화된 라이브러리입니다. 'pd'라는 별칭으로 사용합니다.
import pandas as pd
# matplotlib는 데이터를 그래프로 시각화해주는 라이브러리입니다. 'plt'라는 별칭으로 사용합니다.
import matplotlib.pyplot as plt


# 키와 몸무게 데이터를 받아서 그래프(산점도)로 시각화하는 함수입니다.
def visualize_height_weight(df):
    # 그래프의 크기를 가로 7, 세로 7인치로 설정합니다.
    plt.figure(figsize=(7, 7))
    # 산점도를 그립니다. x축은 몸무게, y축은 키로 설정합니다. alpha는 점의 투명도입니다.
    plt.scatter(df["Weight(Pounds)"], df["Height(Inches)"], alpha=0.7)
    # x축과 y축에 라벨을 추가하여 그래프의 의미를 명확히 합니다.
    plt.xlabel("Weight (Pounds)")
    plt.ylabel("Height (Inches)")
    # 그래프의 제목을 설정합니다.
    plt.title("Height vs Weight")

    # 현재 사용 중인 그래프의 축(axis) 정보를 가져옵니다.
    ax = plt.gca()

    # --- 그래프를 더 보기 좋게 꾸미는 과정 ---
    # 데이터의 최소/최대값을 계산하여 그래프의 표시 범위를 자동으로 조절합니다.
    x_min, x_max = df["Weight(Pounds)"].min(), df["Weight(Pounds)"].max()
    y_min, y_max = df["Height(Inches)"].min(), df["Height(Inches)"].max()

    # 데이터가 그래프 경계에 너무 붙어있지 않도록 10%의 여유 공간을 줍니다.
    x_margin = (x_max - x_min) * 0.1
    y_margin = (y_max - y_min) * 0.1

    # 계산된 여유 공간을 적용하여 x축과 y축의 표시 범위를 설정합니다.
    ax.set_xlim(x_min - x_margin, x_max + x_margin)
    ax.set_ylim(y_min - y_margin, y_max + y_margin)

    # 🔥 그래프의 눈금(grid) 간격을 설정합니다.
    # arange 함수는 특정 간격으로 숫자 리스트를 만듭니다. (시작, 끝, 간격)
    # 몸무게는 20 단위로, 키는 2 단위로 눈금을 표시하도록 설정합니다.
    x_ticks = np.arange(int(x_min) - 20, int(x_max) + 20, 20)
    y_ticks = np.arange(int(y_min) - 5, int(y_max) + 5, 2)

    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)

    # 그래프에 격자(grid)를 표시하여 값을 읽기 쉽게 합니다.
    ax.grid(True, linestyle='--', linewidth=0.7, alpha=0.7)

    # 🔥 x축과 y축의 비율을 동일하게 맞춥니다.
    # 이렇게 하면 데이터의 실제 분포 왜곡 없이 시각화할 수 있습니다.
    # 예를 들어, 이 옵션이 없으면 키와 몸무게의 변화량이 시각적으로 다르게 보일 수 있습니다.
    ax.set_aspect("equal", adjustable="box")

    # 설정이 완료된 그래프를 화면에 보여줍니다.
    plt.show()


# 데이터의 고유값(eigenvalues)과 고유벡터(eigenvectors)를 계산하는 함수입니다.
# 고유값/고유벡터는 데이터가 어떤 방향으로 가장 크게 분산(퍼져 있는지)되어 있는지를 나타내는 지표입니다.
def eigen_values_vectors(df):
    # 분석할 '몸무게'와 '키' 데이터를 numpy 배열(행렬) 형태로 변환합니다.
    X = df[["Weight(Pounds)", "Height(Inches)"]].to_numpy()
    
    # 공분산 행렬을 계산합니다. 공분산은 두 변수(여기서는 키와 몸무게)가 함께 어떻게 변하는지를 나타내는 값입니다.
    # X.T는 행렬의 행과 열을 바꾸는 '전치'를 의미하며, np.cov는 공분산 계산 함수입니다.
    cov_pivot = np.cov(X.T)
    
    # numpy의 선형대수(linalg) 라이브러리를 사용해 공분산 행렬의 고유값과 고유벡터를 계산합니다.
    return np.linalg.eig(cov_pivot)


# 이 파일이 직접 실행될 때만 아래 코드가 동작합니다.
if __name__ == "__main__":
    # --- 데이터 로딩 부분 (현재는 주석 처리되어 실행되지 않음) ---
    # filename = "data/SOCR-HeightWeight.csv"
    # df = pd.read_csv(filename)
    
    # --- 몸무게가 150 이상인 데이터만 필터링하는 예제 (역시 주석 처리됨) ---
    # table = df[df["Weight(Pounds)"] >= 150]
    # print(table)

    # --- 현재 실행을 중단시키는 테스트 코드 ---
    # 아래 코드는 리스트에 특정 값이 있는지 확인하고, 프로그램을 즉시 종료시킵니다.
    # 따라서 이 아래에 있는 그래프 시각화나 고유값 계산 코드는 실행되지 않습니다.
    # 이 부분을 지우거나 주석 처리해야 전체 코드가 동작합니다.
    lists = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    Tf = 11 in lists
    print(Tf) # 11은 lists 안에 없으므로 False가 출력됩니다.
    exit() # 여기서 프로그램이 강제 종료됩니다.
    
    # --- 아래 코드는 위의 exit() 때문에 현재 실행되지 않는 부분입니다. ---
    
    # 데이터프레임(df)을 사용해 위에서 만든 시각화 함수를 호출합니다.
    visualize_height_weight(df)

    # 고유값과 고유벡터를 계산하고 결과를 출력합니다.
    eigen_values, eigenvectors = eigen_values_vectors(df)
    print("Eigenvalues(고유값):\n", eigen_values)
    print("Eigenvectors(고유벡터):\n", eigenvectors)