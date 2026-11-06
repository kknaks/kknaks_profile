# ERD 동결 — v2.4 (2026-11-04 · 사용자 「동결 실버빌드 하자」)

**정본**: `erd-v2.4.md` · `erd-v2.4.json`(빌더 입력) · `erd-v2.4-dictionaries.json` · `erd-v2.4-column-map.md` · `erd-v2.4-tuples.json`(실측)
검산: `erd-v2.4-check.py` PASS 91/91. 생성기 `erd_spec_v24.py`·`erd_colmap_v24.py`·`erd_build_v24.py`.

| 파일 | sha256(16) |
|---|---|
| erd-v2.4.md | `b8bb8eee9588f1fe` |
| erd-v2.4.json | `f9f23d1fa6789f26` |
| erd-v2.4-dictionaries.json | `1e674fd5c2082b72` |
| erd-v2.4-column-map.md | `d8412f37ef275a09` |
| erd-v2.4-tuples.json | `c037ca21c802af08` |

## 동결 근거
독립 검토 4회: v2.1(15건 · 구조 6) → v2.2(11 · 7) → v2.3(12 · 구조 6, 전부 같은 원칙 미적용) → **v2.4(규칙 0 · 동결 가)**. 검토서 `erd-v2.1-review.md` ~ `erd-v2.4-review.md`.
행선지: 원장 21 + step1 조사 = 잎 키 1,072 전부 행선지, 미정 0. 표본 대조 4회 전부 일치.

## 동결 조건 (사용자 정의 3)
1. 시술 = (무엇을, 어디에, 어떻게) 튜플. 미상 칸이 있으면 접지 않음. 조각 버리지 않음. 엣지 끝 = 시술 튜플.
2. 부작용 = (사건, 부위, 경과) 튜플. 원인 시술은 엣지. 표현은 가리키기만.
3. 원장 불변. 충돌은 레코드(④ 자동 해결도 기록). 결정 16 kind · 안정 키 · 적용 순서 ①~⑦. 빌드는 approved 만 읽음.

## 명시 예외 (사용자 결정 2026-11-04)
- **부작용 축에서 부위 없음(none)·경과 미상은 사전 값으로 본다.** (멍, none, 미상) 은 하나의 단위라 「멍 (타박상)」「멍 / 반상출혈」「멍·타박상」등이 접힌다. 시술 축의 「미상이면 접지 않음」과 다른 이유: 부작용의 부위 없음은 「모름」이 아니라 「어디서든 나는 사건」이고, 어느 시술에서 나는지는 R15 엣지가 든다. 멍·타박상·반상출혈 = 동의어 유지(사용자 「멍은 합쳐도 된다」). 분리는 결정 event_split 으로.

## ERD 를 다시 여는 조건
개체·관계·규칙 문장이 바뀔 때만(v3). 사전 값·동의어·매핑·접힘 승인·충돌 판정은 **결정 레코드**이며 ERD 를 열지 않는다. 미해결·미연결 수는 ERD 개정 사유가 아니다.

## 동결 시점 실측 (v2.4)
시술: 분류 항목 521 → 튜플 521(접힘 0) · 참조 367 중 미해결 207 · 시장가 122 중 미해결 106 · 엣지 끝 3,423(procedure 1,883 · modality 953 · product 318 · subcategory 62 · unresolved 207).
부작용: complications 65 → 단위 57(사전 39 + raw 18) · 표현 2,807 중 exact 651 · unlinked 2,156 · 표현 유래 단위 0.
결정 레코드 25(approved 19 · proposed 6). 충돌 0(빌드 전).

## 결정으로 넘긴 것(동결 후 · 실버 빌드 결정 묶음)
「보톡스」 product vs modality · 엑셀V+ · 같은 세 칸 다른 anchor 21조 · 사건 동의어 분리(과민반응·동상·지방괴사·섬유화·공기색전) · 괄호 동의어 미상 튜플 4 · 같은 사건 후보 둘인 표현 10 · 「주사 부위 홍반·부종」부종 부위 · 기법 상속 후보 9계열 · `/` 함께/또는 · 볼뉴머 M4/M9 · 엠페이스류 · 제품 사전 확장(step1 395) · 동의어 묶음(전체얼굴·HIFU·RF·MTS·필링·LED·토닝 …).

