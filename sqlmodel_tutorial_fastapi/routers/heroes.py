from typing import Annotated
from fastapi import APIRouter, Body, Depends
from sqlmodel import Session, select
from sqlmodel_tutorial_fastapi.db import get_session

from sqlmodel_tutorial_fastapi.models import Hero, HeroCreate


router = APIRouter(prefix="/heroes")


@router.post("", response_model=Hero)
def create_hero(
    hero: Annotated[HeroCreate, Body()], session: Session = Depends(get_session)
):
    hero_db = Hero.from_orm(hero)
    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)

    return hero_db


@router.get("", response_model=list[Hero])
def read_heroes(session: Session = Depends(get_session)):
    heroes = session.exec(select(Hero)).all()
    return heroes
