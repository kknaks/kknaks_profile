
# [planner] SPEC 0.9.5 재검수 WARN-1 ~ 3 반영 (D-70 ④ 재검수 처분)

너는 **interpret-pwa `planner` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/roles/interpret-pwa/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

코디 워크트리를 그대로 쓴다. 코디가 `10-decision/` 에 D-67 ~ D-69 · BASE-001 입력 6 을 이미 적었다 — 그 파일은 건드리지 마라.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/work/tongky-quality-re1/review-spec-095-r2-report.md` WARN-1 ~ 3 (줄 번호 · 「닫는 길」)
- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md` D-70 ④ 끝 「재검수 처분」 문장

## 2. 처분 — 이대로 SPEC 문장 · 시험을 맞춘다 (backend 워커는 이미 이 처분으로 만드는 중)

1. `playback_stopped` 로 멈출 때, `audio_start` 를 보냈고 `audio_end` 를 아직 안 보낸 발화가 있으면 PCM 은 끊되 `audio_end{id}` 는 보낸다. 시험 ⑯ 에 한 줄.
2. `playback_stopped` 의 `id` = 「이 통키 차례에서 `audio_start` 를 보낸 발화 id 가운데 하나」 면 멈춘다 · 지난 차례 id 면 아무 일 없음 — §5.3 문장을 §5.13 H 낱말로. 시험 ⑯ 에 두 경우.
3. 멈춤 절차 ③(`terminated` 기다림 · 3초 한도)은 ④ ~ ⑦ 과 front 메시지 처리를 막지 않는다 — ④ ⑤ ⑥ 은 `cancel` 직후 · 끝 = 절차를 시작한 때의 `sent_ms`. 시험 한 줄(스트림 진행 중 · 멈춤 중 재생에서 `playback_stopped` → `resume` · 가짜 TTS 가 `terminated` 를 늦게 줌 → 재생 쪽 언어 첫 토큰이 남는다).
4. 리포트 「참고」 의 표기 둘(`spec:1675` 3초 근거 = D-70 · `30-work/README.md` WORK-001 행에 D-70)도 같이.

## 3. 계약

WS 메시지 이름 · 모양 그대로.

## 4. 먼저 볼 것

리포트 줄 번호 자리.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `para/projects/summer-star/interpret-pwa/20-spec/`
- `para/projects/summer-star/interpret-pwa/30-work/`

## 6. 할 것

위 처분만. 판 0.9.5 그대로(변경 이력 0.9.5 줄에 「재검수 반영」).

## 7. 범위 제약 — 하지 말 것

- DEC · 코드 · `orchestration/` 수정 금지.

## 8. 검증

```
SPEC 의 모든 절이 DEC · 확정 시안 중 하나를 근거로 가리킨다. 근거 없는 정책 0 · 열린 것은 열린 것으로. 링크 · 인덱스 갱신. public — 키 · 계정값 · 실명 0(grep)
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
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_0cdc063d-4b42-4e5f-bc41-65528f81e60f \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_0cdc063d-4b42-4e5f-bc41-65528f81e60f --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
