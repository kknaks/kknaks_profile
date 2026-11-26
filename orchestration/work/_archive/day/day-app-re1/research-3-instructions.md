# [researcher] research-3 — WORK-002 보충 조사: 앱 예약현황 탭 · 태블릿으로 보내기 · Android 스캔(read-only)

너는 day `researcher` 워커다. 역할 · 규칙 · 완료 보고 형식은 같은 폴더 `day-app-re1-research-brief.md` 를 따른다(먼저 읽어라 — §1 git 읽기 규칙 · §7 금지 · §9 보고). 같은 폴더 `research-2-report.md` 를 먼저 읽어라 — 이번은 그 보충이다. 거기서 센 것은 다시 세지 말고 가리키기만 해라.

DAY 코드 기준 = CENTURION_DAY `96036397`(코드 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-app-re1` — 읽기만 · 빌드 · 실행 금지). 스펙 = mediness `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-re1-spec` `products/day/` 읽기만. cc = `/Users/kknaks/git/toy_pr2/cc-prototype` origin/main(`git show origin/main:<path>` 만).

## 배경 — 사용자가 정한 범위(research-2 추천 Q2 · Q3 · Q9 · Q10 · Q11 을 뒤집음 · 다시 묻지 마라)

1. 직원 앱에 **예약현황 탭** 신설. 거기서 **웹 예약 상세 모달 내용이 앱에 그대로** 뜬다(목록만이 아님).
2. 앱 예약 상세에서 **이 기기로** 문진 QR 띄우기 · 여권 스캔.
3. 또는 **웹 예약 상세 · 앱에서 보낼 태블릿을 골라** 그 태블릿으로 보낸다. 태블릿 = 코디용 계정으로 DAY 앱에 로그인한 기기. 태블릿 앱이 열려 있으면 **바로 뜨고**, 아니면 **알림을 눌러서** 뜬다. 보내는 것 = 문진 QR · 여권 스캔 둘 다.
4. 태블릿 = **갤럭시 탭(Android) · 아이패드 둘 다**. Android 도 **카메라 여권 스캔**을 한다.
5. 문진은 KOS 양식 · 약관을 그대로 그리고 KOS 에 제출(cc 와 같음) · 여권 사진은 KOS + DAY 저장소 둘 다.

## 조사

1. **cc 태블릿 띄우기 전수**: 앱 `launchers.dart` 기기 고르기 · 백 `service/display.py` · `api/display.py` · SSE 경로 · 푸시 · 태블릿 쪽에서 무엇이 뜨나(QR 화면 · 스캔 화면 각각) · 알림 누르면 어디로 · 끝나면 보낸 쪽에 어떻게 알리나(폴링 · SSE) · 기기 목록은 어디서 오나(기기 표 · 계정 · 역할) · **여권 스캔도 태블릿으로 보내는 길이 cc 에 있나**(QR 만인가) · **cc 웹에 「태블릿에 보내기」가 있나**(없으면 「없음」). 흐름을 단계별로.
2. **DAY 기기 · 계정 · 알림 구조**: `device` 표 · 기기 등록 API · 푸시 보내는 경로(APNs · FCM 둘 다 되나) · 앱 SSE / 실시간 채널이 있나(채팅 등 — 재사용 후보) · 계정 역할(코디 · 직군) · 「코디용 태블릿 계정」을 지금 구조로 표현할 수 있나(새 칸 필요한지 사실만) · 한 계정이 여러 기기에 로그인 가능한가.
3. **웹 예약 상세 모달 → 앱 이식 범위**: 웹 예약 상세(SPEC-006 · SPEC-007 · `templates/` 예약 상세 partial · 관련 router)에 있는 칸 · 상자 · 버튼 전수 표 — 행마다 「웹 위치 · 데이터 API(HTML partial 인가 JSON 인가 · 앱 토큰으로 부를 수 있나) · 쓰기 동작인가 읽기인가 · 앱에 지금 있나」. 웹 예약 현황 목록(날짜 · 필터) 도 같은 방식. 앱 `/api` 에 예약 JSON 이 있나 · 없으면 빠진 것 목록(설계 금지).
4. **Android 카메라 여권 스캔 길**: DAY 앱 `pubspec.yaml` · Android 빌드(minSdk · CAMERA 권한) 사실 · MRZ 를 Android 에서 읽을 수 있는 후보(ML Kit 글자 인식 · CameraX · Flutter 패키지 등) — 후보별 「오프라인 동작 · 라이선스 · 앱 크기 · cc `mrz.dart` 파서를 그대로 쓸 수 있나」 · iOS cc `TextScanner.swift` 와 같은 꼴(네이티브 채널)로 갈 수 있나. 웹 문서 확인이 필요하면 공식 문서만 · 확인 못 하면 「확인 안 됨」.
5. **스펙 대조**: 태블릿 띄우기를 범위 밖으로 둔 곳(SPEC-003:123 · SPEC-005:77 등) · 예약현황 탭을 숨긴 곳 · 웹 [문진 QR] · [여권 스캔] 비활성(SPEC-007 D13 · D55) — 바꾸려면 고칠 절 목록.
6. **정할 것**: 위 범위 안에서 사용자만 정할 수 있는 것만(추천 한 줄 + 근거). 범위 자체는 다시 묻지 마라.

## 산출물

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/research-3-report.md` — 맨 위 한 화면 요약 · 근거는 파일:줄 @ref · 확인 못 한 것은 「확인 안 됨」. 설계 · WP 쓰지 마라. 실물 KOS · 서버 · DB 접속 금지. 리포트 1개 말고는 아무것도 쓰지 마라.

완료 보고: dispatch preamble 의 `worker_done`(`--report-path` 위 리포트) + 브리프 §9 (2) 직접 주입.
