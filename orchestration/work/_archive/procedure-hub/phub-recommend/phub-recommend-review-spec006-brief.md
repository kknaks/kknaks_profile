# [reviewer] SPEC-006 · WORK-004(hub-evals 실험 앱) 검수 (read-only)
워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 산출 `orchestration/work/phub-recommend/review-spec006-report.md` · 맨 위 PASS/FAIL + 「open = N」.
- 기준: `reference/2026-10-30-hub-evals/README.md` · `jev-research.md` · `_RESUME.md` §2 10-30(원장도 MCP · hub-evals 결정 Q-1~Q-8 · Claude API 키 별도 · 최종 목표 · 공개 레포 · 데이터 · 키 env · 환자 정보 금지) · D-11 · `SPEC-005.md` §5 · §5-12(도구 · 경로 계약)
- 볼 것: ① 세 케이스가 **같은 조건**인가(모델 · 프롬프트 공통부 · thinking · 동시 시작 · 측정 지점) — case1 이 원장 MCP 인가 · case2 골드 MCP · case3 순서(허브 사전 → Jev → 골드 도구 → Sonnet) ② SPEC-005 도구 이름 · 입출력 · 경로가 그대로 맞나(허브 실물은 구현 중 — 문서 대조) ③ Jev 문서(jev-research) 와 맞나(Choice 255 · confidence · SDK · 모델 고정) · Claude 로컬 MCP 방식(Messages connector 아님) ④ 속도 정의 · 기록 꼴 · 품질 두 층(① 원장 대조 결정론 · ② 가리기 · 근거 인용 · 기준 자료) 공정성 ⑤ 공개 레포 안전(키 · 데이터 · 원장 파일 · 환자 정보 커밋 금지 · .env.example 만) ⑥ 결정표에 없는 것을 「정해진 것」으로 썼나(R-1~R-10 은 추천 기본값으로 분리됐나) ⑦ WORK-004 Phase 완료 조건 · 키 없을 때 모의 · 사용자 실행 절차가 실제로 돌 만한가
- 가상 문장 금지 · 지적은 문서 · 결정 근거로
## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_985b2783-a884-4f3f-8c78-49992113369e --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "reviewer 완료: SPEC-006 검수" --body "PASS|FAIL · FAIL N · WARN N · open N"
orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb --text "[worker_done] reviewer 완료 — SPEC-006 검수. 상세는 인박스." --enter
```
