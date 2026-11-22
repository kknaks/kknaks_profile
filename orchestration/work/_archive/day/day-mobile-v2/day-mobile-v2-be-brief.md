
# [backend] P1 — 통역 서버를 통키 `56e43a0` 최신으로 (DAY 직원 앱 0.2.0)

너는 **day `backend` 워커**다. 너는 앞 맥락이 없다 — 이 브리프가 전부다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/roles/day/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-mobile-v2`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

혼자 쓰는 워크트리다(브랜치 `kknaksss/day-mobile-v2` · origin/dev `844eace4`). 이 워크트리에서 P1 → P2 → P3 → F1 을 차례로 하게 된다 — **이번은 P1 만.**

## 1. SSOT — 먼저 읽을 것

- **스펙(정본 · PR 브랜치 — 머지 전이다 · 이 경로의 파일이 정본)**: `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec/products/day/20-spec/spec-003-mobile-app.md` — 개정 ⑲ ⑧ · §3 「통역 — 0.2.0」 절 전부(위 개정 블록 · 표 · 「바뀌지 않는 것」 · OQ-A61 등) · 통역 서버 절(순서 표 · `start` · context · 다시 연결)
- 같은 스펙의 `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec/products/day/20-spec/spec-000-data-model.md`(필요하면) · `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec/products/day/log.md`
- **통키 원천(읽기만)**: `/Users/kknaks/git/toy_pr2/interpret-pwa` — `git -C /Users/kknaks/git/toy_pr2/interpret-pwa show 56e43a0:<path>` 로 읽어라(작업 트리 · 브랜치를 바꾸지 마라). 특히 `back/app/service/interpret/`(session.py · soniox.py · glossary.py · correct.py · turn.py · langs.py) · `back/app/service/records.py`(바로잡기가 기대는 함수 4개만) · `back/seed/glossary.json`(`2026-11-16.11`) · `front/lib/interpret.ts`(클라이언트 프로토콜 사실). DAY 이식 시점 = `17c26b5` → `git log 17c26b5..56e43a0` 5커밋이 이번 차이.
- 통키 결정 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/para/projects/summer-star/interpret-pwa/10-decision/`(D-43 ~ D-71) · `20-spec/spec-001-interpret-pwa.md`
- 조사 · 검수(파일:줄 지도): `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/research-current-state.md` §E · `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/review-doc-1-report.md` F-3 · F-4 · W-9 ~ W-14 · `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/review-doc-2-report.md`
- 레포 규칙: 워크트리 루트 `AGENTS.md` 먼저.

기대는 개념: `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/para/areas/concept/` 에서 `websocket-relay` 를 찾아 읽어라(통역 WS 중계 기준).

## 2. 배경

DAY 통역(`backend/day/services/interpret/` · `adapters/soniox.py` · `policies/interpret/` · `policies/glossary.py` · `seed/glossary.json`)은 2026-11-11 통키 `17c26b5` 를 옮긴 것이다(STT `stt-rt-v5` · 시드 `2026-10-27.6`). **STT v5 는 2026-12-15 종료** — 이번 작업의 마감이다. 사용자 결정: 통역 엔진 정본 = 통키 최신본(`56e43a0`) · DAY 는 그대로 따라간다. 통역 기록(records · D-42)만 DAY 에 없다. 옛 앱(0.1.0) 호환은 챙기지 않는다 — 서버 프로토콜을 새 기준으로 바로 바꾼다.

## 3. 계약

스펙 §3 「통역 — 0.2.0」이 계약이다(mobile 워커 P5 가 이 계약으로 앱을 고친다). 서버 → 앱 메시지 · 앱 → 서버 메시지(`audio_stop` · `playback_stopped` → `audio_end` 응답 · 빈 final caption 지우기 프레임 등) 이름 · 모양을 스펙대로. 스펙과 통키 코드가 다르면 **멈추고 질문**(어느 쪽이 맞는지 정하지 마라).

## 4. 먼저 읽을 핵심 파일

- DAY: `backend/day/services/interpret/__init__.py` · `session.py` · `backend/day/adapters/soniox.py:29-80` · `backend/day/policies/interpret/` · `backend/day/policies/glossary.py:39-92`(로더 허용 칸) · `backend/day/bootstrap/{interpret,glossary}.py` · `backend/day/routers/api/interpret.py` · 기존 테스트(`backend/tests` 에서 interpret · glossary grep)
- 통키: 위 §1

