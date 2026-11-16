# taxonomy.json — 1차 조사 검증

**1차 범위 종료: 예. 원장 전체 완료: 아니오.** 원문 부족(B)·원문 내 불일치(I)·후속 의미 조사(F)·알려진 분석 한계(K)가 남아 있다([`issues.md`](issues.md)). 기계 통과는 원문 대응의 검증이며 의미 정답을 뜻하지 않는다.

## 상태 구분

| 구분 | 상태 | 근거 |
|---|---|---|
| 전수 읽기 | 완료 53/53 구획 | `coverage.json` read_state, `manual/S000~S052.json`(state=read, last_pointer), `progress.md` 로그 |
| 구조·값 수집 | 완료 | `source-map.json` 17,593 노드(말단·빈 컨테이너 11,931) — 키 순서·배열 순서·리터럴 바이트/코드포인트 구간·조상 문맥 |
| 형태소·표현 수집 | 완료(표현은 정규식 단서 공백 있음 — `issues.md` K-EXPR01) | 문자열 11,829 중 적용 10,844 · 제외 985(사유 기록) · 토큰 98,254 · 필드명 57종(출현 위치 포함) · 표현 정규식 후보 10,974 · 직접 읽기 수집 1,073 |
| 기계 검증 | 통과 failure_count=0 | 아래 명령·출력 |
| 읽기 검토 | 완료(구획별) | 구획마다 원문 렌더를 직접 읽고 관찰 404 · 복합 표현 1,073 · 오분절 규칙 100 · 미결 150 기록 |
| 알려진 분석 한계 | 기록됨(K) | `morphology.json` known_segmentation_errors 2,023 출현(W_SERIAL 1,576 포함), `issues.md` K 표 |
| 열린 미결 | B 34 · I 65 · F 47 · K 4 · A 0 · C 0 | `issues.md`(구획 기록 + GLOBAL 묶음) |
| 후속 의미 조사 | 남음 | F 항목 — 개체 병합·계열 경계·축 분해·참조 보강은 설계 단계 과제 |

## 원본 고정

- 경로: `orchestration/work/phub-recommend/bronze/phub-ledger/taxonomy.json` (읽기 전용으로만 열었다)
- 크기 660,679 bytes · UTF-8, BOM 없음 · 디코딩 코드포인트 = `source-map.json` codepoints
- sha256 `5492d0d4354406477206cb46f1bb735ca684d2d4a218c11d31e7889b20f4e8fe` — 작업 시작·각 빌드·verify 시작/끝·최종 `shasum` 모두 일치
- 중복 키 0 (빌드 스캐너와 verify 의 `object_pairs_hook` 이 각각 독립 확인). 문자열 내 백슬래시 이스케이프 0 — 그래도 구간은 리터럴 바이트 구간과 디코딩 값 구간을 분리해 기록했다.

## 구획 계획과 소유

- 53구획: S000(루트 컨테이너) + 모달리티별 문서 순서 묶음(목표 렌더 약 9,000자, 항목·제품 경계에서만 절단) + problem 2구획.
- 모든 노드(컨테이너·말단·빈 컨테이너)는 정확히 한 구획이 소유한다(`owned_pointers`). `context_refs`(조상 id·category·label·name)는 공동 참조이며 소유가 아니다.
- 큰 하위분류(M15-1 케미컬필링 61항목 등)는 항목 범위로 나눴고 경계는 `coverage.json` pointer_first/last·units 에 있다.

## 실행 명령과 결과

```bash
# 레포 루트
uv run --python 3.12 --with kiwipiepy==0.24.1 python orchestration/work/phub-ledger-redesign/first-pass/taxonomy/build.py
# → sha256=5492d0d4… bytes=660679 nodes=17593 sections=53 text_leaves=11829 dups=0
#   read_sections=53/53 · expressions auto=10974 manual=1073 · morph applied=10844 excluded=985 tokens=98254
python3 orchestration/work/phub-ledger-redesign/first-pass/taxonomy/verify.py ; echo EXIT=$?
```

verify 출력(최종):

