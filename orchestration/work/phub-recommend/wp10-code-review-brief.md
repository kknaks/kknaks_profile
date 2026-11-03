# WP-10 구현 코드 검수

- 앱 `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals` 현 미커밋 코드의 WP-10 Jev Noul state·동적 facet 종료·안전 적용 증명·지원 갈래 부분 답을 읽기 전용 검수한다. 정본 SPEC-006 0.3.13/WORK-012 WP-10. `reference/2026-10-30-hub-evals/build-out/wp10-safety-state-fix-report.md`, 저장 Q002 result/offline replay, `tests/fixtures/wp10_safety_chain.json`과 직접 테스트가 근거다.
- 전체 368 tests 보고, 코디 직접 안전 관련 16 tests PASS. 단일 실물은 필러만 생성/4 judge PASS, 133 Hub/35KB Claude/8.3s TTFT. 후속 parser/부분 답 보강은 최종 코드 실물 미검증이다. 여섯 갈래는 blocked다.
- 중대 결함 중심으로 PASS/WARN/FAIL: owner/source/scope/조건의 잘못된 승격·부재 오판, 같은 unit 관계 공유가 타 anchor로 새는지, Jev Noul 선택/종료/뒤 page 유일 근거, blocked 갈래 의료 주장 누출, 부분 답에서 다른 선택지 없다고 단정, 문장 삭제/원문 추가 보정이 임상 의미를 바꾸는지, 최종 검사 누락/회귀를 본다. 여섯 보류가 실제 Gold 공백인지 앱의 과도한 필수 section/증명 오류인지 대표 공개 trace로 구분하고 후속 작업 우선순위를 적는다. 실물 서버/DB/코드 편집·새 batch 금지.
- `reference/2026-10-30-hub-evals/build-out/wp10-code-review.md`에 재현 위치/심각도와 판정을 쓰고 Orca worker_done 보고한다.
