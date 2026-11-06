# reviewer_doc 재검수 — SPEC-001 0.2.0 · WORK-001 (agency-settlement)

앞 판 리포트: `review-spec-007-report.md`(SPEC-007 0.1.0 · FAIL 1 · WARN 6 · NOTE 8). 그 뒤:
- planner 수정 1 · 2 · 3판(지시서 `planner-fix-1/2/3-instructions.md`)
- **사용자 정정: cc-prototype 기능 폴더가 아니라 별도 프로젝트 `agency-settlement`**. 문서가 옮겨지고 번호가 바뀌었다 — DEC-009→**DEC-001** · SPEC-007→**SPEC-001** · WORK-011→**WORK-001** · OQ-9nn→OQ-1nn · D9→D1
- 새 경로: `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/` (10-decision · 20-spec · 30-work · README)
- 코드 레포 `kknaksss/agency-settlement`(private · 루트 back/ · front/) · 역할 문서 `orchestration/roles/agency-settlement/reviewer/`

볼 것:
1. 앞 판 F-1 · W-1~W-6 · NOTE 2~5 가 **실제로** 닫혔나(줄 번호로)
2. 수정 2판(결제일 = ⑤ approvedDateTimeUtc · ① ↔ ⑤ 거래 잇기 · 같은 수단 · 같은 금액 두 건 구분)이 돈 · 날짜를 틀리게 만드는 길이 없나
3. 구조 이동 흔적: 옛 `sales/` · 기능 폴더 · cc-prototype 번호와 새 번호가 섞인 곳 · 깨진 링크 · frontmatter
4. DEC-001 D-01~D-09 대조(D-08 은 별도 프로젝트로 바뀜) · _RESUME §2 대조
5. public grep(실명 · 실제 금액 · 에이전시 이름 · 키 · 테넌트 id 0)

리포트: `orchestration/work/agency-settlement/review-spec-001-r2-report.md` 하나. 판정 PASS/WARN/FAIL. 운영 KOS 호출 · 파일 수정 금지. 끝나면 원 브리프 §9 두 채널(같은 task/dispatch · subject 「reviewer_doc 재검수 완료」).
