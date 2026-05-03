---
type: project
id: P-10
title:
  ko: "Study Timelapse"
  en: "Study Timelapse"
summary:
  ko: "공부하는 모습을 카메라로 녹화 → 자동 타임랩스 영상 생성. iOS 앱 (Expo + native AVFoundation) + FastAPI 백엔드."
  en: "Record studying with the camera → auto-generate timelapse. iOS app (Expo + native AVFoundation) + FastAPI backend."
category: mobile
status: wip
date: "2026.02"
stack:
  - React Native
  - Expo
  - TypeScript
  - FastAPI
  - Python
  - Postgres
  - FFmpeg
  - AVFoundation
visible: true
thumbnail: /assets/projects/P-10/cover.png
links:
  repo: "github.com/kknaks/study_timelapse"
  live: "https://studylaps-api.kknaks.cloud"
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

공부 시간을 설정하고 카메라로 녹화한 뒤 자동으로 타임랩스 영상(경과 시간 오버레이 포함)을 생성하는 iOS 앱 (`FocusTimelapse` 브랜드명, 번들 ID `com.kknaks.studytimelapse`).

처음에는 PRD 상 웹 MVP (React + Vite) 로 시작했지만, "공부하는 모습 녹화" 라는 유스케이스가 모바일 카메라에 더 잘 맞는다고 판단해 모바일 우선으로 pivot. 백엔드는 FastAPI 단일 서버 (`studylaps-api.kknaks.cloud`) 로 운영.

# 기술스택

**Frontend (Mobile · primary)**
- React Native + Expo (`expo` 55) — 앱 셸
- `expo-router` — 파일 기반 라우팅
- `react-native-vision-camera` v4 — 카메라 녹화
- `expo-camera`, `expo-video`, `expo-media-library`, `expo-sharing` — 미디어
- `@tanstack/react-query` + `axios` — 서버 상태·HTTP
- `expo-secure-store` — JWT 토큰 보관
- `react-native-reanimated` + `react-native-gesture-handler` — 인터랙션

**Native module — `timelapse-creator`**
- Swift / AVFoundation
- 2-pass 렌더링 — 1차 속도 압축 + crop, 2차 CALayer 오버레이 합성
- 온디바이스 처리 — 서버 부하 없음

**Frontend (Web · early MVP)**
- React 19 + Vite + TypeScript

**Backend**
- FastAPI + SQLAlchemy 2 (asyncio) + Alembic
- PostgreSQL (Docker)
- Pydantic v2 schemas
- 4계층 구조 (api/services/repositories/models)

**Auth · 배포**
- Google / Apple OAuth → JWT (백엔드 발급, SecureStore 보관, 401 자동 갱신)
- EAS Build (앱 빌드)
- Docker Compose + nginx reverse proxy
- 도메인: `studylaps-api.kknaks.cloud`

# 주요기능

- **세션 셋업** (`/session-setup`) — 공부 시간 + 출력 시간 입력, 타임랩스 배속 자동 계산
- **포커스 모드** (`/focus`) — 카메라 녹화 + 타이머 (남은 시간 / 경과 시간) + 일시정지·종료
- **타임랩스 생성** (`/generating`) — native module 진행률 콜백
- **결과 확인** (`/result`) — 미리보기 + 오버레이 적용된 영상
- **저장** (`/saving`) — 갤러리 저장 / 공유 (인스타·틱톡·메시지)
- **통계** (`/stats`) — 일·주·월 공부 시간 대시보드
- **인증** (`/login`) — Google / Apple Sign-In
- **유료화** (`/paywall`) — 구독 결제 플로우
- **다국어** — KO / EN / JA / ZH / ES (i18n)

# 아키텍처

```
study_timelapse/
├─ backend/                      ← FastAPI
│  ├─ app/
│  │  ├─ api/v1/                 ← 라우터 (auth, sessions, timelapse, upload, users, stats)
│  │  ├─ services/               ← 비즈니스 로직 (auth_service, jwt_service, timelapse_service, upload_service)
│  │  ├─ repositories/           ← DB 접근
│  │  ├─ models/                 ← SQLAlchemy (User, Session, DailyFocus)
│  │  └─ schemas/                ← Pydantic
│  ├─ alembic/                   ← 마이그레이션
│  └─ Dockerfile
├─ frontend/
│  ├─ mobile/                    ← Expo 앱 (primary)
│  │  ├─ app/                    ← expo-router 라우트
│  │  └─ modules/timelapse-creator/  ← Swift native module
│  ├─ web/                       ← React Vite (early MVP)
│  └─ packages/shared/           ← 공유 타입·상수
└─ docker-compose.yml
```

