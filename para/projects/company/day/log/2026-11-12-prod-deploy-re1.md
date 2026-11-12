# 작업 요약 — prod-deploy-re1 (day)

기간: `2026-11-11` ~ `2026-11-12`
결과: DAY prod 첫 배포(`https://day.medisolveai.com` · 운영 병원 1곳 동기화) · 웹 피드백 반영 · 정식 앱 0.1.0 (2) App Store 심사 제출 · Unlisted 신청까지. Apple 결과 대기.

## 1. 무엇을 했나

DAY 4차. prod 서버가 없고, 웹에 사용자 피드백(차트 모달 · 방 옮기기 · 점유 이동 지연 · 복귀 = 취소)이 쌓여 있었고, 정식 앱은 등록만 된 상태였다.
prod 는 같은 VM 의 `day_prod` 스키마로 올렸다 — Key Vault 비밀 8 · `prod.env` · 운영 연결 등록 진입점(`python -m day.register_connection`)을 만들고, dev 머지 → prod fast-forward → migrate-prod → deploy-prod 순으로 처음 배포했다. 운영 KOS 는 조회만 했다.
웹은 점유 이동을 10초 조회 대기에서 **응답 → 상세 조회 이벤트 연쇄**로 바꿨고, 연쇄 결과를 판에 바로 반영해 띠가 1초 안에 나오게 했다. 앱은 테두리 · 설정 「정보」(개인정보 링크)를 더해 정식 빌드 2 로 심사에 냈고, 공개 페이지 `/privacy` · `/support` 와 「모든 직군 보기」 권한까지 prod 에 올렸다.

## 2. 적용한 기술·개념

- **요청-응답 이벤트 연쇄(폴링 대체)** — 점유 이동 「방 배정」 만들기 뒤 다음 쓰기를 10초 일정 조회가 아니라 응답 직후 상세 조회로 잇는다. → [[polling]]
  - 왜 이걸 골랐나: 사용자 「보내고 응답 오면 다시 API 요청하면 되잖아」. 주기를 줄이는 안(조회 부하 · 겹침)을 버리고, 10초 조회는 그대로 두되 이 연쇄만 기다리지 않게 했다. 못 찾거나 실패하면 지금처럼 10초 조회가 잇는다.
  - 무엇이 어려웠나: 연쇄가 1초 안에 KOS 확인까지 끝났는데도 띠는 ~7초 뒤에 나왔다. outbox 시각 · api 접근 로그 · 코드로 따라가니 연쇄가 받은 상세 결과를 **쓰기 큐 확인에만 쓰고 판 작업 행에 넣지 않았다**(`follow_room_assign` 의 update 가 아직 없는 행에 0행). 일정 조회와 같은 반영 함수(`apply_visit_tasks` → `_apply_tasks`)로 판에 넣은 뒤 신호를 보내 0.78초가 됐다. 한 번 잰 0.93초는 10초 조회가 16ms 앞서 끝나 누가 그렸는지 못 갈라, 조회 직후에 다시 쟀다.
  - 근거: `be-3-report.md` · `review-code-8-report.md` · `cf8f5037`
- **반영 대기 중 버튼 숨김으로 엇갈림 막기** — 연쇄가 빨라지자 띠 · [복귀하기]가 연쇄 도중에 보이고, 그때 누른 복귀(「방 배정」 삭제)가 연쇄의 방 옮기기와 엇갈려 「반영 중」이 최대 180초 남았다. → [[pending-write-action-guard]]
  - 왜 이걸 골랐나: (a) 삭제 확인이 남은 쓰기를 닫게 하는 안 대신 (b) 「그 방문에 반영 대기 쓰기가 있으면 [복귀하기]를 안 그린다 · 서버도 409」를 골랐다 — 연쇄 길과 일정 조회 길을 한 번에 닫는다. 리뷰가 「원래 있던 결함이 드러나기 쉬워진 것」으로 판정.
  - 근거: `be-4-report.md` · `review-code-9-report.md` · SPEC-002 ⑱ ⑥
- **같은 서버 · 다른 스키마 prod 첫 배포** — 한 VM 에 dev · prod compose project · `day_prod` 스키마 · 회사 공용 ACR 의 같은 SHA 이미지. → [[artifact-promotion]]
  - 왜 이걸 골랐나: prod 는 빌드하지 않고 dev 에서 확인한 커밋을 `prod` 브랜치로 fast-forward 만 한다(merge · squash 금지). migration 은 확인 문자열이 있는 수동 워크플로로 따로.
  - 무엇이 어려웠나: `prod` 브랜치는 있었지만 워크플로 파일이 없어, 첫 push 의 deploy-prod 가 `revision-mismatch current=none` 으로 멈추는 것이 정상 경로였다 → migrate-prod → 같은 실행 Re-run.
  - 근거: `40-architecture/deployment.md` 「prod 첫 배포 절차」 · run 43153893222 · 43154046130
