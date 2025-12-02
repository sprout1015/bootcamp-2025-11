# pandas 라이브러리를 불러옵니다. pandas는 데이터를 표(테이블) 형태로 다루기 쉽게 도와주는 도구입니다.
# 엑셀의 표를 파이썬으로 옮겨와서 더 강력한 기능을 사용한다고 생각하면 쉽습니다.
import pandas as pd

# 이 파이썬 파일이 직접 실행될 때만 아래 코드가 동작하도록 하는 파이썬의 관용적인 표현입니다.
# 다른 파일에서 이 파일을 불러와 사용할 때는 아래 코드가 실행되지 않아 안전합니다.
if __name__ == "__main__":
    # "data/amazon.csv" 파일을 읽어서 df 라는 변수(데이터 프레임)에 저장합니다.
    # df는 엑셀 시트처럼 생긴 데이터 표라고 생각할 수 있습니다.
    df = pd.read_csv("data/amazon.csv")

    # 'rating' 열(column)의 데이터 타입을 숫자로 바꿉니다.
    # 만약 숫자로 바꿀 수 없는 값이 있다면, 그 값은 'coerce' 옵션에 의해 비어있는 값(NaN)으로 처리됩니다.
    # 데이터 분석을 하려면 숫자 형태여야 계산이 가능하기 때문에 중요한 전처리 과정입니다.
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

    # 'user_name' 열의 값들을 쉼표(,)를 기준으로 나누어 리스트로 만듭니다.
    # "Kim,Lee,Park" 같은 문자열이 ["Kim", "Lee", "Park"] 같은 목록으로 바뀝니다.
    df["user_name"] = df["user_name"].astype(str).str.split(",")

    # 'explode' 함수는 리스트로 묶여있던 'user_name'을 여러 줄로 풀어주는 역할을 합니다.
    # 예를 들어, 한 줄에 ["Kim", "Lee"]가 있었다면, "Kim" 한 줄, "Lee" 한 줄로 분리됩니다.
    # 각 사용자의 개별적인 분석을 위해 필요한 과정입니다.
    df_explode = df.explode('user_name')

    # 'rating' 또는 'user_name'에 비어있는 값(NaN, Not a Number)이 있는 행(row)은 분석에 방해가 되므로 제거합니다.
    df_explode = df_explode.dropna(subset=['rating', 'user_name'])

    # 피벗 테이블을 생성합니다. 엑셀의 피벗 테이블 기능과 동일합니다.
    # 여기서는 각 사용자가 각 제품에 대해 매긴 평점의 '평균'을 표로 재구성합니다.
    pivot_table = pd.pivot_table(
        df_explode,
        values="rating",          # 표의 내용물은 'rating'(평점)으로 채웁니다.
        columns="product_name",   # 표의 가로축(열)은 'product_name'(제품명)이 됩니다.
        index="user_name",        # 표의 세로축(행)은 'user_name'(사용자명)이 됩니다.
        aggfunc="mean",           # 동일한 사용자가 동일한 제품에 여러 평점을 남겼다면 '평균'을 계산합니다.
    )

    # 피벗 테이블에서 각 제품별(열별) 평점 평균을 계산합니다.
    # 이 값은 비어있는 평점(NaN)을 채우는 데 사용됩니다.
    means = pivot_table.mean(axis=0)

    # fillna 함수를 사용해 피벗 테이블의 비어있는 값(NaN)을 위에서 계산한 제품별 평균 평점으로 채웁니다.
    # 예를 들어, A라는 사용자가 B라는 제품에 평점을 매기지 않았다면, B제품의 전체 평균 평점으로 그 자리를 대신 채웁니다.
    # 이렇게 하면 데이터가 비어있어서 발생하는 오류를 막고 더 안정적인 분석이 가능해집니다.
    pivot_table.fillna(means, inplace=True)

    # 아래는 주석 처리된 코드 예시입니다. 특정 열의 데이터를 보거나, 테이블 정보를 확인할 때 사용합니다.
    # print(pivot_table.iloc[:, 3].tolist())
    # pivot_table.info()
    # print(means)