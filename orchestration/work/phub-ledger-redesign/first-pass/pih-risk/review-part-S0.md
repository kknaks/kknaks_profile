# S0 — 상위 메타데이터 — version·updated·description·risk_levels·notes + 루트·procedures 배열 컨테이너

[← review.md 목차](./review.md)

- 읽기 상태: 직접 읽음 · 마지막 읽은 Pointer `/notes/M17`
- 공동 참조 문맥(소유 아님): 없음

## 1. 원문 값 (원본 컬럼명 그대로 · 원문 순서)

원문 값 칸은 디코딩 값을 JSON 리터럴로 그대로 보인다. 관찰은 이 표에 섞지 않고 §2 에 둔다.

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 파일 cp [s,e) | 표현 ID |
|---|---|---|---|---|---|
| `(root)` | (root) | object | (object, 자식 6) | 0–8318 |  |
| `/version` | version | string | "1.0" | 11–16 |  |
| `/updated` | updated | string | "2026-04-05" | 27–39 |  |
| `/description` | description | string | "시술별 PIH(Post-Inflammatory Hyperpigmentation) 위험도. Fitzpatrick skin type III-IV (한국인 대다수)를 기준으로 작성" | 54–153 | E0000, E0001, E0002, E0003, E0004 |
| `/risk_levels` | risk_levels | object | (object, 자식 5) | 168–255 |  |
| `/risk_levels/very_low` | very_low | string | "< 1%" | 180–186 | E0005 |
| `/risk_levels/low` | low | string | "1-5%" | 193–199 | E0006 |
| `/risk_levels/moderate` | moderate | string | "5-15%" | 211–218 | E0007 |
| `/risk_levels/high` | high | string | "15-30%" | 226–234 | E0008 |
| `/risk_levels/very_high` | very_high | string | "> 30%" | 247–254 | E0009 |
| `/notes` | notes | object | (object, 자식 4) | 264–491 |  |
| `/notes/M1_to_M7` | M1_to_M7 | string | "주사 시술(M1 보톡스, M2 필러, M3 바이오스티뮬레이터, M4 스킨부스터, M5 PRP, M6 지방이식, M7 실리프팅)은 표피 손상이 없어 PIH 해당 없음" | 276–369 | E0010, E0011, E0012, E0013, E0014, E0015, E0016, E0017, E0018, E0019 |
| `/notes/M10` | M10 | string | "HIFES/EMS는 피부 표면에 작용하지 않으므로 PIH 해당 없음" | 376–415 | E0020, E0021, E0022 |
| `/notes/M16` | M16 | string | "수액치료는 정맥주사이므로 PIH 해당 없음" | 422–447 | E0023, E0024 |
| `/notes/M17` | M17 | string | "줄기세포치료(도포/주사)는 표피 손상 최소로 PIH 해당 없음" | 454–490 | E0025, E0026, E0027 |
| `/procedures` | procedures | array | (array, 자식 26) | 505–8317 |  |

## 2. 잠정 관찰 (원문과 분리 · 근거 Pointer 포함)

