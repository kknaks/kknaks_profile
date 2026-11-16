# [frontend] CENTURION_DAY#236 구현 — frontend 단계 (기획안 맞추기 화면)

너는 day **frontend** 워커다. 역할 문서 먼저: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/frontend/role.md`(+ 같은 폴더) · 레포 `AGENTS.md`(웹 = 서버 렌더링 Jinja2 + HTMX + 바닐라 JS · medikit).

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-procedure-board-2`. **backend 단계는 끝났다(미커밋)** — 서비스 · 규칙 · 스냅샷 · JSON API 가 새 모양이다. backend 파일(services · queries · dtos · emr · routers/api · config)은 **고치지 마라** — 모자라면 질문으로. 동시에 reviewer 가 backend 를 읽고 있다(읽기만).

## SSOT
- Delivery #236 v2(승인됨): `gh issue view 236 --repo MediSolveAIDev/CENTURION_DAY` — Target Delta 16 · Acceptance(A9 확인 모달 · A10 화면) · Execution frontend phase
- 스펙: `/Users/kknaks/orca/workspaces/mediness-mediness/day-procedure-board-2-spec/products/day/20-spec/spec-002-procedure-board.md` 개정 ⑬ · ⑭ — 화면 구성 · U-1 · U-3 ~ U-8 · U-10 · U-12 · U-13 · 스냅샷 모양 · 오류 · 토스트 표
- 결정 정본: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/_RESUME.md` §2(11-09 ~ 11-10 기획 · 디자인 행)
- backend 보고 요약: 스냅샷 = task `pickable`(준비중만) · `canCall` · `canRecall` · 카드 `needs[]`(wait · anes · call · accept · home · since · limitMin · callId · doctorName) · `limits{}` · `anesthesia.lastSeconds`(lastMinutes 대체) · `inbox.need` = {**need, visitId, card} 목록 · JSON API `GET /api/board/search?q=` · `GET /api/visits/{id}/chart` · `POST /api/tasks/{id}/doctor {doctorStaffId}` · 오류 `call_already_accepted`. **웹 조각 라우트 3쌍(`/board/search` · `/board/visits/{id}/chart` · `/board/tasks/{id}/doctor`)과 MESSAGES 의 `call_already_accepted` 는 네 몫**(화면 라우터).

## 할 것 (화면)
1. 고객 카드: 체크박스 준비중만(나머지 비활성) · 전체 선택 · 고객 이름 눌러도 아무것도 안 열림 · **시술 이름 누르면 차트 모달**(지금 읽기 전용 차트 내용) · 시술 줄 「⋯」 **늘 보임**(호버 아님) · **카드 스크롤 먼저 → 카드 스크롤 끝(맨 위/맨 아래)이거나 없으면 판 스크롤**(지금 `.day-card__scroll` 의 `overscroll-behavior: contain` 이 막음)
2. 고객 검색: 「시술 완료」 탭 검색 칸 → 서버 검색(이름 · 담당 원장 · 관리실) · 결과 카드 누르면 같은 차트 · 빈 결과 문구 스펙대로 · **상단 고객 검색 칸(E06) 화면에서 뺌**
3. 확인 필요: 인박스 「현황」 탭 「확인 필요」 칸에 5상황 카드(문구 스펙 「」 그대로) · **빨강** · 팝업 알림 없음 · 귀가 대기 전 카드 [귀가 대기] · 호출 중 줄 [재호출] 늘 · 확인 필요 카드 [재호출] **글자 검정**
4. 마취: [마취 시작] → [마취중 mm:ss] + [마취 종료] → [마취 완료 mm:ss] + [마취 시작] · 20분 초과 빨강
5. 줄 표시: 「{원장} 수락 완료 HH:MM」 · 「{원장} · 진행 mm:ss」 · 「{원장} · n분」
6. 담당 원장 바꾸기: 수락 · 진행 중 줄의 원장 이름 **호버 툴팁 「원장 교체」** · 누르면 원장 목록(기존 E51 원장 고르기 창 모양) · 고르면 `/board/tasks/{id}/doctor`
7. 동시 수락 거절 토스트 「다른 원장이 먼저 받았습니다」
8. 시작 취소 · 완료 취소 **확인 모달** 「{시술} 시작을 취소할까요?」 · 「{시술} 완료를 취소할까요?」 · 버튼 [시작 취소] / [완료 취소] · [닫기](kit 모달 · 확인 창 E54)
9. web 템플릿 테스트(`backend/tests/day/web/test_board_page.py` 실패 25개)를 새 모양으로 고치고, 위 화면 동작마다 화면 테스트

## 하지 말 것
- 화면 문구 지어내기 금지(스펙 · 결정 「」 · 기획안 「」만 — 없으면 비우고 질문) · 손 CSS 금지(medikit · DS 토큰 · 기존 `styles/app.css` 규칙 안에서) · 인라인 스크립트 금지
- backend 파일 · 커밋 · push · PR 금지 · 사용자 포트 · 프로세스 · day-local 건드리지 않음 · KOS 호출 금지

## 검증
화면 테스트 + `DAY_ENV_FILE=/Users/kknaks/git/CENTURION_DAY/deploy/local.env scripts/test.sh -q` 끝에 1회(전부 통과) · CSS 다시 빌드했으면 `scripts/build-css.sh` 1회 · 인라인 스크립트 0 · 손 CSS 0(grep 결과 보고).

## 완료 보고 (두 명령 모두)
```bash
orca orchestration send --to term_28f2b422-a0ae-490a-bbed-aeb19fbd7fdd --from <네 워커handle> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "frontend 완료: <한 줄>" --body "변경 파일 / 항목별 요약 / 테스트 수 / 미결"
orca terminal send --terminal term_28f2b422-a0ae-490a-bbed-aeb19fbd7fdd --text "[worker_done] frontend 완료 — <한 줄>. 상세는 인박스." --enter
```
막히면 `[질문] frontend: …` 로 같은 터미널에 send. 핸들은 dispatch preamble 값이 맞다.
