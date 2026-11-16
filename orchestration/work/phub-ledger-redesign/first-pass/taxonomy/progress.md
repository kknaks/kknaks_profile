# taxonomy 1차 조사 — 진행 기록

재개 시 이 파일과 `coverage.json`(read_state)·`manual/S###.json` 을 대조한다. manual 파일이 있고 state=read 인 구획만 직접 읽기 완료다.

## 재현 명령 (레포 루트)

```bash
# 구조·구획·읽기 렌더·리뷰만 (kiwi 불필요)
python3 orchestration/work/phub-ledger-redesign/first-pass/taxonomy/build.py --no-morph
# 전체(형태소 포함)
uv run --python 3.12 --with kiwipiepy==0.24.1 python orchestration/work/phub-ledger-redesign/first-pass/taxonomy/build.py
# 검증
python3 orchestration/work/phub-ledger-redesign/first-pass/taxonomy/verify.py
```

## 작업 방식(재개용)

1. `reading/S###.txt` 를 Read 로 전부 읽는다(잘리면 offset 으로 나눠 읽기).
2. `python3 tok.py S### 단어…` 로 전문어 형태소 확인.
3. `manual/S###.json` 작성: observations(status·pointers·note) / expressions(pointer·정확한 원문 text·kinds·note) / seg_errors(scope all|pointer, surface, issue, impact) / issues(id S###-X##, status A/B/C/K/P/F/I).
4. `python3 _prog.py <다음구획>` 로 이 파일 갱신.
5. 전 구획 후: build(전체) → verify.py → validation.md·issues.md·review.md 마무리 → 보고.
- 반복 상용구·전역 패턴은 `manual/GLOBAL.json`. W_SERIAL(범위+목록) 설명 갱신 완료.

## 구획 계획

- 53구획(S000~S052). 모달리티별 문서 순서로 값 단위 묶음(목표 렌더 약 9,000자, 값 중간 절단 없음). problem 은 S051~S052(실제 경계는 coverage.json).
- 읽기 렌더: `reading/S###.txt` (Pointer = `@ base` + 상대경로, 스칼라 배열은 `i:값 ‖` 인라인).

## 상태

- 기계 추출: 전 구획 완료(source-map.json, coverage 계획)
- 직접 읽기: 53/53 완료. 이후 build(전체)·verify(failure_count=0)·validation.md·issues.md 작성 완료 — 1차 범위 종료, 원장 전체 완료 아님
- 현재 구획: S052 까지 직접 읽기 완료 (53/53)
- 다음 구획: 없음 (남은 구획 없음) — 코디 보고 단계

## 읽기 로그

| 구획 | 상태 | 마지막 읽은 Pointer | 기록 |
|---|---|---|---|
| S000 | read | `/problem` | 관찰 1 · 표현 0 · 오분절 0 · 미결 0 |
| S001 | read | `/modality/0/subcategories/1/items/7/extracted/aftercare/4` | 관찰 10 · 표현 28 · 오분절 4 · 미결 4 |
| S002 | read | `/modality/0/subcategories/2/items/6/extracted/aftercare/3` | 관찰 9 · 표현 24 · 오분절 4 · 미결 3 |
| S003 | read | `/modality/0/products/3/extracted/aftercare/3` | 관찰 11 · 표현 34 · 오분절 4 · 미결 3 |
| S004 | read | `/modality/0/name` | 관찰 7 · 표현 17 · 오분절 2 · 미결 3 |
| S005 | read | `/modality/1/subcategories/0/items/14/extracted/aftercare/3` | 관찰 10 · 표현 23 · 오분절 5 · 미결 3 |
| S006 | read | `/modality/1/subcategories/2/items/1/extracted/aftercare/3` | 관찰 9 · 표현 28 · 오분절 4 · 미결 4 |
| S007 | read | `/modality/1/name` | 관찰 9 · 표현 29 · 오분절 4 · 미결 3 |
| S008 | read | `/modality/2/subcategories/3/items/2/extracted/aftercare/2` | 관찰 9 · 표현 24 · 오분절 4 · 미결 4 |
| S009 | read | `/modality/2/products` | 관찰 9 · 표현 24 · 오분절 3 · 미결 3 |
| S010 | read | `/modality/2/name` | 관찰 6 · 표현 14 · 오분절 0 · 미결 3 |
| S011 | read | `/modality/3/subcategories/1/items/6/extracted/aftercare/3` | 관찰 8 · 표현 19 · 오분절 4 · 미결 3 |
| S012 | read | `/modality/3/subcategories/3/items/0/extracted/aftercare/3` | 관찰 8 · 표현 21 · 오분절 5 · 미결 3 |
| S013 | read | `/modality/3/name` | 관찰 9 · 표현 20 · 오분절 2 · 미결 4 |
| S014 | read | `/modality/4/name` | 관찰 9 · 표현 25 · 오분절 1 · 미결 3 |
| S015 | read | `/modality/5/name` | 관찰 6 · 표현 22 · 오분절 0 · 미결 2 |
| S016 | read | `/modality/6/subcategories/2/items/2/extracted/aftercare/4` | 관찰 10 · 표현 27 · 오분절 2 · 미결 3 |
| S017 | read | `/modality/6/subcategories/2/items/15/extracted/aftercare/3` | 관찰 7 · 표현 16 · 오분절 0 · 미결 2 |
| S018 | read | `/modality/6/products/2/extracted/aftercare/4` | 관찰 9 · 표현 27 · 오분절 3 · 미결 3 |
| S019 | read | `/modality/6/name` | 관찰 3 · 표현 9 · 오분절 0 · 미결 2 |
| S020 | read | `/modality/7/subcategories/0/items/11/extracted/aftercare/2` | 관찰 8 · 표현 26 · 오분절 2 · 미결 3 |
| S021 | read | `/modality/7/subcategories/1/items/7/extracted/aftercare/5` | 관찰 8 · 표현 22 · 오분절 4 · 미결 3 |
| S022 | read | `/modality/7/subcategories/3/items/2/extracted/aftercare/5` | 관찰 8 · 표현 22 · 오분절 4 · 미결 3 |
| S023 | read | `/modality/7/subcategories/4/items/5/extracted/aftercare/2` | 관찰 8 · 표현 19 · 오분절 3 · 미결 3 |
| S024 | read | `/modality/7/subcategories/5/items/7/extracted/aftercare/3` | 관찰 8 · 표현 22 · 오분절 1 · 미결 3 |
| S025 | read | `/modality/7/products/2/extracted/aftercare/4` | 관찰 8 · 표현 23 · 오분절 0 · 미결 3 |
| S026 | read | `/modality/7/name` | 관찰 4 · 표현 11 · 오분절 0 · 미결 2 |
| S027 | read | `/modality/8/subcategories/0/items/11/extracted/aftercare/3` | 관찰 7 · 표현 18 · 오분절 4 · 미결 2 |
| S028 | read | `/modality/8/subcategories/1/items/8/extracted/aftercare/2` | 관찰 8 · 표현 17 · 오분절 0 · 미결 4 |
| S029 | read | `/modality/8/subcategories/3/items/3/extracted/aftercare/4` | 관찰 8 · 표현 16 · 오분절 3 · 미결 3 |
| S030 | read | `/modality/8/products/5/extracted/aftercare/3` | 관찰 9 · 표현 22 · 오분절 0 · 미결 4 |
| S031 | read | `/modality/8/name` | 관찰 2 · 표현 3 · 오분절 0 · 미결 1 |
| S032 | read | `/modality/9/name` | 관찰 8 · 표현 24 · 오분절 2 · 미결 3 |
| S033 | read | `/modality/10/subcategories/0/items/12/extracted/aftercare/2` | 관찰 7 · 표현 15 · 오분절 1 · 미결 3 |
| S034 | read | `/modality/10/name` | 관찰 5 · 표현 12 · 오분절 1 · 미결 2 |
| S035 | read | `/modality/11/name` | 관찰 6 · 표현 24 · 오분절 3 · 미결 1 |
| S036 | read | `/modality/12/name` | 관찰 6 · 표현 12 · 오분절 0 · 미결 0 |
| S037 | read | `/modality/13/name` | 관찰 7 · 표현 18 · 오분절 0 · 미결 1 |
| S038 | read | `/modality/14/subcategories/0/items/18/extracted/aftercare/2` | 관찰 10 · 표현 22 · 오분절 2 · 미결 3 |
| S039 | read | `/modality/14/subcategories/0/items/36/extracted/aftercare/3` | 관찰 6 · 표현 19 · 오분절 2 · 미결 2 |
| S040 | read | `/modality/14/subcategories/0/items/55/extracted/aftercare/2` | 관찰 7 · 표현 15 · 오분절 2 · 미결 2 |
| S041 | read | `/modality/14/subcategories/2/items/5/extracted/aftercare/2` | 관찰 9 · 표현 18 · 오분절 0 · 미결 2 |
| S042 | read | `/modality/14/subcategories/8/items/1/extracted/aftercare/1` | 관찰 8 · 표현 20 · 오분절 0 · 미결 2 |
| S043 | read | `/modality/14/subcategories/10/items/10/extracted/aftercare/2` | 관찰 7 · 표현 22 · 오분절 0 · 미결 2 |
| S044 | read | `/modality/14/subcategories/13/items/2/extracted/aftercare/3` | 관찰 7 · 표현 22 · 오분절 2 · 미결 2 |
| S045 | read | `/modality/14/name` | 관찰 6 · 표현 21 · 오분절 0 · 미결 2 |
| S046 | read | `/modality/15/subcategories/2/items/2/extracted/aftercare/2` | 관찰 7 · 표현 25 · 오분절 3 · 미결 3 |
| S047 | read | `/modality/15/subcategories/4/items/5/extracted/aftercare/2` | 관찰 7 · 표현 26 · 오분절 4 · 미결 3 |
| S048 | read | `/modality/15/subcategories/6/items/2/extracted/aftercare/1` | 관찰 8 · 표현 20 · 오분절 3 · 미결 3 |
| S049 | read | `/modality/15/name` | 관찰 8 · 표현 22 · 오분절 2 · 미결 4 |
| S050 | read | `/modality/16/name` | 관찰 8 · 표현 21 · 오분절 0 · 미결 3 |
| S051 | read | `/problem/9/subcategories` | 관찰 10 · 표현 25 · 오분절 0 · 미결 3 |
| S052 | read | `/problem/13/subcategories/3/items/1/modality_ref/0` | 관찰 12 · 표현 18 · 오분절 0 · 미결 3 |
