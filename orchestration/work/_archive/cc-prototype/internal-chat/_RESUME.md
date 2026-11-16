
# 재개 노트 — internal-chat (cc-prototype)

**지금**: r5 배포 끝 — 코드 #19 `bf30db4` · infra #46 `15a1b39` · 운영 DB 사본 `/data/procedure.db.bak-20261029-invite` · Synced Healthy · TestFlight **빌드 14** 업로드 · 코드 리뷰 r4 = FAIL 0 · WARN 3(`review-code-r4.md` — 다음 빌드 몫) → 사용자 실기기
**다음**: 리뷰 r4 WARN 3 + 실기기 피드백 묶어 한 번에 → 빌드 15 · 그 뒤 마감(SPEC 0.5.1 동기 · 문서 PR · archive · 정리)

세팅: `scripts/new-work.sh cc-prototype internal-chat` · 설정 SSOT `config/projects/cc-prototype.json`
코디handle: `term_61179808-14b1-431b-a85f-619d2c232e8e` (10-29 cc59b27c → 61179808 로 되살아남. 발주 직전마다 terminal list)

## 워크트리



## 1. 지금

열린 것만 둔다. 닫히면 지우고 §5 이력으로 내린다.

- [~] 사용자 실기기 E2E(빌드 12) — 피드백은 `sim-feedback.md` 에 기록만
- mobile 터미널 `term_b3bc20ff…` 열어 둠(수정용)
- [ ] SPEC 0.3.1 동기(r3-dispositions)
- [x] infra 변경 완료(미커밋 · 워크트리 `/Users/kknaks/orca/workspaces/k8s_infra_mac/internal-chat`): proxyBodySize 100m · photo 1Gi 그대로 + quota 주석(B 처분 · D-59) · docs 정정 · helm lint/template 통과 · kubectl · sync pending → 배포 때 infra PR
- [!] 시뮬레이터 2대 · 로컬 back `cc-internal-chat` 떠 있음(옛 1판 코드)
- [!] 마감 때 정리: compose `cc-internal-chat`(컨테이너 · 볼륨 2) · 시뮬레이터 2대 · `ios` swiftpm Package.resolved 2개 미추적(커밋 여부)
- [ ] SPEC-007 동기: 브리프 §0 W2-1 ~ 6 처분을 SPEC 에 (planner · E2E 뒤) · 문서 PR
- [!] 코드 워크트리 ignored: `procedure/.env` · `app/ios/Flutter/Signing.xcconfig` (canonical 에서 복사) — 마감 전 확인
- [!] OQ-920 경로 수 SPEC-004 49 ↔ 코드 51 — SPEC-004 §7.3 은 열린 채로(다음에 SPEC-004 손볼 때)
- [!] 코드 워커(backend · mobile)는 SPEC · WORK 가 닫힌 뒤에만 발주한다. `new-work.sh cc-prototype internal-chat --workers backend,mobile`

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-10-29 | 앱(procedure/app)에 내부 채팅. 텔레그램처럼 메시지 · 사진만. Mattermost 참고 | 사용자 입력 |
| 2026-10-29 | 방 = 1:1 + 그룹방 · 새 메시지 APNs 푸시 넣음 · 앱만(웹 없음, API 는 웹이 붙을 수 있는 모양) · researcher 조사 발주 OK | 사용자 선택 |
| 2026-10-29 | 상대 목록 = active + 로그인 가능 계정. 지금은 PoC 1명씩이지만 나중에 전 직원이 채팅 → 코드 변경 없이 늘어나야 함 · 전 직원 계정 발급은 OQ-901 | 사용자(「나중에 전체 직원들 다 채팅」) |
| 2026-10-29 | 잠금 화면 = 보낸이 + 본문 앞부분 | 사용자 선택 |
| 2026-10-29 | 리포트 §6 41건 = 코디 기본값으로 DEC-009 D-01 ~ D-34 · BASE · DEC 작성 후 planner 발주 「진행」 | 사용자 선택 |
| 2026-10-29 | 앱 디자인 = claude design 시안 먼저 → 확정 시안이 정본으로 SPEC | 사용자 선택 |
| 2026-10-29 | 시안 r2 확정 = 화면 정본 · 「확인할 것」 기본값 전부 받음 · 제안 4건 안 넣음 → DEC-009 D-35 ~ D-37 | 사용자(「응 이렇게 가자」) |
| 2026-10-29 | 4차: F11 사진 · 동영상 모아보기 · F13 초대(1:1 → 새 그룹 · 「A님이 B님을 초대했습니다」) · F14 들어온 뒤 대화만(다시 초대도) → D-67 ~ D-69 · F12(1:1 진짜 나가기) 안 함 | 사용자(「f11, 13, 14 만」 · 「응」) |
| 2026-10-29 | review-doc r4 사용자 판단 후보 3 = 코디 기본값: 초성 검색 = 세 곳 전부 · 전달 시트 같은 사람 두 번 안 보임 · 일부 실패 = 시트 유지 + 실패한 곳만 고른 채 · D-66 파일 = 마지막 참조와 함께 지움 | 코디 기본값 |
| 2026-10-29 | 실기기 F7 · F9 → D-62 ~ D-65: 공유 = 앱 안 전달(시스템 공유 없앰 · 검색 · 초성 · [전체][사람] · 10곳 · 같은 파일 이어 씀 · 「전달됨」 없음) · 통역 드로어 높이 결함 고침 · 시스템 공유 [더보기] · [최근 공유] 칩 = 없음(코디 기본값) | 사용자 「응 발주하자」 |
| 2026-10-29 | 시뮬레이터 피드백 → DEC-009 D-46 ~ D-57. 동영상(3분 · 100MB · H.264 MP4 1280) · 여러 개(10 · 메시지 하나씩) · 수정(내 텍스트만 · 「수정됨」) · 공유 = 저장 빼기 · 하이퍼링크 · [+] 시트(최근 줄 + 「사진」) | 사용자 F1 ~ F4 · 「응 이제 발주해」 · 세부 = 코디 기본값 |
| 2026-10-29 | review-doc r2 WARN 6 처분 = 브리프 §0(SPEC 보다 이김 · 뒤에 SPEC 동기) · W2-1 → DEC D-45(처음 추가 = 그때 마지막 메시지까지 읽음) | 코디 기본값 |
| 2026-10-29 | **앱 구현까지 이어서 진행 · 코드 발주 재승인 불필요 · 끝나면 시뮬레이터 띄워 사용자가 본다** — 순서: r2 → review-doc r2 → 문서 PR → backend ∥ mobile → reviewer 코드 → 코디 검증 → 로컬 back + 시뮬레이터 2대(계정 둘) | 사용자(「앱 구현까지 다 끝내고 시뮬레이터 켜놔 내가 볼게」) |
| 2026-10-29 | review-doc r1 처분: 헤더 = 지금 AppHeader + 아래 [새 대화](시안보다 이김) · 앱 앞 채팅 = 앱 안 배너만 소리 없음 · 보고 있는 방 = 채팅 탭 + 맨 위 · 실패 말풍선 저장 안 함 · 비활성 1:1 입력 막음 · 재초대 = 읽음 · 숨김 = 어느 길이든 → DEC-009 D-38 ~ D-44 | 사용자 선택 2 + 코디 기본값 |
| 2026-10-29 | (코디 기본값 · DEC 전) procedure/back+app · 채팅 탭 추가 · 기존 account · 텍스트+사진 · 내 메시지만 삭제 · SSE 허브+REST · last_viewed_at 안 읽음 배지 · 사진 = ccc 볼륨 Bearer · Mattermost 는 개념만 | 코디 제시, 사용자 이의 없음 |

