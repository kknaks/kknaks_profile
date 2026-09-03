# [reviewer_spec] 재검수 — 스펙 확정화 + WP-123 신설

너는 **mediness `reviewer_spec` 워커**다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-interview/orchestration/roles/mediness/reviewer/` 5종.

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/mcp-library-publish-spec`
base: `origin/mediness` → PR `mediness`

**리뷰 모드: planner 리뷰, 재검수.** read-only. 산출물 = 기존 리포트에 「## 재검수 (2차, 2026-08-28)」 섹션 추가:
`/Users/kknaks/orca/workspaces/kknaks_profile/sc-interview/orchestration/work/mcp-library-publish/review-spec-report.md`

## 검수 범위

1차 검수(PASS) 이후 증분 — `git diff origin/mediness...HEAD` 중 이번 변경: 수정 6 (`20-spec.md`·`spec-003`·`spec-013`·`spec-060`·`30-work.md`·`log.md`) + 신규 1 (`30-work/work-123-mcp-baseline-publish.md`).

## 검수 항목

1. **1차 경미 2건 해소 확인** — W-1(SPEC-003 한 행 병합, 선례 동형), W-2(지시자 문구).
2. **OQ-a 닫힘이 사용자 결정 그대로인가** — 즉시형 예외 확정 + 보상 통제 4건 유지 + 「Action Runtime 배선이 baseline 도메인에 닿으면 카드형 승격 재검토」 조건 명문화. 결정에 없는 내용이 추가되지 않았는지.
3. **⏳ 라벨 정리** — 확정 표기 전환이 일관적인지, SPEC-060 인벤토리 예고 주석은 유지됐는지.
4. **WP-123** — WP 규약: 1파일=1WP·SPEC 복제 없이 link·doc_no 중복 없음(243)·frontmatter·covers 3건 타당성. Code Surface 12행이 실코드와 정합한지 spot-check (전수 아님 — 파일:심볼 존재 확인 수준). 비목표가 계약과 모순 없는지.
5. **30-work.md 3자 일치** — WP List·Status Board·Spec Coverage 에 WP-123 이 셋 다 반영, SPEC-013 derive(done→in_dev) 타당성. lint 5→6 게이트 통과.
6. 선재 드리프트(인벤토리 57 vs 실측 60) 기장이 WP Open Issues 에 있는지 — 이번 판정에는 넣지 않는다 (기존 부채).

## 검증 명령

```
python3 scripts/lint-pipeline.py --strict → products/mediness/ 범위 ERROR 0
```

## 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 값과 다르면 preamble 이 맞다.

- 커밋·push·PR 금지. subject 에 판정을 박는다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_915b3ecb-68dd-4d26-98f7-ef3f645318fb --from <네 워커handle> \
  --type worker_done \
  --task-id <taskId — dispatch context> --dispatch-id <dispatchId — dispatch context> \
  --subject "reviewer_spec 완료: <판정 — 한 줄>" \
  --body "판정 / 위반(파일:줄+근거) / 확인한 것 / 리포트 경로"

# (2) 직접 주입
orca terminal send --terminal term_915b3ecb-68dd-4d26-98f7-ef3f645318fb \
  --text "[worker_done] reviewer_spec 완료 — <판정> <한 줄>. 상세는 인박스." --enter
```
