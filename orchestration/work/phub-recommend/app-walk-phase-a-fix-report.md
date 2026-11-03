# case3 반복 탐색 검수 FAIL 수정 보고

- 앱 HEAD `078ac99`; 기존 미커밋 diff를 이어 수정했고 커밋하지 않았다. 읽기 전용 참고 Hub build `567677edfe7123e9`; 사용자 서버·DB·포트·컨테이너는 접근하거나 조작하지 않았다.
- 변경 경로: `clinic_chat/cases/case3.py`, `clinic_chat/config.py`, `tests/phase8/test_case3_walk.py`; 앞 작업의 `clinic_chat/clients/hub_rest.py`, `tests/phase4/test_timing_runs.py` 변경은 보존했다.

## FAIL별 근거

1. **키워드 조기 배제:** `focus_terms`/`facet_cues` 필터를 제거했다. 질문의 intent section·target·owner·scope로 후보 페이지와 원문을 수집하고, slim 줄만으로 뒤 페이지를 닫지 않는다. 모든 후보는 `fact_ids` 원문 조회를 거쳐 선별한다. `test_coverage_rephrased_fact_is_not_filtered_by_question_words`, `test_coverage_slim_first_page_does_not_close_next`, `test_coverage_support_only_on_later_page`가 표현 불일치와 뒤 페이지를 재생한다.
2. **대상·안전·부재:** resolve의 경쟁 후보는 Jev 시작 선택만으로 확정하지 않으며 `ambiguous`로 둔다. I-06의 두 명시 span에는 좌·우 role을 기록한다. checks 종류 이웃은 필수 노드로 추적하고 목록 완결성·section 마지막 page·명시 empty 응답을 기록한다. peek section 미표시만으로 완료하지 않는다. `unresolved_absence`는 필수 이웃과 페이지 완료 및 오류 없는 frontier 소진 후에만 허용한다. WP-4 전 관계 facet은 미완료 relation scope로 기록하고 결정론적으로 답을 보류한다. `test_coverage_incomplete_neighbor_list_cannot_prove_absence`, `test_coverage_absence_requires_completed_page_and_neighbors`, `test_coverage_relation_is_blocked_before_adapter`, 기존 안전 예산 회귀가 관련 증거다.
3. **원장→전달→답:** 원문 조회의 ID/owner/section/source/scope/text를 확인하고 실패를 `blocked/incomplete`로 남긴다. selection에 전달 ID·원문·source·owner·scope를 보존하고 전달 직전 원장과 다시 대조한다. 생성 답은 먼저 버퍼에 담아 전달된 ID의 `[[fact_id]]` 인용과 미지원 부재 표현을 확인한 뒤 한 번 출력한다. 검증 실패는 고정 보류 응답으로 대체한다. `test_coverage_full_mismatch_blocks_answer`, `test_coverage_answer_citation_must_match_delivered_id`가 불일치 차단을 확인한다. 이 기계적 검증은 인용 문장의 의미까지 증명하지 않으므로 실물 품질 검증은 별도 필요하다.
4. **큰 입력:** 그룹별 `_answer()` 호출 경로를 제거했다. 설정된 SDK 입력 cap 초과와 단일 fact 초과를 selection/context_limit에 기록하고 답을 한 번만 보류한다; 정상 전달은 `_answer()` 한 번뿐이다. `test_coverage_input_limit_has_one_safe_answer`가 여러 답·누락을 막는 경로를 확인한다. 실제 provider context 한도는 확인되지 않아 새 경로 기본값을 `False`로 두었다.
5. **deadline·출시 관문:** `asyncio.wait_for`에 각 Hub 호출 직전 남은 전체 deadline을 적용한다. `test_coverage_inflight_call_obeys_remaining_deadline`와 즉시 deadline 회귀가 있다. 120초는 기존 Hub HTTP 기본 timeout 30초의 네 배로 둔 임시 운영값이며, 7초 TTFT와의 실제 차이·provider context는 미측정이다. QID 질문 파일 239개와 고정 목록 50개는 읽기 전용으로 확인했으나, 사용자 서버/포트/DB 비조작 및 새 평가 배치 금지 조건 때문에 실물 QID 재생은 실행하지 않았다. 따라서 기본 활성화 판단은 코디의 실물 관문 뒤에 남는다.

## 검증

- `uv run pytest tests/phase8/test_case3_walk.py tests/phase8/test_verify_runs.py tests/phase4/test_timing_runs.py tests/cli/test_rerun_report.py -q`: 72 passed.
- `uv run pytest -q`: 225 passed.
- `uv run ruff check clinic_chat/cases/case3.py clinic_chat/clients/hub_rest.py clinic_chat/config.py tests/phase8/test_case3_walk.py tests/phase4/test_timing_runs.py`: passed.
- `git diff --check`: passed.

## 잔여

- WP-4 관계 adapter, 실제 QID/고정 50 재생, provider context 측정, TTFT p50/p90, 답변의 문장 의미 검증은 이 범위에서 수행하지 않았다. Citation ID 대조와 범위 프롬프트만으로 의미적 정확성을 보장하지는 않는다.
