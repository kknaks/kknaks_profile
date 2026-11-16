# reviewer 코드 검수 r3 — e2e 수정분만

원 브리프(`ext-api-charty1-review-brief.md`) 제약 그대로(read-only · KOS 호출 0 · 사용자 포트 금지). 이번 대상은 **커밋 `1c3a340`**(= `git diff c4876bd 1c3a340`) 하나다. 지시 = `be-fix-e2e1-instructions.md` · `fix-e2e2-instructions.md`(backend 5차 절). 계약 = SPEC-008 0.4.6 · DEC-012 D-46 · D-47.

볼 것:
1. 시술권: 산 묶음만 먼저 고른 뒤 모양 검사 · `price` 객체에 `value` 없음 = 0 · `price` 없음 · 숫자 아닌 `value` = 502 그대로 · 공개 시술권을 쓰는 다른 경로(있으면) 무변경
2. 상담 메모: 앞뒤 공백 지운 빈 값 = 400 · KOS 호출 0 · `event_log` 0 · 오더 메모 빈 값 = 비움 그대로 · message 꼴이 기존 `body.<칸>: …` 관례와 같은지
3. 시험이 위를 실제로 고정하는지(지운 · 약하게 바꾼 단언 없는지 `git diff c4876bd 1c3a340 -- procedure/back/tests` 전수)
4. 회귀 — r1 · r2 에서 PASS 였던 자리

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2/orchestration/work/ext-api-charty1/review-code-r3.md` 1개 · 판정 맨 위. 완료 보고 원 브리프 §9 두 채널.
