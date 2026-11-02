# 폰 피드백 1 — backend 결과 보고 (D-28)

## 상태: done

base main `046eabe` · 커밋 없음. backend 절만(`back/**`) — D-27(로그인 입력 16px)은 front 일이라 손대지 않았다. 워크트리의 `front/**` 변경은 frontend 워커 것이다.

## 수행 — 파일·모듈 목록

| 파일 | 무엇 |
|---|---|
| `back/app/service/interpret/langs.py` | 앱 lang 에 **`zh-Hant`** 추가(7개) · `SONIOX_LANG["zh-Hant"] = "zh"` · `TRADITIONAL_LANGS = {yue, zh-Hant}` · 새 매핑 `GLOSSARY_COLUMN = {zh-Hant: zh}` + `glossary_column()` — 매핑은 이 한 곳 |
| `back/app/service/glossary.py` | `context_rows` 가 `glossary_column(lang)` 열을 읽는다 → zh-Hant context = zh 열 그대로(정방향 target · 역방향 source 모두 간체 · t2s 는 yue 만) · `menu_rows("zh-Hant")` = zh 열을 `s2tw` 로(표시용) |
| `back/scripts/live_check.py` | `zhhant` 단계 추가(한국어 발화 → 자막 번체 · TTS 입력 간체) |
| `back/tests/test_glossary.py` · `test_interpret.py` | 아래 |

자동으로 따라온 것(코드 변경 없음): `parse_start` 는 `APP_LANGS` 를 그대로 쓰므로 `zh-Hant` 를 받는다 · `/api/glossary?lang=zh-Hant` 400 아님 · 세션의 `CaptionAssembler(traditional=…)` 는 `traditional(lang)` 로 번체 자막 · TTS 는 원형대로 간체 `Utterance.text`(괄호 제거 뒤).

## 검증 — 명령과 수치

`cd back && uv run ruff check . && uv run pytest -q` → **All checks passed · 174 passed**(이전 168 + 6)

- 고친 시험: 잘못된 lang 오류 문구에 `zh-Hant` 포함 · lang 매핑 시험에 zh-Hant(Soniox `zh`) · 「번체 자막 · TTS 간체」 시험에 zh-Hant(자막 「麻醉藥膏」 · TTS `("zh", "麻醉药膏")`)
- 새 시험: zh-Hant 매핑(`parse_start` · `soniox_lang` · `traditional` · `glossary_column`) · STT context = `context_for("zh")` 와 같음(정방향 「필러 → 填充剂」 · 역방향 「填充剂 → 필러」 간체) · 메뉴 zh-Hant = zh 열 번체(「填充劑」 · 「麻醉藥膏」 · 영문 그대로 · 빈 칸 빈 채로)

### 실물 1회 — `uv run python scripts/live_check.py zhhant` (용어집 `2026-07-01-reviewed-v5` · 158행 · max_chars 18,832)

- 한국어 발화(필러 · 쥬비덤 · 신펄) → caption 번역 「今天先做**填充劑**治療，下次來就診時我也會一起諮詢**喬雅登**和新珍珠 (Synpurl)。」 — **번체** · 용어 3/3(번체로 바뀌어 보임)
- TTS 입력 「今天先做填充剂治疗，下次来就诊时我也会一起咨询乔雅登和新珍珠。」 — **간체** · 괄호 제거됨(D-19) · TTS 언어 `zh`
- `audio_start` 1 · 오류 0

## 계약 대조 — DEC-001 D-28

| 항목 | 판정 |
|---|---|
| 繁體 = Soniox `zh` | 같음 |
| 자막 번체(s2tw) · TTS 간체 | 같음 — 실물 확인 |
| 용어집 target = `zh` 열(간체 그대로 Soniox 에) | 같음 — 정방향 · 역방향 둘 다 |
| 용어집 메뉴 표시는 번체 | 같음 — `/api/glossary?lang=zh-Hant` 의 `term` 이 s2tw |
| yue 는 지금 그대로 | 같음(메뉴는 yue 열 원본 · context 는 t2s) |

## 이슈 · 코디가 확인할 것

1. **front 와 맞출 계약 값**: 앱 lang 코드는 정확히 `zh-Hant`(대소문자 그대로)다. WS `start.lang` · `/api/glossary?lang=` 둘 다 이 문자열. front `lib/langs.ts` 가 같은 값을 쓰는지 대조가 필요하다.
2. SPEC §5.5 · §4.6 · §5.4(「가능: …」 문구 · 6개 → 7개)와 OQ-004 는 planner 가 갱신할 자리다.
3. 메뉴의 번체는 기계 변환(OpenCC s2tw)이다. 용어집 원천에 번체 열이 없어 생긴 한계로, 대만식 표기와 다른 낱말이 있을 수 있다.
