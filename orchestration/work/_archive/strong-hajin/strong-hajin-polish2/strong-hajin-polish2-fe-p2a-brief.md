# [frontend] WORK-009 Phase 2a-2 — 채팅 서랍 안 사람 행동 단추, 모든 상태 검정 계열

너는 앞서 이 워크트리를 조사하고 Phase 2b 를 한 **strong-hajin `frontend` 워커**다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/roles/strong-hajin/frontend/role.md` (+ rules 등) · `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish2/AGENTS.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish2` (Phase 2b 커밋 `c64cddf` 위)
⚠ backend 워커가 같은 워크트리 `backend/` 에서 Phase 1 중 — 너는 `frontend/` 만.
이번 판은 **2a-2 만**이다. 2a-1(수정 모달 저장)은 Phase 1 의 서버 계약이 나오면 따로 지시한다 — 지금 손대지 마라.

## 1. SSOT
- WP `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/para/projects/summer-star/strong-hajin/30-work/work-009-polish2.md` **Phase 2a-2** + 원칙 P-3·P-5
- SPEC: SPEC-002 v0.4.0 §2.9 「채팅 서랍 안의 색」 · §6 (`/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/para/projects/summer-star/strong-hajin/20-spec/`)
- 너의 조사 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/fe-survey-report.md` §3(원인 · 단추×상태 표)

## 2. 계약 (WP 2a-2 요약)
- 채팅 서랍(`.scax-drawer--chat`) 안 solid-primary 단추의 진행 중·disabled 가 hover 와 겹쳐도 **파랑이 되지 않는다** — disabled 모양은 `.action-task-card` 의 기존 처리(`ax.css:546`)와 같게 통일
- 같은 구조 **전부**: AxDraftCard 등록 · ActionProgressBatchCard · CommandConfirmationForm · ActionPreview 결과 명령 · grep 으로 나오는 그 밖의 채팅 안 solid-primary
- 채팅 안 outlined-neutral·text-neutral 의 disabled+hover 도 disabled 모양 유지
- 「근거 N개 더 보기」(`.scax-sources__more`)는 사람 행동 → 검정 계열 텍스트 단추
- 범위는 **채팅 서랍 안만** — DS 원본(`components.css`)은 고치지 않는다(DS-gaps 로 보고). 서랍 밖 창(수정 창·홈/칩 카드 창)은 앱 DS
- 포커스 링은 범위 밖

**쓰는 곳을 전부 센다** — 채팅 서랍 안에 그려지는 단추를 grep 으로 다시 세고 상태별 결과 표(조사 §3-2 형식)를 보고에 낸다.

## 3. allowed_paths
- `frontend/src/`

## 4. 하지 말 것
- 커밋·push 금지 · 서버·프론트 띄우지 마라 · 사용자 포트 금지 · 새 모양 금지

## 5. 검증
- 직렬 vitest · tsc · build. 기준선 5 실패 그대로
- 새 테스트: 가능한 범위의 CSS 규칙 단언(선택자·명시도) 또는 렌더 클래스 단언

## 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**
```bash
orca orchestration send \
  --to term_b2ea0fd5-1473-4b83-9a04-dcf769fbedba --from term_82fc2322-7b14-4d60-90ee-efe1c243fd31 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "frontend 완료: WORK-009 Phase 2a-2" \
  --body "변경 파일 / 단추×상태 결과 표 / DS-gaps / 기준선 vs 결과 / 미결"
orca terminal send --terminal term_b2ea0fd5-1473-4b83-9a04-dcf769fbedba \
  --text "[worker_done] frontend 완료 — WORK-009 Phase 2a-2. 상세는 인박스." --enter
```
