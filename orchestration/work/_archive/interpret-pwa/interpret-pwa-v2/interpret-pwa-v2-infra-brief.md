# [infra] interpret-pwa WP17 — back PVC · 기록 env (sync 없음)

너는 **interpret-pwa infra 워커**다. 역할(절대경로): `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/roles/interpret-pwa/infra/role.md` (+ rules · skills · tools · workflow)
작업 워크트리: `/Users/kknaks/orca/workspaces/k8s_infra_mac/interpret-pwa-v2` (k8s_infra_mac main) · 커밋 · push · sync · apply 금지

## SSOT
- `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/20-spec/spec-001-interpret-pwa.md` **0.6.0** — §4.2.1 ~ §4.2.3(사전) · §5.9(통역 기록) · §9.6(배포 PVC) · §9.1 · §9.3 ⑲ ~ ㉑
- `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/30-work/work-001-interpret-pwa.md` **WP17 행**(범위 · 완료 조건 · 부분 검증)
- DEC-001 D-39 ~ D-41 · 처분 `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-v2/research-dispositions.md`(**OQ-018 처분 포함 — SPEC 에 없는 건 이게 기준**) · 조사 리포트 3개(`/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-v2/research-r*-report.md`)

## 할 일
- `charts/interpret-pwa`: back PVC(§9.6 — local-path · `lima-worker-1` nodeSelector · 1Gi · keep — `charts/cc-prototype` back-pvc 선례 그대로) · back 에 마운트 · `INTERPRET_RECORD_DIR` env(configmap) · fsGroup(back uid 10001)
- `docs/interpret-pwa-deploy.md`: PVC · 기록 꺼내기(kubectl cp 명령 · 날짜 파일) · 7일 삭제
- 검증 helm lint · template(가짜 태그) · kubeconform · 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-v2/wp17-infra-report.md`

## 완료 보고 (두 명령 · 코디 handle 은 보고 직전 `orca terminal list --json` 에서 제목에 'Interpretation PWA')
`orca orchestration send --to <코디> --from <너> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "infra 완료: WP17" --body "…"` + `orca terminal send --terminal <코디> --text "[worker_done] infra WP17 완료 — <한 줄>" --enter`
