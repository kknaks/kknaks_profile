# extracted.json — 검증 기록

> 기계 검증 통과는 **원문 대응**(누락·중복·Pointer·구간·해시·적용/제외)이 맞다는 뜻이다. 의미 해석의 정답이나 정규화 완료를 뜻하지 않는다. 1차 범위 종료(자체 판정) · 원장 전체 완료 아님.

## 1. 원본 해시

| 시점 | sha256 |
|---|---|
| 작업 시작(최초 열람 직후 `shasum -a 256`) | `b829d499e3e3fd7f6119f2dc23092cf50f7c13e57ee18e9d3131a14c7e350f2c` |
| build.py 각 실행 시작·끝 | 같음(build-output.txt) |
| verify.py 시작·끝 | 같음 |
| 작업 끝(`shasum -a 256`) | 같음 |

`phub-ledger/HASHES.txt` 의 extracted.json 줄(`b829d499e3e3fd7f`)과 앞 16자리가 같다. 원본·다른 워커 폴더·공통 문서에는 쓰지 않았다(`git status --short` 에서 이 작업으로 생긴 변경은 이 폴더뿐).

## 2. 실행 명령

```sh
# 레포 루트에서
uv run --python 3.12 --with kiwipiepy==0.24.1 python \
  orchestration/work/phub-ledger-redesign/first-pass/extracted/build.py
python3 orchestration/work/phub-ledger-redesign/first-pass/extracted/verify.py
```

build 출력([build-output.txt](./build-output.txt)):

```
source sha256 start=b829d499…0f2c end=b829d499…0f2c
nodes=958 analyzed=648 tokens=9940 excluded=71 expressions=3907 manual_expr=190 observations=76 seg_marks=34 sections=18
```

verify 출력(마지막 실행):

```
source sha256 start=b829d499e3e3fd7f6119f2dc23092cf50f7c13e57ee18e9d3131a14c7e350f2c end=b829d499e3e3fd7f6119f2dc23092cf50f7c13e57ee18e9d3131a14c7e350f2c
원문 노드 958 · 말단 719 · 문자열 717 · 구획 18 · 분석 648 · 제외 71 · 표현 3907 · 관찰 76 · 오분절 표시 34
checks=182 failures=0
```

exit 0.

## 3. verify.py 가 검사하는 것 (독립 구현)

verify.py 는 build.py 의 스캐너를 쓰지 않는다. 표준 `json` 파서에 `object_pairs_hook` 를 걸어 중복 키를 감지하며 원문을 다시 열거하고, 결과를 읽기만 한다(파일 쓰기 없음). 실패가 하나라도 있으면 exit 1.

| 묶음 | 검사 |
|---|---|
| 원본 | sha256 기대값 · 시작=끝 · 중복 키 0 · BMP 밖 문자 0(코드 포인트 = Kiwi UTF-16 단위) |
| 결과 파일 | 필수 13개 실재(없으면 즉시 실패) |
| source-map | 원문 경로 ↔ 노드 **양방향**(누락 0 · 원문에 없는 경로 0) · Pointer 중복 0 · 노드 순서 = 문서 순서 · 자료형·값·길이·키 순서 일치 · `span` 리터럴을 다시 디코드하면 값 · `byte_span` 바이트 재현 · `value_span` · `key_span` 재현 · 필드명 출현 = 원문 키 출현(양방향) |
| coverage | 소유 Pointer 중복 0 · 원문 경로 ↔ 구획 소유 합집합 **양방향** · 원문 말단(빈 컨테이너 포함) = 소유 말단 합집합 · 구획마다 소유 = 접두 범위 전체 · 구획별 「직접 읽음」 · review 파일 실재 · 문맥 참조 Pointer 실재 · 남은 구획 0 |
| review(분할) | 원문 노드 958개 **전부**가 담당 구획 파일의 표에 Pointer·원본 컬럼명·원문 값(문자열은 표 이스케이프 후 전문, null·컨테이너는 길이)으로 실림 · review.md 목차가 구획 파일 17개를 가리킴 · 상태에 「1차 범위」·「원장 전체 완료 아님」 · 자리표시 미치환 0 · 관찰·수동 표현·오분절 ID 가 담당 파일에 실림 |
| 형태소 | 말단 ↔ (분석 ∪ 제외) 양방향 · 분석·제외 겹침 0 · 제외 사유 기록 · 제외 규칙(코드·날짜·버전·열거 키)과 실제 제외 일치 · 토큰 surface = 값[span] · 분석기 설정(0.24.1·cong·스레드 1) · 필드명 분석 = 원문 서로 다른 키 · 오분절 표시 ↔ 원문 구간·원시 토큰·토큰 표시 양방향 |
| 표현 | text = 값[span] · 구획 일치 · (Pointer, 구간, 범주) 중복 생성 0 · ID 유일 · 모든 문자열 값에 segment.value · 수동 표현 전부 배치·원문 실재 · 수량 후보에 코드 속 숫자 0(단위 mm 허용) |
| 관찰 | 근거 Pointer·인용 원문 실재 · ID 유일 · 관찰이 가리키는 미결 ID 가 issues.md 에 실재 |
| 읽기 검토 기록 | reading-review-uncovered.json 의 어절 구간이 원문 재현 |

