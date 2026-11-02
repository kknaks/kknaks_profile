---
title: Tauri local profile DatePicker weekday alignment fix report
status: complete
updated: 2026-09-23
---

# 변경

`frontend/src/styles/screens-b.css`의 `.calendar-weekdays span`에 `text-align: center`를 추가했다. DatePicker의 요일 머리글은 7열 grid의 span이고 날짜 버튼은 `justify-self: center`인데, 요일 span에 중앙 정렬이 없어 「일」 같은 한 글자가 열 왼쪽에 붙었다. 이제 요일과 날짜(예: 30)가 같은 열 중앙에 정렬된다.

이 셀렉터는 DatePicker와 기존 업무 캘린더가 공유하는 범위라 두 화면의 요일 머리글도 같은 정렬 규칙을 사용한다. 운영 셸 설정과 Tauri capability는 변경하지 않았다.

# 검증

- `npx vitest run src/ds/DatePicker.test.tsx --reporter=dot`: 14 passed
- `npx tsc --noEmit`: 통과
- `git diff --check`: 통과
- CSS 정적 확인: `.calendar-weekdays span`에 `text-align: center` 존재

# 한계

이번 변경은 정렬 속성 한 줄과 DatePicker 회귀 테스트로 검증했다. 실제 Tauri 창의 픽셀 확인은 사용자가 `make tauri-local`로 열어 DatePicker를 직접 확인하는 단계에서 수행한다.
