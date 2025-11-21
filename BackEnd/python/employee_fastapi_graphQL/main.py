# main.py
import strawberry
import asyncio
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter

from api.employee_resolver import Query, Mutation
from api.employee_redis_resolver import RedisQuery, RedisMutation, get_redis_context
from core.database import engine, Base, SessionLocal
from core.context import CustomContext
from services.employee_service import EmployeeService
from services.employee_redis_service import EmployeeRedisService
from core.redis_client import redis_client # Import the singleton instance

# --- FastAPI 애플리케이션의 설정 및 초기화 ---

# 1. Strawberry 스키마 생성
schema = strawberry.Schema(query=Query, mutation=Mutation)
redis_schema = strawberry.Schema(query=RedisQuery, mutation=RedisMutation)

# 2. Context Getters 정의
def get_context() -> CustomContext:
    db = SessionLocal()
    try:
        yield CustomContext(db=db)
    finally:
        db.close()

# 3. GraphQL 라우터 생성
graphql_app = GraphQLRouter(schema, context_getter=get_context)
graphql_redis_app = GraphQLRouter(redis_schema, context_getter=get_redis_context)

# 4. FastAPI 앱 인스턴스 생성
app = FastAPI()

# 5. 스타트업 이벤트 핸들러 설정
@app.on_event("startup")
def startup_event():
    """서버가 시작될 때 DB와 Redis를 각각 초기화합니다."""
    # DB 테이블 생성 및 데이터 초기화
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        db_service = EmployeeService(db)
        db_service.init_db_data()
    finally:
        db.close()
        
    # Redis 데이터 초기화
    async def init_redis():
        redis_conn = await redis_client.get_client()
        try:
            redis_service = EmployeeRedisService(redis=redis_conn)
            await redis_service.init_redis_data()
        finally:
            await redis_conn.close()

    asyncio.run(init_redis())

# 6. 미들웨어 설정
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.254.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 7. 라우터 포함
app.include_router(graphql_app, prefix="/graphql")
app.include_router(graphql_redis_app, prefix="/graphql-redis")

# 기본 루트 경로
@app.get("/")
async def root():
    return {"message": "Hello FastAPI! Original(DB) and Redis-only GraphQL APIs are available."}