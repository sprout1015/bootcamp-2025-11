# GraphQL 기반 Spring Boot 애플리케이션

이 프로젝트는 `FrontEnd/Nextjs/ts_employ_graphql/src/redux/api/employeeAPI.ts`와 통신하는 GraphQL 기반의 Spring Boot 백엔드 애플리케이션입니다. 현업 수준의 아키텍처를 적용하여 GraphQL 서비스를 구현하였습니다.

## 📚 1. 도메인 모델

-   **Employee**: 직원 정보를 관리하는 핵심 도메인입니다.

---

## 🏗️ 2. 아키텍처 (Layered Architecture for GraphQL)

이 프로젝트는 계층형 아키텍처를 적용하여 각 관심사를 분리하고 유지보수성 및 확장성을 높였습니다.

```mermaid
graph TD
    A[Client (Frontend)] -- GraphQL Request --> B(Interfaces Layer);
    B -- Calls Application Service --> C(Application Layer);
    C -- Interacts with Domain --> D(Domain Layer);
    C -- Uses Persistence --> E(Infrastructure Layer);
    E -- Communicates --> D;

    subgraph " "
        direction LR
        B
        C
        D
        E
    end

    style B fill:#E6F3FF,stroke:#B3D9FF
    style C fill:#E6FFE6,stroke:#B3FFB3
    style D fill:#FFF5E6,stroke:#FFD9B3
    style E fill:#F0E6FF,stroke:#D1B3FF

```

### 🧩 계층별 역할

1.  **Interfaces Layer (GraphQL Resolver)**
    -   **역할**: GraphQL 쿼리(Query) 및 뮤테이션(Mutation) 요청을 수신하고 응답을 반환합니다. 클라이언트의 요청을 애플리케이션 서비스로 위임하며, GraphQL 스키마에 정의된 타입과 애플리케이션 계층의 DTO 간 변환을 담당합니다.
    -   **위치**: `com.employee.employeewithgraphql.interfaces.resolver`

2.  **Application Layer (응용 계층)**
    -   **역할**: 애플리케이션의 유스케이스(Use Case)를 구현하고 비즈니스 로직을 오케스트레이션합니다. 도메인 객체와 인프라스트럭처 계층을 사용하여 비즈니스 로직을 조정하고, 트랜잭션의 경계를 설정합니다.
    -   **구현**: `@Service` 어노테이션을 사용한 서비스 클래스. `@Transactional`을 통해 트랜잭션 관리를 담당합니다.
    -   **위치**: `com.employee.employeewithgraphql.application.service`

3.  **Domain Layer (도메인 계층)**
    -   **역할**: 애플리케이션의 핵심 비즈니스 로직과 규칙을 포함합니다. 이 계층은 다른 계층에 대한 의존성이 없는 순수한 비즈니스 모델이어야 합니다.
    -   **구현**:
        -   **Model**: 비즈니스 상태와 행위를 가진 `Employee` 엔티티.
        -   **Repository**: 도메인 객체의 영속성을 위한 계약(추상화)을 정의하는 `EmployeeRepository` 인터페이스.
    -   **위치**: `com.employee.employeewithgraphql.domain.model`, `com.employee.employeewithgraphql.domain.repository`

4.  **Infrastructure Layer (인프라 계층)**
    -   **역할**: 상위 계층(주로 도메인 계층)에서 정의한 인터페이스를 기술적으로 구현합니다. 데이터베이스 연동, 외부 API 호출 등을 담당합니다.
    -   **구현**: Spring Data JPA를 사용한 리포지토리 구현체 (`EmployeeJpaRepository`).
    -   **위치**: `com.employee.employeewithgraphql.infrastructure.persistence`

---

## 💡 3. 구현 상세 및 GraphQL 고려 사항

### 1. `Employee` 도메인 엔티티 (`domain/model/Employee.java`)

-   `@Entity`, `@Getter`, `@Builder`, `protected @NoArgsConstructor`를 사용하여 JPA 엔티티로서의 안정성과 DDD 원칙을 준수합니다.
-   엔티티 내부에서 상태 변경 메서드(`update`)를 제공하여 데이터의 일관성을 유지합니다.

### 2. GraphQL 입력 및 출력 DTO

-   **`EmployeeInput` (`graphql/EmployeeInput.java`)**: GraphQL `input` 타입에 직접 매핑되는 레코드입니다. 클라이언트로부터 데이터를 받을 때 사용됩니다.
-   **`EmployeeDto` (`application/dto/EmployeeDto.java`)**: `Employee` 엔티티를 GraphQL `type`에 맞게 변환하여 클라이언트에 제공하는 출력용 DTO입니다. 도메인 엔티티의 직접적인 노출을 방지합니다.

### 3. GraphQL Resolver (`interfaces/resolver/EmployeeGraphQLResolver.java`)

