# [reviewer_doc] 예약 현황 문서 재검수 r2 — SPEC-005 0.2.0 · DEC-006 · WORK-007

너는 **cc-prototype `reviewer_doc` 워커**다. **앞 판의 맥락이 없다.** 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc` (코디 워크트리 — **read-only**. 리포트 1개만 만든다)

## 1. SSOT — 대조 기준

- **결정 정본** = `orchestration/work/overall-board/_RESUME.md` §2 의 **2026-10-26 줄 전부**(예약 구간 · 「코드까지 다 작성」 범위 줄 포함) + §1 메모. 취소선 = 뒤집힘
- **흐름 정본** = `reference/2026-10-26-cc-reservation/workflow-v3.md` · KOS 근거 = 그 머리말의 리포트 15개(`orchestration/work/overall-board/reservation-*-report.md`)
- **시안(정본)** = `reference/2026-10-23-cc-overall-board/design/Ceramique 전체현황판.dc.html` 「예약 현황」 `M:93-715` · 분석 `orchestration/work/overall-board/design-analysis-report.md` §3 · §6 · §7.2 · §11
- 같은 앱 계약(회귀 · 겹침 확인): `para/projects/summer-star/cc-prototype/20-spec/spec-003-procedure-board.md`(0.5.1) · `spec-004-procedure-app.md` · `10-decision/decision-005-procedure-board.md`
- 코드 현실(읽기만): `/Users/kknaks/orca/workspaces/cc-prototype/overall-board/procedure/`

## 2. 검수 대상 (planner 보고 `orchestration/work/overall-board/reservation-spec-report.md` 참고)

- `para/projects/summer-star/cc-prototype/00-baseline/baseline-009-reservation-board.md`
- `para/projects/summer-star/cc-prototype/10-decision/decision-006-reservation-board.md`(D-01 ~ D-43)
- `para/projects/summer-star/cc-prototype/20-spec/spec-005-reservation-board.md`(0.1.0 · 898줄 · API 15 · E2E 32 · OQ 56)
- `para/projects/summer-star/cc-prototype/30-work/work-007-reservation-board.md`(WP 10)
- README 4 · log.md · DEC-005 / SPEC-003 / SPEC-004 frontmatter links · `reference/2026-10-12-cc-prototype/workflow-v2.md` 4곳 — `git -C /Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc diff` 로 바뀐 줄

## 3. 할 일 — 각 지적에 `파일:줄` + 근거 + 판정(FAIL · WARN · PASS)

1. **결정 반영 전수**: `_RESUME` 10-26 줄마다 DEC-006 · SPEC-005 어디에 어떻게. 빠짐 · 다르게 = FAIL. 특히 「KOS 그대로」 · 「같은 데이터(사본 + KOS 기준)」 · 「KOS 에 없으면 안 쓴다 / 있으면 칸」 · 2계층 상태 · 후납 = 수납 필요(금액 없음) · [귀가 완료] 막기 · 상담사 지금 상태 계산 · 처방전/수납 딥링크 · 코디 역할 제한 없음 · 이번 판 밖 목록
2. **KOS 근거 대조**: SPEC §4 · §8 의 호출 · 본문 · 공개/내부 구분이 리포트와 맞나(리포트 절). 리포트에 없는 KOS 동작을 지어냈나. **데모에서 확인된 것 / 미확인**이 구분돼 있나. WP-KOS 게이트가 미확인을 다 덮나
3. **planner 기본값 41개**(SPEC §10): 각각 근거(리포트 · 시안 · 결정) 안에서 고른 것인가, 새 정책 발명인가. 특히 OQ-714(이동 = 내부 `update-reservation` — 브리프 예시는 공개였음 · 지정 의사 보존 근거) · OQ-718(묶음 실패 되돌리지 않음) · OQ-719(접수 켜짐 = 신분 확인 완료 — 시안 「신분 필드 모두 입력」과 비교) · OQ-703 · OQ-704 · OQ-705. 사용자 결정이 필요한 것은 「사용자 결정 필요」로 따로
4. **시안 대조**: 「시안대로」 · 「시안과 다른 곳」 표가 실제 시안(`M:줄`)과 맞나. 조용히 빠진 시안 요소
5. **계약 완결성**: BE ↔ FE 가 SPEC 만 보고 따로 짤 수 있나 — API 15(경로 · 요청 · 응답 · 오류 코드 · `can.*`) · 상태 계산 · 접수 묶음 단계 · 실패 · 반영 지연 · 사본 표 · 시술 현황(SPEC-003)과의 겹침 · 회귀(헤더 · 계정 · 동기화 루프)
6. **WORK-007**: WP 마다 대상 파일 · 완료 조건 · 검증 명령 · 병렬 고정점 · 게이트. E2E 32 가 「넣는다」를 다 덮나 · 사용자가 실물에서 볼 자리인가
7. **workflow-v2 4곳**이 v2 규칙(취소선 + 날짜)대로 · 지금 결정과 맞나
8. 링크 · 인덱스 · 버전 · **public**(실명 · 키 · KOS id · 실제 지점 처방 정보 0 — grep)

## 4. allowed_paths

- 산출물 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/reservation-review-doc-r2.md`. 그 밖 수정 금지

## 5. 범위 제약

- 어떤 파일도 고치지 마라. 결정을 대신 내리지 마라 — 「사용자 결정 필요」로 따로 모은다
- 시술 현황 본체 · 앱은 회귀 확인만

## 6. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 같은 워크트리의 다른 코디 세션으로 보내지 마라.

```bash
orca orchestration send \
  --to term_fa2737b7-e69a-40e1-9fac-019199b9dad3 --from <네 handle> \
  --type worker_done \
  --task-id <preamble 의 taskId> --dispatch-id <preamble 의 dispatchId> \
  --subject "reviewer_doc 완료: 예약 현황 r1 <판정 한 줄>" \
  --body "리포트 경로 / FAIL n · WARN n / FAIL 목록 한 줄씩 / 사용자 결정 필요 목록"

orca terminal send --terminal term_fa2737b7-e69a-40e1-9fac-019199b9dad3 \
  --text "[worker_done] reviewer_doc 예약 현황 r1 — <판정>. 상세는 reservation-review-doc-r2.md" --enter
```

## r2 추가 — 이번 판은 재검수

- r1 리포트 `orchestration/work/overall-board/reservation-review-doc-r1.md` 의 FAIL 3 · WARN 9 가 SPEC-005 0.2.0 부록 C 처분대로 실제로 고쳐졌나(줄마다)
- 사용자 결정 U1~U7(`_RESUME` §2 「SPEC-005 r1 사용자 결정」 줄) · WP-KOS 결과(`reservation-kos-probe-report.md`) 반영이 맞나
- 새로 생긴 모순만. r1 에서 PASS 였던 곳을 다시 뒤지지 마라
- **구현(backend · frontend)이 이 SPEC 으로 이미 병렬로 시작했다** — FAIL 은 구현에 바로 반영해야 할 것만, 짧고 정확하게
