# batch-03 최종 메모 — 검토 후 기록 보완

- 작업: writer 워커 `task_ab140532d140` / `ctx_fe7da4375fe6` · 2026-11-09
- 근거 검토: [batch-03-review-taxonomy.md](./batch-03-review-taxonomy.md) §3-1·§3-2, [batch-03-review-others.md](./batch-03-review-others.md) §2.1·§3
- **상태: 기록 보완 반영, 코디 확인 전.** 원장 전체 완료가 아니다. 의미 정답이나 모든 표현 수집 완료를 주장하지 않는다.

## 1. 변경 파일 (6개 + 이 메모)

| 파일 | 변경 |
|---|---|
| `first-pass/taxonomy/issues.md` | 집계 표 아래에 「구조화 K 4 와 문서 기록 구분」 단락 추가. 끝에 「batch-03 검토 후 기록 보완」 절 추가(K-EXPR01, OBS-M16-PRODUCTS) |
| `first-pass/taxonomy/validation.md` | 「별도 읽기 검토」의 과장 문구 1문장을 정정. 상태 표 「형태소·표현 수집」 칸에 K-EXPR01 참조 추가 |
| `first-pass/taxonomy/review.md` | 상태 표 아래에 보완 안내 1줄 |
| `first-pass/literature-evidence/issues.md` | 상태 요약 아래에 구분 단락. K-ENG/K-ZHJA 원문 아래에 정정 3항목(원문 문장은 남겨 둠). 끝에 K-KOCOND 절(7건 표) |
| `first-pass/literature-evidence/validation.md` | §4 「검토하지 않은 것」 뒤에 보완 단락 |
| `first-pass/literature-evidence/review.md` | 상태 「표현」 줄 아래에 보완 안내 1줄 |
| `batch-03-final-note.md` | 이 메모(신규) |

기존 내용은 지우지 않았다. 예외는 taxonomy validation.md 의 「나머지 출현은 정규식 후보(auto, 문장 구간 포함)로 전수 보존했다」 한 문장이다. 이 문장은 정정 문장으로 바꿨고, 원래 문구는 정정 문장 안에 인용해 두었다.

**주의:** taxonomy·literature-evidence 의 `issues.md`·`review.md` 는 각 `build.py` 가 생성한다(taxonomy validation.md 는 아님, literature validation.md 는 수기). 이번 문구는 빌드 코드 밖에서 덧붙인 것이라 rebuild 하면 사라진다. 각 파일 안에도 이 점을 적었다. 이번 작업에서는 rebuild 하지 않았다.

## 2. 정정 전후 핵심

| 위치 | 전 | 후 |
|---|---|---|
| taxonomy validation.md 별도 읽기 검토 | 「나머지 출현은 정규식 후보로 전수 보존」 | auto 에는 `method.patterns` 단서와 일치한 출현만 남는다. 패턴 밖 단서는 표현 기록에서 빠졌다. 원문·Pointer·토큰은 보존돼 있지만 후속 탐색은 원문 문맥을 다시 읽어야 한다. 열린 과제다 |
| taxonomy validation.md 상태 표 | 형태소·표현 수집 「완료」 | 「완료(표현은 정규식 단서 공백 있음 — K-EXPR01)」 |
| literature issues.md K-ENG/K-ZHJA | zh/ja 수식·조건·부정을 「직접 읽기·수동 표현·영어 보조 정규식으로 수집」 | 그 문장은 영어 값에만 해당한다. zh/ja 는 원문 보존, 제한된 언어 간 차이 관찰(I-LANG·I-SCRIPT), 사례 표시용 수동 표현 zh 3 · ja 12 만 했다. zh/ja 보조 정규식은 없다. 전수 수집은 하지 않았다 |
| literature validation.md §4 | 미검토 = 의미 관계·외국어 형태소·서명 밖 토큰·문헌 대조 | zh/ja 표현 전수 수집과 한국어 「후·시」 조건 구절을 미검토에 추가했다 |

## 3. 기록한 한계 — 위치와 영향

