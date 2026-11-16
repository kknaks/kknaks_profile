
# 재개 노트 — prod-deploy-re1 (day)

**지금(3)**: 코드 커밋 88210079(웹 피드백 · #245) push → PR #244 에 쌓임 · 머지 안 함 · app/ 미추적은 앱 세션 몫(다른 곳에서 커밋 — 사용자)
**지금(2)**: #245 v2 승인(사용자) → planner receipt 적용 중 · backend W4·W5 · frontend W3 발주(2026-11-11) · 스펙 PR mediness#934
**지금**: 스펙 PR mediness#933 · 코드 PR CENTURION_DAY#244(→dev) 올림 · 리뷰 전부 PASS/반영 · **머지 사용자 대기** · #243 v1 승인 안 함
**다음**: #933 머지 → planner 에게 #243 v2 apply(baseline 새 main) → 사용자 v2 승인 · #244 dev 머지(일반) → dev 배포 확인 → prod ff → migrate-prod → deploy-prod Re-run → 운영 연결 등록(KOS IP 허용 뒤)

세팅: `scripts/new-work.sh day prod-deploy-re1` · 설정 SSOT `config/projects/day.json`
코디handle: `term_e62e850f-aae8-4092-a945-6f9406c2af07`

프로젝트·회고·당시 문서의 탐색은 이 폴더의 작업 목차(`README.md`)가 맡는다.
`sync-work-links.py`로 생성하며, 종료 후에도 프로젝트에서 같은 작업을 찾을 수 있어야 한다.

## 워크트리

- `code`: `/Users/kknaks/orca/workspaces/CENTURION_DAY/prod-deploy-re1` (branch `kknaksss/prod-deploy-re1`, base `origin/dev` → PR `dev`)
- `spec`: `/Users/kknaks/orca/workspaces/mediness-mediness/prod-deploy-re1-spec` (base `origin/main` → PR `main`)
- 코디: 이 워크트리 · 브랜치 `kknaksss/day-prod-deploy-re1` · Run `run_e9098fcbf846`

## 1. 지금

열린 것만 둔다. 닫히면 지우고 §5 이력으로 내린다.

- [~] 웹 수정 — 사용자 피드백 `e2e-feedback.md` W1~W5 모으는 중 · W1·W2(차트 모달 medikit)는 사용자 지시로 먼저 frontend 발주 · 나머지는 다 들은 뒤 한 브리프(W3·W5 스펙 변경 · W4·W5 조사)
- [!] **앱 준비(별 세션 · Codex · mobile-* 문서)** 중간: 정식 앱 release 빌드(서명 없음) 성공 · 미정 = 개인정보처리방침/지원 URL · 앱 내 정책 링크 · Soniox 외부 음성 고지/허가 흐름 · 예약 탭 준비중 화면. **M-20(dev.env `DAY_APNS_ALLOWED_APP_IDS` 에 `day.medisolveai` 추가)은 코디 몫** — 데모 푸시 실물 단계 전에(dev 배포 필요)
- [!] **내일(2026-11-12) 사용자 prod TestFlight 테스트 예정**(앱 세션 `mobile-paperwork-registration.md`) — prod 서버가 그 전에 떠 있어야 함(#244 머지 · dev 배포 · prod ff · migrate · deploy-prod · 운영 연결 등록). 운영 내부 API 는 KOS IP 허용 전까지 403
- [ ] **/privacy · /support 페이지** — 문안 확정(앱 세션 · 스펙 60-release §6 · 미커밋 · 지원 메일만 공개 · 심사 연락처/이름 넣지 않음) · **배포와 T1 · T3 · T4 · T5 기술 사실 대조가 서버 코디 몫**(로그인 없이 · day 도메인) — 문안 초안 = 스펙 `products/day/60-release/app-store-preparation.md` §6 · 미정값 §7(운영 주체 · 지원 연락처 · 보관/파기 · 위탁) — **값 확정 뒤 서버 코디가 만들어 배포**. 그 전에 placeholder 공개 안 함
- [!] **앱 등록 끝(앱 세션 · `mobile-registration-report.md`)**: 정식 DAY 0.1.0(1) 업로드 · ASC VALID · 스크린샷 10 · 메타 저장 · 심사 제출 0. **코드 워크트리 미커밋 `app/store/0.1.0` · `app/tool/store_capture/main.dart` = 보존 · 마감 PR 에 같이**(커밋은 app/ 경로 지정). 심사 전 미완: /privacy · /support 본문 · 지원/심사 연락처 · prod 배포 · 예약 탭 · 실기기
- [!] 웹 수정은 #243 범위 밖 — 끝에 Delivery v2 범위에 넣거나 별 Delivery(정할 때)
- [!] 스펙 PR mediness#933(ed831b15 · 3a0dba9c) — 문서 리뷰 2회 반영 · **머지 사용자 대기**
- [ ] 스펙 PR → 머지(사용자) → #243 v2 재결속 → 사용자 승인(v1 승인 안 함 — review W4)
- [ ] backend 끝나면 reviewer 자동 → 코드 PR(prod.env 포함) → dev 머지(사용자)
- [ ] backend — 운영 연결 등록 진입점(`is_demo=false` · 컨테이너 안 `python -m`) · `test_chat_env_contract.py:83` prod 값 확인으로
- [!] **명동점 KOS IP 허용 `<VM IP>`** — 내부 API 전부 403 `IPBlocked`(로그인 · open API 는 됨). 관리자 퇴근으로 못 받음 — 대기(사용자 2026-11-11 「그렇다고 하고 다음으로」). 이 작업은 PR 열린 채 멈춤 · 다음은 웹 수정(별 slug)
- [!] GitHub `prod` Environment · 승인 규칙 — 레포 권한 push 까지라 못 만듦(관리자 필요). 첫 실행 때 규칙 없이 자동 생성
- [!] 운영 연결 값 = 로컬 `~/.config/day/prod-values.local.json` · 시스템 계정 비번 `~/.config/day/prod-kos-system.local` · 운영 open 키 = ax-clinic `scripts/.env` `KOS_API_tenent` — 공개 레포 금지
- [!] 암호화 키 사본 `~/.config/day/prod-encryption-key.local` = Key Vault 와 일치 확인

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-11-11 | 4차는 prod 먼저 → prod 앱 → 수정. slug `prod-deploy-re1` | 사용자 「prod 배포가 젤 급」 · slug 는 코디 |
| 2026-11-11 | `DAY_ADMIN_EMAILS` = <관리자 계정> · `DAY_DEMO_LOGIN_EMAILS` = <데모 계정> | 사용자 |
| 2026-11-11 | prod KOS 시스템 계정 = <관리자 계정> | 사용자 |
| 2026-11-11 | 운영 병원 = 세라미크 명동점(테넌트 끝자리(레포 밖)) · 브랜드 코드 `ceramique` · 방 배정 id = 「방 점유/원장 상담」 | 사용자 「이게 방 배정이야」 · 코드는 코디 |
| 2026-11-11 | 운영 open 키 = ax-clinic `.env` `KOS_API_tenent`(토큰 발급 OK) | 사용자 |
| 2026-11-11 | 운영 등록: 같은 이름 연결이 이미 있고 is_demo 다르면 거절 · 실행 = 코디 · APP_ENV 가드 없음(「환경별 가드 금지」) · env 접두 DAY_SEED_* 재사용 안 함 · 비밀은 표준입력 | 리뷰 W 뒤 코디 결정 |
| 2026-11-11 | 머지 · Delivery #243 마감은 작업 끝에 한꺼번에 — 웹 수정도 같은 slug · 같은 브랜치 · 같은 PR(#244)에 쌓는다. 그때 #933 머지 → #243 v2 재결속 · 승인 · 마감 | 사용자 「이번 pr 합칠 때 다 닫으면 되잖아」 · 「같은 pr 같은 작업」 |
| 2026-11-11 | 차트 모달: 세 칸 높이 = 글 2줄 · 넘치면 칸 안 스크롤 · **작성자 회색 글은 화면에서 뺀다**(SPEC-002 :325 · 규칙 32 「줄마다 마지막 저장 계정」 문장은 문서 정리 때 고친다) | 사용자 「높이 다 2줄로 맞추고 넘어가면 스크롤」 · 「이게 보여 줄 필요가 있냐고」 |
| 2026-11-11 | W3 방 옮기기 목록: 글자 「비어 있음」 / 「배정됨」 · 배정됨 = 오늘 다른 방문이 그 방에 있음(판 카드 · 점유로 잡은 방 · 접수 중 방 있음 · 귀가 대기 · 같은 고객 다른 방문 포함) · 빈 방 먼저 → 배정됨(각 묶음 안 room.order) · 배정된 방도 고를 수 있음 | 사용자 「비어 있음 / 배정됨으로 나머지는 추천으로」 |
| 2026-11-11 | W4 점유 이동: 이벤트 연쇄 — add-flow-tasks 응답 → 그 예약 상세 조회로 새 「방 배정」 sequence → 바로 change-tasks-room 2건 → 바로 상세 조회로 확인. 주기 조정 없음 · 10초 조회는 KOS 웹 변경 받기용으로만 | 사용자 「응답 오면 다시 api 요청 · 이벤트 기반」 · 「그거라고」 |
| 2026-11-11 | W5 복귀: [복귀하기]만 「방 배정」 DELETE(complete:false → cancel-flow-tasks reason DELETE · KOS 웹 순서) · [귀가 대기]는 CANCEL 유지 · 지운 행도 사본에 남겨 원래 방 판정(규칙 33) · 확인 = 조회에서 사라짐 · 기존 CANCEL 행 그대로 · 데모 실물 1회 | 사용자 「삭제라고」 · 「나머지는 추천으로」 |
| 2026-11-11 | 차트 모달 담당자 줄 = 아바타 · 이름 · 직군(오른쪽) · 직군 둘 다면 글자 없음(미결 그대로) | 사용자 「아이콘 이름 직군으로」 |
| 2026-11-11 | Soniox prod = dev 키 · KOS 주소 = dev 와 같음 · 암호화 키 로컬 사본 둠 · 운영 연결 = 운영용 진입점(is_demo=false) | 코디 기본값(사용자 「알아서」) |

뒤집힌 결정은 지우지 않는다. ~~취소선~~ 을 긋고 같은 행에 뒤집은 날짜와 사유를 남긴다 —
지우면 왜 그렇게 갔는지가 사라져서 같은 논의를 다시 한다.

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| planner | `term_c4381756-d7e6-4556-923a-c9e239892740` | `task_f2c97f2efd76` | `ctx_5b5c85bebccd` | `prod-deploy-re1-spec-brief.md` | 완료 — #243 발행 · `delivery-report.md` |
| reviewer_doc | `term_483a198e-c87e-442c-be28-620ce9692a0f` | `task_1c62266a714f` | `ctx_f48ffb293e81` | `prod-deploy-re1-review-doc-brief.md` | 완료 — WARN 6 · `review-doc-1-report.md` |
| planner(수정 1) | `term_c4381756-d7e6-4556-923a-c9e239892740` | — | — | 터미널 send(W1~W6) | 진행 |
| backend | `term_662db7ba-7727-4b8a-b65a-fde2f6119683` | `task_e2323316132a` | `ctx_959f08430ef1` | `prod-deploy-re1-be-brief.md` | 완료 — `be-1-report.md` · 1181 passed |
| reviewer(code) | `term_58369002-ab53-4e14-943b-1959a2dc71d4` | `task_003fb4c2ff55` | `ctx_b475245d68fe` | `prod-deploy-re1-review-brief.md` | 완료 — 재리뷰 PASS |
| frontend(W1·W2) | `term_79355e15-a622-4c93-8d81-eb35e37177fb` | `task_589babd1e1e8` | `ctx_4a9cf554e87d` | `prod-deploy-re1-fe-brief.md` | 진행 — 차트 모달 · 셀렉터 medikit |
| mobile(A1 테두리) | `term_673fbaad-f2e5-4915-8835-e0035563e1ef` | `task_e027a841a369` | `ctx_5db84adabd0d` | `prod-deploy-re1-mobile-border-brief.md` | 진행 |

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.** 워커 보고는 dispatch preamble 의 값을 따르므로
여기 옛 핸들을 남겨 두면 어느 것이 산 것인지 판단이 안 된다.

## 4. 산출물

- spec PR: <링크>
- code PR: <링크>
- 리포트: `<review-*-report.md>` · `<research-*.md>`
- 커밋: `<sha>` — <한 줄>

## 5. 이력 (최신이 위)

- `2026-11-12` Unlisted 근거(코디 확인): Apple https://developer.apple.com/support/unlisted-app-distribution/ 「Your app's distribution method will change to Unlisted App … and will apply to any future versions of the app.」 · 신청서(https://developer.apple.com/contact/request/unlisted-app/ · 사용자 화면) 동의 문구 「Once switched to unlisted app distribution, the app cannot be changed back to public or set to private app distribution.」
- `2026-11-12` **앱 심사 제출 · Unlisted 신청 완료(사용자)** — 정식 DAY 0.1.0 (2) · 메모 블록 A + B(「알림」 뺌) · App Privacy 게시 7종(모두 앱 기능 · 연결됨) · Unlisted 양식: Business · Externally · 32명 · Corporate customers · Healthcare · Unmanaged · 한국. 승인 뒤 수동 출시
- `2026-11-12` ASC 답안 결정(사용자 「추천대로」): Product Interaction 신고 · Health · Audio(Soniox 스트림만) · 접속 IP(수집 안 함) 신고 안 함 · 연령 Messaging Yes · UGC No · 의료 Infrequent · 무료 · 한국만 · 2026 Medisolve AI Co., Ltd. · 제3자 콘텐츠 권리 보유 → mobile ASC-2 입력 중
- `2026-11-12` 결정(사용자): **모든 직군은 시술현황 조회(board view)** — 조작 · 수락만 직군별(11-08 권한 표 「없음」 줄 · ③ 그 밖 없음을 보기로). 파비콘 = 앱 아이콘으로(제안 · 발주 대기)
- `2026-11-12` M-20 안 함(사용자): 푸시는 dev 서버 → DAY Dev 앱 · prod 서버 → 정식 앱만. 정식 앱이 데모로 넘어갔을 때 푸시는 필요 없음
- `2026-11-12` **prod 첫 배포 완료** — #244 dev 일반 머지 382827d5 → dev 배포 OK(/privacy · /support 200) → prod ff 382827d5 → deploy-prod 1차 revision-mismatch(정상) → migrate-prod OK → deploy-prod 재실행 OK → https://day.medisolveai.com ready · /privacy · /support · /login 200 → 운영 연결 등록(명동점 · 시스템 계정 통일 · 「운영 연결 넣음」) → 동기화 OK(구역 1 · 방 28 · 직원 92 · 오늘 방문 7 · 오류 0) · 정식 앱 0.1.0 (2) VALID · 버전 연결 · 내부 그룹 medisolveai(사용자 추가) · DAY Dev 0.1.0 (3) · #243 v2 · #245 v4 승인
- `2026-11-12` 앱 결정(사용자): 예약현황 「곧 출시 예정」 그대로 · 설정 탭에 「정보」 → 「개인정보 처리 안내」 링크(A2 · mobile · 스펙 수정 6) · 끝나면 **DAY Dev 번들 빌드 먼저**(다음 빌드 번호 = ASC 조회) · 오늘 심사 목표 · 앱 인계 = `mobile-handoff.md`
- `2026-11-12` 시스템 계정 dev · prod 모두 같은 계정으로 통일(사용자 · 비번 바뀜 → `~/.config/day/prod-kos-system.local`) · 로컬 local.env · 로컬 데모 연결 · dev 서버 데모 연결 다시 넣음(동기화 정상) · VM 에서 dev@ 로 명동점 get-user-account 200 = 내부 API IP 차단 풀림 · 앱 카드 테두리 다 없앰(A1 · 앱 세션 전달 대기)
- `<YYYY-MM-DD>` <무슨 일이 있었나 — 한 줄>

이 절은 **재개에 필요한 만큼만** 쓴다. 회고·배운 것은 `SUMMARY.md` 몫이다.
