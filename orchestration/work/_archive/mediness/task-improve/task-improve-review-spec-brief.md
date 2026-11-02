
# [reviewer_spec] 업무 요청 축 + 상세 5부 통일 스펙 + WP-129/130 검수

너는 **mediness `reviewer_spec` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/roles/mediness/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/task-improve-spec`
base 브랜치: `origin/mediness`

planner 산출물(미커밋 13파일 + untracked `work-129-task-request-axis.md`·`work-130-task-detail-unification.md`)이 이 워크트리에 있다. **read-only 검수** — 리포 파일을 고치지 마라.

## 1. SSOT — 판정 기준

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/work/task-improve/_RESUME.md` **§2 결정 표** — 2026-09-01 사용자 확정 결정 전체. **스펙이 이 표와 어긋나면 FAIL**
- `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/work/task-improve/task-improve-spec-brief.md` — planner 발주 브리프(계약 A~H·제약)
- `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/work/task-improve/task-improve-wp-split-brief.md` — WP 분할 계약(129/130 경계)
- 층위 SoT: `products/mediness/40-architecture/domains/runtime_task.md`(상태·이벤트 — 변경됐으면 FAIL), `spec-119`(DM 인프라 — 신설 있으면 FAIL)

## 2. 배경

planner 가 결정 15건을 스펙 9건+도메인+ERD 에 반영하고 WP 를 역할별 2건으로 분할했다: WP-129(요청 축+샤라웃 지시 입구 차단, 인덱스 1, BLOCKED 0) / WP-130(상세 5부+완료 근거, 컬럼 2+테이블 1, P7 시안 대기). **비어 있어야 정상인 자리**: /ax/tasks 화면 구조(§4.19.6-R 시안 대기 슬롯)·WP-130 P7. 이 자리가 확정으로 박혀 있으면 그게 FAIL 이다.

## 3. 검수 체크리스트

**결정 SoT 대조 (_RESUME §2 행별 — 어긋나면 FAIL):**

1. 요청 판정 = 파생(비워크플로 ∧ created_by≠assignee), 새 컬럼·type·상태·TaskEvent 0
2. **요청자 자동 cc 없음** — cc 자동 추가 서술이 남아 있으면 FAIL (08-31 구 결정이 뒤집힌 자리)
3. 게이트 0(수락·검수 어떤 형태로도) · 거부=재배정 요청
4. DM graceful(spec-119 재사용·실패해도 생성) — fail-loud 와 혼동 없나
5. 본문 5부: background·goal 컬럼 / 원장 렌더 폐지(스냅샷) / description fallback / 댓글·로그 = task_events 현행(신설 0)
6. task_references: role×kind·soft delete·출처는 행 저장 금지(자동 렌더)·25MB·denylist·권한 3원칙·저장 경로(env root·path-guard·상대경로)
7. 완료 모달: 3조합 중 1 필수·서버 422·시스템 액터 예외
8. 채팅: 배경·목표·체크리스트 필수 채움·첨부 스테이징(drafts/→승인 시 귀속)·발화 패턴(발화 명시 시에만 담당자)
9. 샤라웃: 지시 유형 **입구만** 주석 비활성(슬랙·채팅)·내부 보존·재활성 가능 명시·결정 요청/공유/결재 유지
10. migration 총계 = 컬럼 2+인덱스 1+테이블 1, 분배: 129=인덱스 / 130=컬럼+테이블. k8s hostPath 사전조건 130 에 명시

**교차 정합:**

11. **구 서술 grep 스윕** — `원장.*렌더|마크다운.*합침|본인 고정|자동.*cc` 활성 계약 잔존 시 FAIL (취소선·폐기 표기·이력 인용은 허용). 직전 두 라운드 FAIL 패턴이다 — 전 20-spec/·40-architecture/ 스윕
12. WP 분할 경계 — «background/goal·task_references 필요 여부» 기준 준수. 두 WP 간 phase 중복·누락 0. 스펙의 «구현 WP =» 재배선 정확성
13. planner 판단(«뒤집기 가능» 표기) 6건 — 표기 실재 + 기존 계약과 모순 없음
14. 30-work.md 3표·20-spec.md·log.md 동기 정합
15. 시안 대기 슬롯(§4.19.6-R)·WP-130 P7 — 화면 구조 선확정 서술이 없는지

## 4. 검수 절차

1. SSOT 정독 → `git diff` + untracked 로 변경 전모 산정 (allowed_paths 이탈 확인 포함)
2. 체크리스트 1~15 판정 (근거 = 파일:줄)
3. `python3 scripts/lint-pipeline.py --strict` — mediness 범위 ERROR 0 (SPEC-030 coverage WARN 1건은 선재분·무관)
4. 리포트 작성: `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/work/task-improve/review-spec-report.md` (**덮어쓴다** — 기존 파일은 롤백된 구 라운드 것) — 판정(PASS/WARN/FAIL)+항목별 근거+위반 목록
5. 완료 보고 (§6)

## 5. 범위 제약

- read-only — 리포트 1개 외 수정·생성 금지. 코드 레포(`/Users/kknaks/orca/workspaces/mediness-app/task-improve`) 읽기는 허용
- 문체 지적으로 FAIL 금지 — FAIL 은 결정 위반·구 서술 활성 잔존·계약 모순·비어야 할 자리 선확정만
- «시안 대기»·«P7 BLOCKED» 를 미완성으로 FAIL 하지 마라 — 발주 계약이다

## 6. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 값과 아래가 다르면 preamble 이 맞다.

- 끝나면 아래 두 명령 모두 실행:

```bash
orca orchestration send \
  --to term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --from <네 워커handle> \
  --type worker_done \
  --task-id <preamble 의 taskId> --dispatch-id <preamble 의 dispatchId> \
  --subject "reviewer_spec 완료: <판정 한 줄>" \
  --body "판정(PASS/WARN/FAIL) / 위반 목록(파일:줄) / 리포트 경로"

orca terminal send --terminal term_d5bec05e-881f-4a29-a144-fd73be7e23c4 \
  --text "[worker_done] reviewer_spec 완료 — <판정 한 줄>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --text "[질문] reviewer_spec: <질문>" --enter`
