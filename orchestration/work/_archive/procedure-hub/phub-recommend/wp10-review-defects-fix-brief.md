# WP-10 검수 F1~F3 수정

- 앱 `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals` 현 미커밋 코드. 정본 SPEC-006 0.3.13/WORK-012와 `reference/2026-10-30-hub-evals/build-out/wp10-code-review.md`의 재현을 읽고 세 결함을 고친다. 기존 Jev Noul/동적 page/공개 안전 증명은 유지한다.
- **F1 P1:** 인용 원문의 두 토큰 일치만으로 문장 의미를 승인하지 않는다. 무공백 `[[ID]].다음문장` 경계와 인용 문장 안의 부재 표현(없다/없어요/자료에 없다/비교 불가 등)을 scope별로 검사한다. 임상 주장 방향·부정/수치/조건을 근거와 대조하고 반대 주장/미지원 절을 거부한다. 단순 키워드 추가로 모든 의미 검증을 해결했다고 주장하지 않는다. 의미 판정이 필요하면 공식 TypeSafe citation-check 패턴(원문 존재·scope는 코드, 주장 지원/반대/미지원은 짧은 독립 판단 묶음)을 적용하거나 검증 가능한 원문 기반 축약 답으로 보류한다. 새 모델 검증 시 한 요청 배치·trace/비용·실패 보류를 유지한다. 리뷰의 세 재현은 모두 거부돼야 한다.
- **F2 P2:** `(id,owner)` 내용 중복 제거가 조회 unit 경로를 지우지 않게 수신·full 검증·적용 증명을 `(node,id,owner)` 또는 동등한 provenance 집합으로 보존한다. 최종 Claude 입력 내용만 중복 제거한다. U5-037/018과 U5-102/091이 공유 role/family 원문을 양쪽 순서로 받아도 각 unit의 지원 판정이 보존되고 타 anchor로 새지 않아야 한다. 의미 부위 불일치는 사실 부재와 구분한다.
- **F3 P2:** `_repair_uncited_clauses`의 팔자 하드코딩을 제거한다. 한계 문장은 실제 질문 부위/검증된 scope 불일치에서만 만들고 미인용 정상 role에 임의 한계를 붙이지 않는다. 눈가·이마 양성/부위 불일치 음성 회귀를 추가한다.
- 보고서 재현→실패 테스트→수정 통과를 확인하고 전체 suite/Ruff/diff PASS. 실제 Q002/provider/judge 호출은 이번 작업에서 하지 않는다. 저장 답/fixture 오프라인 재생으로만 검증해 코드 재검수에 넘긴다. 테스트를 약화해 통과시키지 않는다.
- 앱·관련 테스트만 편집. Hub/DB/사용자 포트·컨테이너 변경, 커밋/푸시/PR 금지. 결과를 `reference/2026-10-30-hub-evals/build-out/wp10-review-defects-fix-report.md`에 쓰고 Orca worker_done 보고.
