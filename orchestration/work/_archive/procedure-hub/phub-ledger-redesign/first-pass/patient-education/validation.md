# validation — patient-education.json 1차 조사

**1차 수집 범위 종료 · 원장 전체 완료 아님.** 기계 검증 통과는 원문 대응이 맞다는 뜻이다. 의미 해석의 정답이나 정규화 완료를 뜻하지 않는다.

## 재현 명령 (레포 루트)

```bash
uv run --python 3.12 --with kiwipiepy==0.24.1 python orchestration/work/phub-ledger-redesign/first-pass/patient-education/build.py
python3 orchestration/work/phub-ledger-redesign/first-pass/patient-education/verify.py
```

`verify.py` 는 표준 라이브러리만 쓴다. build.py·pe_common.py 를 import 하지 않고 원본을 `json` 모듈로 따로 열거한다. 원본과 결과 파일을 읽기만 하고 아무 파일도 쓰지 않는다. 실패가 하나라도 있으면 exit 1.

## 마지막 실행 결과 (2026-11-09)

```text
source_sha256 start=6c96520c514b76ef7f93d7f685e53023afe91b05133a9b9ca5db0a95d42d91ac end=6c96520c514b76ef7f93d7f685e53023afe91b05133a9b9ca5db0a95d42d91ac
nodes=327 leaf=240 strings=240 segments=18 applied=221 excluded=19 tokens=4989 expressions=806 regex=572 known_missegmentation=25 observations=90
checks=34232 failures=0
EXIT 0
```

- build.py 를 두 번 연속 실행해 생성물 26개(json·md, validation.md·progress.md 제외)의 sha256 이 같음을 확인했다(재현성).
- 원본 sha256 은 작업 시작 시점, 각 build·verify 실행 전후, 마감 시점에 모두 `6c96520c…d42d91ac` 로 같다. `git status` 에서 원본 경로 변경 없음.

## verify.py 가 검사하는 것

| 영역 | 검사 |
|---|---|
| 원본 | 시작·끝 sha256 이 기대값과 같음 · 중복 키 0(`object_pairs_hook`) |
| source-map | Pointer 집합 양방향 일치·중복 없음·문서(배열) 순서 일치 · 노드마다 자료형·값·자식 수·빈 컨테이너 표시 · `literal_cp` 구간을 `json.loads` 해 원문 하위 트리와 같음 · `value_cp` 구간 = 디코딩 값 · 바이트 구간 = 코드포인트 구간 · 키 리터럴 구간 = 키 · 이스케이프 표시 |
| coverage | 전체 Pointer·말단 목록이 원문과 같음 · 구획 소유 합집합 = 원문 전체(양방향)·구획 간 중복 0 · 소유 규칙(/categories/i → S(i+1)) 독립 재계산 · 구획마다 direct_read·machine_extracted·마지막 읽은 Pointer 가 구획 안·review 파일·수동 기록 실재 · 공동 참조는 소유가 아님 · coverage ↔ manual 읽기 상태 일치 |
| morphology | 분석기 이름·버전·모델·스레드 기록 · 적용 ∪ 제외 = 문자열 값 전체(중복 없음) · 제외는 version·updated·id 만, 사유 있음 · 토큰마다 surface = 원문 구간, file_cp 재현 · **원문의 비공백 문자가 모두 어떤 토큰 구간에 들어감** · 필드명 기록 = 원문 키 집합 · 알려진 오분절 기록의 구간과 관찰 분석이 원시 토큰과 일치 |
| expressions | 표현마다 원문 구간·file_cp·file_byte 재현 · (Pointer, 구간) 중복 생성 0 · 구획 일치 · facet 이 정의된 어휘 안 · **모든 언어 값에 직접 읽기 표현이 있고, 값의 비공백 문자가 모두 어떤 표현 안에 있음(문장 탈락 검사)** · 정규식 후보 구간 재현·모든 후보가 수동 기록 안·수동 구절 밖 후보는 판정 있음 |
| 문서 | issues.md 에 모든 관찰 ID·오분절 K 행 · review.md 목차에 모든 구획 · review-part 에 소유 Pointer 행 전부, 원문 값 JSON 리터럴·원본 컬럼명 일치, 그 구획 표현 ID·관찰 ID 전부 · 컬럼 구성 표에 모든 경로 패턴 |
| 변이 시험 | 메모리 안에서 구획 소유 1개 삭제·구획 간 중복 추가·표현 구간 1칸 이동을 만들어 검사가 잡는지 확인 |

## 검증이 실제로 잡은 것 (작업 중)

- 문장 탈락 검사가 `/categories/0/common_concerns/2/a` 의 쉼표 두 개를 잡았다 → 「가벼운 활동은 … 안전합니다.」「최근 연구는 … 위한 것입니다.」 두 문장이 절 단위로만 기록돼 문장 전체가 빠져 있었다. 문장 기록을 추가하고 재검증했다(A 해소).
- 보조 정규식 대조: 수동 구절 밖 후보 129건 → 실제 누락 구절 49건 보충 → 남은 49건을 직접 판정(문장 단위 보존 43·오탐 6: 「다시」「수축하면서」「재생되면서」「레이저 중 뭐가」「없애는」「따라서」). 판정 근거 `manual/regex-review.json`.

## 별도 읽기 검토 (작성자 2차 읽기 — 독립 검토자 아님)

- 방법: 형태소 원시 출력에서 수식·부정·조건 신호(MAG·MM·MAJ·XPN·VA 계열·XR, VX 않/말, EC 면/으면/더라도/지만/나, NNB·NNG 후/시/중/정도/일부/필요 등)를 모두 뽑아 문장 아닌 구절 기록에 들어갔는지 대조했다. 141건이 걸렸다. 질문형 단문·지시어(이·그)·「다르다」류 비교 서술은 문장 기록으로 충분하다고 판정했다. 「원래 있는」「다만」(단서·예외 도입 6곳)「오래 유지됩니다」「일부 흡수가」「실제로는」「정상적인 과정」「직접 혈관으로」 등 27구절을 보충했다.
- 이 대조에서 새 오태깅 1건을 찾았다: M12 「바른 약물」의 바르다(도포)가 VA(옳다)로 태깅됨 → K 기록.
- 직접 확인한 의미 영향: 「드물게」(M16)는 중증 피부반응에만 붙은 것으로 읽힘(잠정) · 「~에만」(M1)·「일부 고출력 시술」(M9)·「히알루론산 필러는」(M2) 같은 한정이 구절에 보존됨 · 금기 강도 차이(M10 「시술 대상이 아닙니다」 vs 「알려주세요」, M4 「금기에 해당할 수 있으므로」) 보존 · 시간 역할(발현·지속·소실·복귀·최대 효과)을 메모로 구분.
- 미검토: 의미 관계·수식 대상의 최종 확정·임상 사실 여부. 이 목록 밖 형태소 토큰의 정답 여부.

## 한계

- 정규식 후보는 실제 패턴 일치분뿐이다. 패턴 밖 표현은 직접 읽기·형태소 수식어 대조로 수집했으나 그것도 사람 판단이며 전수 정답을 보장하지 않는다.
- 형태소 출력은 교정하지 않았다. 알려진 오분절·오태깅 25출현은 위치·영향을 기록했다(issues.md K). 품사 흔들림은 출현별이 아니라 한계 문장으로 기록했다.
- 독립 검토자 검토는 받지 않았다(코디 판단 사항).
