# planner-delivery230-231-v2 결과 보고 — done (승인 안 함 · W6 · W8 은 손대지 않음)

| Issue | contract | plan_digest(v2) | 이전(v1 · stale) |
|---|---|---|---|
| [#230 ① 백엔드](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/230) | v2 · L3 | `sha256:99bd5c990e7d2da2996e15a2397bb3af056f7dd4f9df088b276b29b1c4bfaa4d` | `f2d64dc0…` |
| [#231 ② 화면](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/231) | v2 · L2 | `sha256:7be75be5c043850a8b83b599a8ad68aab652c77bbfceb1a75876662522c9c27b` | `aa03c1ea…` |

같은 Issue · 같은 key 갱신(apply `scope-delta-recorded`) · 라벨 `delivery-plan:review` 그대로. 파일 = `delivery/v2-board-*.json`(v1 사본 `*.v1.json`) · `*.v2.plan.json` · `*.v2.apply.json`. mediness 워크트리 수정 없음.

## 바뀐 항목

| W | Issue | 바뀐 것 |
|---|---|---|
| W1 | #230 TD「KOS 쓰기」 · A5 · phase · 검증 | **(경로 + 값) 단위로 연다** — flow-step 은 `step = PROCEDURE` 만 · complete 는 `true` 만 · call-tasks-doctors 는 아직 호출 안 된 작업만. 미확인 값(PROCEDURE_WAITING · PROCEDURE_DONE · complete false · WAITING 재호출)은 op 을 만들지 않거나 지원 안 함으로 드러남 · 지금 `SUPPORTED_WRITES`((api, 경로) 집합)를 이 단위로 바꾼다. A5 = 그 단위 테스트 |
| W2 | #230 TD「화면 라우트」 · A3 · **A9 신설** · phase / #231 TD「HTMX 연결」 · 의존 | #230 이 **조각 계약 표**(조각 이름 · 넘기는 값 · SSE 이벤트 · 오류 / kos_failed 토스트 조각 이름)를 Issue 코멘트 또는 코드 문서로 남김(A9) · 웹 라우트 테스트 = 최소 자리 템플릿 · 렌더 컨텍스트(A3). #231 은 그 표를 의존 조건으로 인용 |
| W3 | #230 TD · Non-Goal / #231 TD 새 줄 · **A6 신설** · phase | 토스트 조각 템플릿 두 개(오류 · kos_failed) = **#231** 이 #229 토스트 매크로로 만듦 · #230 은 그 이름으로 렌더해 응답 · SSE 에 실음. #231 A6 = 오류 토스트 · kos_failed 토스트가 뜬다 |
| W4 | #230 의존 | + #229(웹 조립 web.py · Jinja2 · base · 토스트 매크로) |
| W5 | #230 TD「동기화」 · A1 · A8 · Non-Goal | visit_task_staff = cc `[].id` 가정 매핑 → A8 실물(수락 뒤 다음 조회)에서 모양 확인 · fixture 를 실물로 · OQ-12 직원 배열 부분은 A8 이 닫음(procedureConfiguration 은 HAR 뒤) |
| W7 | #231 TD 새 줄 · Non-Goal | E06 · **E08** · E09 · E10 = 자리(모양)는 그리고 동작은 없다 |

## 손대지 않은 것

- **W6**(HAR 미확인 동작의 1차 처리 — Acceptance 가 그 동작을 가정) · **W8**(실물 확인 수락 단계 — 수락할 의사의 DAY 로그인) — 사용자 답 뒤.
