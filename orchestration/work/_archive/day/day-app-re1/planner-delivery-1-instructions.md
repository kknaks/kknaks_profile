# [planner] SPEC-003 ㉑ · SPEC-002 ㉚ → WP 나누기 · Delivery Issue 발행

너는 day `planner` 워커다. 역할 · allowed_paths(`products/day/`) · 완료 보고 형식은 같은 폴더 `day-app-re1-spec-brief.md` 를 따른다(먼저 읽어라).

SPEC 은 검수 끝(review-doc-2 + fix-2) · 커밋됨: 브랜치 `kknaksss/day-app-re1-spec` `e7c51875` · PR MediSolveAIDev/mediness#964(draft · **머지하지 마라** — 최초 Delivery = pending baseline · 사용자가 나중에 한 번에 머지).
Delivery 절차: `start-delivery` 스킬 · `rules/delivery-workflow.md` · `tools/harness/references/requests.md`(이 워크트리). 앞 작업 예시: `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/_archive/day/day-reservation2/planner-delivery-1-instructions.md` · `delivery-1-report.md` · `delivery/`(파일 이름 관례).

작업 워크트리(문서): `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-re1-spec`
코드 워크트리(읽기만): `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-app-re1`(origin/dev `55e60aa4` · 깨끗함)

## 할 것
1. **WP 나누기** — backend · mobile **병렬**이 되게(의존은 실제 순서만). 기대 모양(근거가 다르면 고쳐도 된다 — 이유를 적어라):
   - **BE**: 앱 `/api` JSON 짝 6(SPEC-002 개정 ㉚ — 차트 탭 저장 · 사진 목록 · 올리기 · 삭제 · 다시 시도 · 파일) · 앱 Bearer 인증 · 웹 경로와 같은 서비스 · 오류 코드 · 테스트
   - **APP**: SPEC-003 U-23 — 차트 화면(값 원천 `GET /api/visits/{id}/chart` · 탭 셋 · 탭별 저장 · 담당자 고르기 · 미저장 닫기 · 사진 탭 · 10초 가져오기) · 루트 Navigator(D4 · D14) · 까만 줄 테마 · iOS 권한 문구(D15) · 폰 전체 화면 / 아이패드 가운데 창 · 테스트
   - 각 WP: 범위 · **BE ↔ APP 계약**(경로 · 요청 · 응답 · 오류 — SPEC 인용, 두 워커가 같은 글을 본다) · 완료 조건(BE = 로컬 KOS 데모 지점 실물 호출 1회 · APP = 시뮬레이터에서 로컬 BE 로 저장 · 사진 1회) · migration(없음) · 되돌리기
2. **Delivery Issue 발행** — `mediness start-delivery --mediness-repo /Users/kknaks/orca/workspaces/mediness-mediness/day-app-re1-spec --code-repo /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app-re1 --github-repo MediSolveAIDev/CENTURION_DAY` `--plan` → `--apply`. baseline = `e7c51875`(머지 전 · spec-baseline:pending). 막히면 우회하지 말고 출력 그대로 보고. **승인 receipt 는 적용하지 마라**(사용자 몫). json 은 `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/delivery/`
3. `30-work.md` Spec Coverage 행 · `log.md` 한 줄 → **커밋 · push 해서 PR #964 에 얹어라**(lint 0 error)

## 금지
코드 수정 · SPEC 본문 계약 변경(필요하면 멈추고 보고) · PR 머지 · 승인 receipt 적용.

## 보고
`/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/delivery-1-report.md` — Issue 번호 · WP 표 · BE ↔ APP 계약 전문 · baseline · 막힌 것. 완료 보고 = dispatch preamble 의 `worker_done`(`--report-path` 위 리포트) + 브리프 §9 (2) 직접 주입(subject 「planner 완료: Delivery 1」).
