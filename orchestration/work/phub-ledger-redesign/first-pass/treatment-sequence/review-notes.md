@@header
# treatment-sequence.json — 1차 조사 (읽기용)

> 이 문서는 **원문 대응**과 **잠정 관찰**을 나눠 적는다. 원문 값 표(§2~§8의 「원문 값」)는 build.py 가 원본에서 자동 생성한 것이고, 「잠정 관찰」 절은 직접 읽고 쓴 해석 후보다. 잠정 관찰은 확정 의미·관계가 아니다. 공통 개념 ID·동의어·부위 체계·관계 방향은 정하지 않았다(1차 범위 밖).
> 원문의 임상·법적 주장(간격 일수, 근거 문헌, 금지 사유 등)은 **원장에 적혀 있다는 사실**로만 기록한다. 사실 여부는 검증하지 않았고 외부 자료로 보충하지 않았다.

**상태**: 1차 범위 종료(조건 충족, 코디 확인 전) · **원장 전체 완료 아님** — 미결은 [issues.md](./issues.md).

## 0. 원본과 기록 위치

| 항목 | 값 |
|---|---|
| 원본 | `orchestration/work/phub-recommend/bronze/phub-ledger/treatment-sequence.json` |
| 크기 | 8,964 bytes · 5,208 code points · UTF-8 · BOM 없음 · 개행 0(한 줄) · 백슬래시(이스케이프) 0 · BMP 밖 문자 0 |
| sha256 | `e2f74d41d75a0b4b9d1f6216ccc17402af64bbd455b1c1627395a819ce76cfaf` (작업 시작·build·verify·작업 끝 동일. 원장 폴더 `HASHES.txt` 의 접두 `e2f74d41d75a0b4b` 와도 일치) |
| 구조·값 | [source-map.json](./source-map.json) — 노드 255(전부), 키 출현 142, 필드명 22종 출현 위치, 중복 키 0 |
| 형태소 | [morphology.json](./morphology.json) — 문자열 164 중 분석 155 / 제외 9(사유별), 비문자열 말단 20, 필드명 22, 토큰 1,429 · 오분절 출현 기록 69([segmentation-review.json](./segmentation-review.json)) |
| 복합 표현 | [expressions.json](./expressions.json) — 후보 922(직접 읽기 수동 142 포함) · 알려진 오탐 19(출현별) |
| 미결 | [issues.md](./issues.md) |
| 검증 | [validation.md](./validation.md) · [validation-machine.json](./validation-machine.json) |
| 재현 | [build.py](./build.py) · [verify.py](./verify.py) · 수동 기록: [manual-expressions.json](./manual-expressions.json)(생성기 [manual-expressions-make.py](./manual-expressions-make.py)) · [segmentation-review.json](./segmentation-review.json)(생성기 [segmentation-review-make.py](./segmentation-review-make.py)) · 이 문서의 관찰 원고 [review-notes.md](./review-notes.md) |

구간 기준: 디코딩된 원문 문자열의 Unicode 코드 포인트 `[start,end)`. source-map 의 `span` 은 파일 전체 텍스트 기준(문자열은 따옴표 포함), `value_span` 은 따옴표 제외. morphology·expressions 의 `span` 은 해당 값 문자열 기준(파일 기준 = `value_span[0] + start`). UTF-8 바이트 구간은 `byte_span` 으로 따로 둔다. 이 원장은 이스케이프가 없어 JSON 리터럴 내부 구간과 디코딩 문자열이 같다(검증됨).

## 1. 읽기 범위 (실제로 한 일)

| 구획 | 범위 | 읽기 방식 |
|---|---|---|
| 상위 | `/version` `/updated` `/description` + 다섯 블록의 배열 길이 | 원본 한 줄 전체를 처음부터 끝까지 직접 읽음 |
| principles | `/principles/0` ~ `/principles/12` (13문장) | 1회차 원문 통독, 2회차 값마다 Kiwi 토큰을 원문과 나란히 대조, 3회차 표현 후보·절 분할 대조 |
| sequence_order | `/sequence_order/0` ~ `/10` 각 4필드(order·phase·categories 전 원소·reason) | 같음 |
| incompatible_same_day | `/incompatible_same_day/0` ~ `/8` 각 pair 전 원소·reason | 같음 |
| common_combos | `/common_combos/0` ~ `/7` 각 name·sequence 전 원소·total_time·(note) | 같음 |
| minimum_intervals | `/minimum_intervals/0` ~ `/8` 각 from·to·min_days/min_months·source·reason | 같음 |

