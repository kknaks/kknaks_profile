# [backend] 외부 연동 API 수정 1 — 코드 검수 r1 WARN 반영

검수 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/orchestration/work/api-swagger-docs/ext-review-r1.md` §WARN. 원 브리프(`ext-api-be-brief.md`) 제약 그대로(커밋 금지 · KOS 쓰기 금지 · 사용자 포트 금지 — 8700 에 코디의 compose 가 떠 있다, 건드리지 마라).

**W1 ~ W6 를 리포트 「고칠 방향」 그대로 고친다.** 결정(코디):
- W1: 이름 검색 2xx 인데 `data` 가 배열이 아니면(없음 포함) `502 kos_unavailable` · `create-visitor` 0번 — 조회 · 예약 시험 추가
- W2: 앱 설명 email 문장 다음 줄에 「이름은 KOS 에 저장된 띄어쓰기 그대로 보내야 한다(띄어쓰기가 다르면 찾지 못해 `404`).」 · T29 단언
- W3: 예약 502 · 409 `kos_rejected` 오류 줄을 리포트 문구대로
- W4: 조회 400 줄에서 `start` 제거(조회 · 예약 400 줄 분리)
- W5: `require_ext_key` 를 `async def` 로(카운터 접근 = 이벤트 루프 한 스레드). 미들웨어 IP 카운터도 같은 스레드인지 확인 · 동시 요청 시험(가능하면 지연 주입으로 60 초과 통과 0)
- W6: 미들웨어 `call_next` 예외 → `ext_call` 500 `internal_error` 1줄 + `500 {"error":{"code":"internal_error",…}}` + `no-store` · 본문 · 로그에 예외 문구 없음(종류만) · 시험
- W7 은 SPEC 몫(코드 그대로)

검증: 바꾼 곳 관련 시험 → 끝에 전체 `uv run pytest -q` · `ruff` 한 번. `ext-be-report.md` 끝에 「수정 1」 절(무엇 · 수치)을 더한다. 완료 보고는 원 브리프 §7 두 채널(이번 dispatch 의 taskId · dispatchId).
