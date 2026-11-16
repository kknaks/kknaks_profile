# fix-spec-3 결과 보고 — 문서 리뷰 WARN 11 반영 + 작업 계획(WP)

## 상태: done

- 스펙: mediness `fix-spec` 워크트리(1 · 2판 미커밋 위에 이어 씀) · `products/day/` 만 · 커밋 · push · PR 0 · GitHub 쓰기 0 · `30-work/` 새 파일 0.
- 작업 계획: `orchestration/work/fix/wp-plan.md`(WP 4개).
- 값(키 · Vault 이름 · IP · Team ID) 0 — 코드 `deploy/config/dev.env` 에 값이 있지만 계획 · 스펙에 옮기지 않았다.

## A. 리뷰 반영 — W1 ~ W11 (11/11)

| 지적 | 반영 자리(고친 뒤 줄) | 내용 |
|---|---|---|
| W1 | `spec-003:236` · A-28 `:871` | 「네 줄」 예외에 모두 완료 카드 [귀가 대기] 줄(개정 ⑧) · A-28 「예외 = 호출 줄 A-30 · [귀가 대기] 줄 A-42 · 다섯째 상태 A-41」 |
| W2 | `spec-003:51`(머리 ⑨) · 사전 표 `:670` · OQ-A45 `:985` | 사용자 확정 = 바탕(interpret-pwa back) · 시드 사본(5번 원문 + 통보 이의 없음) · **전 병원 한 벌 · 병원별 사전 없음 = 코디 기본값**으로 옮김(OQ-A45 · 뒤집을 수 있음 · 뒤집으면 정할 것까지) |
| W3a | `spec-004:28` ② · `:60` · `:223` · 프로토 표 · OQ-C14 `:608` · `spec-000:31` | 시스템 줄 없음 = 코디 기본값 OQ-C14 · 「사용자」 표기 걷어 냄 |
| W3b | `spec-004:28` ① · U-1 `:155` · OQ-C15 `:609` | 403 안내 글자 · 버튼 = 코디 지시 · 기존 글자 재사용 · 사용자 통보 · 뒤집을 수 있음 |
| W3c | `spec-005:135` · OQ-N7 `:375` | 출처 = 코디 브리프 `fix-spec-1-brief.md` · 차례 `doctor_call` → `chat` 은 기본값(OQ-N7) |
| W3d | `spec-003:254` · OQ-A44 `:975` | 목록 · 룸 상세 [귀가 대기] 같은 잠금 = planner 기본값 OQ-A44 |
| W4 | 「정리」 `spec-003:653` · 상한 문단 · A-44 `:887` | 「자리는 잡은 뒤 어떤 경로로 끝나도(예외 · 취소 · 앱 사라짐 포함) 한 번만 돌려놓는다 · 두 번 반납 금지」 · A-44 에 반납 갈래(ready 전 STT · TTS 실패 · 설정 재시도 예외 · ready 뒤 끊김 · 앱 강제 끊김 · 서버 작업 취소 → 자리 0 · 음수 아님) |
| W5 | 「연결 시간 상한」 `spec-003:654` · 수명 줄 | **원천 · 라이브러리에서 찾은 값**(기술 기본값 표시): Soniox 연결 수립 10초 = ipwa `soniox.py` `CONNECT_TIMEOUT = 10`(`websockets.connect(open_timeout=…)`) · Soniox ping 20/20 = 원천이 값을 안 줘 `websockets` 17.4 기본값 · 닫기 대기 3초 = 원천 `session.py` · **죽은 앱 연결** = uvicorn 0.54 기본 `ws_ping_interval=20.0` · `ws_ping_timeout=20.0`(DAY compose api 명령은 바꾸지 않음 · 확인) → 끊김 → 정리 · 자리 반납 |
| W6 | 수명 줄 · OQ-A46 `:992` | 판정 안 함 — 사용자 질문 OQ-A46(수명 · 무활동 상한을 둘지) · 지금 그대로 상한 없음 |
| W7 | A-47 `:890` | 「구현 워커 · 로컬(키 비움) · dev 엔 키 있음」 · 확인 대상 `error.code = no_api_key`(글자가 `session_limit` 과 같으므로) |
| W8 | `deployment.md:181` · `:166` | Key Vault = **필수 6 + 선택 3**(`-chat-blob-connection-string`(아직 없음) · `-apns-auth-key` · `-soniox-api-key`) — 리뷰는 「선택 2」였으나 코드 `day_vm.py OPTIONAL_SECRETS` 에 채팅 Blob 이 이미 있어 3 · APNs 줄에 비밀 이름 `day-<env>-apns-auth-key` 를 적어 기준 맞춤 |
| W9 | `spec-004:222` | 출처 = DAY 앱 `app/lib/chat/screens/chat_room_screen.dart:588`(「수정 취소」) · `:638`(「저장」) |
| W10 | `spec-004:432` · 머리 ② | {방 이름} = **푸시 발송 작업이 방을 읽는 때**(커밋 뒤 다시 읽기 — 받는 사람 줄과 같음) |
| W11 | ① U-1 `spec-004:159` · C-A19 `:574` ② 규칙 `:349` ③ U-8 `:233` | ① 조작 중 403 = 본문 안내만 · 토스트 없음 · C-A19 갈래 추가 ② `chat_group_only` `detail` = 화면에 안 나오는 내부 문장 · 앱은 code 로만 ③ 설정 응답에 `chat` 없으면 켜짐 |

### 조용히 통과 1 ~ 6

