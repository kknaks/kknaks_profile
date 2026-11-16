# [researcher] 실버 8단계 — 충돌을 하나로 정하기(보수적 기본값 · 사용자 10-30)

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 작업 폴더 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/`. 8단계: `step8-decisions.json` · `step8-apply.py` · `step8-relations.json` · `.md` · 기록 `para/projects/company/procedure-hub/log/2026-10-29-silver-step8-relation.md`.

## 왜(사용자)
「충돌이 있으면 안 되는 거 아니야」 — 상담 앱에 서로 다른 말이 나가면 안 된다. 1~6단계 충돌은 이미 「정본 기준으로 정함 + 기록」인데 8단계만 D-13b(고르지 않고 보존)로 두 값이 살아 있다(순서 · 간격 19 · 확인 조건 등급 76 · 이소트레티노인 1 · review_status=conflict 엣지 165). **D-13b 를 바꾼다**: 안전 쪽으로 보수적으로 하나를 고르고, 진짜 반대만 의료진에게.

## 규칙(결정 파일 rules 에 문장으로 · 결정론 · 행별 결정 금지)
1. **조건이 다른 가짜 충돌**: 원문에 하위 조건(같은 날 / 별도 세션 · 박리 / 비박리 · 같은 부위 · 깊이 · 레이저 종류 …)이 적혀 있으면 by_sub_condition 으로 나눠 충돌 해제(같은 조건끼리만 비교)
2. **확인 조건 등급**: 기본값 = 더 엄격한 쪽(금기 > 주의 > 확인만) · 덜 엄격한 원문은 근거로 보관
3. **간격 숫자**: 기본값 = 더 긴 간격(하한 · 상한 모두 보수적으로) · 다른 원문 보관
4. **같은 날 가능 ↔ 불가**: 기본값 = 불가(조건 1로 안 나뉠 때)
5. **순서(먼저 하는 쪽)가 반대**: 조건 1로 안 나뉘면 **진짜 반대** → 기본값은 「순서 정보 없음(둘 다 가능 아님)」 + 간격은 규칙 3 + 의료진 질문 · 앱엔 하나만(순서 단정 안 함)
6. 이소트레티노인 대기: 규칙 3(더 긴 쪽)
- 각 엣지 · 조건에 `resolved`(기본값) · `resolution_rule`(1~6) · `alternatives[]`(원문 보관) · 「충돌」 표시는 **해제된 건 빼고 「보수적 선택」 표시**로 · 진짜 반대만 「의료진 확인」 표시
- reading_contract 갱신: 추천 · AI 는 resolved 만 읽는다
- 끝: 앱에 두 값이 나갈 수 있는 엣지 0(전수 검사 가드 · open) · 셈(가짜 충돌 해제 N · 보수 선택 N · 진짜 반대 → 의료진 N)

## 같이 할 것
- 8 재실행 · open 0 · cmp · 고정 시험(규칙 1~6 각 1건 · 결정 빼면 open) · relation-check · semantic-check errors 0 · `semantic-build.py` · `silver-graph-build.py` · `silver-questions-build.py` 재생성(질문 페이지의 충돌 질문은 「진짜 반대」만 남김 · id 유지) · md 셈
- 기록 `2026-10-29-silver-step8-relation.md` 끝에 「추가 — 충돌 하나로(10-30)」 절 · relation-check 스킬 문서 규칙 반영
- **다른 워커(허브 품질 측정 term_5306337a)가 step8 을 읽는 중** — 키 이름 지우지 말 것(더하기만)
- 원천 · DEC · 1~7단계 수정 금지 · 가상 문장 금지

## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_5f8dfd6d-73b8-45da-9d50-2f75df05b7f6 --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "researcher 완료: 8단계 충돌 하나로" --body "가짜 충돌 해제 N · 보수 선택 N · 진짜 반대 → 의료진 N / 두 값 나가는 엣지 0 / open N"
orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb --text "[worker_done] researcher 완료 — 8단계 충돌 하나로. 상세는 인박스." --enter
```
