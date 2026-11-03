# case3 정보 없음 계약 변경안

2026-11-02 · 사용자 검토용 초안 · 공식 SPEC 미변경

대상은 [개선 계획](info-absence-remediation-plan.md)의 계약 단계다. 기준 문서는 [SPEC-005 정본 v3.4 패치](SPEC-005.md)(0.3.5), [SPEC-006 정본 v2.8](SPEC-006.md)(0.3.8)이며, 006은 §3-4-1-3의 안전 예산과 §3-4-1-2의 역할 규칙을 기준으로 읽는다. 이 초안을 검수한 뒤 공식 SPEC과 WORK 계획으로 옮긴다. 외부 코드 변경·새 평가·원천 보강은 이 초안의 산출물이 아니다.

## 1. 근거와 범위

근거: ignored audit의 [다음 계약](../../../reference/2026-10-30-hub-evals/build-out/info-absence-audit/root-cause-next.md), [직접 근거 작업표](../../../reference/2026-10-30-hub-evals/build-out/info-absence-audit/direct-fact-worktable.md), [부분 근거 작업표](../../../reference/2026-10-30-hub-evals/build-out/info-absence-audit/partial-claims-worktable.md)와 각 CSV. 기준 실행은 `b202611020020-edc407`, Gold build `567677edfe7123e9`다. ignored 링크를 못 읽는 검수자에게는 발주 전에 지정 행의 원문·ID·trace를 별도 근거 묶음으로 제공한다.

직접 근거 45는 문장 행 수다(미전달 42, 전달 1, Gold 대응 미확인 2). 추가 trace 검토는 기존 미확정 21행 중 19행의 관측 누락 지점을 정리했고 Q067.2/Q099.1은 남았다. 관계 공백 5행은 4질문, resolve 미시드 3행은 2질문이다. 원인 하나를 고치면 질문 전체가 회복된다고 약속하지 않는다.

부분 근거 89행 중 명시 지원 Gold ID 미전달 84는 조사 후보이며 84건의 retrieval 오류 확정이 아니다. 모두 전달 3, Gold 매핑 미해결 2다. 인접 근거·적용 대상이 다른 근거를 답으로 승격하지 않는다. 범위 검색 미발견 104와 미해결 30은 별도 원천 확인 대상이며 이번 구현 분모에 넣지 않는다.

## 2. 유지할 경계와 예산

- Hub는 결정론 빌드·조회만 맡는다. 질문 해석·관련성 추측·LLM·환자별 적합성 판단을 넣지 않는다. 같은 build/정규화 요청은 같은 fact ID·순서·본문을 반환한다.
- Jev는 의도·시작 노드·이웃을 고른다. 섹션 선택·페이지 양은 앱 규칙이다. 과거 섹션 Choice를 되살리지 않는다.
- 걸음 상한 4, 일반 expand 예산 20,000B, 별도 안전 예산 8,000B, 원문 예산 15,000B, 원문 요청 상한 64 fact를 유지한다. compact UTF-8 실제 응답으로 센다. 관계 읽기를 추가하면 일반/원문 예산 중 해당 형태에 포함하며 예산 밖 우회 통로를 만들지 않는다.
- 필수 checks/site_caution 및 I-04 safety.management, 안전 요약·필수 고지·금기·gap·resolved 충돌 정책과 인용 자격을 유지한다. 안전 예산 먼저 → 일반 예산 순서와 안전 rank 절단을 유지한다. 안전 예산 절단은 기록하고 답변에서 확인되지 않은 안전성을 보장하지 않는다.
- first-page 12줄·40자 line·cut 원문 확인·quotable false 규칙을 유지한다. 잘린 문장을 추측으로 완성하지 않는다.
- 이 값은 정본 006 §3-4-1-3 및 앱 `clinic_chat/config.py`의 walk_max_steps=4, walk_byte_budget=20000, walk_safety_budget=8000, walk_full_byte_budget=15000, walk_full_facts_max=64와 대조했다. 실제 실행 settings 값이 다르면 기본값과 별도 보고한다.
- W-4 목표(정확성 ≥58%, 안전 ≥90%, 첫 글자 ≤7초)는 `_RESUME.md`의 2026-11-01 사용자 수락 기록과 `reference/2026-10-30-hub-evals/HANDOFF.md` §7의 사용자 결정에서 가져온다. 정본 SPEC-006 §7-7 W-4는 아직 열린 것으로 남아 있으므로, 다음 공식 패치에서 이 기록을 연결해 W-4를 닫고 집계 방식까지 일치시켜야 한다. 현재 SPEC에 이미 확정된 기준이라고 쓰지 않는다. 단계별 허브/Jev/원문 시간과 p50/p90을 함께 보고한다. 추가 호출 때문에 예산·걸음·시간 목표를 바꾸려면 별도 결정이 필요하다.

## 3. SPEC-005 조항별 변경

### 3.1 §1-1 · §4-3 · §5-16: 관계 fact 읽기 경로