- **비밀을 화면에 안 내는 운영 등록** — 운영 연결(open 키 · 테넌트 · 시스템 계정)을 prod 컨테이너 안 `--stdin` 으로 1회 넣었다. → [[secret-store]]
  - 왜 이걸 골랐나: 이미지에 `scripts/` 가 없어 backend 모듈 진입점이 필요했다. 테넌트 id 는 컨테이너에서 로그인 응답의 `tenantIds` 중 끝자리로 골라 로컬 600 파일에만 받고, 값 파일은 쓰자마자 지웠다. 같은 이름 · 다른 데모 표시면 거절.
  - 근거: `backend/day/register_connection.py` · `be-1-report.md`
- **App Store 「수집」 정의로 App Privacy 답하기** — 「앱이 기기에서 보내 서버가 실시간 처리보다 오래 보관하는 것」만 신고. → [[app-privacy-disclosure]]
  - 왜 이걸 골랐나: EMR 사본은 서버가 받아 오는 것이라 신고 대상이 아니고, Soniox 통역 음성은 실시간 스트림 · 미저장이라 제외. 대신 계정 이메일 · 이름 · 사용자 ID · 기기 ID(설치 id · 푸시 토큰) · 채팅 글 · 사진/동영상 · 업무 조작 이력은 보관하므로 신고(모두 앱 기능 · 연결됨 · 추적 없음). App Privacy 는 공개 API 가 없어 웹에서 직접.
  - 근거: `mobile-asc-answers.md` · `mobile-asc-apply-report.md`
- **Unlisted 배포** — 링크로만 받는 App Store 배포. 신청은 웹 양식뿐이고, 승인되면 이후 버전 모두 Unlisted · 되돌릴 수 없다. → [[unlisted-app-distribution]]
  - 왜 이걸 골랐나: Apple Business 맞춤형 앱은 병원마다 등록이 필요해 병원이 늘 때마다 절차가 붙는다. 출시는 수동이라 Unlisted 승인 전 공개될 걱정이 없다.
  - 근거: https://developer.apple.com/support/unlisted-app-distribution/ · `mobile-deployment.md`

## 3. 막혔던 것 / 사고

- 운영 내부 API 403 → 응답 본문 `IPBlocked` 로 VM IP 미허용을 확인 → 사용자가 관리자 계정을 받아 풀림(VM 에서 `get-user-account` 200).
- 시스템 계정을 이메일 앞부분만 보고 잘못 읽어 사용자와 엇갈렸다 → 사용자 결정으로 dev · prod 시스템 계정을 한 계정으로 통일하고 로컬 · dev 데모 연결을 다시 넣었다.
- 범위를 넓힌 것이 세 번 반려됐다: 「고치고 닫아」를 머지로 · 디자인만 바뀐 차트 모달을 Delivery 에 · 현황 탭 그림을 「앱 전체 테두리」로(방 상세까지 고침 → 되돌림). **사용자가 보여 준 화면 · 말한 행동이 범위다.**
- 워커에게 보낸 정정(「블록 B 넣지 마라」)이 늦게 닿아, 사실과 다른 문장(「알림」)이 ASC 메모에 들어갔다 → 제출 전에 사용자가 고쳤다. 원천 문안을 그대로 넣게 하기 전에 그 문안이 지금 결정과 맞는지 먼저 본다.
- 판 띠 지연을 처음엔 「반영 중 표시가 있다」고 잘못 말했다 → 스펙 · 코드 · 로그로 다시 보고 정정. 상태는 열어 보고 말한다.

## 4. 결정

| 날짜 | 결정 | 왜 |
|---|---|---|
| 2026-11-11 | 운영 연결 = 운영용 등록 진입점 · `is_demo=false` · prod 컨테이너에서 1회(OQ-01-2 닫음) | 사용자 · 이미지에 `scripts/` 없음 |
| 2026-11-11 | 점유 이동 = 응답 → 상세 조회 이벤트 연쇄 · 주기 조정 없음 | 사용자 「응답 오면 다시 API 요청」 |
| 2026-11-11 | 복귀 = 「방 배정」 **삭제**(`reason=DELETE`) · 방 옮기기 목록 「비어 있음 / 배정됨」 | 사용자 · KOS 웹 HAR |
| 2026-11-12 | 연쇄 결과를 판에 바로 반영 · 반영 대기 중 [복귀하기] 숨김 · 서버 409 | 사용자 「b로 발주해」 · 리뷰 8 |
| 2026-11-12 | 시스템 계정 dev · prod 통일 · 관리자 · 데모 계정 교체 | 사용자 |
| 2026-11-12 | 푸시 = dev 서버 → DAY Dev · prod 서버 → 정식 앱만(M-20 안 함) | 사용자 |
| 2026-11-12 | 앱 카드 테두리 = 시술현황 탭 카드만 없앰 · 설정 「정보」 → 「개인정보 처리 안내」 · 「곧 출시 예정」 그대로 | 사용자 |
| 2026-11-12 | 공개 페이지 `/privacy` · `/support` = 로그인 없이 · 60-release 승인 문안 그대로 | 사용자 · 심사 URL |
| 2026-11-12 | 시술 현황 보기 = 모든 직군 기본값 · 조작 · 수락만 직군별 · 이미 든 행 맞춤 없음(지운 행 0 실측) | 사용자 · 리뷰 9 |
| 2026-11-12 | App Privacy 7종 · 연령 12+ · 무료 · 한국만 · Unlisted 신청 | 사용자 「추천대로」 |

