# [frontend] F21 — 시안 · SPEC 에 없는 화면 문구 걷기(전수)

너는 #231 frontend 워커다. 같은 워크트리 · 커밋 금지 · 백엔드 로직 금지(backend 가 권한 작업 중).
사용자: 「이런 문구는 왜 넣는 거야 · 시안에 있어?」 — 시술 완료 탭 「시술 완료 고객이 없어요」는 시안에 없다(F15 와 같은 일).
1. `backend/day/templates/**` · `static/day.js` 의 **사용자에게 보이는 글자 전부**를 뽑아 표로: 문구 · 위치 · 근거(시안 `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/screen/시술현황_프로토타입 (1).html` 줄 / SPEC-001 · 002 줄 / 원천 결정 줄) · 근거 없음.
2. **근거 없는 문구는 뺀다**(빈 상태는 비워 둠). 단 dev 견본(`/dev/kit`) 설명 글은 제외. 빼면 의미가 사라지는 자리(버튼 이름 · 오류 토스트 등)에 근거가 없으면 빼지 말고 리포트 「사용자 확인」으로.
3. 테스트 기대값 맞춤.
검증 `uv run pytest -m "not infra"` · ruff · 브라우저 /board 스크린샷 · compose down 금지 · api 만 재빌드. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/frontend-copy-audit-report.md`(문구 전수 표 포함). 완료는 preamble 의 worker_done 절차대로(둘 다).
