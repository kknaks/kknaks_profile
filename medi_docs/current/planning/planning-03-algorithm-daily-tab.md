---
id: planning-03
type: planning
title: 코딩 면접 트레이서 — 키보드 없이 흐름·콜스택 연습
status: draft
created: 2026-05-04
updated: 2026-05-05
sources:
  - "[[planning-01-portfolio-overview]]"
  - "[[spec-01-persona-md-format]]"
  - "[[spec-03-activity-scheduler]]"
tags: [planning, coding-interview, persona, notes, mobile, trace, llm]
---

# 코딩 면접 트레이서 — 키보드 없이 흐름·콜스택 연습

## Summary

해외 코딩 면접 (FAANG·빅테크 스타일) 의 *코드 작성* 이 아닌 **사고 흐름** 을 매일 단련하는 모바일 도장. 한 항목 = 한 문제 (NeetCode 150 시퀀스). 면접 라운드 4단계 (**Clarifying → Approach → Trace → Solution**) 를 그대로 매핑한 카드를 손가락으로 따라가며, 특히 **함수 호출·재귀의 콜스택 추적** 을 시각화로 연습한다. **콘텐츠는 스케쥴러가 매일 자동 박음** — 외부 source (LeetCode GraphQL·neetcode-gh repo) 정규화 + 부족분만 open-kknaks 가 채움. 본인은 모바일에서 풀어보는 *수험자* 역할. 키보드 없는 환경 (지하철·이동 중) 이 오히려 코드 작성 의존을 끊고 사고만 단련하는 데 유리하다는 가설.

---

## 1. 배경·포지션

### 1.1 왜 — 해외 코딩 면접 = 키보드보다 입과 사고

해외 코딩 면접 1라운드 (45–60분, 보통 1문제) 표준 포맷:

| 단계 | 시간 | 무엇을 하는가 |
|---|---|---|
| **Clarifying** | 5분 | 입력 형식·범위·엣지 (`중복 가능?`·`빈 입력?`) — 안 물으면 감점 |
| **Approach** | 5–10분 | 후보 2개 + 복잡도 비교 → 1개 선택 (예: brute O(n²) → hash O(n)) |
| **Code** | 20–25분 | 공유 에디터에서 코딩 + **continuous narration** |
| **Trace** | 5–10분 | 예시 입력으로 **한 줄씩 머릿속 dry-run** |
| **Optimize / QnA** | 남으면 | 메모리·다른 접근·후속 |

평가 축은 정답 < **(a) 끊임없이 narrate 하는 communication, (b) 엣지 케이스 능동 발굴, (c) 복잡도 분석, (d) 힌트 수용**.

### 1.2 통증 — 키보드 없는 환경에서 가장 잘 풀림

- **함수 호출·재귀** 들어가면 "이 호출 끝나면 어디로 돌아오지? caller 의 변수 어떻게 됐지?" 가 머릿속에서 흐려진다.
- 면접장에서 **Trace 단계** 가 곧 이 통증 — 손에 키보드 있어도 해결 안 됨. 머릿속 콜스택을 정확히 따라가야 한다.
- 지하철·이동 중엔 키보드가 없으므로 **코드 작성 의존을 차단** — 강제로 흐름·스택만 보게 됨. 이게 오히려 면접에서 평가하는 근육과 정확히 일치.

### 1.3 기존 채널과의 분담

이미 `Notes` (장기 지식) · `Contents` (스터디·교안) 가 있다.

- **Notes**: "이진 탐색은 정렬된 배열에서 O(log n) 탐색" 같은 **개념 정착**.
- **Contents**: 영상·책·교안 정리.
- **트레이서 (본 기획)**: **단일 문제 1개를 면접 4단계 절차대로 손끝으로 굴려보기** — Notes·Contents 둘 다 아닌 *수행 연습*. 콘텐츠 자체는 source-first 정규화 + LLM gap-filler 로 자동 생성 → 본인은 *학습자* 역할.

---

## 2. 사용자·페이스

