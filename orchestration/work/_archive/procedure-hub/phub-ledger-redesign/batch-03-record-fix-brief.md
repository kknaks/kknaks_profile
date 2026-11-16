# [writer] batch-03 검토 후 기록 보완

라이브 dispatch preamble의 보고 인자·정확한 ID·outcome 요구가 §9의 과거 양식보다 우선한다. 완료는 정확히 한 번 보고하고 idle한다. 추가 워커 금지.

## 1. 읽을 것

AGENTS.md 및 적용 규칙, orchestration/work/phub-ledger-redesign/ledger-first-pass/SKILL.md, _RESUME.md, batch-03-review-taxonomy.md, batch-03-review-others.md. 이하 상대 파일은 orchestration/work/phub-ledger-redesign/ 기준이다. 너는 이전 워커의 맥락이 없다. 두 리뷰의 근거를 대상 문서 및 실제 기록과 대조하라.

## 2. 목적

batch-03의 비차단 기록 보완만 수행한다. 수식 표현 후보와 다국어 표현 수집을 전수 수행했다고 과장한 문구를 정정하고, 확인된 미수집 범위·위치·후속 영향을 남긴다. 원장 전체 완료·의미 정답·모든 표현 수집 완료를 주장하지 않는다. 원문 보존만으로 미결을 해결했다고 처리하지 않는다.

## 3. taxonomy 보완

- 검토 §3-1의 후보 패턴 공백을 issues.md의 K 한계로 기록: 자제, 깊이, 얇, 서서히/점진, 권장/주의/필요, 심각, 약N, Pa/N 수치, 시 공백 등의 실제 관측 수와 미덮임 수를 리뷰 근거대로 옮긴다. 정규식 단서 수치이고 의미 전수 조사 결과가 아님을 명시한다. 기존 수동1073/자동10974 표현과 모든 원문 보존의 차이를 명확히 한다.
- validation.md의 '나머지 출현은 정규식 후보로 전수 보존' 등 동등한 과장 문구를 실제 범위로 정정한다. 표현 후보 목록만으로 후속 탐색하면 빠지므로 원문 문맥을 재검토해야 한다는 영향과 열린 후속 과제를 명시한다. 누락 후보를 의미적으로 해결/교정한 것으로 쓰지 않는다.
- M16 /modality/15/products 빈 배열은 source-map에 이미 있다. issues 또는 review.md의 별도 관찰에 위치/원문[]/뜻 미상을 기록한다.
- 한계 추가에 따른 Markdown 집계 표시가 필요하면 기존 구조화 미결 K4와 이번 추가 기록을 구분하라. JSON을 바꾸지 않고 정합을 유지한다.

## 4. literature-evidence 보완

- issues.md K-ENG/K-ZHJA 범위를 정정한다. zh/ja는 원문 보존 및 제한된 언어차 관찰이며 수식·조건·부정 표현 전수 수집을 하지 않았다. 실제 수동 zh3/ja12, zh/ja 보조 정규식 없음, 리뷰의 단서 검출 범위와 한계를 명시한다. 후속에서 expressions.json만 쓰면 가능성·빈도·일시성 등이 빠질 수 있어 원문 재독 필요.
- 리뷰 §2.1②의 한국어 조건/시점 구절 7건을 Pointer·실제 구절·가능하면 디코딩 문자열 코드포인트 [start,end)·누락 상태·후속 영향으로 한계에 기록한다. 위치 계산은 기계 보조로 가능하나 의미를 임의 확정하지 않는다. expressions.json에 추가된 것으로 표시하지 않는다.
- validation.md/review.md에 동등한 과장 문구가 있으면 허용된 파일 안에서 최소한으로 정정한다.
- 선택적 재분류(S09-I2/S07-I3, pih I3)는 이번에 실제 분류를 바꾸지 않고 최종 메모에 후속 권고로 남긴다. pih 파일은 수정하지 않는다.

## 5. 소유권 allowed_paths

수정 허용: first-pass/taxonomy/issues.md, validation.md, review.md; first-pass/literature-evidence/issues.md, validation.md, review.md. 새 보고서 batch-03-final-note.md 한 개. 이 경로 외 파일은 읽기 전용이다. _RESUME.md·발주기록은 코디 소유. 원본24파일·기존11개결과·이번 추출 JSON/코드·분할문서·다른3원장·검토보고서·스킬 수정/삭제 금지. 새 후보 재추출·rebuild·원본 재조사·임상/법률 외부조회·커밋·push·PR 금지. 이번 보완 문구 외 기존 내용을 지우거나 덮어쓰지 말라.

## 6. 검증

시작 전 원본24파일과 batch-03 결과 전체의 SHA256 목록을 scratchpad에 보관한다. 대상 verify.py를 읽기 전용인지 확인한 뒤5개 모두 재실행한다. 출력은 수치 요약만. 종료 시 원본24파일 및 JSON/코드/다른3원장/분할문서 해시 불변과 변경 파일이 allowed_paths 안인지 확인한다. 재생성하지 않는다. 문서 정정이 verify를 깨면 원인을 보고하고 임의 데이터 변경하지 않는다.

## 7. 보고서

batch-03-final-note.md에 변경파일·정정 전후 핵심·한계 위치/영향·검증 명령과 실제수치·해시대조·수정하지 않은 선택권고를 명시한다. 독립 기계대조 전수와 원문 읽기 표본을 구분한다. B/I/F/K는 열린 상태이며 현재 사용자 선택0은 검토 근거와 함께 유지하되 전체 완료라고 하지 않는다. '기록 보완 반영, 코디 확인 전' 상태로 마친다.

## 8. 운영

pkill/killall·프로세스명 패턴 종료 금지. 자신이 시작한 정확PID/세션만 제어한다. pih-risk 사고의 외부 프로세스 영향 미확인 상태를 유지하며, 해시 검증 통과를 피해없음으로 확대하지 않는다. 작업은 작게 끝내고 불필요한 새 포맷/미세 교정 반복을 만들지 않는다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_9817d7e4-b067-40b3-9235-c8dcddad8f26 --from term_8c2999f2-0bca-4945-9d09-c5212852bdaa \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_9817d7e4-b067-40b3-9235-c8dcddad8f26 \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_9817d7e4-b067-40b3-9235-c8dcddad8f26 --text "[질문] researcher: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
