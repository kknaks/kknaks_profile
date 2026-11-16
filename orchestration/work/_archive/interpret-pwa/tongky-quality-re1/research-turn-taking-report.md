# 조사 리포트 — 세 참여자(D-68): 차례 끝 · 겹친 소리 · 끼어들기 신호 (OQ-034 ~ 036)

- 조사 날짜: 2026-11-16 · researcher 워커(task_14b06088ec08)
- 공식 문서: `docs.soniox.com`(`soniox.com/docs/*` 는 308 로 이 주소로 넘어간다) · 2026-11-16 에 읽음 · 문서에 버전 표기 없음
- 실물 시험: 운영 키 · 운영 `stt_config("zh")` / `stt_config("ja")` 그대로(`stt-rt-v6` · two_way ko↔zh/ja · `max_endpoint_delay_ms` 2000 · `endpoint_sensitivity` -0.3) · 세션 63번 · 실시간 속도(40 ms 조각)
- 시험 파일 · 원본 응답 기록은 레포 밖 scratch `…/scratchpad/probe/`(synth.py · probe.py · analyze.py · logs/ · summary.json)에만 있다. 이 리포트에는 수치만 적었고 문장 · 키는 넣지 않았다
- 표시: **[문서]** = 공식 문서 인용 · **[실물]** = 이번 시험 수치 · **[문서에 없음]**

## 0. 시험 방법과 한계

| 항목 | 내용 |
|---|---|
| 음성 | Soniox TTS(`tts-rt-v2` · 16 kHz)로 직접 만들었다. 재생(되울림) = 운영 음색 `Jiwoo`, 진짜 말 = 다른 음색 `Daniel`. 문장은 시술 안내 · 질문을 직접 지어 썼다(시험 목록 · 실기기 기록 문장은 쓰지 않음). 재생문 ko 3 · zh 3 · ja 1(5.3 ~ 8.1 s), 진짜 말 zh 3 · ko 3(ja 쪽 1 포함) · ja 1(2.1 ~ 3.5 s) |
| 겹친 소리 | 두 PCM 의 말소리 RMS 를 같게 맞춘 뒤 재생 쪽에 비율 g 를 곱해 더했다. **g = 2.0**(재생이 6 dB 큼) · **1.0**(같음) · **0.5**(재생이 6 dB 작음). 재생 시작 0.5 s, 진짜 말은 재생 시작 2.0 s 뒤(재생 한가운데)에 시작. 바닥 잡음 가우스 σ 60 |
| 더 거친 되울림만 | 희미(g 0.2 · 잡음 σ 300 — AEC 잔여 흉내) 6 · 과구동 찌그러짐(g 4.0 · 클리핑 2,700 ~ 4,200 표본) 6 |
| 사례 수 | 겹침 zh 세션 18(방향 A: ko 재생 + zh 말 9 · 방향 B: zh 재생 + ko 말 9) · ja 세션 겹침 2 · 되울림만 8 + 거친 것 12 · 말만 6 · agent text 겹침 6 + 되울림만 8(같은 조건 다시 2 포함) · 차례 끝(Q1) 3 · 합 63 |
| **한계** | ① 실제 폰 스피커 · 방 울림 · 마이크 · 브라우저 `echoCancellation` · `noiseSuppression` 을 거치지 않은, **디지털로 더한 소리**다. 실기기의 되울림은 찌그러지고 늦고 울린다. ② 두 목소리 다 합성이다(사람 말의 망설임 · 겹말 없음). ③ 사례가 적다(조합당 1 ~ 3). 그래서 아래 수치는 「합성 조건에서 이렇다」이고, 「되울림이 반대 언어로 잘못 붙는 비율 0」은 **실기기에서 다시 재야 하는 값**이다 |

---

## Q1 (OQ-034) 차례 끝을 무엇으로 아나

### 답(사실)

