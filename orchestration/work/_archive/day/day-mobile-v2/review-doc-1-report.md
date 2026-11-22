# 리뷰 리포트 — day-mobile-v2 / doc 1차 (2026-11-20)

- 대상: mediness 워크트리 `day-mobile-v2-spec` 미커밋 diff(`products/day/` 8파일) · planner `spec-report.md` · Delivery CENTURION_DAY #262 · #263
- 대조: 결정 표 M-1 ~ M-9(spec 브리프 §1 · `_RESUME.md` §2) · CENTURION_DAY `origin/dev` `844eace4` · 통키 interpret-pwa `56e43a0`(+ decision-001 D-42 ~ D-71)
- 표기: `S1:` = spec-001-login-session.md · `S2:` = spec-002 · `S3:` = spec-003 · `S5:` = spec-005 · `dev:` = CENTURION_DAY 844eace4 · `tk:` = interpret-pwa 56e43a0 · `dec:` = 통키 decision-001
- 파일은 이 리포트 하나만 만들었다(워크트리 수정 · 커밋 · Issue 수정 없음).

## 판정: FAIL

FAIL 5 · WARN 14 · 사용자 확인 3. 결정 표 M-1 ~ M-9 는 빠짐 없이 들어갔다. 비밀값은 없고 lint 도 통과했다. 다만 아래 다섯 곳은 코드 워커가 그대로 지으면 틀린다. 「옛 판 규칙이 그대로 남아 새 계약과 맞서는 곳」이 둘, 「웹에 없는 글자를 웹 글자라고 한 곳」이 하나, 통역 서버 · 앱 동작이 빠진 곳이 둘이다.

---

## FAIL

### F-1. SPEC-002 규칙 38 · 케이스 매트릭스가 「호출 취소 알림 없음 · 원래 알림 그대로」를 그대로 말한다 — M-6 과 정면으로 어긋남
- `S2:1078` 규칙 38: 「**알림 행 · 웹 OS 알림 · 앱 푸시 없음 — 다음 스펙** …」 · 「**원래 원장 호출 알림 행 · 앱 푸시는 그대로**」. 취소선이나 개정 표시가 없다.
- 같은 내용이 개정 없이 남은 곳: `S2:233`(⋮ 설명) · `S2:282`(「알림 · 앱 푸시 없음」) · `S2:444`(시나리오 4) · `S2:749`(케이스 매트릭스 「알림 없음」).
- 개정 ㉕(`S2:43`)는 「업무 규칙 · 웹 화면 · KOS 쓰기는 바꾸지 않는다」라고만 했고, 알림 쪽은 SPEC-005 로 넘긴다는 안내도 없다.
- 결과: backend 가 SPEC-002 규칙 38 을 정본으로 읽으면 알림 훅을 넣지 않고 원래 알림도 닫지 않는다. 지금 코드의 docstring(`dev:backend/day/services/board_calls.py` `cancel_call` 「KOS 쓰기 · 알림 없음」)도 같은 말이라 그쪽으로 끌린다. M-6 「원래 원장 호출 알림은 닫는다」 · SPEC-005 `:265-280` 과 맞서는 두 정본이 생긴다.
- 고칠 것: 규칙 38 · `:233 · :282 · :444 · :749` 의 알림 문장에 취소선을 긋고 「→ 2026-11-20 개정 ㉕/SPEC-005 — 호출 취소 알림 행 · 원래 알림 닫기(OQ-N17)」로 바꾼다. 「원래 알림 그대로」 문장도 OQ-N17 기본값에 맞춘다.

