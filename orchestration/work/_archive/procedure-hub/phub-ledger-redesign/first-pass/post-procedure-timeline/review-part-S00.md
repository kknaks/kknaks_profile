# S00 — 상위 메타데이터 (version·updated·consensus_method·reaction_levels) + 루트·timelines 배열 컨테이너

> build.py 생성. 원문 값과 잠정 관찰은 서로 다른 절·칸에 둔다.

- 소유 범위: prefix ['/version', '/updated', '/consensus_method', '/reaction_levels'] · exact ['', '/timelines']
- 공유 문맥(소유 아님): 없음
- 직접 읽기: done (manual/S00.txt) · 마지막 읽은 Pointer `/reaction_levels/emergency`

## 1. 원문 — 모든 노드 (문서 순서)

| # | Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 원문 구간(cp) |
|---|---|---|---|---|---|
| 1 | `(root)` | `(root)` | object | {version, updated, consensus_method, reaction_levels, timelines} | 0–11823 |
| 2 | `/version` | `version` | string | 1.1 | 11–16 |
| 3 | `/updated` | `updated` | string | 2026-07-11 | 27–39 |
| 4 | `/consensus_method` | `consensus_method` | string | Perplexity(리서치) + Gemini(분석) + Claude(교과서 종합) 3-AI 컨센서스 | 59–116 |
| 5 | `/reaction_levels` | `reaction_levels` | object | {normal, abnormal, caution, emergency} | 135–279 |
| 6 | `/reaction_levels/normal` | `normal` | string | 정상 반응 -- 예상 범위, 조치 불필요 | 145–169 |
| 7 | `/reaction_levels/abnormal` | `abnormal` | string | 이상 반응 -- 모니터링 필요, 경과 관찰 | 181–206 |
| 8 | `/reaction_levels/caution` | `caution` | string | 주의 반응 -- 24-48시간 내 클리닉 연락 | 217–244 |
| 9 | `/reaction_levels/emergency` | `emergency` | string | 응급 반응 -- 즉시 응급실/클리닉 | 257–278 |
| 10 | `/timelines` | `timelines` | array | [길이 10] | 292–11822 |

## 3. 수동 표현 (직접 읽기) — 원문 구절과 관찰 칸 분리

| Pointer | 구간 | 원문 구절 | 탐색 관점(잠정) | 잠정 메모 |
|---|---|---|---|---|
| `/version` | [0,3) | 1.1 | version_id | 원장 판 번호. 형태소 제외 대상(ID/코드) |
| `/updated` | [0,10) | 2026-07-11 | date | 갱신일. 시술 후 시간 아님 |
| `/consensus_method` | [0,55) | Perplexity(리서치) + Gemini(분석) + Claude(교과서 종합) 3-AI 컨센서스 | provenance | 작성 방법 전문. 도구명 3개와 괄호 속 역할 |
| `/consensus_method` | [31,45) | Claude(교과서 종합) | provenance | 「교과서 종합」— 어떤 교과서인지 원문 없음 |
| `/consensus_method` | [46,55) | 3-AI 컨센서스 | provenance, quantity | 세 도구 합의라는 서술. 합의 방식·불일치 처리 원문 없음 |
| `/reaction_levels/normal` | [0,22) | 정상 반응 -- 예상 범위, 조치 불필요 | level_def, negation | 「불필요」 = 조치 부정 |
| `/reaction_levels/normal` | [9,14) | 예상 범위 | range | 무엇의 범위인지(증상 정도·기간) 원문 없음 |
| `/reaction_levels/abnormal` | [0,23) | 이상 반응 -- 모니터링 필요, 경과 관찰 | level_def, recommendation | 필요 = 권고 강도 단서 |
| `/reaction_levels/caution` | [0,25) | 주의 반응 -- 24-48시간 내 클리닉 연락 | level_def, action_time, time_range | 24-48시간 = 연락 시한. 기준 시점(증상 인지 후인지) 원문 없음 |
| `/reaction_levels/emergency` | [0,19) | 응급 반응 -- 즉시 응급실/클리닉 | level_def, action_time, alt | 「즉시」 시한, 「응급실/클리닉」 대안 |

## 4. 자동 후보 요약 (정규식 일치분만 — 전수 의미 수집 아님)

P-ADVICE 6, P-ALT 1, P-COMPARE 1, P-DURING 1, P-LATIN 4, P-NEG 1, P-NUMUNIT 1, P-PAREN 3, P-SYMBOL 6

전체 목록은 expressions.json (segment 필터).

## 5. 잠정 관찰

- **S00-O1** 상위 키 5개 중 reaction_levels 의 키 4개(normal·abnormal·caution·emergency)가 timelines[*].phases[*] 의 배열 키 이름과 같다. 이름 일치는 구조적 사실이고, 각 배열이 이 정의를 따른다는 연결은 잠정 관찰이다(P).
- **S00-O2** reaction_levels 값은 모두 「<등급명> -- <설명>, <조치>」 형태이고 구분자는 ASCII 「--」 와 「, 」 이다. caution·emergency 는 조치에 시한(24-48시간 내·즉시)을 담는다.
- **S00-O3** consensus_method 는 원장 전체에 대한 작성 방법 하나뿐이고, 항목별 출처·근거는 원장 어디에도 없다.

## 6. 미결 (이 구획)

| ID | 분류 | 위치 | 내용 |
|---|---|---|---|
| S00-Q1 | B | `/consensus_method` | 항목별 근거·문헌·합의 불일치 기록이 원문에 없다. 개별 시간·빈도 표현의 출처 확인이 제한된다. |
| S00-Q2 | B | `/reaction_levels/caution` | 「24-48시간 내」의 기준 시점(증상 발견 시·시술 시)이 원문에 없다. |
| S00-Q3 | P | `/reaction_levels` | 등급 키와 phases 배열 키의 이름 일치를 정의 참조로 볼지는 후속 의미 조사(F-LEVEL)에서 정한다. |

## 7. 형태소 — 알려진 오분절 (교정 안 함)

| Pointer | 구간 | 원시 토큰 | 판정/설명 | 영향 |
|---|---|---|---|---|

