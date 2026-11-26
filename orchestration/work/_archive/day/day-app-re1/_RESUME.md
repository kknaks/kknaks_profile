
# 재개 노트 — day-app-re1 (day)

**지금**: WORK-001 앱 차트 = 사용자 시뮬레이터 E2E 확인(코드 `96036397` · 로컬 · push 전 · 머지 나중에 한 번에) · WORK-002 여권 스캐너 · 문진 QR · 앱 예약현황 = 결정 닫힘(§2 2026-11-25 행들) · 스펙 `22f7c30f`(planner-2) · review-doc-3 WARN 13 · U1 ~ U4 닫음 · U5(iOS 카메라 문구 여권) 사용자 대기 · spec `8195c0a8` · Delivery #287(backend+web · L3) · #288(mobile · L2) 발행(승인 = 사용자) · be-2 · app-2 완료 → code 커밋 `fb08fe4e`(로컬 · 미push) · review-code-2 FAIL 1(문진 제출 1회 DB 보장) · WARN 15 → code `ab8f6553`(fix) · A6 실물 일부 PASS(문진 QR → KOS 제출 sent · `e2e-a6-report.md`) · 여권 스캔 · 태블릿은 사용자 대기(외국인 오늘 예약 · 코디 계정) · 사용자 확인 = iOS 문구(OQ-A79) · ML Kit 고지(출시 전) · spec-sync 대기 = be-2 §0 계약 차이(kos_status→crm_status 등) · 미결 app-2 §5 8 「국적/통역필요」 웹 템플릿 ↔ SPEC U-3
**다음**: Delivery 1 완료 → backend · mobile 병렬(코드 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-app-re1` · `55e60aa4`) → reviewer → 로컬 스택 + 시뮬레이터 준비 → 사용자 E2E

세팅: `scripts/new-work.sh day day-app-re1` · 설정 SSOT `config/projects/day.json`
코디handle: `term_414d6113-407d-486b-ab54-10a4a6b455cb`

프로젝트·회고·당시 문서의 탐색은 이 폴더의 작업 목차(`README.md`)가 맡는다.
`sync-work-links.py`로 생성하며, 종료 후에도 프로젝트에서 같은 작업을 찾을 수 있어야 한다.

## 워크트리

- code: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-app-re1` (`kknaksss/day-app-re1` · base origin/dev `55e60aa4`)
- spec: `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-re1-spec` (`kknaksss/day-app-re1-spec` · base origin/main `b152d463`)



## 1. 지금

열린 것만 둔다. 닫히면 지우고 §5 이력으로 내린다.

- [!] research-2 §5 — 범위 · 태블릿 보내기는 사용자가 정함(§2) · research-3 완료 · §6 정할 것 9 중 T1 · T3 ~ T6 · T8 · T9 추천 기본값 통보 · 정할 것 전부 닫음(T7 = 읽기 전용) → WORK-002 스펙 발주
- [ ] WORK-002 결정표 → 스펙 → WP · Delivery → 코드(WORK-001 과 같은 slug · 워크트리)
- [ ] app-fix-1 남은 것: 실제 화면에서 채팅 배너가 차트 아래에 깔려 못 누름(푸시 길만 됨) · 저장 중 [버리고 닫기] 면 서버 저장은 끝남 · Q2 판 변경 정리 경로 테스트 없음 · §9 싼 고침(직원 정렬 · 커서 · 올리기 스피너)
- [ ] spec-sync 때: W3 크게 보기 = 새 화면 · W4 저장 띠 자리(2루프 E2E 뒤 SPEC 문장 / 배치 중 고름) · OQ-99 baseBody 문자열(GET null ↔ POST "")
- 시뮬레이터: `fvm flutter run -d 3304444A… --debug` + dart-define LOGIN_ENTRY · DEV_LOCAL_ORIGIN = http://127.0.0.1:11040(ALLOWED_ORIGINS 는 https 만 — http 넣으면 config_allowed_origins_invalid) · REQUIRE_ENVIRONMENT=false · APNS sandbox(로그 scratchpad flutter-run.log)
- [!] 로컬 스택 내려 둠(stop.sh · 볼륨 유지) · env 사본 `deploy/local.env` · `kos-demo.env`(ignored)는 코드 워크트리에 남음 — 마감 때 삭제 · 시뮬레이터 종료
- [ ] Delivery #281 · #282 승인 receipt = 사용자 몫(plan_digest 는 delivery-1-report.md)
- [ ] WORK-002 여권 스캐너 · 문진 QR(cc-prototype `procedure/app` scan/mrz · qr_show) — 차트 TestFlight 검수 뒤
- [!] 사용자 스크린샷 `~/.config/day/reference/app-chart-2026-11-25.png`(공개 레포 금지)

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-11-25 | 목표 = 앱 시술현황 차트를 웹과 같은 기능으로(WORK-001) → 앱 예약 탭(여권 스캐너 · 문진 QR · 시술전후 사진 차트에 넣기, WORK-002) | 사용자 |
| 2026-11-25 | 차트 먼저 · 예약 탭은 차트 사진 흐름을 재사용 | 사용자 승인(코디 추천) |
| 2026-11-25 | 지금 앱 차트 결함: 탭 아래 까만 줄 · 읽기만 됨 · (관찰) 시트가 하단 탭바 밑에 깔림 | 사용자 스크린샷 |
| 2026-11-25 | slug `day-app-re1`(옛 `_archive/day/day-app` 과 겹침 피함) · 브랜치 `kknaksss/day-app-re1` 로 이름 변경 | 코디 |
| 2026-11-25 | 코드 기준 CENTURION_DAY origin/dev `55e60aa4` | fetch |
| 2026-11-25 | **범위 = 차트만**(WORK-001) → 앱 빌드 · TestFlight 검수 → 그다음 여권 스캐너 · 문진 QR(WORK-002). 시술전후사진은 차트 기능 — 예약 탭에 사진 없음 | 사용자(「사이즈가 크잖아 · 차트만」) |
| 2026-11-25 | 시안 없음 — 앱 DS 컴포넌트 · 웹 차트 칸 배치 · 폰 = 전체 화면 · 아이패드 = 가운데 창(지금 그대로). 모양은 2루프 E2E 에서 | 사용자(공수 질문 → 코디 추천) |
| 2026-11-25 | D1 사진 탭 둔다 · D2 탭별 [저장] + 「최근 저장」(웹 C2 ~ C4) · D4 루트(세션) Navigator 에 띄움 · D5 담당자 고르기 = `doctor_picker.dart` 재사용 · D6 미저장 닫기 확인 창, 끌어 내림 · 바깥 누름으로 안 닫힘 · D7 앱용 새 `/api` JSON 경로(웹 HTML 경로 안 넓힘) · D11 값 원천 = `GET /api/visits/{id}/chart` | research-1 §6 추천 · 사용자 이의 없음 |
| 2026-11-25 | D8 사진 대상 방문 규칙 = 웹 그대로(오늘 판 · 시술 완료). 예약 쪽 확장 없음 | 사용자(사진은 차트 기능) |
| 2026-11-25 | D9 까만 줄 = 테마에서(앱 전체) · 탭바 겹침 = 같은 탭 Navigator 시트(원장 고르기 · 확인 시트)도 함께 | 코디 기본값 통보 |
| 2026-11-25 | D10 iOS 권한 문구 = 이번엔 지금 문구 유지 · 정식 출시 전 사용자 문구로(OQ) | 코디 기본값 통보 |
| 2026-11-25 | **D6′**(D6 고침) 미저장 없으면 ✕ · 바깥 누름 · 끌어 내림 · 뒤로 가기 다 닫힘(웹과 같게) · 미저장 있으면 ✕ / 뒤로 가기 → 확인 창 · 바깥 누름 / 끌어 내림 → 안 닫힘 | 사용자 「추천으로」(review-doc-1 확인 1) |
| 2026-11-25 | D12 미저장 때 iOS 가장자리 밀기 = 막힘(확인 창 없음) · D13 탭 글자 = 웹 글자 · D14 아이패드 팝오버 · 창도 루트 Navigator(투명 덮개 유지) | 사용자 「추천으로」 |
| 2026-11-25 | D15 iOS 권한 문구 — 카메라 「채팅으로 보낼 사진과 차트에 올릴 시술 전후 사진을 찍기 위해 카메라를 사용합니다. 찍은 사진은 사진첩에 저장하지 않습니다.」 · 사진 보관함 「채팅으로 보낼 사진 · 동영상과 차트에 올릴 시술 전후 사진을 고르고 최근 사진을 보여 주기 위해 사진 보관함을 사용합니다. 고른 것은 기기에 따로 저장하지 않습니다.」 (D10 대체) | 사용자 「문구도 넣어줘」 → 코디 초안 |

| 2026-11-25 | 머지는 나중에 한 번에(스펙 PR #964 draft · 코드 PR 도) · WP 는 Delivery Issue 로 발행 · 코드 구현까지 끝낸다 | 사용자 |
| 2026-11-25 | **E2E = 사용자가 시뮬레이터에서**(TestFlight 대신) → 로컬 BE 스택 + 시뮬레이터 앱이 완료 기준 · dev 배포 · TestFlight 는 이번 단계 아님 | 사용자 |
| 2026-11-25 | 백엔드 변경 있음 = 앱 `/api` JSON 짝 6 · migration 없음 | SPEC-002 ㉚ |

| 2026-11-25 | Delivery baseline = `ready`(main b152d463 · SPEC-002/003 이미 stable → 「stable 고도화」 갈래 · 변경은 Target Delta) — 그대로 둠 | delivery-workflow · 코디 |
| 2026-11-25 | 실물 e2e(KOS · 로컬 스택 · 시뮬레이터)는 코디 · 워커는 테스트 더블 | 앞 작업 관례 |

| 2026-11-25 | Q1 푸시 · 알림 · 채팅 배너 [보기]가 미저장 차트 위로 이동 = ✕ 와 같은 확인 창 · Q2 룸 상세 닫힘 / 카드 빠짐 = 그 방문 확인 시트 · 원장 고르기 팝오버 같이 닫음(차트 창은 OQ-A69 대로 남김) | review-code-1 · 코디 추천 기본값(사용자 통보) |

| 2026-11-25 | WORK-002 범위(research-2 Q2 · Q9 · Q10 · Q11 뒤집음): 앱에 **예약현황 탭** 신설 · 웹 예약 상세 모달 내용을 앱에 그대로 · 거기서 이 기기로 QR · 여권 스캔 · 또는 **웹 · 앱에서 태블릿 골라 보내기**(코디용 계정으로 로그인한 태블릿) → 앱이 열려 있으면 바로 뜸 · 아니면 알림 눌러서 뜸(cc 띄우기 = SSE + 푸시와 같은 꼴) · 문진 QR · 여권 스캐너 둘 다 | 사용자 |
| 2026-11-25 | 코디 태블릿 = 갤럭시 탭 · **아이패드 · 갤럭시 둘 다** 만든다(사용자는 아이패드) → Android 카메라 스캔도 이번 판(research-2 Q3 뒤집음 · 원천 없음 = 새로 만듦) | 사용자 |
| 2026-11-25 | 남은 것은 추천대로: Q7 문진 = KOS 양식 · 약관을 받아 DAY 가 그리기만 하고 KOS 에 제출(cc 와 같음 · 제출이 KOS 고객 성별 · 생년월일 · 주소 · 휴대폰을 바꾸는 건 KOS 동작 그대로 받음) · Q6 여권 사진 = KOS + DAY 저장소 둘 다 · DAY-ESC-001 은 참조만(비차단) · Q1 · Q4 · Q5 · Q8 · Q12 추천대로 | 사용자 「kos꺼 그대로 랜더링만 바꾼 거 · 추천으로」 |
| 2026-11-25 | 문진 답 = **DAY DB(`questionnaire_history`)에도 저장** + KOS 제출. 순서 = DAY 먼저 저장 → KOS 제출 · KOS 실패해도 답은 남기고 상태(보냄 / 실패) + [다시 보내기](cc 는 KOS 성공 뒤에만 저장 · 실패 = 아무것도 안 남김 — 여기서 바꿈 · 코디 기본값 통보). 직원은 DAY 에 저장된 답을 본다 | 사용자 「우리쪽 db 에도 저장」 |
| 2026-11-25 | 태블릿 = **공용 코디 계정 하나**(KOS 직원 계정 · 직무 코디 · 지점에서 만듦)로 로그인한 태블릿(research-3 T2). 기기 등록 토큰 · 계정 없는 기기안은 버림(사용자 「스펙이 너무 복잡」). 기본값: 보낼 목록 = coordinator 직무 계정의 `device.kind=tablet` 기기(T1 a · 새 칸 없음) · 기기 이름 = 설정 「이 기기 이름」(T3) · 그 기기 하나로만(T4) · 태블릿 스캔의 KOS 쓰기 = 태블릿에 로그인한 코디 계정 토큰(KOS 기록 = 코디 계정 · 알고 감) · 계정당 5대 한도(넘으면 계정 하나 더) · T5 · T6 · T8 · T9 추천대로 | 사용자 + 코디 기본값 통보 |
| 2026-11-25 | 앱 예약현황 = **읽기 전용**(폰 · 태블릿 같음 · research-3 T7). 앱에서 누르는 건 [문진 QR] · [여권 스캔] · [태블릿에 보내기]만 · 웹 모달 쓰기 11개는 앱에 안 넣음. 앱 구조 = cc 앱 예약 현황 · 예약 상세 구조를 DAY 스타일로 | 사용자 「예약현황 읽기 전용 · 큐알 스캐너 버튼만」 |
| 2026-11-25 | 앱 예약현황은 **DAY 웹 예약현황과 닮게** — 칸 · 순서 · 글자 · 단계 이름 · 색 · 카드 정보 = 웹(SPEC-006 · 007) 그대로 · 태블릿 = 웹 같은 시간 × 열 표 · 폰 = 같은 카드를 목록으로 · 상세 = 웹 모달 상자 순서 그대로(읽기 전용). cc 앱은 탭 → 목록 → 상세 흐름 · 스캔 · QR 화면 구조만 참고 | 사용자 「웹이랑 어느 정도 비슷해야」 · 코디 기본값 |
| 2026-11-25 | review-doc-3 U1: **외국인 여권 스캔 저장 = 신분확인 O → 웹 [상담 대기] 켜짐**(웹 예약 동작 하나 바뀜 · OQ-D36 닫음) | 사용자 「스캔하면 신분 확인 되는 거 · 켜야지」 |
| 2026-11-25 | review-doc-3 U2 · U3 · U4 기본값: U2 Android 띄우기 알림 채널 이름 = 「고객 입력 요청」(cc 푸시 제목) · U3 웹 · 앱 글자 = 「태블릿에 보내기」로 통일 · U4 앱 예약 상세 JSON 에 여권번호 안 실음 — 스캔 확인 화면 열 때만 따로 읽음 | 코디 기본값 통보 |
| 2026-11-25 | 보충 조사 research-3 발주 승인 | 사용자 「응」 |
| 2026-11-25 | WORK-001 시뮬레이터 E2E 확인 — 「잘했어」 · 지적 없음(W3 크게 보기 · W4 저장 띠 자리는 지금대로 → spec-sync 때 SPEC 문장을 구현에 맞춤) | 사용자 |
| 2026-11-25 | 다음 = WORK-002 문진 QR · 여권 스캐너(TestFlight 는 이번엔 안 함 — 시뮬레이터 E2E 로 대신) | 사용자 「이제 내리고 다음 거 준비」 |

## 3. 발주 (살아 있는 것만)

Run `run_0f5c43ea997c`

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| researcher | `term_f5efd8c5-81e2-4c58-b4bb-5353dfbd7986` | `task_9d55c6c2dcde` | `ctx_09b37587ff7f` | `day-app-re1-research-brief.md` | 완료 · release(retained 터미널) |
| planner | `term_a66de887-a586-46cb-895d-3c91d320df3c` | `task_501ad4aa67f7` | `ctx_bc06f8ebd5a5` | `day-app-re1-spec-brief.md` | 완료 · released |
| reviewer_doc | `term_ad64ec53-91ea-4d5b-92ff-f2eb52f3728d` | `task_374b6f37d593` | `ctx_60077edbb60b` | `day-app-re1-review-doc-brief.md` | 완료(WARN 7) · released |
| planner | `term_1eda9b39-4c8f-4eaa-838f-9e03ce2fc6f0` | `task_76aef4d6c631` | `ctx_00f1621e4601` | `planner-fix-1-instructions.md` | 완료 · released |
| reviewer_doc | `term_27e860fd-c451-4268-a861-31b13d12a856` | `task_7ad153abe308` | `ctx_14984e8be22c` | `review-doc-2-instructions.md` | 완료(WARN 가벼움 N1 · N2) · released |
| planner | (preamble) | `task_e1984b0d9730` | `ctx_a45888c337ee` | `planner-fix-2-instructions.md` | 완료 · released |
| planner | `term_14517dd0-f92c-4e7f-bf0c-c25bfcd9366d` | `task_c90f835dabb1` | `ctx_0bb921bcda95` | `planner-delivery-1-instructions.md` | 완료 · released |
| backend | `term_87dad2be-8099-4806-aa60-9d608e98d6d6` | `task_20ef194cf224` | `ctx_5d2f4eb88910` | `day-app-re1-be-brief.md` | 완료(be-1-report · 2902 passed) · released |
| mobile | `term_b196a812-747f-433d-812c-1b23eb29b737` | `task_7d4d46f65aa1` | `ctx_c179acd062fa` | `day-app-re1-app-brief.md` | 완료(app-1-report · analyze 0 · build ios OK) · released |
| reviewer | `term_0936ddaf-a6bb-43b4-a9e3-80624c4f9c65` | `task_477660196f54` | `ctx_3ea3687caa43` | `day-app-re1-review-brief.md` | 완료(WARN 9 · Q2) · released |
| backend | `term_0b6f3e54-bb26-47a8-8ca3-abff94785a53` | `task_cacca6fe1e63` | `ctx_dffc42c036e6` | `be-fix-1-instructions.md` | 완료(check.sh 전체 통과 · 2902) · released |
| mobile | `term_789825d5-0273-4f2a-9d2b-d9c1baa85a5c` | `task_2b40793f4fa7` | `ctx_b05b58bf0410` | `app-fix-1-instructions.md` | 완료(test +472 −0 · build OK) · released |
| researcher | `term_9f64455f-2b98-4fb0-a47e-e95c3a2b1a4c` | `task_2500074cf384` | `ctx_1d81c919a2c3` | `research-2-instructions.md` | 완료(이식 18 · 정할 것 12) · released |
| researcher | `term_ca0e7c8f-6f17-4a5d-9225-f535305cf8c4` | `task_2e12c86aa606` | `ctx_8154573e681d` | `research-3-instructions.md` | 완료(웹 상세 17 · 목록 6 · 정할 것 9) · released |

| planner | `term_54cc65f7-67ec-47b8-94ea-6a01b88d5058` | `task_08260be5b11b` | `ctx_064f9b84622f` | `planner-2-instructions.md` (+ 보충 1 웹과 닮게) | 완료(SPEC 6 · migration 1 · lint day 0/0) · released |
| reviewer_doc | `term_665d7618-96dc-4ea3-b388-df4e5aecdb92` | `task_7fe78ba8bab3` | `ctx_b0629c13b637` | `review-doc-3-instructions.md` | 완료(FAIL 0 · WARN 13 · 사용자 확인 5) · released |
| planner | `term_97742dab-ac73-4c38-b1bb-f98b5819fe0d` | `task_ed6f9234f13c` | `ctx_f87111bd5cf9` | `planner-fix-3-instructions.md` | 완료(W1~W13 · U1~U4 · spec `8195c0a8`) · released |
| reviewer_doc | `term_05434896-4287-4726-826d-788deef16384` | `task_811dee409b31` | `ctx_76d20fe60c5f` | `review-doc-4-instructions.md` | 완료(WARN 가벼움 N1~N6 · FAIL 0 · U1 [시술 대기] = 같은 칸 범위 안) · released |
| planner | `term_4947f845-c520-4a26-a575-0694c104187a` | `task_e3a77b7d1707` | `ctx_df06bd332f6b` | `planner-delivery-2-instructions.md` | 완료(N1~N6 `fadb46f6` · #287 · #288 · PR #964 `a018f4fa`) · released |
| backend | `term_dcb1f05f-1727-4150-8d36-338e57863e98` | `task_6bb15427e15f` | `ctx_62d84a6270e6` | `be-2-instructions.md` | 완료(check.sh 2995 passed · migration 0029 · 의존성 segno) · released |
| reviewer | `term_9c207bed-71e1-4574-9f04-4d8f80a18571` | `task_00e2bd7ec014` | `ctx_7245a91a755b` | `review-code-2-instructions.md` | 완료(FAIL 1 F1 · WARN 15 · 계약 PASS) · released |
| backend | `term_edb00cca-def4-42c0-8206-085e681f0318` | `task_86c6613a74a2` | `ctx_02fe2016bef0` | `be-fix-2-instructions.md` | 완료(F1 · BW1~5·7·8 · 3024 passed / 2 failed test_devices_push = 맥 잠듦 시각 의존 · 단독 12 passed 코디 확인) · released |
| mobile | `term_eb939968-a221-4efa-bb43-c08dfd0c685e` | `task_9b6cfde7b5ac` | `ctx_b01b0fc11b48` | `app-fix-2-instructions.md` | 완료(AW1~AW6 · test 527 · Kotlin 12/12 · build OK) · released |
| backend | (orca) | `task_20d5ee2fc02e` | `ctx_6592ef473307` | `merge-dev-2-instructions.md` | 완료(code merge `716e89d6` · spec merge `538befe4` · check.sh 0 · pytest 3185 · flutter 544 · 끊긴 참조 0) · released |
| backend | (orca) | `task_bf9855d26ace` | `ctx_9807fa3d1a41` | `merge-dev-3-instructions.md` | 완료(merge `1142b480` · 0030 · check.sh 0 · 3211) · released |
| mobile | (orca) | `task_f0e97e23637d` | `ctx_3ccf59c438c1` | `mobile-build-2-instructions.md` | 완료(TestFlight 0.3.0(5) VALID · IN_BETA_TESTING · Play internal vc5 completed) · released |
| planner | (orca) | `task_c6d53d38de92` | `ctx_0be998e5e2a0` | `spec-sync-2-instructions.md` | 완료(11 파일 · lint 0/0 · 구현 의심 0 · 사용자 확인 3 = BW6 Redis 장애 · 국적 alpha-2 · OQ-A95/A93) · released |
| reviewer_doc | (orca) | `task_fc87d32922b7` | `ctx_c2eaa578c0fb` | `review-doc-5-instructions.md` | 완료 WARN(FAIL 0 · WARN 7 — 문서 잔재) · released |
| planner | (orca) | `task_1ee4ec736a47` | `ctx_5b5f0c952109` | `spec-sync-3-instructions.md` | 진행 — review-doc-5 WARN 7 고침 |
| backend | (orca) | `task_dd68aa41cf40` | `ctx_e9d3a4816ff7` | `renumber-refs-instructions.md` | 완료(130 파일 ±271 · check.sh 0 · 544) → PR #298 스쿼시 dev `3543d8b2` · released |
| mobile | `term_e084b658-e8d9-4c29-9c97-d7d34f2064d6` | `task_4c76baf77643` | `ctx_6102856d281b` | `app-2-instructions.md` | 완료(test 517 · analyze 0 · build ios · apk OK · Kotlin 9/9) · released |
## 4. 산출물

- code 커밋: `fb08fe4e`(WORK-002) ← `96036397`(fix-1) ← `43ba40a3`(kknaksss/day-app-re1 · 로컬)
- 리포트: `be-1-report.md` · `app-1-report.md` · `e2e-a4-report.md`(A4 PASS)
- Delivery: CENTURION_DAY#281(BE · L3) · #282(APP · L2) — delivery-plan:review
- spec PR: MediSolveAIDev/mediness#964(+ `319dd82e` 30-work · log)(draft · 머지 나중)
- spec 커밋: `e7c51875`(kknaksss/day-app-re1-spec · 로컬)
- 리포트: `review-doc-2-report.md` · `planner-fix-2-report.md`(N1 · N2 코디 확인)
- 리포트: `planner-1-report.md`(완료 · lint 0 error · day 범위 0/0 · 5 파일 +271 −30)
- 리포트: `research-1-report.md`(완료 · 코디 대조: api/board.py:149 차트 GET · chart_sheet.dart:19 탭 Navigator 확인)

## 5. 이력 (최신이 위)

- `2026-11-26` 사용자 「마감하자」 · spec-sync 지금 다 함(스펙 + 코드 주석 번호) · KOS 데모 테스트 데이터 그대로 둠 → spec-sync-2 · renumber-refs 병렬 발주 → review-doc → 스펙 PR #964 main · 주석 PR dev → archive
- `2026-11-26` PR #295 → dev 스쿼시 `8fe0095a` · deploy-dev success · 로컬 DB 0029→0028 UPDATE → upgrade 0029_partner_charty → stamp 0030 · 사용자 결정: TestFlight 0.3.0 (5) · Android internal vc5 같이 · iOS 카메라 문구 OQ-A79 제안 문구 → PR #296 스쿼시 `a76496c4` → mobile-build-2 발주
- `2026-11-26` 사용자 「e2e 확인된 듯 · TestFlight 위해 dev 스쿼시 머지」 → dev 가 다시 10 커밋 앞섬(다른 사람 #293 Charty · 0029_partner_charty 겹침) → merge-dev-3 발주 → 그 뒤 PR → 스쿼시 머지 → TestFlight
- `2026-11-26` merge-dev-2 완료 → 코디 커밋 code `716e89d6` · spec `538befe4`(로컬 · 미push) · 스택 재시작(0029) · iPad 앱 다시 띄움 · 남은 것 = 코드 주석 · 시험 설명의 옛 스펙 번호 약 119 파일(대응표 merge-dev-2-report §4) → spec-sync 때 같이
- `2026-11-26` dev 3 커밋(#285 · #286 메뉴 막음 · #292 방별 순) · 스펙 main 4 커밋 앞서감 → merge-dev-2 발주(사용자 「응 발주」) · 웹 [문진 QR] · [여권 스캔]은 우리 브랜치에서 이미 켜짐 · 메뉴 링크는 #286 대로 막힘 유지
- `2026-11-25` review-code-2 FAIL(F1) · WARN 15 → be-fix-2 · app-fix-2 발주
- `2026-11-25` be-2 · app-2 완료 → code `fb08fe4e`(119 파일) · review-code-2 발주
- `2026-11-25` Delivery 2 발행 #287 · #288(첫 apply 422 본문 한도 → 계약 압축 재발행) · be-2 · app-2 발주
- `2026-11-25` planner-2 완료 → spec 커밋 `22f7c30f`(003 ㉒ · 007 고침 5 · 006 ⑭ · 005 · 004 · 000 · OQ-A79 iOS 여권 문구 · OQ-D36) · review-doc-3 발주
- `2026-11-25` research-3 완료(cc 는 스캔도 태블릿으로 보냄 · 웹 보내기 있음 · DAY SSE / 푸시 = 계정 단위 · 웹 예약 = 쿠키 HTML 만 · Android = CameraX + ML Kit 번들)
- `2026-11-25` WORK-002 범위 사용자 결정(예약현황 탭 · 웹 모달 그대로 · 태블릿 보내기 · 아이패드 + 갤럭시) · research-3 발주
- `2026-11-25` research-2 완료(앱엔 예약 · 접수 단계 고객 화면 없음 · DAY 표만 있고 코드 0 · cc 스캐너 iOS 전용)
- `2026-11-25` WORK-001 사용자 E2E 확인 · 스택 · 시뮬레이터 내림 · research-2 발주
- `2026-11-25` be-fix-1 · app-fix-1 완료 → 커밋 96036397 · 시뮬레이터 띄움 → 사용자 E2E 대기
- `2026-11-25` review-code-1 WARN(FAIL 0) → be-fix-1 · app-fix-1 발주
- `2026-11-25` be-1 · app-1 완료 → 커밋 43ba40a3 → review-code-1 발주 · 코디 A4 실물 PASS
- `2026-11-25` Delivery #281 · #282 발행 → backend · mobile 발주
- `2026-11-25` 스펙 PR #964 · 코드 워크트리 · planner Delivery 1 발주 · E2E = 시뮬레이터
- `2026-11-25` planner-fix-2 완료 · 코디 확인 · 스펙 로컬 커밋 `e7c51875`
- `2026-11-25` review-doc-2 WARN 가벼움(W1 ~ W7 닫힘 · N1 · N2) → planner-fix-2 발주
- `2026-11-25` planner-fix-1 완료 → review-doc-2 발주
- `2026-11-25` review-doc-1 WARN(FAIL 0 · WARN 7) → 사용자 「추천 + 문구」 → planner-fix-1 발주
- `2026-11-25` planner-1 완료 → review-doc-1 발주
- `2026-11-25` 범위 = 차트만 · 결정 D1 ~ D11 닫음 · planner-1 발주
- `2026-11-25` research-1 완료 — 앱 차트 API 0건 · 저장/사진 앱 JSON 없음 · 정할 것 11
- `2026-11-25` 작업 시작 · 차트 먼저 결정 · research-1 발주

이 절은 **재개에 필요한 만큼만** 쓴다. 회고·배운 것은 `SUMMARY.md` 몫이다.
