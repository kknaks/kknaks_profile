# [backend] WP② — 시술전후사진 서버 (DAY 저장 + KOS 등록 + KOS 가져오기)

## 너는 맥락이 없다 — 먼저 읽을 것

- **SPEC (SoT)**: `/Users/kknaks/orca/workspaces/mediness-mediness/day-chart-photo-spec/products/day/20-spec/`
  - `spec-002-procedure-board.md` 개정 ㉘ 보충 — U-16 · 규칙 39 · 「KOS 사진 — 직접 호출」 · API · 매트릭스 · OQ
  - `spec-000-data-model.md` — `visit_photo` · external_ref
  - mediness PR #960 의 최신 커밋을 본다. SPEC 에 없는 건 발명하지 마라.
- **결정**: `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/reference/2026-11-24-day-picture/chart-photo-decisions.md`
  - C8 ~ C13 · C22 · C22-기본값 · C23 · 키 `beforeAfter/`
  - C14 는 취소됨
- **KOS 실물 모양**: `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/reference/2026-11-24-day-picture/*.har`
  - 모양만 본다. 값은 코드 · 테스트 · 리포트에 옮기지 않는다.
- **계약 K4**: `…/day-chart-photo/delivery-1-report.md` · `contract-k3-header-note-1.md`
  - K4 의 썸네일 `data:` · 서명 주소 부분은 SPEC 으로 바뀌었다. **DAY 저장소에서 보낸다.**
  - 조각 값 이름(`photos` 구조)은 frontend 와 맞춘다. 바뀌면 [질문].
- **레포 규칙**: `AGENTS.md`

## 할 것

1. **migration** — `visit_photo`
   - SPEC-000 그대로 만든다.
   - alembic head(0023) 에 잇는다. 그 전에 `git fetch origin dev` 로 dev 에 새 migration 이 있는지 확인한다.
2. **저장소**
   - 채팅 첨부 저장소(`adapters/storage` · `DAY_CHAT_STORAGE` 설정 · 관리 ID · disk/blob)를 재사용한다.
   - 키는 `beforeAfter/{hospital_id}/{32 hex}.{ext}`.
   - 키 검사 규칙에 `beforeAfter` 를 더하고, 주석의 `before-after` 를 바로잡는다.
3. **올리기**
   - 순서: 저장소 → DAY 행 커밋 → (transaction 밖) KOS 7단계(직원 토큰 · get-codes 이름 매칭 · presigned · PUT · register · 목록으로 id 확인) → external_ref
   - KOS 가 실패하면 「KOS 미반영」으로 남기고 [다시 시도] API 를 둔다.
4. **삭제**
   - DAY 는 소프트 삭제하고, KOS 에서도 삭제한다.
   - 실패 처리는 SPEC 기본값대로.
5. **목록 · 썸네일 · 원본** — DAY 행과 저장소에서 내보낸다(권한 확인 · `no-store`).
6. **C23 가져오기 작업**
   - 사진 탭을 열면 중앙 작업을 넣는다(DAY-SPEC-006 다른 날짜 최신화 방식 · 같은 방문 잠금).
   - 작업은 KOS 목록 → DAY 에 없는 것만 원본을 받아 저장소 + 행 + external_ref 에 넣는다.
   - 화면 요청은 DB 만 읽는다.
7. **테스트** — FakeKos · disk 저장소. SPEC 매트릭스 행마다 하나씩.

## 하지 마라

- 템플릿 · JS · CSS — frontend 몫. 조각 값만 맞춘다.
- 10초 동기화 · 앱
- KOS 실물 쓰기 — 실물 e2e 는 코디가 한다.
- 커밋

## 검증

- `scripts/test.sh -q backend/tests/day`(사진 · board)
- ruff · mypy(만진 파일)
- migration up / down 1회(로컬 테스트 DB)

## 보고

- `be-photo-1-report.md`(같은 work 폴더)
- preamble 의 worker_done 두 채널
