# [planner] SPEC-001 0.3.0 · WORK-001 — 에이전트별 탭 · SQLite 저장 · 증분 조회

너는 **agency-settlement `planner` 워커**다. **맥락이 없다고 가정하고** 먼저 읽어라:
- 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/roles/agency-settlement/planner/role.md` (+ 같은 폴더 문서)
- 결정: `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/10-decision/decision-001-monthly-sales-list.md` — **D-10 ~ D-13 이 새로 생겼다**
- 결정 원천: `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/_RESUME.md` §2(2026-10-29 줄 전부 · 이기는 순서 1번)
- 지금 계약: `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/20-spec/spec-001-monthly-sales-list.md`(0.2.1) · `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/30-work/work-001-monthly-sales-list.md`
- 지금 코드(구현 완료 · 운영 10월 조회 성공): `/Users/kknaks/orca/workspaces/agency-settlement/agency-settlement/back/` · `/Users/kknaks/orca/workspaces/agency-settlement/agency-settlement/front/` — 읽기만
- 코드 리뷰 리포트(남은 SPEC 정리 몫): `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/review-code-r1-report.md` W-3 · W-1 · W-5 · W-6
- 시안 v1: `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/design-upload/Ceramique 월별 매출 v1.dc.html` · `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/design-report.md`(정할 것). 시안 v2(에이전시 탭)는 frontend 가 병렬로 만든다 — 화면 세부는 「시안 v2 대로」로 두고 계약(API · 저장)에 집중

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터` (코디 워크트리). allowed_paths: `para/projects/summer-star/agency-settlement/20-spec/` · `30-work/` 만.

## 할 것 — SPEC-001 0.3.0
1. **D-12 저장 · 증분**: `back/` SQLite(파일 경로 env · gitignore). 무엇을 저장하나(① ② ⑤ 를 줄인 필드 · ③ 이름 · 방문일 — 개인정보는 이름만 · 원본 JSON 저장 금지) · 달 상태(`closed` / `current`) · 지난 달 = 첫 조회 때 받고 끝(다시 안 부름) · 이번 달 = 마지막 받은 시각 − 겹침 여유 이후 ① 만 더 부르고 중복은 거래 키로 막음 · ② · ⑤ · ③ 은 새 수납 · 새 거래에만 · [전체 다시 받기](`refresh=full`) · 달이 바뀌는 순간(이번 달 → 확정) 처리 · 증분으로 놓치는 것(이미 받은 품목의 상태 변화 — D-13) · 동시 요청 잠금. 메모리 캐시(OQ-105)는 대체
2. **D-11 에이전트별 조회**: API(예: `GET /api/agencies?month=` 목록 + `GET /api/sales?month=&agency=` 또는 같은 응답에서 front 가 거름 — 근거와 함께 하나를 고르고 OQ 에 대안) · 「에이전시 전체」 · 에이전시 판정 = 최초 유입 채널 이름이 「(에이전시)」로 끝남(자유 텍스트 추정 금지) · 손님 수 · 결제 손님 수 정의
3. **D-10 화면**: 헤더 메뉴 · 넓은 폭 · 「받은 시점 기준」 · 마지막 받은 시각 · 이번 달/지난 달 버튼 — 세부는 시안 v1 · v2 를 가리킨다
4. code r1 남은 SPEC 정리: W-3(§5.4 at 만 null · 잇기 유지) · W-1(§6.2 표 한 줄) · W-5(§6.7 통화 0개) · W-6(SALES_BACK_PORT)
5. WORK-001: 다음 WP(BE2 저장 · 증분 · 에이전시 API / FE2 시안 적용 · 탭 / REVIEW2 / LIVE2 — 9월 한 번 받고 다시 열 때 KOS 호출 0 · 10월 증분 호출 수) 추가
6. 판 0.3.0 · 인덱스 · public grep(실명 · 에이전시 실명 · 실제 금액 · 키 0)

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_d291ae3b-f96b-492e-8274-6c3e14da473f --from term_53ce52e0-0768-4aa5-ad16-a1fb4e218878 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: SPEC-001 0.3.0" \
  --body "변경 파일 목록 / 요약 / 검증 결과(수치) / 미결·주의점"

orca terminal send --terminal term_d291ae3b-f96b-492e-8274-6c3e14da473f \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_d291ae3b-f96b-492e-8274-6c3e14da473f --text "[질문] planner: <질문>" --enter`
