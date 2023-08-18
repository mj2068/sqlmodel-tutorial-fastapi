from typing import Annotated
from fastapi import APIRouter, Body, Depends
from sqlmodel import Session
from sqlmodel_tutorial_fastapi.db import get_session

from sqlmodel_tutorial_fastapi.models import Hero


router = APIRouter(prefix="/heroes")


@router.post("")
def create_hero(hero: Annotated[Hero, Body()], session: Session = Depends(get_session)):
    session.add(hero)
    session.commit()
    session.refresh(hero)

    return hero
