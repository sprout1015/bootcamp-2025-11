# 영화 추천 시스템 튜토리얼 (SOLID 리팩토링 버전)

## 1. 프로젝트 개요

이 프로젝트는 파이토치(PyTorch)를 사용한 간단한 **영화 추천 시스템** 예제입니다. 특히, 소프트웨어 공학의 **SOLID 원칙**을 적용하여 각 코드의 역할을 명확히 분리하고, 유지보수와 확장이 용이한 구조로 리팩토링하는 것에 초점을 맞춥니다.

`Matrix Factorization (행렬 분해)` 알고리즘을 사용해 사용자가 아직 평가하지 않은 영화의 평점을 예측하는 모델을 학습합니다.

---

## 2. SOLID 원칙과 리팩토링

이 프로젝트는 다음과 같은 SOLID 원칙을 적용하여 리팩토링되었습니다.

### 🔹 단일 책임 원칙 (Single Responsibility Principle - SRP)
> "클래스는 단 하나의 변경 이유만을 가져야 한다."

- **기존 문제**: `train_fm.py` 파일 하나가 데이터 로딩, 전처리, 모델 생성, 학습, 평가, 저장 등 너무 많은 책임을 가지고 있었습니다.
- **리팩토링**: 각 기능을 별도의 모듈로 분리했습니다.
  - `src/config.py`: 모든 설정 값 관리
  - `src/data_loader.py`: 데이터 처리 책임
  - `src/model.py`: 모델 구조 정의 책임
  - `src/evaluator.py`: 모델 평가 책임
  - `src/trainer.py`: 모델 학습 과정 책임
  - `train.py`: 전체 파이프라인을 조립하고 실행하는 책임

---

## 3. 새로운 프로젝트 구조

```
fm_deep_learning/
│
├── data/
│   └── ratings.pkl
│
├── model/
│   └── fm_model.pt
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── data_loader.py
│   ├── model.py
│   ├── evaluator.py
│   └── trainer.py
│
├── api.py                  # FastAPI 서버 스크립트
├── test_model.py           # 모델 테스트 스크립트
├── train.py                # 메인 실행 스크립트
├── requirements.txt
└── README.md
```

---

## 4. 학습 파이프라인: 한 눈에 보기

이 프로젝트의 전체 학습 과정(한 사이클)은 다음과 같은 순서로 진행됩니다. 각 단계는 명확한 책임을 가지며, 독립적인 모듈로 구현되어 있습니다.

| 단계 | 설명 | 책임 모듈 |
| :--- | :--- | :--- |
| **1. 설정 로딩** | 학습에 필요한 모든 하이퍼파라미터(학습률, 배치 크기 등)와 파일 경로를 불러옵니다. | `src/config.py` |
| **2. 데이터 준비** | 원본 데이터를 불러와 정제하고, 모델이 학습할 수 있는 형태(Tensor)로 변환합니다. ID를 0부터 시작하는 인덱스로 매핑하고, 학습/테스트 세트로 분리하여 `DataLoader`를 생성합니다. | `src/data_loader.py` |
| **3. 모델 초기화** | `MatrixFactorization` 모델의 인스턴스를 생성합니다. 데이터에서 파악된 총 사용자 수와 아이템 수를 바탕으로 모델의 임베딩 레이어 크기가 결정됩니다. | `src/model.py` |
| **4. 학습기 설정** | 모델, 손실 함수(MSE), 옵티마이저(Adam)를 포함하는 `Trainer` 객체를 생성합니다. 이 때 모델을 GPU/CPU 등 적절한 장치로 이동시킵니다. | `src/trainer.py` |
| **5. 모델 학습** | `Trainer`가 본격적으로 학습을 시작합니다. 전체 데이터를 정해진 횟수(Epoch)만큼 반복하며 모델의 가중치(잠재 요인)를 업데이트합니다. | `src/trainer.py` |
| **6. 모델 평가** | 학습이 끝난 모델을 한 번도 본 적 없는 테스트 데이터로 평가합니다. RMSE, MAE 같은 지표를 통해 모델의 일반화 성능을 확인합니다. | `src/evaluator.py` |
| **7. 모델 저장** | 학습된 모델의 가중치와 ID 변환에 필요한 맵(map) 정보를 `.pt` 파일로 저장하여, 나중에 재사용할 수 있도록 합니다. | `src/trainer.py` |

