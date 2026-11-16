# reviewer 코드 검수 r2 — ext-api-charty1

원 브리프(`ext-api-charty1-review-brief.md`) 제약 그대로(read-only · KOS 호출 0 · 사용자 포트 금지 · 결정하지 않음).

## 대상
같은 워크트리의 커밋 안 된 변경(지금 상태). backend 2차 지시 = `be-fix-r1-instructions.md` · SPEC-008 **0.4.4** · DEC-012 **D-45**.

## 볼 것
1. 네 r1(`review-code-r1.md`) W1 ~ W5 · Q1 ~ Q3 · 참고(명시 null)가 지시대로 고쳐졌는지 — 코드 · 시험을 직접 읽어 확인(backend 보고를 믿지 말 것)
2. W5 새 쿼리(`repo.py` `events_for_reservations` · `customers_in`) — `json_extract` 거르기가 지금 `event_log` payload 모양과 맞는지 · 예약 id 가 빈 집합일 때 · 매개변수 바인딩(문자열 조립 아님) · 직원 쪽 `events()` · `customers()` 무변경
3. W1 수정이 시도 예약 규칙(`BEGIN IMMEDIATE` 안 `await` 0 · KOS 전 커밋)을 깨지 않는지
4. r1 에서 PASS 였던 자리가 이번 수정으로 다시 깨지지 않았는지(회귀) · SPEC 0.4.4 와 코드가 맞는지
5. 시험은 필요한 파일만 돌려 봐도 된다(전체 751 passed 는 코디가 돌림)

## 산출물
`/Users/kknaks/orca/workspaces/kknaks_profile/cc-2/orchestration/work/ext-api-charty1/review-code-r2.md` 1개 — 맨 위 판정(PASS/WARN/FAIL) · r1 항목별 해결 표 · 새 지적 · 질문. 완료 보고는 원 브리프 §9 두 채널.
