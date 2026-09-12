# 코드 검수 5 — WP-004 합성·승격·내보내기 + 검수 4 F-A/W-b/W-c 해소

- 작성: 2026-09-10 / `reviewer_code` (read-only · 검수 1~4 와 같은 세션)
- 범위: `git diff 80dd097..8397d8f` — 커밋 하나(`8397d8f`), 25파일 **+2,142 / −18**.
- **격리본으로 읽고 돌렸다.** 검수 도중 병렬 워커들이 워킹트리를 고쳤다(E-시리즈 후속 + FE P4 — 최종 12항목: `finalize.py`·`stream_service.py`·`work/requests.py`·`catalog.py`·`soniox.py` 등 + `frontend/api.ts`·`viewModels.ts`·`MeetingDetailPage.tsx`). 인용한 `파일:줄`과 검증 수치는 전부 `git archive 8397d8f` 격리본 기준이고 `git stash` 는 쓰지 않았다.
- **아무 파일도 고치지 않았다.** 워크트리·`.git` 변경 0.
- 후속 항목 E1~E6(`sc-meeting-be-wp002-fix-brief.md`)은 지시대로 **FAIL 로 세지 않았다.**

---

## 0. 총평 — **PASS (WARN 3)**

**재발주할 것이 없다.** 검수 4 의 F-A 는 겉만 막지 않고 **세 겹으로** 닫혔다 — 계약(`output_schema` 필드) · 전송(대화 경로 `--output-schema` 파일) · 지시문(스키마 JSON 을 싣고 「JSON 그것만」)이고, 테스트가 **같은 객체인지**(`is OUTPUT_SCHEMA`)와 인자 조립을 따로 단정한다. W-b·W-c 도 제대로 갚았다: 도는 중에 온 트리거를 `_deferred` 에 기억해 배치가 끝나는 자리에서 갚으니 90초 타이머를 기다리지 않고, 게이트 테스트는 이제 `(code, reason) == (4409, "not_meeting_owner")` 를 본다.

WP-004 본체도 계약대로다. `/end` 는 전이만 하고 즉시 답하며 합성은 durable job 이 현행 lease·fence 패턴으로 가져간다. 합성은 **배치와 같은 lock** 을 잡되 배치처럼 건너뛰지 않고 기다리고(「합성은 미룰 수 없다」), 세션을 이어 쓰다 없으면 콜드 폴백하며 그 횟수를 센다. 사람 안건 전수 보존·중복 접기·기한 세 갈래·이미 있는 업무 제외·evidence 강등·제목 후보가 모두 제자리에 있고, 적재는 한 트랜잭션에서 최종 줄과 후보를 전량 교체하되 **승격된 후보만 남긴다.** 승격은 work 모듈을 **기본값 보존형으로만** 건드려(`allow_self_assignment: bool = False`) 기존 계약을 깨지 않았고, 실제로 work 계약 테스트 5파일이 회귀 0으로 통과한다. 코디의 실물 e2e 관측 13가지가 전부 코드와 맞는다.

WARN 셋 중 새로 생긴 것은 하나 — **내보내기 거절이 400 `unsupported_format` 이 아니라 422** 다. 워커가 `Literal["html"]` 로 막고 그 동작을 테스트로 고정했고 코디도 실물에서 422 를 봤으므로, 코드를 고칠지 브리프 문구를 고칠지만 정하면 된다.

---

## 1. F-A 해소 — **PASS**