**추천안: 기존 pair_check를 case3의 관계 조회 출발점으로 채택하고, node section에 관계 원문을 복제하지 않는다.** edge owner를 node라고 바꾸거나 expand fact_ids 검증을 풀지 않는다. 다만 현재 T4 한 응답으로 아래 최소 칸을 모두 받는 계약은 성립하지 않는다. 대안별 출처·생략된 단위 쌍 ID·Q139 전역 메모의 접근은 신규 응답 계약 또는 별도 읽기 경로의 열린 결정이다.

추가할 규범 문구:

> 관계 fact는 node section fact와 별도로 읽을 수 있어야 한다. 확정된 정본 단위 쌍으로 조회한 응답에서 적용 대상 쌍, resolved 값, 해당 관계 주장 fact ID/text/source, 대안별 값·출처, 안전 표시를 검증 가능하게 연결한다. 이 칸을 현 T4가 제공하지 않으면 미수신으로 남기고 신규 계약으로 지정한다. 관계 없음은 그 단위 쌍의 범위 조회가 완료된 경우에만 기록하며 조회 실패·잘림·예산 차단과 구별한다. 구조 edge 존재만으로 원문·수치·권고를 새로 생성하지 않고 기존 resolved 값과 원문 주장의 역할을 뒤집지 않는다.

006이 Jev/resolve에서 확정한 대상 쌍만 넘긴다. Hub는 비교 대상을 추측하지 않는다. 현재 T4는 계열/제품 입력을 단위로 펼치므로 앱은 실제 반환된 단위 쌍과 입력 provenance를 확인한다. fact 단위 출처와 대안별 provenance가 최종 입력까지 보존돼야 한다. 현 응답에서 확인되지 않는 출처를 `source` 한 칸이나 대안 개수로 대신하지 않는다.

Q139의 `scope:all#evidence#step8_notes[26]`은 관계 R8과 owner가 다르다. 현재 T4 `relations_all.global`은 `#sequence_rank`만 고르고, `pair_check.global`은 procedure_relation 전역 행을 담으므로 이 메모의 조회 경로가 확인되지 않는다. 전역 메모의 fact ID/text/source, 적용 쌍·범위, 우선순위와 인용 자격을 반환하는 읽기/부착 계약이 필요하다. R8 두 개의 수신만으로 Q139 전체를 닫지 않는다.

pair_check 재사용의 구체 제약은 정본 §5-5와 A1-6을 따른다. 입력 정본 ID 목록(1~6), 동일 ID 두 번의 자기 쌍, 계열/제품→단위 펼침을 보존한다. 요청 중복 제거 키는 build·정규화 입력·prior/sub_condition/include_conditional/sections를 포함한다. 양방향 쌍은 조회 중복에만 정규화하고 출력 a/b·value.first와 by_direction은 원 응답 방향을 보존한다. 실제 응답의 expanded/pairs를 읽으며 계열 ID 두 개만으로 한 단위 쌍을 가정하지 않는다.

현재 T4의 세 형태를 구별한다. 기본 응답은 주장 원문 ≤2/쌍이고 `alternatives`는 **개수**다. `value.options`·`by_direction`의 `from/rule`도 빠진다. `sections=evidence`는 주장 원문을 전부 싣지만 짧은 응답이므로 대안은 여전히 개수이고 `from/rule`도 복원하지 않는다. `sections=all`은 대안 목록과 `from/rule`을 보존하지만 응답 전체가 커지며, 대안 각각의 fact ID/text/source 연결이 충분한지는 별도 검증해야 한다. 세 형태 모두 `pairs[]`의 resolved·claims·reasons와 실제 출처 연결을 지정 R8 ID별로 검증한다. edge fact는 node `expand(fact_ids)`로 받을 수 없다.

현재 펼침 잘림 칸은 `pairs_more` 목록이 아니라 `pairs_more_n` **개수**다. 짧은 응답에서는 같은 내용의 단위 쌍을 묶어 `pairs[]` 항목이 `a/b` 대신 `pairs:[[a,b],…]`를 가질 수 있다. 따라서 개수만 보고 특정 필수 쌍이 생략됐다고 단정할 수 없다. 질문에서 정본 **단위 쌍**이 이미 확정됐으면 그 두 ID로 좁혀 T4를 재호출해 해당 쌍의 실제 반환 여부를 검사한다. 계열/제품 펼침 뒤 단위 쌍 자체가 미확정이면 `unresolved_pair`로 남겨 006의 대상 해석을 먼저 끝낸다. 생략된 쌍 ID 목록이 필요하다면 T4 신규 응답 칸으로 계약하고, 현재 `pairs_more_n`을 그 목록처럼 사용하지 않는다. 대상 R8 ID가 claims/reasons 등에도 없으면 `missing_fact_id`로 남기고 임의 ID를 주입하지 않는다.

