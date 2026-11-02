# [planner] 조사 A — baseline 이 인터뷰 1차를 어디까지 담고 있나 (조사 전용 · diff 0)

너는 **sc-ax `planner` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-interview/orchestration/roles/sc-ax/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/interview1-update-spec`
base 브랜치: `origin/sc-ax` → 최종 PR 대상 `sc-ax` (PR 은 코디네이터가 올린다)

**⚠ 이번 태스크는 조사 전용이다 — 워크트리 diff 0.** 리포 파일을 한 글자도 고치지 않는다.
산출물은 아래 §6 이 지정한 리포트 파일 1개뿐이다.
**같은 워크트리에서 조사 B 워커가 `00-planning/`·`20-spec/` 를 병렬로 읽는 중** — 둘 다 read-only 라 충돌은 없지만, 그쪽 범위 분석은 네 리포트에 중복해서 쓰지 마라.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-interview/references/2026-08-28-sc인터뷰-경영관리부/현행업무-발견지도.md` ← 인터뷰 해석의 SoT. AS-001~031.
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-interview/references/2026-08-28-sc인터뷰-경영관리부/회의록.md` ← 회의 자동 요약 (주제 13·이슈 7·액션 1).
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-interview/references/2026-08-28-sc인터뷰-경영관리부/트랜스크립트.md` ← 발화 원문. 필요한 대목만 찾아 읽어라 — 전체 정독 금지.

**기대는 개념** — 해당 없음.

## 2. 배경 / 무엇을 조사하나

2026-08-26 경영관리부 1차 관리자 인터뷰가 끝났고, 발견 31건(AS-001~031)이 위 발견지도로 정리돼 있다.
다음 단계는 ① baseline 업데이트 ② planning 업데이트 ③ 회의결과 보고서 작성인데, 발주 전에
**baseline(`products/sc-ax/00-baseline/`)이 지금 무엇을 담고 있고, 이번 인터뷰 내용과 어디가
겹치고 어디가 어긋나는지**를 먼저 알아야 한다. 이 조사가 ①의 발주 범위를 정한다.

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

해당 없음.

## 4. 먼저 읽을 핵심 파일

- `products/sc-ax/00-baseline/00-overview.md` — baseline 구조와 문서 규약 파악의 입구
- `products/sc-ax/00-baseline/02-background-and-problems.md` — 인터뷰 발견과 가장 직접 겹칠 문서
- `products/sc-ax/00-baseline/03-users-and-situations.md` — 경영관리부 사용자·상황 서술 현황
- `products/sc-ax/00-baseline/10-assumptions-risks-open.md` — 이번 인터뷰가 닫거나 열 가정·미결
- `products/sc-ax/00-baseline/B-sources.md` · `C-changelog.md` — 출처 등재·개정 규약 (업데이트 시 따라야 할 형식)
- `products/sc-ax/00-baseline/_working/meeting-notes-consolidated.md` · `survey-dept-status-2026-08.md` — 기존 인터뷰·설문 원료가 어떤 형태로 앉아 있는지

## 5. allowed_paths — 이 밖은 건드리지 마라

- (read-only — 리포 파일 수정·생성 금지. 산출물은 §6 의 리포트 파일 1개뿐)

## 6. 조사 단계

1. `00-baseline/` 전체(번호 문서 00~10 · A~C · `_working/` · `request/` · `SCAX-BL-001-thesc-prototype/`)의 역할과 현재 내용을 파악한다.
2. 발견지도 AS-001~031 · 회의록 주제 13건을 기준으로, baseline 문서별로 **(a) 이미 반영됨 (b) 낡아서 어긋남 (c) 없어서 추가 필요** 를 가른다. 항목마다 근거(`문서:절` + AS-ID)를 붙인다.
3. 이번 인터뷰 원료(발견지도·회의록·트랜스크립트)가 baseline 에 **어떤 형태로 들어가야 하는지** 기존 규약(`_working/` 원료 배치, B-sources 등재, C-changelog 개정 기록)에서 추론해 제안한다.
4. 리포트를 `/Users/kknaks/orca/workspaces/kknaks_profile/sc-interview/orchestration/work/interview1-update/survey-baseline-report.md` 에 쓴다. 형식:
   - 요약 (5줄 이내) / baseline 문서 지도 (문서별 한 줄) / 갱신 지점 표 (문서:절 · a/b/c · 근거 AS-ID · 무엇을) / 원료 배치 제안 / 미결·질문

## 7. 범위 제약 — 하지 말 것

- 리포 파일 수정·생성 금지 (조사 전용). baseline 을 고치기 시작하지 마라 — 그건 다음 태스크다.
- `00-planning/`·`10-decision.md`·`20-spec/`·`30-work.md` 분석은 조사 B 의 몫 — 겹치는 관찰이 있으면 리포트 미결란에 한 줄만 남겨라.
- 발견지도에 없는 사실을 발명하지 마라. 트랜스크립트 재해석으로 새 발견을 만들지 마라.

## 8. 검증

```
git -C /Users/kknaks/orca/workspaces/mediness-mediness/interview1-update-spec status --porcelain → 출력 0줄 (diff 0 확인) + 리포트 파일 존재 확인
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
  --to term_915b3ecb-68dd-4d26-98f7-ef3f645318fb --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_915b3ecb-68dd-4d26-98f7-ef3f645318fb \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_915b3ecb-68dd-4d26-98f7-ef3f645318fb --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