-   `@Controller`와 `@RequiredArgsConstructor`를 사용하여 Spring Bean으로 등록하고 `EmployeeService`를 주입받습니다.
-   `@QueryMapping` 및 `@MutationMapping` 어노테이션을 사용하여 GraphQL 스키마의 쿼리 및 뮤테이션 필드를 구현합니다.
-   모든 비즈니스 로직은 `EmployeeService`에 위임합니다. `@Argument`를 사용하여 GraphQL 인자들을 메서드 파라미터로 받습니다.

### 4. `FrontEnd/Nextjs/ts_employ_graphql/src/redux/api/employeeAPI.ts`와의 통신

-   프론트엔드의 `employeeAPI.ts`는 이 백엔드의 GraphQL 엔드포인트(`http://localhost:8080/graphql`)로 GraphQL 쿼리/뮤테이션 요청을 보냅니다.
-   백엔드에서는 `schema.graphqls`에 정의된 스키마에 따라 요청을 처리하고, `EmployeeDto` 형태의 응답을 반환합니다.
-   `ID!` 타입은 GraphQL에서 고유 식별자를 나타내며, 백엔드에서는 `Long` 타입으로 매핑됩니다.

---

## 🚀 4. GraphQL API 명세서

### 스키마 정의 (`schema.graphqls`)

```graphql
type Employee {
    id: ID!
    name: String!
    age: Int!
    job: String!
    language: String!
    pay: Int!
}

input EmployeeInput {
    name: String!
    age: Int!
    job: String!
    language: String!
    pay: Int!
}

type Query {
    getEmployeeList: [Employee!]!
    getEmployeeById(id: ID!): Employee
}

type Mutation {
    createEmployee(input: EmployeeInput!): Employee!
    updateEmployee(id: ID!, input: EmployeeInput!): Employee!
    deleteEmployee(id: ID!): Boolean!
}
```

### Query 필드

| 필드              | 설명                 | 인자                    | 반환 타입      |
| :---------------- | :------------------- | :---------------------- | :------------- |
| `getEmployeeList` | 모든 직원 목록 조회 | -                       | `[Employee!]!` |
| `getEmployeeById` | 특정 직원 조회     | `id: ID!`               | `Employee`     |

### Mutation 필드

| 필드            | 설명               | 인자                           | 반환 타입    |
| :-------------- | :----------------- | :----------------------------- | :----------- |
| `createEmployee` | 새 직원 등록     | `input: EmployeeInput!`        | `Employee!`  |
| `updateEmployee` | 직원 정보 업데이트 | `id: ID!, input: EmployeeInput!` | `Employee!`  |
| `deleteEmployee` | 직원 삭제         | `id: ID!`                      | `Boolean!`  |

---

## 5. 트러블슈팅 및 설정 (Troubleshooting & Configuration)

### 1. GraphQL 엔드포인트

-   Spring Boot GraphQL 애플리케이션의 기본 GraphQL 엔드포인트는 `/graphql` 입니다.
-   `http://localhost:8080/graphql` 로 접근해야 합니다. (URL에 오타가 없는지 확인해주세요, 예: `grpahql`이 아닌 `graphql`)

### 2. CORS (Cross-Origin Resource Sharing) 설정

-   프론트엔드(예: `http://localhost:3000`, `http://localhost:3002`)와 백엔드(`http://localhost:8080`)가 다른 도메인 또는 포트에서 실행될 때, 브라우저는 보안상의 이유로 CORS 정책을 적용하여 요청을 차단할 수 있습니다.
-   이 프로젝트에서는 `WebConfig.java`를 통해 프로그래밍 방식으로 CORS를 설정합니다.

```java
// BackEnd/java/employee-with-graphql/src/main/java/com/employee/employeewithgraphql/config/WebConfig.java
package com.employee.employeewithgraphql.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebConfig {

    @Bean
    public WebMvcConfigurer corsConfigurer() {
        return new WebMvcConfigurer() {
            @Override
            public void addCorsMappings(CorsRegistry registry) {
                registry.addMapping("/graphql")
                        .allowedOrigins("http://localhost:3000", "http://localhost:3001") // 프론트엔드 Origin 허용
                        .allowedMethods("POST"); // GraphQL은 주로 POST 요청을 사용합니다.
            }
        };
    }
}
```
---

## 6. Docker를 이용한 배포 (Deployment with Docker)

### 1. Docker 이미지 빌드

프로젝트 루트 디렉토리에서 다음 명령어를 실행하여 Docker 이미지를 빌드합니다:

```bash
docker build -t employee-graphql-app .
```

### 2. Docker 컨테이너 실행

빌드된 이미지를 사용하여 Docker 컨테이너를 실행합니다. 애플리케이션은 8080 포트를 사용합니다.

```bash
docker run -p 8080:8080 employee-graphql-app
```

이제 Docker 컨테이너에서 애플리케이션이 실행되며, `http://localhost:8080/graphql` 또는 `http://localhost:8080/graphiql`로 접근할 수 있습니다.