| # | 사실 | 근거 |
|---|---|---|
| 1 | 응답 메시지의 최상위 값은 `tokens` · `final_audio_proc_ms`(「Audio processed into final tokens」) · `total_audio_proc_ms`(「Audio processed into final + non-final tokens」)다 | [문서] <https://docs.soniox.com/api-reference/stt/websocket-api> 「Response」 · <https://docs.soniox.com/stt/rt/real-time-transcription.mdx> 「Audio progress tracking」 |
| 2 | 토큰에는 `start_ms` · `end_ms` 가 있다(선택 값). 「Not included if `translation_status` is `translation`」. 그 밖에 `text` · `confidence` · `is_final` · `language` · `translation_status` · `source_language` · `speaker` | [문서] websocket-api 「Field descriptions」 · <https://docs.soniox.com/translation/stt-translation.mdx> 「Timestamps」(「Translated tokens do not include timestamps」) |
| 3 | 소리가 없을 때도 응답이 오는지, 얼마나 자주 오는지 | **[문서에 없음]**. 빈 `tokens` 는 끝(`finished`) 응답 예시에만 나온다 |
| 4 | **소리가 없어도 응답은 온다.** 무음(PCM 0)이든 바닥 잡음이든 빈 `tokens` 응답이 **1,040 ~ 1,080 ms 마다** 오고, 그때마다 `total_audio_proc_ms` 가 약 1,080 씩 오른다. 말하는 동안은 120 ~ 480 ms 마다 온다 | [실물] q1_zeros · q1_noise · q1_bursts(침묵 8 s 구간 각 7 ~ 8개) |
| 5 | `total_audio_proc_ms` 는 보낸 오디오보다 약 200 ms 뒤에 있다 | [실물] q1 세 세션 모든 응답 |
| 6 | **말하는 중에도 「`total_audio_proc_ms` − 마지막 토큰 `end_ms`」 는 0 이 아니라 840 ~ 900 ms 다**(모델이 앞을 더 듣고 토큰을 낸다). 말이 멈추면 그 값이 응답마다 약 1,080 씩 커진다(1,560 → 2,640 → 3,720 …) | [실물] q1 세 세션 |
| 7 | 토큰이 처음 나타나는 때 = 그 토큰 `end_ms` 뒤 **중앙값 1,040 ms**(p10 800 · p90 1,100). 확정되는 때 = 중앙값 1,700 ms(p90 3,160) | [실물] 63 세션 · 토큰 관측 9,624 |
| 8 | `<end>` 는 이번 운영 값(2000 · -0.3)에서 말이 끝난 뒤 **약 560 ms** 에 왔다(첫 문장). 같은 시험에서 두 번째 말(쉼표 뒤 짧은 쉼)은 한 문장 안에서 `<end>` 가 두 번 더 났다 — `<end>` 는 「차례 끝」이 아니라 「문장 · 발화 끝」이다 | [실물] q1_noise · q1_bursts · [문서] <https://docs.soniox.com/stt/rt/endpoint-detection.mdx> 「Overview」(「semantic endpointing … pauses, intonation, speech patterns, and conversational context」) |
| 9 | 비확정 토큰이 나왔다 사라지는 경우(소음): 잡음 덩어리(0.3 s · 0.15 s)만으로는 토큰이 **하나도 나오지 않았다.** 희미한 한국어 재생(g 0.15)이 섞이자 한국어 토큰이 나왔고 그중 비확정 1개가 한 응답에만 보였다가 사라졌다. 같은 글자의 `start_ms` 가 60 ms 바뀌어 다시 나오는 고쳐 쓰기도 1번 보였다 | [실물] q1_bursts · q1_noise |
| 10 | 사라진 비확정 토큰을 알리는 표시는 없다 — 다음 응답의 비확정 목록에서 빠질 뿐이다. 「Once marked final, it will never change」 · 「Final tokens are sent only once and never repeated」 | [문서] real-time-transcription 「How processing works」 · [실물] |
| 11 | Soniox 에 말소리 감지(VAD) 이벤트 · 「말이 멈춤」 이벤트는 없다 | [문서] endpoint-detection 「Overview」(VAD 에만 기대지 않는다는 설명뿐) · 그 밖 이벤트는 **[문서에 없음]** |
| 12 | 무음이어도 오디오를 계속 보내면 연결은 유지된다. 오디오를 안 보낼 때는 20 s 안에 `keepalive` | [문서] <https://docs.soniox.com/stt/rt/connection-keepalive.mdx> 「Key points」 |

