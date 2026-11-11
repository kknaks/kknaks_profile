# [planner] fix 스펙 개정 1판 — 실기기 피드백 6건 + 배포 문서 반영

너는 **day `planner` 워커**다. **너는 앞 판의 맥락이 없다** — 아래 「읽을 것」으로 시작한다.

- 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/roles/day/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
- **이번 판의 원천(사용자 말 · 확정 · 그림)**: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/e2e-feedback.md` — 「버그 기록」 표 1 ~ 7. 그림 `e2e-shots/`
- 결정 정본: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/_RESUME.md` §2
- 앞 판 결정(읽기): `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/_archive/day/day-app/_RESUME.md` §2 · `_archive/day/day-procedure-board-2/_RESUME.md` §2
- 코드(읽기 전용 · 지금 구현이 어떤지 확인용): `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix` (`app/lib/ui/board_screen.dart` · `room_screen.dart` · `app/lib/chat/` · `app/lib/notify/` · `backend/day/services/chat.py` · `chat_push.py` · `push.py` · `notifications.py` · `backend/day/routers/api/chat.py`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/fix-spec` (base `origin/main` → PR `main`). 범위는 `products/day/` 뿐.

## 1. 무엇을 하나

사용자가 TestFlight 실기기(DAY Dev 0.1.0 빌드 1 · dev 서버)에서 본 것 중 **사용자가 확정한 6건**을 스펙에 반영하고, 오늘 정해진 배포 결정을 배포 문서에 적는다. **통역(피드백 5번)은 이번 판에서 다루지 않는다**(조사 워커가 따로 본다 — 손대지 마라).

코드는 고치지 않는다. 이 스펙이 다음 WP · 코드 발주의 계약이 된다.

## 2. 반영할 것 — 사용자 확정(바꾸지 마라)

### 가. 시술현황 목록 카드 (DAY-SPEC-003 U-3 · 관련 A- 항목 · OQ)

1. **모두 완료 상태를 카드에 추가**(피드백 1 · 4). 지금 U-3 「현재 상황 상자」는 4상태만 정의해서, 시술이 모두 완료된 카드가 「시술 대기」로 그려진다.
   - 카드의 시술 줄이 전부 완료면 상태 칸 = 「시술 모두 완료」 / 「마지막 종료 {HH:MM}」 — **방 상세(U-4 5번)와 같은 글자 · 같은 계산**(표시 계산 · 새 상태값 아님 · 서버 변경 없음).
   - 카드 아래에 **[귀가 대기]** 버튼 — 「수락처럼」(사용자): 카드의 수락 버튼과 같은 자리 · 같은 방식. 노출 조건 = 방 상세와 같게 서버 `canHome` + 판 편집 권한. 누른 뒤 동작 · 토스트 · 오류는 방 상세의 [귀가 대기](U-9)와 같다.
   - 호출 상태 · 수락 줄과 겹치는 경우가 실제로 생길 수 있는지 서버 규칙(SPEC-002)으로 따져, 생기면 어느 것을 보일지 기존 기본값(OQ-A21) 방식으로 적는다.
2. **확인 필요 표시 방법 변경**(피드백 2 · 사용자 「B안」). 카드 전체 빨간 테두리를 **없애고**, 카드 안 현재 상황 상자에 **옅은 빨강 배경 + 왼쪽 얇은 빨간 띠**. 붙는 조건(서버 `needs[]` 가 하나라도)은 그대로 — 표시만 바꾼다. 웹은 대상 아님.
   - 상자가 이미 자기 색을 갖는 상태(마취 중 보라 · 20분 초과 빨강 · 시술 중 주색 · 호출 상태 · 위 「모두 완료」)와 겹치는 자리를 **전부 세어 표로** 만든다. 사용자가 정한 것은 「칸에 옅은 빨강 + 왼쪽 띠」뿐이다 — 겹칠 때의 색은 네가 기본값을 제안하고 「정할 것」에 올린다(확정처럼 쓰지 마라).

### 나. 채팅 (DAY-SPEC-004)

3. **채팅 거절 표시**(피드백 3). 채팅 요청이 403 `forbidden` 이면 「서버에 연결 중...」 · 로딩을 계속 보이지 않고, 채팅 탭 본문 자리에 DAY-SPEC-001 `forbidden` 글자(시술현황 권한 없음 화면과 같은 문구)를 보인다. 다시 시도 · 로그아웃 버튼을 둘지는 시술현황 쪽 기존 처리와 같게 — 새 글자를 짓지 않는다.
4. **그룹 이름 바꾸기**(피드백 6). 「하지 않는 것」에서 뺀다.
   - 그룹 이름 = 방 전체 공통(개인별 아님) · **지금 참여자 누구나** 방 정보에서 바꾼다 · 그룹만(1:1 없음).
   - 대화에 「이름 바꿈」 시스템 줄은 **남기지 않는다**.
   - 서버 API(경로 · 요청 · 응답 · 오류) · 길이 · 빈 값 규칙(만들 때 `title` 규칙과 같게) · 다른 참여자 화면이 실시간으로 바뀌는 방법(기존 채팅 SSE 이벤트를 쓸 수 있는지 먼저) · 푸시 제목에 미치는 영향을 정한다.
   - 화면: 방 정보의 「그룹 이름」에서 바꾼다. **화면 글자는 이미 있는 것만**(「그룹 이름」 · 「비우면 참여자 이름으로 보여요」 등 새 대화 화면 글자). 저장 · 취소처럼 새 글자가 필요하면 짓지 말고 「정할 것」에 후보와 함께 올린다.

### 다. 알림 (DAY-SPEC-005 · DAY-SPEC-004 푸시 · DAY-SPEC-000 `notification_setting`)

5. **채팅 전체 알림 스위치**(피드백 7). 설정 탭 「알림」 칸에 「원장 호출」 옆으로 **「채팅」** 스위치 하나.
   - 채팅만(원장 호출은 지금처럼 따로).
   - 끄면 그 계정은 **모든 방**의 채팅 푸시 · 앱 안 배너를 받지 않는다. 방별 알림 설정 값은 그대로 보존 — 다시 켜면 방별 설정대로.
   - 받는 종류 조건(누구에게 이 스위치가 보이나)은 채팅을 쓸 수 있는 계정(SPEC-004 「활성 직원」) 기준으로 적는다. `notification_setting` 은 이미 「계정 × 종류」다 — 새 종류 이름 · 기본값(저장 없으면 켜짐)을 기존 규칙에 맞춘다. migration 이 필요한지 판단해 적는다.

### 라. 앱 후속 2건 (DAY-SPEC-003 — 앞 판이 미룬 것)

6. 스냅샷 `version` **같은 값도 받는다** — 판이 바뀔 때만 오르므로 앱은 「미만」만 버린다(`app/lib/data/board_stream.dart`). [재호출] 노출 = 서버 `calls[].canRecall`. 스펙에 이미 이렇게 적혀 있으면 그대로 두고 「이미 있음」으로 보고, 다르면 고친다.

### 마. 배포 문서 (`40-architecture/mobile-deployment.md` · 필요하면 `deployment.md`)

7. 오늘 정해진 것(`_RESUME.md` §2 · `orchestration/config/projects/day.json` 의 `apple`):
   - 최종 배포 = 비공개 · 병원 직원에게만 · 방식 **등록되지 않은 앱(Unlisted)** → §2 · §6 의 해당 [미결]을 닫는다. 설치 기기가 개인 폰인지는 사용자가 말하지 않았다 — 지어 넣지 않는다.
   - 개발 / 정식 **두 앱**: `day.medisolveai.dev`(DAY Dev → dev) · `day.medisolveai`(DAY → prod). 「정식 앱 하나로 심사 · 데모 계정 → dev」([확정])와 어떻게 같이 서는지 정리한다 — 개발 앱은 TestFlight 확인용이고 dev 주소 하나만 허용해 빌드했다. 둘이 충돌하면 「정할 것」에 올린다(임의로 한쪽을 지우지 마라).
   - 지금 상태: Bundle ID 둘 등록 · 앱 record 는 DAY Dev 만 · TestFlight 0.1.0 (1) · 수출 규정 키 · 앱 아이콘.
   - M-16(Team ID 를 저장소에 넣지 않는다)의 범위 = 앱 서명 값. 서버 `dev.env` 의 APNs Key ID · Team ID 는 저장소 허용(사용자 2026-11-11).
   - dev 서버: `DAY_PUBLIC_API_BASE` 설정됨 · APNs 선택 비밀 넣음 · 채팅 첨부 Blob 은 아직 없음.
   - **값(Key ID · Team ID · IP · Vault 이름 · 리소스 ID)은 문서에 적지 않는다.**

## 3. 규칙

- **근거 없는 정책 0.** 사용자가 말하지 않은 것은 「정할 것」(OQ)으로 — 열린 것을 추측으로 메우지 않는다.
- **화면 문구를 지어 넣지 않는다.** 이미 스펙 · 화면에 있는 글자만 쓴다.
- 기존 확정을 건드릴 때는 무엇을 대체하는지 개정 머리말에 적는다(이 레포 스펙의 「YYYY-MM-DD 개정 ○」 방식 그대로). 버전 · 상태 · `log.md` 는 레포 규칙대로.
- 스펙마다 영향받는 절 · 케이스 표 · A- 수용 항목 · OQ · 「프로토와 다른 곳」을 **전부 찾아** 같이 고친다(한 절만 고치고 다른 절이 옛 말을 하게 두지 마라). 찾은 자리를 보고에 센다.
- `20-spec.md` · `30-work.md` 같은 목차가 스펙 버전을 적고 있으면 맞춘다. WORK 문서는 이번에 쓰지 않는다.
- allowed_paths: `products/day/` 만. 커밋 · push · PR 금지.

## 4. 검증

```
python3 scripts/lint-pipeline.py --strict     # products/day/ 범위 ERROR 0 (타 제품 기존 WARN/ERROR 는 「무관」으로 분리)
```

## 5. 보고

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/spec-1-report.md`

- 바꾼 문서 · 절 목록(문서:줄) · 버전 변화
- 피드백 번호 ↔ 반영 자리 표
- **정할 것**(사용자에게 물을 것만 · 후보와 추천 · 한 줄씩)
- 코드 영향(서버 · 앱 · migration 유무) — 다음 WP 가 쓸 수 있게
- lint 결과

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
