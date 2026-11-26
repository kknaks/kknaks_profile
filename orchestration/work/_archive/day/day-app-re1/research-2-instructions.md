# [researcher] research-2 — WORK-002 여권 스캐너 · 문진 QR 현황 조사(read-only)

너는 day `researcher` 워커다. 역할 · 규칙 · 완료 보고 형식은 같은 폴더 `day-app-re1-research-brief.md` 를 따른다(먼저 읽어라 — §1 의 git 읽기 규칙 · §7 금지 · §9 보고). 이번 대상만 아래로 바꾼다.

## 배경

WORK-001(앱 차트)은 사용자 시뮬레이터 E2E 확인까지 끝났다. 다음 = **직원 앱에 여권 스캐너 · 문진 QR**. 원천 기능은 cc-prototype(`/Users/kknaks/git/toy_pr2/cc-prototype` · origin/main · read-only — `git show origin/main:<path>`)의 Flutter 직원 앱 · 백엔드 · 고객 웹에 있다. 처음 사용자 말은 「예약 탭을 우리 스타일로 만들고 주요 기능 = 여권 스캐너 · 문진 QR」이다 — 예약 탭을 새로 만들지, 기존 화면에 넣을지는 아직 안 정했다(조사가 근거를 낸다).

DAY 코드 기준 = CENTURION_DAY `96036397`(코드 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-app-re1` — 읽기만 · 빌드 · 실행 금지) · 스펙 = mediness `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-re1-spec`(`products/day/` 읽기만).

## 조사

1. **cc-prototype 여권 스캐너 전수**: `procedure/app/lib/scan/mrz.dart` · `scan_channel.dart` · `screens/scan_screen.dart` · iOS `ios/Runner/TextScanner.swift` · `AppDelegate.swift`(채널 등록) · Android 쪽(있나 없나) · 백 `procedure/back/app/service/passport_scan.py` + 부르는 API · KOS 로 무엇을 쓰나(고객 여권 필드 · 여권 사진 분류 업로드 등) · 어디서 진입하나(예약 상세 · 접수 등) · 쓰는 패키지 · 권한(카메라 문구). 흐름을 단계별로(찍기 → MRZ 읽기 → 확인 화면 → 저장 → KOS)
2. **cc-prototype 문진 QR 전수**: `screens/qr_show_screen.dart` · 백 `api/public_questionnaire.py` · `service/questionnaire.py` · 고객 웹 `procedure/front/components/q/QuestionnairePage.tsx` · QR 에 무엇이 실리나(토큰 · 만료 · 대상 방문/고객) · 고객이 쓴 답이 어디로 가나(DB · KOS 문진 / 상담) · 직원이 결과를 어디서 보나 · 공개 경로 보안(토큰 수명 · 재사용)
3. **cc 문서**: `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/para/projects/summer-star/cc-prototype/` 의 `30-work/work-009-app-v2.md` · `work-010-customer-questionnaire-web.md` · `10-decision/decision-007-app-v2.md` · `00-baseline/baseline-009-reservation-board.md` · `log/2026-10-28-overall-board.md` — 여권 · 문진 결정 · 막혔던 것(KOS 제약 등)
4. **DAY 에 이미 있는 것 / 없는 것**: 고객 여권 칸 · 문진 테이블(SPEC-000 · migration) · 예약 / 접수 API(SPEC-006 · 007 웹) · 앱 탭 구조(`app/lib/ui/shell.dart`) · 앱 네이티브 채널(iOS Swift · Android Kotlin — 카메라 / 텍스트 인식 채널이 있나) · 공개(로그인 없는) 웹 경로가 DAY 에 있나 · 앱 권한 문구(카메라는 WORK-001 D15 로 이미 있음)
5. **이식 표**: 기능 단위 행 — 「cc 에 있음 · 위치 / DAY 에 있음 · 위치 / 새로 필요(백 · 앱 · 웹 · 네이티브 iOS · Android · KOS) / 그대로 못 옮기는 이유(cc 전용 구조 · DB 다름)」
6. **정할 것**: 사용자가 정할 질문만(추천 한 줄 + 근거). 예: 진입 자리(예약 탭 신설 vs 시술현황 / 고객 화면) · Android 스캐너 범위 · 문진 결과를 KOS 에 쓰나 · 고객 웹을 DAY 가 호스팅하나 · 이번 판 범위(스캐너 먼저 / 둘 다)

## 산출물

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/research-2-report.md` — 맨 위 한 화면 요약(cc 에 있음 · DAY 에 있음 · 새로 필요 · 정할 것 수) · 근거는 파일:줄 @ref. 확인 못 한 것은 「확인 안 됨」. 설계 · WP 쓰지 마라. 실물 KOS · 서버 · DB 접속 금지.

완료 보고: dispatch preamble 의 `worker_done`(`--report-path` 위 리포트) + 브리프 §9 (2) 직접 주입.
