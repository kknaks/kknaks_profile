# [planner] 마감 고침 21 — SPEC-006 마지막 결정 · SPEC-000 / SPEC-002 맞추기
너는 맥락이 없다(새 터미널). 먼저 읽어라: 이 폴더 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/` 의 `planner-fix-18-report.md` · `planner-fix-20` 관련(없으면 `review-doc-12-report.md`) · 결정 파일 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/reference/2026-11-23-reservation/reservation-board-decisions.md` 끝 R73 · R74 · R75 · 문서 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation-spec` 의 `AGENTS.md`(있으면).
할 일 (사용자 「문서 다 정리 · 이번 작업 끝」):
1. SPEC-006: R73(같은 30분 행 안 순서 = 닫힘 뒤 · 동행 그룹 먼저(생긴 순 → 넣은 순) · 혼자(시작 → 생성) · 묶기 서버 검사 = 끈 · 놓은 카드 둘 다 같은 날 · 지난 날 아님) · R74(책갈피 탭 · 행 여백 — 뒤집힘) · R75(꼬리표 · 탭 · 행 여백 없앰 → 진한 primary 굵은 테두리만 · R72 꼬리표 뒤집음) 반영 · 낡은 문장 grep(「동행그룹」 꼬리표 · 걸쳐 얹음 · 18px).
2. **migration 번호**: 코드가 dev 최신 위로 rebase 되며 우리 migration 이 0018 ~ 0023 으로 밀린다(0018 reservation 권한 · 0019 거래 상태 · 0020 인덱스 · 0021 공지 권한 · 0022 동행 테이블 · 0023 동행 권한 — dev 0017_ext_catalog 뒤). SPEC 안 migration 번호 언급 전부 이 번호로.
3. **DAY-SPEC-000(데이터 모델)** 개정: `purchase_transaction.status` enum(+ spent · requested · failed) · 결제 수단 매핑 · `external_ref.entity_type = notice` · notice 칸 설명(KOS → DAY 동기화 있음) · 새 테이블 `companion_group` · `companion_member`(SPEC-006 R65 꼴 · §2 규칙) · 인덱스. SPEC-006 「다른 스펙과 다른 곳」에 적어 둔 사실을 SPEC-000 본문으로 옮기고 SPEC-006 쪽은 「SPEC-000 개정 ○ 에 반영」으로.
4. **DAY-SPEC-002(권한)** 개정: 권한 키 `reservation`(view) · `reservation.notice`(edit) · `reservation.companion`(edit) · 기본 모든 직무 · 데이터 migration. 같은 방식으로 SPEC-006 쪽 정리.
5. 10-decision · 20-spec · log 동기(30-work 는 Delivery 재결속 때 — 건드리지 마라). `python3 scripts/lint-pipeline.py --strict` 0 error. 커밋 안 함.
리포트 `planner-fix-21-report.md`(위 폴더) · preamble 의 worker_done.
