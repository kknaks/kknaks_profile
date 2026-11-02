---
type: baseline
id: BASE-001
title: "ccc 통역을 떼어 실시간 통역 PWA로 — Procedure Hub 용어집을 Soniox 번역 용어로"
status: raw
product: interpret-pwa
source:
  type: conversation
  ref: "사용자 대화 2026-10-26"
links:
  baselines: []
  decisions:
    - "[[decision-001-interpret-pwa|DEC-001]]"
  specs: []
  works: []
  releases: []
  related: []
created_at: 2026-10-26
updated_at: 2026-10-26
tags:
  - product/interpret-pwa
  - doc/baseline
  - status/raw
---

# ccc 통역을 떼어 실시간 통역 PWA로 — Procedure Hub 용어집을 Soniox 번역 용어로

> 아직 결정하지 않은 입력이다. 무엇을 정했는지는 DEC-001 이 갖는다.

## Raw

### 입력 1 — 사용자 원문 (2026-10-26)

> 우리 poc 만들건데 ccc poc에서 통역기능만 떼서 별도로 통역 pwa를 만들어 보려고 해
>
> 일단 필요한 거는 실시간 통역 / 로그인 / 프로시저허브 용어 소니옥스에 용어집으로 등록하기
>
> 왜냐하면 피부과 정보를 통역할때 직역해서 가져와서
>
> https://stg-procedure-hub.medisolveai.com/terminology

### 입력 2 — 형태 · 로그인 · 배포 (2026-10-26)

> 웹앱 구조로 만들거임
>
> 통역앱에는 로그인이 필요하지 / 그냥 (아이디) / (비밀번호) 으로 만들자 — 값은 public 레포라 생략, env 로
>
> 백엔드는 맥스튜디오에 일단 배포 할거야 / 일단 로컬에서 되는지 테스트는 해보고 마지막에 배포 해야지
>
> pwa로 만들고 가볼까 키는 내가 env 만들면 거기에 넣을거야 / 말 그대로 그냥 통역 하면 되는데 언어 감지가 되나 ?

- Procedure Hub 용어 조회에는 로그인이 필요 없다(사용자 지적, 코디 확인).

### 입력 3 — 언어 선택 · UI (2026-10-26)

> a로 가자 (← 코디 제안 A: 시작 화면에서 환자 언어를 고르고 two_way 로 연결)
>
> ui는 단순하게 가면 될거 같고 medikit으로 가면 되고
>
> 로그인 하고
> [헤더] 햄버거 (로그아웃, 용어집 메뉴)
> [외국어(드랍다운)] (상하반전)
> ---가운데 원------
> [한국어]
>
> 상하반전은 외국인이 맞음편에서 본다고 생각하자
>
> 가운데 원은 말할때는 음파 웨이브가 음성에 따라 우퍼처럼 원이 줄어들엇다가 커지는거고
> 외국어, 한국어 일때 다른 색으로 보여 주면 좋을거 같고
> 번역 sts 가 나올때는 해당 언어로 sts 출력중이다고 나오면 좋을듯 안내랑

### 입력 4 — 화면 전환 아이콘 · 새 레포 (2026-10-26)

> 외국어 영역에 화면 전환 아이콘 넣자 / 옆에서 볼때 반대편에서 볼때 랜더만 바꾸면 되는 거잖아
>
> 새로 Poc 만드는거랑 완전 새로 스캐폴딩해줘 / 새 레포 만들고

## 확인한 사실 (코디 2026-10-26)

### Procedure Hub 용어집

- `GET https://stg-procedure-hub.medisolveai.com/api/v1/glossary/matrix` — 인증 없이 JSON.
- 2026-10-26 응답: `version` `2026-07-01-reviewed-v5` · `count` 158 · `langs` `en · ja · zh · th · vi · yue`.
- 행 필드: `category` · `ko` · 언어별 표기(6개) · `source` · `verified_at` · `note`. 카테고리 15개(필러 · 보톡스 · 레이저 · 실리프팅 · 스킨부스터 등).
- 158행 모두 6개 언어 표기가 채워져 있다.

### Soniox

- 실시간 번역은 `translation.type` `two_way`(`language_a` · `language_b` 양방향) · `one_way`(`target_language` 한쪽) 두 가지. 양방향은 두 언어를 정해야 한다 — <https://soniox.com/docs/stt/rt/real-time-translation>
- `enable_language_identification` 이면 토큰마다 `language`, 그리고 `translation_status`(`original` · `translation`)가 붙는다 — 같은 문서.
- `context` 는 `general` · `text` · `terms` · `translation_terms`(`source` · `target`) 네 칸, 전체 8,000토큰(약 1만 자) 한도, 넘으면 `invalid_request` — <https://soniox.com/docs/stt/concepts/context>
- 용어집 158행으로 상대 언어 하나 기준 `terms`(ko) + `translation_terms`(ko → 그 언어)를 JSON 으로 만들면 약 8,300~9,700자(zh · yue 가 가장 짧고 th 가 가장 길다). 토큰 기준 한도 안인지는 실물 호출로만 확정된다.

### ccc 통역 원형

- cc-prototype 의 통역은 back 이 WebSocket 으로 중계한다 — 마이크 PCM → back → Soniox STT(two_way) → 자막, 확정 발화 번역문 → Soniox TTS → PCM → 스피커. TTS 재생 중에는 마이크를 멈춘다(반이중, 스피커 되먹임 방지). 근거: `orchestration/work/_archive/cc-prototype/sts-prototype/`.
