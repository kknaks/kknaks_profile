# validation — literature-evidence.json 1차 조사

원본 `orchestration/work/phub-recommend/bronze/phub-ledger/literature-evidence.json`
sha256 `6e179872a9c234491ca62c20899757fca3aa5388833aa6bc4d1ac28a032aebfd` · 118,979 bytes · 94,601 codepoints · 한 줄 JSON(줄바꿈 0) · BOM 없음.
작업 시작 때(`shasum -a 256`)와 마지막 검증 후 해시가 같다. 원본은 읽기만 했다.

## 1. 실행 명령과 결과 (레포 루트)

```
uv run --python 3.12 --with kiwipiepy==0.24.1 python orchestration/work/phub-ledger-redesign/first-pass/literature-evidence/build.py
→ {"nodes": 2137, "leaves": 1726, "dup_keys": 0, "escaped_strings": 9, "morph_applied": 137, "morph_tokens": 3144,
   "morph_excluded": 1569, "expressions": 771, "manual_expressions": 512, "segments_read": 18, "segments": 18}

python3 orchestration/work/phub-ledger-redesign/first-pass/literature-evidence/verify.py --selftest
→ failure_count 0, exit 0, source_sha256_start == source_sha256_end == 6e1798…aebfd
  selftest 11/11 검출: source-map 말단 삭제 · 구획 소유 삭제 · 소유 중복 · 구획 미독 · 표현 구간 이동 · 토큰 구간 변형 ·
  제외 1개 삭제 · 오분절 표시 삭제 · review 행 값 변형 · review 행 삭제 · 원본 바이트 변형
```

재현성: build.py 를 두 번 돌려 source-map·morphology·expressions·coverage·issues-index·review*.md·issues.md 의 sha256 이 같음을 diff 로 확인했다.
`verify.py` 는 결과·원본을 읽기만 하고 파일을 쓰지 않는다. 실패하면 exit 1 이다(검사 중 예외도 실패로 센다).

## 2. verify.py 가 검사하는 것

| 영역 | 검사 |
|---|---|
| 해시 | 원본 sha256 = 기대값, 각 결과 JSON 의 기록 해시 = 원본, 검증 시작·끝 해시 동일 |
| 구조·값 | `json.loads(object_pairs_hook)` 재파싱(중복 키 0) 노드 집합 ↔ source-map 노드 집합 **양방향**(누락·불필요 0). 노드마다 자료형, 원문 `file_cp` 슬라이스를 `json.loads` 로 되읽은 값, 바이트 구간=cp 구간 인코딩, 리터럴, 키 리터럴·구간, 자식 수, 빈 컨테이너 말단 표시, 객체 키 순서, 이스케이프 대응표(9개 title) |
| 구획 | 18구획 소유 합집합 = 원본 전체 노드(2,137), 소유 중복 0, 소유 말단 = 소유∩말단, 구획 규칙(S00 / Sxx=Mxx) 위반 0, 공동 참조 경로 실재, 읽기 상태 `read_direct`, manual·review 파일 실재, last_read_pointer 가 그 구획 소유 |
| review 분할 문서 | 구획마다 소유 노드 전부가 §1 표의 행으로 있고 원본 컬럼명·자료형·원문 리터럴·구간이 source-map 과 같음, 행 수 = 소유 수, §1~§4 절 존재, review.md 목차가 18개 part 를 가리킴, 수동 표현·관찰·미결 ID 가 해당 part 에 실림 |
| 형태소 | 적용 ∪ 제외 = 원본 비컨테이너 말단 1,706개, 겹침 0, 적용 집합 = 정책(patient_ko·accuracy_note·rubric)으로 독립 재계산한 집합, 제외마다 사유·종류, 분석기 버전·모델·스레드 기록, 토큰 표면형 = 값[start:end] = 원문 파일 cp 슬라이스, 오분절 출현 ↔ 토큰 표시 일치, 서명 재검출로 표시 누락 0, 규칙마다 출현 ≥1, 필드명 처리 목록 = 원본 키 집합 |
| 표현 | ID 중복 0, 값 구간 재현, 파일 cp 슬라이스(이스케이프 포함 리터럴을 디코딩해 비교)·바이트 구간 재현, (pointer, span, facets, origin) 중복 0, 상태 문자 유효, 구획 일치, 수동 표현 수 = manual 기록 수 |
| 미결·관찰 | ID 중복 0, Pointer 실재, 미결 문자 유효, 열린 A·C 0, issues-index 수 = manual 미결 수 |

개수 일치만으로 통과시키지 않는다 — 모든 대조는 Pointer 집합·구간 슬라이스 단위다.

## 3. 수치

