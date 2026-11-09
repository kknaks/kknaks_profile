# pih-risk.json — 1차 조사 (읽기용)

> **1차 범위 종료: 예** (전 구획 직접 읽기·구조/값 수집·형태소·표현 수집·기계 검증·읽기 검토 통과)
> **원장 전체 완료 아님** — B 8 묶음 · I 3 · P 2 · F 7 · K 3 묶음(오분절 51 출현) 열림. C(현재 사용자 결정 필요) 0 — 근거는 [issues.md](./issues.md) 「C 0 의 근거」.

| 상태 항목 | 내용 |
|---|---|
| 전수 읽기 | S0~S8 9 구획 전부 직접 읽음(구획별 기록 `manual/S*.json`, 읽기 상태 `coverage.json`). 처음 1회 원문 전체 통독 후 구획별 순차 재독 |
| 구조·값 수집 | 노드 344 / 말단 288 / 키 출현 249 — `source-map.json` |
| 형태소·표현 수집 | Kiwi 0.24.1 cong(스레드 1) 적용 448 · 제외 89(사유 기록) · 토큰 2,083 — `morphology.json`. 수동 표현 310 + regex 보조 107(전부 수동 구간에 포함) — `expressions.json` |
| 기계 검증 | `verify.py` failure 0 — [validation.md](./validation.md) |
| 읽기 검토 | 수식·조건·부정·가능성·비교 단서 131 개가 모두 수동 표현 구간 안에 있음 + 구획별 재독(validation.md §3) |
| 알려진 분석 오류 | 오분절 51 출현 미교정 기록(K1) |
| 열린 미결 | [issues.md](./issues.md) |
| 후속 의미 조사 | 시작 안 함(F1~F7) |

**읽는 법.** 각 구획 파일 §1 은 원문 값만(원본 컬럼명·자료형·JSON 리터럴·파일 구간), §2 는 잠정 관찰(상태 문자 + 근거 Pointer), §3 은 수동 표현, §4 는 형태소 주의 출현, §5 는 미결. 원문과 관찰을 한 칸에 섞지 않았다.


## 원본

- 경로 `orchestration/work/phub-recommend/bronze/phub-ledger/pih-risk.json` · sha256 `cb6e9305113d0b47f447eb314ce3bb34d0278bbc8bdf26bc3303d323028575c8` · 11875 bytes · 8318 코드포인트 · 줄바꿈 0 · 백슬래시 이스케이프 0 · 중복 키 0
- 노드 344 (array 27, object 29, string 288) · 말단 288 · 빈 컨테이너 0 · 빈 문자열 0 · 키 출현 249 (서로 다른 키 24)

## 컬럼 구성 표 (원본 컬럼명/경로 패턴 그대로)

`{i}` = procedures 배열 인덱스 0–25, `{j}` = risk_factors 배열 인덱스. 원문 예시는 해당 패턴의 첫 출현.

