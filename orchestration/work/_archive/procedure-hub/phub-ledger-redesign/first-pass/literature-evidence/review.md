# literature-evidence.json — 1차 조사 review

## 상태

- **1차 범위 종료: 예(아래 기준 충족, validation.md 근거)** · **원장 전체 완료 아님** — 의미 조사·정규화·관계 확정은 시작하지 않았다
- 전수 읽기: 구획 18/18 직접 읽음(coverage.json · manual/S00~S17.json). 진술 119개 × statement·citations·점수·patient_ko/en/zh/ja·added_at 전부
- 구조·값 수집: 노드 2137 · 말단(빈 컨테이너 포함) 1726 · 중복 키 0 · 이스케이프 문자열 9 (source-map.json)
- 형태소: Kiwi 0.24.1(cong) 적용 137값 3144토큰 · 제외 1569(사유별 morphology.json excluded) · 알려진 분석 오류 18규칙 34출현 표시(교정 아님)
- 표현: 수동 512 · 정규식 보조 259 (expressions.json)
  - *batch-03 검토 후 기록 보완:* zh/ja 수식·조건 표현은 전수 수집하지 않았다(수동 zh 3 · ja 12, zh/ja 정규식 없음). 한국어 「시술 후·시」 조건 구절 7건도 표현에 빠져 있다. 표현 목록만으로 탐색하지 말고 원문 값을 다시 읽어야 한다([issues.md](./issues.md) K-ZHJA 정정 · K-KOCOND, 열림). 이 줄은 `build.py` 생성물이 아니어서 rebuild 하면 사라진다.
- 기계 검증·읽기 검토·미결: [validation.md](./validation.md) · [issues.md](./issues.md) · 진행 기록 [progress.md](./progress.md)
- 원본: `orchestration/work/phub-recommend/bronze/phub-ledger/literature-evidence.json` sha256 `6e179872a9c234491ca62c20899757fca3aa5388833aa6bc4d1ac28a032aebfd` · 118979 bytes · 94601 codepoints · 줄바꿈 0(한 줄 JSON)

## 읽는 법

- 각 review-part 의 §1 표는 원본 컬럼명(키 그대로)·자료형·원문 값(JSON 리터럴)·파일 cp 구간만 담는다. 잠정 관찰은 §2, 수동 표현은 §3, 미결은 §4 로 분리했다.
- 미결 문자: A=에이전트 추출/해석 오류 · B=원문 정보 부족 · C=현재 사용자 결정 필요 · 보조 K=알려진 분석 한계 · P=잠정 · F=후속 · I=원문 불일치.
- 관찰·표현의 facets 는 탐색 관점이며 확정 분류가 아니다. 형태소 기본형은 도메인 표준명이 아니다.

## 컬럼 구성 표 (경로 패턴 · 자료형 · 중첩 · 원문 예시와 위치)

`{Mxx}`=카테고리 키, `{i}`=배열 인덱스. 출현 수는 노드 수. 선택 필드 = 같은 부모 패턴 중 일부에만 있는 키.

