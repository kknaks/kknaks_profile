# [planner] SPEC-007 · 006 ⑫ · 002 ㉘ · 000 ② → WP 나누기 · Delivery Issue 발행

SPEC 은 검수 3차 PASS · 커밋됨: 브랜치 `kknaksss/day-reservation2-spec` `479d8f46` · PR MediSolveAIDev/mediness#961(draft · 머지 전 — 최초 Delivery = pending baseline · **머지하지 마라**).
같은 터미널이면 앞 맥락 그대로. Delivery 절차: `start-delivery` 스킬 · `rules/delivery-workflow.md` · `tools/harness/references/requests.md`(이 워크트리).

작업 워크트리(문서): `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation2-spec`
코드 워크트리(읽기만): `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation2`(origin/dev `4bf0b4a1` · **미커밋 변경 있음** — 앞서 멈춘 backend 의 migration `0024_purchase_base_price` · `0025_detail_permission` · 모델 · 매퍼 일부와 frontend 화면 일부. WP 에 「이미 일부 있음」으로 적고 이어서 하게)

## 할 것
1. WP 나누기 — backend · frontend **병렬**이 되게(의존은 실제 순서만):
   - BE 바닥: KOS 쓰기 계획 · `write_open` 새 행 · expect · 순서 묶음 · 할인 전 가격 · 권한 키 · 지정 의사 원천
   - BE 흐름: 예약 등록 · 예약 상세 읽기 · 단계 쓰기 동작 · 우클릭(옮기기 · 취소) · 동행 저장 · 예약 현황 SSE `/reservations/stream`
   - FE: 예약 등록 창 · 예약 상세 모달 · 우클릭 메뉴 · 시술 목록 · 수납 정보 · SSE 연결 · 끌어 묶기 제거
   - 각 WP: 범위 · BE ↔ FE 계약(조각 경로 · 넘기는 값 · SSE 이벤트 — SPEC-007 §3 인용) · 완료 조건(로컬 KOS 데모 지점 실물 e2e 1회) · migration · 되돌리기
2. Delivery Issue 발행 — `mediness start-delivery --mediness-repo /Users/kknaks/orca/workspaces/mediness-mediness/day-reservation2-spec --code-repo /Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation2 --github-repo MediSolveAIDev/CENTURION_DAY` `--plan` → `--apply`. baseline = `479d8f46`(머지 전 · spec-baseline:pending). 막히면 우회하지 말고 출력 그대로 보고. **승인 receipt 는 적용하지 마라**(사용자 몫). json 은 `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/orchestration/work/day-reservation2/delivery/`
3. `30-work.md` Spec Coverage 행 · `log.md` 한 줄 → **커밋 · push 해서 PR #961 에 얹어라**(lint 0 error)

## 금지
코드 수정 · SPEC 본문 계약 변경(필요하면 멈추고 보고) · PR 머지.

## 보고
`delivery-1-report.md`(같은 폴더) — Issue 번호 · WP 표 · BE ↔ FE 계약 · baseline · 막힌 것. 완료 보고 두 명령(subject 「planner 완료: Delivery 1」 · 이번 dispatch 값).
