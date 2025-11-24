# models/employee.py
from sqlalchemy import Column, Integer, String
from core.database import Base

class Employee(Base):
    """
    직원 정보를 나타내는 SQLAlchemy ORM 모델 클래스입니다.
    데이터베이스의 'employees' 테이블과 매핑됩니다.
    """
    
    # __tablename__: 데이터베이스에 매핑될 테이블의 이름을 지정합니다.
    __tablename__ = "employees"

    # Column: 각 속성이 테이블의 어떤 컬럼에 해당하는지 정의합니다.
    id = Column(Integer, primary_key=True, index=True)  # 기본 키 및 인덱스 설정
    name = Column(String(100), nullable=False)          # null을 허용하지 않는 문자열 컬럼
    age = Column(Integer, nullable=False)
    job = Column(String(100), nullable=False)
    language = Column(String(100))
    pay = Column(Integer, nullable=False)