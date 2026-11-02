# D-35 결과 보고 — 대만 현지명 시드 반영 · zh-Hant 출력 s2tw + 「激光 → 雷射」

## 상태: done

base main `2b4976b` · 커밋 없음 · `back/**` 만.
실물 결과 JSON: `orchestration/work/interpret-pwa-poc/live-check-d35-2026-10-27.json`(키 · 토큰 0 — 대조 확인)

## 수행 — 파일·모듈 목록

| 파일 | 무엇 |
|---|---|
| `back/seed/glossary.json` | ① 대만명 77 반영 ② zh 대륙 alias ③ 볼뉴머 카테고리 · `version` `2026-10-27.2` → **`.3`** |
| `back/app/service/interpret/langs.py` | ④ `TRADITIONAL_CONFIG["zh-Hant"]` `s2twp` → **`s2tw`** · 새 표 `DISPLAY_REPLACE = {"zh-Hant": {"激光": "雷射"}}` · `to_display` 가 OpenCC 뒤 표를 적용(한 곳) |
| `back/app/service/glossary.py` | entry `source` 에 **`web-research YYYY-MM-DD`** 모양 허용(정규식) — 조사 날짜를 source 에 적으라는 지시를 시드 검사가 받게. 그 밖 값은 지금처럼 오류 |
| `back/tests/test_interpret.py` · `back/tests/test_seed.py` | 아래 |

반영 방법: 리포트 §2 표를 읽는 1회용 스크립트(레포 밖 scratchpad)로 시드를 고치고, 끝에 `validate_seed` 를 통과해야 쓰게 했다.

### ① 대만명 (리포트 §2 · 77/157)

| 규칙(코디 지시) | 결과 |
|---|---|
| zh-Hant `name` = 대만명 | 77 term(이름이 실제로 바뀐 것 61 · 16 은 시드와 같았음 — 喬雅登 · 保柔緹 · 水光針 등) |
| 기존 초안 → `aliases`(「鐳射」→「雷射」) · 대만 별칭도 `aliases` | 겹침 · 이름과 같은 것은 뺌 |
| 독립 출처 2+ → `reviewed: true` · 1개 → `false` | **true 38 · false 39**(리포트 확신 「높음 38 · 보통 39」와 같음) |
| `source: "web-research 2026-10-27"` · `note` = 대표 URL 1개 | 77 모두(표의 첫 URL) |
| 못 찾은 80 은 그대로 · 단 「鐳射」→「雷射」는 전부 | 못 찾은 것 중 鐳射가 있던 2개(ph-020 클라리티2 · ph-023 엑셀V)만 바뀜 · 시드 zh-Hant 전체에 「鐳射」 0 |

괄호 정리(시드는 `name` · `aliases` 에 괄호 금지): 리포트 표기에 붙은 주석 괄호 3개를 뺐다 — ph-003 「玻尿酸 (填充物)」 → `name` 「玻尿酸」(玻尿酸注射 · 填充物注射 는 별칭) · ph-033 별칭 「保妥適(Botox 상표)」 → 「保妥適」 · ph-071 별칭 「黃金樁(港·韓)」 → 「黃金樁」.

예: 울쎄라 `美國音波`(+ 美版超聲刀 · Ultherapy · Ulthera · 極線音波 · 美版音波 · 音波拉提 · true) · 써마지FLX `鳳凰電波`(+ 美版熱瑪吉FLX · Thermage FLX · 熱瑪吉 · 美版電波 · true) · 올리지오 `玩美電波` · 슈링크유니버스 `海芙音波` · 볼뉴머 `海芙電波` · 레이저 `雷射` · 레스틸렌 `瑞絲朗`(false — 출처 1).

### ② zh 대륙 alias

- 써마지FLX zh `aliases` 에 **「热玛吉」** 추가.
- 「美版超声刀」 → 울쎄라는 **이미 울쎄라 zh `name`** 이라(첫 가져오기 결과) 더할 것이 없었다.
- 超声刀 · 韩版超声刀 · 韩版热玛吉 는 zh 에 넣지 않았다(시험으로 막음).

### ③ ph-071 볼뉴머 `category` 스킨부스터 → **기기 리프팅**

### ④ zh-Hant 출력 변환

| 입력(Soniox 간체) | zh-Hant 자막 | yue 자막 |
|---|---|---|
| 激光治疗 | **雷射治療** | 激光治療 |
| 离子导入 | **離子導入**(s2twp 의 「匯入」 아님) | 離子導入 |
| 特色项目 | 特色項目(s2twp 의 「專案」 아님) | 特色項目 |
| 软件 | 軟件 | 軟件 |

