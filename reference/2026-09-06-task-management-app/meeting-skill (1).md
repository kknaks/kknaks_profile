---
description: 메디솔브 미팅 노트 생성·업데이트. 참석 전 준비(사전 질문·오프닝)와 참석 중·후 기록을 단일 템플릿으로 관리. "미팅 노트 만들어줘", "내일 10시 미팅 준비", "/meeting <주제>" 등의 요청 시 사용.
user_invocable: true
---

메디솔브 미팅(사내 + 외부)의 **사전 준비 → 진행 → 후속 액션**을 한 장으로 관리하는 스킬.

## 목적

- icran는 주 2일 출근 + 비동기 중심 → 미팅마다 **맥락 재구성·결정 사항 추적·후속 액션**이 컨텍스트 단절 흡수의 핵심
- 브리핑 스킬은 "조직 변화 요약", 이 스킬은 "개별 미팅 관리"
- 모든 미팅 노트는 **동일 프레임 + 동일 위치**에 저장 → 회고·검색·Area 노트 연결 일관성

## 저장 위치

```
$OBSIDIAN_VAULT/02_PARA/02_Areas/메디솔브 업무/meetings/YYYY-MM-DD-<주제슬러그>.md
```

- 파일명 슬러그는 한글·kebab 혼용 허용 (예: `2026-04-15-SAY번역-예슬-대정.md`)
- 같은 날 여러 미팅이면 시간 접미사: `2026-04-15-1100-SAY-인수인계.md`

## 템플릿 (frontmatter 필수)

```markdown
---
tags:
  - medisolve
  - meeting
date: YYYY-MM-DD
start: "HH:MM"          # 24h, 따옴표 필수 (YAML이 HH:MM을 숫자로 오인)
end: "HH:MM"
duration_min: 30
location: 3회의실 / Google Meet / 미정
attendees:
  - 한예슬
  - 김대정
  - icran
topic: <한 줄 주제>
status: scheduled       # scheduled | done | cancelled | rescheduled
related_task: <tasks/<name>.md 슬러그>    # 있을 때만
related_project: <Obsidian 프로젝트 노트명>  # 있을 때만
---

# YYYY-MM-DD HH:MM <주제> — <참석자 약어>

> 1-2줄 맥락: 이 미팅이 왜 소집됐는지, 직전 관련 이벤트

## 📌 사전 준비

**상세 컨텍스트 위치 (단일 소스)**:
- 📄 `~/git/medisolve/tasks/<관련 과제>.md` — 섹션 포인터
- 🔗 Confluence/Jira 원문 링크 (출처 명시)

이 미팅 노트는 **진행·결정·후속**에만 집중.

## ⚡ 오프닝 포지션 (1-2줄)

> "<미팅 시작 시 말할 한두 문장>"

icran의 **입장·스코프·역할 분담 제안**을 선언. 오프닝에서 주도권을 잡으면 아젠다 흐름이 정해진다.

## 아젠다 (총 <N>분)

1. **<섹션 1>** (<분>) — Q<번호>
2. **<섹션 2>** (<분>) — ...

## 🎯 In-meeting 필수 질문 (Top N)

### Q1. <질문 제목> (담당자)
> 구체 질문 문장 (한 문장)

답에 따른 분기/판단 기준 요약.

## 추가 질문 (시간 남을 때)

### A. <카테고리>
**Q<번호>. <제목>** (담당자)
"질문 본문"

## 결정 사항 (미팅 중 채움)

- [ ] **결정 항목 1**: _____
- [ ] **결정 항목 2**: _____

## Action Items (미팅 중 채움)

- [ ] <누가> — <무엇을> — <언제까지>
- [ ]

## 메모 (받아적기)

-

---

## 미팅 직후 후속

- [ ] 관련 task 파일 frontmatter 업데이트 (`status`, `requester` 등)
- [ ] 결정·발견을 `knowledge/<해당 파일>.md`에 증류 (예: ax-observations, current-state)
- [ ] 필요 시 CTO·관련자에게 결과 비공식 공유
- [ ] 이 노트 frontmatter `status: scheduled → done`

## 관련 문서

### 1차 참조 (맥락 단일화)
- [<관련 과제/프로젝트 노트>](path)

### 2차 참조
- [[메디솔브 업무]]
- [[기타 Area 노트]]

### Confluence / Jira
- [<페이지 제목> `<ID>`](URL)
```

## 실행 절차

### Step 1 — 미팅 정보 수집

사용자에게 묻거나 캘린더에서 확인:
- 날짜·시작 시각·종료 시각(또는 duration)
- 참석자
- 주제 (1줄)
- 장소 / 링크
- 관련 task 또는 프로젝트

단서가 부족하면 **한 번에 묶어서 질문**. 추측 금지.

### Step 2 — 관련 컨텍스트 찾기

1. `tasks/` 디렉터리에서 주제 관련 과제 파일 검색 (grep topic keyword)
2. `knowledge/` — 관련 제품·조직 노트 포인터 확인
3. Obsidian `02_PARA/01_Projects/` — 관련 프로젝트 노트
4. Slack 최근 덤프 — 해당 채널·참석자 멘션 (출처 기록)
5. Confluence/Jira 인덱스 — 키워드 매칭

