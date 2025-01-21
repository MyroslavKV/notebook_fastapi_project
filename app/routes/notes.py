from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models import Notes
from app.schemas import NoteCreate, NoteUpdate, NoteResponse, NotesList
from app.routes.auth import get_current_user
from settings import get_db

route = APIRouter()

@route.post("/note/create", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(
    note_data: NoteCreate,
    session: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    new_note = Notes(
        title=note_data.title,
        content=note_data.content,
        tags=note_data.tags,
        user_id=current_user.id,
    )
    session.add(new_note)
    await session.commit()
    await session.refresh(new_note)
    return NoteResponse.model_validate(new_note)

@route.get("/note/get_all", response_model=NotesList)
async def get_all_notes(
    session: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    stmt = select(Notes).filter_by(user_id=current_user.id)
    result = await session.scalars(stmt)
    notes = result.all()
    count = await session.scalar(
        select(func.count()).filter(Notes.user_id == current_user.id)
    )
    return NotesList(notes=notes, count=count)

@route.get("/{note_id}/", response_model=NoteResponse)
async def get_note_by_id(
    note_id: int,
    session: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    stmt = select(Notes).filter_by(id=note_id, user_id=current_user.id)
    note = await session.scalar(stmt)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return NoteResponse.model_validate(note)

@route.put("/{note_id}/", response_model=NoteResponse)
async def update_note(
    note_id: int,
    note_data: NoteUpdate,
    session: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    stmt = select(Notes).filter_by(id=note_id, user_id=current_user.id)
    note = await session.scalar(stmt)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    for key, value in note_data.model_dump(exclude_unset=True).items():
        setattr(note, key, value)
    session.add(note)
    await session.commit()
    await session.refresh(note)
    return NoteResponse.model_validate(note)

@route.delete("/{note_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: int,
    session: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    stmt = select(Notes).filter_by(id=note_id, user_id=current_user.id)
    note = await session.scalar(stmt)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    await session.delete(note)
    await session.commit()
