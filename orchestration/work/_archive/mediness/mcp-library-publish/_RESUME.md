
# 재개 노트 — mcp-library-publish (mediness)

**지금**: **전부 머지·배포 검증 완료 (2026-08-31)** — dev: #130·#654 squash 머지, back·mcp 3d72db47 롤아웃·0134 head·leaf+system_admin 단독·tools 61 실측. main: release app #131 + sync docs #658(--admin) merge commit, prod cb175f93 롤아웃·0134·매핑·tools 61 실측
**다음**: 후속 2건 — ① planner: SPEC-060 인벤토리 착지 갱신(실측 61) + WP-123 done 마감·30-work 3자 동기 ② 관리자 계정 실기동 1건으로 감사 결합 확인(수동 권장). 이후 archive-work

세팅: `scripts/new-work.sh mediness mcp-library-publish` · 설정 SSOT `config/projects/mediness.json`
코디handle: `term_915b3ecb-68dd-4d26-98f7-ef3f645318fb`

## 워크트리

- `spec`: `/Users/kknaks/orca/workspaces/mediness-mediness/mcp-library-publish-spec` (branch `mcp-library-publish-spec`, base `origin/mediness` → PR `mediness`)

## 1. 지금

열린 것만 둔다. 닫히면 지우고 §5 이력으로 내린다.

- [~] <진행 중 — 누가 · 무엇을>
- [ ] <다음 할 일>
- [!] <막힌 것 · 사용자 게이트 · 주의>

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-08-28 | MCP 도서관 발행 도구를 연다 — REST thin wrapper, 새 정책 없음 | 사용자 지시 |
| 2026-08-28 | MCP 경유 발행은 시스템 관리자 capability 전용 — 선언층+back 재판정 두 층 모두. 웹 발행(basic)은 유지 | 사용자 지시 |
| 2026-08-28 | 설계 = 전용 라우트 agent-publishes + 신규 leaf baseline.publish.agent(system_admin). upload·update만, 256KiB, 감사 두 원장 결합 | planner 초안 + reviewer PASS |
| 2026-08-28 | OQ-a = 즉시형 예외 확정 (보상통제 4건, Action Runtime 이 baseline 도메인에 닿으면 카드형 승격 조건 명시) | 사용자 선택 |
| 2026-08-28 | W-1 = leaf 표 한 행 병합(8건 선례), W-2 = 지시자 문구 수정 — 확정 반영 태스크에 포함 | 코디 판단 |
| 2026-08-28 | WP-123 사용자 승인 — 「코드부터 발주」 지시로 갈음. backend 구현 발주 | 사용자 지시 |

뒤집힌 결정은 지우지 않는다. ~~취소선~~ 을 긋고 같은 행에 뒤집은 날짜와 사유를 남긴다 —
지우면 왜 그렇게 갔는지가 사라져서 같은 논의를 다시 한다.

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| planner | `term_8cae06bb-9969-43cf-92a3-06d6f68817f9` | `task_ab6e51c218b1` | `ctx_d94a2d653254` | `mcp-library-publish-spec-brief.md` | 완료 (전용 라우트+agent leaf 설계, 5파일 +146/-8) |
| reviewer_spec | `term_571cbe53-bb1f-4ed5-90f5-134c1987b48b` | `task_fa127bb86432` | `ctx_4d41f320371e` | `mcp-library-publish-review-spec-brief.md` | 완료 — PASS (위반 0·경미 2) |
| planner(확정+WP) | `term_42cf4e81-3945-47f6-913d-b217efa8de05` | `task_3490668a88f2` | `ctx_66b87730f19a` | `mcp-library-publish-spec2-brief.md` | 완료 (확정화+WP-123, 7파일) |
| reviewer(재검수) | `term_90add9cf-e03e-4e67-b57e-0649f2767763` | `task_c65a5f90227e` | `ctx_b034053a31f7` | `mcp-library-publish-review-spec2-brief.md` | 완료 — PASS (신규 위반 0) |
| backend(WP-123 구현) | `term_e1680d72-c9dd-499c-aef9-42caa688c614` | `task_36f11bcc71b1` | `ctx_d46fe50ee204` | `mcp-library-publish-be-brief.md` | 완료 (17파일 +296/-29 · back 363p/mcp 525p, 선재 6f 무관) |
| reviewer_code | `term_336efbe1-8bdf-46fa-b0d3-533e82dfe29a` | `task_cb55914dd555` | `ctx_bdc1b9d46a09` | `mcp-library-publish-review-code-brief.md` | 완료 — PASS (위반 0·경미 3) |

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.** 워커 보고는 dispatch preamble 의 값을 따르므로
여기 옛 핸들을 남겨 두면 어느 것이 산 것인지 판단이 안 된다.

## 4. 산출물

- spec PR: <링크>
- code PR: <링크>
- 리포트: `<review-*-report.md>` · `<research-*.md>`
- 커밋: `<sha>` — <한 줄>

## 5. 이력 (최신이 위)

- `<YYYY-MM-DD>` <무슨 일이 있었나 — 한 줄>

이 절은 **재개에 필요한 만큼만** 쓴다. 회고·배운 것은 `SUMMARY.md` 몫이다.
