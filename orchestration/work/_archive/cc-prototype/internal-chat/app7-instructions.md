# [mobile] 직원 앱 내부 채팅 — WORK-011 WP-APP7 (모아보기 · 초대 · 들어온 뒤 대화만)

역할 · allowed_paths(`procedure/app/`) · 하지 말 것(커밋 · 시뮬레이터 · 기기 · 서명 금지) · 검증 · 완료 보고(§9 두 명령)는 **`/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/internal-chat-app-brief.md` 그대로**다. subject 「mobile APP7 완료: …」.

작업 워크트리: `/Users/kknaks/orca/workspaces/cc-prototype/internal-chat` 브랜치 `kknaksss/internal-chat-invite`(HEAD 3ed1089 — F10 정렬 커밋 포함 · 커밋 금지). ⚠ backend 가 `procedure/back` 에서 병렬 — 건드리지 마라. 가짜 응답으로 짓는다.

## SSOT (이기는 순)
1. 코디 처분(있으면) `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/r5-dispositions.md`
2. `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/para/projects/summer-star/cc-prototype/20-spec/spec-007-internal-chat.md` **0.5.0** `(r5)` — §10.8 · §10.10 · §10.16 · §10.17 · §13.2 r5 · WORK-011 **WP-APP7**
3. DEC-009 D-67 ~ D-69 · OQ-962 ~ 969 기본값
4. 사용자 피드백 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/sim-feedback.md` F11 · F13 · F14
5. 공용 시트 `showAppSheet` · 정렬 규칙(F10 — 이름 `Expanded` · 동그라미 오른쪽 끝 · 머리 좌우 같은 폭)을 새 화면에도 쓴다

## 검증
`/Users/kknaks/fvm/versions/3.44.8/bin/flutter analyze` · `flutter test` 1회 · `flutter build ios --simulator --debug` 1회
