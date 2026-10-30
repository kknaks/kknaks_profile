# [mobile] 사용자 피드백 F10 — 전달 시트 정렬

`/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/sim-feedback.md` F10 (사용자 「뭔가 정렬이 안 맞는데?」 · 전달 시트 스샷: 동그라미가 줄마다 다른 자리 · 오른쪽 끝이 아님 · 「공유」 제목이 가운데가 아님). 역할 · allowed_paths(`procedure/app/`) · 하지 말 것 · 완료 보고는 앞 브리프 그대로. subject 「mobile 수정 r5 완료: …」. 브랜치 `kknaksss/internal-chat-forward`(코드 PR #18 머지됨 · 그 위 미커밋으로).

## 원인 (코디 확인)
- `lib/screens/chat_forward_sheet.dart:305-307` 줄 = `Flexible(이름)` + 배지 + `Spacer()` — Flexible(느슨) 과 Spacer 가 남는 폭을 반씩 나눠 동그라미 위치가 이름 길이에 따라 달라진다
- 머리 `:203-215`: 왼쪽 IconButton(48) ↔ 오른쪽 `SizedBox(width: 104)` → 제목이 가운데에서 비킨다 · 머리 오른쪽 여백(12) ≠ 목록 좌우 여백

## 고칠 것
1. 줄: 이름 + 배지를 `Expanded`(안쪽 `Row(mainAxisSize: min)` · 이름만 줄임표) · 동그라미는 늘 오른쪽 끝 같은 x
2. 머리: 좌우 같은 폭(가운데 제목이 시트 가운데) · [✕] · [전송] · 검색칸 · 칩 · 목록의 좌우 바깥 여백을 하나의 값으로
3. **같은 꼴을 채팅 화면 전체에서 grep**(`Flexible(` 다음 `Spacer` · 좌우 폭이 다른 머리 Row) — 새 대화 · 참여자 추가 · 방 목록 · 방 정보 · [+] 시트 머리 · 선택 복사 머리 등. 찾은 곳 목록과 고친 곳을 보고에
4. 시험: 이름 길이가 다른 두 줄의 동그라미 오른쪽 x 같음 · 머리 제목 가운데 x = 시트 가운데 x

검증: `/Users/kknaks/fvm/versions/3.44.8/bin/flutter analyze` · `flutter test` 1회 · `flutter build ios --simulator --debug` 1회
