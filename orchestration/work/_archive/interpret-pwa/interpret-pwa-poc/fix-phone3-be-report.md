# 폰 피드백 3 — backend 결과 보고 (D-32)

## 상태: done

폰 피드백 1 · 2 변경 위에 이어서 · 커밋 없음 · `back/**` 만.

## 수행 — 파일·모듈 목록

| 파일 | 무엇 |
|---|---|
| `back/app/service/interpret/langs.py` | **언어별 변환 선택 한 곳** — `TRADITIONAL_CONFIG = {"yue": "s2tw", "zh-Hant": "s2twp"}`(이전 `TRADITIONAL_LANGS` 집합을 대신함) · `to_display(lang)` → 그 lang 의 간체 → 번체 변환 함수(없으면 `None`) · `traditional(lang)` 은 그대로 |
| `back/app/service/interpret/chinese.py` | `convert(text, config)` — OpenCC 설정 이름으로 변환(캐시 4개) · `to_traditional` · `to_simplified` 는 그대로 |
| `back/app/service/interpret/assembler.py` | `CaptionAssembler(display=…)` — 자막 중국어 쪽을 lang 별 변환으로. `traditional=True` 만 주면 원형대로 s2tw |
| `back/app/service/interpret/session.py` | `CaptionAssembler(display=to_display(lang))` |
| `back/app/service/glossary.py` | 메뉴: zh 열을 빌려 쓰는 zh-Hant 만 `to_display` 로(s2twp) · yue 열은 원본 그대로 |
| `back/scripts/live_check.py` | `zhhant` 단계의 번체 판정을 s2twp 기준으로 |
| `back/tests/test_interpret.py` · `test_glossary.py` | 아래 |

바뀌지 않은 것: Soniox context(zh-Hant = zh 열 간체 · 정방향 · 역방향) · TTS 입력(간체) · yue 자막(s2tw) · yue 메뉴(원본 열).

## 검증 — 명령과 수치

`cd back && uv run ruff check . && uv run pytest -q` → **All checks passed · 190 passed**(이전 185 + 5)

새 시험:
- 자막(WS 전체 흐름 · 번역 「激光治疗」): **zh-Hant → 「鐳射治療」** · **yue → 「激光治療」**(s2tw) · zh → 「激光治疗」(간체 그대로) · 셋 다 TTS 입력은 `("zh", "激光治疗")`
- `to_display`: zh-Hant 「激光 软件」 → 「鐳射 軟體」 · yue → 「激光 軟件」 · zh · en → `None`
- 메뉴: `/api/glossary?lang=zh-Hant` 「激光」 → 「鐳射」 · yue · zh 는 「激光」 그대로 · zh-Hant context 의 target 은 「激光」(간체 그대로)

실물 Soniox 호출은 이번에 하지 않았다(브리프 검증 = ruff · pytest). 변환은 back 안쪽의 순수 변환이라 Soniox 쪽 동작은 바뀌지 않는다.

## 계약 대조 — DEC-001 D-32

| 항목 | 판정 |
|---|---|
| zh-Hant 출력(자막 · 용어집 메뉴) = s2twp | 같음 |
| 매핑은 zh 열(간체) 그대로 | 같음 |
| TTS 간체 그대로 | 같음 |
| yue 는 s2tw 유지 | 같음 |
| 기기 현지 별명은 코드에 별칭을 짓지 않는다 | 같음 — 별칭 표 없음 |

## 이슈 · 코디가 확인할 것

1. s2twp 는 원문(Soniox 원문 · 번역문)의 중국어 쪽 전체에 적용된다. 대만 화자가 말한 원문 자막도 대만식 표현으로 바뀌어 보인다(예: 화자가 「激光」이라 말해도 「鐳射」로 표시). 의도와 같다고 보지만 E2E 때 확인을 권한다.
2. SPEC §5.6(번체 변환 · zh-Hant s2twp) 갱신은 planner 몫.