| 축 | 결정 |
|---|---|
| **작성 (콘텐츠)** | **스케쥴러 + open-kknaks 자동 생성**. NeetCode 150 시퀀스로 매일 1문제. kknaks 본인은 §4.6 Notes 만 사후 추가 (옵션). |
| **사용 (학습)** | **kknaks 가 모바일에서 트레이스 굴리며 본인 학습**. 사이트는 본인 도장. 방문자도 동일 화면 보기 가능 (서버에 풀이 저장 X). |
| 페이스 | 자동 잡이 하루 1개 박음. 잡 실패 날은 빈 칸. |
| 디바이스 | **모바일 우선** (지하철 가정). 데스크탑은 동일 컴포넌트 반응형. |
| 언어 | narration 본문은 **KO 또는 EN 한 쪽** (LLM 프롬프트에서 정함). 영어 연습은 본인이 면접 직접에서 하므로 양국어 강제 X. |

---

## 3. 제품 형태 — 새 탭 「Interview Trace」

| 요소 | 방향 |
|---|---|
| 진입 | 사이트 상단 네비에 `Notes` / `Contents` 와 동급 **`algorithms`** 탭 |
| 목록 | 날짜 desc, 한 행에 [번호·제목·태그·난이도]. 오늘의 항목은 상단 강조 카드. |
| 상세 | **4 섹션** 세로 스크롤. 모바일 한 손 엄지로 진행 가능. |

**시안 매핑** (`claude_design/kknaks_profile_v2.1.0/proto-algorithms.jsx` in-place 갱신):

| 새 시안 (4 섹션) | 렌더링 블록 (planning §4) | 옛 시안 자리 | 처리 |
|---|---|---|---|
| **§01 Problem** | §4.1 | 옛 §02 Problem | 거의 그대로 + 헤더에 LeetCode source link 추가 |
| **§02 Pre-solve** (Clarifying·Approach 탭) | §4.2 + §4.3 | 옛 §01 Sheet | **컴포넌트 통째 교체** — 3단계 quiz (리스트 → 선택 → 정답 공개), 각 카드 ▾ chevron 으로 이유 펼침 |
| **§03 논리 구조** ⭐ | §4.4 (신규) | (없음) | **신규 컴포넌트** — slot 별 단일 선택 quiz, **core region 한정**. format 다원화 (slot / ordering / state-first) ADR 후보 |
| **§04 Solve · Trace** | §4.5 + §4.6 | 옛 §03 Code · Judge | **컴포넌트 통째 교체** — 코드 read-only + 입력 케이스 N개 (머릿속 dry-run) + worked example 1개 (펼침, 답안지). step-by-step UI · 콜스택 viz · Predict 마커 폐기. 끝에 `Solution` 펼침 |

순서: **문제 → 사전 사고 → 논리 합성 → 문제풀이 (분석·트레이스)** — 면접 라운드의 합성·분석 인지 흐름과 정합. §03 논리 구조 (합성) 와 §04 Trace (분석) 가 **동일한 core region 을 공유** (init·teardown boilerplate 는 빠지고 알고리즘 본질이 드러나는 inner body 에만 집중). **옛 §04 Promote 제거** — 노트 승격은 §5 (다음 버전 보류).

---

## 4. 항목 구조 — 면접 라운드 매핑

> **§4.1 ~ 4.6 는 source-first 자동 생성** — 스케쥴러가 NeetCode 150 시퀀스에서 매일 1문제를 골라 (1) 외부 source (LeetCode GraphQL · neetcode-gh repo 등) 에서 가져올 수 있는 건 다 가져와 정규화하고, (2) source 가 없는 영역만 open-kknaks 가 채운다. **LLM 은 gap-filler 이지 1차 생성기 아님**. 잡 정의는 spec-03, 필드별 source 매트릭스는 §4.8. **§4.7 Notes 는 다음 버전 보류** (본인 사후 메모 — MVP 범위 X).

### 4.1 Problem

- **문제는 자체 출제하지 않는다** — NeetCode 150 (LeetCode) 의 풀이 노트가 본 product 의 본질.
- **Source — LeetCode GraphQL** (`https://leetcode.com/graphql/`, 인증 X). `titleSlug` 로 `title · content · exampleTestcases · constraints · hints · difficulty · topicTags` 한 콜에 회수 → 캐시 → 정규화. LLM 호출 0.
- 본문에 박는 것: (a) 출처 링크 (LeetCode 번호·URL — frontmatter `source` 에 멀티 platform 스키마로), (b) 한 줄 요약 (LeetCode content 첫 문단 trim), (c) 입출력 예시 1–2개 (`exampleTestcases` 파싱).

