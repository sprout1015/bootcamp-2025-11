# services/employee_redis_service.py
from typing import List
from redis.asyncio import Redis
from schemas.employee_schema import Employee, EmployeeInput
from repository.employee_redis_repository import EmployeeRedisRepository

def dict_to_employee(data: dict) -> Employee:
    """Redis에서 가져온 딕셔너리를 Employee GraphQL 스키마 객체로 변환합니다."""
    if not data:
        return None
    return Employee(
        id=str(data.get('id')),
        name=data.get('name'),
        age=int(data.get('age')),
        job=data.get('job'),
        language=data.get('language'),
        pay=int(data.get('pay'))
    )

class EmployeeRedisService:
    def __init__(self, redis: Redis):
        self.repo = EmployeeRedisRepository(redis)

    async def init_redis_data(self):
        """리포지토리를 통해 Redis 데이터를 초기화합니다."""
        await self.repo.initialize_data()

    async def get_all_employees(self) -> List[Employee]:
        """모든 직원 목록을 조회합니다."""
        all_employees_data = await self.repo.get_all()
        return [dict_to_employee(data) for data in all_employees_data]

    async def get_employee_by_id(self, emp_id: int) -> Employee:
        """ID로 특정 직원을 조회합니다."""
        employee_data = await self.repo.get_by_id(emp_id)
        if not employee_data:
            raise ValueError(f"직원을 찾을 수 없습니다 (ID: {emp_id})")
        
        employee_data['id'] = emp_id # hgetall은 키를 반환하지 않으므로 id 주입
        return dict_to_employee(employee_data)

    async def create_employee(self, input: EmployeeInput) -> Employee:
        """새로운 직원을 등록합니다."""
        created_data = await self.repo.create(input)
        return dict_to_employee(created_data)

    async def update_employee(self, emp_id: int, input: EmployeeInput) -> Employee:
        """직원 정보를 수정합니다."""
        updated_data = await self.repo.update(emp_id, input)
        if updated_data is None:
            raise ValueError(f"직원을 찾을 수 없습니다 (ID: {emp_id})")
        return dict_to_employee(updated_data)

    async def delete_employee(self, emp_id: int) -> int:
        """직원을 삭제합니다."""
        deleted_id = await self.repo.delete(emp_id)
        if deleted_id == 0:
            raise ValueError(f"직원을 찾을 수 없습니다 (ID: {emp_id})")
        return deleted_id