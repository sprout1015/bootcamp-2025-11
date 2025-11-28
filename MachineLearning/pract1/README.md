# AI/ML 데이터 분석 및 처리 학습 프로젝트

이 프로젝트는 AI와 머신러닝의 핵심 개념을 이해하고, 실제 데이터를 다루는 능력을 기르기 위한 개인 학습용 저장소입니다. Python의 데이터 분석 라이브러리(Pandas, Scikit-learn, Matplotlib)를 활용하여 다양한 데이터셋을 탐색, 변환, 분석하는 스크립트를 포함하고 있습니다.

## 🗂️ 프로젝트 구성

### 1. 핵심 가이드 문서

-   `AI_입문자를_위한_통합_가이드.md`
    -   AI/ML의 근간이 되는 통계, 선형대수, 학습 원리 등을 체계적으로 정리한 종합 가이드 문서입니다.

### 2. 데이터 분석 스크립트

각 스크립트는 특정 데이터셋을 대상으로 한 분석 작업을 수행합니다.

-   `iris_analyst.py`
    -   **목표**: Scikit-learn 라이브러리 기초 실습.
    -   **기능**: `Iris` (붓꽃) 데이터셋을 로드하고, 데이터의 구조(shape, features)를 확인합니다. 행렬 곱셈(`@`)을 이용해 데이터의 공분산 행렬을 계산하고 출력합니다.
    -   **사용 데이터**: `scikit-learn` 내장 Iris 데이터셋.

-   `height_weight_analytics.py`
    -   **목표**: 주성분 분석(PCA)의 핵심 개념인 고유값(Eigenvalue)과 고유벡터(Eigenvector) 이해.
    -   **기능**: 키와 몸무게 데이터를 시각화하고, 데이터의 공분산 행렬을 계산합니다. `numpy.linalg.eig`를 사용해 이 행렬의 고유값과 고유벡터를 찾아내고, 데이터의 주성분(분산이 가장 큰 방향)을 분석합니다.
    -   **사용 데이터**: `data/SOCR-HeightWeight.csv`

-   `merge_with_product.py`
    -   **목표**: 여러 데이터 소스를 결합하는 ETL(Extract, Transform, Load) 파이프라인 실습.
    -   **기능**: `Sales.xlsx`(판매 실적)와 `Details.xlsx`(제품, 고객, 지역 등 차원 정보) 파일을 읽어옵니다. 정의된 규칙에 따라 `pandas.merge`를 사용해 여러 데이터프레임을 순차적으로 병합합니다. 최종적으로 제품별 총매출을 계산하고 상위 5개 제품을 출력합니다.
    -   **사용 데이터**: `data/Sales.xlsx`, `data/Details.xlsx`

-   `pivot.py`
    -   **목표**: 데이터를 재구조화하여 특정 관점의 인사이트 도출.
    -   **기능**: 아마존 제품 리뷰 데이터를 `pivot_table`을 사용해 '사용자-제품' 행렬로 변환합니다. 각 셀은 사용자가 특정 제품에 부여한 평균 평점을 나타냅니다. 이를 통해 협업 필터링(Collaborative Filtering)과 같은 추천 시스템의 기반 데이터를 생성하는 원리를 실습합니다.
    -   **사용 데이터**: `data/amazon.csv`

### 3. 필요 라이브러리

-   `requirements.txt`
    -   위 스크립트 실행에 필요한 파이썬 라이브러리 목록입니다. (`pandas`, `scikit-learn`, `matplotlib`, `numpy`, `openpyxl`)

## 🚀 시작하기

스크립트를 직접 실행해 보려면 다음 단계를 따르세요.

### 1. 저장소 복제

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. 가상 환경 설정 및 라이브러리 설치

```bash
# 가상 환경 생성
python -m venv .venv

# 가상 환경 활성화 (Windows)
.venv\Scripts\activate

# 가상 환경 활성화 (macOS/Linux)
source .venv/bin/activate

# 필요 라이브러리 설치
pip install -r requirements.txt
```

### 3. 스크립트 실행

분석하고 싶은 스크립트를 선택하여 실행합니다.

```bash
# 예: 키-몸무게 데이터 분석 실행
python height_weight_analytics.py

# 예: 판매 데이터 병합 및 분석 실행
python merge_with_product.py
```