### F-2. SPEC-003 U-19 「확인 창: 웹과 같은 확인 창 글자」 — 웹에는 호출 취소 확인 창이 없다(M-9)
- `S3:491`: 「확인 창: 웹과 같은 확인 창 글자(… `board_parts.html` 호출 취소 확인 — 글자는 웹 그대로)」.
- 코드 사실: `dev:backend/day/templates/partials/board_parts.html:123` 의 「호출 취소」는 `ui.menu_row(..., action=…/cancel-call)`, 곧 바로 보내는 버튼이다. `confirm_modal` · `data-day-open-dialog` 가 없다(시작 취소 · 완료 취소 `:127-131` 만 확인 창이 있음).
- 스펙 근거도 같다: `S2:282` 「**확인 창 없음 · 성공 토스트 없음** — 확인 창 글자가 사용자 말에 없어 짓지 않음」 · `S2:1168` OQ-67 ⓓ.
- 결과: 원천에 없는 확인 창 제목 · 버튼 글자를 mobile · designer 가 지어야 한다(M-9 위반). Delivery #262 완료 조건 A3 「호출 취소(canCancelCall · **확인 창**)」에도 그대로 옮겨졌다.
- 고칠 것: U-19 = 「확인 창 없음(웹 · OQ-67 ⓓ와 같음)」. #262 A3 도 v2 재결속 때 맞춘다.

### F-3. 통역 세 참여자 — D-68 규칙 ③(재생 중 재생 언어 토큰 버리기 · TokenGate)이 빠졌고, 「메아리 꼬리 500 ms」를 agent text 쪽으로 잘못 붙였다
- `S3:821`: 「자기 목소리는 Soniox agent text(재생 중인 글을 0.7초 앞서 보냄 · 메아리 꼬리 500 ms)로 지움」.
- 통키 사실:
  - 500 ms 는 재생 구간 판정의 꼬리다(`tk:back/app/service/interpret/turn.py:24` `ECHO_TAIL_MS` · 사용처 `:89` · dec D-70 ②).
  - 이 판정으로 `TokenGate` 가 조립기 **앞에서** 재생 언어 토큰을 버리고(`tk:…/session.py:368-376` `_gate.filter` → `DROP`), 남은 원문이 없는 발화는 통째로 버린다(`asm.drop_open()`).
  - agent text 는 보조 수단이다(dec D-68 「규칙 ③ 언어 걸러내기는 뒷받침」).
- 결과: SPEC 대로 agent text 만 지으면, 반이중을 걷은 앱에서 스피커 소리가 다시 자막 · 번역으로 들어오는 되울림이 남는다. `S3:825` I-6 이 「서버 agent text 로 충분한가」를 실기기 확인으로 미뤄 두었는데, 그 전제부터 틀렸다.
- 고칠 것: 「세 참여자」 행에 ③ 재생 구간(+500 ms) 동안 재생 언어 토큰 버림(TokenGate · 조립기 앞) · 원문 없는 발화 버림을 넣는다. agent text 는 보조로 적는다.

### F-4. 통역 — D-48 「이미 보인 말풍선 지우기」 프레임이 빠짐 → 지금 DAY 앱은 빈 말풍선을 그린다
- `S3:817`: 「원문이 비었거나 문장부호뿐이면 caption · TTS 를 보내지 않음」.
- 통키 사실: 이미 화면에 나간 말풍선이면 서버가 **같은 id 로 `{"type":"caption", "original":"", "translation":"", "final":true}`**를 보낸다(`tk:…/session.py:414-421` 「이미 보인 말풍선 — 둘 다 빈 final 1번으로 지운다(front 는 빈 말풍선을 그리지 않는다)」). F-3 의 `drop_open` 도 같은 프레임을 낸다(`:373-376`).
- DAY 앱 사실: `dev:app/lib/state/interpret_controller.dart:162-169` 는 같은 key 면 그대로 바꿔 끼운다 → 빈 말풍선이 남는다. 닫을 때 요약 「N문장」에도 셀 수 있다(같은 파일 「마지막 통역 · N문장」 셈 · 서브 조사 `:218`).
- 고칠 것: 서버 → 앱 프레임 표에 「빈 final caption = 그 말풍선 지움 · 문장 셈 제외」를 넣는다(mobile P5 범위).

