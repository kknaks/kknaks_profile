# 조사 리포트 — Soniox `translation_terms` 는 왜 안 먹히나 (울쎄라 · 써마지 · 美白针)

- 조사: researcher 워커 · **2026-11-16** · 브리프 task_5d1fa79b9a09
- 공식 문서: 2026-11-16 에 받은 `docs.soniox.com/*.mdx`(문서에 날짜 · 버전 표기 없음)
- 운영 코드: `tongky-quality-re1` HEAD `a374b46`(D-68 ~ D-70 반영) · 시드 `2026-11-15.10` · `build_context(G.terms, "zh", context_max_chars("zh"))` = **19,917자 · translation_terms 431 · 뺀 수 0**(SPEC §4.6 `.10` 표와 같음)
- 실물: 운영 키 · `stt_config("zh", …)`(`stt-rt-v6` · two_way ko↔zh · 끊김 2000 / -0.3 · `enable_agent_text_input`) · **662 세션 · 오류 0** · 실시간 속도(40 ms 조각)
- 시험 파일(레포 밖): `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-kknaks-profile--------/6b7f4a9c-bfce-487f-8c42-08de89fd57d4/scratchpad/probe2/`(`synth.py` · `probe.py` · `analyze.py` · `run_*.jsonl` · `logs/`)

## 0. 요약

| # | 답 한 줄 |
|---|---|
| Q1 | **재현된다.** 운영 context 에서 「울쎄라」 는 사전 이름(`美版超声刀`)이 **0 / 72**(단문 42 + 대화 흐름 30)였다. 나온 것은 영문(`Ulsera` · `Ulthera`), 그리고 `美白药` 류였다. 손님 zh 질문 뒤에서는 `美白针` 이 나왔다. 「써마지」 는 57 / 60(시드 `.10` 에 `써마지 → 热玛吉` 가 있다), 「쥬베룩」 은 48 / 48 이다 |
| Q2 | 전체 사전을 넣은 채 **ⓐ ~ ⓕ 어느 조건도 울쎄라 100% 에 닿지 않았다**(최고 4 / 6). **100% 는 짝이 몇 개뿐인 작은 context 에서만** 나왔다: 2 ~ 3짝(`general` · `text` 를 넣든 안 넣든) 울쎄라 70 / 70 · 써마지 52 / 52 · 쥬베룩 18 / 18. 공식 문서는 「강제」 를 말하지 않는다(「leans toward」 · 「only when it fits」) |
| Q3 | **agent text 는 차이를 만들지 않았다**(끔 · 켬 · 켬 + 되울림 모두 15 / 15 같은 꼴). `美白针` 이 나온 조건은 **같은 세션에서 손님이 먼저 `超声刀` 를 말한 것**이다(15 / 15). 손님이 먼저 `美白` 를 말하면 `美白药` 가 나왔다 |
| Q4 | 역방향 짝 `超声刀 → 울쎄라` 를 더하면 손님 문장에 「울쎄라」 가 **6 / 6**(앞에 두든 뒤에 두든) 나왔다. 넣기 전은 「초음파」 6 / 6. 대신 **직원 쪽 울쎄라가 `超声刀` · `超声` 으로 옮겨지는 부작용이 생겼다**(10 / 10). 시드에서 `超声刀` 는 울쎄라 · 슈링크(옛 raw `韩版超声刀` — 2026-10-27 「모호어」 처분)와 겹친다 |
| 보장 | Soniox 설정만으로는 「항상」 이 문서로도 실물로도 서지 않는다. 실물로 100% 가 나온 모양은 하나다 — **그 발화에 걸린 term 의 짝만 넣은 새 세션으로 그 발화 소리를 다시 번역하기**(§5 B). 대가는 실시간 전송이 필요해 생기는 지연(≥ 발화 길이 + 약 0.7 s)과 연결 하나 더이다 |

