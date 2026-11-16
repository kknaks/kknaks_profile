# reviewer_doc r2 — ext-api-charty1

너는 cc-prototype `reviewer_doc` 워커다. 원 브리프(`ext-api-charty1-review-doc-brief.md`)의 제약 · 판정 기준이 **그대로** 유효하다(read-only · KOS 호출 0 · 커밋 0 · 코드는 `git show origin/main:` · HAR 은 키 · 꼴만).

## 대상
DEC-012(D-01 ~ D-40) · DEC-010 D-12 고침 줄 · SPEC-008 **0.4.1** · WORK-014 · 세 README · work-index.

## 무엇을 보나
1. r1 리포트(`review-doc-r1.md`)의 F1 ~ F3 · W1 ~ W17 이 **실제로** 고쳐졌는지 — 고친 곳을 본문으로 확인(planner 고친 곳 표를 믿지 말 것)
2. 사용자 답 · 코디 기본값(`_RESUME.md` §2 의 2026-11-16 행 전부 · `spec-fix-r2-instructions.md` §1 · §2)이 DEC · SPEC · WORK 에 빠짐 · 뒤틀림 없이 들어갔는지. Q15 · Q16 답은 `_RESUME` §2 코디 기본값 행
3. 고치면서 **새로 생긴** 모순 · 조용히 통과하는 자리 — 특히 첫 상담 대기 저장 규칙(찾은 값만 굳힘 · 5분 간격 · 요청당 10 · 끝난 단계 뒤 1번 · 날짜 지나면 멈춤)이 D-16 의 두 조건(한 번 정해짐 · 건수 비례 안 함)을 지키는지, 열람 헤더가 기존 여섯 경로 계약을 건드리지 않는지, lookup 에 새 502 가 없는지
4. 기존 ext 6개 계약 · 직원 API 동작 무변경
5. public grep

## 산출물
리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2/orchestration/work/ext-api-charty1/review-doc-r2.md` — 맨 위 판정(PASS/FAIL) · r1 항목별 해결 표 · 새 지적 · 질문(결정하지 않고 모음).
완료 보고는 원 브리프의 두 채널 그대로.