### F-5. (판정 근거 겹침 정리) SPEC-001 안에 옛 판 규칙이 개정 표시 없이 남아 「앱 = 401 `invalid_credentials`」를 계속 말한다
- 개정 ⑩(`S1:48`)은 보충 ① · ④ · OQ-K17 · 규칙 9 를 뒤집는다고 적었다. 그런데 아래 줄은 취소선 · 「→ 개정 ⑩」 표시가 없다.
  - `S1:90` U-1 기대 결과: 「앱은 지금과 같은 오류 401 `invalid_credentials`」
  - `S1:125` 웹 API 표 `/login/device`: 「앱 JSON 짝 없음 — 보충 ①」
  - `S1:247` §3 단계 6: 「**앱**(`POST /api/auth/login`)이면 2 이하가 없다 — 목록을 받지 않고 … 401 `invalid_credentials`」. 규칙 본문이다.
  - `S1:617` OQ-K3: 「… 웹만」
  - `S1:621` **OQ-K7 행**: 「닫음 — 앱 JSON 은 `choose_device` 를 주지 않는다 … 지금 코드 그대로」. 개정 ⑩ ④는 「OQ-K7 다시 엶 → 닫음(넘긴다)」라고 했는데, OQ 표는 반대 값으로 닫혀 있다.
- 결과: 데모 넘김(`adapters/environments.py` `read_success`)을 고칠지가 OQ 표와 개정 문단에서 서로 반대다. 「닫힌 것을 반대 값으로 다시 닫은 곳」이 표에 반영되지 않았다.
- 고칠 것: 위 다섯 줄에 개정 ⑩ 표시를 단다. OQ-K7 행은 「다시 닫음(개정 ⑩) — dev `choose_device` 를 prod 가 넘긴다 · `read_success` 고침」으로 바꾼다.

---

## WARN

### 계약 · 코드 사실
- **W-1. `canChangeDoctor` 판정이 안에서 두 갈래다**(`S2:43` ③ · `S2:672` · OQ-78 `S2:1167`)
  - 스펙은 「웹 조건 `(doctor 또는 systemDoctor) 이고 state ∈ accepted · doing`」과 「판정 = `task_not_assignable` 이 안 걸림」을 같은 것으로 적었다.
  - 서비스 판정 `dev:backend/day/policies/board_rules.py:264-270` `doctor_change_block` 은 `visit_home` · 상태만 보고, 담당의 · systemDoctor 유무는 보지 않는다. 웹 템플릿 `board_parts.html:83 · :134` 만 `(t.doctor or t.systemDoctor)` 를 본다.
  - `canCancelCall` 도 같다: 웹 `:122` 는 `state == "called" and t.call` 이고, 서비스 `:641-653` 은 그 호출이 수락됐으면 막는다.
  - OQ-78 「다르면 서비스가 정본」과 #262 A2 「웹 템플릿 조건과 일치」가 서로 다른 시험을 요구한다. OQ-78 기본값에 둘 중 어느 쪽인지 한 줄로 못박을 것.
- **W-2. 방 옮기기 목록 규칙이 빠졌다**(`S3:505` 「방 목록 = 스냅샷 `rooms[]`(서버 순서 · 배정됨 표시)」)
  - 코드 사실: 서버 `rooms[]` 는 그 병원 방 전부이고 `takenBy` 에 이 카드도 들어 있다. 「화면은 옮기는 카드 자신을 `takenBy` 에서 빼고 다시 묶는다」(`dev:backend/day/presentation/board.py:70-79`).
  - 웹은 지금 방을 빼고, 자신을 뺀 `takenBy` 로 비어 있음/배정됨 · 빈 방 먼저로 다시 묶는다(`board_parts.html:283-293`).
  - 그대로면 앱은 지금 방을 보이고, 자기 방을 「배정됨」으로 그린다. U-21 에 이 세 규칙을 적을 것.
