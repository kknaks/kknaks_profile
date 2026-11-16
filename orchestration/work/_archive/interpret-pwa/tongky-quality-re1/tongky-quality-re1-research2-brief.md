
# [researcher] Soniox 번역 용어(translation_terms)는 왜 안 먹히나 — 울쎄라 · 써마지 · 美白针

너는 **interpret-pwa `researcher` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/roles/interpret-pwa/researcher/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)


## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/para/projects/summer-star/interpret-pwa/20-spec/spec-001-interpret-pwa.md` 0.9.5 — §4.5(context 모양 · `general` · `text` · `translation_terms`) · §4.6(줄이기 · 언어별 한도) · §5.10 · §5.12(바로잡기) · §5.13 G(agent text)
- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/para/projects/summer-star/interpret-pwa/00-baseline/baseline-001-interpret-pwa.md` 「확인한 사실 (코디 2026-11-14)」 — 「`translation_terms` 는 강제가 아니다」 · 울쎄라 추정 원인
- 운영 코드(main `c7a582f` = 이 워크트리 HEAD 근처): `/Users/kknaks/orca/workspaces/interpret-pwa/tongky-quality-re1/back/app/service/glossary.py`(`build_context`) · `/Users/kknaks/orca/workspaces/interpret-pwa/tongky-quality-re1/back/app/service/interpret/{soniox,session,correct}.py` · 시드 `/Users/kknaks/orca/workspaces/interpret-pwa/tongky-quality-re1/back/seed/glossary.json`(`.10`)
- 앞 조사 `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/work/tongky-quality-re1/research-turn-taking-report.md` 의 시험 방식(합성 음성 · 실시간 속도)
- Soniox 공식: `https://soniox.com/docs/llms.txt` 에서 context(`stt/concepts/context`) · translation · agent text 문서

## 2. 배경 — 코디가 확인한 사실(2026-11-16 운영 기록 · 수치만)

- 직원 「울쎄라」 · 「써마지」(한 → zh) 를 Soniox 가 낸 번역(바로잡기 전 `translation_before` 기준): 영문 `Ulthera` · `Ultherapy` · `Thermage` 12 · **`美白针`(미백 주사) 4** · **사전 이름(`美版超声刀` · `热玛吉`) 0**. 맞게 보인 건 전부 바로잡기가 영문을 갈아 끼운 것.
- `美白针` 은 D-68 배포 뒤 한 세션(15:53)에서만 나왔다 — 같은 날 앞 세션은 영문. 시드에 `美白针` 은 없다(`美白` = 미백 ph-052 만).
- 바로잡기가 `美白针` 을 못 고친 이유는 코디가 확인함(이번 조사 범위 아님).

## 3. 질문

**Q1** 운영 context 를 그대로 넣었을 때, 직원 문장 「울쎄라는 1회 15만 원입니다」 · 「써마지는 1회 10만 원이고 쥬베룩은 1회 5만 원입니다」(한국어 합성 음성 · zh 세션)의 번역에 사전 이름이 나오는 비율(여러 번). 운영 기록처럼 영문 · 다른 중국어가 나오는지 재현되는가.
**Q2** 무엇을 바꾸면 사전 이름이 나오나 — 변수를 하나씩: ⓐ `translation_terms` 를 그 두 짝만 ⓑ 전체 중 순서(앞 · 뒤) ⓒ 짝의 source 꼴(한글만 · 한글+영문 상표 `Ulthera` 등 별칭 · 공식 문서가 권하는 모양) ⓓ `text`(서술 칸)에 「상표는 사전 이름으로」 류 한 줄이 효과 있나(공식 문서가 그런 쓰임을 말하는지 먼저) ⓔ `general` 항목 ⓕ 모델 v6 그대로. 공식 문서가 translation_terms 를 어떻게 설명하는지(강제 여부 · 권장 양 · 형태) 인용.
**Q3** agent text 가 번역에 영향을 주나 — 같은 대화 흐름(손님 zh 질문 → 통키 ko 재생(agent text 로 보냄) → 직원 ko 문장)에서 agent text 켬 / 끔으로 직원 문장 번역 비교. `美白针` 같은 낱말이 나오는 조건이 있는가.
**Q4** 손님 쪽 `超声刀`(zh → ko)가 「초음파기」 로 나오는 것 — 사전 역방향 짝에 `超声刀` 를 넣으면 울쎄라로 나오는가(넣는다면 다른 시술과 겹치는지 시드에서 확인 · 결정은 하지 않음).

## 4. 실물 시험 — 하는 법

- 스크립트 · 음성 파일은 **`/private/tmp/claude-501/-Users-kknaks-orca-workspaces-kknaks-profile--------/6b7f4a9c-bfce-487f-8c42-08de89fd57d4/scratchpad/probe2/`** 에만(레포 안 금지). 코드 워크트리 `/Users/kknaks/orca/workspaces/interpret-pwa/tongky-quality-re1/back` venv · 모듈을 import 해 쓴다(코드 수정 금지). context 는 `build_context` 결과를 복사해 변형한다.
- Soniox 키: `export SONIOX_API_KEY=$(ssh medi-me "/opt/homebrew/bin/kubectl -n interpret-pwa-prod get secret interpret-pwa-secret -o jsonpath='{.data.SONIOX_API_KEY}'" | base64 -d)` — 그 셸 env 에만 · 출력 · 파일 · 리포트 금지.
- 조건마다 같은 문장을 여러 번(최소 5) — 번역이 흔들리므로 비율로 본다.

## 5. allowed_paths — 이 밖은 건드리지 마라

- 리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/work/tongky-quality-re1/research-translation-terms-report.md`
- 시험 파일: `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-kknaks-profile--------/6b7f4a9c-bfce-487f-8c42-08de89fd57d4/scratchpad/probe2/`

## 6. 리포트 모양

질문마다: 답(사실 · 비율) · 근거([문서] URL 인용 또는 [실물] 수치) · 문서에 없음 표시 · 선택지 · 코디 추천. 끝에 「정할 것」. 키 · 운영 기록 문장 0(시험 문장은 위 둘 · 직접 만든 것만).

## 7. 범위 제약 — 하지 말 것

- 코드 · 문서 · 시드 수정 금지. 결정하지 않는다. 운영 서버 · 사용자 포트 · 프로세스 금지(키 읽는 kubectl 한 줄 외).

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