- 자동 처리: 구조 열거·Pointer·구간·형태소 분석·regex/keyword 후보·Kiwi 품사 기반 수식 후보·수동 구절의 위치 찾기.
- 직접 처리: 원문 전체 통독, 155개 값의 토큰 1,429개 전체 열람(구두점·조사·어미는 위치만 확인), 규칙 후보 전 범주 열람 후 오탐 판정, 규칙 후보에 덮이지 않은 어절 목록 열람 후 수동 구절 보강, 절 분할 결과 열람 후 분할 규칙 수정(issues A1).
- 한계: 「별도 읽기 검토」는 같은 에이전트가 관점을 바꿔 다시 읽은 것이며 독립 검토자가 아니다.
@@structure
### 구조 사실 (원문 대응)

- 최상위 객체 키 8개, 순서 `version` → `updated` → `description` → `principles` → `sequence_order` → `incompatible_same_day` → `common_combos` → `minimum_intervals`.
- `principles` 는 문자열 13개 배열. 나머지 네 블록은 객체 배열(11·9·8·9개).
- `sequence_order` 11개 모두 키 4개 같은 순서(`order, phase, categories, reason`). `order` 값은 배열 순서대로 1~11, 결번·중복 없음. `categories` 길이는 순서대로 1,2,3,3,2,2,1,1,1,1,2.
- `incompatible_same_day` 9개 모두 `pair, reason`. `pair` 길이는 `/incompatible_same_day/4` 만 **1**, 나머지 2.
- `common_combos` 8개 중 `note` 는 `/common_combos/5`·`/6`·`/7` 에만 있다(5개는 키 3개, 3개는 키 4개).
- `minimum_intervals` 9개는 `from, to, (min_days | min_months), source, reason` 순서. `min_days` 7개(14,5,14,14,14,0,14), `min_months` 2개(`/minimum_intervals/2` = 0, `/minimum_intervals/3` = 6). 한 항목에 둘이 함께 있는 경우는 없다.
- null·빈 문자열·빈 배열·빈 객체·실수·불리언 없음. 숫자는 모두 정수(`order` 11, `min_days` 7, `min_months` 2).
- 같은 문자열이 여러 위치에 반복된다(예: `레이저` 5곳, `필러` 4곳, `임상 가이드` 4곳, `이소트레티노인 복용 중` 3곳). 각 출현은 Pointer 별로 따로 기록했다.

### 잠정 관찰 (구조)

- 잠정: `description` 은 「동일 세션 시술 조합 순서 가이드」인데 `minimum_intervals` 와 `/principles/9`(별도 세션)는 세션 사이 간격을 다룬다. 원장의 실제 범위가 설명보다 넓다(issues C7).
- 잠정: `categories` 의 값 형태가 셋으로 갈린다 — `Mn-이름`(10), `Mn`(9), 코드 없는 이름(`국소마취`·`연고마취`). `Mn` 이 가리키는 대상은 이 원장 안에 정의가 없다(외부 참조 — issues B7).
@@principles
### 잠정 관찰 (principles)

