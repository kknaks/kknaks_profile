# S00 — 루트·메타데이터·problems 컨테이너

[← review.md](review.md) · 범위 '' (루트 객체), /version, /updated, /description, /problems (배열 컨테이너만; 원소는 S01~S14) · 소유 노드 5 · 말단 3 · 빈 값 0 · 직접 읽기 done

직접 읽기: 루트 객체·version·updated·description·problems 배열 컨테이너를 직접 읽음. 원본 한 줄(줄바꿈 0)·BOM 없음·이스케이프 0.

## 원문 값 (문서 순서 · 전부)

| # | JSON Pointer | 원본 컬럼명 | 배열 순번 | 자료형 | 원문 값 | 관찰 참조 |
|---|---|---|---|---|---|---|
| 0 | `(루트)` | `(루트)` |  | object{4} | (객체 · 키: `version`, `updated`, `description`, `problems`) |  |
| 1 | `/version` | `version` |  | string | 6.2 | OB-S00-03 |
| 2 | `/updated` | `updated` |  | string | 2026-07-26 | OB-S00-03 |
| 3 | `/description` | `description` |  | string | taxonomy P1~P14 하위구조 기반 CC 자동 생성 | OB-S00-01, OB-S00-02 |
| 4 | `/problems` | `problems` |  | array[14] | (배열 · 14개) | OB-S00-04 |

## 잠정 관찰 (원문 칸과 분리)

