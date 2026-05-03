---
type: project
id: P-05
title:
  ko: "Language Diary"
  en: "Language Diary"
summary:
  ko: "AI 와 음성 대화로 일기를 만들고 영어 학습 포인트를 제공하는 모바일 앱"
  en: "Voice-conversation diary app that auto-generates English entries and surfaces learning points"
category: mobile
status: wip
date: "2026.02"
stack:
  - FastAPI
  - React Native
  - Expo
  - Postgres
  - Redis
  - WebSocket
  - OpenAI
  - ElevenLabs
  - Docker
visible: true
thumbnail: /assets/projects/P-05/cover.png
links:
  repo: "github.com/kknaks/language_diary"
# 포트폴리오 PDF 케이스 스터디 (planning-02 §3.3) — 비면 PDF 에 미표시.
problem:
  ko: ""
  en: ""
approach:
  ko: []
  en: []
impact:
  ko: []
  en: []
learnings:
  ko: []
  en: []
troubles: []
---

# 개요

AI 와 음성 대화로 오늘 있었던 일을 자연스럽게 이야기하면, AI 가 질문하며 맥락을 이어가 대화를 종합해 영어 일기를 자동 생성하는 언어 학습 모바일 앱. 생성된 일기에서 핵심 단어/구문을 학습 포인트로 제공하고, TTS 로 모범 발음을 들으며 학습한다. Phase 2 에서 따라 말하기 (발음 평가) 추가 예정.

# 기술스택

**모바일 (`frontend/`)**
- React Native + **Expo (SDK 54)** — iOS/Android
- expo-router — 파일 기반 라우팅 + tabs
- **expo-audio + @siteed/expo-audio-studio** — 음성 녹음/재생 (대화의 핵심)
- expo-auth-session — 소셜 로그인 (Google / Apple / Kakao)

**백엔드 (`backend/`)**
- FastAPI + **WebSocket** — 대화 세션의 실시간 양방향 통신
- SQLAlchemy (async) + asyncpg + Alembic
- Redis — 캐싱 + 세션 상태

**AI / 음성**
- **OpenAI API** — 대화 엔진 + 일기 생성 + 번역 + 학습 포인트 추출
- **ElevenLabs STT** — WebSocket 경유 실시간 스트리밍 STT (한국어/영어)
- **ElevenLabs TTS** (서버사이드 + 캐싱), fallback OpenAI TTS
- **Azure Speech SDK** — 발음 평가 (Phase 2)

**인프라**
- PostgreSQL + Redis + Docker Compose (개인 서버 배포)
- 파일 저장 — 로컬 디스크 (MVP) → MinIO/S3 (Phase 2)
- 인증 — 하드코딩 (MVP) → JWT (Phase 2)

# 주요기능

**Tabs** (`(tabs)/`):
- **홈** (`index`) — 오늘 대화 시작 진입점
- **일기 작성** (`write`) — AI 와 음성 대화 → 영어 일기 자동 생성
- **히스토리** (`history`) — 과거 일기 + 학습 포인트 복습
- **마이페이지** (`mypage`)

**온보딩** (`onboarding/step1~5`):
1. 학습 언어 선택
2. AI 아바타 선택
3. AI 음성 톤 선택
4. AI 성격 선택
5. 본인 영어 레벨 선택

**대화 흐름**:
1. AI 가 한국어로 질문 ("오늘 하루 어땠어?")
2. 유저가 음성 답변 (한국어/영어 혼용)
3. ElevenLabs STT 가 WebSocket 으로 실시간 스트리밍 인식
4. AI 가 맥락 이어가며 추가 질문
5. 대화 종합 → OpenAI 가 영어 일기 텍스트 생성
6. 핵심 단어/구문 학습 포인트 표시 + TTS 발음 듣기

# 아키텍처

