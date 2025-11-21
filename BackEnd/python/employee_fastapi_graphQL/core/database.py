# core/database.py
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, declarative_base

# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL 환경 변수를 찾을 수 없습니다. .env 파일을 확인해주세요.")

# --- 데이터베이스 연결 설정 ---

# create_engine: 데이터베이스 커넥션 풀을 생성합니다. 애플리케이션 수명 주기 동안 단 한 번만 생성되어야 합니다.
# echo=True: SQLAlchemy가 실행하는 모든 SQL 쿼리를 콘솔에 출력합니다. 디버깅에 유용합니다.
# future=True: SQLAlchemy 2.0 스타일의 사용법을 활성화합니다.
engine: Engine = create_engine(DATABASE_URL, echo=True, future=True)

# sessionmaker: 데이터베이스 세션을 생성하는 팩토리 클래스입니다.
# 이 팩토리를 통해 생성된 세션은 위에서 만든 엔진(커넥션 풀)을 사용하여 DB와 통신합니다.
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# declarative_base: 모든 ORM 모델이 상속받아야 하는 기본 클래스입니다.
# 이 클래스를 상속받은 모델들은 SQLAlchemy에 의해 DB 테이블과 매핑됩니다.
Base = declarative_base()