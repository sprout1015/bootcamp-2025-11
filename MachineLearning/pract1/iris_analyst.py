from sklearn.datasets import load_iris

## 함수 클래스

if __name__ == '__main__':
    iris = load_iris();
    print(iris.data)
        # 행렬 - 차원은 4개 ','로 나누지 않는 이유?
        # 계산해야하니 내부에 따로 Key값은 없는 Array 구조
        # [[5.1 3.5 1.4 0.2]
        #  [4.9 3.  1.4 0.2]..
    print(iris.keys())
        # target - 라벨(분류), feature - 차원
        # dict_keys(['data', 'target', 'frame', 'target_names', 'DESCR', 'feature_names', 'filename', 'data_module'])
    print(iris.data.shape)
    # 데이터 구조 파악용
        # (150, 4) - 튜블 구조(불변 immutable)
        # axios 0번 자리 - 데이터 150개(행개수), 현실적인 데이터를 가장 먼저 보여줘서 실 데이터 개수가 앞
        # axios 1번 자리 - 차원 4개(필드개수)
    print(iris.feature_names)
        # 각 필드 이름 (차원 이름)
        # ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']
    print(iris.target_names)
        # 라벨링된 대상들

    # 행렬은 보통 대문자로 명명
    X = iris.data
    # 행렬 계산은 @로 진행
        # 해당 계산 결과는 공분산
    Cov = X.T @ X
        # 4 X 4로 나옴 - 차원이 4개니까
        #   'sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)'
        # 'sepal length (cm)'   [[5223.85 2673.43 3483.76 1128.14]
        # 'sepal width (cm)'    [2673.43 1430.4  1674.3   531.89]
        # 'petal length (cm)'   [3483.76 1674.3  2582.71  869.11]
        # 'petal width (cm)'    [1128.14  531.89  869.11  302.33]]
    print(Cov)