관계 기본 호출은 일반 20KB, `sections=evidence` 및 `sections=all` 추가 호출은 원문 15KB에 각각 **전체 compact 응답**을 귀속하는 안을 추천한다. 요청 전에 예측 크기/남은 예산을 기록하고 알려진 크기가 잔여 예산을 넘으면 호출하지 않는다. 크기를 보장할 수 없어 호출했다면 응답 수신 뒤 실제 바이트·지연을 기록하고, 전체가 해당 잔여 예산 이하일 때만 채택·차감한다. 초과 응답은 통째로 배제하며 그 안의 resolved·대안·원문·출처 어느 것도 최종 입력이나 인용에 쓰지 않는다. 다른 예산으로 재귀속하거나 필요한 fact만 골라 채택하지 않는다. 필수 관계가 이 때문에 미수신이면 `blocked_budget`이고 `enough` 금지 및 §4.2·§4.5의 부분 답변 규칙을 따른다. 64는 node `expand(fact_ids)` 요청 상한이지 T4 상한이 아니다. T4의 선택적 원문 조회·응답 크기 제한은 신규 계약 결정이며 예산을 늘리는 이유로 삼지 않는다.

### 3.2 §5-16: 기존 페이지 계약 명확화

`page≥1`, section당 12줄 및 기존 정렬을 유지한다. 앱은 section 하나씩 요청한다. `more[section]`은 **요청한 페이지 뒤**에 남은 fact 줄 수이며 0이면 칸이 생략된다. 다음 페이지 존재와 section 전체 수신 완료를 구별한다. 각 요청의 node/section/page와 요청 페이지 fact IDs를 기록할 수 있어야 한다.

다음 쪽 바이트는 1쪽 peek bytes로 추정하지 않는다. 추천은 결정론 page metadata(`page`, `page_size`, `remaining`, `next_page`, `next_page_bytes`)를 section별 제공하는 것이다. `next_page_bytes`는 다음 쪽 기본 응답의 compact 봉투 포함 크기이며 그 응답에 포함되는 metadata까지 고려해 계산한다. 필드 추가로 기존 1쪽 응답 바이트는 달라질 수 있으므로 기존 186호출의 **ID 순서** 보존과 새 bytes 정확성을 각각 검사한다. 새 metadata를 도입하지 않으면 앱은 실제 응답을 받은 뒤 초과 결과를 제외하는 기존 규칙을 적용하되 낭비 호출의 시간 비용을 보고해야 한다(선택 필요).

### 3.3 §4-3 · §6-7 · §7

Q226.2/Q229.2는 source→Gold 누락 확정으로 적재 규칙을 추가하지 않는다. 원장 명제의 구조 edge 표현 여부와 기존 fact 매핑을 먼저 확인한다. 이미 표현돼 있으면 접근 계약, 표현이 없고 빌드 규칙 대상임이 확인되면 그때 특정 원천 경로의 빌드 규칙 변경으로 분리한다.

§6-7에 아래 결정론 관문을 추가하고 §7 X-10 상당 관계 공백·페이지 의존을 닫는 조건으로 연결한다. 과거 「허브 꼴로는 더 못 닫는다」는 설명은 관계 접근 공백과 앱 선택 문제를 분리한 현재 분류로 갱신한다. 과거 수치를 새 개선 실적으로 덮어쓰지 않는다.

## 4. SPEC-006 조항별 변경

### 4.1 §3-4-1-2 · §3-4-1-3 · §3-4-2: 페이지 수신 상태와 수집 순서

`taken[node] = section 집합`을 `received[(node, section, page)] = accepted fact IDs/bytes`와 `pending_pages[(node,section)]`로 바꾼다. 1쪽 수신은 section 완료가 아니다. 동일 tuple 재요청은 재시도 사유가 있을 때만 허용하고 fact ID 중복은 최종 입력에서 제거한다.

추천하는 결정론 수집 순서:

1. 기존 필수 안전 묶음과 상위 3 시술 안전 섹션을 안전 8KB에서 먼저 받고, 시작/선택 노드의 의도 묶음 1쪽을 일반 20KB에서 받는다. 각 실제 응답의 compact 바이트는 해당 호출 예산에 전부 차감한다. 최종 fact ID 중복 제거로 응답 바이트를 환급하지 않는다.
2. 걸음 중에는 다음 필수 대상의 최초 의도 묶음 수집을 페이지 추가보다 앞에 둔다. Jev 이웃 선택·4걸음 상한은 유지한다.
3. 걸음 종료 후 fill에서 방문 노드의 의도 묶음 중 잔여 페이지를 노드 최초 방문 순 → 의도 섹션 순 → page 오름차순의 한 순회당 한 쪽씩 받는다. 각 묶음이 빈 경우에는 기존 미수신 섹션 1쪽 fill을 따른다. 이후에도 예산이 남으면 같은 순서를 반복한다. 질문별 정답 ID·키워드로 page를 건너뛰지 않는다.
4. 새 page 응답이 예산을 넘으면 그 응답을 채택하지 않고 tuple에 `excluded_budget`를 남긴다. 실제 호출 바이트·지연은 남기고 더 작은 다른 작업은 계속한다. 원문은 채택한 fact의 cut 줄만 기존 15KB/64 상한 안에서 받는다.

