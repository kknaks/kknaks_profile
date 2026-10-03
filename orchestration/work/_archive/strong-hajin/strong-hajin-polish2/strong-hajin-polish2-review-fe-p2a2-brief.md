# [reviewer] WORK-009 Phase 2a-2 코드 검수 — 채팅 서랍 단추 상태

앞 판 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/strong-hajin-polish2-review-fe-p2b-brief.md` 의 역할·판정·allowed_paths 규칙이 그대로다. 리포트는 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/review-fe-p2a2-report.md` 하나.

## 대상
코드 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish2` 의 **`frontend/` 미커밋 변경**: `frontend/src/styles/ax.css` · 새 `frontend/src/features/chat/ChatButtonStates.test.tsx` (Phase 2b 는 `c64cddf` 로 커밋됨 — 대상 아님. `backend/` 는 Phase 1 진행 중 — 대상 아님)

## 기준
- WP `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/para/projects/summer-star/strong-hajin/30-work/work-009-polish2.md` **Phase 2a-2** · SPEC-002 v0.4.0 §2.9 「채팅 서랍 안의 색」·§6
- 발주서 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/strong-hajin-polish2-fe-p2a-brief.md` · 조사 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/fe-survey-report.md` §3
- 워커 보고: 서랍 안 solid-primary·solid-danger·outlined-neutral·text-neutral 의 disabled(+hover) → SA/L/ID 회색 · 「근거 N개 더 보기」 INeu 밑줄 · ds/Modal 이 포털이 아니라 카드에서 띄운 창(거절 사유·첨부 고르기)에도 서랍 규칙이 닿음 · 수정 창은 body 포털이라 앱 DS · 새 테스트 7 · 직렬 6 실패(기준선 5 + Checklist 흔들림 1, 단독 3회 통과)
- 코디 판단: AI 답변 본문 근거 링크 `.scax-md__ref` 는 AI 내용의 링크 → 그대로 · 추천 칩 opacity · 명령 폼 네이티브 button 은 그대로

## 볼 것
1. 상태별로 **실제로 이기는 규칙**을 명시도·순서로 다시 계산 — 진행 중+hover 에서 파랑이 0 인지(solid-primary·danger·outlined·text 전부)
2. 덮어쓰기가 **서랍 밖으로 새지 않는지**(선택자 스코프) · 반대로 서랍 안인데 빠진 단추(전수 재계수)
3. 활성 상태 모양이 바뀌지 않았는지(회귀)
4. 테스트가 jsdom 에서 CSS 를 보지 못하는 한계를 어떻게 다루나 — 빈 단언·문자열 존재만 보는 단언인지
5. 사용자가 실물에서 만날 자리

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_b2ea0fd5-1473-4b83-9a04-dcf769fbedba --from term_f8b0a2d6-3e7b-41de-b8c1-2acef6635f48 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "reviewer 완료: WORK-009 Phase 2a-2 코드 검수 <PASS|WARN|FAIL>" \
  --body "판정 / FAIL·WARN(파일:줄) / 재계수 / 화면 확인 목록 / 리포트 경로"
orca terminal send --terminal term_b2ea0fd5-1473-4b83-9a04-dcf769fbedba \
  --text "[worker_done] reviewer 완료 — Phase 2a-2 코드 검수 <판정>. 리포트 review-fe-p2a2-report.md" --enter
```
