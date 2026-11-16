---
type: work
id: WORK-004
title: "프론트 3페이지 — 셸·토큰 레이어부터 모니터링·데이터·채팅까지"
status: todo
product: ontology-demo
work_type: new-feature
owner: kknaks
roles:
  pm: "kknaks"
  design: "디자인 세션(별도)"
  fe: "@ontology-fe"
  be: "—"
  qa: "coordinator"
  ops: "kknaks"
progress: 0
created_at: 2026-09-02
updated_at: 2026-09-02
tags:
  - product/ontology-demo
  - doc/work
  - status/todo
links:
  baselines:
    - "[[baseline-001-demo-agent-app|BASE-001]]"
  decisions:
    - "[[decision-004-web-three-pages-in-front|DEC-004]]"
    - "[[decision-002-pii-masking-boundary|DEC-002]]"
    - "[[decision-005-internal-demo-deploy|DEC-005]]"
  specs:
    - "[[spec-004-three-screens|SPEC-004]]"
  works:
    - "[[work-002-tools-and-api|WORK-002]]"
    - "[[work-003-agent-loop-and-chat|WORK-003]]"
  releases: []
  related: []
---

# 프론트 3페이지 — 셸부터 채팅까지

기존 `app/front/`(Next.js 15) 안에 데모 라우트 그룹을 만들고 모니터링 · 데이터 · 채팅
세 화면을 낸다. **포트폴리오 표면을 건드리지 않는다** — `globals.css` · 루트 레이아웃 ·
기존 `/chat` 불변.
**비목표**: API·에이전트(WORK-002·003) · 배포(WORK-005) · 디자인 조정 대기 20건
(SPEC-004 §7.2 — 정정본이 와야 확정되는 시각 상세).

## Meta

- Baseline: BASE-001
- Covers spec: SPEC-004 전체 (U-1~U-15 · §4 · AC-1~AC-23) + SPEC-003 응답 소비 ·
  SPEC-005 `used_edges` 소비
- Depends on work: P1~P3 은 WORK-002(API), P4 는 WORK-003(채팅 API)
- Parallel work: BE 와 병렬 진행한다 — 계약(SPEC-003·004·005)이 고정돼 있으므로
  **mock 으로 선행**하고 API 가 붙으면 교체한다
- Follow-up work: WORK-005(통합·배포)
- External dependency: 디자인 패키지 `reference/ontology_demo/design/` — **시각 토큰
  값의 SoT**(`01-tokens.md`). `.dc.html`·`support.js` 는 참조물이며 **런타임 의존이 아니다.**

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner | @ontology-fe |
| Status | todo |
| Progress | 0% |
| Branch/PR | - |
| Blocker | P1~P3 은 WORK-002, P4 는 WORK-003 (mock 으로 선행 가능) |
| Next | Phase 1 착수(mock 기준) |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks | 범위와 요구사항 | todo |
| Design | 디자인 세션(별도) | 시각 상세 · 조정 대기 20건 | todo |
| FE | @ontology-fe | 세 화면 구현 | todo |
| BE | — | API 는 WORK-002·003 | todo |
| QA | coordinator | AC·파생 카운트·PII 검증 | todo |
| Ops | kknaks | Vercel env | todo |

## Scope

포함:

- 라우트 그룹 `app/(ontology)` + `/ontology/{monitoring,chat,data}`(기본 monitoring)
- 데모 셸(자체 h64 헤더 · 탭 · 기준일 배지) · 토큰 레이어 `--ont-*` ·
  `color-scheme: light` 재선언 · Pretendard(`next/font`) · 최소 폭 안내
- 접속 게이트 화면
- 모니터링(KPI 카드 · 그래프 · 인스펙터 · 예보) · 데이터(계층 탐색 · 표 · 마스킹 ·
  역추적) · 채팅(빈 상태 · 상태 5종 · 답변 6블록 · 칩 점프 · 컴포저)
- 파생 카운트 전건(SPEC-004 §4 표 12항목) — 하드코딩 금지

