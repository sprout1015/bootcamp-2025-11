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

### 🔹 개방-폐쇄 원칙 (Open/Closed Principle - OCP)
> "소프트웨어 개체(클래스, 모듈, 함수 등)는 확장에 대해 열려 있어야 하고, 수정에 대해서는 닫혀 있어야 한다."

- **기존 문제**: 새로운 평가 지표를 추가하거나 데이터 소스를 변경하려면, 거대한 `train_fm.py` 파일을 직접 수정해야 했습니다.
- **리팩토링**: 기능이 분리되어 이제 새로운 기능을 "수정"이 아닌 "확장"을 통해 추가할 수 있습니다. 예를 들어, `src/evaluator.py`에 새로운 평가 함수를 추가해도 다른 코드에 영향을 주지 않습니다.

### 🔹 의존성 역전 원칙 (Dependency Inversion Principle - DIP)
> "상위 모듈은 하위 모듈에 의존해서는 안 된다. 둘 모두 추상화에 의존해야 한다."

- **기존 문제**: 메인 실행 로직이 데이터 처리나 학습 루프의 구체적인 구현에 직접 의존했습니다.
- **리팩토링**: `train.py`(상위 모듈)는 각 컴포넌트(`Trainer`, `MatrixFactorization` 등)를 가져와 조립하는 역할만 합니다. 각 컴포넌트는 독립적으로 존재하며, `train.py`가 이들의 의존성을 주입해주는 형태로 변경되었습니다.

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
│   ├── config.py           # 모든 설정 관리
│   ├── data_loader.py      # 데이터 로딩 및 전처리
│   ├── model.py            # 모델 클래스 정의
│   ├── evaluator.py        # 평가 함수
│   └── trainer.py          # 학습 클래스
│
├── train.py                # 메인 실행 스크립트
├── requirements.txt
└── README.md
```

---

## 4. 설치 및 실행 방법

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
**실행 방법이 변경되었습니다.** 이제 루트 디렉토리의 `train.py`를 실행합니다.

```bash
python train.py
```

---

## 5. 실행 결과 예시

학습 명령어를 실행하면 터미널에 다음과 같은 결과가 출력됩니다.

```
PyTorch device check: Using CPU
--- Preparing Data ---
Original data length: 10000053, Filtered data length: 313596
User and Movie IDs have been mapped to zero-based indices.
Train data size: 250876, Test data size: 62720
--- Data Preparation Finished ---

--- Start Training ---
Epoch 1/10: 100%|██████████| 3920/3920 [00:11<00:00, 327.62it/s, loss=0.431]
Epoch [1/10] - Average Loss: 2.9544
... (중략) ...
Epoch 10/10: 100%|██████████| 3920/3920 [00:13<00:00, 292.82it/s, loss=0.124]
Epoch [10/10] - Average Loss: 0.1262
--- Training Finished ---

--- Model Evaluation ---
RMSE (평균 제곱근 오차): 0.4879
MAE (평균 절대 오차): 0.3544
------------------------

Model saved successfully -> ./model/fm_model.pt
```

---

## 6. Python 기초 개념

#### `__init__.py` 파일의 역할
- `src` 같은 디렉토리 안에 `__init__.py` 파일이 있으면, 파이썬은 그 디렉토리를 하나의 **패키지(Package)**로 인식합니다.
- 덕분에 `train.py`에서 `from src.model import ...` 와 같이 다른 파일의 클래스나 함수를 쉽게 가져와 사용할 수 있습니다.

#### `if __name__ == "__main__"` 의 의미
- 파이썬 스크립트는 직접 실행될 수도 있고, 다른 파일에서 `import` 되어 사용될 수도 있습니다.
- `if __name__ == "__main__"` 블록 안의 코드는 **오직 해당 스크립트가 터미널에서 직접 실행될 때만 동작합니다.**
- 이를 통해 "직접 실행" 코드와 "재사용 가능한 함수/클래스 정의" 코드를 분리할 수 있습니다.

#### `forward` 와 `__call__` 메소드
- PyTorch에서 `nn.Module`을 상속받는 모든 모델 클래스는 `forward` 메소드를 정의해야 합니다. 이 메소드는 입력 데이터가 모델을 거쳐 출력값을 만들어내는 **순전파** 과정을 정의합니다.
- 실제 코드에서는 `model.forward(data)` 대신 `model(data)` 처럼 객체를 함수처럼 호출하는데, 이는 파이썬의 `__call__` 특별 메소드 덕분입니다. `nn.Module`의 `__call__`은 내부적으로 `forward`를 호출하며, 그 전후에 파이토치가 필요로 하는 여러 추가 작업을 자동으로 처리해줍니다.
- **결론: PyTorch 모델을 사용할 때는 `.forward()`를 직접 호출하지 말고, `model(...)` 과 같이 객체 자체를 함수처럼 호출하는 것이 올바른 방법입니다.**