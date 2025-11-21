from typing import List

import strawberry
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter


@strawberry.type
class Employee:
    id: strawberry.ID
    name: str
    age: int
    job: str
    language: str
    pay: int

@strawberry.input
class EmployeeInput:
    name: str
    age: int
    job: str
    language: str
    pay: int

EMPLOYEELIST: List[Employee] = [
    Employee(id=1, name="John", age=35, job="frontend", language="react", pay=12),
    Employee(id=2, name="Qohn", age=15, job="backend", language="java", pay=13),
    Employee(id=3, name="Wohn", age=25, job="AI", language="python", pay=41),
    Employee(id=4, name="Eohn", age=552, job="Infra", language="AWS", pay=51),
    Employee(id=5, name="2222", age=2222, job="2222", language="2222", pay=2222)
]

@strawberry.type
class Query:
    @strawberry.field
    def get_employee_list(self) -> List[Employee]:
        return EMPLOYEELIST

    @strawberry.field
    def get_employee_by_id(self, input: int) -> Employee:
        result = next((item for item in EMPLOYEELIST if item.id == str(input)), None)
        return result

@strawberry.type
class Mutation:
    @strawberry.mutation
    def register_employee(self, input: EmployeeInput) -> Employee:
        # Employee 등록하는 곳
        new_id = str(len(EMPLOYEELIST) + 1)
        new_emp = Employee(
            id=new_id,
            name=input.name,
            age=input.age,
            job=input.job,
            language=input.language,
            pay=input.pay
        )
        EMPLOYEELIST.append(new_emp)
        return new_emp

    @strawberry.mutation
    def update_employee(self, id:strawberry.ID, input: EmployeeInput) -> Employee:
        # 수정 쿼리
        for idx, emp in enumerate(EMPLOYEELIST):
            if emp.id == id:
                update = Employee(
                    id = emp.id,
                    name = input.name,
                    age = input.age,
                    job = input.job,
                    language = input.language,
                    pay = input.pay
                )
                EMPLOYEELIST[idx] = update
                return update
        # 예외처리
        raise ValueError("Employee not found")

    @strawberry.mutation
    def delete_employee(self, id:strawberry.ID) -> strawberry.ID:
        global EMPLOYEELIST
        # filter 함수와 유사
        EMPLOYEELIST = [e for e in EMPLOYEELIST if e.id != id]
        return id

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.254.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
async def root():
    return {"message": "Hello FastAPI"}