# [researcher] 실버 2단계(계열) 반영 — step2-research 결정대로 계열 원장 + 제품→계열 연결

너는 맥락이 없을 수 있다(같은 터미널이면 앞 판 조사 `step2-research` 를 네가 썼다). 아래부터 읽어라.

## 읽을 것
- 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`
- 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/_RESUME.md` §2 10-28 「2단계 계열 기준」 · 「2단계 계열 조사 반영」 두 행
- 조사 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step2-research.json` · `.md`(D01~D18 · rows 352)
- 1단계 정본(고정 · **수정 금지**) `step1-products.json` · 원천 질문 형식 참고 `step1-origin-questions.md`

## 결정 (사용자 10-28 「추천으로 가자」)
- **D01~D18 전부 step2-research 추천대로.** 단 하나 다르다: **D10 의 X2 카복시 → 새 계열 N2 를 세우지 않는다**(제품 행 0 — 5단계 카복시테라피에서 재검토). 트리필 프로는 「판단 필요」 유지
- 계열 = M1~M17 + N1 「지방분해 주사」 = **18계열**. 계열 밖 = 의약품 3행(D02) · 진단 장비 4행(D12) · 헤어셀(D16 추천 계열 밖)
- M8 정의 = 「레이저·IPL·LED(광)」(D04) · M15 하위 = 화학 박피 · 기계적 박리·클렌징 · 외용제 (+ D09 흡수 보조 기기)
- 이름(D17): 문헌 영문 이름의 한글 이름 · 국내 공식 출처가 있으면 그것 · 없으면 `name_status: "공식 출처 미확인"`. 상담 용어 · 원천 이름은 동의어
- 하위 계열(D18) 규칙대로 — 5 · 3 · 6단계로 넘기는 것은 `deferred_to` 표시만(그 단계 일을 하지 마라)
- 판단 필요 6행(알렉스필 · 이브타이탄 · 벨르업 · 더마큐어 · 트리필 프로 · 헤어셀): 계열은 추천이 있으면 그것(헤어셀 = 계열 밖) · 없으면 `family: null` + 원천 질문 1줄씩
- 결정에 없는 변경 금지 · 추정 금지

## 산출 — 결정론 스크립트로
- `step2-apply.py`(입력 고정: step1-products.json · step2-research.json · literature-evidence.json → 같은 입력이면 같은 출력)
- `step2-families.json` · `.md`:
  - `families[]` 18: id · 이름 · name_status · 정의 · 문헌 근거(PMID/DOI) · 동의어 · 하위 계열[] · deferred[]
  - `product_family[]` 352: ledger_id · 대표 이름 · family(주) · also_families[] · 하위 계열 · 근거 · step1 계열(전) · 판정(맞음/옮김/여러/계열 밖/판단 필요)
  - `out_of_family[]` · `open[]`
  - md 맨 위: 계열별 행 수 · 판정 셈(합 352) · 전후 바뀐 행 목록
- `step2-origin-questions.md` — 판단 필요 행 질문(1단계 파일은 건드리지 않음)
- 끝 조건: 352행 전부 판정 · family 비어 있는 행은 전부 open 에 사유와 함께

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_99ecdef9-59f9-4620-8a6b-cfdd39f0bc09 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 실버 2단계 반영" \
  --body "계열 18 / 행 셈 맞음·옮김·여러·계열밖·판단필요 / open N"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] researcher 완료 — 실버 2단계 반영. 상세는 인박스." --enter
```
