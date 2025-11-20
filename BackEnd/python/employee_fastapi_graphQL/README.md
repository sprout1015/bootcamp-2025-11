# FastAPI와 GraphQL(Strawberry)을 이용한 직원 관리 API

본 프로젝트는 `FastAPI`와 `strawberry` 라이브러리를 사용하여 GraphQL API를 구축한 간단한 직원 관리 CRUD 예제입니다.

## 1. GraphQL 사용의 이점

GraphQL은 API를 위한 쿼리 언어이자 런타임으로, 기존의 REST API가 가진 몇 가지 한계점을 해결합니다.

- **오버-페칭(Over-fetching) 및 언더-페칭(Under-fetching) 해결**:
  - 클라이언트가 API로부터 필요한 데이터만 정확하게 지정하여 요청할 수 있습니다. REST API처럼 정해진 규격의 데이터를 모두 받거나(오버-페칭), 원하는 정보를 얻기 위해 여러 번 요청을 보내지(언더-페칭) 않아도 됩니다.

- **강력한 타입 시스템 (Strongly Typed Schema)**:
  - API의 모든 데이터 구조는 스키마에 명확하게 정의됩니다. 이는 서버와 클라이언트 간의 약속 역할을 하며, 개발 과정에서 타입 체크, 자동 완성 등의 이점을 제공하여 생산성을 높입니다.

- **단일 엔드포인트 (Single Endpoint)**:
  - 일반적으로 모든 요청이 `/graphql`과 같은 단일 엔드포인트로 전송됩니다. 여러 개의 복잡한 URL을 관리할 필요가 없어 API 관리가 단순해집니다.

- **API 진화의 용이성**:
  - 기존 클라이언트를 손상시키지 않고 새로운 필드나 타입을 스키마에 추가하는 것이 매우 쉽습니다.

## 2. 주요 코드 설명 (`main.py`)

- **`@strawberry.type`**
  ```python
  @strawberry.type
  class Employee:
      id: strawberry.ID
      name: str
      # ...
  ```
  GraphQL 스키마의 객체 타입(`type Employee { ... }`)을 정의합니다. 이는 클라이언트가 조회할 수 있는 데이터의 모델(구조)을 나타냅니다.

- **`@strawberry.input`**
  ```python
  @strawberry.input
  class EmployeeInput:
      name: str
      age: int
      # ...
  ```
  데이터 생성(Create)이나 수정(Update) 시 사용될 입력 타입(`input EmployeeInput { ... }`)을 정의합니다. 여러 개의 필드를 하나의 객체로 묶어 뮤테이션(Mutation)의 인자로 전달할 때 유용합니다.

- **`@strawberry.type class Query:`**
  ```python
  @strawberry.type
  class Query:
      @strawberry.field
      def employees(self) -> List[Employee]:
          return EMPLOYEELIST
  ```
  데이터를 **조회(Read)**하는 모든 오퍼레이션을 그룹화합니다. `@strawberry.field` 데코레이터가 붙은 메서드는 GraphQL 스키마의 쿼리 필드가 됩니다. 위 코드에서는 모든 직원 목록을 반환하는 `employees` 쿼리를 정의합니다.

- **`@strawberry.type class Mutation:`**
  ```python
  @strawberry.type
  class Mutation:
      @strawberry.mutation
      def register_employee(self, input: EmployeeInput) -> Employee:
          # ...
  ```
  데이터를 **변경(Create, Update, Delete)**하는 모든 오퍼레이션을 그룹화합니다. `@strawberry.mutation` 데코레이터가 붙은 메서드는 스키마의 뮤테이션 필드가 됩니다. 위 예시는 직원을 등록하는 `register_employee` 뮤테이션을 정의합니다.

- **`GraphQLRouter` 와 `FastAPI` 연동**
  ```python
  schema = strawberry.Schema(query=Query, mutation=Mutation)
  graphql_app = GraphQLRouter(schema)
  # ...
  app.include_router(graphql_app, prefix="/graphql")
  ```
  정의된 `Query`와 `Mutation`으로 `strawberry.Schema`를 생성하고, 이를 `GraphQLRouter`에 연결합니다. 마지막으로 `FastAPI` 앱에 이 라우터를 포함시켜 `/graphql` 경로로 GraphQL API를 제공합니다.

## 3. 패키지 설치

```shell
pip install -r requirements.txt
```

## 4. 서버 실행

```shell
uvicorn main:app --reload --port 3002
```
서버가 실행되면 [http://127.0.0.1:3002/graphql](http://127.0.0.1:3002/graphql) 주소로 접속하여 GraphQL API를 테스트할 수 있습니다.

## 5. GraphQL 쿼리 예시

### 전체 직원 조회 (Query)

```graphql
query {
  employees {
    id
    name
    age
    job
    language
    pay
  }
}
```

### 직원 등록 (Mutation - POST)

```graphql
mutation {
  register_employee(
    input: {
      name: "Taylor"
      age: 29
      job: "backend"
      language: "python"
      pay: 410
    }
  ) {
    id
    name
    age
    job
    language
    pay
  }
}
```

### 직원 정보 수정 (Mutation - PUT)

```graphql
mutation {
  update_employee(
    id: "2"
    input: {
      name: "Peter"
      age: 30
      job: "backend"
      language: "java"
      pay: 350
    }
  ) {
    id
    name
    age
    job
    language
    pay
  }
}
```

### 직원 삭제 (Mutation - DELETE)

```graphql
mutation {
  delete_employee(id: "3")
}
```