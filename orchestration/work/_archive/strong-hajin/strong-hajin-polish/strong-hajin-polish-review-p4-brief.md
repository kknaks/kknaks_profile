# [reviewer] WORK-008 Phase 4 검수 — 회의 요약 실패 (backend + infra)

너는 **strong-hajin `reviewer` 워커**다. 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/roles/strong-hajin/reviewer/role.md`. **read-only.**

## 대상
1. 코드 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish` 미커밋 변경(HEAD `8700bd0`) — backend 9파일 + `delivery/README.md`
2. 인프라 `/Users/kknaks/orca/workspaces/k8s_infra_mac/strong-hajin-polish-infra` 미커밋 변경 — `charts/strong-hajin/` (_helpers.tpl·values*.yaml)

## 기준
- WP `…/para/projects/summer-star/strong-hajin/30-work/work-008-polish.md` **Phase 4** · 조사 `…/orchestration/work/strong-hajin-polish/research-meeting-summary.md`
- 결정(`_RESUME.md` §2): 세션 런타임 홈을 Mac 호스트 hostPath `/mnt/mac/strong-hajin/codex-runtime` → 앱 기본 경로 `/app/.scax/codex-runtime` 에 back·워커 4개 공유(env 불필요). 코드는 env 선택 + resume 실패 시 콜드스타트(안전장치) + stderr 로그
- 발주서 `strong-hajin-polish-be-p4-brief.md` · `strong-hajin-polish-infra-brief.md`

## 볼 것
1. 계약 1~3 · 콜드스타트가 「같은 결과물」인가(전사 전량, 회의록 형식), 재시도 낭비 없음, 콜드도 실패면 기존 상태
2. **공유 홈의 동시성 위험(핵심)**: codex 가 CODEX_HOME 에 쓰는 것(sessions rollout · sqlite state · config · auth symlink 등)을 코드·codex 동작으로 확인하고, **여러 파드가 같은 디렉터리를 동시에** 쓸 때 깨질 자리가 있는지. Mac→lima VM 마운트(`/mnt/mac`) 위 sqlite 잠금이 믿을 만한지 근거로 판단. `prepare_isolated_codex_home` 의 symlink 경합. 위험이 있으면 대안(sessions 만 공유 · 파드별 하위 디렉터리 + sessions 공유 등)을 근거와 함께 제시
3. 인프라: 다섯 deployment 전부·lima-worker-1 고정·codex-home PVC 불변·hostPath type Directory(노드 디렉터리 선행 필요)·dev 경로 분리
4. resume 를 쓰는 다른 자리(워커 보고: 회의 배치·대화 turn) — 공유 홈으로 함께 나아지는지, 남는 위험
5. stderr 로그 마스킹이 비밀값을 정말 막는지
6. 운영 반영 체크리스트(노드 mkdir · 기존 실패 회의 [다시 시도])

## allowed_paths
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/work/strong-hajin-polish/review-p4-report.md` 하나만. 테스트는 Makefile 타깃만, 서버·클러스터 접근 금지

## 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**
```bash
orca orchestration send --to term_d7b4a334-2cbd-42ab-9eab-e64a7b255d44 --from <네 워커handle> --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "reviewer 완료: WORK-008 Phase 4 검수 <PASS|WARN|FAIL>" --body "판정 / FAIL·WARN / 공유 홈 동시성 결론·대안 / 운영 체크리스트 / 리포트 경로"
orca terminal send --terminal term_d7b4a334-2cbd-42ab-9eab-e64a7b255d44 --text "[worker_done] reviewer 완료 — Phase 4 검수 <판정>. 리포트 review-p4-report.md" --enter
```
