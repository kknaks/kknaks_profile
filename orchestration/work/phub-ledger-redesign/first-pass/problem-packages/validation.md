# problem-packages.json — 검증 기록

**1차 범위 종료: 예 · 원장 전체 완료: 아님** (열린 B 9 · I 10 · F 8 · K 5, 잠정 관찰 P 98 — [issues.md](issues.md)). A 0 · C 0.

| 상태 | 결과 |
|---|---|
| 전수 읽기 | 15/15 구획 직접 읽기 done (S00 → S14, 남은 구획 없음 — coverage.json `reading_log`, progress.md) |
| 구조·값 수집 | 노드 3656 · 말단 2366(전부 string) · 빈 값 48(products 빈 배열 47 · combos 빈 배열 1) · 필드명 20종 · 중복 키 0 · 이스케이프 0 · 선택적 필드 0 |
| 형태소 | 텍스트 값 2096 · 필드명 20 · 제외 270(version·updated·problem_id 14·category 254 — 코드/ID) · 토큰 6708(서로 다른 문자열 561 분석) · 길이 0 복원 토큰 69(전부 이/VCP) |
| 표현 | 수동 표현 871 출현 · 정규식 후보 1031 · 절 구간 27 |
| 단서 대조(읽기 검토 보조) | 정규식 단서 375 · 수동 표현이 덮음 360 · 판단 기록 15('반영구' 이름 일부) · 미처리 0 |
| 기계 검증 | verify.py 91851 검사 · 실패 0 · 종료 코드 0. 변조 시험 7종 모두 감지(종료 코드 1) |
| 알려진 분석 오류 | K-01~K-05 (출현별 Pointer·구간·원시 토큰 — morphology.json `known_errors`) |
| 열린 미결 | B 9 · I 10 · F 8 · C 0 · A 0 |
| 후속 의미 조사 | F 8 + I 10 후속 확인 + 1차에서 검토하지 않은 의미 관계 전부 |

## 실행 환경과 명령

- 원본: `orchestration/work/phub-recommend/bronze/phub-ledger/problem-packages.json` · 73526 바이트 · 48965 코드 포인트 · 한 줄 · BOM 없음 · 최대 코드 포인트 U+D790(BMP)
- sha256 시작=끝 `e44fa7216e0eceefde4be368fcdfa623df0834de6989b826f66ba4e408fcb3dc` (build·verify 각각 시작·끝에서 재계산)
- 형태소: Kiwi(kiwipiepy 0.24.1) `model_type="cong"`, `num_workers=1`, `OMP_NUM_THREADS=1`, 기본 내장 사전, 사용자 사전 없음, 오타 교정 없음, 입력 정규화 없음
- 임시 파일: 결과 폴더 밖에 쓰지 않음(uv 공유 패키지 캐시만 사용). 변조 시험은 세션 스크래치패드 사본에서 실행 후 삭제

```sh
# 레포 루트에서
python3 orchestration/work/phub-ledger-redesign/first-pass/problem-packages/reading_dump.py      # 읽기용 덤프(reading/)
OMP_NUM_THREADS=1 uv run --python 3.12 --with kiwipiepy==0.24.1 \
  python orchestration/work/phub-ledger-redesign/first-pass/problem-packages/build.py
python3 orchestration/work/phub-ledger-redesign/first-pass/problem-packages/verify.py
```

build.py 출력(최종):

```text
source sha256 start e44fa7216e0eceefde4be368fcdfa623df0834de6989b826f66ba4e408fcb3dc end e44fa7216e0eceefde4be368fcdfa623df0834de6989b826f66ba4e408fcb3dc same
nodes 3656 leaves 2366 empty 48 fields 20
morph text_values 2096 fields 20 excluded 270 tokens 6708 distinct 561
manual_expr 871 regex 1031 clauses 27 observations 144 issues 32
name_splits 81 form_mismatch 279
cue hits {'cue_hits': 375, 'covered': 360, 'decided': 15, 'unresolved': 0}
clause cut-through (괄호 불균형) [('/problems/10/complaints/2/cc_detail', 0), ('/problems/10/complaints/2/cc_detail', 1)]
```

verify.py 출력(최종):

```text
source sha256 start=e44fa7216e0eceefde4be368fcdfa623df0834de6989b826f66ba4e408fcb3dc end=e44fa7216e0eceefde4be368fcdfa623df0834de6989b826f66ba4e408fcb3dc
nodes=3656 leaves=2366 strings=2366 empty=48 fields=20
sections=15 owned_union=3656 text_values=2096 excluded=270 tokens=6708
manual=871 regex=1031 clauses=27 cue_rows=375 issues=32
zero_width_tokens=69 forms=[('이', 'VCP')]
checks=91851 fails=0
```

## verify.py 가 검사하는 것

pp_common.py·build.py 를 쓰지 않고 표준 `json`(object_pairs_hook 로 중복 키 감지)으로 원본을 다시 파싱해 정답 Pointer 집합을 만든다. 파일은 읽기만 한다.