TTS 입력은 그대로 간체. 메뉴는 0.4.0 부터 런타임 변환이 없다(시드 원본) — 변경 없음.

## 검증 — 명령과 수치

- 시드 검사: 레포 시드 `validate_seed` 통과(시험 ①)
- `cd back && uv run ruff check .` → All checks passed
- `uv run pytest -q` (전체 1회) → **244 passed**(이전 239 + 5)
  - 새 · 바꾼 시험: zh-Hant 자막 「激光治疗 → 雷射治療」 · 「离子导入 → 離子導入」 · yue 「激光治療」 · zh 간체 · TTS 간체 · `to_display` 「激光 软件 导入 项目 → 雷射 軟件 導入 項目」 / 레포 시드: 울쎄라 美國音波 · 써마지 鳳凰電波 · 초안은 별칭 · zh 「热玛吉」 · 모호어 3개 zh 0 · 볼뉴머 기기 리프팅 · zh-Hant 「鐳射」 0 · web-research 77 · note 가 URL · reviewed true 38 / 검사: `web-research`(날짜 없음) · `web-research 2026-1027` 은 오류 · `web-research 2026-10-27` 통과

### 실물 ⑥ — zh-Hant (시드 `.3` · 기본값 20,251)

| 방향 | 발화 | 결과 | 판정 |
|---|---|---|---|
| 대만 → 한국어 | 「我想打美國音波，效果大概可以維持多久？」 | 「**울쎄라**를 받고 싶은데…」 · 원문 자막 「美國音波」 번체 | ✓ |
| 대만 → 한국어 | 「鳳凰電波一次大概多少錢？」 | 「**써마지FLX** 한 번에 대략 얼마예요?」 | ✓ |
| 대만 → 한국어 | 「我想做美國音波跟鳳凰電波，可以一起做嗎？」 | 「**울쎄라**와 **슈링크유니버스**를…」 | 울쎄라 ✓ · 써마지 ✗ |
| 한국어 → 대만 | 「오늘은 울쎄라 시술을 먼저 하실게요.」 | 「今天先給您做**Ultherapy**。」 | ✗ |
| 한국어 → 대만 | 「써마지는 한 번 받으시면…」(ko 별칭) | 「**鳳凰電波**這個項目…」 · TTS 입력 「凤凰电波…」 간체 | ✓ |
| 한국어 → 대만 | 「울쎄라랑 써마지FLX를 같이 받으셔도 돼요.」 | 「…**Ulthera**和**Somagic FLX**。」 | ✗ ✗ |

- 대만 손님이 말한 대만명 → 한국어는 3/4 맞았다. D-35 이전 zh-Hant 에는 美國音波 · 鳳凰電波 짝이 아예 없었다.
- 한국어 → 대만명은 「써마지」(ko 별칭)만 맞았다. 「울쎄라」 · 「써마지FLX」는 정방향 짝(울쎄라 → 美国音波 · 써마지FLX → 凤凰电波)이 context 에 있는데도 Soniox 가 영문 상표명 · 음역으로 냈다.
- **줄이기는 원인이 아니다**: 기본값 20,251 에서 zh-Hant 는 `terms` 138개가 빠진다(아래 이슈 1). 같은 6문장을 **줄이기 없이**(22,000 · 전체 21,605자 · 거절 없음) 다시 돌려도 결과가 같았다(「Ultherra手術」 · 「Ulthera和Somagic FLX」).
- 표본: 문장 1개씩 · 합성 음성(Soniox TTS — 대만 발화는 zh 음성).

## 계약 대조 — DEC-001 D-35

| 항목 | 판정 |
|---|---|
| 대만명을 zh-Hant `name` · 초안은 `aliases`(「鐳射」→「雷射」) | 같음 |
| 독립 출처 2+ 만 `reviewed: true` | 같음(38) |
| 못 찾은 80 은 그대로 | 같음(「鐳射」만 「雷射」) |
| 대륙 구어는 한 기기로 확정되는 것만(美版超声刀 · 热玛吉) | 같음(美版超声刀 는 이미 name) |
| 모호한 말 넣지 않음 | 같음 — **zh 에서**. 아래 이슈 2 |
| 볼뉴머 → 기기 리프팅 | 같음 |
| zh-Hant 출력 `s2tw` + 「激光 → 雷射」 | 같음(`langs.py` 한 곳) |

SPEC 에 반영할 자리(planner): §5.6 zh-Hant 변환(s2twp → s2tw + 표) · §4.2 entry `source` 값에 `web-research YYYY-MM-DD` 추가.

## 이슈 · 코디가 확인할 것

