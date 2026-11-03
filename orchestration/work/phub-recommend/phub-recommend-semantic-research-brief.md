# [researcher] 시맨틱 정의 조사 — 실버 1~8단계 위에 노드 · 엣지 · 용어 · 사전 · 읽는 규칙 정본 초안 (read-only)

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 작업 폴더 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/`.
**읽기만 한다**(실버 json · 원천 · DEC · 기록 수정 금지). 산출 `semantic-research.json` · `semantic-research.md` 둘.

## 왜(사용자 10-29)
순서: 연결 구조 HTML(끝 · `silver-graph.html` · https://claude.ai/artifact/1dxj251H9c7BBzsv9PC37x) → **시맨틱 정의 확정(지금)** → 골드 규칙 → 스펙 → 적재 · 골드 · REST · MCP → E2E.
시맨틱 = 업무 용어 · 개체 사이 관계 · 계산(읽는) 기준 · 동의어와 실제 데이터 대응을 **한 정본**으로(정의 `para/resources/note/db/2026-09-10-data-medallion-overview.md`). 지금은 단계 파일마다 흩어져 있다. 골드 규칙은 이번 범위 아님(시맨틱이 골드에 넘길 「상속 규칙 정의」까지만).

## 입력
- 실버: `step1-products.json` ~ `step8-relations.json` 8개 · 각 `stepN-decisions.json` · 기록 `para/projects/company/procedure-hub/log/2026-10-2*-silver-step*.md`
- 연결 구조: `silver-graph-build.py` 가 뽑은 노드 종류 14 · 엣지 종류 32(이건 **페이지용 뽑기**라 정본 아님 — 실버 파일에서 다시 확인)
- 결정표 `_RESUME.md` §2 전부 · DEC-001 ~ 003 · SPEC-004(옛 · 참고만 · 대체될 것)

## 만들 것(정본 초안 — 항목마다 출처 칸 · 셈은 파일에서)
1. **노드 종류 목록**: id 규칙 · 이름(사이트 용어 · 내부 이름) · 뜻 한 줄 · 필수 속성 · 선택 속성 · 정본 파일 · 칸 경로 · 셈
2. **엣지 종류 목록**: 이름 · 뜻 · 시작 → 끝 · 방향성 · 속성(예: 관계 주장 칸 · interval) · 정본 파일 · 칸 경로 · 셈 · 「계열 단위(상속)」 여부. 페이지의 32종을 **뜻이 같은 것은 합치고 다른 것은 나눈** 추천(같은 「계열」 이름이 두 번 나오는 것 · 「출처」 3종 등)
3. **용어집**: 단위 시술 · 계열 · 하위 계열 · 기법 · 부위(일반인 · 전문의 이름) · 제품 · 패키지 · 추천 조합 · 고민 · 목적 · 확인 조건 · 피함 · 합병증 · **부작용** · 근거 · 충돌 · 조건부 · gap … — 각 단계 결정에서 온 정의 문장 + 출처
4. **동의어 · 이름 해석 사전 지도**: 지금 어느 파일 어느 칸에 있는지(3단계 부위 사전 · 5단계 동의어 · 7단계 고민 동의어 · 규칙 R12~R20 · 8단계 resolver alias …) · 겹침 · 충돌(같은 말이 다른 노드) 전수 · 한 사전으로 모을 때의 구조 추천
5. **읽는 규칙**: 8단계 reading_contract · 간격 낱말 사전 · by_sub_condition · gate_status · 표시(flags) 정의 — 노드 · 엣지 공통으로 쓸 표시 목록 하나로
6. **상속 규칙 정의**(골드에 넘길 것): 계열 → 단위 시술 · 하위 계열 · 기법 조건 · 부위 내림 · 끝점 묶음 — 지금 데이터가 어떤 칸으로 상속을 표시하는지
7. **결정 묶음**(추천 · 근거 · 셈) + **사용자 최종 판단 한 표**(진짜 사용자 몫만). 이미 알려진 것:
   - **부작용 ≠ 합병증**(사용자 10-29): 부작용(흔한 예상 반응 · 멍 · 부기)은 지금 「근거 문장」 119 안에 섞여 있음 → 단위 시술 · 제품 속성으로 꺼내는 추천 · 근거 문장 119 를 종류별(부작용 · 기전 · 효과 · 정확도 · 환자 문장 …)로 전수 분류해 셈
   - **합병증 gap 17계열**(complications.json 은 10계열만): gap 유지 / 문헌 조사로 채움 — 사용자 판단으로
   - **「끝점 묶음」 노드 44**(후보 여럿 · 전체): 정식 노드 종류 / 엣지 속성(후보 목록) 중 추천
   - **그림 밖**: 7단계 앵커 없는 고민 → 시술 원천 행 52 · 부위 노드 없는 단위 시술 31(「해당 없음」 · 「병변 단위」)
   - 실버 json 칸 이름 · id 규칙이 단계마다 다른 것(예: 7단계 `J10-피부결` · `목적:볼륨 회복(충전)` 같은 문자열 id)
- 추정 금지 · 지어낸 종류 금지 · **가상 문장 시험 금지(지금 데이터만)**

## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_bed89150-1ed2-4c29-8a92-044bf8ac6ede --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "researcher 완료: 시맨틱 정의 조사" --body "노드 종류 N · 엣지 종류 N(합침 전 N) · 용어 N · 사전 N곳 · 결정 묶음 N · 사용자 판단 N"
orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb --text "[worker_done] researcher 완료 — 시맨틱 정의 조사. 상세는 인박스." --enter
```