이 순서는 **제안한 정책**이며 4~7쪽 회복을 보장하는 관측 사실이 아니다. Q160처럼 먼 페이지가 예산 내 도달하는지는 결정론 비용 검증에서 판정한다. 초과 시 예산을 몰래 늘리거나 그 사실이 없다고 답하지 않는다. 안전 섹션의 다음 쪽은 안전 8KB 안에서만 수집하고 rank 절단을 유지하는 안을 추천한다. 안전 추가 페이지의 우선순위와 일반 예산 전용 여부는 제품 정책으로 열린 채 두며 §6의 추천안대로 검토한다.

페이지 상태 기계는 `pending → accepted_more | complete | excluded_budget | error_terminal | deadline | no_progress`로 정한다. accepted_more는 다음 tuple을 pending으로 만들고 현재 tuple을 종결한다. complete는 해당 범위의 조회가 끝나 `more=0`(칸 생략)인 **채택 응답**에만 붙인다. excluded_budget/error_terminal/deadline은 이번 실행의 terminal이며 section 전체 완료를 뜻하지 않는다. 예산은 줄기만 하므로 excluded_budget tuple은 재시도하지 않는다. 중복 fact ID가 있어도 요청 page가 증가하고 응답·remaining이 정합하면 페이지 진전으로 센다. page가 전진하지 않거나 동일 tuple이 반복되거나 remaining이 진행과 모순되는 경우에만 `no_progress`로 종료한다. pending 작업 한 순회에서 신규 fact·페이지 진전·대상 상태 변화가 모두 없으면 fill을 종료한다. stop은 범위 조회로 확인된 `empty`와 구별해 `no_progress`를 추가하는 안이다.

페이지/관계 추가 호출의 자동 재시도는 이번 안에서 0회로 추천한다. 다음 사용자 질문은 새 실행이다. 전송 실패는 error_terminal, 시간 만료는 deadline으로 남기며 수신 전 taken을 완료 처리하지 않는다. 추가 수집에는 전체 retrieval deadline과 호출별 timeout을 적용하고 남은 시간이 없으면 호출하지 않는다. 숫자 deadline은 승인 근거가 없으므로 WORK 발주 전 확정할 결정이다. 7초 TTFT 목표를 새 7초 HTTP timeout이라고 해석하지 않는다. 시간값 미확정 상태에서 무제한 재시도/수집 구현을 승인하지 않는다.

안전 수집 **제품 정책 추천안**: 첫 안전 대상(rank 상위3+시술 시작 노드)의 기존 필수 안전 **1쪽을 모두 시도한 뒤** 안전 추가 페이지를 처리한다. 다음 걸음에서 새 시술이 rank 상위3에 들어오면 rank를 재계산해 미수신 1쪽을 안전 잔여 예산으로 먼저 시도한다. 이미 수신한 응답 바이트는 rank 하락으로 환급하지 않는다. 남은 예산이 없으면 rank와 cut 사유를 기록한다. 추가 페이지는 갱신된 rank 순→section 기존 순→page 순, 한 순회당 한 쪽이며 이후 일반 fill로 간다. 최초 안전 1쪽보다 먼 안전 페이지를 먼저 받아 다른 대상 안전을 밀지 않는다. 이 순서·rank 갱신 시점·일반 예산 사용 여부는 관측 사실이 아니며 사용자 결정 전에는 구현 확정 정책이 아니다.

### 4.2 §3-4-1 · §3-4-6: 질문 대상과 resolve 후보 보존

resolve 후보 전부를 강제 방문하지 않는다. Jev 시작 선택 입력/출력에 `question_targets[{span, role, candidate_ids, selected_id?, status, basis}]`를 추가한다. `span`은 질문의 실제 표현 구간, `role`은 그 구간이 명시 질문 대상/비교 상대/동의어 대안/미확정 중 어디에 해당하는지, `basis`는 질문 표현과 resolve 후보·선택을 연결한 입력 근거다. 질문에 두 대상이 명시된 비교는 두 구간을 별개 필수 대상으로 기록한다. 같은 span의 경쟁 동의어 후보는 함께 방문할 의무가 아니다. entity 해석은 앱/Jev가 하며 Hub는 후보를 유지한다. span·role·selected_id를 확정하지 못하면 임의 후보를 필수 대상으로 꾸미지 않고 `ambiguous`를 `unresolved`에 전파한다.

필수 대상의 선택 ID가 시작 노드와 다르면 대기열 seed로 보존한다. 후보가 모호하면 Jev가 고르게 하거나 `ambiguous`로 남긴다. queue 항목은 `{node, target_key?, origin: resolve|neighbor|by_unit, parent?, edge?, state}`를 갖고 동일 node 중복은 합치되 target provenance는 잃지 않는다. seed는 시작 뒤에 명시 대상 순서로 넣는 것을 추천한다. 기존 neighbor 순서표 자체를 감사 표본에 맞춰 재학습하지 않는다.