### 선택지

| 길 | 어떻게 | 실물로 본 성질 | 걸리는 점 |
|---|---|---|---|
| **A. 서버 시계** — 마지막 「말하는 사람 언어」 토큰이 **도착한 때**부터 back 이 N ms 를 센다 | Soniox 응답을 기다리지 않는다(back 의 타이머) | 토큰은 말한 뒤 약 1.04 s 에 도착하므로, 실제 무음 ≈ N + 약 1.0 s 에서 판정된다(1초 기본값이면 말 끝 → 음성 시작 약 2 s + TTS 시간) | 비확정 토큰이 고쳐 쓰일 때 「새 토큰」으로 셀지(같은 글자 · `start_ms` 만 바뀜)를 정해야 한다 |
| **B. Soniox 진행 값** — `total_audio_proc_ms − 마지막 말 토큰 end_ms` ≥ (N + 약 850) | 응답이 올 때만 잰다 | 말하는 중에도 840 ~ 900 이므로 그만큼 빼야 한다. 무음 중 응답 간격이 약 1.08 s 라 **판정이 1.08 s 단위로 뛴다**(1초 기준이면 실제로는 말 끝 1.6 ~ 2.7 s 에서 판정) | 해상도가 거칠다. 오디오 시각 기준이라 네트워크 지연이 섞이지 않는 것은 장점 |
| **C. `<end>` + 시계** — `<end>` 뒤 N ms 안에 새 말 토큰이 없으면 차례 끝 | `<end>` 는 말 끝 뒤 약 0.5 s(이번 값) | `<end>` 가 문장 중간 쉼에도 나므로 「`<end>` 하나 = 차례 끝」은 아니다. 시계를 같이 써야 한다 | `<end>` 시각은 끊김 값(D-67)에 묶인다 — 끊김 값을 바꾸면 차례 끝도 바뀐다 |
| **D. front 음량** | 마이크 RMS 가 일정 시간 문턱 아래 | **[실물] 재지 않음** · 문서 대상 아님 | 재생 중에는 되울림 · 재생 소리가 음량에 섞인다(개념 `half-duplex-echo-suppression`). 되울림과 말을 음량으로 가를 수 없다. 재생이 없을 때만 믿을 수 있다 |
| **E. `finalize`** | 판정 뒤 `{"type":"finalize"}` 로 남은 비확정을 확정 | 판정 수단이 아니라 판정 **뒤** 확정을 앞당기는 도구. 문서: 「Call `finalize` only after sending approximately 200ms of silence」 · 「too often may cause disconnections」 | [문서] <https://docs.soniox.com/stt/rt/manual-finalization.mdx> 「Key points」 |

- 공통: 재생 언어로 받아쓰인 토큰(되울림 · 규칙 ③ 이 버리는 것)은 「말이 이어짐」으로 세면 안 된다. [실물] 희미한 재생 소리(g 0.15)에서도 재생 언어 토큰이 나왔다 — 그대로 세면 재생이 차례 끝을 계속 미룬다.

### 코디 추천

