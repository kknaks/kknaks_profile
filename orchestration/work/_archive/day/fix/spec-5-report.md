# fix-spec-5 결과 보고 — 읽음 표시 계약 정정 1

## 상태: done

출처 = `fix/correction-read-1.md` 「결정」 1 · 2 · 3(문서 리뷰 [긴급] 지적 · 코디 결정 2026-11-11). 스펙에는 「사용자 확정을 바꾸지 않는 계약 구멍 메우기 기술 규칙」으로 적었다. 커밋 · push 0.

## 고친 자리

| 문서:줄 | 내용 |
|---|---|
| `products/day/20-spec/spec-004-internal-chat.md:30` | 머리 개정 ④ 끝에 「정정 1」 한 줄 |
| `spec-004:186` | U-2 「메시지별 읽음 표시」에 새 줄 **「멤버 읽은 자리 합치기」** — ① 받은 메시지(실시간 · 목록 · `since` 메우기 · 전달)의 보낸 사람 `lastReadSeq = max(지금, seq)` · 시스템 줄 제외 · 서버 규칙 「보낸 사람 읽음 = 그 메시지」를 따르는 것(새 업무 규칙 아님) · 없으면 「받은 뒤 읽음 요청 전에 답장」에서 숫자가 재연결까지 남는 이유 ② 늘 max · 다시 들어온 멤버만 새로 |
| `spec-004:372` | 규칙 「읽음 표시 계약」 — 앱 합치기 규칙 · 서버 변경 없음 |
| `spec-004:437` | 실시간 표 `chat_member_read` — 보내기는 이 이벤트를 내지 않음 · 앱은 받은 메시지로 맞춤 · 늘 max |
| `spec-004:477-479` | 케이스 매트릭스 — 끊긴 동안 줄에 max · 새 2줄(읽음 요청 전 답장 · 전달 / 옛 `Room` · 순서 뒤바뀜) |
| `spec-004:605` | C-A24 — 「보내기는 `chat_member_read` 를 내지 않고 보낸 사람 `lastReadSeq` 는 다음 `Room.members[]` 에 그 seq 로」 시험 |
| `spec-004:606` | C-A25 — 정정 1 갈래(읽음 요청 전 답장 · 전달 · 옛 `Room` · 순서 뒤바뀜 · 다시 들어온 멤버) |
| `products/day/log.md` | 5판 1줄 |
| `orchestration/work/fix/wp-plan.md:163` | WP-BE-3 시험 — 보내기 전제 시험 한 건 |
| `wp-plan.md:167` · `:180` · `:185` | WP-APP-3 제목(정정 1 포함) · `chat_state.dart` 줄(받은 메시지 max · `Room` 덮기도 max) · 시험 갈래 |
| `wp-plan.md:209` | §3 읽음 계약 표 새 줄 「멤버 읽은 자리 합치기」 |

서버(결정 3)는 그대로 — 4판 계약(`chat_member_read` = #15 가 올렸을 때만 · `Room.members[]` 칸) 바뀜 없음.

## Delivery #241

손대지 않음. 결과 계약 범위(Target Delta 10번 · Non-Goals)와 수용 항목의 뜻(C-A24 · C-A25 = 읽음 표시 서버 · 앱)은 그대로 — 시험 갈래가 늘었을 뿐 범위 · 위험 변화 없음.

## 검증

`python3 scripts/lint-pipeline.py --strict` → exit 0 · 0 error, 263 warning · `products/day/` 줄 0(263 WARN 은 타 제품).
