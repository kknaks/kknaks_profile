
# [reviewer_doc] 리뷰 — 데모/운영 KOS 쓰기 구분 · dev is_demo 거르기 없앤 SPEC 개정

너는 **day `reviewer_doc` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-procedure-board-2-spec`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

planner 는 끝났다(커밋 전 · 워크트리에 변경 8파일). 너는 읽기만 한다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/day-procedure-board-2-spec-brief.md` ← 이번 개정의 지시(§2 사용자 결정 · §6 · §7). 단 §6.2 · §6.3 은 바뀜: 레포 규칙대로 10-decision 무변경 · 30-work WP 안 만듦 → SPEC 개정 줄 + log.md decision-add · Delivery 초안은 planner 리포트에
- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/research-demo-vs-live-report.md` ← 바꿀 자리 전수 목록(§1 23자리 · §2 쓰기 5개 확인 상태 · §4 스펙 절 · §5 F1~F9)
- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/planner-demo-vs-live-report.md` ← planner 보고 · Delivery 초안 D1~D5
- 대상: `git -C /Users/kknaks/orca/workspaces/mediness-mediness/day-procedure-board-2-spec diff` (products/day/ 8파일)

**기대는 개념** — 이 작업이 따를 판단 기준. 안 주면 워커가 매번 처음부터 정하고,
같은 결정이 작업마다 달라진다. 없으면 "해당 없음".

- 해당 없음

## 2. 배경 / 무엇을 바꾸나

사용자 결정(2026-11-09): KOS 데모와 실제 병원은 같은 API · 테넌트만 다르다. dev/prod 분리는 스키마(`day_dev` · `day_prod`)의 연결 데이터로 이미 된다. 그래서 `is_demo` 로 가르는 분기(데모만 KOS 쓰기 5개 · dev 서버는 is_demo 연결만)와 `is_demo` 칸을 없앤다. 시작 취소 KOS 쓰기는 유지(방배정.har · 데모 실물 확인).

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

화면 · API 계약은 바뀌지 않아야 한다(바뀐 자리가 있으면 지적).

## 4. 먼저 읽을 핵심 파일

- diff 전체 + 리서치 §4 스펙 절 목록

## 5. allowed_paths — 이 밖은 건드리지 마라

- `(read-only — 리포 파일 수정·생성 금지. 산출물은 브리프가 지정한 리뷰 리포트 파일 1개뿐)`
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/review-doc-demo-vs-live-report.md`

## 6. 구현 단계

1. **빠진 자리**: 리서치 §4 의 스펙 절 · §1 의 23자리 중 스펙에 닿는 것이 전부 고쳐졌나 — `products/day/` 를 `is_demo` · `demo` · `데모` · `trial` · `TRIAL` · `ON_LIVE` · `not_supported` · `APP_ENV` 로 다시 grep 해서 남은 것을 전부 판정(남겨도 되는 것 / 빠진 것)
2. **새 갈림 금지**: 환경 · 연결 종류로 동작을 가르는 문장이 새로 생기거나 남지 않았나
3. **사실**: 확인 안 된 4개 쓰기가 「확인됨」으로 바뀐 곳 · 지어낸 KOS 경로 · 값 · 화면 문구가 없나. 시작 취소 「HAR 있음(방배정.har)」 표기가 맞게 바뀌었나
4. **뒤집힌 결정 기록**: log.md 에 11-03 · 11-06 W6 · 11-09 결정이 취소선 · 사유로 있나
5. **planner 가 남긴 판단 확인**: D2 에서 #17~#20(kit · /docs · APP_ENV 필수 · 로컬 기본 dev)을 연결 무관이라 남긴 것이 맞나 · SPEC-000 is_demo 칸 삭제 · OQ-01-2/3 · OQ-22 · OQ-23
6. **Delivery 초안 D1~D5** 가 리서치 §1 · §3 을 빠짐없이 덮나(코드 자리 · 테스트)
7. lint: `python3 scripts/lint-pipeline.py --strict` → products/day/ ERROR 0

## 7. 범위 제약 — 하지 말 것

- 파일 수정 · 커밋 금지 · KOS 호출 금지

## 8. 검증

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
  --to term_b915fb18-742f-4779-962c-79848020b8d5 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_b915fb18-742f-4779-962c-79848020b8d5 \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_b915fb18-742f-4779-962c-79848020b8d5 --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
