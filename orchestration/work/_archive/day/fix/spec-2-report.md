# fix-spec-2 결과 보고 — 1판 「정할 것」 적용 + 통역 서버 계약

## 상태: done

- 워크트리 `mediness-mediness/fix-spec` — 1판 미커밋 변경 위에 이어 씀 · 범위 `products/day/` · 커밋 · push · PR 0 · WORK 문서 0.
- frontmatter `version` 그대로(0.0.1) · `status` 그대로 · 값(키 · Vault 이름 · IP · 리소스 ID) 0 — 비밀 **이름** `day-<env>-soniox-api-key` · env 이름만.

## A. 1판 「정할 것」 적용 자리

| 1판 | 적용 | 맞춘 자리 |
|---|---|---|
| 1 · OQ-A37 겹침 색 (가) | 「코디 기본값 적용 2026-11-11 · 사용자 통보 · 뒤집을 수 있음」 | SPEC-003 머리 ⑧ · U-3 겹침 문단 · 겹침 표 머리(「적용값」) · 케이스 매트릭스 · A-43 · OQ 절 머리 · OQ-A37(뒤집으면 바꿀 자리 = U-3 표 · A-41 · A-43) |
| 2 · 모두 완료 상자 | 오른쪽 비움 · 마취가 열려도 「시술 모두 완료」 | U-3 「시술 모두 완료」 · 겹침 ② · A-41(+「오른쪽 칸 비움」) · OQ-A21 |
| 3 · OQ-A38 | 왼쪽 비움 · 버튼만 적용 | U-3 모두 완료 카드 · OQ-A38 |
| 4 · OQ-C11 (가) | 메시지 수정 모드의 [✓] 「저장」 · [✕] 「수정 취소」(U-4 원문 접근성 이름 그대로 — 새 글자 0) · ✕ = 되돌림 · 요청 없음 · 같은 값이면 ✓ 꺼짐 | SPEC-004 머리 · U-7 저장 · 취소 · C-A20 · OQ-C11 · OQ 절 머리 |
| 5 · OQ-C12 | 다시 로그인 · 앱 다시 열 때 **+ 앱이 앞으로 올 때 한 번** · 버튼 · 주기 재시도 없음 | SPEC-004 U-1 「다시 보는 때」 · 케이스 매트릭스 403 줄 · C-A19 · OQ-C12 |
| 6 · M-20 · M-1 · M-16 | 그대로 열림 | 손대지 않음 |

## B. 통역 서버 계약 — 어디에 · 왜

- **SPEC-003 §3 「통역」을 「앱 · 서버 계약」 절로 바꿔 채웠다**(새 SPEC 없음). 이유: ① 통역 WS 계약 · 사전 규칙이 이미 이 절에 있고 앱 화면(U-15) · 수용 항목(A-14 · A-14b) · 서버 의존(D-3)도 SPEC-003 에 있다 ② 레포의 나눔은 「기능 하나 = 앱 · 서버 계약을 같이 가진 SPEC 하나」(채팅 = SPEC-004) — 통역의 기능 자리는 SPEC-003 이다 ③ 새 SPEC 을 만들면 프레임 · 언어 · 문구를 두 곳에 적거나 SPEC-003 의 앱 계약을 옮겨야 한다. 그래서 같은 계약은 SPEC-003 한 곳에만 있고 배포 문서는 env 이름 · 미결만 적고 링크한다.
- 절 구성: 연결 · 인증 / 프레임(앱 ↔ 서버) / 오류 / 서버 동작(원천 값) / 동시 세션 상한 / 사전 / 설정 · 배포 / 원천과 다른 곳.
- 개정 머리말: SPEC-003 개정 ⑨(무엇을 대체하는지 — 2026-11-09 판 「앱 쪽 계약만 · 서버 내부는 구현 몫」).

### 꼭 넣을 것 반영

