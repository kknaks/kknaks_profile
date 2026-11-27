# [planner] SPEC-008 · 006 ⑭ · 005 · 007 고침 6 · 000 ③ → WP 나누기 · Delivery Issue 발행

SPEC 은 검수 4차 FAIL 0 · 커밋됨: 브랜치 `kknaksss/day-reservation3-spec` `1990be22` · PR MediSolveAIDev/mediness#968(draft · 최초 Delivery = pending baseline · **머지하지 마라**).
같은 터미널이면 앞 맥락 그대로. Delivery 절차: `start-delivery` 스킬 · `rules/delivery-workflow.md` · `tools/harness/references/requests.md`(이 워크트리).

작업 워크트리(문서): `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation3-spec`
코드 워크트리(읽기만): `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation3`(origin/dev `a76496c4` · 깨끗 · alembic head `20261125_0030`)

## 할 것
1. **WP 나누기** — backend · frontend **병렬**이 되게(의존은 실제 순서만). 사용자는 **한 번에 코드까지** 가기로 했다 — 판을 여러 Delivery 로 쪼개지 말고 **Delivery 1개**(WP 여러 개)로:
   - BE 바닥: migration(새 표 4 · `notification` 칸 · `NotificationKind` 새 값 · ext partner 칸/유일키 병원 단위) · ext 키 병원당 하나(partner 전수 · 테스트 포함 · taewoo 리뷰 항목)
   - BE ext: E1 ~ E8 · 판정(RQ24) · 메모 합치기 · 오류 코드 · 길이 상한
   - BE 웹: 스레드 읽기 · 생성/수정/취소 쓰기 묶음(SPEC-007 쓰기 큐 · 확인 대기 · 접음 · 스레드 retry · 공용 retry 409) · 변경 요청 · 철회 · 댓글 · 자동 닫힘 · 알림 행 + `announce_unread` · SSE
   - FE: 오른쪽 「예약 요청」 목록 · 상세 창 1 · 2 · 3열(시안 v15) · 2열 시간 머리 칩 · 버튼 규칙(U-5) · 댓글 입력 · 웹 알림 갈래(`day.js`) · `?request=` 열기
   - 각 WP: 범위 · BE ↔ FE 계약(조각 경로 · 넘기는 값 · SSE 이벤트 — SPEC-008 인용) · 완료 조건(**로컬 KOS 데모 지점 실물 e2e 1회** — ext 요청 → 생성 → KOS 확인) · migration · 되돌리기 · **착수 전 실물 확인** OQ-Q01 · Q02 · Q03(BE 첫 단계)
2. **Delivery Issue 발행** — `mediness start-delivery --mediness-repo /Users/kknaks/orca/workspaces/mediness-mediness/day-reservation3-spec --code-repo /Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation3 --github-repo MediSolveAIDev/CENTURION_DAY` `--plan` → `--apply`. baseline = `1990be22`(머지 전 · spec-baseline:pending). 막히면 우회하지 말고 출력 그대로 보고. **승인 receipt 는 적용하지 마라**(코디 몫). json 은 `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation3/orchestration/work/day-reservation3/delivery/`
3. `30-work.md` Spec Coverage 행 · `log.md` 한 줄 → **커밋 · push 해서 PR #968 에 얹어라**(lint 0 error)

## 금지
코드 수정 · SPEC 본문 계약 변경(필요하면 멈추고 보고) · PR 머지 · 승인 receipt 적용.

## 보고
`delivery-1-report.md`(같은 폴더) — Issue 번호 · WP 표 · BE ↔ FE 계약 · baseline · 승인 receipt 적용 명령(코디가 돌릴 것) · 막힌 것. 완료 보고 두 명령(subject 「planner 완료: Delivery 1」).
