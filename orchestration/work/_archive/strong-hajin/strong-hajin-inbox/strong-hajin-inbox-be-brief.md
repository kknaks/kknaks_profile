
# [backend] WORK-011 Phase BE-1 — 외부 채널 연동 기반 (스키마·저장·소유·기기 토큰·env·연결 라우트)

너는 **strong-hajin `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/roles/strong-hajin/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-inbox`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**같은 코드 워크트리를 다른 워커(frontend · 셸)가 뒤 Phase 에서 쓴다. 이번 Phase 는 너 혼자 — `backend/` · `Makefile` · `docker-compose.yml` 만.** 커밋하지 마라.

## 1. SSOT — 먼저 읽을 것 (너는 맥락이 없다 — 이게 전부다)

- **`/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/20-spec/spec-008-external-channels.md`** (v0.5.0) ← 계약의 SoT. 여기 없는 건 발명하지 마라
- **`/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/30-work/work-011-external-channels.md`** — 너의 범위는 **「Phase BE-1」 절**. 다른 Phase 는 손대지 마라
- **`/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/review-spec-work-r4.md`** — 4차 검수. 그중 **BE-1 에 걸린 것**은 이번에 같이 넣는다(아래 §6-2). SPEC/WORK 문서보다 이 리포트가 최신인 항목은 리포트 + 아래 §6 이 우선
- 관련 SPEC: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/20-spec/spec-009-mac-kakao-collector.md` v0.5.0(§4 업로드·기기 토큰 소비 쪽) · `spec-006-tauri-wrapper.md` v0.6.0
- 결정 원장 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/_RESUME.md` §2 (왜 그런지가 궁금할 때만)
- 코드 레포 `AGENTS.md` · 기존 규약(모듈 배치 `backend/src/ax_workspace/modules/*` · `bootstrap/settings.py` env · `schema_sync`/reset_demo 경로)

**기대는 개념** — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

메일(Gmail API)·슬랙(사용자 토큰)·카톡(Mac 수집기)이 사람마다 메시지함에 쌓이는 기능의 **서버 기반**을 세운다. 뒤 Phase(BE-2 연동 워커 · BE-3 메시지함/답장/프로필/카톡 수신 API · FE · 셸)가 이 위에 나란히 올라간다 — 그래서 **BE-2 ∥ BE-3 이 파일 충돌 없이 가능하도록 모듈 경계를 이번에 갈라 둔다.**

## 3. 계약

SPEC-008 의 데이터·소유·기기 토큰·연결 라우트·env 계약 그대로. BE-1 이 고정한 스키마·모듈 경계·NOTIFY 채널 이름은 뒤 Phase 가 소비한다 — **끝날 때 그 목록을 보고에 적어라.**

## 4. 먼저 읽을 핵심 파일

SPEC-008 의 「코드 관계표」·§5 Implementation Rules 가 든 파일:줄. 특히 인증/세션(`entrypoints/http_auth.py`·`auth_sessions.py`) · `credentials.py` · `persistence.py` · `bootstrap/settings.py` · `Makefile:2-9`(soniox·theconnect env 로드 방식) · operation inventory 시험(`test_operation_inventory`).

## 5. allowed_paths — 이 밖은 건드리지 마라

- `backend/`
- `docker-compose.yml`
- `Makefile`

## 6. 구현 단계

1. WORK-011 「Phase BE-1」 의 항목 전부(스키마 — 연동·고른 방·메시지·첨부 메타·읽음·보낸 답장·기기 토큰 · 소프트 딜리트 · 사람마다 복제 · 카톡 중복 키 (연동, chatId, logId) · 토큰 암호화 `AX_` 대칭키 · 소유 검사 · 연결 라우트(Gmail·슬랙 OAuth, `state` 일회용 · 콜백은 state 로 회원 · 목적지 `AX_WEB_ORIGIN`) · 기기 토큰 발급/철회(범위 = 카톡 수집 라우트 + 고른 방 조회만 · 해시 보관 · 비번 변경·새 발급 시 철회) · **Makefile 에 `~/.config/google/env`·`~/.config/slack/env` 로드 추가**(soniox·theconnect 와 같은 방식)
2. 4차 검수가 BE-1 로 넘긴 것 **전부**: 동기화 상태 칸(연동·방별 실시간/백필 진행/끊김) · **새 메시지 NOTIFY 계약**(채널 이름·페이로드 — BE-2 가 내고 BE-3 WS 가 듣는다) · **모듈 분할**(BE-2 와 BE-3 이 같은 파일을 안 건드리게 — 연동 수집 모듈 / 메시지함·답장 모듈 / 카톡 수신 모듈) · HTTP operation inventory json 갱신 · selected_rooms_version 생성 규칙 · 카톡 첫 handshake 에서 연동 생성 · **★1** handshake selected_rooms 에 `external_id`(chatId) 포함 · **★2** reset-account 는 웹 세션 라우트(수집기 범위 밖)로
3. 로컬 비밀값 로드 확인: `make` 로 백엔드를 띄우면 `GOOGLE_OAUTH_CLIENT_ID`·`SLACK_CLIENT_ID` 가 설정에 잡히는지(값 출력 금지 — 「있음/없음」만)
4. **실물 1회**: 로컬에서 Gmail 연결 시작 → 동의 URL 이 `state` 를 담아 나오고, 콜백이 그 state 로 회원을 찾아 토큰을 **암호화 저장**하는 데까지 — 동의 화면 클릭은 사람만 할 수 있으니 **URL 이 나오는 것 · 콜백을 가짜 code 로 불렀을 때 state 검사·오류 경로**까지 시험으로, 실제 동의는 보고에 「코디 실물 확인 필요」로 남겨라

## 7. 범위 제약 — 하지 말 것

- 연동 워커(슬랙 Socket Mode · Gmail watch/pull) · 메시지함/답장/프로필 API · 카톡 업로드 수신 · 프론트 · 셸 — **다음 Phase**. 이번엔 그 자리(모듈·계약)만 만든다
- 비밀값을 코드·시험·로그에 쓰지 마라 · `~/.config/*/env` 를 고치지 마라(읽기만)
- 사용자 포트·실행 중 프로세스를 건드리지 마라(로컬 스택은 `COMPOSE_PROJECT_NAME=strong-hajin-work` 등 별도 이름으로) · 커밋·push 금지

## 8. 검증

```
코드 레포 AGENTS.md 준수: backend 테스트는 Makefile 타겟으로만 실행. 변경 단계에 맞게 make test-unit 또는 make test-contract, 최종 코디 검증은 make verify 및 격리 PostgreSQL의 make test-postgres와 관련 acceptance journey. 단계별 전량 반복 금지. tests/architecture 경계 및 operation inventory drift 확인(diff 항목만 패치). 스키마 변경은 reset_demo 전용 경로, 일반 API startup DDL 금지. 기존 실패는 기준선과 분리 보고.
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b --from term_b638849c-2972-4ae7-abff-a0a37e118c60 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