### 4.2 Clarifying

- LLM 이 **정답 질문 N개 + distractor M개** mix 한 list 를 박는다 (md 본문 yaml). 각 항목마다 LLM 이 같이 생성:
  - 정답 질문 → `why: "왜 좋은 질문인지"` (예: "엣지 케이스 — 빈 입력 처리 빠뜨리면 IndexError")
  - distractor → `why: "왜 던지면 안 되는지 / 왜 무관한지"` (오답 노트용)
- 학습자 (kknaks) UI 4 단계:
  1. **질문지 리스트 출력** — 정답·distractor 섞인 체크리스트
  2. **유저 선택** — 자기가 던질 질문에 체크
  3. **정답 공개** — 어떤 질문이 좋은 질문이었는지 표시 (각 항목 ✅/❌)
  4. **오답 노트** — 잘못 고른 distractor 별 "왜 안 좋은지" + 빠뜨린 정답 질문 별 "왜 좋은 질문인지" 설명 펼침
- 결과는 **세션 메모리만** — 새로고침 시 초기화. 반복 학습 자연스러움. 서버 mutation·frontmatter 변경 X (stateless).

### 4.3 Approach

§4.2 Clarifying 과 **동일한 4단계 quiz 패턴**.

- LLM 이 **정답 후보 N개 + distractor M개** mix 한 list 박음 (각 항목: 접근 이름 + 복잡도). distractor 예: 잘못된 복잡도, 무관한 자료구조, 입력에 안 맞는 접근.
- 각 항목마다 LLM 이 같이 생성:
  - 정답 후보 → `why: "왜 이 접근이 맞는지·트레이드오프"`
  - distractor → `why: "왜 안 맞는지"` (오답 노트용)
- 학습자 UI 4 단계:
  1. **후보 리스트 출력** — 정답·distractor 섞인 체크리스트 (각 항목에 접근 이름 + 복잡도)
  2. **유저 선택** — 자기가 떠올린 접근 (또는 베스트 후보) 체크
  3. **정답 공개** — 어떤 후보가 맞았는지 (✅/❌)
  4. **오답 노트** — 잘못 고른 distractor 별 "왜 안 맞는지" + 빠뜨린 정답 후보 별 "왜 좋은지"
- 결과는 **세션 메모리만** — §4.2 와 동일.

### 4.4 논리 구조 ⭐ — Code 단계의 본질 (코드 합성 quiz)

면접의 **Code 단계 (20–25분)** 는 키보드 X 환경에서 *typing 자체* 가 아닌 **알고리즘 흐름·자료구조·제어 흐름의 합성** 으로 환원된다. 본 블록이 그 자리.

- **핵심 로직 region 한정** — init / 입력 파싱 / fallback return 같은 boilerplate 는 빼고, 알고리즘 본질이 드러나는 inner region (루프 body / 재귀 body / 분기) 만 quiz 화. **§4.5 Trace 와 동일한 core region** 이 1:1 매칭됨 (합성 ↔ 분석).

- **format 다원화** — 패턴마다 적합한 quiz 형태가 다름. ADR 별도 결정 (§9).

  | format | 적합 패턴 | 인터랙션 |
  |---|---|---|
  | `slot` (기본) | array/hash/two-pointer/sliding window/binary search | slot 별 단일 선택 (정답 1 + distractor N) |
  | `ordering` | tree 재귀, backtracking, linked list | step 들을 섞어서 줌 → 학습자가 순서 재배열 |
  | `state-first` | DP, complex state | state 정의 → transition 식 → base case 단계별 |

  MVP 는 **slot 만** (NeetCode 150 의 array/hash/two-pointer 우선 cover). ordering·state-first 는 후속.

- 각 slot/step 마다 LLM 이 같이 생성:
  - 정답 → `why: "왜 이 라인·식이 맞는지"`
  - distractor → `why: "왜 안 맞는지 / 어떤 함정인지"`

