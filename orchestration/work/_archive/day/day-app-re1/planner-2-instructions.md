# [planner] planner-2 — WORK-002 앱 예약현황(읽기 전용) · 문진 QR · 여권 스캐너 · 태블릿으로 보내기 — DAY SPEC 개정

너는 day `planner` 워커다. 역할 · 규칙 · 검증 · 완료 보고 형식은 같은 폴더 `day-app-re1-spec-brief.md` 를 따른다(먼저 읽어라 — 역할 문서 경로 · §5 allowed_paths `products/day/` · §7 금지 중 「WORK-002 쓰지 마라」 줄만 이번엔 뒤집힘 · §8 lint · §9 보고). 이번 대상만 아래로 바꾼다.

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-re1-spec` (브랜치 `kknaksss/day-app-re1-spec` · WORK-001 커밋 `e7c51875` · `319dd82e` 위에 이어 쓴다 · 커밋 · push 금지)

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/_RESUME.md` §2 — **2026-11-25 WORK-002 행 전부**(「WORK-002 범위」 · 「아이패드 · 갤럭시 둘 다」 · 「남은 것은 추천대로 Q7 · Q6 …」 · 「문진 답 = DAY DB 에도 저장」 · 「공용 코디 계정 하나」 · 「앱 예약현황 = 읽기 전용」). **계약의 SoT — 다시 열지 마라. 여기 없는 정책은 발명하지 마라.**
- `research-2-report.md`(cc 이식 표 S1 ~ S10 · Q1 ~ Q8 · §5 정할 것 Q1 ~ Q12 — 처분은 §2 결정이 이긴다) · `research-3-report.md`(태블릿 띄우기 · DAY 기기 / 푸시 / SSE · 웹 예약 상세 17 · 목록 6 이식 표 · Android 부품 · §5 고칠 절 표 · §6 T1 ~ T9 — 처분은 §2)
- 원천 cc-prototype `/Users/kknaks/git/toy_pr2/cc-prototype` origin/main(`git show` 만) · cc 문서 `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/para/projects/summer-star/cc-prototype/`(work-009 · work-010 · decision-007)

## 2. 결정 요약(§2 를 줄인 것 — 다르면 §2 가 맞다)

1. 앱 하단에 **예약현황 탭 다시 넣음**(SPEC-003 개정 ⑮ 숨김 해제 · 이유 적기). 목록 = 폰 목록 / 태블릿 시간표(T8). 상세 = 웹 예약 상세 모달 **내용을 읽기 전용으로** — 웹 쓰기 11개는 앱에 없음. 누르는 것 = [문진 QR] · [여권 스캔] · [태블릿에 보내기]만. 구조 = cc 앱 예약 현황 · 상세를 DAY 앱 DS 로.
2. 이 기기에서: 문진 QR 전체 화면(cc `qr_show_screen` 꼴) · 여권 스캔(iOS = cc Vision 꼴 · **Android = CameraX + ML Kit 번들 네이티브 채널 · 새로 만듦** · 파서 = cc `mrz.dart` · 손 입력 길 남김).
3. 태블릿으로 보내기: **웹 예약 상세 · 앱 예약 상세** 둘 다에서 기기 고르기 → 그 **기기 하나**로(T4). 태블릿 = **공용 코디 계정(KOS 직원 계정 · 직무 coordinator)으로 로그인한 `device.kind = tablet`**(T1 a · 새 칸 없음). 기기 이름 = 앱 설정 「이 기기 이름」(T3). 앱 열려 있으면 바로 뜸(실시간) · 아니면 알림(cc 그대로 · 소리 없음 · 고객 이름 없음 · 목록 밖 T5) 눌러서 뜸 · 놓친 것 메우기. 보낸 쪽 진행 = 실시간 신호(T6). 지금 DAY SSE · 푸시는 **계정 단위** — 기기 하나로 가는 규칙을 새로 적어야 한다(research-3 §0-2). 계정당 KOS 동시 로그인 5개 = 태블릿 5대 한도(알고 감 · 넘으면 계정 하나 더).
4. 여권 스캔 저장: KOS 고객 수정 = **그 기기에 로그인한 직원 토큰 직접**(태블릿이면 코디 계정 — KOS 기록 = 코디 계정 · 알고 감) · 여권 사진 = KOS(시술전후사진 내부 경로 재사용 · 분류 「여권」) + **DAY 저장소 둘 다** · DAY-ESC-001 은 참조만.
5. 문진: KOS 양식 · 약관을 받아 DAY 가 그리기만(고객 웹 = **DAY 백엔드 로그인 없는 공개 Jinja 페이지**) · 답 = **DAY DB(`questionnaire_history`) 먼저 저장 → KOS 제출** · KOS 실패해도 답은 남고 상태(보냄 / 실패) + [다시 보내기] · KOS 제출이 KOS 고객 성별 · 생년월일 · 주소 · 휴대폰을 바꾸는 건 받아들임 · 직원은 DAY 저장분을 봄(웹 예약 상세 「초진 문진 · 건강정보」 값 채움 · 앱 상세도 읽기). 링크 수명 cc 그대로(열기 10분 · 쓰기 60분 · 제출 1회 · 새 링크가 앞 링크 닫음) · 공개 경로 보안은 cc 규칙을 끌어옴.
6. 웹 예약 상세 [문진 QR] · [여권 스캔] **켬**(SPEC-007 D13 · D20 고침 · D55 보이는 조건은 그대로).

