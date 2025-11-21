# Project Overview

This project is a full-stack employee management application created for learning purposes.

- **Primary Goal:** To practice and understand the integration of React, Redux, Python, FastAPI, GraphQL, and PostgreSQL.

---

## 1. Backend

-   **Path:** `BackEnd/python/employee_fastapi_graphQL/`
-   **Stack:** Python, FastAPI, Strawberry (for GraphQL), SQLAlchemy (ORM), PostgreSQL.
-   **Purpose:** Provides a GraphQL API for CRUD (Create, Read, Update, Delete) operations on employee data.
-   **Architecture:** Follows a 3-tier architecture (API Resolvers, Services, Repositories) for clear separation of concerns.
-   **Key Endpoint:** The GraphQL API is served at `http://localhost:3002/graphql`.
-   **Database:** Uses PostgreSQL for data persistence. Tables are automatically created on application startup.

## 2. Frontend

-   **Path:** `FrontEnd/Nextjs/ts_employ_graphql/`
-   **Stack:** Next.js (App Router), React, TypeScript, Redux Toolkit, Axios, Tailwind CSS.
-   **Purpose:** A web-based user interface for interacting with the backend API to manage employees.
-   **Architecture:** A standard Next.js project structure with client-side components. It uses Redux Toolkit for centralized state management, including handling the state of API interactions (loading, success, error).
-   **API Communication:** It communicates with the backend GraphQL API at `http://localhost:3002/graphql` using `axios`. Redux Toolkit's `createAsyncThunk` is used to manage these asynchronous API calls.

---

## 3. Development Conventions

### Commit Message Policy
- Commit messages should be written with an English prefix followed by a Korean description.
- Example: `feat(redis): 독립적인 Redis 서비스 계층 추가`
