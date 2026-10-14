# Soniox 중국어권 · 국적별 언어 조사 (2026-10-13)

- 조사자: cc-prototype `researcher` 워커 (task_7a6f4cd3b6d6)
- 앞 판: `research-soniox-report.md`(2026-10-10). 거기서 확인한 STT `stt-rt-v5` 번역 내장, TTS `tts-rt-v2`, 「TTS zh는 간체만」은 다시 조사하지 않았다. 이 문서는 그 빈 곳만 채운다
- 정본: Soniox 공식 문서 `https://soniox.com/docs/*`. 각 페이지 `.mdx` 원문과 `https://soniox.com/docs/llms-full.txt`(문서 전체 합본, 2026-10-13 수집)
- 방법: 문서 읽기만 했다. API 호출·코드 실행·설치는 하지 않았다
- 표기
  - 〔공식 문서〕 docs 페이지
  - 〔공식 마케팅〕 soniox.com 제품 페이지·FAQ. Soniox가 쓴 글이지만 API 사양은 아니어서 문서보다 약한 출처다
  - 〔비공식〕 제3자
- **전수 검색 결과.** 문서 합본 전체(약 2.1MB)를 `Cantonese|Traditional|Taiwan|Hong Kong|Mandarin|Simplified|yue|zh-|Hant|Hans`로 검색했다. 걸린 곳은 TTS 지원 언어 페이지의 `Chinese (zh): Simplified Chinese only (not Traditional Chinese)` **한 줄뿐**이다. 광둥어·번체·대만·홍콩에 대한 API 문서 언급은 이 한 줄 말고는 없다

---

## 결론 한 장

| 항목 | 답 | 근거 |
|---|---|---|
| **광둥어 STT(인식)** | **별도 언어 코드가 없다.** 중국어는 `zh` 하나다. 공식 마케팅 FAQ는 「Mandarin, Cantonese, Wu를 한 모델에서 처리한다」고 한다. 광둥어를 말하면 `zh`로 인식될 것으로 보이지만 **API 문서에는 없다**. 결과가 표준 중국어 문어로 나오는지 광둥어 구어 문자(嘅·係·唔)로 나오는지도 문서에 없다 | 〔공식 문서〕 STT 지원 언어 · 〔공식 마케팅〕 speech-translation/chinese FAQ |
| **광둥어 번역** | 원문 쪽은 위와 같다(`zh`로 들어온다고 보면 번역 대상). **대상 언어로 광둥어를 고를 수는 없다**(코드 없음) | 〔공식 문서〕 번역 지원 언어 |
| **광둥어 TTS** | **문서에 없음.** 코드는 `zh` 하나뿐이고 광둥어 음성·억양에 대한 언급이 없다. 「안 된다」고 적혀 있지도 않다 | 〔공식 문서〕 TTS 지원 언어 · Voices |
| **번체 STT 결과** | **문서에 없음.** 출력 문자 체계를 고르는 파라미터가 문서에 없다 | 전수 검색 |
| **번체 번역 결과** | **문서에 없음.** `target_language`는 `zh` 하나뿐이고 간체/번체 선택이 없다 | 〔공식 문서〕 번역 지원 언어 · STT translation |
| **번체 TTS 입력** | **안 된다고 적혀 있다.** 「Chinese (`zh`): Simplified Chinese only (not Traditional Chinese)」. 번체를 넣으면 어떻게 되는지(오류인지, 잘못 읽는지)는 문서에 없다 | 〔공식 문서〕 TTS 지원 언어 |
| **대만 만다린** | `zh`로 처리한다. 대만 억양·어휘에 대한 **API 문서 언급은 없다.** 공식 마케팅에 「China, Taiwan, Singapore에서 쓰이는 중국어」「여러 지역 음성으로 학습」이라는 말만 있다. TTS에 대만 억양 음색은 문서상 없다 | 〔공식 마케팅〕 · 〔공식 문서〕 Voices |

