# 실물 음원 세 벌 e2e — 결과 보고

## 한 줄

**하네스는 돌았고 실물 음성도 끝까지 갔다. 그런데 세 벌은 «확인할 수 없었다» —
지금 떠 있는 API 프로세스가 세 벌 커밋(`51ecceb`) «이전» 코드다.** 스택은 건드리지 않았다.

---

## 돌았나 — 돌았다

`frontend/scripts/meeting-three-tracks-e2e.mjs` 가 로그인 → 빠른 시작 → 실시간 전사 →
종료 → 합성까지 **실제로 밟았다.** 회의 `cdd5199d-2576-484c-b0f4-495a74239938` 가 `done` 으로 끝났다.

### 실시간 전사가 실물 음성에서 말을 건졌나 — **건졌다**

| | 값 |
|---|---|
| 확정 발화 블록 | **29** |
| 총 글자 | **1321** |
| 화자 | **2** (익명 라벨) |
| 마지막 구간 끝 | **195.7초** |

**내용은 옮기지 않는다** — 실제 사람 목소리라 세는 것만 남긴다.
180초를 흘리기로 했고 전사가 195.7초까지 닿았다(마지막 블록이 경계를 걸친다).

### 음원 형식 — **16kHz 를 Chrome 이 그대로 먹었다. 변환 불필요**

발주서가 「16k 를 그대로 먹는지 확인하고 안 되면 `afconvert`」라고 했다. **재서 확인했다** —
스크립트가 브라우저를 띄워 `getUserMedia` 로 받은 소리의 진폭을 직접 읽는다(`audioReaches`).

- 원본 16kHz 그대로: **peak 0.9999** → 소리가 그대로 들어온다. 변환하지 않았다.
- 변환 경로(`afconvert -f WAVE -d LEI16@48000 -c 1`)는 코드에 남겨 두었다 — peak 이 0 에 가까우면
  임시본을 만들고 **끝나면 지운다**. 이번 실행에서는 타지 않았다.
- 원본을 복사하거나 옮기지 않았다.

---

## 세 벌이 갈렸나 — **확인 불가 (환경 문제, 코드 문제 아님)**

단언이 셋 다 「0개」로 떨어졌다:

```
"during": { "memo_agendas": 0, "ai_agendas": 0, "final_agendas": 0 }
"after":  { "memo_agendas": 0, "ai_agendas": 0, "final_agendas": 0 }
"problems": [ 회의 중 AI 벌 없음 / 사람 벌 없음 / 종료 뒤 최종 벌 없음 ]
```

**원인은 화면도 내 단언도 아니다.** 그 회의를 API 로 직접 뜯어 보니:

| 근거 | 관측값 |
|---|---|
| `agendas[0].track` | **`null`** — 응답에 벌 값이 없다 |
| `agenda` 키 | `agenda_id·concluded·last_saved_at·lines·order·source·title·title_placeholder·todos` — **`track`·`merged_from` 이 없다** |
| `line` 키 | `at_ms·author·evidence·line_id·order·text·track` — **`from_lines` 가 없다** |
| `meeting.can_add_agenda` | **`true`** (불리언) — `{memo,ai,final}` 이 아니다 |
| uvicorn(pid 68882) 시작 | **Mon Sep 14 10:39:38** |
| 세 벌 커밋 `51ecceb` | **Mon Sep 14 13:46:27** |

**프로세스가 커밋보다 3시간 먼저 떴다.** 지금 8001 에서 도는 것은 세 벌 이전 코드다.
그래서 서버가 벌 축을 아예 내지 않고, 화면이 `track` 으로 거르면 **모든 안건이 걸러진다.**

### 그런데도 파이프라인은 «한 벌 모양으로» 끝까지 돌았다

같은 회의의 안건 하나를 보면:

```
안건 track=None · source=manual · concluded=False · 줄 track 분포={'ai': 9, 'final': 8} · todos=1
```

**회의 중 배치도 돌았고(ai 줄 9) 종료 합성도 돌았다(final 줄 8).** 다만 0.4.x 모양 그대로다 —
AI 줄과 최종 줄이 **같은 안건 하나에** 매달려 있다. 세 벌이 갈리면 저것이 세 안건으로 서야 한다.

→ **모델·워커·provider 는 실물 음성에서 정상으로 돈다.** 막힌 것은 「어느 코드가 떠 있나」 하나다.

---

## 어디서 깨졌나 — 깨진 자리 없음, 막힌 자리 하나

- 프론트 코드에서 깨진 자리는 **없다.** 화면은 `track` 으로 거르고 서버가 `track` 을 안 준다.
- 백엔드 코드도 아니다 — 커밋에는 들어가 있고 **떠 있는 프로세스가 옛것**이다.
- **스택을 재시작하지 않았다** (발주 금지 사항). API·워커·postgres·vite 전부 그대로 두었다.

### 막은 사고 하나 — 남의 회의를 검사 대상으로 삼을 뻔했다

첫 판에서 회의 id 를 `GET /api/meetings` 의 「진행 중」 첫 건에서 골랐다. **이 기계에서는 사람이
실제 회의를 돌리고 있을 수 있어 그 회의를 집는다.** 빠른 시작 «응답» 에서 id 를 집도록 고쳤다
(`meeting-three-tracks-e2e.mjs:144` `waitForResponse(/quick-start/)`).

---

## 다음에 필요한 것 (사용자 몫)

**API 와 meeting worker 를 지금 코드로 다시 띄우면** 그대로 다시 돌릴 수 있다. 내가 하지 않는다.

```
SCAX_E2E_WAV=".../recordings/2026-09-14-1202-10min.wav" make e2e-meeting-three-tracks
```

기본이 **창을 띄우는 쪽**이고(`SCAX_E2E_HEADED=0` 이면 headless), `slowMo` 250ms 로 클릭이 보이며,
단언이 끝나면 **회의 상세에 머문 채 180초 열어 둔다**(`SCAX_E2E_HOLD`) — 사람이 「메모」·「AI 요약」
탭을 직접 눌러 **두 목록이 갈리는지** 보는 자리다.

## 산출물

- `frontend/scripts/meeting-three-tracks-e2e.mjs` (신규)
- `frontend/package.json` — `e2e:meeting-three-tracks` 한 줄
- `Makefile` — `e2e-meeting-three-tracks` 타깃 + `.PHONY` 한 줄

### 단언이 무엇을 거는가 (돌 준비는 끝났다)

- 회의 중: `memo` 벌과 `ai` 벌이 **따로** 선다 · **AI 줄이 사람 벌 안건에 안 붙는다**(§4.2-9) ·
  AI 벌 안건의 `source` 가 `null`(§4.1-2) · AI 벌에 결론 표시가 없다(§4.0-5)
- 종료 뒤: `final` 벌이 **새로** 섰다 · **원본 두 벌이 개수 그대로 남아 있다**(§4.0-4 · D53) ·
  결론 표시가 최종 벌에만 · `merged_from` 이 최종 안건에 차 있다 · `from_lines` 를 센다
- 실패는 통과로 만들지 않는다 — 문제가 하나라도 있으면 `process.exitCode = 1` 이다

## 지킨 것

스택 무재시작 · 프로덕션/`medi-me` 미접속 · 음원 미복사·미커밋(변환본도 안 만들었고 만들면 지운다) ·
**전사된 말을 로그·보고서에 옮기지 않았다**(세는 것만).
