# [backend] procedure/back — WP1 ~ WP4 (뼈대 · DB · 규칙 · KOS 조회 · KOS 반영)

너는 **cc-prototype `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/orchestration/roles/cc-prototype/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/cc-prototype/myeongdong-poc-v2` (브랜치 `kknaksss/myeongdong-poc-v2`)
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

⚠ **frontend 워커가 WP1 뒤 같은 워크트리 `procedure/front/` 에서 병렬 작업한다 — `procedure/front/` 는 건드리지 마라.** `cc/` 도 건드리지 마라(WP7 에서 아카이브).

## 1. SSOT — 먼저 읽을 것

- **계약**: `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/para/projects/summer-star/cc-prototype/20-spec/spec-003-procedure-board.md` ← **여기 없는 건 발명하지 마라.** 바꿔야 하면 코디에게 [질문]
- **작업 순서 · 완료 조건**: `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/para/projects/summer-star/cc-prototype/30-work/work-003-procedure-board.md` WP1 ~ WP4
- 결정: `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/para/projects/summer-star/cc-prototype/10-decision/decision-005-procedure-board.md`
- KOS: `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/reference/2026-10-12-cc-prototype/kos-demo-api.md` · 키 · 사용법 메인 = `/Users/kknaks/git/ax-clinic-project/para/resources/technology/2026-09-18-kos-developers-api-guide.md` · 호출 예 `/Users/kknaks/git/ax-clinic-project/scripts/kos_collect.py`
- KOS 인증값(읽기만 · 값을 코드 · 시험 · 로그 · 보고에 넣지 마라): `/Users/kknaks/git/ax-clinic-project/scripts/.env` — `KOS_API_tenent_dev`(공개 · 데모) · `KOS_SYSTEM_EMAIL` · `KOS_SYSTEM_PASSWORD`(내부 · 시스템 계정). **`KOS_API_tenent`(운영 명동점) 사용 금지**
- 레포 규칙: 워크트리 `README.md`(기능 폴더 독립 — `procedure/` 밖 import 금지)

**기대는 개념** — 해당 없음.

## 2. 배경

명동 PoC v2 = 새 기능 `procedure/`(시술 현황판). 기존 `cc/` 를 쓰지 않고 새로 만든다. KOS 데모 지점에 실제로 붙는다. 목표 = **사용자가 로컬에서 E2E 할 수 있는 상태**(배포는 나중 WP7).

## 3. 계약

SPEC-003 §7(back ↔ front API · §7.5 SSE) 이 frontend 와의 계약이다. **WP1 에서 이 모양을 코드(`schemas/`)로 먼저 고정**하고, 그 뒤 바꾸지 마라 — 바꿔야 하면 코디에게 [질문].

## 4. 먼저 읽을 핵심 파일

- SPEC-003 §2(폴더 · 실행 · env · 포트) · §3(데이터 모델 · 대응표) · §4(KOS 연동) · §5(규칙 · 전이표 · 활성표) · §7 · §8 · §9
- 결정 표의 HAR 사실: `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/orchestration/work/myeongdong-poc-v2/_RESUME.md` §2 「(사실)」 줄

## 5. allowed_paths — 이 밖은 건드리지 마라

- `procedure/back/**`
- `procedure/docker-compose.yml` · `procedure/.env.example` · `procedure/README.md`

## 6. 구현 단계

1. **WP1** 뼈대 + 계약 고정(WORK-003 WP1 그대로). 끝나면 **중간 알림 한 번** 보내고 멈추지 말고 WP2 로:
   `orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --text "[WP1 완료] backend — schemas · 가짜 스냅샷 · SSE 고정. 커밋 없이 워크트리에 있음. WP2 진행" --enter`
2. **WP2** DB · 로그인 · 도메인 규칙 · 조작 API · 조작 뒤 SSE
3. **WP3** KOS 조회(토큰 2종 · 10초 일정 · 1시간 직원/방 · 09~21 KST · 4층 · 덮어쓰기 규칙) — 실 데모 지점 **조회** 1회로 카드 수 확인
4. **WP4** KOS 반영 대기열 · 확인 · 재전송 · 실패 — **실 데모 지점 쓰기 1회씩**(데모 일정 하나 · 시술 하나 — 담당 · 호출 · 수락 · flow-step · complete). 운영 키 금지
5. 로컬 실행: `procedure/docker-compose.yml` 로 back 이 뜨고(front 자리는 비워 둬도 됨), env 는 `procedure/.env`(gitignore) — `.env.example` 은 이름만. 로컬 `.env` 값은 위 ax-clinic `.env` 를 읽어 만드는 방법을 README 에(값 복사 X · 경로 안내)

## 7. 범위 제약 — 하지 말 것

- 키 · 토큰 · 비밀번호 · 계정 이메일 · 실명 · KOS id **값**을 코드 · 시험 데이터 · 커밋 · 보고에 넣지 마라(public 레포). 시험의 KOS 응답은 모양만 맞춘 가짜
- 운영 명동점 키 · 운영 일정에 쓰기 금지
- 사용자 포트(3600 · 8600 · 3700 · 8700)에 떠 있는 사용자 프로세스를 죽이지 마라 — 네가 띄운 것만 정리
- 커밋 · push · PR 금지

## 8. 검증

```
procedure/back 에서 uv run pytest · uv run ruff check . — WP 마다 그 WP 시험만 1회, 전체는 마지막 한 번. procedure 밖 import 없음 확인. 실 데모 조회 1회(WP3) · 쓰기 4종 1회(WP4) 결과를 수치로. 실행 못 한 검증은 사유와 함께 pending
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
  --to term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
