# tabs-removal-spec-fix 결과 보고 — 아이패드 레일 ASCII W1 + 최신 main baseline 정정

## 상태: done (spec repo 커밋 · CLI · GitHub · 코드 · 하위 위임 없음)

## 변경
- `products/day/20-spec/spec-003-mobile-app.md`(4a5d4a47 위 미커밋 · 개정 ⑤ 안):
  - W1: 아이패드 Wireframe 에서 인박스 탭 줄을 지울 때 함께 지워진 왼쪽 레일 「예약 / 현황」의 「현황」 칸만 복원(본문 칸은 빈 줄 · 새 기능 없음). 레일 4메뉴(예약현황 · 시술현황 · 채팅 · 설정) 다시 온전.
  - 개정 ④ 머리 역사 문장 「… 호출 탭에서만」 끝에 「호출 탭은 이후 개정 ⑤ 로 없음」 꼬리 참고.
- profile `delivery-request-v6.json`(v6 유지 · 미적용):
  - `spec_baseline_revision` 3f57c1af… → **9692e1fb461bf8c4e52bf489e37ab8ff875f9918**(코디 fetch latest main) · pending 유지.
  - 현재 baseline 을 말하는 문장만 정정: scope_delta 끝 「baseline latest origin/main 9692e1fb… pending(3f57c1af..9692e1fb 사이 products/day/ 변경 없음 · main 에 SPEC-003 없음 · SPEC-001 draft)」 · review_surface[0] 첫 문장.
  - 과거 v5 contract/plan digest · 역사 원천 값 · targetDelta · AC · 권한 · 코드 scope 무변경.

## 검증
- `git diff 3f57c1af..9692e1fb -- products/day/` 비어 있음 · 9692e1fb 의 SPEC-001 `status: draft` · SPEC-003 파일 없음(직접 확인).
- `git diff --check` 통과 · ASCII 레일 4메뉴 대조.
- v6 JSON parse · jsonschema 0 errors · `DeliveryRequest.model_validate` OK(v6 · L3 · baseline 9692e1fb). 전체 lint 반복 안 함(브리프).
