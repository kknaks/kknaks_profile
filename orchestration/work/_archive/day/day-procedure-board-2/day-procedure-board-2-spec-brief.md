
# [planner] DAY — 데모/운영 KOS 쓰기 구분 · dev 연결 거르기 없애기 (SPEC 개정 + WORK)

너는 **day `planner` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-procedure-board-2-spec`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

지금 이 스펙 워크트리에서 다른 워커는 일하지 않는다. 앱(별도 slug `day-app`)이 다른 워크트리에서 같은 `products/day/` 공통 문서(`20-spec.md` · `30-work.md`)를 고칠 수 있다 — 그 두 파일은 네 몫 행만 더한다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/research-demo-vs-live-report.md` ← **이번 결정의 근거 · 바꿀 자리 전수 목록.** §1(23자리) · §2(쓰기 5개 확인 상태) · §3(테스트) · §4(스펙 절) · §5(정할 것 F1~F9)
- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/_RESUME.md` §2 결정 표 — 2026-11-09 행들(사용자 결정 원문)
- `/Users/kknaks/orca/workspaces/mediness-mediness/day-procedure-board-2-spec/products/day/20-spec/spec-000-data-model.md` · `spec-001-login-session.md` · `spec-002-procedure-board.md` · `10-decision.md` · `40-architecture/`(system.md · deployment.md · mobile-deployment.md)
- 원천: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/reference/2026-11-03-cc-day/screen/procedure-board-decisions.md` 맨 아래 「결정 — 시작 취소의 KOS 쓰기」(이번에 뒤집힌다 — 아래 §2)

**기대는 개념** — 이 작업이 따를 판단 기준. 안 주면 워커가 매번 처음부터 정하고,
같은 결정이 작업마다 달라진다. 없으면 "해당 없음".

- 해당 없음

## 2. 배경 / 무엇을 바꾸나

**사용자 결정(2026-11-09, 원문 취지)**: KOS 데모 지점과 실제 병원은 **같은 API 에 테넌트만 다르다.** 데모에서 되는 기능이 운영에서 안 될 이유가 없다. prod 배포도 안 했는데 코드로 막을 이유가 없다. dev/prod 분리는 각 DB(스키마)에 어떤 병원 연결을 넣느냐 — **데이터로** 이미 된다(dev = 데모 병원 연결만 · prod = 실제 병원 연결만).

