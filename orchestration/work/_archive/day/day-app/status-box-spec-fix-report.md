# status-box-spec-fix 결과 보고 — 상태 박스 SPEC/WP 범위 최소 정정

## 상태: done (코드 · GitHub · 커밋 · push · merge · 하위 위임 없음)

직전 task_1bca8d3f2090 산출물에 코디 범위 정정(msg_8b0c1ac0cbd9 · msg_8e028282c03f · msg_ac0b6a17bef2 — 호출 박스 제외 · 시술 중 대표 행 일치)을 반영했다. 이전 보고 `status-box-spec-report.md` 는 그 단계 로그로 보존(무수정) — 그 보고의 「호출 상태 박스 2줄」 서술은 이 정정으로 무효.

## 1) 호출 박스 변경 제거 — 현재 상황 상자 4상태만

| 자리 | 처리 |
|---|---|
| SPEC-003 U-3 「호출 뒤 카드」 본문 | `git show cdde456a` 원문 줄로 되돌림(그 줄만 교체 · 전체 reset 아님) — diff 결과 원문과 같음 |
| SPEC-003 A-30 | `cdde456a` 원문 그대로 — diff 결과 같음 |
| 개정 ③ 머리 요약 | 「모든 상태에서 2줄」 → 「4상태(시술 대기 · 마취 중 · 마취 완료 대기 · 시술 중) 2줄」 · 호출 상태 박스 · 호출 줄 · 수락 · 귀가 대기 자리는 바꾸지 않음 명시 |
| U-3 4번 줄 | 제목 「4상태 2줄」 · 시술명 규칙에서 「호출 상자 = called 줄」 제거 · **범위** bullet 추가(호출 상태 · 호출 줄 · 수락 · 귀가 대기 그대로 · 겹치면 호출 상태 기존 기본값 그대로) |
| A-28 | 「4상태 2줄 · 호출 상태 박스는 A-30 그대로」 |
| OQ-A21 | 호출 집계 제거 · 겹치면 호출 상태(개정 ③ 이 바꾸지 않음) |
| v4 JSON | scope_delta · target_delta[v4] · review_surface[-1] · acceptance[0](「A16 · A17 · A18」 → 「A16 · A17」) · **A18 = v3 원문 그대로** + 「이번은 현재 상황 상자 4상태만 · 호출 정의는 v3 그대로」 · phases[3] · verification[0] |

SPEC · JSON 어디에도 「수락 대기 · mm:ss」 · 호출 박스 2줄 · 호출 시술명 집계가 남지 않음(grep 0 · JSON assert).

## 2) 시술 중 대표 행 일치

- 대표 행 = 서버 줄 순서 첫 `doing` 줄 — 그 행의 `startedAt`(「시술 중 · mm:ss」) · `doctor.name`(없으면 「담당의 미정」) · `title` 을 함께 쓴다. 나머지 `doing` 줄만 「외 N개」. 시간 · 담당의가 다른 시술을 설명하지 않는다.
- 시술 대기 · 마취 = `done` 아닌 줄 서버 순서 첫 `title` + 나머지 「외 N개」 · 담당의는 기존 첫 담당의 fallback · 없으면 「담당의 미정」.
- 반영 자리: SPEC U-3 시술 중 bullet · 담당의 bullet · 시술명 bullet · A-29 · OQ-A21 / JSON A16 · A17 · target_delta[v4] · scope_delta · review_surface[-1] — SPEC · JSON 같은 문장 뜻.
- 앱 표시 선택일 뿐 새 업무 판정 · 우선순위 · 다중 담당의 정책 없음.

## 3) 룸 머리 가운데 정렬

- 기록만(OQ-A31 그대로) · 구현 요구 추가 없음 · scope 변경 없음.

## 검증 (각 1회)

- `git diff --check` 통과 · `python3 scripts/lint-pipeline.py --strict` → exit 0 · **0 error, 263 warning** · `products/day/` 0건
- v4 JSON parse OK · jsonschema **0 errors** · `DeliveryRequest.model_validate` OK(v4 · L3 · acceptance 27)
- `delivery-request-v3.json` 무수정

## 남은 것

- SPEC 개정 ③ 미커밋(cdde456a 위) — 코디 커밋 head 로 v4 결속.
- 독립 리뷰 → v4 plan · L3 승인 → apply → mobile 코드 발주(RoomCard._nowBox 4상태만).
