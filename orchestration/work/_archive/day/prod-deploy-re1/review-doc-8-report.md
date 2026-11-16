# 리뷰 리포트 — SPEC-001 개정 ⑦ 공개 페이지 · Delivery #245 contract_version 3 (2026-11-12)

대상
- 스펙 워크트리(`kknaksss/prod-deploy-re1-spec-web` · HEAD `8c1d31fe`)의 미커밋 변경
  - `spec-001-login-session.md`(개정 ⑦ · §2 「화면 라우트」 한 줄 · `last_updated`)
  - `60-release/app-store-preparation.md` §7-2 #1(:371)
  - `log.md` 1행
- Issue CENTURION_DAY#245 본문(meta `contract_version=3` · plan_digest `846f8502…` · 라벨 `delivery-plan:review`)
- 요약: `delivery-web-report.md` 「수정 8」
- 코드 대조: `CENTURION_DAY/prod-deploy-re1`(PR #244 head = `1d4ccfba`) — `cf8f5037`(W6 · W7) · `1d4ccfba`(P2) · 미커밋 P1 파일

## 판정: WARN

FAIL 은 없다. SPEC-001 ⑦ · 60-release #1 · log 는 맞다. #245 v3 의 Target Delta 4줄(W6 · W7 · P1 · P2)은 스펙 · 코드와 맞고, Acceptance A7 ~ A10 으로 하나씩 판정할 수 있다. 고객 값 · 키 · 연락처도 없다. 다만 A1(앱 카드 테두리)은 계약에서 빠졌지만 그 코드 커밋 `01bbed49` 는 같은 PR #244 head 에 들어 있다. 이 사실이 #245 에 적혀 있지 않다(W1). 한 구절만 더하면 된다.

검증
- `lint-pipeline.py --strict`: exit 0 · 0 error · 263 warning · `products/day` 0건
- 스펙 diff 추가 줄에 이메일 모양 문자열: 0건
- #245 본문(사람용 + meta 를 URL 디코드한 것): 이메일 0 · 전화번호 모양 0 · `secret|password|token|api_key =` 모양 0 · JWT · `sk-` 모양 0

## ① 스펙 워크트리

| 항목 | 판정 | 근거 |
|---|---|---|
| SPEC-001 개정 ⑦ 노트 | 맞음 | `GET /privacy` · `GET /support` 로그인 없이 · 사용자 승인 2026-11-12 · 본문 = 60-release §6 · 위치 = §2 「화면 라우트」 한 줄. 노트와 본문 줄(:105)이 같은 말이다 |
| §2 「화면 라우트」 줄(:105) | 맞음 | 「세션 검사 · `/login` 이동 없음」은 바로 위 줄 「업무 화면이 세션 없이 열리면 `/login`」의 예외로 읽힌다. 「이 SPEC 은 글자를 정하지 않는다」로 글자 정본을 60-release §6-1 · §6-2 에 남겼다(한 곳 원칙). 앱 「정보」 링크(SPEC-003 ⑫)와 잇는 문장도 맞다 |
| 지어 넣은 계약 | 없음 | 상태 코드 · 머리 메뉴 · CSRF 같은 새 규칙을 쓰지 않았다. CSRF 는 GET 이라 상관없다 |
| 60-release #1(:371) | 맞음 | 「지금」 칸에 「구현 중(fe-3)(사용자 승인 · 원천 DAY-SPEC-001 개정 ⑦)」만 더했다. 담당 · 막는 것은 그대로다. 「ASC 등록 · 페이지 502」도 남았다. prod 배포 전이라 맞다 |
| `log.md` | 맞음 | 2026-11-12 `spec-change` · `DAY-SPEC-001` 1행 · 요약 1줄 · PR 칸 형식이 위 행들과 같다 |
| frontmatter | 맞음 | `last_updated` 2026-11-12. `status: stable` · `version` 그대로 |

## ② Delivery #245 v3

### Target Delta 4줄 ↔ 스펙 · 코드

| 줄 | 스펙 | 코드 | 판정 |
|---|---|---|---|
| W6 연쇄 상세 결과 판 바로 반영 → 신호 | SPEC-002 ⑱ ⑤ · 규칙 28(PR #934 · `cf412e2e`) | `cf8f5037` `services/emr_sync.py` `_apply_detail` — 첫 상세(새 「방 배정」 찾은 조회)와 마지막 확인 상세 둘 다 `apply_visit_tasks`(일정 조회와 같은 경로)로 반영. 시험 `test_board_room_chain.py::test_연쇄_신호_직후_판에_새_방배정_행과_점유가_보인다` · `…겹쳐도_작업_행은_한_번만` | 맞음 |
| W7 반영 대기 중 [복귀하기] 숨김 · 409 `conflict` | ⑱ ⑥ · 규칙 22 · 29 · 매트릭스 :648 | `cf8f5037` `board_rules.py` `room_return_block` 3번째 검사 `conflict if v.id in reflecting`(순서 = 판에 없음 → 점유 아님 → conflict). 시험 `test_연쇄_도중_반영_대기면_복귀는_꺼지고_확인_뒤_켜진다`. 「토스트 글자 OQ-48 열림」도 스펙과 같다 | 맞음 |
| P1 `/privacy` · `/support` 로그인 없이 · 본문 = §6 그대로 | SPEC-001 ⑦(이번 미커밋) | 코드 워크트리 **미커밋**: `routers/public_pages.py`(세션 · CSRF 의존성 없음 · `session=None`) · `main.py` 라우터 등록 · `templates/public/privacy.txt` · `support.txt`. 두 txt 를 60-release §6-1(:251-293) · §6-2(:323-347) 코드 블록과 `diff` 하면 **글자 같음**. 시험 `test_public_pages.py`(세션 없이 200 · 본문 줄 = 원문 줄 · 세션 쿠키 · HX 요청에도 같은 페이지 · 연락처 = 지원 메일 하나) | 맞음(미커밋 — 참고 1) |
| P2 앱 「정보」 → `/privacy` 외부 브라우저 | SPEC-003 ⑫ U-16 · A-27 | `1d4ccfba` `shell.dart` · `app_flow_test.dart`(고정 주소 `https://day.medisolveai.com/privacy` 를 열었는지 단언) — 7b 리뷰에서 본 것과 같음 | 맞음 |

- `target_specs` = SPEC-002 · 001 · 003. 「검토할 부분」은 baseline `7bdde9f2` 밖(#934 미머지 · ⑦ 미커밋)이고 다음 재결속 = contract_version 4 라고 적었다. 스펙 상태와 맞다.

### A1(디자인)이 빠졌는지 — 계약에서는 빠짐, PR 에는 있음 → W1

- 계약: Target Delta 에 없다. Non-Goal 7 「앱 시술현황 탭 카드 상태 색 테두리 없앰(DAY-SPEC-003 개정 ⑪ · 디자인만)」으로 뺐다. Acceptance · 실행 단계에도 없다. 맞다.
- 코드: 그런데 PR #244 head(`1d4ccfba`) 바로 앞 커밋 `01bbed49 style(app): 시술현황 탭 시술 중 카드 파란 테두리 없앰 (A1)`(`app/lib/ui/board_screen.dart` · `detail_polish_test.dart`)가 같은 브랜치에 있다. #243 계약에도 이 앱 파일은 없다. → W1.

### Acceptance 가 각 항목을 판정할 수 있는지

| A | 판정 가능 | 메모 |
|---|---|---|
| A7 (W6) | 예 | 「다음 10초 조회 전에 판 반영 → 그 뒤 신호(시험)」 — 위 chain 시험이 그대로 판정한다 |
| A8 (W7) | 예 | canReturnRoom false · 화면 버튼 없음 · 409 · op 가 없어지면 다시 보임 — 네 조건 모두 관찰 가능. 「화면에 버튼 없음」은 템플릿이 `canReturnRoom` 하나로 그리므로(`board_parts.html` · review-doc-5 재리뷰) 스냅샷 단언으로 갈음된다 |
| A9 (P1) | 예 | 200 · `/login` 이동 없음 · 본문 = §6 글자(그 밖 글자 없음). 「그 밖 글자 없음」은 페이지 제목 · 바닥글 같은 틀 글자를 빼고 본문 줄만 비교하는 것으로 읽어야 한다 — 시험 `_main_lines` 가 그렇게 한다. 참고 2 |
| A10 (P2) | 예 | 앱 시험 경로가 커밋과 같다(`app/test/ui/app_flow_test.dart`). 실기기 1회는 코디 확인 · Issue 기록으로 판정 |

### 고객 값 · 키 · 연락처

- #245 본문에 없음(위 검증). 공개 페이지 본문에는 지원 메일 하나가 있지만 §6 승인 문안의 글자이고 Issue 에는 싣지 않았다.
- `cf8f5037` 은 `deploy/config/prod.env` 의 관리자 · 데모 계정 두 줄을 바꿨다(값은 보지 않았고 옮기지 않는다). #243 Non-Goal 5 가 「prod.env 의 데모 · 전체 권한 계정은 예외(비공개 레포)」로 허용한 자리라 계약 위반은 아니다. 다만 #245 계약 밖 변경이 #245 이름 커밋에 섞였다 — 참고 3.

## WARN

### W1. A1 코드 커밋(`01bbed49`)이 PR #244 에 있는데 어느 Delivery 에도 적혀 있지 않다
- 위치: #245 Non-Goal 7(`contract.non_goals.7`).
- 근거: review-delivery 는 exact PR head 의 diff 를 계약과 대조한다. 지금 계약은 A1 을 「안 함」으로만 적었다. 그래서 `board_screen.dart` 변경이 계약 밖 diff 로 걸린다. 같은 Issue 의 Non-Goal 0(차트 모달)은 「이미 구현(같은 코드 PR) · 이 Delivery 범위 아님」으로 이 경우를 미리 적어 두었다.
- 고칠 것(택1 · 코디):
  - (가) Non-Goal 7 끝에 「· 이미 구현(같은 코드 PR #244 · `01bbed49`) · 이 Delivery 범위 아님」을 더한다. Non-Goal 0 과 같은 방식이다. 다음 재결속(v4) 때 같이 해도 된다.
  - (나) #244 PR 본문에 「A1 = SPEC-003 ⑪ 디자인 · Delivery 없음」을 적는다.

## 참고(차단 아님)
1. **P1 코드는 아직 미커밋이다.** 지시문의 「커밋된 코드(cf8f5037 · 1d4ccfba)」에 P1 은 없다. 코드 워크트리에 `public_pages.py` · `templates/public/` · `public_page.html` · `test_public_pages.py`(untracked) · `main.py` · `styles/app.css` · `static/day.css`(modified)로 있다. 위 대조는 이 미커밋 상태를 본 것이다. 커밋 뒤 txt 두 파일이 바뀌지 않았는지만 다시 보면 된다. `code_surface.9` 에는 시험 파일 · `static/day.css` 가 빠졌는데, 「수정 후보」라 막을 일은 아니다.
2. **A9 「그 밖 글자 없음」의 뜻.** 페이지에는 `<title>` · 틀 글자가 있을 수 있다. 시험은 본문 영역 줄만 원문과 같다고 단언한다. 지금 문장으로도 판정은 되지만, 「본문 영역에」를 붙이면 리뷰어가 같은 기준으로 읽는다.
3. **code_surface 이름 어긋남.** `code_surface.8` 은 W6 을 `board.py` 라고 적었는데 실제 W6 은 `emr/sync.py` · `services/emr_sync.py` 에 있다(W7 은 `board_rules.py` 맞음). `cf8f5037` 의 `prod.env` 두 줄은 #243 자리다. 이것도 「수정 후보」라 차단은 아니다. v4 재결속 때 맞추면 된다.
4. **Issue 제목**은 아직 「… (DAY-SPEC-002 개정 ⑱)」뿐이다. 「한눈에 보기」 목표 줄은 001 ⑦ · 003 ⑫ 까지 적었다. planner 가 「확인 필요」로 남긴 그대로다. 손으로 바꿀지는 코디가 정한다.
5. 승인은 v2 → `delivery-plan:review` 로 돌아갔다. 코드(`cf8f5037` · `1d4ccfba`)는 이미 커밋돼 있으니, v3(또는 v4) 승인 전까지는 review-delivery 를 돌리지 않는 게 맞다.

## 재리뷰 (2026-11-12 · 수정 9 · #245 contract_version 4)

범위는 수정 9 뿐이다. Non-Goal 7 의 한 구절, 그 밖이 v3 와 같은지를 봤다.

### 판정: PASS

W1 이 닫혔다. 새로 생긴 어긋남은 없다.

검증
- `lint-pipeline.py --strict`: exit 0 · 0 error · 263 warning · `products/day` 0건. 스펙 워크트리 미커밋 3파일은 8 차와 같다
- #245 본문(meta URL 디코드 포함): 이메일 모양 0
- 라벨 `delivery-plan:review` · `execution-plan:ready` · `spec-baseline:ready`

| 항목 | 결과 | 근거 |
|---|---|---|
| W1 Non-Goal 7 | 닫힘 | 사람용 본문 「이번에 하지 않는 것」과 meta `contract.non_goals.7` 둘 다 「… · 이미 구현(같은 코드 PR #244 · 01bbed49) · 이 Delivery 범위 아님」. Non-Goal 0(차트 모달)과 같은 방식이다. `01bbed49` 는 PR #244 head `1d4ccfba` 의 조상이다(`git merge-base --is-ancestor`) |
| 그 밖은 v3 와 같음 | 같음 | 8 차에 받아 둔 v3 본문과 지금 본문을 디코드해 `diff` 했다. 다른 곳은 `contract_version` 3 → 4 · `contract_digest` · `plan_digest`(v4 `962c8c5c…`) · Non-Goal 7(meta · 본문) 뿐이다. Target Delta · Acceptance · 실행 단계 · code_surface · target_specs · baseline(`7bdde9f2`)은 그대로다 |
| 승인 | 사용자 몫 | v4 plan_digest 에 승인 receipt 없음. v3 `846f8502…` 은 대체됐다 |

### 참고(차단 아님)
- 「검토할 부분」 첫 줄(meta `review_surface.0` · 본문 같은 줄)은 아직 「스펙 PR 머지 → 같은 key contract_version 4 로 재결속」이다. 이번에 4 를 썼으니 머지 뒤 재결속은 5 가 된다. planner 도 「확인 필요」로 남겼다. 승인 대상 문장이 낡은 번호를 가리키는 것이라, 사용자 승인 전에 고치거나 머지 뒤 재결속(v5) 때 같이 고치면 된다. scope_delta 「v3 → v4」 줄이 없는 것도 같은 때 정리하면 된다.
- 8 차 참고 1 ~ 4(P1 미커밋 · A9 「본문 영역」 · code_surface W6 파일 이름 · Issue 제목)는 그대로 열려 있다. 모두 차단 아님.