- **W-3. 점유 이동 뒤 앱 표시가 없다.** U-21 은 「점유 이동」을 넣었는데, 웹의 점유 띠(`holdRoom` · `board_parts.html:174-178`)를 앱 카드 · 룸 상세에 그리는지 정하지 않았다. OQ-A55(복귀)와 같이 묶어 사용자에게 물을 것.
- **W-4. 기기 등록 API 표 `S3:589` 「`push_env` 선택」.** FCM 표(`S3:703`)는 「`android` 에선 보내지 않음(보내면 400)」이고 `ios` 는 필수 그대로다(`dev:backend/day/schemas/devices.py:33-35` `Literal` 필수). 「선택」은 「플랫폼별(ios 필수 · android 금지)」로 고칠 것.
  - 덧붙여 잠금 키가 `push_env.value` 를 쓴다(`dev:backend/day/services/devices.py:113`). android(null)에서 바뀌는 자리라는 것을 SPEC-000 device 규칙 「방법은 WP」 옆에 한 줄 남기면 좋다.
- **W-5. SPEC-002 OQ-67 행(`S2:1168`) ⓔ 「이번엔 웹만」이 그대로다.** 개정 ㉕ ②는 「OQ-67 ⓔ 닫음」이라고 했다.

### 알림(M-6)
- **W-6. {N} 기본값(OQ-N16 「이번에 빠진 수」)이면 늘 「시술 1건」이다**
  - 호출 취소는 줄 하나 단위다(`S2:282` · `dev:…/board_calls.py` `cancel_call` 은 `task_id` 하나).
  - 그래서 3줄 호출을 하나씩 취소하면 「시술 1건 · 호출 취소」 알림이 세 번 온다. OQ-N17 기본값(호출이 닫힐 때만 원래 알림 닫음)과 겹치면, 원래 알림은 마지막까지 열려 있고 취소 알림만 쌓인다.
  - 사용자에게 「원장 호출과 같은 꼴」의 N 이 무엇인지 예시와 함께 물을 것(막는 OQ 표에는 이미 있다).
- **W-7. 원래 알림 닫기의 범위가 빠진 곳.**
  - (a) 웹 OS 알림 쪽 원래 호출 알림을 닫는지(웹 `tag = 행 id` · `dev:backend/day/static/day.js:1824-1834`)가 OQ-N17 ①②에 없다.
  - (b) 취소가 「그 줄이 든 **열린 호출 전부**」에서 줄을 뺀다(`S2:1078` · `board_calls.py` `open_ids`). 그런데 받는 계정 · 닫는 알림은 유효 호출 하나만 본다(`S5:272`). 재호출 사슬의 앞 호출 알림을 어떻게 할지 OQ-N17 에 한 줄 더할 것.
- **W-8. OQ-N19 는 코드 사실과 맞다.** 웹에는 알림 목록 · 종 화면이 없고, `day.js:1834` `NOTIFY_KIND = "doctor_call"` OS 알림만 있다(routers 에 웹 알림 화면 없음 · `routers/api/notifications.py` 뿐). 다만 결정 표 글자와 다르므로 아래 「사용자 확인」 U-1 로 올린다. 비차단 판정은 맞다.

### 통역(M-8) — 서브 조사로 통키 56e43a0 대조
- **W-9. D-45 구현 모양이 빠졌다.** Soniox context 에 새 `text` 키(영문 4문장 · 키 순서 general → text → terms)가 생겼다(`tk:back/app/service/interpret/glossary.py:43` `to_soniox`). `invalid_request` 로 다시 연결할 때도 `text` 를 유지하고(`:331-334`), 정리 순서는 `TRIM_ORDER=("terms","reverse")`(`:272`)다. 위 절의 「정방향 기본만」 문장(`S3:760` 근처)과 어긋난다.
- **W-10. 근거 번호.** `S3:818` 사전 context 의 근거 D-54 는 「별칭 빼기」 결정이다(dec:110). 내용 근거는 D-56 · D-71 이다.
- **W-11. 「바뀌지 않는 것」(`S3:827`)에 바뀐 것이 섞였다.**
  - `stop` 이 이제 읽을 큐를 비워 남은 번역을 읽지 않는다(`tk:…/session.py:353`) → 「drain」이 바뀌었다.
  - TTS 설정에 `return_timestamps: true`(`tk:…/soniox.py:91`)와 cancel 메시지 `{stream_id, cancel:true}`(`:210`)가 생겼다. 모델 `tts-rt-v2` 는 그대로다.
