# core/context.py
from functools import cached_property
from sqlalchemy.orm import Session
from strawberry.fastapi import BaseContext
from services.employee_service import EmployeeService

class CustomContext(BaseContext):
    """
    모든 GraphQL 리졸버에 전달될 커스텀 Context 클래스입니다.
    Strawberry는 API 요청이 들어올 때마다 이 클래스의 인스턴스를 생성하며,
    이 인스턴스는 DB 세션과 비즈니스 로직을 처리하는 서비스 객체를 담는 역할을 합니다.
    """
    def __init__(self, db: Session):
        """
        Context가 생성될 때 FastAPI의 의존성 주입 시스템으로부터 DB 세션을 받습니다.
        """
        self.db = db

    @cached_property
    def employee_service(self) -> EmployeeService:
        """
        요청 처리 중에 EmployeeService에 대한 접근이 처음 발생할 때 인스턴스를 생성하고,
        이후 동일한 요청 내에서는 생성된 인스턴스를 계속 반환합니다. (요청당 하나의 서비스 인스턴스)
        
        @cached_property는 이 메서드를 일반 프로퍼티처럼 호출할 수 있게 해줍니다. (예: context.employee_service)
        """
        return EmployeeService(self.db)