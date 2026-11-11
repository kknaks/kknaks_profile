# planner 결과 보고 — 데모/운영 KOS 쓰기 구분 · dev 거르기 없애기 (task_8dffb1d9d28e)

## 상태: done (커밋 · push 안 함 — 워크트리에 변경만)

## 수행 내용

코디 답(2026-11-09)대로 브리프 §6.2 · §6.3 을 바꿔 적용했다 — `10-decision.md` 는 손대지 않음(DEC 폐기 · ESC 아님) · `30-work/work-*.md` 안 만듦. 결정 기록 = SPEC 개정 줄 + `log.md` decision-add 행. WP 나눔은 아래 「Delivery Issue 초안」.

| 파일 | 바꾼 것 |
|---|---|
| `products/day/20-spec/spec-000-data-model.md` | 머리 2026-11-09 개정 줄 · §3 01 `crm_connection.is_demo` 행 **지움**(원천 `erd/01-hospital.md` 의 쓰임은 「`APP_ENV=dev` 거르기」 하나뿐 → 남길 근거 없음) · 「환경」 절: 데모 · 실제 병원 연결을 칸으로 가르지 않음 · dev/prod = 스키마에 넣는 연결 데이터 · 뒤집힌 2026-11-03 줄 취소선 · 새 OQ-01-2(실제 병원 연결을 prod 스키마에 넣는 방법) · OQ-01-3(운영 테넌트 「같은 API」 확인) |
| `products/day/20-spec/spec-001-login-session.md` | 개정 ⑥ · U-2 · Flow 4 · 케이스 매트릭스 `no_connected_hospital` · 시퀀스 그림 · 규칙 5 · OQ-10(취소선 + 뒤집음) |
| `products/day/20-spec/spec-002-procedure-board.md` | 개정 ⑫ 새로 · 개정 ⑤ ⑥ ⑦ 에 뒤집힘 주석 · §3 KOS 쓰기 표 머리(모든 연결 같게 · 확인 안 됨도 막지 않음) · 5개 행(재호출 3단계 · 시작 취소 · 완료 취소 · 귀가 대기 1 · 2)에서 「운영 병원에 열지 않는다」 지움 + 행별 확인 상태 · 시작 취소 = **확인됨**(`방배정.har` · 데모 실물 — 「HAR 없음 · 내부 경로 미확인」 바로잡음) · 나머지 4개 = 확인 안 됨 그대로 · 귀가 2 에 `귀가.har` `COMPLETED` 사실 · 규칙 13 · 14 · 17 · U-9 · OQ-08 · 09 · 10 닫은 표 · 새 OQ-22(`COMPLETED` ↔ `PROCEDURE_DONE`) · OQ-23(확인 안 된 4개 데모 실물 확인) |
| `products/day/40-architecture/system.md` | 「환경」 두 줄 |
| `products/day/40-architecture/deployment.md` | 결정 요약(`KOS_TRIAL_WRITES_ON_LIVE` 취소선) · 그림 아래 줄 · env 표 `APP_ENV` 비고 · **`KOS_TRIAL_WRITES_ON_LIVE` 행 뺌** · 미결 표에 「prod 스키마의 실제 병원 연결」 |
| `products/day/40-architecture/mobile-deployment.md` | 확정 줄 · 구성 그림 · §9 KOS 행 · **M-18 닫음**(prod = 실제 병원 연결만 · 데이터) |
| `products/day/log.md` | decision-add 1(뒤집힌 3결정 취소선 · 사유) · spec-change 1 · arch-change 1 · 최종 수정 |
| `products/day/20-spec.md` | 최종 수정 날짜만 |

