# [planner] DAY-SPEC-002 U-14 개정 — 차트 명시적 저장 · 시술전후사진 탭 (+ 헤더 로그인 표시)

너는 **day `planner` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/roles/day/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-chart-photo-spec`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**너는 앞 맥락이 없다.** 이 브리프와 아래 파일이 전부다. 이 워크트리는 너 혼자 쓴다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/reference/2026-11-24-day-picture/chart-photo-decisions.md` ← **사용자 결정 C1 ~ C16 · KOS 사진 흐름 · 아직 안 정한 것. 계약의 SoT. 다시 열지 마라. 여기 없는 정책은 발명하지 마라.**
- `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/reference/2026-11-24-day-picture/current-chart-modal.png` — 지금 차트 모달 모양
- `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/reference/2026-11-24-day-picture/*.har` — KOS 웹 사진 올리기 · 여러 장 · 삭제 실물(데모 지점). **모양만 읽는다** — 토큰 · presigned URL · 고객 이름 · id 값은 SPEC 에 옮기지 않는다
- `/Users/kknaks/orca/workspaces/mediness-mediness/day-chart-photo-spec/products/day/00-baseline/planning/` 의 시술 현황 기획안 §4-2(차트) — 기획 원문은 「저장」 버튼 · 「저장하지 않고 닫을까요?」 · 「계속 쓰기」 · 「버리고 닫기」를 갖고 있다(개정 ⑯ 이 자동 저장으로 바꿨던 것). **고치지 않는다** — 화면 글자의 원천 후보로만 쓴다

**기대는 개념**

- 해당 없음

## 2. 배경 / 무엇을 바꾸나

DAY 웹 시술 현황(DAY-SPEC-002)의 차트 모달(U-14 · 규칙 31 · 개정 ⑯)은 지금 **자동 저장**이다(칸을 나가거나 2초 멈추면 줄마다 저장 · 저장 버튼 · 미저장 경고 없음 · 「최근 저장」은 모달 오른쪽 위). 사용자가 **명시적 저장**으로 되돌리고, 탭에 **시술전후사진**을 더한다.

1. 차트 탭(간호관리차트 · 의사차트): 자동 저장 삭제 → 탭마다 [저장] 버튼(탭 줄 오른쪽 끝 · 차트 탭에서만) · 「최근 저장 : HH:MM」은 [저장] 바로 왼쪽 · 미저장 닫기 경고 · 한 번 저장 = 그 탭의 시술 줄 전부를 트랜잭션처럼(C2 ~ C7)
2. 시술전후사진 탭(새): 시술 전 / 시술 후 묶음 · 올리기 · 삭제 → 바로 KOS(로그인한 직원 토큰 · KOS 웹과 같은 필드 · 메모 고정 모양 · 분류 · 장비는 get-codes 이름으로 · DAY 서버 경유 · DAY 저장 없음)(C8 ~ C15)
3. 웹 헤더: 로그아웃 버튼 왼쪽에 로그인한 사람 표시(C16) — 이 항목이 사는 SPEC(DAY-SPEC-001 U-3 근처 또는 DAY-SPEC-002 머리)을 근거와 함께 골라 적는다

산출물: **DAY-SPEC-002 개정(다음 개정 번호)** — U-14 · 규칙 31(저장 단위 · 동시성 `baseLogId` · outbox) · 화면 구성(E55 · E56 · 사진 요소 새 번호) · API(이름 제안 — 탭 저장 · 사진 목록 · 올리기 · 삭제 · 썸네일/원본 열기) · KOS 쓰기 표 · 케이스 매트릭스 · 오류 글자 · §4 「앞 판과 달라진 곳」(자동 저장 문장은 지우지 말고 ~~취소선~~ + 날짜 · 사유) · OQ · 필요하면 DAY-SPEC-001 개정(헤더) + `20-spec.md` 지도 · `10-decision.md` · `log.md`. **WORK(30-work)는 이번에 쓰지 않는다** — SPEC 검수 뒤 Delivery 와 함께 따로 발주한다.

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

해당 없음(문서 단계). 경로 · 칸 이름은 SPEC-002 처럼 **「이름 제안」**, 정하지 못한 것은 OQ.

## 4. 먼저 읽을 핵심 파일

문서(이 워크트리):
- `/Users/kknaks/orca/workspaces/mediness-mediness/day-chart-photo-spec/products/day/20-spec/spec-002-procedure-board.md` — U-14(:381 근처) · 규칙 31 · 32 · 개정 ⑯ · ⑱(:64 · :68) · 화면 구성 E55 · 기획안 대조 표(:159 「저장」 버튼 줄) · KOS 쓰기 표 · 동기화 표. **본문 모양(개정 머리글 · 표 · 취소선 관례)을 그대로 따른다**
- `/Users/kknaks/orca/workspaces/mediness-mediness/day-chart-photo-spec/products/day/20-spec/spec-001-login-session.md` — U-3 로그아웃 · 웹 화면 절(헤더 후보)
- `/Users/kknaks/orca/workspaces/mediness-mediness/day-chart-photo-spec/products/day/20-spec/spec-000-data-model.md` — `visit_task_chart_log` · outbox · 데이터 규칙(외부 쓰기는 outbox · DB transaction 안에서 외부를 기다리지 않음)
- `/Users/kknaks/orca/workspaces/mediness-mediness/day-chart-photo-spec/products/day/20-spec.md` · `10-decision.md` · `log.md`

