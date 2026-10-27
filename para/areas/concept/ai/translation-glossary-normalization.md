---
type: concept
id: translation-glossary-normalization
title: 번역 용어 사전 정규화 — 대표명 · 현지명 · 별칭 · 출처 · 검수 (Translation Glossary Normalization)
aliases:
  - 용어 사전 정규화
  - 용어집 정규화
  - 번역 사전
  - 현지명
  - 시드 사전
  - 괄호 병기
up:
  - 2026-10-27-interpret-pwa-poc
tags:
  - 번역
  - 용어집
  - 데이터 모델
  - 다국어
---

# 번역 용어 사전 정규화 — 대표명 · 현지명 · 별칭 · 출처 · 검수

다국어 용어집을 「언어별 칸 하나에 문자열 하나」(예: `Thermage FLX（美版热玛吉FLX）`)로 두지 않고, **용어(term) 하나 × 언어마다 현지명 · 별칭 · 출처 · 검수 여부**로 나눠 두는 것. 번역 엔진에 넣을 때(정방향 · 역방향) · 화면에 보일 때 · 사람이 채울 때 각자 필요한 칸만 꺼내 쓴다.

## 정의

1. **term = 우리 대표명(ko) + ko 별칭** — 같은 ko 를 가진 원천 행은 하나로 합친다
2. **언어마다 `name`(대표 현지명) · `aliases`(현지 별칭) · `source`(어디서 왔나) · `reviewed`(사람이 봤나)** — 출처가 「자동 변환 초안」 이면 `reviewed: false`
3. **분해 못 한 원문은 버리지 않는다** — 괄호 안이 이름이 아니라 설명인 칸(60칸)은 `reviewed: false` + `raw` 보존. 다섯 갈래로 갈린 괄호 모양을 규칙으로 쪼개고, 규칙 밖은 사람이 본다
4. **저장은 사람이 읽는 표기, 매핑은 엔진이 내는 문자로** — 번역 엔진이 중국어를 간체로만 내면 대만 손님 말도 간체로 받아써진다. 사전의 대만 · 광둥어 칸은 번체로 적어 두되, 엔진에 넣는 매핑(정방향 ko → 현지명 · 역방향 현지명 · 별칭 → ko)을 만들 때 `t2s` 로 간체로 바꾼다. 번체는 자막 출력에서만 다시 만든다 → [[chinese-script-conversion]]
5. **현지명이 다른 지역은 별도 언어 칸** — 대만은 간체를 번체로 바꾼 것이 아니라 **단어가 다르다**(울쎄라 = 대륙 美版超声刀 · 대만 美國音波). 지역 칸은 변환이 아니라 조사로 채운다(통키 157 term 중 대만명 77개를 출처 URL · 신뢰도와 함께)

## 사용 예시

```json
{
  "id": "ph-130",
  "ko": "써마지FLX",
  "ko_aliases": ["써마지"],
  "entries": {
    "zh": {
      "name": "美版热玛吉FLX",
      "aliases": ["Thermage FLX", "热玛吉"],
      "source": "procedure-hub",
      "reviewed": true,
      "raw": "Thermage FLX（美版热玛吉FLX）"
    },
    "zh-Hant": {
      "name": "鳳凰電波",
      "aliases": ["美版熱瑪吉FLX", "Thermage FLX", "熱瑪吉", "美版電波"],
      "source": "web-research 2026-10-27",
      "reviewed": true,
      "note": "<출처 URL>"
    }
  }
}
```

`raw` 는 원천의 한 칸을 그대로 남긴 것이다. `zh-Hant` 는 번체로 적혀 있고, Soniox context 를 만들 때 간체(凤凰电波)로 바뀌어 들어간다. `ko_aliases` 「써마지」 는 상담사가 FLX 없이 부른다는 지적에서 왔다.

## 왜 중요한가

- 한 칸에 「영문（현지명）」 이 섞여 있으면 TTS 가 괄호를 빼고 영어만 읽고, 단독 호칭(「써마지」)은 매핑에 없다. 칸을 나누면 별칭이 역방향 매핑으로 그대로 들어간다
- `source` · `reviewed` 가 없으면 자동 초안과 사람이 확인한 이름이 구분되지 않는다. 통키의 대만 칸은 처음 전부 `source: draft-s2twp` · `reviewed: false` 였고, 조사로 출처를 찾은 77개만 대만명으로 올렸다(나머지 80개는 「검수 전」 그대로)

## 경계와 오해

- **[[db-normalization]] 과 같은 원리, 다른 목적** — 중복 제거보다 「한 칸 = 한 의미」 가 목적이다. 저장소는 DB 가 아니라 git 의 시드 파일일 수 있다 → [[seed-data]]
- **모호한 구어는 넣지 않는다** — 한 낱말이 여러 시술을 가리키면(韩版热玛吉) 역방향 매핑이 오역을 만든다. 실제 상담에서 확인할 때까지 비워 둔다
- **번역 뒤 치환이 아니다** — 이 사전은 번역 엔진 **입력**(context)이다. 결과 문장을 사후에 고치는 것과 다르다 → [[transcript-term-correction]]

## 함께 보는 개념

- [[context-catalog-injection]] — 이 사전을 번역 단계에 싣는 쪽
- [[chinese-script-conversion]] — 저장은 간체, 출력만 번체
- [[seed-data]] — 사전이 사는 곳(git PR 로 고치는 시드)
- [[db-normalization]] — 칸을 쪼개는 원리

## 출처

- [[2026-10-27-interpret-pwa-poc]] §2 — Procedure Hub 용어집의 괄호 칸을 term × 언어별 현지명 · 별칭 · 출처 · 검수로 분해(157 term × 7개 언어 · 설명 괄호 60칸 `raw` 보존) · 대만명 웹 조사 77개(`back/seed/glossary.json` · `import_glossary.py` · `research-tw-names-report.md` · DEC-001 D-33 · D-35)