## 부록 — 브론즈 2판 (2026-11-05 · 사용자 결정 「원장의 집 = 메달리온 브론즈」)
- 원장의 집: `bronze/phub-ledger/` (이 레포). Hub main `src/data` 는 2026-09-03 삭제된 옛 파일(스냅샷과 18/21 불일치), 이후 원장은 stg DB 에만 있었음. 1판 = `phub-stg-2026-10-26/`(해시 ERD §source_files 그대로 보존).
- 2판 변경: `bronze/phub-ledger/CHANGELOG.md`. 해시 `bronze/phub-ledger/HASHES.txt`. 빌더는 `--bronze` 가 가리키는 폴더의 HASHES.txt 로 입력을 검증하고 매니페스트에 판 번호·해시를 기록한다. ERD v2.4 본문·JSON 은 바꾸지 않는다(브론즈 판 교체는 ERD 개정이 아님).
- 작성 규칙(`+` 함께 · `/` 대안)은 `bronze/phub-ledger/README.md`. V3-4 규칙과 같은 뜻.

## v3 동결 — 2026-11-05 (사용자 「v3 진행하자」 · 독립 검토 「동결 가」 · 문장 수정 R-1~R-4 반영)
**정본은 v3 로 교체**: `erd-v3.md` · `erd-v3.json`(빌더 입력) · `erd-v3-dictionaries.json` · `erd-v3-column-map.md` · `erd-v3-tuples.json`. 검산 `erd-v3-check.py` PASS 108/108. 생성기 `erd_spec_v3.py`·`erd_colmap_v3.py`·`erd_build_v3.py`. v2.4 는 이전 판으로 보존.

| 파일 | sha256(16) |
|---|---|
| erd-v3.md | `12b679e577de8ed6` |
| erd-v3.json | `0dc43293c963712a` |
| erd-v3-dictionaries.json | `e10fbf7998f273cf` |
| erd-v3-column-map.md | `eaa5195bb5c71347` |
| erd-v3-tuples.json | `e0f835aeea9cae07` |

변경 10건(V3-1~V3-10)은 `erd-v3-brief.md`·`erd-v3.md` §11. 검토 `erd-v3-review.md`(구조 4 → 문장 수정으로 닫음 · 결정 8). 사용자 정의 3 과 명시 예외는 유지하고 승계 문장(정의 2 = 세 칸 + 선택 수식 칸 · 결정 kind 17 · 안정 키에 부위별 anchor)이 §0 에 있다.
**다음**: 빌더를 v3 규칙으로 보강(V3-1~10) → 결정 묶음 3 제안 → 5차 빌드. ERD 를 다시 여는 조건은 v2.4 와 같다.

## v3.1 동결 — 2026-11-05 (사용자 「3.1 진행」 · 독립 검토 「S-1~S-5 닫은 뒤 동결 가」 · 반영 완료)
**정본은 v3.1 로 교체**: `erd-v3.1.md` · `erd-v3.1.json`(빌더 입력) · `erd-v3.1-dictionaries.json` · `erd-v3.1-column-map.md` · `erd-v3.1-tuples.json`. 검산 `erd-v3.1-check.py` PASS 122/122. 생성기 `erd_spec_v31.py`·`erd_colmap_v31.py`·`erd_build_v31.py`.

| 파일 | sha256(16) |
|---|---|
| erd-v3.1.md | `5237e364618e7851` |
| erd-v3.1.json | `a0426d97d1ffa041` |
| erd-v3.1-dictionaries.json | `782aefe25726cf84` |
| erd-v3.1-column-map.md | `536bf85719945c0c` |
| erd-v3.1-tuples.json | `6e67144097ab83c4` |

