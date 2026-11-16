# 리뷰 리포트 — WP28 끊김 기본값 2000 · -0.3 (D-67) / code (2026-11-16)

대상: 워크트리 `tongky-quality-re1` 미커밋 변경(base `6d57ba3`) — `back/app/service/interpret/soniox.py` · `back/scripts/quality_check.py` · `back/tests/test_quality.py` (3파일 · untracked 0)
SSOT: SPEC-001 0.9.4 §5.10 · §9.1 「STT 설정」 · §4.6.1 · §2.4 / DEC D-67 / WORK WP28

## 판정: PASS (WARN 1 · 참고 1)

FAIL 없음. 기본 설정 · 끊김 값을 쓰는 곳 · 재연결 길 · 시험이 SPEC 0.9.4 와 맞는다.

## 확인 결과 (SPEC 항목별)

| 항목 | 근거 | 결과 |
|---|---|---|
| 기본 `max_endpoint_delay_ms` = 2000 | §5.10 「운영 값」 · D-67 | 같음 — `soniox.py:33` · 기본 설정에 들어감 `soniox.py:64` |
| 기본 `endpoint_sensitivity` = -0.3 (새 키) | §5.10 · D-67 | 같음 — `soniox.py:34` · `soniox.py:65` |
| `endpoint_latency_adjustment_level` 안 보냄 | §5.10 「운영 값」 | 같음 — 기본 dict 에 없음(`soniox.py:57-67`) · 품질 시험 덮어쓰기용 `ENDPOINT_KEYS`(`soniox.py:36`)에만 있음 = WP28 「덮어쓰기 길 그대로」 |
| 다른 키 · 키 순서 그대로 | §5.10 「그 밖의 STT 설정」 · §9.1 | 같음 — diff 는 `soniox.py:65` 한 줄 추가뿐. 순서 `max_endpoint_delay_ms` → `endpoint_sensitivity` → `translation` |
| env 아님 · 코드 상수 | §2.4 · §5.10 | 같음 — `config.py` · `.env.example` 변경 없음 |
| 주석 「= Soniox 기본」 오기 바로잡기 | WP28 ② | 고쳐짐 — 옛 주석(「다른 끊김 값은 보내지 않는다(= Soniox 기본)」) 삭제 · `soniox.py:30-32` 가 §5.10 · D-67 을 가리킴. 새 문구 「2000 = Soniox 기본값과 같지만」 은 사실(공식 기본 2000 — SPEC §5.10 공식 문서 표) |
| 덮어쓰기 길 | §9.1 「품질 시험의 끊김 값 인자를 주면 그 값이 나간다」 | 같음 — `soniox.py:68-72` 변경 없음(기본 위에 `update`) · 밖 키는 ValueError 그대로 |
| 시험이 새 기본을 고정 | §9.1 「STT 설정」 | 고정함 — `test_quality.py:66-69` dict **전체 동등**(2000 · -0.3 포함 · 빈 단언 아님) · `:70-72` 키 순서 · `:73-74` `endpoint_latency_adjustment_level` · `enable_agent_text_input` 키 없음 · `:86-90` 덮어쓰기(둘 다 · 하나만 — 나머지 기본 -0.3 유지) · `:93` 인자 None = 기본 |
| `uv run pytest` (back) | WP28 검증 | **489 passed** · 1 warning(starlette `httpx` deprecation — 무관 · 기존) |
| `uv run ruff check .` (back) | WP28 검증 | **All checks passed!** |
| 허용 경로 | WP28 「back soniox.py · scripts/ · tests/」 | 지킴 — 3파일 모두 범위 안 · front · seed · infra 변경 0 |

`git grep -n -E "MAX_ENDPOINT_DELAY_MS|max_endpoint_delay_ms|endpoint_sensitivity|ENDPOINT_KEYS|ENDPOINT_SENSITIVITY|endpoint_latency_adjustment_level"` 로 센 자리 전부: `soniox.py:31-36,64-65` · `quality_check.py:89-91,466-467,607-608,926` · `test_quality.py:68-73,86-90` · `test_quality_script.py:140-142` · `test_quality.py:422,459-460`(세션이 옵션을 넘기는지만 보는 시험 — 값 의미 없음). 기본값을 하드코딩한 다른 자리 없음(`git grep 1000|2000` → `quality_check.py:785` 는 무관한 2초 판정).

