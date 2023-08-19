from typing import Optional, Union
from sqlmodel import Field, Relationship, SQLModel


class HeroBase(SQLModel):
    name: str
    secret_name: str
    age: int | None = Field(default=None)
    team_id: int | None = Field(default=None, foreign_key="teams.id")


class Hero(HeroBase, table=True):
    __tablename__ = "heroes"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)

    team: Union["Team", None] = Relationship(back_populates="heroes")


class HeroCreate(HeroBase):
    pass


class HeroRead(HeroBase):
    id: int


class HeroUpdate(SQLModel):
    name: str | None
    secret_name: str | None
    age: int | None
    team_id: int | None


class TeamBase(SQLModel):
    name: str
    headquarters: str


class Team(TeamBase, table=True):
    __tablename__ = "teams"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)

    heroes: list[Hero] = Relationship(back_populates="team")


class TeamCreate(TeamBase):
    pass


class TeamRead(TeamBase):
    id: int


class TeamUpdate(SQLModel):
    name: str | None
    headquarters: str | None


class HeroReadWithTeam(HeroRead):
    team: TeamRead | None


class TeamReadWithHeroes(TeamRead):
    heroes: list[HeroRead]