| 확인 | 근거 |
|---|---|
| `output_schema` 가 converse 요청에 실리나 | `modules/ax_execution/ai.py:64` `output_schema: dict[str, Any] \| None = None` — `AiGenerationRequest`(`:12`)와 같은 이름·같은 형 |
| 대화 경로가 `--output-schema` 파일을 붙이나 | `platform/codex_cli.py:174-177` 이 임시 디렉터리에 `output-schema.json` 을 쓰고, `:252` `*(["--output-schema", str(schema_path)] if schema_path is not None else [])`. `generate` 경로(`:419-420`)와 **같은 모양**이고, 스키마가 없으면 인자 자체가 붙지 않는다 |
| 배치 지시문이 JSON 하나로 답하라 하고 스키마를 싣나 | `modules/meetings/batch.py` `_OUTPUT_CONTRACT` — 「**아래 스키마를 따르는 JSON 하나로만 답하라.** 설명도 인사도 코드블록 표시도 붙이지 마라」 + `_dumps(OUTPUT_SCHEMA)`. `build_batch_prompt` 가 지시문 뒤에 이어 붙인다. 웜스타트 프롬프트에도 「앞으로 답하는 모양」 절이 새로 섰다 |
| 합성도 같은 자리 | `modules/meetings/finalize.py:239` `_FINAL_INSTRUCTIONS.format(schema=_dumps(FINAL_OUTPUT_SCHEMA))` |
| 호출자가 넘기나 | 배치 `bootstrap/application.py:382` `schema=BATCH_OUTPUT_SCHEMA` → `:398` `output_schema=schema` · 합성 `:295` `output_schema=FINAL_OUTPUT_SCHEMA` |
| **테스트가 동일 객체·인자 조립을 단정하나** | `test_meeting_memo_batch.py:577` **`assert batch.output_schema is OUTPUT_SCHEMA`**(같은 파일에서 온 같은 객체) · `:576` 웜스타트는 `is None`(맥락 turn 은 스키마를 걸지 않는다) · `:596-597` `"--output-schema" in arguments` 와 그 다음 인자가 스키마 파일 경로임을 단정 |

> 검수 4 가 지적한 「강제와 검증이 같은 파일을 본다」가 이제 실제로 성립한다 — 원형(`meeting_batch_service.py:71`·`:321`)과 같은 구조다.

---

## 2. 종료 파이프라인 — **PASS**

| 확인 | 근거 |
|---|---|
| `/end` 즉시 응답 + job 등록 | `bootstrap/application.py:754-764` — 전이·스트림 닫기 뒤 `_enqueue_finalize(session, meeting_id)` 를 **같은 트랜잭션**에서 넣고 커밋. 「합성은 사람이 기다릴 일이 아니다」 |
| durable job kind | `modules/jobs/domain.py:17` `JOB_KIND_MEETING_FINALIZE = "meeting.finalize"` |
| lease·fence 현행 패턴 | `bootstrap/meeting_worker.py:27` 「claim job (tx) → 합성 (tx 밖) → 상태 적재 (tx) → finish job (tx, fenced)」 · `:78-81` `claim(..., lease_seconds=settings.meeting_finalize_lease_seconds)` · `:97` `complete(job.job_id, job.lease_token)` — 기존 transport 그대로 |
| summarizing→done \| failed | `application.py:485` `ensure_transition(status, DONE)` · `:495` `ensure_transition(status, FAILED)`. `fail_finalize` 는 summarizing 이 아니면 조용히 돌아간다(`:493-494`) |
| `/finalize` 는 failed 에서만 | `application.py:506` 이 `ensure_transition(status, SUMMARIZING)` — 전이표상 `FAILED→SUMMARIZING` 하나뿐이라 summarizing 은 「이미 그 상태」로, done 은 없는 전이로 **둘 다 409** ✓ 코디 e2e 「summarizing 중 409」·「done 에서 409」와 일치 |
| 세션 resume + 콜드 폴백 + 카운트 | `finalize_service.py:111-116` — `session_ref` 가 없으면 `cold_start=True`, `self.cold_starts += 1`, 로그 한 줄. 콜드일 때만 `transcript` 전량을 프롬프트에 싣는다(`:122`). 테스트 `test_meeting_finalize.py:246` |
| 시도 상한 | `finalize.py:28` `FINAL_ATTEMPTS = 3` · `finalize_service.py:92-107` — 상한까지 다시 걸고 그래도 안 되면 `commit_failure` |

---

## 3. 합성 규칙 — **PASS**