제외:

- `globals.css` 수정 · 루트 레이아웃 변경 · 기존 `/chat` 변경 — **전부 금지**
- 채팅 우측 근거 그래프 패널 — **두지 않는다**(2026-09-02 확정)
- 컬럼 값 분포 바 — 대응 API 없음(SPEC-004 §7.2 D-18, 제거 권고)
- 반응형(데스크톱 전용) · 다국어(한국어 전용)

## Code Surface

- Repo / module: `kknaks_profile` — `app/front/`
- 만질 파일 후보:

| 경로 후보 | 설명 |
|---|---|
| `app/front/app/(ontology)/layout.tsx` | 데모 셸 · 토큰 스코프 · 폰트 |
| `app/front/app/(ontology)/ontology/monitoring/page.tsx` | 모니터링 |
| `app/front/app/(ontology)/ontology/data/page.tsx` | 데이터 |
| `app/front/app/(ontology)/ontology/chat/page.tsx` | 채팅 |
| `app/front/components/ontology/`(신설 후보) | 카드·그래프·표·칩·인스펙터 |
| `app/front/lib/ontology/`(신설 후보) | API 클라이언트 · 좌표 자산 |
| `app/front/app/globals.css` | **수정 금지 대상**(확인만) |

- Domain / schema note: 해당 없음 — 프론트는 상태를 소유하지 않는다. 페이지 간 공유는
  **URL 쿼리와 세션 쿠키뿐**이고 전역 스토어를 두지 않는다.

## Domain / Schema

해당 없음.

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| WORK-002 API | 계층·KPI·그래프·예보·세션 | 응답 필드를 그대로 쓴다 — 화면이 숫자를 만들지 않는다 |
| WORK-003 채팅 API | conversations·messages·`result` | P4 의 유일한 입력 |
| WORK-005 | 배포된 화면 | 게이트 5-③(하이라이트 = `used_edges`) 검증 대상 |

## Internal Interface Contract

- API 클라이언트는 한 모듈에 모으고, 응답 타입을 SPEC-003 계약 그대로 둔다. 필드가
  어긋나면 **화면에서 변환하지 말고 보고**한다(spec 개정 사안).
- 그래프 좌표 자산은 **확정 `node_id`(snake_case)로 키잉**한다. 디자인 `nodes.json` 의
  camelCase id 를 그대로 쓰지 않는다 — 매핑 표를 손으로 두면 노드가 조용히 사라진다.
- 좌표가 없는 노드가 응답에 있으면 **드러낸다**(조용히 빼지 않는다).

## Execution

### Phase 1 — 셸 · 토큰 레이어 · 폰트 · 접속 게이트 (U-1~U-3)

- **Status**: TODO
- **설명**: 포트폴리오와 데모를 가르는 경계를 먼저 세운다. 여기서 새면 사이트 전체가 샌다.
- **작업**:
  - [ ] 라우트 그룹 `app/(ontology)` + `/ontology/{monitoring,chat,data}`,
        기본 진입 monitoring. **기존 `/chat` 무변경**
  - [ ] 셸 — 자체 h64 헤더(로고·탭 3개·기준일 배지·아바타), 포트폴리오 `TopNav`·
        `PageFooter` 미주입
  - [ ] 토큰 레이어 — `[data-surface="ontology"]` 스코프에 `--ont-*` 선언 +
        **`color-scheme: light` 재선언**. 값은 디자인 `01-tokens.md` 를 따른다
  - [ ] Pretendard `next/font` 도입(CDN `@import` 금지), Mono 는 기존 JetBrains Mono 재사용
  - [ ] 접속 게이트 화면 + 최소 폭 안내(**데모 컨테이너에만** `min-width:1280px`)
- **검증**:
  - [ ] `globals.css` diff 0
  - [ ] 데모 밖 페이지의 색·서체가 변하지 않는다
  - [ ] 산출물에 외부 폰트 요청 0건
  - [ ] 세션 없이 세 라우트 접근 시 게이트, 통과 후 원래 라우트 복귀
  - [ ] 1280px 미만에서 안내가 뜨고 포트폴리오는 영향 없음
