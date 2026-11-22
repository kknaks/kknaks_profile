# 작업 요약 — day-mobile-v2 (day)

기간: `2026-11-20` ~ `2026-11-22`
결과: 직원 앱 0.2.0(병원 인계 판) 코드 · 스펙 끝. CENTURION_DAY #266 → dev 스쿼시 머지 `5ece25ea` · dev 배포(migration 0013 · 0014) · DAY Dev 0.2.0 TestFlight (4) · Play internal vc4 업로드. 스펙 mediness #955 → main `3ae2317e`. Delivery #262(메인) · #263(FCM) v2 재결속. 실기기 확인 · prod 서버 · 정식 앱은 다음(§7).

## 1. 무엇을 했나

1차 배포(0.1.0)는 쓰는 사람이 없었다. 사용자는 「이 버전까지 해서 병원에 인계」하기로 하고 범위를 넷으로 잡았다. 처음 셋에 사용자가 중간에 호출 취소 알림을 더했다.

- **KOS 기기 제한 → 앱 기기 선택**: 웹 #257 의 서비스를 다시 쓰고, 앱용 JSON(`choose_device` · `POST /api/auth/device`)만 더했다. 데모 넘김(prod → dev)도 받게 했다.
- **시술 현황 앱**: 바로 시작([의사 호출] 옆 · 의사 호출 드로어 재사용) · 호출 취소 · 「간호관리」 · 방 옮기기 · 복귀 · 점유 띠 · 원장 바꾸기. 스냅샷에 `canCancelCall` · `canQuickStart` · `canChangeDoctor` 를 더했다. 귀가 대기 취소 · 정렬 탭 · 순서 변경은 뺐다.
- **호출 취소 알림** `doctor_call_cancel`: 호출이 완전히 닫힐 때 한 번만 보낸다. 받는 사람은 원래 알림을 받은 계정이다. 원래 알림은 닫는다. iOS 는 APNs, 웹은 OS 알림이다. migration 0013.
- **Android 푸시 FCM**: 기기 platform `android`(migration 0014), FCM HTTP v1, 채널 「원장 호출」 · 「채팅」, [수락].
- **통역 = 통키(interpret-pwa `56e43a0`) 최신**: STT v6(v5 는 12-15 종료), 세 참여자(반이중 걷음 · TokenGate · `audio_stop` · `playback_stopped`), 바로잡기, 시드 `.11`, 동시 상한 3.
- 시안은 그리지 않았다(사용자 「새로 만드는 건 거의 없잖아」). 기존 앱 컴포넌트에 웹 배치와 글자를 썼고, 캡처로 확인했다.

## 2. 적용한 기술·개념

- **옛 클라이언트 호환을 버리는 판단 — 쓰는 사람이 0이면 버전 가르기가 비용만** → [[tolerant-reader]]
  - 조사에서 「깔린 옛 앱 + 새 서버」 깨질 곳 15곳이 나왔다. 처음 추천은 앱 버전 칸으로 옛/새를 가르는 것이었다.
  - 사용자: 「1차라 아무도 안 써 · 이걸로 인계」. 그래서 가르기를 통째로 뺐다(M-2). 로그인 응답 · 알림 종류 · 통역 프로토콜을 새 앱 기준으로 바로 바꿨다.
  - 대신 출시 순서가 계약이 됐다. **prod 서버 먼저 → 정식 앱**이다. 반이중을 걷은 새 앱이 옛 통역 서버에 붙으면 재생 소리가 자막으로 되울린다(검수 W-16).
  - 근거: `research-current-state.md` A2 · SPEC-003 개정 ⑲ ①②
- **「닫힐 때만」 알림 — 일부 변경은 조용히, 끝났을 때 한 번** → [[apns-direct-push]] · [[notification-coalescing]]
  - 호출 취소는 줄 단위다. 본문에서 시술 수를 빼자(사용자) 「3줄 중 1줄 취소」에도 「호출 취소」가 가서 원장이 전체 취소로 읽을 수 있게 됐다(검수 R-3).
  - 결론: 호출이 완전히 닫힐 때만 한 번 보낸다. 일부 취소는 알림이 없다.
  - 이어서 OS 알림 센터에 남는 원래 푸시를 지우려고 했다. 앱이 꺼져 있으면 지울 수 없어서 **서버가 같은 묶음 id 를 붙였다**: APNs `apns-collapse-id`=callId, Android 알림 tag = data.callId. 그러자 같은 id 때문에 iOS 앱이 취소 알림 자신까지 지울 수 있게 됐다(푸시 검수 W-1). 묶음은 서버 · 앱이 함께 정해야 한다.
