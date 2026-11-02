# [backend] WORK-008 Phase 4 — 운영 회의 요약(종료 합성) 실패 고치기 (B-03)

너는 이 원인을 조사한 **strong-hajin `backend` 워커**다(`research-meeting-summary.md`). 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/roles/strong-hajin/backend/role.md` (+ rules 등).
워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish` (HEAD `4a89650`).
⚠ 같은 워크트리에 **미커밋 변경**이 있다: `frontend/`(3b) · `backend/` 의 `result_contracts.py`·`platform/actions.py`·`platform/action_center.py`·`tests/contract/test_action_center.py`·`docs/unified-operations-inventory.json`(채팅 created_at — 다른 backend 워커가 마무리 중). **그 파일들을 건드리지 마라.** 겹쳐야 하면 먼저 [질문]

## SSOT
- WP `…/kknaks_profile/스트롱하진-고도화/para/projects/summer-star/strong-hajin/30-work/work-008-polish.md` **Phase 4**
- 너의 조사 `…/orchestration/work/strong-hajin-polish/research-meeting-summary.md`

## 계약 (WP Phase 4 — 코디 결정)
1. 종료 합성이 이전 세션을 **이어 갈 수 없으면(resume 실패) 콜드스타트로 합성** — 저장된 전사 전문으로 새 세션을 열어 같은 결과물. 일반 재시도와 구분(세션 없음은 3번 재시도할 이유가 아니다). 콜드스타트 경로가 이미 있으면 재사용
2. 런타임 홈 경로를 **env 로 설정 가능**하게(기본값은 지금 그대로 — 배포 변경 없이 동작). 설정 자리는 기존 settings 관례대로
3. codex 실패 시 **stderr 요약을 로그에**(비밀값·토큰 마스킹, 길이 제한)
4. resume 를 쓰는 **다른 자리**(배치·대화 등)도 같은 「다른 파드에서 세션 없음」 위험이 있는지 grep 으로 전부 세고 보고. 고칠지는 보고 후 코디가 정한다(이번에는 종료 합성만)

## 하지 말 것
- 운영 접근 금지(이번엔 코드만). 커밋·push 금지. 서버 기동 금지(코디 스택 8001·5176·54329). 로컬 codex 실행 금지 — 테스트는 가짜 provider 로
- `~/strong-hajin-deploy-data/` 금지

## 검증
- 테스트: resume 실패 → 콜드스타트 성공 · 콜드스타트도 실패 → 지금처럼 실패 상태·사유 · env 설정 반영 · stderr 로그 마스킹
- `make test-unit` · `make test-contract`(기존 실패는 분리 보고) · architecture/inventory drift 는 diff 항목만

## 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**
```bash
orca orchestration send --to term_d7b4a334-2cbd-42ab-9eab-e64a7b255d44 --from <네 워커handle> --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "backend 완료: WORK-008 Phase 4 회의 요약" --body "변경 파일:줄 / 계약 1~4 / resume 쓰는 곳 전수 / 테스트 결과"
orca terminal send --terminal term_d7b4a334-2cbd-42ab-9eab-e64a7b255d44 --text "[worker_done] backend 완료 — Phase 4 회의 요약. 상세는 인박스." --enter
```
