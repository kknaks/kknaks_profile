# 구현 추가 지시 1 — review-doc r2 WARN 반영 (backend · frontend 공통)

원천: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/reservation-review-doc-r2.md`. SPEC-005 0.2.0 본문 개정은 다음 판에 같이 한다 — **이 파일이 SPEC 보다 우선**.

1. **W1 (frontend · FE3)** — 상세 모달도 조작 성공 **직후 1번 + 2초 뒤 1번** 다시 읽는다(스케줄 표와 같은 규칙 · §6.7). 고객 정보 저장 → `identity.complete` 켜짐 · 메모 · 진행 경로 저장이 바로 보이게
2. **W2 (frontend · FE1 / backend 확인)** — 드래그: **끄는 카드의 구역이 그 칸 `columns[].capacities[].zoneId` 에 없으면 놓기 금지**(빨간 점선 · `full` 과 같은 표시). back `move` 는 그 경우 400 `invalid_request`(지금 계약 그대로)
3. **W3 (둘 다)** — WORK-007 대상 파일에 더한다: back `app/domain/errors.py` · front `app/layout.tsx` · `app/globals.css` · `lib/hooks.ts` · `package-lock.json`. 이 파일들은 allowed_paths 안이다
4. **W4 (둘 다 · 코디 기본값 — U4 「부도 접수 허용 = KOS 그대로」의 따름)** — 부도(`noshow`) 카드도 `reserved` 처럼 **진행 경로 라디오 · 예약 메모 [저장]을 연다**: 진행 경로 켜짐 = `main ∈ {reserved, noshow}` + 재진 · 메모 저장 = `main ≠ canceled`. back `can.*` 계산 · front 버튼 둘 다
5. **W5 (둘 다)** — 오류 본문 §7.1 에 `fields?: string[]`(값 = §7.3 `identity.fields[].key` 와 같은 KOS 키 · 예: `passportNumber`) — `identity_incomplete` 때 실린다