- **늦게 도는 비동기 작업은 보내기 직전에 다시 읽는다** → [[idempotency]]
  - 원장 호출 푸시 워커 태스크가 취소 뒤에 돌면, 이미 닫힌 호출로 푸시와 안 읽은 행을 만들 수 있었다(P3 검수 ①).
  - 고침: 보내기 · 행 쓰기 직전에 호출을 다시 읽고, 닫혔으면 건너뛴다. 경쟁 시험 2.
- **외부 API 오류는 뜻으로 가른다 — FCM `INVALID_ARGUMENT`** → [[external-api-error-classification]]
  - 처음 구현은 `INVALID_ARGUMENT` 전부를 죽은 토큰으로 봤다. 그러면 본문 오류 하나로 Android 기기 결속이 대량으로 풀린다(F1 검수 W-1).
  - 실물 1회(validate_only · 가짜 토큰)로 모양을 확인했다: 토큰 오류는 `fieldViolations` field=`message.token` 이다. 그때만 `token_removed`, 나머지는 실패로 두고 결속을 유지한다.
- **비밀값 배선은 목록 전부 — 하나 빠지면 조용히 꺼진다** → [[contract-surface-enumeration]]
  - FCM 키를 Key Vault 이름 · 배포 OPTIONAL_SECRETS 에만 넣고 끝났다고 봤다. 검수가 금지 목록 · 로컬 가드 · 예시 env · compose · 배포 문서에도 없다고 짚었다(F1 FAIL-1). 하나라도 빠지면 Android 푸시가 오류 없이 skipped 로 꺼진다.
  - release Android 빌드는 Firebase 설정이 없으면 실패하게 바꿨다. 푸시 없는 정식 앱이 조용히 나가는 것을 막는다.
- **통역 엔진 이식 — 원천 버전을 정본으로 고정하고 커밋 차이만 옮긴다** → [[websocket-relay]]
  - DAY 통역은 11-11 통키 `17c26b5` 를 옮긴 것이었다. 사용자: 「통역 엔진은 통키가 최신본」. `git log 17c26b5..56e43a0` 5커밋을 항목 표로 만들어 옮겼다. records(D-42) 계열만 뺐다.
  - 바로잡기(`correct.py`)가 records 함수 4개를 import 했다. 함수만 떼어 `matching.py` 로 옮겼다.
  - 시드 `.11` 은 DAY 로더가 모르는 칸(`proper` · `wrong`) 때문에 거절됐다. 칸을 넓히고 검사 8 도 함께 가져왔다.
  - 동작 같음은 검수가 AST 정규화 diff 로 확인했다. 통키 경쟁 · 시간 초과 시험 15건은 따로 옮겼다(코드 무수정 통과).
  - Soniox 조직 TTS 한도 3 을 통키와 함께 쓴다. 세 참여자는 세션 내내 TTS 하나를 쥔다 → DAY 상한 3(사용자 · 한도 상향은 사용자 몫).
- **같은 테이블에 두 세션의 migration — 번호는 머지 순서가 정한다** → [[database-migration]] · [[online-schema-change]]
  - 다른 세션(`day-cc-mig`)도 `0012` 를 0011 뒤에 붙였다. 우리 것은 enum 값 추가뿐이라, 저쪽이 dev 에 먼저 들어간 뒤 rebase 해 0013 · 0014 로 옮겼다. 중간 커밋은 잠깐 head 가 둘이고 마지막 커밋이 닫는다.
  - enum 값 추가는 되돌리기가 어렵다. 0013 이전 이미지로 되돌리면 알림 목록이 500 이라, 되돌릴 때 migration 도 함께 내린다(배포 메모).

## 3. 막혔던 것 / 사고