| ID | 상태 | 위치 | 관찰 |
|---|---|---|---|
| OB-S00-01 | P | `/description` | description 은 'taxonomy P1~P14 하위구조 기반 CC 자동 생성' — 이 원장이 다른 원장(taxonomy)에서 자동 생성됐다고 스스로 밝힌다. 참조 대상(taxonomy)의 해당 구조는 이번 범위에서 열지 않았다(후속 연결 F-01). |
| OB-S00-02 | P | `/description` | 'CC' 는 약어로만 나오고 원문에 풀이가 없다. 하위 항목 키 cc·cc_detail·cc_group 과 같은 표기다. |
| OB-S00-03 | P | `/version`<br>`/updated` | version '6.2' 는 문자열, updated '2026-07-26' 은 ISO 날짜 형식 문자열. README 의 '1판=10-26 스냅샷' 서술과 날짜가 다르다(파일 내부 updated 는 스냅샷 날짜가 아님일 수 있음 — 판단하지 않음). |
| OB-S00-04 | P | `/problems` | problems 14개, 각 원소 키는 전부 problem_id·problem·complaints 3개로 동일. complaints 115개 전부 키 6개(cc·cc_detail·cc_group·procedures·combos·alternatives) 동일 순서. procedures 254개 키 4개(name·category·role·products), combos 146개 키 4개(name·combo·reason·evidence). 선택적 필드 없음, 빈 값은 빈 배열 48개(products 47·combos 1)만. |
| OB-S00-05 | I | `/problems/0/complaints/3/combos/0/combo/1`<br>`/problems/0/complaints/12/combos/0/combo/1`<br>`/problems/3/complaints/3/combos/1/combo/1`<br>`/problems/3/complaints/4/combos/0/combo/1`<br>`/problems/3/complaints/4/combos/1/combo/1`<br>`/problems/5/complaints/0/combos/0/combo/1`<br>`/problems/5/complaints/1/combos/0/combo/1`<br>`/problems/5/complaints/2/combos/0/combo/1`<br>`/problems/8/complaints/0/combos/0/combo/1`<br>`/problems/8/complaints/0/combos/1/combo/2`<br>`/problems/8/complaints/1/combos/0/combo/1`<br>`/problems/8/complaints/1/combos/1/combo/2`<br>`/problems/8/complaints/2/combos/0/combo/1`<br>`/problems/8/complaints/2/combos/1/combo/2`<br>`/problems/8/complaints/3/combos/0/combo/1`<br>`/problems/8/complaints/3/combos/1/combo/2`<br>`/problems/8/complaints/4/combos/0/combo/1`<br>`/problems/8/complaints/4/combos/1/combo/2`<br>`/problems/8/complaints/5/combos/1/combo/1`<br>`/problems/8/complaints/5/combos/2/combo/2`<br>`/problems/10/complaints/5/combos/0/combo/1`<br>`/problems/10/complaints/6/combos/0/combo/1`<br>`/problems/12/complaints/0/combos/0/combo/0`<br>`/problems/12/complaints/0/combos/0/combo/1`<br>`/problems/12/complaints/1/combos/0/combo/0`<br>`/problems/12/complaints/1/combos/0/combo/1`<br>`/problems/12/complaints/2/combos/0/combo/0`<br>`/problems/12/complaints/2/combos/0/combo/1`<br>`/problems/12/complaints/3/combos/0/combo/1`<br>`/problems/12/complaints/4/combos/0/combo/1`<br>`/problems/12/complaints/5/combos/0/combo/1`<br>`/problems/12/complaints/6/combos/0/combo/1`<br>`/problems/12/complaints/7/combos/0/combo/1`<br>`/problems/12/complaints/8/combos/0/combo/1`<br>`/problems/12/complaints/9/combos/0/combo/1`<br>`/problems/12/complaints/10/combos/0/combo/1` | 읽기 검토 중 전 구획 대조(기계 보조 비교 후 원문 확인): combos.combo 원소가 같은 complaint 의 procedures.name 에 글자 그대로 없는 출현 36곳 — 'PRP' 23(procedures 는 'PRP/자가혈'), 'MTS' 6('마이크로니들링(MTS)'), '바이오스티뮬레이터' 4('바이오스티뮬레이터/콜라겐부스터'), '필링' 3('메디컬스킨케어'). I-01·I-06 의 전체 출현 목록이다. |
| OB-S00-06 | P | `/problems/5/complaints/3/cc`<br>`/problems/6/complaints/1/cc`<br>`/problems/5/complaints/4/cc`<br>`/problems/6/complaints/0/cc`<br>`/problems/6/complaints/2/cc`<br>`/problems/8/complaints/8/cc`<br>`/problems/8/complaints/10/cc`<br>`/problems/6/complaints/3/cc`<br>`/problems/8/complaints/4/cc`<br>`/problems/8/complaints/11/cc`<br>`/problems/6/complaints/5/cc`<br>`/problems/8/complaints/0/cc`<br>`/problems/10/complaints/2/cc`<br>`/problems/11/complaints/4/cc` | 같은 cc 문자열이 여러 complaint 에 나오는 경우 6종: 아그네스(P6·P7), 스킨보톡스(P6·P7), 프락셔널레이저(P7·P9×2), 니들RF(P7·P9×2), 서브시전(P7·P9), 브이올렛(P11·P12). cc 만으로 complaint 를 식별할 수 없고 Pointer 로만 구분된다. |
| OB-S00-07 | P | `/problems/0/complaints/3/procedures/1/category`<br>`/problems/3/complaints/2/procedures/0/category`<br>`/problems/5/complaints/0/procedures/1/category`<br>`/problems/0/complaints/13/procedures/0/category` | category 코드 하나에 procedures.name 이 여럿: M5 = PRP·PRP/자가혈, M8 = 레이저·서브시전·제모레이저·프락셔널·피코레이저·혈관레이저, M9 = 리프팅기기·미라드라이·인모드, M14 = 지방분해·크라이오, M15 = 메디컬스킨케어·모발이식·반영구화장·병변내 스테로이드주사·약물치료, M16 = 미백주사·수액. M13 은 출현하지 않는다. 코드 체계 해석은 taxonomy 대조(F-01). |

## 수동 복합 표현 (직접 읽기 · 출현별)

| 표현 | 위치(Pointer · 값 내 구간) | 관점(탐색용, 확정 분류 아님) |
|---|---|---|
| taxonomy P1~P14 하위구조 기반 CC 자동 생성 | `/description` [0,32) | 출처·생성 방법, 다른 원장 참조 |
| P1~P14 | `/description` [9,15) | 범위(~), ID 범위 |
| CC | `/description` [24,26) | 약어(원문 풀이 없음) |
| 자동 생성 | `/description` [27,32) | 출처·생성 방법 |

## 이 구획에서 연 미결

- **F-01** (F) description 이 taxonomy P1~P14 하위구조를 생성 원천으로 지목한다. problem_id(P1~P14)·category(M코드)·procedures.name·products 가 taxonomy 의 어느 값과 대응하는지는 이 원장만으로 확인할 수 없다. — 영향: 원장 간 연결(후속 비교 단계). 이번 1차에서는 참조 표현과 위치만 보존.
- **B-01** (B) 'CC' 의 풀이가 원문에 없다. — 영향: cc 필드의 정보 종류(호소/요청/시술 요구 등)를 원문만으로 확정할 수 없다. 후속 의미 조사에서 다른 원장·사용자 정의 확인.
