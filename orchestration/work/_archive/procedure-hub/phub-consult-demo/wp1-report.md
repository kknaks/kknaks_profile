# WP-1 리포트 — kos_map(매핑 JSON v3) + 설정 + 장부 칸 (app 워커 · 2026-11-20)

발주 `task_ce6642ccaaa8` · `ctx_7b0b649b3a5a` · SPEC-010 0.2.2 §3 · §2-3 · §13 WP-1. 커밋 0 · push 0 · 18222 손 안 댐(pid 그대로) · 시험 서버는 18299(끝에 내림).

## 0. 착수 중 바뀐 것 — `$J` sha

작업 도중 두 경로(앱 `data/kos/` · 메인 로컬)의 v3 가 **`94b88022…` → `1af2216c5a3ed2806936777314ad4fbdc1ca8e70b78fee99ad387ac5f0e26568`**(16:51)로 바뀌었다(WP-H 의 WH5 로 보임). meta `hub_gold_hash` = **`caa03560…`** · `made_at` 16:51:06 · items 324 · 옵션 493 · groups 131 · sites 71(꼴 검사 · 색인 수 같음). 허브 18105 는 아직 `57b420ad`(재기동 전) → 실물 시작에서 JS4 `hash_mismatch: true` 가 그대로 찍힌다(아래 §3). 시험은 실물 sha 를 박지 않고 파일에서 셈한다.

## 1. 바뀐 파일

| 파일 | 무엇 |
|---|---|
| `clinic_chat/consult/kos_map.py`(새) | JS1 `load` / `from_settings`(비면 · 없으면 · JSON 아니면 · 꼴 틀리면 `KosMapError`) · JS2 `check`(아래) · JS3 `file_sha` · `sha_matches`(전체 또는 앞 8 자 이상) · `KosMap.stamp()` · JS4 `hash_check(kos, health)` · JS5 색인 여덟 `item` · `by_case` · `by_proc` · `by_product` · `by_site` · `by_kos_procedure` · `site_children` · `option` / `option_product` / `covers_of` + 도움 `descendants` · `ancestors` · `sort_codes` · `order`(코드 목록은 늘 `groups` 순서). 가격 칸은 색인에만 있고 오류 글 · 장부에 0(JS6) · `items[].options`(v2)는 안 읽음(D-20) |
| `clinic_chat/config.py` | `chat_kos_map` · `chat_kos_map_sha` · **`chat_kos_map_items`(기본 324 · 0 = 수 검사 안 함 — 스펙 밖 칸 · 시험 고정본용)** · `chat_image_dir` · `chat_kos_llm_items_max`(30) · `chat_rec_max`(2) · `chat_ask_list_min`(4) |
| `.env.example` | 위 env 일곱 빈 줄 + 설명 |
| `clinic_chat/consult/server.py` | `create_app` 이 시작 때 `$J` 를 읽음(실패 = 시작 실패) · 인자 `hub_health` 로 JS4 · `app.state.kos` · `app.state.kos_check` · `Ledger.kos_map` 설정 · `main()` 은 허브 `GET {HUB_REST_URL}/health`(3 초) 를 넘김 · 새 함수 `hub_health(s)` |
| `clinic_chat/consult/ledger.py` | `Ledger.kos_map` 칸 · 시작 줄에 `kos_map{sha, made_at, hub_gold_hash, hash_mismatch}`(JS3 · JS4) |
| `clinic_chat/consult/turn.py` | `Ctx.kos: KosMap | None`(뒤 WP 가 씀 · 기본 None — e3 · e5 · e6 그대로) |
| `tests/conftest.py` | `make_settings` 기본값에 `chat_kos_map` = 고정본 · `chat_kos_map_items = 6`(모든 0.4 시험 서버가 고정본으로 뜸) · `KOS_FIXTURE` · `KOS_FIXTURE_ITEMS` |
| `tests/kos_fixture/kos_map_v3_small.json`(새) | **지은 값만**의 작은 v3(진료항목 6 · 상품 6 · 옵션 8 · single / group · 판매 종료 상품 · 0 원 옵션 · 케이스 여럿 · 케이스 0 둘 · RT1 꼴 코드 `ZZ IV DRIP + VIT` · `ZZ-시트` · `ZZ--` · 얼굴 point / pair · 몸 list · 부위 3 단). 실물 `$J`(git 무시 · 공개 레포)는 넣지 않았다. `tests/data/` 는 `.gitignore` `data/` 에 걸려 `tests/kos_fixture/` 로 둠 |
| `tests/test_v05_kos_map.py`(새) | 30 시험(아래) |