- **완료 증거**: 미작성 — `git diff app/front/app/globals.css` 빈 출력 + 세 라우트
  스크린샷(게이트/셸) + 네트워크 탭 폰트 요청 목록 (SPEC-004 AC-1~AC-7)

### Phase 2 — 모니터링 (U-4~U-7)

- **Status**: TODO
- **설명**: 「지금 봐야 할 것 → 왜 그런지 → 다음 위험」이 한 화면에서 이어져야 한다.
- **작업**:
  - [ ] KPI 카드 행 — 알림 → 관찰 → 정상 정렬, `dod`·`unit`·`spark[7]`·`grain` 캡션,
        미관측 카드(`—`·스파크라인 없음), 「그 외 KPI」 내역 파생, 기간 스테퍼
  - [ ] 그래프 SVG(`viewBox 0 0 1130 560`) — 좌표 자산을 확정 `node_id` 로 키잉,
        색=상태 · 모양=타입 · 선=판정 · 굵기=신뢰도
  - [ ] 라벨 매핑 — **엣지 판정은 번역이 없다**(API 값 = 정본 한글값 = 화면 카피:
        채택 · 자동 확정 · 선언 · 보류 · 기각). 번역 축은 **`node_type` 하나**로,
        영문 enum(`kpi`·`intervention`·`organic`·`exogenous`·`unobserved`·`attribute`)을
        화면에 그대로 노출하지 않는다(SPEC-004 U-5 매핑표)
  - [ ] 툴바 토글 — `/api/graph` **1회** 호출 후 클라이언트 필터, 헤더·범례 카운트 연동
  - [ ] 인스펙터(`kind`·`note`·`evidence`·액션 2종) · 예보 카드(`title`·`message`·근거 줄)
  - [ ] `?edge=` 로 진입하면 해당 엣지가 선택 상태
- **검증**:
  - [ ] 화면 코드에 숫자 리터럴로 박힌 카운트 0건
  - [ ] 토글 시 재요청이 발생하지 않는다(네트워크 탭)
  - [ ] 좌표 없는 노드가 있으면 드러난다
- **완료 증거**: 미작성 — 카운트 파생 확인(헤더 `노드 x/y · 엣지 x/y` + 범례) + 토글
  전후 네트워크 요청 수 + `?edge=` 진입 스크린샷 (SPEC-004 AC-8~AC-11)

### Phase 3 — 데이터 (U-13~U-15)

- **Status**: TODO
- **설명**: 「모든 수치는 내려갈 수 있다」를 화면으로 증명하는 자리다.
- **작업**:
  - [ ] 계층 탭 3종(브론즈·실버·골드) — **온톨로지 계층 없음**. 탭 카운트는 응답 파생
  - [ ] 브론즈 칩 2단 — 원천 3(vegas·리뷰·nexus) → nexus 선택 시 하위 14테이블.
        칩은 전부 실제 테이블에 1:1(합성 테이블 금지). 선택 키는 **테이블 이름**
  - [ ] 표 — sticky 헤더 · `1–N / total` 표기 · 행 선택 · 숫자 우측 정렬
  - [ ] 마스킹 바(`masked_fields` 파생) · 중립 바(`chart_no` 모순 없는 카피) ·
        **언마스킹 UI 없음**
  - [ ] 컬럼 상세 — `rule_id`·`gate`·`downstream`·`is_provisional`(`—`+「미확정」)
  - [ ] 「이 원본이 가는 곳」 — `flows_to[]` 파생, 클릭 시 해당 계층·테이블 점프
  - [ ] 컬럼 부분 표시 시 「N개 컬럼 중 M개 표시」
- **검증**:
  - [ ] 브론즈 16테이블 전부에 도달 가능
  - [ ] 화면 어디에도 실명·전화·생년월일 원값 0건
  - [ ] 골드 → 실버 → 브론즈 역추적이 끊기지 않는다
