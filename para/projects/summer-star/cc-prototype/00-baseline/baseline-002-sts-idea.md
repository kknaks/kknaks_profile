---
type: baseline
id: BASE-002
title: "sts — 한국어 ↔ 다른 언어 실시간 음성 통역 (Soniox)"
status: raw
product: cc-prototype
feature: sts
source:
  type: conversation
  ref: "사용자 대화 2026-10-10 · orchestration/work/sts-prototype/research-soniox-report.md"
links:
  baselines:
    - "[[baseline-001-feature-lab|BASE-001]]"
  decisions: []
  specs: []
  works: []
  releases: []
  related:
    - "[[baseline-003-cc-idea|BASE-003]]"
created_at: 2026-10-10
updated_at: 2026-10-10
tags:
  - product/cc-prototype
  - feature/sts
  - doc/baseline
  - status/raw
---

# sts — 한국어 ↔ 다른 언어 실시간 음성 통역 (Soniox)

> 아이디어 노트다. 아직 아무것도 정하지 않았다. 정하는 것은 sts 의 DEC 가 갖는다.

## 아이디어

말하면 상대 언어 **음성**으로 나온다. 한국어 ↔ 다른 언어. 고객에게 보여줄 데모로 빨리 만든다.

### 사용자 원문 (2026-10-10)

> soniox를 구독 중인데 이걸 사용해서 sts 를 할건데
>
> 한국어 <-> 다른언어 번역 + sts 인데
>
> 바로 sts 가 안되면 stt -> 추록 -> tts 로 가도 돼

## 조사에서 알게 된 것

> 출처: `orchestration/work/sts-prototype/research-soniox-report.md` (2026-10-10, 공식 문서 기준).
> 문서 조사뿐이다 — 실물 호출은 아직 안 했다.

**Soniox 한 곳으로 된다 — 단, 연결 두 개를 잇는 구조다.**

```text
마이크 → [Soniox STT · 번역 내장] → 번역 텍스트 → [Soniox TTS] → 상대 언어 음성
```

- 음성 → 음성 단일 모델은 **없다.** 공식 STS 는 STT WebSocket + TTS WebSocket 을 앱 코드로 잇는다.
- 번역은 STT 안에 있다 — 별도 번역(LLM) 단계가 필요 없다. 용어 고정(`translation_terms`)도 된다.
- 번역 모드 두 가지
  - 단방향 `one_way` — 한국어 → 대상 언어 하나
  - 양방향 `two_way` — 한국어 ↔ 상대 언어(두 사람 대화). 문서 예시가 ja↔ko
- 한국어: STT · 번역 · TTS 모두 지원. en · ja · zh · vi · th 도 지원
- 번역은 문장이 끝나기 전에 흘러나오고, 발화 끝(`<end>`)을 감지해 준다
- **공식 데모가 FastAPI + 브라우저** 구조 — 우리 기본 스택(DEC-001 D-04)과 같다. 첫 음성까지 약 0.5~1.5초(데모 README)
- 모델: STT `stt-rt-v5` · TTS `tts-rt-v2`

### 붙이는 방식 후보

| 후보 | 흐름 | 메모 |
|---|---|---|
| 백엔드 중계 | 브라우저 마이크 → FastAPI → Soniox STT → FastAPI → Soniox TTS → FastAPI → 브라우저 | 공식 STS 데모 구조. 키가 서버에만 |
| 브라우저 직결 | FastAPI 는 임시 키만 발급(STT·TTS 2종) → 브라우저 SDK(`@soniox/react`·`@soniox/client`)가 직접 | STS 직결 공식 예제는 없음(Next.js 예제는 STT 만) |
| 텍스트만 | TTS 생략, 원문·번역 자막만 | 데모 토글로 쓸 수 있음 |

### 걸리는 것

- **TTS 동시 스트림 기본 3** — 양방향 한 세션이 거의 다 쓴다. 동시 시연이 많으면 Console 에서 증설 요청(1~3영업일). STT 동시 기본 10
- 한국어 음성 **품질 수치는 문서에 없다** — 귀로 들어 봐야 한다
- 비용: STT 약 $0.12/시간 · TTS 약 $0.70/생성 시간. 번역 과금은 공식 페이지끼리 표기가 엇갈린다(포함 vs $0.18/시간) — 사용량 로그로 실측
- 리전 기본 US, 가장 가까운 건 JP. Korea 는 준비 중
- 사용자 Soniox 계약 형태(구독/종량제)·한도는 Console 에서 확인 필요

## 열린 질문

- 사용자 「cc 에 다 통합 될거 같은데」(2026-10-10) — 현황판(BASE-003) 안에 어떻게 들어가나

- 연결 구조 — 백엔드 중계 / 브라우저 직결
- 번역 모드 — 단방향 / 양방향 (토글로 둘 다?)
- 데모 언어 쌍 — 한국어 ↔ ?
- 동시 시연 규모 → 한도 증설 필요한가
- 존댓말·문체·지원 밖 언어처럼 LLM 번역이 필요한 요구가 있나
- 첫 실물 호출에서 볼 것 — 실제 첫 음성까지 시간, 한국어 음색, 번역 과금
