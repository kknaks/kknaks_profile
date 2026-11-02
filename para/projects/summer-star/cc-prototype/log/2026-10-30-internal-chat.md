
# 작업 요약 — internal-chat (cc-prototype)

기간: `2026-10-29` ~ `2026-10-30`
결과: 운영 배포 완료(https://ccc.medisolveai.xyz · 코드 kknaksss/cc-prototype #17 · #18 · #19 · infra MediSolveAIDev/k8s_infra_mac #44 · #45 · #46) · TestFlight 빌드 12 · 13 · 14 · 문서 PR(이 워크트리)

## 1. 무엇을 했나

직원 앱(procedure · Flutter iOS)에 직원끼리 쓰는 메신저를 넣었다. 사용자 요구는 「Mattermost 참고 · 텔레그램처럼 메시지 · 사진만」이었고, Mattermost 를 researcher 로 조사(모델 · 흐름 · 라이선스 · 우리 코드에 붙일 자리)한 뒤 1:1 + 그룹 · 텍스트 · 사진 · APNs 푸시 · 안 읽음으로 1판을 세웠다(SPEC-007 · DEC-009).
그 뒤 시뮬레이터 · 실기기 피드백을 다섯 번 받으며 범위가 넓어졌다: 동영상(앱에서 H.264 변환 · Range 재생) · 여러 장 · 수정 · 5메뉴 · 하이퍼링크 · 카톡 꼴 입력줄과 [+] 시트 → [공유] = 앱 안 전달(서버가 같은 파일을 이어 씀) → 사진 · 동영상 모아보기 · 초대(1:1 → 새 그룹) · 「들어온 뒤 대화만」.
채팅과 별개로 기존 결함 둘(통역 드로어가 상태 표시줄 밑으로 올라가 못 닫음 · 바텀 시트 머리 잘림 10곳)을 같이 고쳤다. 마지막 착지는 back `bf30db4` · 빌드 14 · DEC-009 D-01 ~ D-69 · SPEC-007 0.5.x.

## 2. 적용한 기술·개념

- **Mattermost 를 「개념만」 참고하기 — 라이선스 구역을 먼저 나눔** — 오픈소스 메신저를 설계 참고로 쓸 때
  - 왜 이걸 골랐나: 모델 정의(`server/public/model`)는 Apache 2.0, 동작 흐름(`server/channels/app`)은 AGPL 구역이었다. 코드 · 이름을 옮기지 않고 필드 뜻 · 흐름만 우리 말로 다시 지어서 AGPL 파생 논란을 피했다
  - 무엇이 어려웠나: Mattermost 의 그룹 DM(G)은 멤버 고정이라 사용자 요구(추가 · 나가기)와 맞지 않았다 — 비공개 채널(P) 동작을 따라야 한다는 걸 조사에서 알았다
  - 근거: `research-mattermost-report.md` §1 · §3.3 · DEC-009 D-02 · D-07

- **안 읽음 · 다시 받기를 시각이 아니라 메시지 id 로** [[idempotency]] — 같은 초 · 같은 밀리초 경계에서 메시지를 잃지 않게
  - 왜 이걸 골랐나: 기존 DB 시각이 초 단위라 `since >` · `created_at > last_viewed_at` 이 같은 초 메시지를 버렸다(시험은 가짜 시계로 초록). 채팅 시각만 밀리초로 · `since >=` + 앱이 id 로 겹침 지움 · 안 읽음 = `id > last_read_message_id` · 「들어온 뒤 대화만」 경계도 `from_message_id`(id)로 했다
  - 무엇이 어려웠나: 앱이 삭제 뒤 자기 기기 로컬 시각(오프셋 없음)을 `updatedAt` 으로 넣어 서버가 UTC 로 읽고 9시간 미래 `since` 가 됐다 — 「since 원천 = 서버 값만」 규칙으로 막음
  - 근거: review-doc r1 F-2 · review-code r1 FAIL-1 · SPEC-007 §5 · 코드 `0f0d969` · `949969b`

- **푸시 · SSE 는 커밋 뒤, 받는 사람은 「그 메시지를 볼 수 있는 멤버」** [[apns-direct-push]] [[server-sent-events]] [[per-user-fanout]]
  - 왜 이걸 골랐나: 기존 계정 단위 SSE 허브(`send_to_account`)와 계정 → 기기 APNs 를 재사용 — 새 연결(WebSocket)을 만들지 않았다. 채팅만 만료 1일 · `thread-id` = 방
  - 무엇이 어려웠나: ① 기존 `_dispatch` 는 이벤트 루프가 없으면 경고 한 줄만 남기고 푸시를 건너뛴다 → 채팅 라우트는 전부 `async def`(동기면 실기기에서 「푸시가 안 온다」로만 보임) ② 받는 사람을 커밋 뒤 태스크에서 다시 읽어, 글과 초대가 거의 동시이면 새 멤버에게 들어오기 전 글이 푸시로 갔다 → `from_message_id < m.id` 로 거름
  - 근거: review-doc r1 F-3 · review-doc r5 FAIL-1 · `push.py:175-187` · 코드 `bf30db4`

- **「들어온 뒤 대화만」 = 읽기 길 전수** [[as-of-visibility]] [[contract-surface-enumeration]] — 사용자 「새로 초대된 사람은 이전 대화 못 보겠지?」(당시엔 다 보였다)
  - 왜 이걸 골랐나: 경계 하나를 목록 API 에만 걸면 since · 미리보기 · 안 읽음 · 첨부 열기 · 썸네일 · 전달 원본 · 수정 · 삭제 · SSE · 푸시 · 모아보기로 샌다. planner 가 V1 ~ V12 를 코드에서 grep 해 표로 만들고, backend 는 길마다 HTTP 시험 + 거름을 하나씩 빼 보는 mutation(13 중 12 죽음)으로 확인
  - 무엇이 어려웠나: 옛 DB 채우기(첫 부팅) 뒤 기존 멤버의 대화 · 안 읽음이 그대로인지 — 로컬 옛 볼륨으로 먼저 확인하고 운영 배포 전 DB 사본(`procedure.db.bak-20261029-invite`) · 운영 `from_message_id>0` = 0명 확인
  - 근거: SPEC-007 §4.6 · review-doc r5 · review-code r4 「실물 자리 1」 · `deploy.md`

- **첨부 파일 = 마지막 참조와 함께 지움 + 전달 ↔ 삭제 경합은 쓰기 잠금** [[database-lock]] — 앱 안 전달이 파일을 복사하지 않고 같은 파일을 가리키게 하면서
  - 왜 이걸 골랐나: 동영상(90MB)을 대상마다 복사하면 볼륨이 금방 찬다. 대상마다 첨부 행만 새로 · 파일은 공유 · 삭제는 남은 참조가 0 일 때만(D-66)
  - 무엇이 어려웠나: 전달이 원본 확인을 잠금 전에 해서, 같은 파일의 마지막 참조 삭제와 겹치면 파일 없는 전달본이 생겼다 → 전달 tx 첫머리 `BEGIN IMMEDIATE` · 삭제와 같은 순서. 두 연결로 겹침을 재현하는 시험(잠금을 빼면 실패)을 남김
  - 근거: review-code r3 W3-2 · 코드 `8a6688b` · `test_chat_forward_vs_last_delete_race`

- **포맷은 「다 받고 한 꼴로 바꿔 보낸다」 — iOS 네이티브 변환** — 사용자 「기기별로 사진 · 동영상 포맷 다 지원」
  - 왜 이걸 골랐나: 받는 쪽 재생 문제를 없애려 사진 = JPEG 2048 · 동영상 = H.264 MP4 1280 + 썸네일로 앱이 바꿔 올린다. 서버는 Range(206)로 끊어 준다
  - 무엇이 어려웠나: 권장 패키지 `video_compress`(20개월 전 판)는 실패를 오류로 안 돌려주고(path! 크래시) 한 번에 하나만 받아 `AVAssetExportSession` 네이티브 채널로 갈아탔다. 재생 플러그인은 오디오 세션을 `.playback` 으로 올려 무음 스위치를 무시 → `.soloAmbient` 로 바꾸는 채널. 업로드 진행률은 「읽은 바이트」라 셀룰러에서 100% 에 서 있음 → 되밀기 있는 스트림
  - 근거: review-code r2 W-2 · W-4 · 코드 `edabe00` · `AppDelegate.swift`

- **업로드 한도는 앞단부터 센다 — Cloudflare 100MB · ingress 10m · local-path quota 없음** [[reverse-proxy]] [[kubernetes]]
  - 왜 이걸 골랐나: 동영상 한도를 100MB 로 정했다가 infra 를 열어 보니 운영 길이 Cloudflare(요청 본문 100MB) → ingress `proxy-body-size: 10m` 이었다 → 서버 한도 90MB · ingress 100m. 사진 PVC 1Gi 를 20Gi 로 올리려 했으나 local-path 는 quota 가 없고(1Gi 넘게 써짐) `allowVolumeExpansion` 이 없어 값만 바꾸면 ArgoCD sync 실패 → 1Gi 그대로 + 주석
  - 근거: DEC-009 D-58 · D-59 · `infra-report.md` · infra #44

- **확정 시안이라도 DS 컴포넌트를 쓰는지 센다** [[design-system]] — Claude Design 시안 r1 이 medikit 컴포넌트 0회 · 손 CSS
  - 왜 이걸 골랐나: 워커 자체 검증이 「클래스가 모두 DS」였고 코디도 그대로 넘겼다. 사용자 「디자인 시스템이 하나도 안 들어가 있다」 → `x-import` 개수를 기준 시안과 나란히 세는 것을 검증 조건으로(r2 = 316)
  - 근거: `design-chat-report.md` r1 · r2 · 메모리 feedback-design-brief-ds-components

- **바텀 시트 · 드로어 높이 = 놓인 칸 기준 + 위 안전 영역 아래** [[viewport-aware-overlay]] — 통역 드로어 · 전달 시트에서 같은 결함 두 번
  - 왜 이걸 골랐나: 높이를 화면 전체 × 0.92 로 잡고 탭바 위 본문 안에 그려 머리가 상태 표시줄 밑으로 밀렸다(손잡이가 잘려 못 닫음). 공용 도우미 `showAppSheet` 로 10곳을 바꾸고 직접 `showModalBottomSheet` 호출 0 을 grep 시험으로 잠금. 키보드: 셸이 본문에 키보드 높이를 다시 넘겨 입력줄이 한 번 더 떠 있던 것도 같은 뿌리
  - 근거: sim-feedback F6 · F9 · review-code r3 W3-1 · 코드 `216b154` · `8a6688b`

## 3. 막혔던 것 / 사고

- **시안 r1 을 DS 검사 없이 사용자에게 넘김** → 「클로드 디자인으로 한 거 맞아?」 반려. 원인은 브리프 검증 조건(클래스만) — x-import 수를 세는 조건으로 고치고 메모리에 남김
- **「공유」를 iOS 시스템 공유 시트로 읽음** → 사용자는 카톡처럼 앱 안 방으로 전달을 원했다. 시스템 공유 · 저장 빼기 · 임시 파일 흘려 받기까지 한 판을 짓고 걷어냄. 메신저 용어(공유 · 첨부 · 초대)는 카톡 화면 기준으로 먼저 확인할 것
- **입력줄을 카톡 PC 스샷으로 읽음** → 큰 네모 입력칸 + 아래 줄로 지었다가 모바일 알약으로 다시. 앱이면 모바일 스샷을 달라고 할 것
- **문서 처분을 브리프 §0(SPEC 보다 이김)로 먼저 내고 SPEC 동기를 뒤로 미룸** — 속도는 났지만 처분 문서가 r3 · r4 · r5 로 쌓여 planner 동기 범위가 매번 23줄까지 커졌다
- **워커 터미널을 일찍 닫아 문맥을 버림**(planner · backend 여러 번) → 같은 영역 수정 때 새 워커가 처음부터 읽음. mobile 은 열어 둔 한 터미널을 끝까지 재사용해 빨랐다
- **시뮬레이터가 중간에 꺼져 있었음**(설치 실패 `Unable to lookup in current state: Shutdown`) → 설치 전 boot · bootstatus 를 늘 같이
- **orca 가 코드 워크트리에 빈 셸 터미널(..internal-chat)을 여러 개 만들어 둠** → 마감 때 정리

## 4. 결정

| 날짜 | 결정 | 왜 |
|---|---|---|
| 2026-10-29 | 1:1 + 그룹(추가 · 나가기 = Mattermost P 동작) · 텍스트 + 사진 · APNs 푸시 · 앱만 · 상대 = 로그인 가능 계정(나중에 전 직원) | 사용자 · 조사 |
| 2026-10-29 | 디자인 = Claude Design 시안 먼저 → r2 확정 = 화면 정본 · 헤더는 10-28 AppHeader 가 이김 | 사용자 |
| 2026-10-29 | ~~영상 없음 · 사진 1장 · 수정 없음~~ → 동영상(3분 · 90MB · H.264 1280) · 여러 개 10 · 수정(내 텍스트 · 「수정됨」) | 사용자 시뮬레이터 피드백 |
| 2026-10-29 | 입력줄 = 카톡 모바일 알약 · 키보드 열리면 탭바 숨김 | 사용자 |
| 2026-10-29 | ~~[공유] = iOS 공유 시트(저장 뺌)~~ → 앱 안 전달(검색 · 초성 · 10곳 · 같은 파일) | 사용자 실기기 |
| 2026-10-29 | 동영상 서버 한도 90MB(Cloudflare 100MB) · ingress 100m · 사진 PVC 1Gi 그대로(local-path quota 없음) | 코디 확인 · infra 리포트 |
| 2026-10-29 | 사진 · 동영상 모아보기 · 초대(1:1 → 새 그룹 · 「A님이 B님을 초대했습니다」) · ~~다시 초대되면 옛 대화 전부~~ → 들어온 뒤 대화만 · 1:1 진짜 나가기(F12)는 안 함 | 사용자 |

전체 결정 표(D-01 ~ D-69 · 뒤집힌 줄 포함)는 `para/projects/summer-star/cc-prototype/10-decision/decision-009-internal-chat.md` · 아카이브의 `_RESUME.md` §2.

## 5. 날짜별 로그

- `2026-10-29` 착수 · Mattermost 조사 · BASE-010 · DEC-009 · Claude Design 시안 r1(반려) · r2 확정 · SPEC-007 0.1 → 0.2 · 1판 구현 · 시뮬레이터 · 피드백 F1 ~ F6 · 2판(동영상 · 수정 · 5메뉴 · 알약) · 운영 배포 #17 · 빌드 12 · F7 전달 · F9 통역 드로어 · #18 · 빌드 13 · F10 정렬 · F11 · F13 · F14 · #19
- `2026-10-30` 운영 배포 #19(모아보기 · 초대 · 들어온 뒤 대화만) · 빌드 14 · 마감

## 6. 산출물

- 문서: BASE-010 · DEC-009(D-01 ~ D-69) · SPEC-007 0.5.x · WORK-011 · SPEC-004 가리킴 줄 · `deploy.md` 기록 3줄
- code PR: kknaksss/cc-prototype #17 · #18 · #19 · infra MediSolveAIDev/k8s_infra_mac #44 · #45 · #46
- 리포트(이 폴더): `research-mattermost-report.md` · `design-chat-report.md` · `spec-report.md` · `spec-r2..r6-report.md` · `review-doc-r1..r5.md` · `review-code-r1..r4.md` · `infra-report.md` · `sim-feedback.md` · `r3/r4/r5-dispositions.md`
- 시안: Claude Design `dda9a931` 「Ceramique 의료진 앱 — 채팅」 · 사본 `design/`

## 7. 잔여

- **코드 리뷰 r4 WARN 3**(고치지 않고 마감 · SPEC §15 OQ): ① 꺼진 기기의 열린 대화 — 같은 구성으로 나갔다 다시 초대되면 옛 메시지가 남음(앞으로 올 때 열린 방은 처음 50 다시 받기로 고침) ② 모아보기 칸 누름의 404 확인이 메모리 캐시에 막힘 ③ 아이패드에서 다른 기기로 나가도 방 정보 시트(격자)가 남음
- **실기기 E2E C1 ~ C21 사용자 확인** — 시뮬레이터로 못 본 것: 카메라 칸 · 원격 푸시 · 잠금 화면 · 무음 스위치 · 셀룰러 업로드 진행률 · 실제 HEVC 4K · 슬로모 변환 · 90MB 근처 동영상(Cloudflare 앞단)
- **법적 검토**(OQ-902): 고객 정보가 채팅 · 사진 · 동영상으로 오가는 것 · 사진 볼륨 암호화 없음
- **전 직원 계정 발급**(OQ-901): 지금은 역할별 PoC 계정만 채팅 상대로 보임
- **운영 DB 사본** `/data/procedure.db.bak-20261029-invite`(PVC 안) — 이상 없으면 지울지 사용자 판단
- SPEC-004 §7.3 경로 수 49 ↔ 코드(채팅 전 51 · 지금 71) 문장 낡음(OQ-920)