**A(서버 시계) — 「말하는 사람 언어의 원문 토큰(확정 · 비확정 모두)이 새로 나온 마지막 시각」부터 N ms.** 해상도가 응답 간격(1.08 s)에 묶이지 않고, 재생 언어 토큰을 빼는 규칙 ③ 과 같은 기준(토큰 `language`)을 쓴다. N 은 「토큰 도착이 말보다 약 1 s 늦다」는 것을 넣어 정해야 한다(D-68 의 「말이 멈춘 뒤 1초」를 서버 시계 1초로 두면 실제 무음 약 2 s). B 는 시계 없이 쓸 수 있지만 1.08 s 단위로 뛰는 것이 걸린다. C 는 끊김 값과 엮인다.

---

## Q2 (OQ-035) 겹친 소리에서 받아쓰기 · 언어 태그

### 답(사실)

| # | 사실 | 근거 |
|---|---|---|
| 1 | 언어는 **토큰마다** 붙지만 문장 단위로 맞춰진다: 「Language identification in Soniox is performed at the token level」 · 「the model is trained to maintain sentence-level coherence」. 실시간에서는 「Temporary misclassification of language」 · 「Language tags being revised as more speech context arrives」 | [문서] <https://docs.soniox.com/stt/concepts/language-identification.mdx> 「How it works」 · 「Real-time considerations」 |
| 2 | 겹친 말 · 여러 사람이 동시에 말할 때의 받아쓰기 · 언어 태그 정확도 | **[문서에 없음]** |
| 3 | **진짜 말이 남는 비율(글자 기준 재현율, 진짜 말 언어로 태그된 확정 글자 기준)** — 아래 표 | [실물] |
| 4 | **재생 쪽 글자가 진짜 말 언어로 잘못 태그된 수: 0**(재생이 든 54 세션 — 겹침 26 · 되울림만 16 · 거친 되울림 12 · 확정 재생 글자 합 1,144). **진짜 말 글자가 재생 언어로 태그된 수: 0** | [실물] |
| 5 | 확정 토큰의 언어는 ko · zh · ja 셋만 나왔다(en 등 다른 언어 0). 같은 토큰(같은 `start_ms` · 글자)의 언어가 응답 사이에 바뀐 경우 **0 / 토큰 관측 9,624** | [실물] 63 세션 전체 |
| 6 | 재생 소리가 진짜 말보다 6 dB 크면(g 2.0) 진짜 말이 대부분 사라진다 — 6 세션 중 3 세션은 진짜 말 토큰이 0. 남은 것도 잘못 태그되지는 않았다(사라질 뿐) | [실물] |

**진짜 말 재현율(확정 · 진짜 말 언어 태그)**

| 방향 | g 2.0 (재생 +6 dB) | g 1.0 | g 0.5 (재생 −6 dB) | 말만(기준) |
|---|---|---|---|---|
| A: ko 재생 + zh 말 (3쌍) | 0.21 · 0.31 · 0.00 | 0.93 · 1.00 · 1.00 | 1.00 · 1.00 · 1.00 | 1.00 · 1.00 · 1.00 |
| B: zh 재생 + ko 말 (3쌍) | 0.00 · 0.57 · 0.00 | 1.00 · 1.00 · 1.00 | 1.00 · 1.00 · 1.00 | 1.00 · 1.00 · 1.00 |
| ja 세션: ko 재생 + ja 말 / ja 재생 + ko 말 | — | 0.88 / 1.00 | — | — |

- 재생 쪽 재현율(재생 언어 태그): g 2.0 에서 0.93 ~ 1.00 · g 1.0 에서 0.66 ~ 0.89 · g 0.5 에서 0.55 ~ 0.84 · 되울림만 0.89 ~ 1.00. 즉 **겹치면 재생 쪽이 일부 빠지고**, 더 큰 쪽이 이긴다.
- 「태그된 글자 기준」과 「태그 무관 전체 글자 기준」 재현율이 모든 세션에서 같았다 — 진짜 말이 엉뚱한 언어로 태그되어 숨은 경우가 없다.

