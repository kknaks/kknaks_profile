# WP-11 근거를 보존한 자연어 답과 최종 전달 계측 제안

2026-11-02 · 상태: 구현 전 제안 · 범위: case3 coverage의 답변 생성 이후 한 경로.

**하나의 변경을 제안한다.** 수집·노드 선택을 그대로 두고, 검증된 답변 묶음에서 Claude가 환자용 원자 claim과 source ID를 구조화해 만들게 한다. 앱의 출처·범위 검사 → 한 요청에 묶은 Jev 의미/필수 내용 검증 → 짧은 번호 인용 렌더링 → 최종 on_text 기록으로 연결한다. 자연스러운 의역을 허용하되 임상 의미를 토큰 겹침·정규식·원문 일부 포함만으로 승인하지 않는다. 원문 전체 일치 경로는 최후의 제한된 fallback이며, 길거나 안전 커버를 유지할 수 없으면 범위 보류로 끝낸다.

## 1. 읽은 근거와 현재 판정

- 앱 `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals`의 HEAD는 `078ac99b2f307de65acdcdecc9beb94bcda1249c`. case3, loop, Hub client, config, prompt, fixture 등에 기존 미커밋 변경이 있다. 본 작업은 이를 읽기만 했으며 HEAD만으로 실행 코드를 특정하지 않는다.
- 정본 [SPEC-006 0.3.13](SPEC-006.md) §3-4-1-5~7, §4와 [WORK-012](WORK-012.md)를 읽었다. 0.3.13의 후보별 Noul 묶음이 이전 복수 Choice 슬롯보다 우선한다. 아래 claim별 Choice는 서로 다른 claim을 각각 삼분류하는 용도이며 노드 다중 선택 계약을 되돌리지 않는다.
- [최종 Q002 보고](../../../reference/2026-10-30-hub-evals/build-out/wp10-final-q002-live-report.md), [실제 답](../../../reference/2026-10-30-hub-evals/build-out/wp10-final-q002-answer.txt), [로컬 TypeSafe 설명](../../../para/resources/note/ai/llms.txt)을 읽었다. run `1297a5c89976`, batch `b202611022243-162908`, Gold `567677edfe7123e9`는 **기존 실물의 증거**이며 이번 세션에서 새 health 확인이나 실행은 하지 않았다.
- 기존 최종 답은 2,201자, 21개 인용 원문 행과 여섯 갈래 보류다. judge4 PASS지만 역할 도입이 제거되고, 척도 설명 없는 `4`, 내부 ID, 중복 위험 설명과 시술자용 문장이 남았다. 자연어 품질 완료가 아니다.
- 기존 수치는 Jev 3회/605.6ms, 전체 Hub 104회, coverage 수신 279,705B, Claude 전달 46,803B, 모델 첫 토큰 5,777.8ms, CLI 반환 14,601.6ms다. 마지막 값은 correction 뒤 최종 전달 시간이 아니다.
- 코드 근거: `case3.py::_grounded_recommendation/_supported_answer`는 intact source를 요구하고 `_coverage_answer_failures`와 `_repair_uncited_clauses`가 답을 교정한다. `_missing_relevant_safety/_flag_shown`의 문구 검사만으로 의역의 안전 의미를 승인해서는 안 된다. `coverage_run`은 최종 답을 buffered 생성·검증 후 `on_text`로 보낸다. `_finish`는 CLI timing 사본을 사용해 최종 후처리 시간을 놓칠 수 있다.

### 공식 문서에서 가져오는 범위

