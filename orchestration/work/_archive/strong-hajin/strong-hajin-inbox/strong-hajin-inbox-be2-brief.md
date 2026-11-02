
# [backend] WORK-011 Phase BE-2 — 연동 워커 (슬랙 Socket Mode · Gmail watch+pull · 백필 · 메우기)

너는 **strong-hajin `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/roles/strong-hajin/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-inbox`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**같은 코드 워크트리를 다른 워커(frontend · 셸)가 뒤 Phase 에서 쓴다. 이번 Phase 는 **BE-3 워커와 동시**다 — 너는 연동 수집 쪽만.** 커밋하지 마라.

## 1. SSOT — 먼저 읽을 것 (너는 맥락이 없다 — 이게 전부다)

- **SPEC-008** `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/20-spec/spec-008-external-channels.md` (v0.5.1) ← 계약의 SoT
- **WORK-011** `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/30-work/work-011-external-channels.md` — 너의 범위는 아래 §6 의 Phase 절만
- **BE-1 결과** — 이 워크트리의 커밋 `78f014f`(스키마 9표 · `modules/external_channels`(domain·events·application, `sync.py`/`inbox.py`/`kakao_ingest.py` 자리) · platform 어댑터(저장소·Fernet·OAuth·pg_notify) · NOTIFY `ax_user_events`(UserEvent v1) · `ax_external_sync`(깨움)). **BE-1 이 만든 경계를 지켜라**
- 4차 검수 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/review-spec-work-r4.md` · 대응 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/review-spec-work-fix4.md`
- 결정 원장 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/_RESUME.md` §2 (왜 그런지 궁금할 때만) · 코드 레포 `AGENTS.md`

**같은 워크트리에서 다른 backend 워커가 동시에 일한다** — 파일 경계(§5)를 넘지 마라. 공용 파일(`settings.py`·`Makefile`·inventory json·`http.py` 라우터 등록)을 고쳐야 하면 **한 줄 추가만**, 그리고 보고에 적어라. 커밋·push 금지.

**기대는 개념** — 해당 없음.

## 2~4. 배경 · 계약 · 핵심 파일

WORK-011 「Phase BE-2」 절과 SPEC-008 동기화 절(§5 Implementation Rules 의 프로세스 배치 · 실시간 · 백필 · 재시작 메우기 · 사람별 팬아웃)이 전부다. 새 메시지는 BE-1 의 저장소에 쓰고 `ax_user_events` NOTIFY 로 알린다(BE-3 WS 가 듣는다).

## 5. allowed_paths — 이 밖은 건드리지 마라

- `backend/src/ax_workspace/modules/external_channels/sync.py` 및 그 하위로 새로 만드는 수집 모듈 · 연동 워커 엔트리포인트(`entrypoints/` 새 파일) · `platform/` 의 슬랙·Gmail 클라이언트 어댑터(새 파일) · 관련 `backend/tests/**`
- 공용 파일은 한 줄 추가만: `Makefile`(연동 워커 띄우기 · **★3 개발 전용 슬랙 토큰 주입 타겟**) · `docker-compose.yml` · `bootstrap/settings.py` · `pyproject.toml`/`uv.lock`(슬랙·구글 SDK)
- **금지**: `inbox.py` · `kakao_ingest.py` · 메시지함/답장/프로필 라우트(BE-3 몫)

## 6. 구현 단계

1. WORK-011 「Phase BE-2」 항목 전부: 연동 전용 워커(레플리카 1 · 슬랙 Socket Mode 앱 토큰 1개 연결 단일 소유) · 슬랙 이벤트(message.channels/groups/im/mpim · 스레드 · 수정/삭제) → **사람별 팬아웃**(그 방을 고른 사용자마다 각자 저장) · 고른 방 최초 백필(허용 끝까지, 진행률 칸) · Gmail **watch 등록·매일 갱신** + **Pub/Sub pull**(서비스 계정 `GOOGLE_PUBSUB_SA_KEY_FILE`) → history.list 로 받은편지함 새 메일 · 연결 직후 받은편지함 **전체 백필**(진행률) · 재시작 메우기(마지막 시점 이후) · 토큰 만료·권한 회수 → 연동 상태 끊김 · 원문 그대로 저장
2. **★3**: 로컬에서 `~/.slack_test_token`(사용자 토큰)을 「연결된 슬랙 연동」으로 넣는 **개발 전용 make 타겟**(운영 프로필이면 거절)
3. **실물 1회(로컬)**: 슬랙 — 개발 토큰으로 연동을 만들고 방 하나를 골라 백필이 쌓이고, 그 방에 새 메시지를 보내면 수 초 안에 저장 + NOTIFY 가 나오는 것까지(메시지는 사람이 보내야 하면 **코디에게 요청**) · Gmail — 실제 OAuth 연동은 사용자 동의가 필요하니 **코디 실물 확인 필요**로 남기고, 그 전까지는 Pub/Sub pull 연결(구독 `ax-gmail-pull`)이 서비스 계정으로 열리는 것까지 확인
4. 비밀값은 로그·시험에 쓰지 마라 · 사용자 포트·프로세스 금지(로컬 스택은 별도 COMPOSE_PROJECT_NAME)

## 7. 범위 제약

- 메시지함·답장·프로필·카톡 수신 API(BE-3) · 프론트 · 셸 · 인프라 차트 금지

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
