# api/employee_resolver.py
from typing import List
import strawberry
from strawberry.types import Info

from core.context import CustomContext
from schemas.employee_schema import Employee, EmployeeInput

# --- API 계층 (GraphQL Resolvers) ---
# Java의 Controller와 유사한 역할을 합니다.
# 클라이언트의 요청을 받아 적절한 서비스 메서드를 호출하고, 그 결과를 반환합니다.

@strawberry.type
class Query:
    """GraphQL API의 모든 조회(Query) 연산을 정의하는 클래스"""

    @strawberry.field
    def get_employee_list(self, info: Info[CustomContext, None]) -> List[Employee]:
        """모든 직원 목록을 반환하는 리졸버"""
        # info.context를 통해 CustomContext 객체에 접근하고,
        # context 내부의 employee_service를 호출하여 비즈니스 로직을 수행합니다.
        return info.context.employee_service.get_all_employees()

    @strawberry.field
    def get_employee_by_id(self, id: int, info: Info[CustomContext, None]) -> Employee:
        """ID로 특정 직원을 조회하는 리졸버"""
        return info.context.employee_service.get_employee_by_id(id)

@strawberry.type
class Mutation:
    """GraphQL API의 모든 변경(Mutation) 연산을 정의하는 클래스"""

    @strawberry.mutation
    def register_employee(self, input: EmployeeInput, info: Info[CustomContext, None]) -> Employee:
        """새로운 직원을 등록하는 리졸버"""
        return info.context.employee_service.create_employee(input)

    @strawberry.mutation
    def update_employee(self, id: strawberry.ID, input: EmployeeInput, info: Info[CustomContext, None]) -> Employee:
        """직원 정보를 수정하는 리졸버"""
        # GraphQL의 ID 타입을 Python의 int 타입으로 변환하여 서비스 계층에 전달
        return info.context.employee_service.update_employee(int(id), input)

    @strawberry.mutation
    def delete_employee(self, id: strawberry.ID, info: Info[CustomContext, None]) -> strawberry.ID:
        """직원을 삭제하는 리졸버"""
        deleted_id = info.context.employee_service.delete_employee(int(id))
        # 성공적으로 삭제된 ID를 다시 GraphQL ID 타입으로 변환하여 반환
        return strawberry.ID(str(deleted_id))
