# [reviewer_code] 코드 검수 5 — WP-004 합성·승격·내보내기 + 검수 4 F-A/W-b/W-c 해소 (차분만)

너는 **sc-ax `reviewer_code` 워커**다. 검수 1~4 를 한 세션이다 — **WP-004 커밋 차분만** 본다.

작업 워크트리: `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting` — 읽기만. 범위 = `git diff 80dd097..8397d8f`(HEAD 가 더 나갔으면 8397d8f 까지만). 서버·reset·5176/8001 금지. 워킹트리가 더러우면(FE P4 워커 병렬) `git archive HEAD` 격리본으로.

## 1. 기준

- SPEC 0.4.1 §8(종료와 합성) · §8.1 중복 방지 · §8.2 Todo 값 · §8-9 줄 편집(안건 덮어쓰기·409) · §8-10 내보내기 HTML · §9 승격(언제나 업무 요청, 출처 두 id) · §5.1(summarizing→done|failed, failed→summarizing) · §7.2-6 구조화 출력 강제. WP-004 `30-work/work-004-final-merge-followup.md` Phase 1~3 검증.
- 브리프 `sc-meeting-be-wp004-brief.md` §3(코디 확정 계약) + 코디 추가 지시: **F-A**(`AiConversationRequest.output_schema` → converse 경로 `--output-schema` · 배치 지시문에 스키마 JSON 요구 · 합성도 같은 자리) · **W-b**(실행 중 안건 전환 트리거 기억) · **W-c**(게이트 테스트 close code 단정). 워커 리포트 `report-be-wp004.md`. 검수 4 리포트 `review-code-04-report.md`.
- 코디 실물 e2e(2026-09-10, 실제 Codex): `/end` 즉시 200 summarizing · summarizing 중 `/finalize` 409 · **30초 뒤 done** · title_candidate 생성 · final 줄 2+4(근거 구간 결박) · todos 2+2(description 2~3문장+스탬프, checklist 4개, **due 전부 null** — E5 로 후속) · concluded True/False · done 에서 `/finalize` 409 · export html 200 text/html(안건 포함)·pdf **422** · promote 참석자(교차 조직) **422 eligible** — E4/D29 로 후속 · promote 자기 자신 201 linked · delete 204 · PATCH stale 409 `meeting_agenda_stale` · fresh 200. 코드가 이 관측과 일치하는지 대조. 후속 항목(E1~E6)은 별도 브리프 `sc-meeting-be-wp002-fix-brief.md` — **여기서 FAIL 로 세지 않는다**.
- 원형 `/Users/kknaks/git/toy_pr2/task_management/app/back/service/meeting_finalize_service.py` · `meeting_batch_service.py` 최종 분기.

## 2. 확인 — 각각 PASS/FAIL(파일:줄)

1. **F-A 해소** — `output_schema` 가 converse 요청에 실리고 codex_cli 대화 경로가 `--output-schema` 파일을 붙이는가(generate 와 같은 모양) · 배치·합성 지시문이 JSON 하나로 답하라고 말하고 스키마를 싣는가 · 테스트가 인자 조립과 스키마 동일 객체를 단정하는가.
2. **종료 파이프라인** — `/end` 즉시 응답 + durable job `meeting.finalize` 등록(lease·fence 현행 패턴) · `meeting_worker` claim → 합성 → 커밋 · summarizing→done|failed · `/finalize` 는 failed 에서만(그 외 409) · 세션 resume(WP-003 `ai_session_ref`) + 콜드 폴백 분기와 카운트.
3. **합성 규칙** — 사람 안건 누락·병합 시 배치 폐기·failed · 중복 접기 · 담당자 없음 · description/checklist 항상 · due 세 갈래 · 기존 업무 있으면 후보 없음(`task_list` 조회) · evidence 밖 강등 · `concluded` AI 채움 · 최종 스키마 strict(회의 중 스키마와 별도 파일, 제목 후보·todos·concluded 포함).
4. **적재** — 트랜잭션 하나 · track final 전량 교체 · todos 전량 교체(승격된 것 유지) · `meetings.title_candidate` · `last_saved_at` · failed + `failure_reason`.
5. **줄 편집·동시성** — `PATCH /agendas/{aid} {lines, expected_last_saved_at}` 409 + 현재 줄 반환 · 줄별 엔드포인트 0.
6. **승격·삭제** — `POST /todos/{todoId}/promote` 가 현행 업무 요청 생성 경로를 부르고 `source_meeting_id`·`source_agenda_id`·`origin_kind="meeting"` 을 싣는가 · `linked.work_request_id` 채움 · 중복 409 · 자기 자신 담당 허용 · `DELETE /todos/{todoId}`(승격된 것 409) · 수락 시 task 에 출처 복사 · **work 모듈 최소 변경 + 기존 work 계약 테스트 회귀 0**.
7. **내보내기** — `GET /export?format=html` 마지막 저장분(회의 정보·안건별 최종 줄·다음 할 일) · 다른 format 400 `unsupported_format` · 열람 축(참석·공유).
8. **W-b·W-c** 해소 · **경계·회귀** — modules/* import 경계 · reset_demo 안 스키마 · 검증 재현 1회: `cd backend && uv run pytest -q tests/contract/test_meeting_core.py tests/contract/test_meeting_stream.py tests/contract/test_meeting_memo_batch.py <WP-004 테스트> <work 계약 테스트> tests/architecture -m 'not integration'` · 리포트 주장 vs 코드.

## 3. 산출물 — 하나

`/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/work/sc-meeting/review-code-05-report.md` — 총평(PASS / FAIL — 재발주) · 항목 1~8 표 · FAIL 파일:줄 + 방향 · WARN 이월.

## 4. 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_9efe51f3-aec0-44b1-94ea-f86134b6ddea \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "reviewer_code 완료: 코드 검수 5" \
  --body "총평 / 항목 1~8 / FAIL·WARN / 검증 수치"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] reviewer_code 완료 — 코드 검수 5: <PASS/FAIL 한 줄>. 상세는 인박스." --enter
```
