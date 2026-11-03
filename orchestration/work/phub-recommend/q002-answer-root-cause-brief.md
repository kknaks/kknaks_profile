# Q002 근거 전달 후 답변 실패 원인 진단

## 목표·범위

- 앱 워크트리 `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals`의 현재 코드, 프로필 `reference/2026-10-30-hub-evals/build-out/q002-after-multi-edge-live-report.md`와 해당 run `3a1e0cb325c6`를 읽는다.
- Q002 네 역할 fact는 모두 Claude 입력·최종 인용까지 도달했지만, 첫 답·재작성은 인용 검증에 실패하고 최종 부분 답은 안전·관련성에 실패했다. **답 생성/검증 구조의 원인과 최소한의 수정 계약**을 찾는다.

## 조사

1. Claude에 전달된 실제 payload의 항목 수·bytes와 Q002에 직접 관련된 근거 비율, 안전 fact 포함 여부를 측정한다. 민감한 원문 전체를 보고서에 복사하지 않는다. 158KB가 된 주된 구성 요소를 수치로 보여준다.
2. 첫 답과 재작성의 `uncited_sentence` 9개가 어떤 문장인지, validator가 인용 가능한 주장과 안내/구조 문장을 어떻게 오판하는지, 재작성 prompt가 실패 이유를 충분히 전달하는지 확인한다. `unsupported_absence_claim` 한 건의 실체를 확인한다.
3. 다른 complaint overview(`U5-090`), 무관한 `U5-037`·`U5-009` 조각이 왜 최종 부분 답에 들어왔는지 selection·ranking·fallback 경로로 추적한다. 필러 위험(안면동맥·괴사·색전) 근거가 Gold에 있는지, 수신/선택/전달 중 어디서 사라졌는지 확인한다.
4. Q002를 실제로 쓸 수 있는 답으로 만들 **하나의 응집된 수정안**을 제시한다. 질문과 직접 연결된 갈래별 근거 및 필수 안전 정보를 먼저 선택하고, 그 작은 집합에서 답안을 구성·인용 검증하는 계약이어야 한다. 임의의 하드코딩/무근거 의료 주장을 금지한다. 기존 Jev·walk·Gold ownership 계약은 유지한다. 수정안의 수용 조건과 대표 회귀 케이스를 명시한다.

## 경계·보고

- 읽기 전용 조사. 코드·DB·포트·컨테이너 변경, Claude 호출/새 batch, 커밋/푸시/PR 금지. 추측은 사실과 분리한다.
- `reference/2026-10-30-hub-evals/build-out/q002-answer-root-cause-report.md`에 분석과 수정 계약을 쓰고 Orca `worker_done`으로 보고한다.
