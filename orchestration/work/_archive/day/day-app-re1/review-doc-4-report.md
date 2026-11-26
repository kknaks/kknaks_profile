# 리뷰 리포트 — day-app-re1 / doc · review-doc-4 · planner-fix-3 재검수 (2026-11-25)

- 대상: 워크트리 `day-app-re1-spec` 커밋 `22f7c30f..HEAD`(= `8195c0a8` 한 개) · `products/day/` 8 파일 +55 −43
- 대조 기준: `review-doc-3-report.md`(W1 ~ W13 · U1 ~ U5) · `planner-fix-3-instructions.md` · `planner-fix-3-report.md` · `_RESUME.md` §2 「review-doc-3 U1」 · 「U2 · U3 · U4 기본값」 행(:69 · :70)
- 원천 확인(read-only): CENTURION_DAY `96036397`(`queries/reservation_treatments.py:52-67` · `services/reservation_care_writes.py:330-339 · :431-446` · `emr/kos/client.py:245-263` · `routers/api/ext_peer.py:32-41` · `docs/development/deployment.md:200-201` · `models/reception.py:85-99`) · cc-prototype `0553173`(`procedure/back/app/service/push.py:155-163` · `procedure/app/lib/screens/settings_screen.dart:78 · :117-121`)
- 줄 번호 = HEAD 기준

## 판정: WARN (가벼움만 — 구현 착수를 막지 않음)

FAIL 0 · WARN 무거움 0 · 가벼움 6.
W1 ~ W13 모두 닫힘. U1 ~ U4 결정 글자대로 들어감. **U1 의 [시술 대기] 확장은 결정 범위 안**(같은 칸 하나 — 코드 사실로 확인). U5(OQ-A79) 열린 채 · 글자 안 지음. lint day 범위 0/0. 새 ID(A-77 · OQ-A91 · OQ-D41) 중복 0. 남은 것은 새 경로 한 곳의 빈칸 둘과 출처 · 꼬리표 정도.

---

## 1. W1 ~ W13 닫힘

| # | 자리(파일:줄) | 결과 |
|---|---|---|
| W1 | `spec-003-mobile-app.md:1135` | 닫힘 — 「여권 스캔 · 띄우기 · QR 은 여전히 넣지 않음」 ~~취소선~~ + 「(개정 ㉒ — 넣음)」. 같은 절 :1144 와 모순 없음 |
| W2 | `spec-003:1144` · :834 · :838 · A-69 :1426 · OQ-A91 :1615 | 닫힘 — 이유 문장 「시스템 카메라 앱이라 선언이 없었다」 취소선 + **확인 안 됨**(research-2 §6). 사실로 남긴 것 = 「지금 매니페스트에 `CAMERA` 없음」 한 줄. 차트 · 채팅 카메라 영향 = OQ-A91(기본값 표시 · 거부 글자 안 지음) + A-69 실물 확인 줄 |
| W3 | `spec-007-reservation-detail.md:591` · :590 · :505 · OQ-D41 :807 | 닫힘 — `sending` 이 KOS 시간 한도 + 여유보다 오래 남으면 읽을 때 「실패」 · [다시 보내기] 대상 · 409 아님. 근거 확인: `KosClient(timeout_seconds)` → `httpx.AsyncClient(timeout=…)`(`client.py:252 · :262`) · `questionnaire_history` 는 `Timestamps` 믹스인(`reception.py:85`)이라 `updated_at` 있음. 가벼운 빈칸 → N3 · N6 |
| W4 | `spec-007:593` · OQ-D40 :806 | 닫힘 — 소켓 주소가 믿는 앞단일 때만 헤더 · IP 꼴일 때만. 근거 `ext_peer.py:32-41` `ip_key`(`X-Day-Client-IP` · `ext_proxy_host` · `ipaddress.ip_address`) — SPEC 문장과 그대로 맞음. (참고: 같이 단 `deployment.md:200-201` 은 「지금 코드는 클라이언트 IP 를 읽지 않는다」라는 **미정 메모**라 규칙 근거로는 약함 — `ext_peer.py` 만으로 충분 · 고칠 필요 낮음) |
| W5 | `spec-003:631` · :656 · OQ-A83 :1607 · `spec-007:551` | 닫힘(U3 로) — 살아 있는 「태블릿에 띄우기」 화면 글자 0. 예외 하나 = 고침 5 머리 :49 → N4 |
| W6 | `spec-007:544` · OQ-D33 :799 | 닫힘 — 「기본값(planner 제안) · cc 종류 글자 차용」 · 이름 기본값 「iPad」/「iPhone」 출처 · OQ-D33 에 넣음 |
| W7 | `spec-003:638` | 닫힘 — 「Scan with your phone camera」 넣음 |
| W8 | `spec-003:670` · OQ-A88 :1612 · `spec-000-data-model.md:1104` | 닫힘 — cc 원문 확인: `settings_screen.dart:78`(빈 값이면 `renameDevice` 안 부름) · `:117-121`(이름 줄 늘 누름 · 등록 전엔 안내 줄 **더함**). SPEC 과 같음 |
| W9 | `spec-003:1430` A-73 | 닫힘 — 「스트림이 연결된 동안」 폴링 0 · 끊긴 동안 OQ-A84 |
| W10 | `spec-004-internal-chat.md:540` | 닫힘 — 「DAY 범위 밖」 취소선 + 이유 |
| W11 | `spec-007:589` | 닫힘 — DAY-SPEC-001 직원 토큰 원칙의 예외 · KOS 기록에 직원 안 남음 |
| W12 | `spec-007:538` | 닫힘 — 앱 닫기 = `{status: "canceled"}` 만 · 다른 값 400 |
| W13 | `spec-000:1201` | 닫힘 — 일반 문장 취소선 → 「`id_photo` 에는 상태 칸을 두지 않는다」 |

