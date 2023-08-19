from sqlmodel import Field, SQLModel


class HeroBase(SQLModel):
    name: str
    secret_name: str
    age: int | None = Field(default=None)


class Hero(HeroBase, table=True):
    __tablename__ = "heroes"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)


class HeroCreate(HeroBase):
    pass


class HeroRead(HeroBase):
    id: int


class HeroUpdate(SQLModel):
    name: str | None
    secret_name: str | None
    age: int | None
