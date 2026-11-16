# 리뷰 리포트 — ext-api-charty1 / code r3 (2026-11-16)

**판정: PASS — FAIL 0 · WARN 0 · 질문 0** (커밋 `1c3a340` 의 두 고침이 SPEC-008 0.4.6 · DEC-012 D-46 · D-47 그대로 · 시험이 실제로 고정함(변이 셋 모두 잡힘) · 지운 · 약하게 바꾼 단언 0 · 회귀 0)

- 대상: `git diff c4876bd 1c3a340` — 앱 3(`app/api/ext.py` · `app/schemas/ext.py` · `app/service/ext.py`) · 시험 3(`tests/fake_kos.py` · `tests/test_ext_lookup2.py` · `tests/test_ext_write.py`). 워크트리 깨끗(HEAD = `1c3a340`)
- 근거: SPEC-008 0.4.6(§4.3 「거르기」 · 「모양 오류」 · `bundlePrice` · §6.12 오류 표 · §6.15 · T50 · T64) · DEC-012 D-46 · D-47(D-35 고침 줄) · `be-fix-e2e1-instructions.md` · `fix-e2e2-instructions.md` 「backend 5차」
- 돌린 시험(사용자 포트 · KOS 호출 없음): `test_ext_{lookup,lookup2,write,docs,detail,board,auth,clinic,history}.py` · `test_openapi_docs.py` · `test_order.py` · `test_resv_{detail,board,write}.py` → **304 passed**(r2 289 + 새 15)
- 변이 확인(파일은 고치지 않음 · 스크래치 스크립트가 시험 프로세스 안에서만 함수를 바꿔 끼움): 아래 표 · 셋 다 실패로 잡힘

## 1. 시술권 — D-46 · §4.3

| 볼 것 | 판정 | 근거 파일:줄 |
|---|---|---|
| 산 묶음만 **먼저** 고른 뒤 모양 검사 · 칸 만들기 | **PASS** | `app/service/ext.py:325-326` — `[self._ticket(b) for b in data if isinstance(b, dict) and self._live_bundle(b)]`. 거르기(`_live_bundle` `:370-373`)는 장 상태만 보고(`_bundle_tickets` `:366-368` 은 모양이 깨진 세트 · 장을 건너뛸 뿐 예외 없음), `_ticket` 은 고른 묶음에만 불린다. 옛 `_live` 임시 키 · `pop` 은 없어짐 |
| `price` 객체에 `value` 없음 = 0 | **PASS** | `:384` `price.get("value", 0)` → `{"value": 0, "currency": …}` |
| `price` 없음 · 객체 아님 · 숫자 아닌 `value`(문자열 · null · bool) = 502 그대로 | **PASS** | `:381-386` — `price` 가 dict 가 아니면 `BadGateway`, `value` 가 int/float 아니거나 bool 이면 `BadGateway`(`value: null` 은 키가 있으므로 0 이 아니라 502 — SPEC 「숫자 아닌 꼴」과 맞음) |
| 공개 시술권을 쓰는 다른 경로 무변경 | **PASS(해당 없음)** | `app/` 안 `get-ticket-bundles` 사용은 lookup 의 내부 호출 하나뿐(`:315`) — 공개 시술권을 부르는 앱 코드가 없다. 그 밖 경로 · 메뉴 동기화 코드 변경 0 |
| 칸 이름 · 뜻 | **PASS** | 응답 칸 그대로(`optionId` … `bundlePrice`) — SPEC 0.4.5 「칸 이름 · 뜻 바뀐 것 0」 |

## 2. 상담 메모 빈 값 — D-47 · §6.15

| 볼 것 | 판정 | 근거 파일:줄 |
|---|---|---|
| 앞뒤 공백 지운 빈 값 = 400 | **PASS** | `app/schemas/ext.py:395-408` — `field_validator` 가 `v.strip()` 이 비면 `PydanticCustomError`. 보내는 값은 원문 그대로(공백을 지워 보내지 않음 — 글 앞뒤 공백 유지 · 시험 `tests/test_ext_write.py:247-256`) |
| KOS 호출 0 · `event_log` 0 | **PASS** | 요청 본문 검증 단계(FastAPI)에서 끝나 서비스 `consultation_memo` 가 불리지 않는다 → `kos_write` · `kos_rejected` 줄도 0. 시험 `tests/test_ext_write.py:237-245`(KOS 0 · `event_log` 행 수 그대로 · `kos_rejected` 포함) |
| 오더 메모 빈 값 = 비움 그대로 | **PASS** | `ExtOrderMemoRequest`(`app/schemas/ext.py:386-390`) 변경 0 · 시험 `tests/test_ext_write.py:247-256`(`""` 를 KOS 에 그대로 보냄 · 가짜 KOS 값이 비워짐) |
| message 꼴이 `body.<칸>: …` 관례와 같은지 | **PASS** | 오류 처리기 `app/main.py:122-124` 가 `"<loc>: <msg>"` 로 만든다 → `body.consultationMemo: KOS 는 상담 메모를 비울 수 없어요`(시험이 문자열 전체를 단언 · `tests/test_ext_write.py:237`). 참고: 기존 `ValueError` 갈래(예 `_not_blank`)는 pydantic 이 `Value error, ` 를 앞에 붙여 `body.name: Value error, 빈 값이에요` 꼴이다. 이번에는 `PydanticCustomError` 를 써서 그 접두가 없다 — SPEC 0.4.6 이 정한 문구와 맞추기 위한 선택이고 `body.<칸>: ` 접두 관례는 같다 |
| `null` | **PASS** | `str` 타입이라 지금처럼 타입 오류 400(검증기 전) — 바뀐 것 없음 |
| Swagger | **PASS** | `app/api/ext.py:468-471`(상담 메모 description · 「비울 수 없다」 · 상담 전 일정 · 상담사 · 의사 그대로) · `:476-479` `CONSULT_400` 을 상담 메모 경로에만(`:502`) · 예약 상세 「예약을 만든 직후 … `reservation_gone` … 다시 부르면 된다」(`:386` · `:428-429` · D-47 ②). 시험 `tests/test_ext_write.py:258` |