| 브리프 | 스펙 |
|---|---|
| 인증 | 헤더 Bearer 하나 · 세션 + `board` view(`is_admin`) · accept 전 close 1008 → 앱 HTTP 403 · DB 세션 accept 전 닫음 · **쿼리 토큰 · Origin 없음** · accept 뒤 1008 안 씀 |
| 메시지 · 오디오 · 언어 · 오류 | ipwa §5.3 · §5.4 · §5.5 그대로 — 아래 대조표 |
| 동시 세션 상한 6 | `DAY_INTERPRET_MAX_SESSIONS`(처음 값 6) · 서버 전체 = api worker 1 프로세스 셈 · dev · prod 각자 · 자리 = start · 키 확인 뒤 Soniox 열기 전 · 정리 때 반환 · 넘으면 `error {code:"session_limit", message:"통역 서버를 쓸 수 없어요"}` → 닫음 → **앱의 기존 「서버 error 프레임」 갈래**(message 그대로 · error 상태 · [다시 연결]) — 원천 문구 재사용 · 새 문구 0 · 글자 바꾸고 싶으면 OQ-A43 |
| 키 없음 · Soniox 거절 · 끊김 | `no_api_key` 「통역 서버를 쓸 수 없어요」 · ready 전 `soniox_unavailable` 「통역 서버에 연결하지 못했어요」 · ready 뒤 「통역 연결이 끊겼어요」 · 서버 재연결 없음 · 문구에 env 이름 · 받은 값 · 업체 · 원인 없음(원인은 로그) |
| 사전 | 시드 사본 한 벌(바이트 그대로 · `backend/day/` 아래 시드 폴더 · 경로는 구현) · 기동 때 한 번 읽고 검사 · 깨지면 기동 실패 · 로그 `glossary seed loaded: version=…`(A-14) · context 조립 · 줄이기 순서 · 언어별 한도 = 원천 그대로 · 한도 덮기 env 는 안 옮김 |
| 배포 | 선택 비밀 `day-<env>-soniox-api-key` 한 줄 · env `DAY_SONIOX_API_KEY` · `DAY_INTERPRET_MAX_SESSIONS`(deployment.md env 표) · 새 의존성 `opencc-python-reimplemented` · api worker 1 · 배포 중 세션 끊김(앱 [다시 연결]) · deployment.md 미결 2줄(Caddy WS · 의존성 · 메모리) · mobile-deployment §1-1 Soniox 키 넣음 |
| 실물 완료 조건 | A-44(서버 단위 · 가짜 Soniox) · **A-45 ① 실제 Soniox 7개 언어 · 왕복 · 멈춤 35초 뒤 두 번째 발화** · **A-46 ② TestFlight 실기기 + ③ 4분 넘는 세션 — 사용자 실기기 몫으로 표시** · **A-47 ④ 키 없는 환경 · 권한 없는 계정** |
| 확인 안 됨 5건 | SPEC-003 「통역 서버 — 구현 때 확인」 I-1(TTS 동시 한도 3) · I-2(Caddy 101 · 6MiB) · I-3(OpenCC × 3.13) · I-4(메모리 · 루프 막힘) · I-5(누르고 말하기 부재 — 서버 무관) |
| 코디 기본값 | OQ-A39 기록 없음 · A40 핸드셰이크 한 번 · A41 시드 PR · A42 앱 문구 그대로 — 「적용 · 사용자 뒤집을 수 있음」 표(뒤집을 때 정할 것도 적음) |

### 조사 §3 표 ↔ 스펙 필드 대조 — **다른 줄 0**

| 앱(조사 §3) | 스펙 §3 「통역」 | 같나 |
|---|---|---|
| `wss://…/api/interpret` · Bearer 헤더 · Origin 안 보냄 · `?token=` 안 씀 · 리다이렉트 안 따라감 | 같음 · 서버도 쿼리 토큰 · Origin 안 봄 | ○ |
| 핸드셰이크 401 · 403 → 로그인 거절 글자 | 거절 = accept 전 1008 → 403 | ○ |
| 연결 뒤 1008 → 로그인 거절 · 그 밖 닫힘 → 끊김 | accept 뒤 1008 안 씀 · 닫힘 1000 | ○ |
| ping 20초 | uvicorn 자동 응답 | ○ |
| `{"type":"start","lang"}` 한 번 | 같음 · 그 밖 칸 무시 | ○ |
| `lang` 7개 `en ja zh zh-Hant th vi yue` | 같음(대소문자) | ○ |
| PCM16 16 kHz mono 1,280 B | 같음 | ○ |
| `pause` · `resume` · `stop` | 같음 · stop 뒤 3초 drain | ○ |
| `ready` | 같음 | ○ |
| `caption` `id` · `side`(me/them) · `original` · `translation` · `final` | 같음 | ○ |
| `audio_start` `sampleRate`(24000) · 바이너리 24 kHz · `audio_end` | 같음(`id` 포함 — 앱은 안 읽음) | ○ |
| `error` `message`(비면 `code`) | `{code, message}` · 4코드 + `session_limit` | ○ |
| 모르는 `type` 무시 | 서버는 정해진 type 만 보냄 | ○ |

주의 한 줄(계약 오류 아님): 서버는 `start` 뒤 모르는 앱 프레임에 `bad_request` 를 보내되 닫지 않는다(원천) — 앱은 `error` 를 받으면 스스로 닫는다. 앱은 그런 프레임을 보내지 않으므로 실제로는 생기지 않는다(스펙에 적어 둠).

## 정할 것 (사용자 몫만)

1. **OQ-A43** 동시 세션 상한에 찼을 때 글자 — 지금 「통역 서버를 쓸 수 없어요」(원천 문구 재사용 · 키 없음과 같은 글자). 다른 글자를 원하면 사용자가 정함(서버 `message` 만 바뀜 · 앱 무수정). **추천: 그대로**.
2. (1판에서 열린 채로 둔 것) M-20 · M-1 · M-16 서명 — 이번 코드에 안 걸림.
3. (코디 기본값으로 적용 · 통보만) OQ-A37 · A38 · C11 · C12 · A39 ~ A42 — 뒤집을 때만.

