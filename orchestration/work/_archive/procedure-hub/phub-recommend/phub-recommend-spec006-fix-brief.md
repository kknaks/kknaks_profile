# [planner] SPEC-006 · WORK-004 검수 FAIL 1 · WARN 7 수정 + 결정 반영
너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/planner/role.md`. 작업 폴더 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/`.
(맥락 `review-spec006-report.md` · 앞 지시 `phub-recommend-hub-evals-spec-brief.md`)
- **F-1**: ① 정규화 = `semantic.json dictionary.resolve_rules.normalize` 그대로(답 · 원장 · 사전 같은 함수) · Phase 5 시험에 「한글 시작 + 영문 대문자」 원장 문자열
- **W-1**: Phase 1 시험 = 키 두 개 값 빈칸 · 사용자 홈 경로 없음 · **W-2**: case3 경로 = SPEC-005 §6-1 의도 → 도구 그대로(I-09 T3 sections · I-07 자기 쌍) · **W-4**: config 가 `.env` 를 읽음(pydantic-settings) — §8 명령 그대로 · **W-5**: Done 을 둘로(「모의 완료」 / 실물 E2E 1질문 뒤 「완료」 — 실물 없이 완료 금지) · **W-6**: 중증도 = 허브 vocab 에 없음 · 7단계 중증도 → 하위 고민(P2-2 · P2-3)으로 고민 슬롯에 덮임 한 줄 · **W-7**: 「T1 은 늘 부름(시술 슬롯 판단)」 근거 · stages 로 분리
- **코디 판단 W-3**: ② Opus 기준 자료의 원장 도구 = **앱 안 로컬 구현(같은 R1 ~ R3 계약 · 로컬 원장 파일)** — ① 과 같이 채점이 실험 대상 서버에 기대지 않게. R-10 문구 고침
- **R-1 ~ R-10 = 사용자 승인(10-30)** — §7-3 을 「결정됨」으로 · U-1 · U-2 = 사용자 완료(키 받음 · 키는 워크트리 `.env` 에 사용자가 직접)
- 레포 세팅 사실 반영: canonical `/Users/kknaks/git/clinic_chat` · 워크트리 `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals`(브랜치 kknaksss/hub-evals · main 240c321 — README · .gitignore · .env.example 이미 있음) · §8 경로를 이것으로
- **실험 기록 저장 위치 = 열린 것으로 둠**(사용자 답 대기: (가) runs/ 레포 폴더 · 커밋 안 함 — 지금 .gitignore / (나) 레포에 커밋) — §7 에 한 줄
- 머리에 「검수 반영 2026-10-30(F-1 · W-1~W-7)」 한 줄
## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_cdc0e84b-15b5-44fc-bb48-3325858e4452 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "planner 완료: SPEC-006 검수 수정" --body "FAIL N/1 · WARN N/7 · 열린 것 N"
orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb --text "[worker_done] planner 완료 — SPEC-006 검수 수정. 상세는 인박스." --enter
```