**JS2 꼴 검사 항목**: 칸 여섯(meta · items · groups · sites · products · product_categories) · `meta.version == v3` · items 수(`CHAT_KOS_MAP_ITEMS`) · 코드 빈 값 · 중복 · `product_key` · (상품, `option_key`) 유일 · 옵션 type ∈ single · group · `covers` ⊂ items · `option_refs` ⊂ 옵션 · **`option_refs` ↔ `covers` 같은 집합**(실물 551 = 551) · `site_codes` ⊂ sites · 얼굴 = point / pair + 빈 points 0 · 그 밖 = body · `parent_code` ⊂ sites · `groups` 가 items 를 한 번씩 · `hub` 객체. 「삭제 제외본」 은 v3 가 거른 것이라 따로 검사하지 않는다.

## 2. 시험

| 명령 | 결과 |
|---|---|
| `.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_v05_kos_map.py` | **30 passed**(색인 여덟 · 부위 걷기 · stamp 가격 0 · JS2 깨기 18 가지 각각 실패 · 빈 / 없는 / JSON 아닌 파일 · 오류 글 가격 0 · sha 전체 / 앞자리 / 틀림 · JS4 같음 / 다름 / 허브 오류 / 칸 없음 · 서버 시작 실패 셋 · 서버 시작 + 가짜 턴 → 시작 줄 `kos_map` · 장부에 가격 칸 0 · 실물 v3 적재 · 실물 서버 시작 · **실물 사본 깨면 시작 실패**) |
| 위 + 0.4 관련 22 파일(`test_consult_{page,chat_ui,prompt,turn,ledger,material,sites,listing,carry}` · `test_v03_{frame,start,fixes,prompt,sites}` · `test_v04_{ledger,start,turn,list,verify,understand}` · `test_state_{blanks,carry}`) | **188 passed / 11.8 초** |
| `ruff check` 손댄 7 파일 · `ruff format` 새 2 파일 | 통과 |

- 걸렸다 고친 것: 0.4 T17(「주석 밖 한글 0」 — `test_consult_page`)이 `kos_map.py` 오류 글의 한글을 잡음 → 오류 글을 영어로 바꿈.
- 전체 pytest 는 돌리지 않았다(D-8 · WP-7).

## 3. 실물 시작 확인(빈 포트 18299 · 끝에 내림)

| 무엇 | 결과 |
|---|---|
| `CHAT_KOS_MAP=data/kos/…-v3.json CHAT_KOS_MAP_SHA=1af2216c CHAT_FAKE_TURN=true python -m clinic_chat.consult --port 18299` | 뜸 · `GET /` 200 · 가짜 턴 `POST /c/wp1real00000001/turns` 200 |
| 장부 시작 줄 | `kos_map{sha: 1af2216c…, made_at: 2026-11-20T16:51:06+09:00, hub_gold_hash: caa03560…, hash_mismatch: true}` — 허브 `/health` = 57b420ad(재기동 전) → JS4 대로 시작은 하고 표지 |
| `CHAT_KOS_MAP` 빔 | `KosMapError: CHAT_KOS_MAP is empty`(시작 실패) |
| `CHAT_KOS_MAP_SHA=94b88022`(옛 sha) | `KosMapError: sha256 1af2216c5a3ed280 != CHAT_KOS_MAP_SHA` |
| v2 파일(`…20261120.json`) | `KosMapError: missing key: products` |

## 4. 다음 WP 메모

- **18222 재기동 때 env 필요**: 이제 `CHAT_KOS_MAP` 이 비면 0.5 서버가 뜨지 않는다. 사용자 `.env` 는 손대지 않았다 → 코디 · 사용자가 `CHAT_KOS_MAP=data/kos/myeongdong-mapping-20261120-v3.json`(+ 원하면 `CHAT_KOS_MAP_SHA=1af2216c…`)을 넣어야 한다. 허브를 caa03560 판으로 재기동하면 `hash_mismatch: false` 가 된다.
- JS4 패널(`CHAT_DEBUG_PANEL=on`) 표시는 **WP-2**(값은 `app.state.kos_check` 에 있음).
- 뒤 WP 는 `ctx.kos`(턴) · `app.state.kos`(라우트)로 색인을 쓴다. 코드 목록은 늘 `groups` 순서 · 부위 자손 / 조상은 `descendants` / `ancestors`(SF2 · SF3 · FS4).
- 0.4 시험 서버는 모두 고정본(진료항목 6)으로 뜬다 — WP-2 이후 화면 시험이 고정본 값을 기대값으로 쓸 수 있다(RT1 꼴 코드 셋 포함).
- `chat_kos_map_items` 는 스펙 §2-3 에 없는 칸이다(시험 고정본이 JS2 「items 324」 를 지나게) — 스펙 0.2.3 에 한 줄 올릴지 코디 판단.