판정 규칙: zh 번역(확정 토큰 · `translation_status = translation` · `language = zh`)에 사전 이름이 있으면 DICT로 셌다 — 울쎄라 `美版超声刀` · 써마지 `热玛吉`(`美版热玛吉FLX` 같은 다른 term 의 이름 속에 든 것도 셈) · 쥬베룩 `Juvelook`(시드 zh name 이 영문 · `reviewed: false`). 원문 받아쓰기는 모든 세션에서 맞았다(울쎄라 · 써마지 · 쥬베룩 한글 그대로).

## 1. 시험 방식

| 항목 | 값 |
|---|---|
| 음성 | Soniox TTS `tts-rt-v2` · 16 kHz. 직원 문장은 음색 3개(Daniel · Mina · Grace)로 만들고, 실행마다 다른 시드의 잡음(σ 40)을 더했다. 앞 조사 `research-turn-taking-report.md` 와 같은 방식이다 |
| 직원 문장(ko) | **SU** 「울쎄라는 1회 15만 원입니다.」 · **ST** 「써마지는 1회 10만 원이고 쥬베룩은 1회 5만 원입니다.」 (브리프의 두 문장) · 보강용으로 직접 지은 두 문장 **SX** 「울쎄라 받으시면 효과가 일 년 정도 가요.」 · **SY** 「써마지랑 울쎄라를 같이 하시는 분도 많아요.」 |
| 대화 흐름(Q3) | 손님 zh 질문(**F1** 「超声刀做一次多少钱？」 · **F2** 「你们这里有美白的项目吗？」 — 직접 지음) → 1.5 s → 통키 ko 재생(Jiwoo · F1 「초음파 리프팅은 한 번 하는 데 얼마예요?」 · F2 「여기 미백 시술 있어요?」) → 0.8 s → 직원 SU / ST. 조건 셋: **끔**(재생 소리 없음 · agent text 없음) · **켬**(재생 소리 없음 · 재생 시각에 맞춰 agent text 를 글자 수로 고르게 나눠 0.3 s 앞서 보냄 · 끝에 `end_of_segment`) · **켬 + 되울림**(재생 소리를 0.3 배로 섞음 + agent text) |
| 횟수 | 조건 × 문장마다 5 ~ 6회(음색 · 잡음이 다름) |
| 한계 | ① 합성 음성이고, 폰 · 방 · 사람 말의 흔들림이 없다. ② 문장이 넷뿐이다. ③ agent text 는 **ko 재생문만** 시험했다(운영은 zh 재생문도 보낸다). ④ 「100%」 는 「이번 n 회에서 빠짐 0」 이지 보장이 아니다 |

## 2. Q1 — 운영 context 그대로

**답**: 재현된다. 울쎄라 사전 이름 **0 / 72**.

| 조건 | 울쎄라 DICT | 써마지 DICT | 쥬베룩 DICT | 울쎄라 자리에 나온 것 |
|---|---|---|---|---|
| 단문(SU · SX · SY · 세 번 나눠 돌림) | **0 / 42** | 27 / 30 | 18 / 18 | `Ulsera` · `Ulthera` · `美白药` |
| 대화 흐름 F1(손님 `超声刀` 뒤 · agent text 세 조건 합) | **0 / 15** | 15 / 15 | 15 / 15 | **`美白针` 15 / 15** |
| 대화 흐름 F2(손님 `美白` 뒤) | **0 / 15** | 15 / 15 | 15 / 15 | `美白药` 13 · `美白剂` 2 |
| (참고) context 없음 · 단문 | 0 / 6 | 0 / 6 | 0 / 6 | `Ulsera` · `乌塞拉` · 한글 그대로 |

