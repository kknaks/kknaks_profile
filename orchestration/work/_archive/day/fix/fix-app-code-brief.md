# [mobile] fix 코드 — WP-APP-1(시술현황 카드 + 앱 후속 2) → WP-APP-2(채팅 · 설정)

너는 **day `mobile` 워커**다. 앞 판(같은 터미널 · TestFlight 준비)의 맥락이 있더라도 **아래 파일을 기준으로** 한다.

## 먼저 읽을 것

- 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/roles/day/mobile/role.md` (+ 같은 폴더 문서)
- 레포 규칙: `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix/AGENTS.md` 「앱」 · `app/README.md`
- **작업 계획(네 범위 · 파일 목록 · 시험 · 계약 표)**: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/wp-plan.md` — §1 · §2 「WP-APP-1」 「WP-APP-2」 · §3 계약 표 · §4 순서
- **계약의 SoT(스펙 — 미커밋 워크트리)**: `/Users/kknaks/orca/workspaces/mediness-mediness/fix-spec/products/day/20-spec/` — `spec-003-mobile-app.md`(개정 ⑧ · U-3 다섯째 상태 · 모두 완료 카드 [귀가 대기] · 확인 필요 표시 · 겹침 표 · U-12 `version` · U-4 `calls[].canRecall` · A-28 · A-33 · A-37 · A-41 ~ A-43) · `spec-004-internal-chat.md`(U-1 채팅 거절 · U-7 그룹 이름 · U-8 · C-A19 ~ C-A21) · `spec-005-notifications.md`(U-3 「채팅」 스위치 · N-A13)
- 사용자가 본 것 · 그림: `…/work/fix/e2e-feedback.md` 「버그 기록」 1 ~ 4 · 6 · 7 · `e2e-shots/`
- 스펙에 없는 것은 **발명하지 마라.** 계획과 스펙이 다르면 스펙이 맞다 — 다르다는 것을 보고에 적는다.

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix` (`kknaksss/fix`).
⚠ **backend 워커가 같은 워크트리의 `backend/` · `scripts/` · `deploy/` · 루트 `pyproject.toml` · `uv.lock` 에서 동시에 일한다.** 그쪽은 읽기만 · 건드리지 마라. `git stash` · `git checkout -- .` · `git clean` 금지.

## 할 것 — 차례로

### 1. WP-APP-1 시술현황 카드 + 앱 후속 2

`wp-plan.md` 「WP-APP-1」 그대로. 서버 변경 없음 — 서버 값 소비만.

- 「시술 모두 완료」 · 「마지막 종료 {HH:MM}」 · [귀가 대기] 는 **방 상세와 같은 글자 · 같은 계산 · 같은 조건**(`card.allDone` · `canHome` + 판 편집 권한 · 같은 잠금 키). 계산 · 글자를 복사해 둘로 만들지 말고 한 곳에서 쓴다.
- 확인 필요 표시: 카드 전체 빨간 테두리를 **없애고** 현재 상황 상자에 `Ms.red100` 바탕 + 왼쪽 `Ms.red` 띠. 붙는 조건(서버 `needs[]`)은 그대로. 겹침은 스펙 U-3 겹침 표(적용값) 그대로 — 7자리 전부.
- 업무 규칙을 앱이 다시 계산하지 않는다(서버 값만).

### 2. WP-APP-2 채팅 · 설정

`wp-plan.md` 「WP-APP-2」 · §3 계약 표 그대로. 서버(WP-BE-1)는 backend 워커가 같은 시간에 짓는다 — **계약 표 + 테스트 더블로** 짓는다. 서버가 끝나기를 기다리지 않는다.

- 채팅 403: 「서버에 연결 중...」 · 로딩을 멈추고 본문 안내(시술현황 권한 없음과 같은 글자 · [로그아웃]) · 스트림 재연결 멈춤 · 다시 보는 때 = 다시 로그인 · 앱 다시 열 때 · **앱이 앞으로 올 때 한 번** · 조작 중 403 = 본문 안내만(토스트 없음).
- 그룹 이름 바꾸기: 방 정보 「그룹 이름」 · [✓] · [✕] = 메시지 수정 모드의 것과 같은 아이콘 · 접근성 이름(「저장」 · 「수정 취소」) 재사용.
- 「채팅」 스위치 · 앱 안 배너 억제 · 설정 응답에 `chat` 이 없으면 켜짐.

## 범위 제약

- allowed_paths: `app/lib/` · `app/test/` · (필요할 때만) `app/README.md`.
- 금지: `app/ios/` 프로젝트 · `Info.plist` · 아이콘 · `pubspec.yaml` 의존성 추가(필요해 보이면 **멈추고 물어라**) · `backend/` 등 서버 쪽.
- **화면 문구를 지어 넣지 않는다.** 새 글자는 스펙에 적힌 것뿐이다(스펙이 출처 줄을 적어 두었다 — 그 기존 상수를 재사용한다). 새 문자열 상수를 만들었다면 보고에 전부 적고 스펙 줄을 단다.
- 통역(`app/lib/interpret/`)은 건드리지 않는다 — 통역은 서버만 짓는다.
- 서명 빌드 · 아카이브 · TestFlight 업로드 **금지**(이번 발주에는 승인이 없다). 사용자 포트(11040 등) · 로컬 스택 · 시뮬레이터 · 실기기 금지. 커밋 · push · PR 금지.

## 검증

- WP 마다: `cd app && fvm flutter analyze`(1회) · 네가 만들거나 고친 테스트 파일만 `fvm flutter test <파일들>`(1회).
- 마지막에 한 번: `fvm flutter test`(전체) · `fvm flutter build ios --no-codesign`(1회).
- 눈 확인용 그림: 기존 캡처 방식(`DAY_CAPTURE_DIR=<폴더> fvm flutter test test/capture/…` — `app/README.md`)으로 **바뀐 화면을 PNG 로** 낸다 — 목록 카드(모두 완료 + [귀가 대기] · 확인 필요 겹침 7자리) · 채팅 403 안내 · 방 정보 그룹 이름 편집 · 설정 「채팅」 스위치. 폴더 = `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/app-captures/`. 가짜 값만(실명 · 실제 고객 값 금지).

## 보고

리포트 2개(WP 마다 — 끝나는 대로 쓴다):
- `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/app-1-report.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/app-2-report.md`

각각: 변경 · 새 파일 목록 / 수용 항목 ↔ 시험 이름 표 / 새 화면 글자 표(글자 · 코드 자리 · 스펙 줄) / 계약 표(wp-plan §3)와 앱이 보내고 읽는 것이 같은지 필드 단위 / 돌린 명령과 수치 / 캡처 파일 목록 / 스펙과 달라진 곳 · 물을 것 / pending.

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 값과 다르면 preamble 이 맞다.

전부 끝나면 **두 명령 모두**:

```bash
orca orchestration send \
  --to term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --from term_8fae9ebc-816d-4674-970b-4107e45084ff \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "mobile 완료: <한 줄>" \
  --body "WP 별 변경 파일 수 / 시험 수치 / 캡처 / 스펙과 다른 곳 / pending"

orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 \
  --text "[worker_done] mobile 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

막히면 30분 넘게 혼자 헤매지 말고: `orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[질문] mobile: <질문>" --enter`
