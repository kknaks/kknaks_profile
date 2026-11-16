# [researcher] 웹 피드백 W1~W9 — 바꿀 표면 전수조사 · 앱 영향 판정 (read-only)

너는 **day `researcher` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web/orchestration/roles/day/researcher/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web` (코디 워크트리)
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

⚠ 코디 워크트리다 — 리포트 파일 1개 외 수정 · 생성 금지.

## 1. SSOT — 먼저 읽을 것

- 사용자 피드백: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web/orchestration/work/fix-web/e2e-feedback.md` — **W1~W9 표 + 「보충(사용자)」 전부**. 보충이 표보다 나중 말이다(W4 카드 구조 · W5 확인 필요 4가지 · 아코디언 전부 제거).
- 코드(읽기만): `/Users/kknaks/git/CENTURION_DAY` — dev `c5045a99`(#248). **사용자 체크아웃 · pull/checkout 금지 · 파일 읽기만.** 레포 루트 `AGENTS.md` 먼저.
  - 웹: `backend/day/templates/partials/board_regions.html`(inbox_tabs · inbox_now · inbox_calls) · `board_parts.html`(need_card · call_card · inbox_card · 방 카드 · 수락 버튼) · `backend/day/static/` JS(카드 선택 포커스) · `backend/day/styles/app.css`
  - 백엔드: `backend/day/services/board_rules.py`(`needs()` :380 · `inbox_section()` :492 · 스냅샷 조립) · 스냅샷 API 라우터 · 알림/푸시
  - 앱: `app/` (Flutter)
- 스펙(읽기만): mediness `origin/main` — `git -C /Users/kknaks/git/harness_works/mediness-mediness show origin/main:<path>` 로 읽는다(canonical 은 더티 체크아웃 · checkout/pull 금지). `products/day/20-spec/spec-002-procedure-board.md` · `spec-000-data-model.md` · `products/day/20-spec.md` · `products/day/00-baseline/planning/` 의 시술 현황 · 설정 · 개요 기획안(「확인할 상황」 · 「확인 필요 기준 분」 · 알림 표)

기대는 개념: 해당 없음.

## 2. 배경

사용자 2026-11-12 /board 웹 피드백 9건(W1~W9). 요지:
- 왼쪽 받은함 탭 = 「확인 필요 n」 · 「수락 대기 n」(· 「시술 완료」는 그대로로 보임 — 확인). 탭 아래 아코디언 전부 제거 → 시작 가능 · 시술 대기 · 수락함 목록 없어짐.
- 확인 필요 상황 = **대기 길 때(wait) · 마취 초과(anes) · 호출 안 옴(call) · 귀가 대기 필요(home) 4가지** → 지금 5가지에서 **수락 뒤 미시작(accept) 하나 뺌**.
- 카드 = 머리 「룸 이름 · 상태 · 경과」 / 「이름」 / 버튼 한 칸 아래.
- **사이드바 확인 필요 카드의 [귀가 대기] 버튼 제거(W10)** — 상황 카드는 남고 버튼만 없음. 사이드바 카드 버튼은 [재호출] 하나.
- 방 카드 [수락] 버튼 제거 · 오더 메모 글자 2pt ↑ · 탭 변경/카드 밖 클릭 시 포커스 해제.

수정 발주 전에 **바꿀 곳을 전부 세고, 백엔드를 바꾸면 앱에 번지는지** 판정한다. **결정하지 않는다** — 후보와 「정할 것」만.

## 3. 계약

해당 없음.

## 4. 먼저 읽을 핵심 파일

위 §1.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `(read-only — 브리프가 지정한 리포트 파일 1개만 생성)`

## 6. 구현 단계 (질문)

**표면 전수조사 — 목록을 받지 말고 grep 으로 전부 센다** (백엔드 · 템플릿 · JS · CSS · 테스트 · 앱 · 알림/푸시 · 스냅샷 API · 설정 화면 · 시드 스크립트)
1. 확인 필요 `accept`(수락 뒤 미시작): 만드는 곳 · 쓰는 곳 전부(`why` 값 · `accept_min` 기준 분 설정 · 알림 문구 · 카드 문구 · 정렬 · urgency · 테스트).
2. `inbox_section` 의 `startable` · `waiting` 과 스냅샷의 해당 칸: 쓰는 곳 전부.
3. 수락함(`acceptedBy` 있는 call) 목록: 웹 외에 쓰는 곳.
4. 방 카드(시술 줄) [수락] 버튼 · **사이드바 need_card [귀가 대기] 버튼(W10)**: 템플릿 · 라우터 · 권한 · 테스트. 사이드바 [수락]과 같은 엔드포인트인지.
5. 받은함 탭 이름 · 개수(「현황」 · 「호출 n」 · 「시술 완료 n」): 정의 위치 · 테스트 단언.
6. 카드 구조(W4): need_card · call_card 의 지금 줄 구성과, 바뀐 구조(머리=룸·상태·경과 / 이름 / 버튼 한 칸 아래)로 갈 때 손댈 매크로 · CSS · 테스트. 상태 문구(「대기 n분째」 등) 정의 위치.
7. W1 오더 메모 글자 크기 정의(CSS 토큰/클래스 · 다른 화면과 공유하는지). W9 카드 선택 포커스를 잡고 푸는 JS 위치 · 지금 풀리는 조건.
8. 「귀가 대기 전」(home)이 확인 필요 **개수**에 실제로 세지는지 — 탭 개수 계산식과 need 목록이 같은 원천인지(사용자: 「귀가 대기가 확인 필요에 계산 안 된다」).

**앱 영향 (사용자 요청 — 핵심)**
9. 앱(`app/`)이 쓰는 백엔드 값: 스냅샷/API 응답의 `needs[]` · `why` · `inbox` 구간(startable · waiting) · calls 수락함 · 탭 개수 · 알림/푸시 payload. 파일:줄로.
10. 각 변경(W5 accept 빼기 · W6/W7 목록 제거 · W8 수락 버튼)을 **「웹만」 / 「API 같이」 / 「앱 수정 필요」**로 판정. 앱이 쓰는 값이면 API 는 두고 웹에서만 감추는 선택지가 되는지도.
11. 이미 배포된 앱(TestFlight DAY Dev · 심사 중 정식 0.1.0 (2))이 옛 API 값을 기대하는 곳 — API 를 바꾸면 깔린 앱이 깨지는지.

**스펙 위치**
12. 위 변경마다 스펙/기획안의 정의 위치(파일 · 절 · 줄): 규칙 16 · U-10 「확인할 상황」 · 「확인 필요 기준 분」(설정) · 알림 표 · 받은함 탭 · 아코디언 · 카드 와이어 · 방 카드 [수락]. 스펙과 지금 코드가 이미 어긋난 곳이 있으면 따로.

## 7. 범위 제약 — 하지 말 것

- 파일 수정(리포트 외) · 커밋 금지. `/Users/kknaks/git/CENTURION_DAY` · mediness canonical 에서 checkout · pull · 빌드 금지(읽기 · `git show`/`git grep` 만).
- 사용자 포트 · 프로세스(로컬 11040 · `day-local` 컨테이너) 금지. dev/prod 서버 접속 불필요.
- 고객 값 · 키 · 토큰 · 계정 이메일 출력 금지.

## 8. 검증

```
질문마다 답 + 근거(파일:줄 · git ref · 문서 URL). 확인 못 한 것은 「확인 안 됨」. 결정하지 않고 「정할 것」으로 모은다
```

- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web/orchestration/work/fix-web/research-1-report.md` — 질문 1 ~ 12 각각 답 + 근거(파일:줄 · git ref) · 「확인 안 됨」 · 변경별 판정 표(웹만 / API 같이 / 앱 수정 필요) · 고칠 방향 후보 · 정할 것.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_b1db5638-c143-4f48-b35e-4550ff2d45d4 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_b1db5638-c143-4f48-b35e-4550ff2d45d4 \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_b1db5638-c143-4f48-b35e-4550ff2d45d4 --text "[질문] researcher: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