대상별 상태는 `pending / received_supported / unresolved / blocked`로 기록하고 facet마다 상태·근거 ID·사유를 별도로 둔다. 최소 수집 범위는 대상별 `required_sections`와 질문 항목별 `required_facets`로 명시한다. required_sections는 005 §5-14′의 해당 intent 기본 묶음 및 기존 안전 섹션이다. I-06 비교는 **양쪽 각각** 같은 묶음과 질문이 요구한 facet을 검증한다. I-07/08은 단위 쌍 확정 뒤 해당 쌍의 resolved·claims·방향·대안·출처 및 관계 적용범위를 검증한다. 단위 쌍 확정 전 T4를 필수 쌍 조회로 성공 처리하지 않는다. 질문에서 별도 요구한 duration/aftercare 등 facet은 대상과 연결해 입력에 보존하되 Jev가 수집 양을 정하지 않는다.

`received_supported`는 필수 대상의 required_sections 첫 페이지가 채택되거나 확인된 empty이고, 필수 facet마다 적용 범위가 맞는 인용 가능 원문 fact가 채택되며, 해당 facet에 요구되는 resolved/대안·방향·출처가 확인된 때만 붙인다. 한 fact 수신, 무관한 fact 수, 첫 페이지만의 수신 자체, 또는 미확인 사유 기록은 충족이 아니다. `empty`는 정해진 대상·section·쌍의 범위 조회가 끝났고 `more=0` 또는 동등한 완료 신호가 채택됐으며 해당 범위에 fact가 없을 때만 쓴다. 확인된 empty라도 필수 facet의 지원 fact는 아니므로 `unresolved_absence`로 남겨 enough를 열지 않는다. 후보/역할/단위 쌍 미확정, 필요한 facet의 조회가 남은 partial, 미수신, 대안 출처 미확인은 `unresolved`와 해당 사유로 남긴다. steps·budget·error·deadline·no_progress로 더 읽을 수 없으면 `blocked`와 제한 사유를 기록한다. `enough`는 기존 Noul≥0.8·일반 예산80% 조건에 더해 **모든 필수 대상의 모든 필수 facet이 received_supported**일 때만 허용한다. 필수 대상 하나라도 pending/unresolved/blocked이면 금지한다. 추가 경로가 없으면 `incomplete`로 종료하고, 4걸음·예산 등 hard stop은 그대로 지키며 남은 pending을 blocked로 전환한다. queue 전체 소진은 요구하지 않지만 필수 대상의 미방문 queue 항목은 충족으로 간주하지 않는다. 종료 사유·대상/facet별 미충족 사유를 답변 입력에 전달한다.

### 4.3 §3-4-2 · §3-4-3: 관계 읽기와 fallback

관계 의도/명시 비교 질문에서 **단위 쌍까지** 해석된 경우에만 §3.1 경로로 읽는다. 관계 조회도 trace·예산·원문 자격의 대상이다. 현재 fallback 조건(no_start/peek_failed/no_facts)은 유지하며 모든 미완료 질문을 fallback으로 우회하지 않는다. 추천은 유효한 단위 쌍 확정 직후 걷기 중 결정론 보조 호출로 T4를 쓰는 것이다. 동일 정규화 쌍·동일 요청 형태의 중복 호출은 막되, 기본/evidence/all은 서로 다른 조회로 기록한다. 필수 관계가 조회 실패·잘림·예산 차단·출처 미확인 상태이면 `received_supported`로 승격하지 않는다.

### 4.4 §3-4-4 · §4-2 · §4-4: trace와 검증

추가 필수 칸은 `targets`(span/role/basis/selected_id와 대상·facet별 상태), `queue_seed`, queue 항목의 origin/처리 상태, `coverage_at_stop`, `enough_blocked_reason`, `pages[]{node,section,page,next_page,remaining,request_bytes,response_bytes,accepted,fact_ids,exclusion_reason}`, `relations[]{pair,tool,sections,request,fact_ids,resolved,alternatives_status,provenance_status,response_bytes_actual,accepted_budget_bytes,ms,status,exclusion_reason}`다. 관계의 호출 전 예측 크기/잔여 예산, 호출 후 compact 전체 크기, 응답 채택/배제와 예산 소유권도 기록한다. fill/required/base_bundle도 node/section/page를 기록한다. section별 more 합계는 참고치만 유지한다.

검증기는 받은 tuple 중복, page 누락(이유 없는 건너뛰기), 동일 Gold ID의 본문 불일치, 실제 bytes 차이, 일반/안전/원문 상한 초과, 배제 응답의 fact가 최종 입력·인용으로 들어간 판, 필수 facet이 `received_supported`가 아닌데 enough 종료한 판을 실패로 센다. 강제 종료에 blocked 사유가 있는 판은 수집 미완료로 보고하며 잘못된 enough와 혼동하지 않는다.

### 4.5 §3-4-7 · case3 답변 계약 · §5: 부분 답변

추가할 규범 문구:

