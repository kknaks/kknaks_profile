# WP-10 Jev 후보의 의미 정보 누락 수정

## 대상·확인된 결함

- 앱 `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals` 현재 미커밋 코드. 정본 SPEC-006 0.3.13 §3-4-1-7/WORK-012 WP-10과 `para/resources/note/ai/llms.txt`. `wp10-noul-recovery-report.md`의 357 pass/Q002 후보 전부 0.50~0.62 보류가 근거다.
- 코디가 직접 `coverage_run` options 구성을 읽었다. `description=f"{node} · {edge or origin} · build..."`라 Jev에 실제 후보 이름·역할·추천 근거가 없다. `_frontier_choice` state도 node ID/edge/description만 보내며 사람이 의미를 알 수 없다. 이는 새 설계 문제가 아니라 기존 계약의 **의미 정보 전달 누락**이다.

## 수정

1. public_cards/peek/검증된 neighbor/recommend 응답에서 실제 노드 이름, 종류, 질문 anchor 이름, 직접 관계의 의미, 역할 원문과 source/scope를 얻어 후보 state에 넣는다. 필요한 직접 role ID만 원문 조회하고 7 unit 모든 section을 읽지 않는다. ID/build는 코드의 검증에 쓰되 Jev 설명을 대체하지 않는다. 질문 instructions는 구조화 state의 해당 후보 경로를 정확히 가리킨다. `answer_ready`에도 현재 검증된 사실의 짧은 내용과 미지원 항목을 전달한다.
2. 전 후보가 불확실하다고 즉시 끝내지 않는다. 검증된 직접 관계의 짧은 역할/이름 근거를 추가해 **달라진 state로 한 번** 재평가한다. 반복 동일 요청/임계값 인하/강제 선택으로 우회하지 않는다. 계속 불확실하면 범위 보류를 유지한다. 명시 target/안전·부재 hard gate, 노드 Noul 배치와 facet page 종료는 유지한다.
3. fixture에서 실제 Jev 요청 state에 의미 이름·역할·출처가 존재하는지 확인하고 내부 ID만 있는 후보는 평가 성공으로 처리하지 않는 회귀를 둔다. Noul 분포·선택/재판단·scope/안전·뒤 page 유일 근거 회귀 유지. 전체 suite/Ruff/diff check PASS 후에만 Q002 한 문항 실물 실행.

## 경계·보고

- 사용자 Hub 18005·앱 18210·DB/컨테이너 비조작. 격리 18015 본인 프로세스만 종료. Hub 코드/DB 수정·커밋/푸시/PR·50문항 금지. Q002 단일 실물에서 Jev state 대표 예(비밀 제외), 후보별 Noul, 실제 답/인용·안전·관련성, 호출/bytes/TTFT를 보고한다. 실패 후 반복 batch 금지.
- 결과 `reference/2026-10-30-hub-evals/build-out/wp10-semantic-state-fix-report.md`, Orca worker_done 보고.
