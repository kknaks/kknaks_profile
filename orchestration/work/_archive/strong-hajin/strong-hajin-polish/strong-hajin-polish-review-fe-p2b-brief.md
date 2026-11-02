# [reviewer] WORK-008 Phase 2 재검수 (fix1 후)

너는 Phase 2 를 검수한 **strong-hajin `reviewer` 워커**다. 규칙은 `strong-hajin-polish-review-fe-p2-brief.md` 와 같다. **read-only**, 대상은 `frontend/` 만(backend 워커가 `backend/` 작업 중).

## 볼 것
1. 앞 리포트 `review-fe-p2-report.md` 의 **FAIL-1 · WARN 1~5 가 각각 닫혔나**(파일:줄). WARN-4 는 워커가 「MyWork actionItems 는 죽은 상태라 해당 없음」이라 했다 — 사실인지 확인
2. 세대 토큰: 기억을 쓰는 경로가 **전부** 같은 문을 지나는지 워커 계수(쓰기 경로 33)를 다시 센다. `App.tsx` 에서 언마운트 시 주인 해제 effect 를 지운 것이 누설을 만들지 않는지(StrictMode·로그아웃·탭 닫기)
3. WARN-1 의 「갱신 전 명령 잠금」이 갱신 실패 시 영구 잠김으로 남는 경로 · 잠금이 빠진 명령 자리
4. fix1 이 새로 만든 문제. 직렬 전체 1144 중 6 실패(기준선 5 + 플레이크 Checklist 1)라는 보고를 필요하면 확인
5. 사용자가 실물에서 만날 자리(코디 화면 확인 목록 갱신)

## allowed_paths
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/work/strong-hajin-polish/review-fe-p2b-report.md` 하나만

## 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**
```bash
orca orchestration send \
  --to term_7941dbc9-8078-4818-8d3d-bfd5545cce31 --from <네 워커handle> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "reviewer 완료: WORK-008 Phase 2 재검수 <PASS|WARN|FAIL>" \
  --body "판정 / 앞 지적 닫힘표 / 새 지적(파일:줄) / 리포트 경로"
orca terminal send --terminal term_7941dbc9-8078-4818-8d3d-bfd5545cce31 \
  --text "[worker_done] reviewer 완료 — Phase 2 재검수 <판정>. 리포트 review-fe-p2b-report.md" --enter
```