| 경로 패턴 | 자료형(출현) | 출현 수 | 원문 예시(리터럴) | 예시 Pointer | 빈 값 출현 |
|---|---|---|---|---|---|
| `(root)` | object×1 | 1 | (object, 자식 5) | `(root)` | 0 |
| `/version` | string×1 | 1 | "2.0" | `/version` | 0 |
| `/updated` | string×1 | 1 | "2026-09-03" | `/updated` | 0 |
| `/source_method` | string×1 | 1 | "Curated successor of v1.0. Citation identity and metadata normalized from NCBI ESummary; unverified citations and claims without verified citations excluded… | `/source_method` | 0 |
| `/accuracy_summary` | object×1 | 1 | (object, 자식 8) | `/accuracy_summary` | 0 |
| `/accuracy_summary/scored_by` | string×1 | 1 | "Legacy content-quality scores retained for surviving statements; not a clinical claim approval." | `/accuracy_summary/scored_by` | 0 |
| `/accuracy_summary/rubric` | string×1 | 1 | "95-100=교과서 consensus, 85-94=주류 표준, 70-84=뉘앙스 보정, 50-69=근거 약함, 0-49=부정확" | `/accuracy_summary/rubric` | 0 |
| `/accuracy_summary/overall_average` | number_float×1 | 1 | 95.0 | `/accuracy_summary/overall_average` | 0 |
| `/accuracy_summary/n_scored` | number_int×1 | 1 | 17 | `/accuracy_summary/n_scored` | 0 |
| `/accuracy_summary/by_field_average` | object×1 | 1 | (object, 자식 3) | `/accuracy_summary/by_field_average` | 0 |
| `/accuracy_summary/by_field_average/moa` | number_float×1 | 1 | 97.5 | `/accuracy_summary/by_field_average/moa` | 0 |
| `/accuracy_summary/by_field_average/adverse_effects` | number_float×1 | 1 | 95.0 | `/accuracy_summary/by_field_average/adverse_effects` | 0 |
| `/accuracy_summary/by_field_average/effects` | number_float×1 | 1 | 90.0 | `/accuracy_summary/by_field_average/effects` | 0 |
| `/accuracy_summary/by_category_average` | object×1 | 1 | (object, 자식 7) | `/accuracy_summary/by_category_average` | 0 |
| `/accuracy_summary/by_category_average/{Mxx}` | number_float×7 | 7 | 97.5 | `/accuracy_summary/by_category_average/M1` | 0 |
| `/accuracy_summary/patient_ko_coverage` | string×1 | 1 | "119/119" | `/accuracy_summary/patient_ko_coverage` | 0 |
| `/accuracy_summary/patient_translations_coverage` | object×1 | 1 | (object, 자식 4) | `/accuracy_summary/patient_translations_coverage` | 0 |
| `/accuracy_summary/patient_translations_coverage/ko` | string×1 | 1 | "119/119" | `/accuracy_summary/patient_translations_coverage/ko` | 0 |
| `/accuracy_summary/patient_translations_coverage/en` | string×1 | 1 | "119/119" | `/accuracy_summary/patient_translations_coverage/en` | 0 |
| `/accuracy_summary/patient_translations_coverage/zh` | string×1 | 1 | "119/119" | `/accuracy_summary/patient_translations_coverage/zh` | 0 |
| `/accuracy_summary/patient_translations_coverage/ja` | string×1 | 1 | "119/119" | `/accuracy_summary/patient_translations_coverage/ja` | 0 |
| `/categories` | object×1 | 1 | (object, 자식 17) | `/categories` | 0 |
| `/categories/{Mxx}` | object×17 | 17 | (object, 자식 4) | `/categories/M1` | 0 |
| `/categories/{Mxx}/name` | string×17 | 17 | "Botulinum toxin type A (aesthetic)" | `/categories/M1/name` | 0 |
| `/categories/{Mxx}/moa` | array×17 | 17 | (array, 자식 3) | `/categories/M1/moa` | 6 (예: `/categories/M6/moa`) |
| `/categories/{Mxx}/moa/{i}` | object×50 | 50 | (object, 자식 8) | `/categories/M1/moa/0` | 0 |
| `/categories/{Mxx}/moa/{i}/statement` | string×50 | 50 | "Botulinum toxin type A inhibits the secretion of acetylcholine at the presynaptic neuromuscular junction." | `/categories/M1/moa/0/statement` | 0 |
| `/categories/{Mxx}/moa/{i}/citations` | array×50 | 50 | (array, 자식 1) | `/categories/M1/moa/0/citations` | 0 |
| `/categories/{Mxx}/moa/{i}/citations/{i}` | object×50 | 50 | (object, 자식 8) | `/categories/M1/moa/0/citations/0` | 0 |
| `/categories/{Mxx}/moa/{i}/citations/{i}/authors` | string×50 | 50 | "Park MY, Ahn KY" | `/categories/M1/moa/0/citations/0/authors` | 0 |
| `/categories/{Mxx}/moa/{i}/citations/{i}/title` | string×50 | 50 | "Scientific review of the aesthetic uses of botulinum toxin type A." | `/categories/M1/moa/0/citations/0/title` | 0 |
| `/categories/{Mxx}/moa/{i}/citations/{i}/journal` | string×50 | 50 | "Archives of craniofacial surgery" | `/categories/M1/moa/0/citations/0/journal` | 0 |
| `/categories/{Mxx}/moa/{i}/citations/{i}/year` | number_int×50 | 50 | 2021 | `/categories/M1/moa/0/citations/0/year` | 0 |
| `/categories/{Mxx}/moa/{i}/citations/{i}/pmid` | string×50 | 50 | "33714246" | `/categories/M1/moa/0/citations/0/pmid` | 0 |
| `/categories/{Mxx}/moa/{i}/citations/{i}/doi` | string×48 | 48 | "10.7181/acfs.2021.00003" | `/categories/M1/moa/0/citations/0/doi` | 0 |
| `/categories/{Mxx}/moa/{i}/citations/{i}/pmc` | string×49 | 49 | "PMC7968983" | `/categories/M1/moa/0/citations/0/pmc` | 0 |
| `/categories/{Mxx}/moa/{i}/citations/{i}/oa_url` | string×49 | 49 | "https://pmc.ncbi.nlm.nih.gov/articles/PMC7968983/" | `/categories/M1/moa/0/citations/0/oa_url` | 0 |
| `/categories/{Mxx}/moa/{i}/accuracy_score` | number_int×6 | 6 | 100 | `/categories/M1/moa/0/accuracy_score` | 0 |
| `/categories/{Mxx}/moa/{i}/accuracy_note` | string×6 | 6 | "아세틸콜린 분비 억제는 보툴리눔 톡신의 핵심 기전임." | `/categories/M1/moa/0/accuracy_note` | 0 |
| `/categories/{Mxx}/moa/{i}/patient_ko` | string×50 | 50 | "보툴리눔 톡신은 근육으로 가는 신경 신호 전달 물질이 나오는 것을 방해하여 근육의 움직임을 줄여줍니다." | `/categories/M1/moa/0/patient_ko` | 0 |
| `/categories/{Mxx}/moa/{i}/patient_en` | string×50 | 50 | "Botulinum toxin stops nerve signals from reaching muscles to reduce their movement." | `/categories/M1/moa/0/patient_en` | 0 |
| `/categories/{Mxx}/moa/{i}/patient_zh` | string×50 | 50 | "肉毒素通过阻断传递给肌肉的神经信号，帮助减少肌肉的过度运动。" | `/categories/M1/moa/0/patient_zh` | 0 |
| `/categories/{Mxx}/moa/{i}/patient_ja` | string×50 | 50 | "ボツリヌストキシンが筋肉に届く神経の合図を遮断し、動きを和らげます。" | `/categories/M1/moa/0/patient_ja` | 0 |
| `/categories/{Mxx}/moa/{i}/added_at` | string×44 | 44 | "2026-04-19" | `/categories/M1/moa/1/added_at` | 0 |
| `/categories/{Mxx}/adverse_effects` | array×17 | 17 | (array, 자식 4) | `/categories/M1/adverse_effects` | 6 (예: `/categories/M6/adverse_effects`) |
| `/categories/{Mxx}/adverse_effects/{i}` | object×32 | 32 | (object, 자식 8) | `/categories/M1/adverse_effects/0` | 0 |
| `/categories/{Mxx}/adverse_effects/{i}/statement` | string×32 | 32 | "Dry eye and diplopia have been reported following injection in the periocular region." | `/categories/M1/adverse_effects/0/statement` | 0 |
| `/categories/{Mxx}/adverse_effects/{i}/citations` | array×32 | 32 | (array, 자식 1) | `/categories/M1/adverse_effects/0/citations` | 0 |
| `/categories/{Mxx}/adverse_effects/{i}/citations/{i}` | object×32 | 32 | (object, 자식 8) | `/categories/M1/adverse_effects/0/citations/0` | 0 |
| `/categories/{Mxx}/adverse_effects/{i}/citations/{i}/authors` | string×32 | 32 | "Witmanowski H, Błochowiak K" | `/categories/M1/adverse_effects/0/citations/0/authors` | 0 |
| `/categories/{Mxx}/adverse_effects/{i}/citations/{i}/title` | string×32 | 32 | "The whole truth about botulinum toxin - a review." | `/categories/M1/adverse_effects/0/citations/0/title` | 0 |
| `/categories/{Mxx}/adverse_effects/{i}/citations/{i}/journal` | string×32 | 32 | "Postepy dermatologii i alergologii" | `/categories/M1/adverse_effects/0/citations/0/journal` | 0 |
| `/categories/{Mxx}/adverse_effects/{i}/citations/{i}/year` | number_int×32 | 32 | 2020 | `/categories/M1/adverse_effects/0/citations/0/year` | 0 |
| `/categories/{Mxx}/adverse_effects/{i}/citations/{i}/pmid` | string×32 | 32 | "33603602" | `/categories/M1/adverse_effects/0/citations/0/pmid` | 0 |
| `/categories/{Mxx}/adverse_effects/{i}/citations/{i}/doi` | string×30 | 30 | "10.5114/ada.2019.82795" | `/categories/M1/adverse_effects/0/citations/0/doi` | 0 |
| `/categories/{Mxx}/adverse_effects/{i}/citations/{i}/pmc` | string×29 | 29 | "PMC7874868" | `/categories/M1/adverse_effects/0/citations/0/pmc` | 0 |
| `/categories/{Mxx}/adverse_effects/{i}/citations/{i}/oa_url` | string×29 | 29 | "https://pmc.ncbi.nlm.nih.gov/articles/PMC7874868/" | `/categories/M1/adverse_effects/0/citations/0/oa_url` | 0 |
| `/categories/{Mxx}/adverse_effects/{i}/accuracy_score` | number_int×8 | 8 | 95 | `/categories/M1/adverse_effects/0/accuracy_score` | 0 |
| `/categories/{Mxx}/adverse_effects/{i}/accuracy_note` | string×8 | 8 | "안구 주위 시술 후 안구 건조 및 복시 발생 가능성이 보고됨." | `/categories/M1/adverse_effects/0/accuracy_note` | 0 |
| `/categories/{Mxx}/adverse_effects/{i}/patient_ko` | string×32 | 32 | "눈 주변 시술 시 드물게 눈이 건조해지거나 사물이 겹쳐 보이는 증상이 나타날 수 있습니다." | `/categories/M1/adverse_effects/0/patient_ko` | 0 |
| `/categories/{Mxx}/adverse_effects/{i}/patient_en` | string×32 | 32 | "Temporary dry eyes or vision changes can happen if the product reaches nearby areas." | `/categories/M1/adverse_effects/0/patient_en` | 0 |
| `/categories/{Mxx}/adverse_effects/{i}/patient_zh` | string×32 | 32 | "如果成分扩散到邻近区域，可能会出现暂时的眼睛干涩或视觉变化。" | `/categories/M1/adverse_effects/0/patient_zh` | 0 |
| `/categories/{Mxx}/adverse_effects/{i}/patient_ja` | string×32 | 32 | "成分が周囲に広がると、一時的な目の乾きや見え方の変化が起こります。" | `/categories/M1/adverse_effects/0/patient_ja` | 0 |
| `/categories/{Mxx}/adverse_effects/{i}/added_at` | string×24 | 24 | "2026-04-19" | `/categories/M1/adverse_effects/1/added_at` | 0 |
| `/categories/{Mxx}/effects` | array×17 | 17 | (array, 자식 4) | `/categories/M1/effects` | 8 (예: `/categories/M3/effects`) |
| `/categories/{Mxx}/effects/{i}` | object×37 | 37 | (object, 자식 7) | `/categories/M1/effects/0` | 0 |
| `/categories/{Mxx}/effects/{i}/statement` | string×37 | 37 | "Botulinum toxin type A eliminates facial wrinkles." | `/categories/M1/effects/0/statement` | 0 |
| `/categories/{Mxx}/effects/{i}/citations` | array×37 | 37 | (array, 자식 1) | `/categories/M1/effects/0/citations` | 0 |
| `/categories/{Mxx}/effects/{i}/citations/{i}` | object×37 | 37 | (object, 자식 8) | `/categories/M1/effects/0/citations/0` | 0 |
| `/categories/{Mxx}/effects/{i}/citations/{i}/authors` | string×37 | 37 | "Park MY, Ahn KY" | `/categories/M1/effects/0/citations/0/authors` | 0 |
| `/categories/{Mxx}/effects/{i}/citations/{i}/title` | string×37 | 37 | "Scientific review of the aesthetic uses of botulinum toxin type A." | `/categories/M1/effects/0/citations/0/title` | 0 |
| `/categories/{Mxx}/effects/{i}/citations/{i}/journal` | string×37 | 37 | "Archives of craniofacial surgery" | `/categories/M1/effects/0/citations/0/journal` | 0 |
| `/categories/{Mxx}/effects/{i}/citations/{i}/year` | number_int×37 | 37 | 2021 | `/categories/M1/effects/0/citations/0/year` | 0 |
| `/categories/{Mxx}/effects/{i}/citations/{i}/pmid` | string×37 | 37 | "33714246" | `/categories/M1/effects/0/citations/0/pmid` | 0 |
| `/categories/{Mxx}/effects/{i}/citations/{i}/doi` | string×35 | 35 | "10.7181/acfs.2021.00003" | `/categories/M1/effects/0/citations/0/doi` | 0 |
| `/categories/{Mxx}/effects/{i}/citations/{i}/pmc` | string×36 | 36 | "PMC7968983" | `/categories/M1/effects/0/citations/0/pmc` | 0 |
| `/categories/{Mxx}/effects/{i}/citations/{i}/oa_url` | string×36 | 36 | "https://pmc.ncbi.nlm.nih.gov/articles/PMC7968983/" | `/categories/M1/effects/0/citations/0/oa_url` | 0 |
| `/categories/{Mxx}/effects/{i}/patient_ko` | string×37 | 37 | "보톡스는 얼굴의 주름을 펴주는 주사예요." | `/categories/M1/effects/0/patient_ko` | 0 |
| `/categories/{Mxx}/effects/{i}/patient_en` | string×37 | 37 | "Botulinum toxin helps smooth the face by addressing the cause of expression lines." | `/categories/M1/effects/0/patient_en` | 0 |
| `/categories/{Mxx}/effects/{i}/patient_zh` | string×37 | 37 | "肉毒素通过针对表情纹产生的原因，帮助您恢复面部的平滑。" | `/categories/M1/effects/0/patient_zh` | 0 |
| `/categories/{Mxx}/effects/{i}/patient_ja` | string×37 | 37 | "ボツリヌストキシンが表情じわの原因に働き、お顔を滑らかに整えます。" | `/categories/M1/effects/0/patient_ja` | 0 |
| `/categories/{Mxx}/effects/{i}/added_at` | string×34 | 34 | "2026-04-19" | `/categories/M1/effects/0/added_at` | 0 |
| `/categories/{Mxx}/effects/{i}/accuracy_score` | number_int×3 | 3 | 95 | `/categories/M5/effects/0/accuracy_score` | 0 |
| `/categories/{Mxx}/effects/{i}/accuracy_note` | string×3 | 3 | "만성 상처 및 시술 후 상처 치유를 돕는 보조 요법으로 가치가 큼." | `/categories/M5/effects/0/accuracy_note` | 0 |

