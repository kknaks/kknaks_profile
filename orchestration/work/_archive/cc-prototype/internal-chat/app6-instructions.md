# [mobile] 직원 앱 내부 채팅 — WORK-011 WP-APP6 (전달 시트 · 시스템 공유 걷어냄 · 통역 드로어)

역할 · allowed_paths(`procedure/app/`) · 하지 말 것(커밋 · 시뮬레이터 · 기기 · 서명 금지) · 검증 · 완료 보고(§9 두 명령)는 **앞 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/internal-chat-app-brief.md` 그대로**다. 먼저 그 브리프 · 역할 문서를 읽어라. subject 「mobile APP6 완료: …」.

작업 워크트리: `/Users/kknaks/orca/workspaces/cc-prototype/internal-chat` — 브랜치 `kknaksss/internal-chat-forward`(운영 main `a6c4123` 에서 새로 땀 · 커밋 금지).
⚠ backend 워커가 같은 워크트리 `procedure/back/` 에서 병렬 작업 중 — 건드리지 마라. 앱은 SPEC 계약 모양의 가짜 응답으로 짓는다.

## SSOT (이기는 순)
1. 코디 처분(있으면) `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/r4-dispositions.md`
2. `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/para/projects/summer-star/cc-prototype/20-spec/spec-007-internal-chat.md` **0.4.0** `(r4)` 줄 — §10.14 전달 시트 · 5메뉴 [공유] · §12.3 · §13.2 · WORK-011 **WP-APP6** 행
3. `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/para/projects/summer-star/cc-prototype/10-decision/decision-009-internal-chat.md` D-62 ~ D-65
4. 사용자 피드백 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/sim-feedback.md` **F7**(카톡 공유 시트 꼴: 맨 위 검색 「이름 · 채팅방 검색(초성 가능)」 · 칩 · 목록 + 동그라미 · [전송]) · **F9**(통역 드로어가 상태 표시줄 밑으로 올라가 손잡이가 안 보여 못 내림 — `lib/widgets/interpret_drawer.dart:192-193` 높이 = 화면 전체 × 0.92 인데 탭바 위 본문 안에 그려짐)
5. 리뷰 `review-doc-r4.md`

## 주의
- `share_plus` · 시스템 공유 코드 · 임시 파일 흘려 받기를 걷어낸다(pubspec 에서도 — 다른 데서 안 쓰면)
- 통역 드로어(D-65): 폰 · 아이패드 둘 다 · 손잡이 끌어 내려 닫기 · 시험(작은 화면 높이에서 손잡이가 화면 안)

## 검증
`/Users/kknaks/fvm/versions/3.44.8/bin/flutter analyze` · `flutter test` 1회 · `flutter build ios --simulator --debug` 1회