- **W-12. 프레임 세부.**
  - `audio_stop.id` 는 `_last_start` 라 이전 차례 id · `null` 일 수 있다(`session.py:442 · :525`). 앱은 id 를 보지 말고 멈추면 된다(통키 front 도 무시 · `interpret.ts:187`).
  - `playback_stopped` 를 받으면 서버가 `{"type":"audio_end","id"}` 를 보낸다(`session.py:527`). 이 응답이 `S3:823` 에 없다.
- **W-13. 앱 PCM 조각 버리기 범위 · OQ-A61 기본값.**
  - 통키 front 는 멈춤 · 닫기 · 오류 · `audio_stop` **모든** 경로에서 다음 `audio_start` 까지 PCM 을 버린다. SPEC(`S3:824`)은 `audio_stop` 때만 버린다고 적었다.
  - 통키가 `playback_stopped` 를 보내는 조작은 `pause`(`interpret.ts:291`) · `clearPlayback`(`:306`)뿐이다. `close()`(언어 바꿈 포함)는 보내지 않는다(`:250 · :317-324`). 그러니 OQ-A61 기본값(`S3:1164` 「드로어 닫기 · 언어 바꿈 · 다시 연결 — 통키 front 와 같은 뜻」)은 사실과 다르다.
  - 통키는 출력 구간(+400 ms) 표시를 판정용으로 남긴다(`interpret.ts:252`). SPEC 은 400 ms 를 「없앰」으로만 적었다.
- **W-14. 시드 `.11` 세부.**
  - 시드 버전은 `2026-11-16.11` · term 170 · `proper:true` 74 · entry `wrong` 18개(47꼴)다. **`ko_wrong` 은 시드에 0건**이다(코드만 허용).
  - 로더는 칸만 넓히면 안 된다. 통키의 `proper` bool 검사 · 검사 8 `wrong_form`(`tk:…/glossary.py:173-175`)과 `correct.py` 가 가져오는 `glossary.wrong_key`(DAY 에 없음 · `correct.py:14-16`)도 같이 와야 한다. 바로잡기 행 「records 함수 4개만」에 덧붙일 것.
  - records 4함수는 DB · 파일 없이 같은 파일 `_squeeze · _is_word · _SIMPLIFY` 와 `to_simplified` 에만 기댄다 → 「함수만 가져옴」은 된다(OK).

### WP · Delivery · 출시
- **W-15. #262 실행 단계가 전부 「앞 단계 완료」로 한 줄로 이어졌다**(Issue 실행 정보 표 1 ~ 7).
  - spec-report 의 의존 표(designer P4 = 스펙 머지 · A55 뒤, mobile P5 = P1 뒤)와 다르다. 이대로면 designer 가 backend 알림(P3) 끝을 기다리고, 통역 앱(P5)이 시안(P4)을 기다린다.
  - 통역은 12-15 마감이 있어 P1 → P5 를 따로 앞당길 수 있어야 한다. v2 재결속 때 「시작 조건」을 의존 표대로 고칠 것.
  - #262 는 `spec-baseline:ready` 라벨이지만 baseline 은 옛 계약 `ccede286` 이다. planner 도 적었다(재결속 전에는 승인하지 말 것).
- **W-16. 서버 · 앱 배포 순서가 없다(M-2 의 반대편 — 새 앱이 깨질 자리).**
  - 반이중을 걷은 0.2.0 앱이 **옛 통역 서버**(TokenGate · agent text 없음)에 붙으면, 재생 소리가 마이크로 다시 들어가 자막 · 번역 되울림이 생긴다. 바로 시작 경로도 404 다.
  - 정식 0.2.0 출시 전에 prod 서버 배포를 끝내야 한다는 순서가 SPEC-003 개정 ⑲ ① · mobile-deployment ⑤ 에 없다. #262 되돌리기는 「서버 revert 시 0.2.0 앱 새 경로 404」만 적었는데, 통역 되울림은 빠졌다.
  - P7 에 「prod 서버 먼저 → 정식 앱」을 명시할 것.