```json
{"source_nodes": 17593, "source_leaves_or_empty": 11931, "duplicate_keys": 0, "source_map_nodes": 17593,
 "sections": 53, "sections_read": 53, "zero_length_tokens": 19, "morph_applied": 10844, "morph_excluded": 985,
 "tokens": 98254, "field_names": 57, "known_seg_flags": 2023, "expr_auto": 10974, "expr_manual": 1073,
 "issues_by_status": {"B": 34, "F": 47, "I": 65, "K": 4},
 "sha_start": "5492d0d4…f8fe", "sha_end": "5492d0d4…f8fe", "failure_count": 0}
EXIT=0
```

### verify.py 가 확인하는 것 (읽기 전용, 실패 시 exit 1)

1. 원본 해시 시작/끝 = 작업 시작 시 고정값.
2. 독립 파싱(중복 키 감지)으로 전체 Pointer 집합을 만들고 `source-map.json` 과 **양방향** 대조(누락·불필요), 자료형·값·자식 수 일치.
3. 모든 노드의 `literal_byte_span` 을 원본 바이트에서 잘라 JSON 디코딩 → 값 재현, `literal_codepoint_span` 의 텍스트 = 같은 바이트, 키 리터럴 구간 → 키 재현.
4. `coverage.json` 소유 합집합 = 원문 전체 Pointer, 중복 소유 0, 모든 구획 read·manual(state=read, last_pointer 가 그 구획 소유 범위 안)·읽기 렌더·review-part 파일 실재, source-map 의 section 표기 일치.
5. 분할 review: 각 review-part 의 「원문 값」 표에 그 구획 소유 Pointer 가 모두 있고 말단 원문 값(이스케이프 반영)이 같은 줄에 있음, 「원본 컬럼명」「잠정 관찰」 절 존재, review.md 목차·컬럼 구성 표 존재.
6. 형태소: 모든 문자열 값이 적용 또는 사유 있는 제외 중 정확히 하나, 레코드 text = 원문 값, 모든 토큰 `text[start:end] == surface`, 집계·파트 파일 sha256 일치, 필드명 57종의 출현 위치 = source-map 의 키 출현, 알려진 오분절 표시 구간 재현.
7. 표현: auto·manual 모든 구간과 문장 구간이 원문 값에서 재현, (pointer·구간·관점) 중복 0, 구획 표기 일치.
8. 수동 기록: 상태 문자 ∈ {A,B,C,K,P,F,I}, 관찰·미결·오분절 Pointer 가 원문에 존재, 미결 ID 중복 0.

### 검증 중 발견해 고친 것

- 첫 verify 실행에서 실패 2건: (a) review-part 대조 시 「수동 복합 표현」 표의 Pointer 줄이 「원문 값」 표 줄을 덮어 읽힌 **검증기 쪽 오류** → 값 표 영역만 읽도록 수정, (b) kiwi 가 생략된 서술격 조사 '이'를 **길이 0 토큰**(start==end, surface "")으로 내는 실제 도구 동작 19건 → 데이터는 그대로 두고 `morphology.json` span_unit 설명에 명시, 검증 조건을 start≤end 로 바로잡고 개수를 `zero_length_tokens` 로 보고.
- 수동 기록 작성 후 모든 manual 표현 텍스트·Pointer 를 원문과 대조(불일치 0)한 뒤 빌드했다.

### 검증기 음성 시험

스크래치 복사본에서 (1) 구획 소유 Pointer 1개 삭제, (2) review-part 값 줄 1개 삭제, (3) 수동 표현 구간 1개 변조 → verify 가 4개 FAIL(소유 누락, section 표기 불일치, review 누락, 표현 구간 불일치)과 exit 1. 원본 폴더 산출물은 건드리지 않았다.

## 형태소 분석 설정

- kiwipiepy 0.24.1 (`uv run --python 3.12 --with kiwipiepy==0.24.1`), `Kiwi(num_workers=1, model_type='cong')`, 기본 사전, 사용자 사전·오타 교정 없음, tokenize 기본 옵션, 원문 정규화 없음.
- 값 단위 분석. 토큰 = [form, tag, start, end, surface, lemma(분석기 제공·form 과 다를 때만)]. 구간 = 디코딩 값의 코드포인트 [start,end). 분석기가 주지 않은 기본형은 만들지 않았다.
- 제외(사유·위치 `morphology.json` excluded): id 필드 857, modality_ref 원소 105, reclassified_to 1, 빈 문자열 22. 불리언·null(mfds, is_marketing_name)은 텍스트 아님 — 원값은 source-map 에 보존.
- 필드명: 57종 모두 분석(역할 field_name, 언어 텍스트와 구분)하고 출현 Pointer 목록을 붙였다.

