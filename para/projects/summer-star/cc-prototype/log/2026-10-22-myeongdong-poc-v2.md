
# 작업 요약 — myeongdong-poc-v2 (cc-prototype)

기간: `2026-10-20` ~ `2026-10-22`
결과: 머지 · 배포 완료(2026-10-21, https://ccc.medisolveai.xyz = 시술 현황판으로 교체) · iOS 앱 TestFlight 빌드 1 ~ 3 — 코드 `kknaksss/cc-prototype#3` · `#4` · `#5` · infra `MediSolveAIDev/k8s_infra_mac#22` · `#23` · `#24` · 문서 `kknaks/kknaks_profile#99`

## 1. 무엇을 했나

10-16 명동점 현장 인터뷰에서 나온 진짜 문제(원장 호출을 놓친다 · 마취 시간을 「마취용」 가짜 계정과 손글씨로 잰다 · 오더지를 출력해 방 번호와 꽂아 둔다)를 풀려고, 1 · 2차 시드 데모를 버리고 **KOS 데모 지점에 실제로 붙는 시술 현황판**을 새 기능 폴더 `procedure/`(FastAPI + Next.js + SQLite)로 만들었다.
간호 스테이션 웹(오더지 카드 · 마취 타이머 · 시술 골라 의사 호출 · 의국 「호출」 탭 수락 · 시술마다 [시작]/[종료] · 귀가 대기)이 KOS 공개 API + **HAR 로 찾은 내부 API 쓰기 체인**으로 KOS 를 직접 움직이고, 10초 조회 · SSE 로 화면이 실시간으로 맞는다.
같은 back 위에 시술실 · 원장용 **Flutter iOS 앱**(계정 3종 · 권한 · 통역 · APNs 원장 호출 푸시 · 알림에서 바로 [수락])을 얹어 TestFlight 로 아이폰 · 아이패드에 깔았고, 웹 E2E 12 · 앱 7 · 실기기 8 피드백을 반영한 뒤 정상 로그인(bcrypt · 잠금)까지 넣어 배포했다. 마지막에 데모 환자 190건을 KOS 데모 지점에 채우는 스킬과 「구현 v3」 시안 4개로 문서 · 시안을 코드에 맞췄다.

## 2. 적용한 기술·개념

- **KOS 내부 API 쓰기 체인(HAR 역공학)** — 공개 API 에 없는 호출 · 수락 · 완료 · 방 · 작업 취소를 KOS 웹이 쓰는 내부 API 로 보낸다
  - 왜 이걸 골랐나: 공개 API(쓰기 25개 전수)에는 담당자 · 호출 · 집도의 · 완료 쓰기가 없다. 「KOS 에 요청」은 PoC 기간 안에 안 된다 → HAR 로 경로 · 본문을 읽고 데모 지점에 실호출로 하나씩 확인(10-20 4종 200 · 10-21 관리자 권한 재확인 · 다른 원장 id 로 대신 수락 200)
  - 무엇이 어려웠나: ① `sign-in` 응답 id 를 담당자로 넣으면 **200 을 주고 무시** — 진짜는 `get-user-account` 의 `data.id` ② 같은 단계로 `change-flow-step` 하면 400 ③ 시술 작업에 방이 없으면 `call-tasks-doctors` 400 `roomId NotFound`(방은 「방 배정」 ETCETERA 작업에만) → 호출 앞에 `change-tasks-room` 을 끼워 **방 → 담당자 → 호출** ④ [귀가 대기]를 flow-step 만 보내면 「방 배정」이 준비중으로 남아 방이 안 빈다 → `cancel-flow-tasks` → `PROCEDURE_DONE`
  - 근거: `procedure/back/app/domain/kos_ops.py:12-18` · `:29` · `:55` · `kos/client.py:27` · `_RESUME.md` §2 10-20 · 10-21 「(사실)」 줄 · `e2e-feedback-batch-1.md` #1 · #3 · SPEC-003 §8
- **조작 대기열 + 1.5초 확인 조회** — ccc 상태를 먼저 바꾸고 KOS 반영은 `kos_op` 대기열로(확인 · 재전송 · 3회 실패 · 뒤 op 멈춤)
  - 왜: 조작 응답이 KOS 를 기다리면 화면이 굳는다. 대신 「KOS 반영 중 · 실패」를 카드에 보이고, KOS 에 있는 값은 10초 조회로 KOS 기준 덮어쓰기(반영 대기 중인 필드만 보호)
  - 무엇이 어려웠나: 처음엔 「앞 op confirmed(= 다음 10초 조회) 뒤 다음 op」 → 방 · 담당자 · 호출 3단계가 KOS 에 20 ~ 30초 늦게 떴다(E2E-6). 2xx 면 바로 다음 op · 보낸 게 있으면 1.5초 뒤 조회 1회. 그러자 앞 op(호출 WAITING)의 확인 조건이 뒤 op(수락 READY)에 덮여 영영 안 맞아 **재전송이 KOS 를 되돌리는** 문제 → 「뒤 op 이 같은 값을 바꿨으면 앞 op 은 확인」(`superseded`)
  - 근거: `back/app/kos/runtime.py:23` · `kos/ops.py:27` · `:70` · SPEC-003 §4.4 · 리뷰 r1 W1 · W2 · r2 N2
- **SSE 전체 스냅샷** — 현황판 · 의국 화면 · 앱이 같은 `board` 이벤트 하나를 받는다
  - 왜: 폴링은 의국 화면에서 호출이 늦게 보인다(사용자 「의국에서도 실시간으로」). 바뀐 것만 보내면 합치기 · 순서 · 빠진 이벤트 복구가 front · 앱에 생긴다 — 하루 한 구역이라 스냅샷이 작아(HAR 15건 ≈ 32KB) 통째로 보내고 규칙 계산(`canStart` 등)은 back 한 곳에
  - 무엇이 어려웠나: `EventSource` 는 헤더를 못 실어 `?token=` → 접근 로그에 토큰이 남는다(리뷰 F3) → uvicorn 쿼리 지움 필터. 시간 경과로 바뀌는 「확인이 필요」 때문에 10초마다 무조건 발행. Flutter 는 `EventSource` 가 없어 스트림 요청 + 직접 파서 · 45초 무소식이면 재연결. 배포는 ingress 버퍼링 끔 · timeout 3600s
  - 근거: `back/app/api/board.py:15` · `main.py:27` · `app/lib/sse/sse_parser.dart` · infra #22 · SPEC-003 §7.5 · SPEC-004 §7.1
- **APNs 직접(ES256 JWT · HTTP/2) + 알림 액션 수락** — Firebase 없이 원장 호출 푸시, 잠금 화면 · Apple Watch 에서 바로 [수락]
  - 왜: 앱이 iOS 만이라 FCM 을 끼울 이유가 없다(의존 0 · 키 하나). 원장이 앱을 열지 않고 받게(사용자 「와치에도 · 수락 버튼까지」)
  - 무엇이 어려웠나: JWT 는 20 ~ 60분 재사용 → 40분 · `.p8` · Team ID 는 레포 밖. 의사 알림에만 카테고리 `CALL`(관리자는 원장을 골라야 해서 액션 없음). 수락은 Flutter 가 아니라 **네이티브 `AppDelegate` 가 키체인 토큰으로 백그라운드 요청**(앱이 꺼져 있어도) → 결과를 로컬 알림 한 줄로. 번들 id 를 바꾼 뒤 옛 토큰이 400 `DeviceTokenNotForTopic` → 죽은 토큰 400 3종 · 410 이면 기기 행 삭제. 발송은 `push_log`, 수락 출처는 `X-Accept-Source` 로
  - 근거: `back/app/push/apns.py:17` · `:30` · `:43` · `service/push.py:27` · `:97` · `api/actions.py:42` · `app/ios/Runner/AppDelegate.swift:23-25` · SPEC-004 §5-1
- **Flutter iOS → TestFlight** — 시안(간호사 모바일 · 시술실 태블릿)을 Flutter 로, 사용자 맥북에서 빌드 · 업로드 · 내부 테스터 설치
  - 왜: 시술실은 태블릿 · 폰. 웹으로는 푸시 · 백그라운드 수락 · 마이크 통역이 약하다. 내부 테스터는 심사가 없다
  - 무엇이 어려웠나: 팀 id · 번들 id 를 public 레포에 안 넣으려고 `Signing.xcconfig`(gitignore) 의 `APP_BUNDLE_ID`. 처음엔 기기 back = 같은 Wi-Fi 맥 IP(ATS 로컬 허용) → 「배포 먼저」로 바뀌어 release 는 배포 주소 고정 · 서버 주소 칸은 debug 만(T8). 앱 아이콘이 Flutter 기본(A7) · 빌드 번호는 업로드마다 +1 · 최소 iOS 15
  - 근거: `app/lib/config/server.dart:40` · `ios/Podfile:2` · 코드 #4 · #5 · SPEC-004 §2.4
- **k8s Secret 파일 마운트 — `/run/secrets` 함정** — APNs `.p8` 를 Secret 파일로
  - 무엇이 어려웠나: Secret 을 `/run/secrets` 에 통째로 ro 마운트 → `/var/run` = `/run` 이라 kubelet 의 서비스계정 토큰 마운트가 막혀 back CrashLoop(`mkdirat … read-only file system`). → `/etc/apns` 로 옮기고 `automountServiceAccountToken: false`(back 은 k8s API 를 안 쓴다)
  - 근거: infra #23 본문 · SPEC-004 §2.3 `APNS_KEY_PATH`
- **이미지 태그 = 커밋 전체 sha · ArgoCD 수동 sync** — `latest` · `main` 태그 없음
  - 왜: 무엇이 떠 있는지 차트 값 하나로 알 수 있게 · 잘못 추측한 태그로 배포하지 않게(차트가 `image.tag` 없으면 렌더 실패)
  - 무엇이 어려웠나: Actions 는 `github.sha`(40자)로 민다 — 차트 `values-prod.yaml` 도 40자여야 한다(PR 제목의 7자 sha 로는 이미지가 없다). ConfigMap 이 바뀌면 back 재시작이 필요해 sync 는 코디가 수동(`cc-prototype-prod`)
  - 근거: `.github/workflows/procedure-back-image.yml:45` · infra #22 차트 `required "image.tag …"` · #24(`329b543…` 40자) · `_RESUME` 10-21 「태그 = 전체 sha」
- **bcrypt 로그인 · 잠금** — 계정 카드(비밀번호 없음)에서 아이디 + 비밀번호로(OQ-601)
  - 왜: 배포 주소가 공개다. 카드 목록 API 자체가 계정 이름을 흘린다 → 목록 API 제거
  - 무엇이 어려웠나: 비밀번호 원천 = env/Secret → 서버 시작 · 계정 동기화 때 해시(맞으면 다시 안 만듦). 없는 아이디 · 틀린 비밀번호 · 해시 없는 계정을 같은 401 · 같은 시간(가짜 해시 비교)으로. 같은 아이디 5회 실패 → 1분 429(메모리) · 72바이트 넘는 비밀번호
  - 근거: `back/app/service/auth.py:35-38` · `service/accounts.py` `_passwords` · 코드 #4 · SPEC-004 §3.3
- **권한은 back 이 조작 API 마다** — 의사 = 자기 원장으로만 수락 · 지정 호출은 지정 원장만 · 간호사 수락 403 · 관리자는 원장을 골라 수락
  - 왜: 앱 버튼 숨김만으로는 안 된다(사용자 「권한 체크는 중요」). 역할 · 원장 id 는 토큰이 아니라 DB 의 지금 값으로
  - 근거: `back/app/service/actions.py` `accept` · SPEC-004 §3.4
- **`reserveV2` 예약 그룹 지정** — 데모 고객을 국적별 예약 칸(4층 5칸)에 슬롯당 2명
  - 무엇이 어려웠나: `reserveByTimeSlot` 은 그룹을 못 정해 **전부 기본 그룹(국내)** 에 들어갔다 → `reserveV2` 의 `occupiedResources[].reservationGroup` 으로 · 국내 아닌 32건 취소 후 재생성. 공개 API 로 만든 내원객은 모두 첫내원(재내원 불가) · 접수 · 수납 · 방 배정 API 가 없어 카드로 띄우려면 KOS 화면
  - 안전: 데모 표식 계정이 없으면(= 운영) 멈춤 · 예약 메모 표식으로 우리 것만 list/delete
  - 근거: `procedure/tools/kos_demo_patients.py:33` · `:115` · `:259-262` · `.claude/skills/kos-demo-patients/SKILL.md` · 코드 #5 · `demo-patients-2026-10-22.md`
- **반응형 글자 배율** — 아이패드에서 웹 디자인 시스템 px(캡션 13 등) 그대로라 글자가 작았다(T4 「반응형 고려해서 비율로 했어?」)
  - 무엇을: 폰 = 1 · 태블릿 = 짧은 변 / 700(1.15 ~ 1.3)을 `MediaQuery.textScaler` 로 모든 글자에, 버튼 높이 · 격자 최소 폭도 같은 배율. 웹 카드 높이도 같은 결(E2E-12) — 판 높이 절반을 `100cqh` 로
  - 근거: `app/lib/theme/tokens.dart:75-76` · `front/app/(main)/procedures/live/page.tsx:199` · `e2e-device-feedback-batch-1.md` T1 ~ T4
- **ccc DB 가 KOS 를 품는다** — 모든 행 = ccc id + `kos_id` · KOS 원천은 덮어쓰고 ccc 에만 있는 것(마취 · 호출 기록 · 수락 · [시작] · 귀가 대기)은 이벤트 로그로 쌓기만
  - 왜: 장기 방향이 「KOS 를 화면 하나씩 교체」 — 원천만 바꾸면 되게. 호출은 지우지 않고 「유효 호출 = 가장 최근 호출」로 수락 범위 · [시작] 조건을 계산(되돌리기는 나중에 로그로)
  - 근거: SPEC-003 §3 · §5.4 · DEC-005 D-12 · D-25

## 3. 막혔던 것 / 사고

- **시안 v1 반려** — 배포 현황판과 구조 · 테마 · 글자 · 카드가 달라 「완전히 다른 프로그램이야?」. 원인 = 브리프가 기준을 옛 claude design 시안으로만 주고 배포 코드(`cc/front`)를 주지 않았다 → r2 는 배포 코드 기준 · 결국 사용자가 claude design 에서 직접 고친 r3/r4 를 확정본으로(`design-feedback-batch-1.md`)
- **코디가 BASE · DEC 를 직접 쓰고 SPEC 까지 쓰려다 질책** — 「워커 보내서 구현 - 리뷰 - 수정으로 가야지」. 이후 SPEC · WORK 는 planner 발주(메모리 「스펙 문서도 워커로」)
- **카드 높이를 px 로 박았다** — E2E-5 를 「2줄 고정 + 안 스크롤 + 최소 360px」로 구현 → 「화면에 절반 정도는 나와야 · 하드코딩 하지 말라」(E2E-12). 비율(`100cqh`) · 카드 안 스크롤 없음으로
- **E2E-3 되돌림이 잘못 전송됐다** — 사용자가 거절한 명령 안에서 backend 에 「E2E-3 되돌림」이 실제로 나가 [귀가 대기]의 방 배정 취소가 한 번 빠졌다 → 정정 지시로 복구(시험 3 passed). 거절된 명령도 부작용이 남는다
- **귀가 대기 카드가 두 번 뒤집혔다** — 흐리게 남김(10-20) → 판에서 없앰(E2E-8) → 다시 남김 · KOS `COMPLETED` 때 사라짐(E2E-9). `_RESUME` 10-20 줄 하나는 E2E-8 상태로 낡은 채 남았다
- **이미지 태그 · back CrashLoop** — 차트 태그는 Actions 가 민 40자 sha 여야 한다. 배포 직후 back 이 CrashLoop — APNs Secret 을 `/run/secrets` 에 마운트해 SA 토큰 마운트가 막힘 → infra #23(§2)
- **Secret 생성 스크립트 실패** — 결과적으로 코디가 클러스터에서 `cc-prototype-secret`(22키) · `cc-prototype-apns` 를 만들었다(값은 레포 0 · `_RESUME` 10-21). 실패 원인 · 메시지는 work/ 에 기록이 없다 — 다음엔 실패 출력을 남긴다
- **Cloudflare 가 Python 기본 UA 를 403** — 배포 확인 때 Python 기본 UA 요청은 403 · Dart UA(앱)는 200(`_RESUME` 10-21 배포 완료 줄). 서버 문제로 오인하지 말 것
- **데모 환자가 국내 칸에만** — `reserveByTimeSlot` 이 그룹을 못 정해 38건 전부 국내 → `reserveV2` 로 재배치(§2)
- **SPEC 이 코드보다 늦었다** — E2E 수정을 「바로 발주」로 돌리면서 SPEC 반영을 미뤄, 마감 전 동기화에서 한 번에 맞췄다(SPEC-003 부록 C · D · SPEC-004 부록 B). 코드와 달랐던 곳: 죽은 토큰 400 삭제 · 웹 로그인 역할 미제한 · 웹 `etc` 줄

## 4. 결정

| 날짜 | 결정 | 왜 |
|---|---|---|
| 2026-10-20 | 명동 PoC v2 = 시술 현황판 · KOS **데모 지점** 실연동(운영 키 금지) | 10-16 인터뷰 · 사용자 |
| 2026-10-20 | 마취 = 고객 단위 · 여러 회차 · ccc DB · 「마취용」 계정 제외 | 인터뷰 · 사용자 |
| 2026-10-20 | ~~콜 승인 = 시술 진행~~ → **첫 시술 [시작] = 시술 진행**(같은 날) | 사용자 |
| 2026-10-20 | ~~원장 쪽 = `/staff` 「들어온 콜」 칸~~ → 의국 화면(10-21) | 사용자 |
| 2026-10-20 | ~~원장 모바일 앱 → 나중~~ → 앱 만든다(10-21 · 디자인 2단계) | 사용자 |
| 2026-10-20 | 화면 = 고객 중심 · 오더지 카드 나열 · [입실순 \| 배치순] · KOS 시스템 계정 1개 | 사용자 · 부팀장 인터뷰 |
| 2026-10-20 | ~~v1 시드 주석 처리~~ → 새 폴더 `procedure/` · 테마만 복사(10-21) | 사용자 |
| 2026-10-21 | 시안 확정 = 사용자 수정본 r3 · r4(카드 아래 큰 버튼 하나) | 사용자 |
| 2026-10-21 | 카드 = 방 있는 시술 대기 고객 · 수납 전이어도 「수납 필요」 · ~~방 배정 작업 안 보임~~ → 읽기 전용으로 보임(E2E-4) | 사용자 |
| 2026-10-21 | 마취 = 시술 진행과 별개 · 확인 필요 20분 · 호출 미수락 5분 | 사용자 |
| 2026-10-21 | 호출은 쌓기만 · 유효 호출 = 가장 최근 · 수락 = 그 호출의 미수락만 · 새 호출이면 [시작] 꺼짐 · 진행/완료 시술 원장 못 바꿈 | 사용자 |
| 2026-10-21 | [되돌리기] 뺌 · 되돌리기 정책 나중 · ~~실수는 KOS 화면에서~~ → 현장은 KOS 직접 조작 안 함 | 사용자 |
| 2026-10-21 | ~~[시작] · [종료] = 태블릿만~~ → 지금은 현황판에서(원칙은 시술실) · [종료]는 시작한 시술만 | 사용자 |
| 2026-10-21 | [귀가 대기] = 방 빼기 · ccc 는 시술 완료로 방 안 비움 · 남은 작업 취소 → PROCEDURE_DONE · ~~귀가 대기 카드 없앰(E2E-8)~~ → 흐리게 남고 COMPLETED 때 사라짐(E2E-9) | 사용자 |
| 2026-10-21 | 10초 조회 · KOS 기준 / ccc 기준 · 4층 · 직원/방 1시간 · 09:00 ~ 21:00 · 내부 `get-schedules-grouped-by-zone` | 사용자 |
| 2026-10-21 | ccc DB 가 KOS 를 품는 구조(ccc id + kos_id · 이벤트 로그) · 장기 KOS 점진 교체 | 사용자 |
| 2026-10-21 | KOS 「진행중」 = 수락 그대로(E2E-2 · 수정 없음) | 사용자 「KOS 안 본다면」 |
| 2026-10-21 | 화면 갱신 = SSE · 검증 = 단계별 · 통합은 마지막 | 사용자 |
| 2026-10-21 | 디자인 2단계 = Flutter 앱 · 로직 정본 = 코드 · 계정 어드민 · 의사 · 간호사 · 권한 = back 검사 · 통역 = 이전 PoC 복사 | 사용자(U1 ~ U5) |
| 2026-10-21 | ~~원장 호출 휴대폰 알림 = 다음~~ → APNs 푸시 · 관리자도 받음 · 알림에서 바로 [수락] · `push_log` | 사용자 |
| 2026-10-21 | ~~ccc 로그인 = 관리자 1개 · 카드 눌러 바로~~ → **정상 로그인**(아이디 + 비밀번호 · 목록 API 제거 · 5회/1분) | 사용자 「웹 앱 다」 |
| 2026-10-21 | ~~앱 E2E 뒤 최종 배포 · 기기 back = 맥 IP~~ → **배포 먼저** · 앱 = 배포 주소 TestFlight | 사용자 「지금은 배포 먼저」 |
| 2026-10-21 | 배포 = 기존 주소를 시술현황으로 교체 · `cc/` → `_archive/cc` | 사용자 |
| 2026-10-22 | 데모 환자 = 국적별 예약 칸 · 슬롯당 2명(데모 테넌트만) | 사용자 |

전체 줄(100줄)과 SPEC 절 대응은 SPEC-003 부록 D.

## 5. 날짜별 로그

- `2026-10-20` slug 생성 · KOS 데모 연구(공개 72 전수 · `kos-demo-api.md`) · `workflow-v1/v2` · HAR 로 내부 API 찾기 · 내부 쓰기 4종 실호출 · 시안 v1 → 반려 · r2
- `2026-10-21` 사용자 시안 r3/r4 확정 · DEC-005 · SPEC-003 · WORK-003 · back WP1 ~ 4 · front WP5 · 리뷰 r1(FAIL 3) → fix · r2 · 사용자 웹 E2E batch 1(E2E-1 ~ 12) · 모바일 시안 읽기 · SPEC-004 · back 계정 · 권한 · 통역 · 푸시 · Flutter 앱 · 앱 E2E(A1 ~ A7) · 코드 #3 · infra #22 · #23 · 배포 · TestFlight 빌드 1 · 2 · 실기기 피드백 T1 ~ T8 · 정상 로그인 · 코드 #4 · infra #24
- `2026-10-22` 데모 환자 190건 · 스킬 · 빌드 3(코드 #5) · SPEC/WORK 머지 전 동기화(0.3.0 · 부록 D) · 시안 「구현 v3」 4개 · 문서 #99 · 마감

## 6. 산출물

- spec PR: `kknaks/kknaks_profile#99`(`50187e0`) — BASE-008 · DEC-005 · SPEC-003 · SPEC-004 0.3.0 · WORK-003 · WORK-004 · `workflow-v2.md` · `kos-demo-api.md`
- code PR: `kknaksss/cc-prototype#3`(`0f4634a` — 시술 현황판 · 시술실 앱 · KOS 데모 연동) · `#4`(`329b543` — 정상 로그인 · 실기기 T1 ~ T8) · `#5`(`eaa9169` — 데모 환자 스킬 · 빌드 3)
- infra PR: `MediSolveAIDev/k8s_infra_mac#22`(`f6edf1d` — procedure 로 교체) · `#23`(`a52f36c` — APNs `/etc/apns` · SA 토큰 끔) · `#24`(`c7e2ed5` — 이미지 329b543 · 비밀번호 env 이름)

- `kknaksss/myeongdong-poc-v2` → `main`
  - `0f4634a` feat(procedure): 명동 PoC v2 — 시술 현황판 · 시술실 앱 · KOS 데모 연동
- `kknaksss/procedure-login-device-fix` → `main`
  - `329b543` feat(procedure): 정상 로그인 · 아이패드 실기기 피드백(T1~T8)
- `kknaksss/procedure-demo-skill` → `main`
  - `eaa9169` feat(procedure): KOS 데모 환자 채우기 스킬 · 앱 빌드 3
- `kknaksss/cc-prototype-apns-mount` → `main`(infra)
  - `a52f36c` fix(cc-prototype): APNs 키 마운트 /etc/apns + SA 토큰 automount 끔
- `kknaksss/cc-prototype-login` → `main`(infra)
  - `c7e2ed5` chore(cc-prototype): procedure 정상 로그인 이미지(329b543)
- 시안(claude design `dda9a931` · 로컬 사본 `design-sync/`): `Ceramique 시술현황판 v2 (구현 v3).dc.html` · `Ceramique 간호사 모바일 (구현 v3).dc.html` · `Ceramique 시술실 태블릿 (구현 v3).dc.html` · `Ceramique 의료진 앱 (구현 v3).dc.html` — 원본 시안은 그대로
- 리포트: `review-wp1-5-report.md` · `review-r2-report.md` · `fix-decisions-r1.md` · `e2e-feedback-batch-1.md` · `e2e-app-feedback-batch-1.md` · `e2e-device-feedback-batch-1.md` · `design-feedback-batch-1.md` · `design-r3-read-report.md` · `design-r4-read-report.md` · `design-mobile-read-report.md` · `design-sync-frontend-report.md` · `design-sync-mobile-report.md` · `wp5-frontend-report.md` · `demo-patients-2026-10-22.md` · `reference/2026-10-12-cc-prototype/kos-demo-api.md`

## 7. 잔여

- **SPEC 열린 것**
  - SPEC-003 OQ-517 — 웹 카드 「방 배정 · 준비중」 줄 빼기(E2E-10 기록만 · 코드는 아직 그림)
  - SPEC-003 OQ-518 — 웹 로그인 역할 제한(결정 「웹 = 관리자」 · 코드는 어느 역할이든 들어감)
  - SPEC-003 OQ-519 — 데모 표식 계정을 원장 목록에서 뺄지(`KOS_EXCLUDE_ACCOUNT_IDS`)
  - SPEC-004 OQ-616 — 실기기 Apple Watch 알림 [수락]
  - SPEC-004 OQ-617 — 통역 실음성 기기 확인(마이크 · 스피커)
  - SPEC-004 OQ-618 — 빌드 3 기기 설치 확인
  - DEC-005 OQ-501 ~ 503 — 지정 호출의 KOS 본문(`doctorIds`?) · 시술권 차감 · 내부 API 가 막히거나 바뀌면
- **시안 정책 후보**(`design-sync-frontend-report.md`)
  - P-1 토스트 위치 — 앱은 위(A3 「웹/앱 같은 규칙」) · 웹 코드는 아직 아래
  - P-2 「방 배정」 줄 — 코드에 보임(OQ-517 과 같음)
  - P-3 「귀가」 칩 — 앱엔 있음(T5) · 웹 현황 6칸엔 없음
  - P-4 `canCall` — 진행 중 시술만 남은 카드는 바닥 버튼이 없음(원본 r4 Q4 는 꺼진 버튼이 보임)
  - P-5 국적 칩 — KOS 코드(TW · CN …) 그대로 · 원본 시안은 한글 이름 · 대응표 없음
- **KOS API 없음** — 공개 API 에 재내원 예약(새 내원객은 늘 첫내원) · 접수 · 수납(시술 작업 생성) · 방 배정이 없다 → 데모 카드는 KOS 화면에서 준비. KOS 에 요청할 목록
- **옛 `cc-db` PVC · scenario/staff Secret** — infra #22 에서 keep · 지울지 미정
- **접근 제한 비밀번호가 약하다** — 사용자 선택으로 그대로(공개 주소 · 데모 데이터). 운영 전에 다시
- SPEC-004 범위 코드 리뷰(WORK-004 WP6)는 하지 않았다 · `.env.example` 에 `PROC_SESSION_HOURS` · `PROC_BCRYPT_ROUNDS` 없음