2026-11-02 [공식 llms.txt](https://docs.typesafe.ai/llms.txt)에서 링크를 찾은 뒤 다음 원문을 확인했다. 인덱스의 `.md` 링크 일부는 web 도구로 열리지 않아 같은 공식 URL의 확장자 없는 페이지로 확인했다.

| 공식 근거 | 이 제안에 적용하는 것 | 적용하지 않는 것 |
|---|---|---|
| [citation_check](https://docs.typesafe.ai/cookbooks/citation_check) | 출처 존재 확인과 claim의 지원/반대/미지원 의미 판정을 분리 | RFC 예제의 임계값·정확도를 한국어 의료 승인 기준으로 복사하지 않음 |
| [primitives](https://docs.typesafe.ai/primitives) | claim마다 Choice 하나; 각 질문은 같은 state를 독립 평가; instructions에 배열 위치를 명시 | 한 질문 결과를 같은 요청의 다른 질문이 읽는다는 가정 |
| [fan-out](https://docs.typesafe.ai/patterns/fan-out) | 여러 독립 질문을 한 요청에 묶고 앱이 결과를 합침 | 질문을 늘리면 언제나 지연·비용이 일정하다는 보장 |
| [Python SDK](https://docs.typesafe.ai/sdk/python) | 기존 AsyncTypeSafeClient.system_one, Choice/Noul과 typed 결과 사용 | 새 SDK/provider 설치 또는 이번 작업에서 API 실행 |
| [models](https://docs.typesafe.ai/models) | 실제 응답 model 기록, 기본 요청/질문 문맥 한도, 한국어 검증 필요 | alias 고정성·모델 판단의 의료적 보증 |

Jev는 답문을 생성하지 않는다. 공식 citation cookbook은 단일 claim의 문맥 판단 예이며, 이를 여러 claim 및 coverage 질문으로 묶는 것은 본 제안의 설계 확장이다. 한국어 의역·부정·조건 누락에 대한 효능은 아직 검증되지 않았다.

## 2. 작은 구현 범위와 파일

첫 구현은 **WALK_COVERAGE_MODE의 I-01 경로**에만 `answer_contract_version=claim_v1` 옵션으로 붙인다. 기존 수집/관계/페이지 종료, 다른 의도, provider 구성, Hub 계약은 바꾸지 않는다. 대표 4문항에서는 나머지 의도의 기존 동작 회귀도 확인한다. 전체 의도 확대는 별도 판단이다.

| 파일/함수(추가 함수명은 제안) | 변경 |
|---|---|
| `clinic_chat/cases/answer_contract.py` (신규 작은 모듈) | strict schema 파싱, `validate_bindings`, `build_semantic_questions`, `decide_contract`, `render_verified_answer`를 한곳에 둠 |
| `clinic_chat/cases/case3.py::_answer/coverage_run` | 기존 selected/answer_scope를 입력으로 구조화 생성 연결. 임상 의역에는 intact-only 승인 대신 새 관문 적용. 수정·fallback·보류를 공통 최종 전달 함수로 모음 |
| `prompts/case3.md` | claim별 한 주장, 환자용 문장, 근거/조건 유지. 의료 주장 제목도 claim으로 제출. 원문 모두 나열/모든 전달 ID 인용 강제 금지 |
| `clinic_chat/llm/cli.py` 기존 `run(schema=...)` | 이미 있는 `--json-schema`/`structured` 결과 경로를 case3에서 사용. 이벤트가 구조화 결과를 누락하면 파싱 실패로 보류; 자유 텍스트를 몰래 승인하지 않음 |
| `clinic_chat/config.py` | 기능 플래그, 검증 정책 버전·보정 임계값 참조. 기존 키·모델·클라이언트 사용 |
| `clinic_chat/timing.py`, `case3.py::_finish`, `clinic_chat/runner.py` | 후처리 뒤 현재 timer snapshot 저장; 최종 callback 및 delivery 상태 계측. CLI별 timing 원본도 보존 |
| `clinic_chat/verify_runs.py`, `report.py`, `rerun_report.py` | partial/full/hold, 의미 판정/커버, 최종 전달 시간 별도 표시. 기존 TTFT/CLI total과 혼합 금지 |
| `tests/phase8/test_answer_contract.py`, `tests/phase4/test_timing_runs.py` | 아래 경계 fixture와 가짜 시계 검증 |

CLI 경로부터 적용한다. SDK provider까지 같은 flag를 활성화하려면 현재 Anthropic 어댑터의 구조화 출력 전달 지원을 별도 확인해야 한다. 지원되지 않은 provider에는 기존 정책을 명시하고 semantic PASS로 기록하지 않는다. 새 provider나 독립 judge를 추가하는 계획이 아니다.

## 3. 데이터/API 계약

외부 HTTP API를 새로 만들지 않는다. 아래는 앱 내부 계약이며 기존 runs JSONL/trace에 추가하는 필드다. 표에 없는 추가 필드는 거부하고(`additionalProperties:false`) 문자열/배열 타입·빈값·중복 키·유효한 enum을 엄격하게 검사한다. build/ID는 모두 앱이 발급한 목록과 대조한다.

### 앱 → Claude

- `contract_version`, `bundle_id`, `build`, `question`, `answer_branches`, `held_branches`.
- `evidence[]`: `id, full_text, source, owner, applies_to, unit, site, condition, facet, flags, relation_proof, build, text_hash`. cut 원문 미복구·source 미확인·다른 build는 투입 금지. 사실의 제한/충돌을 해석할 필수 문맥도 포함하고, 관련 반대 근거를 선택에서 숨기지 않는다.
- `requirements[]`: 앱이 만든 `requirement_id, target_key, facet, proposition, qualifiers, allowed_source_ids, mandatory, absence_proof_id?`. 개별 안전 명제·조건·고지는 각각 행으로 남긴다. 기존 required 상태를 옮기고 명시 target 의무는 유지한다. 새 임상 안전 목록을 모델이 만들어 필수 목록을 줄이게 하지 않는다.
- `absence_proofs[]`: 같은 build/target/section/condition의 실제 완료 page/neighbor/pair/global 범위와 오류 없음 증거. 전체 lookup_complete boolean 하나만 넘겨 부재를 허용하지 않는다.

### Claude → 앱: `AnswerDraftV1`

```json
{
  "contract_version": "claim_v1",
  "bundle_id": "app-issued-bundle",
  "claims": [
    {
      "claim_id": "c1",
      "text": "환자에게 보일 하나의 임상 주장",
      "kind": "role",
      "target_key": "app-issued-target",
      "unit": "app-issued-unit",
      "facet": "evidence",
      "source_ids": ["app-issued-source"],
      "requirement_ids": ["app-issued-requirement"],
      "absence_proof_id": null
    }
  ],
  "sections": [{"heading_key": "options", "claim_ids": ["c1"]}]
}
```

`kind=role|risk|condition|disclosure|absence`. 한 claim은 의미 검증 가능한 한 주장으로 제한하며, 복수 조건·독립 주장이 뭉쳐 있으면 분리 요청 또는 거부한다. `sections`는 표시 순서만 정한다. 모든 claim은 정확히 한 번 렌더되고, 나열되지 않은 claim/모르는 ID/빈 임상 claim/임의 heading은 실패다. 자유 문단·임의 인사말·미검증 임상 제목을 별도 출력하지 못하게 한다. 제목은 앱의 비임상 고정값(예: 선택지/주의할 점/확인할 점)에서 선택한다. 문진·보류 문장은 앱의 범위 상태를 이용한 고정 안내로 생성한다. 새로운 임상 내용이 필요한 안내는 claim으로 취급한다.

모델이 붙인 target/facet/requirement 태그는 **주장일 뿐 증명은 아니다**. 예를 들어 role 태그에 안전 주장이나 다른 시술을 몰래 넣어도 의미 관문에서 실패해야 한다. 부재 claim도 proof 참조와 의미/범위 확인을 모두 거친다.

### 앱 → Jev: 한 `system_one` 요청

`state={question, claims[], sources[], requirements[], absence_proofs[], policy_version}`. 출처는 ID 중복 제거해 원문과 필수 조건·한정 문맥을 보존한다. 각 claim의 `source_indices`는 앱이 ID를 매핑한 결과이며 Claude가 넘긴 본문으로 바꾸지 않는다.

1. claim마다 `relation_i: Choice`를 둔다. instructions는 `claims[i].text`와 그 claim의 `source_indices`가 가리키는 원문/조건만으로 **모든 임상 내용이 지원되는가**를 묻는다. 옵션은 `supports`, `contradicts`, `unsupported`다. 다른 claim이나 모델 상식에서 사실을 빌리지 않는다. 대상·부위·조건·부정·가능성/확실성·위험 강도·수치 분모가 달라지거나 일부만 지지되면 supports 금지다. 반대 원문이 있거나 지원/반대가 섞이면 contradicted 경로로 차단한다. 모호함은 unsupported/불확실로 처리한다.
2. 필수 명제마다 `covers_r: Noul`을 둔다. instructions는 `requirements[r]`의 명제·한정 조건이 **실제로 렌더할 claim 텍스트**에 명시적으로 남는지 묻는다. 이름만 언급하거나 source ID만 붙은 것은 커버가 아니다. 같은 요청의 relation 결과를 읽지 않으며, 답안 텍스트와 원문을 직접 본다.
3. branch/claim의 대상·조건 일치를 위한 `scope_i: Noul`을 함께 묻는다. 앱이 확인한 provenance는 그대로 요구하고 Jev의 범위 해석도 통과해야 한다. source에 없는 시술 추가나 환자별 적합성 확정, 제한 의미 누락을 거부한다.

개념 호출은 `await deps.jev.system_one(state=state, questions={relation_0: Choice(...), covers_0: Noul(...), scope_0: Noul(...), ...})`이고 응답은 기존 SDK의 `response.choices[key]`/`response.nouls[key]`에서 읽는다. 질문 ID는 모델에게 의미 있는 지시가 아니므로 instructions에 정확한 배열 위치를 쓴다. source/claim 원문은 판단 대상 데이터로 구분하고 그 안의 실행 지시는 따르지 않게 한다.

claim별 `choice, probabilities, confidence`, coverage/scope별 `noul`, 실제 `response.model`, usage·소요시간·전체/누락 질문 키, 입력 hash, policy/prompt 버전을 trace에 저장한다. `supports` 선택만으로 승인하지 않는다. 보정된 support 확률·confidence와 coverage/scope 임계값을 모두 요구하며 불확실 구간은 보류한다. 임계값은 한국어 양·음성 fixture와 독립 실물 검수로 정한다. 공식 예제의 0.8을 그대로 쓰지 않으며, 보정 정책이 없으면 자동 의역 승인은 꺼 둔다. 이 확률은 의료적 효과나 해당 문장의 정확도 보증이 아니다.

## 4. 앱 hard gate와 상태 전이

`bundle_ready → drafted → bindings_passed → semantic_passed → coverage_passed → rendered → final_validated → delivered`를 한 경로로 둔다. trace의 draft/검증 결과와 실제 최종 text hash를 묶어, 검증 후 한 글자라도 임상 문장이 바뀌면 이전 승인은 무효다.

- **bindings:** bundle/build 일치, 전달 allowlist 내 ID, 원문 hash/source/owner/applies_to/관계 방향·chain·unit/site/condition, cut 없음, claim 참조 정합을 앱이 확인한다. `owner==unit`만 요구하지 않고 edge 소유 역할과 검증된 family 안전 상속을 허용한다. scope 해석 불명확은 fail-closed다.
- **semantics:** 각 출력 claim의 supports+scope 승인. 한 문장에 근거가 있는 절/없는 절이 붙으면 전체 실패다. 인용 존재·키워드 겹침·정규식은 의미 승인의 대체물이 아니다.
- **safety/conditions:** 추천·효과를 실제 말하는 unit마다 필수 위험·금기·고지, 인용 근거의 conditional/conflict/gap/default 의미를 requirement 원장과 대조한다. 모든 필수 행은 승인 claim에 매핑되고 해당 covers 판정도 통과해야 한다. 렌더 단계에서 문장을 합치거나 조건을 삭제하지 않는다. 제목으로 추천을 추가하거나 낮은 Jev 점수로 의무를 면제하지 못한다.
- **absence:** 부재 claim의 target×section×condition과 완료 조회 증거를 앱이 대조한다. timeout/오류/전달 누락/여섯 갈래 blocked는 부재가 아니다. `retrieval_limits`는 임상 근거로 인용하지 않는다.
- **final:** 번호 인용 ↔ 내부 ID 매핑과 모든 claim 렌더 여부, 필수 coverage, 보류 목록/범위, 최종 hash를 재검사한다. 정확히 검증한 문장과 앱 안내만 내보낸다. 최종 단계 뒤 새로운 자유 텍스트나 relation 보충을 붙이지 않는다.

실패는 `draft_failed|binding_failed|semantic_rejected|semantic_uncertain|mandatory_missing|verification_error`로 남긴다. 응답 누락·NaN/잘못된 확률·키 불일치·timeout/429/529·context 초과는 PASS가 아니다. 기존 클라이언트의 실제 retry 설정과 검증 deadline을 trace에 남기고 무제한 재시도하지 않는다.

정상 생성의 형식/내용 실패는 **같은 근거만으로 최대 1회** 수정 가능하다. 실패 claim·사유·허용 ID·누락 requirement를 보내며, 새 draft를 처음부터 다시 검사한다. 예산/기한 부족이나 비용 불명확이면 수정 호출을 건너뛴다. 수정이 새로운 검색·미지원 안전 사실 생성 경로가 되어서는 안 된다.

끝내 실패하면 먼저 이미 검증된 claim만으로 닫힌 부분 답을 만들 수 있는지 본다. 실패 claim 제거가 unit 안전 커버를 깨면 그 unit의 추천·효과 claim도 함께 제거한다. 남은 unit은 모든 필수 항목을 다시 대조한다. 검증된 원자 문장의 순서 변경·번호 인용만 허용하며 새로운 축약 의역은 다시 의미 검증해야 한다.

그다음 최후 경로로 기존 exact-source 모듈을 제한적으로 재사용할 수 있다. 현재 그대로 21행 덤프를 성공 처리하지 않는다. 완전한 원문·같은 범위·필수 항목 커버·환자 안내 가능성을 모두 만족하는 짧은 묶음일 때만 `fallback_kind=exact_source`로 표시한다. 선택적 군더더기만 덜 수 있고 필수 고지를 길이 때문에 자를 수 없다. 짧은 원문 부분 답이 불가능하거나 의미 검증 장애로 환자 안내 가능성도 확인 못 하면 앱의 범위 보류 문장으로 종료한다. 원문 일치 자체도 임상 의역 PASS나 UX PASS로 올리지 않는다.

## 5. 안전 중복 제거와 표시 계층

내부 trace에는 원래 fact ID/source/path/역할 edge를 모두 보존한다. 사용자에게는 `[1]`, `[2]`와 출처 목록의 짧고 검증 가능한 이름을 보인다. 앱이 `display_number → source_ids[] → original source/owner/scope/build`를 결정론적으로 만든다. 공개 URL이 없으면 링크를 만들어내지 않고 “허브 자료 · 필러 계열 · 필수 고지”처럼 실제 메타데이터의 이름만 표시한다. 자세한 원문/내부 ID는 trace 상세로 분리한다. 번호 순서는 최종 첫 등장 순서이며 같은 출처를 재사용해도 매핑이 바뀌지 않는다.

중복 제거 단위는 문자열이 아니라 **같은 unit/site/condition의 필수 명제**다. 서로 다른 범위·확실성·시점은 합치지 않는다. 먼저 requirement를 원자 명제로 보존한 후 Claude가 각각의 환자용 문장을 만들고, 반복되는 원문 여러 개가 한 claim을 지지할 수 있게 한다. 아래는 기존 실제 답 21행의 처리 대응표다. 이 표의 행 번호와 Q002 ID는 문서·fixture 설명용이며 런타임 하드코딩 키가 아니다. 런타임 의무와 매핑은 해당 실행의 검증된 build/source/scope·필수 고지 메타데이터에서 만든다.

| 실제 답 근거 | 표현/커버 처리 | 남아야 할 원자 내용 |
|---|---|---|
| 역할 행 1 | 시술명은 검증된 unit 메타데이터로 안내, 역할 claim 1개 | 깊은 주름의 볼륨 충전이라는 근거 범위; 환자 개인 적합성 확정 금지 |
| 부위 primary risk 행 2, 고지 [0]·[1] 행 4~5 | 한 위험 단락에 원자 claim들을 배치, 같은 위험 설명 반복 제거 | 안면동맥 관련 위험·역행성 색전, 혈관폐색, 피부 괴사, 실명, 뇌졸중 각각 requirement 보존. 위험 경로를 임의로 새로 연결하지 않음 |
| risk_level 행 3 | 척도 정의/환자 의미 근거가 없으면 선택적 숫자 출력 제외 | 내부 원문은 trace에 남김; 위험 경고의 삭제 근거로 쓰지 않음 |
| 부위 통계 행 6 | 다른 부위 수치·분모가 설명되지 않으면 선택적 출력 제외 | 통계를 생략해 위험이 작다는 의미가 생기지 않게 함. 필수이면 정의/분모 확보 전 보류 |
| caveat 행 7 | 시술자 명령형을 환자용 한정·안전 설명의 원자 claim으로 변환 | 어떤 혈관 내 주입도 실명 가능, 음성 흡인이 안전 보장 아님 등 원장이 필수로 지정한 제한. 예방 수단을 안전 보장으로 바꾸지 않음 |
| 고지 [2] 행 8, 상담 항목 행 21 | 중복 상담 문장 대신 한 대비 설명 | HA 용해 가능/비HA 용해 불가의 양쪽 조건; 용해가 모든 합병증 해결을 뜻하지 않음 |
| 고지 [3] 행 9 | 한 고지 문장 | 결절·육아종·이물반응과 수개월~수년의 지연 가능성 |
| 고지 [4] 행 10, 일반 비대칭 행 18 | 같은 범위 비대칭 한 번, 나머지는 유지 | 비대칭·과교정·이동의 세 항목 |
| 고지 [5] 행 11 | 한 고지 문장 | 감염 시 농양·바이오필름의 조건과 결과 |
| 고지 [6] 행 12 | 필수로 지정됐다면 짧게 유지 | HA, 6~18개월, 개인차를 모두 보존 |
| 고지 [7] 행 13 | 한 안내 claim | 시술 전후 치과 시술 사실을 의료진에게 알림 |
| 일반 부작용 행 14~17 | 필요하면 짧은 목록 한 번 | 멍·부종·통증·홍반; 선택적 제외는 requirement 원장에 근거해야 함 |
| 준비 항목 행 19~20 | 환자에게 확인하도록 안내하되 이미 준비됐다고 단정 금지 | 혈관폐색 응급 프로토콜, 히알루로니다아제 비상 비치의 각각 확인 |

최초 구현은 Q002의 **8개 필수 고지를 모두 requirement로 유지**하는 보수적 fixture로 시작한다. 현 코드의 작은 위험 범주만 충족했다고 나머지를 조용히 빼지 않는다. 고지 중 일부를 선택적 항목으로 줄이는 정책은 본 표현 변경에 끼워 넣지 않는다. 위 표의 선택적 항목도 자동 삭제가 아니라 앱이 `justified_not_required` 사유를 남겨야 한다. claim 병합 뒤 `requirement_id → approved claim_id → source_ids → rendered span`의 대응표에 구멍이 있으면 실패다. 읽기 길이 목표보다 이 커버가 우선한다.

## 6. 검증 후 최종 전달 시각

모든 coverage 조기 종료/부분 답/수정 성공/보류를 `deliver_final(answer, final_verdict, timer, on_text)` 한 함수로 모은다. SDK delta와 CLI text는 계속 내부 buffer로만 받고, 검증 전에는 사용자 text 이벤트로 내보내지 않는다.

| 추가 timing 필드 | 정확한 경계 |
|---|---|
| `model_first_text_ms` | 기존 생성 첫 텍스트를 수신한 시각. `ttft_ms`의 과거 정의를 보존 |
| `generation_returned_ms` | 마지막 사용 생성 호출이 앱으로 반환한 시각; 첫 호출/수정별 값도 attempts에 유지 |
| `final_validation_completed_ms` | 렌더 결과와 필수 coverage·최종 hash 검사가 끝난 직후 |
| `final_on_text_started_ms` | 같은 clock에서 **실제 최종 `on_text(final_text)` 호출 직전** 기록 |
| `final_on_text_completed_ms` | callback 정상 반환 직후 기록. 예외면 null과 `delivery_error` |
| `case_completed_ms` | 전달 시도와 후처리 정리까지 끝난 시각; judge 실행 전 |
| `delivery_status` | `not_attempted|emitted|failed`; 보류라도 정상 전달이면 emitted |

모든 값은 runner 공통 `t0`의 단조 시계 경과 ms다. 최종 전달 함수는 text hash와 이벤트 수를 기록하고 중복 호출을 거부한다. 시작/종료를 별도 남겨 callback 비용을 숨기지 않는다. 이 시각은 앱의 callback/SSE 큐 전달 경계이며 **브라우저 수신·화면 표시 시각을 증명하지 않는다**. 브라우저 관측이 필요하면 별도 클라이언트 ACK 계측이 필요하고 이번 작은 구현에서는 주장하지 않는다.

현재 `_finish`의 CLI timing 사본 덮어쓰기를 고친다. 원본 CLI 반환 timing은 `provider_attempts[].timing`에 보존하고, 최종 case timing은 현재 timer에서 전달 이후 스냅샷을 만든다. CLI 전용 메타데이터만 병합하며 `stages`, final 필드, case total을 오래된 사본으로 덮지 않는다. 모든 최종 경로에서 이 동작이 같아야 한다. 기존 `total_ms`의 의미 변경은 `timing_schema_version=2`와 보고서 라벨로 표시하고 과거 CLI total과 직접 같은 지표로 비교하지 않는다. 보고에는 `generation_returned_ms`, 최종 callback 시작/완료, case 완료를 나란히 둔다. judge 시간은 별도다. 과거 누락 값은 null이며 14,601.6ms로 역산해 채우지 않는다.

## 7. 수용 fixture와 실물 관문

이번 제안에서는 테스트·provider·judge·batch를 실행하지 않았다. 구현 발주 뒤 다음을 먼저 offline fake로 검증한다.

| fixture | 기대 결과 |
|---|---|
| 원문과 어휘가 다른 한국어 정상 의역 | bindings/의미/coverage 모두 통과하고 원문 전체 복사 없이 출력 |
| 같은 단어·source ID에 부정 뒤집기, 가능→확정, 조건 삭제 | semantic 또는 coverage 실패. 단어 겹침이 높아도 승인 금지 |
| 하나의 claim에 지원 절+미지원 효과 절/효과 제목 | 전체 거부; 문장 분리로 우회 불가 |
| 다른 unit/site/family/조건, 역방향 edge, 옛 build, cut 원문, fake ID/source/hash | Hub/provider 추가 호출 없이 binding 실패 |
| edge 소유 role, 공개 chain이 증명된 family 고지 | owner가 unit과 달라도 올바른 범위는 통과 |
| 서로 반대되는 출처와 원문 속 지시 | supports로 자동 합의 금지, 충돌/미지원 기록 |
| 8개 고지와 primary risk 중 한 명제만 누락·용해 조건/개인차 삭제 | safety hard gate 실패. 인용 8개만 붙이는 답도 실패 |
| 중복 비대칭·혈관 위험 제거 | 모든 개별 requirement의 최종 span이 남으면 통과, 위험 일부 소실이면 실패 |
| 실제 범위 완료 부재 vs timeout/미전달/blocked | 전자만 해당 범위 부재 허용; 전역 “다른 시술 자료 없음” 거부 |
| 여섯 갈래 보류 + 필러 부분 답 | partial_supported만 PASS, completion은 incomplete; 새 미지원 시술 추천 실패 |
| 누락 Jev 질문, 잘못된 확률, 낮은 확신, 오류/한도, 무효 JSON | fail-closed, 최대 1회 수정 또는 안전한 부분 답/보류 |
| 번호 인용·렌더/추가 자유 텍스트 | source 대응 1:1 재현; 미검증 문장·잘못된 번호·임상 제목 삽입 실패 |
| 가짜 시계 generation=10, validation=20, callback 시작=21/종료=23, finish=24 | 각 값 정확히 저장, 오래된 CLI total=10이 final을 덮지 않음 |
| correction/repair/hold/early return/callback 예외 | 최종 on_text 1회 이하, 미시도/실패는 성공 시간으로 채우지 않음 |

가짜 Jev가 supports를 반환하는 시험은 앱 조합 로직만 증명한다. **의미 검증의 효능**은 사람이 라벨링한 한국어 정상 의역/반대/미지원·범위 전이·필수 누락 평가로 따로 확인한다. 중대 위험 누락·확실성 강화 음성 fixture의 오승인은 0이어야 하며, 정상 의역 오차단률·보류율도 공개한다. 모델/prompt/임계값을 바꾸면 해당 관문을 다시 통과한다. 독립 judge PASS는 이 fixture나 환자 가독성 검수를 대체하지 않는다.

실물 순서는 기존 Gold/앱 build 일치·격리 인스턴스·fixture PASS를 확인한 뒤 **Q002 1문항 → 대표 4문항 → 고정 50**이다. 각 단계는 기존 발주/승격 절차를 따른다. Q002는 실제 최종 답/구조화 draft/모든 판정/requirement 대응/출처 번호표/최종 timing을 함께 저장한다. 필러 역할 안내가 먼저 나오고 내부 ID·정의 없는 숫자·시술자 명령형·불필요 반복이 사라지는지 사람이 검수한다. 일반적으로 짧은 문단 3~5개를 목표로 삼되 안전 커버를 줄이거나 글자수 절단으로 통과시키지 않는다. 의료 검수와 읽기 검수는 별도 결과다.

같은 Gold 및 실행 코드 fingerprint로 baseline과 Hub/Jev 호출·bytes, Claude input/output, 생성·재작성 수, semantic 검증 시간, model TTFT, final_on_text 시간을 함께 비교한다. Q002는 1회 표본이며 지연·가격 개선을 일반화하지 않는다. 새 최종 전달 지표는 과거 값이 없으므로 “개선” 대신 최초 측정이라고 보고한다.

## 8. 공개 안전 공백과 비용·지연 위험

두 작업 원장을 분리한다.

1. **표현/계측(WP-11):** 지원된 필러 부분 답의 자연어 의역, 안전 중복 제거, 번호 인용, 최종 전달 시간. 안전·가독성 관문을 통과해도 `partial_supported_units=[U5-082]`, 전체 `completion=incomplete`를 유지한다.
2. **Gold 공개 안전 공백(별도 Hub/WORK-011):** U5-009/U5-018/U5-037/U5-090/U5-091/U5-102의 부위 주요 위험·원문/source/owner/scope/공개 관계 증거 및 일부 evidence scope 문제. 공개 projection과 같은 build 적용 증명으로 해결해야 한다. 앱 프롬프트에 위험 문자열을 박거나 Jev 상식으로 채우지 않는다. 해결 전 여섯 이름의 범위 보류는 계속 표시한다. 필러 부분 답 통과는 전체 추천 완료나 해당 시술의 효과 부정이 아니다.

정상 경로에는 **기존 생성 1회 + 최종 Jev 검증 1요청**이 추가된다. 현재 Q002 Jev 3회에 더해 보통 4회가 될 수 있다는 계획치이며 실측값이 아니다. 수정 시 생성 1회와 검증 1요청이 더 필요할 수 있다. 기존 judge 비용은 별도 유지한다. 질문은 한 요청 안에서 병렬이지만 generation→검증→전달 의존은 직렬이므로 최종 사용자 대기 시간은 늘 수 있다. 토큰 TTFT가 빨라도 실제 전달은 늦을 수 있다.

Jev state는 source를 한 번 넣고 질문에서 인덱스로 참조한다. 공식 현재 기본 한도는 state+모든 질문 64k, state+각 질문 32k이며 alias/가격/한도는 배포 시 재확인한다. 짧은 입력을 우선하고 기본 long-context 옵션을 새로 켜지 않는다. 한도를 넘으면 claim별 관련 원문·조건·requirements를 보존하는 안정된 묶음으로 나누되 전체 claim/requirement 결과를 합친 뒤에만 전달한다. 누락 묶음은 incomplete, 무음 절단은 금지다. 작은 1차 범위에서 한 요청에 맞지 않고 기한·예산도 부족하면 보류한다.

추가 비용은 실제 `response.usage`와 적용 중인 단가로 계산하고 요청 모델/실제 응답 모델/단가 기준일을 남긴다. 공식 문서의 싸고 빠른 예제를 이 앱 비용 추정치로 쓰지 않는다. 한국어·전문용어·다중 출처·긴 state의 오판, 모델 alias 이동, SDK 재시도 지연, CLI structured 누락, 출력 JSON으로 인한 생성 길이 증가가 주요 위험이다. 검증 모델과 생성 모델이 둘 다 틀릴 가능성도 남는다. 따라서 의미 검증은 provenance·안전 hard gate와 독립 의료/가독성 검수를 보강하는 관문이며 의료 정확성의 보증은 아니다.

## 9. 이번 작업 완료 범위

이 제안서만 신규 작성했다. 앱 코드/DB/서비스/정본 SPEC·WORK는 수정하지 않았고, 새 provider/judge/batch/API 평가는 호출하지 않았다. 남은 일은 코디네이터의 구현 발주, 한국어 검증 정책 보정, fixture/격리 실물 관문 수행이며 공개 안전 공백 해소는 별도 작업이다.
