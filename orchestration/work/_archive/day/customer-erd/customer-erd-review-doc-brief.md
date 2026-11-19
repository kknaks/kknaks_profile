
# [reviewer_doc] DAY-SPEC-000 · erd.md 메뉴 · 결제 · 시술권 · 선불카드 반영 검수

너는 **day `reviewer_doc` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/customer-erd-spec`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

너는 맥락이 없다 — 아래 파일이 전부다. planner 가 끝낸 변경(미커밋)을 **읽기만** 한다. 파일을 고치지 마라.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/reference/2026-11-18-day-customer/erd-draft.md` ← **대조 기준 (사용자와 닫은 ERD v1).**
- `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/customer-erd-spec-brief.md` — planner 가 받은 발주서(§2 두 조건 · §6 단계 · §7 금지).
- `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/spec-change-report.md` — planner 리포트(그대로 믿지 말고 diff 로 확인).
- `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/har-check-report.md` · `-2.md` · `-3.md` — KOS 실측 근거.
- 지금 prod 모델(읽기만): `git -C /Users/kknaks/git/CENTURION_DAY show origin/prod:<path>`.

**기대는 개념** — 해당 없음.

## 2. 배경

ERD v1 을 메디니스 정본(DAY-SPEC-000 칸 계약 · `40-architecture/erd.md` · `system.md` 한 줄 · `20-spec.md` · `README.md` 범위 문장)으로 옮겼다. 이 검수 PASS 뒤 코디가 mediness PR 을 올린다.

## 3. 계약

해당 없음.

## 4. 먼저 읽을 핵심 파일

- `git -C /Users/kknaks/orca/workspaces/mediness-mediness/customer-erd-spec diff origin/main -- products/day/` — 검수 대상 전부.

## 5. allowed_paths

- 리뷰 리포트 1개만 생성: `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/review-spec-report.md`
- 그 밖 전부 읽기만.

## 6. 할 일 — 축마다 PASS/WARN/FAIL + 파일:줄 근거

1. **ERD v1 대조** — v1 의 테이블 · 관계 · 핵심 칸 · 「정한 것」 전부가 SPEC-000 에 있나(빠진 것 · 다르게 쓴 것 · **v1 에 없는데 만든 것**). 테이블 이름 전수 표.
2. **상용 운영 조건** — 지금 prod 테이블 · 칸의 이름 · 타입을 바꾼 곳 0 인가(prod 모델을 직접 열어 대조) · 새 칸이 nullable/더하기인가 · 테이블마다 prod 표시가 맞나 · 백필 · 원장 전환이 OQ 로 열려 있나.
3. **KOS 제거 조건** — KOS id 칸이 `external_ref` 밖에 없나 · enum 이 DAY 말인가(KOS 문자열은 외부 열에만) · 시술권 생성 · 카드 생성 · 잔액 · 결제 합계 · 부분 환불을 DAY 칸만으로 할 수 있나 · KOS 응답에만 있는 계산값(카드 총액 · 티켓 가격)을 칸으로 만들지 않았나.
4. **이름 변경 일관성** — `procedure` · `medical_service`(메뉴 뜻) 잔존 grep(`products/day/` 전체 · 작업 `TaskKind.procedure` 같은 다른 뜻은 제외하고 분류).
5. **근거 · 열린 것** — 근거 없는 정책 0 · v1 「열린 것」이 §6 OQ 에 전부 · HAR 값(개인정보 · KOS id) 0(`grep -nE '01[0-9]-?[0-9]{3,4}-?[0-9]{4}|[0-9a-f]{24}'`).
6. **범위** — `products/day/` 밖 변경 0 · SPEC-001~005 · WORK · 10-decision 미변경.
7. **문서 정합** — erd.md 개략도 · 인벤토리 · 개수 문장이 SPEC-000 과 맞나 · `20-spec.md` · `README.md` 범위 문장.

리포트 끝: 전체 판정 · FAIL 은 고칠 곳 목록(파일:줄 · 무엇으로).

## 7. 범위 제약

- 파일 수정 금지(리포트 1개 제외). 커밋 · push · PR 금지.
- 결정하지 마라 — v1 과 다른 판단이 필요해 보이면 「사용자 판단」으로 모은다.

## 8. 검증

```
cd /Users/kknaks/orca/workspaces/mediness-mediness/customer-erd-spec && python3 scripts/lint-pipeline.py --strict  → products/day/ 범위 ERROR 0 (타 제품 기존 WARN/ERROR 는 '무관')
```

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_3d82d3ad-3bc3-4cdc-8cbd-0e98fbc89591 --from term_a1493591-1ed4-4c67-bdd4-651c5e654512 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_3d82d3ad-3bc3-4cdc-8cbd-0e98fbc89591 \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_3d82d3ad-3bc3-4cdc-8cbd-0e98fbc89591 --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
