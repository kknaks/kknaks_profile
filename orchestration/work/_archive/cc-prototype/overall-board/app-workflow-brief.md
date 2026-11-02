# [planner] ① 앱 다음 판 — 앱 업무 흐름(workflow-app) 초안

너는 **cc-prototype `planner` 워커**다. **앞 판 맥락이 없다.** 먼저 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/planner/role.md`(+ 같은 폴더 rules · skills · tools · workflow)를 읽어라 — 「앱 · 새 화면은 시안이 정본 · 배포된 웹은 구현본이 정본」. 작업 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc`(공유).

**이번 판은 흐름 문서 하나만 쓴다.** 사용자가 흐름을 확인한 뒤 SPEC-004 · DEC · WORK 를 다음 판에 쓴다.

## SSOT
- 결정 정본: `orchestration/work/overall-board/_RESUME.md` §2 **2026-10-26 · 10-27 줄 중 앱에 닿는 것 전부** — 앱 범위 · 앱도 쓴다 · 웹이 정본(앱은 웹 규칙) · 상담사 계정 · 배정 푸시 · QR 문진(국적/언어 · 방문별 이력) · 스캐너(여권만 · 가이드 = 마스킹 · 사진 ccc · KOS 둘 다 · 법적 검토 주석) · 문진 언어 원천 · iOS 만 · 시안에서 뺌 · 수납 · 처방전 = 웹만 · **알림 = 상담사 호출 · 의사 호출 두 가지만** · 코디 역할 · 동시 로그인 구상(10-26) · 직무별 권한은 마지막
- 앱 시안(정본 · 로컬만 · 실명 옮기지 마라): `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-23-cc-overall-board/design/` — `Ceramique 모바일 v4.dc.html` · `Ceramique 태블릿 v4.dc.html` · `의료진 앱 (구현 v3)` 등. 분석: `orchestration/work/overall-board/design-refresh-report.md`(§3 화면 · §6 정할 것 Q-1~16)
- KOS 근거: `app-kos-report.md`(고객 수정 · 언어 · 공개 문진 제출) · `reservation-questionnaire-report.md` · `reservation-visitor-update-report.md` · `reservation-create-report.md` · `reservation-consultation-report.md`
- 웹 계약(앱이 따를 규칙): `para/projects/summer-star/cc-prototype/20-spec/spec-005-reservation-board.md` 0.4.0 · `spec-003-procedure-board.md` 0.6.0 · 지금 앱 계약 `spec-004-procedure-app.md` 0.3.2(§10.1 앱 후속 포함)
- 지금 앱 코드(읽기만): `/Users/kknaks/orca/workspaces/cc-prototype/overall-board/procedure/app/` · back 계정 · 푸시(`push_log` · APNs)

## 쓸 문서
- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-27-cc-app/workflow-app.md`(새) — 형식은 `reference/2026-10-26-cc-reservation/workflow-v3.md` 를 따른다:
  1. 사람(역할) × 기기(폰 · 태블릿 · 데스크 웹)별 하루 흐름 — 코디 · 상담사(실장) · 간호사 · 의사 · 데스크
  2. 화면 목록(시안 4탭 + 로그인 · 알림 · 문진 화면(고객용) · 스캔 화면 · 스캔 확인) — 화면마다 시안 근거(`M:` · `T:` 줄) 또는 「시안 없음 → DS 기본값」
  3. 흐름별 단계: 예약 · 내원 현황(웹과 같은 쓰기) · 상담사 배정 → 푸시 · 의사 호출 푸시(지금 그대로) · QR 문진(웹 [태블릿에 띄우기] → 기기 → 고객 입력 → KOS 제출 · 언어 고르기 순서) · 여권 스캔(가이드 · 마스킹 · 새 고객 / 기존 고객 · KOS 쓰기 · ccc 사진 저장) · 웹 따라잡기(되돌리기 · 2계층 · 공유 순서)
  4. KOS 표(단계 → API · 공개/내부 · 확인됨/미확인 · 근거 리포트)
  5. 웹 ↔ 앱 차이 표(앱에서 뺀 것 · 보기만인 것 · 시안과 웹이 다를 때 웹 규칙)
  6. **정할 것** 목록(번호 · 기본값 제안 · 결정하지 마라) — 예: 상담사 계정 만드는 법 · 기기 하나에 여러 계정 · 문진 화면 잠금(고객이 다른 화면으로 못 가게) · 스캔 실패 때 · 사진 저장소(infra)
- 보고 `orchestration/work/overall-board/app-workflow-report.md`(결정 줄 → 흐름 대조 · 빠짐 0)

## 금지 · 검증
- allowed_paths = 위 두 파일. 코드 · SPEC · DEC 수정 금지 · 실명 · KOS id · 키 · 토큰 금지(public)
- 열린 것은 정할 것으로. 결정 줄과 다른 흐름을 지어내면 FAIL

## 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 커밋·push 금지.
```bash
orca orchestration send --to term_678ac61d-2472-4a9b-ba73-61883337b957 --from term_9c9f00d7-1f83-4040-890e-02b80c9c329d --type worker_done \
  --task-id <preamble 의 taskId> --dispatch-id <preamble 의 dispatchId> \
  --subject "planner 완료: <한 줄>" --body "산출 경로 / 요약 / 검증 수치 / 정할 것 개수"
orca terminal send --terminal term_678ac61d-2472-4a9b-ba73-61883337b957 --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
