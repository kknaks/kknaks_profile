# 리뷰 리포트 — 상단 인박스 탭 제거 SPEC 개정 ⑤ · WP v6 W1/baseline 정정 재검수 (2026-11-10)

- 대상:
  - `products/day/20-spec/spec-003-mobile-app.md`(`4a5d4a47` 위 미커밋 · 앞 리뷰 +31/−30 → 지금 +33/−31)
  - profile `delivery-request-v6.json`
- 근거: 앞 리뷰 `review-tabs-removal-spec-report.md` W1 · 참고 1 · `tabs-removal-spec-fix-report.md`
- 방법:
  - 수정 줄 직접 대조 · `git diff --check`
  - v5 ↔ v6 경로 diff · 모델 1회
  - 전체 lint · 테스트는 반복하지 않았다
  - 수정 · 하위 위임 없음

## 판정: PASS (FAIL 0 · WARN 0)

| 확인 | 실제 근거 | 결과 |
|---|---|---|
| W1 레일 복원 | Wireframe 아이패드 열 `:105-111` 레일 = `DAY / 예약 / 현황 / 시술 / 현황 / 채팅 / 설정`(= 예약현황 · 시술현황 · 채팅 · 설정 4메뉴). 복원 줄 `│ 현황 │ (빈 본문) │`이고, 폰 열 같은 줄은 빈칸이다. 인박스 탭 글자는 양쪽 모두 없다 | PASS — 늘어난 1줄은 레일 칸뿐 · 새 기능 · 글자 없음 |
| 개정 ④ 역사 꼬리 | `:41` 「… 호출 탭에서만(U-6 직무 분기 · API · 서버 권한 그대로 · 호출 탭은 이후 개정 ⑤ 로 없음)」 | PASS — 꼬리 한 구절만 |
| SPEC 다른 변경 | diff hunk 목록 · 줄 수 차이(+2/−1)가 위 두 자리로 설명된다 | PASS — 의미 · AC · 권한 무변경 |
| baseline 필드 | `spec_baseline_revision` = `9692e1fb461bf8c4e52bf489e37ab8ff875f9918` = 로컬 `origin/main`(rev-parse 일치). `git diff 3f57c1af..9692e1fb -- products/day/` 비어 있음 · 9692e1fb의 SPEC-001 `status: draft` · SPEC-003 파일 없음 → **pending 유지 정직** | PASS |
| baseline 문장 | scope_delta 끝 · `review_surface[0]` 첫 문장만 9692e1fb로 정정. 남은 `3f57c1af` 2곳은 「3f57c1af..9692e1fb 사이 변경 없음」 · 「3f57c1af 뒤 변경 없음」 비교 문맥이다 | PASS |
| JSON 범위 | v5 대비 바뀐 키 = 앞 리뷰 20개 + `spec_baseline_revision` 1개 = 21. A0 ~ A28 · target_delta · non_goals · 권한 · app/만 · PR #237 · L3 · contract_version 6은 앞 리뷰 PASS 판 그대로. 승인 receipt · 승인 주장 없음 | PASS |
| 검증 | `git diff --check` exit 0 · `DeliveryRequest.model_validate` OK(v6 · L3) · planner 보고 schema 0 errors | PASS |

## 남은 것

- 코디: 개정 ⑤ 커밋(exact head) → v6 plan(origin/main 재 fetch · 9692e1fb 확인) → L3 승인 → #235 apply → mobile 발주.
