## 마감 — contract v2 · plan 승인 · 머지 · dev 배포

**결과 계약** contract_version 2 · baseline `4443a99a`(mediness#945 머지) · plan_digest `sha256:b39ede6a290592528dda459d19be6925b014ade38975f7de9081f16689c76b9b` — 담당자 kknaksss 승인(2026-11-17 · 로컬 E2E 2회 확인 뒤).

### 들어간 것
- F-1 귀가 대기 취소(⋮ · KOS change-flow-step 직전 단계) · F-2 정렬 탭 시술순/방별순(`sort=room`)
- F-3 「바로 시작 · N건」 — 집도의 없으면 시스템 계정을 KOS 집도의로 · E3 그 줄 원장 자리 「간호관리」
- F-5 줄마다 ⋮ 되돌리기 — 호출 취소(DAY 만 · 알림 없음) · 시작 취소 · 완료 취소
- F-4 웹 원장 호출 OS 알림(늘 띄움 · E5) · F-6 작성된 차트만 파란 아이콘 · E6 시술 이름 글자만 차트 + 호버 「차트 작성」
- F-7 원장 계정 본인 즉시 수락 · E2 의사 호출 팝오버 위쪽 잘림 고침
- migration 0 · 앱(Flutter) 코드 변경 0(스냅샷 `systemDoctor` 칸만 추가 · 앱은 무시)

### 근거
- Code PR CENTURION_DAY#255 머지 — dev `0c401726`
- Spec PR mediness#945 머지 — main `4443a99a`(SPEC-002 개정 ㉑ · ㉒ · SPEC-005 2026-11-17 개정 · SPEC-003)
- 검증: 백엔드 pytest 전체 1298 passed · 로컬 day-local 사용자 E2E 2회 · lint-pipeline --strict 0 error
- dev 배포: GitHub Actions `DAY dev` run 44028948837 성공

### 남은 것 (이 Issue 밖)
- prod 배포 — 사용자 판단(병원 마감 뒤 · migration 없음)
- 호출 취소 알림 · 앱 푸시 — 앱 업데이트 뒤 다음 스펙(SPEC-005 OQ-N14)
- KOS 로그인 기기 제한(`SignInLimitExceeded` 구분 · 시스템 계정 자리) — 별도 후속
- 토스트 글자 미정 3개 — `conflict` · `task_not_called` · `visit_not_home`

spec-sync closeout 은 제품 레포 Delivery 에서 돌지 않는 알려진 제약(mediness#749 — dashboard projection digest 없음)이라 이 댓글과 close 로 대신한다.
