from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_session():
    with SessionLocal() as session:
        yield session


class Base(DeclarativeBase):
    pass


# 🔥 Создаём таблицы при запуске
def init_db():
    Base.metadata.create_all(bind=engine)