> 질문의 항목별로 입력에 있는 인용 가능한 근거부터 답한다. 유보는 근거가 전달되지 않았거나 적용범위가 확인되지 않은 항목에 한정한다. 조회 미완료를 원장 전체의 부재로 단정하지 않는다. 일반 원천 사실과 개인별 적합성·장비/제품별 조건을 분리한다. 안전 사실과 필수 표시를 유지한다. 인접 시술·다른 제품·응급 프로토콜을 원 질문의 직접 근거로 바꾸지 않는다.

최종 입력에 `retrieval_limits[{target,facet?,section?,pair?,reason,stop}]`를 추가한다. 이 칸은 수집 한계를 뜻하며 의료 사실 근거로 쓰지 않는다. 필수 관계의 T4 `sections=evidence`/`all` 전체 응답이 원문 잔여 예산(최대 15KB)을 넘어 배제됐으면 해당 쌍·facet을 `blocked_budget`로 표시하고 배제된 응답의 resolved·원문·대안을 인용하지 않는다. 이미 **별도로 채택한** 지원 fact로 답할 수 있는 항목만 답하고, 막힌 관계 항목은 “이 두 대상의 관계는 이번 조회의 자료 한도로 확인하지 못했습니다”처럼 특정한다. 필수 관계만이 질문의 전부이면 확인되지 않은 관계 값을 추정하지 않는다. 일반 예시도 “확인된 내용은 A입니다. B의 구체 조건은 현재 받은 자료로 확인이 필요합니다”처럼 항목 범위를 특정한다. 조회 차단을 관계 자체가 없다는 뜻으로 쓰거나 전체 질문에 “정보 없음”을 붙이지 않는다. 자연스러운 표현은 허용하며 문자열 삭제만으로 통과시키지 않는다.

§5의 답변 검수는 (a) 지원 사실을 실제로 답함 (b) 남은 유보 범위가 정확함 (c) 적용 대상·환자별 판단·인접 근거를 혼동하지 않음 (d) 안전 누락 없음으로 분리한다. 부분 89행 전체를 오답 분모로 삼지 않는다.

## 5. 수용 기준과 대표 고정 사례

아래 표는 최소 회귀 묶음이다. 구현 WORK는 직접 45행 전부의 수정 대상/비대상/미확정을 고정한 manifest를 만들고 전 행 근거 관계를 검수해야 한다. 대표 사례 통과로 45행 전체 회복을 주장하지 않는다.

| 관문 | 사례와 fact | 통과 조건 |
|---|---|---|
| 관계 접근 | Q018.1 `R8-0163`, Q064.1 `R8-0075`, Q139.1/2 `R8-0218`/`R8-0219`, Q173.1 `R8-0111` | 확정 단위 쌍의 기본/evidence/all 실제 반환 칸·전체 바이트·채택 여부를 대조해 ID·원문·출처와 resolved/대안별 출처를 확인. 현재 계약이 못 주는 칸은 신규 계약 미완료로 실패 처리. Q139 전역 메모는 별도 검증. 5문장/4질문으로 보고 |
| 페이지 | Q085.2 `SE-M9-05#incidence`(M9 side_effects 2쪽); Q098.1 `product:M11-1-1#aftercare#extracted[M11-1-1].source_text.aftercare[2]`(U5-110 2쪽) | 같은 Gold 정렬에서 위치 재현, 수신 tuple·ID·원문 연결. 결정론 페이지 경로 접근과 실제 앱 예산 내 수신을 별도 판정 |
| 먼 페이지 | Q136.1 `product:M8-2-4#aftercare#taxonomy_products[M8-P-5].source_text.aftercare[1]`(U5-027 4쪽); Q160.1 `product:auto-M8-1775364775126#safety.side_effects#extracted[auto-M8-1775364775126].source_text.safety.common[1]`(U5-100 4쪽), 같은 product의 `#safety.side_effects#product_links[auto-M8-1775364775126].side_effect_override[0].values.common[1]`(7쪽) | 건너뛰기 없는 페이지 수신/미수신 사유, 실제 예산 검증. 예산 내 회복 못 하면 해당 사례 미해결로 남김 |
| queue | Q015.1 `combo:RC-CP-lifting#evidence#members[0].attrs_text.duration` 및 `[1]`; Q072.1/2 `product:M9-1-3#method#step9[taxonomy.modality[8].subcategories[0].items[2].extracted.mechanism]` | pending 대상이 있으면 enough 금지. Q015 비교 양쪽을 각각 검증하며 queue 하나 회복으로 전체 비교 통과하지 않음 |
| resolve | Q069.1/2 `product:M4-1-1#method#step9[taxonomy.modality[3].subcategories[0].items[0].extracted.mechanism]`; Q173.2 `family:M15#method#step9[taxonomy.modality[14].extracted.mechanism]` | span/role에 따른 대상 seed 및 실제 수신/blocked 추적. 경쟁 동의어 후보 전체를 강제 방문하지 않음 |
| 복합 원인 | Q004.2 U5-070 overview 17번째, Q237.2 `family:M1#overview#step9[taxonomy.modality[0].extracted.indications.extended[9]]`(3쪽) | node 선택 회복과 다음 페이지를 모두 검증. steps 한도 유지 시 blocked가 정확히 남고 전체 부재 단정 없음 |
| 전달 후 답변 | Q004.1 `SE-M14-07#incidence`/`#management`/`#mechanism`/`#prevention` | 전달 사실 중 질문에 적용 가능한 내용 실제 사용. 같은 사실을 다시 없다고 하지 않음 |
| 부분 답변 | Q021.1 `K8-0066`/`K8-0115`; Q058.1 `family:M4#overview#family_text[환자 설명 가이드(patient-education)][0].pain_level`; Q122.2 U5-045 side_effects common[3]의 작업표 두 ID | 이미 전달된 지원 범위와 남은 유보를 분리. 환자별 결론 생성 없음 |
| 잘못된 확대 금지 | Q017.1/2 `R8-0146`/`#reason`; Q050.1 `site_caution:SC-glabella-M2#site_caution#spec.emergency_protocol`; Q147.2 U5-023/U5-099 pih_rate | RF/HIFU→소프웨이브, 응급용해→통상 미용용해, 토닝 owner→제모 PIH로 전이하지 않음. Q147 owner 정합성 확인 전 수혜 실적 제외 |
| 미확정 유지 | Q067.2, Q099.1; Q226.2/Q229.2; 부분 Q166.1/Q214.1 | 대상 동일성·구조 edge·Gold 매핑 확인 전 확정 개선/원천 공백으로 세지 않음 |