- 학습자 UI 3 단계 (Pre-solve quiz 와 동일 패턴):
  1. **slot 또는 step 출력** — format 별 다름
  2. **유저 선택** — slot 별 라디오 또는 step 순서 배열
  3. **정답 공개** — slot/step 별 ✓/✗, 옵션별 ▾ 로 이유 펼침
- 결과는 **세션 메모리만** — §4.2/4.3 와 동일.

- **Source — neetcode-gh 솔루션 코드의 core region 발췌**. core region 판별·format 결정·distractor 생성·why 텍스트는 LLM 영역 (§4.8 매트릭스).

### 4.5 Trace — 머릿속 dry-run 연습 출발점

§4.4 논리 구조 합성 결과를 학습자가 **머릿속으로 직접 dry-run**. UI 는 walk-through *해주지 않음* — 본인이 굴려야 학습 가치 발생.

- **정답 코드** 표시 (read-only) — 보고 머릿속으로 따라가기
- **입력 케이스 N개** (3개 권고) — 각각 머릿속 dry-run 대상. 입력 source = LeetCode `exampleTestcases` 가 1차
- **walked-through 예시 1개** (펼침) — 막히면 답안지 확인. step text 자유 형식 한 줄 (라인 번호·콜스택 시각화 X)

step-by-step interactive stepper · 콜스택 viz · Predict 마커 · subprocess sandbox 통째 폐기. LLM 이 cases + worked_example 한 번에 생성 (open-kknaks). 상세 결정은 ADR-09.

### 4.6 Solution

- **Source — `neetcode-gh/leetcode` repo** (community-maintained, Navi 본인 endorse, MIT). `raw.githubusercontent.com` 으로 slug 별 파이썬 솔루션 fetch → 캐시. 누락 슬러그만 LLM fallback.
- 코드 (길이 ~30줄 권고).
- 복잡도 (시간·공간) — 코드 주석 / README 파싱이 1차, 누락 시만 LLM.
- variations / follow-up 면접관이 던질 만한 후속 1–2 개 — 정형 source 없음 (LeetCode editorial 은 premium 유료) → LLM 전적.

### 4.7 Notes & 노트 승격 — 다음 버전 보류

- 본인이 트레이스 풀어본 사후 메모 (자체 노트 추가) 와 **Notes 그래프로의 승격 파이프라인** 통째 다음 버전 (post-MVP) 으로 보류.
- 본 MVP 의 본인 작성 활동 = **0** (콘텐츠 자동 생성, 학습 stateless). 잔디 카운트는 자동 잡 commit 으로 충분.
- frontmatter `promoted_to` · `related_notes` 필드 미사용 (다음 버전에서 부활).

### 4.8 Source 매트릭스 (필드별 1차 source · LLM gap-filler 경계)

원칙 — **source 가 있으면 source. 없을 때만 LLM**. 정확도·재현성·비용 모두 source 우위. 정규화·캐시·LLM 호출 경계의 구체 파이프라인은 spec-07 에서 명세.

| §4 필드 | source (raw) | LLM 가공 영역 |
|---|---|---|
| §4.1 Problem statement (풀 지문) | LeetCode `content` (HTML 본문) | HTML → plain text 변환 + 한국어 번역 (교육·개인 용도, 2026-05-07 결정) |
| §4.1 Problem constraints | LeetCode `content` (HTML 의 `<strong>Constraints:</strong>` 섹션) | HTML → list[str] 추출 |
| §4.1 Problem io.input | LeetCode `exampleTestcases` | 없음 (`metaData.params.length` 줄씩 split — deterministic) |
| §4.1 Problem io.output | LeetCode `content` (HTML 의 `Output:` 라벨) | HTML → 추출 |
| §4.1 Problem tags · difficulty | LeetCode `topicTags`·`difficulty` | difficulty `.lower()` 만 |
| §4.2 Clarifying 질문 + distractor + why | ❌ 정형 source 없음 | 전적 — 면접관 시뮬레이션 |
| §4.3 Approach 후보 이름·복잡도·why | neetcode-gh 패턴 추론 가능 | 전적 LLM (distractor·trade-off·why) |
| §4.4 논리 구조 정답 코드 | **neetcode-gh code 의 core region 라인 추출** | distractor·why·label·indent·format (slot 기본) |
| §4.5 Trace cases.input | LeetCode `exampleTestcases` | 없음 |
| §4.5 Trace cases.expected | LeetCode `content` (HTML) | HTML → 추출 또는 LLM 시뮬레이션 |
| §4.5 worked_example (step text + 정답) | — | 전적 LLM (NeetCode 150 well-known → hallucination 위험 낮음) |
| §4.6 Solution code | neetcode-gh repo | 없음 (그대로) |
| §4.6 Solution complexity | — | LLM 추론 |
| §4.6 Solution followup | — | 전적 LLM |

