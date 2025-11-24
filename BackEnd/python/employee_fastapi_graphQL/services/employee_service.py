# services/employee_service.py
from typing import List
from sqlalchemy.orm import Session
from repository.employee_repository import EmployeeRepository
from schemas.employee_schema import Employee, EmployeeInput, orm_to_graphql

class EmployeeService:
    """
    비즈니스 로직을 처리하는 서비스 계층입니다.
    API 계층(resolver)과 데이터 영속성 계층(repository) 사이의 중재자 역할을 합니다.
    HTTP 요청의 세부사항이나 DB 접근 방식에 대해 알지 못하며, 오직 비즈니스 규칙에만 집중합니다.
    """
    def __init__(self, db: Session):
        """
        Context로부터 DB 세션을 주입받아 Repository 객체를 생성합니다.
        """
        self.repo = EmployeeRepository(db)

    def get_all_employees(self) -> List[Employee]:
        """모든 직원 목록을 조회하는 비즈니스 로직"""
        employees_orm = self.repo.get_all_employees()
        # ORM 모델 리스트를 GraphQL 스키마 객체 리스트로 변환하여 반환
        return [orm_to_graphql(emp) for emp in employees_orm]

    def get_employee_by_id(self, emp_id: int) -> Employee:
        """ID로 직원을 조회하는 비즈니스 로직"""
        employee_orm = self.repo.get_employee_by_id(emp_id)
        if employee_orm is None:
            raise ValueError(f"직원을 찾을 수 없습니다 (ID: {emp_id})")
        return orm_to_graphql(employee_orm)

    def create_employee(self, input: EmployeeInput) -> Employee:
        """직원을 등록하는 비즈니스 로직"""
        employee_orm = self.repo.create_employee(input)
        return orm_to_graphql(employee_orm)

    def update_employee(self, emp_id: int, input: EmployeeInput) -> Employee:
        """직원 정보를 수정하는 비즈니스 로직"""
        employee_orm = self.repo.update_employee(emp_id, input)
        if employee_orm is None:
            raise ValueError(f"직원을 찾을 수 없습니다 (ID: {emp_id})")
        return orm_to_graphql(employee_orm)

    def delete_employee(self, emp_id: int) -> int:
        """직원을 삭제하는 비즈니스 로직"""
        deleted_id = self.repo.delete_employee(emp_id)
        if deleted_id is None:
            raise ValueError(f"직원을 찾을 수 없습니다 (ID: {emp_id})")
        return deleted_id
    
    def init_db_data(self):
        """샘플 데이터를 초기화하는 로직"""
        self.repo.init_sample_data()