### 손대지 않은 것 (리포트 §4 목록 중)
- SPEC-002 상태 그림 · S-5 · S-6 — 데모/운영 문구 없음(그림은 이미 시작 취소 · 귀가 대기를 「DAY → KOS」로 그림). 변경 불필요.
- SPEC-002 §3 「권한 — 1차 기본」(리포트 #23) — 이름 표가 데모 지점 이름 기준인 것은 플래그 분기 아님 · 이번 결정 범위 밖.
- `30-work.md` — 새 WP 없음 → 행 추가 없음(Spec Coverage 그대로 `proposed`).
- `10-decision.md` — 코디 지시.

## 검증

- `python3 scripts/lint-pipeline.py --strict` → exit 0 · **0 error** · 263 warning — **products/day/ 경고 0**. 경고는 전부 타 제품(selly 등 doc_no · frontmatter 누락) — 무관.
- 남은 키워드: `products/day` 에서 「운영 병원에 열지」 · `KOS_TRIAL` · 「`is_demo = true` 연결만」은 취소선 · log 이력 행에만 남음.
- 근거 없는 정책 0 — 새로 정한 것은 브리프 사용자 결정(2026-11-09)뿐. 확인 안 된 4개 쓰기는 「확인 안 됨」 그대로 · KOS 경로 · 값 새로 안 적음 · 화면 문구 안 넣음.
- HAR 직접 재확인은 못 함 — 이 머신 `kknaks_profile` 체크아웃에 `2026-10-23-cc-overall-board/har/*.har` 이 없다. 시작 취소 「HAR 확인됨」 · 귀가 `COMPLETED` 는 조사 리포트 §2 를 근거로 적었다.

## 계약 준수
- 화면 · API 계약(경로 · 응답 모양) 변경 없음. `ActionResult.not_supported` · `event_log.payload.kos.status = not_supported` 는 스펙에 원래 없었다 — 응답 필드를 지울지는 아래 D1(코드 몫).
- `KOS_TRIAL_WRITES_ON_LIVE` 는 deployment.md env 표에서 뺐다. `deploy/config/{dev,prod}.env` 는 코드 레포 — D1.
- 환경 · 연결 종류로 가르는 새 규칙 없음.

## 리포트 §5 F1 ~ F9

| F | 이번에 | 어디 |
|---|---|---|
| F1 (가) 범위 | **닫음** — (ㄱ) 5개 모두 모든 연결에 같게 | SPEC-002 개정 ⑫ · KOS 쓰기 표 |
| F2 시작 취소 KOS 쓰기 | **닫음** — 쓰기 유지 · 「KOS 안 씀」 뒤집음 | SPEC-002 규칙 13 · 표 · log decision-add |
| F3 HAR 표기 | **스펙 닫음** — 「확인됨(`방배정.har`)」로 바로잡음. 코드 `writes.py:17` docstring 은 D1 | SPEC-002 표 |
| F4 확인 안 된 4개 | **방법 닫음**(데모 실물 · 코드 뒤 QA = D5) · **결과는 열림** OQ-23 · `COMPLETED` ↔ `PROCEDURE_DONE` 관계 **열림** OQ-22 | SPEC-002 §5 |
| F5 (나) 유지? | **닫음** — 없앤다 · M-18 도 닫음(prod 스키마 = 실제 병원 연결만) | SPEC-000 「환경」 · SPEC-001 · mobile-deployment |
| F6 `is_demo` 쓰임 | **닫음** — 칸 지움. **열림**: 실제 병원 연결을 prod 스키마에 넣는 방법 OQ-01-2 | SPEC-000 |
| F7 「같은 API」 근거 범위 | **열림** — OQ-01-3 · prod 배포 때 | SPEC-000 §6 · deployment.md 미결 |
| F8 남은 pending | **코드 몫** — D1 에서 확인(아래) | Delivery 초안 |
| F9 테스트 정리 | **범위 정함** — D4 | Delivery 초안 |

## Delivery Issue 초안 (발행은 코디)

**제목**: DAY — 데모/운영 KOS 쓰기 구분 · dev `is_demo` 거르기 · `crm_connection.is_demo` 칸 없애기
**Target SPEC**: DAY-SPEC-000 · DAY-SPEC-001 · DAY-SPEC-002 (이번 개정본 — 2026-11-09 개정 줄)
**코드 기준**: CENTURION_DAY `origin/dev` 91728737 · 파일:줄 = 조사 리포트 §1 · §3
**계약**: 화면 · API 경로 · 응답 모양 그대로. 5개 쓰기는 연결 · `APP_ENV` 와 무관하게 같은 op 을 만든다.

### D1 — (가) 데모/운영 KOS 쓰기 구분 제거 (리포트 #1 ~ #12)
- `emr/factory.py:96-98` `trial_writes` 삭제 · `:56-61` `build_adapter` 에서 `trial_writes=` 인자 뺌 (#1 · #5)
- `common/config.py:96-99` `kos_trial_writes_on_live` 삭제 · `deploy/config/prod.env:12-14` · `dev.env:13` 줄 삭제 · `docs/development/deployment.md:114` (#2 · #3 · #4)
- `emr/kos/writes.py` — `KosWritePlanner(trial=…)` · `TRIAL_STEPS :56` · `WriteNotSupportedError("… demo connections only")` 5곳(`:85-174`) · `write_open :61-78` 의 trial 분기 제거 — 5개는 늘 계획 · 늘 통과. docstring `:17-26` 표 「cc 구현 근거(HAR 없음 · trial) — 데모 연결에만」 → 시작 취소 = HAR 확인 · 나머지 = 확인 안 됨(SPEC-002 표 문구 맞춤) (#7 · #8 · F3)
- `emr/kos/__init__.py:66-70,182-190` `KosAdapter.trial_writes` · `supports_write` 인자 정리 (#9)
- `services/board.py:186-203,247-280` `_connection` · `_queue` 의 `trial_writes(is_demo, …)` 제거 · 주석 `:11-15,:730,:788` (#11 · #12)
- `ActionResult.not_supported`(`board.py:83`) · `event_log.payload.kos = {"status":"not_supported"}` — 이 5개 쓰기에서 더는 안 생김. **읽는 곳 0**(리포트 §1 참고) → 지울지 남길지(다른 `WriteNotSupportedError` 경로 — 예: 「시스템 계정 없음」 — 가 남는지 보고) 코드에서 정함
- `outbox.py:223-233,484-486` `decide_after_send` NOT_SUPPORTED 경로 (#10) — trial 이 없어지면 이 5개 op 이 보내는 시점에 막힐 길이 없다. 남은 다른 not-supported 경로가 있으면 유지. **F8**: 배포 전 dev 큐에 `failed(NOT_SUPPORTED)` 로 남은 행이 있는지 · 처리할지 확인(dev 만 배포됨 · prod 미배포)
- `ConnectionConfig.is_demo` · `fingerprint`(`factory.py:32-37`) (#6) → D3 와 같이

### D2 — (나) `APP_ENV=dev` 의 `is_demo` 거르기 제거 (리포트 #13 ~ #16)
- `services/crm_connections.py:21-33` `syncable_conditions` 의 `app_env != "prod"` → `is_demo IS TRUE` 조건 제거 (#13)
- 부르는 쪽 `tasks/emr.py:41-43` · `services/emr_sync.py:6,111-114` (`not_syncable` 경로 · docstring #226 A6) (#14)
- `services/board.py:186-203` 쓰기 대상 거르기 (#15)
- `services/auth.py:7,167-180,206,252` 로그인 후보 · `routers/api/auth.py:58,76` · `routers/login.py:122,144` (#16)
- **그대로 둠(확인만)**: #17 `/dev/kit*` · #18 `/docs` · #19 `APP_ENV` 필수 · 스키마 짝 · #20 로컬 기본 dev — 연결 거르기가 아니라 서버 기능 노출 · 배포 안전장치. 이번 결정(연결로 가르지 않음)과 무관하다고 판단 — 코디 확인 필요하면 질문

### D3 — `crm_connection.is_demo` 칸 지우기 (리포트 #21 · SPEC-000 §3 01)
- migration(새 revision · forward-only): `crm_connection.is_demo` drop · `models/hospital.py:57`
- `services/crm_connections.py:80-131` `ensure_demo_connection` · `day/public.py:27-45` · `scripts/seed_demo_connection.py` — `is_demo=True` 넣던 값 뺌(시드 이름 · 「데모 지점만」 안내는 그대로 두어도 됨 — 시드가 넣는 테넌트가 데모라는 것은 env 값 책임)
- `factory.py:32-37` `ConnectionConfig.is_demo` · 지문
- 그대로: #22 `scripts/seed_demo_board.py`(데모 테넌트 가드 = 시드 도구 대상 제한) · #23 권한 이름 표

### D4 — 테스트 (리포트 §3)
- 바뀜(가): `tests/day/emr/test_kos_board_contract.py:84,93-100,121-124,181-205,208-221` — OPEN/CLOSED 를 「trial 없이 5개 모두 계획 · `write_open` True」로 · `test_kos_client.py:262-284` → 5개 `supports_write` True · 요청 나감 · `test_board_api.py:338-368`(데모 전제 제거) · `:752-773`(운영 연결 not_supported → 운영 연결도 op 쌓임으로 뒤집기) · `tests/deploy/test_day_vm.py:76-77` 삭제
- 바뀜(나): `test_emr_sync_service.py:86-117,120-130` → dev · prod 모두 연결 전부 동기화 · `test_auth_api.py:303-318` → dev 후보도 연결 전부
- 바뀜(다): 픽스처 `tests/day/board/conftest.py:119` · `tests/day/auth/conftest.py:218,231` · `test_constraints.py:153,385` · `test_encryption.py:56` · `test_encryption_canary.py:27` 의 `is_demo=` 인자 · `test_column_snapshot.py:141` 칸 목록
- 그대로: `test_kit.py` · `test_config.py` · `test_startup_key.py` · (미추적) `test_seed_demo_board.py`
- 새로 권장: 「연결 종류 · `APP_ENV` 와 무관하게 5개 쓰기가 같은 op」 한 테스트

### D5 — 데모 실물 확인 (코드 뒤 QA · 마지막)
- DAY dev(데모 지점 연결)에서 `scripts/seed_demo_board.py` 로 시험 방문을 시술 대기까지 넣고, 화면에서 5개 쓰기를 눌러 본다: ① 다시 호출 · 재호출(이미 WAITING · READY 작업에 `call-tasks-doctors`) ② 시작 취소(`PROCEDURE_WAITING` — 확인됨 · 회귀 확인) ③ 완료 취소(`complete=false`) ④ 귀가 대기 1(`cancel-flow-tasks reason=CANCEL`) ⑤ 귀가 대기 2(`PROCEDURE_DONE`)
- 각각: KOS 응답 2xx 여부 · 다음 조회(10초)가 SPEC-002 KOS 쓰기 표 「확인」 칸 값을 주는지 · `external_outbox` 상태(`confirmed` / `failed`)
- 결과 → SPEC-002 OQ-23 닫기(행별 「확인됨」/실패면 그 행 재논의) · ⑤ 때 KOS 웹 화면 단계가 「귀가(`COMPLETED`)」와 어떻게 다른지 보고 OQ-22 에 사실 기록 — spec-sync 로 반영

## 미결 · 주의점
- `log.md` 새 3행의 PR 칸 = 「PR 미정 — 근거 …report.md」. 코디가 PR 올릴 때 PR 번호(#NNN)로 바꿔 주면 규칙(PR 칸 = 닿는 링크)에 맞는다.
- D2 #17 ~ #20 은 「연결 무관」이라 남기는 쪽으로 적었다 — 브리프가 (나) 8 자리 전부를 WP 로 하라고 했으므로 코디 확인 권장.
- 열린 것: SPEC-000 OQ-01-2 · OQ-01-3 · SPEC-002 OQ-22 · OQ-23 · deployment.md 미결 「prod 스키마의 실제 병원 연결」.
- `20-spec.md` · `30-work.md` 는 앱 워크트리(`day-app`)와 겹칠 수 있다 — 이번 변경은 `20-spec.md` 최종 수정 날짜 한 줄뿐 · `30-work.md` 무변경.