| Pointer | 관찰(잠정) |
|---|---|
| `/principles/0` | 「클렌징 → 마취 → 시술 → 진정」 4단 순서와 `sequence_order` 의 첫 두 phase·마지막 phase 가 대응해 보인다. 「기본」은 기본값이라는 수식. |
| `/principles/1` · `/principles/2` | 보톡스와 열시술(HIFU/RF)의 당일 병행은 「가능」, 순서는 「웬만하면 열시술 먼저」(선호). `/principles/2` 는 HIFU 에 한해 「HIFU 선행 또는 2주 이상 간격」을 두 선택지로 제시하고, RF·IPL·비침습 레이저는 당일 병행 가능으로 나눈다. 「효력 저하」의 대상(보톡스 효력인지)은 원문에 명시가 없다(issues B4). |
| `/principles/3` | 「레이저/IPL은 필러 주입 전에」 — 같은 세션 안 순서로 읽힌다. 괄호의 「부종 상태」는 필러 주입 뒤 상태로 추정되나 원문에 명시 없음. |
| `/principles/4` · `/principles/5` | 채널을 연 뒤 도포를 허가 의료 제제로 한정하고 화장품 분류 제제를 금지하는 같은 취지 문장이 둘 있다. 채널을 여는 시술 목록이 `/principles/4` 는 MTS/니들RF, `/principles/5` 는 MTS/니들RF/프락셔널로 다르다(issues C8). `/principles/5` 에만 「⚠️」 표지가 있다. |
| `/principles/6` · `/principles/7` | 「침습도 높은 시술」「출혈 위험 시술」의 판정 기준·목록이 원문에 없다(issues B2). |
| `/principles/8` · `/principles/9` | 같은 날은 「필러 먼저 → 보톡스 나중에」이되 「같은 날엔 순서 유연」, 별도 세션은 「보톡스 먼저 → 2주 후 필러」. 조건(같은 날/별도 세션)에 따라 방향이 반대다. |
| `/principles/10` ~ `/principles/12` | 기기·필러 사이 간격 세 규칙. 강도 표현이 `/principles/10` 「필수」, `/principles/12` 「권장」. 같은 내용이 `incompatible_same_day`·`minimum_intervals` 에 다른 강도로 다시 나온다(issues C1). `/principles/11` 은 정방향(RF/HIFU → 필러) 같은 날 가능과 역순 14일 이상 대기를 한 문장에 담는다. |
@@sequence_order
### 잠정 관찰 (sequence_order)

| Pointer | 관찰(잠정) |
|---|---|
| `/sequence_order/2` | `categories` 에 `M9-HIFU`·`M9-RF`·`M8-IPL` 이 함께 있다. `M8` 은 `/sequence_order/3`(레이저)에도 `M8-토닝`·`M8-프락셔널`·`M8-혈관` 으로 나온다 — 같은 코드 접두가 두 phase 에 걸친 구조 사실. 코드 체계 해석은 하지 않았다. |
| `/sequence_order/2/reason` | 「…가능성을 고려」로 끝나며 그 결과 행동(선행 또는 간격)은 `/principles/2` 에만 있다(issues B4). |
| `/sequence_order/3/reason` | 「에너지 기기 다음, 주사 전」 — 다른 phase 이름으로 앞뒤를 정한다. phase 이름이 순서 관계의 참조 대상으로 쓰인다. |
| `/sequence_order/5` ~ `/sequence_order/8` | phase 이름이 모두 「주사-」 접두. 주사 묶음 안의 순서가 필러(6) → 스킨부스터(7) → 보톡스(8) → PRP/성장인자(9). |
| `/sequence_order/5/reason` | 같은 날 필러 먼저의 이유(몰딩/마사지, 독소 확산 위험, ASPS 권고)와 근거 수준(전문가 컨센서스, RCT 근거 아님), 완화(「같은 날이면 어느 순서든 허용」)가 한 값에 함께 있다. |
| `/sequence_order/7/reason` | 「보톡스 마지막」이지만 order 8 이고 뒤에 PRP(9)·약물 도포(10)·진정(11)이 있다. 「마지막」이 주사 묶음 안에서인지 원문만으로 정할 수 없다(issues C3). |
| `/sequence_order/9/reason` | `/principles/4` 와 같은 제한을 경피 전달 관점으로 다시 적고, 위험 목록에 「과민반응」이 더해졌다. |
| `/sequence_order/1/categories` · `/sequence_order/4~8/categories` | 마취 phase 의 두 값만 코드가 없다. 니들RF/MTS(M11·M12), 필러(M2·M3)처럼 `phase` 이름의 두 요소와 두 코드의 대응은 이 원장에 적혀 있지 않다. |
@@incompatible_same_day
### 잠정 관찰 (incompatible_same_day)