| # | 상태 | 근거 Pointer | 관찰 |
|---|---|---|---|
| 1 | P | `/description` | description 이 원장 전체 수치의 기준 집단을 'Fitzpatrick skin type III-IV' 로 선언한다. 괄호 '(한국인 대다수)' 는 그 집단에 대한 원장 측 주장이다. 각 항목 pih_rate 가 이 집단 기준인지는 description 으로만 추정되고 항목 단위 표기는 없다. |
| 2 | B | `/description`, `/risk_levels` | 비율의 분모(환자당·시술 회차당·누적 등)·관찰 기간·출처가 원장 어디에도 없다. 'PIH 위험도' 의 % 가 무엇의 비율인지 원문만으로 정할 수 없다. |
| 3 | P | `/risk_levels/very_low`, `/risk_levels/low`, `/risk_levels/moderate`, `/risk_levels/high`, `/risk_levels/very_high` | risk_levels 는 영문 열거 키 → 백분율 범위 문자열의 사전이다. 키 순서 very_low·low·moderate·high·very_high. 값은 숫자가 아니라 문자열('< 1%', '1-5%' …). |
| 4 | B | `/risk_levels/low`, `/risk_levels/moderate`, `/risk_levels/high` | 경계값이 인접 구간에 함께 나온다(5 는 low '1-5%' 와 moderate '5-15%', 15 는 moderate 와 high, 30 은 high '15-30%' 와 very_high '> 30%'). 끝점 포함/제외가 원문에 없다. very_low '< 1%' 와 low '1-5%' 사이 1 은 low 쪽만 표기. |
| 5 | P | `/notes` | notes 의 키(M1_to_M7·M10·M16·M17)는 procedures 에 없는 카테고리 코드다. procedures 의 category 값(M8·M9·M11·M12·M13·M15)과 합쳐도 M14 는 원장 어디에도 나오지 않는다(원장 안 사실만 기록, 의미 판단 안 함). |
| 6 | P | `/notes/M1_to_M7` | 키 'M1_to_M7' 은 범위형 키다. 값 괄호 안에 M1 보톡스 … M7 실리프팅 일곱 이름을 쉼표로 나열해 범위를 풀어 준다. 코드↔이름 대응은 원장 안의 진술일 뿐이고 다른 원장과의 연결은 후속. |
| 7 | P | `/notes/M1_to_M7`, `/notes/M10`, `/notes/M16`, `/notes/M17` | notes 네 값은 모두 '[이유] → PIH 해당 없음' 구조다. 이유: M1~M7 '표피 손상이 없어', M10 '피부 표면에 작용하지 않으므로', M16 '정맥주사이므로', M17 '표피 손상 최소로'. |
| 8 | I | `/notes/M17` | M17 은 '표피 손상 최소' (= 0 이 아님) 를 이유로 '해당 없음' 이라 한다. 다른 notes 의 '없어'·'작용하지 않으므로' 와 근거 강도가 다르다. 원문 내 표현 차이로 기록하고 판단은 후속. |
| 9 | P | `/notes/M17` | '(도포/주사)' — 줄기세포치료의 두 방식이 '/' 로 나열된다. README 규칙상 '/'=대안이지만 기호만으로 확정하지 않는다. |
| 10 | P | `/notes/M10` | 'HIFES/EMS' 는 '/' 로 두 약어를 묶는다. 같은 것의 두 이름인지 대안인지 원문만으로 불명. |

## 3. 수동 표현 기록 (원문 구간 · facets 는 탐색 관점)

