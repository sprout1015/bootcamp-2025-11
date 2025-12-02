# pandas 라이브러리를 pd라는 별칭으로 불러옵니다. 데이터 분석의 필수 도구입니다.
import pandas as pd


# 이 파일이 직접 실행될 때만 아래 코드가 동작합니다.
if __name__ == "__main__":
    # --- 1. 데이터 불러오기 ---
    # "Sales.xlsx" 파일의 "Sheet1" 시트에서 판매 실적 데이터를 불러옵니다.
    sales = pd.read_excel("data/Sales.xlsx", sheet_name="Sheet1")
    
    # "Details.xlsx" 파일의 모든 시트를 한 번에 불러옵니다.
    # sheet_name=None 옵션은 각 시트의 이름이 key가 되고, 시트의 내용이 value(DataFrame)가 되는 딕셔너리 형태로 데이터를 반환합니다.
    details = pd.read_excel("data/Details.xlsx", sheet_name=None)
    
    # 딕셔너리 형태로 불러온 'details'에서 각 시트(DataFrame)를 개별 변수에 할당합니다.
    # 이렇게 하면 코드를 읽고 이해하기가 더 쉬워집니다.
    promotion = details['프로모션']
    channel = details['채널']
    region = details['지역']
    category = details['분류']
    product_category = details['제품분류']
    product = details['제품']
    date = details['날짜']
    customer = details["2018년도~2022년도 주문고객"]

    # '날짜' 열의 데이터 타입을 문자열에서 날짜/시간(datetime) 타입으로 변환합니다.
    # 이렇게 해야 날짜 관련 계산이나 분석(예: 월별, 연도별 분석)이 가능해집니다.
    date['날짜'] = pd.to_datetime(date['날짜'])
    
    # --- 2. 데이터 병합(Merge) ---
    # 'sales' 데이터를 기준으로, 필요한 정보들을 순차적으로 합쳐 나갑니다.
    # pd.merge 함수는 두 데이터프레임을 특정 열('on' 옵션)을 기준으로 합쳐줍니다.
    # how='left'는 왼쪽(sales) 데이터는 모두 유지하고, 오른쪽(date, product 등)에서 키 값이 일치하는 정보를 가져와 붙이는 방식입니다.
    # 마치 VLOOKUP 함수를 여러 번 실행하는 것과 비슷합니다.
    
    # 1. sales 데이터에 '날짜' 정보를 붙입니다. (기준: '날짜' 열)
    merge_df = pd.merge(sales, date, on='날짜', how='left')
    # 2. 위 결과에 '제품' 정보를 붙입니다. (기준: '제품코드' 열)
    merge_df = pd.merge(merge_df, product, on="제품코드", how='left')
    # 3. 위 결과에 '고객' 정보를 붙입니다. (기준: '고객코드' 열)
    merge_df = pd.merge(merge_df, customer, on="고객코드", how='left')
    # ... 이런 식으로 필요한 모든 정보(프로모션, 채널, 분류 등)를 계속해서 붙여 나갑니다.
    merge_df = pd.merge(merge_df, promotion, on="프로모션코드", how='left')
    merge_df = pd.merge(merge_df, channel, on='채널코드', how='left')
    merge_df = pd.merge(merge_df, product_category, on="제품분류코드", how='left')
    merge_df = pd.merge(merge_df, category, on='분류코드', how='left')
    merge_df = pd.merge(merge_df, region, on="지역코드", how='left')
    
    # --- 3. 데이터 정리 및 가공 ---
    # merge_df.keys()는 현재 데이터의 모든 열 이름을 보여줍니다. 어떤 열이 있는지 확인할 때 유용합니다.
    # print(merge_df.keys())

    # 분석에 필요한 열들만 선택하여 새로운 데이터프레임을 만듭니다. 순서도 보기 좋게 재배치합니다.
    merge_df = merge_df[[
        '날짜','고객명', 'Quantity', '단가', '원가',
        '지역_x', '색상','프로모션', '할인율', '채널명',
        '제품명', '제품분류명', '분류명', '시도', '구군시'
    ]]
    
    # 열 이름을 더 알아보기 쉽게 한국어로 변경합니다. ('Quantity' -> '수량', '지역_x' -> '지역')
    merge_df.rename({"Quantity": "수량", "지역_x": "지역"}, axis=1, inplace=True)
    
    # '판매량'이라는 새로운 열을 계산하여 추가합니다.
    # 계산식: 수량 * (할인 적용된 판매가 - 원가) -> 여기서는 원가 대신 단가를 빼서, 총 할인 금액의 음수 값을 계산하고 있습니다.
    # 이 값은 '얼마나 많이 할인해줬나'를 나타내는 지표로 해석할 수 있습니다. (값이 작을수록 할인액이 큼)
    merge_df['판매량'] = merge_df["수량"] * (merge_df["단가"] * (1- merge_df['할인율']) - merge_df['단가'])

    # --- 4. 데이터 분석 및 결과 출력 ---
    # '제품명'을 기준으로 데이터를 그룹화(groupby)하고, 각 제품별 '판매량'의 합계를 계산합니다.
    # 그리고 그 결과를 내림차순(ascending=False)으로 정렬하여 어떤 제품의 할인액이 가장 컸는지 확인합니다.
    product_group_revenue = merge_df.groupby("제품명")['판매량'].sum().sort_values(ascending=False)
    
    # 최종 분석 결과를 출력합니다.
    print(product_group_revenue)