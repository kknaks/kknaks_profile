
# [backend] WP19 — 통역 기록 보관 기간을 env `INTERPRET_RECORD_KEEP_DAYS` 로 · 비면 삭제 안 함 (D-42 · SPEC 0.7.0)

너는 **interpret-pwa `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/roles/interpret-pwa/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/interpret-pwa/interpreter-idea`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

너는 앞 맥락이 없다. 이 워크트리는 너 혼자 쓴다(front 변경 없음).

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/para/projects/summer-star/interpret-pwa/20-spec/spec-001-interpret-pwa.md` (0.7.0 · 코디 커밋 `98753c94`) ← 계약의 SoT. **여기 없는 건 발명하지 마라.** 볼 절: §2.4 env 표 `INTERPRET_RECORD_KEEP_DAYS` 행 · **§5.9 「보관 기간 — env」 표 · 「삭제 규칙 — 보관 기간이 N 일 때만」** · 기동 ② ④ · §9.1 「기록」 ⑦ ⑨
- `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/para/projects/summer-star/interpret-pwa/30-work/work-001-interpret-pwa.md` **WP19 행**(86줄) — 할 일 ① ~ ⑤ · 산출 파일 · 완료 조건 · 검증 명령
- `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md` D-42(98줄)
- 코드 레포 `AGENTS.md`(있으면)

**기대는 개념**: 해당 없음.

## 2. 배경 / 무엇을 바꾸나

통역 기록(D-41)은 지금 `KEEP_DAYS = 7` 고정으로 기동 1회 + 24시간마다 7일 지난 날짜 파일을 지운다. 베타 기간 데이터 수집 때문에 사용자가 7일 삭제를 없애기로 했다(D-42). 보관 기간을 env 로 빼고 **비어 있으면 지우지 않는다**. 운영에는 값을 넣지 않는다 → 배포되면 운영에서 삭제가 멈춘다.
**기한**: 운영의 가장 오래된 파일(11-11)이 11-18 에 지워진다 — 이 WP 가 빨리 끝나야 배포(WP20)가 그 전에 된다.

## 3. 계약 (SPEC §5.9 표 요지 — 판정 순서)

| 값(앞뒤 공백 지운 뒤) | 동작 | 기동 로그 |
|---|---|---|
| 없음 · 빈 문자열 · 공백만 | 삭제 안 함 · 경고 0 · 기동 삭제 0 · 24시간 배경 작업 **안 만듦** | `interpret records: on dir=<경로> keep_days=off` |
| 십진 숫자로만 된 1 이상(`7` · ` 7 ` · `07`) | 0.6.0 삭제 규칙에 N(오늘 KST − N 이하 · 이름 `YYYY-MM-DD.jsonl` 만) · 기동 1회 + 24시간마다 | `… keep_days=N` |
| 그 밖(`0` · `-1` · `abc` · `+7` · `7.0`) | 경고 로그 1줄 · 삭제 안 함 · 배경 작업 없음 · **기동 성공 · 기록은 켜짐** | 경고 1줄 + `… keep_days=off` |
| `INTERPRET_RECORD_DIR` 비었음 | 지금처럼 기록 끔 — 이 값 무관 | `interpret records: off` |

- 설정 클래스에서 정수 필드로 두면 `abc` 에서 기동이 죽는다 — **문자열로 받고 판정은 기록 쪽에서**(방법은 너의 재량, 계약은 위 표)
- 경고 문구는 재량 — 값 자체는 찍어도 된다(비밀 아님). 기록 문장 · 키는 로그에 0

## 4. 먼저 읽을 핵심 파일

- `back/app/service/records.py:28` `KEEP_DAYS = 7` · `:132` `sweep` · `:155` `sweep_forever` · `:220 ~ 240` `open_records`(기동 로그 · 기동 삭제)
- `back/app/main.py:70 ~ 85` lifespan 배경 작업(`sweep_forever` 태스크 만들기 · 취소)
- `back/app/config.py:15 ~ 35`(`env_ignore_empty=True` — 빈 문자열은 걸러지지만 공백만은 안 걸러진다)
- `back/app/container.py` `open_records` 호출
- `back/tests/test_records.py:300 ~ 430` 기동 로그 · 7일 삭제 시험들(N=7 시험으로 옮길 것)
- `.env.example`(레포 루트) — 이름만 한 줄 추가

## 5. allowed_paths — 이 밖은 건드리지 마라

- `back/`
- `docker-compose.yml · .env.example (레포 루트)`

## 6. 구현 단계

1. WORK WP19 ① ~ ⑤ 그대로(config · records · main · 시험 · `.env.example`)
2. §9.1 ⑨ (a) · (b) · (c) 갈래를 **값마다 하나씩** 시험(공백만 · ` 7 ` · `07` · `+7` · `7.0` 포함) · ⑦ 끔 + 값 7 → 끔
3. 기존 0.6.0 7일 삭제 시험은 지우지 말고 「값 7」 시험으로 옮긴다
4. 보고서를 `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/interpreter-idea/wp19-be-report.md` 에 쓴다(변경 파일 · 시험 수 · 명령 출력 요지)

## 7. 범위 제약 — 하지 말 것

- 기록 줄 모양 · 걸린 term 판정 · 넣지 않는 것 · 쓰기 실패 동작은 건드리지 않는다(D-41 그대로)
- `test_api_surface.py` 는 고치지 않는다(그대로 통과해야 한다)
- front · infra · 문서(`para/`) 수정 금지 · 운영 서버 접근 금지 · Soniox 실물 호출 불필요(키 없이 시험만)
- 사용자 포트 · 프로세스를 건드리지 않는다

## 8. 검증

```
back 에서 uv run pytest · uv run ruff check . — Phase 범위에 맞게 1회씩, 통과하면 반복하지 마라. Soniox · Procedure Hub 경로는 실물 호출 1회(키 없으면 pending). 사용자 포트·프로세스를 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending 으로 보고
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
  --to term_0065c22f-b4a3-475e-bf78-3b62bac38378 --from term_576cdff8-b677-444b-8839-492a5f8e8f88 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_0065c22f-b4a3-475e-bf78-3b62bac38378 \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_0065c22f-b4a3-475e-bf78-3b62bac38378 --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
