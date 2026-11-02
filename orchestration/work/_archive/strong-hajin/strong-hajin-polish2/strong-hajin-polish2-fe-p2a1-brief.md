# [frontend] WORK-009 Phase 2a-1 — AX 초안 「수정」 모달 = 저장

너는 이 워크트리에서 2b·2a-2 를 한 **strong-hajin `frontend` 워커**다. 역할 문서·AGENTS 는 앞 판과 같다(`/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/strong-hajin-polish2-fe-p2a-brief.md`).

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish2` (2b `c64cddf` · 2a-2 `d1bb87d` 위). ⚠ `backend/` 에 Phase 1 미커밋 변경이 있고 reviewer 가 검수 중이다 — 너는 `frontend/` 만, 서버 코드는 읽기만.

## 1. SSOT
- WP `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/para/projects/summer-star/strong-hajin/30-work/work-009-polish2.md` **Phase 2a-1** — 체크박스 하나하나가 계약
- SPEC-002 v0.4.0 §2.9([등록]·[수정]·수정 창 「저장」·저장 뒤) · S-7 · §4 「초안 저장」 · §6
- **서버 계약(Phase 1, 정본)**: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/be-p1-worker-report.md` 의 「저장 명령 FE 계약 — 2a」 절. 요지:
  - 명령 id `save_draft`, `POST /api/action-items/{id}/commands/save_draft` — 기존 `runActionCommand` 경로 그대로
  - 입력 `{expected_version, base_submission_version, draft, attachment_draft_ids?}` (confirm+draft 와 같은 모양)
  - 응답 = 판단 대기 봉투 모양 — `submission_version`·`edit_contract.values`·`edit_contract.base_submission_version` 이 새 회차, `expected_version` 은 그대로, status `awaiting_review`
  - 찾는 법: `allowed_commands`/`commands` 에 `save_draft` · `edit_contract.save_command === "save_draft"`
  - 오류: 낡은 회차 422 「base submission version is stale」·「action version is stale」(지금 confirm 과 같은 문장) · 검증 422 · 다른 상태 422
  - ⚠ 범용 렌더러(ActionCenter footer `commands.map`, MessageList `ActionCommandButtons`)가 `save_draft` 를 단추로 그리지 않게 — 두 kind 가 그 경로로 떨어질 때 「저장」 단추가 서면 안 된다(제외 처리)
- 조사 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/fe-survey-report.md` §2

## 2. 계약 (WP 2a-1 요약)
- `axDraft` 모드 하단 주 단추 = 「저장」/「저장 중…」, 색 앱 DS 파랑(서랍 밖 포털). 닫기 그대로
- 「저장」 = `save_draft`(confirm 아님). 성공 → 모달 닫고 카드가 **서버 새 회차 값**을 보인다(채팅 = 대화 재조회, 홈·칩 = 판단 대기 재조회). 카드는 pending 그대로 [거절][수정][등록], 머리 「초안 · N회차」 가 오른다
- 실패 문구는 모달 안(`axDraft.error`), 입력은 남는다. 낡음 오류는 지금 confirm 낡음과 같은 문구 처리
- 카드 「등록」 = 최신 회차 draft 없이 confirm — `base_submission_version` 이 **저장 뒤 새 회차**여야 한다(옛 값을 들고 있으면 낡음 오류). 카드가 어디서 그 값을 읽는지 확인
- 자료 탭: 지금처럼 즉시 판단 항목 자료 초안 → 저장 때 `attachment_draft_ids` 실림
- 홈 판단 대기·「AX 제안」 칩의 `AxDraftModal` 「수정」도 같은 저장
- `CreateWorkModal` 을 미리 채운 값으로 여는 다른 자리(조사 §2-4 7자리)는 **바꾸지 않는다** — 전부 세어 확인

## 3. allowed_paths
- `frontend/src/`

## 4. 하지 말 것
- 커밋·push 금지 · 서버·프론트 띄우지 마라 · 사용자 포트 금지

## 5. 검증
- 직렬 vitest · tsc · build. 기준선 5 실패 그대로
- 새 테스트: 저장 단추 문구 · 저장이 save_draft 를 부르고 confirm 을 부르지 않음 · 저장 뒤 재조회 · 실패 문구 모달 안 · 저장 뒤 카드 등록이 새 base_submission_version 으로 confirm · 범용 렌더러에 save_draft 단추 없음 · 다른 CreateWorkModal 자리 불변

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_b2ea0fd5-1473-4b83-9a04-dcf769fbedba --from term_82fc2322-7b14-4d60-90ee-efe1c243fd31 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "frontend 완료: WORK-009 Phase 2a-1" \
  --body "변경 파일 / 계약별 구현 위치 / 다른 CreateWorkModal 자리 확인 / 기준선 vs 결과 / 미결"
orca terminal send --terminal term_b2ea0fd5-1473-4b83-9a04-dcf769fbedba \
  --text "[worker_done] frontend 완료 — WORK-009 Phase 2a-1. 상세는 인박스." --enter
```
