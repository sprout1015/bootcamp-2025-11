# Full-Stack Employee Management System

이 프로젝트는 **React, Redux, Next.js**를 사용한 프론트엔드와 **Python, FastAPI, GraphQL, PostgreSQL, Redis**를 사용한 백엔드를 결합한 풀스택 직원 관리 시스템 예제입니다.

전체 스택의 통합 과정을 학습하고, 각 기술의 실용적인 사용법을 익히는 것을 목표로 합니다.

---

## 🚀 Tech Stack

| 구분        | 기술 스택                                                                 |
| :---------- | :------------------------------------------------------------------------ |
| **Frontend**  | React, Next.js, TypeScript, Redux Toolkit, Axios, Tailwind CSS            |
| **Backend**   | Python, FastAPI, GraphQL (Strawberry), SQLAlchemy (ORM), PostgreSQL, Redis |
| **Database**  | PostgreSQL, Redis                                                       |

---

## 📂 Project Structure

프로젝트는 `FrontEnd`와 `BackEnd` 두 개의 메인 디렉토리로 구성되어 있습니다.

```
C:\Project_2025_11\
├── BackEnd/
│   └── python/
│       └── employee_fastapi_graphQL/  (FastAPI + GraphQL 백엔드)
├── FrontEnd/
│   └── Nextjs/
│       └── ts_employ_graphql/         (Next.js + Redux 프론트엔드)
├── GEMINI.md                          (프로젝트 정보 및 개발 규칙)
└── README.md                          (현재 파일)
```

### 1. BackEnd (`employee_fastapi_graphQL`)
- FastAPI와 Strawberry 라이브러리를 기반으로 한 GraphQL API 서버입니다.
- **두 개의 독립적인 API 엔드포인트**를 제공합니다.
  - **PostgreSQL 기반 API (`/graphql`)**: SQLAlchemy ORM을 통해 PostgreSQL 데이터베이스와 통신하여 데이터를 영구적으로 관리합니다.
  - **Redis 기반 API (`/graphql-redis`)**: DB와 완전히 독립적으로, In-memory 데이터베이스인 Redis만을 사용하여 데이터를 관리합니다.
- 유지보수와 확장성을 고려하여 **3-티어 아키텍처 (API - Service - Repository)** 로 설계되었습니다.

### 2. FrontEnd (`ts_employ_graphql`)
- Next.js(App Router)를 기반으로 한 직원 관리 웹 애플리케이션입니다.
- **Redux Toolkit**을 사용하여 직원 목록, API 통신 상태(로딩, 에러) 등 모든 클라이언트 상태를 중앙에서 관리합니다.
- `axios`를 사용하여 백엔드 GraphQL API와 비동기적으로 통신하며, CRUD 기능을 사용자에게 제공합니다.

---

## 🏁 How to Run

이 프로젝트를 실행하려면 백엔드 서버와 프론트엔드 개발 서버를 각각 실행해야 합니다.

### 1. Backend Server

#### 가. 경로 이동
```shell
cd BackEnd/python/employee_fastapi_graphQL
```

#### 나. 가상 환경 생성 및 활성화 (필요시)
```shell
# 가상 환경 생성
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

#### 다. 의존성 패키지 설치
```shell
pip install -r requirements.txt
```

#### 라. `.env` 파일 생성
프로젝트 루트(`employee_fastapi_graphQL`)에 `.env` 파일을 생성하고, 사용하는 DB 및 Redis 정보를 아래와 같이 입력합니다.
```
# .env

# PostgreSQL 접속 정보
DATABASE_URL=postgresql://<USER>:<PASSWORD>@<HOST>:<PORT>/<DB_NAME>

# Redis 접속 정보 (없을 경우 redis://localhost:6379로 기본 설정됨)
REDIS_URL=redis://localhost:6379
```

#### 마. 백엔드 서버 실행
```shell
uvicorn main:app --reload --port 3002
```
- 서버가 정상적으로 실행되면 아래 두 주소에서 GraphQL Playground를 각각 확인할 수 있습니다.
  - **DB API**: `http://localhost:3002/graphql`
  - **Redis API**: `http://localhost:3002/graphql-redis`

### 2. Frontend Server

#### 가. 경로 이동
```shell
cd FrontEnd/Nextjs/ts_employ_graphql
```

#### 나. 의존성 패키지 설치
```shell
npm install
```

#### 다. 프론트엔드 서버 실행
```shell
npm run dev
```
- 서버가 정상적으로 실행되면 브라우저에서 `http://localhost:3000` 주소로 접속하여 직원 관리 애플리케이션을 사용할 수 있습니다.