- **[실물]** 운영 기록의 세 갈래(영문 · `美白针` · 사전 이름 0)가 모두 다시 나왔다. 써마지는 사전 짝이 생긴 뒤(시드 `.10` kr-014) 대체로 맞지만 단문에서 3 / 30 이 `热敷剂` 류로 빗나갔다.
- **[실물 · 관찰]** context 가 있을 때 울쎄라 자리에 나온 중국어는 모두 **`美` 로 시작한다**: `美白药` 80 · `美白针` 15 · `美版超声治疗` 10 · `美白乳` 2 · `美白剂` 2 · `美白霜` 1(전체 662 세션 합). context 가 없을 때는 `美` 꼴이 0이다(`Ulsera` · `乌塞拉` · `超声检查` 등). 사전 이름 `美版超声刀` 의 첫 글자에서 시작해 다른 낱말로 흘렀다고 볼 수 있지만, 이것은 **추정**이다. 모델 내부를 설명하는 공식 문서는 없다.
- **[실물]** `美白` 짝(미백 ph-052) 탓이 아니다. `美白` 이 든 짝을 모두 뺀 조건(`k_nomibaek`)에서도 `美白药` 이 3 / 6 나왔다.

## 3. Q2 — 무엇을 바꾸면 사전 이름이 나오나

### 3.1 공식 문서가 `translation_terms` 를 어떻게 말하나

| 내용 | 인용 | 출처 |
|---|---|---|
| 용도 | 「Tell the model how specific words should be translated. Use this only for translation; for transcription, use `terms`.」 · 「To keep a name unchanged in the translation, map it to itself.」 | [문서] <https://docs.soniox.com/stt/concepts/context.mdx> 「Translation terms」 |
| 용도 | 「Use `context.translation_terms` to control how specific words or phrases are translated. This is useful for: Technical terminology. Entity names. Words with ambiguous domain-specific translations. Idioms…」 | [문서] <https://docs.soniox.com/translation/stt-translation.mdx> 「Context and translation terms」 |
| **강제 여부** | 「Context gives the model hints about what it's likely to hear. When a word in the audio could be one of your terms, the model leans toward your term and your spelling.」 · 「The model uses one of your terms only when it fits the rest of the sentence.」 — context 전체에 대한 설명이다. **`translation_terms` 가 반드시 적용된다는 문장은 없다** | [문서] context.mdx 「How context works」 |
| 권장 양 | **`translation_terms` 의 권장 개수 · 순서는 문서에 없음.** `terms` 에 대해서만 「Order doesn't matter, and long lists are fine」 이라고 적혀 있다. `general` 은 「2 to 8 pairs」. 전체 한도는 「Maximum 8,000 tokens (about 10,000 characters)」 · 넘으면 `invalid_request` | [문서] context.mdx 「Terms」 · 「General」 · 「Context size limit」 |
| 형태 | 예시는 모두 짧은 낱말 · 이름 한 쌍이다(`dry needling → punción seca` · `MRI → RM` · `Mr. Smith → Sr. Smith`). 별칭을 어떻게 넣는지, 양방향(two_way)에서 짝의 방향을 어떻게 정하는지는 **문서에 없음** | [문서] context.mdx · stt-translation.mdx |
| 실시간 번역 | 「You can also provide custom translation terms in the context to improve translation accuracy.」 — 「improve」 이다 | [문서] <https://docs.soniox.com/translation/stt-translation/rt-translation.mdx> 「Supported languages」 |
| v6 | 「gets more out of the context you provide」(BASE-001 2026-11-14 인용) | [문서] <https://soniox.com/docs/stt/models.mdx> |

### 3.2 실물 — 변수를 하나씩 (단문 SU · ST · 각 6회 · 별도 표시 없으면 전체 사전에서 하나만 바꿈)

