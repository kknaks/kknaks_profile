# [frontend] DAY 예약 현황 — Delivery #269(화면 · Jinja2 + HTMX)

너는 **day `frontend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/roles/day/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

**backend 워커가 같은 워크트리에서 #267 · #268 을 만든다** — 너는 frontend 몫만. 라우터 함수 · view model 은 backend 가 만든다 — 너는 템플릿 · 정적 파일 · 화면 테스트. backend 가 아직 없으면 `delivery-3-report.md` view model 표대로 **가짜 값**으로 템플릿을 세우고, backend #267 이 끝났다는 알림이 오면 실제 값에 붙인다. 서로의 미커밋 변경을 지우지 마라(stash · checkout · reset 금지).

## 1. SSOT — 먼저 읽을 것

**너는 앞 맥락이 없다.** 아래가 전부다.

- **Delivery Issue 본문**(계약의 SoT · 결과 계약 · Acceptance · 수정 후보 · 하지 않는 것): `gh issue view <번호> -R MediSolveAIDev/CENTURION_DAY` — 번호는 §2
- **계약 최종 문장**(폴링 구분 신호 · 최신화 task 입구 · view model 표 · 조각 `#reservation-main` 범위): `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/delivery-3-report.md` — Issue 본문과 같아야 한다. 다르면 Issue 가 이긴다 · 다르다고 [질문]
- SPEC: `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation-spec/products/day/20-spec/spec-006-reservation-board.md` (DAY-SPEC-006 · stable · mediness PR #958 · 머지 전) — Issue 에 없는 세부는 여기서. **여기 없는 건 발명하지 마라**
- 사용자 결정: `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/reference/2026-11-23-reservation/reservation-board-decisions.md` (R1 ~ R41)
- 레포 규칙: 작업 워크트리 루트 `AGENTS.md` — 계층 · 이름 · 테스트 규칙(repository 층 없음 · 묶음 조회 = `queries/` 등)

**기대는 개념**: 해당 없음

## 2. 배경 / 무엇을 바꾸나

DAY 웹에 「예약 현황」 화면을 새로 만든다 — **Issue #269**. 시안 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/reference/2026-11-23-reservation/20261113_예약현황_시연 (1).html` 이 생김새 · 문구의 정본(3MB 한 파일 · grep). 범위: SPEC RV-01 ~ RV-41 · U-1 ~ U-7 — 하루 표(세로 열 = 예약 그룹 · 30분 칸 · 회색 면 · 현재 시각 선 · 좌우 넘김) · 카드(띠 색 = 내원 단계 · 초진 · 수납 필요 · 국가 · 툴팁) · 날짜 ‹ › · 오늘 · 달력 · 필터 · 10초 조각 폴링 · 오른쪽 패널(위 공지 / 아래 「예약 요청」 제목만 · 「공지 / 예약」 탭 하나). 뺀 것(상세 모달 · 고객 등록 · 고객 검색 · 원내 현황 · 근무표 · 예약 요청 내용)은 그리지 않는다.

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

`delivery-3-report.md` 의 계약을 **문자 그대로** 소비: ① 폴링 요청은 정해진 구분 신호를 싣는다(날짜 바꾸기는 안 싣는다) ② view model 표 · 조각 `#reservation-main` 범위. 이름 · 모양이 안 맞으면 [질문].

## 4. 먼저 읽을 핵심 파일

- Issue #269 「수정 후보」 전부
- `backend/day/templates/board.html` · `templates/partials/` · `ui.html` 매크로 · `base.html` · `static/day.js`(이벤트 위임 · data-*) · `styles/` — 시술 현황 화면이 본
- `AGENTS.md` 「웹 화면」 절(인라인 스크립트 0 · 손 CSS 0 · medikit 토큰)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `backend/day/routers/ (api/ 제외) · backend/day/templates/ · backend/day/static/ · backend/day/styles/ 중 브리프가 지정한 곳`
- `backend/tests/day/ 의 화면 테스트`

## 6. 구현 단계

1. 작업 워크트리 · `AGENTS.md` · Issue #269 · `delivery-3-report.md` · 시안을 읽는다
2. 가짜 값으로 템플릿 · day.js · 화면 테스트(TestClient — 전체 페이지 · HX 조각 · 폴링 신호)
3. backend #267 이 끝나면 실제 view model 에 붙인다
4. §8 검증(네 화면 테스트만 · CSS 빌드했으면 1회 · 인라인 스크립트 / 손 CSS grep 0)
5. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/fe-1-report.md`(Acceptance 체크 · 시안 대조 표 · 바꾼 파일 · 못 한 것)
6. §9 완료 보고

## 7. 범위 제약 — 하지 말 것

- **화면 문구를 지어 넣지 않는다** — 시안에 있는 글자만. 없으면 비움
- 라우터 함수 · services · queries · 동기화(backend 몫) · migration
- 상세 모달 · 쓰기 동작 · 클릭 동작
- 커밋 · push · PR · 사용자 포트 · 프로세스

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
  --to term_28a8c525-c408-4f25-a0f2-ffd6c29fb56d --from term_0bf335ae-7e06-4bc0-90fe-a3eb019ef6e6 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_28a8c525-c408-4f25-a0f2-ffd6c29fb56d \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_28a8c525-c408-4f25-a0f2-ffd6c29fb56d --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
