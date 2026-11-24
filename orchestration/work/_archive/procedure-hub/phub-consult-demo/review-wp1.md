# 검수 — SPEC-010 WP-1 코드(kos_map · 설정 · 장부 칸) · 2026-11-20

reviewer 워커 · 읽기만(수정 0) · 대상 `clinic_chat/phub-consult-demo` 미커밋 변경(고친 파일 6 + 새 파일 3) · 정본 SPEC-010 0.2.3 §3 JS1 ~ JS6 · §2-3 · §9-1 · §13 WP-1 행 · 리포트 `wp1-report.md`.

## 판정 — **PASS**(P0 0 · P1 0 · P2 6)

WP-1 완료 조건 셋(`test_v05_kos_map.py` 통과 · 실물 v3 로 시작 성공 · 꼴 어긋난 사본으로 시작 실패)을 다시 확인했다. 스펙 계약과 코드도 맞다. P2 는 다음 WP 와 함께 고치거나 스펙에 한 줄 올리면 된다.

## 1. 다시 돌린 것

| 명령 | 결과 |
|---|---|
| `pytest -q tests/test_v05_kos_map.py` | **30 passed** |
| 리포트의 0.4 관련 22 파일(`test_consult_{page,chat_ui,prompt,turn,ledger,material,sites,listing,carry}` · `test_v03_{frame,start,fixes,prompt,sites}` · `test_v04_{ledger,start,turn,list,verify,understand}` · `test_state_{blanks,carry}`) | **158 passed**(리포트의 188 = 이 158 + kos_map 30 · 셈 맞음) |
| `ruff check` 손댄 7 파일 | All checks passed |
| 깨기 18 가지를 `km.check` 에 바로 넣고 오류 글 확인(스크래치 · 파일 0) | **18 가지 모두 의도한 검사에서 실패**(version → `meta.version` · item_count → `items count 5 != 6` · ref_missing → `option_refs not in products` · refs_ne_covers → `option_refs and covers differ` · face_shape / face_no_points → `site shape` · site_parent → `parent_code` · groups_miss / twice → `groups do not cover` …) |
| `$J` sha256 | `1af2216c5a3e…` = 브리프 · 리포트와 같음 |
| 허브 18105 `GET /procedure-hub/gold/health`(읽기만) | `build.gold_hash = caa03560…` = `$J` `meta.hub_gold_hash` → 지금은 `hash_mismatch: false` 가 될 값(리포트 시점은 57b420ad 라 true — 그 뒤 허브가 재기동됨). 칸 경로 `build.gold_hash` 는 JS4 와 같음 |

18222 손대지 않음 · 서버 띄우지 않음.

## 2. 계약 대조

| 계약 | 코드 | 판정 |
|---|---|---|
| JS1 시작 때 한 번 읽기 · 파일 감시 0 | `server.py` `create_app` → `kos_mod.from_settings(s)` 한 번 · `app.state.kos` · `ctx.kos` | 맞음 |
| JS2 꼴 검사(version v3 · items 324 · sites · products · product_categories · option_refs ⊂ options · covers ⊂ items · site_codes ⊂ sites · 얼굴 point/pair + points · 키 유일) | `kos_map.py:102-179` 전부 + 더 엄격(refs ↔ covers 같은 집합 · parent_code · groups 한 번씩 · region) | 맞음(더한 검사는 실물 통과 · 막지 않음) |
| JS3 sha · 장부 시작 줄 `kos_map{sha, made_at, hub_gold_hash}` · `CHAT_KOS_MAP_SHA` 다르면 실패 | `ledger.py:152-153` · `server.py:79` · `kos_map.py:233-242` | 맞음(앞 8 자 이상 비교는 확장 — P2-3) |
| JS4 `build.gold_hash` 다르면 시작은 하고 장부 `hash_mismatch: true` · 화면 문구 0 | `kos_map.py:263-274` · `server.py` `hub_health` | 맞음 · 패널 표시는 WP-2 로 넘김(리포트 §4 · `app.state.kos_check` 에 값 있음) |
| JS5 색인 여덟 · `groups` 순서 | `kos_map.py:182-230` · 시험 `test_indexes_on_fixture` · 실물 셈(케이스 137 · 옵션 493 · 옵션 0 진료항목 24) | 맞음 |
| JS6 오류 글 · 장부에 가격 0 | 오류 글 = 코드 · 키 튜플만 · `stamp()` 칸 셋 · 시험이 장부 원문에 `price_amount` · `event_price` 0 확인 | 맞음 |
| §2-3 env 여섯 | `config.py:102-109` · `.env.example` | 맞음 + `CHAT_KOS_MAP_ITEMS` 하나 더(P2-2) |
| 0.4 회귀 | `conftest.make_settings` 가 고정본을 기본으로 넣음 → `create_app` 부르는 시험(`state_fixture.py` · `test_consult_*` · `test_v03_frame`)은 모두 `make_settings` 를 거침 · `clinic_chat/web/server.py` 의 `create_app` 은 건드리지 않음 · `Ctx.kos` 기본 None | 회귀 0 |
| 코드 규약(0.4 꼴) | 모듈 하나 · 데이터클래스 · 오류는 도메인 예외(`KosMapError`) · 0.4 `prompt.load` 와 같은 「꼴 틀리면 시작 실패」 꼴 | 맞음(P2-5 하나) |

## 3. 지적

