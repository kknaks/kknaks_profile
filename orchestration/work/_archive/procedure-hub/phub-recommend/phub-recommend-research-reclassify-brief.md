# [researcher] 분류표 재판정 v2 — 1차 검수 반영

너는 **procedure-hub `researcher` 워커**다(read-only). 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`
작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` (아래 2개 파일 외 수정 금지)

## 1. 기준 (`orchestration/work/phub-recommend/`)

- `taxonomy-classify.json` (v1 정본 · 521) · `DEC-002.md` · `DEC-003.md`(특히 D-05 · D-06 반려 유형 규칙 · OQ-306~317)
- `_RESUME.md` §2 **10-27 행 전부** — 특히: 부위 없는 시술 · 「전신」 두 뜻 분리(수액 = 부위 해당 없음 + 투여 경로) · 필링 외 11건 개별 · 수액 경로는 허가 용법 확인 전까지 미정 · **OQ-317: 계열 아래 「용도별」 항목은 부위 이름이면 단위 시술(계열 × 부위), 목적 이름이면 목적 엣지 + 그 부위들의 단위 시술**
- 1차 검수 답: `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-kknaks-profile-----------/7f782343-8998-41d7-8392-00bd3c8596ee/scratchpad/classify-answers/answers/*.json` — {decision approve|reject, reason}. 521 전부 있다
- 원천 저장본 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/`

## 2. 할 일 — 항목마다 v2 판정과 처리 상태

| 대상 | 처리 |
|---|---|
| 승인 + kind ≠ site_or_purpose | **그대로**(status `approved`, 다시 묻지 않음) |
| kind = site_or_purpose (승인 · 반려 모두, 20) | OQ-317 규칙으로 재판정 → `regate` |
| 반려 ③ 판정 틀림(사유에 고칠 값) | 사유대로 고침 → `regate` |
| 반려 ② 부위 없음 | DEC-003 D-05 · _RESUME 규칙으로 재판정(수액 → 부위 해당 없음, 경로는 「허가 용법 확인 대기」 · 필링 → 얼굴 전체 · 그 외 11은 원천 부위 표현으로 개별) → `regate` |
| 반려 ④ 분류 경계 | 해당 OQ(309~316) 번호를 붙이고 **질문 카드** — 선택지 2~3개(DEC-003 OQ 문장에서) → `question` |
| 반려 ① 정체 확인 불가 | 판정 유지, `waiting_mfds`(식약처 원장 대기) — 사유 안의 허가 정보(사용자가 붙인 것)는 `evidence` 로 옮긴다 |
| 반려 ⑤ 참고 자료 | 자료를 `evidence` 로 · 판정 재검토 후 `regate` |

- 유형 판정은 DEC-003 D-06 규칙과 같은 방식으로(DEC-003 의 건수 ① 137 · ② 47 · ③ 42 · ④ 67 · ⑤ 3 과 맞춘다. 다르면 notes)
- 사유의 링크 · 붙여 넣은 설명은 요약해서 `evidence`(출처 표시). 사람 이름 · 연락처는 옮기지 않는다

## 3. 산출물

1. `orchestration/work/phub-recommend/taxonomy-classify-v2.json` — v1 과 같은 items 구조 + 필드: `status`(approved · regate · question · waiting_mfds) · `v1`(바뀐 필드의 이전 값) · `change_reason` · `review_type`(①~⑤ · site_or_purpose) · `question`({oq, text, options[]} — question 일 때) · `evidence`[]
   - summary 에 status 별 건수 · 유형별 건수
2. `taxonomy-classify-v2.md` — 요약: status 별 건수 · regate 의 대표 변경 예 · question 목록(OQ 별) · waiting_mfds 수

## 4. 제약

- 원천 저장본 · 위 파일만 읽는다. 식약처 · stg 호출 금지 · 추측 금지(모르면 question 이나 waiting)
- public — 키 · 실명 금지

## 5. 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 분류표 재판정 v2" \
  --body "status 별 건수 / 유형별 건수(DEC-003 과 대조) / question OQ 별 / 미결"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] researcher 완료 — 분류표 재판정 v2. 상세는 인박스." --enter
```
