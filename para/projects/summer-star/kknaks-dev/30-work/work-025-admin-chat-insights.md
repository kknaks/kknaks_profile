---
type: work
id: KDEV-WORK-025
title: "어드민 채팅 열람·인사이트 — 사이드바 탭 · 대화 목록/상세 · 위젯 3종"
status: done
product: kknaks-dev
work_type: new-feature
owner: kknaks
roles:
  pm: "kknaks"
  design: "21-html/admin-chat-mockup.html"
  fe: "worker:frontend"
  be: "worker:backend"
  qa: "coordinator"
  ops: "kknaks"
progress: 100
created_at: 2026-08-29
updated_at: 2026-08-29
tags:
  - product/kknaks-dev
  - doc/work
  - status/done
links:
  baselines:
    - "[[baseline-008-recruiter-chat|KDEV-BL-008]]"
  decisions:
    - "[[decision-026-anonymous-visitor-session|KDEV-DEC-026]]"
  specs:
    - "[[spec-017-recruiter-chat|KDEV-SPEC-017]]"
  works:
    - "[[work-023-recruiter-chat-backend|KDEV-WORK-023]]"
    - "[[work-024-recruiter-chat-frontend|KDEV-WORK-024]]"
  releases: []
  related: []
---

# 어드민 채팅 열람·인사이트 — 사이드바 탭 · 대화 목록/상세 · 위젯 3종

SPEC-017 §2 U-8(v0.0.15) 구현 — 채용담당자가 무엇을 묻는지 어드민에서 본다.
데이터는 이미 전부 쌓인다(WORK-023) — **조회 API 3종과 화면만 얹는다.**
**비목표**: 대화 개입(답장·삭제) · 사전 집계 테이블 · 알림.

## Meta

- Baseline: KDEV-BL-008
- Covers spec: KDEV-SPEC-017 §2 U-8 · §4 admin chat API 3종(응답 계약 명시됨)
- Depends on work: WORK-023(테이블·데이터) — done
- Parallel work: BE↔FE 분담(같은 발주)
- External dependency: 시각 정본 `21-html/admin-chat-mockup.html`

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner | kknaks |
| Status | done |
| Progress | 100% |
| Branch/PR |  |
| Blocker |  |
| Next | 배포 |

## Scope

포함:

- BE: `GET /api/admin/chat/conversations`(페이지네이션·최신순) ·
  `GET /api/admin/chat/conversations/{id}`(소유 무관 상세) ·
  `GET /api/admin/chat/insights`(totals·recentQuestions·daily 30일·topSources 5)
- FE: 어드민 사이드바 「채팅」 탭 + `/admin/chats` — 위젯 3종(질문 피드·일별 바 차트·
  근거 Top) + 대화 목록 테이블 + 읽기 전용 상세(스레드 렌더 재사용)

제외:

- 검색·필터(후속) · 미답변 질문 위젯(후속 후보) · WS 갱신(정적 로드로 충분)

## Code Surface

| 경로 후보 | 설명 |
|---|---|
| `app/back/api/chat_router.py` 또는 admin 라우터 신설 | admin chat API 3종 (require_admin) |
| `app/back/repository/chat_repo.py` | 목록·집계 쿼리 (daily 는 date_trunc, topSources 는 jsonb 전개) |
| `app/back/schemas/chat.py` | admin 응답 스키마 |
| `app/front/app/admin/(panel)/chats/page.tsx` | 신설 — 시안 이식 |
| `app/front/components/admin/chat-*` | 위젯·목록·상세 |
| `app/front/components/chat/*` | 스레드 렌더 재사용(수정 최소) |
| admin 사이드바/네비 컴포넌트 | 「채팅」 탭 추가 (기존 관례) |

- Domain / schema note: **DB 무변경** — migration 0.

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| FE | spec §4 admin 응답 계약 | 필드명 임의 변경 금지 — mock 으로 병행 가능 |

## Execution

### Phase 1 — BE: admin chat API 3종

- **Status**: DONE
- **작업**:
  - [ ] 목록(페이지네이션) · 상세(공개 상세 shape 재사용 + sessionId) · 인사이트
        (요청 시 집계 — daily 빈 날 0 채움, topSources 는 sources jsonb 전개 count)
  - [ ] admin 인증 — 기존 `require_admin` 관례, 계층 규약 준수
- **검증**:
  - [ ] 새 테스트: 목록 정렬/페이지 · 상세 소유무관 · 인사이트 집계(빈 날 0·Top 순서) ·
        비인증 401/403
- **완료 증거**: 2026-08-29 — BE 17 신규 테스트 + 기존 56 회귀(코디 재현 186 전체) · FE tsc 0 · 로컬 실데이터(대화 12건) 화면 확인. sources jsonb 'null' 실버그 1건 발견·수정(재시도 경로의 실제 운영 값)

### Phase 2 — FE: 사이드바 탭 + /admin/chats

- **Status**: DONE
- **작업**:
  - [ ] 사이드바 「채팅」 탭 (기존 admin 네비 관례)
  - [ ] 위젯 3종 — 시안 그대로(질문 피드 클릭→상세 · 30일 바+hover 툴팁+요약 3수치 ·
        근거 Top 5 막대). 차트는 라이브러리 없이 시안의 CSS 바 방식
  - [ ] 대화 목록 테이블(페이지네이션) → 행 클릭 상세(스레드 렌더 재사용 — tool 단계·
        근거 카드, 읽기 전용)
- **검증**:
  - [ ] `npx tsc --noEmit` 0 · 시안 대비 육안(위젯 3·목록·상세 전환)
- **완료 증거**: 2026-08-29 — BE 17 신규 테스트 + 기존 56 회귀(코디 재현 186 전체) · FE tsc 0 · 로컬 실데이터(대화 12건) 화면 확인. sources jsonb 'null' 실버그 1건 발견·수정(재시도 경로의 실제 운영 값)

## Pre-deploy Check

- [ ] admin 미인증 접근 전부 차단(3 API + 페이지)
- [ ] 응답에 쿠키 토큰·해시 등 세션 비밀 미포함(sessionId 는 정수 id 만)

## Rollback

- 라우터 미등록 + 탭 제거. DB 무변경이라 데이터 영향 없음.

## Done Criteria

- [ ] 전 Phase DONE · spec U-8 AC 충족 · 로컬에서 실데이터로 화면 확인

## Open Issues

- 미답변(「기록에 없다」) 질문 모아보기 위젯 — 후속 후보(콘텐츠 보강 신호)

## Related

- SPEC: KDEV-SPEC-017 §U-8 · 시안: `21-html/admin-chat-mockup.html`