| 원본 경로 패턴 | 자료형 | 중첩(컨테이너[자식수]) | 출현 수 | 빈 값 | 원문 예시 | 예시 위치 |
|---|---|---|---|---|---|---|
| `(root)` | object | object[6] | 1 | 0 | (컨테이너) | `(root)` |
| `/version` | string | 말단 | 1 | 0 | "1.0" | `/version` |
| `/updated` | string | 말단 | 1 | 0 | "2026-04-05" | `/updated` |
| `/description` | string | 말단 | 1 | 0 | "시술별 PIH(Post-Inflammatory Hyperpigmentation) 위험도. Fitzpatrick skin type III-IV (한국인 대다수)를 기준으로 작성" | `/description` |
| `/risk_levels` | object | object[5] | 1 | 0 | (컨테이너) | `/risk_levels` |
| `/risk_levels/very_low` | string | 말단 | 1 | 0 | "< 1%" | `/risk_levels/very_low` |
| `/risk_levels/low` | string | 말단 | 1 | 0 | "1-5%" | `/risk_levels/low` |
| `/risk_levels/moderate` | string | 말단 | 1 | 0 | "5-15%" | `/risk_levels/moderate` |
| `/risk_levels/high` | string | 말단 | 1 | 0 | "15-30%" | `/risk_levels/high` |
| `/risk_levels/very_high` | string | 말단 | 1 | 0 | "> 30%" | `/risk_levels/very_high` |
| `/notes` | object | object[4] | 1 | 0 | (컨테이너) | `/notes` |
| `/notes/M1_to_M7` | string | 말단 | 1 | 0 | "주사 시술(M1 보톡스, M2 필러, M3 바이오스티뮬레이터, M4 스킨부스터, M5 PRP, M6 지방이식, M7 실리프팅)은 표피 손상이 없어 PIH 해당 없음" | `/notes/M1_to_M7` |
| `/notes/M10` | string | 말단 | 1 | 0 | "HIFES/EMS는 피부 표면에 작용하지 않으므로 PIH 해당 없음" | `/notes/M10` |
| `/notes/M16` | string | 말단 | 1 | 0 | "수액치료는 정맥주사이므로 PIH 해당 없음" | `/notes/M16` |
| `/notes/M17` | string | 말단 | 1 | 0 | "줄기세포치료(도포/주사)는 표피 손상 최소로 PIH 해당 없음" | `/notes/M17` |
| `/procedures` | array | array[26] | 1 | 0 | (컨테이너) | `/procedures` |
| `/procedures/{i}` | object | object[9] | 26 | 0 | (컨테이너) | `/procedures/0` |
| `/procedures/{i}/category` | string | 말단 | 26 | 0 | "M8" | `/procedures/0/category` |
| `/procedures/{i}/subcategory` | string | 말단 | 26 | 0 | "색소/토닝" | `/procedures/0/subcategory` |
| `/procedures/{i}/name` | string | 말단 | 26 | 0 | "레이저 토닝 (QS Nd:YAG 1064nm 저에너지)" | `/procedures/0/name` |
| `/procedures/{i}/procedure_ref` | string | 말단 | 26 | 0 | "M8-1-1" | `/procedures/0/procedure_ref` |
| `/procedures/{i}/pih_risk` | string | 말단 | 26 | 0 | "low" | `/procedures/0/pih_risk` |
| `/procedures/{i}/pih_rate` | string | 말단 | 26 | 0 | "~5%" | `/procedures/0/pih_rate` |
| `/procedures/{i}/fitzpatrick_note` | string | 말단 | 26 | 0 | "III-IV에서도 비교적 안전. 저에너지 반복 조사로 멜라닌 점진적 제거" | `/procedures/0/fitzpatrick_note` |
| `/procedures/{i}/risk_factors` | array | array[1], array[2], array[3], array[4], array[5] | 26 | 0 | (컨테이너) | `/procedures/0/risk_factors` |
| `/procedures/{i}/risk_factors/{j}` | string | 말단 | 68 | 0 | "과도한 fluence" | `/procedures/0/risk_factors/0` |
| `/procedures/{i}/prevention` | string | 말단 | 26 | 0 | "시술 간격 2-4주 유지, SPF 50+ 자외선 차단, 저에너지 유지" | `/procedures/0/prevention` |

## 키 구성의 변형

- procedures 26 항목의 키 순서: category → subcategory → name → procedure_ref → pih_risk → pih_rate → fitzpatrick_note → risk_factors → prevention ×26
- 선택적 필드: 없음(26 항목 모두 9 키). 빈 문자열·빈 배열·빈 객체·null: 0. 숫자·불리언 말단: 0(수치는 모두 문자열 — 예 `"~5%"`, `"1.0"`).
- risk_factors 길이 분포: 1개 3항목, 2개 9항목, 3개 10항목, 4개 3항목, 5개 1항목
- 열거/코드 값 분포 — pih_risk: low 14, moderate 5, very_high 1, high 2, very_low 4 · category: M8 15, M9 3, M11 2, M12 1, M13 2, M15 3

## 대조 — pih_risk · pih_rate · risk_levels (원문 값 / 잠정 관찰 분리)