## 별도 읽기 검토

- 구획마다 `reading/S###.txt` 원문 렌더를 위에서 아래로 직접 읽고, 전문어는 `tok.py` 로 형태소 결과를 원문과 대조했다(`reading/S###.seg.txt` 는 오분절 의심 어절 보조 목록).
- 수식·조건·부정·가능성·범위·시간·비교·기호·참조 표현은 원문 구간으로 1,073개를 직접 수집했다(1,022개 값). 반복 상용구는 대표 출현을 수동 기록했다. 나머지 출현 가운데 정규식 후보(auto, 문장 구간 포함)로 남은 것은 `method.patterns` 에 든 단서와 일치한 출현뿐이다. 패턴에 없는 단서(`자제`·`깊`·`얇`·`서서히`/`점진`·`권장`/`주의`/`필요`·`심각`·`약 N`·Pa/N 수치·`… 시` 조건)는 표현 기록에 빠진 출현이 있다(*정정, batch-03 검토 후 기록 보완: 이전 문구 「나머지 출현은 정규식 후보로 전수 보존」은 실제보다 넓었다. 수치·위치는 [`issues.md`](issues.md) K-EXPR01*). 원문 값·Pointer·형태소 토큰은 전부 보존돼 있다. 하지만 표현 후보 목록만으로 후속 탐색을 하면 위 출현이 빠지므로 원문 문맥을 다시 읽어야 한다. 이 공백은 열린 후속 과제이며 의미적으로 해결하거나 교정하지 않았다. auto 후보 중 수동 표현과 겹치는 비율(예: 부정·금지 437 중 114, 조건 432 중 66, 가능성·빈도 480 중 138)은 수동 표현이 대표 선택임을 보여 준다 — auto 는 오탐·누락이 있는 수집 보조이며 전수 의미 해석이 아니다.
- 확인한 영향 예: '드물게/극히 드문/거의 필발' 빈도어(형태소로는 부사·NNG 조각), '최소/이상/이내' 하한·상한, '(… 시)' 조건 괄호, '않/금지/아님' 부정, W_SERIAL 범위·목록 혼동, 제품명의 조사·어미 오분석(더채움·볼뉴머·울쎄라·온다 등), 수사·단위 오탐(대이개신경·삼염화초산·초회통과효과), 질환/시술 동형('주사').
- 1차에서 검토하지 않은 것: 의미 관계(동의어 병합·상하 관계·관계 방향·적용 조건), 임상·규제 사실의 진위(외부 확인 안 함), 형태소 토큰 전체의 정답 여부.

## 산출물

| 파일 | 내용 |
|---|---|
| `review.md` | 상태·컬럼 구성 표(경로 패턴·자료형·중첩·선택적·빈 값·예시/Pointer)·구획 목차 |
| `review-part-S000~S052.md` | 구획별 원문 값 전부(원본 컬럼명·자료형·Pointer) / 잠정 관찰 / 수동 표현 / 오분절 / 미결 — 분리된 절 |
| `source-map.json` | 전 노드 구조·값·구간·문맥·소유 구획 |
| `coverage.json` | 구획 계획·소유 Pointer·문맥 참조·읽기 상태·파일 대응 |
| `morphology.json` + `morphology/S###.json` | 설정·제외·필드명·알려진 오분절 + 구획별 토큰(파트 sha256) |
| `expressions.json` | 정규식 후보(문장 구간) + 직접 읽기 표현 |
| `issues.md` | 미결 집계·전체 목록·알려진 분석 한계 표 |
| `manual/` | 구획별 직접 읽기 기록(S000~S052) + GLOBAL 묶음 |
| `reading/` | 읽기 렌더·오분절 보조 목록(빌드/보조 스크립트 생성) |
| `build.py` · `verify.py` | 재현 빌드 · 독립 검증 |
| `tok.py` · `seg_candidates.py` · `_prog.py` | 읽기 보조(형태소 조회, 오분절 후보, 진행 기록 갱신) — 산출 판정에 쓰지 않음 |
| `progress.md` | 진행·재개 기록 |