- **W-17. 빠진 일(WP 표).**
  - (a) 웹 쪽 일: `day.js` NOTIFY_KIND 확장(P3 에 있음 OK).
  - (b) SPEC-002 개정 표시 정리(F-1)는 스펙 일이다.
  - (c) 방 복귀(A55)가 「넣음」이면 designer 시안 · P6 범위가 는다. 시안 5자리 표의 「방 옮기기」 칸에 「(복귀)」가 이미 있다(OK).
  - (d) 앱 「서버 계산 값만」 규칙의 예외로 방 목록 재묶음(W-2)을 P6 에 적을 것.

---

## 사용자 확인 (결정 표와 코드 사실이 갈리는 곳 · FAIL 아님)

- **U-1. M-6 「웹 알림 목록 · 종 배지」.**
  - 웹에는 원장 호출의 목록 · 종 화면 자체가 없다(`dev:backend/day/static/day.js:1824-1834` — OS 알림만 · `routers/` 에 웹 알림 화면 없음).
  - planner 는 OQ-N19(`S5:461`)로 「웹 OS 알림만」을 기본값으로 두었다. `_RESUME.md` §1 정정과 같은 해석이지만, §2 결정 행 · spec 브리프 M-6 글자는 아직 「목록 · 종 배지 · OS 알림」이다.
  - 웹 목록 · 종 화면을 새로 만든다는 뜻이면 범위 · 시안이 커진다. 사용자 답을 받고 결정 표 글자를 고칠 것.
- **U-2. OQ-A55 방 복귀 + 점유 띠 표시(W-3).** M-4 넣음 목록에 없다. 점유 이동만 넣으면 앱에서 돌아올 길이 없다(planner 기본값 = 넣음).
- **U-3. {N} 의 뜻(W-6).** 「원장 호출과 같은 꼴」이 그 호출의 처음 시술 수인지, 이번에 빠진 수(늘 1)인지.

## 결정 표 M-1 ~ M-9 대조 요약

| # | 판정 | 메모 |
|---|---|---|
| M-1 | PASS | 0.2.0 · Dev 먼저 · 빌드 번호 iOS Dev 4 · 정식 3 · Android 4 · 심사 건 그대로(mobile-deployment ⑤ · §10). 배포 순서는 W-16 |
| M-2 | PASS(+W-16) | 버전 가르기 장치 없음(OQ-K14 닫음 · 서버 분기 0). 새 앱이 깨질 자리는 W-16 |
| M-3 | FAIL(F-5) | 계약은 맞음 — `auth.login(device_choice=True)` · `choose_device` · `dtos/auth.py` · `read_success`(`adapters/environments.py:184-213`) 사실 일치 · 글자 = `login_card.html` · 첫 항목 선택 = `loop.first checked` 일치 · 로그아웃 해제 안 함. 옛 판 줄이 남음 |
| M-4 | PASS | 넣음 5 · 뺌 3 반영. 복귀는 OQ-A55(U-2) |
| M-5 | PASS(+W-1 · W-2) | quick-start 응답 모양 = `board_quick_start.py:37-134` 그대로(`systemDoctorTaskIds` 는 event_log 만 — 일치) · cancel-call `{ok}`(`TaskActionResponseData`) · room-move 본문 `{mode, roomId}` 일치 |
| M-6 | FAIL(F-1) | SPEC-005 새 절은 결정 표대로. SPEC-002 규칙 38 이 반대로 남음 |
| M-7 | PASS | 칸 이름 · 위치만 · Firebase 값 없음 · FCM 별도 Delivery #263 |
| M-8 | FAIL(F-3 · F-4) | 상수(v6 · 2000/-0.3 · 1.0s · 2토큰 · 0.7s · 3s · ×0.96 · 74/170)는 통키 코드와 일치. 날짜 D-43 「v5 는 2026-12-15 제거」 일치 · records(D-42) · D-36 제외 OK. 빠진 동작 2 |
| M-9 | FAIL(F-2) | 나머지 글자(KOS 기기 선택 · 「바로 시작 · N건」 · 「간호관리」 · 「점유 이동」/「이동」 · 「비어 있음」/「배정됨」 · 「원장 변경」)는 웹에 있음을 확인. 성공 토스트 · FCM 채널 이름은 「미정」(OK) |

