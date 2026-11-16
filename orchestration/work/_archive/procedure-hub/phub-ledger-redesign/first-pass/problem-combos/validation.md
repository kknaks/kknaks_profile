# validation — problem-combos 1차

## 실행 명령 (레포 루트)

```sh
uv run --python 3.12 --with kiwipiepy==0.24.1 python orchestration/work/phub-ledger-redesign/first-pass/problem-combos/build.py
python3 orchestration/work/phub-ledger-redesign/first-pass/problem-combos/verify.py   # 실패 시 exit 1, 아무 파일도 쓰지 않음
```

## 기계 검증 결과 (2026-11-09 최종 실행)

`132 checks, 0 failures; nodes=460 leaves=370 strings=370` · exit 0

| 검사 | 결과 |
|---|---|
| 원본 sha256 시작/끝 `74453c72…2cf2262` (HASHES.txt 접두 `74453c724800975e` 일치) | PASS · 불변 |
| 중복 키 (object_pairs_hook) | 0 |
| 원본 전체 Pointer 460 ↔ source-map 노드 양방향·문서 순서 | PASS |
| 값·자료형·키 순서·배열 길이 | PASS |
| 리터럴 구간(코드포인트)·바이트 구간·문자열 내용 구간·키 리터럴 구간 원문 재현 | PASS (460 노드, 키 340 출현) |
| 빈 값(빈 문자열·빈 배열·빈 객체·null) | 0 — review 주장과 일치 |
| 비문자열 말단(숫자·불리언) | 0 |
| 구획 소유 합집합 = 원본 전체(양방향)·중복 0, 말단 370 대응 | PASS |
| 구획 9개 직접 읽기 상태 `read`·수동 기록·review 파일 실재 | PASS |
| 각 review-part 에 소유 Pointer 전부·원문 값 전부 원문 그대로 | PASS |
| 수동 관찰 Pointer 유효·구획 안, 수동 표현 원문 실재 | PASS |
| 형태소: 문자열 말단 370 ↔ 기록 1:1·순서, 적용 249/제외 121 규칙 일치·사유 | PASS |
| 토큰 구간 재현(0폭 복원 토큰 24개 포함)·공백 외 모든 문자 토큰 덮음 | PASS (토큰 4,045) |
| 필드명 출현 = 원본 모든 키 출현(340)·고유 키 20 토큰 기록 | PASS |
| 알려진 오분절 81건 구간 재현·상태 K | PASS |
| 표현 666건(수동 323·정규식 343) 값 구간·파일 구간 재현·생성 중복 0 | PASS |
| 수동 기록 표현 → expressions 전부 반영 | PASS |
| 문장 구간 388 재현·적용 값 전부 문장 보유 | PASS |
| 구획 미결 ID 전부 issues.md 에 | PASS |

### verify 자체 시험 (scratchpad 사본에서 변조, 레포 파일 무변경)

| 변조 | 결과 |
|---|---|
| coverage S3 에서 `/combos/2/packages/0/id` 소유 제거 | FAIL 「누락 ['/combos/2/packages/0/id']」 · exit 1 |
| review-part-S5 원문 「트라넥사민산(TXA)」 → 「트라넥사민산」 | FAIL 「S5 review 에 원문 값 전부」 |
| expressions E0010 끝 구간 +1 | FAIL 「표현 구간…재현」 |

## 별도 읽기 검토

- 구획 S0~S8 원문을 위에서 아래로 직접 읽고 구획마다 관찰·표현·미결을 `manual/S*.json` 에 즉시 기록(progress.md).
- 보조 정규식 후보(부정·가능성·조건·정도·수량·순서·괄호·대안) 중 수동 표현에 덮이지 않은 것을 전부 열어 읽음 → 실제 누락 구절 29건(최상급·조건·시술(기전) 나열 전체·순서 연쇄 전체·problem 값 `/` 나열 등)을 수동 표현에 추가(`added_in: 읽기 검토`). 남은 미덮음은 오탐 `동안`·`세안`, 부분 연쇄 1건(양쪽 구절은 수동에 있음) — issues.md K.
- 수식·부정·가능성·조건·범위·시간: 「드물게」「거의 없어서」「않아」「안 돼요」「아닌」「보장하지는 않습니다」「~ 가능」「~할 수 있으나」「-시면」「3~6개월」「6개월 이상」「(개인차 큼)」 등 원문 구간으로 보존, 수치·백분율 변환 없음.
- 형태소 오분절이 의미에 주는 영향: `안내`→부정 부사 오탐, `리쥬란` 제품명 분해(12출현), `하안면`·`심부`·`이중` 손실 — issues.md K, morphology.json `known_missegmentations`.
- 고친 A: 정규식 `더`/`약` 오탐(`더블로골드`·`약하지만`), K 분류 미구분 → 수정 후 재생성·재검증.
- 미검토: 의미 관계·필드 역할·공통 개념·코드 연결(후속 단계). 기계 통과는 의미 정답이 아니다.
