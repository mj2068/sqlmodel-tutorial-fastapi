from typing import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status
from sqlmodel import Session, select
from sqlmodel_tutorial_fastapi.db import get_session

from sqlmodel_tutorial_fastapi.models import Hero, HeroCreate, HeroRead


router = APIRouter(prefix="/heroes")


@router.post("", response_model=HeroRead)
def create_hero(
    hero: Annotated[HeroCreate, Body()], session: Session = Depends(get_session)
):
    hero_db = Hero.from_orm(hero)
    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)

    return hero_db


@router.get("", response_model=list[HeroRead])
def read_heroes(
    skip: Annotated[int | None, Query()] = 0,
    limit: Annotated[int | None, Query(ge=0, le=50)] = 10,
    session: Session = Depends(get_session),
):
    heroes = session.exec(select(Hero).offset(skip).limit(limit)).all()
    return heroes


@router.get("/{id}", response_model=HeroRead)
def read_hero(
    id: Annotated[int, Path(description="id for the hero")],
    session: Session = Depends(get_session),
):
    hero = session.get(Hero, id)
    if not hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"could not find hero with id: {id}.",
        )

    return hero
