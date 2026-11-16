# [reviewer_doc] SPEC 0.9.5 재검수 — 리뷰 수정 반영 확인(D-70 ④)
# [reviewer_doc] <한 줄 제목>

너는 **interpret-pwa `reviewer_doc` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/roles/interpret-pwa/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)


## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md` D-67 ~ D-70 · OQ-034 ~ 036 ← 대조 기준
- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/work/tongky-quality-re1/research-turn-taking-report.md` ← 사실 · 공식 문서 인용의 원천
- 검수 대상: `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/para/projects/summer-star/interpret-pwa/20-spec/spec-001-interpret-pwa.md`(0.9.5 — `git diff` 로 바뀐 곳) · `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/para/projects/summer-star/interpret-pwa/30-work/work-001-interpret-pwa.md` WP30 ~ WP32

기대는 개념: 해당 없음.

## 2. 배경

SPEC 0.9.5 는 통키를 세 번째 참여자로 바꾼다(차례 끝에 음성 · 늘 듣기 · 재생 언어 버림 · 끼어들기 멈춤 · agent text). 이 계약대로 back(WP30) · front(WP31)가 **병렬로** 만든다 — 계약 구멍은 두 워커가 서로 다르게 메운다.

## 3. 볼 것

0. **재검수다** — 앞 리포트 `review-spec-095-report.md` 의 FAIL-1 · WARN-1 ~ 8 이 DEC D-70 ④ 처분대로 닫혔는지 하나씩 판정하고, 수정이 새로 만든 구멍이 없는지 본다. backend · frontend 워커가 이 SPEC 으로 **이미 병렬 구현 중**이다 — 계약(WS 메시지 · 순서 · 숫자)에 닿는 지적은 맨 위에 따로 모은다.

1. 모든 새 정책이 DEC D-68 ~ D-70 · 조사 리포트 · 공식 문서 중 하나를 가리키는가. 근거 없는 정책 · 화면 문구 0.
2. **back ↔ front 계약이 닫혀 있나**: `audio_stop` · `playback_stopped` 모양 · 순서 · 이미 받은 PCM · 재생 큐 · 원 표시 · 누르고 말하기 · 멈춤(pause)/재개 · 언어 바꿈 · 오류 때. 한쪽만 읽고 만들 수 있는가.
3. agent text: 공식 문서(`https://docs.soniox.com/stt/rt/agent-text-input.mdx`)와 메시지 이름 · 키 · 순서 · 끝내는 법이 맞나(직접 문서를 읽어 대조).
4. 반이중을 전제한 문장이 남았나(§5 · §7 · §8 · §9 전부 grep).
5. 시험(§9.1)이 규칙 ① ~ ④ 와 D-69 숫자를 고정하나 · 「가짜 Soniox 만으로 done 금지」 실물 항목.
6. 현재 코드(`/Users/kknaks/orca/workspaces/interpret-pwa/tongky-quality-re1`, 읽기만)에 비춰 계약이 만들 수 있는 것인가(예: back 이 재생 구간을 어떻게 아는지).

## 4. 하지 말 것

- 문서 · 코드 수정 금지. 결정하지 않는다.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `(read-only — 브리프가 지정한 리뷰 리포트 파일 1개만 생성)`

## 6. 할 것

리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/work/tongky-quality-re1/review-spec-095-r2-report.md` — 판정 PASS · WARN · FAIL · 지적마다 파일:줄 + 근거.

## 8. 검증

```
SPEC·WORK 를 DEC 에 대조. 각 지적에 파일:줄 + 근거. 판정 FAIL/WARN/PASS
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_0cdc063d-4b42-4e5f-bc41-65528f81e60f --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_0cdc063d-4b42-4e5f-bc41-65528f81e60f \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_0cdc063d-4b42-4e5f-bc41-65528f81e60f --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
