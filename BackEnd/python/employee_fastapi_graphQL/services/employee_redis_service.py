# services/employee_redis_service.py
import json
from typing import List
import asyncio
from redis.asyncio import Redis
from schemas.employee_schema import Employee, EmployeeInput

# --- Helper Functions ---
def dict_to_employee(emp_id: int, data: dict) -> Employee:
    """Redis에서 가져온 딕셔너리를 Employee GraphQL 스키마 객체로 변환합니다."""
    return Employee(
        id=str(emp_id),
        name=data.get('name'),
        age=int(data.get('age')),
        job=data.get('job'),
        language=data.get('language'),
        pay=int(data.get('pay'))
    )

class EmployeeRedisService:
    def __init__(self, redis: Redis):
        self.redis = redis
        self.id_counter_key = "employee:id:counter"
        self.all_employees_set_key = "employees:all:set"

    async def init_redis_data(self):
        """애플리케이션 시작 시 Redis에 샘플 데이터를 초기화합니다."""
        # 기존 데이터 초기화
        await self.redis.flushdb()
        
        sample_data = [
            {"name": "Redis-Alice", "age": 30, "job": "Engineer", "language": "Python", "pay": 60000},
            {"name": "Redis-Bob", "age": 25, "job": "Designer", "language": "JavaScript", "pay": 55000},
            {"name": "Redis-Charlie", "age": 35, "job": "Manager", "language": "Go", "pay": 80000},
        ]
        
        # ID 카운터 0으로 설정
        await self.redis.set(self.id_counter_key, "0")

        # 파이프라인으로 샘플 데이터 생성
        pipe = self.redis.pipeline()
        for emp_data in sample_data:
            new_id = await self.redis.incr(self.id_counter_key)
            employee_key = f"employee:{new_id}"
            
            pipe.hset(employee_key, mapping=emp_data)
            pipe.sadd(self.all_employees_set_key, new_id)
        await pipe.execute()
        print("Redis data initialized successfully.")

    async def get_all_employees(self) -> List[Employee]:
        """모든 직원 목록을 조회합니다."""
        employee_ids = await self.redis.smembers(self.all_employees_set_key)
        
        pipe = self.redis.pipeline()
        for emp_id in employee_ids:
            pipe.hgetall(f"employee:{emp_id}")
        
        results = await pipe.execute()
        
        employees = []
        for emp_id, data in zip(employee_ids, results):
            if data:
                employees.append(dict_to_employee(int(emp_id), data))
        return employees

    async def get_employee_by_id(self, emp_id: int) -> Employee:
        """ID로 특정 직원을 조회합니다."""
        data = await self.redis.hgetall(f"employee:{emp_id}")
        if not data:
            raise ValueError(f"직원을 찾을 수 없습니다 (ID: {emp_id})")
        return dict_to_employee(emp_id, data)

    async def create_employee(self, input: EmployeeInput) -> Employee:
        """새로운 직원을 등록합니다."""
        new_id = await self.redis.incr(self.id_counter_key)
        employee_key = f"employee:{new_id}"
        
        pipe = self.redis.pipeline()
        pipe.hset(employee_key, mapping=input.__dict__)
        pipe.sadd(self.all_employees_set_key, new_id)
        await pipe.execute()
        
        # 생성된 객체 반환
        created_data = await self.redis.hgetall(employee_key)
        return dict_to_employee(new_id, created_data)

    async def update_employee(self, emp_id: int, input: EmployeeInput) -> Employee:
        """직원 정보를 수정합니다."""
        employee_key = f"employee:{emp_id}"
        if not await self.redis.exists(employee_key):
             raise ValueError(f"직원을 찾을 수 없습니다 (ID: {emp_id})")

        await self.redis.hset(employee_key, mapping=input.__dict__)
        
        updated_data = await self.redis.hgetall(employee_key)
        return dict_to_employee(emp_id, updated_data)

    async def delete_employee(self, emp_id: int) -> int:
        """직원을 삭제합니다."""
        employee_key = f"employee:{emp_id}"
        
        pipe = self.redis.pipeline()
        pipe.srem(self.all_employees_set_key, emp_id)
        pipe.delete(employee_key)
        results = await pipe.execute()
        
        # `delete`가 성공하면 1을 반환, 대상이 없으면 0을 반환
        if results[1] == 0:
            raise ValueError(f"직원을 찾을 수 없습니다 (ID: {emp_id})")
        
        return emp_id