| Pointer | name (원문) | pih_risk (원문) | risk_levels[pih_risk] (원문) | pih_rate (원문) | 잠정 관찰 |
|---|---|---|---|---|---|
| `/procedures/0` | 레이저 토닝 (QS Nd:YAG 1064nm 저에너지) | low | 1-5% | ~5% | low 상한 5 와 맞닿음 — B2 |
| `/procedures/1` | QS Nd:YAG 1064nm (표준 에너지, 색소 치료) | moderate | 5-15% | ~10% | 범위 안 |
| `/procedures/2` | 피코토닝 (피코초 Nd:YAG 1064nm) | low | 1-5% | 1-3% | 범위 안 |
| `/procedures/3` | 피코슈어 (755nm 피코초) | low | 1-5% | 2-5% | 범위 안 |
| `/procedures/4` | CO2 프락셔널 (10600nm, 박리성) | very_high | > 30% | ~50% | 범위 안 |
| `/procedures/5` | 어븀야그(Er:YAG) 프락셔널 (2940nm, 박리성) | high | 15-30% | 10-20% | **I1** 하한 10 이 high 범위 밖 |
| `/procedures/6` | 프락셀듀얼 (1550+1927nm, 비박리~얕은 박리) | moderate | 5-15% | 5-15% | 범위 안 |
| `/procedures/7` | 피코프락셀 (비박리성 피코초) | low | 1-5% | 1-3% | 범위 안 |
| `/procedures/8` | 피코슈어 프락셀 (755nm 비박리성) | low | 1-5% | 1-3% | 범위 안 |
| `/procedures/9` | IPL (560-950nm 광대역) | moderate | 5-15% | 5-10% | 범위 안 |
| `/procedures/10` | 브이빔 (PDL 595nm) | low | 1-5% | 1-5% | 범위 안 |
| `/procedures/11` | 엑셀브이/더마브이 (LP 532+1064nm) | low | 1-5% | 1-3% | 범위 안 |
| `/procedures/12` | 장파장 제모 (Nd:YAG 1064nm LP) | very_low | < 1% | ~1% | **I2** ~1% 가 '< 1%' 경계 |
| `/procedures/13` | 알렉산드라이트 제모 (755nm LP) | low | 1-5% | 2-5% | 범위 안 |
| `/procedures/14` | 다이오드 제모 (800-810nm LP) | low | 1-5% | 1-3% | 범위 안 |
| `/procedures/15` | HIFU (울쎄라, 슈링크 등) | very_low | < 1% | < 1% | 범위 안 |
| `/procedures/16` | 써마지/올리지오 (모노폴라 RF) | very_low | < 1% | < 1% | 범위 안 |
| `/procedures/17` | 인모드 (바이폴라 RF + IPL/다이오드) | low | 1-5% | 1-5% | 범위 안 |
| `/procedures/18` | 니들RF - 절연침 (포텐자, 시크릿RF 등) | very_low | < 1% | < 1% | 범위 안 |
| `/procedures/19` | 니들RF - 비절연침 | low | 1-5% | 2-5% | 범위 안 |
| `/procedures/20` | 마이크로니들링 (MTS, 더마롤러/더마펜) | low | 1-5% | 1-5% | 범위 안 |
| `/procedures/21` | 플라즈마 (콜드플라즈마) | low | 1-5% | 2-5% | 범위 안 |
| `/procedures/22` | 플라즈마 (열플라즈마/플렉서) | moderate | 5-15% | 5-15% | 범위 안 |
| `/procedures/23` | AHA/BHA 필링 (표재성) | low | 1-5% | 1-5% | 범위 안 |
| `/procedures/24` | TCA 필링 (중간-심층) | high | 15-30% | 15-30% | 범위 안 |
| `/procedures/25` | 제스너 필링 | moderate | 5-15% | 5-10% | 범위 안 |

## 구획 목차 (모든 값은 구획 파일에 원본 컬럼명 그대로 실림)

| 구획 | 범위 | 소유 Pointer | 읽기 상태 | 마지막 읽은 Pointer | 파일 |
|---|---|---|---|---|---|
| S0 | 상위 메타데이터 — version·updated·description·risk_levels·notes + 루트·procedures 배열 컨테이너 | ``, `/procedures`, `/version`, `/updated`, `/description`, `/risk_levels`, `/notes` | 직접 읽음 | `/notes/M17` | [review-part-S0.md](./review-part-S0.md) |
| S1 | procedures 0–3 · M8 색소/토닝 | `/procedures/0`, `/procedures/1`, `/procedures/2`, `/procedures/3` | 직접 읽음 | `/procedures/3/prevention` | [review-part-S1.md](./review-part-S1.md) |
| S2 | procedures 4–8 · M8 프락셔널 | `/procedures/4`, `/procedures/5`, `/procedures/6`, `/procedures/7`, `/procedures/8` | 직접 읽음 | `/procedures/8/prevention` | [review-part-S2.md](./review-part-S2.md) |
| S3 | procedures 9–11 · M8 IPL·혈관 | `/procedures/9`, `/procedures/10`, `/procedures/11` | 직접 읽음 | `/procedures/11/prevention` | [review-part-S3.md](./review-part-S3.md) |
| S4 | procedures 12–14 · M8 제모 | `/procedures/12`, `/procedures/13`, `/procedures/14` | 직접 읽음 | `/procedures/14/prevention` | [review-part-S4.md](./review-part-S4.md) |
| S5 | procedures 15–17 · M9 HIFU·RF·복합 에너지 | `/procedures/15`, `/procedures/16`, `/procedures/17` | 직접 읽음 | `/procedures/17/prevention` | [review-part-S5.md](./review-part-S5.md) |
| S6 | procedures 18–20 · M11 니들RF·M12 MTS | `/procedures/18`, `/procedures/19`, `/procedures/20` | 직접 읽음 | `/procedures/20/prevention` | [review-part-S6.md](./review-part-S6.md) |
| S7 | procedures 21–22 · M13 플라즈마 | `/procedures/21`, `/procedures/22` | 직접 읽음 | `/procedures/22/prevention` | [review-part-S7.md](./review-part-S7.md) |
| S8 | procedures 23–25 · M15 케미컬필링 | `/procedures/23`, `/procedures/24`, `/procedures/25` | 직접 읽음 | `/procedures/25/prevention` | [review-part-S8.md](./review-part-S8.md) |

