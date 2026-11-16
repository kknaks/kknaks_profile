# [reviewer_doc] 통키 품질 개선 — SPEC 0.8.1 재검수 (앞 판 WARN 6 처분 확인)

너는 **interpret-pwa `reviewer_doc` 워커**다. 앞 판(0.8.0 검수 · WARN 6)을 네가 했다 — 맥락이 없으면 아래부터 읽어라. **read-only** — 리포트 1개만.
작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토` · ⚠ PUBLIC

## 1. 읽을 것

- 앞 리포트: `orchestration/work/interpreter-idea/review-quality-doc-report.md`
- 수정 발주: `orchestration/work/interpreter-idea/quality-spec-fix1-brief.md` §2 표(코디 처분)
- planner 보고: `orchestration/work/interpreter-idea/quality-spec-report.md` 끝 「0.8.1 보완」 절
- DEC 새 행 **D-49 · D-50** · 고친 **D-47** · 앞 판 참고 1 처분(BASE · DEC 의 기록 문장 조각을 서술로 바꿈 — 코디)

## 2. 볼 것

1. W-1 ~ W-6 이 처분대로 닫혔나(각각 `파일:줄`)
2. D-49 문안 S1 ~ S4 가 D-45 · D-49 밖 내용을 담지 않았나 · §4.6 수치(424 · 439자 · zh-Hant 33 → 44 · th 여유 100)를 코드로 다시 세어 맞나
3. D-50 21문장(T34 ~ T54) 정의가 §9.3 · WORK 와 맞나 · 문장 자체를 SPEC 에 짓지 않았나(조건만)
4. 수정하면서 새로 생긴 어긋남 · 근거 없는 정책 0
5. public — 시험 목록 · 통역 기록 문장 0 · 키 · 실명 0. **BASE · DEC 도 이번엔 같이 본다**(참고 1 처분 확인)

## 3. 산출

- 리포트: `orchestration/work/interpreter-idea/review-quality-doc-report-2.md` — 판정 PASS / WARN / FAIL · 지적마다 `파일:줄` + 근거

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_d181fbae-29f2-43bb-9a41-6bc888ca07de --from term_9bf4f5be-03de-42ff-81a7-d3e96f2e238d \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_d181fbae-29f2-43bb-9a41-6bc888ca07de \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_d181fbae-29f2-43bb-9a41-6bc888ca07de --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
