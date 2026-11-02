# [mobile] 코드 리뷰 r3 WARN 수정 (W3-1 · W3-3)

리뷰 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/review-code-r3.md` 의 W3-1 · W3-3 을 리뷰 권장대로 고친다. 역할 · allowed_paths(`procedure/app/`) · 하지 말 것 · 완료 보고는 앞 브리프 그대로. subject 「mobile 수정 r4 완료: …」.

- **W3-1** 폰 전달 시트 높이 = 화면 전체 × 0.88 → 큰 아이폰 · 키보드 열림에서 머리([✕] · [전송])가 상태 표시줄 밑. **통역 드로어(D-65)와 같은 규칙**: 놓인 칸 높이 기준 · 상태 표시줄(위 안전 영역) 아래로 제한 · 키보드가 열리면 시트가 키보드 위로 줄어도 머리는 화면 안. **[+] 시트 · 다른 바텀 시트도 같은 꼴인지 grep 해서 전부** 같은 규칙으로(공용 도우미 하나). 시험: 작은 화면 · 큰 화면 · 키보드 열림에서 머리가 위 안전 영역 아래
- **W3-3** 보내는 중에는 시트를 닫지 못하게(끌어 내림 · 바깥 누름 · [✕] 막음 · [전송] 은 「보내는 중…」) — 또는 닫혀도 결과 토스트가 뜨게. 리뷰 권장 쪽으로 · 시험

검증: `/Users/kknaks/fvm/versions/3.44.8/bin/flutter analyze` · `flutter test` 1회 · `flutter build ios --simulator --debug` 1회
