
# [researcher] 사전을 고유명사만으로 — 170개 나누기 · 줄인 사전 실물 시험 (D-71)

너는 **interpret-pwa `researcher` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/roles/interpret-pwa/researcher/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)


## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md` **D-71**(사전에는 고유명사만) ← 이번 일의 근거
- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/work/tongky-quality-re1/research-translation-terms-report.md` ← 앞 조사(시험 방식 · 스크립트는 `…/scratchpad/probe2/` — 그대로 다시 써도 된다)
- 시드 `/Users/kknaks/orca/workspaces/interpret-pwa/tongky-quality-re1/back/seed/glossary.json`(`.10` · 170 term) · `/Users/kknaks/orca/workspaces/interpret-pwa/tongky-quality-re1/back/app/service/glossary.py`(`build_context`)
- SPEC `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/para/projects/summer-star/interpret-pwa/20-spec/spec-001-interpret-pwa.md` §4.2 · §4.5 · §4.6(시드 · context 규칙 — 읽기만)

## 2. 할 일

**A. 170 term 나누기 표** — 갈래 셋: ① 고유명사(상표 · 제품 · 장비 · 등록 시술 이름 — 예 울쎄라 · 써마지 · 쥬베룩 · 리쥬란 · 나보타) ② 일반 낱말 · 분류 이름(예 혈관 · 색소 · 제모 · 레이저 · 주름 · 미백 · 재생 · 딥클렌징 · 여드름 전용) ③ 애매(예 성분명 PDRN · PN · PLLA · 기법명 실리프팅 · 물광 · HIFU · RF — 일반 번역으로 충분한지 갈림). term 마다: id · ko · 갈래 · 한 줄 이유 · zh 이름. ③ 은 **사용자가 판단할 수 있게** 짧고 분명하게(수 세기 — 사람 몫은 50개 안쪽이 목표 · 넘으면 묶어서).
**B. 줄인 사전 실물 시험(zh)** — ① 만 넣은 context(정방향 · 역방향 · 별칭은 지금 규칙 그대로 ① 에만)와 ① + ③ context 두 가지. 각각 글자 수 · 짝 수. 문장: 앞 조사의 직원 문장 2개 + 「리쥬란」 · 「나보타」 · 「슈링크유니버스」 등 다른 고유명사가 든 직원 문장 2 ~ 3개(직접 만듦) + 손님 쪽 `热玛吉` 류 1 ~ 2개. 조건마다 최소 6회 · 손님 `超声刀` 질문 뒤 흐름(F2)도. 사전 이름이 나오는 비율 · 틀린 꼴.
**C. 빠진 일반 낱말의 번역** — ② 에서 몇 개(혈관 · 색소 · 제모 · 토닝 · 미백)를 문장에 넣어, 사전 없이 Soniox 가 무엇으로 옮기는지(지금 사전 이름과 비교 · 뜻이 맞는지는 「판단 필요」 로만).

## 3. 하는 법

- 스크립트 · 음성은 **`/private/tmp/claude-501/-Users-kknaks-orca-workspaces-kknaks-profile--------/6b7f4a9c-bfce-487f-8c42-08de89fd57d4/scratchpad/probe3/`** 에만. 코드 · 시드 수정 금지(context 는 복사해 변형).
- Soniox 키: `export SONIOX_API_KEY=$(ssh medi-me "/opt/homebrew/bin/kubectl -n interpret-pwa-prod get secret interpret-pwa-secret -o jsonpath='{.data.SONIOX_API_KEY}'" | base64 -d)` — 그 셸 env 에만.

## 4. 결과물

- 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/work/tongky-quality-re1/research-proper-noun-dict-report.md` — A 요약(갈래별 수) · B 표 · C 표 · 「정할 것」.
- 나누기 표 `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/work/tongky-quality-re1/dict-classification.md` — 170행(사용자 확인용 · ③ 을 맨 위에).

## 5. allowed_paths — 이 밖은 건드리지 마라

- 위 파일 둘 · `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-kknaks-profile--------/6b7f4a9c-bfce-487f-8c42-08de89fd57d4/scratchpad/probe3/`

## 6. 리포트 모양

[문서] · [실물] 표시 · 결정 0 · 키 · 운영 기록 문장 0.

## 7. 범위 제약 — 하지 말 것

- 코드 · 문서 · 시드 수정 금지. 운영 서버 · 사용자 포트 금지(키 읽는 kubectl 한 줄 외).

## 8. 검증

```
질문마다 답 + 공식 문서 URL. 문서에 없는 것은 「문서에 없음」. 결정하지 않고 「정할 것」으로 모은다
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
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_0cdc063d-4b42-4e5f-bc41-65528f81e60f \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_0cdc063d-4b42-4e5f-bc41-65528f81e60f --text "[질문] researcher: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
