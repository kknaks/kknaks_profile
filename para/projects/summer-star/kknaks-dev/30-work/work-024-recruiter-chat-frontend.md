---
type: work
id: KDEV-WORK-024
title: "채용담당자 채팅 FE — 홈 재구성 · /chat · 폴링 대화 표면"
status: done
product: kknaks-dev
work_type: new-feature
owner: kknaks
roles:
  pm: "kknaks"
  design: "21-html 시안"
  fe: "worker:frontend"
  be: "—"
  qa: "coordinator"
  ops: "kknaks"
progress: 100
created_at: 2026-08-28
updated_at: 2026-08-28
tags:
  - product/kknaks-dev
  - doc/work
  - status/done
links:
  baselines:
    - "[[baseline-008-recruiter-chat|KDEV-BL-008]]"
  decisions:
    - "[[decision-025-chat-first-home|KDEV-DEC-025]]"
  specs:
    - "[[spec-017-recruiter-chat|KDEV-SPEC-017]]"
  works:
    - "[[work-023-recruiter-chat-backend|KDEV-WORK-023]]"
  releases: []
  related: []
---

# 채용담당자 채팅 FE — 홈 재구성 · /chat · 폴링 대화 표면

SPEC-017 의 화면 전부 — 홈 채팅 히어로(기존 히어로 터미널 대체), `00 Ask` 탭,
`/chat`(사이드바 + 대화 + 폴링). 시각 정본은 `21-html/chat-home-mockup.html`.
**비목표**: 백엔드(WORK-023) · WS · 모바일 사이드바 드로어(OQ — 우선 숨김 처리).

## Meta

- Baseline: KDEV-BL-008
- Covers spec: KDEV-SPEC-017 (§2 U-1~U-6 · §3 S-1~S-8 방문자 측)
- Depends on work: WORK-023 (API — 계약은 spec 으로 고정, 구현 전엔 mock 으로 개발)
- Parallel work: WORK-023 과 병렬 (같은 작업 단위의 분담)
- Follow-up work: 모바일 사이드바 · WS 승격
- External dependency: 시안 `para/.../21-html/chat-home-mockup.html`(코디네이터
  워크트리에서 읽기 전용 제공) — 마크업·토큰을 그대로 옮기는 기준

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner | kknaks |
| Status | done |
| Progress | 100% |
| Branch/PR |  |
| Blocker |  |
| Next | PR (코디네이터) |

## Scope

포함:

- 홈(`/`) 재구성 — 100vh 채팅 히어로(칩 없음 · scroll 큐) + 기존 `LandingPreview`
  스크롤 유지, 히어로 터미널 컴포넌트 제거
- topnav `00 Ask` 탭(+활성 표시)
- `/chat` — 빈 상태 · 사이드바(＋ 새 대화 · 목록 · ← 홈으로) · 스레드
  (`$ ask` 줄 · 답변 블록 · 근거 카드 · tool 단계 박스 U-5a) · 컴포저(대기 중 잠금)
- 2초 폴링 훅 — pending 동안 content/steps 증분 렌더, done/failed 로 중단,
  failed 시 「다시 시도」

제외:

- 백엔드 · 레이트리밋 UI · WS · 어드민 화면(chat_exposed 토글 화면은 WORK-023 의
  admin API 가 생긴 뒤 기존 admin 표면 관례를 따라 이 work P3 에서 최소로)

## Code Surface

- Repo / module: `kknaks_profile` — `app/front/`
- 만질 파일 후보:

| 경로 후보 | 설명 |
|---|---|
| `app/front/app/page.tsx` | 히어로 교체 (LandingPreview 유지) |
| `app/front/components/home/chat-hero.tsx` | 신설 — 시안 이식 |
| `app/front/components/home/hero-terminal.tsx` | 제거 (DEC-025 D1) |
| `app/front/app/chat/page.tsx` | 신설 |
| `app/front/components/chat/*` | 사이드바 · 스레드 · 컴포저 · tool 단계 · 근거 카드 |
| `app/front/lib/chat.ts` | API 클라이언트 + 폴링 훅 + 타입(spec §4) |
| `app/front/components/shell/topnav.tsx` | `00 Ask` 탭 |

