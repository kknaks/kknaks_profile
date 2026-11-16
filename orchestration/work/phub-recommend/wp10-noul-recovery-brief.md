# WP-10 공식 Noul 전환·회귀 복구

## 정본·현 상태

- 앱 `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals`의 미커밋 WORK-012/WP-8~10 구현을 이어서 수정한다. 정본은 프로필 `SPEC-006.md` 0.3.13 §3-4-1-7 마지막 primitive 정정과 `WORK-012.md` 0.3.13 WP-10 마지막 문단. 공식 가이드는 `para/resources/note/ai/llms.txt`와 그 안의 TypeSafe 원문 링크. 읽기 근거: `reference/2026-10-30-hub-evals/build-out/wp10-node-choice-implementation-report.md`, `wp10-typesafe-noul-review.md`.
- 현 WP-10 Q002는 첫 `stop_answer`에 선택 갈래 0/Claude 입력 0으로 FAIL. 뒤에 종료 게이트를 보수했지만 실물 미검증. 전체 suite 325 pass/30 fail. 복수 동일 Choice 슬롯은 공식 문서의 독립 질문 의미와 맞지 않는다.

## 구현과 선행 검증

1. 현재 `pick_1..pick_k` 복수 Choice를 제거한다. 다음 **그래프 노드 후보별** 관련성 Noul과 `answer_ready` Noul을 짧은 구조화 state와 함께 한 `system_one` 요청에 배치한다. 각 질문 instructions는 후보 ID가 아니라 state의 정확한 후보 경로·질문/미지원 facet을 가리킨다. `response.nouls[id].noul`을 원 후보 ID/build에 매핑해 여러 후보를 선택·불확실 보류한다. API 한도에서는 후보 묶음을 안정적으로 나누어 결과를 합치고 누락 묶음은 incomplete. 응답 확률/임계값/선택·보류 이유를 trace에 남긴다. Noul은 의료 효능 확률이 아니며 낮은 확률로 명시 target·필수 안전을 삭제하지 않는다. `answer_ready`는 앱의 지원/범위/안전/부재 검증을 통과하기 전엔 종료 명령이 아니다.
2. 선택된 노드 내부 facet/page는 Jev graph choice 없이 지원 근거 확인 시 뒤 page 종료, 미지원 시 관련 뒤 page 진행. slim에서 관련 후보 ID만 full 원문 조회한다. 의미가 불명확한 후보만 별도 Jev 판단을 사용하며 원문/source/scope 검증을 대체하지 않는다. Q002 직접 역할 네 edge는 얕게 보존, 7 unit 전수 기본 동작은 제거. 추천 갈래 0개인 I-01은 complete/lookup_complete/답변 준비가 될 수 없다. 선택·답 계획에 뒤늦게 추가된 unit의 필수 안전을 다시 연다. Gold의 부위 고유 위험이 공개되지 않으면 해당 갈래 추천을 안전 지원/부재로 통과시키지 않는다.
3. **실물 전 테스트 게이트:** 현 30개 실패를 원인별로 판정한다. 옛 Choice/page 전수 기대와 진짜 계약 위반을 분리하고, 후자는 로직을 고친다. fake Jev 0.1/0.9/0.8→후보 2·3 한 API 호출, 불확실/오류/묶음 누락, 첫 stop/무갈래, page 1 지원·page 2~7 유일 근거/cut·범위, 명시 두 target·조건부 안전·부재/장애, I-02~I-08을 검증한다. 전체 `uv run pytest -q`와 `uv run ruff check .`, `git diff --check`가 통과할 때까지 Q002 실물은 실행하지 않는다. 테스트 기대값을 기계적으로 바꾸어 실패를 숨기지 않는다. 해결할 수 없는 검증 실패가 남으면 코드/테스트 상태와 원인을 보고하고 종료한다.

## 실물·경계·보고

- 위 게이트가 모두 통과한 경우에만 격리 Hub 18015의 같은 Gold hash에서 Q002 case3 **한 문항**을 새 label로 실행한다. Jev/Hub 호출·bytes·Claude 입력/TTFT와 최종 답 역할 4개, 인용·관련성·의료 안전을 비교한다. 실패면 반복 batch 금지, 정확한 실패 단계 보고. 사용자 Hub 18005·앱 18210·DB 포인터/컨테이너 비조작. 본인이 띄운 격리 Hub만 종료.
- 앱 코드·직접 관련 테스트만 수정, Hub 코드·DB/커밋·푸시·PR/50문항 금지. 결과를 `reference/2026-10-30-hub-evals/build-out/wp10-noul-recovery-report.md`에 쓰고 Orca `worker_done` 보고.