| 규칙 | 근거 | 테스트 |
|---|---|---|
| 사람 안건 누락·병합 → 그 시도 실패 | `finalize.py:116` `ensure_human_agendas_survive` · `finalize_service.py:95-98` 이 `FinalizeFailed` 를 시도 실패로 접는다 | `:272` |
| 중복 접기 | 프롬프트 규칙 + | `:291` |
| 담당자 없음 | 최종 스키마에 assignee 키 자체가 없다 | `:431` |
| description/checklist 항상 | `stamp_source_lines`(`finalize.py:136`)가 출처 문장을 붙인다 | `:368` |
| due 세 갈래 | `finalize.py:150-159` `resolve_due` — ① AI 가 채운 날짜 ② 이어진 다음 회의 **전날** ③ 없음. 「근거 없이 지어내지 않는 것이 ③」 | `:390` |
| 기존 업무 있으면 후보 없음 | `finalize_service.py:142` `existing_task_titles` + `:147` `is_already_work` + `:153` 같은 배치 안 재출현까지 막는다 | `:403`·`:424` |
| evidence 밖 강등 | `finalize.py:128` `bind_evidence(notes, covered_ms)` — 본문은 산다 | `:316` |
| `concluded` AI 채움 | `application.py:457` `agenda.concluded = bool(output.concluded)` | e2e True/False 확인 |
| 최종 스키마가 **별도 파일**·strict | `schemas/ai_final_output.json`(96줄) — `ai_batch_output.json` 과 다른 파일. 제목 후보·todos·concluded 를 포함하고 회의 중 스키마에는 없다 | `:431` |
| 제목이 이미 있으면 후보를 버린다 | `finalize_service.py:133-135` + `application.py:480-482` — 사람이 지은 이름을 AI 가 덮지 않는다 | `:338`·`:354` |

> 코디 e2e 「due 전부 null」은 코드와 일치한다 — AI 가 안 채웠고(①) 이어진 다음 회의가 없어(②) ③으로 떨어진다. **E5 로 후속**이므로 여기서 세지 않는다.

---

## 4. 적재 — **PASS**

| 확인 | 근거 |
|---|---|
| 트랜잭션 하나 | `bootstrap/application.py:265-269` `commit_success` — `commit_finalized` 하나를 부르고 커밋 |
| track final 전량 교체 | `application.py:442` `replace_track(meeting, "final")` |
| todos 전량 교체 + **승격된 것 유지** | `platform/meetings.py:492-508` `replace_todos` — `linked_work_request_id is not None` 인 행을 먼저 뽑아 지우지 않는다. 「승격은 남에게 간 요청이므로 합성이 다시 돌아도 그 자리를 지운다는 뜻이 될 수 없다」 |
| `meetings.title_candidate` | `application.py:480-482` (사람 제목이 없을 때만) · `persistence.py` 신규 컬럼 |
| `last_saved_at` | `application.py:484` |
| failed + `failure_reason` | `application.py:490-498`, 2000자 절단 |
| 사람 안건 제목·출처 불변 | `application.py:443-455` — 매칭된 기존 안건은 `concluded` 와 줄만 손대고 제목·source 를 건드리지 않는다. 20개 상한도 지킨다(`:448-449`) |

---

## 5. 줄 편집·동시성 — **PASS**

| 확인 | 근거 |
|---|---|
| `PATCH /agendas/{aid}` 가 `lines` + `expected_last_saved_at` 를 받는다 | `entrypoints/http.py:322` 필드 · `:314` 설명(「그 사이에 누가 저장했으면 덮어쓰지 않고 409 로 지금 것을 낸다」) · `application.py:619-625` |
| 409 + **현재 줄 반환** | `http.py:851` `detail={"code": "meeting_agenda_stale", "current": error.current}` ✓ 코디 e2e 「PATCH stale 409 `meeting_agenda_stale` · fresh 200」 |
| 줄별 엔드포인트 0 | `grep 'lines/{'` → **0건** — 안건 단위 덮어쓰기 하나뿐 (SPEC §8-9) |

---

## 6. 승격·삭제 — **PASS**