### taxonomy K-EXPR01 (`first-pass/taxonomy/issues.md` 끝)

단서별 「출현 / 미덮임」. 수치는 리뷰 근거이며 정규식 단서 수치다(의미 전수 조사 아님).

- `자제` 334/298
- `깊` 180/77
- `얇` 6/3
- `서서히` 16/13 · `점진` 56/44
- `권장` 270/243 · `주의` 62/47 · `필요` 83/49
- `심각` 5/4
- `약 N` 23/10
- Pa·N 범위 미덮임 14 (재셈 13)
- `시 ` 360/270

**영향:** 표현 기록만 보고 회피·깊이·두께·속도·권고 강도·근사·물성 단위·조건을 탐색하면 이 출현이 빠진다. 후속 단계는 원문 문맥을 다시 읽어야 한다. 상태는 열림이다.

### taxonomy OBS-M16-PRODUCTS (같은 절)

- 위치: `/modality/15/products` (S049). 원문 값은 `[]`.
- 뜻은 미상이다. 「제품 없음」인지 「미수집」인지 원문이 밝히지 않는다.
- 다른 빈 products 6개와 같은 상태다. 빈 products 는 GLOBAL-B01 묶음에 들어 있지 않다는 점도 함께 적었다.

### literature K-ZHJA 정정 (`first-pass/literature-evidence/issues.md` K-ENG/K-ZHJA 절)

- 리뷰의 단서 정규식 결과: zh 70값 · ja 40값에 단서가 있고, 그중 표현이 있는 값은 2 · 6 이다.
- **영향:** `expressions.json` 만 쓰면 zh/ja 의 가능성·빈도·일시성·부정·조건이 빠진다. zh/ja 문장을 쓰려면 원문을 다시 읽어야 한다. 상태는 열림이다.

### literature K-KOCOND (같은 파일 끝, 7건 표)

7개 Pointer 마다 다음을 기록했다. 구간은 디코딩된 값 문자열의 코드포인트 `[start,end)` 이고, 원문에서 각 1회 일치했다.

- 리뷰 인용 구절의 구간
- 조건·시점 단서의 구간: `시술 후` · `시술 시` · `리프레싱 시`
- 기존 표현과의 겹침. 2건은 결과절만 manual 에 있다.
- 상태: 누락(열림)

**영향:** 발생 조건과 기준 시점이 표현 기록에 없다. 같은 원인으로 다른 값에도 누락이 있을 수 있다. 이 7건은 전수 목록이 아니다. `expressions.json` 에 추가하지 않았고 의미도 확정하지 않았다.

## 4. 기계 대조와 원문 읽기 구분

- **독립 기계 대조 — 전수:** 두 리뷰가 원문 ↔ 기록 대응을 전수 대조했고 실패는 0 이었다. 이번 워커는 그 대응을 다시 검사하지 않았다.
- **단서 재계산 — 읽기 전용 보조:** scratchpad 스크립트로 `source-map.json`·`expressions.json`·원본 JSON 을 읽기만 해서 리뷰 수치를 다시 셌다.
  - taxonomy 단서 11종: 리뷰와 같았다. 다만 Pa·N 은 13 으로 리뷰(14)와 달랐다.
  - literature 7개 구간: 계산했고 각 1회 일치했다.
  - zh/ja: 더 좁은 단서 집합으로 셌더니 40 · 30 값이었고, 표현이 있는 값은 2 · 6 으로 리뷰와 같았다.
  - 이 수치는 의미 판정이 아니다.
- **원문 읽기 — 표본:** 7개 값 전문, 그리고 taxonomy 미덮임 예시 각 1건의 앞뒤 문맥만 읽었다. 이 밖의 미덮임 출현은 읽지 않았다.

## 5. 검증 명령과 실제 수치

레포 루트에서 다섯 원장 모두 실행했다: `python3 orchestration/work/phub-ledger-redesign/first-pass/<원장>/verify.py`. 시작 전에 grep 으로 쓰기 호출이 없는지 확인했다. taxonomy·literature 는 `.md` 를 읽기만 하거나 존재만 확인한다.