| Pointer | 관찰(잠정) |
|---|---|
| 블록 전체 | 이름은 「같은 날 불가」이지만 내용은 섞여 있다: 같은 날 회피(`/0`·`/1`·`/2`), 복용 상태와 중단 후 기간(`/3`·`/7`·`/8`), 방향 있는 간격 규칙(`/4`·`/5`), 모든 시술 대상(`/6`). `/4` 의 reason 은 「역순…같은 날 가능」까지 말한다(issues C2). |
| `/incompatible_same_day/2` | 원문이 스스로 근거 수준(in vitro)·반대 사실(실제 임상에서 병용 많음)·불확실성(in vivo 검증 중)·범위(같은 부위 즉시)·강도(보수적으로 피함)를 모두 담는다. |
| `/incompatible_same_day/3` · `/7` · `/8` | `pair[0]` 이 시술이 아닌 「이소트레티노인 복용 중」. reason 은 복용 중이 아니라 **중단 후** 0~2개월·6개월을 말한다. 상대 표현이 「프락셔널/필링」「프락셔널 레이저」「케미컬 필링」으로 겹치며 갈린다(issues C5). |
| `/incompatible_same_day/4` | `pair` 원소가 1개이고 그 안에 순서(「HA 필러 주입 후 RF/HIFU」)가 문자열로 들어 있다. |
| `/incompatible_same_day/5` | pair 는 방향이 없는데 reason 은 「최소 5일 간격 필요」. `/principles/3`(레이저 먼저 같은 세션)과 `/minimum_intervals/1`(HA 필러 → 레이저 5일)을 함께 보면 방향에 따라 다른 규칙일 수 있으나 이 항목만으로는 정할 수 없다(issues B6). |
| `/incompatible_same_day/6/pair/0` | 「TCA 50%+」의 「+」는 README 의 「+ = 함께」가 아니라 「이상」으로 읽힌다(잠정, issues B9). |
@@common_combos
### 잠정 관찰 (common_combos)

| Pointer | 관찰(잠정) |
|---|---|
| 블록 전체 | `sequence` 배열 순서가 시행 순서라는 말은 원문에 없다. `note` 가 있는 3개(`/5`·`/6`·`/7`)만 순서를 문장으로 말한다(issues B5). |
| `/common_combos/0` · `/2` | 배열 순서가 HIFU → 보톡스 → 필러(…→ 스킨부스터)인데 `sequence_order` 는 필러(6) → 스킨부스터(7) → 보톡스(8). 배열이 시행 순서라면 `/principles/8` 의 같은 날 기본 순서와 다르다. 다만 `/principles/8` 이 같은 날 순서를 유연하다고도 하므로 충돌인지 정할 수 없다(issues C4). |
| `/common_combos/4` | 피코토닝(레이저) → IPL 순서. `sequence_order` 는 IPL(3) → 레이저(4). 같은 조건부 관찰(issues C4). |
| `/common_combos/5/note` | 「순서 준수」 — 같은 원장의 「같은 날엔 순서 유연」(`/principles/8`)보다 강한 표현(issues C3). |
| 이름 표면형 | 「울쎄라 HIFU」(`/2/sequence/0`)·「HIFU 울쎄라」(`/6/sequence/0`), 「레이저토닝」(`/1/sequence/1`)·「토닝」(`/6/sequence/1`)·「레이저 토닝」(`/6/note`), 「프락셔널 CO2」(`/7/sequence/0`)·「CO2 프락셔널」(`/incompatible_same_day/0/pair/0`). 같은 대상인지 정하지 않았다(issues C6). |
| 부위 표현 | 「보톡스 이마+미간」「필러 팔자」「보톡스 턱선」「필러 볼+턱」「필러 팔자+볼」 — 시술·부위가 한 문자열에 붙어 있다. 분리는 후속. |
@@minimum_intervals
### 잠정 관찰 (minimum_intervals)

| Pointer | 관찰(잠정) |
|---|---|
| 블록 전체 | `from` → `to` 는 방향 있는 쌍으로 보인다(필드명 기준 잠정). 숫자 칸은 `min_days` 또는 `min_months`. |
| `/minimum_intervals/2` | `min_months` = 0 이고 reason 은 「중단 후 0~2개월 범위에서 의사 판단」. 0 이 하한인지, 대기 없음인지 원문만으로 정할 수 없다(issues B1). 잠정 해석: reason 의 「0~2개월 범위」로 보아 0 은 그 범위의 **하한일 수 있다**(확정 아님). 숫자 칸만 단독으로 쓰면 「대기 0개월(=즉시 가능)」로 읽힐 위험이 있어 reason 과 함께 읽어야 한다. |
| `/minimum_intervals/3` | reason 이 적용 범위를 「전안면 박리성 재표면화·기계적 박피에 한해」로 좁히고 「국소 부위·비박리성 시술에는 적용하지 않음」으로 제외한다. `to` 는 「박리성(ablative) 레이저/심부 필링」. |
| `/minimum_intervals/7` | `min_days` = 0, reason 「같은 날 가능」 — 최소 간격 블록 안의 같은 날 허용. `/minimum_intervals/0` 과 from/to 가 뒤바뀐 쌍. |
| `/minimum_intervals/6` | `to` = 「필러 (별도 세션)」 — 세션 조건이 대상 문자열 안 괄호에 있다. `/principles/9` 는 「2주 후」, 여기는 `min_days` 14(최소). |
| `/minimum_intervals/8` | `from`·`to` 가 같은 「필러」이고 `to` 괄호에 「동일 부위 재시술」. |
| `source` | 문헌 표기(JCD·ASDS·AAD·PRS)와 비특정 표현(「임상 가이드」 4곳), 출처가 아닌 문구(「피부 회복」, `/minimum_intervals/5/source`)가 섞여 있다(issues B8). |
@@footer
## 9. 형태소·표현 수집 요약

