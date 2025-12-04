# arona_f_stats.py
# 이 스크립트는 F-검정(일원분산분석, ANOVA)을 사용하여
# 여러 그룹 간의 평균 값에 통계적으로 유의미한 차이가 있는지 분석합니다.
# 예: 할인율 그룹에 따라 상품 평점의 '평균'에 차이가 있는지 검정합니다.

import numpy as np
import pandas as pd
import scipy.stats as stats

if __name__ == "__main__":
    # 1. 데이터 불러오기 및 기본 전처리
    df = pd.read_csv("data/amazon.csv")
    df = df[["rating", "discount_percentage"]]
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df["discount_percentage"] = df["discount_percentage"].str.replace("%", "").astype(int)

    # 2. 연속형 데이터 '할인율'을 범주형 '할인율 그룹'으로 변환
    df['discount_percentage_group'] = pd.cut(
        df['discount_percentage'],
        bins=[0, 20, 40, 60, 80, 100],
        labels=["0-20", "20-40", "40-60", "60-80", "80-100"],
        include_lowest=True,
    )
    # 분석에 필요한 컬럼에 결측치가 있는 행 제거
    df.dropna(subset=["rating", "discount_percentage"], inplace=True)

    # (참고) 카이제곱 검정의 임계값 (이 F-검정 분석에서는 직접 사용되지 않음)
    critical_value = np.array([
        [0.05, 3.841],
        [0.01, 6.635],
        [0.001, 10.828]
    ])
    critical_df = pd.DataFrame(critical_value, columns=["유의수준", "임계값"])

    # 3. F-검정을 위한 데이터 구조 생성
    # 'discount_percentage_group'으로 그룹화한 뒤, 각 그룹에 속한 'rating' 값들을 리스트로 묶습니다.
    # 예: [ [0-20% 그룹의 평점들], [20-40% 그룹의 평점들], ... ]
    discount_groups = [group["rating"].values for name, group in df.groupby("discount_percentage_group", observed=False)]

    # 4. F-검정(일원분산분석) 수행
    # *discount_groups는 리스트의 각 배열을 개별 인자로 함수에 전달합니다.
    # stats.f_oneway(group1, group2, group3, ...)와 동일한 효과
    f_stat, p_value = stats.f_oneway(*discount_groups)

    print("--- F-검정(ANOVA) 분석 결과 ---")
    print(f"F-통계량 (F-statistic): {f_stat}")
    print(f"p-value: {p_value}")

    # 5. 결과 해석
    # p-value가 매우 작으므로 (예: 0.05보다 작음),
    # "할인율 그룹 간에 평점 평균의 차이가 없다"는 귀무가설을 기각합니다.
    # 결론: 할인율 그룹에 따라 평점 평균에 통계적으로 유의미한 차이가 존재합니다.

#     유의수준     임계값
# 0  0.050   3.841
# 1  0.010   6.635
# 2  0.001  10.828
# ------------------------
# F-통계량 :  7.475362313166936
# p_value :  5.849926204744066e-06
