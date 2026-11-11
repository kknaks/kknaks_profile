# [planner] fix 스펙 개정 2판 — 1판 「정할 것」 확정 반영 + 통역 서버 계약

너는 **day `planner` 워커**다. 앞 판(같은 터미널)의 맥락이 있더라도 아래 파일을 기준으로 한다.

- 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/roles/day/planner/role.md` (+ 같은 폴더 문서)
- 네 1판 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/spec-1-report.md`
- **통역 조사 리포트(이번 판의 근거)**: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/research-interpret-report.md`
- 사용자 원천 · 확정: `…/work/fix/e2e-feedback.md` 5번 · `…/work/fix/_RESUME.md` §2

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/fix-spec` — 1판 변경이 미커밋으로 있다. 그 위에 이어서 쓴다. 범위 `products/day/` 만. 커밋 · push · PR 금지.

2판이 끝나면 문서 리뷰어가 1판 + 2판을 한 번에 본다.

## A. 1판 「정할 것」 — 이렇게 닫는다

| 1판 번호 | 결정 | 누가 |
|---|---|---|
| 1 · OQ-A37 겹침 색 | **(가)** 확인 필요가 바탕을 가져간다(옅은 빨강 + 띠 · 상태 글자 색 유지 · 20분 초과는 띠만 더함) | 코디 기본값(네 추천) — 사용자에게 통보 · OQ 는 「기본값 적용 · 사용자 뒤집을 수 있음」으로 남긴다 |
| 2 · OQ-A37 모두 완료 상자 | 오른쪽 비움 · 마취가 열려 있어도 「시술 모두 완료」 | 같음 |
| 3 · OQ-A38 [귀가 대기] 줄 왼쪽 | 비움(버튼만) | 같음 |
| 4 · OQ-C11 그룹 이름 저장 · 취소 | **(가)** 메시지 수정 모드와 같은 ✓ · ✕ 아이콘(새 화면 글자 없음) | 같음 |
| 5 · OQ-C12 채팅 403 다시 시도 | **앱이 앞으로 올 때도 한 번** 다시 본다(다시 로그인 · 앱 다시 열 때 + 앞으로 올 때) | 같음 — 문서 기본값을 이쪽으로 바꾼다 |
| 6 · M-20 · 7 · M-1 · 8 · M-16 서명 | 열린 채로 둔다(이번 코드에 안 걸림) | — |

OQ 표 · 본문 · 수용 항목이 같은 말을 하게 전부 맞춘다.

## B. 통역 서버 계약 (피드백 5)

**사용자 확정(2026-11-11) — 바꾸지 마라**

- 서버 통역은 **interpret-pwa back 을 바탕으로 DAY 서버에 옮긴다.** 앱은 고치지 않는다.
- 사전 = interpret-pwa 시드 파일 사본(전 병원 한 벌). 병원별 사전 없음.
- Soniox 키 = interpret-pwa 가 쓰는 회사 공용 DAY 키. dev Key Vault 에 **`day-dev-soniox-api-key`** 로 이미 넣었다 → 선택 비밀 이름 규칙 `day-<env>-soniox-api-key` · env 이름은 네가 기존 규칙(`DAY_…`)에 맞춰 정한다.
- **동시 통역 세션 상한 6**(서버 전체).

**코디 기본값(조사 §8 — 사용자에게 통보함 · OQ 로 남겨 뒤집을 수 있게)**

- 통역 기록(interpret-pwa D-41)은 **남기지 않는다.**
- 세션 · 권한 확인은 **연결할 때 한 번**(핸드셰이크). 연결 중 재확인 없음.
- interpret-pwa 시드를 고치면 사람이 PR 로 다시 가져온다(지금 SPEC-003 그대로).
- 앱의 거절 문구는 그대로(앱 무수정).

**네가 쓸 것**