## 3. 시험이 고정하나

`git diff c4876bd 1c3a340 -- procedure/back/tests` 의 `-` 줄은 3개 — 모두 `tests/fake_kos.py` 의 `menu_handle` 서명 · 본문 · 부르는 줄(가짜 KOS 기능 넓힘)이다. **시험 단언을 지우거나 약하게 바꾼 줄 0.**

변이(시험 프로세스 안에서만 · `tests/test_ext_lookup.py` + `tests/test_ext_lookup2.py` 54개):

| 변이 | 결과 | 잡은 시험 |
|---|---|---|
| 거르기를 없앰(`_live_bundle` 늘 참) | **10 failed** | `test_t50_*` · `test_e2e1_*` 등 |
| `value` 없음을 0 이 아니라 502 로(옛 동작) | **1 failed** | `tests/test_ext_lookup2.py:294`(① 산 묶음 `{currency}` 만 → 0) |
| 옛 순서(모든 묶음에 칸 만들기 먼저 · 그다음 거르기) | **1 failed** | `:303`(② 다 쓴 묶음의 `price = "x"` 가 섞여도 200) |

- ③ 산 묶음의 `price` 없음 · 문자열 · 숫자 아닌 `value` · `null` → 502(`tests/test_ext_lookup2.py:316` · 5갈래)
- ④ 가짜 KOS 기본 응답에 실물처럼 `value` 없는 다 쓴 묶음을 섞음(`tests/fake_kos.py:64-71` · `:209-214` · 내부 호출에만 · 명시 `{}` 응답에는 안 붙음). 그래서 lookup 을 부르는 **모든** 기존 시험이 이제 실물 모양을 지나간다 — 기존 시험(`test_t15` · `test_t50` 등)이 그대로 통과하는 것이 「걸러진 묶음은 안 나옴」을 함께 고정한다
- 상담 메모는 `""` · `"  "` · `"\n\t "` 세 갈래(`tests/test_ext_write.py:237`). 검증기를 빼면 200 이 되어 status · message · KOS 0 단언이 모두 실패한다(코드 읽기로 확인)

## 4. 회귀 — r1 · r2 PASS 자리

이 커밋이 닿는 곳은 lookup 시술권 조립(r1 표 #5)과 상담 메모 요청 모델(#9 · #11)뿐이다. 둘 다 위에서 다시 확인했다(**PASS**). 그 밖(board · 시도 예약 · 상세 · 헤더 · `ext_view` · `ext_call` · 병원 · 직원 · 직원 API · 기존 여섯 · Swagger 개수)은 파일 변경이 없거나 description 줄만 더해졌고, 관련 시험 304 passed(**PASS · 변화 없음**). 실명 · 키 grep: 새 시험 값은 `<다 쓴 묶음>` · `pur-dead` 같은 자리표시뿐(**PASS**).

## 참고 (판정 밖)

- `tests/test_ext_lookup.py:130` 의 주석 「묶음 {}」 은 이제 틀렸다 — 가짜 KOS 기본값이 `{}` 에서 `{"data": [다 쓴 묶음]}` 으로 바뀌어 그 줄은 「다 쓴 묶음만 → `[]`」 갈래를 본다. 「`data` 키 없음 `{}` → `tickets: []`」(T14)은 `tests/test_ext_lookup2.py:311-312` 가 명시 `{}` 로 이어서 고정하므로 빈칸은 아니다. 주석만 낡았다
- T50(0.4.5)의 「걸러진 묶음의 `price` 가 **없어도** 200」은 시험이 `price` 를 지운 다 쓴 묶음이 아니라 `price = "x"`(객체 아님)로 본다(`tests/test_ext_lookup2.py:303`). 코드 경로가 같아(거르기에서 빠지면 `price` 를 보지 않음) 계약은 고정된다
- r2 의 N1 ~ N3(W5 시험 · board 고객 값 단언 · T48 「그 밖 400」 · T49 null 둘)은 이 커밋 범위 밖이라 보지 않았다 — 처리 여부는 r2 Q-r2 그대로
