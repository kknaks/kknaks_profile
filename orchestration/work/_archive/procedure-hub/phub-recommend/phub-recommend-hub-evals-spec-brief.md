# [planner] SPEC-006 · WORK-004 — hub-evals 실험 앱(원장 MCP vs 골드 MCP vs 골드 + Jev) · 로컬 프론트에서 질문 → 세 갈래 실행 · 측정

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/planner/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 산출 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/SPEC-006.md` · `WORK-004.md`.

## 정본(이것만 근거)
- 설계 초안 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-30-hub-evals/README.md`(세 케이스 · 속도 칸 · 품질 두 층 · 화면 와이어 · 기록 꼴 · 열린 것 O-1~O-9)
- 조사 `jev-research.md`(Jev = TypeSafe System One · MCP 없음 · Choice 255 한도 · confidence · SDK · Claude 로컬 MCP 는 SDK + MCP 클라이언트로)
- 결정표 `_RESUME.md` §2 — 특히 10-30 「원장도 MCP 로」 · 「hub-evals 결정(사용자 「응」)」 Q-1~Q-8 · 「최종 목표」 · 「hub-evals 는 골드 완성 뒤 · 레포 kknaks/clinic_chat 공개 · 데이터 · 키는 env」 · D-11
- 허브 `SPEC-005.md` §5(골드 도구 9 · 입출력) · §5-12(원장 도구 3) · 포트 `127.0.0.1:18005` · 골드 MCP `/procedure-hub/gold-mcp/mcp` · 원장 MCP `/procedure-hub/raw-mcp/mcp` · REST `/procedure-hub/gold`
- 품질 측정 `quality-eval-set.json`(나중 회귀용 참고만 — 실험은 사용자가 그때그때 입력)

## 목표(사용자)
사용자가 **로컬 프론트에서 질문을 입력**하면 case1(원장 MCP + Claude Sonnet) · case2(골드 MCP + Claude Sonnet) · case3(앱 서버: 허브 사전 → Jev Choice 슬롯 → 골드 도구 → Claude Sonnet) 이 **동시에** 돌고, 열마다 속도(ttft · total · 단계별 · LLM 왕복 · 토큰) · 답 스트리밍 · 도구 호출 / Jev 슬롯 / 허브 경로 · ① 단어 검사(원장 대조 결정론) · ② Opus 채점(항목별 통과/실패 · 근거 인용 · 가리기) · 사람 확인 표시 · 기록(jsonl)이 나온다.

## SPEC-006 에 담을 것
1. 범위 · 경계(실험 앱만 · 허브는 SPEC-005 · LLM 키는 env · 공개 레포라 데이터 · 키 · 환자 정보 금지)
2. 구성: 실험 서버(Python · Anthropic SDK + 공식 MCP Python SDK 클라이언트 · TypeSafe SDK) + 프론트(로컬 · 스택 추천과 이유) · 레포 `kknaks/clinic_chat` 구조
3. 세 케이스 흐름 · 같은 조건(모델 · 프롬프트 공통부 · thinking 끔 · 동시 시작) · case1 · 2 도구 루프 상한 · case3 단계(사전 검색 → Choice(255 넘으면 후보 줄이기) → confidence 0.3 미만 표시 → 골드 도구 경로 → Sonnet 1회)
4. 속도 측정 정의(ttft = 첫 텍스트 델타 등) · 기록 꼴(README §6 + 모델 id · 프롬프트 판 · 골드 빌드 해시 · Jev 버전 · 선택지 순서 seed)
5. 품질 두 층: ① 이름 뽑기 방법(추천 · 근거) → 정규화 → 원장 대조 · ② Opus 채점 항목 · 기준 자료(README O-3 — 추천과 이유) · 가리기 · 근거 인용 · 사람 확인 칸
6. 화면(README §5 와이어 그대로 + 질문 기록 목록)
7. README 열린 것 O-1~O-9 · Jev Q-1~Q-8 처리 표(결정된 것 · 추천 기본값 · 사용자 몫)
8. 사용자 실행 절차(키 넣는 env 파일 이름 · 허브 서버 · 실험 서버 · 프론트 기동 명령 · 첫 질문)
## WORK-004: Phase(레포 뼈대 → 케이스 1 · 2 → 케이스 3 → 측정 · 기록 → 품질 ① ② → 화면 → 로컬 E2E) · Phase 마다 완료 조건 · 실물 호출은 키가 있을 때(없으면 모의로 뼈대 시험 · 실물은 사용자 키 뒤)
- 허브 골드 서버가 아직 구현 중 — SPEC-005 도구 스키마를 계약으로 삼고, 실물 대조는 허브 완성 뒤
- 결정표에 없는 새 결정을 「정해진 것」으로 넣지 말 것 · 실명 · 키 금지

## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_d604db9d-e1da-4569-bef7-73441af2e8d8 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "planner 완료: SPEC-006 · WORK-004 hub-evals" --body "SPEC 절 N · Phase N · 사용자 몫 N"
orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb --text "[worker_done] planner 완료 — SPEC-006 · WORK-004 hub-evals. 상세는 인박스." --enter
```
