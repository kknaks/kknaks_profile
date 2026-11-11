# [planner] fix 스펙 3판 — 문서 리뷰 WARN 11건 반영 + 작업 계획(WP) 작성

너는 **day `planner` 워커**다. 앞 판(같은 터미널)의 맥락이 있더라도 아래 파일을 기준으로 한다.

- 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/roles/day/planner/role.md` (+ 같은 폴더 문서)
- **문서 리뷰 리포트(이번 판이 고칠 것)**: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/review-doc-1-report.md`
- 네 리포트: `…/work/fix/spec-1-report.md` · `spec-2-report.md`(둘 다 「코드 영향」 절)
- 사용자 원천: `…/work/fix/e2e-feedback.md` · 결정 `…/work/fix/_RESUME.md` §2
- 코드(읽기): `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix` — `AGENTS.md` 먼저

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/fix-spec`(1 · 2판 미커밋 위에 이어서). 커밋 · push · PR 금지.

## A. 리뷰 WARN 반영 (판정 WARN · FAIL 0)

W1 ~ W11 과 「조용히 통과하는 자리」 1 ~ 6 을 리포트의 「고칠 것」대로 반영한다. 코디가 정한 것:

| 지적 | 이렇게 |
|---|---|
| **W2** 통역 출처 | 「interpret-pwa back 을 바탕으로」 · 「사전 = interpret-pwa 시드 사본」 = **사용자**(5번 원문 「번역 플로우는 … interpret-pwa 에 있어 · 사전도 … interpret-pwa 처럼」 + 조사 결과 통보에 이의 없음). **「전 병원 한 벌 · 병원별 사전 없음」 = 코디 기본값**(사용자가 말한 적 없음) → 확정 목록에서 빼고 OQ-A39 ~ A42 와 같은 「기본값 · 뒤집을 수 있음」 줄로. 코디가 `_RESUME` §2 를 같은 말로 맞춘다 |
| **W3a** 시스템 줄 없음 | 코디 기본값 → OQ-C14 신설 · 「사용자」 표기 걷어 냄 |
| **W3b** 채팅 403 글자 · 버튼 | 코디 지시(기존 글자 재사용) · 사용자 통보 · 뒤집을 수 있음 → 표시 + OQ 한 줄 |
| **W3c** 「원장 호출 옆으로」 | 출처를 코디 브리프로 |
| **W3d** 같은 잠금 | OQ 표에 한 줄 |
| **W4** 자리 반납 | 「자리는 잡은 뒤 어떤 경로로 끝나도(예외 · 취소 포함) 한 번만 돌려놓는다」를 계약으로 · A-44 에 갈래 추가(리포트대로) |
| **W5** timeout | Soniox STT · TTS 연결 수립 상한 · 죽은 앱 연결을 끊는 서버 ping/timeout — **원천(interpret-pwa `17c26b5`) 값을 코드에서 찾아** 적는다. 원천이 라이브러리 기본값에 기댄다면 그 기본값과 출처를 적고 「기술 기본값」으로 표시한다(업무 정책처럼 쓰지 않는다) |
| **W6** 상한 6 × 수명 상한 없음 | 판정하지 않는다 — OQ-A43 옆에 「오래 열린 세션이 자리를 쥘 수 있음」을 사용자 질문으로 올린다(수명 · 무활동 상한을 둘지). 기본값은 지금 그대로(상한 없음) |
| **W7** A-47 | 「구현 워커 · 로컬(키 비움)」 · 확인 대상에 `error.code` |
| **W8 · W9 · W10** | 리포트대로 |
| **W11** | ① 조작 중 403 = 본문 안내만(토스트 없음) — 한 화면에 같은 글자가 두 번 나오지 않게. C-A19 에 갈래 추가 ② `chat_group_only` 의 `detail` = 화면에 나오지 않는 내부 문장(앱은 code 로만) ③ 설정 응답에 `chat` 이 없으면 앱은 켜짐으로 본다 |
| 조용히 통과 1 | A-46 시험 조건 = 「듣는 상태 누적 약 3분 20초 이상(올린 오디오 6 MiB 넘게)」 |
| 조용히 통과 4 | 「옅은 빨강」 · 「왼쪽 띠」의 기준 토큰을 앱 `ui/theme.dart` 에 **이미 있는 토큰 이름**으로 적는다(없으면 「구현 때 정함 · 리뷰 눈 확인」으로 두고 지어내지 않는다) |
| 조용히 통과 5 | C-A21 에 「다른 기기 = 다음에 앞으로 올 때부터」 |
| 참고 3 | `spec-000` 형식 칸 표기 정리 |

OQ-A43(상한에 찼을 때 글자)은 사용자 답이 없어 **그대로**(「통역 서버를 쓸 수 없어요」 재사용) 둔다.

## B. 작업 계획(WP)

이 레포는 새 `30-work/work-*.md` 를 만들지 않는다(Delivery Issue 가 SoT). Delivery Issue 등록은 **이번에 하지 않는다**(2차 Delivery 마감과 함께 사용자와 따로 닫는다 · GitHub 에 아무것도 쓰지 마라). 대신 구현 워커 브리프의 바탕이 될 **작업 계획 파일 1개**를 쓴다:

`/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/wp-plan.md`

담을 것:

1. **WP 나눔** — 코드 워커는 `backend`(서버) · `mobile`(앱) 둘이고 **같은 코드 워크트리에서 동시에** 돈다. 그래서 WP 는 경로가 겹치지 않게(`backend/` · `scripts/` · `deploy/` ↔ `app/`) 나눈다. 제안 뼈대(네가 더 낫게 나눠도 된다 · 이유를 적는다):
   - WP-BE-1 채팅 · 알림 서버(그룹 이름 API · `chat` 알림 종류 · 푸시 받는 사람)
   - WP-BE-2 통역 서버(라우트 · 서비스 · 사전 시드 · 상한 · 설정 · 선택 비밀 · 의존성 · 실물 스크립트)
   - WP-APP-1 시술현황 카드(모두 완료 · [귀가 대기] · 확인 필요 표시) + 앱 후속 2건(`version >=` · `calls[].canRecall`)
   - WP-APP-2 채팅 · 설정(403 안내 · 그룹 이름 바꾸기 · 「채팅」 스위치 · 앱 안 배너)
2. WP 마다: 근거 SPEC 절 · 수용 항목 번호 / **고칠 파일을 코드에서 전부 grep 으로 센 목록**(「쓰는 곳 전부」 — 목록 밖에서 FAIL 이 나지 않게) / 새로 만들 파일 / 하지 말 것 / 시험(추가 · 수정할 테스트 파일 · 돌릴 명령 — `AGENTS.md` 규칙대로 · 워커는 자기 테스트만) / 실물 확인 몫(워커 · 코디 · 사용자).
3. **WP 사이 계약** — 앱이 기다리는 서버 응답(API #22 요청 · 응답 · 오류 / 설정 `items` 의 `chat` / SSE `chat_room`)을 필드 단위로 한 표에. 서버와 앱이 같은 표를 본다.
4. **순서 · 의존** — 동시에 돌 수 있는 것 / 먼저 끝나야 하는 것. 통역(WP-BE-2)은 앱 변경이 없다.
5. **통역 원천 가져오기 규칙** — interpret-pwa `origin/main` `17c26b5` 의 어느 파일을 어디로(조사 §7 · 네 2판 「코드 영향」) · 로컬 canonical 은 뼈대 커밋뿐이라 `git -C /Users/kknaks/git/toy_pr2/interpret-pwa show origin/main:<path>` 로 읽는다는 것 · 기록기(`records`)는 가져오지 않는다는 것.
6. **위험** — 깨진 시드 = api 기동 실패(통역 사전 하나가 로그인 · 시술현황 · 채팅을 막는다 — 사용자에게 알릴 것) · `runtime` → `day.public` 경계 · OpenCC × Python 3.13 · Caddy 6MiB · 루프 막힘.
7. 배포 뒤 사용자 실기기 확인 목록(A-46 등)을 한곳에.

## 규칙

- 근거 없는 정책 0 · 화면 문구 지어 넣지 않기 · 영향받는 절 전수 수정 · `log.md`.
- 값(키 · Vault 이름 · IP)은 적지 않는다.
- WP 계획은 스펙을 다시 정하지 않는다 — 스펙에 없는 것을 계획에서 정하면 안 된다(필요하면 스펙을 고치고 계획이 가리킨다).

## 검증 · 보고

```
python3 scripts/lint-pipeline.py --strict     # products/day/ ERROR 0
```

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/spec-3-report.md`
— W1 ~ W11 · 조용히 통과 1 ~ 6 각각 반영 자리(문서:줄) 또는 반영 못 한 이유 · 정할 것(사용자 몫만) · `wp-plan.md` 요약 · lint.

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 값과 다르면 preamble 이 맞다.

끝나면 **두 명령 모두**:

```bash
orca orchestration send \
  --to term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --from term_bf6ad1b2-354a-4423-8fd4-eb60fc4732c8 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "planner 완료: <한 줄>" \
  --body "WARN 반영 N/11 / WP N개 / 정할 것 N건 / lint"

orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

막히면: `orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[질문] planner: <질문>" --enter`
