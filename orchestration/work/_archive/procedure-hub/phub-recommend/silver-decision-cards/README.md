# 문제와 근거를 보고 결정하기 — v2

[index.html](index.html)을 직접 여세요. 같은 링크의 내용이 v2로 교체됐습니다. 브라우저에 옛 화면이 남으면 새로고침하세요. 단일 HTML로 오프라인에서 동작합니다.

이전 v1은 152개 미부착 필드를 각각 결정할 문제처럼 제시했고, 복수 연결과 미확정 후보·이관 범위 제외를 충분히 설명하지 못했습니다. 그 화면은 폐기했습니다. `cards.json`은 고정 후보판의 원문/추적 자료로 유지하지만, 그 파일의 기존 question/recommendation 문구는 현재 사용자 화면의 판단 안내로 사용하지 않습니다.

## 현재 화면

26개 검토 주제를 담았습니다. 같은 원문이 문맥과 연결 규칙 양쪽에서 검토될 수 있습니다. 중복을 제외하면 원문 62행 / 152필드를 그대로 포함합니다. 전체 데이터 품질 조사에서 모든 문제가 이 26건으로 확정됐다는 뜻은 아닙니다.

- 원문 문맥 확인 4건: 다한증·주름·목주름/턱선의 교근 문구, PLLA 실리프팅 행의 주입/비가교HA 문구. **의학적 오류 확정이 아니라 문장과 원문 범위를 구체적으로 대조할 대상**입니다.
- 복수 연결 규칙 1건: 5행 / 17필드. 기존 units와 각 시술의 같은 ledger source ID를 대조했습니다. 여러 연결을 갖는다는 이유만으로 하나의 시술을 고르라고 하지 않습니다. 연결 보존과 문장별 임상 적용 승인은 다릅니다.
- 스킨보톡스 연결 근거 1건: 기존 실버에는 U5-009가 적혀 있으나 해당 시술 sources에는 M4-P-3가 없습니다. 기존 basis에 명시된 결정 문서를 추적할 대상입니다.
- 기존부터 후보였던 관계 19건: 원문 이름/detail과 실제 후보를 각 카드에서 제시합니다. 후보가 많다는 이유만으로 오류라고 하지 않습니다.
- 이관 범위 1건: 37행 / 83필드는 한 번에 묶었습니다. 기존 원문 보관 분류를 제시하고 후속 이관 포함 여부를 묻습니다. 품질 오류로 단정하지 않습니다.

각 카드에는 문제 → 확인한 사실 → 아직 모르는 것 → 적용 시 예상 영향 → 처리안 → 결정할 것과 선택의 결과가 있습니다. 원문 내용과 기존 연결은 펼쳐서 볼 수 있고, 위치·기술 ID·매핑 근거는 그 아래에 있습니다. 예상 영향은 현재 서비스에서 재현한 답변 오류로 표기하지 않습니다.

## 선택·저장

선택은 **후속 조사나 수정 방향**입니다. 의학적 사실·임상 적용·정본 전환을 승인하는 기능이 아닙니다. 자동 기본 선택은 없습니다. 메모만 남기는 것도 가능합니다. 데이터 적용 기능은 없습니다.

‘처리 방향 JSON 저장’으로 파일을 받습니다. 브라우저 임시 저장은 편의 기능입니다. 같은 v2 검토판의 JSON을 불러올 수 있습니다. 검토판 지문·후보판 지문·주제·원문 필드 참조·선택·시각이 맞지 않거나 기존 선택/메모와 충돌하면 거부합니다. v1의 질문과 선택 의미가 달라졌으므로 **v1 JSON을 v2로 자동 변환하지 않습니다.** 기존 v1 브라우저 저장 내용은 지우지 않습니다.

## 파일과 검증

- `index.html`: 현재 사용자용 v2 화면.
- `review.json`, `build-review.py`, `review-template.html`: v2 설명/추적 자료와 생성기.
- `cards.json`: 기존 후보판의 원문/claim/scope/대상/출처 추적 자료. 옛 권고 문구는 현재 화면에서 사용하지 않음.
- `verify.py`: 원문 값·파일·포인터·후보판·매핑을 대조하고 HTML의 실제 내장 데이터 검증.
- `verify-review.py`: 26주제와 62행/152필드 보존, 5행 복수 연결 근거, 스킨보톡스 근거 단절, 원문 문구, 후보판 불변 검증.
- `review-browser-test.cjs`: 실제 Chromium에서 설명 표시·선택·재접속·JSON 다운로드/불러오기·잘못된 가져오기 거부·필터·모바일 확인.
- `results/review-desktop.png`, `review-mobile-evidence.png`, `review-ui-validation.json`: 현재 화면 검증 결과.
- `results/review-test-export.json` 및 기존 `results/ui-export.json`: **자동 테스트 자료. 사용자 결정이 아니며 적용하면 안 됩니다.**

레포 루트에서 재생성 및 확인:

```sh
python3 orchestration/work/phub-recommend/silver-decision-cards/build-review.py
python3 orchestration/work/phub-recommend/silver-decision-cards/verify.py
python3 orchestration/work/phub-recommend/silver-decision-cards/verify-review.py
node orchestration/work/phub-recommend/silver-decision-cards/review-browser-test.cjs
```

`build.py`도 마지막에 v2 생성기를 실행하므로 다시 실행해도 옛 화면으로 돌아가지 않습니다. 옛 `template.html`·`decision-schema.json`·`browser-test.cjs`·`schema-test.cjs`는 v1 기록이며 현재 화면의 사용법/검증기로 삼지 않습니다.

고정 후보판은 기존 P5 검수에서 검증기 결함으로 미승인된 판입니다. 별도 검증기 보완 작업과 이 화면의 사용자 선택은 구분합니다. 본 작업은 후보판 payload/manifest나 원본 파일을 바꾸지 않았습니다. 실제 반영은 사용자의 처리 방향을 확인한 뒤 원문 근거·적용 범위·새 후보판 검증을 갖춘 별도 작업으로 수행해야 합니다.

## 최신 검증기 상태

2026-11-03 추가 [독립 폐쇄 검수](../silver-batch1-validator-closeout-review/report.md)는 BR-H1/BR-M1을 PASS 판정했습니다. 최초 P5 FAIL 보고와 고정 후보판 메타데이터는 과거 증거로 유지합니다. 검증기 두 결함의 폐쇄이며 이 화면의 문맥/관계 의미나 의학적 정확성·정본 전환 승인은 아닙니다. 검토판 fingerprint와 사용자 선택은 바꾸지 않았습니다.
