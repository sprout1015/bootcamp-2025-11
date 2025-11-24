# repository/employee_redis_repository.py
from typing import List, Dict
from redis.asyncio import Redis
from schemas.employee_schema import EmployeeInput

class EmployeeRedisRepository:
    def __init__(self, redis: Redis):
        self.redis = redis
        self.id_counter_key = "employee:id:counter"
        self.all_employees_set_key = "employees:all:set"

    async def initialize_data(self):
        """애플리케이션 시작 시 Redis에 샘플 데이터를 초기화합니다."""
        await self.redis.flushdb()
        
        sample_data = [
            {"name": "Redis-Alice", "age": 30, "job": "Engineer", "language": "Python", "pay": "60000"},
            {"name": "Redis-Bob", "age": 25, "job": "Designer", "language": "JavaScript", "pay": "55000"},
            {"name": "Redis-Charlie", "age": 35, "job": "Manager", "language": "Go", "pay": "80000"},
        ]
        
        await self.redis.set(self.id_counter_key, "0")

        pipe = self.redis.pipeline()
        for emp_data in sample_data:
            new_id = await self.redis.incr(self.id_counter_key)
            employee_key = f"employee:{new_id}"
            
            pipe.hset(employee_key, mapping=emp_data)
            pipe.sadd(self.all_employees_set_key, new_id)
        await pipe.execute()
        print("Redis data initialized by repository.")

    async def get_all(self) -> List[Dict]:
        """모든 직원 데이터를 딕셔너리 리스트로 조회합니다."""
        employee_ids = await self.redis.smembers(self.all_employees_set_key)
        
        pipe = self.redis.pipeline()
        for emp_id in employee_ids:
            pipe.hgetall(f"employee:{emp_id}")
        
        results = await pipe.execute()
        
        employees = []
        for emp_id, data in zip(employee_ids, results):
            if data:
                data['id'] = emp_id # Add id to dict for service layer
                employees.append(data)
        return employees

    async def get_by_id(self, emp_id: int) -> Dict:
        """ID로 특정 직원 데이터를 딕셔너리로 조회합니다."""
        return await self.redis.hgetall(f"employee:{emp_id}")

    async def create(self, input: EmployeeInput) -> Dict:
        """새로운 직원 데이터를 생성하고 딕셔너리로 반환합니다."""
        new_id = await self.redis.incr(self.id_counter_key)
        employee_key = f"employee:{new_id}"
        
        # input.__dict__ might contain non-string values
        input_data = {k: str(v) for k, v in input.__dict__.items()}

        pipe = self.redis.pipeline()
        pipe.hset(employee_key, mapping=input_data)
        pipe.sadd(self.all_employees_set_key, new_id)
        await pipe.execute()
        
        created_data = await self.redis.hgetall(employee_key)
        created_data['id'] = new_id
        return created_data

    async def update(self, emp_id: int, input: EmployeeInput) -> Dict:
        """직원 정보를 수정하고 딕셔너리로 반환합니다."""
        employee_key = f"employee:{emp_id}"
        if not await self.redis.exists(employee_key):
             return None

        input_data = {k: str(v) for k, v in input.__dict__.items()}
        await self.redis.hset(employee_key, mapping=input_data)
        
        updated_data = await self.redis.hgetall(employee_key)
        updated_data['id'] = emp_id
        return updated_data

    async def delete(self, emp_id: int) -> int:
        """직원을 삭제합니다."""
        employee_key = f"employee:{emp_id}"
        
        pipe = self.redis.pipeline()
        pipe.srem(self.all_employees_set_key, emp_id)
        pipe.delete(employee_key)
        results = await pipe.execute()
        
        # `delete`가 성공하면 1을 반환, 대상이 없으면 0을 반환
        if results[1] == 0:
            return 0
        
        return emp_id