**규칙**: 컨텍스트를 이 노트에 복붙하지 말고 **포인터만** 남긴다. 상세는 원본에서 읽는다.

### Step 3 — 노트 생성

1. 경로: `$OBSIDIAN_VAULT/02_PARA/02_Areas/메디솔브 업무/meetings/YYYY-MM-DD-<슬러그>.md`
2. frontmatter 필수 필드 채움 (`start`·`end`는 따옴표 필수)
3. 사전 준비·오프닝·아젠다·Top N 질문까지 **사전 작성**
4. 결정 사항·Action Items·메모는 **빈 체크박스**로 남김 (미팅 중 받아적기)

### Step 4 — 사전 체크리스트 제공

사용자에게 미팅 시작 전 해야 할 액션을 **3-5개로 추림**:
- CTO/키맨 사전 sync 필요한가?
- 시연·데모 자료 준비?
- 원문 링크 탭 열어두기?
- 관련 수치·스크린샷 첨부?

### Step 5 — 미팅 직후 업데이트 (사용자가 다시 요청 시)

1. 결정 사항·Action Items·메모 받아서 해당 섹션 채움
2. `status: scheduled → done`
3. 후속 액션 실행:
   - 관련 task frontmatter 업데이트
   - knowledge 문서에 증류 (ax-observations / current-state / org / products 등)
   - todos.md에 Action Items 반영
   - Daily Note `## 4. 회고` 섹션에 한 줄 요약

## 규칙

- **frontmatter time 필드는 따옴표 필수** — `start: "11:00"` (숫자로 해석되면 파싱 깨짐)
- **출처 명시** — 미팅 소집 배경·사전 시그널 인용 시 `(출처: #채널 MM/DD HH:MM 작성자)` 꼬리표
- **해석과 원문 구분** — 김대정 업무일지에 "인수인계 미팅 참여"가 적혔다고 해서 공식 인수인계라고 단정 금지. "시그널"로만 표시
- **사전 질문은 Top 4 → 전체 나열** 순서로 배치 — 시간 부족 시 자르는 순서가 명확해야 함
- **오프닝 1-2줄 필수** — icran 포지션을 미팅 시작에 선언하지 않으면 방향 잃기 쉬움
- **인수인계·온보딩·첫 sync 미팅이면 Q0(배경·시도 이력) 필수** — 답을 갖고 오기 전에 **상대가 겪은 타임라인·시도·폐기 사유**를 먼저 듣는 오픈 질문 블록을 Top 질문보다 앞에 배치. 주도권을 상대에게 넘기고 청취. 아젠다 시간 배분도 여기 가장 넉넉하게(전체의 30~40%)
  - 소질문 템플릿: (a) 타임라인 (b) 시도한 것들 — 모델/파라미터/아키텍처 차원 (c) 무엇이 막혔나 — 비용·품질·레이턴시·운영·정치 중 주 사유 (d) 현재 바꿀 수 없는 것 vs 여지 있는 것 (e)(f) 각 참석자 개인 경험 (g) 추가 포인터(문서·PR·레포)
  - 산출: "시도 × 폐기 사유 매트릭스" → task 노트 §이전 시도, knowledge/ax-observations 반복 페인으로 증류
- **결정 사항·Action Items는 공란으로 생성** — 미팅 중 받아적을 자리 확보
- 미팅 노트는 **진행·결정 기록용**. 상세 리서치는 task 노트에 단일화

## 파일명 슬러그 가이드

- 길지 않게 (한 줄 안)
- 주제 키워드 + 약식 참석자 표기
  - 예: `2026-04-15-SAY번역-예슬-대정.md`
  - 예: `2026-04-22-PAY기술검토-서형석.md`
- 같은 날 다회 미팅: `YYYY-MM-DD-HHMM-<슬러그>.md`
  - 예: `2026-04-15-1100-SAY인수인계.md`, `2026-04-15-1500-DAY스펙논의.md`

## 유사 스킬 경계

| 스킬 | 범위 | 저장 위치 |
|------|------|----------|
| briefing | 출근일 "지난 간격 조직 변화" 요약 | `briefings/YYYY-MM-DD.md` |
| **meeting** (이 스킬) | 개별 미팅 사전·중·후 | `meetings/YYYY-MM-DD-*.md` |
| Daily Note (Obsidian) | 개인 하루 기록 | `03_Tracking/daily/...` |
| tasks/ (레포) | 과제 단위 리서치·결정 | `~/git/medisolve/tasks/` |

겹치지 않도록: 미팅 결정이 과제에 영향 → **task 업데이트**. 미팅 결정이 조직 사실 → **knowledge 업데이트**. 미팅 그 자체의 흐름 → **meeting 노트**.

## 향후 확장

- `gcal` 연동 → 캘린더 이벤트에서 time/attendees 자동 추출
- 미팅 시리즈(반복 미팅) 체이닝 — 이전 회차 `related_meetings` 링크
- Zoom/Meet 녹취 transcription 자동 첨부
- AI 요약 → 결정 사항·Action Items 추출 (transcription 있을 때)