**대만·홍콩 고객에게 무엇이 나가나(문서로 확인되는 범위):**
- **듣기(TTS):** 간체 `zh` 텍스트를 읽은 **만다린 음성**이 나간다. 음색은 공용 음색 중 하나이고, 대만·홍콩 억양을 고르는 수단은 문서에 없다. 광둥어 음성은 문서에 없다
- **보기(화면 텍스트):** 번역문이 간체로 나올지 번체로 나올지는 문서에 없다. 실물 호출로 확인해야 한다. 번체로 보여야 한다면 앱에서 변환해야 할 가능성이 높다(OpenCC 등, 비공식)
- **홍콩 고객이 광둥어로 말할 때:** 공식 마케팅은 처리한다고 하지만, `language` 태그(아마 `zh`)와 표기 방식은 문서에 없다. **실물 확인이 필요하다**

---

## 질문 1~6 답

### 1. 광둥어(Cantonese) — STT · 번역 · TTS

| 단계 | 지원 | 언어 코드 | 근거 |
|---|---|---|---|
| STT(인식) | 공식 문서: **언급 없음.** 중국어는 `Chinese / zh` 한 줄이다. 공식 마케팅: 「Soniox handles Chinese dialects like **Mandarin, Cantonese, and Wu in a single model**」. Soniox App 페이지: 「Chinese has several recognized varieties, including Mandarin, Cantonese, Wu, Min … Soniox is trained on diverse Chinese speech data」 | 별도 코드 없음(`yue`·`zh-HK` 없음). 문서상 쓸 수 있는 코드는 `zh`뿐 | https://soniox.com/docs/stt/concepts/supported-languages · 〔공식 마케팅〕 https://soniox.com/speech-translation/chinese (FAQ 「Does Soniox handle dialects and accents in Chinese?」) · 〔공식 마케팅〕 https://soniox.com/soniox-app/for/consultants-multilingual-client-calls-in-chinese (FAQ) |
| 번역 — 원문 | 위와 같다. 광둥어 음성이 `zh`로 들어오면 `zh`가 낀 쌍으로 번역될 것으로 보이지만 **문서에는 없다** | `zh` | https://soniox.com/docs/translation/supported-languages |
| 번역 — 대상 | **고를 수 없다.** 대상 코드에 광둥어가 없다. 광둥어 구어체로 번역해 주는지는 문서에 없다 | — | 같은 페이지 |
| TTS(음성) | **문서에 없음.** 코드는 `zh` 하나다. zh 설명에 문자 제약(간체만)은 있지만 광둥어에 대한 언급은 없다. 「안 된다」는 명시도 없다 | — | https://soniox.com/docs/tts/concepts/supported-languages |

- 「안 되면 문서에 그렇다고 적혀 있나」 → **적혀 있지 않다.** 광둥어라는 단어가 API 문서에 한 번도 나오지 않는다(전수 검색)
- 참고: 지원 언어 목록을 API로 받는 엔드포인트가 있다(STT `Get models`, TTS `Get TTS models`). 문서의 응답 예시에서 중국어는 `{"code": "zh", "name": "Chinese"}` 하나다. 실제 응답은 호출하지 않아 확인하지 않았다. https://soniox.com/docs/api-reference/tts/get_tts_models

### 2. 번체

| 단계 | 번체 가능? | 근거 |
|---|---|---|
| STT 결과 | **문서에 없음.** 출력 문자 체계를 고르는 파라미터(예: `zh-Hant`)가 STT 요청 필드·언어 페이지 어디에도 없다 | https://soniox.com/docs/stt/concepts/supported-languages · 전수 검색 |
| 번역 결과 | **문서에 없음.** `target_language` / `language_a`·`language_b`는 지원 언어 코드만 받고, 중국어 코드는 `zh` 하나다 | https://soniox.com/docs/translation/stt-translation · https://soniox.com/docs/translation/supported-languages |
| TTS 입력 | **안 된다(명시).** 「**Chinese (`zh`)**: Simplified Chinese only (not Traditional Chinese).」 번체를 넣었을 때의 동작은 문서에 없다 | https://soniox.com/docs/tts/concepts/supported-languages §Overview Note |