| 조건 | 바꾼 것 | 울쎄라 | 써마지 | 쥬베룩 | 100%? |
|---|---|---|---|---|---|
| 운영(base) | — | 0 / 6 | 6 / 6 | 6 / 6 | ✗ |
| **ⓐ 두 짝만** | `translation_terms` = [울쎄라 → 美版超声刀, 써마지 → 热玛吉] · `general` · `text` · `terms` 그대로 | **6 / 6** | **6 / 6** | 0 / 6(짝 없음 → `朱贝绿`) | 두 term 만 ○ |
| ⓐ 두 짝만 · 흐름 F1 / F2 | 같음 · 손님 질문 뒤 | 5 / 5 · **3 / 5** | 5 / 5 · 5 / 5 | 0 | ✗(F2 에서 `美白乳液` · `美白药`) |
| ⓑ 순서 — 두 짝을 맨 앞 | 431짝 중 [U, T] 를 앞으로 | 0 / 6 | 6 / 6 | 6 / 6 | ✗ |
| ⓑ 순서 — 두 짝을 맨 뒤 | 역방향 짝 뒤로 | 0 / 6 | **0 / 6**(`热敷剂` · `热摩刺`) | 6 / 6 | ✗ — 뒤로 보내면 써마지도 깨짐 |
| ⓒ source 꼴 — 영문 상표 source 더함 | `Ulthera` · `Ultherapy` → 美版超声刀 · `Thermage` → 热玛吉 를 정방향 뒤에 | 0 / 6 | 6 / 6 | 6 / 6 | ✗ |
| ⓒ 영문 역방향 짝 빼기 | source 가 라틴 글자만인 역방향 짝(영문 상표 → 한국어)을 모두 뺌 | 0 / 6 | 6 / 6 | 6 / 6 | ✗ |
| ⓒ 공식 권장 모양 | 운영 짝이 이미 문서 예시와 같은 모양(짧은 이름 → 이름)이다. 더 권하는 모양은 **문서에 없음** | — | — | — | — |
| ⓓ `text` 한 줄 | 「When a procedure in translation_terms is mentioned, always use its target name exactly, never the English brand name.」 를 덧붙임 | 0 / 6(모두 영문) | 6 / 6 | 6 / 6 | ✗ |
| ⓔ `general` 항목 | `{"procedure names": "Chinese market names"}` 더함 | 0 / 6 | 6 / 6 | 6 / 6 | ✗ |
| ⓕ 모델 | v6 그대로가 운영. 비교로 `stt-rt-v5`(base context) | 0 / 6(`美白药` 5) | 6 / 6 | 6 / 6 | ✗ — v5 도 같음 |
| (더) `terms` 에 zh 이름 더함 | `terms` += 美版超声刀 · 热玛吉 | 0 / 6 | 6 / 6 | 6 / 6 | ✗ |
| (더) `terms` 비움 | `terms` = [] | 0 / 6 | 6 / 6 | 6 / 6 | ✗ |
| (더) 역방향 모두 뺌 | 정방향(기본 + 별칭)만 | 4 / 6 | 6 / 6 | 6 / 6 | ✗ — 전체 사전 조건 중 최고 |
| (더) 정방향 기본만 | `forward_only` 와 같은 짝 | 0 / 6 | 6 / 6 | 6 / 6 | ✗ |

**ⓓ 근거**: 공식 문서는 `text` 를 「Longer background, written however you like. It helps most when it mentions the same names and words that come up in the audio」 라고 적는다. 지시문을 넣으라는 쓰임은 **문서에 없음**이다(context.mdx 「Text」). agent text 쪽은 「Don't use agent text for instructions, notes or background information」 이라고 막아 둔다(agent-text-input.mdx 「What to send」).

### 3.3 실물 — 목록의 크기와 구성 (U · T 두 짝 + 다른 정방향 짝 n − 2개, 시드 순서)

| 다른 짝 | 울쎄라 |
|---|---|
| 정방향 앞 8개(n10) · 앞 28개(n30) | 6 / 6 · 6 / 6 |
| 앞 38 · 43 · 48 · 58 · 98개(n40 ~ n100) | 0 / 6 (모두 `美白药` 류) |
| 28 ~ 55번째 28개(w28_30) | 1 / 6 |
| 56 ~ 83 · 84 ~ 111 · 112 ~ 139번째 28개 | 6 / 6 · 6 / 6 · 6 / 6 |
| 28 ~ 39번째를 2개씩 다섯 묶음(w28_4 ~ w36_4) | 다섯 묶음 모두 6 / 6 |

