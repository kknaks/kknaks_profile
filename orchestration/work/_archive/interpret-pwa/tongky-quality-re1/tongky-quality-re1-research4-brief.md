# [researcher] 통키 요금 다시 — 오늘 실기기 세션의 실제 청구액(usage-logs)으로 price.md 갱신

너는 **interpret-pwa `researcher` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/roles/interpret-pwa/researcher/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선`

## 1. 배경 — 사용자 요청

「price.md 내용 업데이트 해 주라. 연결 비용이 과대하게 나왔는데 오늘 우리 측정한 데이터로 요금제 다시 비교할 수 있지 않을까? 마지막 테스트 기준으로 요금 측정할 수 있지 않을까?」

- 11-12 price.md 는 연결 1회(context) = **42.4원**(번체 중국어 최대 · 약 7,576 토큰 추정)으로 놓고 3 ~ 5절 요금제를 계산했다.
- 오늘(11-16) 운영에 시드 `.11` 배포(D-71): context = 고유명사 74개 · 정방향 + 역방향만 → 일곱 언어 6,916 ~ 7,768자(전 약 2만 자). 그 밖에 바뀐 것: STT `stt-rt-v6` · 세 참여자(재생 중에도 STT 송신 · **Soniox agent text 입력 켬** — `input_agent_text_tokens` 과금 여부 미확인) · 끊김 2000 / -0.3.
- 배포(KST 19:19 · UTC 10:19) 뒤 사용자가 실기기로 시험한 세션(운영 기록 · KST):

| 세션 | 언어 | 시작 ~ 끝 | 발화 | 끝 이유 |
|---|---|---|---|---|
| bc701e27 | zh-Hant | 19:20:50 ~ 19:21:37 | 4 | stop |
| e4c67c3f | zh | 19:22:26 ~ 19:25:48 | 17 | stop |
| 11f17f7b | en | 19:25:52 ~ 19:31:00 | 18 | stop |
| 36044aa4 | ja | 19:30:43 ~ 19:32:08 | 2 | stop |
| f5869adc | zh | 19:31:03 ~ 19:31:13 | 0 | error(연결 시간 초과) |
| b7ed7ed2 | zh | 19:31:23 ~ 19:34:11 | 13 | stop |
| 58b03042 | ja | 19:34:14 ~ 19:37:22 | 15 | stop |

- 운영 기록 원본(로컬 · git 제외): `/Users/kknaks/git/toy_pr2/kknaks_profile/reference/2026-11-12-interpreter-idea/records/2026-11-16.jsonl` — 발화 시각 · 원문 · 번역 글자 수를 쓸 수 있다. **문장은 리포트 · price.md 에 옮기지 마라**(수치만).

## 2. SSOT — 먼저 읽을 것

- 갱신 대상: `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/reference/2026-11-12-interpreter-idea/price.md`(git 제외 로컬 파일 · 432줄)
- 그 계산 스크립트: `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/work/_archive/interpret-pwa/interpreter-idea/price-calc/`(sec3 · sec4 · sec5) · 앞 측정 `…/pricing-calc/`(usage-logs 원본 · calc.py) · 설계 `…/pricing-design-v1.md` — **_archive 는 읽기 전용**(복사해서 쓴다)
- 오늘 context 크기: `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/work/tongky-quality-re1/wp33-context-report.md`

## 3. 할 일

A. **실측** — Soniox `GET https://api.soniox.com/v1/usage-logs`(읽기 조회만 · Soniox 새 STT/TTS 호출 금지), `2026-11-16T10:15:00Z ~ 10:40:00Z`. 줄마다 모델 · 시각 · 토큰(입력 텍스트 · 오디오 · agent text · 출력) · cost 항목. 위 세션 표와 시각으로 맞춰 **세션별 STT · TTS 청구액**(맞추기 어려운 줄은 그렇다고 적는다 · 추측으로 붙이지 않는다). 원본은 scratchpad 에 JSON 으로.
B. **연결 1회(context) 실측** — 언어별 `input_text_tokens` · 비용. 11-12 값(42.4원 추정 · zh 실측 6,494 토큰)과 표로. agent text 가 따로 과금되는지(`input_agent_text_tokens` · cost).
C. **price.md 갱신** — 1.1 ~ 1.5 의 연결비 · 실측 대조에 오늘 실측을 더하고(11-12 값은 지우지 말고 「11-12(시드 .6)」 로 나란히), 3 ~ 5절 요금제 계산을 새 연결비로 다시(스크립트 복사본 재실행 · 손 편집 금지). 오늘 실기기 세션 기준 「발화 1개 · 사용 1분 · 세션 1회」 원가와 5.2 마진별 2만 원 포함량 다시. 문서 머리 작성일 줄에 「갱신 2026-11-16」 · 근거 표기 규칙(〔공식〕 〔실측〕 〔계산〕 〔가정〕) 그대로.
D. 짧은 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/work/tongky-quality-re1/research-price-update-report.md` — 무엇이 얼마나 바뀌었나(전 → 후 표) · 정할 것.

## 4. 하는 법

- Soniox 키: `export SONIOX_API_KEY=$(ssh medi-me "/opt/homebrew/bin/kubectl -n interpret-pwa-prod get secret interpret-pwa-secret -o jsonpath='{.data.SONIOX_API_KEY}'" | base64 -d)` — 그 셸 env 에만. 출력 · 파일 · 로그에 키 0.
- 스크립트 · 원본: `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-kknaks-profile--------/6b7f4a9c-bfce-487f-8c42-08de89fd57d4/scratchpad/price2/` 에만.
- 환율 1,400원 · 단가는 price.md 1.1 그대로(공식 페이지가 바뀌었는지 한 번 확인해 다르면 「정할 것」).

## 5. allowed_paths — 이 밖은 건드리지 마라

- `reference/2026-11-12-interpreter-idea/price-v2.md`(새 파일 · price.md 는 고치지 않음) · 위 리포트 하나 · scratchpad `price2/`

## 6. 범위 제약 — 하지 말 것

- 코드 · 시드 · SPEC · DEC · _archive 수정 금지. 운영 서버 · 사용자 포트 금지(키 읽는 kubectl 한 줄 외). Soniox 는 usage-logs 조회만.
- 결정하지 않는다 — 요금제 추천을 바꿔야 하면 「정할 것」으로.

## 8. 검증

```
모든 숫자에 근거 표기. 실측 = usage-logs 원본에서 다시 셀 수 있어야 한다. 계산 = 스크립트 재실행으로 같은 값. 기록 문장 0 · 키 0
```

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
