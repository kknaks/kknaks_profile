# WP-8 답변용 근거 묶음·안전 적용·검증 구현

## 정본·현 상태

- 앱 워크트리 `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals`의 기존 미커밋 변경을 이어서 수정한다. 프로필 `orchestration/work/phub-recommend/SPEC-006.md` §3-4-1-5의 `Q002 실물 후속`부터 `WP-8 검수 보강`까지와 `WORK-012.md` WP-8이 계약이다. 읽기 근거: `reference/2026-10-30-hub-evals/build-out/q002-answer-root-cause-report.md`, `q002-answer-contract-review.md`, `q002-after-multi-edge-live-report.md`.
- Q002는 walk complete, 네 역할 fact 전달 PASS. 그러나 75 fact/112 facet/15 target을 두 번 Claude에 보내고, family/site_caution 소유 안전을 버리며, 재작성 뒤 raw fact 부분 답이 안전·관련성 FAIL이다.

## 구현 순서

1. **공개 관계 증명부터:** Q002 필러 unit의 site_caution/family 위험과 보톡스 unit의 제한 효과·비대칭 fact를 공개 Gold `peek`/안전 동봉/원문에서 unit·family/site·조건·owner/source까지 연결할 수 있는지 확인한다. 증거 경로를 코드/trace로 구현한다. 공개 응답에 없는 연결을 추측하지 말고 그 갈래를 보류한다. 필요 API가 있으면 구체적인 빠진 칸과 재현을 보고한다.
2. I-01의 직접 추천 edge/역할은 모두 유지하되 `treats`·`treats_unit`의 동일 unit을 **답변 갈래 한 개**로 묶는다. 질문 범위의 역할·시술명/방식·필수 안전·고지·gap만 선택한다. 타 complaint overview/무관한 일반 안전 목록·내부 값은 제외한다. 모든 명시 target/facet/required_safety는 `included|justified_not_required|unresolved|blocked`와 이유로 대조한다. 작은 입력을 위해 필수 범위를 자르지 않는다.
3. 임상 주장 제목/문장에는 근거 ID를 요구하고 순수 문진·전환·상담 안내를 비임상으로 판정한다. 실패 재작성에는 실제 실패 문장·검사·이유·사용 가능한 근거/금지 범위를 넣고 같은 작은 묶음으로 다시 검증한다. 실패 시 raw fact 나열 반환을 중지하고, 같은 안전·관련성·인용·부재 범위 검사를 통과한 축약 답 또는 범위를 특정한 보류 답만 반환한다.
4. Gold source/owner/build 대조와 Jev/walk 완료 기준은 유지한다. 특정 Q002 ID·위험 문구·제품/조합을 일반 로직에 하드코딩하지 않는다. 공개 사실 없는 제품/조합은 생성하지 않는다.

## 수용·경계

- 같은 unit 두 edge와 네 Q002 역할, owner가 unit과 다른 검증 가능한 안전 사실, 타 부위/family/complaint·조건 불일치 배제, 같은 범위 시술명 유지, 명시 두 target·나중 page 유일 근거·조건부 금기/고지 누락 방지, 임상 제목 대 순수 문진, 재작성 및 실패 보류를 fixture로 검증한다. 전체 앱 suite·Ruff·diff check를 실행한다.
- 가능하면 격리 Hub 18015에서 Q002 한 문항만 실제 Claude로 실행해 네 역할/필수 안전/인용·관련성/TTFT·입력 bytes를 보고한다. Q002 실패 시 반복 batch는 하지 말고 정확한 실패 지점을 보고한다. 사용자 Hub 18005·앱 18210·DB 포인터/컨테이너 비조작. 격리 Hub는 본인이 띄운 것만 종료.
- 앱 코드·직접 관련 테스트만 수정. Hub 코드·DB는 수정 금지. 커밋/푸시/PR 및 50문항 금지. 결과를 `reference/2026-10-30-hub-evals/build-out/wp8-answer-bundle-report.md`에 쓰고 Orca `worker_done`으로 보고한다.