- **[실물]** 원인이 짝 수만은 아니다. 28개를 더해도 어느 구간이냐에 따라 6 / 6 도 되고 1 / 6 도 된다. 그렇다고 짝 하나 탓도 아니다. 28 ~ 39번째 구간의 짝을 2개씩 넣었을 때는 모두 6 / 6 이었다. **어느 짝 조합이 깨뜨리는지는 이번에 가르지 못했다.**
- **[실물]** 문서는 순서를 말하지 않는다. 그런데 써마지 짝을 431짝 맨 뒤로 보내자 6 / 6 → 0 / 6 이 됐다. 「순서 상관없음」 은 `terms` 에 대한 문장이고, `translation_terms` 에는 실물상 순서가 영향을 준다.

### 3.4 Q2 답

- **전체 사전을 넣은 채로 울쎄라를 100% 로 만든 조건은 없다.** ⓐ ~ ⓕ · 순서 · 꼴 · 서술 · `terms` 를 하나씩 바꿔도 0 / 6 이었고, 최고가 4 / 6(역방향을 모두 뺌)이었다.
- **100% 는 짝이 적을 때만 나왔다.** 2 ~ 3짝을 넣은 조건의 합계는 다음과 같다(합성 단문 4종 · 흐름 포함).

| 모양 | 울쎄라 | 써마지 | 쥬베룩 |
|---|---|---|---|
| `translation_terms` 2짝만(다른 칸 없음 · g_min) | 16 / 16 | 16 / 16 | (짝 없음) |
| 3짝만(g_min3 · 쥬베룩 짝 더함) | 18 / 18 | 12 / 12 | 6 / 6 |
| 운영 `general` + `text` + `terms` 3 + 3짝(g_min3_full) | 36 / 36 | 24 / 24 | 12 / 12 |
| 합 | **70 / 70** | **52 / 52** | **18 / 18** |

- 단, 운영 `general` · `text` · `terms` 를 그대로 두고 짝만 2개로 줄인 조건(ⓐ)은 흐름 F2 에서 3 / 5 였다. 작은 context 도 앞 대화가 있으면 흔들릴 수 있다는 뜻이다.

## 4. Q3 — agent text 가 번역에 영향을 주나

**답**: 이번 조건에서는 **영향이 없었다.** `美白针` 이 나온 조건은 agent text 가 아니라 **같은 세션의 앞 손님 발화**였다.

| 흐름 | agent text 끔 | 켬 | 켬 + 되울림 0.3 |
|---|---|---|---|
| F1(손님 `超声刀` 질문 → 재생 → 직원 SU) | `美白针` 5 / 5 | `美白针` 5 / 5 | `美白针` 5 / 5 |
| F2(손님 `美白` 질문 → 재생 → 직원 SU) | `美白药` 5 / 5 | `美白药` 3 · `美白剂` 2 | `美白药` 5 / 5 |
| 써마지 · 쥬베룩(ST) | 10 / 10 · 10 / 10 | 같음 | 같음 |

