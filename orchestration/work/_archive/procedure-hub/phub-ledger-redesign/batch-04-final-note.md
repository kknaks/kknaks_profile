# batch-04 최소 기록 보완 — 마감 노트

- 작업: writer 워커(Opus) · `task_a12ed7a25f37` / `ctx_88ab611e8300` · 2026-11-09
- 근거: [독립 검토](./batch-04-review.md) §2.4(R1)·§2.5(R2), [보완 브리프](./batch-04-record-fix-brief.md)
- **상태: 보완 반영 · 코디 확인 전.** 원장 전체 완료 아님 — 다섯 원장 모두 B·I·P·F·K 미결이 열려 있다. 현재 사용자 선택 0건(검토 §4 근거 그대로).
- 범위: R1·R2 기록 보완만 했다. 1차 원장 재조사·형태소 재분석·외부 검증·관계 확정은 하지 않았다. 커밋·push·PR 없음.

## 1. 변경 파일

| 원장 | 파일 | 무엇이 바뀌었나 |
|---|---|---|
| pre-procedure-checklist | `manual/segment-notes.json` | `morph_known_errors` 44출현에 `span` 추가(각 4줄 추가, 그 밖 동일) |
| | `build.py` | span 재현·1회 확인(실패 시 중단) · issues.md K 목록에 `[start,end)` 출력 |
| | `verify.py` | span 형식·범위·재현(기록값·독립 원본 양쪽)·표면형 1회 · 레코드별↔전역 known_errors 동등 검사 |
| | `morphology.json` | 전역·레코드별 `known_errors` 에 `span` (build 산출물) |
| | `issues.md` | K-형태소 오분절 44줄에 구간 표기 + 구간 정의 1줄 (build 산출물) |
| | `validation.md` | §5 실행 결과 추가 |
| treatment-optimization | `manual/seg-10.json` | I-10-1·I-10-2·I-10-4 에 `note` 추가(그 밖 동일) |
| | `build.py` | `write_issues` 가 `note` 를 `  - 비고:` 줄로 출력 |
| | `verify.py` | `issues.all_recorded` 가 manual note 의 issues.md 반영도 확인 |
| | `issues.md` | 세 항목에 비고 1줄씩 (build 산출물) |
| | `validation.md` | §5 실행 결과 추가 |
| (작업 폴더) | `batch-04-final-note.md` | 이 노트(신규) |

source-map·coverage·expressions, 다른 세 원장, 원본 24파일, 스킬·검토 보고서·_RESUME·발주 JSON 은 건드리지 않았다.

## 2. checklist — 오분절 구간 44건 실제 검사

- span 정의: 해당 Pointer 의 **디코딩된 값 문자열 안 Unicode 코드포인트 [start,end)**.
- 원본 값을 직접 읽어 표면형 출현 수를 셌다 → **44/44 정확히 1회**. 그 위치로 span 을 정했다.
- `값[start:end] == 표면형` **44/44**(morphology 기록 text 와 독립 순회한 원본 값 양쪽).
- 전역 `known_errors` 44 = 레코드별 `known_errors` 합 44, 내용 동일(포인터별 순서까지).
- 원시 토큰·값·Pointer·영향 문구는 그대로다. 재분석 없음.

## 3. optimization — 세 항목 비고

분류 I·ID·집계(I 12)는 유지. 세 항목 모두 「양립 가능; 모순으로 확정하지 않음」이고 원문 모순 확정 목록에 넣지 않는다고 적었다.

| ID | 관계 | 후속 검토로 남긴 것 |
|---|---|---|
| I-10-1 | 「14일 이내 RF/HIFU 금지·위험」(금지 하한)과 「필러 후 HIFU 4주 이상 간격 권장」(권장 간격)은 강도가 다른 별개 진술 | 14일~4주 구간 처리, 간격 기준 시점, RF 포함 범위(4주 문장은 HIFU 만 명시) |
| I-10-2 | rule 「당일 필러 금지」 ⊂ detail 「최소 4주 간격」 — 포함 관계 | 금지 범위가 당일인지 4주인지(제목·상세 범위 차), 기준 시점 |
| I-10-4 | 「동시 금지」 ⊂ 「2주 내 동일 부위 금지」 — 포함 관계 | 「동시」 범위, 2주 이후 처리, 「제모 부위」·「동일 부위」가 같은 범위인지 |

