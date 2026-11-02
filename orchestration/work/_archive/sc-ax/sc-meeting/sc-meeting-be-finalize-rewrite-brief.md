# [backend] 종료 합성 = 재료(메모+AI 요약+전사)로 처음부터 새로 쓰기 · 사람 안건 보존 검사 제거 · 실패 사유 문구

너는 **sc-ax backend 워커**다. 세션 그대로. 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`(HEAD 504e1d8). `backend/` 만. 커밋 금지. 서버 재기동 금지.

## 사용자 결정(2026-09-11) — 통합 회의록의 뜻
종료 합성은 **사람 메모 트랙 + AI 요약 트랙 + 전사 전체를 재료로 삼아 회의록을 처음부터 새로 쓴다.** 안건 목록도 AI 가 새로 잡는다 — 사람이 예약 때 적은 안건은 재료의 하나일 뿐이고, AI 가 합치거나 새로 세워도 된다. 결과는 「누가 썼나」가 남지 않는 한 벌.

## 고칠 것
1. `finalize.py` 의 `ensure_human_agendas_survive`(사람 안건 id 완전 일치 검사) **제거**. 출력의 `agenda_id` 는 있으면 그 안건(사람·AI 무관)을 갱신, null·모르는 id 면 신설. 안건 출처는 사람 안건이 이어지면 원래 출처 유지, 새 것은 `ai`.
   - 실물 실패 예: 회의 3edd8f88 — 「사람 안건을 정확히 한 번씩 덮지 않았습니다: 기대 [] · 실제 [AI 안건 3]」 3회 실패 → failed.
2. 합성 프롬프트를 이 뜻으로: 「안건·줄·다음 할 일을 재료로 새로 쓴다. 사람 안건 제목은 참고하되 묶고 나눠도 된다」. 남는 검증 = 스키마 strict · evidence 가 실제 확정 블록 범위 안(밖이면 그 근거만 강등) · 이미 있는 업무면 후보 제외.
3. `failure_reason` 은 **사람 말 한 줄**(내부 id·리스트 노출 금지). 예: 「회의록을 만들지 못했습니다 — 출력 형식이 맞지 않았습니다」.
4. `POST /finalize` 로 failed 회의 재시도가 새 규칙으로 도는지(3edd8f88 은 코디가 실물 재시도).

## 검증
```
cd backend && uv run pytest -q tests/contract/test_meeting_finalize.py tests/architecture -m 'not integration'. 테스트: 안건 0 + AI 안건 3 → 성공 · 사람 안건이 AI 안건과 합쳐져도 성공 · failure_reason 에 uuid 없음.
```

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_50bcf0cc-bae5-4c55-b23a-4143537dd1f3 \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "backend 완료: 합성 재작성·검사 제거·사유 문구" \
  --body "변경 파일 / 검증 수치 / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] backend 완료 — 합성 재작성. 상세는 인박스." --enter
```