- **[실물]** 손님 발화 없이 직원 문장만 보낸 단문(Q1 표)에서는 영문이 섞였다. 앞에 손님 zh 발화가 있으면 30 / 30 이 `美白*` 류 중국어였다. 손님이 `超声刀` 를 말한 F1 에서만 `美白针` 이 나왔다(15 / 15 · F2 에서는 0).
- **[실물]** context 가 없을 때 F1 직원 울쎄라는 `超声刀` · `超声检查` 로 옮겨졌다(울쎄라 문장 5 / 5). 써마지 문장의 써마지 자리도 `超声刀` · `超声检查` 로 5 / 5 옮겨졌다. 앞 손님 말에 따라 옮김이 바뀐다.
- **[문서]** agent text 는 「so it knows what the user is replying to」 · 「transcribes the user's reply with that in mind」 · 「The agent's text never appears in the transcript」 라고 적혀 있다. **번역(translation 토큰)에 주는 영향은 문서에 없음.** <https://docs.soniox.com/stt/rt/agent-text-input.mdx> 「Overview」 · 「Why use it」
- **[문서]** 「Agent text and context work well together: context covers the names and words of your business for the whole conversation, and agent text covers what the agent just said.」 (같은 문서 「What to send」)
- 운영 기록에서 `美白针` 이 D-68 배포 뒤 세션에서만 나온 것은 시각이 겹친 것일 수 있다. 같은 세션에 손님 발화가 앞에 있었는지로 다시 보면 가를 수 있다(운영 기록은 이번 범위 밖 — 코디 몫). **zh 재생문(직원 말의 번역)을 agent text 로 보내는 조건은 시험하지 않았다.**

## 5. Q4 — 손님 `超声刀` → 「초음파」

**답**: 역방향 짝을 넣으면 6 / 6 으로 「울쎄라」 가 나왔다. 다만 직원 쪽에 부작용이 있다.

| 조건 | 손님 「超声刀做一次多少钱？」 의 ko 번역 |
|---|---|
| 운영 context | 「초음파」 6 / 6(「초음파를 한 번 하면 얼마인가요?」) |
| `超声刀 → 울쎄라` 를 431짝 맨 뒤에 | 「울쎄라」 6 / 6 |
| `超声刀 → 울쎄라` 를 맨 앞에 | 「울쎄라」 6 / 6 |
| **부작용** — 그 짝(맨 뒤)을 넣은 채 F1 흐름의 직원 SU | 울쎄라 → **`超声刀` 3 · `超声` 2**(사전 이름 0 / 5) · F2 는 `美白药` 5 / 5 |

- **[실물]** 역방향 짝이 반대 방향(ko → zh) 번역에도 영향을 준다. 짝 하나가 한 방향에만 걸리는지 공식 문서에는 **적혀 있지 않다**.
- **시드에서 겹치는 것**(`seed/glossary.json` `.10` · 읽기만):
  - 울쎄라 ph-121 zh `美版超声刀`(raw `Ultherapy（美版超声刀）`) · yue `美版超聲刀`(raw `Ultherapy（超聲刀）`)
  - 슈링크유니버스 ph-126 zh `Shurink Universe` — raw `Shurink Universe（韩版超声刀）`. note 「OQ-018 처분 ① — zh name 모호어(韩版超声刀) → 영문 · **모호어는 alias 에도 두지 않음**(코디 2026-10-27)」
  - `超声` 이 든 다른 이름: HIFU (초음파) ph-131 `聚焦超声`(별칭 `超声波`) · 초음파관리 ph-093 `超声波护理`
  - `超声刀` 자체를 name · alias 로 가진 term 은 없다. raw 로 보면 미국판(울쎄라)과 한국판(슈링크) 둘 다 `超声刀` 다. 이미 한 번 「모호어」 로 처분한 말과 같은 갈래다.
- 결정하지 않는다(§7 「정할 것」 3).

## 6. 「항상」 사전 이름이 나가게 할 길 — 후보 (사용자 요구 2026-11-16)

### 6.1 Soniox 설정만으로 「항상」 이 되나

- **[문서]** 안 된다고 보는 근거: 「leans toward your term」 · 「only when it fits the rest of the sentence」(context.mdx). `translation_terms` 를 강제로 적용한다는 설정 · 옵션은 **문서에 없음**.
- **[실물]** 운영 사전 전체로는 어느 변형도 100% 에 닿지 않았다(§3). 100% 는 2 ~ 3짝 context 에서만 나왔다(70 / 70 · 52 / 52 · 18 / 18). 이것도 n 회 안의 결과일 뿐 문서가 보장하지 않는다.
- **[문서]** context 는 세션 시작 때 한 번만 보낸다 — 「You send context once, when the session starts, and it's used for the whole session」(context.mdx 「How context works」). 그래서 발화마다 짝을 바꿀 수는 없다.