원문 밖 임상 판단은 채우지 않았다. 원문을 고치거나 새 관계를 적용하지 않았다. 나머지 I(I-10-3·I-05-1·I-03-1·I-04-1·I-06-1·I-07-1·I-11-1·I-12-1)는 그대로다.

## 4. 검증 (실제 실행값)

| 원장 | `python3 first-pass/<원장>/verify.py` |
|---|---|
| market-pricing | checks=11930 failures=0 · EXIT 0 (변경 없음) |
| patient-education | checks=34232 failures=0 · EXIT 0 (변경 없음) |
| post-procedure-timeline | checks=27804 failures=0 · EXIT 0 (변경 없음) |
| pre-procedure-checklist | checks=15083 failures=0 · EXIT 0 (보완 전 14,697) |
| treatment-optimization | checks=140 failures=0 · EXIT 0 |

**5/5 오류 0.**

변이 시험(스크래치 복사본): checklist 전역 span start+1·범위 밖·span 삭제·레코드별 span 만 변조 → 모두 exit 1, 수동 기록 span 변조 후 build → 중단. optimization 비고 변조 → exit 1, 복원 → exit 0.

## 5. 해시 · 보완 외 동일

- 작업 전 원본 24파일 + `phub-ledger-redesign/` 전체(909파일) sha256 baseline 을 스크래치에 두고 작업 뒤 대조했다.
- 바뀐 파일은 §1 표의 11개(그중 validation.md 2개는 해시 대조 뒤 추가)와 이 노트뿐이다. 원본 24파일·다른 세 원장(market-pricing·patient-education·post-procedure-timeline)·그 밖 모든 결과 파일 해시 불변.
- checklist: `morphology.json` 에서 span 키를 빼면 기존과 동일. `issues.md` 는 K 목록 44줄 + 정의 2줄(설명·빈 줄) 외 동일. 나머지 생성물(source-map·coverage·expressions·review*·progress) 바이트 동일.
- optimization: `issues.md` 는 비고 3줄 추가 외 동일. 나머지 생성물 바이트 동일.

## 6. 재생성 보존 근거

- 보완은 생성 원천(수동 기록 `manual/…json`)에 넣었고 build.py 가 그것을 산출물로 옮긴다. 산출물을 손으로만 고치지 않았다.
- 스크래치 복사본(같은 상대 경로 + 원본)에서 `uv run --python 3.12 --with kiwipiepy==0.24.1` 로 build.py 를 돌렸다.
  - 보완 전: 두 원장 모두 기존 산출물과 바이트 동일(checklist 14개 · optimization 13개).
  - 보완 후: 재생성 산출물을 실제 폴더에 그대로 복사했다 — 지금 폴더의 생성물 = 다음 build 결과.
- validation.md 는 두 원장 모두 build 가 쓰지 않는 수기 문서라 재생성에 지워지지 않는다.

## 7. 잔여 한계 · 유지 사항

- R3(market-pricing 가격 분모 2축 · timeline 기간 표기 차 분류)와 patient-education 문장 안 조건 분해는 **다음 21개 비교 때 검토 권고로 유지**한다. 지금 재분류하지 않았다.
- post-procedure-timeline 경로 위반은 기록된 사건이다. 그때 과거 파일 내용이 어땠는지·피해가 없었는지는 단정하지 않는다.
- optimization 세 항목의 범위 문제(14일~4주, 당일 vs 4주, 동시 범위)는 후속 의미 조사 몫이다.
- span 은 값 기준 코드포인트만 넣었다. 파일 전체 기준 구간은 morphology 레코드의 `value_cp_in_file` 시작점을 더하면 나온다(이 원본은 이스케이프 0).
