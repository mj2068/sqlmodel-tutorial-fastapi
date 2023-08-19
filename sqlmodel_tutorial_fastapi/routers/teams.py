from typing import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from sqlmodel import Session, select
from sqlmodel_tutorial_fastapi.db import get_session

from sqlmodel_tutorial_fastapi.models import (
    Team,
    TeamCreate,
    TeamRead,
    TeamReadWithHeroes,
)


router = APIRouter(prefix="/teams")


@router.post("", response_model=TeamRead)
def create_team(
    team: Annotated[TeamCreate, Body()], session: Session = Depends(get_session)
):
    team_db = Team.from_orm(team)
    session.add(team_db)
    session.commit()
    session.refresh(team_db)
    return team_db


@router.get("", response_model=list[TeamRead])
def read_teams(session: Session = Depends(get_session)):
    teams = session.exec(select(Team)).all()
    return teams


@router.get("/{id}", response_model=TeamReadWithHeroes)
def read_team(id: Annotated[int, Path()], session: Session = Depends(get_session)):
    team = session.get(Team, id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"could not find team with id {id}.",
        )
    print(team.heroes)
    return team


@router.patch("/{id}", response_model=TeamRead)
def update_team(
    id: Annotated[int, Path()],
    team: Annotated[TeamCreate, Body()],
    session: Session = Depends(get_session),
):
    team_db = session.get(Team, id)
    if not team_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"could not find team with id {id}.",
        )

    team_new = team.dict(exclude_unset=True)
    for key, value in team_new.items():
        setattr(team_db, key, value)

    session.add(team_db)
    session.commit()
    session.refresh(team_db)
    return team_db


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team(id: Annotated[int, Path()], session: Session = Depends(get_session)):
    team = session.get(Team, id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"could not find team with id {id}.",
        )

    session.delete(team)
    session.commit()
