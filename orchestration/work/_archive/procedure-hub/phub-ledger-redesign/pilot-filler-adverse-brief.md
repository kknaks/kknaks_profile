# 발주서 — 시범 2: 필러 × 부작용 교차 비교 (phub-ledger-redesign)

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 경로는 이 레포 기준.

## 1. 목표

피부과 시술 원장 21개를 정규화한 실버 ERD 를 설계하고 있다. 시범 1(보톡스 × 부작용)에서 「적용 케이스 × 부작용 = 값 하나 + 출처 여럿」 틀을 세웠다.
이번 시범 2는 **같은 틀이 필러에서도 통하는지** 시험한다. 필러는 부위·조직층·깊이·제품(HA/비HA)·기법(캐뉼러/니들)·용량 조건이 보톡스보다 많고, 혈관폐색·실명 같은 사건 연쇄가 있다.
틀이 맞으면 그대로, 안 맞으면 어디가 왜 안 맞는지와 고친 틀을 낸다.

## 2. 산출물 (이 파일만 만든다)

`orchestration/work/phub-ledger-redesign/silver-model/pilot-filler-adverse.md`

그 밖의 파일은 만들거나 고치거나 지우지 않는다. 원장(`orchestration/work/phub-recommend/bronze/`)·`first-pass/`·`silver-model/` 의 다른 파일은 읽기 전용. 이슈 목록·관리 문서를 따로 남기지 않는다(값 수집용 임시 스크립트는 레포 밖 임시 경로에서만 돌리고 결과만 문서에 옮긴다). 커밋·push 하지 않는다.

## 3. 읽을 것

1. **시범 1 결과(틀의 기준)**: `orchestration/work/phub-ledger-redesign/silver-model/pilot-botox-adverse.md` — 특히 §3 정리 규칙, §5 테이블 초안, §6. 형식도 이것을 따른다.
2. 원장(브론즈 3판 · 최신 기준 데이터): `orchestration/work/phub-recommend/bronze/phub-ledger/*.json` 21개.
3. 색인: `orchestration/work/phub-ledger-redesign/first-pass/<원장>/source-map.json` — **누락 확인용으로만**. first-pass 의 해석은 믿지 말고 원문으로 판단. morphology.json 은 열지 않는다.

## 4. 범위 — 「필러 부작용」 값을 빠짐없이

필러(계열 M2 · 그 하위분류(HA·비HA 등)·항목·제품 · 부위별 필러 메뉴) 에 대해 원장이 적은 **부작용 관련 값** 전부. 최소한:
- extracted `M2.safety.*` · taxonomy `modality[M2].extracted.safety.*` 와 하위 항목·제품의 `extracted.safety.*`·aftercare 중 부작용
- complications 의 필러 카테고리 전 칸 · consent-checklist `M2` mandatory_disclosures·emergency_signs
- post-procedure-timeline 의 필러 타임라인(HA 필러 등) 전 단계
- anatomy-danger-zones `zones[].filler_specific`(primary_risk·risk_level·safe_technique·max_per_point_ml·emergency_protocol 등)·`vessels[].danger`·`critical_safety_facts`(실명 최소량·고위험 부위·기전 등)·clinical_pearls 중 필러
- literature-evidence `M2.adverse_effects` · patient-education 필러 범주 · procedure-comparison · pih-risk · pre-procedure-checklist 의 필러 관련
- treatment-sequence·contraindications·synergy·treatment-optimization·problem-combos 의 필러 관련 문장 중 부작용(예: 「CO2 프락셔널 + 필러 · 열린 상처에 필러 주입 감염 위험」)

부작용이 아닌 것(효과·금기·고민)은 넣지 않고, 같은 말이 다른 역할로 쓰인 사례만 짧게 적는다(시범 1 §1 처럼). 다른 시술로 넘어가지 않는다.

## 5. 틀 (시범 1 + 사용자 결정)

**부작용 개념** — 명칭(의학용어) · 별칭(일반용어) · 현상 설명[] · 상위 사건(is-a) · 사건→사건 연결(원인→결과, 케이스별). 한 표현에 사건이 둘이면 나눈다. **폐색 ≠ 색전**처럼 함께 적힌 다른 사건은 합치지 않는다.

**적용 케이스** — 필러 + 원장이 적은 좁힘. 필러에서 새로 필요할 수 있는 좁힘: 부위 · **조직층/깊이** · 제품 종류(HA/비HA·재질) · 제품 · 기법(캐뉼러/니들·볼루스 등) · 용량 · 병행 시술. 「표재 주입 시」「과량 시」 같은 시술 방식은 시범 1처럼 조건 칸으로 둘지, 케이스 좁힘으로 올릴지 필러 값을 보고 정하고 이유를 적는다.

