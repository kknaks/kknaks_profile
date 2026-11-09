# synergy.json — 검증 기록

**1차 수집 범위 종료: 예(작성자 판단, 코디 확인 전) · 원장 전체 완료 아님.** 열린 미결: 원문 부족 B 10묶음 · 잠정 P 5 · 후속 F 10묶음 · 원본 수정 관련 후속 검토 후보 U 2(U1 → F1 · U2 → 실버 변환 규칙, batch-01 검토 반영 재분류) · **현재 사용자 선택 대기 0**. 원본은 사용자 지시대로 보존. 집계는 [issues.md](./issues.md) 요약과 같다.

> 기계 검증 통과는 **원문 대응**(누락·중복·포인터·구간·해시·적용/제외)의 증거다. 의미 해석의 정답이나 정규화 완료를 뜻하지 않는다.

## 1. 실행 명령 (레포 루트)

```bash
# 빌드(형태소 분석 포함)
OMP_NUM_THREADS=1 uv run --python 3.12 --with kiwipiepy==0.24.1 \
  python orchestration/work/phub-ledger-redesign/first-pass/synergy/build.py

# 독립 검증(표준 라이브러리만, 파일 쓰기 없음, 실패 시 exit 1)
python3 orchestration/work/phub-ledger-redesign/first-pass/synergy/verify.py
```

## 2. 결과 (2026-11-09 마지막 실행)

`verify.py` → **exit 0, failure_count 0**

```json
{
 "source_sha256": "2c0fb244f6dc7f8521be355e83586bc7b6446979c041a51c77046bae1c3c653f",
 "nodes": 1039, "keys": 923, "string_values": 922,
 "analyzed": 690, "excluded": 232, "tokens": 4133,
 "segmentation_review": 391, "pos_review": 135,
 "expressions": 2631, "link_observations": 37,
 "self_test": {
  "node value altered": "detected", "token span altered": "detected",
  "analyzed value dropped": "detected", "expression span altered": "detected",
  "node dropped": "detected", "segmentation judgement dropped": "detected"
 },
 "failure_count": 0
}
```

`build.py` 출력은 [build-output.txt](./build-output.txt) (시작·끝 sha256 동일).

## 3. verify.py 가 실제로 확인하는 것

| # | 검사 | 방법 |
|---|---|---|
| 1 | 원본 해시 불변 | 시작·끝 sha256 == `2c0fb244…c653f`, 결과 JSON 4종에 기록된 시작·끝 해시·크기·코드포인트 수 일치 |
| 2 | 중복 키 | 표준 `json` 의 `object_pairs_hook` 으로 독립 감지 = 0, source-map 기록 = 0 |
| 3 | 구조 양방향 대응 | 원본을 독립 순회한 pointer 집합 == source-map 노드 pointer 집합(1,039), 노드 pointer 중복 0. 노드마다 자료형·부모·자식 키 순서·배열 길이·값 일치 |
| 4 | 구간 재현 | 노드 `span` 원문 slice 를 다시 파싱하면 해당 서브트리와 같음. `byte_span` 바이트 slice 디코딩 == 코드포인트 slice, 누적 UTF-8 길이와 일치. 문자열 `literal_span` slice == 값(이스케이프 0), 따옴표 바로 안쪽. 키 923개 `key_span`·`key_byte_span` 재현, 키 순서, value_pointer 중복 0, 필드명 출현 색인 합계 == 키 출현 수 |
| 5 | 형태소 적용/제외 대응 | 문자열 922 = 분석 690 ∪ 제외 232, 교집합 0. 모든 문자열이 정책 패턴에 걸리고 정책과 실제 처리가 같음. 제외 값은 원문과 같고 사유가 있으며 코드값 정규식(`^M\d+$`) 충족 |
| 6 | 토큰 | 분석 텍스트 == 원문, `file_span_of_text` 재현, 토큰 surface == 원문 slice, 순서·인덱스, `form_equals_surface` 플래그 정합, 길이 0 토큰은 `zero_length=true` 와 일치, **공백 아닌 모든 문자가 어떤 토큰에 덮임**(분석 탈락 0) |
| 7 | 필드명 | 분석한 필드명 집합 == 원본 고유 키 11, 토큰 surface 재현, 규칙 분해 재결합 == 원래 이름 |
| 8 | 구절 규칙 판정 | 규칙 26개 각각의 원문 출현 집합 == 판정된 출현 집합(빠짐 0), 구절 구간 재현, 참조 토큰이 실제 토큰과 같고 구간과 겹침 |
| 9 | 품사 판정 | 대상 품사(MAG·MAJ·MM·NR·NP·VCN·XPN·VX)의 모든 토큰 출현 == 판정 출현(135), 출현당 1회, 토큰 참조 일치 |
| 10 | 표현 | id 중복 0, (pointer·span·범주·방법) 중복 0, 모든 span 이 원문 slice 재현, 분석 값마다 `segment.value` 1개, manual 82건 전부 반영, 오탐 표시 12건 == expression-review 기록 |
| 11 | link 관찰 | 모든 pointer(패턴 포함)가 원본에 존재, 모든 quote 가 해당 pointer 아래 원문 값의 부분문자열 |
| 12 | review.md | 115 link 각각의 7필드 행과 reason 행이 원문 값과 정확히 같음(230행, 중복 0), 원본 컬럼명 헤더 4구획 |
| 13 | 변이 시험 | 메모리 안에서 노드 값 변경·토큰 구간 변경·분석 값 삭제·표현 구간 변경·노드 삭제·구절 판정 삭제 6종을 만들어 각각 검출됨을 확인(파일 쓰기 없음) |