- **완료 증거**: 미작성 — 16테이블 도달 경로 기록 + 역추적 1건 스크린샷 연쇄 +
  PII 화면 스캔 0건 (SPEC-004 AC-17~AC-20·AC-22)

### Phase 4 — 채팅 (U-8~U-12)

- **Status**: TODO
- **설명**: 디자인에 없던 **진행 상태 5종**이 여기서 처음 화면이 된다. 스피너만 도는
  구간을 만들지 않는다.
- **작업**:
  - [ ] 빈 상태 — 히어로 + 시작 카드 4장(dot·상태 라벨만 알림 KPI 파생, 질문·메타는 정적)
  - [ ] 컴포저 — 1,000자 검증 · `pending` 중 잠금 · `?q=` 프리필 · 빈 입력 no-op
  - [ ] 메시지 상태 5종 — `pending`(부분 텍스트 + `steps` 단계 리스트, **2초 폴링**) ·
        `done` · `failed`+재시도 · 타임아웃 · 컴포저 잠금
  - [ ] 답변 6블록 — 상태 배지 · 본문 · 근거 블록(`row_count` 포함) · `used_edges` 칩 ·
        드릴다운 표(최대 5행 + 「5 / N」) · 후속 질문 칩
  - [ ] 칩 클릭 → `/ontology/monitoring?edge=<edge_id>` 점프. **그래프 패널 없음**
  - [ ] 드릴다운 「전체 보기」 → `/ontology/data?tier=&table=&filters=`
- **검증**:
  - [ ] `pending` 동안 본문·단계가 자란다(`done`/`failed` 에서 폴링 중단)
  - [ ] `used_edges` 빈 배열이면 「엣지를 밟지 않았습니다」 문구가 나온다
  - [ ] 드릴다운 행이 마스킹 표기로만 보이고 `total` 이 5를 넘으면 「5 / N」 표시
- **완료 증거**: 미작성 — 상태 5종 스크린샷 + 칩 → 모니터링 하이라이트 연쇄 기록
  (게이트 5-③ 의 화면 측) + 드릴다운 「5 / N」 (SPEC-004 AC-12~AC-16·AC-21)

## Pre-deploy Check

- [ ] `globals.css` · 루트 `layout.tsx` · 기존 `/chat` diff 0
- [ ] 화면·툴팁·예문에 PII 원값 없음
- [ ] 「실시간」·「지금」·「live」 카피 0건, 기준일 배지 전 화면 존재
- [ ] `support.js`·`.dc.html` 런타임 의존 0건, 새 CSS 프레임워크 미추가
- [ ] Vercel env(백 API base URL)가 값 없이 커밋되지 않는다

## Rollback

- **라우트 그룹 `app/(ontology)` 디렉토리 삭제로 원복된다.** 포트폴리오 표면을 건드리지
  않았으므로 부분 revert 의 영향 범위가 없다.

## Done Criteria

- [ ] 모든 Phase 가 `DONE`
- [ ] SPEC-004 AC-1~AC-23 커버
- [ ] 디자인 조정 대기 항목이 반영됐거나, 미반영 항목이 목록으로 남아 있다
- [ ] product `log.md` · `30-work/README.md` 갱신(코디네이터)

## Open Issues

- **디자인 조정 대기 20건**(SPEC-004 §7.2)이 미해소 상태다. 정정본이 오기 전에는
  해당 시각 상세를 **워커가 임의로 정하지 않는다** — 막히면 질문으로 올린다.
- SPEC-004 OQ-1(KPI 카드 클릭 목적지) · OQ-2(「그 외 KPI」 표기) · OQ-3(좌표 자산 위치) ·
  OQ-4(최소 폭 문구)는 미결이다. OQ-3 은 구현 재량이고 나머지는 확인 후 진행한다.

## Related

- SPEC: frontmatter `links.specs` · Work: 선행 WORK-002·003 · 후속 WORK-005
