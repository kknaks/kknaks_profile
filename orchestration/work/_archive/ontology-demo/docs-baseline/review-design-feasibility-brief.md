
# [reviewer] 디자인 핸드오프 실현 가능성 검토 — 페이지별 판정

너는 **ontology-demo `reviewer` 워커**다 (read-only). 역할 문서:
`/Users/kknaks/orca/workspaces/kknaks_profile/ontology-demo/orchestration/roles/kknaks-dev/reviewer/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/docs-baseline` (docs 워커와 공유 —
**리포 파일을 절대 수정·생성하지 마라.** 산출물은 §4 의 리포트 파일 1개뿐이다.)

## 1. 입력

**검토 대상 — 디자인 핸드오프 패키지** (절대경로, read-only):
`/Users/kknaks/orca/workspaces/kknaks_profile/ontology-demo/reference/ontology_demo/design/`
- `README.md` → `01-tokens.md` ~ `08-rules-and-gates.md` 순서로 정독
- `data/nodes.json` · `edges.json` · `tables.json`
- `design/*.dc.html` 프로토타입은 동작·레이아웃 참고용(코드 복사 대상 아님)

**대조 기준 — 계약과 실환경** (워크트리 안):
- `para/projects/summer-star/ontology-demo/20-spec/` — SPEC-001(데이터 계층)·002(MCP 도구)·003(API·채팅·게이트)·005(에이전트·게이트) — draft, 미커밋 상태가 최신이다
- `para/projects/summer-star/ontology-demo/10-decision/` — DEC-001~005
- `app/front/` — 실제 구현 대상 (Next.js 15 App Router · `app/front/app/globals.css` 토큰 SSOT · 인라인 style + var 패턴 · d3-force 가용)
- 원천 실데이터 요약: 노드 25 · 엣지 27(판정: 채택4·자동확정14·선언3·보류3·기각3) · vegas 78,216 · 리뷰 1,962 · nexus 14테이블

## 2. 검토 질문 — 페이지별로 답하라

각 페이지(**모니터링 · 채팅 · 데이터**)에 대해:

1. **데이터 실현성** — 디자인이 화면에 요구하는 모든 값이 SPEC-001 테이블·SPEC-003 응답 shape 로 나오는가? 안 나오는 필드는 무엇이고, spec 을 고칠 일인가 디자인을 고칠 일인가.
2. **동작 실현성** — 상호작용(07-interactions-state)·상태 전이가 SPEC-003 계약(채팅 = 폴딩 + 2초 폴링, 접속 게이트 = env 비번 1개)과 맞는가? 디자인이 스트리밍·즉시성 등 계약에 없는 동작을 전제하는가.
3. **스택 실현성** — Next.js App Router + 인라인 style + d3-force 로 무리 없이 재구현 가능한가? 프로토타입에만 있는 런타임 의존(support.js 류)이 스펙에 스며들 위험은.

**전 페이지 공통 검토 포인트 (코디가 이미 잡은 의심 2건 — 반드시 판정하라):**

- **C-1 테이블 수 불일치**: 디자인 `tables.json` 은 브론즈 3 · 실버 6 · 골드 4 (=13)인데
  SPEC-001 은 브론즈 16(vegas·리뷰·nexus 14) · 실버 6 · 골드 4 · 온톨로지 2. 데이터 화면이
  nexus 14테이블을 어떻게 다루는 설계인지, 화면 단순화라면 spec 과 어떻게 정합시킬지.
- **C-2 토큰 충돌**: 핸드오프 제약은 「`app/front/app/globals.css` 토큰 SSOT, 새 색·폰트 금지」였다.
  디자인 `01-tokens.md` 가 주는 hex 확정값·로고 그라디언트(#7181F8→#A6CDFF)가 기존 토큰으로
  환원 가능한가, 신규 토큰 도입이 불가피한 항목은 무엇인가(목록으로).
- **C-3 PII·게이트**: `08-rules-and-gates.md` 의 제약이 SPEC-001 마스킹 표기(김○○ /
  010-****-1234 / 1990-**-**)·노출 0건 게이트와 어긋나는 곳이 있는가.
- **C-4 used_edges 하이라이트**: `05-screen-chat.md` 의 하이라이트 설계(채팅 안 미니그래프인지
  모니터링 점프인지)가 SPEC-005 답변 스키마·SPEC-003 API 로 구현 가능한가. 페이지 간 상태
  공유가 필요하면 그 요구를 명시하라.

## 3. 판정 형식

페이지별: **FEASIBLE / FEASIBLE-WITH-CHANGES / BLOCKED** + 근거(디자인 파일:절 ↔ spec 파일:절 대조).
FEASIBLE-WITH-CHANGES 는 변경 목록을 「spec 개정 필요」 vs 「디자인 조정 필요」 vs 「구현 재량」으로 갈라라.
전체 요약 표 1개 + C-1~C-4 판정 + SPEC-004(화면 spec) 작성 시 들어가야 할 계약 항목 제안 목록.

## 4. 산출물 — 이 파일 1개만 생성

`/Users/kknaks/orca/workspaces/kknaks_profile/ontology-demo/orchestration/work/docs-baseline/review-design-feasibility-report.md`

(워크트리 밖 코디 영역이다 — 리포트만 여기에 쓰고 다른 파일은 만들지 마라.)

## 5. 하지 말 것

- 워크트리·디자인 패키지의 어떤 파일도 수정 금지. 코드 실행·테스트 불필요.
- `reference/ontology_demo/` 의 원천 데이터(bronze/·silver/ 등 디자인 폴더 밖)는 열지 마라 — PII.
- 판정을 뭉개지 마라 — 애매하면 BLOCKED 가 아니라 「무엇이 확인되면 FEASIBLE 인지」를 적어라.

## 6. 완료 보고 — 2채널 모두 (preamble 의 taskId·dispatchId 사용)

```bash
orca orchestration send --to term_45e793be-0adb-44c7-9d9a-eb35c4f48320 --from <네 워커handle> \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "review 완료: 디자인 실현성" --body "페이지별 판정 / C-1~C-4 / 변경 목록 요약"
orca terminal send --terminal term_45e793be-0adb-44c7-9d9a-eb35c4f48320 \
  --text "[worker_done] review 완료 — 디자인 실현성 판정. 상세는 리포트·인박스." --enter
```
