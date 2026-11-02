
# [reviewer_spec] task·incident 재정비 스펙 + WP-124 검수

너는 **mediness `reviewer_spec` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/roles/mediness/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/task-redesign-spec`
base 브랜치: `origin/mediness` → 최종 PR 대상 `mediness` (PR 은 코디네이터가 올린다)

planner 워커의 산출물(미커밋 변경 + untracked 3파일)이 이 워크트리에 있다. **read-only 검수** — 리포 파일을 고치지 마라.

## 1. SSOT — 먼저 읽을 것

**판정 기준 (결정의 SoT — 스펙이 이것과 어긋나면 FAIL):**

- `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/work/task-redesign/_RESUME.md` §2 결정 표
- `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/work/task-redesign/task-redesign-spec-brief.md` — planner 가 받은 발주 브리프 (범위·계약·제약)

**사실 대조 근거 (조사 스냅샷 — 코드 좌표·죽은 계약 목록):**

- `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/work/task-redesign/research-task-status.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/work/task-redesign/research-incident.md` (특히 §A-7 D-1~D-27 죽은 계약, §B-9 C1~C15)

기대는 개념 — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

planner 가 task 원장 단일화 + incident 재정비를 스펙 층위에 반영했다: 도메인 문서 2건 신설(`runtime_task.md`·`version_wbs_task.md`), ERD 전면 재작성, SPEC 6건 개정(152 전면 / 154 / 125 / 110 / 153 / 031), WP-124 신설(proposed), WP-074 폐기 표시, 인덱스·log 동기. 이 산출물이 ① 결정 SoT 와 정합한지 ② 죽은 계약이 실제로 제거됐는지 ③ SoT 층위 규칙(도메인 문서 = enum/전이표 정본, SPEC 은 링크)이 지켜졌는지 검수한다.

## 3. 계약 (검수 관점 체크리스트)

**결정 SoT 대조 — 각 항목이 스펙에 정확히 반영됐는지:**

1. 상태 5값(todo/in_progress/blocked/done/canceled), `accept_pending` 부재
2. 수락·거절 개념 폐기 — decline 계약·`task_declined`·`accepted_at` 축이 새 계약에 없어야 함. 거절 = 재배정(담당자 본인 재배정 요청 가능)
3. 재배정 = todo 리셋 + started_at 클리어, terminal 재배정 금지 유지
4. 착수 = 명시 시작만 — 자동전환 폐기(알림 강등), 시스템 생성 태스크도 todo 생성 후 시작 **전이**
5. incident 정본 흐름(브리프 §3 코드블록)과 spec-152 서술 일치 — is_lead 게이트 · Slack fail-loud · cc=버전 참여자(OQ 표기) · 완료 표면 슬랙만 · 피드백 게이트 유지 · 라운드 판정 활성 라운드 기준 · run 감사 · 종결 시 추적 테스크 정리
6. 범위 제외가 본문 계약에 침입 안 했는지 — 알림/DM·에스컬레이션·슬랙 어댑터는 OQ/후속 절에만
7. WP-124 가 새 스펙만 SoT 로 참조하는지(연구 문서·구 계약 참조 금지), WP2(incident) 문서를 안 썼는지

**교차 정합:**

8. 죽은 계약 D-1~D-27 grep 스윕 — products/mediness/ 에 활성 서술로 잔존하면 FAIL (개정 이력·«폐기됨» 명시문·동결 work-074 는 허용)
9. 도메인 문서 ↔ SPEC 층위 — enum·전이표가 SPEC 본문에 복제돼 있으면 WARN
10. ERD ↔ 도메인 문서 ↔ SPEC 상호 링크·테이블 정합
11. planner 자체 보고의 예외 6건(HTML 시안 manual_incident 잔존 / §4.19 와이어프레임 / WP-114 충돌 OI-1 / accepted_at drop OI-6 / task_unblocked 신설 OI-5 / WP2 미작성) — 각각 문서에 명시돼 있는지 확인하고 판정에 참작

## 4. 먼저 읽을 핵심 파일

- `products/mediness/40-architecture/domains/runtime_task.md` — 새 SoT. 전이표·이벤트 어휘부터
- `products/mediness/30-work/work-124-task-ledger-unification.md` — 빌드 계획. 코드 좌표 실재 여부는 research 문서 §B 와 대조
- `products/mediness/20-spec/spec-152-...md` — 전면 재정비본. 구 화석 3절(§Action.status 등) 제거 여부
- `git -C <워크트리> diff` + untracked 3파일 — 변경 범위 산정은 diff 로

## 5. allowed_paths — 이 밖은 건드리지 마라

- (read-only — 리포 파일 수정·생성 금지. 산출물은 아래 리뷰 리포트 파일 1개뿐)
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/work/task-redesign/review-spec-report.md`

## 6. 구현 단계

1. 결정 SoT·발주 브리프를 읽고 판정 기준을 세운다
2. `git diff` + untracked 로 변경 전모를 산정한다
3. §3 체크리스트 1~11 을 각각 판정한다 (근거 = 파일:줄)
4. `python3 scripts/lint-pipeline.py --strict` 실행, mediness 범위 ERROR 0 확인
5. 리포트를 지정 경로에 작성 — 판정(PASS/WARN/FAIL) + 항목별 근거 + 위반 목록(파일:줄)
6. 완료 보고 (§9)

## 7. 범위 제약 — 하지 말 것

- 리포 파일 수정·생성 금지 (리포트 1개 예외 — 코디 레포 쪽 경로다)
- 코드 레포(mediness-app) 수정 금지 — 대조를 위한 읽기는 허용
- 문체·표현 지적으로 FAIL 을 내지 마라 — FAIL 은 결정 SoT 위반·죽은 계약 잔존·계약 모순만

## 8. 검증

```
python3 scripts/lint-pipeline.py --strict 실행 → 이번 제품 범위 ERROR 0 확인 (타 제품 기존 WARN/ERROR 는 '무관'으로 분리 보고). 리뷰는 read-only — 문서를 고치지 않는다
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_1d6e5d93-2be9-4125-b7eb-42b1de52b5ed --from term_8412cd16-b0f5-4f5d-a841-da64055e98ba \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_spec 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_1d6e5d93-2be9-4125-b7eb-42b1de52b5ed \
  --text "[worker_done] reviewer_spec 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_1d6e5d93-2be9-4125-b7eb-42b1de52b5ed --text "[질문] reviewer_spec: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