## 착수 막는 OQ 표 점검

- 표(spec-report · `S3:1152-1166` · SPEC-001/002/005 OQ 표) 사이 서로 어긋남: 없음.
- 빠진 막는 것:
  - (1) `canChangeDoctor` · `canCancelCall` 의 정본(W-1 — OQ-78 기본값에 못박기)
  - (2) 통역 서버 TokenGate · 빈 final 지우기(F-3 · F-4 — OQ 가 아니라 계약 보충)
  - (3) 서버 → 정식 앱 배포 순서(W-16)
- 막지 않는데 막는다고 한 것: 없음. OQ-A61 은 통키 front 코드로 답이 나오므로 사실상 계약 보충이다(W-13).

## 직원이 실물에서 만날 자리

- 3줄 호출을 하나씩 취소하면 원장 폰에 「시술 1건 · 호출 취소」가 세 번 오고, 원래 호출 알림은 마지막 취소 때까지 남는다(W-6 · OQ-N16/N17 기본값).
- 통역 중 폰 스피커 소리가 다시 자막으로 들어온다 — TokenGate 없이 agent text 만 지으면(F-3), 또는 정식 앱이 옛 prod 서버에 먼저 붙으면(W-16).
- 통역 자막에 빈 말풍선이 남고, 닫은 뒤 「N문장」이 실제보다 많다(F-4).
- 방 옮기기 목록에 지금 방이 보이거나 자기 방이 「배정됨」으로 나온다(W-2).
- 점유 이동 뒤 앱에서 원래 방으로 돌아올 수 없다(A55 · W-3).
- 데모 계정(심사용) 기기 선택 제출이 최장 60초로 넘김 60초와 겹쳐 `environment_unavailable` 이 날 수 있다(OQ-K19 — 알고 감수).

## 참고(기존 부채 · 확인 안 됨)

- Soniox TTS 연결은 **세션 내내 하나를 쥔다**(`tk:…/session.py:201` 세션 시작 때 한 번 열고 · cancel 뒤에도 재사용). 조직 TTS 한도 3 vs DAY 상한 6(I-1)은 0.2.0 뒤에도 그대로 실제 위험이다.
- iOS 정식 0.1.0 (2) 심사 중에 0.2.0 정식 심사를 낼 때의 Apple 절차는 공식 문서와 대조하지 않았다(조사 F-2 그대로).
- `log.md` 2026-11-20 행의 PR 칸이 「근거 …(PR 전 · 코디가 PR)」다. PR 번호를 받은 뒤 바꿀 것(규칙: 모호한 단어만으로 채우지 않음).
- `mobile-deployment.md` 의 Android 앱 id 두 개는 origin/main 에 이미 27회 나오는 값이라 새 노출이 아니다.

## 검증

- `python3 scripts/lint-pipeline.py --strict` → **0 error, 263 warning · exit 0** · `products/day/` 줄 **0**(ERROR · WARN 모두). 263 WARN 은 다른 제품(selly 등)이라 무관.
- 비밀값 grep(diff `+` 줄: 이메일 · IPv4 · `AIza` · private_key · azure) → 0건.
- 코드 대조 ref: CENTURION_DAY HEAD = `844eace4`(origin/dev 일치) · interpret-pwa `56e43a0`(`git show`). 테스트는 실행하지 않았다(read-only).
