
# [mobile] 직원 앱 차트 = 웹과 같은 기능 (U-23) — Delivery #282

너는 **day `mobile` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/roles/day/mobile/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-app-re1`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

**같은 코드 워크트리를 다른 워커와 나눠 쓴다** — backend 는 `backend/` · `deploy/` 만, mobile 은 `app/` 만. 상대 영역은 건드리지 마라. git stash · checkout · reset 금지.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/delivery-1-report.md` §「BE ↔ APP 계약 전문」 C0 ~ C3 ← **두 워커가 같은 계약을 본다. 이대로 만든다.** 이름 제안과 달라져야 하면 멈추고 코디에게 먼저 알린다(§9 (2) 질문)
- Delivery Issue: MediSolveAIDev/CENTURION_DAY#281(backend) · #282(mobile) — `gh issue view <N> -R MediSolveAIDev/CENTURION_DAY` (읽기만 · 댓글 · 라벨 · 승인 건드리지 마라)
- SPEC(원천 · 읽기만): `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-re1-spec/products/day/20-spec/spec-002-procedure-board.md`(개정 ㉚ · §3 차트 · 사진 JSON 짝 · 규칙 23 · 31 · 39) · `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-re1-spec/products/day/20-spec/spec-003-mobile-app.md`(개정 ㉑ · U-23 · A-51 ~ A-60 · OQ 기본값)
- 결정: `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/_RESUME.md` §2(D1 ~ D15 · D6′)
- 조사: `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/research-1-report.md`(근거 파일:줄 @`55e60aa4`)

**기대는 개념**: 해당 없음

## 2. 배경 / 무엇을 바꾸나

직원 앱 시술현황에서 시술 줄을 누르면 뜨는 차트(`app/lib/ui/chart_sheet.dart`)가 지금 읽기 전용(스냅샷 노트 · API 0건)이고, 탭 아래 까만 줄 · 탭바 겹침이 있다(사용자 스크린샷 `/Users/kknaks/.config/day/reference/app-chart-2026-11-25.png` — 레포에 복사 금지). SPEC-003 개정 ㉑ U-23 대로 웹과 같은 기능으로 올린다. **시안 없음** — 앱 DS 컴포넌트(`app/lib/ui/theme.dart` · 기존 위젯)만 쓰고 칸 배치는 웹 차트를 따른다. 화면 글자는 SPEC 에 있는 것만(없으면 비움 — 지어 넣지 마라).

backend 워커가 같은 시각에 C2 · C3 경로를 만든다 — 너는 계약대로 클라이언트를 만들고 **테스트 더블**로 검증한다(실서버 호출 없음).

## 3. 계약

위 §1 의 C0 ~ C3 그대로.

## 4. 먼저 읽을 핵심 파일

코드 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-app-re1`(`kknaksss/day-app-re1` · base origin/dev `55e60aa4`):
- `app/lib/ui/chart_sheet.dart`(지금 차트) · `app/lib/ui/room_screen.dart`(:584-587 여는 곳 · :753 확인 시트) · `app/lib/ui/doctor_picker.dart`(:85 · :88 · :93 — 담당자 고르기 재사용 · 팝오버) · `app/lib/ui/shell.dart` · `app/lib/ui/theme.dart`(까만 줄 = TabBar 구분선 · outlineVariant)
- `app/lib/chat/chat_kit.dart`(:55-58 세션 Navigator 로 띄우는 방식) · `app/lib/chat/screens/chat_attach_sheet.dart`(카메라 · 앨범 · 이미지 고르기 재사용)
- `app/lib/data/` · `app/lib/model/board.dart` · `app/lib/state/board_controller.dart`(API 클라이언트 · SSE `board`)
- `app/lib/core/copy.dart`(:22-23 `chart_conflict` 「웹 전용」 — 이제 앱도 씀) · `app/test/core/board_messages_contract_test.dart`(:19)
- `app/ios/Runner/Info.plist`(:52-57 권한 문구 → D15 글자 그대로)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `app/ 중 브리프가 지정한 곳`

## 6. 구현 단계

1. 데이터: C1 차트 GET · C2 탭 저장 · C3 ① ~ ⑤ 클라이언트 · 모델(계약 칸 이름 그대로)
2. 차트 화면(U-23): 탭 셋(웹 글자 D13) · 탭별 [저장] · 「최근 저장」(병원 시간대 — SPEC) · 담당자 고르기(doctor_picker 재사용) · 충돌 409 → 서버가 준 이어 붙인 글 반영 · 거절 글자 · 보기 권한이면 읽기만(/me 권한)
3. 닫기(D6′ · D12): 미저장 없음 = ✕ · 바깥 누름(아이패드) · 끌어 내림 · 뒤로 가기 다 닫힘 / 미저장 있음 = ✕ · Android 뒤로 → 확인 창 · 바깥 누름 · 끌어 내림 = 안 닫힘 · iOS 가장자리 밀기 = 막힘
4. 사진 탭: 목록(시술 전 · 시술 후 묶음) · 올리기(여러 장 · 카메라 / 앨범 = OQ-A73 기본값) · 삭제 확인 · 크게 보기(파일 GET · Bearer 머리) · 「KOS 미반영」 [다시 시도] · 탭 열린 동안 10초 `tick=1` · 413 / rejected 처리
5. 자리: 폰 = 전체 화면 · 아이패드 = 가운데 창 · 세션(루트) Navigator(D4 · D14 — 차트 · 원장 고르기 · 확인 시트 / 팝오버 · 창 · 원장 고르기 투명 덮개 그대로) · 까만 줄 = 테마에서(D9)
6. Info.plist 권한 문구 = `_RESUME.md` D15 글자 그대로(한 글자도 바꾸지 마라)
7. 테스트: A-51 ~ A-60 · A-17 · A-38 위젯 / 단위 테스트(테스트 더블) · 계약 시험 갱신 · 테마 · 닫기 표 전부
8. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/app-1-report.md`(변경 파일 · 화면 흐름 · 테스트 수치 · 계약에서 애매했던 곳 · 코디가 시뮬레이터에서 볼 순서 · 사람 눈에 이상해 보일 자리)

## 7. 범위 제약 — 하지 말 것

- 실서버 · 로컬 스택 호출 · 시뮬레이터 / 기기 실행(통합 실물은 코디 몫) · 서명 · TestFlight · 버전 올리기
- 새 화면 글자 지어 넣기 · 새 패키지 추가(꼭 필요하면 멈추고 질문)
- `backend/` · `deploy/` 건드리기 · 커밋 · push · PR · Issue 라벨 / 댓글

## 8. 검증

```
cd app && flutter analyze · flutter test · flutter build ios --no-codesign — 각 1회(통합은 마지막). 사용자 포트·프로세스·기기를 건드리지 않는다. 서명·TestFlight 는 사용자 몫 — 실행 못 한 검증은 사유와 함께 pending
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **(코디 추가 · 2026-11-25)** 이번 발주는 orca Run(`worker-start`)으로 나간다. **dispatch preamble 에 적힌 `worker_done` 명령(Task · Dispatch ID · `--outcome` · `--report-path`)이 아래 (1)보다 우선**이다. (2) 직접 주입은 그대로 해도 된다.

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_414d6113-407d-486b-ab54-10a4a6b455cb --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "mobile 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_414d6113-407d-486b-ab54-10a4a6b455cb \
  --text "[worker_done] mobile 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_414d6113-407d-486b-ab54-10a4a6b455cb --text "[질문] mobile: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