공통 결정론 관문: 기준 build의 기존 186 section 호출 1쪽 ID 순서 보존, 같은 요청 두 번 ID/본문/metadata 동일, byte 일치, 수신 ID와 최종 인용 가능 원문 대조, safety.management 회귀 없음. 새 빌드에서는 차이 manifest와 이유를 함께 남긴다.

예산 회계는 세 장부로 분리한다. (1) `response_bytes_actual`은 compact 응답 전체로, 제외·중복·실패 후 재수신도 호출별 기록한다. (2) `accepted_budget_bytes`는 채택한 호출 응답 전체를 단일 소유 예산(safety/general/full)에 차감한다. 초과로 제외된 호출은 actual에는 남고 accepted에는 넣지 않는다. 관계 기본은 general, evidence/all은 full 소유로 **호출 전** 고정한다. 응답 크기를 모르면 잔여 예산을 확인한 뒤 호출하되 전체 실제 크기가 넘으면 통째로 배제한다. (3) 최종 fact 집합은 ID로 중복 제거하되 수신 바이트를 줄이지 않는다. 따라서 accepted 상한 준수와 실제 네트워크량/지연은 별도 지표다. 배제 응답의 어떤 필드도 인용 자격을 얻지 않는다. safety 섹션을 이미 수신했으면 일반 base/fill은 동일 tuple을 요청하지 않고 기존 fact를 참조한다. 혼합 응답은 요청 전 하나의 소유 예산을 고정하며 사후 유리한 예산으로 옮기지 않는다.

그다음 직접 미전달 42행을 개별 재생해 수신/원문/답변을 각각 판정하고, 부분 지원 89행은 의미 범위 검수를 먼저 한다. 첫 작은 실행은 기존 sample50 case3 한 번이다. 핵심 지표는 직접 근거가 있는데 부재라고 답한 문장 건수와 질문 수를 따로 기록하며, 안전·정확성·첫 글자·예산·비대상 회귀를 함께 본다. sample50 분모는 기존 sample50-questions.txt의 고정 50 QID이며 중간 누락·오류·timeout도 제외하지 않는다. 같은 baseline 50과 현재50을 짝지어 지원 사실 부재 주장/안전/정확성/TTFT를 비교한다. 50에서 개선된 QID만 골라 분모를 줄이지 않는다. **검토용 승격 추천**은 신규 안전 오류·필수 고지 누락 0건, 예산/인용 위반 0건, 직접 근거 부재 주장과 정확성의 짝 비교 개선을 확인하고, TTFT는 같은 집계 방식의 p50/p90 및 7초 목표 대비 변화량을 제시해 사용자 판단을 받는 것이다. 허용할 정확성 최소 개선 건수/비율과 TTFT 악화 폭은 승인 근거가 없으므로 수치를 만들지 않는다. 새 안전 오류·고지 누락·지연 악화가 확인되면 전체 승격을 멈추고 원인을 검토한다. W-4의 182×2 평균 기준을 50×1에 그대로 대입해 최종 합격으로 선언하지 않는다. 고정50 결과·안전/지연 판정·승격 결정을 사용자 리뷰에서 확정한 뒤에만 239×3 전체 평가를 발주한다. fullrun-v2 안전 87.5% 미달은 기준선으로 병기하고, 50 한 번으로 90% 달성을 주장하지 않는다.

## 6. 의존성과 사용자 결정 항목

