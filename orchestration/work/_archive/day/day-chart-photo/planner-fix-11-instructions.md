# [planner] fix-11 — 결정 C33 · C34 + 검수 4 기본값

## 읽을 것
- 결정 파일 `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/reference/2026-11-24-day-picture/chart-photo-decisions.md`
  - **C33 · C34** — 사용자 결정
- 같은 work 폴더의 `review-code-4-report.md`(F1 · W1 ~ W7) · `e2e-2-feedback.md`

## 고칠 곳 — SPEC-002 사진 절 · 화면 구성
- **C33** — 본문 상한
  - 올리기 경로만 서버 앞단 본문 상한 100MiB
  - 넘으면 413 토스트
  - 배포 설정 한 줄을 「서버 앞단」으로 적는다(40-architecture 에 Caddy 절이 있으면 거기도)
- **C34** — C31 판정 안전장치 두 개
- **기본값(코디)** — 각각 「기본값(코디)」 표시
  - 10초 확인은 사진 목록만 다시 그린다. 올리기 칸은 유지하고, 고르기 · 보내기 중에는 건너뛴다
  - 모달이 열려 있으면 토스트를 모달과 같은 층에
  - 빠진 장(형식 · 크기 · 저장소)은 토스트로 알린다
  - 숨겨진 브라우저 탭에서는 10초 확인을 멈춘다
  - KOS 에 없다고 확인된 사진은 다시 지우지 않는다
  - 삭제와 확인 응답이 엇갈리면 지운 사진을 다시 그리지 않는다

## 작업 자리
- 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-chart-photo-spec`(커밋 `7c5820d5` 위)
- 커밋하지 마라

## 검증
- lint `--strict` → `products/day` ERROR 0

## 보고
- `planner-fix-11-report.md`
- preamble worker_done 두 채널