## 4. 변이 시험 (검출력)

결과 폴더를 scratchpad 로 복사해 하나씩 망가뜨리고 `verify.py --results <복사본>` / `--source <변형 원본>` 로 돌렸다. 원 결과 폴더·원본은 건드리지 않았다.

| 변이 | 결과 | 처음 잡힌 실패 |
|---|---|---|
| source-map 에서 노드 1개 삭제(`/M7/safety/uncommon/4`) | exit 1 | 원문 경로 → source-map 누락 |
| `/M1/name` span 시작 +1 | exit 1 | span 원문 재현 |
| review-part-09 값 「두통」→「두동」 | exit 1 | 모든 원문 노드가 review 에 실림 |
| coverage S03 소유 Pointer 1개 제거 | exit 1 | coverage 소유 누락 · 접두 범위 · review 담당 없음 |
| coverage S04 에 S05 Pointer 중복 추가 | exit 1 | coverage 소유 Pointer 중복 |
| coverage S07 직접 읽기 상태 → 미읽음 | exit 1 | coverage S07 직접 읽음 |
| 형태소 토큰 span 끝 +1 | exit 1 | 토큰 surface = 값[span] |
| 제외 기록 1개 삭제 | exit 1 | 말단 → 분석 또는 제외 누락 |
| 표현 후보 text 변조 | exit 1 | 표현 text = 값[span] |
| 관찰 인용을 없는 문자열로 | exit 1 | 관찰 근거 인용 실재 |
| 오분절 원시 토큰 변조 | exit 1 | 오분절 표시 대응 |
| 원본 사본 바이트 변경(「두통」→「두동」) | exit 1 | 해시 · 값 · span · review · 형태소 · 표현 등 9개 |
| issues.md 삭제 | exit 1 | 파일 실재 |

변이 시험 중 verify.py 결함 2건을 고쳤다 — (1) coverage 에서 빠진 Pointer 를 만나면 KeyError 로 죽던 것을 실패 기록으로 바꿈, (2) 수량 검사의 실패 카운터가 표현 검사 카운터와 섞이던 것을 분리. 수량 검사가 정상 단위 「0.2~2.0mm」를 오판하던 것도 단위 mm 허용으로 고쳤다.

## 5. 재현성

build.py 를 두 번 연속 실행해 source-map·morphology·expressions·coverage·review.md·review-part 17개(22 파일)의 sha256 이 같음을 확인했다(`diff` 무출력).

## 6. 별도 읽기 검토 (기계 검증과 구분)

같은 작성자가 관점을 바꿔 다시 읽은 것이다. 독립 검토자가 아니다.

1. **표지 누락 점검** — 규칙·수동 후보(segment.*·latin_term 제외)가 하나도 걸리지 않은 어절을 전부 뽑아 값 문맥에서 읽었다. 경과(일시적 등)·정도 부사·상태·범위 한정「…만」·인과·종점 표지 누락을 찾아 규칙 6범주를 보강했다(issues A3, 3,716 → 3,907). 보강 뒤 남은 2,664출현(서로 다른 1,393어절)을 다시 열람해 내용어임을 확인했고, 표지 글자를 포함한 27출현은 내용어 일부로 판정했다([reading-review-uncovered.json](./reading-review-uncovered.json)).
2. **수식·조건·부정 대상 확인** — 수동 표현 190건·관찰 76건을 원문 값과 대조했다. 수식 대상이 원문에서 확정되지 않는 경우(「드물게」의 적용 범위, 「0.2~2.0mm」가 무엇의 수치인지, 「운동 병행 시 효과」의 대상)는 확정하지 않고 B6 로 남겼다.
3. **오분절 영향 확인** — 34출현을 원문 어절과 대조해 영향(부위어 소실·질환명 소실·층위 뒤바뀜·단위 오인·부정 표지 품사 소실·사건 명사 부사화)을 기록했다(K1). 표현 후보는 원문 문자열에 직접 적용했으므로 오분절이 후보로 옮겨 가지 않는다. 3회차 대조 범위 밖 토큰은 보장하지 않는다.
4. **상태 문장 확인** — 관찰 OB-S09-03 의 「그 밖의 23개」를 원문 수(primary 4 · extended 19 = 미간주름 포함 23)에 맞게 고쳤다.

검토하지 않은 것: 의미 관계(동의어·상하·관계 방향·적용 조건)의 정답, 원문 임상 주장의 사실성. 1차 범위 밖이다.
