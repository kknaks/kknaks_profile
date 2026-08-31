
# [frontend] <한 줄 제목>

너는 **mediness `frontend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/roles/mediness/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/meeting-room-workflow`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

<같은 워크트리를 다른 워커와 공유하면 여기에 경고를 적는다. 예: "BE 워커가 `back/` 에서 병렬 작업 중 — 건드리지 마라.">

## 1. SSOT — 먼저 읽을 것

- `<spec/WP 절대경로>` ← 계약의 SoT. **여기 없는 건 발명하지 마라.**
- `<추가 참조 절대경로>`

**기대는 개념** — 이 작업이 따를 판단 기준. 안 주면 워커가 매번 처음부터 정하고,
같은 결정이 작업마다 달라진다. 없으면 "해당 없음".

- `<…/para/areas/concept/<영역>/<stem>.md>` — <이 작업에서 무엇을 이대로 하라는 건지 한 줄>

## 2. 배경 / 무엇을 바꾸나

<현재 상태 → 바꿀 것. 왜 하는지 1~2문단.>

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

<BE↔FE 계약이 있으면 필드명·shape·에러코드까지 명시. 없으면 "해당 없음".>

## 4. 먼저 읽을 핵심 파일

- `<파일:줄>` — <왜 봐야 하는지>

## 5. allowed_paths — 이 밖은 건드리지 마라

- `front/`

## 6. 구현 단계

1. <…>

## 7. 범위 제약 — 하지 말 것

- <…>

## 8. 검증

```
cd front && npx tsc --noEmit (네가 만진 파일 0 에러) + prettier --check <네가 만진 파일만>. 전체 빌드·전체 포맷 검사 금지 — 사용자 방침. 검증은 1회만
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
  --to term_e8a1a258-210f-466b-8b05-c43a7ec8a7ad --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_e8a1a258-210f-466b-8b05-c43a7ec8a7ad \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_e8a1a258-210f-466b-8b05-c43a7ec8a7ad --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