**케이스 × 부작용 = 값 하나 + 출처 여럿.** 빈도{원문·수치 범위·분모/대상·서술 등급} · 심각도 · 발현·지속{원문·범위·단위·기준점·수식} · 정도 · 조건·원인 · 대응 기준(경과표·응급 징후) · 관리·예방 · 출처.

**사용자가 정한 규칙(그대로 적용)**
- **D2** 서술 등급과 수치가 다른 원장에서 같이 오면 **두 칸에 병기**, 충돌로 보지 않는다. %↔등급 변환 금지.
- **D6** taxonomy 항목·제품의 `common`/`serious` 키는 **빈도 근거로 쓰지 않는다.** 원문 수식(「드물게」「일시적」)만 빈도·정도로 쓰고, 나머지 빈도는 계열 케이스 값을 상속한다. `serious`·`emergency` 계열 키는 심각도 쪽.
- **D1·D3·D4·D5·D7** 원장 간 수치 충돌은 **complications 값을 채택**하고 다른 원장은 출처로만 남긴다(timeline 의 짧은 기간은 대응 기준 행으로). 필러에서도 같은 원칙을 쓰되, complications 가 명백히 틀린 문맥이면 충돌로 올린다.
- **D8** 케이스에 맞지 않아 보이는 값은 담되 「케이스 부적합 의심」 표시.
- 서술 등급 순서: 대부분 > 흔함 > 가끔 > 드묾 > 매우 드묾. 숫자 없는 기간(「수일」)은 단위 수준까지만.

**원장끼리 다를 때 가리기** — 1 케이스가 달랐다 · 2 칸을 잘못 읽었다(합침) · 3 진짜 불일치(위 규칙으로도 안 풀리는 것만 사용자 판단) · = 차이 없음. 완전 복사본(extracted `M2` = taxonomy 계열 extracted 등)은 출처 하나로 센다.

**테이블 수를 줄이는 쪽으로 검토** — 시범 1 은 부작용 쪽에만 16개였다. 아래를 필러 값으로 시험하고 결론을 적는다.
- 별칭(`adverse_alias`)과 현상 설명(`adverse_phenomenon`)을 「표현」 테이블 하나(종류 칸)로 합쳐도 되는가.
- `case_adverse` 아래 자식(빈도 측정·조건·대응 기준·관리) 중 칸으로 접을 수 있는 것, 꼭 따로 있어야 하는 것(1:N 이 실제로 나오는가).
합칠 수 있으면 합친 안을 §5 에 낸다.

외부 임상 사실로 보충하지 않는다. 원문에 없는 칸은 비운다. 문맥으로 판단 가능한 것은 판단해서 채운다.

## 6. 문서 형식 (시범 1 과 같은 순서)

1. 수집 범위(원장·자리별 값 수 · 빠짐 확인 방법) · 역할이 다른 같은 표현
2. 부작용 개념 표(보톡스 시범의 E 개념과 같은 것은 같은 명칭을 쓰고 「시범1 E04 와 같음」처럼 표시 — 시술이 달라도 사건 개념은 공유된다)
3. 케이스 × 부작용 비교 표(케이스별 절) · 대응 기준
4. 판정 3 목록(원문·이유·추천·선택지·영향)
5. 테이블 초안 — 시범 1 대비 **추가·변경·합침**만 표시하고 최종 목록. 「담을 칸 없는 값」 0 또는 원문과 함께.
6. 틀 판정 — 시범 1 틀이 필러에 통했나: 그대로 통한 것 / 고친 것(이유) / 보톡스 쪽에 소급해야 할 변경.

분량은 표 위주로 대략 400행 이하.

## 7. 완료 기준

- §4 자리의 필러 부작용 값이 전부 표에 들어가 있고 빠짐 확인 방법이 적혀 있다.
- 원장 차이가 전부 1/2/3/= 로 판정돼 있고, 사용자 규칙(D2·D6·complications 채택·D8)이 적용돼 있다.
- 테이블 축소 검토 결론이 있다. 담을 칸 없는 값이 0 이거나 원문과 함께 적혀 있다.
- 산출물은 `silver-model/pilot-filler-adverse.md` 하나. `git status` 로 다른 변경이 없음을 확인한다.

## 8. 질문

설계를 실제로 막는 것이 있으면 먼저 원문을 확인하고, 그래도 사용자 선택이 필요하면 preamble 의 ask 로 묻는다. 범위를 혼자 넓히지 않는다.

## 9. 완료 보고

preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-ledger-redesign/silver-model/pilot-filler-adverse.md`).
그다음 코디 터미널에 한 줄:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "pilot-filler-adverse 완료: orchestration/work/phub-ledger-redesign/silver-model/pilot-filler-adverse.md" --enter`