| 원장 | EXIT | 수치 요약 |
|---|---|---|
| taxonomy | 0 | nodes 17593 · sections_read 53/53 · morph 10844/985 · tokens 98254 · expr auto 10974 / manual 1073 · issues B34 F47 I65 K4 · sha 시작=끝 `5492d0d4…f8fe` · failure_count 0 |
| literature-evidence | 0 | nodes 2137 · leaves 1726 · segments 18/18 · morph 137/1569 · tokens 3144 · expressions 771(manual 512) · issues 71 · sha 시작=끝 `6e179872…aebfd` · failure_count 0 |
| problem-packages | 0 | nodes 3656 · tokens 6708 · manual 871 · regex 1031 · issues 32 · checks 91851 · fails 0 · sha 시작=끝 |
| problem-combos | 0 | 132 checks · 0 failures · nodes 460 · leaves 370 |
| pih-risk | 0 | tokens 2083 · expressions 310 · regex 107 · check_count 11410 · failure_count 0 |

구조화 미결 수(K4, issues 71 등)는 그대로다. 이번 문서 기록은 JSON 에 넣지 않았기 때문이다.

## 6. 해시 대조

시작 전과 끝(verify 실행 뒤, 이 메모 작성 전)에 scratchpad 에 sha256 목록을 저장해 비교했다.

- 원본 `phub-recommend/bronze/phub-ledger/` 24 파일: diff 0, 불변.
- `phub-ledger-redesign/` 아래 681 파일: 바뀐 것은 §1 의 6개 `.md` 뿐이다. 다음은 모두 불변이다.
  - 모든 결과 JSON과 코드(`build.py`·`verify.py` 등)
  - 분할 문서(`review-part-*`)
  - 다른 3원장(problem-packages·problem-combos·pih-risk) 결과
  - 검토 보고서·스킬·`_RESUME.md`·발주 기록
- 파일 추가·삭제는 없었다(이 메모 제외).
- 해시가 같다는 것은 파일이 바뀌지 않았다는 뜻일 뿐이다. pih-risk A1 사고(`pkill -f cat`)가 외부 프로세스에 끼친 영향은 여전히 확인되지 않았다. 이번 작업은 프로세스 종료 명령을 쓰지 않았다.

## 7. 수정하지 않은 선택 권고 (후속)

- literature `S09-I2`(인용 제목 single-dot ultrasound ↔ statement HIFU)와 `S07-I3`(「실 모아넣기 시술」 ↔ Thread insertion 대응 불명)
  - 리뷰는 이 둘이 값끼리 모순이 아니라 「같은 대상인지 원문이 밝히지 않음」이라고 보고 I → F(또는 B) 재분류를 권고했다.
  - 분류는 바꾸지 않았다.
- pih-risk I3(`/notes/M17` 근거 강도 해석)
  - 리뷰는 I → P 또는 F 를 권고했다.
  - pih-risk 파일은 건드리지 않았다.
- 표현 후보 보강(K-EXPR01 단서 추가, zh/ja 단서, 한국어 「후·시」 조건)은 재추출과 rebuild 가 필요해 이번 범위 밖이다. 하게 되면 §1 주의처럼 문서 기록과 빌드 생성물을 맞추는 일이 함께 필요하다.

## 8. 상태

- B/I/F/K 는 모두 열려 있다.
  - taxonomy: B34 · I65 · F47 · K4 + 문서 기록 K-EXPR01 · OBS-M16-PRODUCTS
  - literature: B20 · I33 · F17 · K1+18규칙 + K-ZHJA 정정 · K-KOCOND
- 현재 사용자 선택은 0건이다. 두 리뷰의 근거를 유지한다: 원본 변경 후보는 F/I, 원문 부족은 B, 언어 기준·병합은 2단계에서 다룬다. 0건이라는 것이 미결이 없다는 뜻은 아니다.
- **기록 보완 반영, 코디 확인 전.**
