# [planner] fix-10 — e2e 1회차 결정 C28 ~ C32

**읽을 것**
- 결정 파일 `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/reference/2026-11-24-day-picture/chart-photo-decisions.md`
  - C28 ~ C32 — 사용자 결정이고, 글자도 승인됐다
- `e2e-1-feedback.md`(같은 work 폴더)

## 고칠 SPEC 자리
- **C28** — 사진 여러 장 올리기
  - 규칙 39 ② · API(`file` 여러 개) · 매트릭스
  - OQ-86 닫음
- **C29** — 토스트 표 · 규칙 31 거절 글자
  - OQ-41 · OQ-90 해당분 닫음
- **C30** — 사진 탭을 고를 때마다 다시 읽음 · 열려 있는 동안 10초마다 그 방문 가져오기
  - 규칙 39 ⑪ · U-16
  - 화면 요청은 작업을 넣기만 한다는 원칙은 그대로 둔다
- **C31** — KOS 에서 지운 사진은 DAY 소프트 삭제
  - 대상: KOS 목록에 없는 · ref 가 있는 DAY 행
  - OQ-96 닫음
- **C32** — [바로 시작] 집도의 = 시스템 계정(지금 규칙 34 그대로)
  - 의사차트 미리 고른 원장은 쓰지 않는다는 문장을 확인 · 보충한다

## 그 밖
- 차트 저장 전 KOS 읽기(C17)는 병원별 KOS 클라이언트를 재사용한다 — 저장마다 sign-in 하지 않는다. 규칙 31 KOS 읽기 문장에 한 줄 넣는다(e2e E3).
- 앞 문장은 취소선으로 남긴다.
- §4 · 10-decision · log 도 맞춘다.

## 작업 자리
- 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-chart-photo-spec` — 커밋 `1179b017` 위
- 커밋하지 마라

## 검증 · 보고
- lint `--strict` → `products/day` ERROR 0
- 보고 `planner-fix-10-report.md` + preamble worker_done 두 채널
