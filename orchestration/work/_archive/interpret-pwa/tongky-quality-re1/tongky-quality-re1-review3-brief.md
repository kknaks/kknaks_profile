# [reviewer] WP30 · WP31 코드 검수 — 세 참여자(D-68 ~ D-70)
# [reviewer] <한 줄 제목>

너는 **interpret-pwa `reviewer` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/roles/interpret-pwa/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/interpret-pwa/tongky-quality-re1`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)


## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/para/projects/summer-star/interpret-pwa/20-spec/spec-001-interpret-pwa.md` 0.9.5 — §5.3 · §5.10 · **§5.13** · §7.3 · §7.4 · §9.1(① ~ ㉔) · §9.2 · §9.3 ㉘ ← 대조 기준
- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md` D-68 ~ D-70(④ 리뷰 · 재검수 처분 포함)
- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/work/tongky-quality-re1/review-spec-095-r2-report.md` — 문서 단계에서 짚은 위험 자리(「고객이 실물에서 만날 자리」)

기대는 개념: 해당 없음.

## 2. 배경

backend · frontend 워커가 같은 워크트리에 미커밋 변경을 남겼다(`git status` · `git diff` — back/ 과 front/). 통키를 세 번째 참여자로: 차례 끝에 음성 · 재생 중 송신 · 재생 언어 토큰 버림 · 반대 언어 토큰 2개면 `audio_stop` · `playback_stopped` · Soniox agent text.

## 3. 계약

§5.3 `audio_stop{type,id}` · `playback_stopped{type,id}` — **back 과 front 를 서로 맞대어** 본다(병렬로 따로 만들었다).

## 4. 볼 것

1. back ↔ front 계약 일치: 메시지 이름 · 키 · 보내는 때 · id · `audio_end` 처리 · 버림 표시 · 원 표시(`outputting`).
2. §5.13 규칙이 코드에 그대로인가 — 차례 끝 시계(1초 · 재생 언어 · 시각만 바뀐 비확정 제외) · 되울림 구간(끝 · 여유 500 · 멈춤 중 여유 0 · 보관 30초 서버 시계) · 끼어들기 2개 · 멈춤 절차 순서(audio_stop 먼저 · 진행 중만 cancel · 기다림이 다른 처리를 막지 않음) · agent text 시점 · end_of_segment.
3. 「조용히 통과하는 자리」: 언어 바꿈 · stop · 연결 끊김 · 오류 때 타이머 · 태스크 · TTS 스트림 정리 · 누르고 말하기 · pause/resume · 빈 원문 막기 · 바로잡기 · 기록이 새 큐 구조에서 그대로 도는가.
4. backend 보고의 미결 ①(멈춤 중 차례 끝에 글 없는 end_of_segment) · ⑤(시험이 실제 1초를 기다림)가 SPEC 과 맞는지.
5. back: `uv run pytest` · `uv run ruff check .` / front: `npx tsc --noEmit` · `npm run lint` · `npx vitest run` — 1회씩.

## 4-1. 하지 말 것

- 파일 수정 · 커밋 금지. Soniox 실물 호출 하지 마라(backend 가 했다).

## 5. allowed_paths — 이 밖은 건드리지 마라

- `(read-only — 리포 파일 수정 금지. 산출물은 브리프가 지정한 리뷰 리포트 파일 1개뿐)`

## 6. 할 것

리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/work/tongky-quality-re1/review-wp30-31-code-report.md` — PASS · WARN · FAIL · 지적마다 파일:줄 + 근거(SPEC 절 · DEC).

## 8. 검증

```
각 지적에 파일:줄 + 근거(SPEC 절 · DEC D-번호). 판정 FAIL · WARN · PASS. 「조용히 통과하는 자리」를 따로 본다
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
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_0cdc063d-4b42-4e5f-bc41-65528f81e60f \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_0cdc063d-4b42-4e5f-bc41-65528f81e60f --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
