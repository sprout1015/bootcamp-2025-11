# FastAPI, GraphQL, PostgreSQL & Redis를 이용한 직원 관리 API

본 프로젝트는 `FastAPI`와 `strawberry` 라이브러리를 사용하여 GraphQL API를 구축한 직원 관리 CRUD 예제입니다.

이 프로젝트는 두 가지 독립적인 데이터 소스를 사용합니다:
1.  **PostgreSQL**: `SQLAlchemy` ORM을 통해 데이터베이스와 연동됩니다.
2.  **Redis**: 데이터베이스와 무관하게 자체적으로 데이터를 관리하는 독립적인 API를 제공합니다.

---

## 1. 아키텍처 (3-Tier Architecture)

이 프로젝트는 역할별로 코드를 분리하여 구조화했습니다. 특히 Redis 관련 기능은 기존 코드(`employee_*.py`)를 수정하지 않고 별도의 파일(`employee_redis_*.py`)로 구현되었습니다.

```
employee_fastapi_graphQL/
├── .env                  # 환경 변수 설정 (DB, Redis 접속 정보)
├── main.py               # FastAPI 앱 초기화, 라우팅 및 실행
├── requirements.txt      # 의존성 패키지 목록
├── api/
│   ├── employee_resolver.py      # [DB용] GraphQL Query/Mutation 정의
│   └── employee_redis_resolver.py # [Redis용] GraphQL Query/Mutation 정의
├── core/
│   ├── database.py             # [DB용] DB 연결 설정
│   ├── redis_client.py         # [Redis용] Redis 연결 설정
│   └── context.py              # [DB용] GraphQL Context 정의
├── models/
│   └── employee.py             # [DB용] ORM 모델 (Entity)
├── repository/
│   └── employee_repository.py  # [DB용] 데이터 영속성 계층 (DAO)
├── schemas/
│   └── employee_schema.py      # API 스키마 (DTO)
└── services/
    ├── employee_service.py       # [DB용] 비즈니스 로직
    └── employee_redis_service.py  # [Redis용] 비즈니스 로직
```

---

## 2. API 엔드포인트

이 프로젝트는 두 개의 독립적인 GraphQL 엔드포인트를 제공합니다.

### 가. PostgreSQL 기반 API (`/graphql`)
- **특징**: 전통적인 데이터베이스(PostgreSQL)를 사용하는 API입니다. 데이터는 영구적으로 저장됩니다.
- **아키텍처**: `api` -> `services` -> `repository` -> `models` -> `DB` 순서로 데이터를 처리합니다.
- **주소**: [http://127.0.0.1:3002/graphql](http://127.0.0.1:3002/graphql)

### 나. Redis 기반 API (`/graphql-redis`)
- **특징**: In-memory 데이터베이스인 Redis만을 사용하는 API입니다. DB와 완전히 독립적이며, 서버 재시작 시 데이터가 초기화됩니다.
- **아키텍처**: `api` -> `services` -> `Redis` 순서로 데이터를 처리합니다.
- **주소**: [http://127.0.0.1:3002/graphql-redis](http://127.0.0.1:3002/graphql-redis)

---

## 3. 환경 변수 설정 (`.env` 파일)

프로젝트 루트에 `.env` 파일을 생성하고 데이터베이스 및 Redis 접속 정보를 설정해야 합니다.

```
# .env

# PostgreSQL 접속 정보
DATABASE_URL=postgresql://<USER>:<PASSWORD>@<HOST>:<PORT>/<DB_NAME>

# Redis 접속 정보 (선택 사항, 없으면 기본값으로 연결)
REDIS_URL=redis://localhost:6379
```

---

## 4. 실행 방법

**가. 패키지 설치**
```shell
pip install -r requirements.txt
```

**나. 서버 실행**
```shell
uvicorn main:app --reload --port 3002
```
서버가 실행되면 위에서 설명한 두 개의 주소로 각각 접속하여 GraphQL Playground를 통해 API를 테스트할 수 있습니다.

---

## 5. GraphQL 쿼리 예시

### 가. PostgreSQL API (`/graphql`)

#### 전체 직원 조회 (Query)
```graphql
query {
  get_employee_list {
    id
    name
  }
}
```

#### 직원 등록 (Mutation)
```graphql
mutation {
  register_employee(input: {name: "Gildong Hong", age: 30, job: "swordsman", language: "korean", pay: 500}) {
    id
    name
  }
}
```

### 나. Redis API (`/graphql-redis`)

#### 전체 직원 조회 (Query)
```graphql
query {
  get_employees_redis {
    id
    name
    job
  }
}
```

#### 직원 등록 (Mutation)
```graphql
mutation {
  register_employee_redis(input: {name: "Redis Hong", age: 25, job: "cache manager", language: "redis-cli", pay: 7000}) {
    id
    name
  }
}
```

#### 직원 정보 수정 (Mutation)
```graphql
mutation {
  update_employee_redis(id: "1", input: {name: "Updated Redis Hong", age: 26, job: "cache expert", language: "redis-cli", pay: 7500}) {
    id
    name
    age
  }
}
```

#### 직원 삭제 (Mutation)
```graphql
mutation {
  delete_employee_redis(id: "2")
}
```
