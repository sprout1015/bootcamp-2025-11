# api/employee_redis_resolver.py
from typing import List
import strawberry
from strawberry.types import Info
from functools import cached_property
from redis.asyncio import Redis

from core.redis_client import get_redis_session
from schemas.employee_schema import Employee, EmployeeInput
from services.employee_redis_service import EmployeeRedisService

class CustomRedisContext(strawberry.fastapi.BaseContext):
    def __init__(self, redis: Redis):
        self.redis = redis

    @cached_property
    def employee_redis_service(self) -> EmployeeRedisService:
        return EmployeeRedisService(redis=self.redis)

async def get_redis_context(
    redis: Redis = strawberry.fastapi.Depends(get_redis_session),
) -> CustomRedisContext:
    """
    요청마다 Redis 클라이언트를 포함한 Context 객체를 생성하는 의존성 주입(DI) 함수.
    """
    return CustomRedisContext(redis=redis)

@strawberry.type
class RedisQuery:
    """Redis만을 사용하는 GraphQL API의 조회(Query) 연산 정의"""

    @strawberry.field
    async def get_employees_redis(self, info: Info[CustomRedisContext, None]) -> List[Employee]:
        """Redis에서 모든 직원 목록을 반환하는 리졸버"""
        return await info.context.employee_redis_service.get_all_employees()

    @strawberry.field
    async def get_employee_by_id_redis(self, id: int, info: Info[CustomRedisContext, None]) -> Employee:
        """Redis에서 ID로 특정 직원을 조회하는 리졸버"""
        return await info.context.employee_redis_service.get_employee_by_id(id)

@strawberry.type
class RedisMutation:
    """Redis만을 사용하는 GraphQL API의 변경(Mutation) 연산 정의"""

    @strawberry.mutation
    async def register_employee_redis(self, input: EmployeeInput, info: Info[CustomRedisContext, None]) -> Employee:
        """Redis에 새로운 직원을 등록하는 리졸버"""
        return await info.context.employee_redis_service.create_employee(input)

    @strawberry.mutation
    async def update_employee_redis(self, id: strawberry.ID, input: EmployeeInput, info: Info[CustomRedisContext, None]) -> Employee:
        """Redis의 직원 정보를 수정하는 리졸버"""
        return await info.context.employee_redis_service.update_employee(int(id), input)

    @strawberry.mutation
    async def delete_employee_redis(self, id: strawberry.ID, info: Info[CustomRedisContext, None]) -> strawberry.ID:
        """Redis의 직원을 삭제하는 리졸버"""
        deleted_id = await info.context.employee_redis_service.delete_employee(int(id))
        return strawberry.ID(str(deleted_id))