| 순서/결정 | 추천과 남은 확인 |
|---|---|
| 기준판 정합성 | 정본 005 0.3.5(v3.4 패치)와 006 0.3.8(v2.8)을 사용한다. G20 safety.management 이동과 006 안전 8KB를 유지하며 발주 기준 commit/build/settings를 고정한다 |
| 관계 읽기 방식 | 기존 pair_check를 출발점으로 추천. 기본/evidence/all의 실제 칸과 비용은 §3.1대로 구분. 대안별 출처·생략 쌍 ID는 현 API에서 확인 불가하므로 신규 칸/전용 읽기 모드 중 결정. 15KB 안에 필요한 관계만 받는 선택 조회가 없으면 필수 facet은 blocked로 남김 |
| 전역 관계 메모 | Q139 `scope:all#evidence#step8_notes[26]`은 현 T4 `relations_all.global`의 sequence_rank 선택 범위 밖이다. 적용 쌍·원문·출처를 검증 가능한 별도 읽기/부착 경로 결정 필요 |
| 다음 페이지 비용 | page metadata 추가 추천. 응답 봉투와 bytes 정확성·호환성 검수 필요. metadata 없이 실제 호출 후 제외하는 대안은 호출 시간 검증 필요 |
| 페이지 우선순위 | 대상 최초 묶음→의도 묶음 페이지 round-robin→미수신 section 1쪽 추천. 안전 추가 페이지는 1쪽 대상 완료 뒤 rank 순·8KB 안에서 처리하고 새 상위3 대상은 1쪽 우선하는 안을 사용자 판단에 부침. 일반 예산으로 안전 절단을 보충할지는 열린 제품 정책 |
| 대상 seed/충분 | 질문 span·비교 역할·resolve 연결 근거로 명시 대상만 seed 추천. 모호한 대상/단위 쌍은 unresolved이며 모든 필수 facet의 received_supported 전에는 enough 금지. 미지정 인접 후보는 기존 Jev 선택 유지 |
| hard stop 뒤 수혜 범위 | 4걸음·일반20KB/안전8KB/원문15KB 유지. 관계 전체 응답이 원문 잔여 예산을 넘으면 통째 배제하고 필수 facet blocked, enough 금지, 채택 사실만 부분 답변. Q004.2·Q160 등도 미완료 가능하므로 수혜 건수 약속에서 제외 |
| 50 승격/시간값 | 50×1은 진단 관문이다. 안전 오류·고지 누락·예산/인용 위반 0건을 추천하고, 정확성 최소 개선량과 TTFT p50/p90 허용 악화 폭은 사용자 결정. 추가 수집 deadline·호출 timeout 숫자, T4 선택 원문 계약도 확정 필요. 승인 전 새 숫자 문턱을 만들지 않음 |
| 성능 예산 | 호출 추가량·TTFT 영향을 결정론 비용 표/개별 재생에서 확인. 7초 목표의 기존 집계 방식과 동일하게 비교하고 실패하면 정책 재검토 |

공식 SPEC 검수 → 사용자 WORK 계획 리뷰 → runbook에 따른 Hub/앱 워커 발주 순이다. Hub 관계 응답 계약이 먼저 확정돼야 앱 관계 어댑터를 만들 수 있다. 앱 페이지/trace 설계는 기존 page 계약으로 준비할 수 있으나 새 metadata 의존 구현은 Hub 패치 뒤다. 답변 범위 계약은 전달 사례 3행과 Q004.1로 독립 검수할 수 있다. 원천 보강은 source/owner 검수와 출처 확보 뒤 별도 WORK로 분리한다.

## 7. 이번 검수 항목 처리

| 항목 | 이번 초안 처리 | 남은 결정 |
|---|---|---|
| F-1 / W-1 | T4 기본/evidence/all의 실제 반환 차이, `pairs_more_n`, Q139 전역 메모 공백을 명시 | 대안별 출처·생략 단위 쌍 ID·전역 메모의 신규 읽기 계약 |
| F-2 / W-3 | 대상·facet별 `received_supported`와 미수신/미확정/차단을 분리하고 필수 facet 미충족 시 enough 차단 | span/role/선택 ID의 입력 근거 및 모호성 해소 구현 검수 |
| F-3 | 관계 호출 전후 바이트 귀속, 전체 응답 채택/배제, blocked·인용 금지·부분 답변을 연결 | 15KB 안의 선택적 T4 원문 계약 및 제품의 hard stop 답변 범위 |
| W-2 | `more`의 페이지 뒤 잔여 의미와 합법적 중복 ID의 페이지 진전을 고정 | page metadata 도입 여부·바이트 정확성/호환성 |
| W-4 | 고정 50×1을 진단 관문으로 두고 안전·인용 위반 0건을 추천 | 정확성 최소 개선량, TTFT 허용 변화, 239×3 승격 수치 |

안전 추가 페이지 우선순위·일반 예산 사용 여부, 추가 호출 deadline/timeout도 사용자/계약 결정으로 남는다. 이 초안만으로 공식 SPEC 패치나 전체 평가 수혜를 확정하지 않는다.
