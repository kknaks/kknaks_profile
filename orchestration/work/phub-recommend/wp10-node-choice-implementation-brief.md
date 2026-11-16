# WP-10 노드 묶음 Jev 선택·facet 페이지 종료 구현

## 정본·현 실패

- 앱 워크트리 `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals`의 미커밋 WORK-012/WP-8·9 코드를 이어서 수정한다. 정본 `orchestration/work/phub-recommend/SPEC-006.md` 0.3.12 §3-4-1-7, `WORK-012.md` WP-10 우선/검수 차단 해소. `reference/2026-10-30-hub-evals/build-out/wp9-jev-frontier-implementation-report.md`, `wp10-node-choice-review.md`, `wp10-node-choice-rereview.md`를 읽는다.
- WP-9 실물 Q002는 **245 Jev/461 Hub/73초 TTFT**, 7 unit 전수와 팔자 보톡스 고유 위험 누락으로 FAIL. 사용자의 흐름은 `노드→후보 1,2,3→Jev가 2,3 선택→두 노드 탐색→다음 후보→Jev가 종료`다. Jev를 각 page마다 호출하는 구현은 제거한다.

## 구현

1. 질문에 따라 허용된 **다음 graph node** 후보 묶음이 생길 때만 Jev에 짧은 state와 `action`, `pick_1..pick_k(k=min(4,후보 수))` Choice를 보낸다. 같은 후보 키+`none`, 슬롯 순서, 중복 첫 값, 미선택 후보 보존, >254+none 2단 묶음/원집합 대조, stop+pick 충돌의 거부→1회 재선택→`no_progress/incomplete`를 구현한다. build/typed edge/방향/방문 tuple 검증은 앱이 맡고, 관련성 판단은 Jev가 맡는다. 선택된 노드의 section/page를 읽는 동안 Jev graph-choice를 다시 부르지 않는다.
2. I-01 직접 역할 edge는 얕게 모두 검증하고, 후보 7 unit을 자동 필수로 등록하는 경로를 없앤다. 명시 target은 필수, Jev가 선택하거나 실제 답 계획에 들어간 unit만 답 갈래로 확정한다. 선택되지 않은 선택적 후보는 이유와 비전수 답 범위를 `justified_not_required`로 기록한다. 답 계획에 새 갈래가 들어가면 그 갈래의 위험/금기/고지를 다시 연다.
3. 선택 노드에서 현재 질문 facet의 직접 역할→명시 facet→주요 안전/조건/고지 순으로 **필요한 section 첫 page**를 연다. slim fact를 owner/section/flags/관계 scope로 후보화하고 관련 후보 ID만 `expand(fact_ids)` 원문 확인한다. 원문/source/owner/scope/의미 지원이 확인되면 그 facet의 뒤 page를 `not_required`로 취소한다. 미지원이고 `more>0`이면 같은 section 다음 page를 이어 읽으며 page마다 Jev를 호출하지 않는다. 의미가 불명확할 때만 짧은 후보 집합을 Jev가 한 번 평가할 수 있으나 원문·scope 검증을 대체할 수 없다. 부재는 허용 범위의 끝을 증명할 때만, 오류/시간/안전 공백은 `incomplete`다.
4. 공개 Gold에 해당 부위 주요 위험이 없으면 그 갈래를 안전 지원/부재로 처리하거나 추천 완료하지 않는다. Q002의 `botox_specific.risk` 문구/ID를 일반 코드·프롬프트에 넣지 않는다. Hub 투영이 필요한 정확한 공개 칸·관계·원천 경로를 보고한다. 기존 WP-8 답 보정과 수집 원장/인용 검증을 유지한다.

## 수용·경계

- fake Jev `2,3,none`/stop 충돌/중복·무효/옛 build/역방향/>254, 첫 page 지원 중지·page 7 유일 근거·cut/범위 불일치·필요 없는 full 조회, 네 역할 얕은 확인/7 unit 비전수, 명시 두 target·조건부 위험/고지·안전 공백, 참된 부재·장애, I-02~I-08 회귀. 전체 앱 suite·Ruff·diff check.
- 격리 Hub 18015 Q002 **한 문항만** 새 label로 실물 검증한다. 245 Jev/461 Hub/73초 WP-9와 290 Hub/12.5초 WP-8에 대해 호출/bytes/Claude 입력/TTFT와 최종 답 인용·안전·관련성을 판정한다. 실패면 추가 batch 없이 정확한 실패 단계만 보고한다.
- 사용자 Hub 18005·앱 18210·DB 포인터/컨테이너 비조작. 본인이 띄운 격리 Hub만 종료. Hub 코드·DB 수정, 커밋/푸시/PR, 50문항 금지. 결과를 `reference/2026-10-30-hub-evals/build-out/wp10-node-choice-implementation-report.md`에 쓰고 Orca `worker_done` 보고.
