# pencil 지시 — 앱 모드 중단, headless 로 전환 (2026-11-12 코디)

앱 화면에 `RuntimeError: Out of bounds memory access (evaluating 'e.ae.fe(e.Rd)') ×6 · ('r(...d)') ×5` 가 떴다(사용자 스크린샷, 「section/SelectAll」 근처). 직렬로 돌려도 세 번째 — **앱 모드 eval 은 더 쓰지 않는다.**

1. 지금 돌던 eval 이 있으면 끝나길 기다리고, **앱에 더는 eval · save 를 보내지 마라.** 앱 상태는 버린다(저장 금지).
2. **headless 로 같은 스크립트를 돌린다**: `bun ~/.bun/bin/openpencil eval <파일> -w --stdin < 스크립트` (파일에 직접 쓰기). API 가 앱 모드와 다른 곳이 있으면(`figma.notify` 등) 스크립트를 조건 분기로 맞춘다. 결과 파일은 같은 경로 `medikit.fig`. 시작 전에 디스크 `medikit.fig` 를 `medikit.before-headless.fig` 로 복사해 둔다.
3. 순서 그대로: _vars.js → import-medikit.js → run-all.sh(1차 → 2차). 각 단계 뒤 `info <파일>` 로 노드 수 확인.
4. headless 에서도 같은 메모리 오류가 나면 **어느 스크립트 · 어느 호출에서 나는지 최소 재현**(예: SelectAll 의 특정 노드 · createNodeFromSvg · combineAsVariants)을 리포트에 적고 `[질문]` 으로 알린다.
5. 끝나면 코디에게 알린다 — 코디가 사용자에게 앱에서 파일을 다시 열게 한다(앱이 옛 상태를 덮어쓰지 않게 사용자가 먼저 앱 탭을 저장 없이 닫는다).
6. 린트도 headless: `lint <파일> --json`.
