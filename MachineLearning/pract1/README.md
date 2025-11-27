# AI/ML 기초 개념 학습 프로젝트

이 프로젝트는 AI와 머신러닝의 핵심 개념을 이해하기 위해 생성된 개인 학습용 저장소입니다.

Python 코드(`iris_analyst.py`)를 통해 실제 데이터를 다루는 것에서 출발하여, AI/ML의 근간이 되는 통계, 선형대수, 학습 원리 등을 정리한 종합 가이드 문서(`AI_입문자를_위한_통합_가이드.md`)를 완성하는 것을 목표로 합니다.

## 🗂️ 주요 파일

-   `AI_입문자를_위한_통합_가이드.md`
    -   본 프로젝트의 핵심 결과물입니다.
    -   비전공자의 시선에서 AI의 기본 원리를 **"Why → What → How → Advanced"** 흐름에 따라 체계적으로 정리한 문서입니다.
    -   Mermaid 다이어그램을 포함하여 복잡한 개념의 시각적 이해를 돕습니다.
-   `iris_analyst.py`
    -   학습의 시작점이 된 파이썬 스크립트입니다.
    -   `scikit-learn` 라이브러리를 사용하여 Iris 데이터셋을 불러오고, 데이터의 형태와 기본적인 행렬 연산을 실습합니다.
-   `requirements.txt`
    -   `iris_analyst.py` 스크립트 실행에 필요한 파이썬 라이브러리 목록입니다.

## 🚀 시작하기

이 저장소는 애플리케이션이 아닌 학습 과정을 담고 있습니다. `iris_analyst.py` 스크립트를 직접 실행해 보려면 다음 단계를 따르세요.

### 1. 저장소 복제

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. 가상 환경 설정 및 활성화

가상 환경을 생성하여 프로젝트별 라이브러리 의존성을 관리하는 것을 권장합니다.

```bash
# 가상 환경 생성
python -m venv .venv

# 가상 환경 활성화 (Windows)
.venv\Scripts\activate

# 가상 환경 활성화 (macOS/Linux)
source .venv/bin/activate
```

### 3. 필요 라이브러리 설치

```bash
pip install -r requirements.txt
```

### 4. 스크립트 실행

```bash
python iris_analyst.py
```

스크립트를 실행하면 Iris 데이터셋의 구조와 행렬 연산 결과가 콘솔에 출력됩니다.