- 노드 2,137 · 말단 1,726(= 비컨테이너 1,706 + 빈 배열 20) · 진술 119(moa 50 · adverse_effects 32 · effects 37) · citations 119(모두 진술당 1개) · 고유 PMID 25
- 형태소 적용 137값(patient_ko 119 · accuracy_note 17 · rubric 1) · 토큰 3,144 · 제외 1,569 = id_code 460 · bibliographic 357 · en_text 257 · zh_text 119 · ja_text 119 · version_date 104 · ratio_code 5 · non_string 148(int·float)
- 필드명(키) 처리: 원본 키 전부 excluded(영어 snake_case·Mxx 코드·언어 코드) — 사유 기록, 원본 컬럼명은 review 에 그대로
- 표현 771 = 수동 512(P 404 · I 105 · F 3) + 정규식 259(P 233 · I 6 · 오탐 K 20)
- 미결(구획 기록) 71 = I 33 · B 20 · F 17 · K 1. A 0 열림 · C 0
- accuracy_summary 재계산: accuracy_score 보유 진술 17 → overall 95.0, by_field moa 97.5·adverse_effects 95.0·effects 90.0, by_category M1 97.5·M2 100.0·M5 98.0·M12 95.0·M15 97.5·M16 87.5·M17 95.0 — 원문 값과 모두 일치. patient_*_coverage "119/119" = 진술 119 와 일치(값 존재만 확인, 번역 충실도 아님)

## 4. 별도 읽기 검토

1. **구획 직접 읽기**: `read_segment.py Sxx` 로 구획마다 모든 노드를 원문 순서로 출력해 읽고(citations 는 객체당 한 줄로 묶었으나 8키 값 전부 출력), 읽은 직후 manual/Sxx.json 에 관찰·표현·미결을 저장했다. 순서 S00→S17. 마지막 읽은 Pointer 는 각 manual 의 `last_read_pointer`.
2. **형태소 출력 전수 대조**: 137값의 토큰열(form/tag)을 값 단위로 전부 출력해 원문과 대조했다(구두점·괄호 토큰만 출력에서 생략). 찾은 오류 18규칙 34출현을 segmentation-review.json 에 서명으로 기록, build 가 출현별로 표시(교정 안 함). 수식·부정 토큰(드물/VA, 거의/MAG, 덜/MAG, 더/MAG, 매우/MAG, 않/VX, 없/VA, 못하/VX, 아니/VCN, 비·불·부/XPN)은 출력에 보존돼 있음을 확인했다. 예외: '비가교'는 NNG 한 토큰이라 부정 접두가 분리되지 않음(N02).
3. **정규식 미포함 후보 대조**: 수동 표현이 덮지 않는 정규식 후보 전부(54건)를 문맥과 함께 읽었다. 실제 수식·조건·부정인데 수동 기록에서 빠진 33건은 수동 표현으로 추가했고(manual 의 `-R` ID, A 수정), 남은 20건은 오탐으로 판정해 regex-review.json 에 사유와 함께 남겼다(CO2·M2·CXCL6 의 숫자, under, lower face, 분비·불리는·비타민·더해). 나머지 미포함은 citation_marker(정규식 전수가 정본)·mixed_hangul(I) 이다.
4. **언어 간 대조**: 진술마다 statement·accuracy_note·patient_ko/en/zh/ja 를 나란히 읽어 수식·조건·극성 차이를 I(I-LANG)로 기록했다. 의미상 어느 쪽이 맞는지는 판정하지 않았다.

검토하지 않은 것(미검토로 둠): 의미 관계(정보 종류·수식 대상·관계 방향)의 정답, 영어·중국어·일본어 형태소, 서명 밖 Kiwi 토큰의 정확성, 인용 문헌 내용과 진술의 일치(외부 자료 미사용).

*batch-03 검토 후 기록 보완:* 미검토 항목이 둘 더 있다.
- patient_zh·patient_ja 의 수식·조건·부정 표현 전수 수집. 수동 표현은 zh 3 · ja 12 뿐이고 zh/ja 보조 정규식은 없다.
- 한국어 「… 시술 후 / … 시」 조건·시점 구절. 보조 정규식에 패턴이 없어 3단계 대조 대상(54건)에 들어가지 않았다.

4번의 언어 간 대조는 I-LANG 차이를 관찰하는 데 그쳤고 zh/ja 표현 수집이 아니다. 범위·위치·영향은 [issues.md](./issues.md) K-ZHJA 정정과 K-KOCOND 에 있다. 둘 다 열림이다.

## 5. 작업 중 발견·수정한 에이전트 오류(A)

| 발견 | 수정 | 재검증 |
|---|---|---|
| 읽기 검토 3단계에서 수동 표현 누락 33건(patient_en 의 can/may·비교급, 한국어 '비-' 부정 재질/장비명, '가벼운' 정도 등) | manual S01·S04·S05·S07·S08·S12·S15·S16·S17 에 `-R` 표현으로 추가 | build → verify failure 0 |
| verify selftest 에서 결과 파일 변형 시 검사 자체가 KeyError 로 중단 | 검사 예외를 실패로 세도록 래핑 | selftest 11/11 검출 |

현재 열린 A 는 없다.
