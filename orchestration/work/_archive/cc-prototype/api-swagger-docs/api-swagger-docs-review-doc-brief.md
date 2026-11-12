# [reviewer_doc] SPEC-008 · WORK-012 검수 — DEC-010 대조

너는 **cc-prototype `reviewer_doc` 워커**다(read-only). 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/orchestration/roles/cc-prototype/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2` (코디 워크트리 — 파일 수정 금지. 리포트 1개만 쓴다)

## 1. SSOT — 먼저 읽을 것

- 기준: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/para/projects/summer-star/cc-prototype/10-decision/decision-010-product-ext-api.md` (accepted · D-01 ~ D-34 · D-05 는 2026-11-11 고침)
- 추가 결정(planner 질문 Q1 ~ Q5 코디 답): `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/orchestration/work/api-swagger-docs/_RESUME.md` §2 의 「planner 질문」 「planner Q4」 「planner Q5」 줄
- 검수 대상: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/para/projects/summer-star/cc-prototype/20-spec/spec-008-product-ext-api.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/para/projects/summer-star/cc-prototype/30-work/work-012-product-ext-api.md` (+ 두 README 행 · DEC-010 links)
- KOS 사실: 같은 폴더 `research-procedure-menu.md` · `research-purchase-snapshot.md` · `research-har-product-edit.md` · `research-name-email-lookup.md`
- 코드(읽기만): `/Users/kknaks/git/toy_pr2/cc-prototype` main `c9f30ac` — SPEC 이 「코드 규약: 파일:줄」로 가리킨 곳

## 2. 볼 것

1. **DEC 대조** — D-01 ~ D-34 · Q1 ~ Q5 가 SPEC 에 빠짐 · 뒤틀림 없이 들어갔나(부록 A 대조표를 믿지 말고 본문으로 확인). DEC 와 다른 정책 · DEC 에 없는 정책(근거 없는 것)
2. **코드 규약 근거** — 「코드 규약: 파일:줄」이 그 줄에 실제로 있나 · 지금 동작과 맞나(예: 오류 형식 · 400 invalid_request · 기본 구역 규칙 · `identifiable()` · 예약 생성 흐름 · `require_login` 과의 분리 · `test_openapi_docs` 단언)
3. **KOS 사실** — 조사 리포트와 다른 서술(경로 · 칸 이름 · 페이징 · email 칸 · 시술권 모양). 리포트에 없는 KOS 사실을 단정한 곳
4. **구현 가능성 · 조용히 통과하는 자리** — 외부 키가 직원 API 를 통과하거나 직원 토큰이 외부 API 를 통과할 틈, 이름/이메일 원문이 기록 · 로그 · 오류 메시지로 새는 틈, 「없음」과 「특정할 수 없음」 응답 차이로 어느 쪽이 틀렸는지 알 수 있게 되는 틈, 0 / 1 / 2+ 갈래와 KOS 실패의 구분, 페이징 끝 조건, 동기화 실패 시 이전 값
5. **WORK-012** — WP 순서 · 완료 조건 · 실물 확인(데모 조회 · 예약) 포함 · 검증 범위(관련 시험만, 전체는 끝에 1번)
6. **열린 것 0** · public grep(키 · 토큰 · 실명 · 이메일 · KOS id 값 0)

## 3. 산출물

리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/orchestration/work/api-swagger-docs/review-doc-r1.md`
- 맨 위 종합 판정(FAIL · WARN · PASS)과 건수
- 지적 표: 번호 · 판정 · 파일:줄 · 무엇이 틀렸나 · 근거(DEC D-번호 / 코드 파일:줄 / 리포트 절) · 고칠 방향
- 「조용히 통과하는 자리」 절 따로

## 4. 제약

- 파일 수정 금지(리포트 1개만) · KOS 호출 금지 · 커밋 · push 금지
- 결정하지 않는다 — DEC 가 틀렸다고 보이면 「DEC 질문」으로 따로 모은다

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_2be25447-14e8-4dcf-9ed4-6b05f0fb0e46 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_2be25447-14e8-4dcf-9ed4-6b05f0fb0e46 \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_2be25447-14e8-4dcf-9ed4-6b05f0fb0e46 --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
