# day-app planner — 재리뷰 N-1 ~ N-3 정정(fix2) 보고

## 상태: done

- task `task_1f51f6e72a19` · dispatch `ctx_1301c3d0e543` · 원천 `review-spec2-report.md` · 이전 보고서 보존
- 커밋 · push · PR 없음 · 문구 · 정책 · 계약 변경 없음(위치 · 참조 정정만)

## 수정 위치

| 지적 | 파일:줄 | 고친 것 |
|---|---|---|
| N-1 | `products/day/20-spec/spec-003-mobile-app.md:548`(A-18) · `:554`(A-24) | A-24 끝에 붙어 있던 `✓ \| ✓ release(D-1 전 prod 에 붙이면 실패해야 함)` 두 칸을 A-18 행 끝으로 옮김. 인수조건 표 머리 · 모든 행 4칸(인라인 코드 안 파이프 제외 기계 확인 — 어긋난 행 0) |
| N-2 | `spec-003-mobile-app.md:358`(「연결 대상 검증」 비교 줄) · `:550`(A-20) | 병원 고르기 응답 = `api_base_url`(정규화 origin) + `environment` 둘 다 비교 / `/me` 응답 = `environment` 만 비교로 나눔. `/me` 에 새 칸 없음(SPEC-001 「응답 칸」 그대로) |
| N-3 | `products/day/20-spec/spec-001-login-session.md:289`(규칙 3 본문) · `:293`(늦은 성공 불릿) | 기존 만료 근거 참조 「규칙 8」 → 「§4 규칙 8」. 「dev 가 4xx 오류(…)를 주면 그 HTTP · 본문 그대로」 문장을 늦은 성공 하위 불릿에서 규칙 3 본문(첫 줄 뒤)으로 옮김 — 뜻 그대로 |

## 검증

- `git diff --check` → 출력 없음(exit 0). 추적 안 된 `spec-003-mobile-app.md` 줄끝 공백 0(grep).
- `python3 scripts/lint-pipeline.py --strict` 1회 → exit 0 · `0 error, 263 warning` · products/day 해당 0. 263건은 전부 다른 제품 — 무관.
- 변경 파일 = 기존 5파일 그대로(`30-work.md` 는 승인 한 줄 그대로 · 이번 변경 없음). 이번에 손댄 파일은 `spec-003-mobile-app.md` · `spec-001-login-session.md` 둘.

## 미결

- 정책 OQ(OQ-A15 통역 권한 · OQ-A17 푸시 대상 · 알림 수락 조건 · OQ-A1 · A9 · A11) — 사용자 답 대기 · 열린 그대로.
