# combo-recipes.json — 1차 조사 (읽기용)

> 원문 값과 잠정 관찰을 분리한다. 값 표의 「원문 값」 칸은 디코딩된 원문 그대로이고(표 안 `|` 만 `\|` 로 이스케이프), 관찰은 각 구획의 「잠정 관찰」 절에 근거 Pointer 와 함께 둔다. 공통 개념 ID·동의어·관계 방향·정규화는 하지 않았다(1차 범위 밖). 원문의 효과·임상 서술은 **원장에 적혀 있다는 사실**로만 기록한다.

## 상태

| 항목 | 상태 |
|---|---|
| **1차 범위 종료** | 예 — 아래 기준 충족(validation.md) |
| **원장 전체 완료** | **아님** — 원문 부족 B·잠정 P·후속 F·원문 불일치 I 가 남아 있다(issues.md) |
| 전수 읽기 | 구획 8/8 직접 읽음 (coverage.json) |
| 구조·값 수집 | 노드 192개 · 키 출현 137개 · 말단 141개 (source-map.json) |
| 형태소·표현 수집 | 적용 값 78 · 제외 35 · 토큰 961 · 표현 633(수동 181) |
| 기계 검증 | verify.py — validation.md |
| 읽기 검토 | 같은 에이전트의 별도 관점 재독(독립 검토자 아님) — validation.md §3 |
| 알려진 분석 오류 | 오분절 규칙 14개 · 출현 29건 (morphology.json segmentation_flags) |
| 열린 미결 · 후속 의미 조사 | issues.md — 사용자 결정 필요(C) 0건(검토 후 판단 근거는 issues.md §0) |

## 원본

| 항목 | 값 |
|---|---|
| 경로 | `orchestration/work/phub-recommend/bronze/phub-ledger/combo-recipes.json` |
| 크기 | 6,486 bytes · 4,026 code points · UTF-8 · BOM 없음 · 개행 0 · 백슬래시(이스케이프) 0 · BMP 밖 문자 0 |
| sha256 | `1bb7c309e8ec72768ae9c5db94e1911188be240f4c7d770d54244008aeab0c94` |
| 중복 키 | 0건 |

구간 기준: source-map 의 `span` 은 파일 텍스트 코드 포인트 `[start,end)`, morphology·expressions 의 `span` 은 값 문자열 기준(파일 기준은 `file_span`). 바이트는 `byte_span`.

## 컬럼 구성

| 원본 컬럼명(경로 패턴) | 자료형 | 중첩 구조 | 출현 | 원문 예시 | 예시 위치 | 빈 값 |
|---|---|---|---|---|---|---|
| `(root)` | 객체 | 객체 {version, updated, description, recipes} | 1 | — | `(root)` | 0 |
| `/version` | 문자열 | 스칼라 | 1 | 1.0 | `/version` | 0 |
| `/updated` | 문자열 | 스칼라 | 1 | 2026-04-04 | `/updated` | 0 |
| `/description` | 문자열 | 스칼라 | 1 | 대표원장급 검증 조합 레시피 — 목적별 프리셋 + 기대 효과 + 후속 프로토콜 | `/description` | 0 |
| `/recipes` | 배열 | 배열 길이 7 | 1 | — | `/recipes` | 0 |
| `/recipes/[]` | 객체 | 객체 {id, name, subtitle, goal, intensity, procedures, expectedResults, patientExplanation, analogy, repeatCycle, followUp} | 7 | — | `/recipes/0` | 0 |
| `/recipes/[]/id` | 문자열 | 스칼라 | 7 | R1 | `/recipes/0/id` | 0 |
| `/recipes/[]/name` | 문자열 | 스칼라 | 7 | 리프팅 기본 | `/recipes/0/name` | 0 |
| `/recipes/[]/subtitle` | 문자열 | 스칼라 | 7 | 처진 살 올리기 입문 | `/recipes/0/subtitle` | 0 |
| `/recipes/[]/goal` | 문자열 | 스칼라 | 7 | lifting | `/recipes/0/goal` | 0 |
| `/recipes/[]/intensity` | 문자열 | 스칼라 | 7 | 기본 | `/recipes/0/intensity` | 0 |
| `/recipes/[]/procedures` | 배열 | 배열 길이 2/3/4 | 7 | — | `/recipes/0/procedures` | 0 |
| `/recipes/[]/procedures/[]` | 문자열 | 스칼라 | 19 | M9 | `/recipes/0/procedures/0` | 0 |
| `/recipes/[]/expectedResults` | 문자열 | 스칼라 | 7 | 턱선 정리 + 볼처짐 개선. 자연스러운 리프팅. 주변에서 '좀 쉬었나?' 수준 | `/recipes/0/expectedResults` | 0 |
| `/recipes/[]/patientExplanation` | 문자열 | 스칼라 | 7 | 초음파로 피부 아래 콜라겐을 조여서 당기고, 보톡스로 아래로 당기는 근육을 쉬게 해서 올라간 효과를 오래 유…(전체는 구획 표) | `/recipes/0/patientExplanation` | 0 |
| `/recipes/[]/analogy` | 문자열 | 스칼라 | 7 | HIFU = 옷감을 다림질해서 팽팽하게, 보톡스 = 늘어진 고무줄을 리셋 | `/recipes/0/analogy` | 0 |
| `/recipes/[]/repeatCycle` | 문자열 | 스칼라 | 7 | 3~6개월 간격 반복 | `/recipes/0/repeatCycle` | 0 |
| `/recipes/[]/followUp` | 배열 | 배열 길이 3/4/5 | 7 | — | `/recipes/0/followUp` | 0 |
| `/recipes/[]/followUp/[]` | 객체 | 객체 {week, action} | 28 | — | `/recipes/0/followUp/0` | 0 |
| `/recipes/[]/followUp/[]/week` | 정수 | 스칼라 | 28 | 4 | `/recipes/0/followUp/0/week` | 0 |
| `/recipes/[]/followUp/[]/action` | 문자열 | 스칼라 | 28 | 경과 확인. 효과 부족 부위 추가 HIFU 가능 | `/recipes/0/followUp/0/action` | 0 |

- 선택적 필드: 없음 — recipes 7개 모두 11키 전부, followUp 원소 28개 모두 week·action 두 키.
- 빈 문자열·빈 배열·빈 객체·null: 0.

## 구획 목차

