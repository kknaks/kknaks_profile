# [backend · e2e-2] KOS 문진 제출 500 원인 · 제출 id 위치 · 시험 문진 지우기

같은 터미널 · 같은 맥락(`e2e-1-report.md`). 사용자 허락(11-28): **KOS DEMO 에 문진 다시 제출 1회** · **시험 문진 지우기**.

스택(11340)은 qa 워커가 쓰는 중 — **시작 · 멈춤 · 재시작 금지 · 이 단계에서 워크트리 코드 수정 금지**(리로드로 qa 가 깨진다). 실험은 스크래치 스크립트로(같은 어댑터 · 같은 페이로드 생성 코드를 import).

## 할 것
1. **500 원인**: 스크래치 스크립트로 DAY 와 같은 제출 페이로드를 만들어(`services/questionnaire_kos.py` · `emr/kos/identity.py` 의 생성 코드 그대로 · 값만 출력 안 함) KOS 제출 1회 — 응답 **상태 · 본문 전체 모양**(키 이름 · `className`/오류 이름 · 메시지 — PII 는 가림)을 남긴다. 대상 = DEMO 고객 중 **생년월일이 KOS 에 있는** 사람 1명(오늘 방문 있으면 그 사람 · qa 의 `def4cbab` · `7511bbb0` 방문은 쓰지 마라 — 다른 고객). 500 이면 e2e-1 제출과 페이로드 차이(생년월일 · 성별 · 첫 보기 · INPUT_BOX 건너뜀 · 약관)를 비교해 원인 후보를 한 줄씩. **제출은 이 1회만**(성공이든 실패든 다시 안 함).
2. **제출 id 위치**: 2xx 면 응답에서 id 가 오는 칸(최상위 · `data.questionnaireId` 등)과 내부 legacy 읽기 `id` 가 같은지. 코드 `identity.submit_questionnaire` 가 읽는 칸과 맞나.
3. **시험 문진 지우기**: 이번 제출분 + e2e-1 제출분(`6b0a712a` · 고객 `1b9a7c0c`)을 KOS 에서 지우는 **내부 API** 를 찾아(KOS 웹 HAR · 코드 · 내부 경로 — 공개 open 은 쓰지 마라) 지운다 → 내부 legacy 읽기로 400(없음) 확인. 내부 지우기 경로가 없으면 지우지 말고 「경로 없음」 근거를 적어라.
4. 코드 고칠 것은 **고치지 말고 제안만**: ⓐ `questionnaire_kos.py:105` 오류에 `KosError.name` 싣기 ⓑ 500 인데 KOS 에 저장된 경우 [다시 보내기] 이중 제출을 막는 방법(예: 다시 보내기 전 내부 legacy 읽기로 같은 제출 있나 확인) — file:line 과 바꿀 모양.
5. 끝나면 네 KOS 로그인 해제.

## 리포트
`/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/e2e-2-report.md` — 제출 응답 모양 · 원인 · id 위치 · 지운 것 · 코드 제안. 완료 보고 두 명령(subject 「backend 완료: e2e-2」 · 코디 `term_99b025fc-f3ef-403e-8162-509c41545e2e` — preamble 우선).
