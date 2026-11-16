# WP-10 F1 제목·도입문 우회 수정

- 앱 `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals` 현 미커밋 코드. `reference/2026-10-30-hub-evals/build-out/wp10-code-rereview.md` 잔여 F1 P1의 두 직접 재현과 fake 전체 경로 재현을 고친다. F2/F3는 PASS이므로 보존한다.
- `_nonmedical_bridge`에서 번호+짧은 한글, 임의 도입/종결 형식이라는 이유만으로 자유 문장을 비임상으로 승인하지 않는다. 위험 단어 blacklist를 확장하는 방식으로 해결하지 않는다. 고정된 순수 UI/안내문 allowlist 또는 검증된 payload의 이름을 그대로 표시하는 제한된 문법만 허용하고, 임의 의료 내용이 붙으면 인용/원문 검증으로 넘긴다. 이름·제목도 의미 주장을 추가할 수 없게 한다. 필요한 상담 질문은 내용이 순수 질문인지 좁게 검증하고 의료적 전제를 붙인 질문은 예외로 두지 않는다.
- `1. 임신 중에도 시술 가능`, `다음은 임신 중에도 시술 가능함을 설명드리겠습니다.`는 직접 validator·보정 후·fake 전체 walk 최종 출력 모두에서 거부/제거돼야 한다. 같은 형식의 효과/위험/금기/수치/비교 부재 등 다른 내용도 시험하고 고정 비임상 제목·순수 안내 양성을 유지한다. 지원 원문/안전/facet/공유 provenance/Noul 동적 종료 회귀 유지.
- 신규 음성 실패→수정 통과, 전체 suite/Ruff/diff PASS. provider/Hub/judge/실물 batch 호출 금지. 코드 재검수로 넘길 보고서 `reference/2026-10-30-hub-evals/build-out/wp10-heading-bypass-fix-report.md` 작성 후 Orca worker_done 보고. Hub/DB/포트·컨테이너·커밋/푸시/PR 변경 금지.
