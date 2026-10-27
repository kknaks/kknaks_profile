---
type: concept
id: chinese-script-conversion
title: 중국어 문자 변환의 한계 — 글자 · 지역 표기는 되고 현지 별명은 안 된다 (Chinese Script Conversion)
aliases:
  - 간체 번체 변환
  - 간번 변환
  - OpenCC
  - s2tw
  - s2twp
  - 번체는 출력에서만
  - 대만 표기
up:
  - 2026-10-27-interpret-pwa-poc
tags:
  - 중국어
  - 다국어
  - 텍스트 변환
  - 번역
---

# 중국어 문자 변환의 한계 — 글자 · 지역 표기는 되고 현지 별명은 안 된다

간체 → 번체 변환기(OpenCC 등)는 층이 셋이다 — **글자**(热 → 熱), **지역 표기**(대만식 낱말 · 「激光 → 雷射」), 그리고 변환기가 닿지 않는 **현지 별명**(써마지 = 대륙 热玛吉 · 대만 鳳凰電波). 앞의 둘은 설정으로 고르고, 셋째는 데이터로 채운다. 그리고 엔진 안은 간체로 두고 번체는 **사람에게 보이는 출력에서만** 만든다.

## 정의

1. **글자 변환(`s2t` · `s2tw`)** — 글자를 대응 번체로. `s2tw` 는 대만 글자꼴 기준. 낱말은 바꾸지 않아 의미가 안 바뀐다
2. **낱말 · 지역 표기 변환(`s2twp`)** — 대만식 낱말까지 바꿔 준다고 하지만, **사전이 무엇을 대만식으로 보는지**가 문제다. 통키에서 드러난 것:
   - 「激光 → 鐳射」 — 鐳射는 **홍콩 표기**다. 대만 병원 · 지자체 문서는 모두 「雷射」
   - 「导入 → 匯入」 · 「项目 → 專案」 · 「设备 → 裝置」 — IT 용어 쪽으로 바뀐다(匯入 = import). 대만 미용 문맥은 「導入」
3. **현지 별명은 어떤 변환기로도 안 나온다** — 울쎄라 美版超声刀 → 대만 美國音波, 올리지오 韩版热玛吉 → 玩美電波. 글자가 아니라 **단어가 다르다.** 조사해 사전(데이터)에 넣는다 → [[translation-glossary-normalization]]
4. **변환 위치는 경계에서만** — 엔진이 간체만 내면 엔진에 들어가는 것(용어 매핑 · TTS 텍스트)은 간체, 사람에게 보이는 것(자막)만 번체. 번체로 적어 둔 사전은 엔진 입력 직전 `t2s`, 자막은 출력 직전 `s2tw`. TTS 에 번체를 넣으면 오류 없이 발음이 깨졌다

## 사용 예시

```python
# 통키 langs.py — 출력(자막)만 번체. 매핑 · TTS 는 간체 그대로
TRADITIONAL_CONFIG = {"yue": "s2tw", "zh-Hant": "s2tw"}   # s2twp 는 쓰지 않는다
DISPLAY_REPLACE = {"zh-Hant": {"激光": "雷射"}}            # 글자 변환 뒤 대만 표기 한 쌍만

def to_display(lang):
    config = TRADITIONAL_CONFIG.get(lang)
    if not config:
        return None                                       # 간체 그대로
    replace = DISPLAY_REPLACE.get(lang, {})
    def display(text):
        text = convert(text, config)                      # OpenCC s2tw
        for old, new in replace.items():
            text = text.replace(old, new)
        return text
    return display
```

반대 방향도 있다 — 사람이 번체로 적어 둔 사전 칸(대만 · 광둥어)은 엔진에 넣기 **직전에** `t2s` 로 간체로 바꾼다.

## 왜 중요한가

- 「대만식 표현까지」 라는 설명만 보고 `s2twp` 를 넣으면 레이저 계열이 전부 홍콩식이 되고 일부 낱말은 다른 뜻이 된다. 통키는 실측을 「일반 낱말이 바뀌나」 로만 하고 **표기 지역**은 안 봐서 넣었다가 되돌렸다(D-32 → D-35)
- 「번체로 바꾸면 대만어」 라고 생각하면 손님이 실제로 부르는 시술명이 영영 안 나온다. 변환과 조사의 경계를 알아야 조사 범위가 정해진다

## 경계와 오해

- **번체 ≠ 대만** — 홍콩도 번체를 쓴다. 지역 표기는 `tw` / `hk` 가 다르다. 고를 때 「번체인가」 가 아니라 「어느 지역의 표기인가」 를 본다
- **변환 결과를 사전 초안으로 쓰면 `reviewed: false`** — 변환기 출력은 근거가 아니다. 출처로 확인한 것만 검수됨으로 올린다
- [[character-encoding]] 과 다르다 — 그쪽은 같은 글자를 바이트로 어떻게 적나, 여기는 다른 글자 · 다른 낱말로 바꾸는 것

## 함께 보는 개념

- [[translation-glossary-normalization]] — 변환이 못 하는 현지 별명을 담는 곳
- [[websocket-relay]] — 통역 중계에서 번체를 자막에만 적용하는 자리
- [[unicode]] — 간체 · 번체가 서로 다른 코드 포인트인 이유

## 출처

- [[2026-10-27-interpret-pwa-poc]] §2 — OpenCC 변환 단계: `s2twp` 를 넣었다가 鐳射(홍콩) · 匯入 오변환이 조사에서 드러나 `s2tw` + 激光 → 雷射 로 되돌림 · 기기 현지 별명은 데이터로(`back/app/service/interpret/chinese.py` · `research-tw-names-report.md` · DEC-001 D-17 · D-32 · D-35)
