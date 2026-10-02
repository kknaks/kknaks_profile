# [reviewer] WORK-008 Phase 5 검수 — AX 탐색 (backend)

너는 **strong-hajin `reviewer` 워커**다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/roles/strong-hajin/reviewer/role.md`. **read-only.** 코디 핸들 `term_d7b4a334-2cbd-42ab-9eab-e64a7b255d44`.

## 대상
`/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish` 의 **`backend/`·`docs/` 미커밋 변경**(HEAD `94cacfd`). `frontend/` 는 대상 아님(다른 워커가 project 참조 렌더 중).

## 기준
WP `…/para/projects/summer-star/strong-hajin/30-work/work-008-polish.md` **Phase 5** · 조사 `…/orchestration/work/strong-hajin-polish/research-graph-search.md` · 발주 `strong-hajin-polish-be-p5-brief.md`

## 볼 것
1. 계약 1: 정책·도구 설명이 「찾아서 한 후보로 확정될 때만 채우고, 못 찾거나 여럿이면 비우고 말한다, ID 를 지어내지 않는다」를 말하나. 「graph_search 먼저 부르지 말라」 축소가 다른 흐름(사람 찾기 등)을 깨지 않나. Claude 어댑터 동일
2. 계약 2: project 참조 bind·재인가 — **권한 없는 프로젝트가 근거로 새지 않나**(_remember 범위·읽기 시 재인가). graph 도구로 본 노드를 기억하는 범위가 넓어져 생기는 누설·오인용
3. 계약 3: graph_search 인자 설명 = 실제 스키마
4. `test_material_identity` 단언을 좁힌 것이 정당한가(계약 약화가 아닌가)
5. inventory 는 설명·제목 문자열만인가
6. 조용히 통과하는 자리

## allowed_paths
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/work/strong-hajin-polish/review-p5-report.md` 하나만. 테스트는 Makefile 타깃만, 서버 금지

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send --to term_d7b4a334-2cbd-42ab-9eab-e64a7b255d44 --from <네 워커handle> --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "reviewer 완료: WORK-008 Phase 5 검수 <PASS|WARN|FAIL>" --body "판정 / FAIL·WARN(파일:줄) / 리포트 경로"
orca terminal send --terminal term_d7b4a334-2cbd-42ab-9eab-e64a7b255d44 --text "[worker_done] reviewer 완료 — Phase 5 검수 <판정>. 리포트 review-p5-report.md" --enter
```