**HTML 파싱이 LLM 으로 위임된 이유** — LeetCode `content` 의 example 포맷이 두 종류 (옛 `<pre>` / 새 `<div class="example-block">`) + 트리 문제는 `<img>` 섞임. 정형 파서가 깨끗하게 안 잡혀서 LLM 이 robust. **source-first 정신은 유지** — 정답 코드 라인 + cases input 은 deterministic 추출, LLM 은 *발명* 이 아닌 *추출 + 가공*.

LLM 호출 단위 — **5 단계 파이프라인의 (d) 1회 호출** 에 위 모든 LLM 영역 통합 (raw HTML + 솔루션 코드 → spec-07 yaml 6 키 통째). spec-07 §7 참고.

이 매트릭스가 **§4.1~4.6 의 자동 생성 절차** 의 source-of-truth. spec-07 의 정규화 파이프라인은 이 표를 입력으로 받아 (a) source fetch → (b) 캐시 → (c) 정규화 → (d) 비어있는 칸만 LLM 호출 → (e) md 박음 의 5 단계를 박는다.

---

## 5. 노트 승격 — 다음 버전 보류

이번 버전은 *수험자 도장* 의 핵심 (Pre-solve · 논리 구조 · Trace) 에 집중. Notes·Contents 와 연결되는 노트 승격 파이프라인은 **다음 버전 (post-MVP)** 으로 통째 보류:

- 디자인 §05 Promote 섹션 제거 (시안 4 섹션)
- frontmatter `promoted_to` · `related_notes` 필드 미사용 — 데이터 모델에는 남아있되 렌더링 X (다음 버전에서 부활)
- 목록의 `→ note` 뱃지 제거
- 잔디 카운트는 자동 잡 daily commit 이 그대로 대체 (사용자 활동 트리거 0)

---

## 6. 데이터·API

상세는 후속 **spec-07** 에서. 본 planning 은 모양만 잡는다.

- 페르소나 새 카테고리 — `persona/algorithms/A-NNN-slug.md`.
- 한 항목 = **한 md 파일** — 스케쥴러 잡이 자동 박음 (잡 정의는 spec-03).
- frontmatter + `## Problem / Clarifying / Approach / Logic / Trace / Solution` 헤딩 (Notes 는 다음 버전).
- Trace 시퀀스는 본문에 **fenced yaml** (step 배열) — LLM 이 채운다.
- API 후보: `GET /api/<slot>` (목록·오늘 항목), `GET /api/<slot>/{id}` (디테일). **judge·실행·write API 없음** — 모든 비교는 클라이언트가 yaml 의 정답과 학습자 입력을 비교. 학습자 풀이는 세션 메모리만, frontmatter 변경 X.

---

## 7. 비범위 (이번 product 가 *아닌* 것)

- 코드 에디터 + 채점 (judge) — **명시적 폐기**.
- 사용자 코드 저장·계정·로그인.
- **통과 상태·진척·오답 노트 영구 저장** — stateless. 결과는 세션 메모리만, 새로고침 시 초기화. 학습 진척 시각화는 잔디 (자동 잡 daily commit) 가 대체.
- **자작 문제 출제** — NeetCode 150 풀이 노트가 본질. 자체 콘텐츠 출제는 본 product 범위 외.
- **본인이 직접 풀이·트레이스 작성** — LLM 자동 생성으로 위임. **노트 승격·Notes 는 다음 버전 보류** — 본 MVP 의 본인 작성 활동 0.
- 알고리즘 *개념* 백과사전 — 그건 `Notes` 가 함.
- 점수·랭킹·순위 — 본인 단독 도장이지 경쟁 플랫폼 아님.

