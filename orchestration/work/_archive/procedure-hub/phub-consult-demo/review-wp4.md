# 검수 — WP-3 고침 재검수 + SPEC-010 WP-4 코드 · 2026-11-20

reviewer 워커 · 읽기만(수정 0). 앱 워크트리 `clinic_chat/phub-consult-demo` 미커밋 변경 · 정본 SPEC-010 0.2.7 · 리포트 `wp3-fix-report.md` · `wp4-report.md` · 스크린숏 `wp4-shots/`. 허브 18105(gold caa03560)는 GET 만 했다 · 서버 띄움 0 · 18222 손대지 않음.

## 판정

| 대상 | 판정 |
|---|---|
| **WP-3 고침**(`review-wp3.md` P1 1 · P2 5) | **PASS** — P1-1 · P2-1 ~ P2-4 닫힘 · P2-5 는 코디 몫(스펙 옮기기) · 새 지적 P2 1 |
| **WP-4**(모달 · 그림) | **PASS**(P0 0 · P1 0 · P2 4) — 다만 **배포 전 필수 하나**(§3 B-1: 명동점이 쓰는 방법 그림 10 장이 허브 레포에 커밋되지 않았다) |

## 1. 다시 돌린 것

| 명령 · 확인 | 결과 |
|---|---|
| `pytest -q tests/test_v05_modal.py tests/test_v05_images.py tests/test_v05_detect.py tests/test_v05_ask_axis.py` | **64 passed** |
| v05 page · kos_map + 0.4 `test_consult_page`(T17) · `chat_ui` · `v03_frame` · `v03_start` · `consult_ledger` · `v04_ledger` + WP-3 회귀 목록(`consult_turn` · `v04_list` · `consult_listing` · `consult_carry` · `state_carry` · `v04_prompt` · `v04_verify` · `v04_understand` · `v04_turn` · `answer_key`) · `state_blanks` | **168 passed · 1 skipped**(T17 통과 — 앞 검수의 실패 닫힘) |
| 명동점 케이스 137 전부 허브 `facets profile` GET(스크래치 스크립트) → 원리 · 방법 코드 → 그림 폴더 대조 | 원리 코드 26 · 방법 코드 26 · **파일 없음 0** · 원리 코드 빈 시술 = PRC-020(태반주사 — IM9 대로 figure 0) |
| 그림 폴더(허브 레포 `assets/procedure-images/images/`) 정규식 파일 수 | 원리 55 · 방법 66(IM13 기대와 같음) |
| 허브 레포 `git status assets/procedure-images` | **미추적 18 장**. 그 가운데 명동점이 쓰는 것 10 장: MET-008 · 110 · 111 · 112 · 113 · 114 · 117 · 120 · 122 · 124(B-1) |
| 스크린숏 `1-jurek-zomn-desc.png` | 시안 꼴(태그 「시술 원리」 · 「시술 방법」 · 글 · 그림) 맞음 · 방법 글에 큐레이터 메모가 보임(P2-W4) |

## 2. WP-3 고침 대조

| 지적 | 코드 | 시험 | 판정 |
|---|---|---|---|
| P1-1 허브 오류 → 목록 0 · D1 이 조건 지움 | `detect.py` `value_set` 이 오류면 `None` 을 돌려 그 칸 합집합에서만 빼고, 칸 전부가 오류면 교집합에서 뺀다 · 국가 칸도 같다 · `Detector.errors` 를 턴 동안 모은다. `turn.py` `_detect` 는 `det.errors` 가 있으면 decide 결과를 버리고 주제 · 조건 · 목록을 앞 그대로 둔다 + `items.hub_error` · `topic.hub_error` · `items` 조각 0 · 축 0 | `test_hub_error_drops_that_basis_only`(고침) · `test_hub_error_one_value_of_slot` · `test_p1_1_hub_error_turn_keeps_topic_conditions_and_list` | **닫힘**(코디 판단 「그 턴은 그대로」 와 같음) |
| P2-1 한도가 화면에만 | `topics.visible_prev` 하나를 화면 · 턴 메시지 주제 블록 · 검증 앞 주제 id · decide 규칙 되돌림 · TP11 이 같이 씀 | `test_p2_1_return_targets_only_within_limit` | **닫힘** |
| P2-2 빈 첫 주제 | `topics.py:317` 새로 만든 주제가 막혀 빈 칸이면 지움(TP1) | `test_p2_2_first_turn_all_blocked_makes_no_topic` | **닫힘** |
| P2-3 T17 | `modal.py` 상수 이스케이프 | T17 통과 | **닫힘** |
| P2-4 국가 호출 상한 | `country(…, among=다른 칸 교집합)` · 실물 C5 63 → 5 호출 | `test_country_asks_only_products_of_other_slots` | **닫힘**(국가만 말한 턴은 여전히 62 · 첫 턴만 · 캐시 뒤 0 — 그대로 둬도 됨) |
| P2-5 스펙 옮기기 | 코드 그대로 | — | 코디 몫(리포트 §1 P2-5 목록 · 새 넷 포함) |

