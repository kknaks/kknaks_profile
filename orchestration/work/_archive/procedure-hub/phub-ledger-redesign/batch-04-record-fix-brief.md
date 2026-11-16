# [writer] batch-04 최소 기록 보완

Opus 워커, 추가 에이전트 금지. 라이브 preamble의 정확한 ID·보고명령·outcome이 §9의 과거 양식보다 우선한다. worker_done 정확히 한 번 후 idle.

## 1. 읽을 것

AGENTS.md 및 적용 규칙, orchestration/work/phub-ledger-redesign/ledger-first-pass/SKILL.md, _RESUME.md, batch-04-review.md. 이하 상대경로는 orchestration/work/phub-ledger-redesign 기준. 원본은 ../phub-recommend/bronze/phub-ledger, 전부 읽기전용.

## 2. 대상/목표

독립검토의 R1/R2만 최소 보완. 1차 원장 재조사·형태소 재분석·외부검증·관계확정 금지.

## 3. checklist

first-pass/pre-procedure-checklist/morphology.json known_errors 및 각 record 내 known_errors 44출현에 디코딩 원문 값 기준 Unicode 코드포인트 span [start,end)을 추가한다. 표면형이 해당값에서 정확히1회인지 직접 검증하며 44/44 일치해야 한다. 원시토큰·값·Pointer·오류내용은 유지한다. 생성부(build.py 및 자기폴더 수동기록)도 다음 재생성에 span이 남도록 최소 수정하고 verify.py에 실제 span 재현·범위 검사를 추가한다. issues.md에도 각 출현 구간을 명시하고 validation.md에 실제 실행 결과를 남긴다. 기존값/토큰/표현 재분석은 하지 않는다. 전체 rebuild가 불필요하면 하지 말고, 하더라도 자기폴더 기존 모든 내용이 동일하고 span/해당문서/검증코드만 바뀌었는지 대조한다.

## 4. optimization

first-pass/treatment-optimization/issues.md 및 해당 생성 원천에 I-10-1·I-10-2·I-10-4 각각 비고를 추가한다(분류ID/집계는 유지). 리뷰 §2.5의 원문근거를 읽고 '양립 가능; 모순으로 확정하지 않음'과 구체적인 범위를 적는다. 14일이내 금지와4주권장은 별개 강도, 당일금지와최소4주는 포함관계, 동시금지와2주내금지는 포함관계. 남은 기준/범위/14일~4주 처리 등은 후속검토이며 원문밖 임상판단을 채우지 않는다. 이를 원문 모순 확정목록에 넣으면 안 된다고 적는다. 원문을 고치거나 임의 새관계를 적용하지 않는다. 기존나머지 I는 그대로 유지. 생성부·수동기록과 문서의 보완이 다음build에도 유지되도록 최소 수정한다.

## 5. 소유권

쓰기허용은 위 두 원장 결과폴더 내부의 보완에 필요한 morphology.json·issues.md·validation.md·build.py·verify.py·해당 수동기록·필요시 review 안내뿐이다. 새 batch-04-final-note.md 한 개. source-map/coverage/expressions의 값·구조·토큰 및 다른3개 원장·원본24파일·기존16개결과·스킬·검토보고서·_RESUME·발주JSON은 읽기전용. 삭제·다른경로 생성 금지. 커밋·push·PR·추가워커 금지. pkill/killall/패턴종료 금지. 임시는 자기 scratchpad만.

## 6. 검증

작업전 원본24파일·결과5폴더 해시 baseline을 scratchpad에 보관. verify5개 읽기전용으로 실행하고5/5오류0. checklist44/44 span재현과 구조화레코드↔전역 known_errors 동등성 검사. 원본24파일·다른3원장·비대상 JSON의 해시불변, checklist는 기존데이터와 추가span외 동일, optimization는 세항목 비고 외 기존데이터동일을 확인. 검증을 통과시키기 위해 의미나 원문을 바꾸지 않는다. 자동생성 문구를 수기로만 고쳐 소실시키지 않는다.

## 7. 보고

batch-04-final-note.md에 변경파일·44개실제검사·세항목정정·검증5개실제수치·해시/보완외동일·재생성보존근거·잔여한계를 적는다. R3 가격분모2축/기간표기차 분류와 patient-education 문장내 조건분해는 다음21개 비교시 검토권고로 유지하고 지금 재분류하지 않는다. timeline 경로위반은 기록된 사건이며 과거파일내용/피해없음을 단정하지 않는다. 상태는 '보완 반영·코디 확인 전', 원장전체 완료 아님·미결열림·현재사용자선택0(리뷰근거).

## 8. 범위

이번 두 기록보완만 수행하고 불필요한 포맷확대·반복검토·전면재조사를 하지 않는다. 3문장요약·보고서경로로 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_3a1dfb1a-f4de-478c-862b-87f953b66fea --from term_8c2999f2-0bca-4945-9d09-c5212852bdaa \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_3a1dfb1a-f4de-478c-862b-87f953b66fea \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_3a1dfb1a-f4de-478c-862b-87f953b66fea --text "[질문] researcher: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
