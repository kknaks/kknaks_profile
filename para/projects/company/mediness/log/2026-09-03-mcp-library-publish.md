
# 작업 요약 — mcp-library-publish (mediness)

기간: `2026-08-28` ~ `2026-08-31` (아카이브 정리 `2026-09-03`)
결과: **머지·배포 완료** — dev(#130·#654)·main(#131·#658) 머지, prod `cb175f93` 롤아웃, 마이그레이션 0134 head, tools 61 실측 검증

## 1. 무엇을 했나

MCP 경유로 도서관 발행을 열어 달라는 요구. 웹 발행(basic capability)은 있었지만 에이전트가
MCP 로 발행할 통로가 없었다. 새 정책 없이 REST thin wrapper 로 열되, 시스템 관리자 전용으로
제한하는 설계를 spec 개정(SPEC-013·060·003 + WP-123 신설) → backend 구현(17파일 +296/-29) →
spec·code 리뷰 각 PASS 로 완주했다. dev·main 머지와 prod 롤아웃·실측(tools 61)까지 08-31 에 끝났다.

## 2. 적용한 기술·개념

- **전용 라우트 + 신규 leaf capability (`baseline.publish.agent`, system_admin 전용)** — MCP 발행 창구 → [[defense-in-depth]]
  - 왜 이걸 골랐나: 기존 웹 발행 라우트에 분기를 넣는 대신 `agent-publishes` 전용 라우트를 신설.
    웹 발행(basic)과 에이전트 발행(system_admin)의 권한 축이 달라서 한 라우트에 섞으면 재판정이 흐려짐
  - 무엇이 어려웠나: 권한을 **선언층 + back 재판정 두 층 모두**에 걸어야 했다 — 한 층만 걸면
    tools/list 필터를 우회한 직접 호출이 뚫린다. upload·update 만 허용, 256KiB 제한, 감사 두 원장 결합
  - 근거: `mcp-library-publish-spec-brief.md` · `review-spec-report.md` (PASS 위반 0·경미 2) · dev #130
- **OQ 즉시형 예외 처리** — Action Runtime 미연동 상태의 열린 질문을 카드로 미루지 않고 닫음 → [[compensating-control]]
  - 왜 이걸 골랐나: 보상통제 4건을 명시하면 즉시형으로 닫을 수 있었고, Action Runtime 이
    baseline 도메인에 닿는 순간 카드형으로 승격한다는 조건을 spec 에 박아 재논의 여지를 없앰
  - 근거: _RESUME §2 (OQ-a, 2026-08-28 사용자 선택)
- **leaf 표 한 행 병합** — 신규 leaf 를 표에 행 단위로 얹지 않고 기존 행에 병합 (8건 선례 준수)
  - 근거: `mcp-library-publish-spec2-brief.md` (W-1) · `review-spec-report.md`

## 3. 막혔던 것 / 사고

- **squash 머지 잔상으로 아카이브 안전검사에 걸림 (09-03)** — 로컬 `mcp-library-publish` 브랜치가
  origin/dev 보다 1커밋 앞서고 내용도 다르게 보였다 → blob 해시 비교로 브랜치 트리가 squash 커밋
  `3d72db47`(#130) 트리와 전 파일 동일함을 확인(런북 STEP 7 절차) → 워크트리·브랜치 삭제로 원인 제거.
  머지 직후 브랜치를 바로 지웠으면 없었을 일 — **머지 확인 즉시 워크트리를 정리한다**
- 작업 기록(work/)이 SUMMARY 없이 main 에 먼저 커밋됐다(#34) → archive-work 절차(SUMMARY 게이트)를
  뒤늦게 밟아 정리. **기록 커밋 전에 archive-work dry-run 부터**가 맞는 순서였다

## 4. 결정

| 날짜 | 결정 | 왜 |
|---|---|---|
| 2026-08-28 | MCP 도서관 발행을 연다 — REST thin wrapper, 새 정책 없음 | 사용자 지시 |
| 2026-08-28 | MCP 경유 발행 = system_admin capability 전용 (선언층+back 두 층), 웹 발행(basic) 유지 | 사용자 지시 |
| 2026-08-28 | 설계 = 전용 라우트 + 신규 leaf `baseline.publish.agent`, upload·update 만, 256KiB, 감사 두 원장 결합 | planner 초안 + reviewer PASS |
| 2026-08-28 | OQ-a = 즉시형 예외 확정 (보상통제 4건 + 카드형 승격 조건 명시) | 사용자 선택 |
| 2026-08-28 | WP-123 승인 — 「코드부터 발주」 지시로 갈음, backend 구현 발주 | 사용자 지시 |
| 2026-09-03 | 아카이브 — 후속 2건은 별건으로 넘기고 slug 를 닫는다 | 사용자 지시 |

## 5. 날짜별 로그

- `2026-08-28` spec 개정 발주 → 리뷰 PASS → 확정화+WP-123 → 재검수 PASS → backend 구현 발주
- `2026-08-31` code 리뷰 PASS → dev #130·#654 머지, back·mcp `3d72db47` 롤아웃 → main #131·#658, prod `cb175f93` 롤아웃 — 0134 head·leaf 매핑·tools 61 실측 검증
- `2026-09-03` squash 잔상 워크트리 2개(spec·app) 정리, 아카이브

## 6. 산출물

- spec PR: dev #654 · main #658 (docs sync)
- code PR: dev #130 · main #131 (release)
- 커밋: dev `3d72db47` — feat(library): MCP 도서관 발행 창구 (WP-123)
- 리포트: `review-spec-report.md` (PASS 위반 0·경미 2) · `review-code-report.md` (PASS 위반 0·경미 3)

## 7. 잔여

- **후속 ①** planner 발주: SPEC-060 인벤토리 착지 갱신(실측 tools 61 반영) + WP-123 done 마감·30-work 3자 동기 — 별건 slug 로 진행
- **후속 ②** 관리자 계정 실기동 1건으로 감사 두 원장 결합 실확인 — 수동 권장
