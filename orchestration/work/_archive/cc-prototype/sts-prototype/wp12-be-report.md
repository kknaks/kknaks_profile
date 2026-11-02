# WORK-001 WP12 결과 보고 (backend) — 근거 없는 표시 빼기 (E2E #27 · #28)

## 상태: done

## 수행 — 파일

`cc/back/` 만. 커밋 · push 없음.

| 파일 | 변경 |
|---|---|
| `app/service/memos.py` | `visible_texts` · `mentioned_staff` · `risk_hits` · `customer_mentions` 삭제 — 방문 카드(`visits`)만 남음 |
| `app/service/patient_service.py` | 응답에서 `riskWords` · `riskHits` · `mentionedStaffIds` 삭제 · 생성자 인자 정리 |
| `app/service/board_service.py` | board 의 `customers[].mentionedStaffIds` · `riskWords` 삭제 |
| `app/config.py` · `app/container.py` | `CC_RISK_WORDS` 설정 · 전달 삭제 |
| `.env.example` · `README.md` | `CC_RISK_WORDS` 줄 · 응답 예시의 세 필드 · 설명 줄 삭제 |
| `tests/test_scenario.py` | 해당 단언 삭제 → 「세 필드가 응답에 없다」 단언으로(`test_memos_raw_no_unfounded_marks`) |

## 검증

| 명령 | 결과 |
|---|---|
| `uv run pytest` | **53 passed** |
| `uv run ruff check .` | **All checks passed** |
| `grep mention · risk` (`app/`) | 0 |

## 계약 대조

- 응답에서 빠진 필드: `GET /api/patients/{id}` 의 `riskWords` · `riskHits` · `mentionedStaffIds`, `GET /api/board` 의 `riskWords` · `customers[].mentionedStaffIds`. 그 밖 모양 그대로
- 메모는 원문 그대로(0.3.0) · 셀렉터의 직원 목록 = board `staff`(직군 · 지금 일 `work`)로 front 가 거른다

## 이슈

- 8600 서버는 코드 반영을 위해 재시작만(시드 · DB 변경 없음). front WP12 는 이 필드들을 더 이상 기대하지 않아야 한다
