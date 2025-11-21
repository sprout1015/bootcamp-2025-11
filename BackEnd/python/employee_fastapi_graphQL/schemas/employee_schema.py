# schemas/employee_schema.py
import strawberry
from models.employee import Employee as EmployeeModel

# --- GraphQL 스키마 정의 (Java의 DTO와 유사) ---
# Strawberry를 사용하여 API의 데이터 형태를 정의합니다.
# 클라이언트와 서버는 이 스키마를 기준으로 데이터를 주고받습니다.

@strawberry.type
class Employee:
    """
    GraphQL 쿼리를 통해 클라이언트에 반환될 직원 데이터의 형태를 정의합니다. (Output DTO)
    """
    id: strawberry.ID
    name: str
    age: int
    job: str
    language: str
    pay: int

@strawberry.input
class EmployeeInput:
    """
    GraphQL 뮤테이션(생성, 수정)을 통해 클라이언트로부터 입력받을 데이터의 형태를 정의합니다. (Input DTO)
    """
    name: str
    age: int
    job: str
    language: str
    pay: int

def orm_to_graphql(emp: EmployeeModel) -> Employee:
    """
    SQLAlchemy ORM 모델 객체(EmployeeModel)를 GraphQL 스키마 객체(Employee)로 변환하는 유틸리티 함수입니다.
    데이터베이스 계층의 모델과 API 계층의 스키마를 분리해줍니다.
    """
    return Employee(
        id=strawberry.ID(str(emp.id)),
        name=emp.name,
        age=emp.age,
        job=emp.job,
        language=emp.language,
        pay=emp.pay
    )


def redis_to_graphql(emp_id:int, emp: dict) -> Employee:
    """
    Redis 내부 Key를 기반으로 존재하는 객체를 GraphQL 스키마 객체(Employee)로 변환하는 유틸리티 함수입니다.
    데이터베이스 계층의 모델과 API 계층의 스키마를 분리해줍니다.
    """
    return Employee(
        id=strawberry.ID(str(emp_id)),
        name=emp.name,
        age=emp.age,
        job=emp.job,
        language=emp.language,
        pay=emp.pay
    )