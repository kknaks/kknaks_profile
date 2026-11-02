
# [reviewer_spec] WP-126(incident 재정비) 검수

너는 **mediness `reviewer_spec` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/roles/mediness/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/task-redesign-spec` — **read-only 검수.** 리포 파일 수정·생성 금지.

검수 대상 = planner 산출물(미커밋): 신규 `products/mediness/30-work/work-126-incident-workflow-realign.md` + `30-work.md`·`log.md` 동기 + 코디가 정정한 3곳(WP-125 §Scope/OI-4 · spec-152 §예방 Task 종결 게이트의 is_required 문장 — migration 0066 실측 근거).

## 1. SSOT — 판정 기준

- `products/mediness/20-spec/spec-152-incident-response-workflow.md` — WP-126 이 구현해야 하는 계약 정본
- `products/mediness/30-work/work-125-task-ledger-unification.md` — 선행 WP (depends_on 대상·OI 이월 원점)
- `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/work/task-redesign/task-redesign-wp2-brief.md` — planner 가 받은 발주 브리프(§3 포함 축 8건·§7 제약)
- `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/work/task-redesign/_RESUME.md` §2 — 결정 SoT
- (대조용) `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/work/task-redesign/research-incident.md` §B — 코드 좌표 스냅샷

## 2~4. 검수 체크리스트

1. 브리프 §3 포함 축 8건이 WP-126 phase 에 전부 실렸는지 (라운드 판정 1벌 / run 감사+추적 정리 / Slack fail-loud / RegenGate 가드 / 죽은 코드 / OI-4 처분 / is_lead·cc / 범위 밖 유지)
2. spec-152 계약과 WP-126 의 정합 — WP 가 계약에 없는 설계를 발명하지 않았는지, 계약이 있는데 WP 에서 빠진 축이 없는지
3. `depends_on: [MEDINESS-WP-125]`·WP 번호/doc_no(126/DOC-246) 정합·상대링크 실재
4. 30-work.md 3표·log.md 동기 완전성
5. planner 의 OI 처분 판단 적정성 — 특히 OI-1(is_required 대상 없음 실측)·OI-2(/incidents/slack/complete 소유 중복 → P0 조건부)·OI-3(RegenGate = SPEC-150 소유 공용 조각이라 버그 수정 범위만)
6. 코디 정정 3곳이 실측(alembic 0066)과 맞는지 재확인
7. `python3 scripts/lint-pipeline.py --strict` — mediness 범위 ERROR 0

## 5. 산출물

- 리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/work/task-redesign/review-wp126-report.md` — 판정(PASS/WARN/FAIL) + 항목별 근거(파일:줄). 문체 지적으로 FAIL 금지.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 preamble 이 맞다.

- **커밋·push·PR 하지 마라.**
- 끝나면 아래 두 명령을 **모두** 실행한다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_1d6e5d93-2be9-4125-b7eb-42b1de52b5ed --from term_8b0f1b27-4a48-476e-8390-709dbfaf7940 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch preamble> \
  --dispatch-id <이 태스크의 dispatchId — dispatch preamble> \
  --subject "reviewer_spec 완료: <한 줄>" \
  --body "판정 / 항목별 결과 / 위반 목록(파일:줄) / 미결"

# (2) 직접 주입
orca terminal send --terminal term_1d6e5d93-2be9-4125-b7eb-42b1de52b5ed \
  --text "[worker_done] reviewer_spec(WP-126) 완료 — <판정 한 줄>. 상세는 인박스." --enter
```

- 막히면 30분 이상 헤매지 말고: `orca terminal send --terminal term_1d6e5d93-2be9-4125-b7eb-42b1de52b5ed --text "[질문] reviewer(WP-126): <질문>" --enter`
