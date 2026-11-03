# Q002 다중 관계 수정 후 단일 실문항 검증

## 목표

- 앱 `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals`의 현재 구현을 사용한다. Hub `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend`의 현 Gold 발행본을 격리 포트 18015에서 사용한다.
- 기존 `reference/2026-10-30-hub-evals/build-out/q002-live-gate-brief.md`의 실행 경계와 `q002-live-gate-report.md`, `q002-multi-edge-report.md`를 읽는다.
- Q002 팔자주름 한 문항만 새 label로 실행한다. 4문항/50문항 반복 금지.

## 확인 항목

1. 격리 Hub health의 Gold hash `567677edfe7123e9`, raw manifest, selected route를 확인한다. 사용자 Hub 18005·앱 18210·포트/컨테이너/DB 포인터는 건드리지 않는다. 본인이 띄운 격리 Hub만 종료한다.
2. `treats:0151~0154#evidence#row.evidence.role` 네 ID가 Hub→received→selection→Claude 입력에 모두 들어가는지와 `treats:0013`/`0152`가 같은 필러 카드 `why`에 함께 있는지 확인한다. 원천을 구분하고 필러를 두 번 추천하는 것으로 해석하지 않는다.
3. walk 완료·오류·요청 수/bytes, Claude 호출/재작성/TTFT·비용, answer validation 결과, 최종 답의 관련성·의료 안전·인용을 기록한다. 제품명/조합이 Gold 근거 없이 새로 나오면 실패로 판정한다.
4. 네 역할 전달과 **최종 답 품질**을 각각 PASS/FAIL로 판정한다. 실패하면 어느 단계에서 왜 실패했는지 적고, 코드 수정이나 추가 시험 없이 보고한다.

## 경계·보고

- 읽기/격리 실행과 결과 보고만 한다. 코드·DB 변경, 커밋/푸시/PR 금지. 기존 CLI 예산/재시도 설정을 임의로 올리지 않는다.
- `reference/2026-10-30-hub-evals/build-out/q002-after-multi-edge-live-report.md`에 결과를 쓰고 Orca `worker_done`으로 보고한다.
