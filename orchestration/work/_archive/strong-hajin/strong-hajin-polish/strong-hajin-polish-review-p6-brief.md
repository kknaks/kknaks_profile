# [reviewer] WORK-008 Phase 6 핫픽스 검수 — 세션 잃은 대화·회의 배치

너는 **strong-hajin `reviewer` 워커**다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/roles/strong-hajin/reviewer/role.md`. **read-only.** 코디 핸들 `term_d7b4a334-2cbd-42ab-9eab-e64a7b255d44`.

## 대상
`/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish` 브랜치 `kknaksss/strong-hajin-hotfix-session`(origin/main `3d47a32` 기준) 미커밋 `backend/` 변경.

## 기준
WP `…/para/projects/summer-star/strong-hajin/30-work/work-008-polish.md` **Phase 6** · 발주 `strong-hajin-polish-be-p6-brief.md` · 운영 증거(`no rollout found for thread id`)

## 볼 것
1. 대화: 세션 없음일 때만 새 세션 재시도, 같은 turn 안, 최근 기록 포함, 첫 시도 이벤트가 turn 상태를 오염하지 않음, 다음 turn 이 새 세션을 이음. 일반 실패를 삼키지 않음
2. 회의 배치: 새 세션에 **처음부터 전체** 재전송이 맞는가(앞 안건 유실 없음) · 중복 기록·이중 과금성 반복이 없는가 · 재오픈 실패 시 평소 실패
3. 세션 없음 판정이 진짜 오류를 「세션 없음」으로 오인하지 않는가(문구 매칭 범위)
4. Claude 판정은 실측 없음 — 위험만
5. 조용히 통과하는 자리

## allowed_paths
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/work/strong-hajin-polish/review-p6-report.md` 하나만. 테스트는 Makefile 타깃만

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send --to term_d7b4a334-2cbd-42ab-9eab-e64a7b255d44 --from <네 워커handle> --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "reviewer 완료: WORK-008 Phase 6 검수 <PASS|WARN|FAIL>" --body "판정 / FAIL·WARN(파일:줄) / 리포트 경로"
orca terminal send --terminal term_d7b4a334-2cbd-42ab-9eab-e64a7b255d44 --text "[worker_done] reviewer 완료 — Phase 6 검수 <판정>. 리포트 review-p6-report.md" --enter
```