## 2. U1 ~ U4 — 결정 글자 대조

| # | 결정(§2) | SPEC 자리 | 결과 |
|---|---|---|---|
| U1 | 「외국인 여권 스캔 저장 = 신분확인 O → 웹 [상담 대기] 켜짐 · OQ-D36 닫음」(사용자) | `spec-007:51` ① · :76 · :310 · :660 · :686 · :714 · OQ-D36 :802 · D23 :864 · B17 :911 · `spec-000:49` · :1180 · `spec-003:1434` A-77 · `20-spec.md:49` · `10-decision.md:40` · `log.md:17` | 반영. 웹 예약 동작 변경을 007 머리 보충 :51 에 「웹 예약 동작은 바꾸지 않는다는 이 한 곳을 뺀 나머지에 그대로」로 적음 — 지시대로 |
| U1 확장 | [시술 대기] 신분확인 칸도 같은 판정(`spec-007:310` 끝 · :714 · `spec-000:1180`) | **범위 안(사실 판정)** — 아래 §2.1 |
| U2 | Android 띄우기 채널 이름 = 「고객 입력 요청」 · OQ-N22 닫음 | `spec-005-notifications.md:44` · :326 · OQ-N22 :490 | 반영(글자 그대로). 출처 표기 하나 → N5 |
| U3 | 웹 · 앱 글자 = 「태블릿에 보내기」 | `spec-007:551` · `spec-003:631` · :656 · OQ-A83 :1607 | 반영 |
| U4 | 앱 상세 JSON 에 여권번호 안 실음 · 스캔 확인 화면 열 때만 따로 읽음 | `spec-007:524`(싣지 않는 것에 넣음) · :525(새 경로) · :516(권한) · OQ-D29 :795 · `spec-003:648` · :748 · `10-decision.md:40` | 반영. 새 경로 빈칸 둘 → N1 · N2 |

### 2.1 U1 [시술 대기] 확장 — 같은 칸인가

**같은 칸 하나다 → 결정 범위 안.**