## 5. allowed_paths — 이 밖은 건드리지 마라

- `backend/day/services/interpret/` · `backend/day/adapters/soniox.py` · `backend/day/policies/interpret/` · `backend/day/policies/glossary.py` · `backend/day/bootstrap/interpret.py` · `backend/day/bootstrap/glossary.py` · `backend/day/seed/glossary.json` · `backend/day/routers/api/interpret.py`(필요할 때만) · 통역 · 사전 테스트 파일
- 새 파일이 필요하면 같은 폴더 안(예 `services/interpret/turn.py` · `correct.py`)
- 리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/be-p1-report.md`

## 6. 구현 단계

1. 통키 `17c26b5..56e43a0` 차이와 스펙 §3 「통역 — 0.2.0」을 항목 표로 만든다(항목 · 통키 파일:줄 · DAY 넣을 곳 · 스펙 근거). records(D-42) 계열 · PWA 전용은 「안 가져옴」 표시.
2. 이식: STT `stt-rt-v6` · 끊김 D-67(`max_endpoint_delay_ms` 2000 · `endpoint_sensitivity` -0.3) · 역할 context `text` 키(D-45 · 키 순서 · 다시 연결 때 유지 · `TRIM_ORDER`) · 빈 원문 막기(D-48) · 빈 final caption 지우기 · 언어별 한도(D-56 · v6 × 0.96) · 고유명사 context(D-71) · 세 참여자(D-68 ~ D-70: 차례 끝 서버 시계 1초 · 재생 중 듣기 · TokenGate 재생 언어 토큰 버림 · ECHO_TAIL · 반대 언어 끼어들면 `audio_stop` · `playback_stopped` 받으면 `audio_end` · agent text) · TTS `return_timestamps` · cancel 메시지 · `stop` 때 읽을 큐 비움 · 시술명 바로잡기(D-58 ~ D-66 · `correct.py` + records 함수 4개 · `wrong_key`)
3. 시드 `.11` 을 DAY 로 가져오고 로더 허용 칸(`proper` bool · entry `wrong` · 검사 8 `wrong_form`)을 넓힌다.
4. 테스트: 통키 테스트 중 해당하는 것을 DAY 테스트로 옮기거나 새로 — 최소 차례 거르기 · `audio_stop` · `playback_stopped` → `audio_end` · 시드 로드 · 바로잡기 · context 키 순서.
5. **실물 1회**: 로컬에서 Soniox 에 실제로 붙어 v6 `start` → `ready` 가 오는지(키는 로컬 `/Users/kknaks/git/CENTURION_DAY/deploy/local.env` 의 값을 읽어 쓰되 **출력 · 리포트에 쓰지 마라**). 붙지 못하면 사유와 함께 pending.

## 7. 범위 제약 — 하지 말 것

- 앱(`app/`) · 웹 화면 · 다른 서버 기능(P2 · P3 · F1) 금지. migration 금지.
- 통키 레포 수정 · 체크아웃 금지. 사용자 포트 · 프로세스 · docker 의 `day-local` 컨테이너 건드리지 마라(테스트는 `scripts/test.sh` 의 테스트 스키마).
- 커밋 · push · PR 금지(코디가 한다). 비밀값 출력 금지.

## 8. 검증

```
cd backend && uv run pytest -q <네가 만들거나 고친 테스트 파일만> · uv run ruff check <네가 만진 파일> — 각 1회, 통과하면 반복하지 마라. 테스트 DB 는 로컬 compose — 공유 STG·PROD 금지. 사용자 포트·프로세스를 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending
```
- 로컬 테스트 실행 방법: `DAY_ENV_FILE=/Users/kknaks/git/CENTURION_DAY/deploy/local.env scripts/test.sh`(스키마 day_test) — 레포 문서 확인 후.
- 리포트 `be-p1-report.md`: §6-1 항목 표 · 바꾼 파일 · 테스트 결과(수치) · 실물 1회 결과 · 스펙과 어긋난 곳 · 남은 것.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **완료 보고는 dispatch preamble 의 worker_done 명령을 그대로 따른다**(아래 옛 형식과 다르면 preamble 이 맞다).
- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_5e3720e2-a945-4350-86e9-f3f6bce65ac0 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_5e3720e2-a945-4350-86e9-f3f6bce65ac0 \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_5e3720e2-a945-4350-86e9-f3f6bce65ac0 --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