뒤집힌 결정은 지우지 않는다. ~~취소선~~ 을 긋고 같은 행에 뒤집은 날짜와 사유를 남긴다 —
지우면 왜 그렇게 갔는지가 사라져서 같은 논의를 다시 한다.

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.** 워커 보고는 dispatch preamble 의 값을 따르므로
여기 옛 핸들을 남겨 두면 어느 것이 산 것인지 판단이 안 된다.

## 4. 산출물

- spec PR: <링크>
- code PR: <링크>
- 리포트: `research-mattermost-report.md` (완료) · `design-chat-report.md` (r2 확정 · sha 7148eb3fc0e0) · `spec-report.md` (완료) · `review-doc-r1.md` (FAIL 4 · WARN 17) · `spec-r2-report.md` (대기)
- 문서: BASE-010 · DEC-009 (proposed · 미커밋) · config `designer` 워커 + `roles/cc-prototype/designer/` 신설
- 커밋: `<sha>` — <한 줄>

## 5. 이력 (최신이 위)

- `2026-10-29` 리뷰 r3 WARN 3 → back(경합 잠금 · 522) · app(공용 시트 · 보내는 중 · 235) → 커밋 8a6688b → PR #18 머지 · infra #45 · sync · 빌드 13 업로드
- `2026-10-29` r4: planner SPEC 0.4.0 · review-doc r4 WARN 5 → r4-dispositions · BE4 · APP6 완료 → 리뷰 r3 · 시뮬레이터 재설치
- `2026-10-29` 사용자 「TestFlight 배포」 → 코드 PR #17 머지 · back 이미지 · infra PR #44(back.imageTag · body 100m · PVC 주석) 머지 · sync · 운영 확인 · 빌드 12 업로드
- `2026-10-29` mobile r3 완료(test 216 · 기존 결함 키보드 이중 차감 · 아이패드 레일 넘침 같이 고침) → 커밋 → 재설치
- `2026-10-29` 사용자 2차 F5 · F6 → D-60 · D-61 → mobile 수정 r3 발주
- `2026-10-29` 리뷰 r2 FAIL 0 · WARN 7 → mobile 수정(test 213) → 커밋(2판) · 시뮬레이터 재설치
- `2026-10-29` BE3 완료(pytest 515) · APP4 · APP5 완료(test 210 · 동영상 변환 = iOS 네이티브 채널 — video_compress 실패 처리 불가) · back 재빌드 · 시뮬레이터 재설치 · 리뷰 r2 발주
- `2026-10-29` planner r3 → SPEC 0.3.0 · review-doc r3 FAIL 2 · WARN 8 → r3-dispositions · infra 워커(B 처분 · 미커밋) · BE3 ∥ APP4-5 발주
- `2026-10-29` 사용자 시뮬레이터 피드백 F1 ~ F4 → DEC D-46 ~ 57 · 코드 커밋 0f0d969 · planner r3 발주(`term_18cdaeff…` · task_fb44d9c5a31b · ctx_b032bca05dcb)
- `2026-10-29` mobile 수정 r1 완료(test 186) → 시뮬레이터 2대 설치 · 실행 · 사용자에게 넘김. mobile 터미널 열어 둠(피드백 수정용)
- `2026-10-29` backend 완료(pytest 500 · 코디 재확인) · mobile 완료(test 184 · 코디 재확인) · reviewer 코드 r1 FAIL 1 · WARN 1 · 나머지 PASS → mobile 수정 발주 · 로컬 back + 시뮬레이터 준비
- `2026-10-29` planner r2 → SPEC-007 0.2.0 · reviewer_doc r2 WARN 6 → 처분 → new-work backend,mobile(코드 워크트리) · 두 워커 발주
- `2026-10-29` reviewer_doc r1 FAIL 4 · WARN 17 → 사용자 결정 2 → DEC D-38 ~ 44 → planner r2 발주 · reviewer 터미널 닫음
- `2026-10-29` planner 완료 — SPEC-007 · WORK-011 · SPEC-004 3줄 · 코디 확인(D9 37 grep · SPEC-004 diff) → reviewer_doc 발주
- `2026-10-29` designer r2 완료(x-import 316 · 손 CSS 0 · 코디 확인) → 사용자 확정 → planner 발주 · designer 터미널 닫음
- `2026-10-29` designer r1 완료(25장) → 사용자 반려 「DS 하나도 안 들어감」 — x-import 0 · 손 CSS(.v3b · .v3in). 브리프 검증이 클래스만 봐서 통과. r2 = 컴포넌트 전환 · x-import 수치 검증
- `2026-10-29` researcher 완료(정할 것 41) → 사용자 결정 3 → BASE-010 · DEC-009 작성 · designer 워커 신설 · 발주
- `2026-10-29` 착수. slug internal-chat · 사용자 결정 4건 · researcher 발주

이 절은 **재개에 필요한 만큼만** 쓴다. 회고·배운 것은 `SUMMARY.md` 몫이다.
