# [backend] WORK-008 Phase 3b 보조 — 채팅 뷰 action 에 created_at

너는 Phase 3a 를 구현한 **strong-hajin `backend` 워커**다. 같은 워크트리(`/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish`, HEAD 위 3a 커밋 `4a89650`), 같은 규칙(`strong-hajin-polish-be-p3a-brief.md`). ⚠ frontend 워커가 `frontend/` 를 고치는 중 — `backend/` 만.

## 할 일 (이것만)
- 채팅 대화 조회(`GET /api/conversations/{id}`)의 각 action(`ActionPresenter` 채팅 뷰, `platform/actions.py` 근처)에 **`created_at`**(ISO 8601, `ActionItemRecord.created_at.isoformat()` — 3a 봉투와 같은 형식)을 더한다. 근거: SPEC-002 §2.9 「만든 지 며칠 — 만든 시각에서 센다」를 채팅 카드에서도 지키기 위해(검수 `review-fe-p3b-report.md` WARN-3)
- 그 뷰를 쓰는 다른 표면(MCP 대화 도구 등)에 같은 필드가 실리면 operation inventory drift 는 **그 항목만** 패치
- 테스트 1: 대화 조회의 action 에 created_at 이 ISO 로 실린다

## 하지 말 것 / 검증
- 커밋·push·서버 기동 금지(코디 스택 8001·5176·54329)
- `make test-unit` · `make test-contract`

## 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**
```bash
orca orchestration send \
  --to term_7941dbc9-8078-4818-8d3d-bfd5545cce31 --from <네 워커handle> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "backend 완료: WORK-008 Phase 3b 채팅 created_at" \
  --body "변경 파일:줄 / 필드 이름·형식 / 테스트 결과"
orca terminal send --terminal term_7941dbc9-8078-4818-8d3d-bfd5545cce31 \
  --text "[worker_done] backend 완료 — 채팅 created_at. 상세는 인박스." --enter
```