**agent text 입력(선택지 비교용 · 아래 Q3 「선택지」 참고)** — 재생할 번역문을 `agent_text` 로 같은 STT 연결에 흘렸을 때

| | 결과 |
|---|---|
| 되울림만 8 세션 | 7 세션은 재생 쪽 글자 **0**(통째로 빠짐). 1 세션(첫 실행)은 0.95 남음 — 같은 조건 다시 2번은 0 |
| 겹침 g 1.0 · 6 세션 | 진짜 말 재현율 **6 / 6 모두 1.00**. 재생 쪽은 5 세션 0 · 1 세션 0.30(앞부분만 남음) |
| two_way 번역과 같이 써도 오류 없음 | [실물] |
| 문서: 「Agent text input is available on `stt-rt-v6`」 · 「The agent's text never appears in the transcript」 · 「Keep your echo cancellation on. Agent text input handles what it leaves behind; it doesn't replace it」 · 재생 0.5 ~ 1 s 앞서 보내라 · 끼어들면 「Send `end_of_segment: true`. Don't send the rest of the reply」 · 입력 텍스트 토큰 요금 | [문서] <https://docs.soniox.com/stt/rt/agent-text-input.mdx> 「Overview」 · 「Send the text in time with the audio」 · 「When the user interrupts」 · 「Pricing」 |
| 이번 시험은 글자를 재생 시간에 **고르게 나눠** 0.7 s 앞서 보냈다(TTS 타임스탬프를 쓰지 않음). 문서는 TTS 문자 타임스탬프(`return_timestamps`)로 맞추라고 한다 — 실패 1 세션이 이 근사 탓인지는 가르지 못했다 | [문서] <https://docs.soniox.com/tts/rt/timestamps.mdx> · [실물] |

### 선택지

| 길 | 무엇에 기대나 | 실물 |
|---|---|---|
| **① 언어 태그로 버리기(D-68 ③ 그대로)** | 재생 언어 토큰 = 되울림 | 합성 조건에서 잘못 태그 0. 재생이 진짜 말보다 크면 진짜 말이 사라지는 것은 막지 못한다 |
| **② ① + agent text** | Soniox 가 재생문을 알고 되울림을 빼 준다 | 재생 쪽이 대부분 아예 안 나옴 · 진짜 말 그대로. 같은 언어로 끼어든 말(D-68 이 「감수」로 버리는 것)도 살릴 수 있을지는 **[실물] 재지 않음** · **[문서에 없음]** |
| ③ front 음량 · AEC 만 | 브라우저 `echoCancellation` | 재지 않음. cc-prototype 에서 폰 스피커 소리를 못 뺐다는 기록(개념 `half-duplex-echo-suppression`) |

### 코디 추천

**① 을 기본으로 만들고, 실기기에서 「재생 소리 대 손님 목소리」 크기부터 잰다.** 합성 조건에서는 언어 태그가 매우 믿을 만했다(잘못 태그 0). 진짜 위험은 태그가 아니라 **크기**다 — 폰 스피커가 마이크 바로 옆이라 손님 목소리보다 6 dB 이상 크게 들어오면 진짜 말이 통째로 사라진다(g 2.0 에서 6 중 3). ②(agent text)는 그 크기 문제를 직접 줄이는 유일한 Soniox 기능이라 실기기 비교 후보로 둔다(SPEC §5.10 이 「쓰지 않는다 — 결정 없음」으로 두었으므로 결정 사항).

---

## Q3 (OQ-036) 끼어들기 신호

### 답(사실)

