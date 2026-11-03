# [researcher] 허브 데이터 품질 측정 1차 — 정답 세트 · 결정론 측정 (실버 · 시맨틱 수정 금지)

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 작업 폴더 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/`.

## 왜(사용자 10-30)
골드 · 스펙 · 구현 전에 **허브 데이터가 상담에 쓸 만큼 유효한지 숫자로** 본다. 앞서 사용자가 연결 구조 페이지에서 오연결(이중턱 → 겨드랑이 마이크로웨이브 등)을 직접 찾았다 — 이번엔 측정으로 먼저 잡는다. KOS 연결은 기록만(이번 범위 아님).

## 입력
- 실버 `step1` ~ `step8` json · 시맨틱 정본 `semantic.json`(사전 · id 대응 · 상속 9) · 골드 조사 `gold-research.md` · `.json`(의도 12 · 탐색 경로 11 · 골드 규칙 17 — **아직 결정 전 추천안**) · 결정표 `_RESUME.md` §2
- 상담 장면: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-30-chatry-sample/`(S3p-Scenario 11단계) · 원천 브론즈 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/`(정답 근거)

## 측정 4가지
1. **질문 세트 정답률**: 상담 질문 세트(샘플 11단계 + 골드 조사 의도 12 고르게 · 50~100문항 · 고민 × 부위 · 시술 설명 · 같이 · 순서 · 간격 · 확인 조건 · 부작용 · 회복). 문항마다 **정답 초안**(맞는 단위 시술 · 반드시 나와야 할 안전 정보 · 나오면 안 되는 것)을 **원천 브론즈 · 문헌 근거 칸으로** 적는다(근거 없는 정답 금지 · 근거 없으면 「정답 미정」). 골드 조사 탐색 경로를 지금 실버 · 시맨틱 위에 결정론 스크립트로 흉내 내 돌리고 비교 → 재현율 · 정밀도 · 안전 누락 · 문항별 틀린 이유
2. **말 → 노드 찾기**: 상담에서 쓰는 말 목록(샘플 대화 · 원천 사이트 화면 문구 · 시장가 · 원장 이름 · 흔한 별명 · 오타/띄어쓰기 변형)을 시맨틱 사전에 넣어 찾음 / 못 찾음 / 틀리게 찾음 / 후보 여럿 비율 · 못 찾은 말 목록
3. **엣지 표본 검수**: 엣지 종류 21 마다 무작위 표본(고정 시드 · 종류당 20 또는 전부)을 원천 근거와 대조 → 종류별 오류율 · 오류 꼴
4. **안전 누락**: 원천에 금기 · 간격 · 합병증 · 확인 조건이 있는데 실버에서 빠진 것(원천 → 실버 방향 전수 대조) · 시술 노드에 안전 정보가 하나도 안 닿는 단위 시술 셈

## 산출
- `quality-eval-set.json`(문항 · 정답 · 근거) · `quality-eval.py`(결정론 · 두 번 실행 cmp · LLM 없음) · `quality-report.md` · `.json`
- 리포트 맨 위: 4 측정 지표 한 표 · **원인별 묶음**(같은 원인은 규칙 하나로 고칠 수 있게 · 어느 단계 결정을 고치면 되는지) · 의료진에게 물을 것(정답이 갈리는 문항만)
- 고치는 건 하지 말 것(측정만) · 가상 문장 시험 금지(원천 · 샘플에 있는 말만 · 별명 · 오타 변형은 규칙으로 만든 것만 · 표시) · 실명 · 키 금지

## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_5306337a-ff90-459b-a3b1-5fd89884bc25 --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "researcher 완료: 허브 품질 측정 1차" --body "문항 N · 재현율 N · 정밀도 N · 안전 누락 N / 말 찾기 N% / 엣지 오류율 N% / 원인 묶음 N · 의료진 질문 N"
orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb --text "[worker_done] researcher 완료 — 허브 품질 측정 1차. 상세는 인박스." --enter
```