**핵심 설계 원칙**:
1. **온디바이스 영상 처리** — 타임랩스 생성·오버레이 모두 iOS AVFoundation. 서버 부하 0.
2. **2-pass 렌더링** — 1차 (속도 압축 + crop), 2차 (CALayer 오버레이). 미리보기 후 오버레이 선택 가능.
3. **JWT + SecureStore** — 401 자동 갱신 인터셉터 (axios).

DB 스키마: `User` (OAuth provider + sub) — `Session` (시작·종료·녹화 메타) — `DailyFocus` (집계).

# 핵심 구현

**API 엔드포인트** (`backend/app/api/v1/`):
- `POST /api/v1/auth/{google,apple}` — OAuth 토큰 → JWT 발급
- `POST /api/v1/auth/refresh` — 401 자동 갱신
- `POST /api/v1/sessions` — 세션 시작 (시간·출력 시간 메타)
- `POST /api/v1/upload` — 녹화 영상 업로드 (청크)
- `POST /api/v1/timelapse` — 타임랩스 변환 요청 (서버 fallback 용 — 현재는 native 우선)
- `GET  /api/v1/stats` — 일/주/월 공부 시간 집계

**Native module — `timelapse-creator`**:
- 비동기 진행률 콜백 — RN Bridge 통해 JS 에 progress 푸시
- AVAssetExportSession 으로 1차 속도 압축
- `AVMutableVideoComposition` + `CALayer` 로 오버레이 합성
- VideoTrack `preferredTransform` 적용 — orientation 보정

**디자인 measurement 매칭**:
- 디자인 시안 측정값 → CALayer 좌표·크기 1:1 변환 (`scale`, `labelGap`, watermark size, progressBar height 등)
- 비디오 해상도 / 화면 해상도 비율 보정 (preview 와 export 일치)

# 마주친 문제

> (자동 추론 — 검토 필요. commit log 패턴 기반)

- **오버레이 합성 매트릭스**: `buildOverlay` 의 `layerInstruction` 이 identity matrix 사용 시 회전이 잘못 박혔음 → `videoTrack.preferredTransform` 사용으로 수정
- **double center-crop**: 입력이 이미 output resolution 인데 다시 center-crop 해서 화면 잘림 → 한쪽 crop 제거
- **CALayer 좌표 스케일**: video / screen ratio 가 다른 디바이스에서 오버레이 크기가 미리보기와 export 가 안 맞음 → ratio 기반 스케일 적용
- **텍스트 overflow 잘림**: progress bar 라벨 / watermark 가 layout overflow 로 잘림 → 폭·라인 정책 명시
- **디자인 reference 매칭의 반복**: `scale`, `labelGap`, watermark·logo·progress bar 크기를 reference 디자인과 매칭하기 위해 다수의 미세 조정 fix commit
- **EAS build 에서 XCTest 미지원**: `TimelapseCreatorModuleTests.swift` 제거 (네이티브 테스트는 EAS 환경에서 못 돌림)

# 회고

> (자동 추론 — 검토 필요)

- **모바일 우선 pivot 의 정당성**: PRD 는 웹 MVP → 모바일 Phase 2 였지만, "공부하는 본인을 녹화" 라는 유스케이스 자체가 모바일 카메라에 더 자연스러움. 웹 MVP 는 보류.
- **온디바이스 처리 결정**: 서버 FFmpeg 변환 → iOS native AVFoundation 으로 옮긴 것. 서버 부하 / 변환 비용 / 응답성 트레이드오프에서 모바일 native 가 압도적. 백엔드는 인증·세션·통계 메타데이터만 담당.
- **디자인 매칭의 반복**: 디자인 시안과 native 합성 결과를 1:1 로 맞추는 데에 가장 많은 시간이 들어갔음. iOS layer 좌표 시스템 + video composition transform + 해상도 비율 — 세 축이 곱해져서 측정값을 일일이 보정해야 했음.
- **expo-router 의 장점**: 화면 단위 분리 (`focus.tsx`, `session-setup.tsx`, `generating.tsx`, `result.tsx`, `saving.tsx`, `stats.tsx`) 가 자연스럽게 사용자 플로우와 일치 — 라우트 = 상태가 됨.
- **다음 단계**: TestFlight → 정식 출시 단계 진행 중 (빌드 73·74). 통계 / paywall 모듈은 출시 후 사용 패턴 보고 다듬는 방향.
