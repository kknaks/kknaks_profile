# [researcher] Jev(TypeSafe) · Claude SDK MCP 가능성 조사 (read-only · 키 호출 없음)

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 산출 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/jev-research.md` 하나.

## 왜(사용자 10-30)
상담 앱 구조 = Jev(빠름 · 슬롯) → 허브 도구 → Claude(답). hub-evals 실험(`reference/2026-10-30-hub-evals/README.md` — case1 원장 MCP + Claude · case2 골드 MCP + Claude · case3 골드 + Jev + Claude)을 하려면 **Jev 가 무엇이고 어떻게 쓰나 · MCP 를 쓸 수 있나 · Claude SDK 에 우리 MCP 를 쥐어 줄 수 있나**를 먼저 안다. 허브 MCP = 로컬 `127.0.0.1:18005` Streamable HTTP(stateless · JSON) — 골드 `/procedure-hub/gold-mcp/mcp` · 원장 `/procedure-hub/raw-mcp/mcp`(SPEC-005).
결정 근거: DEC-001 D-08(Jev = TypeSafe · 발화 → 고민 · 부위 · 중증도 · 조건 슬롯을 허브 노드 id 로 · 선택지는 허브 노드 목록 · 스키마 도구로 · 신뢰도 낮은 슬롯은 Claude 가 되묻기) · D-11(키는 사용자 · env 로만). 참고 링크 https://docs.typesafe.ai · https://simonwillison.net/2026/Sep/21/jev/

## 조사할 것(공식 문서 · 1차 출처 · 날짜 표기 · 추정은 「추정」 표시)
1. **Jev 정체**: 제공사 · 모델 · API 형태(엔드포인트 · SDK 언어 · 인증) · 가격 · 한도 · 지연(공식 수치 있으면)
2. **정해진 꼴 출력**: 스키마 · enum(허브 노드 id 수백~천 개 선택지 넣는 방법 · 한도) · 신뢰도 값 · 실패 처리
3. **도구 호출 · MCP**: Jev 가 tool calling · MCP 클라이언트를 지원하나 · 원격 MCP · 로컬 MCP 가능 여부. 안 되면 case3 은 「앱 서버가 Jev 슬롯으로 허브 호출」(README 설계 그대로)로 충분한가
4. **Claude 쪽**: Claude Agent SDK(Python/TS) · Messages API MCP connector 가 **로컬 Streamable HTTP MCP(127.0.0.1)** 를 붙일 수 있나(Messages API connector 는 공개 URL 필요한지 등) · 실험 레포에서 쓸 방식 추천 · 모델 id(Sonnet · Opus 최신)
5. **실험 레포 구성 추천**(`kknaks/clinic_chat` · 공개 레포 — 키 · 데이터 env · 커밋 금지): case 별 호출 흐름 · 속도 측정 지점(ttft · 단계별)
6. 막히는 것 · 사용자가 해야 할 것(키 발급 · 계정 등) — 표로
- **실제 API 호출 · 키 사용 금지**(문서만) · 실명 · 키 기록 금지

## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_6a96a0d1-e279-48e3-a5df-939a56092e57 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "researcher 완료: Jev · Claude SDK MCP 조사" --body "Jev MCP 가능 여부 · Claude SDK 로컬 MCP 가능 여부 · 막히는 것 N"
orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb --text "[worker_done] researcher 완료 — Jev · Claude SDK MCP 조사. 상세는 인박스." --enter
```
