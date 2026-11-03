# WP-9 Jev 동적 frontier·종료 구현

## 정본·대상

- 앱 워크트리 `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals`의 현재 미커밋 WORK-012 구현을 이어서 수정한다. 정본은 프로필 `orchestration/work/phub-recommend/SPEC-006.md` 0.3.11 §3-4-1-6과 `WORK-012.md` WP-9/Choice 구현 계약이다. 읽기 근거: `reference/2026-10-30-hub-evals/build-out/wp8-answer-gate-repair-report.md`, `wp9-jev-frontier-review.md`, `wp9-jev-frontier-rereview.md`.
- 사용자 요구: 질문과 다음 후보가 관련 있는지, 더 탐색할지 종료할지를 **Jev가 매 단계 판단**한다. depth는 동적이되 target×facet별 끝 조건이 있다. 현재 Q002는 `get_page`가 `more`마다 뒤 page를 자동 큐에 넣어 7 직접 후보/290 Hub 호출/133 side effects page/1.54MB를 읽는다.

## 구현

1. 현재 `coverage_run`의 직접 추천 관계·Jev 시작 선택·Gold build/owner/source/scope 검증·WP-8 답변 보정은 보존한다. 각 frontier에서 유효한 typed edge의 다음 node/section/page와 `stop_answer|stop_incomplete`를 후보화한다. 안전/명시 target은 우선 **후보로 제시**하되 무조건 전수 호출하지 않는다. Jev `system_one`의 실제 `Choice` 형식으로 `action`과 앱 발행 candidate key 하나를 선택하고, 실행·상태 갱신 뒤 다음 순회에 다시 묻는다. >255는 기존 2단 선택을 적용하고 원 후보 집합에 대조한다. 질문/의도/미지원 목표/이미 검증된 ID·범위/관계 source/`more`만 짧게 전송한다.
2. 각 target×facet을 `pending|supported|justified_not_required|absence_proved|incomplete`로 관리한다. 원문/source/scope 확인으로 지원되면 해당 뒤 page/무관한 이웃을 취소한다. 지원이 안 됐고 `more>0`이면 다음 page는 Jev 후보로 유지한다. `more` 자체는 자동 호출 명령이 아니다. 부재를 주장할 facet만 허용 범위의 마지막 page와 이웃/pair/global 완료를 증명한다. Jev stop은 명시 target/실제 답 갈래의 필수 효과·조건·안전·고지 검증을 우회하지 못한다. 미완료는 `정보 없음`으로 바꾸지 않는다.
3. Jev 관련성 선택을 키워드 규칙으로 대체하지 않는다. 앱은 후보 ID/build/관계 방향/owner/source/scope와 방문 tuple만 검증한다. 임의 ID·옛 build·다른 고민·역방향 edge·반복 선택/같은 tuple 재호출은 거부하며 재선택 또는 `no_progress/incomplete`로 닫는다. 지원된 선택지와 보류된 범위/제외 이유, Jev 선택과 확률, Hub 호출/bytes/TTFT를 trace에 남긴다. 고정 depth·바이트 상한으로 조용히 자르지 않는다.
4. Q002 네 직접 역할 edge는 얕게 모두 평가하되 7 unit 모든 section 전수 기본 동작을 없앤다. 효과/방식/기간/가격/안전 등 모든 facet에 같은 동적 종료를 적용한다. I-02~I-08 명시 대상/쌍 방향/관계·안전 계약을 깨지 않는다.

## 수용·경계

- fake Jev의 유효/무효 선택·>255 2단·빈 후보·오류·반복, 첫 page 지원 뒤 종료·page 2~7 유일 근거, cut 원문 미확인, 명시 두 target, 조건부 중대 위험·금기·고지, 진짜 부재 vs 미완료, 타 고민/부위/방향/옛 build를 직접 회귀한다. 전체 앱 suite·Ruff·diff check.
- 격리 Hub 18015에서 **Q002 한 문항만** 새 label로 실행한다. Q002 290 Hub 호출/1.54MB·Claude 입력 132KB/TTFT 12.5초 기준과 호출/bytes/지연을 비교하고, 네 역할/적용 범위/핵심 안전/인용·관련성의 최종 답을 함께 판정한다. 감소량은 실측만 말한다. 실패 시 반복 batch 없이 정확한 단계와 필요한 계약을 보고한다.
- 사용자 Hub 18005·앱 18210·DB 포인터/컨테이너 비조작. 본인이 띄운 격리 Hub만 종료. Hub 코드·DB 변경, 커밋/푸시/PR, 50문항 금지. 결과를 `reference/2026-10-30-hub-evals/build-out/wp9-jev-frontier-implementation-report.md`에 쓰고 Orca `worker_done` 보고.