1. 지금 SPEC-003 §3 「통역」 · U-15 · A-14 · D-3 줄이 이미 덮는 것과 빠진 것을 조사 리포트 §3 · §4 · §5 · §7 과 대조해 **서버가 지을 수 있을 만큼** 채운다. 새 SPEC 문서를 만들지 SPEC-003 을 보강할지는 이 레포의 문서 나눔(채팅 = SPEC-004 가 앱 · 서버 계약을 같이 가짐)과 중복이 없는 쪽으로 네가 정하고 이유를 보고에 적는다. 같은 계약이 두 문서에 적히면 안 된다.
2. 서버 계약으로 꼭 들어갈 것:
   - `WS /api/interpret` — 인증(앱 Bearer 세션 · `board` view · accept 전 거절 = close 1008 → 앱에는 핸드셰이크 403) · 쿼리 토큰 · Origin 칸은 두지 않는다(조사 §4 — 통역 사용자는 앱뿐).
   - 메시지 · 오디오 형식 · 언어 7개 · 오류 코드 — **앱이 이미 구현한 것과 필드 단위로 같게**(조사 §3 표). 앱과 다른 줄이 하나라도 생기면 그건 계약 오류다.
   - 동시 세션 상한 6 — 넘을 때 서버가 무엇을 보내고 앱에 어떻게 보이는지를 **앱이 이미 가진 오류 갈래 중 하나**로 정한다(앱 무수정). 맞는 갈래가 없으면 「정할 것」으로 올린다(새 문구를 짓지 않는다). 상한은 설정값으로 바꿀 수 있게.
   - Soniox 키가 없을 때(`no_api_key`) · Soniox 가 거절 · 끊길 때의 동작. 오류 문구에 env 이름 · 받은 값을 싣지 않는다(조사 §1 — 원형은 실었다).
   - 사전: 시드 파일 위치 규칙 · 기동 때 읽기 · 깨진 시드면 기동 실패 · 버전 로그(A-14) · context 를 언어별로 조립하는 방식은 원천 그대로.
   - 배포: 선택 비밀 한 줄 · env 표(`deployment.md`) · 새 의존성(`opencc-python-reimplemented`) · api 는 worker 1 · 배포 중 세션 끊김.
3. **완료 조건(수용 항목)에 실물 확인을 넣는다** — 조사 §7 「시험 방법」: ① 실제 Soniox 로 7개 언어 연결 · 한 언어 왕복 · 멈춤 35초 뒤 두 번째 발화 ② dev 배포 뒤 TestFlight 실기기에서 자막 양쪽 · 번역 음성 · 언어 바꾸기 · 종료 ③ **4분 넘는 세션 1회**(Caddy `request_body 6MiB` 가 WS 에 걸리는지) ④ 키 없는 환경 · 권한 없는 계정. ②③ 은 사용자 실기기 몫으로 표시한다.
4. 조사 「확인 안 됨」 5건은 스펙의 「정할 것 / 구현 때 확인」으로 옮긴다(추측으로 메우지 않는다).

## 규칙 (1판과 같음)

- 근거 없는 정책 0 · 화면 문구 지어 넣지 않기 · 영향받는 절 전수 수정 · 개정 머리말 · `log.md`.
- 값(키 · Vault 이름 · IP · 리소스 ID)은 적지 않는다. 비밀 **이름** · env **이름**만.
- WORK 문서는 이번에도 쓰지 않는다(리뷰 통과 뒤 따로 발주).

## 검증 · 보고

```
python3 scripts/lint-pipeline.py --strict     # products/day/ ERROR 0
```

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/spec-2-report.md`
— A 반영 자리 · B 를 어느 문서에 왜 · 조사 §3 표와 스펙의 필드 대조 결과(다른 줄 0 인지) · 정할 것(사용자 몫만) · 코드 영향(서버 파일 · 설정 · 시험 — WP 가 쓸 수 있게) · lint.

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 값과 다르면 preamble 이 맞다.

끝나면 **두 명령 모두**:

```bash
orca orchestration send \
  --to term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --from term_bf6ad1b2-354a-4423-8fd4-eb60fc4732c8 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "planner 완료: <한 줄>" \
  --body "바꾼 문서 / 정할 것 N건 / lint 결과 / 주의점"

orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

막히면: `orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[질문] planner: <질문>" --enter`