| ID | Pointer | 원문 구간 | [s,e) | facets | 상태 | 메모 |
|---|---|---|---|---|---|---|
| E0000 | `/description` | 시술별 PIH(Post-Inflammatory Hyperpigmentation) 위험도 | 0–48 | claim_scope, mixed_language | P | 원장 주제 선언. PIH 약어와 영문 풀이 병기 |
| E0001 | `/description` | Post-Inflammatory Hyperpigmentation | 8–43 | mixed_language | P | PIH 의 풀이 |
| E0002 | `/description` | Fitzpatrick skin type III-IV (한국인 대다수)를 기준으로 작성 | 50–97 | population, claim_scope, range | P | 수치 전체의 기준 집단 선언 |
| E0003 | `/description` | Fitzpatrick skin type III-IV | 50–78 | population, range, mixed_language | P | 로마숫자 범위 III-IV |
| E0004 | `/description` | 한국인 대다수 | 80–87 | population, claim_scope | P | 집단 비율 주장(원장 측). 검증 대상 아님 |
| E0005 | `/risk_levels/very_low` | < 1% | 0–4 | comparison, rate, quantity_unit | P | 미만 부등호. 끝점 표기 방식은 원문 그대로 |
| E0006 | `/risk_levels/low` | 1-5% | 0–4 | range, rate | B | 끝점 포함 여부 불명 |
| E0007 | `/risk_levels/moderate` | 5-15% | 0–5 | range, rate | B | 5·15 가 인접 구간과 겹침 |
| E0008 | `/risk_levels/high` | 15-30% | 0–6 | range, rate | B | 15·30 이 인접 구간과 겹침 |
| E0009 | `/risk_levels/very_high` | > 30% | 0–5 | comparison, rate, quantity_unit | P | 초과 부등호 |
| E0010 | `/notes/M1_to_M7` | 주사 시술(M1 보톡스, M2 필러, M3 바이오스티뮬레이터, M4 스킨부스터, M5 PRP, M6 지방이식, M7 실리프팅) | 0–70 | name_candidate, reference | F | 범위 키를 코드+이름 나열로 풀이 |
| E0011 | `/notes/M1_to_M7` | M1 보톡스 | 6–12 | reference, name_candidate | F |  |
| E0012 | `/notes/M1_to_M7` | M2 필러 | 14–19 | reference, name_candidate | F |  |
| E0013 | `/notes/M1_to_M7` | M3 바이오스티뮬레이터 | 21–33 | reference, name_candidate | F |  |
| E0014 | `/notes/M1_to_M7` | M4 스킨부스터 | 35–43 | reference, name_candidate | F |  |
| E0015 | `/notes/M1_to_M7` | M5 PRP | 45–51 | reference, name_candidate, mixed_language | F |  |
| E0016 | `/notes/M1_to_M7` | M6 지방이식 | 53–60 | reference, name_candidate | F |  |
| E0017 | `/notes/M1_to_M7` | M7 실리프팅 | 62–69 | reference, name_candidate | F |  |
| E0018 | `/notes/M1_to_M7` | 표피 손상이 없어 | 72–81 | negation, cause_reason, tissue_layer | P | 해당 없음의 이유 |
| E0019 | `/notes/M1_to_M7` | PIH 해당 없음 | 82–91 | negation | P | 적용 제외 진술 |
| E0020 | `/notes/M10` | HIFES/EMS | 0–9 | name_candidate, symbol_ambiguity, mixed_language | F | '/' 의 뜻 불명 |
| E0021 | `/notes/M10` | 피부 표면에 작용하지 않으므로 | 11–27 | negation, cause_reason, tissue_layer | P |  |
| E0022 | `/notes/M10` | PIH 해당 없음 | 28–37 | negation | P |  |
| E0023 | `/notes/M16` | 수액치료는 정맥주사이므로 | 0–13 | cause_reason, name_candidate | P |  |
| E0024 | `/notes/M16` | PIH 해당 없음 | 14–23 | negation | P |  |
| E0025 | `/notes/M17` | 줄기세포치료(도포/주사) | 0–13 | name_candidate, symbol_ambiguity | F | 두 방식 '/' 나열 |
| E0026 | `/notes/M17` | 표피 손상 최소로 | 15–24 | degree, cause_reason, tissue_layer | I | '최소' 는 0 이 아님 — I3 |
| E0027 | `/notes/M17` | PIH 해당 없음 | 25–34 | negation | P |  |

## 4. 형태소 — 알려진 오분절·주의 출현 (원시 출력은 morphology.json)

| Pointer | 원문 구간 | 원시 토큰 | 영향 | 상태 |
|---|---|---|---|---|
| `/risk_levels/very_low` | < [0,1) | </SSO | 비교 부등호가 여는 괄호(SSO)로 태깅 — 형태소만 보면 '미만' 의미가 사라진다 | K |
| `/risk_levels/very_high` | > [0,1) | >/SSC | 비교 부등호가 닫는 괄호(SSC)로 태깅 — '초과' 의미 소실 | K |
| `/risk_levels/low` | 1-5 [0,3) | 1-5/W_SERIAL | 범위가 일련번호(W_SERIAL) 한 토큰 — 하한·상한이 분리되지 않음(moderate·high 및 항목 pih_rate 의 같은 형태 공통) | K |
| `/notes/M1_to_M7` | 필러 [17,19) | 필/NNG 러/EC | 제품군명 '필러' 가 명사+어미로 오분절 | K |
| `/notes/M1_to_M7` | M1 [6,8) | M/SL 1/SN | 카테고리 코드가 문자+숫자로 쪼개짐(M2~M7 동일) — 코드 단위 정보는 expressions 에 원문 구간으로 보존 | K |

## 5. 미결 (이 구획)

- B-S0-1 비율의 분모·관찰 기간·출처 없음 (issues.md B1)
- B-S0-2 risk_levels 경계 포함/제외 불명 (issues.md B2)
- F-S0-1 notes 코드(M1~M7·M10·M16·M17)와 procedure_ref·다른 원장 카테고리 연결은 후속 (issues.md F1)
- I-S0-1 M17 '최소' → '해당 없음' 근거 강도 차이 (issues.md I3)
