# [reviewer_doc] review-doc-3 — WORK-002 SPEC 개정 검수

너는 day `reviewer_doc` 워커다. 역할 · 범위 · allowed_paths(read-only · 리포트 1개) · 검증 · 완료 보고는 같은 폴더 `day-app-re1-review-doc-brief.md` 를 그대로 따른다(먼저 그 브리프 전체를 읽어라 — 거기 「차트」 대상 문장은 이번 대상으로 바꿔 읽는다). 대상 = 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-re1-spec` 커밋 **`319dd82e..HEAD`** 의 `products/day/` 변경(WORK-001 판은 이미 검수 끝 — 보지 마라).

읽을 것(모두 `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/`):
- `_RESUME.md` §2 — 2026-11-25 **WORK-002 행 전부**(범위 · 아이패드 + 갤럭시 · Q7 / Q6 추천 · 문진 DAY DB 먼저 · 공용 코디 계정 · 읽기 전용 · 웹과 닮게). 계약 SoT
- `planner-2-instructions.md`(보충 1 포함) · `planner-2-report.md`
- `research-2-report.md` · `research-3-report.md`(§3.1 · §3.2 이식 표 · §5 고칠 절 · §7 확인 안 됨)

## 볼 것

1. **결정 대조**: §2 WORK-002 결정 하나하나가 본문 · API 계약 · 인수 조건에 들어갔나 · 뒤집히거나 빠진 것(특히 읽기 전용 — 앱 상세에 쓰기가 새어 들어갔나 · 기기 하나로만 · 문진 DAY 먼저 저장 → KOS · 실패 상태 · [다시 보내기] · 공용 코디 계정 판정 · 웹과 닮게)
2. **전수**: research-3 §5 표 11행 · §3.1 17행 · §3.2 6행 · research-2 S1 ~ S10 · Q1 ~ Q8 처분이 빠짐없이 있나
3. **발명**: 결정 · 원천(cc · DAY SPEC)에 없는 정책 · 화면 글자 · 권한 문구가 들어갔나(없으면 비우고 OQ 여야 함)
4. **모순**: SPEC 사이(003 ↔ 007 ↔ 006 ↔ 005 ↔ 000) · 앞 개정과 · WORK-001 차트 계약과 · 상태 이름 · 오류 코드 · 경로 이름 일치. 실시간 신호가 계정 단위 → 기기 하나로 가는 규칙이 SSE · 푸시 · 메우기 셋에서 맞물리나
5. **보안 · 공개 경로**: 문진 공개 API · 페이지가 cc 보안 규칙(토큰 헤더 · 수명 · 1회 · 속도 제한 · no-store · 개인정보 미리 채움)을 빠짐없이 끌어왔나 · 직원 인증을 비켜 가는 경로가 공개 페이지 말고 생겼나
6. migration 판단 근거 · OQ 처분이 「확인 안 됨」을 메우지 않았나
7. lint(`python3 scripts/lint-pipeline.py --strict` · day 범위)

리포트: `review-doc-3-report.md`(같은 폴더) — 판정 PASS / WARN / FAIL · 지적마다 파일:줄 + 근거 + 고칠 방향 · 사용자 확인이 필요한 것은 따로 묶음.

완료 보고: dispatch preamble 의 `worker_done`(`--report-path` 위 리포트) + 브리프 §9 (2) 직접 주입.
