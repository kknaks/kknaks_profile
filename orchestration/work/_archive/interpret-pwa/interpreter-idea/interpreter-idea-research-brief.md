# [researcher] 통키 요금제 설계 보고서 — 처음부터 (`pricing-design.md`)

너는 **interpret-pwa `researcher` 워커**다. 앞 맥락은 없다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/roles/interpret-pwa/researcher/` (`role.md` 외 4개)
작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토` (코디 워크트리 탑승) · ⚠ PUBLIC 레포 — 키 · 실명 금지.

## 0. 이 작업의 규칙 — 가장 중요

- **모든 숫자에 근거를 단다.** 근거 종류는 넷뿐: 「실측」(Soniox usage-logs) · 「공식」(Soniox 문서 URL) · 「정책 · 사용자 지정」(아래 §2 에 적힌 것만) · 「계산」(식을 같이 적는다). **이 넷에 없는 숫자는 쓰지 마라** — 필요하면 「정할 것」으로 올린다.
- **가격은 결과다.** 가격 · 마진 · 포함량을 먼저 정하지 마라. 아래 §3 플로우 5단계에서 역산으로 나와야 한다.
- 특정 병원 · 지점 데이터는 쓰지 않는다(이번 요금제와 무관).
- 사용자 용어(「상담 1발화」 · 「간단 통역 1발화」 · 해피/워스트)의 뜻은 §2 그대로. 바꾸거나 늘리지 마라.

## 1. 원천

- Soniox 공식 단가: https://soniox.com/pricing · 과금 규칙 · 한도: `reference/2026-11-12-interpreter-idea/useage.md` §2 · §3 (URL 은 거기서 다시 확인)
- **실측 2건** — Soniox `GET https://api.soniox.com/v1/usage-logs` (키 = `/Users/kknaks/git/toy_pr2/interpret-pwa/.env` 의 `SONIOX_API_KEY`, **출력 · 기록 금지 · 읽기 조회만, 새 호출 금지**), 2026-11-12 UTC, `client_reference_id`:
  - `cost-probe-2026-11-12-d` = **상담 1발화**(325자 · ko→zh)
  - `cost-probe-2026-11-12-real` = **간단 통역 1발화**(48자 · ko→en)
  - 토큰 6종 · `cost_usd` 를 로그에서 다시 가져와 쓴다. (`…-synth` 는 입력 음성 합성 비용 — 원가 아님)
- 실측 문장 · 지금까지의 함수 정리: `reference/2026-11-12-interpreter-idea/pricing-function.md` — **§1 · §1.5 · §2 · §4 만 참고 자료.** §3 이후(그래프 · §5 ~ §10)는 근거 없이 쓴 것이라 **쓰지 마라.** 이 파일은 고치지 마라.
- 통키 코드(context 생성 · 세션 구조): `/Users/kknaks/git/toy_pr2/interpret-pwa` main `17c26b5` — `back/app/service/glossary.py` · `back/app/service/interpret/session.py` · `soniox.py` · `langs.py`

## 2. 사용자가 정한 것 (이것만 「사용자 지정」으로 쓴다)

| 항목 | 값 |
|---|---|
| 요금제 후보 | **시간제 · 토큰제 · 정액제** 3개를 비교 |
| 한 달 | **30일**(쉬는 날 없음) · 하루 근무 **12시간** |
| 하루 실사용 시간 | 범위 **1 ~ 12h** (해피 1 · 워스트 12) |
| 동시 사용 대수 | 범위 **1 ~ 5** (해피 1 · 워스트 5) |
| 상담 비율 | **0 : 100** (해피 0% · 워스트 100%) |
| 무발화 정책 | **무발화 1분이면 세션 종료** — 말 없는 연결은 원가에서 뺀다 |
| 연결 고정비 | **context 가 가장 큰 언어 기준으로 통일** (번체 zh-Hant — 토큰 수는 실측 없음 → 코드로 글자 수를 세고 실측 언어들의 글자당 토큰으로 추정, 「추정」 표기) |
| 분석 방법 | **독립변인 1개만 움직이고 나머지는 해피 세트 / 워스트 세트에 고정** — 변인별 범위 |
| 데이터 | 실사용 패턴 데이터는 **없다** — 극값 차이가 큰 것은 그대로 보인다 |

- 「1시간」의 정의, 시간당 세션 · 발화 수의 범위처럼 위에 없는 변인은 **실측 시간 · 정책에서 계산으로 끌어낼 수 있으면 식과 함께**, 아니면 「정할 것」.
- 마진율은 사용자가 정하지 않았다 → **변수 m** 으로 두고 30 · 50 · 70% 를 비교용으로 계산(「비교용」 표기).
- 「월 2만원」은 대표 투표 결과(4명 전원 「잘만 되면 월 2만원도 가능」) — 참고선으로만. 목표가로 쓰지 마라.

## 3. 보고서 플로우 (이 순서 · 절 제목 그대로)

1. **원가 함수** — 토큰 × 단가 식 · 원 단위 식 · 실측 2건 대입 = `cost_usd` 일치 확인 표
2. **변인 정의와 범위** — 변인 표(해피 · 워스트 · 근거). 계산으로 낸 범위는 식
3. **원가 범위** — 변인 1개씩 · 나머지 해피 / 워스트 고정 → 월 원가 구간(표 + 그래프). 어느 변인이 가장 크게 흔드나
4. **요금제 구조 정의** — 시간제 / 토큰제 / 정액제의 매출 공식. **가격은 변수 p** (정액제 포함량이 있다면 그것도 변수)
5. **요금제별 가격 역산** — 3단계의 같은 범위에 4단계 공식을 넣어, 범위 안 모든 조건에서 마진 m 이상 남는 **최저 p** 를 요금제마다 구한다. 변인별 「매출 vs 원가」 그래프 · 손익분기
6. **마진율별 가격표** — m = 30 · 50 · 70%(비교용) × 요금제 3
7. **비교** — 세 요금제를 고객 쪽 가격 · 적자 위험 · 어느 변인에서 깨지는가로. **추천은 「안」으로만**, 결정 문장 금지
8. **근거 없는 것 · 조사할 것** — 범위를 좁히려면 어떤 데이터가 필요한가

그래프: matplotlib PNG(범례 필수 · 축 제목 · 단위 · 한글 폰트 `AppleGothic`). 숫자 · 그래프는 전부 스크립트가 뽑는다(손 편집 금지).

## 5. allowed_paths

- `reference/2026-11-12-interpreter-idea/pricing-design.md` (새 파일) · 같은 폴더의 `pd-*.png` (새 그래프)
- `orchestration/work/interpreter-idea/pricing-calc/` (계산 · 그래프 스크립트 · 원시 응답 JSON — 키 없이)
- 그 외 read-only. Soniox **새 호출 금지**(usage-logs 조회만). 운영 서버 접근 금지.

## 8. 검증

- 보고서의 모든 숫자에 근거 표기가 붙어 있는지 스스로 grep · 목록화해 보고에 첨부(근거 없는 숫자 0).
- 스크립트 재실행 → 보고서 숫자 diff 0.
- 키 문자열 0 · 실명 0.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_0065c22f-b4a3-475e-bf78-3b62bac38378 --from term_5e3d8a95-c548-4e88-b0a0-31254bf0dfb5 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_0065c22f-b4a3-475e-bf78-3b62bac38378 \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_0065c22f-b4a3-475e-bf78-3b62bac38378 --text "[질문] researcher: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
