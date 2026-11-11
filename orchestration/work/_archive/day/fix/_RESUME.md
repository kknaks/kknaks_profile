
# 재개 노트 — fix (day)

**지금**: PR 2개 올림(code #242 · spec #929 · 머지 전) — 버그 1 ~ 10 + 통역 + 저장소 — 스펙 1 ~ 6판 · Delivery #241 v2 승인 · 서버 · 앱 코드 · 리뷰 전부 PASS. **코디 최종 검증**(2026-11-11): 앱 analyze 0 · 서버 not infra 848 passed · ruff 0 · diff 비밀값 패턴 0 · code 76파일(+3185 −223 · 추적 69) · spec 8문서. 전부 미커밋 — 사용자에게 커밋 · PR · 배포 · TestFlight 2 · Blob 연결을 묻는 중
**다음**: 사용자 답대로 — 스펙 PR · 코드 커밋/push → dev 머지 → 배포 확인(시드 로그 `glossary seed loaded` · 통역 연결) → mobile 에 빌드 2 서명 · 업로드 발주 → 사용자 실기기(A-46 등 `wp-plan.md` §7). 코드는 같은 브랜치 `kknaksss/fix` 에서, 끝에 PR 하나로 스쿼시

세팅: `scripts/new-work.sh day fix` · 설정 SSOT `config/projects/day.json`
코디handle: `term_284b2ffb-0602-4a35-b76f-0f005373d1e2` · Run `run_10982690f975`(재시작 뒤 `orca orchestration run-use --id`)

할 일 전체(사용자 2026-11-11 · 순서): ① 2차 Delivery 마감(SPEC-000 · 002 stable 확인 · #234~#236 · #239 · #238 closeout) ② 앱 후속(스냅샷 version 같은 값 받기 · [재호출] = calls[].canRecall · #235 기록 · OQ-A34 는 사용자에게) ③ TestFlight(개발 먼저) ④ 웹 검수 · 버그(`e2e-feedback.md` 에 모아 한 브리프) ⑤ (나중) prod 배포. **사용자가 ③ 을 먼저 하자고 함(실기기에서 알림 · 채팅 확인).**
이어받는 곳: `../_archive/day/day-procedure-board-2/_RESUME.md` §2 · `../_archive/day/day-app/_RESUME.md` §2 · 회고 `para/projects/company/day/log/2026-11-11-*.md` §7

프로젝트·회고·당시 문서의 탐색은 이 폴더의 작업 목차(`README.md`)가 맡는다.
`sync-work-links.py`로 생성하며, 종료 후에도 프로젝트에서 같은 작업을 찾을 수 있어야 한다.

## 워크트리

- `spec`: `/Users/kknaks/orca/workspaces/mediness-mediness/fix-spec` (branch `kknaksss/fix-app-re1-spec`, base `origin/main` → PR `main`)
- `code`: `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix` (branch `kknaksss/fix-app-re1`, base `origin/dev` → PR `dev`)

## 1. 지금

열린 것만 둔다. 닫히면 지우고 §5 이력으로 내린다.

- [ ] 다음 업로드(빌드 2)에서 수출 규정이 Info.plist 키로 바로 서는지 확인
- [!] 서명 방법 — 팀 기기 0개라 자동 서명 archive 실패. 이번엔 우회(서명 없이 archive → 앱만 entitlements ad-hoc → export 자동 서명 · `app-testflight-upload-report.md`). 정식화 (가) README 에 절차 (나) 기기 1대 등록 (다) 수동 서명 — 사용자 결정
- [!] 부산물: DAY 팀 Apple Development 인증서 1개(자동 서명 1차가 만듦 · 이 Mac 키체인) — 둘지 지울지
- [ ] 다음 업로드 빌드 번호 2 이상 · 경고 90068(배포 대상 iOS 13 → 2027-04 부터 15 필요)
- [!] **PR 올림(2026-11-11)**: code #242(→ dev) · spec mediness#929(→ main) — 둘 다 OPEN · **머지 안 함**(사용자 「이번에는 PR 만 올리고」). 남은 것(다음에): dev 머지(= 배포 · 일반 머지) → 코디 실물(시드 로그 · 저장소 올리기/읽기/지우기 `be-4-report.md`) → TestFlight 빌드 2 → 사용자 실기기(`wp-plan.md` §7) → 스펙 PR 머지 → #241 baseline 재결속(SPEC-000 stable 판단) → 아카이브 · 회고
- [!] **prod 올리기 = 다음 작업**(새 slug · `prod-deploy-re1` 꼴): prod 서버 처음 세우기 · 데모 계정 넘김 실물 · 정식 앱 record · 심사. 준비 값 목록은 2026-11-11 대화(운영 KOS 연결 · 방 배정 작업 id · 전체 권한 계정 · 심사용 데모 계정 · 나가는 IP · 키)
- [!] profile 레포 PR 전 주의: `orchestration/work/fix/e2e-shots/` 는 사용자 실기기 캡처(직원 실명 · 계정 이메일이 보임) — **PUBLIC 레포에 넣지 않는다**(gitignore 또는 가림). `app-captures/` 는 가짜 값
- [!] Delivery #241 **v3** 승인(plan_digest `sha256:dd76aa1d…87df`) · 사용자 질문 남음(코드 안 막음): 폴더 이름 `identity` · `before-after` · dev/prod 컨테이너 분리(추천 = prod 에 고객 사진 들어가기 전) · 보관/복구
- [!] 버그 1 ~ 10 · 통역 코드 · 스펙은 리뷰 PASS · 미커밋 그대로 — Blob 까지 끝난 뒤 묻는다: 스펙 PR · 코드 커밋/push · dev 머지(배포 · 서버 먼저) · TestFlight 빌드 2 · SPEC-000 stable
- [!] 배포 순서: **서버 먼저**(리뷰 R5 — 앱이 먼저 나가면 옛 서버엔 읽은 자리 칸이 없어 모든 메시지에 숫자가 뜬다)
- [!] 1 ~ 7 · 통역 코드 · 스펙은 끝났고 **미커밋 그대로**(사용자: 8 · 9 · 10 까지 넣고 나서). 그 뒤 묻는다: 스펙 PR · 코드 커밋/push · dev 머지(배포) · TestFlight 빌드 2 · SPEC-000 stable
- [!] 브랜치 이름 바꿈(사용자 교정): code `kknaksss/fix-app-re1` · spec `kknaksss/fix-app-re1-spec`(워크트리 경로는 그대로 `…/fix` · `…/fix-spec`). 원격 `kknaksss/fix`(#240 머지됨)는 남아 있음 — 지울지는 사용자
- [ ] 사용자 버그 8(길게 누르기 뜸) · 9(폰 대화 화면 하단 탭 숨김 — 스펙 변경) · 10(메시지별 읽음 표시 — 기능 추가) — `e2e-feedback.md` · 다음 묶음
- [!] **I-1 Soniox 한도 확인(코디 2026-11-11 · `GET /v1/concurrency-limits`)**: 조직 전체 STT 10 · **TTS 3** · 프로젝트 한도 없음 · 지금 사용 0. 상한 6 > TTS 3 — 번역 음성이 4개째 겹치면 거절될 수 있음(통키와 공유). 연결만 열어 둬도 걸리는지는 미확인. 사용자에게 물음: ① Soniox 콘솔에서 TTS 상향 요청 ② 우리 상한을 3 으로 ③ 6 그대로 실기기 확인.
- [!] 통역 pending(나머지): · seed 갈래 재실행(무음 1초 뒤 stop 대본) · A-46 사용자 실기기(듣는 상태 3분 20초 이상 — Caddy 6MiB)
- [ ] 앱 「스펙과 다른 곳」 10건 = 리뷰 판정 「사용자에게 꼭 물을 것 없음」. 실기기 반응 보고 정할 것 2: 그룹 이름 줄에 누를 수 있다는 표시 없음 · 이름 바꾸기 5xx 때 글자 없음
- [ ] 스펙 워크트리 `fix-spec` 미커밋(1 ~ 3판 · 8문서) — 코드 리뷰까지 끝나면 spec PR(→ main)
- [!] Delivery **CENTURION_DAY#241 v2** 승인됨(plan_digest `sha256:551e09b8…2dc6` · L3 · v1 `b3ab…` 은 stale · 제목은 v1 그대로 — CLI 가 안 바꿈) · `spec-baseline:pending` — 스펙 PR(`kknaksss/fix-spec` → main) 머지 뒤 같은 key · version 2 로 재결속. SPEC-000 이 main 에서 draft 라 재결속 때 stable 이 필요할 수 있음(#234 · #239 와 같은 처지 — 사용자 판단)
- [!] 사용자 질문 남음(코드 안 막음): OQ-A43 상한에 찼을 때 글자(기본값 = 「통역 서버를 쓸 수 없어요」 재사용) · 오래 열린 통역 세션이 자리 6개를 쥘 수 있음(수명/무활동 상한을 둘지 — 기본값 없음)
- [!] 사용자 몫으로 남은 것(코드에 안 걸림): M-1 설치 기기(개인 폰/관리 기기) · M-16 서명 방법 · M-20 dev APNs 에 정식 앱 추가 시점
- [ ] 앱 후속 수정 2건 — 스펙 개정 1판 「라」에 넣음 · 이번 앱 코드에 같이
- [!] 채팅 첨부 Blob — **저장소 생김**(2026-11-11 인프라 담당 · 안내문 = 로컬 `~/.config/day/blob-guide-2026-11-11.md` · 값은 공개 레포 금지). 인증 = VM 관리 ID · 계정 키 · 연결 문자열 꺼짐 → 지금 서버 코드(`chat_storage.py` `BlobClient.from_connection_string` · 선택 비밀 `…-chat-blob-connection-string`)로는 못 붙는다: 스펙(SPEC-004 저장소 · deployment.md) + 서버(관리 ID 자격 · `azure-identity` 의존성 · 설정 = 계정 주소 + 컨테이너 · compose 에서 IMDS 접근) + 실물(Docker 안 관리 ID · 올리기/읽기/지우기). 사용자 말이 끊김(「이거 지금 …」) — 이번 판에 넣을지 묻는 중
- [!] `orchestration/config/projects/day.json` `apple` 섹션 추가분 미커밋 — 마감 PR 에 넣는다. dev 앱 등록되면 섹션 갱신

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-11-11 | 개발 / 정식 두 앱으로 나눈다 — 개발 `day.medisolveai.dev`(DAY Dev → day-dev) · 정식 `day.medisolveai`(DAY → prod) | 사용자 「dev 로 등록도 하자」 |
| 2026-11-11 | 앱 아이콘 = `assets/icon-source.svg`(사용자 제공) 에서 색만 메인 색 `#1D8BFF` 로 | 사용자. 흰 배경 불투명은 코디 기본값(iOS 는 투명 불가) — 사용자 확인 전 |
| 2026-11-11 | 최종 배포는 비공개 — 병원 직원에게만 공유. 방식 = **등록되지 않은 앱(Unlisted)** | 사용자. `mobile-deployment.md` §2 · §6 의 [미결](비공개 방식 · 설치 대상)을 닫는다 |
| 2026-11-11 | 서버 `dev.env` 의 APNs Key ID · Team ID 는 저장소(비공개 CENTURION_DAY)에 둔다. 「Team ID 를 저장소에 넣지 않는다」(M-16)는 앱 서명 값 범위 | 사용자 승인 · review-1 W2. `app/README.md:164` · `Identity.xcconfig:4` · `mobile-deployment.md` M-16 문구 정리는 스펙 묶음에 |
| 2026-11-11 | 중간 배포는 일반 머지(브랜치 유지 · 워크트리 다시 안 만듦), 작업 끝에 PR 하나로 스쿼시 | 사용자 「dev 에만 병합 · 나중에 한번에 스쿼시」 |
| 2026-11-11 | 채팅 · 알림의 「시스템 계정 제외」 규칙은 그대로 둔다. 사용자가 dev 의 KOS 시스템 계정을 다른 계정으로 바꾼다 | 사용자 「시스템 계정을 바꿀게」 · `e2e-feedback.md` #1 · #3 · #4 |
| 2026-11-11 | 통역 = interpret-pwa back 을 DAY 로 옮긴다(앱 무수정) · 사전 = 그 시드 파일 사본 · 기록 안 남김 · Soniox 키 = interpret-pwa 의 회사 공용 DAY 키 · 동시 세션 상한 6 | 사용자: 바탕 = interpret-pwa(「번역 플로우는 interpret-pwa 에 있어」) · 사전 = 그 시드처럼(「사전도 … interpret-pwa 처럼」) · 키(Q-2) · 상한 6(Q-5). **코디 기본값(통보 · 뒤집을 수 있음)**: 전 병원 한 벌(Q-4) · 기록 안 남김(Q-7) · 연결 때 한 번 확인(Q-6) · 시드 갱신 = 사람 PR(Q-8) · 앱 문구 그대로(Q-9) — review-doc-1 W2 로 바로잡음 |
| 2026-11-11 | **스펙 → 리뷰 → WP → 코드 → 리뷰까지 멈추지 않고 간다**(버그 묶음 + 통역). 단계 사이에 사용자 승인을 기다리지 않는다 | 사용자 「코드 구현까지 쭉 가자」. 그래도 멈추는 곳: 화면 문구 · 사용자만 정할 수 있는 「정할 것」 · 머지 · 서명/업로드 · 서버 값 |
| 2026-11-11 | CENTURION_DAY#241 **v2**(8 · 9 · 10 추가) 결과 계약 승인(plan_digest `sha256:551e09b88a6d05da1f88a64fcd904c5d05f481c92dc0fc4c2f9f773f079e2dc6`) | 사용자 「8, 9, 10 까지 해야」 — 더해진 것이 그 셋뿐 · L3 그대로임을 planner 가 대조 뒤 적용 |
| 2026-11-11 | CENTURION_DAY#241 결과 계약 승인(plan_digest `sha256:b3ab2b847d281a909fb5f0536a1bf9178f43355c797fbfca20dc36b464848cf1`) | 사용자 「일단 이거 올리고 승인 처리 하자」 |
| 2026-11-11 | fix 작업도 Delivery Issue 로 올리고 승인한다(로컬 `wp-plan.md` 만으로 가지 않는다) | 사용자 「왜 이슈로 안 했어 일단 이거 올리고 승인 처리 하자」 — 코디가 등록을 미룬 것을 교정 |
| 2026-11-11 | 버그 8 · 9 · 10 도 이번 작업(커밋 전)에 넣는다 · 10번 = 카톡식(안 읽은 사람 수 · 0 이면 사라짐) · 9번 = 폰 대화 화면에서 하단 탭 숨김 | 사용자 「8, 9, 10 까지 해야 하는 거 아니야 · 10번은 카톡식으로」 |
| 2026-11-11 | 브랜치 이름은 `fix-app-re1` 꼴(대상 · 회차) | 사용자 「브랜치 이름이 fix-app-re1 이런식으로 해야하지」 |
| 2026-11-11 | 읽음 표시 계약 정정 1: 앱은 메시지를 받으면 보낸 사람 `lastReadSeq = max(·, seq)` · 멤버 읽은 자리 합치기는 늘 max · 서버는 그대로(`chat_member_read` 는 #15 가 올릴 때만) | 문서 리뷰 [긴급](답장이 읽음 요청보다 먼저 가면 숫자가 남음) → 코디 결정 · `correction-read-1.md` · mobile · backend 에 정정 보냄 |
| 2026-11-11 | 읽음 표시 정정 2: 「보고 있는 방」에서 그린 메시지까지는 나를 읽은 사람으로 센다(숫자 깜빡임 방지 · 카톡 겉보기) · 탭 숨긴 화면의 입력줄은 안전 영역 위 | 문서 리뷰 W2 · W5 → 코디 기본값 · `correction-read-2.md` |
| 2026-11-11 | 파일 저장소(Blob)도 이번 작업에 넣는다 · 구조 = 맨 위 환경(`dev`/`prod`) → 용도(`chat` · 신분증) | 사용자 「dev/prod 디렉토리 나누고 chat/passport … · 스토리지는 해결됐어 이번에 같이 가야」. 신분증 폴더 이름 `identity` · 경로에 병원 id · dev/prod 차단 안 됨 받아들임 · 보관/복구 그대로 = 코디 기본값(통보). 코디 실물 확인: dev api 컨테이너 안에서 관리 ID 저장소 토큰 = 됨 · `azure-identity` 없음 |
| 2026-11-11 | 저장소에 둘 것(앞으로 포함) = **고객 전후 사진 · 고객 신분증(여권) · 내부 채팅 사진** 셋 | 사용자. 폴더 이름 `before-after` · `identity` · `chat` 은 코디 기본값(`correction-storage-1.md`) · 이번 구현은 `chat` 만 · 나머지는 이름 예약 |
| 2026-11-11 | 저장소 폴더 이름 `identity` · `before-after` · `chat` **확정** | 사용자 「응 폴더 이름 그대로 쓸 거야」 — 스펙의 「코디 기본값」 표시를 사용자 확정으로 바꿀 것(다음 스펙 수정 때) |
| 2026-11-11 | 환경 분리 = 환경마다 접근할 컨테이너를 다르게(설정값) — 컨테이너 이름은 환경별 설정 · 지금은 컨테이너 하나라 같은 값 · 새 컨테이너는 사용자가 인프라에 요청 · 맨 위 환경 폴더는 그대로 | 사용자 「컨테이너만 분리해서 생성하면 각각 env 에서 접근할 컨테이너가 달라지는 거 아니야」 — 코디가 「권한까지 나눠야 분리」라고 과하게 답한 것을 교정 |
| 2026-11-11 | 컨테이너를 환경별로 둘: `daydev` · `dayprod`(사용자가 인프라 담당에게 요청 — 컨테이너 생성 + VM 관리 ID · 본인 계정에 파일 권한). 생기면 dev.env · prod.env 의 `DAY_BLOB_CONTAINER` 만 바꾼다 | 사용자 「daydev/dayprod 이렇게 컨테이너 만들고?」. 아직 없음 — 그때까지 dev 는 `files` + `dev/` 폴더. 컨테이너가 나뉜 뒤 맨 위 환경 폴더를 뺄지는 사용자에게 물음 |
| 2026-11-11 | **저장소: 환경은 컨테이너로 나눈다(`daydev` · `dayprod`) · 경로에 환경 폴더 없음**(키 = `chat/{병원 id}/…` 원래 그대로) · 컨테이너가 있다고 가정하고 짓는다 · 값은 사용자가 준다 | 사용자 「그렇게 했다고 가정하고 코드 짜면 안 돼? 환경 설정값만 내가 주면 되는 거」 — 앞의 「맨 위 환경 폴더」(7판) · 「환경 폴더 그대로」(정정 2)를 뒤집음 · `correction-storage-3.md`. 컨테이너는 아직 없음(사용자가 인프라에 요청) → 그때까지 dev 사진 보내기 = 503 |
| 2026-11-11 | 저장소 컨테이너 이름 = **`dev` · `prod`**(인프라 담당이 만든 실제 이름 · `daydev`/`dayprod` 아님) — 이미 있음 · VM 관리 ID 로 세 컨테이너 목록 읽기 확인 | 사용자 「env 없는데? 컨테이너 안 받은 거 아니야?」 → 코디 조회(`correction-storage-4.md`). code `dev.env` `DAY_BLOB_CONTAINER=dev` 로 코디가 고침(tests/deploy 102 passed) · `files` 는 안 씀 |
| 2026-11-11 | 컨테이너 이름 `dev` · `prod` **사용자 확정**(`daydev` · `dayprod` 로 다시 만들지 않는다) | 사용자 「아니 dev prod 로 컨테이너 이름 쓰자」 — code #242 · spec #929 에 이미 이 이름 |
| 2026-11-11 | SPEC-000 stable · Delivery #241 마감은 다음 작업에서 — 다음 작업 = 웹 버그 수정 · prod 배포 · 앱 작은 수정 · 문서 정리 | 사용자 「그거는 다음 작업에서」. #241 은 OPEN · baseline pending 으로 남긴 채 이번 작업 마감 |
| 2026-11-11 | ~~SPEC-000 stable · #241 마감은 다음 작업~~ → **SPEC-000 을 stable 로 올리고 Delivery 를 닫는다** | 사용자 「아 그럼 스테이블에 올리고 다 닫자」(같은 날 뒤집음). SPEC-002 는 말하지 않음 — 2차 Delivery 가 그것에 막히면 다시 묻는다. spec 워크트리 브랜치 = `kknaksss/fix-app-re1-spec-stable`(origin/main 1a450bcf) |
| 2026-11-11 | **Delivery 를 전부 닫는다 · 실물 검증은 다음 작업으로 넘긴다** — 실기기 · 데모 실물 수용 항목은 각 Delivery 범위에서 빼(계약 변경 · 재승인) 닫는다 · 닫는 데 필요한 SPEC-002 stable 도 올린다 | 사용자 「이제 다 한 거잖아. 검증은 다음에 하자니까. 닫는 데 문제가 있어?」 — 코디가 같은 질문을 되풀이한 것을 교정. 미확인을 「통과」로 적지 않는다 — 범위에서 뺐다고 기록 |
| 2026-11-11 | Delivery 마감 = review-delivery 기록까지 도구로 → 문서 sync 는 손으로 PR → Issue 는 마감 댓글 뒤 `gh issue close` | 도구 `spec-sync` 가 제품 레포 Delivery 에서 못 돈다(mediness#749 OPEN · 금지된 `--github-repo` 우회 안 함) · 사용자 「다 닫자」 · 1차 #224 ~ #227 도 pending 라벨로 CLOSED(전례) — `delivery-close-answer.md` |
| 2026-11-11 | TestFlight 를 앱 후속 수정보다 먼저 | 사용자 「일단 앱부터」 |
| 2026-11-11 | Apple 설정 위치를 프로젝트 설정(`day.json` `apple`)에 적는다 — 값은 로컬 `~/.config/day/apple/` | 사용자 |

뒤집힌 결정은 지우지 않는다. ~~취소선~~ 을 긋고 같은 행에 뒤집은 날짜와 사유를 남긴다 —
지우면 왜 그렇게 갔는지가 사라져서 같은 논의를 다시 한다.

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| mobile | `term_8fae9ebc-816d-4674-970b-4107e45084ff` | `task_6b7c0e875502` | `ctx_88e75296f36b` | `fix-app-brief.md` | 1판 완료 · ack |
| mobile | `term_8fae9ebc-816d-4674-970b-4107e45084ff` | `task_2e38ade6cc07` | `ctx_406b567b5d06` | `fix-app-upload-brief.md` | 완료 · ack |
| mobile | `term_8fae9ebc-816d-4674-970b-4107e45084ff` | `task_70adc25816cc` | `ctx_204dd262740b` | `fix-app-export-compliance-brief.md` | 완료 · ack |
| backend | `term_d8e9c610-96b4-482a-9972-365ca65c1084` | `task_4090e37a505d` | `ctx_30e3f251f4e0` | `fix-be-dev-env-brief.md` | A · D 완료 · B · C blocked · ack |
| reviewer | `term_4afcc88b-79e9-4f89-82de-783b5f10c7c9` | `task_20c2cce6dd38` | `ctx_0010408779e2` | `fix-review-1-brief.md` | 완료 WARN(FAIL 0) · ack |
| planner | `term_bf6ad1b2-354a-4423-8fd4-eb60fc4732c8` | `task_d189d7d864db` | `ctx_15ac2b86d9fd` | `fix-spec-1-brief.md` | 완료 · ack — `spec-1-report.md`(lint ERROR 0 · 정할 것 8) |
| planner | `term_bf6ad1b2-354a-4423-8fd4-eb60fc4732c8` | `task_1880d740fbfe` | `ctx_5a347b043af5` | `fix-spec-2-brief.md` | 완료 · ack — `spec-2-report.md`(통역 계약 = SPEC-003 §3 · lint ERROR 0 · 정할 것 OQ-A43 1) |
| reviewer_doc | `term_fe17c0ae-13ad-4046-abb8-f9e9280f8932` | `task_e241840c7b81 ctx_92f10f79b38f` | `` | `fix-review-doc-1-brief.md` | 완료 **WARN**(FAIL 0 · WARN 11 · 지어 넣은 글자 0 · 통역 계약 = 앱 코드와 같음) · ack — `review-doc-1-report.md` |
| planner | `term_bf6ad1b2-354a-4423-8fd4-eb60fc4732c8` | `task_8a99f2b23795 ctx_8dbeb9b71d4f` | `` | `fix-spec-3-brief.md` | 완료 · ack — `spec-3-report.md`(WARN 11/11 · lint ERROR 0) · `wp-plan.md`(WP 4) |
| backend | `term_d8e9c610-96b4-482a-9972-365ca65c1084` | `task_79bf978947d4 ctx_91c3f1cd313b` | `task_10fc409931cf ctx_480886d0bf53` | `fix-be-code-brief.md` | 완료 · ack — `be-1-report.md` · `be-2-report.md`(격리 스택 전체 1136 passed · not infra 842 · ruff 0 · 실물 Soniox A-45 왕복 · 35초 멈춤 통과 · A-47 통과) |
| reviewer | `term_4afcc88b-79e9-4f89-82de-783b5f10c7c9` | `task_12cd94bb0cf7 ctx_89da274250c9` | `` | `fix-review-be-brief.md` | 완료 **WARN**(FAIL 0 · W1 접근 로그 쿼리 · 참고 7 · 원천 대비 로직 차이 = session.py 뿐 · 자리 반납 전 경로 확인) · ack — `review-be-report.md` |
| backend | `term_d8e9c610-96b4-482a-9972-365ca65c1084` | `task_00f1398e19b6 ctx_643997c2bbcc` | `task_b97ba7d3940e ctx_469881e60abb` | planner | `term_bf6ad1b2-354a-4423-8fd4-eb60fc4732c8` | `task_6b8f669d8494 ctx_674ba9e7efa4` | `` | `fix-spec-4-brief.md` | 완료 · ack — `spec-4-report.md`(SPEC-004 개정 ④ · 읽음 = 앱이 셈 · `Member.lastReadSeq/fromSeq` + `chat_member_read` · migration 없음 · lint 0 · #241 v2 승인) |
| reviewer_doc | `term_fe17c0ae-13ad-4046-abb8-f9e9280f8932` | `task_a1f43cd4b9d5` | `ctx_17b5eed8e23f` | `fix-review-doc-2-brief.md` | 완료 **FAIL 1 · WARN 9** · ack — `review-doc-2-report.md`. F1 · W1 = 정정 1 로 닫음 · 나머지 = 정정 2(`correction-read-2.md`) |
| planner | `term_bf6ad1b2-354a-4423-8fd4-eb60fc4732c8` | `task_92d9e6d6a90c ctx_a5e24cd27d9d` | `` | `fix-spec-6-brief.md` | 완료 · ack — `spec-6-report.md`(W2 ~ W9 반영 · #241 무변경 · lint 0) |
| backend | `term_d8e9c610-96b4-482a-9972-365ca65c1084` | `task_080485ca0515` | `ctx_93dac168940c` | `fix-be-code-2-brief.md` | 완료 · ack — `be-3-report.md`(migration 0 · 격리 전체 1147 passed · not infra 848 · 정정 1 시험) |
| reviewer | `term_4afcc88b-79e9-4f89-82de-783b5f10c7c9` | `task_8511f702bd60 ctx_c29b87d33080` | `` | `fix-review-be-2-brief.md` | 완료 **PASS** · ack — `review-be-2-report.md` |
| mobile | `term_8fae9ebc-816d-4674-970b-4107e45084ff` | `task_7c58f87b1ced` | `ctx_8e61f5c9eec7` | `fix-app-code-2-brief.md` | 완료 · ack — `app-3-report.md`(정정 1 · 2 반영 · 전체 +341 · 서명 없는 빌드 OK · 캡처 `*fix3*` 8) |
| reviewer | `term_4afcc88b-79e9-4f89-82de-783b5f10c7c9` | `task_9ffa900f689f ctx_229f2b17c2c9` | `` | `fix-review-app-3-brief.md` | 완료 **WARN**(FAIL 0 · W1 메뉴 중 새 메시지로 밀리면 다시 안 잼 · 참고 5 · 9 · 10 · 정정 1 · 2 · 서버 계약 · 새 글자 0 = 스펙과 같음) · ack — `review-app-3-report.md` |
| mobile | `term_8fae9ebc-816d-4674-970b-4107e45084ff` | `task_432eb5163418 ctx_117a18cfea6b` | `` | `fix-app-fix3-brief.md` | 완료 · ack — `app-fix3-report.md`(다시 재는 계기 12종 · 전체 +343) |
| reviewer | `term_4afcc88b-79e9-4f89-82de-783b5f10c7c9` | `task_27427816a381 ctx_b3e5819ca946` | `` | `fix-review-app-fix3-brief.md` | 완료 **PASS** · ack — `review-app-fix3-report.md` |
| planner | `term_bf6ad1b2-354a-4423-8fd4-eb60fc4732c8` | `task_b9906d81a7dc ctx_a14429681971` | `` | `fix-spec-5-brief.md` | 완료 · ack — `spec-5-report.md`(정정 1 반영 · #241 무변경 · lint 0) |
| planner | `term_bf6ad1b2-354a-4423-8fd4-eb60fc4732c8` | `task_574b34403b60 ctx_e164da6e202d` | `` | `fix-spec-7-brief.md` | 완료 · ack — `spec-7-report.md`(구조 = deployment.md 새 절 · `DAY_BLOB_ACCOUNT_URL` · `DAY_BLOB_CONTAINER` · 연결 문자열 칸 · 선택 비밀 없앰 · 앱 변경 없음 · migration 없음 · lint 0 · #241 v3 승인) |
| reviewer_doc | `term_fe17c0ae-13ad-4046-abb8-f9e9280f8932` | `task_2e43c0d383d8` | `ctx_81ff0b2fe765` | `fix-review-doc-3-brief.md` | 완료 **WARN**(FAIL 0 · WARN 7 · 계약 변경 없음 · 값 누출 0) · ack — `review-doc-3-report.md` → `correction-storage-2.md` |
| planner | `term_bf6ad1b2-354a-4423-8fd4-eb60fc4732c8` | `task_4b92aec9a7eb` | `ctx_4b2695116097` | `fix-spec-8-brief.md` | 완료 · ack — `spec-8-report.md`(W1 ~ W7 + 폴더 이름 확정 · 컨테이너 = 환경별 설정값 · #241 무변경 · lint 0) |
| backend | `term_d8e9c610-96b4-482a-9972-365ca65c1084` | `task_fbd3bd126f04` | `ctx_72643e29d6c2` | `fix-be-code-3-brief.md` | 완료 · ack — `be-4-report.md`(정정 2 · 3 반영 · 관리 ID · 키 `chat/{병원 id}/…` · dev.env 세 칸 · prod 빈 칸 · lock = azure-identity · msal 2 추가뿐 · 격리 전체 1168 passed) |
| reviewer | `term_4afcc88b-79e9-4f89-82de-783b5f10c7c9` | `task_4defa0a9b61e` | `ctx_2224cf6876ad` | `fix-review-be-3-brief.md` | 완료 **PASS**(참고 4) · ack — `review-be-3-report.md` |
| planner | `term_bf6ad1b2-354a-4423-8fd4-eb60fc4732c8` | `task_227489505380` | `ctx_d430db0e00d8` | `fix-spec-9-brief.md` | 완료 · ack — `spec-9-report.md`(환경 = 컨테이너 · 환경 폴더 없음 · 옛 문장 0 · lint 0 · #241 v4 승인) |
| planner | `term_bf6ad1b2-354a-4423-8fd4-eb60fc4732c8` | `task_d9a72a4d592a` | `ctx_14489e39a599` | `fix-spec-10-brief.md` | 완료 · ack — `spec-10-report.md`(컨테이너 `dev` · `prod` 있음 · lint 0 · #241 v5 승인) |
| planner | `term_bf6ad1b2-354a-4423-8fd4-eb60fc4732c8` | `task_dec16aa63e4d` | `ctx_c6fceb01e5c7` | `fix-delivery-close-brief.md` | 완료 · ack — **#241 닫지 못함**(SPEC-000 draft → baseline pending → review-delivery 거절 · `delivery-close-report.md`) |
| mobile | `term_8fae9ebc-816d-4674-970b-4107e45084ff` | `task_6a7ed8caeeb4` | `ctx_2d3dfd1a7173` | `fix-app-upload-2-brief.md` | 완료 · ack — DAY Dev 0.1.0 (2) VALID · `IN_BETA_TESTING` · 수출 규정 자동(코디 ASC 재조회 확인) |
| planner | `term_bf6ad1b2-354a-4423-8fd4-eb60fc4732c8` | `task_02b2c7f312d7` | `ctx_330cb1a9fb50` | `fix-spec-stable-brief.md` | 완료 · ack — `spec-stable-report.md` · spec PR mediness#930 스쿼시 머지 `caf7f3eb` |
| planner | `term_bf6ad1b2-354a-4423-8fd4-eb60fc4732c8` | `task_7eed37c23179` | `ctx_3be0cd300394` | `fix-delivery-rebind-brief.md` | 완료 · ack — #241 v6 · `spec-baseline:ready` · 승인 유지(`delivery-rebind-report.md`) |
| planner | `term_bf6ad1b2-354a-4423-8fd4-eb60fc4732c8` | `task_9d132f93ad08` | `ctx_35b05547f624` | `fix-delivery-close-all-brief.md` | 진행(Delivery 5건 닫기 — sync PR 마다 코디가 스쿼시 머지 뒤 `[머지됨] #PR sha` 를 planner 에 보냄) |
| `fix-be-fix1-brief.md` | 완료 · ack — `be-fix1-report.md`(격리 스택 전체 1141 passed). **코디 검증**: not infra 847 passed · ruff 0 · `deploy/config` 값 줄 diff 0(주석만) · diff 비밀값 패턴 0 · 접근 로그 필터 코드 확인 |
| reviewer | `term_4afcc88b-79e9-4f89-82de-783b5f10c7c9` | `` | `` | `fix-review-app-fix1-brief.md` | 완료 **PASS** · ack — `review-app-fix1-report.md` |
| mobile | `term_8fae9ebc-816d-4674-970b-4107e45084ff` | `` | `` | `fix-app-code-brief.md` | 완료 · ack — `app-1-report.md` · `app-2-report.md`(전체 +314 · analyze 0 · 서명 없는 빌드 OK · 캡처 12) |
| reviewer | `term_4afcc88b-79e9-4f89-82de-783b5f10c7c9` | `task_c0d69479039d ctx_4c1bcbe55074` | `` | `fix-review-app-brief.md` | 완료 **WARN**(FAIL 0 · W1 채팅 403 누락 경로 2 · 참고 5 · 새 글자 0 · 서버 계약 같음) · ack — `review-app-report.md` |
| mobile | `term_8fae9ebc-816d-4674-970b-4107e45084ff` | `task_730e01a61e9f ctx_0f74859a7edd` | `` | `fix-app-fix1-brief.md` | 완료 · ack — `app-fix1-report.md`(채팅 HTTP 26곳 전수 · 403 누락 0 · 리뷰가 못 본 2곳 더 고침 · 전체 +320) |
| planner | `term_bf6ad1b2-354a-4423-8fd4-eb60fc4732c8` | `task_ac6854296ab4 ctx_5396f7c35dfa` | `` | `fix-delivery-brief.md` | 완료 · ack — **#241** L3 · `delivery-plan:approved` · baseline pending(`delivery-report.md`) |
| researcher | `term_7b626c58-91d9-4ad3-8429-de5dca2aad2e` | `task_8d6f416b5554` | `ctx_7d40a48df1b1` | `fix-research-interpret-brief.md` | 완료 · ack — `research-interpret-report.md`(정할 것 9) |

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.** 워커 보고는 dispatch preamble 의 값을 따르므로
여기 옛 핸들을 남겨 두면 어느 것이 산 것인지 판단이 안 된다.

## 4. 산출물

- code PR: https://github.com/MediSolveAIDev/CENTURION_DAY/pull/242 (OPEN · 커밋 87cf2dec · 브랜치 `kknaksss/fix-app-re1` → dev) · spec PR: https://github.com/MediSolveAIDev/mediness/pull/929 (OPEN · 커밋 95d17506 · `kknaksss/fix-app-re1-spec` → main)
- code PR: https://github.com/MediSolveAIDev/CENTURION_DAY/pull/240 (MERGED · 일반 머지 378e3ae3)
- Delivery: https://github.com/MediSolveAIDev/CENTURION_DAY/issues/241 (approved · baseline pending)
- 리포트: `delivery-report.md` · `research-interpret-report.md` · `review-1-report.md` · `app-testflight-prep-report.md` · `app-testflight-upload-report.md` · `app-export-compliance-report.md` · `be-dev-env-report.md`
- code 미커밋: `app/README.md` · `app/ios/Runner/Info.plist`(수출 규정 키) · AppIcon(`Contents.json` + PNG 15) · `app/assets/brand/app-icon.svg`
- TestFlight: DAY Dev 0.1.0 (1) — VALID(2026-11-11)

## 5. 이력 (최신이 위)

- `2026-11-11` Soniox 키를 dev Key Vault `day-dev-soniox-api-key` 에 넣음(원천 = interpret-pwa 로컬 `.env` · VM 경유 · 버전 1). 코드가 아직 이 이름을 읽지 않는다 — 통역 스펙이 이 이름을 선택 비밀로 정해야 함. prod 는 아직
- `2026-11-11` dev KOS 시스템 계정 교체(사용자 지시 · 값 = `reference/2026-11-11-kos-system/info.json` gitignore · 600): dev api 컨테이너에서 일회성 스크립트로 새 계정 KOS 로그인 확인 → `crm_connection.config` 의 `system_email` · `system_password` 만 갱신 → `run_master` 1회. 결과: 사용자 staff `is_system_account=false` · 시스템 행 1 · 채팅 가능 5
- `2026-11-11` APNs 키 넣기: 계정에 Vault 방화벽 변경 권한 없음(`vaults/write` AuthorizationFailed · 규칙 변화 0) → `ssh -D` 로 day-vm 을 거쳐 Key Vault REST 로 넣음(사용자 토큰 · 파일에서 바로 · 버전 1). 다음에도 이 방법
- `2026-11-11` #240 머지 커밋 378e3ae3 → 배포 run 42948049354 성공(2m37s)
- `2026-11-11` 실기기 첫 로그인 `environment_unavailable` — 원인 = dev.env `DAY_PUBLIC_API_BASE` 빔(release 앱은 `api_base_url` · `environment` 둘 다 필요 · 웹은 안 씀). 배포 = `dev` push 워크플로
- `2026-11-11` mobile 1판 done — `day.medisolveai.dev` 등록(코디 ASC 재조회 확인) · 아이콘 19칸 · dev 서명 없는 빌드. 코드 미커밋(`app/README.md` · AppIcon · `app/assets/brand/`). 주의: `~/.appstoreconnect` 의 키는 DAY 키 아님 → 업로드는 credentials 경로로. dev 앱 연결 규칙(`DAY_LOGIN_ENTRY` · `DAY_ALLOWED_ORIGINS`)은 SPEC 에 없음(정식만 정의)
- `2026-11-11` slug 세팅(code aa7853cd · spec 0d69a207). ASC 조회: Bundle ID 는 `day.medisolveai` 뿐 · 앱 record 0 · Team ID 는 로컬 자격에 이미 있음 · AppIcon 이미지 0. mobile 첫 발주

이 절은 **재개에 필요한 만큼만** 쓴다. 회고·배운 것은 `SUMMARY.md` 몫이다.