| # | 사실 | 근거 |
|---|---|---|
| 1 | Soniox 에 끼어들기(barge-in) 이벤트는 없다. agent text 문서는 「If the user starts talking and you stop the agent's playback」 뒤의 할 일만 적는다(판정은 앱 몫) | [문서] agent-text-input 「When the user interrupts」 · 그 밖 **[문서에 없음]** |
| 2 | 진짜 말 시작 → **반대 언어 토큰 첫 도착**(비확정 포함 · k=1): 말만 980 ~ 1,500 ms · 겹침 g 1.0 1,380 ~ 1,780 ms(ja 1,300 · 2,460) · g 0.5 1,380 ~ 1,660 ms · agent text 겹침 1,180 ~ 1,660 ms. 합성 음성의 앞 무음 약 70 ~ 90 ms 포함 | [실물] |
| 3 | 되울림만 있을 때 반대 언어 토큰(비확정 포함)이 나온 수: **0** — 되울림만 16(agent text 8 포함) · 거친 되울림 12 · 겹침 26 세션의 진짜 말 시작 전 구간. 그래서 「몇 개 · 얼마나 이어지나」는 이번 조건에서 잴 것이 없었다 | [실물] |
| 4 | 반대 언어 토큰 낱개 크기: zh · ja 는 거의 한 글자 = 한 토큰(60 ms 짜리 `start_ms` ~ `end_ms`), ko 는 어절 조각 단위. 같은 k 라도 말 길이가 언어마다 다르다 | [실물] |

**기준 후보별 지연(진짜 말 시작 → 기준 충족 응답, ms)** — k = 반대 언어 원문 토큰 수(재생 시작 뒤 확정 + 지금 비확정), t = 그 토큰들의 `end_ms` 최댓값 − `start_ms` 최솟값

| 기준 | 말만(6) | 겹침 g 1.0 (zh 6) | 겹침 g 0.5 (6) | 겹침 g 2.0 (6) | agent 겹침 (6) | 오발 — 되울림만 · 거친 것 · 시작 전(54 구간) |
|---|---|---|---|---|---|---|
| k ≥ 1 | 980 ~ 1,500 | 1,380 ~ 1,780 | 1,380 ~ 1,660 | 3 세션 1,420 ~ 3,060 · 3 세션 못 잡음 | 1,180 ~ 1,660 | 0 |
| k ≥ 2 | 1,220 ~ 1,740 | 1,500 ~ 1,900 | 1,500 ~ 1,900 | 〃 | 1,300 ~ 1,660 | 0 |
| k ≥ 3 | 1,460 ~ 1,980 | 1,620 ~ 1,940 | 1,620 ~ 2,020 | 〃 | 1,420 ~ 1,900 | 0 |
| k ≥ 2 · t ≥ 300 | 1,420 ~ 1,980 | 1,620 ~ 1,980 | 1,620 ~ 2,020 | 2 세션만 | 1,420 ~ 1,900 | 0 |
| k ≥ 3 · t ≥ 500 | 1,460 ~ 1,980 | 1,860 ~ 2,940 | 1,620 ~ 2,140 | 2 세션만 | 1,780 ~ 2,100 | 0 |

- 응답이 120 ~ 240 ms 간격으로 오므로 k 를 하나 올릴 때마다 대략 120 ~ 240 ms 늦어진다.
- 「진짜 말 시작 → 재생 멈춤」의 실제 시간은 위 값 + back → front 전달 + front 재생 멈춤.

### 선택지

| 기준 | 장점 | 단점 |
|---|---|---|
| k ≥ 1 | 가장 빠름(약 1.4 ~ 1.8 s) | 실기기에서 되울림 · 잡음이 반대 언어 토큰 하나를 내면 바로 재생이 끊긴다(합성에선 0 이었지만 실기기는 미측정) |
| **k ≥ 2 또는 3**(t 없이) | 낱개 오발 하나로는 안 끊긴다 · 지연 +120 ~ 360 ms | zh 는 두세 글자, ko 는 한두 어절 조각 — 언어마다 말 길이가 다르다 |
| k + t(예 k ≥ 2 · t ≥ 300) | 길이를 언어와 상관없이 맞춘다 | 이번 결과로는 k ≥ 3 과 거의 같고 더 늦은 경우가 있다 |
| 확정 토큰만 | 오발에 가장 강함 | 확정은 말 끝 뒤 중앙값 1.7 s — 「바로 멈춤」(D-68 기본값)과 맞지 않음 |

