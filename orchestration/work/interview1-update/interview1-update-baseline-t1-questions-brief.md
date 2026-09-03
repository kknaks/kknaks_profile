# [planner] baseline T1 — D-4 질문지 원장 반입 (`00-baseline/interview/` 신설)

너는 **sc-ax `planner` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-interview/orchestration/roles/sc-ax/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/interview1-update-spec`
base 브랜치: `origin/sc-ax` → 최종 PR 대상 `sc-ax` (PR 은 코디네이터가 올린다)

이 워크트리에서 네가 앞서 조사 A(baseline 현황)를 수행했다 — 그 맥락을 그대로 쓴다.
이번에는 조사가 아니라 **실작업**이다. 단, 범위는 §7 이 정한 것뿐이다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-interview/references/2026-08-28-sc인터뷰-경영관리부/관리자인터뷰-1차-질문지.html` ← 반입할 원본. `<script>` 안 `const D = [...]` 가 본체다 — 섹션(t·m·bridge·note)과 문항(n·q·p·w·warn) 구조.
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-interview/orchestration/work/interview1-update/survey-baseline-report.md` ← 네가 쓴 조사 A. baseline 규약(실명 금지·S 대장·changelog 형식)의 근거가 여기 있다.

**기대는 개념** — 사용자 결정 (코디네이터 전달):
- 질문지가 **D-4 의 원장**이다. 회차 결과는 이후 태스크에서 이 원장에 대조해 쌓는다 — 이번 태스크는 원장 반입까지만.

## 2. 배경 / 무엇을 바꾸나

baseline 은 `06-scope.md` D-4·`08-metrics.md`·`09-roadmap.md` 세 곳에서 "D-4 면담"에 정량 기준선까지 걸어 놨는데, 정작 질문지 실물과 회차 진행 대장이 baseline 에 없다. 질문지는 sc-interview 레포에 html 로만 있다. 이를 md 로 뽑아 `00-baseline/interview/` 에 정식으로 앉힌다 — `request/`(고객사 발송 문서) 와 대칭인 「고객사 대면 도구」 자리다.

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

해당 없음.

## 4. 먼저 읽을 핵심 파일

- `products/sc-ax/00-baseline/request/README.md` — 대칭 모델. 대장(README) + 상세 문서 구조와 머리말 형식을 따른다
- `products/sc-ax/00-baseline/06-scope.md:116-124` — D-1~D-5 표. D-4 행이 이 원장을 가리키게 된다
- `products/sc-ax/00-baseline/00-overview.md` — 문서 맵·구조 결정 5번(실명 금지) · 새 문서 반입 시 문서 맵 갱신 여부 확인
- `products/sc-ax/00-baseline/C-changelog.md` — 개정 행 형식 (S13 행이 모델)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `products/sc-ax/`

## 6. 구현 단계

1. `00-baseline/interview/01-questions-mgmt-1.md` 생성 — html `D` 배열의 **충실한 md 변환**:
   - 도입 script(인사·취지·녹음 동의 안내) 포함 — 진행 도구이므로 살린다
   - 섹션별 배분 시간(m), bridge, note 보존
   - 문항마다 번호(n)·질문(q)·파고들 것(p)·왜 묻나(w)·주의(warn) 전부 보존 — **문항 번호는 회차 닫힘 점검이 인용하는 키다. 바꾸지 마라**
   - **실명 → 역할명 치환**: 진행자 실명 → 「수행사 기획 담당」, 문항 속 피면담자 실명(예: 2-2 의 과장 실명) → 「법무파트 담당자」 류. 치환한 곳은 문서 머리말에 규칙 한 줄로 밝힌다
   - 머리말: 무엇(1차 관리자 질문지) · 사용 회차(2026-08-26 경영관리부 1차) · 원본 위치는 「수행사 내부 보관」 으로만 (sc-interview 레포 경로를 적지 않는다)
2. `00-baseline/interview/README.md` 생성 — **D-4 원장**:
   - 이 폴더가 무엇인지 (D-4 면담의 질문지·회차 대장. `request/` 와 대칭)
   - 회차 대장 표: 1행 = 2026-08-26 경영관리부 1차 관리자 (질문지 `01`, 상태 「실시 — 결과 반영 대기」). 닫힘 현황 상세는 **비워 두고 자리만** — 다음 태스크가 채운다
   - `08-metrics.md` 가 D-4 에 걸어 둔 정량 문항 셋(O-1·O-3·H-1 횟수)이 다음 회차에서 물을 것임을 명시
3. `06-scope.md` D-4 행에 원장 링크 추가 — **한 줄 수정만**. D-4 진행 상태 서술 신설은 하지 않는다 (다음 태스크)
4. `00-overview.md` 문서 맵이 폴더 단위 등재를 요구하면 `interview/` 행 추가 — 요구 형식이 불명확하면 고치지 말고 §9 로 물어라
5. `C-changelog.md` 최상단에 개정 행 1건 — 「D-4 질문지 원장 반입 (`interview/` 신설)」

## 7. 범위 제약 — 하지 말 것

- 이번 태스크의 수정 범위는 **`00-baseline/interview/` 신설 + `06-scope.md` D-4 행 링크 1줄 + `C-changelog.md` 1행 + (필요시) `00-overview.md` 문서 맵 1행** 뿐이다.
- 회차 결과 반영(S14 등재·닫힘 현황·PR 신설·b/c 갱신)은 **하지 마라** — 전부 다음 태스크다.
- 질문지 내용을 요약·개선·재구성하지 마라 — 원본 충실 변환이다.
- 트랜스크립트·회의록·발견지도 내용을 이 문서들에 들이지 마라.

## 8. 검증

```
python3 scripts/lint-pipeline.py --strict → products/sc-ax/ 범위 ERROR 0 (타 제품 기존 WARN 은 무관 분리)
grep -rn "조상아\|권예은" products/sc-ax/00-baseline/interview/ → 0건 (실명 치환 확인)
git -C /Users/kknaks/orca/workspaces/mediness-mediness/interview1-update-spec status --porcelain → 변경 파일이 §7 범위 안뿐인지 확인
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
