
# [backend] WORK-011 Phase BE-3 — 메시지함 · 답장 · 프로필 · 카톡 수신 API

너는 **strong-hajin `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/roles/strong-hajin/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-inbox`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**같은 코드 워크트리를 다른 워커(frontend · 셸)가 뒤 Phase 에서 쓴다. 이번 Phase 는 **BE-2 워커와 동시**다 — 너는 API 쪽만.** 커밋하지 마라.

## 1. SSOT — 먼저 읽을 것 (너는 맥락이 없다 — 이게 전부다)

- **SPEC-008** `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/20-spec/spec-008-external-channels.md` (v0.5.1) ← 계약의 SoT
- **WORK-011** `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/30-work/work-011-external-channels.md` — 너의 범위는 아래 §6 의 Phase 절만
- **BE-1 결과** — 이 워크트리의 커밋 `78f014f`(스키마 9표 · `modules/external_channels`(domain·events·application, `sync.py`/`inbox.py`/`kakao_ingest.py` 자리) · platform 어댑터(저장소·Fernet·OAuth·pg_notify) · NOTIFY `ax_user_events`(UserEvent v1) · `ax_external_sync`(깨움)). **BE-1 이 만든 경계를 지켜라**
- 4차 검수 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/review-spec-work-r4.md` · 대응 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/review-spec-work-fix4.md`
- 결정 원장 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/_RESUME.md` §2 (왜 그런지 궁금할 때만) · 코드 레포 `AGENTS.md`

**같은 워크트리에서 다른 backend 워커가 동시에 일한다** — 파일 경계(§5)를 넘지 마라. 공용 파일(`settings.py`·`Makefile`·inventory json·`http.py` 라우터 등록)을 고쳐야 하면 **한 줄 추가만**, 그리고 보고에 적어라. 커밋·push 금지.

**기대는 개념** — 해당 없음.

## 2~4. 배경 · 계약 · 핵심 파일

WORK-011 「Phase BE-3」 절과 SPEC-008 §4.3(메시지함) · §4.4(답장) · §4.6(카톡 수신 — 기기 토큰 Bearer) · 프로필/비밀번호 절 · HTML 메일 소독·샌드박스(F-3) · 이미지 프록시 SSRF 규칙 · 새 메시지함 WS(`ax_user_events` LISTEN) 가 전부다. 요청/응답/오류 모양은 SPEC 그대로.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `backend/src/ax_workspace/modules/external_channels/inbox.py` · `kakao_ingest.py` 및 그 하위 새 모듈 · 프로필/비밀번호 모듈 · 해당 HTTP 라우트(새 파일) · WS 엔드포인트(새 파일) · 관련 `backend/tests/**`
- 공용 파일은 한 줄 추가만: `entrypoints/http.py`(라우터 등록) · `bootstrap/settings.py`(hostPath 경로 env) · inventory json · `pyproject.toml`/`uv.lock`(HTML 소독 라이브러리 등)
- **금지**: `sync.py` · 연동 워커 · 슬랙/Gmail 수집 어댑터(BE-2 몫) — 단 **답장 보내기**는 BE-3 이 슬랙 `chat.postMessage`/`files` · Gmail `messages.send` 를 직접 부른다(어댑터 새 파일로, BE-2 수집 어댑터와 파일 분리)

## 6. 구현 단계

1. WORK-011 「Phase BE-3」 항목 전부: 메시지함 목록(출처 필터 · 미읽음 · 페이지네이션 · 카드 = 메일 한 통 / 방 하나) · 본문(메일 HTML **서버 소독** + 샌드박스 전제 · 슬랙/카톡 대화 · 스레드) · 읽음/모두 읽음 · **새 메시지함 WS**(`ax_user_events` LISTEN → 그 사용자에게만) · 첨부 받기(메일·슬랙 = 그 사용자 토큰으로 **중계, 저장 안 함** / 카톡 = hostPath 저장본) · 이미지 프록시(SSRF 규칙) · **답장**(슬랙 채널/스레드 · 내 이름 · 파일 50MB · 메일 답장/전체 답장 · 스레드 이어짐 · 첨부 합계 25MB · 보낸 기록) · **카톡 수신**(기기 토큰 Bearer · handshake · 메시지 묶음 업로드 · 첨부 업로드 → hostPath(`AX_` 경로 env) · 상태/생존 신호 · **서버 고른 방 기준 403** · 중복 키 (연동, chatId, logId)) · **프로필**(이미지 업로드 즉시 저장 → hostPath · 조회 GET · 삭제 · 비밀번호 변경 API 신설 + **변경 시 기기 토큰 철회**) · 이름·직무는 명부 읽기 전용 · **★2** reset-account 는 웹 세션
2. **실물 1회(로컬)**: 카톡 업로드는 **가짜 수집기 요청**(기기 토큰 발급 → handshake → 묶음·첨부 업로드 → 메시지함 조회에 보임 · 고르지 않은 방 403) · 메일 HTML 소독(스크립트·이벤트 속성 제거) · WS 로 새 메시지 알림 수신 · 프로필 이미지 업로드/조회 · 비밀번호 변경 후 기기 토큰 무효. 슬랙·Gmail 답장 실물은 BE-2 연동이 생긴 뒤 **코디 실물 확인 필요**로 남겨라
3. 비밀값 로그 금지 · 사용자 포트·프로세스 금지

## 7. 범위 제약

- 연동 수집 워커(BE-2) · 프론트 · 셸 · 인프라 차트 금지

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
  --to term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b --from term_4e60d06d-45f3-4a0a-bb72-169d2b5a91d6 \
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