### 코디 추천

**k ≥ 2(비확정 포함 · 반대 언어 · 재생 시작 뒤에 나온 토큰 · t 없음)를 시작값으로, 실기기에서 「되울림만」 오발 수를 세어 k 를 1 ~ 3 사이에서 맞춘다.** 근거: 합성 조건 54 구간에서 오발 0 이라 k=1 도 통과했지만, 실기기 되울림은 찌그러지고 울려 문서가 말하는 「Temporary misclassification of language」가 나올 수 있다. k=2 는 k=1 보다 120 ~ 360 ms 늦을 뿐이다. t 는 이번 수치로는 더할 이득이 없었다.

---

## 정할 것 (코디 · 사용자)

1. **차례 끝 판정 방식**(OQ-034) — A 서버 시계 / B Soniox 진행 값 / C `<end>` + 시계 / D front 음량 중 무엇으로. 추천 A.
2. **차례 끝 N** — D-68 기본값 「말이 멈춘 뒤 1초」를 「실제 무음 1초」로 볼지 「마지막 토큰 도착 뒤 1초」(≈ 실제 무음 2초)로 볼지. 토큰이 말보다 약 1 s 늦게 온다는 사실이 이 둘을 가른다.
3. **차례 끝을 셀 토큰** — 비확정 토큰이 고쳐 쓰이는 것(같은 글자 · `start_ms` 만 바뀜)을 「새 말」로 셀지.
4. **끼어들기 기준**(OQ-036) — k 값(추천 k ≥ 2로 시작) · t 를 쓸지 · 「재생 시작 뒤에 나온 토큰만」으로 셀지.
5. **agent text 입력을 쓸지**(SPEC §5.10 이 「결정 없음」으로 둔 것) — 쓴다면 TTS `return_timestamps` 로 재생 위치에 맞춰 보내야 하고(front 재생 위치를 back 이 알아야 함 · 문서는 「서버에서 보낸 시간으로 어림해도 된다」), 입력 텍스트 토큰 요금이 붙는다.
6. **실기기 시험(OQ-035 를 닫는 것)** — 이번 결과는 디지털 합성이라 아래를 폰 스피커로 다시 잰다: ① 재생 소리 대 손님 목소리 크기(dB) ② 되울림만 틀어 둔 채 반대 언어 오발 수 · 지속 ③ 재생 중 손님이 말했을 때 남는 비율. 조건(폰 위치 · 음량 · 방)과 횟수를 정해야 한다.
7. **재생이 진짜 말보다 클 때**(g 2.0 에서 진짜 말 소실 6 중 3) — 재생 음량 상한을 둘지 · agent text 로 풀지 · 감수할지.

## 부록 — 근거 문서

- <https://docs.soniox.com/api-reference/stt/websocket-api> — Response · Field descriptions · Ending the stream
- <https://docs.soniox.com/stt/rt/real-time-transcription.mdx> — How processing works · Audio progress tracking
- <https://docs.soniox.com/stt/rt/endpoint-detection.mdx> — Overview · 끊김 값
- <https://docs.soniox.com/stt/rt/manual-finalization.mdx> — Key points
- <https://docs.soniox.com/stt/rt/connection-keepalive.mdx> — Key points
- <https://docs.soniox.com/stt/concepts/language-identification.mdx> — How it works · Real-time considerations
- <https://docs.soniox.com/translation/stt-translation.mdx> — Token format · Timestamps
- <https://docs.soniox.com/stt/rt/agent-text-input.mdx> — Overview · Send the text in time with the audio · When the user interrupts · Errors · Pricing
- <https://docs.soniox.com/tts/rt/timestamps.mdx> — return_timestamps
