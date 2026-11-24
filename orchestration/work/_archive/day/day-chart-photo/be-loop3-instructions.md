# [backend] 3루프 — 코드 검수 4 · e2e 2회차 반영 (C33 · C34 · W3 · W5 · W6 · W7)

## 읽을 것
이 폴더 `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/work/day-chart-photo/` 에서:
- `review-code-4-report.md`
- `e2e-2-feedback.md`
- 결정 파일 C33 · C34
- SPEC 고침 `planner-fix-11-report.md`(mediness #960 최신)

## 할 것
- **C33**
  - `deploy/caddy/Caddyfile` 에서 사진 올리기 경로(`/board/visits/*/photos`, POST)만 `request_body max_size 100MiB`. dev · prod 둘 다.
  - 다른 경로는 6MiB 그대로 둔다.
  - 서버 쪽 전체 본문 상한도 100MiB 로 맞춘다.
  - `deploy/` 수정 허용 — 이 줄만.
- **C34** — `services/visit_photo_import.py` 의 `_remove_gone` 에 안전장치 두 개:
  - 매핑 실패가 하나라도 있으면 그 회차는 삭제 판정 안 함 — `emr/kos/photos.py` 가 실패 목록을 돌려주게
  - 목록이 비었는데 KOS 반영된 행이 있으면 판정 안 함
  - 테스트 포함
- **W3** — 빠진 장(형식 · 크기 · 저장소)을 응답 `message` 로 알린다. 글자가 SPEC 에 없으면 비우고 [질문].
- **W5** — KOS 에 이미 없다고 확인된 사진은 C25 재삭제를 다시 하지 않는다. ref 정리.
- **W6** — 캐시 어댑터 동시 첫 생성 · 교체 경합을 정리한다.
- **W7** — 서버 쪽에서 필요한 것만 한다(지운 행은 목록에서 확실히 제외).

## 하지 마라
- 템플릿 · JS (frontend 몫)
- 커밋

## 검증
- `scripts/test.sh -q backend/tests/architecture backend/tests/day/board`
- ruff

## 보고
- `be-loop3-report.md`
- preamble worker_done 두 채널
