import pandas as pd

if __name__ == "__main__": # 현재 파일을 직접 실행할 때만 아래 코드 실행

    df = pd.read_csv("data/amazon.csv")

    # df.keys() → 데이터프레임의 컬럼 이름 확인
    # ['product_id', 'product_name', 'category', 'discounted_price',
    #        'actual_price', 'discount_percentage', 'rating', 'rating_count',
    #        'about_product', 'user_id', 'user_name', 'review_id', 'review_title',
    #        'review_content', 'img_link', 'product_link'],
    #       dtype='object'

    # df.info() → 데이터프레임의 전체 구조, 행 개수, 컬럼별 데이터 타입/결측치 개수 확인
    # RangeIndex: 1465 entries, 0 to 1464
    # Data columns (total 16 columns):
    #  #   Column               Non-Null Count  Dtype
    # ---  ------               --------------  -----
    #  0   product_id           1465 non-null   object
    #  1   product_name         1465 non-null   object
    #  2   category             1465 non-null   object
    #  3   discounted_price     1465 non-null   object
    #  4   actual_price         1465 non-null   object
    #  5   discount_percentage  1465 non-null   object
    #  6   rating               1465 non-null   object
    #  7   rating_count         1463 non-null   object
    #  8   about_product        1465 non-null   object
    #  9   user_id              1465 non-null   object
    #  10  user_name            1465 non-null   object
    #  11  review_id            1465 non-null   object
    #  12  review_title         1465 non-null   object
    #  13  review_content       1465 non-null   object
    #  14  img_link             1465 non-null   object
    #  15  product_link         1465 non-null   object
    # dtypes: object(16)
    # memory usage: 183.2+ KB
    # 총 16개 컬럼, 모두 object 타입(문자열), rating_count만 결측치 2개 있음

    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    # rating 컬럼을 숫자(float)로 변환. 변환 불가능한 값은 NaN으로 처리

    df["user_name"] = df["user_name"].str.split(",")
    # user_name 컬럼에 여러 유저 이름이 ','로 붙어있으므로 리스트로 분리

    df_explode = df.explode("user_name")
    # user_name 리스트를 행 단위로 펼침 → 한 유저 이름당 한 행으로 변환

    df_explode.reset_index(inplace=True, drop=True);
    # 인덱스를 다시 0부터 순서대로 재설정, 기존 인덱스는 버림
    my_pivot = pd.pivot_table(
        df_explode,
        # info의 rating 타입이 object(String)형이라 집계함수 불가능
        #       -> pd.to_numeric()을 통해 숫자로 변환
        #  6   rating               1465 non-null   object -> float
        values = "rating",          # 집계할 값: rating
        columns="product_name",     # 열 축: 상품 이름
        index="user_name",          # 행 축: 유저 이름
        aggfunc="mean",             # 집계 함수: 평균
        fill_value=None             # 값이 없으면 NaN 유지
    )
    # → 유저 × 상품 매트릭스 생성, 각 셀은 해당 유저가 남긴 상품 평점 평균

    means = my_pivot.mean(axis=0)
    # 각 상품별 평균 평점 계산 (열 기준 평균)

    print(my_pivot.dropna(how="all"))
    # 모든 값이 NaN인 행(즉, 어떤 상품도 평가하지 않은 유저)은 제거 후 출력

