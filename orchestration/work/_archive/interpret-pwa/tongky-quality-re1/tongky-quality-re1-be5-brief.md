# [backend] WP33 — Soniox context 를 고유명사 74개 · 정방향 + 역방향만으로 (D-71) + 실물 측정

너는 **interpret-pwa `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/roles/interpret-pwa/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/interpret-pwa/tongky-quality-re1`
브랜치: `kknaksss/tongky-quality-re1-dict`(코디가 `origin/main` `c7a582f` 에서 새로 땄다) → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

front/ 는 건드리지 마라.

## 1. SSOT — 먼저 읽을 것

- DEC D-71(사전에는 고유명사만): `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md`
- 나누기 표(① 74개가 대상): `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/work/tongky-quality-re1/dict-classification.md` — `## ① 고유명사 — 74개` 절의 id 전부. ② · ③ 은 context 에서 뺀다(사용자 결정: ③ 애매 35개도 뺌)
- 앞 측정: `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/work/tongky-quality-re1/research-proper-noun-dict-report.md` · 스크립트 · 음성 `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-kknaks-profile--------/6b7f4a9c-bfce-487f-8c42-08de89fd57d4/scratchpad/probe3/`(그대로 다시 써도 된다)
- 코드: `back/app/service/glossary.py`(`build_context` · `ContextParts` · `to_soniox` · 시드 검사) · `back/app/container.py`(`context_for`) · `back/seed/glossary.json`(`.10`)

## 2. 사용자 결정 — 이대로

Soniox STT 설정 `context` 를 이렇게 바꾼다(일곱 언어 모두 같은 규칙):

| 칸 | 지금 | 바꾼 뒤 |
|---|---|---|
| `general` · `text` | 고정 | **그대로** |
| `terms`(한국어 받아쓰기 힌트) | 170개 ko 이름 + ko 별칭 | **고유명사 74개의 ko 이름만**(별칭 없음 · 170개로 두지 않는다 — 사용자 「170개 하지 말고 74개만」) |
| `translation_terms` | 정방향 · 정방향 별칭 · 역방향 · 역방향 별칭 | **고유명사 74개의 정방향(ko 이름 → 현지 이름) + 역방향(현지 이름 → ko 이름)만**. 별칭 짝 둘은 넣지 않는다 |

- 고유명사 표시는 **시드에** 둔다: term 키 `proper`(bool · 선택 · 없으면 false) — 시드 검사에 키 · 타입 추가. ① 74 id 에 `true`. 시드 버전 `2026-11-16.11`
- 바로잡기(`correct_terms` · 별칭 · `wrong`)는 **지금 그대로 170개 전부**를 쓴다 — context 만 줄인다. 시드의 별칭 · wrong 값은 지우지 않는다
- 역방향 source 중복 처리(처음 짝만) · yue · zh-Hant t2s · 크기 줄이기 · `invalid_request` 때 정방향만 다시 연결은 지금 규칙 그대로(줄일 묶음이 줄었을 뿐). 줄이기 순서에서 없어진 묶음은 빠진다
- 로그(칸 수 · 글자 수)는 지금 모양 그대로 — 별칭 칸은 0 으로 찍혀도 된다

## 3. 할 일

A. 위 변경 구현 + 시험 고침 · 추가: ① proper 아닌 term 은 context 에 0 · ② 별칭 짝 0 · ③ terms = proper ko 이름 수 · ④ 바로잡기는 proper 아닌 term 도 그대로 동작(예: 지금 시험 하나 유지) · ⑤ 시드 검사 `proper` 타입 오류.
B. **실물 측정(운영 키 · 새 코드의 `build_context` 출력을 그대로 Soniox 에 보냄)**
   - zh: probe3 의 문장 전부(울쎄라 · 써마지 · 쥬베룩 · 리쥬란 힐러 · 나보타 · 슈링크유니버스 + 울쎄라 같은 문장 · 손님 `美版超声刀` · `热玛吉` · 손님 `超声刀` 질문 뒤 흐름 F2 · 일반 낱말 혈관 · 색소 · 미백 · 토닝 · 제모) 각 **6회 이상**. 사전 이름이 나온 수 / 횟수 · 틀린 꼴 · 「제모」 받아쓰기(→ 「제목」 여부)
   - 비교: 같은 문장 · 같은 횟수를 앞 리포트의 p1(① 만 · 별칭 포함 · terms 74) 수치와 한 표로
   - 나머지 여섯 언어(en · ja · zh-Hant · th · vi · yue): 설정이 받아들여지는지(오류 0) · context 글자 수 · 짝 수 · 울쎄라 · 써마지 직원 문장 각 3회(사전 이름 나온 수)
   - 음성 · 스크립트 · 결과는 `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-kknaks-profile--------/6b7f4a9c-bfce-487f-8c42-08de89fd57d4/scratchpad/probe4/` 에만
   - Soniox 키: `export SONIOX_API_KEY=$(ssh medi-me "/opt/homebrew/bin/kubectl -n interpret-pwa-prod get secret interpret-pwa-secret -o jsonpath='{.data.SONIOX_API_KEY}'" | base64 -d)` — 그 셸 env 에만. 출력 · 파일 · 로그에 키 0
C. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/work/tongky-quality-re1/wp33-context-report.md` — 바꾼 파일 · 시험 수 · 언어별 context 글자 수 · 짝 수 · B 표 · 틀린 꼴 · 「정할 것」(결정 0 · 운영 기록 문장 0)

## 4. allowed_paths — 이 밖은 건드리지 마라

- `back/app/service/glossary.py` · `back/app/container.py`(필요할 때만) · `back/seed/glossary.json` · `back/tests/**` · `back/scripts/**`(필요할 때만)
- 위 리포트 하나 · scratchpad `probe4/`

## 5. 범위 제약 — 하지 말 것

- 문서(SPEC · DEC · WORK) 수정 금지 — 코디가 따로 맡긴다. 운영 서버 · 배포 · 사용자 포트 · 사용자 프로세스 금지(키 읽는 kubectl 한 줄 외)
- 바로잡기 · 끊김 · 세 참여자 로직 건드리지 않기

## 6. 검증

```bash
cd /Users/kknaks/orca/workspaces/interpret-pwa/tongky-quality-re1/back && uv run pytest -q && uv run ruff check .
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.
- 실물 측정(B)이 끝나야 완료다.

## 7. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- **커밋은 해도 된다(브랜치 `kknaksss/tongky-quality-re1-dict`) · push·PR 하지 마라.** 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_0cdc063d-4b42-4e5f-bc41-65528f81e60f --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_0cdc063d-4b42-4e5f-bc41-65528f81e60f \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_0cdc063d-4b42-4e5f-bc41-65528f81e60f --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