## 코드 영향 (WP 용)

**서버(CENTURION_DAY `backend/`)**
- 라우트 `day/routers/api/interpret.py`(`@router.websocket("/interpret")`) · `day/public.py api_routers()` 등록 — 헤더 Bearer 읽기(`day/session.py _bearer` 규칙) → `async with get_async_session()` 안에서 `sessions.current_session(token, "bearer")` + `require_permission(BOARD, VIEW)` → `ServiceError` 면 `ws.close(1008)` → DB 세션 닫고 `accept()`(WS 는 `current_session` 의존성 · HTTP 예외 처리기를 못 씀 — 조사 §4).
- `day/services/` 에 interpret-pwa `session · soniox · assembler · chinese · langs` 복사(기록기 `records` 빼고) · `glossary`(로더 · 검사 · context) · 값 묶음은 `day/dtos/`.
- 동시 세션 상한 — 프로세스 안 셈(세마포어류) · `session_limit` 오류 · 정리 때 반환.
- 시드 `backend/day/seed/glossary.json`(interpret-pwa `17c26b5` `back/seed/glossary.json` 바이트 그대로) · `runtime/main.py` lifespan → `day.public` 경유로 기동 때 적재 · 깨지면 기동 실패.
- `common/config.py`: `day_soniox_api_key: SecretStr` · `day_interpret_max_sessions: int = Field(default=6, ge=1, …)`.
- `scripts/deploy/day_vm.py OPTIONAL_SECRETS` 에 `"DAY_SONIOX_API_KEY": "soniox-api-key"` 한 줄(+ 시험) · `deploy/config/*.env` 주석.
- `pyproject.toml` · `uv.lock`: `opencc-python-reimplemented`.
- 시험 `backend/tests/day/`: interpret-pwa `test_interpret` · `test_context` · `test_seed` 를 DAY fixture · 인증으로 + 인증 갈래 · `session_limit` · 문구에 env 이름 없음 · accept 뒤 1008 없음(A-44) · `test_import_boundaries` 지킴. 실물 스크립트(interpret-pwa `scripts/live_check.py` 의 seed · idle · zhhant 갈래)로 A-45.
- migration 없음(DB 안 씀).

**앱** — 고칠 것 없음(통역). 1판 코드 영향(카드 · 채팅 · 알림)은 `spec-1-report.md` 그대로 + 이번 적용: 그룹 이름 ✓ · ✕ 아이콘(U-4 접근성 이름 재사용) · 채팅 403 안내는 앱이 앞으로 올 때 한 번 다시 읽음 · 확인 필요 겹침 (가) · 모두 완료 상자 오른쪽 비움 · 마취 겹침 = 모두 완료.

**사용자 몫** — prod Key Vault `day-prod-soniox-api-key`(prod 배포 때) · A-46 실기기 · 4분 세션.

## 바꾼 문서 (2판분)

- `20-spec/spec-003-mobile-app.md` — 머리 ⑨ · 머리 26줄 문장 · U-3 · 겹침 표 · U-15 끝 줄 · §3 API 표 통역 줄 · §3 「통역 — 앱 · 서버 계약」 전체 · 케이스 매트릭스 통역 3줄 · D-3 · A-14b · A-41 · A-43 · 새 A-44 ~ A-47 · OQ-A21 · OQ-A37 · OQ-A38 · 새 절 3개(OQ-A39 ~ A42 · OQ-A43 · I-1 ~ I-5)
- `20-spec/spec-004-internal-chat.md` — 머리 · U-1 · U-7 · 케이스 매트릭스 403 · C-A19 · C-A20 · OQ-C11 · OQ-C12 · OQ 절 머리
- `40-architecture/deployment.md` — env 2줄 · 미결 2줄 · `40-architecture/mobile-deployment.md` — §1-1 · `log.md` — 1줄

## 검증

```
python3 scripts/lint-pipeline.py --strict   → exit 0 · 0 error, 263 warning
products/day/ 범위: ERROR 0 · WARN 0 (263 WARN 은 모두 타 제품 — 무관)
```

## 주의점

- 리뷰어에게: 1판 + 2판이 같은 미커밋 묶음이다. SPEC-003 머리 ⑧(1판) · ⑨(2판) · `log.md` 2026-11-11 4줄.
- `session_limit` 은 원천에 없는 DAY 코드다(문구는 원천 재사용). 코드 이름 자체는 앱이 읽지 않는다(`message` 가 있으므로).
- 시드 경로 · 기동 때 7개 언어 context 미리 만들기는 구현 몫으로 남겼다(계약은 결과만).
