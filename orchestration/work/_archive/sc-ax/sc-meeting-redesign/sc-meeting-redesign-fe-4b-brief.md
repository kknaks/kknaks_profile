# [frontend] 바퀴 4b — 두 그리드의 선 굵기를 화면에서 맞춘다

너는 **sc-ax `frontend` 워커**다. 바퀴 4 커밋 `2f6e9ea` 위에서 이어간다.
작업 워크트리: `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting-redesign`

## 1. 판단 — 네가 물은 것에 답한다

**맞춰라.** H-6 의 「굵기 규칙 유지」는 **화면에 보이는 굵기**를 정한 것이지 `strokeWidth` 속성의
숫자를 고정하라는 뜻이 아니었다. 규칙의 값(16·20 → 1.5, 14 이하 → 1.3)은 **viewBox 16 기준**으로
쓰인 것이고, viewBox 24 가 섞인 지금은 **숫자를 그대로 두는 쪽이 오히려 규칙을 어긴다.**

- 24그리드 글리프: viewBox 24, 16px 렌더 → `1.5 × 16/24` = **1.0px**
- 16그리드 글리프: viewBox 16, 16px 렌더 → **1.5px**

정본은 새 DS 다. 그러니 **16그리드 8종을 DS 쪽(1.0px)에 맞춘다** — 네가 말한 `16/24` 곱셈이 그것이다.

## 2. 할 일

`src/Icon.tsx` 한 곳. 16그리드 글리프일 때만 `strokeWidth` 에 `16/24` 를 곱한다.

- **24그리드 글리프의 숫자는 건드리지 마라.** DS 가 정한 값 그대로다
- 곱하는 자리에 **왜 곱하는지 한 줄 주석** — viewBox 가 달라 같은 숫자가 다른 굵기로 보인다는 것,
  그리고 **G-03 이 닫혀 8종이 24그리드로 오면 이 분기가 통째로 사라진다**는 것
- `size` 분기(14 이하 1.3)도 같은 방식으로 스케일되어야 한다 — 하드코딩하지 말고 계산으로

## 3. allowed_paths

- `frontend/`

**`backend/` 는 한 줄도 안 건드린다.**

## 4. 검증

```
cd frontend && npx tsc --noEmit     → 0 에러
cd frontend && npx vitest run <네가 만진 테스트 파일만>
```

이 바퀴는 **전체 스위트를 돌리지 마라.** 한 파일 한 줄짜리라 전체를 돌 이유가 없다.
`Icon.test.tsx` 가 `strokeWidth` 를 단언하면 그 값만 고쳐라.

## 5. 보고

- 바꾼 줄과 계산식
- 네가 지목한 세 곳(TodayPage 메트릭의 `circle` · ActionTaskCard 자료 목록의 `folder` ·
  WorkModals 체크리스트의 `arrow-up`/`down`)이 **이제 옆 글리프와 같은 굵기로 보이는지**
- `tsc` · vitest 결과
