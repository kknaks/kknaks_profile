# treatment-optimization.json — 검증 기록

> 손으로 쓰는 문서다(build.py 가 생성·덮어쓰지 않는다). 명령은 모두 레포 루트에서 실행했다.

## 상태 (맨 위)

- **1차 범위 종료: 예** — 14/14 구획 직접 읽기, 구조·값 전수 대응, 형태소(적용/제외 명시)·복합 표현 수집과 원문 대조, 기계 검증 140/140, 별도 읽기 검토 완료.
- **원장 전체 완료 아님** — 원문 정보 부족 B 26 · 원문 내 불일치 후보 I 12 · 후속 의미 조사 F 14 · 알려진 분석 한계 K 6 이 열려 있다([issues.md](./issues.md)). 사용자 결정 C 0(근거는 issues.md 끝 절).

| 항목 | 상태 |
|---|---|
| 전수 읽기 | 14/14 구획 direct_read_done(manual/seg-00~13.json). 1회차 원문 통독 + 관찰 즉시 저장 → 2회차 토큰 3,025개 전체를 원문과 나란히 대조 → 3회차 자동 후보·미덮임 어절·블록 간 대조 |
| 구조·값 수집 | 노드 691(말단 502: 문자열 455·정수 36·빈 배열 11) · 키 출현 388 · 필드명 41종 · 중복 키 0 |
| 형태소·표현 수집 | Kiwi 0.24.1 cong 단일 스레드 · 분석 413값 / 제외 42값(사유별) / 비문자열 36 · 필드명 41 별도 · 토큰 3,025 · 표현 1,758(자동 정규식 1,114 · 자동 절 231 · 직접 읽기 수동 413) |
| 기계 검증 | verify.py 140검사 통과(EXIT 0) · 변이 시험 7종 모두 검출 · build 재실행 산출물 해시 동일 |
| 읽기 검토 | 같은 에이전트의 관점 바꾼 재읽기(독립 검토 아님, K-06). 수식·조건·부정 탈락 점검 |
| 알려진 분석 오류 | 오분절·오태깅 77출현(manual/segmentation-review.json) — 교정 안 함, 영향 기록 |
| 열린 미결 | B 26 · I 12 · K 6 · F 14 · C 0 |
| 후속 의미 조사 | 표기 연결·기호 쓰임·블록 간 연결·간격 기준 시점·추천/금지 조건 구조(F-G1~G5 + 구획별 F) |

## 1. 실행 명령과 결과

```bash
# 생성(Kiwi 필요)
OMP_NUM_THREADS=1 uv run --no-project --python 3.12 --with kiwipiepy==0.24.1 \
  python orchestration/work/phub-ledger-redesign/first-pass/treatment-optimization/build.py
# → build-output.txt: sha256 07b9ebe0…9767b expected_match True · nodes 691 keys 388 dups 0
#   tokens 3025 applied 413 excluded 42 nonstring 36 · expressions total 1758 · auto_false_positive 14
#   modifier_tokens_unreviewed 0 · segments_read 14/14 · sha256_end unchanged True

# 독립 검증(표준 라이브러리만, 파일 쓰기 없음, 실패 시 exit 1)
python3 orchestration/work/phub-ledger-redesign/first-pass/treatment-optimization/verify.py
# → checks=140 failures=0 nodes=691 leaves=502 tokens=3025 expressions=1758 · EXIT 0

# 변이 시험(임시 디렉토리 복사본만 변경, 끝나면 삭제)
python3 orchestration/work/phub-ledger-redesign/first-pass/treatment-optimization/mutation-test.py
```

`--no-project` 는 레포 루트에 pyproject 가 없어도 uv 가 프로젝트 탐색을 하지 않게 붙였다(전역 설정 변경 없음, 공유 uv 캐시만 사용).

변이 시험 결과(각각 복사본 하나만 망가뜨림):

| 변이 | verify | 잡은 검사 |
|---|---|---|
| (기준) 변경 없음 | exit 0 | — |
| coverage 에서 말단 Pointer 하나 삭제 | exit 1 | coverage.leaf_source_to_segments · segment_matches_source_map |
| 말단 하나를 두 구획이 소유 | exit 1 | coverage.leaf_no_duplicate_owner · segment_matches_source_map |
| 구획 하나를 not_read 로 | exit 1 | coverage.SEG-12.direct_read |
| 토큰 하나의 start +1 | exit 1 | morph.token_surface_reproduces_source · every_nonspace_char_in_some_token |
| review-part 에서 값 행 하나 삭제 | exit 1 | review.every_node_row_in_owning_part |
| 수동 표현 구간 +1 | exit 1 | expr.span_reproduces_source |
| source-map 값 하나 변경 | exit 1 | source_map.values_types_match_source · value_span_literal |