---

## 8. 결정 박힘 (오픈 큐 클로즈)

| 항목 | 결정 |
|---|---|
| 문제 출처 | **NeetCode 150** + frontmatter `source` 멀티 platform 스키마 |
| 콘텐츠 생성 | **source-first 정규화 + LLM gap-filler** (§4.8 매트릭스) |
| 카테고리·탭 이름 | **`algorithms`** 유지. 디렉터리 `persona/algorithms/A-NNN-slug.md`, 라우트 `algorithms/A-NNN` |
| §4.4 논리 구조 | **core region 한정** 합성 quiz. MVP format = `slot` (array/hash/two-pointer 우선) |
| §4.5 Trace | **입력 케이스 리스트 + worked example 1개** (머릿속 dry-run). step-by-step UI · 콜스택 viz · Predict 마커 폐기 — 학습자가 직접 굴려야 학습 가치 |
| 디바이스 | **모바일 우선**, 데스크탑은 `m-stack` 으로 동일 컴포넌트 반응형 |
| 초기 백필 | **백필 X** — 출시일부터 1일 1개씩 자동 누적. 스케쥴러가 매일 박음 |
| 노트 승격·Notes | **다음 버전 보류** — MVP 범위 외 |
| 학습자 인터랙션 | **stateless** — 세션 메모리만, 서버 mutation·frontmatter 변경 X |

ADR 후속:
- **논리 구조 quiz format 다원화** (slot · ordering · state-first) — §9 산출물 3
- **Trace yaml 생성 방식** (sys.settrace · LLM 직접 · 검증) — §9 산출물 4

---

## 9. 다음 산출물

| 순서 | 산출물 | 이유 |
|---|---|---|
| 1 | **spec-07** (`spec-07-algorithms-trace`) | 본 product 의 **데이터·API 형식 명세** — 페르소나 슬롯·frontmatter (`source` 멀티 platform) ·논리 구조·Trace yaml 스키마·API · **source 정규화 파이프라인** (§4.8 매트릭스 → fetch · 캐시 · 정규화 · LLM gap-filler 호출 경계 · 실패 처리). 실 SoT 는 per-항목 `persona/algorithms/A-NNN-slug.md` 자체. |
| 2 | **spec-03 갱신** | `neetcode-canonical` 잡 추가 — 매일 NeetCode 150 시퀀스에서 1문제 → §4.8 파이프라인 실행 → md 생성 + commit. open-kknaks 호출은 매트릭스의 LLM 칸에 한정. |
| 3 | **ADR — 논리 구조 quiz format 다원화** | `slot` / `ordering` / `state-first` 3종, LLM 이 패턴별로 결정. **MVP = slot 만** (NeetCode 150 의 array/hash/two-pointer 우선), ordering·state-first 후속. core region 판별 휴리스틱 (loop body / 재귀 body / 분기) 도 같이 결정. |
| 4 | **ADR — Trace 시각화 단순화** | step-by-step interactive UI · sys.settrace · subprocess sandbox 통째 폐기. 코드 + 입력 케이스 N개 + worked example 1개 (LLM 생성, 자유 텍스트) 로 결정. NeetCode 150 well-known 문제라 hallucination 위험 낮음. |
| 5 | **디자인 시안 in-place 갱신** — v2.1.0 `proto-algorithms.jsx` 4섹션 재배치 | 옛 §01 Sheet → §02 Pre-solve (Clarifying·Approach 탭) / **새 §03 논리 구조** (slot quiz) / 옛 §03 CodeJudge → §04 Solve · Trace (콜스택·변수·Predict). **§05 Promote 제거** (노트 승격 다음 버전). 라우트 prefix `A-` 유지. |
| 6 | **api-design** (필요 시) | API 가 단순하면 spec-07 안에서 끝. |
| 7 | **plan** | 시안 → 백 로더 → 프론트 라우트 → 스케쥴러 잡 마일스톤. |

---

