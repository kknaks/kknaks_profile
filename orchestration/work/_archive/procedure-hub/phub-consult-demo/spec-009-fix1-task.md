# [writer] SPEC-009 수정 1 — 검수 FAIL 반영 (0.1.0 → 0.1.1)

검수 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo/review-spec-009.md`(FAIL 5 · WARN 11).

- **FAIL 5 전부 고친다**(리포트의 「고칠 것」 그대로): F1 D3 겹침 목록(침샘 · 쇄골 · 승모근 · 귀밑샘 · 턱밑샘은 정해진 배치 — 다시 묻지 마라) · F2 T2-1(SITE-120 실측 — 계층 변경이 gold 바이트에 주는 영향 정정) · F3 근거 종류 식 세 곳 + 정렬 목록 둘(gold-build 가 새 값에서 멈추는 자리 전부) · F4 「눈 → 눈 주변 다른 이름」 과 기존 SITE-018 「눈」 충돌 처리(정해진 결정을 바꾸지 말고, 충돌을 처리하는 꼴을 제시하거나 처리 방식을 「정할 것」 으로) · F5 `_RESUME` 줄 인용 전부 다시 맞춤(:37 결정 행 포함).
- **WARN 11 도 반영** — 특히 W1(근거 종류를 줄 내용으로 정하나 · 경로로 정하나 → 정할 것) · W2(범위 값 합치는 규칙 → 정할 것) · W7(gold-check A3 · G1 → Q9-12 · Q9-13) · W9(묶음 이름 · 진료항목 코드 공개 여부 → Q9-2 넓힘) · 「사용자가 실물에서 만날 자리」(부위 3단은 이 판으로는 앱에 안 보임)를 §0 요약에 분명히.
- 결정을 새로 만들지 마라. 바꾼 절마다 변경 기록 0.1.1 에 한 줄.
- 끝나면 앞과 같은 2채널 보고(subject 「writer 완료: SPEC-009 0.1.1」).

## 맥락(처음 작성 브리프 — 읽을 것 · 범위 · 하지 말 것은 그대로)
- `/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo/phub-consult-demo-write-brief.md` 를 먼저 읽어라. 대상 파일은 `orchestration/work/phub-consult-demo/SPEC-009-hub-clinic-supplement.md` 하나.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_fa431c7d-dde7-4285-a9a5-415b72081747 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 \
  --text "[worker_done] writer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[질문] writer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
