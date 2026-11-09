
# [reviewer_doc] DAY SPEC-000 데이터 모델 · architecture 검수 — 원천 대비 누락 · 발명 · 왜곡

너는 **day `reviewer_doc` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**너는 앞 맥락이 없다.** planner 워커가 이 워크트리의 `products/day/` 를 막 썼다(미커밋). 너는 **read-only** — 문서를 고치지 마라. 산출물은 리포트 파일 1개뿐이다.

## 1. SSOT — 먼저 읽을 것

**원천(정답지) = 사용자가 2026-11-03 칸 단위로 확정한 테이블 설계.** SPEC 은 이걸 옮긴 것이어야 한다.

- `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/erd/README.md` — 1차 범위 · 공통 규칙 · 관계도
- `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/erd/01-hospital.md` · `02-customer.md` · `03-visit.md` · `04-staff.md` · `04-1-menu.md` · `05-task.md` · `06-room.md` · `07-misc.md`
- planner 발주서 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/day-data-architecture-spec-brief.md` — planner 에게 무엇을 시켰나(§6 · §7)
- planner 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-report.md` — planner 가 주장한 것(개수 대조 · 미결 13항). **주장을 믿지 말고 실물로 확인하라.**

(원천 파일은 작업 중 `erd/` 하위로 옮겨졌다 — 내용은 그대로다.)

## 2. 배경 / 무엇을 바꾸나

planner 가 원천 설계를 mediness 문서 모양으로 옮겼다: `README.md` · `20-spec/spec-000-data-model.md`(DAY-SPEC-000) · `20-spec.md` · `30-work.md` ·
`40-architecture/`(README · system · erd) · `10-decision.md`(DAY-ESC-001) · `log.md`. 설계는 바꾸지 않는 것이 계약이었다.
너는 **옮기는 과정에서 생긴 누락 · 발명 · 왜곡**을 찾는다. 설계 자체의 좋고 나쁨은 판정 대상이 아니다(눈에 띄면 「참고」로만).

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

해당 없음.

## 4. 먼저 읽을 핵심 파일

- `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec/products/day/` 전부 — 검수 대상
- `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec/rules/document-pipeline.md` · `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec/AGENTS.md` — 폴더별로 두는 것 · 두지 않는 것(40-architecture 에 컬럼 전체 목록 금지 등) · frontmatter
- `git -C /Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec status --short` — 범위 산정(전부 untracked `products/day/`)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `(read-only — 리포 파일 수정·생성 금지. 산출물은 브리프가 지정한 리뷰 리포트 파일 1개뿐)`

## 6. 구현 단계

1. **누락**: 원천의 테이블 · 칸(주제 01 ~ 07 + 04-1)이 SPEC-000 에 전부 있는가. 주제별로 원천 행 수 · SPEC 행 수를 **직접 세어** 대조표를 만든다(planner 숫자를 베끼지 마라).
2. **발명**: SPEC · architecture · README · ESC 에 원천에 없는 테이블 · 칸 · 타입 · 필수 여부 · 정책 · enum 값이 들어갔는가.
3. **왜곡**: 타입 · 필수 · 설명 · 외부(KOS) 칸 · 관계가 원천과 다른가. 「1차 만들지 않음(04-1)」 · 「보류」 · 「범위 밖」 · 「바로 적용 — 검토는 이후(07)」 표시가 살아 있는가.
4. **열린 것**: 원천의 「정할 것 · 확인할 것 · 논의 중」이 전부 OQ 로 옮겨졌고, 결정된 것처럼 쓰이지 않았는가.
5. **문서 규칙**: 40-architecture 에 칸 전체 목록이 없는가(관계 · 키만) · frontmatter · 인덱스(20-spec.md · 30-work.md) 미러 · ESC 형식 · lint `--strict` 1회.
6. **planner 미결 13항** — 각각 「원천이 실제로 그렇다(원천 쪽 문제)」 / 「옮기면서 생긴 문제」로 가른다.
7. **보안**: KOS 키 · 토큰 · 테넌트 id · 실명 · 이메일이 없는가(grep).

## 7. 범위 제약 — 하지 말 것

- 리포 파일 수정 · 생성 금지(리포트 1개만). 커밋 · push · PR 금지.
- 설계를 판정하지 마라 — 원천과 다른지만 본다.

## 8. 검증

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-doc-report.md` — 판정 PASS / WARN / FAIL · FAIL · WARN 각 항목에 `파일:줄` + 근거(원천 `파일:줄`) · 주제별 개수 대조표 · planner 미결 13항 분류.

```
SPEC·WORK 를 DEC·baseline 에 대조. lint-pipeline --strict 로 products/day/ ERROR 0. 각 지적에 파일:줄 + 근거. 판정 FAIL/WARN/PASS
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
  --to term_70b6f193-86a2-4c1d-8965-4e2220cef9b3 --from term_441c2cdb-68e6-4463-b694-d8d6adfc7210 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: DAY SPEC-000 검수 <판정>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_70b6f193-86a2-4c1d-8965-4e2220cef9b3 \
  --text "[worker_done] reviewer_doc 완료 — DAY SPEC-000 검수 <판정>. 리포트 work/day-data-architecture/review-doc-report.md" --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_70b6f193-86a2-4c1d-8965-4e2220cef9b3 --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
