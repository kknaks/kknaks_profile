# [backend] 운영 회의 요약 실패 — 원인 조사 (read-only)

너는 **strong-hajin `backend` 워커**(조사)다. 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/roles/strong-hajin/backend/role.md`.
코드: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish` (읽기만).

## 증상 (사용자, 운영 https://ax.medisolveai.xyz , 2026-10-01)
- 회의 목록에 「제목 없는 회의 · 실패」가 둘(10-01 09:02, 14:15, 참석 1명). 상세: 「회의 내용은 저장됐지만 글로 옮기지 못했습니다. 다시 시도할 수 있습니다」 · 「회의록을 만들지 못했습니다 — 잠시 뒤 다시 시도해 주세요」. AI 회의록이 비어 있다
- 다른 회의(14:00 Ax KPI 설정 회의)는 취소 상태

## 할 일 — 원인을 증거로 가른다
1. 운영 로그·상태 (읽기만):
   - `ssh medi-me '/opt/homebrew/bin/kubectl -n strong-hajin-prod logs deploy/worker-meeting --tail=500'` · `deploy/back` · `deploy/worker-report` — 해당 회의 id·시각 근처 traceback
   - 필요하면 `kubectl -n strong-hajin-prod exec postgres-0 -- psql -U strong_hajin -d strong_hajin -c "<SELECT ...>"` 로 해당 회의·전사·작업(durable_jobs 등) 상태 **조회만**
   - 녹음 파일 존재: back 파드의 recordings 경로(`/mnt/mac/strong-hajin/recordings` hostPath)
2. 코드 경로: 「글로 옮기지 못했습니다」·「회의록을 만들지 못했습니다」 문구 → 그 상태가 서는 조건 → 운영에서 실제로 어디서 실패했나(STT Soniox · 전사 정착 · 회의록 생성 AI(codex) · 워커 큐)
3. 운영 프로파일·환경에서만 갈리는 조건(SONIOX 키·codex 인증·노드 codex 0.146 · hostPath 권한 · 네트워크) 대조. 참고: `…/kknaks_profile/스트롱하진-고도화/para/projects/summer-star/strong-hajin/70-runbook/runbook-002-production-deploy.md` §6

## 하지 말 것
- **운영에 쓰기 금지**: 재시작·재시도 버튼·DB UPDATE/DELETE·시크릿 변경·sync 금지. 조회만
- **비밀값을 출력하지 마라**(키·토큰·DB 접속 문자열). 실명·메일을 리포트에 쓰지 마라(공개 레포)
- `~/strong-hajin-deploy-data/` 접근 금지. 로컬에서 codex 실행 금지
- 코드 수정 금지

## 산출물
`/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/work/strong-hajin-polish/research-meeting-summary.md` — 0 한 줄 원인 · 1 증거(로그 발췌·조회 결과, 파일:줄) · 2 실패 경로 · 3 고칠 자리 후보(코드/인프라/운영 조치 구분, 설계는 쓰지 말고 위치만) · 4 조사 한계

## 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**
```bash
orca orchestration send --to term_d7b4a334-2cbd-42ab-9eab-e64a7b255d44 --from <네 워커handle> --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "조사 완료: 운영 회의 요약 실패" --body "한 줄 원인 / 증거 요약 / 고칠 자리 / 리포트 경로"
orca terminal send --terminal term_d7b4a334-2cbd-42ab-9eab-e64a7b255d44 --text "[worker_done] 회의 요약 실패 조사 완료. 리포트 research-meeting-summary.md" --enter
```
