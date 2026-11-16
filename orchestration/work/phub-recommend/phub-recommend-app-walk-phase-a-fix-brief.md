# [clinic_chat backend] case3 반복 탐색 1단계 코드 검수 FAIL 수정

너는 앞 판 코드의 수정 워커다. Orca dispatch preamble의 완료 보고 명령을 우선한다. 현재 앱 worktree의 미커밋 변경을 이어서 고친다.

## 읽을 것

- 필수: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/review-app-walk-phase-a-code.md` 전체 FAIL/WARN과 `SPEC-006.md` 0.3.10 §3-4-1-5, `WORK-012.md` WP-1~3/5
- 현재 app diff 및 `clinic_chat/cases/case3.py`, `clients/hub_rest.py`, `config.py`, 관련 시험
- 앞 브리프 `phub-recommend-walk-app-phase-a-brief.md`; 현재 HEAD `078ac99`, Hub build `567677edfe7123e9`

## 수정 요구

검수 FAIL을 수락 가능한 수준으로 닫는다. 특히 사용자 요구는 **그래프에서 필요한 근거를 찾기 전에 버리지 않고, 최종 답에 필요한 자료만 Claude에 넘기는 것**이다.

1. `focus_terms`/`facet_cues` 7개 고정 단어를 지원 판정·section 제외·원문 조회·Claude 전달의 유일한 기준으로 쓰지 않는다. 질문 target·intent facet·section·owner/scope 기반으로 후보를 넓게 모으고, 원문·출처·적용 범위를 확인한 뒤 관련성을 판단한다. slim `line`만으로 지원 완료/뒤 page·이웃 `not_required` 처리 금지. full 조회가 실패하면 열었던 frontier를 보존하거나 `blocked/incomplete`로 남긴다. 사우나/회복 표현 불일치처럼 필요한 fact를 키워드 불일치로 놓치는 재생을 추가한다.
2. resolve span/role/명시 양쪽과 경쟁 동의어 후보를 구분한다. 필수 안전 확인 조건 이웃을 별도 frontier/완료 상태로 추적한다. peek section 미표시가 완료 empty의 증거인지 Hub 계약에 맞춰 확인한다. `unresolved_absence`는 해당 page `more=0`뿐 아니라 필요한 이웃 목록/pair/global 범위의 완료 증거가 있어야 한다. 관계 WP-4 전에는 관계 의도를 답할 때 일반 카드 fact로 방향/우열/대안을 추정하지 않도록 명시적 차단을 둔다.
3. 수집 원장→선별→Claude payload의 ID·owner·원문·source·applies_to/scope 대조를 실제 경로에 넣고, 불일치/누락은 지원 완료가 아닌 `blocked/incomplete`. `retrieval_limits`를 프롬프트에 넣는 것만으로 답변 검증이 끝난다고 보지 않는다. 미완료 facet의 `정보 없음` 단정을 막는 답변 계약과 검증을 추가한다.
4. 그룹마다 `_answer()`를 호출해 여러 답이 출력되거나 CLI에서 마지막 그룹만 남는 현재 분할 경로를 제거한다. 실제 provider 한도를 확인한 단일 최종 입력이 가능하면 한 번만 답한다. 너무 크면 ID 보존한 내부 분할→근거 대조→최종 답 한 번을 구현하거나, 이번 단계에서 안전하게 `blocked/incomplete`로 처리하고 조용한 누락/잘린 답을 내지 않는다. 단일 fact 초과도 selection 상태와 결과에 남긴다. 제공자 한도 미확인인데 기본 활성화하지 않는다.
5. 120초 deadline은 호출 전 체크뿐 아니라 남은 시간으로 각 호출을 제한한다. 7초 TTFT 목표와의 실제 차이는 미측정으로 정직하게 남긴다. QID 실물 재생이 불가능하면 그 이유를 확인해 보고한다. 새 경로를 기본으로 켤지는 위 FAIL과 실물 검증 후 코디가 판단할 수 있게 feature gate 기본값을 안전하게 둔다.

필요하면 검수 지적과 다른 더 나은 구현 방식을 택해도 되지만, 각 FAIL의 해결 증거를 완료 메시지에서 항목별로 보여라. WORK-012 WP-4 관계 adapter 자체는 Hub 공개 계약 인계 전 시작하지 않는다. 사용자 서버/포트/컨테이너·개발/운영 DB·평가 배치를 건드리지 않는다.

## 범위·검증

- 앞 브리프의 허용 코드/시험 경로만 수정. 허용 범위 밖이 꼭 필요하면 코디에게 먼저 질문한다. 다른 레포·SPEC/WORK 수정 금지.
- 최소 재생: 다른 표현의 필요한 fact, slim line만의 조기 종료 금지, 안전 이웃 8KB 넘는 사례, 미완료 이웃/pair/global 부재 단정 금지, 큰 입력 한 번의 사용자 답, CLI 마지막 그룹 유실 금지, deadline 강제, 기존 회귀.
- `uv run pytest` 관련 시험, 전체 unit suite, 만진 파일 ruff, `git diff --check`. 실제 QID 재생과 provider context 측정이 불가능하면 명시한다.
- 커밋·push·PR 금지. 완료 시 dispatch preamble대로 `worker_done` 한 번.