## 변경 이력 (요약)

- **2026-05-07 (LLM 통째 위임)** — plan-02 M3 fetch 탐색 결과 반영. LeetCode `content` 가 HTML (옛 `<pre>` / 새 `<div class="example-block">` / 트리 `<img>` 혼재) + Output·constraints 가 별도 필드 X 라 정형 파서가 robust 안 함 → §4.8 매트릭스에서 **HTML 파싱 (statement·constraints·io.output) 도 LLM 책임으로 위임**. 정답 코드·cases.input·tags·difficulty 는 deterministic 그대로. spec-07 §7.1 (c) 단계 *축소* + (d) LLM 호출이 raw HTML 통째 받아 yaml 6키 출력하는 구조로 정정.
- **2026-05-05 (close opens + scope cut)** — §8 오픈 큐 4개 모두 close → **결정 박힘 박스** 로 (탭 = `algorithms`, Predict = 핵심 step 만, 모바일 우선·데스크탑 반응형, 백필 X). **§5 노트 승격·§4.7 Notes 통째 다음 버전 보류** — 시안 §05 Promote 섹션 제거 → 4 섹션. §9 row 1 — spec-07 표현 "본 SoT" → "**형식 명세** (실 SoT 는 per-항목 md)" 정정. §3 매핑 5섹션 → 4섹션.
- **2026-05-05 (logic + core region)** — §4.4 **논리 구조** 신설 (Code 단계의 본질 = 코드 합성 quiz). format 다원화 (slot/ordering/state-first) — MVP 는 slot. §4.4 Trace → §4.5 로 밀고 **core region 한정** 명시 (3–5 step). §4.5~4.7 renumber. §4.8 source 매트릭스에 §4.4 행 추가 + 필드 reference 동기 (Trace 는 core region 만 sys.settrace 실행). §9 산출물에 ADR — 논리 구조 quiz format 다원화 추가.
- **2026-05-05 (source-first)** — §4 전제를 *모두 LLM 자동 생성* → **source-first 정규화 + LLM gap-filler** 로 정정 (Summary·§1.3·§4 prelude·결정 박힌 항목 동기). §4.1 source = LeetCode GraphQL, §4.5 source = neetcode-gh repo (community-maintained, MIT) 명시. §4.4 trace yaml 정확도 — `sys.settrace` 자동 추출이 1차 후보로 강해짐 (LLM 은 narration·Predict 만). **§4.7 신설** — 필드별 source 매트릭스. §9 산출물 — spec-07 에 source 정규화 파이프라인 추가, ADR 명칭/옵션 (b) 우선시 명시.
- **2026-05-05 (layout)** — §3 디자인 매핑을 4섹션 새 안 (Pre-solve 탭 / Problem / Trace / Promote) 으로 정정. §4.3 Approach 도 4단계 quiz 패턴 (§4.2 동일). §4.6 Notes 다음 버전 보류. §9 산출물 4번 — v2.1.0 in-place 갱신 (라우트 prefix `A-` 유지).
- **2026-05-05 (earlier)** — §4.2 Clarifying 인터랙션 명세: 4단계 (리스트 → 선택 → 정답 공개 → 오답 노트). 학습자 입력은 stateless (세션 메모리만), §7 비범위에 "통과 상태·진척·오답 노트 영구 저장 X" 명시, §6 에 "write API 없음" 강조.
- **2026-05-05 (later)** — 콘텐츠 자동 생성 모델로 전환: 스케쥴러+open-kknaks 가 §4.1~4.5 자동 박음, 본인은 §4.6 Notes 만. §7 잔디 절 삭제 (자동 잡 = 잔디 룰과 무관), §7 비범위에 "본인 풀이 작성" 추가, §9 산출물에 spec-03 갱신·LLM trace 정확도 ADR 추가. 결정 박힌 항목: 문제 출처 = NeetCode 150 + 멀티 platform, Trace yaml = LLM 생성.
- **2026-05-05** — 옛 *알고리즘 코드 작성·judge* product 폐기, **면접 트레이서** 로 통째 재정의. spec-07 (옛 알고리즘 SoT) 삭제.
- 2026-05-04 — 초안 (옛 product).
