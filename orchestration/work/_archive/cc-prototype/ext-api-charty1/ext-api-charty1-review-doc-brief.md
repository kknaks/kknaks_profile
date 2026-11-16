
# [reviewer_doc] charty 1차 문서 검수 r1 — DEC-012 · SPEC-008 0.4.0 · WORK-014

너는 **cc-prototype `reviewer_doc` 워커**다(read-only). **앞 맥락은 하나도 없다.** 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2/orchestration/roles/cc-prototype/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2` (코디 워크트리 · 공유 — 리포트 1개 말고는 건드리지 마라)

## 1. SSOT — 먼저 읽을 것

`P = /Users/kknaks/orca/workspaces/kknaks_profile/cc-2/para/projects/summer-star/cc-prototype` · `W = /Users/kknaks/orca/workspaces/kknaks_profile/cc-2/orchestration/work/ext-api-charty1`

- 사용자 결정: `W/_RESUME.md` §2 · planner 브리프 `W/ext-api-charty1-spec-brief.md` §2 · §3 (사용자 결정 D 와 코디 기본값)
- 검수 대상: `P/10-decision/decision-012-ext-api-charty1.md` · `P/20-spec/spec-008-product-ext-api.md`(0.4.0 · 0.4.0 에서 바뀐 절 중심 — §3.6 · §4.3 · §4.4 · §6.4 · §6.9 ~ §6.18 · §8 · §9 T48 ~ T73 · 부록 F · G) · `P/30-work/work-014-ext-api-charty1.md` · 세 README · `P/work-index.md`
- KOS 사실: `W/research-charty1-sources.md` · `W/research-clinic-staff.md` · `W/research-har-history-hospital.md`
- 앞 결정: `P/10-decision/decision-010-product-ext-api.md` · `P/10-decision/decision-011-ext-api-add1.md`
- 코드(읽기만): kknaksss/cc-prototype `origin/main` `0a58aba` — canonical `/Users/kknaks/git/toy_pr2/cc-prototype` 는 예전 커밋이다. **`git -C /Users/kknaks/git/toy_pr2/cc-prototype show origin/main:procedure/back/app/<경로>`** 로만 읽어라(checkout · pull 금지)

## 2. 볼 것

1. **결정 대조** — 사용자 결정(API 8개 · D-01 ~ D-07)과 코디 기본값이 DEC-012 · SPEC 에 빠짐 · 뒤틀림 없이 들어갔나(부록 F 대조표를 믿지 말고 본문으로). DEC 에 없는 정책(근거 없는 것). **「원하는 데이터만」** — 연동처가 요청하지 않은 칸 · 경로를 더한 곳
2. **기존 계약** — 기존 ext 6개 · 직원 API 를 깨는 곳. lookup 은 칸 추가만인가. 직원 서비스 안을 손대는 곳(판정 함수 이동 · `_detail_reads` · `personal()` actor)이 동작을 바꾸지 않나
3. **코드 규약 근거** — 「코드 규약: 파일:줄」이 origin/main 에 실제로 있나 · 지금 동작과 맞나
4. **KOS 사실** — 조사 리포트와 다른 서술. 리포트가 「추정 · 미확인」이라 한 것을 SPEC 이 단정한 곳(이력 조회 · 휴무 모양 · 선불카드 값 타입 · 상담 메모 쓰기 · 개인 묶음 쓰기). 그런 칸이 WORK 의 KOS0 · E2E 에서 확인되게 묶였나
5. **조용히 통과하는 자리** — 처음 상담 대기 시각 저장(한 번 null 저장되면 영영 null 이 되는 틈 · 상담 대기 재진입) · 쓰기 실패 후 사본 · `event_log` 불일치 · 헤더 직원 id 가 로그 · 오류로 새거나 검증 없이 행위자로 들어가는 모양 · 부분 실패가 200 으로 숨는 곳 · board KOS 호출이 건수에 비례하게 되는 틈 · 내부 API 토큰 만료 · UA
6. **WORK-014** — Phase 순서(KOS0 먼저 · 의존) · Phase 마다 부분 검증 명령 · 끝 조건에 데모 KOS 실물 호출(쓰기는 시험 고객 · 되돌림) · 기존 6개 회귀 · 전체 검증은 끝에 1번
7. **planner 질문 Q1 ~ Q14(부록 G)** — 각 제안값이 근거(조사 · 코드 · DEC)와 맞나. 판정만 하고 정하지 않는다
8. public grep(키 · 토큰 · 실명 · 이메일 · 전화 · KOS id · uuid · hex24 0)

## 3. 산출물

리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2/orchestration/work/ext-api-charty1/review-doc-r1.md`
- 맨 위 종합 판정(FAIL · WARN · PASS)과 건수
- 지적 표: 번호 · 판정 · 파일:줄 · 무엇이 틀렸나 · 근거(DEC D-번호 / 코드 파일:줄 / 리포트 절) · 고칠 방향
- 「조용히 통과하는 자리」 절 · 「Q1 ~ Q14 판정」 절 따로

## 4. 제약

- 파일 수정 금지(리포트 1개만) · KOS 호출 금지 · 커밋 · push 금지 · public 기준(값 원문 0)
- 결정하지 않는다 — DEC 가 틀렸다고 보이면 「DEC 질문」으로 따로 모은다

## 8. 검증

```
SPEC·WORK 를 DEC 에 대조. 각 지적에 파일:줄 + 근거. 판정 FAIL/WARN/PASS
```

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_aad33590-4323-443d-9c17-3541475ee5f5 --from term_7afd8629-5aa7-426f-add3-72325ed1f994 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_aad33590-4323-443d-9c17-3541475ee5f5 \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_aad33590-4323-443d-9c17-3541475ee5f5 --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