- 분석기: Kiwi(kiwipiepy 0.24.1 / kiwipiepy_model 0.24.0), `Kiwi(num_workers=1, model_type='cong')`, 사용자 사전 없음, tokenize 기본 옵션, 원문 정규화 없음. 기본형은 Kiwi `Token.lemma` 그대로.
- 제외 9: `/version`(버전 문자열), `/updated`(날짜), 한글 없는 카테고리 코드 7(`M11` `M12` `M2` `M3` `M4` `M1` `M5`). 비문자열 말단 20(정수)은 리터럴만 보존. 필드명 22종은 값과 따로 분석(영문 snake_case → Kiwi SL + underscore 규칙 분할).
- 알려진 오분절 69출현(교정 안 함, 원시 토큰 유지): 의미 영향 큰 것 — 「열시술/열 시술」→ 열/NR(수사) 4출현, 「필러」→ 필+러/EC 5출현, 「박리성·비박리성」 분절 9출현, 「전안면」→ 저/NP+ᆫ 2출현, 「(에) 한해」→ 한/MM+해/NNB(1년) 1출현, 「>」→ SSC 2출현, 부위 「이마」「팔자」 4출현, 「진정」→ MAG 2출현, 「육아종」「이물」「세럼」「몰딩」「니들」「경피」「리쥬란」「나중」「유연」 각 출현. 전체 목록·영향은 [segmentation-review.json](./segmentation-review.json), 요약은 issues A2.
- 표현 후보 922: 값 전체 155 · 절 분할 · regex/keyword 13규칙 · Kiwi 품사(MAG/MM/VCN/VX/MAJ) 수식 구절 · 직접 읽기 수동 142. 알려진 오탐 19(부분일치 8 · 범주 불일치 3 · 오태깅 유래 8)는 지우지 않고 [manual-expressions.json](./manual-expressions.json) `known_false_positives` 에 출현별로 둔다. 규칙 후보는 탐색 보조이며 전수 의미 해석이 아니다.

## 10. 상태

| 항목 | 상태 |
|---|---|
| **1차 범위 종료** | 종료 조건 충족(아래 전 항목) — 코디 확인 전 |
| **원장 전체 완료** | **아님** — 원문 부족 B 10 · 원문 내 불일치 C 8 · 후속 의미 조사 D 8 열림 |
| 전수 읽기 | 상위 3 + 5블록 전 항목 전 필드, 3회 통독(같은 에이전트) |
| 구조·값 수집 | 노드 255/255 · 키 142 · 중복 키 0 · 말단 184(문자열 164 + 정수 20) |
| 형태소·표현 수집 | 분석 155 / 제외 9 / 비문자열 20 · 토큰 1,429 · 오분절 기록 69 · 표현 922(수동 142, 오탐 19 표시) |
| 기계 검증 | build 내장 12검사 + 독립 verify.py 32검사 통과, 변이 시험 검출(validation.md) |
| 읽기 검토 | 같은 에이전트 별도 관점 재독 — 수식·조건·부정·오분절 영향 대조(validation.md §3). 독립 검토 없음 |
| 알려진 분석 오류 | 오분절 69(표시, 교정 아님) · 표현 오탐 19(표시) |
| 열린 미결 | B 10 · C 8 · D 8 · 사용자 선택 대기 0(issues E) |
| 후속 의미 조사 | 시작 안 함 |