### 선택 필드·형태 변형

- 진술 객체 `/categories/{Mxx}/{moa|adverse_effects|effects}/{i}`: 키 구성 2종
  - 17개 — `statement, citations, accuracy_score, accuracy_note, patient_ko, patient_en, patient_zh, patient_ja` (예: `/categories/M1/moa/0`)
  - 102개 — `statement, citations, patient_ko, patient_en, patient_zh, patient_ja, added_at` (예: `/categories/M1/moa/1`)
- 인용 객체 `…/citations/{i}`: 키 구성 3종
  - 108개 — `authors, title, journal, year, pmid, doi, pmc, oa_url` (예: `/categories/M1/moa/0/citations/0`)
  - 6개 — `authors, title, journal, year, pmid, pmc, oa_url` (예: `/categories/M12/moa/5/citations/0`)
  - 5개 — `authors, title, journal, year, pmid, doi` (예: `/categories/M12/adverse_effects/0/citations/0`)
- 빈 배열 20개: M3·M15·M17 effects, M9 adverse_effects, M17 moa, M6·M10·M11·M13·M14 의 세 배열 전부. 빈 문자열·null·불리언 0.
- 숫자: `accuracy_score` int, `year` int, `/accuracy_summary` 의 평균값 float(리터럴 `95.0` 등 소수점 보존), `n_scored` int.

