from sqlmodel import Field, SQLModel


class Hero(SQLModel, table=True):
    __tablename__ = "heroes"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = Field(default=None)
