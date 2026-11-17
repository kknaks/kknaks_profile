# spec-4 리포트 — 마감 전 스펙 맞추기

워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/kos-signin-limit-spec` (미커밋 · 커밋 안 함)

## 변경
- `products/day/20-spec/spec-002-procedure-board.md` — **개정 ㉓** 머리 문단(㉒ 위) 추가.
  1. 차트 여는 곳 = 시술명 영역 전체(1줄 이름 + 2줄 상태 줄 · 빈 자리 포함 · 체크박스 · 줄 버튼 · ⋮ · 「원장 변경」 원장 이름 버튼 제외 · 판 줄 · 「시술 완료」 탭 줄 모두). 반영: 화면 구성 E30 행 · 차트 행 · U-3 · U-12 · U-13 · U-14 · 규칙 23 · 규칙 37 메모. 옛 「시술 이름 글자만」(㉒ E6)은 취소선 + 사유.
  2. 차트 영역 호버 · 키보드 포커스 = 배경 · 테두리 없음 · 툴팁 「차트 작성」만 — U-3 · 차트 행 · U-14 · 규칙 23.
  3. 정렬 탭 「시술대기 순」 · 「방별 순」 — 1차 범위 · E07 · U-2 정렬 탭 · §3 API 「정렬 탭」 · 규칙 36 · OQ-59 ⓐ 취소선 + 「닫은 것」 행 추가(ⓑ ~ ⓕ 는 열림 그대로).
  - §4 「개정 ㉓ — 앞 판과 달라진 곳」 표 신설 · ㉑ · ㉒ 표의 해당 행에 → ㉓ 표시.
- `spec-001-login-session.md` — 개정 ⑨ 배포 메모 한 줄(`KOS_CLIENT_TAG` dev `dev` · prod `prod` · 로컬 `local` · OQ-K15 가리킴).
- `20-spec.md` — SPEC-002 줄 정렬 탭 이름 · 「방별 순」 표기.
- `log.md` — spec-change 1행(DAY-SPEC-002, DAY-SPEC-001).

## 검증
- `python3 scripts/lint-pipeline.py --strict` → 0 error · products/day 경고 0 (263 warning 은 타 제품 기존 doc_no 등 — 무관).
