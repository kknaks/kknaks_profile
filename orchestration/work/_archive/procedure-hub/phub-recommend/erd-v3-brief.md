# ERD v3 발주서 — 실버 빌드 1~4차에서 드러난 구조·규칙 변경 (사용자 승인 2026-11-05 「v3 진행하자」)

동결 v2.4(`ERD-FROZEN.md` · `erd-v2.4.*` · 생성기 `*_v24.py` · `erd-v2.4-tuples.py` · `erd-v2.4-check.py`)를 **v3 로 개정**한다.
근거: `ERD-V3-CANDIDATES.md` V3-1 ~ V3-8 **전부** + 실버 빌드에서 드러난 빌더 제약 2건(아래 V3-9·10). 그 밖의 개체·관계·규칙은 v2.4 그대로.
사용자 정의 3(ERD-FROZEN §동결 조건)과 명시 예외(부작용 축 none·미상은 값)는 그대로 유지한다. 바뀌는 것이 그 정의를 깨면 안 된다.
입력·금지는 v1~v2.4 발주서와 같다. 추가로 읽어도 되는 것: `ERD-FROZEN.md` · `ERD-V3-CANDIDATES.md` · `silver-v3/decisions/_batch3-candidates.md` · `silver-v3/out/report.md` · `silver-v3/README.md` · `bronze/phub-ledger/`(브론즈 2판 — 원장 21 은 이것을 읽는다. 1판과의 차이는 CHANGELOG 6곳뿐).

## 변경 10건
| # | 변경 | 어디 |
|---|---|---|
| V3-1 | 부작용 튜플에 **선택 수식 칸** `qualifier`(물질·기전): (event, site, course, qualifier?). qualifier 는 사전(`adverse_qualifier`: 공기·필러 물질·혈전·… 출처 필수). 식별자는 qualifier 포함. qualifier 없음 = none(값). 「공기색전」→ (색전, none, 미상, 공기). 접힘 조건·표현 연결 규칙에 qualifier 반영 | §1.5 · §2.14 · 사전 |
| V3-2 | 분해 규칙: 괄호 안 조각이 **회사 사전(manufacturer)·제품 사전**에 닿으면 바깥 what 의 그 회사/제품으로(「보톡스(엘러간)」= 엘러간 톡신 제품). 닿지 않으면 기존대로 | §1.3/1.4 resolve_rules |
| V3-3 | 분해 규칙: **수식어 제외 목록**(stopwords) — 회·차·터치업·유지·집중·연말·하반기·가을·관리·케어·과도한·빈도 + 원장 실측에서 추가되는 것. 조각이 아니라 참조의 `qualifier_text` 속성(회차는 R12 엣지 `session_index`). 목록은 규칙 데이터로, 출처 locator 필수 | resolve_rules.stopwords · R12 속성 |
| V3-4 | **조합 기호 규칙 확정**: `+` 는 항상 함께. `/` 는 양쪽 조각으로 — 같은 what 의 부위 둘 → 함께 · 대안(계열·하위분류·장비·재질·제품) 둘 → 또는 · 괄호 안 대안은 바깥 하나. **「무엇을 하나 × 부위 여럿」**(「보톡스 이마+미간」「보톡스(턱선+광대)」「필러 볼+턱」)은 조합 패키지가 아니라 **같은 what 의 시술 튜플 여럿**이며 패키지 멤버 엣지(R12)가 각각 붙는다. R12 에 `member_mode: and|or` 속성 추가. 4차 빌드에서 `+` 4곳이 미해결로 남은 원인이 이 규칙 부재 | resolve_rules · R12 |
| V3-5 | 부위 개체에 `kind` 열거형: anatomical(얼굴 부위) · relative(주사 부위·시술 부위) · **layer(조직층: 피부·피하 지방층·근육·혈관·점막)** · region(바디·두피 등 넓은 구역). 사전 값은 출처 필수(anatomy-danger-zones 층 정보·complications 이름). 부작용 (괴사, 피부)·(괴사, 피하 지방층) 가 가능해진다 | §2.7 site · 사전 |
| V3-6 | 결정 kind `canonical_rename`: 사전 정준값 교체(같은 코드·같은 id 유지, 옛 정준값은 동의어로 내림, 선택적으로 is_marketing_name 표시). 대상: M1 「보톡스」→「보툴리눔 톡신」 · M3 → 「바이오스티뮬레이터」 · M5 → 「자가혈 유래 시술」(값은 묶음 3 결정, ERD 는 kind 만) | §5 결정 kind · 적용 순서 ①에 포함 |
| V3-7 | technique · product 개체에 `description`(출처 locator 필수) · `media_refs[]`(path·sha256·captured_at·source·kind). 사진 파일은 브론즈 밖 에셋, 참조만 실버. 새 브론즈 원천(조사 파일) 입구로 채움 | §2.5 · §2.6 |
| V3-8 | 기법 상속 규칙: 계열 기본 기법은 **하위분류 단위**로 둘 수 있고(R5 를 subcategory → technique 로 확장), 계열이 섞여 있으면(M16) 하위분류별 또는 항목별 지정. 상속은 결정(canonical_mapping)으로만, 자동 아님(v2.2 유지) | R5 · §9.5.6 |
| V3-9 | 결정 적용 대상 확장: `tuple_assign` · `tuple_assign_multi` · `adverse_tuple_assign` 가 **미해결 참조(unresolved) 와 조합 참조**에도 적용된다(anchor = REF-id). 4차에서 거부된 HIFU(슈링크/울쎄라) 2건의 자리 | §5 결정 kind · 빌더 규칙 |
| V3-10 | `fold_approve` 는 접히는 anchor 쌍의 ⑦ duplicate_candidate 를 **닫는다**(status=resolved · decision_id). 「단계 끝 = open 0」에 닿기 위해 | §5 규칙 ⑦ |

## 검산
`erd-v3-check.py` = v2.4 항목 전부 + 10건 각각 반영 여부 + 브론즈 2판 해시(`bronze/phub-ledger/HASHES.txt`) + 행선지 전수(2판 잎 키 = 1판과 같아야 함, 다르면 표) + 「사용자 정의 3 과 명시 예외 유지」문장.
`erd-v3-tuples.py` = v2.4 실측 전부 재실행(2판 원장) + 신설: `+`/`/` 규칙 적용 결과(2B 12건 + 2판 `+` 4곳이 규칙만으로 어떻게 풀리는지 전부 표) · stopwords 적용 전후 미등록 조각 수 · 회사 괄호 규칙 적용 건 · qualifier 가 생기는 부작용 이름 전부 표.

## 산출물
`erd-v3.md` · `erd-v3.json` · `erd-v3-column-map.md` · `erd-v3-dictionaries.json` · `erd-v3-check.py` · `erd-v3-tuples.py/.json` · 생성기 `*_v3.py`. 이전 판 전부 보존. `erd-v3.md` 끝에 「v2.4 → v3 변경 목록(V3-# 대응)」 · 「v3 밖 관찰」.

## 보고
10건 각각 어디서 반영했는지 한 줄씩 · 개체·관계·사전 수 변화 · `+`/`/` 규칙 실측(16건 결과) · stopwords 전후 · qualifier 생긴 이름 수 · 검산 결과. 본문 재붙임 금지.