### P2-1 깨기 시험이 실패 **까닭**을 단언하지 않는다
- `tests/test_v05_kos_map.py:99-105` — `"kos_map:" in str(e.value)` 만 본다. 지금은 18 가지가 모두 맞는 검사에서 실패했다(§1). 그런데 검사 하나를 지워도 다른 검사가 대신 잡아 시험이 그대로 통과한다. 예: `item_count` 검사를 지우면 `items.pop()` 을 groups 검사가 잡고, `cover_missing` · `ref_missing` 검사를 지우면 refs ↔ covers 검사가 잡는다. 그래서 「JS2 각각 실패」(§9-1)를 지키는 힘이 약하다.
- 고칠 방향: `BREAKS` 값을 `(변형, 기대 글 조각)` 쌍으로 바꾸고 `assert 조각 in str(e.value)` 를 넣는다(예 `"items count"` · `"covers not in items"` · `"option_refs not in"`).

### P2-2 `CHAT_KOS_MAP_ITEMS` 는 스펙 밖 칸이고 0 이면 수 검사를 끈다
- `config.py:105` · `kos_map.py:260`(`s.chat_kos_map_items or None`) — 운영 `.env` 에 0 을 넣으면 JS2 「items 324」 검사가 꺼진다. 리포트 §4 가 이미 스펙 반영 여부를 코디 판단으로 올렸다.
- 고칠 방향: (가) 스펙 §2-3 에 「시험 고정본 전용 · 0 = 끔」 을 한 줄 올린다. 또는 (나) env 칸을 없애고 `make_settings` 에서만 `kos_map.N_ITEMS` 를 덮는다. 코디가 고른다.

### P2-3 sha 앞자리 비교는 JS3 의 확장이다
- `kos_map.py:233-237` — 스펙은 「주면 sha256 이 같아야」 라고만 한다. 코드는 앞 8 자 이상이 맞으면 통과시킨다. 코디가 쓰는 값(`1af2216c`)이 8 자라 실제로 이 경로를 탄다.
- 고칠 방향: 코드는 그대로 두고 스펙 §2-3 `CHAT_KOS_MAP_SHA` 줄에 「앞 8 자 이상 = 앞자리 비교」 를 올린다.

### P2-4 JS2 검사가 꼴이 아주 틀린 입력에서 `KosMapError` 가 아닌 예외를 낸다
- `kos_map.py:119` · `124` · `133-139` · `206` — `items` · `products` · `options` 원소가 객체가 아니면 `AttributeError`, `groups[].kos_procedure` 가 없으면 `build` 에서 `KeyError` 가 난다(`check` 가 이 칸을 보지 않는다). 시작은 어쨌든 실패하므로 동작은 맞다. 다만 「꼴 틀림 = `KosMapError`」 계약과 어긋나고, 깨기 시험에도 없다.
- 고칠 방향: 원소마다 `isinstance(…, dict)` · `groups[].kos_procedure` 문자열 검사를 `check` 에 더한다. 깨기 시험도 한 줄씩 더한다.

### P2-5 허브 health 를 새 urllib 로 부른다(0.4 클라이언트를 안 씀)
- `server.py` `hub_health()`(diff 끝 · 함수 안 import 둘) — 0.4 에는 이미 `clients/hub_rest.py:204` `health()` 가 있다(비동기 · httpx). 시작 때 한 번 부르는 동기 호출이라 따로 둔 것으로 보이고, 동작은 맞다(경로 = `hub_rest_url + /health` = `/procedure-hub/gold/health`).
- 고칠 방향: 지금 고칠 것은 없다. 허브 호출 길을 한 곳에 모으려면 WP-3(허브 호출 묶음)에서 `HubRest.health` 를 동기로 감싸 쓴다. 그러지 않을 거라면 그대로 두고 주석에 까닭을 한 줄 남긴다.

### P2-6 허브를 못 불렀을 때 장부에서 원인이 사라진다
- `server.py:79` — 장부에는 `sha · made_at · hub_gold_hash · hash_mismatch` 넷만 복사한다. 허브가 꺼졌을 때(`hub_error`)와 대조를 아예 안 했을 때(`health=None`)가 장부에서는 둘 다 `hash_mismatch: null` 로 같아 보인다. JS3 · JS4 칸 정의 안이라 계약 위반은 아니다.
- 고칠 방향: (선택) `hub_error` 가 있을 때만 장부 `kos_map` 에 같이 남긴다. 또는 WP-2 패널에서 `app.state.kos_check` 전체를 보인다.

## 4. 운영 메모(지적 아님)
- 앱 워크트리 `.env` 에 **`CHAT_KOS_MAP` 줄이 없다**(키 이름만 grep · 값은 보지 않음). 이 변경이 들어간 뒤 18222 를 다시 띄우면 시작에 실패한다. 재기동 전에 코디 · 사용자가 `CHAT_KOS_MAP=data/kos/myeongdong-mapping-20261120-v3.json`(+ `CHAT_KOS_MAP_SHA=1af2216c`)을 넣어야 한다. 리포트 §4 와 같은 내용이다.
- `.env.example` 의 빈 int 줄(`CHAT_KOS_MAP_ITEMS=` 등)을 `.env` 에 그대로 옮기면 pydantic int 해석이 실패한다. 0.4 의 `CHAT_PICK_LIST_MAX=` 와 같은 기존 꼴이라 이번 지적에서는 뺐다.