1. 원본 해시 시작/끝 불변, source-map 기록 해시·크기 일치
2. source-map Pointer 집합 ↔ 원본 전체 Pointer 집합 양방향 일치, 중복 0, 문서 순서 일치, 빈 값 목록·필드명 출현 위치 일치
3. 노드마다 자료형·구획·값·자식 키/개수, JSON 리터럴 구간(코드 포인트)·바이트 구간·문자열 내용 구간이 원문을 그대로 재현
4. coverage: 구획 소유 합집합 = 전체 Pointer(누락·중복 소유 0), 구획 밖 Pointer 소유 금지, 소유 말단·빈 값 일치, 15구획 모두 direct_read=done·machine_extracted=done, review-part·manual 기록 실재, 공유 문맥 참조가 S00 소유
5. morphology: 적용∪제외 = 전체 말단(양방향), 겹침 0, 제외마다 사유·규칙 일치, 토큰 구간 순서·표면 재현·파일 구간 재현, 길이 0 토큰은 surface '' 로 표시, 토큰 수 일치, 필드명 20종, K 출현 구간 재현
6. expressions: 수동·정규식·절 구간 모두 값·파일 코드 포인트·바이트 재현, 수동 표현 (Pointer,구간) 중복 0, 15구획 모두 수동 표현 있음
7. cue-review: 단서마다 덮임 여부 재계산 일치, 덮이지 않은 단서는 판단 기록 필수, 판단 기록은 실제 단서에만
8. manual 기록 상태 문자가 A/B/C/I/K/P/F 안에 있음, 미결 ID 접두=상태, C 항목 없음
9. review.md 가 모든 review-part 를 링크, 각 part 에 소유 Pointer 전부의 행·원본 컬럼명·원문 값(문자열 전부)이 있음, issues.md 에 모든 미결 ID
10. 필수 산출 파일 실재

### 변조 시험 (스크래치패드 사본)

| # | 변조 | 결과 |
|---|---|---|
| 0 | 없음(대조군) | exit 0 |
| 1 | 원본 값 1자 변경(쁘띠시술→쁘띠시숧) | exit 1 — 해시 불일치, 값 불일치 |
| 2 | coverage 소유 Pointer 1개 삭제 | exit 1 — 합집합 누락 1 |
| 3 | 수동 표현 구간 1칸 이동 | exit 1 — 구간 재현 실패 |
| 4 | review-part-S07 행 1개 삭제 | exit 1 — part 에 Pointer 없음 |
| 5 | S09 direct_read=pending | exit 1 — 미독 구획 |
| 6 | morphology 텍스트 값 1개 제거 | exit 1 — 적용∪제외 누락 |
| 7 | 다른 구획 Pointer 중복 소유 | exit 1 — 구획 밖 소유·중복 소유 |

## 읽기 검토 (기계 검증과 별도)

- **단서 대조**: 부정·한정(없/않/아닌/허가 외/부족/제한), 가능성(수 있/가능), 조건(…시/경우), 범위(n~m, n-m), 수량·단위(nm·개월·주·회·배), 시간·순서(후/뒤/간격/즉각/장기/사전/동시), 정도·지시(가장/최대/영구/필수/권장/추천 등) 375 출현을 수동 표현과 대조했다. 처음 빌드에서 덮이지 않은 17건 중 2건(`/problems/10/complaints/5·6/procedures/1/role` '장기 콜라겐')은 수동 표현 누락이라 S11 기록에 보강했고, 15건은 '반영구화장' 이름 안의 '영구' 라서 정도 단서가 아니라는 판단을 `manual/cue-decisions.json` 에 남겼다.
- **부정·가능성 보존**: '없음'(없/VA 음/ETN), '않으며'(않/VX), '아닌'(아니/VCN), '수 있음'(수/NNB 있/VA), '피할 것'(피하/VV) 은 토큰에 남아 있다. 다만 '있음'·'쳐짐'·'무너짐'·'꺼짐' 의 '-ㅁ' 이 EF 로 분석되는 등 오분석은 K-02 로 기록했다.
- **절 분할 한계**: `/problems/10/complaints/2/cc_detail` 은 세미콜론이 괄호 안에 있어 절 구간 2개가 괄호를 가로질러 잘린다(paren_balanced=false 로 표시). 값 전체는 source-map·morphology 에 그대로 있고, 수동 표현이 괄호 전체(`턱밑지방 개선 허가(…)`)와 내부 구절을 따로 덮는다. 절 구간은 문맥 보조이며 의미 단위가 아니다.
- **이름형 값 오분절**: cc·name·products·combo 원소 중 조사·어미·접사·용언 태그가 끼어든 값 81 출현을 `name_value_functional_splits` 로 기록했고, 출현값을 원문과 대조해 K-02~K-05 트리거로 묶었다(대조 후 K 에 없던 '무너짐'·'꺼짐'·'수 있음' 추가).
- **관찰 주장 재확인**: 원장 전체 대조 스크립트로 products 빈 배열 47, combo 원소 ↔ procedures 이름 불일치 36(PRP 23·MTS 6·바이오스티뮬레이터 4·필링 3), 중복 cc 6종, category 코드별 이름 목록, alternatives 반복 빈도를 다시 셌고 S00 관찰(OB-S00-05~07)에 전체 Pointer 를 붙였다. 기계 비교는 후보 찾기에만 썼고 각 사례는 reading/ 덤프에서 원문을 다시 확인했다.
- **미검토**: 의미 관계(공통 개념·동의어·관계 방향·적용 조건), 다른 원장과의 대응, 임상·법적 진술의 사실 여부.
