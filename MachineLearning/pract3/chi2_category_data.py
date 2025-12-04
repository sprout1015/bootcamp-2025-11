# chi2_category_data.py
# 이 스크립트는 카이제곱(Chi-squared) 검정을 사용하여
# 두 범주형 변수 간의 연관성(독립성)을 분석합니다.
# 예: 기저귀 구매 여부와 맥주 구매 여부가 서로 관련이 있는지 검정합니다.

import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

# 카이제곱 검정의 임계값 예시 (자유도=1일 때)
# 이 값과 카이제곱 통계량을 비교하여 가설을 검정할 수 있습니다.
critical_value = np.array([
    [0.05, 3.841],
    [0.01, 6.635],
    [0.001, 10.828]
])
critical_df = pd.DataFrame(critical_value, columns=["유의수준", "임계값"])


# 범주형 데이터는 평균을 구할 수 없으므로, 빈도(횟수)를 기반으로 분석합니다.

def diaper_beer_chi2_pract():
    """ '기저귀-맥주' 예제로 카이제곱 검정을 시연하는 함수 """
    # 1. 관측 빈도를 담은 분할표(Contingency Table)
    observed = np.array([
        #         맥주 구매 O / 맥주 구매 X
        [30, 10],  # 기저귀 구매 O
        [5, 55]    # 기저귀 구매 X
    ])
    index = ["buy_diaper", "non_diaper"]
    column = ["buy_beer", "non_beer"]
    pivot_df = pd.DataFrame(observed, index=index, columns=column)
    print("--- 기저귀-맥주 교차표 ---")
    print(pivot_df)

    # 2. 카이제곱 검정 수행
    # chi2_contingency는 교차표를 입력받아 통계량, p-value 등을 반환합니다.
    chi2, p_value, _, _ = chi2_contingency(pivot_df)
    print(f"\n카이제곱 통계량: {chi2}")
    print(f"p-value: {p_value}")


def discount_rating_prac():
    """ '할인율-평점' 데이터로 카이제곱 검정을 시연하는 함수 """
    # 1. 데이터 불러오기 및 전처리
    df = pd.read_csv("data/amazon.csv")
    df = df[["rating", "discount_percentage"]]
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df["discount_percentage"] = df["discount_percentage"].str.replace("%", "").astype(int)

    # 2. 연속형 데이터를 `pd.cut`을 이용해 범주형 데이터로 변환
    df['rating_group'] = pd.cut(
        df['rating'],
        bins=[0, 3.0, 4.0, 5.0],
        labels=["0-3.0", "3.0-4.0", "4.0-5.0"],
        include_lowest=True,
    )
    df['discount_percentage_group'] = pd.cut(
        df['discount_percentage'],
        bins=[0, 20, 40, 60, 80, 100],
        labels=["0-20", "20-40", "40-60", "60-80", "80-100"],
        include_lowest=True,
    )

    # 3. `pd.crosstab`으로 두 범주형 변수 간의 교차표(빈도표) 생성
    pivot_df = pd.crosstab(df['discount_percentage_group'], df['rating_group'])
    print("\n--- 할인율-평점 교차표 ---")
    print(pivot_df)

    # 4. 카이제곱 검정 수행
    chi2, p_value, _, _ = chi2_contingency(pivot_df)
    print("\n--- 카이제곱 검정 분석 결과 ---")
    print("임계값 표:")
    print(critical_df)
    print("------------------------")
    print(f"카이제곱 통계량: {chi2}")
    print(f"p-value: {p_value}")

    # 5. 결과 해석
    # p-value가 매우 작으므로(예: 0.05보다 작음), 
    # "할인율 그룹과 평점 그룹은 서로 독립적이다"라는 귀무가설을 기각합니다.
    # 결론: 두 변수 간에는 통계적으로 유의미한 연관성이 있습니다.


if __name__ == "__main__":
    # diaper_beer_chi2_pract()
    # "할인율"과 "rating"을 카이제곱 검정으로 분석합니다.
    # 연속적인 데이터를 카이제곱으로 분석하려면 먼저 데이터를 범주화해야 합니다.
    discount_rating_prac()

# --- 카이제곱 검정 요약 ---
# - 두 범주형 변수 간의 '독립성' 또는 '연관성'을 검정하는 데 사용됩니다.
# - 통계량 계산 원리: (관측 빈도 - 기대 빈도)² / 기대 빈도 의 총합.
# - 기대 빈도: 두 변수가 독립적일 때 기대되는 빈도수.
#   (예: (행 합계 * 열 합계) / 전체 합계)
# - 해석: 카이제곱 통계량이 임계값보다 크거나, p-value가 유의수준(e.g., 0.05)보다 작으면
#   "두 변수는 연관성이 있다"고 결론 내립니다.
