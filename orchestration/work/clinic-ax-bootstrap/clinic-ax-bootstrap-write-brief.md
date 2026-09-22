
# [writer] 병원 AX 별도 레포 PARA 초기 구성

너는 **ax-clinic-project `writer` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/병원AX전략/orchestration/roles/ax-clinic-project/writer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/git/ax-clinic-project`
base 브랜치: `main (unborn)` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

단독 문서 작업. 원본 개인 레포는 read-only. 새 레포가 unborn 상태라 초기 구성만 직접 경로에 작성한다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/병원AX전략/reference/2026-09-16-병원AX/ax-clinic/00-strategy-flow.md` ← 계약의 SoT. **여기 없는 건 발명하지 마라.**
- `/Users/kknaks/orca/workspaces/kknaks_profile/병원AX전략/reference/2026-09-16-병원AX/ax-clinic/00-rules.md`

**기대는 개념** — 이 작업이 따를 판단 기준. 안 주면 워커가 매번 처음부터 정하고,
같은 결정이 작업마다 달라진다. 없으면 "해당 없음".

해당 없음 — 이번 작업은 사용자가 합의한 문서 배치와 복사.

## 2. 배경 / 무엇을 바꾸나

사용자가 새 빈 레포에 PARA 구조 및 지금까지 작성한 문서를 구성하라고 요청했다. 한국어 본문과 영어 파일명을 유지한다.

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

대상 루트: README.md, AGENTS.md(규칙 원본 링크만 안내), rules/document-rules.md, projects/clinic-ax-strategy/, areas/, resources/{market,cases,technology}/, archive/.
프로젝트 안: README.md(목표, 산출물 링크, 상태, 기한), 원본의 00-strategy-flow.md 및 01~08 정식 문서, A-sources.md; evidence/{internal-data,interviews,fieldwork}/. 빈 디렉터리는 .gitkeep. 05~08와 A-sources가 빈 파일이면 그대로 유지. temp 파일 복사 금지.
원본 00-rules.md를 rules/document-rules.md로 옮긴 사본이 새 원본. 근거 태그 및 규칙은 보존. 미정표의 문서 구성/독자처럼 이미 정해진 내용은 갱신하고 문서목록은 프로젝트 README를 링크. 원본 외부 참고자료 목록은 필요하면 출처 경로를 이관 전 위치로 명시하되, 자료는 복사하지 말고 미이관임을 명시해 상대경로 오류 방지. 전략문서 작성원칙 링크는 ../../rules/document-rules.md로 변경.
이 프로젝트는 전략 수립 단계다. 5년 표현 넣지 말 것. 자료조사 2026-09-23, 인터뷰 10-02, 현장 10-14, 전략수립 10-19 기한 유지. 실증/승인이 완료됐다고 쓰지 않는다.
02 병원 현황(고객구성, 매출, 외국인매출비중, 객단가, 비용); 03 고객 시간순 여정; 04 일/주/월/이벤트 운영. 내용 임의 추가 금지. README에는 새 레포를 향후 원본으로 안내. 기존 원본 삭제 금지.
areas는 상시 운영, resources는 범용 참고 자료, archive는 완료 프로젝트. README에 분류 기준 설명. 빈 폴더 외 별도 실행 프로젝트 생성 금지.

## 4. 먼저 읽을 핵심 파일

- 위 source 디렉터리의 정식 문서 00~08 및 A-sources.md만 읽고 복사.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `README.md`
- `AGENTS.md`
- `rules/`
- `projects/`
- `areas/`
- `resources/`
- `archive/`

## 6. 구현 단계

1. 원본과 대상 확인 → 구조 생성 → 문서 복사 및 상대링크 수정 → README/AGENTS 작성 → 링크 및 내용 보존 검증.

## 7. 범위 제약 — 하지 말 것

- 원본 변경, 커밋, push, PR, 조사 수행, 사실 생성 금지.

## 8. 검증

```
Check local links, exact copied documents and empty placeholders; no invented facts.
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
  --to term_66daaa12-cf95-40e0-862b-2acc09e6ff72 --from term_76c658c3-3b7c-4043-bd32-031cb3cc6ac1 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_66daaa12-cf95-40e0-862b-2acc09e6ff72 \
  --text "[worker_done] writer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_66daaa12-cf95-40e0-862b-2acc09e6ff72 --text "[질문] writer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
