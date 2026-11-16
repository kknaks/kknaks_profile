# [infra] 앱 WORK-009 — WP-INFRA 사진 볼륨

너는 **cc-prototype `infra` 워커**다. **앞 판 맥락이 없다.** 먼저 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/infra/role.md`(+ 같은 폴더 rules · skills · tools · workflow)를 읽어라.

작업 워크트리: infra `/Users/kknaks/orca/workspaces/k8s_infra_mac/overall-board`(지금 브랜치는 머지된 옛 것 — **`origin/main` 에서 새 브랜치 `kknaksss/cc-prototype-app-photo`** 를 만들어라) · 코드 `/Users/kknaks/orca/workspaces/cc-prototype/overall-board` 의 `procedure/compose*.yml` · `procedure/.env.example` 만.

## 계약 (SSOT)
- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/20-spec/spec-004-procedure-app.md` **0.4.1** · `10-decision/decision-007-app-v2.md` · `30-work/work-009-app-v2.md`(내 WP 줄 · 병렬 · 주의)
- 웹 규칙: `20-spec/spec-005-reservation-board.md` 0.4.0 · `spec-003-procedure-board.md` 0.6.0 · KOS 근거 `orchestration/work/overall-board/app-kos-report.md` · `app-wp-kos-report.md`
- 결정: `orchestration/work/overall-board/_RESUME.md` §2 10-27 앱 줄 — **E2E 는 먼저 iPhone 시뮬레이터**
- 코드: `/Users/kknaks/orca/workspaces/cc-prototype/overall-board` branch **`kknaksss/overall-board-2`**(최신 `95c64bc`)

## 할 일 — WORK-009 WP-INFRA 줄
- back 파드에 사진용 PVC(작게 · 백업 없음) 마운트 · env `PROC_PHOTO_DIR` · 상담사 env Secret **예시 이름**(`CCC_COUNSELOR_*` — 값 금지)
- **암호화(U2)**: 이 클러스터(Mac Studio · Lima + kubeadm)의 스토리지 클래스가 볼륨 암호화를 지원하는지 확인 → 되면 켜고 · 안 되면 끄고 보고서에 근거(사용자 결정 「안 되면 없음 + 법적 검토 주석」)
- 주의: 최근 커밋 「lima-worker-1(PVC 노드) CPU 예약 98%」(`99920a3`) — PVC 를 붙이면 back 이 그 노드로 가는지 · 자원 영향 확인
- 코드 레포: compose 에 이름 있는 볼륨 · `.env.example` 한 줄
- 검증: `docker compose config` · `kubectl apply --dry-run=client`(가능하면) · **클러스터에 apply · ArgoCD sync 금지**(코디 · 사용자가 머지 뒤)

## 금지
- 커밋 · push · PR 금지(코디) · 운영 Secret 값 · 키 금지 · 사용자 포트 금지
- 보고서 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/app-infra-report.md`

## 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** **커밋 · push · PR 금지**(코디가 한다).
- WP 하나 끝날 때마다 보고서에 절을 더하고 **아래 (2) 한 줄만** 보내 진행을 알린다. 전부 끝나면 (1) · (2) 둘 다.
```bash
# (1)
orca orchestration send --to term_678ac61d-2472-4a9b-ba73-61883337b957 --from term_fd0c40a0-8b01-4731-8bae-daaed24b1310 --type worker_done \
  --task-id <preamble 의 taskId> --dispatch-id <preamble 의 dispatchId> \
  --subject "infra 완료: <한 줄>" --body "보고서 경로 / 바뀐 파일 / 검증 수치 / 데모 흔적 / 미결"
# (2)
orca terminal send --terminal term_678ac61d-2472-4a9b-ba73-61883337b957 --text "[worker_done] infra — <WP · 한 줄>. 상세는 보고서." --enter
```
- 막히면: `orca terminal send --terminal term_678ac61d-2472-4a9b-ba73-61883337b957 --text "[질문] infra: <질문>" --enter`
