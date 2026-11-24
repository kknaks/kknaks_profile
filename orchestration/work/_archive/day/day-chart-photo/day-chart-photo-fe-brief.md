
# [frontend] DAY 차트 모달 — 탭 3 · 명시적 저장 · 사진 탭 · 헤더 (WP ③)

너는 **day `frontend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/roles/day/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-chart-photo`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

**backend 워커가 같은 워크트리에서 병렬로 WP ①(탭 저장 서버)을 만든다** — 서버 서비스 · `routers/board.py` 차트 라우트 함수는 backend 몫. 서로의 미커밋 변경을 지우지 마라(stash · checkout · reset 금지). 커밋하지 않는다.

## 1. SSOT — 먼저 읽을 것

**너는 앞 맥락이 없다.** 아래가 전부다. Delivery Issue 는 발행하지 않았다(사용자 「PR 은 나중에 머지 · 바로 구현」) — 아래 문서가 Issue 대신이다.

- **WP · 계약 K1 ~ K5 · 공통 e2e**: `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/work/day-chart-photo/delivery-1-report.md` 「WP 나누기」 · 「BE ↔ FE 계약」 ← 두 워커가 같은 글자로 맞춘다. **계약의 SoT**
- **결과 계약 · Acceptance · 수정 후보 · 하지 않는 것**: `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/work/day-chart-photo/delivery/request-be-chart.json` · `request-be-photo.json` · `request-fe.json`(Issue 본문이 될 뻔한 것)
- **SPEC**: `/Users/kknaks/orca/workspaces/mediness-mediness/day-chart-photo-spec/products/day/20-spec/spec-002-procedure-board.md` 개정 ㉘(U-14 · U-16 · 규칙 31 · 39 · API · 매트릭스 · KOS 사진 표) · `spec-001-login-session.md` 개정 ⑫(U-3) — 커밋 `a896cda0` · mediness PR #960(머지 전). 여기 없는 건 발명하지 마라
- 사용자 결정: `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/reference/2026-11-24-day-picture/chart-photo-decisions.md`(C1 ~ C17)
- 레포 규칙: 워크트리 루트 `AGENTS.md`

**기대는 개념**: 해당 없음

## 2. 배경 / 무엇을 바꾸나

차트 모달을 탭 3개(간호관리차트 | 의사차트 | 시술전후사진)로 바꾸고 **자동 저장을 걷어낸다** → 차트 탭마다 [저장](탭 줄 오른쪽 끝 · 차트 탭에서만) · 「최근 저장 : HH:MM」([저장] 바로 왼쪽 · 탭마다) · 미저장 닫기 확인 창(기획 4-2 글자) · 충돌(409) 그리기. 사진 탭은 **구조만**(K4 조각 · 올리기/삭제 폼 · 글자 OQ-88 비움 — 사진 서버는 아직 없다 · 가짜 응답으로). 웹 헤더 로그아웃 왼쪽에 로그인한 사람 표시 — 모양 = **「이름 직군」**(코디 기본값 · OQ-K21 · 차트 담당자 칸과 같은 모양).

지금 모양: `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/reference/2026-11-24-day-picture/current-chart-modal.png` · 합의된 와이어(코디 · 사용자 확인): 탭 줄 = `간호관리차트 | 의사차트 | 시술전후사진 ……… 최근 저장 : 13:26 [저장]` · 사진 탭 = 「시술 전」 · 「시술 후」 묶음 · 썸네일 + ✕ + 올리기 자리.

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

delivery-1-report 의 **K1 · K2 · K3 · K4 · K5(템플릿 · day.js 쪽)**. 조각 `partials/board_chart_tab.html` · `partials/board_photos.html` 은 네가 만든다. 값 이름은 K3 · K4 그대로.

## 4. 먼저 읽을 핵심 파일

- `backend/day/templates/base.html`(:36 ~ 61 헤더) · 차트 모달 템플릿(`grep -rl "최근 저장" backend/day/templates`) · `partials/board_chart_saved.html`(지움) · `backend/day/static/` day.js 의 자동 저장 · 실패 안내(다시 시도 · 저장하지 않고 닫기) · `ui.html` 매크로 · CSP
- `.agents/skills/verify-day-web/features/clinical-chart.md` — 「별도 저장 버튼은 없다」 등 갱신 대상

## 5. allowed_paths — 이 밖은 건드리지 마라

- `backend/day/routers/ (api/ 제외) · backend/day/templates/ · backend/day/static/ · backend/day/styles/ 중 브리프가 지정한 곳`
- `backend/tests/day/ 의 화면 테스트`

- 이번 지정: 위 템플릿 · static · styles · `routers/board.py` 는 **템플릿 이름 바꾸기 등 화면 연결 한 줄만**(함수 본문은 backend) · `.agents/skills/verify-day-web/features/clinical-chart.md`

## 6. 구현 단계

1. 모달 탭 3 · [저장] · 「최근 저장」(K1 `savedAt` 최댓값 · 탭마다) · 자동 저장 JS 걷어냄(입력 멈춤 · blur 저장 0)
2. 탭 저장 폼 — 바뀐 줄만 보낸다(안 바뀐 줄 칸 disabled · K2) · 200 = 조각 교체 · 409 = 조각 교체(이어 붙인 칸) + 토스트 자리(글자 OQ-90 — 비움)
3. 미저장 확인 창(E59 · 기획 4-2 글자 — SPEC 에 적힌 그대로) · ✕ · Escape · 바깥 누르기 · 탭 옮기기 처리는 SPEC 대로
4. 사진 탭 조각(K4) · 올리기(multipart · category) · 삭제 · 원본 열기 — 글자 없는 자리는 비움
5. 헤더 「이름 직군」 — 값이 렌더 공통 컨텍스트에 없으면 [질문](backend 와 경계)
6. verify-day-web 차트 기능 문서 갱신 · 화면 테스트

## 7. 범위 제약 — 하지 말 것

- 서버 서비스 · KOS 호출 · migration · 앱 · 화면 글자 짓기(SPEC · 기획 4-2 에 없는 글자 금지) · 인라인 스크립트 · 손 CSS

## 8. 검증

```
uv run pytest -q <네가 만든 화면 테스트만>(TestClient 로 전체 페이지 · HX 조각 렌더 확인) — 1회. CSS 를 다시 빌드했다면 빌드 명령 1회. 인라인 스크립트 0 · 손 CSS 0(grep). 사용자 포트·프로세스를 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_fae12a17-bcf2-4cd6-8e83-5f06c52bfc17 --from term_f69bad17-fd69-468b-81f6-d30eca448f36 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_fae12a17-bcf2-4cd6-8e83-5f06c52bfc17 \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_fae12a17-bcf2-4cd6-8e83-5f06c52bfc17 --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