변경 10건(V3.1-1~10 · `ERD-V3-CANDIDATES.md` v3.1 절 · `erd-v3.1.md` §11). 검토 `erd-v3.1-review.md`.
**사용자 정의 2 개정(2026-11-05 사용자 결정)**: 부작용 단위 = (사건, 부위[조직층·절대 부위만 · 상대 부위 = none], 물질). 경과는 시술 → 부작용 엣지(R15) 속성. 조합은 세 칸 전부 사전 값이면 어느 출처든 생성. 원장 문구는 개체가 아니라 **문구 사전**(정규화형 1줄 · 단위 매핑 · parsed) + 엣지 부록. 명시 예외: 부위 none · 물질 none 은 값. 정의 1·3 유지.
개체 21 → 20(−adverse_expression) · 관계 31(−R29 +R32 rule_applies_to) · 사전 49(+person_condition +phrase_dictionary) · 결정 kind 20(+product_reclassify +dictionary_remove +phrase_map).
**다음**: 빌더 v3.1 반영(적합성 열거기가 새 경우를 요구) → 6차 빌드 → 결정 묶음 4(부작용·시술 동의어) 제안.

## v3.2 동결 — 2026-11-05 (사용자 「v3.2 진행 · 오퍼스로」 · 독립 검토 「S-1~S-4 닫은 뒤 동결 가」 · 반영 완료 · 검산 52/52)
**정본은 v3.2 로 교체**: `erd-v3.2.md` · `erd-v3.2.json`(빌더 입력) · `erd-v3.2-dictionaries.json` · `erd-v3.2-column-map.md` · `erd-v3.2-tuples.json` · `erd-v3.2-seed-candidates.json/.md`(사전 씨앗 승인용). 생성기 `erd_spec_v32.py`·`erd_colmap_v32.py`·`erd_build_v32.py`.

| 파일 | sha256(16) |
|---|---|
| erd-v3.2.md | `f04c511a887a7a1a` |
| erd-v3.2.json | `9e750fc739281c0d` |
| erd-v3.2-dictionaries.json | `b898d226fa9fc031` |
| erd-v3.2-column-map.md | `b86950b5c7fa316a` |
| erd-v3.2-tuples.json | `c5633d73461e4d2c` |

**v3.2 원칙(사용자 2026-11-05)**: ① 원장 문구는 먼저 「어느 테이블 것인가」(부작용 문구 / 타임라인 / 동의서 고지·금기·응급 징후 / 시술 전 확인 / 메모·문헌)로 분류 · 부작용 단위에는 부작용 문구만 · 나머지는 자기 테이블로 정규화 뒤 참조 ② 부작용 문구에서 사전에 없는 사건은 **그 말로 새 노드**(출처·설명·미검토) · 사전 사건이 닿으면 거기에 exact, 남은 토큰은 속성 또는 그 토막만 새 노드 · 비슷한 노드끼리 ⑦ 중복 후보(strong 만 게이트) · 추정 매칭 0 · **미연결 상태 없음** ③ 사전 씨앗은 원장 전체에서 · 부위 전수(바디·parent) · 장비 = 제품 자동 등록 · 성분(필링 산) what · 토큰화(조사·어미·~감·관형형, 목록·보존) · 표기 변형 목록 ④ R15 속성 3층 상속(단위→계열→항목 · basis · 참조) ⑤ post_procedure_timeline 개체(R33/R34) · emergency_sign 개체(R35). 개체 22 · 관계 34 · kind 20 · 사전 49.
**실측(v3.2)**: 부작용 문구 2,285 = exact 1,407 · new 835(새 노드 262) · 메모 30 · 설명문 13 · 안 붙음 0 · ⑦ strong 98(weak 207) · 타임라인 줄 435(참조 193·부분 104·없음 57·정상 81) · 항목 자신이 시술 477→324(장비 150 승격) · ⑨ 303.
**다음**: 빌더 v3.2 반영(열거기) → 7차 → 게이트 = 새 사건 노드 262 목록 + ⑦ strong 98 + 씨앗(부위 14·성분 17·줄임말 29) + 묶음 3 미결 15.