- Domain / schema note: DB 안 건드림. 타입은 spec §4 계약에서 수기 정의.

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| 방문자 | SPEC-017 §2 UX | 문구·상태 계약 그대로 (임의 문구 금지) |
| 이 work | SPEC-017 §4 API | BE 미완이면 fixture mock 으로 개발, 통합은 코디 검증 |

## Execution

### Phase 1 — 홈 재구성 + 네비

- **Status**: DONE
- **설명**: 첫 화면 교체. 기존 섹션은 그대로 이어진다.
- **작업**:
  - [ ] `chat-hero` 이식(시안 HTML→컴포넌트, globals.css 토큰만 사용) · 질문 전송 시
        `/chat?q=` 이동
  - [ ] `hero-terminal` 제거 · `page.tsx` 재배선 · topnav `00 Ask`
- **검증**:
  - [ ] `npx tsc --noEmit` 0 에러(만진 파일) · 히어로 100vh + 스크롤 섹션 육안 확인
- **완료 증거**: 2026-08-28 — 워커 구현 + fix1(retry 전환·토큰 밖 색). tsc 0 에러(코디 재현), 로컬 dev(:3000)에서 실 API 연동 확인

### Phase 2 — /chat 페이지 + 폴링

- **Status**: DONE
- **설명**: 대화 표면 본체.
- **작업**:
  - [ ] 페이지 + 사이드바 + 빈 상태 + 스레드 + 컴포저(잠금) — 시안 구조 그대로
  - [ ] API 클라이언트 + 2초 폴링 훅(pending 동안만) · `?q=` 첫 질문 자동 전송
  - [ ] Case Matrix 의 FE 출력(422 문구 · 404 → 빈 상태 · failed → 다시 시도)
- **검증**:
  - [ ] mock 으로 S-1~S-8 흐름 수동 확인 · tsc 0 에러
- **완료 증거**: 2026-08-28 — 워커 구현 + fix1(retry 전환·토큰 밖 색). tsc 0 에러(코디 재현), 로컬 dev(:3000)에서 실 API 연동 확인

### Phase 3 — tool 단계 박스 · 근거 카드 · 어드민 토글 최소 UI

- **Status**: DONE
- **설명**: U-5a(진행 중 쌓임 · 완료 후 접힘) + 근거 카드 + admin 토글.
- **작업**:
  - [ ] steps 증분 렌더(진행 중 뱃지) · 접힘/펼침 · 0건이면 미표시
  - [ ] 근거 카드(type 태그 + 링크) · 기존 admin 목록에 chat_exposed 토글 추가
- **검증**:
  - [ ] mock steps 로 U-5a 상태 3종(진행/완료접힘/0건) 확인 · tsc 0 에러
- **완료 증거**: 2026-08-28 — 워커 구현 + fix1(retry 전환·토큰 밖 색). tsc 0 에러(코디 재현), 로컬 dev(:3000)에서 실 API 연동 확인

## Pre-deploy Check

- [ ] 기존 랜딩 섹션·다른 페이지 회귀 없음 (라우팅·네비만 diff)
- [ ] 폴링이 done/failed 에서 확실히 멈춤 (탭 방치 시 무한 폴링 없음)

## Rollback

- `page.tsx` 히어로 배선 되돌림 + `/chat` 라우트 제거. 상태 없는 UI 라 데이터 영향 없음.

## Done Criteria

- [ ] 모든 Phase DONE
- [ ] SPEC-017 AC 중 화면 측 항목 충족
- [ ] product `log.md` · `30-work/README.md` 갱신 (코디네이터)

## Open Issues

- 모바일(≤720px)에서 사이드바는 v1 숨김(시안과 동일) — 드로어는 후속.

## Related

- SPEC: KDEV-SPEC-017 · Work: WORK-023(BE, 병렬) · 시안: `21-html/chat-home-mockup.html`
