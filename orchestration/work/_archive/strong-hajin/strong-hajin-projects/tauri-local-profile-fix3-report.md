---
title: Tauri local profile DatePicker footer alignment fix report
status: complete
updated: 2026-09-23
---

# 변경

`frontend/src/styles/components.css`의 `.date-picker-foot`에 `padding-inline: 12px`를 추가했다. DatePicker 팝오버의 「지우기」와 「오늘」 버튼이 날짜 격자의 좌우 기준선과 맞도록 내부 가로 여백을 사용한다.

운영 Tauri 설정과 capability는 변경하지 않았다.

# 검증

- `npx vitest run src/ds/DatePicker.test.tsx --reporter=dot`: 14 passed
- `npx tsc --noEmit`: 통과
- `git diff --check`: 통과
