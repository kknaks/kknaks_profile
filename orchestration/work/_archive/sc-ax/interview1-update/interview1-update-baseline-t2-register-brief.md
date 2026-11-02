# [planner] baseline T2 — 경영관리부 1차 인터뷰 결과 등재 (S14 · 정리본 · 회차 대장)

너는 **sc-ax `planner` 워커**다. 역할 문서(`/Users/kknaks/orca/workspaces/kknaks_profile/sc-interview/orchestration/roles/sc-ax/planner/` 5종)와 T1 맥락을 그대로 쓴다.

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/interview1-update-spec`
base 브랜치: `origin/sc-ax` → 최종 PR 대상 `sc-ax` (PR 은 코디네이터가 올린다)

**이번 태스크는 기록 전용이다 — 사실 등재만.** 인터뷰가 확인한 것을 대장·정리본에 적는다.
해석 추가·재분류·baseline 본문(00~10 절) 수정은 전부 다음 태스크다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-interview/references/2026-08-28-sc인터뷰-경영관리부/현행업무-발견지도.md` ← AS-001~031 · §5 회차 닫힘 점검. **여기 적힌 사실만 옮긴다.**
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-interview/references/2026-08-28-sc인터뷰-경영관리부/회의록.md` ← 회의 메타(일시·참석)와 자동 요약.
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-interview/orchestration/work/interview1-update/survey-baseline-report.md` ← 네가 쓴 조사 A. **「원료 배치 제안」 절(S14 행 형식·정리본 구조)과 「갱신 지점 표」(AS→착지 a/b/c)를 그대로 쓴다.**

**기대는 개념** — 사용자 결정 (코디네이터 전달):
- 이것은 **경영관리부 1차 관리자 인터뷰(2026-08-26)** 의 결과 등재다.
- 원문 미반입·역할명만·AS ID 는 정리본 매핑표만 보유 (T1 에서 확립한 규약 그대로).

## 2. 배경 / 무엇을 바꾸나

T1 이 질문지 원장을 앉혔다. 이제 그 원장 위에 1회차(경영관리부) 결과를 등재한다 —
출처 대장(S14) · 작업 정리본(AS↔baseline 매핑) · 회차 대장 닫힘 현황. 이후 태스크(본문 반영)가
전부 이 등재를 근거로 걸리므로, 여기가 사실 기록의 기준점이 된다.

## 3. 계약

해당 없음.

## 4. 먼저 읽을 핵심 파일

- `products/sc-ax/00-baseline/B-sources.md` — S1~S13 대장. S13 행(한계 명기 방식)이 형식 모델
- `products/sc-ax/00-baseline/_working/survey-dept-status-2026-08.md` — 정리본이 따를 형식 모델 (머리말·역할명 규칙)
- `products/sc-ax/00-baseline/interview/README.md` — T1 이 만든 회차 대장. 닫힘 현황 열이 비어 있다

## 5. allowed_paths — 이 밖은 건드리지 마라

- `products/sc-ax/`

## 6. 구현 단계

1. `B-sources.md` 에 **S14 행 신설** (S13 다음, 시간순):
   - 무엇: 경영관리부 1차 관리자 인터뷰 (2026-08-26) · 전사 원문 + 자동 요약 · 성격 「근거」
   - 한계를 S13 방식대로 명기: ⚠ 관리자 중심 진술(실무자 아님, 표본 편향 S13 과 같은 방향) · ⚠ 정량 기준선 문항을 물었으나 숫자 미확보 (D-4 정량 4건 전부)
   - 원본 위치는 「수행사 내부 보관」. sc-interview 경로·발견지도를 S 로 올리지 않는다 (조사 A 판단 — 발견지도는 다른 레포의 살아 있는 해석 문서)
   - 같은 파일의 인용 규칙·회수 현황 줄에 갱신이 필요하면 최소로만
2. `_working/interview-mgmt-dept-2026-08.md` **신설** — `survey-dept-status-2026-08.md` 와 대칭 구조:
   - 머리말: 작업 자료이며 SoT 아님 · 원본 수행사 내부 보관 · 역할명만 · 반영 상태(본문 반영은 후속 작업)
   - 회차 정보: 일시 · 참석 역할(관리자 2인 · 발화 6명 중 역할 구분은 아는 만큼만) · 회차 성격(D-4 1회차) · 표본 한계
   - **AS ↔ baseline 매핑표** (이 문서의 핵심): AS-001~031 각 행에 발견 한 줄 요약 · baseline 착지(PR/US/A/R/Q/HOLD 또는 「자리 없음 — 신설 대상」) · 구분(a 이미 반영 / b 어긋남 / c 자리 없음). 조사 A 갱신 지점 표를 그대로 옮기되, **판단을 새로 하지 말고 조사 A 결과를 전사한다**
   - 회차 닫힘 점검 요약: 발견지도 §5 그대로 — 닫힘 3 · 절반 9 · 안 닫힘 8 · **D-4 정량(기준선) 4건 전부 미확보, 발견지도가 2차 회차로 넘김** · 질문지에 없던 주제 5개에서 발견 20건
   - 「2차로 넘기는 것」 표: 발견지도 §5 의 해당 표 전사
3. `interview/README.md` 회차 대장의 **닫힘 현황 칸 채우기**: `닫힘 3 · 절반 9 · 안 닫힘 8` + 상세는 정리본 링크. 상태는 「실시 — 결과 반영 대기」 **유지** (본문 반영이 아직이므로)
4. **changelog 는 이번에 쓰지 않는다** — S14 반영 전체가 끝나는 마지막 태스크에서 한 행으로 몬다 (코디네이터 결정)

## 7. 범위 제약 — 하지 말 것

- baseline 본문(00~10 절·A-glossary) 수정 금지. **`B-sources.md` 와 `interview/README.md` 닫힘 현황 칸, `_working/` 신규 1개** — 이 셋뿐이다.
- 발견지도에 없는 사실·해석을 만들지 마라. 조사 A 의 a/b/c 판단을 바꾸지 마라 (의문이 있으면 정리본에 각주로 남기고 §9 로 보고).
- 실명 금지. 급여·계약 금액 등 값은 인용하지 않는다 (00-overview 구조 결정 5).
- 트랜스크립트 원문 인용을 정리본에 옮기지 마라 — AS ID 와 요약만.

## 8. 검증

```
python3 scripts/lint-pipeline.py --strict → products/sc-ax/ 범위 ERROR 0
grep -rn "조상아\|권예은\|정은애\|박소은\|서형석\|이건학\|전창원\|최우영" products/sc-ax/00-baseline/_working/interview-mgmt-dept-2026-08.md products/sc-ax/00-baseline/B-sources.md → 0건
git -C /Users/kknaks/orca/workspaces/mediness-mediness/interview1-update-spec status --porcelain → 변경이 §7 의 셋 + T1 기존분뿐인지
```

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
