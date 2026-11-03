# [researcher] 실버 2단계 open 40 — 행마다 해결 값 + 출처

`step2-families.md` §6 · `step2-families.json` `open[]` 40건을 **전부 해결 값으로** 가져온다. 「open 으로 남김」은 답이 아니다. 결정 `_RESUME.md` §2 10-28 「하위 계열도 주 · 보조로」 행(사용자).

## 해결 방식
1. **광원 · 재료 2종 행**(M8 광원 2종 14 · 아이콘 · 젠틀맥스 프로 플러스 · 바이리즌 등): 하위 계열 **주 1 + 보조**(`also_sub_families`). 주 = 허가 품목 매질 → 없으면 원천 설명 첫 매질. 허가 ↔ 원천이 다른 행(셀렉V · BBL 히어로)은 주 = 허가, 원천 쪽은 보조 + `conflict` 기록
2. **칸이 없던 것**: M4 하위에 「무세포동종진피(hADM)」(원천 M3 하위 이름 그대로) → hADM 6행 · M9 하위에 원천 이름 「SUPERB 초음파」 → 소프웨이브(정체 · 원리 출처 붙여)
3. **매질 표기 없는 레이저 5행**(피코코어 · 트루피코 · 브이빔 퍼펙타 · 아톰 등) · **M7 실 재질 9행**: 제조/수입사 공식 사양 · 허가 상세(emedi 원재료 · 모양 및 구조) · 브로슈어 · 보도에서 매질/재질을 찾아 값 + URL. MFDS MCP `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-mfds-mcp/` 사용
4. **계열 모름 5행**(알렉스필 · 이브타이탄 · 벨르업 · 더마큐어 · 트리필 프로): 다시 조사(허가 상세 · 제조사 · 피부과 홈페이지 · `/Users/kknaks/Downloads/data-anyang` read-only)해서 **추천 계열 + 근거**. 끝까지 출처가 없으면 「추천 값 + 근거 수준(약함) + 병원에 확인할 한 줄」 — 빈 값 금지
- 추정 금지 = 근거 없는 값 금지. 근거가 약하면 약하다고 적되 값은 낸다

## 산출
`step2-open-resolve.json` · `.md` 만(step2-apply.py · step2-families 는 아직 고치지 마라 — 사용자 확인 뒤 반영).
md 맨 위: 40행 표(이름 · 지금 · 해결 값 · 근거 한 줄 · 근거 수준 강/약) + 묶음 셈. 근거 약한 행만 따로 목록.

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_99ecdef9-59f9-4620-8a6b-cfdd39f0bc09 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 실버 2단계 open 40 해결안" \
  --body "해결 값 40/40 · 근거 강 N · 약 N"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] researcher 완료 — 실버 2단계 open 40 해결안. 상세는 인박스." --enter
```