- SPEC: [상담 대기] 빠진 칸(D21 · `spec-007:310`)의 「신분확인」과 [시술 대기] 빠진 칸(D50 · :311 「**신분확인** + 「오늘」 ✓ + 관리실」)이 같은 값을 본다. 앞 판 규칙 4(:714 · 이번에 안 바뀐 앞 문장)도 이미 「단 [상담 대기] · [시술 대기] 켜는 조건이다(D21)」로 한 조건을 두 버튼에 걸었다.
- 코드(`96036397`): 두 쓰기 모두 **같은 함수** `care_rows.identity_confirmed(session, customer.id, start, end)`를 부르고 같은 400 `reception_missing(field="identity")`를 낸다 — [상담 대기] `reservation_care_writes.py:338-339` · [시술 대기] `:445-446`. 그 함수(`reservation_treatments.py:52-67`)는 「그 고객 · 그 날 KST 창의 마지막 `identity_check` 가 `confirmed`」 하나만 보고 국적 · 방법(`method`)을 가리지 않는다. 화면 「O」도 같은 함수(`reservation_detail_care.py:109`).
- 따라서 여권 스캔 저장이 `identity_check(status=confirmed)` 를 남기는 순간(007 §3 ⑤ :571) 두 버튼의 신분확인 칸이 **함께** 채워진다 — 한쪽만 채우려면 오히려 새 갈래(방법 · 국적 분기)를 지어야 한다. SPEC 이 [시술 대기]를 같이 적은 것은 결정의 필연적 결과를 드러낸 것이지 범위 확장이 아니다. planner 리포트의 「다르게 원하면 이 한 구절만 되돌리면 된다」는 코드상 한 구절로 안 끝나므로(새 분기 필요) 되돌릴 이유 없음.

## 3. 새로 생긴 문제 — 가벼움

| # | 파일:줄 | 무엇 · 근거 | 고칠 방향 |
|---|---|---|---|
| N1 | `spec-007:525` `GET /api/reservations/visits/{visit_id}/passport` | **권한은 맞음**(스캔 저장과 같은 `reservation.detail` edit · :516 · 앞 판보다 노출 좁음 — `reservation` view 전원 → edit 만). 다만 스캔 저장(:567 ①)은 409(오늘 ∧ 예약 · 접수 아님 · KOS 연결 없음)로 막는데 이 읽기는 **날짜 · 단계 조건이 없다** — edit 직원이면 아무 방문 id 로 여권번호를 읽을 수 있다. 화면 밖 호출을 막는 말은 「앱은 그 화면 밖에 두지 않음」(클라이언트 약속)뿐. 워크인(KOS 연결 없음) · 여권 칸이 빈 고객의 응답 꼴도 없음 | 스캔 저장 ① 과 같은 조건(오늘 ∧ 예약 · 접수 · 409 같은 코드)을 붙이거나 「조건 없음 — 이유」 한 줄 · 빈 고객 = 7칸 null 200(기본값) 한 줄 |
| N2 | `spec-003:648` U-27 「읽기 실패 = 「KOS 지금 값」 열 비움 · 저장은 그대로」 ↔ `spec-007:562` 저장 `fields` = **바뀐 칸만** | 비교 값이 없을 때 앱이 무엇을 「바뀐 칸」으로 보낼지 없음(전부? 0개 = `unchanged`로 아무것도 안 감?). 0개로 해석하면 「저장은 그대로 됨」이 KOS 에 아무것도 안 쓰는 저장이 된다 — 구현자가 되물을 빈칸 | 「비교 값이 없으면 읽은 7칸을 모두 보낸다(서버 ② 가 KOS 를 다시 읽어 합치므로 안전)」 한 줄(기본값(planner 제안)) |
| N3 | `spec-000:1240` `questionnaire_history.kos_status` | 「`sending` → `sent` / `failed`」만 — 이번에 정한 「멈춘 `sending` = 읽을 때 실패」(007:591)를 가리키지 않음. 데이터 모델만 읽는 백엔드가 놓칠 수 있음 | 행 끝에 「멈춘 `sending` 판정 = DAY-SPEC-007 §3 「보내는 중 고착」 · 칸 변화 없음」 꼬리표 |
| N4 | `spec-007:49` 고침 5 머리 ① | 「[문진 QR] = 이 화면 QR + **[태블릿에 띄우기]**(cc 웹 꼴)」가 취소선 없이 살아 있음(보충 :51 ② 가 바꿨다고 적었지만 같은 머리 안 글자는 그대로) | 그 글자에 ~~취소선~~ + 「→ [태블릿에 보내기] · 보충 ②」 (개정 기록이라 꼬리표만으로도 됨) |
| N5 | `spec-005:44` · :326 · OQ-N22 :490 | 출처 「cc 띄우기 푸시 제목 「고객 입력 요청」 · 문진 · 스캔 같은 채널」 — cc 원문(`push.py:162`)은 `"고객 입력 요청" if d.kind == "questionnaire" else "여권 스캔 요청"`. 즉 「고객 입력 요청」은 **문진** 푸시 제목이고 스캔은 「여권 스캔 요청」. 채널 이름 = 「고객 입력 요청」은 결정(§2 :70) 글자 그대로라 바꿀 것은 없고, 출처 표기만 부정확 | 「cc 문진 푸시 제목(스캔 제목은 「여권 스캔 요청」 — 채널은 하나)」로 출처를 좁힘. 알림 **제목**은 cc 대로 종류별 둘이라는 것도 :326 에 한 구절(지금 `title` 칸만 있어 값이 안 적힘) |
| N6 | `spec-007:591` 「보내는 중 고착」 | 근거 `client.py` 시간 한도는 `KosClient` 의 `httpx` 한도다. 문진 KOS 제출은 KOS **공개** 경로(OQ-D39 · :589)라 지금 `KosClient` 에 그 호출이 없다 — 새 호출이 같은 클라이언트(같은 한도)를 쓴다는 말이 없으면 「한도 + 여유」의 한도가 정해지지 않음 | 「KOS 공개 제출도 시간 한도가 있는 같은 `KosClient`(또는 같은 `timeout_seconds`)로 부른다」 한 구절 |

