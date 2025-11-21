# repository/employee_repository.py
from typing import List
from sqlalchemy.orm import Session
from models.employee import Employee as EmployeeModel
from schemas.employee_schema import EmployeeInput

class EmployeeRepository:
    """
    데이터 영속성 계층(Persistence Layer)입니다.
    데이터베이스에 대한 CRUD(Create, Read, Update, Delete) 연산을 직접 수행합니다.
    Java의 DAO(Data Access Object) 또는 JPA Repository와 동일한 역할을 합니다.
    """
    def __init__(self, db: Session):
        """
        서비스 계층으로부터 DB 세션(db: Session)을 주입받습니다.
        """
        self.db = db

    def get_all_employees(self) -> List[EmployeeModel]:
        """모든 직원 정보를 조회합니다."""
        return self.db.query(EmployeeModel).all()

    def get_employee_by_id(self, emp_id: int) -> EmployeeModel | None:
        """ID를 기준으로 특정 직원 정보를 조회합니다."""
        return self.db.query(EmployeeModel).filter(EmployeeModel.id == emp_id).first()

    def create_employee(self, input: EmployeeInput) -> EmployeeModel:
        """새로운 직원 정보를 데이터베이스에 생성합니다."""
        new_emp = EmployeeModel(**input.__dict__)
        self.db.add(new_emp)
        self.db.commit()
        self.db.refresh(new_emp)  # DB에서 생성된 정보를 객체에 다시 로드 (예: auto-increment ID)
        return new_emp

    def update_employee(self, emp_id: int, input: EmployeeInput) -> EmployeeModel | None:
        """ID를 기준으로 특정 직원 정보를 수정합니다."""
        emp = self.get_employee_by_id(emp_id)
        if emp:
            # 입력받은 데이터로 기존 객체의 필드를 업데이트
            emp.name = input.name
            emp.age = input.age
            emp.job = input.job
            emp.language = input.language
            emp.pay = input.pay
            self.db.commit()
            self.db.refresh(emp)
        return emp

    def delete_employee(self, emp_id: int) -> int | None:
        """ID를 기준으로 특정 직원 정보를 삭제합니다."""
        emp = self.get_employee_by_id(emp_id)
        if emp:
            self.db.delete(emp)
            self.db.commit()
            return emp_id
        return None

    def init_sample_data(self):
        """(서버 최초 실행 시) 샘플 데이터를 삽입합니다."""
        if self.db.query(EmployeeModel).count() > 0:
            return

        samples = [
            EmployeeModel(name="John", age=35, job="frontend", language="react", pay=400),
            EmployeeModel(name="Peter", age=28, job="backend", language="java", pay=300),
            EmployeeModel(name="Sue", age=38, job="publisher", language="javascript", pay=400),
            EmployeeModel(name="Susan", age=45, job="pm", language="python", pay=500),
        ]

        self.db.add_all(samples)
        self.db.commit()