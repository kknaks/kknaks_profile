# [writer] SPEC-004 · WORK-002 수정 — 검수 FAIL 3 (실물 입력 기준) · 오늘 범위 축소

너는 SPEC-004 를 쓴 writer 다. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`.

## 읽을 것 (`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/`)
- `review-spec-004-report.md` — FAIL 3 · WARN 9 · 「오늘 범위 제안」
- **실물 입력**: `procedure-master-v3.json`(+ `.md` · `procedure-master-build.py`) · `product-master-draft.json`(v4) · `gate-answers/product-match.json` · `classify-v1.json` · `classify-v2.json` · `source-fix.json` — **실제 키 · 값으로** 계약을 다시 쓴다

## 할 일
1. **F-1** §3.1.2 를 procedure-master-v3 실물 구조로(ledger_map 행선지 11종 · X1~X6 계열 · 부위 해당없음/null/트리밖 처리 — dangling 은 error 가 아니라 warning + 노드 미생성 · approval 값 전부 정의)
2. **F-2** §3.1.3 를 product-match.json 실물로(items[] · status auto/unconfirmed/not_applicable/pending · new_devices[])
3. **F-3** 제조사 노드는 `manufacturers[].products[].link` 대신 **선택된 허가 후보의 company(허가 업체 = 수입/국내 업체) · manufacturer_original(제조원) 필드**에서 만든다(허가 key → 후보 행 조인). 오늘 범위에서 빼야 하면 빼고 OQ 로
4. **오늘 범위 축소**: 검수 제안대로 미룰 것은 SPEC 에 「2차」로 옮긴다(규격 ② · procedure_relation 단위 시술 해석 · treats ④ device 갈래 · expected 엣지/이슈 독립 재계산 등). 제조사 노드 + manufactured_by/licensed_to 는 3번이 단순하면 오늘 포함
5. **W-1 결정(코디 기본값)**: 미확인 · 원천 근거만 · 임시값도 노드/엣지로 넣되 상태를 달고, **골드 tool 기본 응답은 승인 · 자동만** — `include_unconfirmed=true` 일 때만 나머지를 함께. 승인 게이트 원칙(_RESUME 「승인된 것만 다음 단계」)과 맞춘다
6. W-2(공유 동의어 40 → 이름 해석이 임의 단위 시술로 감): 동의어가 여러 노드에 걸리면 **후보 전부 반환**(임의 선택 금지) · W-3 · W-4 · W-8 반영
7. WORK-002 Phase 를 축소 범위로 다시(오늘 약 5시간 기준)

## 산출물 · 제약
- `SPEC-004.md` · `WORK-002.md` 수정만. 변경 이력 한 줄

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: SPEC-004 검수 반영" \
  --body "F-1~3 처리 / 오늘 범위 · 2차로 미룬 것 / WARN"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] writer 완료 — SPEC-004 검수 반영. 상세는 인박스." --enter
```