모순 · 발명 점검 결과(문제 없음):

- 새 기본값 셋(W3 여유 · OQ-A91 권한 요청 시점 · U4 읽기 실패 처리) 모두 「기본값(planner 제안)」 + OQ 표시. 새 화면 글자 = cc 원문 2개(「Scan with your phone camera」 · 「고객 입력 요청」)뿐 — 둘 다 원천 확인.
- 「외국인 늘 회색」 · 「여권 칸(OQ-D29)」 · 「OQ-D36)」 · 「kos_status 를 두지」 살아 있는 앞 판 문장 = 0(취소선 밖 grep).
- A-77 「다른 날 스캔 기록은 오늘 칸을 채우지 않음」 = 코드 `identity_confirmed` 의 KST 하루 창과 맞음.
- migration 변화 없음 판단 = 맞음(U1 읽기 판정 · U4 새 읽기 · W3 기존 칸 읽기).

## 4. U5(OQ-A79) — 열린 채인가

열림. `spec-003:1603` OQ-A79 기본값 = **「없음 — 사용자 문구」** · :1144 「planner 가 합쳐 짓지 않는다」 · `spec-004:540` 「여권 용도 = OQ-A79」 · `10-decision.md:40` 「사용자 몫」. 새 문구 글자 0 → PASS.

## 5. lint

`python3 scripts/lint-pipeline.py --strict` → `0 error, 263 warning` · `products/day` 줄 0(ERROR 0 · WARN 0). 263 WARN = 다른 제품(selly 등 frontmatter · `doc_no`) — 무관(기존 부채). 새 ID A-77 · OQ-A91 · OQ-D41 각 1회 정의.

## 6. 사용자 확인 필요

없음(새로 열 결정 없음). U5 는 그대로 사용자 문구 대기.
