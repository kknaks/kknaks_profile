# [frontend] WP31 — 반이중 걷음 · audio_stop · playback_stopped (D-68)
# [frontend] <한 줄 제목>

너는 **interpret-pwa `frontend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/roles/interpret-pwa/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/interpret-pwa/tongky-quality-re1`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

backend 워커가 같은 워크트리 `back/` 에서 병렬 작업 중 — 건드리지 마라.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/para/projects/summer-star/interpret-pwa/20-spec/spec-001-interpret-pwa.md` **0.9.5** — §5.13(세 참여자 · 줄 1550 ~) · §5.3 메시지(`audio_stop` · `playback_stopped`) · §5.10 · §7.3 · §7.4 · §9 ← 계약의 SoT(코디 워크트리 · read-only). **여기 없는 건 발명하지 마라.** 막히면 질문으로.
- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md` D-68 ~ D-70 · `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/para/projects/summer-star/interpret-pwa/30-work/work-001-interpret-pwa.md` **WP31** 행(할 일 · 완료 조건의 SoT)
- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/work/tongky-quality-re1/research-turn-taking-report.md` — Soniox 응답 · agent text 실물 사실
- 문서 리뷰가 같이 돌고 있다 — 계약이 바뀌면 코디가 알린다(체크포인트마다 `orca orchestration check`).

기대는 개념: 해당 없음.

## 2. 배경

통키를 「고객 – 통키 – 직원」 세 번째 참여자로 바꾼다 — 자막은 바로 · 음성은 차례 끝(마지막 새 말 1초 뒤) · 재생 중에도 듣기 · 재생 언어 토큰 버림 · 반대 언어 토큰 2개면 재생 멈춤 · agent text 로 되울림 빼기. 브랜치 `kknaksss/tongky-quality-re1` 는 `origin/main`(`fe375ad`)에서 시작.

## 3. 계약

SPEC §5.3 · §5.13 의 WS 메시지 그대로(`audio_stop` back → front · `playback_stopped` front → back). 이름 · 키 · 순서를 바꾸지 마라 — 반대편 워커가 병렬로 같은 계약을 만든다.

## 4. 먼저 읽을 핵심 파일

- `front/lib/interpret.ts`(송신 조건 · 재생 · `clearPlayback`) · `front/lib/halfDuplex.ts` · `front/lib/ptt.ts` · `front/components/interpret/InterpretScreen.tsx`(원 상태) — `outputting` · `speaking` · `audio_start` · `audio_end` 를 쓰는 곳 전부 grep 으로 센다.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `front/`

## 6. 구현 단계

WORK WP31 행과 SPEC §7.3 · §7.4 · §5.3 순서대로: 반이중 송신 조건 걷기 · `audio_stop` 받으면 재생 즉시 멈춤 · `playback_stopped` 보내기(SPEC 이 정한 때만) · 원 표시는 SPEC 표 그대로 · 누르고 말하기 동작 SPEC 대로. 새 화면 문구 0.

## 7. 범위 제약 — 하지 말 것

- `back/` 는 backend 워커가 같은 워크트리에서 병렬로 고친다 — **건드리지 마라.** 커밋 금지(코디가 한다).
- 실기기(마이크 · 스피커 되울림)는 pending 으로 보고 — 배포 뒤 사용자가 한다. 사용자 포트 · 프로세스(dev 서버 포함)를 건드리지 않는다.

## 8. 검증

```
front 에서 npx tsc --noEmit · npm run lint · npm run build — 각 1회. 사용자 포트·프로세스를 건드리지 않는다. 실기기(마이크 · PWA 설치) 확인은 pending 으로 보고
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
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_0cdc063d-4b42-4e5f-bc41-65528f81e60f \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_0cdc063d-4b42-4e5f-bc41-65528f81e60f --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