**그래서 없앤다(리서치 리포트 기준)**
1. **(가) 데모/운영 KOS 쓰기 구분** — `trial_writes` · 설정 `KOS_TRIAL_WRITES_ON_LIVE` · `TRIAL_STEPS` · 「데모 연결에만 · 운영은 not_supported」 규칙. 5개 쓰기(시작 취소 `change-flow-step PROCEDURE_WAITING` · 완료 취소 `change-tasks-complete complete=false` · 재호출(이미 호출된 작업에 다시) `call-tasks-doctors` · 귀가 대기 1 `cancel-flow-tasks reason=CANCEL` · 귀가 대기 2 `change-flow-step PROCEDURE_DONE`)는 **모든 연결에서 같게** 보낸다. 환경 · 연결 종류로 가르지 않는다.
2. **(나) `APP_ENV=dev` 서버의 `is_demo` 거르기** — 동기화 · 쓰기 대상 · 로그인 병원 후보. dev 와 prod 는 같은 코드로 같게 동작한다.
3. **`crm_connection.is_demo` 칸** — 위 둘이 없어지면 쓰는 곳이 없다. 칸을 지울지(migration) 는 SPEC-000 에서 정하되, **남길 근거가 원천에 없으면 지우는 쪽**으로 쓴다. 지우면 시드(`ensure_demo_connection`)가 넣던 값도 빠진다.
4. **시작 취소 뒤집기**: 같은 날 결정 「시작 취소는 KOS 에 쓰지 않는다」(procedure-board-decisions.md 맨 아래 · profile #123)는 **뒤집혔다** — 시작 취소의 KOS 쓰기는 **방문 단계**(시술 대기 ↔ 시술 중) 쓰기이고, 데모에서 정상 동작(사용자) · `reference/2026-10-23-cc-overall-board/har/방배정.har` 에 같은 내부 요청(200)이 있다. 쓰기 유지 · 「HAR 없음」 표기 바로잡기.

**확인 상태 표기**: 5개 중 시작 취소만 HAR + 데모 실물 확인. 나머지 4개는 「확인 안 됨」으로 **그대로 적는다**(지어내지 않는다). 확인 안 된 것을 환경별로 막는 대신, 「모든 연결에 같게 열고 데모 실물로 확인한다」가 이번 방향이다. 4개를 데모에서 확인하는 일은 코드 뒤 QA 단계로 WORK 에 둔다.
귀가 대기 2 는 KOS 웹 「귀가」가 `step: COMPLETED`(`귀가.har`)를 보낸다는 사실도 함께 적고, `PROCEDURE_DONE` 과의 관계는 열린 질문(OQ)으로 둔다.

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

- 화면 · API 계약(경로 · 응답 모양)은 바꾸지 않는다. `ActionResult.not_supported` · `event_log.payload.kos.status = not_supported` 가 이 5개 쓰기에서 더는 안 생긴다 — 응답 필드를 지울지는 코드 몫으로 WORK 에 적는다(화면에서 읽는 곳 0 — 리포트 §1 참고).
- 설정 `KOS_TRIAL_WRITES_ON_LIVE` 제거 → `deploy/config/{dev,prod}.env` · 40-architecture/deployment.md 환경별 env 표에서도 뺀다.

## 4. 먼저 읽을 핵심 파일

- 리서치 리포트 §1 · §3 · §4 에 파일:줄 · 스펙 절이 전부 있다. 그 목록이 바꿀 범위다 — 목록 밖은 다시 grep 해 확인하고 빠진 것은 보고에 적는다

## 5. allowed_paths — 이 밖은 건드리지 마라

- `products/day/`

## 6. 구현 단계

1. 리포트 §4 의 스펙 절을 **전부** 고친다 — SPEC-000(§3 01 환경 · `is_demo` 칸) · SPEC-001(규칙 5 · OQ-10 로그인 후보) · SPEC-002(개정 ⑤ ⑥ ⑦ · KOS 쓰기 표 · 규칙 13 · 14 · 17 · U-9 · S-5 · S-6 · OQ-08~10 · 상태 그림 · 시작 취소 행) · 40-architecture(system.md · deployment.md · mobile-deployment.md M-18). 각 SPEC 머리에 개정 줄(날짜 · 사용자 결정 · 근거 리포트)
2. `10-decision.md` 에 DEC 한 건: 무엇을 왜 없앴나 · 뒤집힌 결정(11-06 W6 의 「KOS 쓰기 닫기」 · 11-03 「APP_ENV=dev 는 is_demo 만」 · 11-09 「시작 취소 KOS 안 씀」)을 취소선 · 사유와 함께
3. `30-work/` 에 WORK 한 건(코드 WP): 리포트 §1 의 (가) 12 · (나) 8 · (다) #21 자리와 §3 테스트 목록을 WP 로 나눈다. 마지막 WP = 데모 실물 확인(DAY dev 에서 5개 쓰기 · 테스트 데이터 `scripts/seed_demo_board.py`). `20-spec.md` · `30-work.md` 색인에 행 추가
4. 리포트 §5 F1~F9 를 이 결정으로 닫은 것 / 아직 열린 것으로 나눠 보고

## 7. 범위 제약 — 하지 말 것

- 코드 수정 금지(스펙 레포만)
- 확인 안 된 4개 쓰기를 「확인됨」으로 적지 마라 · KOS 경로 · 값을 지어내지 마라
- 화면 문구를 지어 넣지 마라
- 환경 · 연결 종류로 동작을 가르는 새 규칙을 만들지 마라(이번 결정의 반대)
- `products/day/` 밖 · 다른 제품 문서 금지 · 커밋 · push 금지

## 8. 검증

```
python3 scripts/lint-pipeline.py --strict → products/day/ 범위 ERROR 0 (타 제품 기존 WARN/ERROR 는 '무관'으로 분리 보고). 근거 없는 정책 0 · 열린 것은 열린 것으로
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_b915fb18-742f-4779-962c-79848020b8d5 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_b915fb18-742f-4779-962c-79848020b8d5 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_b915fb18-742f-4779-962c-79848020b8d5 --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
