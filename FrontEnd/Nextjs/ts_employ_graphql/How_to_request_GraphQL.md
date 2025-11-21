# React/Next.js에서 GraphQL API를 요청하는 방법

이 문서는 `axios` 라이브러리를 사용하여 React 또는 Next.js 애플리케이션에서 GraphQL API와 통신하는 기본적인 방법을 설명합니다.

## 1. GraphQL 요청의 기본 구조

GraphQL은 일반적으로 단일 엔드포인트(예: `/graphql`)를 통해 모든 요청을 처리합니다. REST API처럼 작업 종류(조회, 생성, 수정, 삭제)에 따라 다른 URL을 사용하지 않습니다.

요청은 항상 `POST` HTTP 메서드를 사용하며, 요청 본문(body)은 다음과 같은 JSON 구조를 가집니다.

```json
{
  "query": "...",
  "variables": { ... }
}
```

- **`query`**: 실행하려는 GraphQL 쿼리 또는 뮤테이션을 담는 문자열입니다.
- **`variables`**: 쿼리나 뮤테이션에 동적인 값을 전달할 때 사용하는 객체입니다. (선택 사항)

## 2. Axios를 이용한 요청 예제

### 기본 설정

먼저 `axios` 인스턴스를 설정하거나, 요청을 보낼 때마다 API의 전체 URL을 포함해야 합니다.

```typescript
import axios from 'axios';

const API_URL = "http://localhost:3002/graphql";

const graphqlRequest = async (query: string, variables?: object) => {
    try {
        const response = await axios.post(API_URL, {
            query,
            variables,
        });

        if (response.data.errors) {
            throw new Error(response.data.errors.map((err: any) => err.message).join(', '));
        }

        return response.data.data;
    } catch (error: any) {
        console.error("GraphQL 요청 중 오류 발생:", error);
        throw error;
    }
};
```
이 헬퍼 함수는 반복적인 `axios` 호출 코드를 줄여주고, GraphQL 에러를 일관되게 처리하는 데 도움을 줍니다.

### 데이터 조회 (Query)

모든 직원 목록을 가져오는 예제입니다.

```typescript
const fetchAllEmployees = async () => {
    const query = `
        query {
            getEmployeeList {
                id
                name
                job
            }
        }
    `;
    
    const data = await graphqlRequest(query);
    console.log(data.getEmployeeList); // [{ id: '1', name: 'John', job: 'frontend' }, ...]
};
```
- `query` 타입으로 요청을 시작하고, 필요한 필드(`id`, `name`, `job`)만 지정하여 요청합니다.
- 변수가 필요 없으므로 `graphqlRequest` 함수에 `query`만 전달합니다.

### 데이터 생성 (Mutation with Variables)

새로운 직원을 등록하는 예제입니다. 동적인 값을 전달하기 위해 `variables`를 사용합니다.

#### **주의: 데이터 타입 전처리**
GraphQL 스키마는 강력한 타입 시스템을 가지고 있습니다. 예를 들어, 스키마에 `age: Int`라고 정의되어 있다면, 클라이언트는 반드시 숫자 형태의 `age` 값을 보내야 합니다. 폼(form) 입력값은 종종 문자열(`string`)로 처리되므로, API 요청을 보내기 전에 `Number()` 등을 사용하여 올바른 타입으로 변환하는 과정이 필요합니다.

```typescript
const registerNewEmployee = async (formData: any) => {
    // $input: EmployeeInput! : 변수($input)의 타입(EmployeeInput!)을 정의합니다.
    // registerEmployee(input: $input): 뮤테이션을 실행하며 인자로 변수를 전달합니다.
    const mutation = `
        mutation RegisterEmployee($input: EmployeeInput!) {
            registerEmployee(input: $input) {
                id
                name
            }
        }
    `;
    
    // API 스키마에 맞게 타입을 변환하고, 불필요한 필드는 제거합니다.
    const variables = {
        input: {
            name: formData.name,
            age: Number(formData.age), // 문자열일 수 있는 값을 숫자로 변환
            job: formData.job,
            language: formData.language,
            pay: Number(formData.pay) // 문자열일 수 있는 값을 숫자로 변환
        }
    };
    
    const data = await graphqlRequest(mutation, variables);
    console.log("새로 등록된 직원:", data.registerEmployee);
};
```
- `mutation` 타입으로 요청을 시작하고, 쿼리에 사용될 변수(`$input`)를 정의합니다.
- `graphqlRequest` 함수를 호출할 때, 두 번째 인자로 실제 값을 담은 `variables` 객체를 전달합니다.

## 3. Apollo Client와 같은 라이브러리 사용

`axios`나 `fetch`는 GraphQL 요청을 보내는 데 충분하지만, 실제 프로덕션 환경에서는 다음과 같은 기능을 제공하는 특화된 라이브러리를 사용하는 것이 더 효율적일 수 있습니다.

- **[Apollo Client](https://www.apollographql.com/docs/react/)**: 캐싱, 로딩 및 에러 상태 관리, UI와 데이터 동기화 등 강력한 기능을 제공합니다.
- **[React Query](https://tanstack.com/query/latest)**: 서버 상태 관리에 특화되어 있으며, 간단한 설정으로 GraphQL 요청을 통합할 수 있습니다.
- **[graphql-request](https://github.com/prisma-labs/graphql-request)**: `axios`보다 가볍고 GraphQL에 최적화된 간단한 클라이언트입니다.

이러한 라이브러리들은 반복적인 코드 작성을 줄여주고, 애플리케이션의 성능과 안정성을 높이는 데 도움을 줍니다.