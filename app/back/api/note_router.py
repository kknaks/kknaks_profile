"""노트(note) — 1층. 전부 어드민 뒤다 — 공개 표면은 아직 안 정해졌다.

- GET    /api/admin/notes        — 목록. published_on DESC NULLS LAST
- GET    /api/admin/notes/files  — 등록 후보 md 파일 (frontmatter 프리필 포함)
- POST   /api/admin/notes        — 등록. 실존 md 아니면 422(케이스 4), slug 중복 409
- PATCH  /api/admin/notes/{id}   — 부분 수정. 보낸 필드만. detail_path 변경도 같은 검사
- DELETE /api/admin/notes/{id}   — 등록 해제. md 파일은 건드리지 않는다
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_db, require_admin
from schemas.note import (
    AdminNoteItem,
    AdminNotesResponse,
    NoteCreate,
    NoteFileItem,
    NoteFilesResponse,
    NoteUpdate,
)
from service.note_service import note_service

admin_router = APIRouter(
    prefix="/api/admin/notes",
    tags=["note"],
    dependencies=[Depends(require_admin)],
)


@admin_router.get("", response_model=AdminNotesResponse, response_model_by_alias=True)
async def list_notes(db: AsyncSession = Depends(get_db)) -> AdminNotesResponse:
    dtos = await note_service.list_notes(db)
    return AdminNotesResponse(items=[AdminNoteItem.from_dto(d) for d in dtos])


# /{note_id} 보다 먼저 선언한다 — 경로 매칭이 선언 순서를 따른다.
@admin_router.get("/files", response_model=NoteFilesResponse)
async def list_note_files(db: AsyncSession = Depends(get_db)) -> NoteFilesResponse:
    dtos = await note_service.list_file_candidates(db)
    return NoteFilesResponse(items=[NoteFileItem.from_dto(d) for d in dtos])


@admin_router.post(
    "", response_model=AdminNoteItem, response_model_by_alias=True, status_code=201
)
async def create_note(
    body: NoteCreate, db: AsyncSession = Depends(get_db)
) -> AdminNoteItem:
    dto = await note_service.create(db, body.model_dump())
    return AdminNoteItem.from_dto(dto)


@admin_router.patch(
    "/{note_id}", response_model=AdminNoteItem, response_model_by_alias=True
)
async def patch_note(
    note_id: int, body: NoteUpdate, db: AsyncSession = Depends(get_db)
) -> AdminNoteItem:
    dto = await note_service.update(db, note_id, body.model_dump(exclude_unset=True))
    return AdminNoteItem.from_dto(dto)


@admin_router.delete("/{note_id}")
async def delete_note(note_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    await note_service.delete(db, note_id)
    return {"ok": True}
