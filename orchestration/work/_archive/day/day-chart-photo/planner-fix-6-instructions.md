# [planner] fix-6 — KOS 사진 가져오기 (결정 C23)

## 읽을 것
- 결정 파일 `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/reference/2026-11-24-day-picture/chart-photo-decisions.md`
  - **C23**(새로 들어옴 · 사용자 결정 · 다시 열지 않음)
  - C23 은 C22-기본값 ③(목록 = DAY 행만)을 바꾼다
- 본: DAY-SPEC-006 「다른 날짜 최신화」 절(같은 워크트리 `products/day/20-spec/spec-006-reservation-board.md`)
  - 화면 요청은 중앙 작업을 넣기만 한다
  - (병원, 날짜) 잠금 · 조건 C1 ~ C3 · 폴링

## 작업 자리
- 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-chart-photo-spec`
- 네 fix-5 미커밋 변경 위에서 이어서 한다
- 커밋하지 마라

## 할 것
SPEC-002 사진 절(U-16 · 규칙 39 · API · 매트릭스)에 「사진 탭 열기 = KOS 사진 가져오기 작업 넣기」를 넣는다.
- **작업 내용**: KOS `get-visitor-images`(그 방문) 1회 → DAY 에 없는 것(external_ref 로 판정)은 원본을 받아 저장소에 저장 → `visit_photo` + `external_ref` 에 넣는다
- **토큰**: 직원 토큰(사진 읽기 · OQ-92 기본값과 같음). 작업 안에서는 시스템 계정인지 판단해 근거를 적는다
- **잠금**: 같은 방문은 한 번만 돈다
- **화면**: DAY 행만 읽는다. 작업이 끝나면 어떻게 다시 그리는지(폴링 · 다시 열기) 정한다
- **실패**: KOS 실패는 조용히 지금 DAY 목록을 보인다. 표시가 필요하면 OQ
- **KOS 에서 지워진 사진**: OQ + 기본값
- **10초 동기화**: 손대지 않는다

C22-기본값 ③ 문장은 취소선으로 남긴다. §4 · 10-decision · log 를 갱신한다.

## 검증 · 보고
- lint `--strict` → `products/day` ERROR 0
- 보고 `planner-fix-6-report.md`(같은 work 폴더) + preamble worker_done 두 채널