### P2-W3 (새) decide 뒤 목록 재셈에서 난 허브 오류는 턴을 막지 않는다
- `turn.py` `_detect` — `det.errors` 는 `decide` 바로 뒤에 한 번만 본다. 그다음 `res = await det.items(cur["conditions"])`(장부 `by` · `dropped_reach` 용)가 새 호출을 하다 오류가 나면 주제 바뀜은 그대로 쓰이고, 오류는 `items.errors` 에만 남는다. 예: LLM `to` 로 되돌린 앞 주제(`cond_dropped` 길은 decide 안에서 셈 0)의 고민이 캐시에 없을 때다. 목록 코드는 저장 상태를 쓰므로 화면은 맞다. 장부 `by` 만 비게 된다.
- 고칠 방향: 영향이 작아 지금은 둬도 된다. 맞추려면 `hub_error` 판정을 이 재셈 뒤로 옮기거나, 이 재셈의 오류에도 `items.hub_error` 를 붙인다.

## 3. WP-4 계약 대조

| 계약 | 코드 | 판정 |
|---|---|---|
| §4-5 `$J` 칸(kind · name · code · kind2 · site = IL4 · drug · device · 게시 배지) | `modal.base` | 맞음 |
| lead · 원리 글 · 코드 = 케이스 profile 의 물려받은 시술 행(`layer.holder.holder_table = procedure` · N5) · 시술 여럿 = `hub.procedure_codes` 순서 · 같은 원리 한 번(IM5) | `modal.py:88-89` · `131-153` | 맞음 |
| 방법 = 케이스 행 `method_codes`(` · `) ↔ `method_texts`(`\n`) 같은 자리 · 케이스 순서 → 안 순서 · 같은 코드 한 번(MD1 · IM6 · WH1 · WH2) | `modal.py:80-87` | 맞음(실물 방법 둘인 케이스 5 / 5 = silver 순서 · 리포트) |
| 효과 = `effect_code` 있는 줄만(N3 · 경과 줄은 `course` 로 따로) · 부작용 = `polarity` 「발생함」 만(N4) · 같은 코드 먼저 나온 케이스 · `data-case` | `modal.py:90-118` | 맞음 |
| MD2 케이스 0 = 허브 칸 0 · 호출 0 · MD3 오류 = 허브 칸 0 + `error` · 캐시 안 함 · 다시 부름 | `modal.py:68-69` · `119-130` · `_rows` | 맞음 |
| MD4 조각 · 장부 `viewed{code, figs, error}` · RT1 쿼리 값 | `server.py` `item_modal`(`/c/<id>/item?code=` — §4-9 · RT1 에 맞춘 꼴 · 리포트 G2) | 맞음(MD4 경로 문구만 스펙 고침 거리) |
| IM1 · IM2 표 둘 · 정규식 · 표 ↔ 접두어 · `..` · 확장자 · 폴더 밖 링크 404 · `image/svg+xml` · `nosniff` · 폴더 빔 = 404 · 그림 칸 숨김 | `images.file_of` · `server.py` `image` · `image_on` | 맞음 |
| IM3 요청마다 있음 판단 · `no-cache` · ETag sha256 앞 16 · 304 | `images.present` · `etag` · 라우트 | 맞음 |
| IM8 파일 없음 = img 0 + 빈 `pm-fig-missing` · IM9 코드 없음 = figure 0 · IM10 alt = slot `fig-alt` | `modal_body.html` · 시험 | 맞음 |
| IM12 장부 `figs` · IM13 시작 셈 · 로그 | `modal.figs` · `server.py:85-86` | 맞음(55 · 66) |
| 실물 표본 셋(케이스 1 · 여럿 · 0) · 그림 빠짐 0 | 리포트 §3 + 위 독립 대조 | 맞음 |
| 장부 가격 0 | `viewed` 칸 = 코드 · figs · error | 맞음 |
| 0.4 회귀 · T17 | §1 | 맞음 |

