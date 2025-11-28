import pandas as pd

# -------------------------------
# 1. 병합 규칙 정의
# -------------------------------
# 각 규칙은 (변수 키, 시트명, 병합 기준 컬럼)으로 구성
MERGE_RULES = [
    ("date", "날짜", "날짜"),
    ("region", "지역", "지역"),
    ("product", "제품", "제품코드"),
    ("customer", "2018년도~2022년도 주문고객", "고객코드"),
    ("promotion", "프로모션", "프로모션코드"),
    ("channel", "채널", "채널코드"),
    ("product_category", "제품분류", "제품분류코드"),
    ("category", "분류", "분류코드"),
]

# -------------------------------
# 2. Response DTO 스키마 정의
# -------------------------------
# 응답용 컬럼 이름 매핑 (API 친화적인 이름으로 변환)
# Keys = ['날짜', '제품코드', '고객코드', '프로모션코드', '채널코드', 'Quantity', 'UnitPrice', '지역',
#        '날짜코드', '년도', '분기', '월(No)', '월(영문)', '지역코드_x', '시도', '구군시', '제품명',
#        '색상', '원가', '단가', '제품분류코드', '지역코드_y', '고객명', '성별', '생년월일', '프로모션',
#        '할인율', '채널명', '제품분류명', '분류코드', '분류명']
COLUMN_MAPPING = {
    "날짜": ("date", True),
    "고객명": ("customerName", True),
    "Quantity": ("quantity", True),
    "단가": ("price", True),
    "원가": ("originalPrice", True),
    "지역": ("region", True),
    "색상": ("color", True),
    "프로모션": ("promotionName", True),
    "할인율": ("discountRate", True),
    "채널명": ("channelName", True),
    "제품명": ("productName", True),
    "제품분류명": ("productCategoryName", True),
    "분류명": ("categoryName", True),
    "시도": ("province", True),
    "구군시": ("city", True),
    ###############################################3
    "UnitPrice": ("unitPrice", False),
    "성별": ("gender", False),
    "년도": ("year", False),
    "분기": ("quarter", False),
    "월(No)": ("month_no", False),
    "월(영문)": ("month_name", False),
    "제품코드": ("productId", False),
    "고객코드": ("customerId", False)
}
# 응답용 컬럼 매핑 + 표시 여부

# -------------------------------
# 3. 함수 정의
# -------------------------------

def load_details(path, rules):
    """
    엑셀 파일에서 모든 시트를 읽어 dict로 반환
    rules에 정의된 시트명 기준으로 dict 구성
    """
    details = pd.read_excel(path, sheet_name=None)
    details_dict = {var: details[sheet] for var, sheet, _ in rules}

    # 날짜 컬럼은 datetime으로 변환
    details_dict["date"]["날짜"] = pd.to_datetime(details_dict["date"]["날짜"])
    return details_dict


def merge_sales(sales, details_dict, rules):
    """
    Sales 엔티티와 Details 차원 테이블을 병합
    rules에 정의된 기준 컬럼을 사용하여 순차적으로 merge
    """
    df = sales.copy()
    for var, _, on_col in rules:
        df = pd.merge(df, details_dict[var], on=on_col, how="left")
    return df


def to_response_dto(df, mapping):
    """
    Entity DataFrame → Response DTO 변환
    COLUMN_MAPPING에서 True인 컬럼만 선택하고 이름을 매핑
    """
    # True인 컬럼만 추출
    selected_cols = [col for col, (_, flag) in mapping.items() if flag]

    # DTO 생성
    dto = df[selected_cols].copy()

    # 이름 매핑 dict 생성
    rename_dict = {col: new_name for col, (new_name, flag) in mapping.items() if flag}

    return dto.rename(columns=rename_dict)


def group_by_response_dto(df):
    # sales는 숫자형으로 계산
    df["sales"] = df["quantity"] * ((df["price"] * (1 - df["discountRate"])) - df["originalPrice"])
    # 집계 (숫자 상태)
    result = df.groupby("productName")["sales"].sum().sort_values(ascending=False)
    # 집계 결과를 포맷팅해서 문자열로 변환
    result_formatted = result.apply(lambda x: f"KRW {int(x):,}")
    return result_formatted

# -------------------------------
# 4. 실행 부분
# -------------------------------
if __name__ == "__main__":
    # Sales 엔티티 로드
    sales = pd.read_excel("data/Sales.xlsx", sheet_name="Sheet1")

    # Details 차원 테이블 로드
    details_dict = load_details("data/Details.xlsx", MERGE_RULES)

    # Entity 병합
    merge_df = merge_sales(sales, details_dict, MERGE_RULES)

    # Response DTO 변환
    response_dto = to_response_dto(merge_df, COLUMN_MAPPING)

    # GroupBy
    response_dto_with_group = group_by_response_dto(response_dto)

    # 결과 출력
    print(response_dto_with_group.head())