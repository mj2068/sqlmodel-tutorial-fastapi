from sqlmodel import create_engine
from .config import settings
from sqlmodel import Session


engine = create_engine(
    f"postgresql://{settings.username}:{settings.password}@{settings.address}/{settings.dbname}",
    echo=True,
)


def get_session():
    with Session(engine) as session:
        yield session