1. **zh-Hant context 가 기본값을 넘는다** — 대만 별칭이 늘어 역방향 별칭이 190개가 됐다(이전 55). 전체 21,605자 > 20,251 → 줄이기 1단계로 `terms` 138개(ko 대표명 뒤쪽)가 빠지고 **짝은 전부 남는다**. 다른 언어는 줄이기 0(th 19,340 그대로). 21,605자는 실물에서 거절되지 않았다(이전 zh-Hant 한도 22,842). 실측으로는 기본값을 22,842 × 0.9 = 20,557 로 올려도 zh-Hant 는 여전히 줄인다 — 별칭이 더 늘면 줄이기 2단계(역방향 별칭)가 시작된다.
2. **모호어가 zh-Hant 쪽으로 들어왔다** — 규칙 ①(기존 초안은 `aliases`)대로 하면 올리지오 zh-Hant 에 「韓版熱瑪吉」, 슈링크유니버스 zh-Hant 에 「韓版超聲刀」가 별칭으로 남는다. zh-Hant context 는 t2s 를 거치므로 Soniox 에는 「韩版热玛吉 → 올리지오」 · 「韩版超声刀 → 슈링크유니버스」 역방향 짝이 된다. ② 는 zh 만 막으라고 했으므로 손대지 않았다 — 빼려면 시드에서 두 별칭을 지우면 된다.
3. 한국어 → 대만명의 「울쎄라」 · 「써마지FLX」 실패는 코드 · 시드로 더 할 것이 보이지 않는다(짝은 context 안에 있고 줄이기와 무관). 사람 목소리로 로컬 E2E 에서 다시 보기를 권한다.
4. 가져오기 스크립트(`scripts/import_glossary.py`)의 zh-Hant 초안은 여전히 `s2twp` 다(SPEC §4.8 · 한 번만 도는 스크립트라 그대로 뒀다). 다시 가져오는 일이 생기면 「鐳射」가 다시 나온다.

---

## 장애 — 2026-10-27 02:07 운영 통역 중 `invalid_request` (먼저 처리)

### 상태: 원인 확정 · 고침 · 실물 재현으로 확인

로그(운영): `soniox error: error_type=invalid_request request_id=876a69d5-…` · lang=zh-Hant · context 16,464자 · 연결 02:06:10 → **50초 뒤**(설정 확인 2초 창 밖).

### 원인 — TTS keepalive 메시지 모양

- back 의 TTS keepalive 가 **`{}`** 를 보냈다(원형에서 복사한 `SonioxTts.keepalive` — 멈춤 · 말 없음이 20초를 넘으면 10초 주기 루프가 보낸다).
- Soniox 공식 형식은 **`{"keep_alive": true}`**(`tts/rt/connection-keepalive`). `{}` 는 stream_id 없는 스트림 메시지로 본다.
- **실물 확인**: TTS 연결에 `{}` 를 보내면 → `{"stream_id": "", "error_code": 400, "error_type": "invalid_request", "error_message": "Missing stream_id"}`. `{"keep_alive": true}` 는 응답 없음(정상).
- 공식 문서(`api-reference/tts/websocket-api` 「Error handling」 2): 검증 오류는 오류 응답만 보내고 **연결은 유지**한다. 그런데 우리 `speak()` 는 TTS 소켓을 발화 때만 읽고, **stream_id 를 보기 전에 `_check` 로 오류를 올렸다** → keepalive 때 생긴 오류가 소켓에 쌓여 있다가 **다음 발화 TTS 에서** 터져 세션 전체가 `soniox_unavailable` 로 끝났다. 그래서 「연결 50초 뒤 · 2초 창 밖 · 한도와 무관」이었다(첫 TTS 뒤 20초 넘게 쉬었다가 다음 발화).
- 후보 대조: 멈춤 중 STT keepalive(`{"type":"keepalive"}` — 공식 형식 그대로 · 문제 없음) · finalize(공식 제어 메시지) · TTS 텍스트(빈 문자열은 이미 안 보냄 · 길이 · 언어 · 간체 변환과 무관 — 재현에서 같은 텍스트가 고친 코드로는 통과) · zh-Hant 경로(언어와 무관 — keepalive 는 모든 언어에서 같다. zh-Hant 는 그때 쓰던 언어였을 뿐).

### 고친 것 (`back/app/service/interpret/{soniox,session}.py`)

