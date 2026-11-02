# [mobile] 직원 앱 내부 채팅 — WORK-011 WP-APP4 → WP-APP5 (입력창 · [+] 시트 · 여러 개 · 변환 · 동영상 → 5메뉴 · 선택 복사 · 공유 · 수정 · 링크)

역할 · allowed_paths(`procedure/app/`) · 하지 말 것(커밋 · 시뮬레이터 · 기기 · 서명 금지) · 검증 · 완료 보고(§9 두 명령)는 **앞 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/internal-chat-app-brief.md` 그대로**다. 먼저 그 브리프 · 역할 문서를 읽어라. subject 「mobile APP4 · APP5 완료: …」.

작업 워크트리: `/Users/kknaks/orca/workspaces/cc-prototype/internal-chat` — 1판이 커밋 `0f0d969` 로 있다. 그 위에 이어서 짓는다(커밋 금지).
⚠ backend 워커가 같은 워크트리 `procedure/back/` 에서 병렬 작업 중 — 건드리지 마라. 앱은 SPEC 계약 모양의 가짜 응답으로 짓는다.

## SSOT (이기는 순)
1. **`/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/r3-dispositions.md`** (코디 처분 — SPEC 보다 이김 · 동영상 90MB · 링크 ASCII · 공유 흘려 쓰기 · 카메라 칸 · 비활성 1:1 수정 숨김)
2. `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/para/projects/summer-star/cc-prototype/20-spec/spec-007-internal-chat.md` **0.3.0** (`(r3)` 줄 · §9.3 패키지 권장 · §10 화면) · `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/para/projects/summer-star/cc-prototype/30-work/work-011-internal-chat.md` **WP-APP4 · WP-APP5 행**
3. `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/para/projects/summer-star/cc-prototype/10-decision/decision-009-internal-chat.md` D-45 ~ D-59
4. 사용자 피드백 원문 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/sim-feedback.md` — **[+] 시트 = 카톡 꼴**(위 「최근 사진」 가로 줄 · 맨 앞 카메라 칸 · 동그라미 여러 개 · 오른쪽 위 [전송] · 아래 메뉴 「사진」 하나) · **입력창 = 넓은 입력칸 + 아래 줄 [+] … [전송]**(아이콘 없음)
5. 리뷰 `review-doc-r3.md` 「조용히 통과하는 자리」 · 「사용자가 실물에서 만날 자리」

## 주의
- `video_compress` 는 오래된 판 — 시뮬레이터 빌드가 깨지거나 API 가 안 맞으면 iOS 네이티브(`AVAssetExportSession`) 채널로 간다(SPEC §9.3). 어느 쪽으로 갔는지 보고
- 권한 문구(사진 보관함 읽기 · 카메라)는 `Info.plist` 에 · 저장(쓰기) 문구는 넣지 않는다(D9-24)

## 검증
APP4 → `flutter analyze && flutter test` 1회 · APP5 → 1회 · 마지막 `flutter build ios --simulator --debug` 1회. (flutter = `/Users/kknaks/fvm/versions/3.44.8/bin/flutter`) · §13.2 r3 줄 → 시험 이름 표
