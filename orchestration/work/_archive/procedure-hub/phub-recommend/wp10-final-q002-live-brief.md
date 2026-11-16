# WP-10 검수된 최종 코드 Q002 단일 실물 확인

- 앱 `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals` 현재 미커밋 최종 코드와 Hub `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend`를 읽기/격리 실행만 한다. `wp10-absence-code-review.md` PASS, `wp10-safety-state-fix-report.md`의 이전 부분 답 실물과 이후 검증기 수정이 기준이다. 코드 수정 금지.
- 빈 포트 18015에 본인 격리 Hub를 기동하고 health ok/db ok/raw21/21/Gold hash567677edfe7123e9 확인. 사용자 Hub18005·앱18210·DB포인터/컨테이너 비조작. 앱 서버 없이 세 Hub URL/WALK_COVERAGE_MODE=true로 Q002 case3 claude-cli **한 문항만** 새 label 실행. 기존 예산/재시도 그대로, 추가 batch 금지.
- 실제 최종 환자 답을 별도 파일로 보존하고 다음을 나눠 판정: (1) 지지된 필러 갈래+primary risk·고지·인용/의미 검증, (2) 나머지 여섯 갈래의 정확한 보류와 다른 시술 자료 없음 단정 부재, (3) 자연어 답의 읽기 쉬움/원문 나열·내부 ID 노출/중복/길이, (4) 독립 judge 정확성·안전·불확실성·관련성, (5) Jev/Hub 호출·수신/Claude입력 bytes·첫 토큰·검증 완료 최종 전달 시간. 원문 전체 승인 제한으로 답이 덤프가 됐다면 judge PASS와 별개로 품질 미완료를 명시한다.
- 이후 코드 수정 없이 `reference/2026-10-30-hub-evals/build-out/wp10-final-q002-live-report.md` 및 답/trace artifact에 기록한다. 새 4문항/50문항/커밋·푸시·PR 금지. 본인 격리 Hub만 종료하고 Orca worker_done 보고.
