
# [planner] WP2 — incident 재정비 WP 작성 (task 축 WP-125 의 후속)

너는 **mediness `planner` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/roles/mediness/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/task-redesign-spec`
base 브랜치: `origin/mediness` → 최종 PR 대상 `mediness` (PR 은 코디네이터가 올린다)

이 워크트리에는 직전 라운드의 스펙 개정 커밋(spec PR #661)이 이미 있다 — **그 위에서** 작업한다. 스펙 본문은 확정 계약이니 고치지 마라(아래 §7).

## 1. SSOT — 먼저 읽을 것

- `products/mediness/20-spec/spec-152-incident-response-workflow.md` — **incident 계약 정본(재정비본).** WP 는 이것만 구현한다
- `products/mediness/30-work/work-125-task-ledger-unification.md` — 선행 WP. §Scope «제외» 목록·§Open Issues OI-3(라운드 판정 수렴)·OI-4(`is_required`/`scope_slug` drop)가 **이번 WP 로 이월된 자리**다
- `products/mediness/40-architecture/domains/runtime_task.md` — 상태·이벤트 정본 (이번 WP 가 올라서는 축)
- `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/work/task-redesign/research-incident.md` §B — 조사 시점 코드 좌표(냄새 S·충돌 C·죽은 코드 목록). **계약이 아니라 지도** — 어긋나면 코드 실물이 맞다
- `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/work/task-redesign/_RESUME.md` §2 — 사용자 결정 표

기대는 개념 — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

spec-152 재정비로 incident 의 정본 계약(Slack fail-loud·라운드 판정 1벌(활성 라운드)·run 감사·종결 시 추적 태스크 정리·스테이지 8/엣지 11·done 조건 경로 A/B)이 확정됐고, task 축은 WP-125 로 코드 발주가 나가 있다. 이번 산출물은 **incident 축 코드 재정비의 빌드 계획(WP 문서 1건)** 이다 — WP-125 가 세운 상태 축 위에 선다.

## 3. 계약 (이대로 반영)

WP 에 포함할 축 (spec-152 + WP-125 이월분):

1. **라운드 판정 1벌 수렴** — 활성 라운드(최대 `round_no`) 기준. 3벌 구현(round_piece / tasks_surface.round_complete / factory.has_open_in_run_chain)을 정본 1벌로. WP-125 P8 이 옮겨 둔 seam 훅 위에서
2. **run 감사** — `workflow_closed` 를 run 축으로 도입(`set_run_status` 단일 쓰기 경로) + 종결 시 추적 태스크(round 0) 정리
3. **Slack fail-loud** — 토큰 미설정 시 declare 승인 실행 실패(조용한 no-op 폐기) + `/incidents/slack/complete` 인증 구멍 폐쇄(`/slack/interact` 만 유지)
4. **RegenGate 이벤트 이름 가드** (spec-152 재정비본에 계약이 있으면 그 절 기준, 없으면 OQ 로)
5. **죽은 코드 정리** — BFF 3건(review/revise·publish·finalize-request)·참조 0 상수·고아 pyc (research-incident §B-7 목록)
6. **`is_required`·`scope_slug` drop 마이그레이션** (WP-125 OI-4 이월)
7. **is_lead 게이트·추적 태스크 cc(버전 참여자)** — cc 해소 규칙이 OQ-13 이면 WP 에서도 OQ 로 유지(발명 금지)
8. 범위 밖 유지: 알림/DM·에스컬레이션·슬랙 인바운드 어댑터·GitHub/Jira mirror

## 4. 먼저 읽을 핵심 파일

- `spec-152` 재정비본 전체 — 특히 상태 전이·done 경로 A/B·Slack 절
- `work-125` §의존 관계 — 이번 WP 가 소비하는 인터페이스(5값 전이표·`task_unblocked`·seam 훅)
- `research-incident.md` §B-5(냄새)·§B-7(죽은 코드)·§B-11(코드 관점 주의)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `products/mediness/`
- `context/`

## 6. 구현 단계

1. WP 번호는 `30-work/` 의 **다음 빈 번호**를 실측으로 확인해 쓴다 (doc_no 도 동일 규율 — 기존 최대 +1)
2. WP 문서 1건 작성 — WP-125 와 같은 골격(Scope/Code Surface/Domain·invariant/의존/Execution phase/Pre-deploy/Rollback/Open Issues). `depends_on: [MEDINESS-WP-125]`
3. 30-work.md 3표(Board/WP List/Spec Coverage)·log.md 동기
4. `python3 scripts/lint-pipeline.py --strict` — mediness 범위 ERROR 0
5. 완료 보고 (§9)

## 7. 범위 제약 — 하지 말 것

- **스펙 본문(20-spec/)·도메인 문서(40-architecture/)를 고치지 마라** — 확정 계약이다. WP 작성 중 계약 모순을 발견하면 §9 질문 채널로 보고만
- 코드 레포(mediness-app) 수정 금지 — read-only 참조만
- WP-125 문서를 고치지 마라 (OI 이월은 새 WP 쪽에서 인용으로)
- 결정 SoT 에 없는 설계 발명 금지 — 애매하면 OQ

## 8. 검증

```
python3 scripts/lint-pipeline.py --strict
```

- mediness 범위 ERROR 0. 타 제품 기존 WARN/ERROR 는 "무관"으로 분리 보고.
- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다. preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_1d6e5d93-2be9-4125-b7eb-42b1de52b5ed --from term_b1761f6d-c81c-4fc1-9d78-f6c23d006422 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch preamble> \
  --dispatch-id <이 태스크의 dispatchId — dispatch preamble> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입
orca terminal send --terminal term_1d6e5d93-2be9-4125-b7eb-42b1de52b5ed \
  --text "[worker_done] planner(WP2) 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_1d6e5d93-2be9-4125-b7eb-42b1de52b5ed --text "[질문] planner(WP2): <질문>" --enter`
