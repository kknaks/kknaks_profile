# [planner] fix-9 — 결정 C25 · C26 · C27 (사진 삭제 실패 · 삭제 확인 창 · KOS 실패 토스트)

## 읽을 것
- 결정 파일: `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/reference/2026-11-24-day-picture/chart-photo-decisions.md`
  - **C25 · C26 · C27** — 사용자 결정. 글자도 사용자 승인됨
- 검수 리포트: `review-code-3-report.md`(같은 work 폴더) P2 · P3 · P6

## 할 것
SPEC-002 사진 절을 아래대로 고친다.
- **C25**: 가져오기 작업이 KOS 삭제를 다시 한다
  - 고칠 곳: 규칙 39 ⑤ · ⑪
  - 지금 열려 있는 OQ-94 를 닫는다
- **C26**: 화면 구성에 삭제 확인 창 요소를 넣는다
  - 글자와 버튼은 결정 파일 그대로
  - OQ-88 중 이 부분을 닫는다
- **C27**: 토스트 표에 「KOS 반영에 실패했습니다」를 넣는다

§4 · 10-decision · log 도 갱신한다.

## 작업 자리
- 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-chart-photo-spec`(커밋 `4d9214af` 위)
- 커밋하지 마라

## 검증
- lint `--strict` → `products/day` ERROR 0

## 보고
- `planner-fix-9-report.md`
- preamble 의 worker_done 두 채널
