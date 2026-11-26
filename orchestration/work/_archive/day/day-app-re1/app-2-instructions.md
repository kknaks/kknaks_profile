# [mobile] app-2 — WORK-002 앱 — Delivery CENTURION_DAY#288

너는 day `mobile` 워커다. 역할 문서 경로 · 워크트리 공유 규칙 · §8 검증 · §9 완료 보고는 같은 폴더 `day-app-re1-app-brief.md`(WORK-001 판)를 따른다(먼저 읽어라). **범위 · allowed_paths · 금지는 아래가 이긴다.**

작업 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-app-re1`(HEAD `96036397` = WORK-001 코드 · 그 위에 쌓는다). backend 워커가 같은 워크트리의 `backend/` 를 동시에 고친다 — 너는 `app/` 만. git stash · checkout · reset · 커밋 금지.

## 1. SSOT

- Delivery Issue **CENTURION_DAY#288**(`gh issue view 288 -R MediSolveAIDev/CENTURION_DAY`) — WP 범위 · 계약(압축판)
- `delivery-2-report.md` §4 · **§5 B 상세판 계약 전문**(같은 폴더) — backend 와 같은 글. 서버는 아직 없다 — 계약대로 짓고 테스트 더블로 시험
- SPEC(`/Users/kknaks/orca/workspaces/mediness-mediness/day-app-re1-spec` HEAD `a018f4fa` · `products/day/20-spec/`): **spec-003 개정 ㉒**(U-24 ~ U-30 · A-61 ~ A-77 · 네이티브 채널 · OQ) · spec-006 ⑭ · spec-007(웹 상세 칸 · 순서 · 글자 = 앱이 닮을 것) · spec-005(푸시 갈래)
- 결정 SoT `_RESUME.md` §2 WORK-002 행 전부(읽기 전용 · 웹과 닮게 · 아이패드 + 갤럭시) · 원천 cc `/Users/kknaks/git/toy_pr2/cc-prototype` origin/main(`git show` 만 — `procedure/app/lib/scan/mrz.dart` · `scan_channel.dart` · `screens/{scan_screen,qr_show_screen,reservation_detail_screen,launchers,settings_screen}.dart` · `ios/Runner/TextScanner.swift`) · research-2/3 리포트

## 2. allowed_paths

- `app/` 전부(`lib/` · `test/` · `ios/Runner/` · `android/app/`(Kotlin 채널 · Manifest `CAMERA` · gradle 의존성 CameraX · ML Kit 번들 Latin) · `pubspec.yaml`(새 Flutter 패키지는 꼭 필요할 때만 · 리포트에 이유 — QR 그리기 · 화면 꺼짐 막기는 네이티브 채널이 cc 꼴))

## 3. 구현

#288 범위 전부 — 메뉴 4(예약현황 다시 넣음) · 예약현황(폰 = 카드 목록 · 태블릿 = 웹 같은 시간 × 열 표 · 칸 · 순서 · 글자 · 단계 색 = 웹) · 상세(웹 모달 상자 순서 · **읽기 전용** · 버튼 = [문진 QR] · [여권 스캔] · [태블릿에 보내기]만) · 문진 QR 전체 화면(cc 꼴) · 여권 스캔 채널 `day/scan`(iOS Vision = cc `TextScanner.swift` · **Android CameraX + ML Kit 번들 = 새로** · 같은 채널 모양) · `mrz.dart` 옮김 · 손 입력 · 확인 화면(여권 값은 확인 화면 열 때만 읽음) · 「태블릿에 보내기」 기기 고르기 · 진행 · 태블릿 받기(알림 스트림 `display` · 푸시 갈래 Dart + Kotlin · 놓친 것 메우기) · 설정 「이 기기 이름」 · iOS 카메라 문구 = 지금 D15 그대로(OQ-A79 열림 — 바꾸지 마라).

- 화면 글자는 SPEC · cc 원천 · 웹 템플릿에 있는 것만 — 없으면 비우고 리포트에
- 테스트: A-61 ~ A-77 앱 몫 위젯 / 단위(테스트 더블) · MRZ 파서 · 푸시 갈래 · 폰 / 태블릿 모양

## 4. 금지

실서버 · 로컬 스택 · 시뮬레이터 / 에뮬레이터 / 기기 실행(통합 A4 = 코디 몫) · 서명 · TestFlight · 버전 올리기 · `backend/` · `deploy/` · 커밋 · push · PR · Issue 라벨 / 댓글.

## 5. 검증 · 보고

`cd app && fvm flutter analyze · fvm flutter test · fvm flutter build ios --no-codesign · fvm flutter build apk --debug` 각 1회(통합은 마지막). `app-2-report.md`(같은 폴더) — 변경 파일 · 화면 흐름 · 네이티브 채널 표(iOS / Android) · 테스트 수치 · 계약에서 애매했던 곳 · 코디가 시뮬레이터에서 볼 순서 · 사람 눈에 이상해 보일 자리. 완료 보고 = dispatch preamble 의 `worker_done` + 브리프 §9 (2) 직접 주입(subject 「mobile 완료: app-2」).