## 구획 목차

| 구획 | 범위 | 소유 노드 | 소유 말단 | 진술 수 | 읽기 상태 | 문서 |
|---|---|---|---|---|---|---|
| S00 | 상위 메타데이터 · /version · /updated · /source_method · /accuracy_summary · /categories 컨테이너 | 28 | 22 | 0 | read_direct | [review-part-S00.md](./review-part-S00.md) |
| S01 | /categories/M1 | 194 | 157 | 11 | read_direct | [review-part-S01.md](./review-part-S01.md) |
| S02 | /categories/M2 | 244 | 198 | 14 | read_direct | [review-part-S02.md](./review-part-S02.md) |
| S03 | /categories/M3 | 90 | 72 | 5 | read_direct | [review-part-S03.md](./review-part-S03.md) |
| S04 | /categories/M4 | 141 | 113 | 8 | read_direct | [review-part-S04.md](./review-part-S04.md) |
| S05 | /categories/M5 | 129 | 104 | 7 | read_direct | [review-part-S05.md](./review-part-S05.md) |
| S06 | /categories/M6 | 5 | 4 | 0 | read_direct | [review-part-S06.md](./review-part-S06.md) |
| S07 | /categories/M7 | 345 | 281 | 20 | read_direct | [review-part-S07.md](./review-part-S07.md) |
| S08 | /categories/M8 | 311 | 253 | 18 | read_direct | [review-part-S08.md](./review-part-S08.md) |
| S09 | /categories/M9 | 73 | 58 | 4 | read_direct | [review-part-S09.md](./review-part-S09.md) |
| S10 | /categories/M10 | 5 | 4 | 0 | read_direct | [review-part-S10.md](./review-part-S10.md) |
| S11 | /categories/M11 | 5 | 4 | 0 | read_direct | [review-part-S11.md](./review-part-S11.md) |
| S12 | /categories/M12 | 337 | 273 | 20 | read_direct | [review-part-S12.md](./review-part-S12.md) |
| S13 | /categories/M13 | 5 | 4 | 0 | read_direct | [review-part-S13.md](./review-part-S13.md) |
| S14 | /categories/M14 | 5 | 4 | 0 | read_direct | [review-part-S14.md](./review-part-S14.md) |
| S15 | /categories/M15 | 126 | 102 | 7 | read_direct | [review-part-S15.md](./review-part-S15.md) |
| S16 | /categories/M16 | 71 | 55 | 4 | read_direct | [review-part-S16.md](./review-part-S16.md) |
| S17 | /categories/M17 | 23 | 18 | 1 | read_direct | [review-part-S17.md](./review-part-S17.md) |

## 산출물

| 파일 | 내용 |
|---|---|
| source-map.json | 모든 노드: Pointer·부모·키 리터럴/구간·순서·자료형·디코딩 값·JSON 리터럴·파일 cp/byte 구간·이스케이프 대응표·구획 |
| coverage.json | 구획별 소유 노드/말단 Pointer·공동 참조·읽기 상태·manual/review 파일 |
| morphology.json | 분석기 설정·적용 값별 토큰(표면형·form·tag·lemma·구간·파일 cp)·제외 목록·필드명 처리·알려진 분석 오류 출현 |
| expressions.json | 수동·정규식 표현(구간·파일 cp/byte·facets·상태) |
| issues.md · issues-index.json | 미결 묶음·구획별 미결 원본 |
| segmentation-review.json | 형태소 출력 직접 대조로 찾은 오류 서명(교정 아님) |
| manual/S??.json | 구획별 직접 읽기 기록(관찰·표현·미결) |
| build.py · verify.py · read_segment.py | 재현 생성 · 독립 검증 · 읽기 출력 도우미 |