| # | 반영 |
|---|---|
| 1 | A-46 `spec-003:889` — 「듣는 상태 누적 약 3분 20초 이상(올린 오디오 6 MiB 넘게 · 재생 · 멈춤 시간은 안 셈)」 |
| 2 | W7 과 같음(A-47 `error.code`) |
| 3 | W4 와 같음(A-44 반납 갈래) |
| 4 | U-3 기준 토큰 `spec-003:270` · A-43 `:886` — 앱 `app/lib/ui/theme.dart` **이미 있는 이름**: 바탕 `Ms.red100` · 띠 `Ms.red`(지금 마취 20분 초과 바탕 = `Ms.red100` · 칩 · 카드 테두리 = `Ms.red`) · 띠 굵기 픽셀 = 구현 때 · 리뷰 눈 확인 |
| 5 | C-A21 `spec-004:576` — 다른 기기 = 푸시는 바로 0 · 배너는 그 기기가 다음에 앞으로 올 때부터 · 실물 = 두 기기 |
| 6 | W11 ① 과 같음(C-A19 조작 중 403) |

참고 3: `spec-000:1025` 형식 칸 「enum」 → 「text(열린 값)」 + 머리 개정 줄. 참고 1 · 2 · 4 는 `wp-plan.md` §6 위험 · §2 BE-2 로 넘김.

OQ-A43 은 그대로(사용자 답 없음 · 「통역 서버를 쓸 수 없어요」 재사용) — 덧붙여 2판 OQ-A43 의 예시 글자(「잠시 뒤」)를 지웠다(지은 글자처럼 읽혀서).

## 정할 것 (사용자 몫만)

1. **OQ-A46** 통역 세션 수명 · 무활동 상한을 둘지(상한 6 × 수명 없음 → 열어 둔 기기가 자리를 쥠). 지금 = 상한 없음.
2. **OQ-A43** 상한 찼을 때 글자 — 지금 「통역 서버를 쓸 수 없어요」(키 없음과 같음).
3. 코디 기본값 · 지시로 적용해 통보만 한 것(뒤집을 때만): OQ-A37 · A38 · A44 · A45 · A39 ~ A42 · C11 · C12 · C14 · C15 · N7.
4. 열린 채로: M-1 · M-16 · M-20.

## `wp-plan.md` 요약

- **WP 4개** — 경로로 나눔(`backend` 워커 = `backend/` · `scripts/` · `deploy/` · 루트 `pyproject.toml` · `uv.lock` / `mobile` 워커 = `app/`): WP-BE-1 채팅 · 알림 서버 · WP-BE-2 통역 서버 · WP-APP-1 시술현황 카드 + 후속 2 · WP-APP-2 채팅 · 설정. 워커 안에서는 차례(BE-1 → BE-2 · APP-1 → APP-2), 워커끼리 동시.
- WP 마다 근거 스펙 절 · 수용 항목 · **grep 으로 센 고칠 파일**(BE-1 6 · BE-2 기존 11 + 새 6묶음 · APP-1 5 · APP-2 13) · 하지 말 것 · 시험 파일 · 명령(`uv run pytest -q -m "not infra"` · `scripts/test.sh -q` · `ruff` · `fvm flutter analyze/test`) · 실물 몫.
- **WP 사이 계약 표**(#22 요청 · 응답 · 오류 · `chat_room` SSE · 설정 `items` · 푸시 · 403) — 서버 · 앱이 같은 표.
- **통역 원천 가져오기 표** — `git -C …/interpret-pwa show origin/main:<path>` · `17c26b5` · 파일 → 자리 · 가져오지 않음(`records` · `import_glossary` · front).
- **위험 8줄** — 깨진 시드 = api 기동 실패(로그인 · 시술현황 · 채팅까지 멈춤 — 사용자에게 알림) · `runtime` → `day.public` · OpenCC × 3.13 · Caddy 6MiB · 루프 막힘 · Soniox 동시 한도 · 자리 누수 · 오래 열린 세션.
- **사용자 실기기 확인 7줄** 한곳에.
- 계획 안에서 새로 정한 동작 없음 — 「시드 경로 · 폴더 vs 펼침 · `websockets` 직접 의존」은 구현 몫으로 표시(스펙도 구현 몫으로 둠).

## 바꾼 문서 (3판분)

- `20-spec/spec-003-mobile-app.md` — `:51` · `:236` · `:254` · `:270` · `:610 대` 수명 · `:653-654` · 상한 문단 · `:670` · A-28 · A-43 · A-44 · A-46 · A-47 · OQ-A43 · 새 OQ-A44 · A45 · A46
- `20-spec/spec-004-internal-chat.md` — `:28` · `:60` · `:155` · `:159` · `:222-223` · `:233` · `:349` · `:432` · 프로토 표 · C-A19 · C-A21 · OQ 절 머리 · 새 OQ-C14 · C15
- `20-spec/spec-005-notifications.md` — `:135` · 새 OQ-N7
- `20-spec/spec-000-data-model.md` — `:31` · `:1025`
- `40-architecture/deployment.md` — `:166` · `:181`
- `log.md` — 1줄(3판)

## 검증

```
python3 scripts/lint-pipeline.py --strict   → exit 0 · 0 error, 263 warning
products/day/ 범위: ERROR 0 · WARN 0 (263 WARN 은 모두 타 제품 — 무관)
```

## 주의점

- W8 은 리뷰 지시(「선택 2」)와 다르게 「선택 3」으로 적었다 — 코드 `scripts/deploy/day_vm.py:47-50` `OPTIONAL_SECRETS` 에 채팅 Blob 비밀이 이미 있어서다.
- `_RESUME` §2 의 통역 행 「전 병원 한 벌 = 코디 기본값」 맞춤은 코디 몫(브리프대로).