## 4. 지적(WP-4)

### B-1 (배포 전 필수 · 코드 지적 아님) 명동점이 쓰는 방법 그림 10 장이 허브 레포에 커밋되지 않았다
- 코디 G1 은 「허브 레포 `assets/procedure-images/images/` · 허브와 함께 배포됨」 이다. 그런데 그 레포에서 `git status` 미추적이 18 장이고, 명동점 케이스가 쓰는 MET-008 · 110 · 111 · 112 · 113 · 114 · 117 · 120 · 122 · 124 가 그 안에 든다. 지금 로컬에서는 빠짐 0 이다. 하지만 허브 레포를 커밋 · 배포하는 길로는 이 10 장이 가지 않는다(IM4 바인드 마운트 자리에서 빠짐 → IM8 빈 그림).
- 고칠 방향: 허브 레포 작업(WP-H 쪽 · 코디 · 사용자)에서 18 장을 커밋한다. 배포 체크(WP-7)에 「`git ls-files` 기준 정규식 파일 55 · 66」 을 넣는다.

### P2-W1 `CHAT_IMAGE_DIR` 기본값이 코드에 박힌 개인 절대 경로다
- `clinic_chat/config.py:108` — `"/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-consult-demo/assets/…"`. 스펙 §2-3 기본은 「비면 그림 칸 숨김」 이고, 다른 경로 칸은 env · `ROOT` 상대로 둔다. 이 기본값 때문에 `tests/conftest.py` `make_settings` 는 그림 폴더를 넘기지 않는 모든 시험(page · detect · 0.4)을 이 개인 폴더에 기대게 한다(이 기계에서만 `image_on = True`). stg 컨테이너에서는 이 경로가 없어 조용히 숨김이 된다.
- 고칠 방향: 코드 기본은 `None` 으로 되돌린다. 경로는 `.env`(로컬) · 배포 env(IM4)에 둔다. `make_settings` 기본에 `chat_image_dir=None` 을 넣는다. 코디 G1 은 「자리」 결정이므로 env · README 로 충분하다.

### P2-W2 모달 캐시 키의 gold 해시가 허브 실물이 아니라 `$J` meta 값이다
- `server.py` `item_modal` → `modal_mod.build(kos, d.hub, kos.hub_gold_hash, …)`. 스펙 MD3 키는 (gold_hash, 노드, facet)다. `$J` meta 해시와 허브 실제 해시가 다를 때(JS4 `hash_mismatch` 상황)는 허브를 재기동해도 앱을 재기동하기 전까지 옛 응답을 쓴다.
- 고칠 방향: 시작 때 `kos_check.hub_build_gold_hash`(있으면)를 키로 쓴다. 어긋남 자체는 이미 JS4 로 표지되므로 낮은 우선이다.

### P2-W3 → §2(WP-3 쪽)

### P2-W4 방법 글 14 / 66 에 큐레이터 메모가 손님 화면에 그대로 나온다(데이터 · 사용자 판단)
- WH2 계약대로 `method_texts` 는 silver `method.csv` `description` 원문이다. 그런데 66 가운데 **14** 가 「원장은 … 로 적는다」 · 「원장에 영어 표기만 있어 name_ko 도 원장 표기」 같은 **정리자 메모**를 품는다. 스크린숏 `1-jurek-zomn-desc.png` 「시술 방법」 에 「원장은 정맥 투여와 나란히 고르는 길로 적는다(「정맥 또는 근육 주사」)」 가 보인다.
- 고칠 방향: 코드는 계약대로라 고칠 것이 없다. 사용자 · 코디가 정한다. (가) silver `method.csv` 에 손님용 글 칸을 따로 두거나 메모를 다른 칸으로 옮긴다(데이터 워커 · WP-H 재빌드). (나) 그대로 둔다(PoC). 「화면 문구 지어 넣지 않기」 원칙상 앱이 잘라 내는 것은 안 된다.

## 5. 남은 것(지적 아님)
- 스펙 고침 거리(코디): IM1 · D-19 · IM4 의 그림 자리 문구(옛 시드 → 허브 레포) · MD4 경로 꼴(`?code=`) · WP-3 고침 P2-5 목록.
- 경과(`course`) · 「보고 없음 / 해당 없음」 부작용 · `viewed` → LLM 블록은 WP-6(리포트 G5 · G6).
