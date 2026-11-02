
# [docs] SPEC-004 작성 + SPEC-001/002/003/005 개정 — 디자인 검토 반영

너는 **ontology-demo `docs` 워커**다. 같은 워크트리, 같은 규칙.
작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/docs-baseline`

## 1. SSOT — 먼저 읽을 것

- **리뷰 리포트** (read-only, 절대경로): `/Users/kknaks/orca/workspaces/kknaks_profile/ontology-demo/orchestration/work/docs-baseline/review-design-feasibility-report.md`
  — 디자인 실현성 판정. **§5(SPEC-004 계약 항목 28개)와 §5.5(타 spec 개정 요구)가 이번 작업의 목록이다.**
- **디자인 패키지** (read-only, 절대경로): `/Users/kknaks/orca/workspaces/kknaks_profile/ontology-demo/reference/ontology_demo/design/`
  — `01`~`08` 문서 + `data/*.json`. **이 폴더 밖(reference/ontology_demo/ 의 bronze/ 등)은 열지 마라 (PII).**
- 기존 spec 4건·decision·기록 01~09 — 직전 태스크와 동일.

## 2. 사용자 확정 (2026-09-02 문답 — 이대로 박는다)

1. **채팅 우측 근거 그래프(520px 패널의 축약 그래프)는 뺀다.** `used_edges` 는 답변 안
   **칩으로만** 표시하고, 칩 클릭 → 모니터링 `?edge=` 점프로 하이라이트한다.
   게이트 5-③ 의 검증 대상 화면 = **모니터링 그래프 단일**(SPEC-005 OQ-4 닫힘).
   리포트 C-4 의 A/B 안은 둘 다 폐기 — 패널 제거가 확정이다.
2. **Pretendard 도입** — next/font 경로(CDN `@import` 금지), 데모 라우트 그룹에만 적용.
3. **답변 패턴 C(계수 기반 정량 추정)는 문구 제거** — 관계 방향·근거(r·n)까지만 제시.
   SPEC-005 에 「에이전트는 엣지 계수 기반 정량 추정을 하지 않는다(도구가 주지 않는 수치
   생성 금지)」를 명문화. 계수 도구는 범위 밖(파이프라인 단계 검토).
4. **월 단위 집계 = 골드 월 View** — 빌드가 생성, `query_kpi` 는 조회만(S-002 유지).
   SPEC-001(골드 테이블 목록)·SPEC-002(`grain=monthly` 의 출처) 동기 개정.
5. (기확정 재확인) 직전 태스크의 「제안」 21건 중 위 4건 외 전건 **승인됨** — 「제안 — 리뷰」
   딱지를 떼고 확정 서술로 바꾼다. SPEC-001 OQ-3(retention 행수)만 「빌드 실측 등재」로 유지.

## 3. 할 일

### 3-A. SPEC-004 신규 — `spec-004-three-screens.md` (status: **draft**)

리포트 §5.1~5.4 의 28개 항목을 계약으로. 주의:

- §5 항목 19(우측 그래프 계약)는 §2-1 확정으로 대체 — 패널 제거·칩+점프 일원화를 계약으로.
- §5 항목 4(폰트)는 §2-2 확정 반영.
- 항목 20(예문 정정): 패턴 A·B 는 **실재 확정 엣지로 예문을 교체하라는 요구를 「디자인
  조정 대기」로 명시**(spec 이 예문을 창작하지 말 것 — 정본 엣지 목록만 제약으로 걸어라),
  패턴 C 는 §2-3 확정 반영.
- 토큰 레이어 계약(C-2 권고 1~5): `globals.css` 불변 · `--ont-*` 스코프 토큰 ·
  `color-scheme: light` 재선언 · 신규 토큰 목록은 디자인 `01-tokens.md` 를 SoT 로 링크
  (hex 전사본 복사 금지 — 두 곳이 되면 어긋난다).
- 라우트: `app/(ontology)` 그룹 + `/ontology/{monitoring,chat,data}` 접두, 기본 진입
  monitoring, 기존 `/chat`(포트폴리오) 불변.
- frontmatter `links.decisions`: DEC-004(주)·DEC-002·DEC-005. 20-spec/README 의 결번
  표기를 해제하고 목록·묶음 표 갱신.

### 3-B. 기존 4건 개정 (리포트 §5.5 표 전건 + §2 확정)

- **SPEC-001**: 골드에 월 View 추가 · `v_bronze_reviews` 마스킹 목록에 `authorName` 추가
  (DEC-002 의 「리뷰 작성자명」이 이미 대상이다 — 뷰 목록 누락 정정) · `node_id` 25종
  확정 목록(snake_case, SPEC-002/003 표기 기준) 등재.
- **SPEC-002**: `grain=monthly` = 월 View 조회로 확정 · lag 표기 형식 통일(`"0d"/"1d"/"7d"/"60d"`
  — edges 원천 형식으로 전 spec 통일).
- **SPEC-003**: `/api/kpi/cards` 에 `dod`·`dod_pct`·`unit`·`grain`·`spark[7]`·기간 파라미터 ·
  `/api/graph` 에 `kind`·`note`·노드 `source`·`edge_id` · `/api/forecast` 에 `title`·`message`·
  `edge.evidence` · `lineage` 에 `rule_id`·`gate`·`downstream`·`is_provisional` ·
  `/api/layers/{layer}/tables` 에 `flows_to` · lag 표기 통일 · 예보 예시 수치를 기록 07
  정본값으로 정정.
- **SPEC-005**: 답변 객체에 `drilldown{...}`·`followups[]`·`citations[].row_count` 추가 ·
  정량 추정 금지 명문화(§2-3) · G5-③ 검증 대상 = 모니터링 그래프 명시(OQ-4 닫음) ·
  `used_edges[]` 에 `edge_id` 추가(SPEC-003 과 동일 규약).
- 4건 개정 후 **status: draft → ready, version 올림**(제안 전건 승인 — §2-5).
  SPEC-004 만 draft 유지(사용자 리뷰 대기).

### 3-C. 동기 갱신

20-spec/README(목록·OQ 표 — 닫힌 것 정리, SPEC-004 행) · 10-decision/README 미결 표 ·
각 DEC Resulting Spec · 제품 README · log.md.

## 4. 하지 말 것

- 디자인 조정 몫(행수 오기·enum 오기·예문 엣지·카피 모순·진행 상태 화면·게이트 화면)은
  **spec 이 대신 그리지 마라** — SPEC-004 에 「디자인 조정 대기」 항목 표로만 남긴다.
- 리포트·디자인 파일·allowed_paths 밖 수정 금지. 커밋·push 금지. PII 원값 금지.

## 5. 검증·완료 보고 — 직전 태스크와 동일 (2채널, preamble 값, 코디 `term_45e793be-0adb-44c7-9d9a-eb35c4f48320`)

보고 body 에: 변경 파일 / SPEC-004 계약 항목 수 / 개정 4건 요약 / 닫힌 OQ·남은 OQ / 디자인 조정 대기 목록.
