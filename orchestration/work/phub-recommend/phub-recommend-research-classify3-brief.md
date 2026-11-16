# [researcher] 시술 원장 확정안 — 분류표 v3 (단위 시술 목록)

역할: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`.
사용자 지시(10-27): **오늘 골드까지 간다.** 이 산출물이 그래프 v2 빌드의 시술 원장 입력이다.

## 입력 (`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/`)
- `DEC-002.md` · `DEC-003.md` · `_RESUME.md` §2 10-27 행 전부(특히 OQ-317 용도별 = 계열 × 부위 · 부위 없는 시술 · 장비 이름 = 시술 동의어 · 계열 이름 = 공식 일반명(M1 보툴리눔 톡신) · 제품 이름 정규화 · 라인 제품)
- `taxonomy-classify-v2.json` + 2차 승인 답(아티팩트 db) — 코디가 내려받아 둔 1차 답 `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-kknaks-profile-----------/7f782343-8998-41d7-8392-00bd3c8596ee/scratchpad/classify-answers/answers/`
- 제품 쪽 판정은 **`product-master-draft-v3-frozen.json`**(고정본 — 4차가 원본을 고치는 중이니 원본을 읽지 마라) + `product-match-build.py` 규칙
- 원천 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/`

## 만들 것 — `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/procedure-master-v3.json` · `.md`
1. **계열(무엇을)** 목록: 시술군 17 → 공식 일반명 + 동의어(원장 이름 · 상담 용어)
2. **단위 시술** 목록: 무엇을 × 어디에(DEC-002 부위 트리 + 추가분) × 어떻게(원천 기법 표현 81종을 큰 기법으로 묶은 것 — 묶음표 포함, 원천 표현은 동의어). 각 단위 시술에 id · 이름(상담 용어, 예 「사각턱 보톡스」) · 동의어(원장 항목 이름 · 장비 이름) · 원천 항목 id
3. **원장 항목 521 → 어디로 갔나** 표: 단위 시술 / 제품(product-master id) / 장비 / 패키지(구성 단위 시술) / 목적(고민 엣지 후보) / 시술 아님
4. 판정이 1차 · 2차 사용자 답과 다르면 **사용자 답이 우선**. 아직 답 없는 question 63 은 각 질문의 첫 선택지를 임시값으로 적용하고 `provisional: true` 표시
5. md 맨 위: 계열 수 · 단위 시술 수 · 부위별/계열별 표 · 임시값 목록

- 추측 금지 — 원천에 없는 부위 · 기법을 만들지 않는다. 다른 파일 수정 금지

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 시술 원장 확정안 v3" \
  --body "결과 수치 / 산출물 / 미결"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] researcher 완료 — 시술 원장 확정안 v3. 상세는 인박스." --enter
```