## 4. 추가 확인 (명령 · 결과)

| 확인 | 명령 요지 | 결과 |
|---|---|---|
| 재현성 | build 결과 JSON·review.md 의 sha256 을 저장 → build 재실행 → 비교 | 전부 동일(`REPRO_SAME`) |
| verify 무쓰기 | verify 전후 폴더 `ls -l -T` 비교 | 차이 없음(`VERIFY_WROTE_NOTHING`) |
| 원본 무변경 | `shasum -a 256 …/synergy.json` · `git status --porcelain` | 해시 동일, `phub-recommend/` 변경 없음 |
| 부정·조건·한정·근거 표지의 문맥 보존 | 분석 값 전체에서 `않|불가|아니|아닌|제한적|수 있|에 따라|한해|한정|해당 시|때는|입증|소지` 출현마다 그것을 감싸는 manual 절이 있는지 | 누락 0 |
| 미포착 어절 | regex·keyword·manual 후보(오탐 제외)에 덮이지 않은 reason·timing·target 어절 214종 목록 열람 | 대안 접속·상태 수식·출처 수식·비교·「실」 누락 발견 → 범주 5개 추가(issues A5). 남은 미포착은 효과·결과 어휘·행위 동사로, 문장·기호 분할 구간과 manual 절로 문맥 보존 |
| 후보 오탐 | 순서·조건·부정·가능성·정도·부위·선택 기준·수량 후보를 범주별로 문맥과 함께 전부 열람 | 오탐 12건 표시(issues A4) |

## 5. 별도 읽기 검토 (같은 작성자, 관점 바꿔 다시 읽음 — 독립 검토 아님)

| 관점 | 확인한 것 | 결과 |
|---|---|---|
| 수식·정도 | 「극대화·배가·오래·빠름·점차·과도한·선택적으로·깊이」가 무엇을 수식하는지 문장 안에서 | 대상(효과·회복·근육·전달)은 문장 안에 있음. 시간 기준·수치는 원문에 없음(B7). 수치로 바꾸지 않음 |
| 조건·한정 | `/64` 의 SVF 한정·불가·해당 시, `/96` 조합할 때는, `/5` 근육만 | manual condition_scope·negation_scope 로 절 단위 보존. timing 칸 안 조건은 LO13 |
| 부정 | `/14` `/27` `/59` `/76` `/84` `/87` `/101` | 부정 범위(허가 제제가 아닌 것, 화장품 전달·주입, 재발 방지 효과, 단순 예산 택1)를 절로 보존. link 라벨과의 긴장은 LO09–LO11 |
| 가능성·근거 | 제한적·소지·고려할 수 있으나·보조할 수 있으나·입증되지 않았으며 | hedge_evidence·regulatory_statement 로 보존. 근거 출처 없음(B8) |
| 범위·대안 | 1~2주·2~3개월·같은 날 또는 2주·직후 또는 1주 후·둘 다·모두 | quantity_time·time_range·time_alternative·condition_scope 로 보존 |
| 방향·순서 | 다음에 49건의 timing 문장 순서와 from→to | 1건 반대(`/54`), 양방향 3쌍, 총칭/개별 순서 충돌(LO01–LO05) |
| 오분절 영향 | 위 구절의 형태소가 사라지거나 허위로 생기는 곳 | 써마지→말다(허위 부정), 실로/MAG(허위 부사·수단 소실), 자가 소실, 전달 소실, 열/NR·CO2·코드 숫자(수량 오탐), 동안(동형어) — 출현별 표시 |

검토하지 않은 것: 의미 관계(방향의 정답, type 라벨의 뜻, 명칭 동일성·상하, 시술×부위)의 확정, 다른 원장(taxonomy)과의 이름 대조, 임상·법적 사실 여부.

## 6. 한계

- 형태소: 구절 규칙 26·품사 서명 31 밖의 토큰 정확성(NNP/NNG, VA/VV, 기타 명사 분절)은 출현별로 판정하지 않았다.
- 표현 범주: regex·keyword·수동 목록 결과이며 전수 의미 해석이 아니다. 효과·결과 어휘에는 별도 범주가 없다.
- 읽기 검토: 같은 에이전트의 재독이다. 독립 검토는 코디 판단에 맡긴다.
- 이후 batch-01 독립 묶음 검토(`../../batch-01-review.md` §3.5)가 WARN(분류만, 1차 종료를 막지 않음)으로 판정했다. 지적에 따라 U1·U2 를 후속 검토 후보로 재분류하고 `/links/55/reason` [35,37) 「전층」 미표시 분절을 issues A' 에 알려진 한계로 적었다. 토큰·JSON 은 바꾸지 않았다.