## 5. 날짜별 로그

- `2026-11-11` prod 준비(Key Vault 8 · prod.env · 운영 등록 진입점) · 운영 KOS 403 원인 확인 · 웹 피드백 W1 ~ W5 · 차트 모달 · 이벤트 연쇄 · 복귀 = 삭제
- `2026-11-12` W6(띠 1초) · (b) · 앱 테두리 · 설정 정보 링크 · 공개 페이지 · DAY Dev 빌드 3 · 정식 빌드 2 · prod 첫 배포 · 운영 연결 · 모든 직군 보기 · ASC · 심사 제출 · Unlisted 신청 · 마감 문서 sync

## 6. 산출물

- spec PR: MediSolveAIDev/mediness#933 · #934(스쿼시 `d7c9b313`)
- code PR(→ dev · 일반 머지): MediSolveAIDev/CENTURION_DAY#244(`382827d5`) · #246(`0b2f8cff`) · #247(`ad658b1d`) · prod = `0b2f8cff`
- Delivery: CENTURION_DAY#243(v2) · #245(v6)
- 앱: 정식 DAY 0.1.0 (2) 심사 제출 · DAY Dev 0.1.0 (3) TestFlight

- `kknaksss/prod-deploy-re1-spec-web` → `main`
  - `fc10547c` docs(day): 마감 sync — prod 첫 배포 · 정식 앱 제출 · Unlisted 실제 결과
  - `9ddbebeb` docs(day): SPEC-002 개정 ⑲ — 시술 현황 보기 = 모든 직군 기본값 · SPEC-001 규칙 9 맞춤
  - `42c0ac1a` docs(day): SPEC-001 개정 ⑦ — 공개 페이지 /privacy · /support
  - `8c1d31fe` docs(day): SPEC-003 설정 「정보」 개인정보 링크 · 60-release 앱 제출 준비 갱신
  - `93ffc695` docs(day): SPEC-003 개정 ⑪ — 시술현황 탭 카드 상태 색 테두리 없음 (A1)
  - `cf412e2e` docs(day): SPEC-002 개정 ⑱ 보충 — 연쇄 결과 판 바로 반영 · 반영 대기 중 [복귀하기] 숨김(W6)
  - `0303e6a0` docs(day): SPEC-002 개정 ⑱ — 방 옮기기 「비어 있음/배정됨」 · 점유 이동 이벤트 연쇄 · 복귀 = 「방 배정」 삭제 · 차트 모달 (CENTURION_DAY#245) · 앱스토어 준비 문서
- `kknaksss/prod-deploy-re1` → `dev`
  - `2096c92d` chore(app): 앱스토어 0.1.0 스크린샷 · 촬영 전용 진입점
  - `d8d0910f` fix: 시술 현황 보기 = 모든 직군 기본값
  - `79e730b5` feat(web): 공개 페이지 /privacy · /support
  - `1d4ccfba` feat(app): 설정 탭 「정보」 — 개인정보 처리 안내 링크
  - `01bbed49` style(app): 시술현황 탭 시술 중 카드 파란 테두리 없앰
  - `cf8f5037` fix: 점유 이동 연쇄 결과 판 바로 반영 · 반영 대기 중 [복귀하기] 숨김
  - `88210079` feat: 웹 피드백 — 차트 모달 · 방 옮기기 · 이벤트 연쇄 · 복귀 = 삭제
  - `5f7806d3` feat: prod 첫 배포 준비 — 운영 연결 등록 진입점 · prod 설정
- 리포트: `be-1` ~ `be-5` · `fe-1` ~ `fe-3` · `review-code-1` ~ `13` · `review-doc-1` ~ `10` · `mobile-*` · `doc-sync-report.md` · `delivery-*report.md`

## 7. 잔여

- Apple 앱 심사 · Unlisted 승인 결과 → 승인되면 수동 출시. 거절되면 사유 대응.
- 파비콘 = 앱 아이콘(제안 · 발주 안 함).
- 미결 OQ-51(상담 단계 · completed 방문 「배정됨」) · OQ-53(KOS 가 지운 sequence 재사용) · OQ-54(직군 둘 다인 직원) · OQ-37(10초 신호 판 전체 다시 그리기) · OQ-28 [조건 지우기] · 토스트 문구 정리(문구는 사용자) · 국적 코드 → 이름.
- 문서 정리: 4차 프롬프트 5번(낡은 「구현 전」 문장) 중 이번 sync 밖에 남은 것.
- 경고 90068: iOS 최소 13.0 → 2027-04 전 15.0 이상.
- 다음 정식 업로드 빌드 번호 3 이상 · DAY Dev 4 이상.

<!-- work-links:start -->
## 작업 기록

- [[orchestration/work/_archive/day/prod-deploy-re1/README|prod-deploy-re1]]
<!-- work-links:end -->
