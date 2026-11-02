# [planner] 조사 B — planning·spec 이 발견 파생을 받을 준비가 됐나 + 보고서 착지 (조사 전용 · diff 0)

너는 **sc-ax `planner` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-interview/orchestration/roles/sc-ax/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/interview1-update-spec`
base 브랜치: `origin/sc-ax` → 최종 PR 대상 `sc-ax` (PR 은 코디네이터가 올린다)

**⚠ 이번 태스크는 조사 전용이다 — 워크트리 diff 0.** 리포 파일을 한 글자도 고치지 않는다.
산출물은 아래 §6 이 지정한 리포트 파일 1개뿐이다.
**같은 워크트리에서 조사 A 워커가 `00-baseline/` 를 병렬로 읽는 중** — 둘 다 read-only 라 충돌은 없지만, 그쪽 범위 분석은 네 리포트에 중복해서 쓰지 마라.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-interview/references/2026-08-28-sc인터뷰-경영관리부/현행업무-발견지도.md` ← 인터뷰 해석의 SoT. **특히 §1 색인의 「파생」 열과 §2 카드의 갈래 표** — R-13~19 · plan-001~007 · 미결 #48~53 이 이번 대조의 기준이다.
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-interview/references/2026-08-28-sc인터뷰-경영관리부/회의록.md` ← 이슈 7건·액션 1건 — 보고서에 들어갈 재료.

**기대는 개념** — 해당 없음.

## 2. 배경 / 무엇을 조사하나

2026-08-26 경영관리부 1차 인터뷰의 발견 31건이 발견지도에 있고, 파생 열이 `plan-001~007`
「바꿀 것」·「답할 것」, R-ID 요구, 미결 번호를 가리킨다. 다음 단계 ② planning 업데이트와
③ 회의결과 보고서 작성을 발주하기 전에, **그 착지들이 `products/sc-ax/` 안 어느 문서의 어느
자리인지, 지금 반영 상태가 어디까지인지**를 알아야 한다. 이 조사가 ②·③의 발주 범위를 정한다.

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

해당 없음.

## 4. 먼저 읽을 핵심 파일

- `products/sc-ax/00-planning.md` — planning 층의 구조·규약 입구
- `products/sc-ax/00-planning/plans/plan-001-work-management.md` ~ `plan-008-…` — 발견지도 파생이 가리키는 착지. 「바꿀 것」·「답할 것」 절이 실제로 있는지, 인터뷰 결과 대기 표시가 있는지
- `products/sc-ax/10-decision.md` — DEC-004·DEC-005 등 발견지도가 검증 대상으로 지목한 결정
- `products/sc-ax/20-spec.md` + `20-spec/spec-001~008` — plan 과 spec 의 대응 관계, X-08·X-16·X-19·X-20·X-27 류 항목이 여기 있는지
- `products/sc-ax/30-work.md` · `log.md` · `README.md` — 작업 관리·기록 규약 (보고서가 앉을 자리 후보)
- `products/sc-ax/00-baseline/present/kickoff-report/README.md` — 기존 「보고서」 산출물의 형태 (baseline 내용 분석은 하지 마라 — 형태만)

## 5. allowed_paths — 이 밖은 건드리지 마라

- (read-only — 리포 파일 수정·생성 금지. 산출물은 §6 의 리포트 파일 1개뿐)

## 6. 조사 단계

1. `00-planning/`(plans·policies·screens·stories) · `10-decision.md` · `20-spec/` · `30-work.md` 의 구조와 문서 규약을 파악한다.
2. **파생 대조표를 만든다**: 발견지도 §1 파생 열 + §2 갈래 표의 항목(R-13~19 · plan-001~007 착지 · DEC-004/005 · 미결 #48~53 · X-08/16/19/20/27 · V-08)마다 → 실제 착지 문서·절이 존재하는가 / 이미 반영됐는가 / 비어 있는가. 근거는 `문서:절`.
3. 발견지도가 가리키는 착지 중 **`products/sc-ax/` 안에 존재하지 않는 것**(예: `ax/컨펌-미결사항.md` 류 외부 경로, R-ID 대장, 전환-단계설계)을 목록으로 분리한다 — 어디 있는지 아는 척하지 말고 「리포 내 부재」로만 기록한다.
4. ③ 회의결과 보고서의 착지를 제안한다: 기존 규약(kickoff-report 형태, log.md, 30-work 등)에 비춰 보고서가 앉을 자리·형식 후보 2~3개와 각각의 근거.
5. 리포트를 `/Users/kknaks/orca/workspaces/kknaks_profile/sc-interview/orchestration/work/interview1-update/survey-planning-report.md` 에 쓴다. 형식:
   - 요약 (5줄 이내) / planning·spec 문서 지도 (문서별 한 줄) / 파생 대조표 / 리포 내 부재 목록 / 보고서 착지 제안 / 미결·질문

## 7. 범위 제약 — 하지 말 것

- 리포 파일 수정·생성 금지 (조사 전용). plan 문서를 고치기 시작하지 마라 — 그건 다음 태스크다.
- `00-baseline/` 내용 분석은 조사 A 의 몫 (kickoff-report 형태 확인만 예외) — 겹치는 관찰이 있으면 리포트 미결란에 한 줄만 남겨라.
- 발견지도에 없는 사실을 발명하지 마라. 반영 여부 판단마다 근거 절을 붙여라.

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