코드(read-only · git ref 로 읽는다 — 체크아웃 · 수정 금지):
- DAY `git -C /Users/kknaks/git/CENTURION_DAY show origin/dev:<path>` — `backend/day/services/board_charts.py`(save_chart) · `services/board_chart_writes.py` · `policies/board_chart_rules.py` · `templates/base.html`(:36 ~ 61 헤더 · 로그아웃) · 차트 모달 템플릿(`grep -rl 최근 저장`) · `emr/kos/client.py` · `emr/kos/staff_client.py`(직원 토큰 · User-Agent) · `emr/kos/__init__.py`(경로 상수 · `PATH_CODES`) · `.agents/skills/verify-day-web/features/clinical-chart.md`(지금 자동 저장 동작 · 충돌 · 네트워크 실패 경우 목록 — 명시적 저장으로 무엇이 바뀌는지 대조) · `AGENTS.md`
- cc-prototype(참고): `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/work/_archive/cc-prototype/overall-board/app-backend-report.md` 「WP-BE5」 · 「E2E batch 2 #5」 · 「여권 사진 분류」 절 — 서버에서 KOS 사진을 올린 실물 기록(공개 vs 내부 경로 비교 표 포함)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `products/day/`

## 6. 구현 단계

1. 결정 C1 ~ C16 을 SPEC-002 의 어느 절 · 규칙 · 요소를 바꾸는지 표로 짝짓는다(새 개정 머리글에 「① ② …」로)
2. **차트 저장** — 자동 저장 문장(U-14 · 규칙 31 · 매트릭스 · 기획안 대조 표 · 웹 검증 기능 목록이 가정하는 것)을 찾아 명시적 저장으로 바꾼다. 정할 것: 저장 요청 단위(탭 = 그 방문의 그 차트 종류 시술 줄 전부) · DB transaction 한 번 · 줄별 `baseLogId` 충돌이 한 줄이라도 나면 어떻게 하나 · 바뀐 줄만 이력/outbox · outbox 「반영 중」과 「최근 저장」의 관계 · 시술 전 의사차트(결정 (가))는 그대로인지 · 미저장 경고가 뜨는 경우(✕ · Escape · 바깥 누르기 · 탭 옮기기). 근거 없는 것은 OQ + 「기본값(코디 제안)」 칸
3. **사진 탭** — 화면 구성(새 요소 번호) · 열 때 목록 읽기 · 올리기(여러 장 여부는 OQ) · 삭제 · 썸네일/원본 · KOS 호출 순서(결정 파일 「KOS 사진 흐름」) · 토큰 = 그 직원(규칙 24 와 같은 방식인지 확인) · 분류 · 장비 이름 매칭 실패 · KOS 실패 · 권한(보기 권한이면 올리기 · 삭제 막힘 — 지금 권한 규칙에서 끌어온다). **공개 `generate-uploading-url` vs 내부 `generate-presigned-url`** 중 무엇을 계약에 쓸지 C10 과 cc 기록을 근거로 정하고 이유를 적는다. KOS 쓰기 표 · 동기화 표(사진은 DAY 테이블 없음 — C14)에 반영
4. **헤더 로그인 표시**(C16) — 어느 SPEC 에 둘지 고르고 넣는다. 표시 모양은 OQ(코디 제안 「이름 직군」 · 사용자 확인 전)
5. 화면 글자: 기획안 §4-2 에 있는 글자만 가져온다. 없는 것(사진 탭 글자 · 실패 토스트 등)은 비워 두고 OQ — **지어 넣지 않는다**
6. 케이스 매트릭스 · 오류 글자 · API(이름 제안) · §4 「앞 판과 달라진 곳」 · OQ 를 갱신한다. migration 이 필요한지(차트 저장 · 사진) 판단해 적는다
7. `20-spec.md` · `10-decision.md` · `log.md` 반영
8. §8 검증

## 7. 범위 제약 — 하지 말 것

- 결정 C1 ~ C16 을 다시 열지 않는다. 결정과 기획안 · 앞 판이 다르면 결정을 따르고 차이를 적는다
- 직원 앱(DAY-SPEC-003) 차트 · 사진은 범위 밖(C15) — Out Of Scope 에 「다음 스펙」으로만
- 사진을 DAY DB · Blob 에 저장하는 계약을 넣지 않는다(C14) · 분류 · 장비 코드 테이블을 만들지 않는다(C13)
- 편집 · 보기 권한 규칙을 바꾸지 않는다(C7)
- 화면 문구를 지어 넣지 않는다 · HAR 의 값(토큰 · URL · 고객 이름 · id)을 옮기지 않는다
- 기획안(`00-baseline/planning/`) · 다른 제품 폴더를 고치지 않는다 · WORK 를 쓰지 않는다

## 8. 검증

```
python3 scripts/lint-pipeline.py --strict → products/day/ 범위 ERROR 0 (타 제품 기존 WARN/ERROR 는 '무관'으로 분리 보고). 근거 없는 정책 0 · 열린 것은 열린 것으로
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
  --to term_fae12a17-bcf2-4cd6-8e83-5f06c52bfc17 --from term_3b019a47-8c77-4d76-ba69-466956084d6b \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_fae12a17-bcf2-4cd6-8e83-5f06c52bfc17 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_fae12a17-bcf2-4cd6-8e83-5f06c52bfc17 --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