### 6.2 후보 — 원문 term 검출(지금 정확함)을 바탕으로

| # | 길 | 확인된 것 | 대가 · 남는 위험 |
|---|---|---|---|
| **B** | **그 발화만 다시 번역**: 확정 원문에 term 이 걸리고 번역에 사전 이름이 없으면, 그 발화의 마이크 소리(back 이 이미 중계하는 PCM)를 **새 STT 세션**에 다시 보낸다. 새 세션에는 그 발화에 **걸린 term 의 짝만** 넣는다(운영 `general` · `text` + 걸린 term). 나온 번역으로 바꾼다 | [실물] 바로 이 모양(합성 음성 → 새 세션 · 운영 `general` + `text` + 3짝)에서 울쎄라 36 / 36 · 써마지 24 / 24 · 쥬베룩 12 / 12. 다른 칸 없이 짝만 둔 모양까지 합하면 70 / 70 · 52 / 52 · 18 / 18. 새 세션이라 앞 대화의 영향(§4)이 없다 | [문서] 소리는 「in real-time or near real-time speed」 로만 보낼 수 있다(<https://docs.soniox.com/stt/rt/error-handling.mdx> 「Real-time cadence」). 그래서 **지연이 늘어난다 ≥ 발화 길이 + 말 끝 → 번역 확정 중앙값 740 ms(680 ~ 1,140 · 24회 · 운영 context 760 ms 와 같음)**. 시험 문장 기준 2.4 ~ 4.7 s 가 더해진다. STT 연결 하나 더 · 그만큼 오디오 요금(요금표는 이번에 보지 않음). 100% 는 합성 4문장 n 회의 결과다 — 실제 목소리 · 다른 문장에서 다시 재야 한다 |
| **C** | **바로잡기 틀린 꼴 늘리기**(§5.12 ① `wrong` 에 이번에 본 꼴을 더함) | [실물] 울쎄라 자리에 나온 꼴이 **17 가지**다: `美白药` 80 · `Ulsera` 48 · `Ulthera` 27 · `美白针` 15 · `美版超声治疗` 10 · `超声刀` 5 · `超声检查` 3 · `美白乳` · `乌塞拉` · `美白剂` · `超声` · `万事达` 각 2 · `美白霜` · `乌荚拉` · `日光疗法` · `乌尔啥` · 한글 그대로 각 1 | **닫힌 목록이 아니다** — 문장 · 앞 대화에 따라 새 꼴이 나온다(n 이 늘 때마다 늘었다). `美白*` · `超声*` 는 진짜 미백 · 초음파 말과 겹쳐 잘못 갈아 끼울 위험이 있다. 보장이 아니다 |
| **D** | 번역 토큰의 자리를 원문 term 에 맞춰 찾아 바꾸기 | [문서] 안 된다: 「Translated tokens do not include timestamps」 · 「Transcription and translation chunks follow each other, but tokens are not 1-to-1 mapped and may not align」(rt-translation.mdx 「Timestamps in real-time」 · 「Overview」) | 틀린 꼴을 모르면 바꿀 자리를 Soniox 출력에서 찾을 수 없다 — C 의 한계가 여기서 온다 |
| **F** | **사전 이름 덧붙이기**: 걸린 term 의 사전 이름이 번역에 없으면 번역 끝에 사전 이름을 붙인다(예: 「…（美版超声刀）」) | 우리 코드만으로 결정적이다 — 사전 이름이 늘 나간다(만든 방식으로 보장 · Soniox 확인 필요 없음) | 틀린 말(`美白针` 등)은 그대로 남는다 — 손님이 「미백 주사」 와 「울쎄라」 를 함께 듣는다. 자막 · TTS 문구 모양은 SPEC 결정 |

- **확인하지 못한 것**(후보로 올리지 않음):
  - Soniox 에는 **글 번역(text → text) API 가 없다**(<https://soniox.com/docs/llms.txt> 목차 — 제품은 STT · TTS · 음성 번역뿐).
  - 그래서 「원문 글을 사전을 강제하는 번역기 · LLM 으로 다시 번역」 하려면 다른 서비스가 필요하다. 이번에 문서 · 실물을 확인하지 않았다.
  - SPEC 0.8.0 범위는 「LLM 번역으로 바꾸기 · 다른 STT 회사 비교 같은 것은 DEC 에 없다(하지 않는다)」 이다(§1 0.8.0 줄).
  - 비동기 번역(<https://docs.soniox.com/translation/stt-translation/async-translation.mdx>)의 지연도 재지 않았다.

### 6.3 코디 추천

**B 를 실기기 시험 후보로 두고, F 를 B 가 실패했을 때의 마지막 보장으로 묶는 안을 추천한다.** 근거:

- 이번 시험에서 「매번」 이 나온 Soniox 모양은 「짝이 적은 새 세션」 하나뿐이었다(70 / 70). 원문 term 검출이 정확하므로 「어느 짝을 넣을지」 는 이미 안다.
- C 는 꼴이 17 가지로 늘었고 닫히지 않는다.
- D 는 문서상 불가능하다.
- B 의 대가(term 이 걸린 발화만 2.4 ~ 4.7 s + 약 0.7 s 늦어짐)를 받아들일지는 「속도 우선」 결정(interpreter-idea)과 부딪친다. 그래서 사용자 판단이다.

## 7. 정할 것 (코디 · 사용자)

1. **보장 길** — §6.2 B(그 발화 다시 번역 · 지연 ≥ 발화 길이 + 약 0.7 s) · C(틀린 꼴 늘리기 · 보장 아님) · F(사전 이름 덧붙이기 · 틀린 말 남음) 가운데 무엇으로 할지, 몇 개를 묶을지. B 라면 지연을 term 이 걸린 발화에만 받아들일지(「속도 우선」 결정과 부딪침), 다시 번역한 결과에도 이름이 없을 때 F 로 넘어갈지.
2. **보장 범위** — 울쎄라만인가, 모든 term 인가. 써마지도 운영 context 에서 단문 27 / 30 으로 흔들렸다(`热敷剂` 류). 쥬베룩은 사전 이름이 영문(`Juvelook` · `reviewed: false`)이라 「사전 이름 = 영문」 인 term 도 같은 기준으로 볼지.
3. **`超声刀 → 울쎄라` 역방향 짝** — 손님 쪽은 6 / 6 으로 좋아지지만 직원 쪽 울쎄라가 `超声刀` 로 바뀐다(10 / 10). 2026-10-27 「모호어는 alias 에도 두지 않음」(슈링크 `韩版超声刀`) 처분과 같은 갈래라 넣을지 말지는 사전 처분이다.
4. **`translation_terms` 순서 · 구성** — 실물로 순서가 영향을 준다(써마지를 맨 뒤로 보내면 6 / 6 → 0 / 6). 지금 순서(정방향 → 역방향)를 그대로 둘지. 어느 짝 조합이 울쎄라를 깨뜨리는지는 가르지 못했다 — 더 가를지.
5. **agent text 의 zh 재생문 조건** — 이번에는 ko 재생문만 시험했다(영향 0). zh 재생문(직원 말 번역)을 보내는 운영 조건을 따로 잴지.
6. **실기기 · 실제 목소리 다시 재기** — 이번 수치는 합성 음성 4문장이다. B 를 고르면 실제 목소리로 같은 표(§3.4 · §6.2 B)를 다시 재는 시험을 정할지.

— 키 · 운영 기록 문장 0(시험 문장은 브리프의 두 문장 · 직접 지은 것만).
