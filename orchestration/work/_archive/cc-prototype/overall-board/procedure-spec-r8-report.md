# procedure-spec r8 결과 보고 — review-doc r5 처분 반영

## 상태: done

## 수행 내용
- `para/projects/summer-star/cc-prototype/20-spec/spec-003-procedure-board.md` — 0.6.0 그대로 · 고친 줄 끝 `(r8)` · 머리말 0.6.0 줄에 r8 한 문장
- `para/projects/summer-star/cc-prototype/30-work/work-008-procedure-board-v2.md` — sources · Meta · 계약 고정점 · WP-FE2 · WP-FE3 · WP-E2E · 하지 않는 것
- `para/projects/summer-star/cc-prototype/log.md` — r8 한 줄

## 처분 → 고친 곳 대조표

| # | 처분 | 고친 곳 |
|---|---|---|
| W1 | 판 = 흰 판(스크롤 컨테이너) 전체 · 가장자리 12px 도 판 안 | SPEC §5.12 「놓는 곳」 · §6.3 드래그 줄 · 부록 K.2 기본값 줄 · WORK 계약 고정점 「놓기」 · WP-FE2(「격자 영역에서도」 → 「흰 판에서도」 · 「격자의 drop」 → 「판의 drop」) |
| W2 | `fake_board.py` 예시 값만 예외 · 카드 수 5 유지 · 있는 카드 값만 · `cd procedure/back && uv run pytest -q` | WORK Meta 코드 레포 줄(예외) · WP-FE3 대상 파일 · 완료 조건 · 검증 · WP-E2E 검증(`pytest` → `uv run pytest`) · 하지 않는 것 back 줄 · SPEC §9 끝 「0.6.0 더함」 back 무변경 문장에 예외 |
| W3 | WP-E2E · §9 #32 에 「SPEC-005 §9 #42 부상태 색 그대로」 | SPEC §9 #32 · WORK WP-E2E 내용 · 완료 조건 |
| W4 | 발음 근거 문구만 | SPEC §6.3 고객 줄 발음 — 「같은 꼴」 → 「같은 관계(이름보다 한 단계) · 값은 다름(그쪽 body-600 / body-400)」. 값 `caption-md-400 gray-500` 그대로 |
| W5 | #28 = 오른쪽 칸 한 줄 · 시술 이름 줄바꿈 허용 | SPEC §9 #28 |

## 검증
- 처분 5줄 → 고친 곳 빠짐 0
- 옛 문구 grep: 「격자 영역 전체」 0 · 「두 줄로 밀리지」 0 · `back && pytest -q`(uv 없음) 0 · 발음 「같은 꼴 · 구현 `ResvAside`」 0 (남은 1건 = §5.14 대조표 #1 Badge 줄 — 리뷰 §2 에서 맞음 확인된 Badge 꼴이라 W4 대상 아님)
- public grep(바뀐 줄): 실명 · KOS id · 키 · 토큰 0 (걸린 것 = 기존 커밋 해시 `901267f` 뿐)
- 코드 수정 없음 · allowed_paths 안

## 미결·주의점
- W1 · W2 의 frontend 확인(지금 구현이 흰 판에 drop · fake_board 카드 수) 은 frontend 몫
- W5 는 사용자 E2E(#28 · OQ-534)에서 판단
- 리뷰 「참고」(log 「14곳」 셈 · `'warning'` grep 패턴) 는 이번 처분 밖이라 손대지 않음