- **코디가 확인 없이 틀린 말을 두 번 했다.**
  - 「앱 로그아웃 때 KOS 세션도 끊는다」 → 해제 API 가 비밀번호를 요구한다. 11-17 에 이미 「로그아웃 때 해제 안 함」으로 정해져 있었다. 조사 리포트 B3 를 읽고 정정했다.
  - 「호출 취소 알림이 웹 알림 목록 · 종 배지에도 뜬다」 → 웹에는 목록 · 종 화면 자체가 없다(`day.js` OS 알림만). planner 가 OQ-N19 로 짚어 정정했다.
  - → 상태는 열어 보고 말한다(기억 verify-before-claiming 재발).
- **스펙 검수가 세 번 돌았다.** 1차 FAIL 5 의 원인은 모두 「옛 판 문장을 취소선 없이 남김」(규칙 38 알림 없음 · 앱 401) 아니면 「웹에 없는 글자를 웹 글자라 함」(확인 창)이었다. 2 · 3차는 개정이 만든 새 잔재(`migration 없음` · 「취소 횟수만큼」)였다. 개정 때마다 반대 문장을 grep 으로 전수하는 게 검수보다 싸다.
- **Delivery 재결속이 머지 전 baseline 을 거절했다.** `start-delivery` 는 baseline = fetched origin/main 만 받는다(`workflow.py:917`). 다른 스펙 작업(#954)이 같은 `spec-000` · `log.md` 를 고치는 중이라 머지를 미뤘다. 그래서 「코드 먼저 · 승인 뒤」로 순서를 바꿨다(사용자 B).
- **orca CLI 가 바뀌어 첫 발주가 실패했다.** `task-create` 가 `run_required` 로 거절했다. `run-create` → `worker-start --spec/--terminal` 로 바꿨다. 수동으로 만든 터미널은 `--terminal` 로 붙였다.
- **워커가 allowed_paths 밖 질문을 일곱 번 했다**(dtos 2 · tasks · notification_cancel · devices 라우터 · taut.toml · configuration.py). 브리프가 「바꿀 파일」을 기능 폴더로만 적었다. 계약을 바꾸는 작업은 dtos · schemas · 라우터 · 배포 목록까지 열어 두는 게 맞다.
- **캡처 하네스가 그림자를 꺼 메뉴가 검은 상자로 찍혔다.** 코디가 화면 이상으로 짚었고, 검수가 렌더 탓임을 확인했다. 캡처는 실제 렌더 옵션으로 찍어야 화면 판단에 쓸 수 있다.
- **원장 변경 창에 웹에 없는 「호출할 시술 · 1개」 칸**이 들어갔다(M2 FAIL). 워커는 웹 출처라고 적었지만 다른 레이아웃의 줄이었다. 「글자 출처 파일:줄」을 리포트에 쓰게 해 둔 덕에 검수가 바로 잡았다.
- **디스크가 꽉 찼다**(남은 0.3GB · Android 빌드 ENOSPC). 사용자가 정리해 26GB 를 확보했다.
- **dev 배포 1차가 체크 단계에서 취소됐다.** 다른 세션(`day-cc-mig`)이 dev 에서 업데이트를 돌리던 중이라 그쪽에서 멈췄다(그 회고 §2). 코디가 보낸 cancel 은 거절돼 실행되지 않았다. 사용자 「배포 하자」로 2차 rerun → 성공 · `0014 (head)`. dev 는 여러 작업이 같이 머지 · 배포하는 곳이라, 머지 전에 다른 세션의 긴 실행을 먼저 확인해야 한다.

## 4. 결정

| 날짜 | 결정 | 왜 |
|---|---|---|
| 2026-11-20 | 범위 4: 기기 선택 · 시술 현황 · 호출 취소 알림 · 통역 통키 최신 | 사용자 |
| 2026-11-20 | 출시 = DAY Dev 먼저 → 실기기 → 같은 코드로 정식 · 0.2.0 | 사용자 |
| 2026-11-20 | **옛 앱 호환 안 챙김**(1차 · 사용자 없음 · 인계 판) | 사용자 |
| 2026-11-20 | 통역 엔진 정본 = 통키 `56e43a0` · records 만 빼고 따라감 | 사용자 |
| 2026-11-20 | 시술 현황 앱: 넣음 = 바로 시작 · 호출 취소 · 간호관리 · 방 옮기기 · 복귀 · 원장 바꾸기 / 뺌 = 귀가 대기 취소 · 정렬 · 순서 | 사용자 |
| 2026-11-20 | 호출 취소 알림 `doctor_call_cancel` · 「호출 취소」 / 「{방} · 호출 취소」 · 호출이 닫힐 때만 · 웹 = OS 알림만 | 사용자(추천) |
| 2026-11-20 | Android FCM 이번에 · Firebase 는 사용자 · 키 dev/prod 둘 | 사용자 |
| 2026-11-20 | 시안 없이 코드 · 바로 시작 = 의사 호출 드로어 재사용 | 사용자 |
| 2026-11-20 | 통역 동시 상한 3 · 한도 상향은 사용자 | 사용자 |
| 2026-11-20 | 통역 재생 중 안내 줄 지움 · 「번역 읽는 중」 · 대리 수락 「호출할 시술」 그대로 | 사용자(추천) |
| 2026-11-20 | 푸시 묶음 = iOS `apns-collapse-id` · Android tag = callId · 새 칸 없음 | 코디 |
| 2026-11-20 | 머지 · 승인 전에 코드 먼저 → dev 스쿼시 머지 · dev 배포 · DAY Dev 업로드 | 사용자 |
| 2026-11-22 | 스펙 #955 코디 머지 · 마감 범위 = dev + TestFlight · internal | 사용자 |

## 5. 날짜별 로그

- `2026-11-20` 착수 · 현황 조사(정할 것 18) · 범위 결정 · 스펙(planner) · 문서 검수 3회 · PR #955 · 코드 P1 통역 · P2 API · P3 알림 · F1 FCM · M1 ~ M5 앱 · 단계마다 코드 검수 · rebase(0013 · 0014) · #266 dev 스쿼시 머지 · dev 배포(1차 취소 · 2차 성공) · Key Vault dev FCM · DAY Dev 0.2.0 업로드
- `2026-11-22` 스펙 rebase · 구현 동기화 · #955 머지 · Delivery #262 · #263 v2 재결속 · 검수 WARN · 승인 · 회고 · 개념 · 아카이브

## 6. 산출물

프로젝트와 당시 작업 문서는 `sync-work-links.py`가 만드는 작업 목차로 연결한다.

- code PR: https://github.com/MediSolveAIDev/CENTURION_DAY/pull/266 (dev `5ece25ea`)
- spec PR: https://github.com/MediSolveAIDev/mediness/pull/955 (main `3ae2317e`)
- Delivery: https://github.com/MediSolveAIDev/CENTURION_DAY/issues/262 · https://github.com/MediSolveAIDev/CENTURION_DAY/issues/263
- 리포트(이 작업 폴더): 조사 `research-current-state.md` · 스펙 `spec-report.md` ~ `spec-8-report.md` · 문서 검수 `review-doc-1` ~ `4` · 코드 `be-*` · `mobile-*` · 코드 검수 `review-code-*` · 캡처 `shots/`
- 앱 산출물(레포 밖): `~/.config/day/android/out/DAY-Dev-0.2.0-4.aab`

## 7. 잔여

- **실기기 확인**(사용자): DAY Dev 0.2.0 — 기기 선택 · 시술 현황 5동작 · 호출 취소 알림(원래 알림 덮기) · 통역(재생 중 말하기 · 끼어들기 · 메아리 I-6) · Android 푸시(F3 · 상태 바 아이콘). 실 KOS 앱 로그인 기기 제한도 여기서.
- **prod**: prod 서버 먼저 — `5ece25ea` 로 ff → migrate-prod(0012 · 0013 · 0014 함께 · dev 성공 이력 조건) → deploy-prod → prod Key Vault `day-prod-fcm-service-account`(한 줄 JSON) → worker 같이. 그 뒤 정식 0.2.0(iOS 3 · Android 4 · release 는 Firebase 설정 필수).
- **Delivery #262 · #263**: v2 승인됨(2026-11-22 · 검수 WARN 3 — #262 Non-Goals 「Firebase 준비」 잔재 · 실행 표 「시작:」 빠져 직렬로 보임 · #263 롤백에 0014 경고 없음 — 닫을 때 댓글로 정정) · 실기기 · prod 뒤 닫음.
- **Soniox 한도 상향**(사용자) → DAY 상한 다시 올림.
- 화면 판단값(시안 없음): 방 이름 ▾ · 점유 띠 모양 · 아이패드 팝오버 폭 · 원장 변경 창 두 칸(아이패드).
- iOS 배포 대상 경고(altool 90068 · 90725 — 2027-04 iOS 15 · Xcode 27).