이 모든 과정은 최종적으로 `train.py` 스크립트 하나를 실행하여 순차적으로 수행됩니다.

---

## 5. 설치 및 실행 방법

### 1단계: 가상환경 설정 및 활성화
```bash
# Windows, PowerShell
python -m venv .venv
.venv\Scripts\Activate.ps1

# Mac/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 2단계: 필요 라이브러리 설치
```bash
pip install -r requirements.txt
```

### 3단계: 모델 학습 실행
```bash
python train.py
```
---

## 6. 모델 활용

### 1) API 서버 실행
추천 모델을 API 형태로 제공하는 FastAPI 서버를 실행합니다.

```bash
uvicorn api:app --reload
```
서버가 실행되면, 웹 브라우저에서 `http://127.0.0.1:8000/docs` 로 접속하여 API 문서를 확인하고 직접 테스트해볼 수 있습니다.

#### API 요청 및 응답 예시
`GET http://localhost:8000/recommend/9500`
```json
{
    "user_id": 9500,
    "top_k": 10,
    "recommended_movie_ids": [ 8125, 5619, 1039, 48596, ... ],
    "scores": [ "6.3957", "6.3032", "6.2313", "6.2268", ... ]
}
```

### 2) 단독 테스트 실행
`test_model.py` 스크립트는 저장된 모델을 불러와 임의의 사용자에 대한 예측 및 추천을 수행하는 간단한 테스트입니다.

```bash
python test_model.py
```

---

## 7. 개발 및 트러블슈팅

개발 과정에서 발생했던 주요 문제와 해결 과정을 공유합니다.

### 문제 1: `torch.load` 실행 시 `Weights only load failed` 오류
- **원인**: 최신 PyTorch 버전은 보안상의 이유로 모델 가중치 외에 다른 파이썬 객체(pickle)가 포함된 파일의 로드를 기본적으로 차단합니다.
- **해결**: `torch.load()` 함수에 `weights_only=False` 인자를 명시적으로 추가하여, 신뢰할 수 있는 소스임을 알리고 딕셔너리 객체도 함께 불러오도록 허용했습니다.

### 문제 2: FastAPI 실행 시 `ValueError` / `TypeError` 발생
- **원인**: API가 추천 결과로 `numpy.int64` 타입의 ID 리스트를 반환했습니다. FastAPI의 기본 JSON 인코더는 NumPy 고유의 숫자 타입을 처리하지 못해 직렬화(Serialization) 오류가 발생했습니다.
- **해결**: 추천 ID를 반환하기 직전에, 리스트의 각 ID를 파이썬 표준 `int` 타입으로 명시적으로 변환(`int()`)해주어 문제를 해결했습니다.

---

## 8. Python 기초 개념

#### `__init__.py` 파일의 역할
- `src` 같은 디렉토리 안에 `__init__.py` 파일이 있으면, 파이썬은 그 디렉토리를 하나의 **패키지(Package)**로 인식합니다. 덕분에 다른 파일에서 `from src.model import ...` 와 같이 쉽게 코드를 가져와 사용할 수 있습니다.

#### `if __name__ == "__main__"` 의 의미
- 파이썬 스크립트는 직접 실행될 수도 있고, 다른 파일에서 `import` 되어 사용될 수도 있습니다. `if __name__ == "__main__"` 블록 안의 코드는 **오직 해당 스크립트가 터미널에서 직접 실행될 때만 동작합니다.**

#### `forward` 와 `__call__` 메소드
- PyTorch에서 `nn.Module`을 상속받는 모든 모델은 `forward` 메소드를 정의해야 합니다. 이 메소드는 모델의 순전파 과정을 정의합니다. 실제 코드에서는 `model.forward(data)` 대신 `model(data)` 처럼 객체를 함수처럼 호출하는데, 이는 파이썬의 `__call__` 특별 메소드 덕분입니다.