| 무엇 | 어떻게 |
|---|---|
| TTS keepalive | `{}` → **`{"keep_alive": true}`** |
| TTS `speak()` | **다른 stream_id(빈 문자열 포함)의 오류는 그 발화를 끊지 않는다** — 경고 로그 1줄(`soniox tts stray error: error_type · request_id · message`) 뒤 계속. 자기 stream_id(또는 stream_id 없음)의 오류는 지금처럼 올린다. 공식 「검증 오류 뒤에도 연결 유지」와 맞춤 · 같은 종류 실수가 다시 생겨도 세션이 죽지 않게 |
| `SonioxError.channel` | `"stt"` · `"tts"` — Soniox 오류 · 세션이 만든 STT 오류(닫힘 · 확인 중 닫힘) 모두 |
| 오류 로그 ① | `soniox error: channel=… error_type=… request_id=… message=<str(e)> lang=… paused=… speaking=… queue=… stt_last=<audio·finalize·keepalive·end·config> N.Ns ago tts_last=<text·keepalive·none> N.Ns ago [len=… lang=…]` — 종류 · 길이 · 몇 초 전만(값 · 키 · 발화 원문 0). 기동 때 거절 로그(`soniox rejected`)에도 channel |

### 검증

- 시험(`tests/test_interpret.py`): TTS keepalive 가 공식 메시지 · 스트림 밖 검증 오류(stream_id "")가 와도 그 발화의 오디오가 끝까지 나옴 + 경고 로그 · 자기 스트림 오류는 `SonioxError(channel="tts")` · 중계 도중 오류 로그에 channel · message · lang · paused · stt_last · tts_last(len · lang) 가 있고 번역문 · 키 0
- **실물 재현**(`live_check.py idle` 새 시나리오 — zh-Hant · 발화 → 멈춤 35초(TTS keepalive 가 나감) → 다시 듣기 → 발화):

| 모드 | 결과 |
|---|---|
| **고치기 전 코드**(keepalive `{}` + 옛 `speak`) | **47.4초에 `error soniox_unavailable`** · 로그 `channel=tts error_type=invalid_request … message=invalid_request: Missing stream_id … stt_last=audio 0.0s ago tts_last=text 0.0s ago len=19 lang=zh` — **운영 장애 그대로 재현**(운영 50초) |
| keepalive 만 옛것(`{}`) + 새 `speak` | 끝까지 통과 · 오디오 2 · `soniox tts stray error … Missing stream_id` 경고만(방어가 동작) |
| **고친 코드** | 끝까지 통과 · 발화 2 · 오디오 2 · 오류 0 |

### 이슈

- 이 버그는 **언어와 무관**하다 — TTS 뒤 20초 넘게 쉬었다가 다시 말하는 모든 세션에서 났다(배포본 전부). 고친 이미지를 빨리 배포하는 것을 권한다.
- 원형(cc-prototype `procedure/back` `soniox.py`)에도 같은 `{}` 가 있을 것이다 — 이 레포 범위 밖이라 손대지 않았다.

## 처분 — D-35 이슈(코디 2026-10-27)

| 이슈 | 처분 | 한 것 |
|---|---|---|
| 1 zh-Hant 줄이기 | 그대로 | — (시드 `.4` 에서 zh-Hant 전체 20,250자 기준 `terms` 31개 남음 · 짝은 전부) |
| 2 zh-Hant 모호 별칭 | **지운다** | zh 에서 막은 말과 같은 것(간체로 바꿔 「超声刀」 · 「韩版超声刀」 · 「韩版热玛吉」)을 zh-Hant `aliases` 에서 지움 — **ph-123 올리지오 「韓版熱瑪吉」 · ph-126 슈링크유니버스 「韓版超聲刀」** 2개. 시험: 레포 시드 zh · zh-Hant 어디에도 모호어 0 |
| 3 한국어 → 대만명 실패 | 그대로 | — |
| 4 가져오기 초안 변환 | **s2tw + 激光→雷射** | `scripts/import_glossary.py` 의 zh-Hant 초안이 `langs.to_display("zh-Hant")`(자막과 같은 함수)를 쓴다 · source 값은 스키마 이름 그대로 `draft-s2twp`. 시험: 「离子导入 → 離子導入」 · 「激光导入 → 雷射導入」 · 「特色项目 → 特色項目」 · 가져오기 결과 「激光 → 雷射」 |

- 시드 `version` **`2026-10-27.3` → `.4`**.
- 최종 검증: 시드 검사 통과 · `uv run ruff check .` All checks passed · `uv run pytest -q` **249 passed**.
- 변경 파일(장애 + 처분): `back/app/service/interpret/soniox.py` · `back/app/service/interpret/session.py` · `back/seed/glossary.json` · `back/scripts/import_glossary.py` · `back/scripts/live_check.py` · `back/tests/test_interpret.py` · `back/tests/test_seed.py` · `back/tests/test_import_glossary.py`.
- 실물 JSON(`live-check-d35-2026-10-27.json`)에 장애 재현 결과(`incident_idle_repro`) · TTS 프로브(`incident_tts_probe`)를 더했다(키 0).
