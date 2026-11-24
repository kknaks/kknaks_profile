# [reviewer] 검수 4 — 2루프(e2e 1회차 피드백) 코드

## 읽을 것
이 폴더 `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/work/day-chart-photo/` 에서:
- `e2e-1-feedback.md`
- `be-loop2-instructions.md` · `be-loop2-report.md`
- `fe-loop2-instructions.md` · `fe-loop2-fix-1-instructions.md`(+ 인박스 보고)

그 밖:
- 결정 파일 C28 ~ C32
- SPEC: mediness #960 `7c5820d5`

## 작업 자리
워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-chart-photo` — read-only.

## 볼 것

### E3 — `build_adapter` 호출처
- 전수 grep 으로 다 찾는다.
- 차트 저장 KOS 읽기가 캐시 어댑터를 쓰는지 본다.
- 프로세스 종료 때 닫히는지 본다.
- 토큰 만료 · 재로그인이 지금 동기화와 같은 방식인지 본다.

### C28 — 여러 장 올리기
- 장마다 실패가 갈라지는지 본다.
- KOS register 를 묶은 요청에서 일부만 실패하면 어떻게 되는지 본다.
- 메모리 · 크기 한도를 본다.

### C29 — 토스트 글자
- 글자가 결정 파일과 같은지 본다.
- 실제 화면에 뜨는지(템플릿 · JS 경로) 본다.

### C30 — 열린 탭 10초 동기화
- 탭을 닫거나 바꾸면 멈추는지 본다.
- 모달을 닫으면 멈추는지 본다.
- 올리기 · 삭제와 겹치는지 본다.
- 같은 방문의 작업이 잠금으로 겹치지 않는지 본다.
- 부하: 한 직원이 탭을 열면 10초에 KOS 몇 번인지 센다.

### C31 — KOS 에서 지운 사진 정리
- DAY 가 먼저 지운 행(C25)과 충돌하지 않는지 본다.
- KOS 목록 조회가 실패했을 때 전부 지우지 않는지 본다. **가장 위험하다.**

### 조용히 통과하는 자리 · e2e 2회차 체크리스트
- 조용히 통과하는 자리를 적는다.
- e2e 2회차 체크리스트를 이번 고침 중심으로 짧게 만든다.

### 관문 명령
- `scripts/test.sh -q backend/tests/architecture backend/tests/day`
- ruff
- npm check

## 보고
- 리포트 `review-code-4-report.md`
- 수정 · 커밋 금지
- 완료는 preamble worker_done 두 채널