| 구획 | 범위 | 소유 말단 | 직접 읽음 |
|---|---|---|---|
| [S0](#s0) | 상위 메타데이터와 recipes 컨테이너 | 3 | done |
| [S1](#s1) | /recipes/0 (R1 리프팅 기본) | 17 | done |
| [S2](#s2) | /recipes/1 (R2 리프팅 풀패키지) | 23 | done |
| [S3](#s3) | /recipes/2 (R3 피부 재생 골든루틴) | 20 | done |
| [S4](#s4) | /recipes/3 (R4 탄력 + 주름 집중) | 20 | done |
| [S5](#s5) | /recipes/4 (R5 모공/흉터 집중) | 19 | done |
| [S6](#s6) | /recipes/5 (R6 동안 쁘띠 패키지) | 19 | done |
| [S7](#s7) | /recipes/6 (R7 레이저 토닝 + 재생) | 20 | done |

<a id="s0"></a>
## S0 — 상위 메타데이터와 recipes 컨테이너

읽기 기록: 2026-11-09 원본 한 줄 전체를 출력해 상위 키 4개와 recipes 배열 길이·각 원소 키 순서를 직접 읽었다. 이후 구획 S1~S7 을 이 상위 문맥(description)과 함께 읽었다.

### 원문 값

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `(root)` | (root) | 객체 | (키 version, updated, description, recipes) |
| `/version` | version | 문자열 | 1.0 |
| `/updated` | updated | 문자열 | 2026-04-04 |
| `/description` | description | 문자열 | 대표원장급 검증 조합 레시피 — 목적별 프리셋 + 기대 효과 + 후속 프로토콜 |
| `/recipes` | recipes | 배열 | (원소 7개) |

### 잠정 관찰 (원문 아님)

| ID | 상태 | 근거 Pointer | 관찰 |
|---|---|---|---|
| S0-1 | P | `/description` | description 의 세 구성(목적별 프리셋·기대 효과·후속 프로토콜)은 각각 goal·expectedResults·followUp 필드와 대응하는 것으로 보인다. 원문이 대응을 명시하지는 않는다. |
| S0-2 | B | `/description` | 「대표원장급 검증」은 원장의 자기 주장이다. 누가·언제·어떤 근거로 검증했는지 원문에 없다. 사실 여부를 판단하지 않는다(issues B-9). |
| S0-3 | P | `/version` `/updated` | version 「1.0」·updated 「2026-04-04」는 문자열이다. 다른 원장 판과의 관계는 이 원장만으로 정할 수 없다. |
| S0-4 | P | `/recipes` | recipes 7개는 모두 같은 11개 키를 같은 순서로 가지며, followUp 원소는 모두 week(정수)·action(문자열) 두 키다. 선택적 필드·빈 값은 없다. |

수동 표현 6건 · 전체 표현 10건 → expressions.json (segment="S0")

<a id="s1"></a>
## S1 — /recipes/0 (R1 리프팅 기본)

읽기 기록: /recipes/0 의 11필드와 followUp 3원소를 위에서 아래로 직접 읽음. procedures [M9,M1] 와 본문 명칭(초음파·HIFU·보톡스·실리프팅)을 나란히 대조.

### 원문 값

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/recipes/0` | recipes[0] | 객체 | (키 id, name, subtitle, goal, intensity, procedures, expectedResults, patientExplanation, analogy, repeatCycle, followUp) |
| `/recipes/0/id` | id | 문자열 | R1 |
| `/recipes/0/name` | name | 문자열 | 리프팅 기본 |
| `/recipes/0/subtitle` | subtitle | 문자열 | 처진 살 올리기 입문 |
| `/recipes/0/goal` | goal | 문자열 | lifting |
| `/recipes/0/intensity` | intensity | 문자열 | 기본 |
| `/recipes/0/procedures` | procedures | 배열 | (원소 2개) |
| `/recipes/0/procedures/0` | procedures[0] | 문자열 | M9 |
| `/recipes/0/procedures/1` | procedures[1] | 문자열 | M1 |
| `/recipes/0/expectedResults` | expectedResults | 문자열 | 턱선 정리 + 볼처짐 개선. 자연스러운 리프팅. 주변에서 '좀 쉬었나?' 수준 |
| `/recipes/0/patientExplanation` | patientExplanation | 문자열 | 초음파로 피부 아래 콜라겐을 조여서 당기고, 보톡스로 아래로 당기는 근육을 쉬게 해서 올라간 효과를 오래 유지시킵니다. |
| `/recipes/0/analogy` | analogy | 문자열 | HIFU = 옷감을 다림질해서 팽팽하게, 보톡스 = 늘어진 고무줄을 리셋 |
| `/recipes/0/repeatCycle` | repeatCycle | 문자열 | 3~6개월 간격 반복 |
| `/recipes/0/followUp` | followUp | 배열 | (원소 3개) |
| `/recipes/0/followUp/0` | followUp[0] | 객체 | (키 week, action) |
| `/recipes/0/followUp/0/week` | week | 정수 | 4 |
| `/recipes/0/followUp/0/action` | action | 문자열 | 경과 확인. 효과 부족 부위 추가 HIFU 가능 |
| `/recipes/0/followUp/1` | followUp[1] | 객체 | (키 week, action) |
| `/recipes/0/followUp/1/week` | week | 정수 | 12 |
| `/recipes/0/followUp/1/action` | action | 문자열 | 보톡스 터치업 (효과 감소 시) |
| `/recipes/0/followUp/2` | followUp[2] | 객체 | (키 week, action) |
| `/recipes/0/followUp/2/week` | week | 정수 | 24 |
| `/recipes/0/followUp/2/action` | action | 문자열 | 리프팅 유지 시술 (HIFU 반복 or 실리프팅 업그레이드) |

### 잠정 관찰 (원문 아님)

| ID | 상태 | 근거 Pointer | 관찰 |
|---|---|---|---|
| S1-1 | B | `/recipes/0/procedures/0` `/recipes/0/procedures/1` | procedures 는 M 코드만 있고 이름이 없다. 본문의 「초음파」「HIFU」「보톡스」가 어느 코드인지 이 원장 안에 대응표가 없다(B-1). 배열 순서 M9→M1 은 본문 서술 순서(초음파 → 보톡스)와 같다(잠정 대조). |
| S1-2 | F | `/recipes/0/followUp/2/action` | 「HIFU 반복 or 실리프팅 업그레이드」의 실리프팅은 procedures 에 없는 시술을 가리키는 것으로 보인다. R2 가 실리프팅을 포함하는 레시피인지는 코드 대응을 알아야 한다(F-2). |
| S1-3 | B | `/recipes/0/repeatCycle` | 「3~6개월 간격 반복」이 레시피 전체(두 시술 함께)의 주기인지 특정 시술 주기인지 원문에 없다(B-5). followUp 의 week 값(4·12·24)과의 대조는 week 단위·기준 시점이 정의되지 않아(B-4) 판정하지 않는다. |
| S1-4 | B | `/recipes/0/followUp/0/week` `/recipes/0/followUp/1/week` `/recipes/0/followUp/2/week` | week 의 기준 시점(첫 시술일 등)과 단위(주)가 원문에 정의되지 않았다. 키 이름 week 로만 짐작된다(B-4). |
| S1-5 | P | `/recipes/0/followUp/1/action` | 「보톡스 터치업 (효과 감소 시)」는 조건부 행위다. R6 의 「부족하면 터치업」(week 2)과 같은 낱말이 다른 시점·조건에 쓰인다. |
| S1-6 | P | `/recipes/0/expectedResults` | 효과 정도는 「자연스러운」「'좀 쉬었나?' 수준」처럼 체감 표현으로만 적혔다. 수치로 바꾸지 않는다. |

### 이 구획의 알려진 오분절 (Kiwi 원시 출력, 미교정)

| 규칙 | Pointer | 구간 | 원문 | 원시 토큰 | 영향 |
|---|---|---|---|---|---|
| K-7 | `/recipes/0/analogy` | [11, 14] | 다림질 | 다리/VV ᆷ/ETN 질/XSN | 기본형 「다리다」는 원문 표면과 다르다. 비유 문장이라 의미 영향은 작으나 lemma 를 그대로 쓰면 안 된다. /recipes/3/analogy 의 같은 낱말은 다림/NNG 질/XSN 으로 다르게 나온다. |
| K-9a | `/recipes/0/patientExplanation` | [0, 3] | 초음파 | 초/XPN 음파/NNG | 에너지원 명칭이 접두사+명사로 쪼개진다. 「음파」만으로 찾으면 다른 뜻과 섞일 수 있다. |

수동 표현 28건 · 전체 표현 74건 → expressions.json (segment="S1")

<a id="s2"></a>
## S2 — /recipes/1 (R2 리프팅 풀패키지)

읽기 기록: /recipes/1 11필드·followUp 5원소 직접 읽음. repeatCycle 의 시술별 주기 4개와 followUp week 를 대조.

### 원문 값

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/recipes/1` | recipes[1] | 객체 | (키 id, name, subtitle, goal, intensity, procedures, expectedResults, patientExplanation, analogy, repeatCycle, followUp) |
| `/recipes/1/id` | id | 문자열 | R2 |
| `/recipes/1/name` | name | 문자열 | 리프팅 풀패키지 |
| `/recipes/1/subtitle` | subtitle | 문자열 | 확실한 리프팅 + 볼륨 복원 |
| `/recipes/1/goal` | goal | 문자열 | lifting |
| `/recipes/1/intensity` | intensity | 문자열 | 풀패키지 |
| `/recipes/1/procedures` | procedures | 배열 | (원소 4개) |
| `/recipes/1/procedures/0` | procedures[0] | 문자열 | M7 |
| `/recipes/1/procedures/1` | procedures[1] | 문자열 | M9 |
| `/recipes/1/procedures/2` | procedures[2] | 문자열 | M2 |
| `/recipes/1/procedures/3` | procedures[3] | 문자열 | M1 |
| `/recipes/1/expectedResults` | expectedResults | 문자열 | 확실한 턱선 + 볼/관자놀이 볼륨 복원 + 주름 개선. '5살 어려 보이는' 수준 |
| `/recipes/1/patientExplanation` | patientExplanation | 문자열 | 실로 처진 뼈대를 올리고(텐트 기둥), 초음파로 주변을 단단하게 고정한 뒤, 꺼진 곳은 필러로 채우고(쿠션), 주름 잡는 근육은 보톡스로 쉬게 합니다. |
| `/recipes/1/analogy` | analogy | 문자열 | 실 = 텐트 기둥 세우기, HIFU = 천을 팽팽하게, 필러 = 쿠션 넣기, 보톡스 = 찡그리는 습관 리셋 |
| `/recipes/1/repeatCycle` | repeatCycle | 문자열 | 실리프팅 12개월, HIFU 6개월, 보톡스 3~4개월, 필러 6~12개월 |
| `/recipes/1/followUp` | followUp | 배열 | (원소 5개) |
| `/recipes/1/followUp/0` | followUp[0] | 객체 | (키 week, action) |
| `/recipes/1/followUp/0/week` | week | 정수 | 2 |
| `/recipes/1/followUp/0/action` | action | 문자열 | 부종 완화 확인. 실 위치·대칭 체크 |
| `/recipes/1/followUp/1` | followUp[1] | 객체 | (키 week, action) |
| `/recipes/1/followUp/1/week` | week | 정수 | 6 |
| `/recipes/1/followUp/1/action` | action | 문자열 | 필러 안착 확인. 부족하면 터치업 |
| `/recipes/1/followUp/2` | followUp[2] | 객체 | (키 week, action) |
| `/recipes/1/followUp/2/week` | week | 정수 | 16 |
| `/recipes/1/followUp/2/action` | action | 문자열 | 보톡스 재시술 |
| `/recipes/1/followUp/3` | followUp[3] | 객체 | (키 week, action) |
| `/recipes/1/followUp/3/week` | week | 정수 | 24 |
| `/recipes/1/followUp/3/action` | action | 문자열 | HIFU 유지 시술 |
| `/recipes/1/followUp/4` | followUp[4] | 객체 | (키 week, action) |
| `/recipes/1/followUp/4/week` | week | 정수 | 52 |
| `/recipes/1/followUp/4/action` | action | 문자열 | 실리프팅 재시술 검토 |

### 잠정 관찰 (원문 아님)

| ID | 상태 | 근거 Pointer | 관찰 |
|---|---|---|---|
| S2-1 | P | `/recipes/1/procedures` `/recipes/1/repeatCycle` | procedures [M7,M9,M2,M1] 4개와 repeatCycle 의 시술 4개(실리프팅·HIFU·보톡스·필러), patientExplanation 의 서술 순서(실 → 초음파 → 필러 → 보톡스)가 같은 순서다. 코드↔명칭 대응을 확정하지 않는다(B-1). |
| S2-2 | P | `/recipes/1/patientExplanation` | 「초음파로 주변을 단단하게 고정한 뒤」의 「뒤」는 실 다음 초음파의 선후를 말한다. 같은 날 시행 순서인지 설명 순서인지 원문만으로 정할 수 없다(P-3). |
| S2-3 | P | `/recipes/1/followUp/2/week` `/recipes/1/repeatCycle` | followUp 의 week 16 「보톡스 재시술」·week 24 「HIFU 유지 시술」·week 52 「실리프팅 재시술 검토」는 repeatCycle 의 보톡스 3~4개월·HIFU 6개월·실리프팅 12개월과 같은 시술 순서로 놓여 있다. week↔개월 환산 기준이 원문에 없어(B-4) 일치 여부는 판정하지 않는다. 필러 6~12개월에 대응하는 followUp 재시술 항목은 없다(week 6 은 「필러 안착 확인」). |
| S2-4 | F | `/recipes/1/expectedResults` | 「볼/관자놀이」의 / 가 README 규칙의 대안(둘 중 하나)인지, 두 부위 병기인지 원문만으로 정할 수 없다(F-3). |
| S2-5 | P | `/recipes/1/followUp/0/action` | 「부종 완화 확인」은 부작용·경과로 보이는 사건(부종)을 전제한다. 어느 시술의 부종인지·빈도는 원문에 없다. |
| S2-6 | K | `/recipes/1/patientExplanation` | 첫 어절 「실로」가 부사로 오분절돼 시술 「실」이 형태소에서 사라진다(K-1). |

### 이 구획의 알려진 오분절 (Kiwi 원시 출력, 미교정)

| 규칙 | Pointer | 구간 | 원문 | 원시 토큰 | 영향 |
|---|---|---|---|---|---|
| K-1 | `/recipes/1/patientExplanation` | [0, 2] | 실로 | 실로/MAG | 시술 명칭 「실」이 사라지고 부사 「실로(참으로)」가 수식어 후보로 오탐된다. 이 문장의 첫 시술이 형태소만으로는 보이지 않는다. |
| K-2 | `/recipes/1/repeatCycle` | [32, 34] | 필러 | 필/NNG 러/EC | 시술 명칭 「필러」가 「필」+어미로 쪼개져 형태소 기반 시술 후보에서 빠진다. 같은 원장의 다른 「필러」는 NNP 로 맞게 나온다(문맥 의존). |
| K-8 | `/recipes/1/followUp/4/action` | [0, 4] | 실리프팅 | 실/NNG 리프팅/NNG | 같은 표면 「실리프팅」이 다른 두 곳(/recipes/0/followUp/2/action, /recipes/1/repeatCycle)에서는 한 토큰(NNG)으로 나온다. 토큰 문자열로 같은 표현을 모으면 이 출현이 빠진다. |
| K-9a | `/recipes/1/patientExplanation` | [22, 25] | 초음파 | 초/XPN 음파/NNG | 에너지원 명칭이 접두사+명사로 쪼개진다. 「음파」만으로 찾으면 다른 뜻과 섞일 수 있다. |

수동 표현 28건 · 전체 표현 102건 → expressions.json (segment="S2")

<a id="s3"></a>
## S3 — /recipes/2 (R3 피부 재생 골든루틴)

읽기 기록: /recipes/2 11필드·followUp 4원소 직접 읽음. 회차와 week 간격을 대조.

### 원문 값

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/recipes/2` | recipes[2] | 객체 | (키 id, name, subtitle, goal, intensity, procedures, expectedResults, patientExplanation, analogy, repeatCycle, followUp) |
| `/recipes/2/id` | id | 문자열 | R3 |
| `/recipes/2/name` | name | 문자열 | 피부 재생 골든루틴 |
| `/recipes/2/subtitle` | subtitle | 문자열 | MTS + PRP + 스킨부스터 |
| `/recipes/2/goal` | goal | 문자열 | regeneration |
| `/recipes/2/intensity` | intensity | 문자열 | 표준 |
| `/recipes/2/procedures` | procedures | 배열 | (원소 3개) |
| `/recipes/2/procedures/0` | procedures[0] | 문자열 | M12 |
| `/recipes/2/procedures/1` | procedures[1] | 문자열 | M5 |
| `/recipes/2/procedures/2` | procedures[2] | 문자열 | M4 |
| `/recipes/2/expectedResults` | expectedResults | 문자열 | 피부결 개선 + 톤 균일 + 잔주름 완화 + 탄력 향상. 3~5회 반복 시 확연한 차이 |
| `/recipes/2/patientExplanation` | patientExplanation | 문자열 | 미세 바늘로 피부에 수천 개의 아주 작은 통로를 만들고, 거기에 본인 피의 성장인자(PRP)와 수분·영양 성분(스킨부스터)을 넣어서 피부가 스스로 재생하게 만듭니다. |
| `/recipes/2/analogy` | analogy | 문자열 | MTS = 밭에 씨앗구멍 파기, PRP = 비료 뿌리기, 스킨부스터 = 물 주기 |
| `/recipes/2/repeatCycle` | repeatCycle | 문자열 | 2~4주 간격, 총 3~5회가 1클 |
| `/recipes/2/followUp` | followUp | 배열 | (원소 4개) |
| `/recipes/2/followUp/0` | followUp[0] | 객체 | (키 week, action) |
| `/recipes/2/followUp/0/week` | week | 정수 | 3 |
| `/recipes/2/followUp/0/action` | action | 문자열 | 2회차 시술 (동일 프로토콜) |
| `/recipes/2/followUp/1` | followUp[1] | 객체 | (키 week, action) |
| `/recipes/2/followUp/1/week` | week | 정수 | 6 |
| `/recipes/2/followUp/1/action` | action | 문자열 | 3회차 시술 |
| `/recipes/2/followUp/2` | followUp[2] | 객체 | (키 week, action) |
| `/recipes/2/followUp/2/week` | week | 정수 | 9 |
| `/recipes/2/followUp/2/action` | action | 문자열 | 4회차 시술 (경과에 따라 강도 조절) |
| `/recipes/2/followUp/3` | followUp[3] | 객체 | (키 week, action) |
| `/recipes/2/followUp/3/week` | week | 정수 | 12 |
| `/recipes/2/followUp/3/action` | action | 문자열 | 5회차 완료 → 결과 비교 사진. 유지 프로그램 전환 (월 1회 스킨부스터) |

### 잠정 관찰 (원문 아님)

| ID | 상태 | 근거 Pointer | 관찰 |
|---|---|---|---|
| S3-1 | B | `/recipes/2/repeatCycle` | 「총 3~5회가 1클」의 「클」이 무엇의 축약인지 원문에 없다(B-6). |
| S3-2 | P | `/recipes/2/followUp/0/week` `/recipes/2/followUp/0/action` | week 3 이 「2회차」이므로 1회차는 followUp 밖(기준 시점)으로 암묵된다. week 값 3·6·9·12 는 등간격(3)이다. week 를 주로 읽으면 repeatCycle 「2~4주 간격」 범위 안이지만, 단위·기준 시점이 정의되지 않아(B-4) 대조 후보로만 둔다. |
| S3-3 | P | `/recipes/2/followUp/3/action` `/recipes/2/repeatCycle` | followUp 은 5회차까지 적었고 repeatCycle 은 「총 3~5회」다. 5회 고정인지 상한 예시인지 원문에 없다. |
| S3-4 | P | `/recipes/2/patientExplanation` | 괄호가 일반어↔시술명 대응을 준다: 「본인 피의 성장인자(PRP)」「수분·영양 성분(스킨부스터)」. 성분 서술을 제품의 사실로 승인하지 않는다. |
| S3-5 | B | `/recipes/2/followUp/2/action` | 「경과에 따라 강도 조절」의 강도가 어느 시술의 무엇(에너지·깊이 등)인지 원문에 없다. |

### 이 구획의 알려진 오분절 (Kiwi 원시 출력, 미교정)

| 규칙 | Pointer | 구간 | 원문 | 원시 토큰 | 영향 |
|---|---|---|---|---|---|
| K-10 | `/recipes/2/followUp/0/action` | [1, 3] | 회차 | 회/NNB 차/NNB | 같은 낱말이 출현마다 1토큰/2토큰으로 갈려 회차 표현을 토큰으로 모을 때 누락·불일치가 생긴다. 숫자와 회차의 결합은 expressions 의 regex.number_unit 으로 보존했다. |
| K-10 | `/recipes/2/followUp/1/action` | [1, 3] | 회차 | 회/NNB 차/NNB | 같은 낱말이 출현마다 1토큰/2토큰으로 갈려 회차 표현을 토큰으로 모을 때 누락·불일치가 생긴다. 숫자와 회차의 결합은 expressions 의 regex.number_unit 으로 보존했다. |
| K-10 | `/recipes/2/followUp/2/action` | [1, 3] | 회차 | 회/NNB 차/NNB | 같은 낱말이 출현마다 1토큰/2토큰으로 갈려 회차 표현을 토큰으로 모을 때 누락·불일치가 생긴다. 숫자와 회차의 결합은 expressions 의 regex.number_unit 으로 보존했다. |
| K-11 | `/recipes/2/repeatCycle` | [18, 19] | 클 | 클/NNG | 분석기가 일반명사로 태깅했으나 정답 여부를 판단할 근거가 없다. |

수동 표현 29건 · 전체 표현 103건 → expressions.json (segment="S3")

<a id="s4"></a>
## S4 — /recipes/3 (R4 탄력 + 주름 집중)

읽기 기록: /recipes/3 11필드·followUp 4원소 직접 읽음. subtitle 「에너지기기」와 analogy 「HIFU/RF」, procedures [M9,M1,M4] 를 대조.

### 원문 값

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/recipes/3` | recipes[3] | 객체 | (키 id, name, subtitle, goal, intensity, procedures, expectedResults, patientExplanation, analogy, repeatCycle, followUp) |
| `/recipes/3/id` | id | 문자열 | R4 |
| `/recipes/3/name` | name | 문자열 | 탄력 + 주름 집중 |
| `/recipes/3/subtitle` | subtitle | 문자열 | 에너지기기 + 보톡스 + 스킨부스터 |
| `/recipes/3/goal` | goal | 문자열 | tightening |
| `/recipes/3/intensity` | intensity | 문자열 | 표준 |
| `/recipes/3/procedures` | procedures | 배열 | (원소 3개) |
| `/recipes/3/procedures/0` | procedures[0] | 문자열 | M9 |
| `/recipes/3/procedures/1` | procedures[1] | 문자열 | M1 |
| `/recipes/3/procedures/2` | procedures[2] | 문자열 | M4 |
| `/recipes/3/expectedResults` | expectedResults | 문자열 | 피부 타이트닝 + 주름 개선 + 피부결 향상. 시술 다음날부터 일상 가능 |
| `/recipes/3/patientExplanation` | patientExplanation | 문자열 | 초음파/고주파로 피부 속 콜라겐을 자극해서 스스로 조여지게 하고, 보톡스로 주름 잡는 근육을 쉬게 하고, 스킨부스터로 영양을 넣어 회복을 도와줍니다. |
| `/recipes/3/analogy` | analogy | 문자열 | HIFU/RF = 세탁기 건조(수축), 보톡스 = 다림질(주름 펴기), 스킨부스터 = 섬유유연제(부드럽게) |
| `/recipes/3/repeatCycle` | repeatCycle | 문자열 | HIFU 6개월, 보톡스 3~4개월, 스킨부스터 월 1회 |
| `/recipes/3/followUp` | followUp | 배열 | (원소 4개) |
| `/recipes/3/followUp/0` | followUp[0] | 객체 | (키 week, action) |
| `/recipes/3/followUp/0/week` | week | 정수 | 4 |
| `/recipes/3/followUp/0/action` | action | 문자열 | 보톡스 효과 확인. 스킨부스터 2회차 |
| `/recipes/3/followUp/1` | followUp[1] | 객체 | (키 week, action) |
| `/recipes/3/followUp/1/week` | week | 정수 | 8 |
| `/recipes/3/followUp/1/action` | action | 문자열 | 스킨부스터 3회차 |
| `/recipes/3/followUp/2` | followUp[2] | 객체 | (키 week, action) |
| `/recipes/3/followUp/2/week` | week | 정수 | 16 |
| `/recipes/3/followUp/2/action` | action | 문자열 | 보톡스 재시술 + 스킨부스터 유지 |
| `/recipes/3/followUp/3` | followUp[3] | 객체 | (키 week, action) |
| `/recipes/3/followUp/3/week` | week | 정수 | 24 |
| `/recipes/3/followUp/3/action` | action | 문자열 | HIFU 재시술 검토 |

### 잠정 관찰 (원문 아님)

| ID | 상태 | 근거 Pointer | 관찰 |
|---|---|---|---|
| S4-1 | F | `/recipes/3/subtitle` `/recipes/3/analogy` `/recipes/3/patientExplanation` `/recipes/3/procedures/0` | 같은 자리에 「에너지기기」(subtitle)·「초음파/고주파」(patientExplanation)·「HIFU/RF」(analogy)·「HIFU」(repeatCycle·followUp)가 쓰이고 procedures 는 코드 하나다. 대안 표기가 한 코드 안의 장비 선택인지 별개 시술인지 정하지 않는다(F-1). |
| S4-2 | P | `/recipes/3/expectedResults` | 「시술 다음날부터 일상 가능」은 회복 시점 표현이다. 어느 시술 기준인지, 전부 함께 받은 경우인지 원문에 없다. |
| S4-3 | P | `/recipes/3/followUp/0/action` `/recipes/3/followUp/1/action` `/recipes/3/repeatCycle` | 스킨부스터 2회차(week 4)·3회차(week 8)와 repeatCycle 「스킨부스터 월 1회」가 같은 시술의 반복을 말한다. week↔월 환산은 원문 정의가 없어(B-4) 일치 판정을 하지 않는다. |

### 이 구획의 알려진 오분절 (Kiwi 원시 출력, 미교정)

| 규칙 | Pointer | 구간 | 원문 | 원시 토큰 | 영향 |
|---|---|---|---|---|---|
| K-9a | `/recipes/3/patientExplanation` | [0, 3] | 초음파 | 초/XPN 음파/NNG | 에너지원 명칭이 접두사+명사로 쪼개진다. 「음파」만으로 찾으면 다른 뜻과 섞일 수 있다. |
| K-9b | `/recipes/3/patientExplanation` | [4, 7] | 고주파 | 고/XPN 주파/NNG | K-9a 와 같다. |
| K-10 | `/recipes/3/followUp/0/action` | [18, 20] | 회차 | 회/NNB 차/NNB | 같은 낱말이 출현마다 1토큰/2토큰으로 갈려 회차 표현을 토큰으로 모을 때 누락·불일치가 생긴다. 숫자와 회차의 결합은 expressions 의 regex.number_unit 으로 보존했다. |
| K-10 | `/recipes/3/followUp/1/action` | [7, 9] | 회차 | 회/NNB 차/NNB | 같은 낱말이 출현마다 1토큰/2토큰으로 갈려 회차 표현을 토큰으로 모을 때 누락·불일치가 생긴다. 숫자와 회차의 결합은 expressions 의 regex.number_unit 으로 보존했다. |

수동 표현 24건 · 전체 표현 83건 → expressions.json (segment="S4")

<a id="s5"></a>
## S5 — /recipes/4 (R5 모공/흉터 집중)

읽기 기록: /recipes/4 11필드·followUp 4원소 직접 읽음. 조건 「평가 후 결정」의 범위를 앞뒤 원소와 함께 읽음.

### 원문 값

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/recipes/4` | recipes[4] | 객체 | (키 id, name, subtitle, goal, intensity, procedures, expectedResults, patientExplanation, analogy, repeatCycle, followUp) |
| `/recipes/4/id` | id | 문자열 | R5 |
| `/recipes/4/name` | name | 문자열 | 모공/흉터 집중 |
| `/recipes/4/subtitle` | subtitle | 문자열 | 니들RF + PRP |
| `/recipes/4/goal` | goal | 문자열 | texture |
| `/recipes/4/intensity` | intensity | 문자열 | 적극 |
| `/recipes/4/procedures` | procedures | 배열 | (원소 2개) |
| `/recipes/4/procedures/0` | procedures[0] | 문자열 | M11 |
| `/recipes/4/procedures/1` | procedures[1] | 문자열 | M5 |
| `/recipes/4/expectedResults` | expectedResults | 문자열 | 모공 축소 + 여드름 흉터 개선 + 피부결 정돈. 3~5회 반복 시 확연한 개선 |
| `/recipes/4/patientExplanation` | patientExplanation | 문자열 | 미세 바늘이 피부 속으로 들어가서 고주파 열을 쏩니다. 이 열이 늘어난 모공과 흉터 조직을 수축시키고, PRP 성장인자가 새 피부 재생을 촉진합니다. |
| `/recipes/4/analogy` | analogy | 문자열 | 니들RF = 피부 속에서 정밀 용접, PRP = 용접 부위에 영양제 |
| `/recipes/4/repeatCycle` | repeatCycle | 문자열 | 4~6주 간격, 총 3~5회 |
| `/recipes/4/followUp` | followUp | 배열 | (원소 4개) |
| `/recipes/4/followUp/0` | followUp[0] | 객체 | (키 week, action) |
| `/recipes/4/followUp/0/week` | week | 정수 | 5 |
| `/recipes/4/followUp/0/action` | action | 문자열 | 2회차 (에너지 레벨 조절 가능) |
| `/recipes/4/followUp/1` | followUp[1] | 객체 | (키 week, action) |
| `/recipes/4/followUp/1/week` | week | 정수 | 10 |
| `/recipes/4/followUp/1/action` | action | 문자열 | 3회차 |
| `/recipes/4/followUp/2` | followUp[2] | 객체 | (키 week, action) |
| `/recipes/4/followUp/2/week` | week | 정수 | 15 |
| `/recipes/4/followUp/2/action` | action | 문자열 | 4회차 (개선도 평가 후 결정) |
| `/recipes/4/followUp/3` | followUp[3] | 객체 | (키 week, action) |
| `/recipes/4/followUp/3/week` | week | 정수 | 20 |
| `/recipes/4/followUp/3/action` | action | 문자열 | 5회차 완료 → 유지: 3개월마다 1회 |

### 잠정 관찰 (원문 아님)

| ID | 상태 | 근거 Pointer | 관찰 |
|---|---|---|---|
| S5-1 | P | `/recipes/4/followUp/2/action` `/recipes/4/followUp/3/action` | 4회차는 「개선도 평가 후 결정」으로 조건부인데, 5회차는 조건 없이 적혀 있다. 조건이 4회차만인지 이후 회차 전체인지 원문만으로 정할 수 없다(P-5). |
| S5-2 | B | `/recipes/4/followUp/3/action` | 「유지: 3개월마다 1회」의 유지 대상 시술(니들RF·PRP·둘 다)이 원문에 없다(B-7). |
| S5-3 | P | `/recipes/4/patientExplanation` | 「이 열이」는 앞 문장의 「고주파 열」을 가리키는 문장 간 지시다. 두 문장을 함께 보존해야 기전 서술이 이어진다. |
| S5-4 | F | `/recipes/4/name` | name 「모공/흉터 집중」의 / 가 대안인지 병기인지 정하지 않는다. expectedResults 는 「모공 축소 + 여드름 흉터 개선」으로 둘 다 나열한다(F-3). |
| S5-5 | K | `/recipes/4/patientExplanation` `/recipes/4/followUp/2/action` | 「새 피부」의 새가 동사로(K-4), 「개선도」가 개선+조사로(K-5) 오분절. |

### 이 구획의 알려진 오분절 (Kiwi 원시 출력, 미교정)

| 규칙 | Pointer | 구간 | 원문 | 원시 토큰 | 영향 |
|---|---|---|---|---|---|
| K-4 | `/recipes/4/patientExplanation` | [68, 69] | 새 | 새/VV 어/EC | 「새 피부」의 관형 수식이 동사 「새다」로 바뀐다. 같은 구가 /recipes/6/patientExplanation 에서는 새/MM 으로 맞게 나온다. |
| K-5 | `/recipes/4/followUp/2/action` | [5, 8] | 개선도 | 개선/NNG 도/JX | 평가 대상인 「개선의 정도」가 「개선 + 보조사 도」로 바뀐다. |
| K-9b | `/recipes/4/patientExplanation` | [19, 22] | 고주파 | 고/XPN 주파/NNG | K-9a 와 같다. |
| K-10 | `/recipes/4/followUp/0/action` | [1, 3] | 회차 | 회/NNB 차/NNB | 같은 낱말이 출현마다 1토큰/2토큰으로 갈려 회차 표현을 토큰으로 모을 때 누락·불일치가 생긴다. 숫자와 회차의 결합은 expressions 의 regex.number_unit 으로 보존했다. |
| K-10 | `/recipes/4/followUp/1/action` | [1, 3] | 회차 | 회/NNB 차/NNB | 같은 낱말이 출현마다 1토큰/2토큰으로 갈려 회차 표현을 토큰으로 모을 때 누락·불일치가 생긴다. 숫자와 회차의 결합은 expressions 의 regex.number_unit 으로 보존했다. |
| K-10 | `/recipes/4/followUp/2/action` | [1, 3] | 회차 | 회/NNB 차/NNB | 같은 낱말이 출현마다 1토큰/2토큰으로 갈려 회차 표현을 토큰으로 모을 때 누락·불일치가 생긴다. 숫자와 회차의 결합은 expressions 의 regex.number_unit 으로 보존했다. |

수동 표현 22건 · 전체 표현 90건 → expressions.json (segment="S5")

<a id="s6"></a>
## S6 — /recipes/5 (R6 동안 쁘띠 패키지)

읽기 기록: /recipes/5 11필드·followUp 4원소 직접 읽음. 부위 나열과 시술의 짝을 문장 구조로 확인.

### 원문 값

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/recipes/5` | recipes[5] | 객체 | (키 id, name, subtitle, goal, intensity, procedures, expectedResults, patientExplanation, analogy, repeatCycle, followUp) |
| `/recipes/5/id` | id | 문자열 | R6 |
| `/recipes/5/name` | name | 문자열 | 동안 쁘띠 패키지 |
| `/recipes/5/subtitle` | subtitle | 문자열 | 보톡스 + 필러 (런치타임 시술) |
| `/recipes/5/goal` | goal | 문자열 | anti-aging |
| `/recipes/5/intensity` | intensity | 문자열 | 기본 |
| `/recipes/5/procedures` | procedures | 배열 | (원소 2개) |
| `/recipes/5/procedures/0` | procedures[0] | 문자열 | M1 |
| `/recipes/5/procedures/1` | procedures[1] | 문자열 | M2 |
| `/recipes/5/expectedResults` | expectedResults | 문자열 | 주름 개선 + 볼륨 복원. 30분 내 완료. 바로 일상 복귀 |
| `/recipes/5/patientExplanation` | patientExplanation | 문자열 | 보톡스로 주름 잡는 근육을 쉬게 해서 이마·미간·눈가 주름을 펴고, 필러로 꺼진 팔자·볼·턱을 자연스럽게 채워서 동안 얼굴을 만듭니다. |
| `/recipes/5/analogy` | analogy | 문자열 | 보톡스 = 구겨진 종이를 펴는 것, 필러 = 꺼진 곳에 솜 넣기 |
| `/recipes/5/repeatCycle` | repeatCycle | 문자열 | 보톡스 3~4개월, 필러 6~12개월 |
| `/recipes/5/followUp` | followUp | 배열 | (원소 4개) |
| `/recipes/5/followUp/0` | followUp[0] | 객체 | (키 week, action) |
| `/recipes/5/followUp/0/week` | week | 정수 | 2 |
| `/recipes/5/followUp/0/action` | action | 문자열 | 보톡스 효과 확인. 부족하면 터치업 |
| `/recipes/5/followUp/1` | followUp[1] | 객체 | (키 week, action) |
| `/recipes/5/followUp/1/week` | week | 정수 | 4 |
| `/recipes/5/followUp/1/action` | action | 문자열 | 필러 안착 확인 |
| `/recipes/5/followUp/2` | followUp[2] | 객체 | (키 week, action) |
| `/recipes/5/followUp/2/week` | week | 정수 | 16 |
| `/recipes/5/followUp/2/action` | action | 문자열 | 보톡스 재시술 |
| `/recipes/5/followUp/3` | followUp[3] | 객체 | (키 week, action) |
| `/recipes/5/followUp/3/week` | week | 정수 | 48 |
| `/recipes/5/followUp/3/action` | action | 문자열 | 필러 재시술 검토 |

### 잠정 관찰 (원문 아님)

| ID | 상태 | 근거 Pointer | 관찰 |
|---|---|---|---|
| S6-1 | P | `/recipes/5/patientExplanation` | 문장 구조상 보톡스 ↔ 이마·미간·눈가 주름, 필러 ↔ 팔자·볼·턱이 짝이다. 부위 목록을 시술의 적용 범위 전체로 확정하지 않는다. |
| S6-2 | K | `/recipes/5/patientExplanation` | 「이마」가 「이/MM 마/NNG」로 오분절돼 부위가 형태소에서 사라진다(K-3). |
| S6-3 | P | `/recipes/5/subtitle` `/recipes/5/expectedResults` | 「런치타임 시술」과 「30분 내 완료」「바로 일상 복귀」는 소요시간·회복 표현이다. 30분이 두 시술 합계인지 원문에 없다. |
| S6-4 | P | `/recipes/5/followUp/3/week` `/recipes/5/repeatCycle` | week 48 「필러 재시술 검토」와 repeatCycle 「필러 6~12개월」이 같은 시술의 재시술을 말한다. 환산 기준이 없어(B-4) 일치 판정은 하지 않는다. |

### 이 구획의 알려진 오분절 (Kiwi 원시 출력, 미교정)

| 규칙 | Pointer | 구간 | 원문 | 원시 토큰 | 영향 |
|---|---|---|---|---|---|
| K-2 | `/recipes/5/analogy` | [20, 22] | 필러 | 필/NNG 러/EC | 시술 명칭 「필러」가 「필」+어미로 쪼개져 형태소 기반 시술 후보에서 빠진다. 같은 원장의 다른 「필러」는 NNP 로 맞게 나온다(문맥 의존). |
| K-2 | `/recipes/5/repeatCycle` | [11, 13] | 필러 | 필/NNG 러/EC | 시술 명칭 「필러」가 「필」+어미로 쪼개져 형태소 기반 시술 후보에서 빠진다. 같은 원장의 다른 「필러」는 NNP 로 맞게 나온다(문맥 의존). |
| K-3 | `/recipes/5/patientExplanation` | [21, 23] | 이마 | 이/MM 마/NNG | 부위 「이마」가 관형사 「이」+「마」로 쪼개져 부위 후보에서 사라지고 관형사 수식어 후보로 오탐된다. |
| K-13 | `/recipes/5/name` | [0, 2] | 동안 | 동안/NNG | 태그는 맞지만 기본형·태그만으로는 동형이의어가 구분되지 않는다. 부정 키워드 「안 」 정규식이 이 두 곳을 오탐했다(expressions review 참조). |
| K-13 | `/recipes/5/patientExplanation` | [63, 65] | 동안 | 동안/NNG | 태그는 맞지만 기본형·태그만으로는 동형이의어가 구분되지 않는다. 부정 키워드 「안 」 정규식이 이 두 곳을 오탐했다(expressions review 참조). |

수동 표현 23건 · 전체 표현 79건 → expressions.json (segment="S6")

<a id="s7"></a>
## S7 — /recipes/6 (R7 레이저 토닝 + 재생)

읽기 기록: /recipes/6 11필드·followUp 4원소 직접 읽음. 「재생」이 가리키는 시술 묶음을 subtitle·repeatCycle·followUp 에서 대조.

### 원문 값

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/recipes/6` | recipes[6] | 객체 | (키 id, name, subtitle, goal, intensity, procedures, expectedResults, patientExplanation, analogy, repeatCycle, followUp) |
| `/recipes/6/id` | id | 문자열 | R7 |
| `/recipes/6/name` | name | 문자열 | 레이저 토닝 + 재생 |
| `/recipes/6/subtitle` | subtitle | 문자열 | 색소/톤 개선 + 피부 회복 |
| `/recipes/6/goal` | goal | 문자열 | tone |
| `/recipes/6/intensity` | intensity | 문자열 | 표준 |
| `/recipes/6/procedures` | procedures | 배열 | (원소 3개) |
| `/recipes/6/procedures/0` | procedures[0] | 문자열 | M8 |
| `/recipes/6/procedures/1` | procedures[1] | 문자열 | M5 |
| `/recipes/6/procedures/2` | procedures[2] | 문자열 | M4 |
| `/recipes/6/expectedResults` | expectedResults | 문자열 | 색소 개선 + 톤 균일 + 피부 광채. 5~10회 반복 시 확연한 개선 |
| `/recipes/6/patientExplanation` | patientExplanation | 문자열 | 레이저가 색소를 잘게 부수고, PRP 성장인자와 스킨부스터가 새 피부 재생을 촉진해서 맑고 균일한 피부톤을 만듭니다. |
| `/recipes/6/analogy` | analogy | 문자열 | 레이저 = 얼룩 지우개, PRP = 새 도화지 만들기, 스킨부스터 = 코팅 |
| `/recipes/6/repeatCycle` | repeatCycle | 문자열 | 2~4주 간격, 레이저 5~10회 + 재생 3~5회 |
| `/recipes/6/followUp` | followUp | 배열 | (원소 4개) |
| `/recipes/6/followUp/0` | followUp[0] | 객체 | (키 week, action) |
| `/recipes/6/followUp/0/week` | week | 정수 | 3 |
| `/recipes/6/followUp/0/action` | action | 문자열 | 2회차 레이저 + 재생 |
| `/recipes/6/followUp/1` | followUp[1] | 객체 | (키 week, action) |
| `/recipes/6/followUp/1/week` | week | 정수 | 6 |
| `/recipes/6/followUp/1/action` | action | 문자열 | 3회차 (에너지 조절) |
| `/recipes/6/followUp/2` | followUp[2] | 객체 | (키 week, action) |
| `/recipes/6/followUp/2/week` | week | 정수 | 12 |
| `/recipes/6/followUp/2/action` | action | 문자열 | 중간 평가. 필요시 레이저 종류 변경 |
| `/recipes/6/followUp/3` | followUp[3] | 객체 | (키 week, action) |
| `/recipes/6/followUp/3/week` | week | 정수 | 24 |
| `/recipes/6/followUp/3/action` | action | 문자열 | 유지: 월 1회 토닝 + 스킨부스터 |

### 잠정 관찰 (원문 아님)

| ID | 상태 | 근거 Pointer | 관찰 |
|---|---|---|---|
| S7-1 | P | `/recipes/6/name` `/recipes/6/repeatCycle` `/recipes/6/followUp/0/action` `/recipes/6/procedures` | 「재생」이 시술군 이름처럼 쓰인다(「레이저 5~10회 + 재생 3~5회」「2회차 레이저 + 재생」). patientExplanation 문맥상 PRP·스킨부스터 묶음으로 보이나 확정하지 않는다(P-6). |
| S7-2 | I | `/recipes/6/repeatCycle` `/recipes/6/followUp/0/action` | repeatCycle 은 레이저와 재생의 횟수를 다르게(5~10회 vs 3~5회) 적었는데, followUp 은 회차마다 「레이저 + 재생」을 함께 적는다(2회차). 회차 번호가 어느 시술 기준인지 원문 안에서 맞춰지지 않는다(I-1). |
| S7-3 | P | `/recipes/6/followUp/3/action` | 「유지: 월 1회 토닝 + 스킨부스터」의 「토닝」은 name 의 「레이저 토닝」과 같은 것으로 보인다. 「월 1회」가 둘 다에 걸리는지 원문에 없다. |
| S7-4 | P | `/recipes/6/followUp/2/action` | 「필요시 레이저 종류 변경」은 조건부 변경이다. 어떤 종류로 바뀌는지 원문에 없다. |

### 이 구획의 알려진 오분절 (Kiwi 원시 출력, 미교정)

| 규칙 | Pointer | 구간 | 원문 | 원시 토큰 | 영향 |
|---|---|---|---|---|---|
| K-6 | `/recipes/6/followUp/2/action` | [7, 10] | 필요시 | 필요시/NNG | 분절 자체는 원문 표기(붙여 씀)를 따른 것이나, 조건 표지 「시」가 한 명사 안에 숨어 형태소 기반 조건 후보(NNB 시)에서 빠진다. |
| K-10 | `/recipes/6/followUp/0/action` | [1, 3] | 회차 | 회/NNB 차/NNB | 같은 낱말이 출현마다 1토큰/2토큰으로 갈려 회차 표현을 토큰으로 모을 때 누락·불일치가 생긴다. 숫자와 회차의 결합은 expressions 의 regex.number_unit 으로 보존했다. |
| K-10 | `/recipes/6/followUp/1/action` | [1, 3] | 회차 | 회/NNB 차/NNB | 같은 낱말이 출현마다 1토큰/2토큰으로 갈려 회차 표현을 토큰으로 모을 때 누락·불일치가 생긴다. 숫자와 회차의 결합은 expressions 의 regex.number_unit 으로 보존했다. |
| K-12 | `/recipes/6/patientExplanation` | [25, 26] | 와 | 와/JKB | 부사격(함께)으로 태깅되면 두 시술이 병렬 주어라는 구조가 형태소 정보에서 약해진다. /recipes/2/patientExplanation 의 「(PRP)와」는 JC. |

수동 표현 21건 · 전체 표현 92건 → expressions.json (segment="S7")

## 기록 위치

- [source-map.json](./source-map.json)
- [morphology.json](./morphology.json)
- [expressions.json](./expressions.json)
- [coverage.json](./coverage.json)
- [issues.md](./issues.md)
- [validation.md](./validation.md)
- [build.py](./build.py)
- [verify.py](./verify.py)
- [manual-expressions.json](./manual-expressions.json)
- [manual-observations.json](./manual-observations.json)
- [segmentation-review.json](./segmentation-review.json)
