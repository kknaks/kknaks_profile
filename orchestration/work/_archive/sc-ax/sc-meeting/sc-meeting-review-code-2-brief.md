# [reviewer_code] 코드 검수 2 — 검수 1 FAIL 해소분 + D19-3·D24 변경분만

너는 **sc-ax `reviewer_code` 워커**다. 코드 검수 1 을 한 세션이다 — 그 리포트 위에서 **수정분만** 본다.

작업 워크트리: `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting` — 읽기만. 범위 = 검수 1 이후 바뀐 파일(아래 §2).

## 1. 기준

- 검수 1 리포트 `orchestration/work/sc-meeting/review-code-01-wp001-wp006-report.md` F1~F4·W8·§8
- 코디 결정 D22(검수 1 처리): F1 created_at<ends_at 예외 · F2 Todo=SPEC §8.1 8필드 · F3 `can_edit_agendas`(scheduled|done|failed|cancelled·만든 사람, in_progress·summarizing 사람 안건 편집 409)와 `can_edit_note`(done|failed|cancelled) 분리, FE [수정]은 둘 중 하나 · F4 패널 [다음 회의 예약] 제거 · 열람 축 셋째(meeting.read.private×조직) board/get 제거, list 캘린더만 유지 · list_meetings commit · 공유 토스트 「공유했습니다.」 · api.ts 안건 반환형 Agenda
- D19-3·D24(FE): Todo 계약 {todo_id, agenda_id, title, description, due_candidate, checklist_candidate, reference, linked} · 다음 할 일 행 = 할 일·기한·[업무 생성]·× · 승격 행은 「요청됨」 텍스트, 「연관 업무 ›」 없음 · [업무 생성]→CreateWorkDrawer(요청만, 담당 비움·참석자 우선)
- SPEC 0.4.1 §3.3·§4.1-5·§8.1·§9 · 시안 두 장(회의실 D24 반영본)

## 2. 대상 파일

- BE: `modules/meetings/domain.py` · `application.py` · `platform/persistence.py` · `bootstrap/application.py` · `tests/contract/test_meeting_core.py` · `docs/domain-model.md`
- FE: `frontend/src/viewModels.ts` · `api.ts` · `labels.ts` · `WorkModals.tsx` · `App.tsx` · `meetings/AgendaBlock.tsx` · `MeetingListPage.tsx` · `MeetingDetailPage.tsx` · 두 테스트

## 3. 확인 — 각각 PASS/FAIL(파일:줄)

1. F1~F4 해소 여부와 회귀 테스트 존재.
2. BE↔FE 계약: `can_edit_agendas` 양쪽 · Todo 8필드 양쪽(BE `_todo_view` vs FE `MeetingTodo`) · 안건 반환형 · 승격 행 렌더(linked 있으면 「요청됨」, 링크 없음).
3. 열람 축: `_can_read_detail` 참석·공유만, `_can_read_calendar_detail` 는 list() 만. 비참석 대표 404·목록 0 테스트.
4. 안건 편집 게이트: in_progress·summarizing 409 테스트, 예정에서 안건 편집 열리고 줄 편집 닫힘.
5. 새 어긋남: [수정] 을 둘 중 하나로 세운 FE 판단이 시안 E77(네 상태)과 맞는가 · 「연관 업무」·「알림」 문구 잔존 0 · 코디가 실물로 확인한 것(과거 일시 회의 scheduled 유지 · 409 · 404/0건)과 코드가 일치.
6. 검증 재현 1회: `uv run pytest -q tests/contract/test_meeting_core.py tests/architecture -m 'not integration'` · `npx tsc --noEmit` · `npx vitest run src/meetings/`. 서버·reset·포트 금지.

## 4. 산출물 — 하나

`/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/work/sc-meeting/review-code-02-report.md` — 총평(PASS / FAIL — 재발주) · 항목 1~6 표 · 남은 것.

## 5. 완료 보고 — **문구 변경 금지**

> ⚠ 핸들은 dispatch preamble 값 우선.

```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_9efe51f3-aec0-44b1-94ea-f86134b6ddea \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "reviewer_code 완료: 코드 검수 2" \
  --body "총평 / 항목 1~6 / 남은 것 / 검증 수치"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] reviewer_code 완료 — 코드 검수 2: <PASS/FAIL 한 줄>. 상세는 인박스." --enter
```