- 문서에 있는 간접 수단: STT `context`의 `translation_terms`(원문→번역어 고정)로 특정 용어의 번역 결과를 정할 수 있다. 문자 체계 전체를 바꾸는 기능이라는 언급은 없다. https://soniox.com/docs/stt/concepts/context
- 표준 변환 방법(**비공식**): OpenCC(오픈소스 간↔번 변환기, https://github.com/BYVoid/OpenCC). 설정 파일 `s2t`(글자 단위), `s2tw`(대만 글꼴), `s2twp`(대만 + 어휘 치환), `s2hk`(홍콩 글꼴)이 있다
- **한계 한 줄(비공식):** 글자는 기계적으로 바뀌지만 **어휘 차이**(软件→軟體, 视频→影片, 出租车→計程車/的士 등)는 `s2twp`가 사전에 있는 만큼만 바꾼다. 홍콩 광둥어 구어체(嘅·係·唔)는 만들지 못한다. 결과는 「번체로 쓴 대륙식 중국어」가 될 수 있다
- 파이프라인에 주는 함의: TTS는 간체를 받으므로 **TTS로 보내는 텍스트는 간체로 두고, 화면 표시만 번체로 바꾸는** 구조가 자연스럽다. 이건 문서에서 끌어낸 추론이고 결정은 하지 않는다 → 「정할 것」 D-2

### 3. 대만 만다린

| 항목 | 답 | 근거 |
|---|---|---|
| `zh` 인식에서 대만 억양·어휘 언급 | **API 문서에 없음.** 공식 마케팅에 「Chinese is spoken … across China, Taiwan, Singapore, and beyond」와, Soniox App FAQ에 「every region has its own accent, pace, and everyday vocabulary. Soniox App is trained on real-world Chinese speech from multiple regions」가 있다. 이 FAQ는 Soniox App(제품)에 대한 설명이고 API 사양은 아니다 | 〔공식 마케팅〕 https://soniox.com/speech-to-text/chinese · 〔공식 마케팅〕 https://soniox.com/soniox-app/for/consultants-multilingual-client-calls-in-chinese |
| `zh` TTS의 대만 억양·어휘 | **문서에 없음.** `language` 필드가 「overall delivery and a light accent bias」를 정하는데, 중국어 쪽 값은 `zh` 하나라 대만식을 지정할 수단이 없다 | https://soniox.com/docs/tts/concepts/language-mixing |
| 대만식 음색 | **문서에 없음.** 음색에는 `accent` 속성이 있다(예시 `american`, `british`). 문서에 실린 음색 목록 예시(§6)에서 억양이 적힌 음색은 Spanish·British·Australian·Indian뿐이고 중국어권 억양 음색은 없다. Console의 accent 필터로 확인해야 한다(호출하지 않음) | https://soniox.com/docs/tts/concepts/voices · https://soniox.com/docs/api-reference/tts/get_shared_voices |

### 4. two_way 번역에서의 언어 지정

- two_way 사양: `{"type": "two_way", "language_a": "ko", "language_b": "zh"}` 형식. **두 언어 밖의 말은 `translation_status: "none"`으로 전사만 하고 번역하지 않는다**(문서 예시에서 en↔de 설정에 fr 발화). https://soniox.com/docs/translation/stt-translation §Token format
- **상대 언어를 `zh`로 고정했는데 상대가 광둥어로 말하면:** **문서에 없음.** 광둥어 전용 코드가 없고 마케팅이 「한 모델에서 처리한다」고 하므로 `language: "zh"`로 태깅되어 번역될 가능성이 높아 보인다. 하지만 문서 근거가 없는 추론이다. 다른 코드로 태깅되면 `none`(번역 안 됨)이 된다. **실물 호출 1회로 확인할 항목이다**
- **language hints · 언어 식별로 만다린/광둥어를 가를 수 있나:** **문서상 가를 수 없다.** 힌트·제한·식별은 모두 지원 언어의 ISO 코드 단위로 동작하고(`language_hints: ["en","es"]`, 토큰마다 `language` 태그), 만다린과 광둥어는 같은 `zh`다. 하위 변종 태그를 낸다는 언급이 없다
  - https://soniox.com/docs/stt/concepts/language-hints
  - https://soniox.com/docs/stt/concepts/language-identification
  - https://soniox.com/docs/stt/concepts/language-restrictions
- 관련 사실(공식 문서)
  - `language_hints`는 **편향만 줄 뿐 제한하지 않는다.** 「similar-sounding languages」일 때 쓰라고 권한다
  - `language_hints_strict: true`는 best-effort 제한이다. **언어 하나일 때 가장 강하다**고 하고, 여러 언어를 지정하면 비슷한 언어끼리 판별이 흔들릴 수 있다고 경고한다
  - 실시간 언어 식별은 일시적으로 잘못 분류하고 나중에 고칠 수 있다
  - two_way(ko+zh)에서 strict에 두 언어를 줄 수 있는지, 그 효과가 어떤지는 문서에 없다

### 5. 국적 → 언어 후보 표

→ 아래 「국적 → 언어 후보 표」 절.

### 6. TTS 음색

- **공용인가, 언어마다 다른가 → 공용.** 「Any voice, any language → Every voice works with all 60+ supported languages」, 「The same voice preserves its timbre and style whether it is speaking English, Japanese, or Spanish」. 언어별 전용 음색은 없다. ko·zh·ja 등 위 언어 모두 같은 음색 집합을 쓴다. https://soniox.com/docs/tts/concepts/voices · https://soniox.com/docs/tts/concepts/supported-languages
- `language`는 음색과 따로 정하고, 「light accent bias」를 준다. https://soniox.com/docs/tts/concepts/language-mixing
- **음색 이름과 수:** 문서에 「현재 tts-rt-v2 음색 전체 목록」 표는 **없다.** 전체는 Console(Text-to-speech > Voices)이나 `GET /v1/tts-models` · `Get shared voices` API로 보라고 한다(호출하지 않음)
- 문서에 실린 유일한 목록은 `Get TTS models` **응답 예시**다. **모델 id가 `tts-rt-v1`이다.** tts-rt-v1은 2026-08-31에 제거되어 v2로 넘어갔고(https://soniox.com/docs/tts/models), v2는 「fully compatible」이라고만 한다. 그래서 아래 목록이 v2 현재 목록과 같은지는 **확인하지 못했다.** 예시 기준 28개:

| 성별 | 이름(예시에 적힌 억양) |
|---|---|
| 여 (14) | Maya · Nina · Emma · Claire · Grace · Mina · Lucia(스페인) · Sofia(스페인) · Isla(영국) · Victoria(영국) · Ruby(호주) · Elise(호주) · Priya(인도) · Meera(인도) |
| 남 (14) | Daniel · Noah · Jack · Adrian · Owen · Kenji · Rafael(스페인) · Mateo(스페인) · Oliver(영국) · Arthur(영국) · Cooper(호주) · Mason(호주) · Arjun(인도) · Rohan(인도) |

  (성별은 예시 JSON의 `gender` 필드 그대로. v2의 정확한 수는 API 응답으로 확인한다)
  출처: https://soniox.com/docs/api-reference/tts/get_tts_models (응답 예시)
- 음색 속성 스키마: `gender`(male/female/neutral), `age`(young/middle_aged/old), `accent`(문자열, 예 `american`·`british`), `use_case`, `style`. https://soniox.com/docs/api-reference/tts/get_shared_voices
- 중국어·한국어·일본어 억양이 적힌 음색은 예시에 **없다.** Mina·Kenji는 이름만 동아시아풍이고 설명에 억양 언급이 없다. 음성 복제로 자체 음색을 만들 수는 있다. https://soniox.com/docs/tts/concepts/voice-cloning

---

## 국적 → 언어 후보 표

- 지원 여부는 STT·번역·TTS 지원 언어 표에 그 코드가 있는지로 판정했다. 세 표의 언어 집합은 같다(번역 페이지 「uses the same supported-language set」)
  - https://soniox.com/docs/stt/concepts/supported-languages
  - https://soniox.com/docs/translation/supported-languages
  - https://soniox.com/docs/tts/concepts/supported-languages
- 「후보」는 그 나라에서 흔히 쓰는 언어를 나열한 것이다(언어 사용 실태는 일반 지식이고 Soniox 출처가 아니다). **확정이 아니다**
- 건수는 브리프의 열흘 전체 기준이다

| 국적 (건수) | 언어 후보 | 코드 | STT | 번역 | TTS | 비고 |
|---|---|---|---|---|---|---|
| **TW** (97) | 만다린(번체 사용) | `zh` | ○ | ○ | ○ (간체 입력만) | 번체 출력: STT·번역 문서에 없음, TTS 입력 불가(명시). 대만 억양 음색: 문서에 없음 |
| | 대만어(台語·민난어) | 없음 | 문서에 없음 (마케팅에 「Min」 언급만) | ✗ (코드 없음) | ✗ (코드 없음) | |
| **KR** (25) | 한국어 | `ko` | ○ | ○ | ○ | 직원 언어와 같다. 통역이 필요한지 → 정할 것 D-5 |
| **CN** (24) | 만다린(간체) | `zh` | ○ | ○ | ○ | 문서상 제약이 없는 유일한 중국어권 경우 |
| | 광둥어(광둥성 등) | 없음 | 마케팅만 「처리」 | 원문만(문서에 없음) / 대상 ✗ | 문서에 없음 | |
| **US** (8) | 영어 | `en` | ○ | ○ | ○ | |
| | 스페인어 | `es` | ○ | ○ | ○ | |
| **HK** (7) | 광둥어(번체 사용) | 없음 (`zh`로 들어올 가능성, 문서에 없음) | 마케팅만 「처리」 | 원문: 문서에 없음 / 대상 ✗ | 문서에 없음 | 표기(표준 문어인지 구어 문자인지) 문서에 없음 |
| | 영어 | `en` | ○ | ○ | ○ | |
| | 만다린 | `zh` | ○ | ○ | ○ (간체 입력만) | |
| **JP** (6) | 일본어 | `ja` | ○ | ○ | ○ | 앞 판 문서 예시가 ja↔ko two_way |
| **TH** (5) | 태국어 | `th` | ○ | ○ | ○ | |
| **FR** (2) | 프랑스어 | `fr` | ○ | ○ | ○ | |
| **PH** (2) | 타갈로그어(필리피노) | `tl` | ○ | ○ | ○ | 표 이름은 「Tagalog」. 필리피노를 따로 표기하지 않는다 |
| | 영어 | `en` | ○ | ○ | ○ | |
| | 세부아노어 등 | 없음 | ✗ | ✗ | ✗ | 지원 목록에 없다 |
| **IN** (1) | 힌디어 | `hi` | ○ | ○ | ○ | |
| | 영어 | `en` | ○ | ○ | ○ | 인도 억양 음색이 예시에 있다(Arjun·Rohan·Priya·Meera) |
| | 벵골·타밀·텔루구·마라티·구자라트·칸나다·말라얄람·펀자브·우르두 | `bn` `ta` `te` `mr` `gu` `kn` `ml` `pa` `ur` | ○ | ○ | ○ | 모두 지원 목록에 있다 |

---

## 정할 것 — 코디·사용자가 결정할 항목 (결정하지 않음)

| # | 항목 | 선택지 | 근거 |
|---|---|---|---|
| D-1 | **HK 고객의 언어** | (a) `zh` 만다린 TTS로 응대(광둥어 인식은 마케팅 주장에 기댐) / (b) `en` / (c) 시작할 때 고객이 고름 | Q1 · Q4. 광둥어 TTS는 문서에 없다 |
| D-2 | **TW·HK 화면 표시 문자** | (a) Soniox가 내는 대로 둔다 / (b) 앱에서 OpenCC 등으로 번체 변환(TTS로는 간체를 보낸다) / (c) 표시 안 함(음성만) | Q2. TTS는 간체만(명시). STT·번역의 번체 출력은 문서에 없다 |
| D-3 | **실물 확인 항목**(API 호출 1회씩, 이 조사 범위 밖) | ① `zh` STT 결과가 간체인지 번체인지 ② 광둥어 발화가 `zh`로 태깅되고 two_way(ko↔zh)에서 번역되는지 ③ 번체를 TTS에 넣으면 어떻게 되는지 ④ v2 공용 음색 목록·수와 accent 값 | 문서에 없음 항목 전부 |
| D-4 | **국적에 후보가 둘 이상일 때 기본값** | US(en/es) · HK(D-1) · PH(tl/en) · IN(hi/en/…) · TW(zh/대만어 — 대만어는 미지원) | 표 |
| D-5 | **KR 국적 환자** | 통역 끔 / 켬(같은 언어라 의미가 없다) | 표 |
| D-6 | **음색 선택** | 언어마다 바꿀지 하나로 고정할지(모든 음색이 모든 언어를 말한다). 성별 선택을 둘지 | Q6 |
| D-7 | **language_hints / strict 사용 여부** | 국적으로 고른 언어를 two_way의 `language_b`와 `language_hints`에 넣을지, strict를 켤지(문서는 언어 하나일 때 strict를 권장) | Q4 |

---

## 출처 목록

**공식 문서 (2026-10-13 수집)**
- https://soniox.com/docs/llms.txt · https://soniox.com/docs/llms-full.txt (전수 검색용 합본)
- https://soniox.com/docs/stt/concepts/supported-languages
- https://soniox.com/docs/stt/concepts/language-hints
- https://soniox.com/docs/stt/concepts/language-restrictions
- https://soniox.com/docs/stt/concepts/language-identification
- https://soniox.com/docs/stt/concepts/context
- https://soniox.com/docs/stt/models (stt-rt-v5, 2026-06-16)
- https://soniox.com/docs/translation/supported-languages
- https://soniox.com/docs/translation/stt-translation
- https://soniox.com/docs/tts/concepts/supported-languages (zh 간체만 명시)
- https://soniox.com/docs/tts/concepts/language-mixing
- https://soniox.com/docs/tts/concepts/voices
- https://soniox.com/docs/tts/concepts/voice-cloning
- https://soniox.com/docs/tts/models (tts-rt-v2 GA 2026-08-11, v1 2026-08-31 제거)
- https://soniox.com/docs/api-reference/tts/get_tts_models (음색 예시, 모델 id tts-rt-v1)
- https://soniox.com/docs/api-reference/tts/get_shared_voices (음색 속성 스키마)

**공식 마케팅 (API 사양 아님)**
- https://soniox.com/speech-translation/chinese — FAQ 「Mandarin, Cantonese, and Wu in a single model」
- https://soniox.com/speech-to-text/chinese — 「across China, Taiwan, Singapore, and beyond」
- https://soniox.com/soniox-app/for/consultants-multilingual-client-calls-in-chinese — FAQ 「Mandarin, Cantonese, Wu, Min」, 「China, Taiwan, and Singapore … accent, pace, and everyday vocabulary」(Soniox App 설명)

**비공식**
- OpenCC https://github.com/BYVoid/OpenCC — 간↔번 변환 설정(s2t·s2tw·s2twp·s2hk)
- 참고: 웹 검색 요약 중 「Soniox가 간체·번체 출력을 모두 지원한다」는 문장이 있었다. Soniox 페이지 원문에서 그 문장을 찾지 못해 **근거로 채택하지 않았다**