## 조용히 통과하는 자리 (따로 봄)

1. **재연결(§4.6.1 「정방향 기본만」)** — PASS. `session.py:197-209` 재연결은 context 만 `forward_only` 로 줄이고 `session.py:217-218` 이 같은 `self._stt_options` 로 `open_stt` → `SonioxStt.open`(`soniox.py:121-128`) → `stt_config` 를 다시 부른다. 기본 두 값은 `stt_config` 안의 상수라 재연결 설정에도 **그대로 들어간다**(따로 복사해 둔 설정 dict 가 없음). 다만 가짜 Soniox 시험은 `open_stt` 를 통째로 바꿔서 재연결 때 실제 나간 JSON 을 보지 않는다 — 구조상 보장이지 시험 고정은 아님(아래 「고객이 실물에서 만날 자리」 1).
2. **품질 시험 결과 기록의 끊김 값** — WARN (아래 W-1).
3. **`--endpoint` 파싱** — `quality_check.py:468` `"-0.3"` → float, `"-1"` → int. 변경 없음 · 영향 없음.

## FAIL

없음.

## WARN

- **W-1 `back/scripts/quality_check.py:606-608` — 결과 기록의 `endpoint` 가 기본값을 손으로 다시 짜 맞춘다(시험 없음).** `stt_config` 의 조립(`soniox.py:64-65` + `update`)을 상수 두 개로 복제했다. 지금은 값 · 덮어쓰기 순서가 `stt_config` 와 같아 맞게 적힌다(WP28 ③ 충족). 그러나 이 필드를 단언하는 시험이 없다(`grep '"endpoint"' back/tests` → `test_quality.py:401` 은 금지 키 목록일 뿐). 나중에 기본 끊김 키가 하나 더 늘면 기록만 조용히 어긋난다 — WP28 ③ 「값을 쓰는 곳은 목록을 믿지 말고 전부」 의 취지. 권고(필수 아님): 실제 설정 `cfg = stt_config(lang, endpoint_config=combo["endpoint_config"])` 에서 `{k: cfg[k] for k in ENDPOINT_KEYS if k in cfg}` 로 꺼내 적거나, 기본 조합의 `endpoint` == `{2000, -0.3}` 시험 1건. 근거: SPEC §9.3 「조합」 끊김 행(기본) · D-67.

## 고객이 실물에서 만날 자리

1. **`endpoint_sensitivity` 를 Soniox v6 실시간이 받는가** — SPEC §5.10 공식 문서 표에 「어느 모델이 받는지는 그 문서에 없다」. 만약 `invalid_request` 로 거절되면 재연결(§4.6.1)도 **같은 키를 다시 보내므로** 거절 → 모든 세션 `soniox_unavailable`. 가짜 Soniox 시험으로는 못 잡는다 → 코디의 실물 연결 1회(WP28 검증) · WP29 배포 뒤 확인에서 반드시 확인. (WP24 C2 는 2000 만 실물로 돌렸고 -0.3 은 실물 미시험 — §5.10 「결과(0.9.0)」)
2. **지연 증가** — 2000 + -0.3 은 말 끝 → 자막 · 음성이 늦어진다(D-55 측정: 2000 만으로 T23 · T25 +900 ~ 1,000 ms). 사용자 실기기 판단(D-67 · §9.6 「배포 뒤 확인 (0.9.4)」 · WP29).

## 참고(기존 부채)

- pytest warning 1건 — starlette `TestClient` 의 `httpx` deprecation. 이번 변경과 무관.
- `test_interpret.py:99-104` `test_configs` 는 끊김 값을 보지 않는다(기존 그대로 · 고정은 `test_quality.py` 가 함 — 중복 불필요).
