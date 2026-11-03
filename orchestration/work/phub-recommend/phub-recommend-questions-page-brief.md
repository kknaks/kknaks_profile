# [tool_dev] 실버 1~7단계 질문 페이지 — 받는 사람별 3탭 · 추천값 미리 채움

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/tool_dev/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 만들 것: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/silver-questions.html` 하나(코디가 아티팩트로 게시) + 질문 원본 데이터 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/silver-questions.json`. 스타일 · 테마 토큰 · 폰트 · 저장 방식은 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-open.html` · `step1-decisions.html` 과 같게(window.claude.use('db') · 저장 상태 표시 · U+FFFD 이스케이프 · node 구문 검사 1회).

## 사용자 요구(10-29)
「8단계 조사 동안 내가 결정하면 되는 거 아니야」 — 지금까지 쌓인 질문을 **받는 사람별로** 모아 한 곳에서 답한다.

## 입력 (전부 읽고 질문을 뽑아라 · 같은 질문은 한 번만 — 나온 단계 표시)
- `step1-origin-questions.md` · `step2-origin-questions.md` · `step3-sites.json` doctor_questions · `step5-origin-questions.md` · `step6-origin-questions.md` · `step7-origin-questions.md` · `step7-concerns.json` correspondence(human_check true 88 — 추천 대응 · 근거)
- 결정표 `_RESUME.md` §2 — 이미 답이 정해진 것은 넣지 않는다

## 탭 3 (이 순서 · 탭마다 개수 · 진행률)
1. **사람 확인 게이트(사용자가 바로)** — 7단계 고민 대응 88: 「원천 표현 → 추천 대응 고민/목적」 한 줄 + 근거 접기 · 라디오 [맞음 / 아님(대응 고르기 또는 메모) / 모름]. 「추천대로 전부 맞음」 일괄 버튼(그 탭만 · 확인창)
2. **의료진** — 3단계 해부학 이름 후보(약 29 — 노드 · 일반인 이름 · 전문의 후보 한 · 영 · 근거) · 근거 약 동의어 · 위험 부위 대응 · 5단계 관절치료 · 7단계 보톡스 풀페이스 등: 추천값 + [맞음 / 고침(입력) / 모름]
3. **병원 · 원장님(원천)** — 1 · 2 · 5 · 6 · 7단계 원천 질문(제품 정체 · 허가 · 성분 · 구성 · 경로): 질문 한 줄 + [받은 답 입력] · 탭 전체 질문 **복사 버튼**(병원에 그대로 보낼 수 있게 · 번호 붙은 목록)
- 항목마다 id(단계 + 원 id) · 나온 곳 · 지금 상태(추천 제외 / 근거 약 / 확인 대기) 작게
- 맨 위: 「8단계 질문은 나중에 더해진다」 한 줄 · 탭별 개수
- 쉬운 말 · 항목은 한 줄 · 근거는 접기

## 답 저장
db 컬렉션 `answers` · 문서 id = 항목 id · {tab, choice, value, note, at} — 코디가 ArtifactData 로 읽는다. 항목 데이터는 페이지에 내장(json 과 같은 내용)

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_50fbb84c-9a28-4e5a-bbd2-b4351bc8594e \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "tool_dev 완료: 실버 질문 페이지" \
  --body "탭별 항목 수 / 중복 합침 N / 파일 크기 / 검사 결과"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] tool_dev 완료 — 실버 질문 페이지. 상세는 인박스." --enter
```
