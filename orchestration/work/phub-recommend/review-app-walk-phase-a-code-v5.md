# case3 분할 수정 5차 코드 검수

**종합 판정: FAIL — coverage 수락·활성화 보류.** 앱 HEAD `078ac99` 대비 현재 미커밋 diff 6개 파일을 SPEC-006 0.3.10 §3-4-1-5와 WORK-012 WP-1~3/5에 대조했다. 읽기 전용으로 격리 단위 시험 9개(`claim_validator or source_answer or repeated_preposed or shared_trailing or split_`)와 `git diff --check 078ac99`가 통과했다. 실물 provider, Hub, QID 재생, 서버·DB·평가는 실행하지 않았다.

| 항목 | 판정 | 파일:줄·근거·최소 수정안 |
|---|---|---|
| 분할 후 부분 답변·유보·필수 flags | **PASS** | `case3.py:2030–2053`은 실패 facet을 blocked로 바꾸고 성공 facet의 검증된 원문만 합성하며, `2040–2049`는 미완료 유보와 전체 `must_show_flags`를 답·검증에 포함한다. 전 차수의 조기 반환 FAIL은 닫혔다. |
| 지원 fact의 묶음 완전성 | **PASS** | `case3.py:1965–1985`는 facet의 `support_ids`만 그룹화하고 미그룹 ID를 명시한다. 같은 대상의 다른 section 지원 fact도 해당 facet 묶음으로 남는다. `tests/phase8/test_case3_walk.py:979–986,1053–1068`이 회귀를 확인한다. |
| SDK·CLI part의 error/refusal/stop/빈 답 | **PASS** | `case3.py:2003–2019`는 예외·error·refusal·비정상 stop·빈 답을 실패로 남기고 해당 facet을 blocked로 처리한다. CLI 오류 단위 시험은 `tests/phase8/test_case3_walk.py:1094–1121`에 있다. |
| **part 근거 대조 후 완료 판정** | **FAIL** | `case3.py:2020–2024`는 `_supported_answer(...)`의 결과를 `answer_valid` trace에만 적고 무조건 `succeeded`·`delivery_groups`에 넣는다. 따라서 정상 stop이지만 원문·ID·owner·target_key가 틀린 part도 처리 성공이 되고 `2053`에서 `passed_source_contract`까지 가능하다. 최종 답은 서버 원문에서 다시 합성하므로 허위 모델 문장이 직접 노출되지는 않지만, §3-4-1-5의 **묶음별 결과 근거 ID 대조·처리 실패 incomplete** 계약은 충족하지 못한다. 최소 수정: `answer_valid=False`를 실패로 기록하고 해당 facet을 blocked로 전환하거나, 원문 재합성을 모델 결과와 독립된 무모델 성공 경로로 명시해 완료 판정·trace를 그 의미에 맞게 고친 뒤 SDK·CLI의 잘못된 ID/owner/target 답 시험을 추가한다. |
| 같은 section의 두 대상과 claim별 target/owner/scope | **PASS(허용 원문형), WARN(표현 범위)** | `case3.py:436–456`은 한 줄마다 `target_key owner section: 원문 [[ID]]`의 정확한 일치와 해당 facet `support_ids`를 요구한다. `tests/phase8/test_case3_walk.py:966–976`이 같은 section 두 대상을 구분한다. `case3.py:1832–1867,1886–1905`가 owner/scope와 대상별 지원을 확인한다. 자유 서술은 통과시키지 않고 원문으로 fallback하므로 안전하나, 이 판정은 원문형 답에 한정된다. |
| 반복·전치·공통 facet | **PASS(격리 시험), WARN(실문항)** | `case3.py:1553–1587`은 반복 span의 다음 위치, 앞부분 공통 facet, 마지막 대상 뒤 공통 facet을 기록한다. `tests/phase8/test_case3_walk.py:990–1030`의 해당 격리 시험 통과. 실제 QID의 다절 문장·resolve 순서가 같은 규칙에 맞는지는 재생 전 미확인이다. |
| CLI 비용·timing | **PASS(코드), WARN(실물)** | `case3.py:1502–1512`는 part 비용을 합산하고 마지막 CLI `_timing`의 보강 필드·stages를 전체 timer에 보존한다. `tests/phase8/test_case3_walk.py:1071–1091` 통과. 실제 CLI 래핑·인증·TTFT는 미측정이다. |
| 관계·운영 관문 | **WARN** | `case3.py:1599–1610,1914–1916`은 WP-4 관계를 지원 완료로 꾸미지 않고 blocked로 남긴다. `config.py:73`의 coverage 기본 gate는 False다. 실물 Hub page/source/cut, provider별 전체 프롬프트 한도, CLI 래핑 오버헤드, 개별 QID·고정 50 재생과 120초 TTFT 분포는 코드 검수로 확정할 수 없다. |

**WP-4 발주:** 현재 보류. 프로필 레포 `WORK-011.md:5,23,62`는 아직 `todo`이고 공개 계약 및 §6-9 PASS 확인·인계가 없으며, 이 관문은 앱의 관계 blocked 처리와 별개다.

**Coverage 활성화 전 관문:** part 결과 대조 FAIL 수정과 음성 시험, 실제 provider 한도 설정, Hub page/원문/source/cut·관계 공개 계약 확인, 요구 QID 개별 및 고정 50 재생, TTFT p50/p90·오류 분포 확인. `walk_coverage_mode=False`는 현 경로의 기본 노출을 막지만 수락 근거는 아니다.