## 2. verify.py 가 확인하는 것

- **원본**: sha256 시작·끝 불변(07b9ebe0a843280b4eef9487590951932192435ea46284aba425338ab9d9767b, 원장 폴더 HASHES.txt 접두와 일치), 중복 키 0(json 파서 hook 로 독립 감지).
- **구조·값 양방향**: build 스캐너를 쓰지 않고 json 파서 + 재귀로 다시 만든 경로 집합과 source-map 노드를 양방향 대조(누락·여분·순서·중복 Pointer), 자료형·값·객체 키 순서·배열 길이 일치, 키 출현(객체·키·순번) 양방향.
- **구간 재현**: 모든 노드의 span 을 원문에서 잘라 다시 파싱하면 원본 하위 트리와 같다. byte_span 은 UTF-8 바이트로 같은 텍스트를 재현. 문자열 value_span 은 디코딩 값과 같다(이스케이프 0).
- **구획 대응**: 전체 말단(빈 컨테이너 포함) 집합 ↔ 구획 소유 말단 합집합 양방향, 중복 소유 0, 컨테이너 소유 양방향, 구획별 direct_read_done·manual 기록 실재·review 파일 앵커 실재, context_refs 는 실재하고 그 구획이 소유하지 않음.
- **문서 대조**: 모든 노드가 소유 구획의 review-part 절에 Pointer·원본 컬럼명·원문 JSON 리터럴로 한 행씩 있다. review.md 목차가 모든 구획을 링크하고 컬럼 구성 표가 모든 경로 패턴을 담는다.
- **형태소**: 분석 적용 ∪ 제외 = 전체 문자열(서로소), 제외 사유 존재, 비문자열 말단 전부 목록, 필드명 = 전체 키 종류. 모든 토큰 surface = 원문 구간, 분석 값의 공백 아닌 모든 문자가 어떤 토큰 안에 있음(누락 문자 0), 알려진 오분절 77출현의 원문·원시 토큰 재현.
- **표현**: id 유일·완전 중복 0, 모든 구간이 원문 재현, 제외 값에 표현 없음, 수동 구절 ↔ manual 기록 양방향, 자동 정규식을 다시 돌린 결과와 양방향 일치, 오탐 표시 ↔ expression-review 일치, 수식·부정 토큰 점검 목록이 기준(태그·형태)에 맞는 토큰 전부를 담고 UNREVIEWED 0.
- **미결·파일**: manual 의 모든 issue id 와 전역 issue id 가 issues.md 에 있다. 필수 산출 파일 실재.

## 3. 별도 읽기 검토 (같은 에이전트, 관점 변경)

