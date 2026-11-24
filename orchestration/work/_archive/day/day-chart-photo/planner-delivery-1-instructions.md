# [planner] SPEC-002 개정 ㉘ → WP 나누기 · Delivery Issue 발행

너는 이 개정을 쓴 planner 다. SPEC 은 검수 PASS · 커밋됨: 브랜치 `kknaksss/day-chart-photo-spec` `a896cda0` · PR MediSolveAIDev/mediness#960(머지 전 — 머지하지 마라).
맥락이 없으면 읽어라(이 폴더 `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/work/day-chart-photo/`): `day-chart-photo-spec-brief.md` · `planner-fix-1-report.md` · `planner-fix-2-report.md` · `review-doc-3-report.md` · 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/reference/2026-11-24-day-picture/chart-photo-decisions.md`(C1 ~ C17).
Delivery 절차: `start-delivery` 스킬 · `rules/delivery-workflow.md` · `tools/harness/references/requests.md`(이 워크트리). 앞 작업의 같은 발주 기록: `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/work/_archive/day/day-reservation/planner-delivery-1-instructions.md` · `delivery-1-report.md`(참고 — 막혔던 곳 · 쓴 명령).

작업 워크트리(문서): `/Users/kknaks/orca/workspaces/mediness-mediness/day-chart-photo-spec`
코드 워크트리(읽기만): `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-chart-photo` (origin/dev `4bf0b4a1`) — 레포 루트 `AGENTS.md` 먼저

## 할 것
1. 개정 ㉘(+ SPEC-001 ⑫)을 WP 로 나눈다. 축 제안(근거 있으면 바꿔도 됨 · 이유 적기):
   - **backend** — 탭 저장 API(transaction · `base` 비교 · KOS 확인 · 충돌 응답 · outbox 묶음 · event) · 사진 API 5개(KOS 내부 이미지 호출 · 직원 토큰 · 서버 경유 · 이름 매칭) · 옛 줄 저장 경로 정리
   - **frontend** — 모달 탭 3 · [저장] · 최근 저장 · 미저장 확인 창 · 충돌 칸 채움 · 사진 탭(시안 전이라 구조만 · 글자 OQ 비움) · 헤더 로그인 표시 · 자동 저장 JS · `verify-day-web` 차트 기능 문서 갱신
   - BE ↔ FE 계약(경로 · 요청/응답 · 조각)을 WP 에 명시 → 병렬 가능하게. 의존은 실제 순서만
   - 각 WP: 범위 · 완료 조건(**실물 e2e 1회 — 로컬 · KOS 데모 지점**: 탭 저장 · 충돌(KOS 웹에서 먼저 고친 뒤 저장) · 사진 올리기/삭제가 KOS 일정 사진 탭에 보이는지) · migration 여부(없음 예상) · 되돌리기
2. Delivery Issue 발행 — `mediness start-delivery --mediness-repo /Users/kknaks/orca/workspaces/mediness-mediness/day-chart-photo-spec --code-repo /Users/kknaks/orca/workspaces/CENTURION_DAY/day-chart-photo --github-repo MediSolveAIDev/CENTURION_DAY` `--plan` → `--apply`. baseline = `a896cda0`(머지 전). harness 가 main 머지를 요구해 막히면 **우회하지 말고** 이유 · 출력 그대로 보고. **승인 receipt 는 적용하지 마라**(사용자 몫). plan / request / apply json 은 `…/day-chart-photo/delivery/` 에 남긴다
3. `30-work.md` Spec Coverage 행(lint 규칙대로) · `log.md` 한 줄 — 커밋하지 마라(코디가 #960 에 얹는다)

## 금지
코드 수정 · 커밋 · push · PR · 머지 · SPEC 계약 변경(필요하면 멈추고 보고).

## 보고
`…/day-chart-photo/delivery-1-report.md` — Issue 번호 · WP 표(범위 · 의존 · 완료 조건) · BE ↔ FE 계약 · baseline · 막힌 것. 완료 = preamble 의 worker_done 두 채널.