| 확인 | 근거 |
|---|---|
| 현행 업무 요청 생성 경로를 부르나 | `bootstrap/application.py:839` `self._work_requests(session).create(...)` — 회의가 요청을 직접 만들지 않는다. 「요청을 만드는 것은 work 모듈이다 — 회의는 무엇을 넘기는지까지다」(`:833`) |
| 출처 두 id | `:847-848` `source_meeting_id=meeting.id` · `source_agenda_id=…reference["agenda_id"]` |
| `origin_kind="meeting"` | `platform/work_tasks.py` — `origin_kind="meeting" if request.source_meeting_id is not None else "request_effect"`. **기존 값이 기본**이라 회의 밖 경로는 그대로다 |
| `linked.work_request_id` 채움 | 승격 뒤 todo 에 기록 · 코디 e2e 「promote 자기 자신 201 linked」 |
| 중복 409 | `application.py:523-525` |
| 자기 자신 담당 허용 | `modules/work/requests.py` — `allow_self_assignment: bool = False` 가 **기본 False**, 회의 승격만 True 로 부른다. SPEC §9-5 「누르는 사람 자신이어도 된다」 | 
| `DELETE /todos/{todoId}` · 승격된 것 409 | `application.py:541-543` |
| 수락 시 task 에 출처 복사 | `work_tasks.py` — accept 가 `source_meeting_id`·`source_agenda_id` 를 업무로 옮긴다 (§9-7) |
| **work 모듈 최소 변경 + 회귀 0** | 변경분 전량이 **기본값 있는 선택 인자 추가**와 `origin_kind` 조건 하나다 — 기존 호출자가 손대지 않아도 같게 돈다. 실측: work 계약 테스트 5파일(`test_request_amendment`·`test_request_evidence_and_cc`·`test_task_assignments`·`test_task_origin`·`test_decision_continuity`) 포함 **157 passed, 실패 0** (§8) |

테스트: `:488`(출처 왕복) · `:519`(중복) · `:530`(자기 자신) · `:544`(담당 없음) · `:554`(수락 시 복사) · `:580`·`:591`(삭제 두 갈래) · `:599`(재합성이 승격분을 남긴다)

---

## 7. 내보내기 — **PASS (WARN 1)**

| 확인 | 근거 |
|---|---|
| `GET /export?format=html` 이 마지막 저장분 | `http.py:807-823` · `modules/meetings/export.py`(83줄). 테스트 `:619-631` 이 회의 정보·최종 줄·다음 할 일이 담기는 것과 **`storage_key`·`meetings/audio`·`soniox` 가 없는 것**, 링크가 없는 것까지 단정한다 |
| 열람 축(참석·공유) | 테스트 `:642-647` 이 외부인 404 |
| **다른 format 거절** | **동작은 PASS, 모양이 브리프와 다르다** → W-1 |

### W-1 · WARN — 내보내기 거절이 400 `unsupported_format` 이 아니라 422 (담당: 코디 결정)

- `http.py:810` `format: Literal["html"] = "html"` — 다른 값은 **FastAPI 쿼리 검증**에 걸려 422 가 된다. `unsupported_format` 문자열은 회의 경로 어디에도 없다(전수 grep 결과 자료 추출 모듈의 동명 코드만 나온다).
- 브리프 §3(및 이 검수 §2-7)은 「다른 format **400 `unsupported_format`**」이라고 적었다.
- **의도된 선택으로 보인다** — 테스트 `test_meeting_finalize.py:634-639` 가 `assert answer.status_code == 422` 로 그 동작을 고정했고, 코디 실물 e2e 도 「pdf **422**」를 보고 후속(E) 항목으로 걸지 않았다.
- 기능상 차이는 없다(둘 다 거절). **코드를 400+코드로 바꿀지, 브리프 문구를 422 로 맞출지만 정하면 된다.**

---

## 8. W-b·W-c 해소 · 경계·회귀 — **PASS**