1. **토큰 대조**: 413값의 토큰 3,025개 전체를 구획 순서로 원문과 나란히 열람했다. 의미를 바꾸는 오분절 77출현을 출현별로 기록(manual/make-segmentation-review.py → segmentation-review.json). 영향이 큰 것: 거짓 수량(「열시술」→열/NR 시/NNB 3출현, 「CO2」→2/SN 12출현, 「미백」→백/NR), 부정 소실(「비수술 조합」→비수/NNG, 「비가교」·「비마사지군」 한 토큰), 거짓 부사(「엑소좀」→좀/MAG, 「아이스픽」→픽/MAG, 「슬림」→슬/MAG), 시점어 소실(「동시」→동/MM 시/NNB, 「선행」→선+행, 「남은」→남/NNG), 단계어 분해(「중등도」→중등+도/JX 8출현). 반면 「미승인」(미/XPN)·「불필요」(불/XPN)·「비수술로」(비/XPN)·「않음」·「없었으며」 는 부정이 보존됐다.
2. **자동 후보 대조**: 정규식 후보 1,114개를 패턴별로 문맥과 함께 열람해 의미를 바꾸는 오탐 14출현을 표시했다(「비만」의 만, 「지지하지만」의 만, 「최소화」의 최소, 「광고 내」, 「FDA 미용」의 미, 고민 상태 「저하」 3, 일정이 아닌 「동시」 2, 경계 잘림 4). 「개월」 안의 「월」을 잡던 R19 는 추출 오류(A-01)라 정규식을 고쳤다. R04/R05 의 경계 잘림 전반은 K-03 으로 남겼다.
3. **수식·부정 토큰 포괄**: Kiwi 태그 MAG·MAJ·MM·VA·XPN·XSA·VCN·VX·NR 와 형태 목록(않·없·미·비·불·만·후·내·이내·이상·최소·가능·금지·단독·동시·당일·직후·즉시 등)에 걸린 토큰 206개 전부가 수동 구절 안(covered_by_manual)이거나 알려진 오분절 구간 안(known_missegmentation)이다. 미검토 0.
4. **미덮임 어절**: 자동(오탐 제외)·수동 어느 구절에도 덮이지 않은 어절(앞뒤 구두점 제거 후) 163개(55종)를 전부 열람했다. 단독 시술명·고민명 값(토닝 31·스킨부스터 19·보톡스 13 …)과 괄호·구두점으로 이어진 어절(「수준)+소규모」「교차(시험」 등 — 각 부분은 다른 구절에 덮임)뿐이다. 이 검토 중 누락 수동 구절 2건(「엑소좀 근거는」「HA 필러는」)을 찾아 추가했다(A-04).
5. **패턴 밖 수식·조건 수집**: 정규식 목록에 없는 형용사·부사·회피/권고·깊이/두께·속도·근사·수치단위·「후/시」 조건을 직접 읽기에서 수동 구절로 모았다(예: 「얕은 필링」「약한 산」「즉각 볼륨」「점진적 개선」「위주」「흉터급」「울쎄라급」「사이사이」「매회 마무리」「후부터」「활성 여드름 시」「필요시」「소범위는 … 충분」「웬만하면」「HIFU와 동일한 절대 규칙으로 취급하지 않음」「2-4회/년」「12-18개월 + 유지」). 수동 구절은 대표 표현 표본이 아니라 구획별 직접 읽기 결과지만, 이것이 원문 전체의 의미 해석이라고 주장하지 않는다.
6. **블록 간 대조(원장 내부만)**: combination_rules ↔ by_concern 금지문, by_age_group.maintenance ↔ annual_plans.schedule 빈도, annual_plans.age_group ↔ by_age_group.age 를 대조해 원문 내 불일치 후보 I 12건을 기록했다(예: HA 필러→HIFU 「4주 이상 권장」 vs 「14일 이내 금지」, 프락셔널 후 필러 「당일 금지」 vs 「최소 4주」, 기미 「저출력 토닝만 권장」 vs 「저출력 IPL(병용 보조)」, 제모 부위 「2주 내」 vs 「동시」, 토닝 「월 4회」 vs 「월 1-2회」). 판정하지 않았다.
7. **다국어**: 영어·한자 구간은 원문 그대로 보존했고, Kiwi 는 SL/SH 토큰으로만 자른다(K-02). 영어 표현은 수동 구절(kinds=language_en)과 R20 라틴 연속 후보로만 수집했다.

## 4. 검증하지 않은 것

- 원시 형태소 출력의 77출현 밖 정확성, NNP/NNG 태그 흔들림의 출현별 목록.
- 원장의 임상·규제·문헌 서술의 사실 여부(외부 자료로 보충하지 않음).
- 의미 관계(효과 보완·동일일·순서·간격·회피·조건)의 확정, 같은 대상의 다른 표기 병합, 블록 간 연결 규칙 — 1차 범위 밖(F).

## 5. batch-04 기록 보완 — I-10-1·I-10-2·I-10-4 비고 (2026-11-09)

독립 검토 [batch-04-review.md](../../batch-04-review.md) §2.5 R2 반영. 분류(I)·ID·집계(I 12)는 그대로다. 원문을 고치거나 새 관계를 적용하지 않았다.

- 무엇: `manual/seg-10.json` 의 세 issue 에 `note` 를 추가했다 — 「양립 가능; 모순으로 확정하지 않음」, 관계(14일 이내 금지 vs 4주 권장 = 별개 강도 · 당일 금지 ⊂ 최소 4주 · 동시 금지 ⊂ 2주 내 금지), 후속 검토로 남는 범위, 「원문 모순 확정 목록에 넣지 않는다」.
- 생성부: build.py `write_issues` 가 `note` 를 `  - 비고:` 줄로 찍는다. verify.py 의 `issues.all_recorded` 가 manual 의 note 가 issues.md 에 그대로 있는지도 본다(검사 수는 그대로 140).
- 실제 결과:
  - `python3 treatment-optimization/verify.py` → `checks=140 failures=0`, EXIT 0.
  - 스크래치 복사본에서 build.py 재실행: 보완 전 상태로는 기존 산출물 13개 전부 바이트 동일. 보완 후에는 `issues.md` 만 다르고 차이는 비고 3줄 추가뿐이다.
  - 변이 시험(스크래치): issues.md 의 I-10-2 비고 변조 → exit 1, 복원 → exit 0.
