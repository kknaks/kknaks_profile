# [reviewer] 검수 3 — WP② 시술전후사진 (backend be-photo-1 · frontend fe-photo-1)

## 읽을 것
이 폴더 `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/work/day-chart-photo/` 에서:
- 지시서: `be-photo-1-instructions.md` · `fe-photo-1-instructions.md`
- 리포트: `be-photo-1-report.md` · frontend 는 인박스 보고
- 계약: `contract-k3-header-note-1.md` 보충 3(K4)

그 밖:
- SPEC: `/Users/kknaks/orca/workspaces/mediness-mediness/day-chart-photo-spec/products/day/20-spec/` — 커밋 `4d9214af`
  - SPEC-002: U-16 · 규칙 39 · 「KOS 사진」 · API · 매트릭스
  - SPEC-000: `visit_photo`
- 결정: `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/reference/2026-11-24-day-picture/chart-photo-decisions.md`
  - C8 ~ C13 · C22 ~ C24
  - 키 `beforeAfter/`
- KOS 실물 모양: `…/reference/2026-11-24-day-picture/*.har` — 모양만

## 작업 자리
워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-chart-photo` — read-only.

## 볼 것

### 1. migration 0024
- SPEC-000 그대로인지
- 데이터 규칙: 소프트 삭제 · UTC · 업체 칸 0 · external_ref
- down

### 2. 올리기
- 순서: 저장소 → 커밋 → transaction 밖 KOS 7단계
- 직원 토큰
- 이름 매칭 실패
- 「KOS 미반영」 · kos-retry 가 같은 사진을 KOS 에 두 번 등록하지 않는지
- 형식 · 크기 한도
- 저장소가 꺼졌을 때

### 3. 삭제 · 파일 열기
- 소프트 삭제 + KOS 삭제 · 실패 처리
- 권한
- `no-store`
- 다른 방문 · 병원의 photo_id 로 열리지 않는지

### 4. C23 가져오기
- 화면 요청은 작업을 넣기만 하는지
- 잠금
- external_ref 로 중복을 막는지
- PNG / JPEG
- 받은 파일 검증
- KOS 에서 지워진 사진
- 같은 방문을 동시에 열 때

### 5. 화면
- 실패 자리 · `reread` · 미반영 표시
- 지어 넣은 글자 0
- 인라인 0

### 6. 조용히 통과하는 자리
테스트가 FakeKos 라 못 보는 것을 짚는다.

### 7. 실물 e2e 체크리스트
차트(WP①③ — `review-code-1-report.md` 목록) + 사진을 합친 **최종 e2e 목록**을 만든다.

### 8. 관문 명령 1회
- `scripts/test.sh -q backend/tests/day`
- ruff
- `npm run -s check`

## 보고
- 리포트 `review-code-3-report.md`
- 수정 · 커밋 금지
- 완료는 preamble 의 worker_done 두 채널로