| 확인 | 결과 |
|---|---|
| **W-b** 실행 중 트리거 기억 | **해소** — `batch_service.py` 에 `self._deferred: dict[str, str]` 신설. 실행 중이면 사유를 기억하고(`_deferred[meeting_id] = cause`), 배치가 끝나는 자리에서 `pop` 해 `schedule(meeting_id, deferred)` 로 **그 자리에서 갚는다**. 「90초 타이머를 기다리게 하지 않는다」. `reset()` 이 함께 비운다 |
| **W-c** 게이트 테스트 close code 단정 | **해소** — `test_meeting_stream.py` 가 `pytest.raises(Exception)` → `pytest.raises(WebSocketDisconnect)` 로 좁히고 **`assert (refused.value.code, refused.value.reason) == (CLOSE_CONFLICT, REASON_NOT_OWNER)`** 를 더했다 |
| `modules/*` 가 fastapi·mcp·sqlalchemy·subprocess import | **0건 ✓** (`finalize.py`·`finalize_service.py`·`export.py` 신규 셋 포함 — 전부 포트로만 말한다) |
| reset_demo 안 스키마 | `create_all` 은 `bootstrap/reset.py:20` 하나뿐 ✓. 신규 컬럼 6개(`title_candidate`·`failure_reason`·`source_meeting_id`·`source_agenda_id` ×2 표)가 전부 **nullable 추가**라 reset 이 만든다 |
| 검증 재현 (격리본, 1회) | **157 passed** (218.67s) — meeting_core · meeting_stream · meeting_memo_batch · **meeting_finalize(28)** · work 계약 5파일 · architecture |
| 리포트 주장 vs 코드 | 일치. 검수 4 가 잡은 「provider 에 그대로 걸고」가 이번엔 실제로 그렇다 |

**WP-004 Phase 1~3 검증** — `test_meeting_finalize.py` **28개**가 종료 파이프라인·합성 규칙·적재·줄 편집·승격·삭제·내보내기·열람 축을 조목조목 덮는다.

경고 14건은 starlette deprecation — **무관·기존 부채**.

**워킹트리 귀속**: 실행 직전 12항목이 떠 있었다(E-시리즈 + FE P4 병렬 작업). 격리본으로 돌렸으므로 **157 passed 는 `8397d8f` 의 수치**다.

---

## 9. 코디 실물 e2e 대조 — 13/13 일치

| 관측 | 코드 |
|---|---|
| `/end` 즉시 200 summarizing | `bootstrap/application.py:754-764` |
| summarizing 중 `/finalize` 409 | `application.py:506` `ensure_transition` 동일 상태 |
| 30초 뒤 done | 워커 claim → `commit_success` → `:485` |
| title_candidate 생성 | `:480-482` |
| final 줄 2+4, 근거 결박 | `:459-462` + `bind_evidence` |
| todos 2+2, description 2~3문장+스탬프, checklist 4 | `:463-478` + `stamp_source_lines` |
| **due 전부 null** | `resolve_due` ③ (E5 후속 — 세지 않음) |
| concluded True/False | `:457` |
| done 에서 `/finalize` 409 | 전이표에 없음 |
| export html 200 text/html(안건 포함) | `http.py:807-823` |
| export pdf **422** | `Literal["html"]` → W-1 |
| promote 참석자(교차 조직) **422 eligible** | work 모듈 `is_work_request_assignee` (E4/D29 후속 — 세지 않음) |
| promote 자기 자신 201 linked · delete 204 · PATCH stale 409 / fresh 200 | `:839-848` · `:541-543` · `http.py:851` |

---

## 10. WARN 이월

| # | 자리 | 내용 | 담당 |
|---|---|---|---|
| **W-1** | `http.py:810` | 내보내기 거절이 422(Literal) — 브리프는 400 `unsupported_format`. 테스트가 422 를 고정했고 코디도 실물 확인. 코드/브리프 중 하나를 맞추면 닫힌다 | 코디 결정 |
| **W-a**(검수 4 이월) | `frontend/src/viewModels.ts` | D26 셋(`at_ms`·`can_write_memo`·`started_at`) FE 소비. **이 커밋 범위 밖**이고, 검수 중 워킹트리에서 `api.ts`·`viewModels.ts`·`MeetingDetailPage.tsx` 가 고쳐지고 있어 FE P4 가 이미 다루는 것으로 보인다 | FE(진행 중) |
| **W-d**(검수 3·4 이월) | `codex_cli.py` | 도구 필터가 CLI 의 `enabled_tools` config 에 산다(서버측 필터 아님). 서버 조립물이라 유효 — 기록만 | — |
| ~~F-A~~ · ~~W-b~~ · ~~W-c~~ | | **셋 다 해소 확인** | ✅ |

---

## 11. 재발주 요약

**없다.** 이 커밋으로 되돌릴 것이 없고, 남은 것은 코디가 한 줄로 정할 W-1 과 이미 진행 중인 W-a 뿐이다.
