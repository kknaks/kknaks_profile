# [reviewer] WORK-009 Phase 2a-1 코드 검수 — AX 초안 「수정」 모달 = 저장

너는 **strong-hajin `reviewer` 워커**다. **맥락이 없다** — 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/roles/strong-hajin/reviewer/role.md` (+ `rules.md`). **read-only.** 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/review-fe-p2a1-report.md` 하나. 판정 FAIL(계약과 다르게 돈다)·WARN·PASS, 각 지적 파일:줄+근거. 테스트는 직렬로만(`npx vitest run --no-file-parallelism <파일>`), 서버·브라우저 금지.

## 1. 대상
`/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish2` 의 **`frontend/` 미커밋 변경**(`git diff -- frontend` · 새 `frontend/src/features/action/AxDraftSave.test.tsx`). 2b `c64cddf`·2a-2 `d1bb87d` 는 커밋됨. `backend/` 미커밋 변경은 Phase 1 — 다른 reviewer 가 본다, 대상 아님(계약 확인용으로 읽기만).

## 2. 기준
- WP `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/para/projects/summer-star/strong-hajin/30-work/work-009-polish2.md` **Phase 2a-1** · SPEC-002 v0.4.0 §2.9·S-7·§4 「초안 저장」·§6
- 서버 계약: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/be-p1-worker-report.md` 「저장 명령 FE 계약 — 2a」 (실제 코드 `backend/` 로 대조)
- 발주서 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/strong-hajin-polish2-fe-p2a1-brief.md` · 추가 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/strong-hajin-polish2-fe-p2a1-fix0.md` · 워커 보고 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/fe-p2a1-worker-report.md` · 조사 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/fe-survey-report.md` §2

## 3. 볼 것
1. 계약 충실도 — 창 「저장」(파랑) · save_draft 만(confirm 안 부름) · 저장 뒤 카드 새 회차(채팅=대화 재조회 / 홈·칩=저장 응답 봉투로 교체) · 실패 창 안만(전역 띠 없음, fix0) · 입력 유지 · 등록이 새 `base_submission_version` 으로 · 자료 `attachment_draft_ids` · [수정] 은 save 명령 있을 때만
2. **낡음 경합** — 채팅 카드가 저장 뒤 재조회 전에 등록되면? 홈·칩 창이 저장 응답 봉투를 쥔 채 부모가 옛 item 을 다시 내리면(「더 높은 회차를 따른다」 구현이 맞나) · `expected_version` 이 저장으로 안 오른다는 서버 계약과 FE 가 맞나
3. 범용 렌더러 제외 5자리 — 빠진 자리 재계수(`allowed_commands`·`commands` 를 map 해서 단추로 그리는 곳 grep)
4. 다른 `CreateWorkModal` 자리 불변 — 6 호출 재계수
5. 조용히 통과하는 자리 — 모킹이 서버 계약과 다른 응답 모양을 쓰는 테스트 · 빈 단언
6. 사용자가 실물에서 만날 자리 목록

## 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**
```bash
orca orchestration send \
  --to term_b2ea0fd5-1473-4b83-9a04-dcf769fbedba --from term_6cc0e759-ad0f-4ac7-96e5-17dc23eb0cc1 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "reviewer 완료: WORK-009 Phase 2a-1 코드 검수 <PASS|WARN|FAIL>" \
  --body "판정 / FAIL·WARN(파일:줄) / 재계수 / 화면 확인 목록 / 리포트 경로"
orca terminal send --terminal term_b2ea0fd5-1473-4b83-9a04-dcf769fbedba \
  --text "[worker_done] reviewer 완료 — Phase 2a-1 코드 검수 <판정>. 리포트 review-fe-p2a1-report.md" --enter
```
