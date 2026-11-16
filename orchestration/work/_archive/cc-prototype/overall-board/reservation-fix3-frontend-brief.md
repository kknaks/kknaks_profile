# [backend · frontend] WP-FIX3 — 예약 카드 드래그(E2E batch 4 #1) · 공지 [수정하기]

너는 **cc-prototype `backend` 또는 `frontend` 워커**다(dispatch 에 적힌 역할). **앞 판 맥락이 없다.** 먼저 읽어라:
- 역할 문서 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/frontend/role.md` + 같은 폴더 rules · skills · tools · workflow
- 앞 판 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/reservation-frontend-brief.md` — allowed_paths · 금지 · 검증 규칙(보고 대상 핸들은 **아래 §5 가 맞다**)

작업 워크트리(코드): `/Users/kknaks/orca/workspaces/cc-prototype/overall-board` — branch **`kknaksss/overall-board-2`**(= main `64e1989`). backend · frontend 가 같은 워크트리(back / front 나눠서 · 서로의 폴더 금지).

## 1. 계약 (SSOT)

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/20-spec/spec-005-reservation-board.md` **0.4.0** — §5.4(이동) · §5.15(공지) · §6.4 · §7.2 · §7.5 · §7.6 · §8 공지 줄 · §9 #11 · #46 · 부록 G
- `30-work/work-007-reservation-board.md` **WP-FIX3** 줄(대상 파일 · 완료 조건 · 검증 명령)
- KOS 공지 근거: `orchestration/work/overall-board/reservation-notice-report.md`(데모 실호출 확인) · 기본값 `reservation-spec-r4-addendum-1.md`
- **화면 정본 = 지금 배포된 웹 구현**(D-60). 시안 대조 하지 마라
- reviewer_doc 이 같은 SPEC 을 **병렬로 검수 중**이다. FAIL 이 나오면 코디가 추가 지시로 보낸다

## 2. backend

1. **`PUT /api/reservations/notice`**(§5.15 · §7): 저장 직전 그 날 공지를 KOS 에서 다시 읽기 → 있으면 `change-content` · 없으면 `create-notice`(`releaseDateTimeUtc` = 그 날 KST 00:00 의 UTC) · 빈 내용(trim 뒤 0) = `delete-notice` · 2000자(trim 길이) 넘으면 400 · 지난 날짜 409 `notice_past_date` · `event_log(notice_save)` · 날짜별 캐시 비움 · 응답 = SPEC 모양. ccc API 는 행 id 를 받아도 KOS 호출은 `kos_id`(§ Q-143)
2. `board.noticeEditable` · 경로 수 35(`test_route_count_35`) · 가짜 모드 응답
3. 시험 `tests/test_resv_notice.py`(4갈래 · 지난 날짜 · 2000자 · 빈 저장 · 캐시)
4. **데모 실물 호출 1회가 완료 조건**(가짜 KOS 만으로 done 금지): 데모 테넌트 assert(`.env` 값 출력 금지) · 운영 키(`KOS_API_tenent`) 금지 · 2026-11-11 KST 에 ccc API 로 쓰기 → 고치기 → 비우기 한 번씩 · 남긴 데모 흔적을 보고에
5. 드래그(b4 #1)에 back 원인이 있으면(이동 API 오류 등) 고치고 보고 — 없으면 「back 원인 없음」

## 3. frontend

1. **예약 카드가 안 잡힌다(b4 #1)** — 사용자: 「카드가 안 잡혀」(끌기 시작 자체가 안 됨). 원인을 코드에서 찾아 고친다(`draggable` · 잡는 영역 · 포인터 이벤트 · 겹친 레이어 · 클릭과 충돌 등). **원인을 보고에 한 단락으로.** 이동 계약(§5.4 — 정원 찬 칸 미리 막기 · KOS 거절 시 원위치 + 오류 토스트 · 길이 유지)은 그대로. 고친 뒤 실제로 끌어 다른 시각 · 다른 칸으로 놓아 보고 스크린샷
2. **공지 [수정하기]**(§5.15 · §6.4): 그 날 공지 **하나**(지금 목록 전부 → 첫 번째 하나) · 제자리 편집 [수정하기] ↔ 「저장」 · [취소] · 글자 수(2000) · 지난 날짜엔 버튼 없음(`noticeEditable`) · 빈 저장 = 지우기 · 실패 = 오류 토스트 + 편집 유지 · 성공 토스트. DS(medikit) 컴포넌트만 — 브라우저 기본 컨트롤 금지
3. 스크린샷 → `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/fe-shots-reservation/fix3-*.png`(드래그 전 · 중 · 후 · 공지 보기 · 편집 · 지난 날짜)

## 4. 검증 · 금지

- backend `cd procedure/back && uv run ruff check . && uv run pytest -q` / frontend `cd procedure/front && npx tsc --noEmit && npm run lint && npm run build`
- **사용자 포트 3700 · 8700 · 그 프로세스 건드리지 마라**(임시 포트는 쓰고 끝나면 정리) · **커밋 · push 금지**(코디가 한다)
- KOS 쓰기는 §2.4 데모 시험만 · public 레포 — 실명 · KOS id · 키 · 토큰 금지
- 응답 모양이 SPEC 과 달라야 하면 멈추고 물어라(SPEC 먼저)

## 5. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 과 다르면 preamble 쪽으로만.

- 보고서: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/reservation-fix3-frontend-report.md`(바뀐 파일 · 원인 · 검증 수치 · 데모 흔적 · 미결)

```bash
orca orchestration send \
  --to term_678ac61d-2472-4a9b-ba73-61883337b957 --from term_fd1ce51a-dd31-4e6b-af8a-a3ccf26baf24 \
  --type worker_done \
  --task-id <preamble 의 taskId> --dispatch-id <preamble 의 dispatchId> \
  --subject "frontend 완료: WP-FIX3 <한 줄>" \
  --body "보고서 경로 / 바뀐 파일 / 검증 수치 / 미결"

orca terminal send --terminal term_678ac61d-2472-4a9b-ba73-61883337b957 \
  --text "[worker_done] frontend WP-FIX3 완료 — <한 줄>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_678ac61d-2472-4a9b-ba73-61883337b957 --text "[질문] frontend: <질문>" --enter`
