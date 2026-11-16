# [writer] 스킬 설명서 최신화 4 · 품질 측정 스킬 새로 · 기록 2 (10-30 오후)

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/writer/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 기록 자리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/para/projects/company/procedure-hub/log/` · 스킬 자리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-skills-procedure-hub/`. **사용자 「로그도 잘 좀 써라」** — 아래 「기록 기준」을 지킬 것.

## 1. 스킬 설명서 최신화(스크립트는 이미 최신 · 설명서 · references 만 맞춤 — 스크립트를 읽고 실제 규칙대로)
- `procedure-hub-concern-check`: R28(구체 고민 CC) · R29(원천 부위 낱말) · R30(원천 계열 밖 금지) · R31(원천 제품 → 하위) · R32(층 표시 U-1 ②) · 언제 쓰나 · 끝 조건 · 흔한 실수
- `procedure-hub-semantic-check`: resolve_rules(사전 출처 F · 접두 규칙 G · 정규화 H 「쳐짐 → 처짐」 · 괄호 · 끝말 · 문서 = 코드 M)
- `procedure-hub-family-check`: 다파장 하위 규칙(원천 파장 낱말 → 보조 하위 · 엑셀V · 노블린 등 5)
- `procedure-hub-unit-check`: 부작용 원문 source_text(J) · 덮어쓰기 값(골드 빈틈 ①)
- 각 스킬 `scripts/` 를 실제로 한 번 돌려 errors 0 확인(설명서의 실행 명령이 맞는지)

## 2. 새 스킬 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-skills-procedure-hub/procedure-hub-quality-eval/`(SKILL.md · scripts(`quality-eval.py` 를 감싸거나 그대로 가리킴) · references — 앞 스킬과 같은 꼴)
- 언제: 실버 · 시맨틱이 바뀔 때마다 · 골드 E2E
- 하는 일: 측정 4(질문 세트 · 말 → 노드 · 엣지 표본 · 안전 누락) · 목표 6 판정(CC 슬롯 · CC 없음 두 값) · **문항 · 정답 · 채점 식이 안 바뀌었는지**(정답 하위처럼 규칙으로 계산되는 칸은 무엇이 바뀌었는지 보고) · 판끼리 비교(v1 · v2 · v3 보관)
- selftest: 틀린 값 넣어 잡히는지 · README 지도 한 줄

## 3. 기록 2
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/para/projects/company/procedure-hub/log/2026-10-30-quality-eval.md` — 허브 품질 측정 · 수정: 왜(사용자가 페이지에서 오연결을 직접 찾은 것 · 「허브 데이터 유효한지 측정 먼저」) · 측정 설계(4측정 · 정답은 원천 근거 · 목표 6) · 1차 결과와 원인 14 · 8단계 충돌 하나로(D-13b 바꿈)와 순서에 따라 갈리는 같은 날 값(O) · 수정 · CC 슬롯 판단 · 2차 · 남은 8문항 처리 · 3차 · 다파장 · 지표 1차 → 3차 표 · 남은 것
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/para/projects/company/procedure-hub/log/2026-10-30-gold-decisions.md` — 골드 규칙 판단: 골드가 무엇인지(카드 묶음 아님 · 규칙 적용 그래프 · 허브 고정 · 병원 연결 층은 앱) · 골드 조사 요약(G1~G17 · 의도 12 · 도구 9) · U-1 ② · 판단 ①~⑤ · D-01~D-14(D-08 정정) · U-2 · U-3 은 앱 단계로 · KOS 는 기록만 · hub-evals 는 골드 뒤 · 다음(SPEC-005)
- README 지도 두 줄

## 기록 기준(사용자 요구 — 지난 기록보다 잘)
- **처음 읽는 사람이 이해되게**: 각 절 첫 줄에 「무엇을 · 왜」 한 문장 · 용어는 처음 나올 때 한 줄 풀이(CC · R28 · gate · resolved …) · 내부 번호만 늘어놓지 말 것
- **전/후를 구체 예로**: 수치 표만이 아니라 같은 질문 · 엣지의 전 → 후 예 5~8개(이중턱 → 마이크로웨이브 · 다한증 → 이마 보톡스 · 보톡스 ↔ 레이저 같은 날 · 여드름 · 아그네스 CC · 엑셀V KTP …)
- **사람이 고친 것 · 틀린 것을 숨기지 말 것**: 사용자가 직접 찾은 오류 · 코디가 순서를 잘못 묶은 것(「빈틈 + 원인 한 번에」 → 「원인 먼저 · 숫자 확인 뒤 빈틈」) · 처음 설계가 틀린 것(W2 「후보 전부」 · 게이트 88 · D-13b 보존) — 무엇이 틀렸고 어떻게 고쳤나
- **결정마다 출처**: _RESUME §2 행 날짜 · 사용자 말 인용(짧게)
- **수치는 파일에서 다시 셈**(quality-report.json · 각 단계 json) · 추정 금지 · 실명 · 키 금지
- 다 쓰고 나서 스스로 한 번 읽고: 처음 보는 사람이 「왜 이렇게 했나」에 답할 수 있나 점검

## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_72b71d34-5e18-49d7-8c10-d9865ecaf5f2 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "writer 완료: 스킬 최신화 · 품질 스킬 · 기록 2" --body "스킬 갱신 N · 새 스킬 selftest N/N · 기록 경로"
orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb --text "[worker_done] writer 완료 — 스킬 최신화 · 품질 스킬 · 기록 2. 상세는 인박스." --enter
```