## 3. 산출물

research-3 §5 고칠 절 표를 **전부** 처리한다(행마다 「고침 / 그대로 + 근거」 · 빠진 행 0) — SPEC-003 · SPEC-005 · SPEC-006 · SPEC-007 · SPEC-004(OQ-C7 여권 문구) · SPEC-000(`display_request` 스캔 종류 · 기기 하나 대상 규칙 · `id_photo` KOS 상태 자리 · `questionnaire_history` 상태 · SPEC-000:1076 outbox 문장과 결정 4 · 5 의 차이). 문진 공개 페이지 · 공개 API 를 어느 SPEC 에 둘지는 네가 정해 근거와 함께 적는다(새 SPEC 이 필요하면 그 이유).

각 SPEC: 다음 개정 번호 머리글(①②… 결정 짝) · 화면 구성 · API 계약 표(앱 `/api` JSON — 예약 목록 · 상세 읽기 · 기기 목록 · 띄우기 요청 / 메우기 / 상태 · 여권 스캔 저장 · 문진 공개 API · **이름 제안**) · 권한 · 오류 코드 · 인수 조건 · OQ. 앞 판 「범위 밖」 · 「비활성」 조항은 ~~취소선~~ + 날짜 · 사유. migration 필요 여부를 근거와 함께(기대: 있음 — `display_request` · `id_photo` · `questionnaire_history` 칸 · 상태). `20-spec.md` · `10-decision.md` · `log.md` 반영.

**30-work 는 이번에 쓰지 않는다** — SPEC 검수 뒤 따로.

## 4. 범위 제약

- 결정을 다시 열지 않는다. 결정과 앞 판이 다르면 결정을 따르고 차이를 적는다
- 화면 문구 · iOS / Android 권한 문구를 지어 넣지 않는다 — cc 원천 · DAY SPEC 에 있는 글자만, 없으면 비우고 OQ. 6개 언어 문진 문구도 cc 원천 것만
- 앱 예약 상세에 쓰기를 넣지 않는다 · 웹 예약 동작 · WORK-001 차트 계약을 바꾸지 않는다
- 「확인 안 됨」(research-3 §7 · research-2 §6)은 OQ 로 두고 메우지 않는다

## 5. 완료 보고

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/planner-2-report.md`(바꾼 절 목록 · research-3 §5 표 처분 · research-2 S1 ~ S10 · Q1 ~ Q8 처분 · OQ · migration 판단 · lint 결과). dispatch preamble 의 `worker_done` + 브리프 §9 (2) 직접 주입.

## 보충 1(코디 · 발주 직후 사용자 결정 — §2 결정 1 의 「구조」 줄을 이걸로 바꿔 읽어라)

앱 예약현황은 **DAY 웹 예약현황 · 예약 상세와 닮게** 만든다. 칸 · 상자 순서 · 화면 글자 · 단계 이름 · 단계 색 · 카드에 싣는 정보 = **웹(SPEC-006 · SPEC-007) 그대로**. 태블릿 = 웹과 같은 시간 × 열 표 · 폰 = 같은 카드를 목록으로 · 상세 = 웹 모달 상자 순서 그대로(읽기 전용 · 쓰기 버튼 자리는 두지 않음). cc 앱은 **탭 → 목록 → 상세 흐름과 스캔 · QR 화면 구조만** 참고한다. research-3 §3.1 · §3.2 표 행마다 「앱에 넣음(읽기) / 쓰기라 뺌」 처분을 적어라.
