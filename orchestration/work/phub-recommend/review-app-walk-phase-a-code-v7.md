# case3 분할 ID 완전성 7차 코드 검수

**종합 판정: 코드 PASS, coverage 활성화 보류.** 앱 HEAD `078ac99` 대비 현재 미커밋 diff를 SPEC-006 0.3.10 §3-4-1-5와 WORK-012 WP-1~3/5에 대조했다. 6차 FAIL의 F1/F2 부분 인용 결함은 SDK·CLI 경로 모두 수정됐다. 이 검수에서 구체적으로 재현된 새 결함은 없다. 실물 provider·Hub·QID 재생은 수행하지 않았다.

| 항목 | 판정 | 파일:줄·근거·최소 수정안 |
|---|---|---|
| F1/F2 중 F1만 인용한 part | **PASS** | `clinic_chat/cases/case3.py:1992–1995`가 실제 part의 `facts`와 `support_ids`를 같은 ID 집합으로 만든다. `:2025–2035`가 기대 ID와 실제 인용 ID를 대조해 F2 누락을 `answer_id_mismatch`로 실패 처리한다. `:2042–2045`의 완료·`delivery_groups` 기록에 도달하지 않는다. 최소 수정 없음. |
| 추가·중복 ID, 잘못된 owner/target/원문 | **PASS** | `case3.py:2025–2041`은 추가·중복 인용을 ID mismatch로, `:436–456`의 원문/owner/section/target 검증 실패를 evidence mismatch로 처리한다. `tests/phase8/test_case3_walk.py:1072–1147`의 SDK·CLI 음성 시험 통과. 최소 수정 없음. |
| 실패 trace와 전달 묶음 | **PASS** | 실패 part는 `split_part_results=failed`와 `missing_ids/extra_ids/duplicate_ids`를 남기고 `delivery_groups`에 들어가지 않는다(`case3.py:2029–2045`). 해당 facet은 `blocked`와 실제 실패 사유의 `unread`, 전체는 `incomplete/tool_error`, 최종 검증은 `partial_source_contract`가 된다(`:2046–2064,2083`). 최소 수정 없음. |
| 성공 부분 답·유보·안전 flags | **PASS(격리 시험)** | 실패 범위는 유보하고 성공 범위의 원문 답을 합성하며 필수 flags를 붙인다(`case3.py:2068–2083`). `tests/phase8/test_case3_walk.py:1138–1147`에서 성공 part·유보·flags·실패 범위 제외를 확인했다. 최소 수정 없음. |
| 실제 운영·WP-4 | **WARN** | `case3.py:1914–1916`은 관계를 지원 완료로 세지 않는다. `WORK-011.md:5,23,61–62`의 공개 관계 계약과 §6-9 PASS/인계가 아직 없으므로 **WP-4 발주 불가**. 관계 어댑터 착수 전 해당 관문을 닫아야 한다. |

**재현·검증:** `uv run pytest tests/phase8/test_case3_walk.py -q -k 'split_rejects_invalid_part_answer or split_merges_once_and_keeps_ids'` → **17 passed**. 음성 시험의 `missing_id`는 첫 part의 두 개 이상 fact 중 마지막 한 줄을 빼 F1만 인용하는 상황이며 SDK·CLI 양쪽에서 실패 상태·미전달·유보를 확인한다(`tests/phase8/test_case3_walk.py:1088–1090,1125–1147`). `git diff --check 078ac99` 통과. 코드·서버·DB·평가는 수정하지 않았고 소수 단위 시험만 실행했다.

**Coverage 활성화 전 관문:** 실제 provider의 전체 입력 한도를 설정·검증하고, Hub page/source/cut 및 WORK-011 관계 공개 계약을 확인한다. 요구 QID 개별 재생과 고정 50×1에서 수집→전달→답 ID·원문·source·scope, 안전 고지, 정확성, TTFT p50/p90, blocked 분포를 확인한 뒤 사용자 승격 판단을 받는다. 현재 기본 `walk_coverage_mode=False`는 미검증 경로의 노출을 막는다.
