# [backend] 전사 블록 경계 — 한 블록 최대 20초 · 150자 · 문장 끝에서 끊기(D51)

너는 **sc-ax backend 워커**다. 세션 그대로. 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`(HEAD 15d0cf5). `backend/` 만. 커밋·재기동 금지. **pytest 스위트 돌리지 마라(사용자 지시) — import 확인 + `build_blocks` 를 python -c 로 직접 눌러 본 결과만.**

## 사용자 결정 (2026-09-11, 실물 3회차 회의 8c63e19b)
재전사 원문에서 한 화자 51초가 한 블록(03:29~04:20)으로 묶여 칩 매핑이 이상해 보이고 근거 구간이 블록 경계에 걸쳐 두 줄이 켜진다. 블록 경계 규칙(`build_blocks`: 화자 변경 · 2초 침묵 · 300자)을 이렇게 바꾼다 — **실시간·재전사 공통**:
1. **한 블록 최대 20초**(end_ms − at_ms ≤ 20000). 넘기면 끊는다.
2. 글자 상한 300 → **150자**.
3. 끊을 자리는 **문장 끝(. ? ! 및 한국어 종결 뒤 공백)을 우선** — 상한에 닿기 전 마지막 문장 끝에서 끊고, 문장 끝이 없으면 상한에서 끊는다.
4. 화자 변경 · 2초 침묵 규칙은 그대로.

## 검증
`python -c` 로: 한 화자 51초 연속 토큰 → 20초 이하 블록 여러 개 · 문장 끝에서 끊김 · 150자 넘는 문장은 상한에서 끊김 · 화자 바뀜/2초 침묵은 그대로. 결과 수치를 보고에.

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_50bcf0cc-bae5-4c55-b23a-4143537dd1f3 \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "backend 완료: 블록 20초·150자·문장 끝(D51)" \
  --body "변경 파일 / 규칙 / 직접 확인 수치 / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] backend 완료 — D51. 상세는 인박스." --enter
```