```
language_diary/
├─ frontend/            ← React Native (Expo)
│  └─ app/
│     ├─ (tabs)/        ← 4탭
│     ├─ onboarding/    ← 5단계
│     ├─ login.tsx
│     └─ _layout.tsx
├─ backend/             ← FastAPI
│  └─ app/api/v1/
│     ├─ auth.py
│     ├─ user.py
│     ├─ convai.py      ← 대화 + WebSocket
│     └─ tasks.py
├─ docs/                ← 16+ 설계 문서 (PRD, API, DB, ELEVENLABS_*, AEC_DIAGNOSIS)
├─ scripts/
└─ docker-compose.yml   ← backend + db + redis
```

**데이터 흐름**:
1. 모바일 → WebSocket 연결 (`/api/v1/convai/...`)
2. 모바일 → 음성 chunk 스트림 → backend → ElevenLabs STT (forward) → 텍스트 chunk 수신
3. backend → OpenAI 호출 (대화 응답 생성)
4. backend → ElevenLabs TTS → 응답 음성 chunk 스트림 → 모바일 재생
5. 세션 종료 시 → backend → OpenAI (대화 종합 + 일기 + 학습 포인트) → DB 저장

**외부 의존**:
- OpenAI API (GPT, 일기 생성, 번역, 학습 포인트)
- ElevenLabs (STT WebSocket + TTS)
- Azure Speech SDK (Phase 2 — 발음 평가)

# 핵심 구현

**WebSocket 음성 파이프라인** (`backend/app/api/v1/convai.py`)
- 모바일 ↔ backend ↔ ElevenLabs 3노드 WebSocket relay
- backend 가 STT/TTS 라이센스 키 보호 (서버사이드만)
- chunk 단위 forwarding 으로 latency 최소화

**음성 입력** (`frontend/`)
- expo-audio + expo-audio-studio — 모바일 측 raw audio 캡처
- base64 인코딩 후 WebSocket 으로 전송
- AEC (Acoustic Echo Cancellation) 처리 — `docs/AEC_DIAGNOSIS.md` 참고

**대화 종합 → 영어 일기**
- `tasks.py` 가 비동기 작업 (대화 종료 → OpenAI 호출 → 일기 + 학습 포인트 생성)
- DB 저장 후 모바일에 push

**문서 풍부**: `docs/` 16+ 설계 문서 (PRD 38KB, SPRINT_PLAN, API_DESIGN_BACKEND/FRONTEND, ELEVENLABS_* 5개, DB_MODEL, AEC_DIAGNOSIS, flow.md 등) — 의사결정 추적성 높음.

# 마주친 문제

> 자동 추론 결과 — 사용자 검토 필수.

- **(자동 추론)** **AEC (Acoustic Echo Cancellation)** — `docs/AEC_DIAGNOSIS.md` 별도 문서. AI 음성과 사용자 마이크 입력의 echo 제거가 모바일 음성 대화의 핵심 challenge.
- **(자동 추론)** **STT 클라이언트 vs 서버사이드 결정** — `DISCUSSION_STT_BACKEND.md` / `DISCUSSION_STT_FRONTEND.md` / `ELEVENLABS_CLIENT_SIDE.md` / `ELEVENLABS_SEVER_SIDE.md` 4개 문서로 길게 토론한 흔적. 결국 서버사이드 + WebSocket relay 채택.
- **(자동 추론)** **오디오 fix 작업** — `PLAN_AUDIO_FIX.md` 별도 문서. 모바일 오디오 처리 안정화.
- **(자동 추론)** **180 커밋, 1 개월** — 빠른 반복 사이클. README 부재 + PRD/SPRINT_PLAN 중심 작업.

# 회고

> 자동 추론 결과 — 사용자 검토·교체 필수.

- **(자동 추론)** PRD 38KB / SPRINT_PLAN 16KB 라는 양은 사전 설계에 시간을 많이 쓴 패턴. 음성 + 실시간 + 외부 SDK 다중 (ElevenLabs/OpenAI/Azure) 조합이라 사전 결정이 quality 에 큰 영향.
- **(자동 추론)** Phase 2 로 미룬 항목 — JWT 인증 / 발음 평가 / S3 저장 / Phase 1 의 MVP 가시화 우선.
- **(자동 추론)** 다음에 시도한다면 — 음성 latency 최적화 (WebSocket relay 의 hop 1개 줄이기), Whisper / Gemini 같은 다른 STT 모델 비교.
