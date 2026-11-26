# [planner] fix-1 — review-doc-1 WARN 7 + 사용자 확인 5 반영

너는 day `planner` 워커다. 역할 · 범위 · allowed_paths · 검증 · 완료 보고는 같은 폴더 `day-app-re1-spec-brief.md` 를 그대로 따른다(먼저 그 브리프 전체를 읽어라). 작업 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-re1-spec` — 앞 판(planner-1)의 미커밋 변경 위에 이어서 고친다.

읽을 것:
- `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/review-doc-1-report.md` — WARN W1 ~ W7 · 「사용자 확인 필요」 1 ~ 5
- `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/_RESUME.md` §2 — 결정(오늘 추가된 D6′ · D12 ~ D15 포함)

## 할 것

1. **WARN W1 ~ W7 전부** 리포트의 고칠 방향대로 고친다(W1 은 아래 D12 로 닫는다).
2. **사용자 결정(2026-11-25) 반영** — OQ 를 닫고 본문 · 인수 조건에 넣는다:
   - **D6′**(D6 고침): 미저장이 **없으면** ✕ · 바깥 누름(아이패드) · 끌어 내림 · 뒤로 가기 모두 그냥 닫힌다(웹 U-14 와 같게). 미저장이 **있으면** ✕ · 뒤로 가기(안드로이드 버튼) → 확인 창, 바깥 누름 · 끌어 내림 → 닫히지 않음. OQ-A71 닫기
   - **D12**: 미저장일 때 iOS 가장자리 밀기 = 막힘(아무 일 없음 · Flutter 기본) — 확인 창 없음. ✕ 를 누르면 확인 창. W1 닫기
   - **D13**: 탭 글자 = 웹 글자 「간호관리차트」 · 「의사차트」 · 「시술전후사진」. OQ-A65 닫기
   - **D14**: 아이패드 팝오버 · 가운데 창도 세션(루트) Navigator 로 옮긴다. 원장 고르기 팝오버의 투명 덮개(F1 · 판이 보임)는 그대로. OQ-A76 닫기
   - **D15**: iOS 권한 문구(사용자가 넣으라고 지시 — 이 글자 그대로 계약에 넣는다). OQ-A64 닫기 · A-17 권한 조항이 있으면 맞춘다:
     - `NSCameraUsageDescription`: 「채팅으로 보낼 사진과 차트에 올릴 시술 전후 사진을 찍기 위해 카메라를 사용합니다. 찍은 사진은 사진첩에 저장하지 않습니다.」
     - `NSPhotoLibraryUsageDescription`: 「채팅으로 보낼 사진 · 동영상과 차트에 올릴 시술 전후 사진을 고르고 최근 사진을 보여 주기 위해 사진 보관함을 사용합니다. 고른 것은 기기에 따로 저장하지 않습니다.」
     - 안드로이드는 권한 설명 문구 칸이 없으면 「해당 없음」으로 적는다(근거와 함께)
3. 개정 번호는 새로 따지 않는다 — 같은 개정 ㉑ · ㉚ 안에서 고친다. `log.md` 한 줄 · `10-decision.md` 반영.
4. 브리프 §8 검증(lint) → 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/planner-fix-1-report.md`(W1 ~ W7 · D6′ · D12 ~ D15 각각 → 고친 파일:줄).

하지 말 것: 브리프 §7 그대로. 위 권한 문구 외 새 화면 글자를 지어 넣지 않는다. 커밋 · push 금지.

완료 보고: dispatch preamble 의 `worker_done`(`--report-path` 위 리포트) + 브리프 §9 (2) 직접 주입.
