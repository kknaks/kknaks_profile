
# [backend] KOS 내부 API 호출에 웹 클라이언트 헤더(User-Agent · Origin · kos-client-uri) 넣기

너는 **cc-prototype `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-시술현황-업데이트/orchestration/roles/cc-prototype/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/cc-prototype/kos-client-headers`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

이 워크트리는 너 혼자 쓴다.

## 1. SSOT — 먼저 읽을 것

- 이 브리프 §2 · §3 이 계약이다. 운영 장애 핫픽스라 SPEC 개정은 없다. **여기 없는 건 발명하지 마라.**
- `procedure/back/app/kos/client.py` 머리 주석 — KOS 공개 · 내부 API 인증 방식

**기대는 개념** — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

운영(ccc.medisolveai.xyz)에서 **2026-11-03 18:23 KST 부터 KOS 내부 API(`KOS_INTERNAL_API_BASE` = `https://api.kos-solution.com`) 호출이 전부 `403 {"message":"Unsupported client."}`** 로 막혔다. 일정 폴링 · 하루 예약 · 직원/방 · 예약 목록 · 고객 검색 · KOS 쓰기가 다 멈췄다. 공개 API(`open-api…`)는 정상이다.

코디가 운영 pod 안에서 urllib 로 재현했다(2026-11-04):

| 요청 | 결과 |
|---|---|
| 내부 `sign-in` — 기본 UA(`Python-urllib/…`) | 403 Unsupported client. |
| 내부 `sign-in` — Origin · Referer · `kos-client-uri` 만 추가 | 403 |
| 내부 `sign-in` — 브라우저 User-Agent 추가 | **200** |
| 내부 `get-rooms` — 같은 토큰, 브라우저 UA 없이 | 403 |
| 내부 `get-rooms` — 같은 토큰, 브라우저 UA | **200** |

즉 KOS 가 **매 내부 요청마다** User-Agent 를 본다. 지금 back 은 httpx 기본 UA(`python-httpx/…`)로 보낸다.
사용자 결정: **User-Agent 와 함께 KOS 웹이 보내는 `Origin` · `kos-client-uri` 도 같이 넣는다**(앞으로 KOS 가 이것까지 볼 수 있어서).

## 3. 계약 — 내부 API 요청에 붙일 헤더

KOS 웹(app.kos-solution.com)이 실제로 보내는 값(HAR 캡처 기준)을 따른다.

| 헤더 | 값 |
|---|---|
| `User-Agent` | `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36` |
| `Origin` | `KOS_WEB_BASE`(설정 `kos_web_base`, 운영값 `https://app.kos-solution.com`)의 끝 `/` 뗀 값 |
| `kos-client-uri` | `{kos_web_base}/{kos_tenant_id}/reservation/schedule/` |

- 붙이는 자리: **내부 API 로 가는 요청 전부** — `sign-in` · `get-user-account` · `internal()`(= `send(api="internal")` 포함). 기존 `Authorization` 헤더와 합친다.
- `kos_web_base` 가 비어 있으면 `Origin` · `kos-client-uri` 는 빼고 `User-Agent` 만 붙인다.
- **공개 API(`open-api…`) 요청과 presigned URL `PUT` 에는 붙이지 않는다** — 공개는 지금 정상이고, presigned 는 서명이 헤더에 민감하다.
- UA 문자열은 `client.py` 상수 하나로 둔다(env 로 빼지 않는다).

## 4. 먼저 읽을 핵심 파일

- `procedure/back/app/kos/client.py:61-169` — `KosClient`. KOS 로 가는 HTTP 는 전부 여기 하나(코디가 `kos_internal_api_base` 사용처 grep 으로 확인 — 이 파일 밖 없음). `_post_raw` · `internal_token` · `_user_account_id` · `_call` · `internal` · `put_presigned`
- `procedure/back/app/config.py:18-30` — `kos_open_api_base` · `kos_internal_api_base` · `kos_web_base` · `kos_tenant_id`
- `procedure/back/tests/fake_kos.py` — 테스트용 가짜 KOS(transport). 헤더 검증 테스트를 여기에 맞춰 단다

## 5. allowed_paths — 이 밖은 건드리지 마라

- `procedure/back/` (이번 범위는 `app/kos/client.py` + 테스트)

## 6. 구현 단계

1. **전수조사 먼저**: `procedure/back/app` 에서 KOS 로 나가는 HTTP 호출을 grep 으로 전부 센다(`kos_internal_api_base` · `kos_open_api_base` · `self.http.` · `httpx`). 내부 API 로 가는 자리 목록을 보고에 적는다.
2. 내부 요청 헤더를 만드는 함수 하나를 두고(§3), 내부로 가는 모든 자리가 그것을 거치게 한다.
3. 테스트: 가짜 KOS transport 로 ① `sign-in` · `get-user-account` · `internal()` 요청에 세 헤더가 §3 값으로 실리는지 ② 공개 API · presigned PUT 에는 안 실리는지 ③ `kos_web_base` 가 비면 UA 만 실리는지.

## 7. 범위 제약 — 하지 말 것

- 403 재시도 · 토큰 재발급 로직을 바꾸지 마라(401 처리 그대로).
- 로그 문구 · 다른 기능 · 프론트 · 앱을 건드리지 마라.
- 실제 KOS(운영 · 데모)에 요청을 보내지 마라. 실물 확인은 배포 뒤 코디가 한다.

## 8. 검증

```
procedure/back 에서 uv run pytest · uv run ruff check . — Phase 범위에 맞게 1회씩, 통과하면 반복하지 마라. 기능 폴더 밖 import 가 없는지 확인. 사용자 포트·프로세스를 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending 으로 보고
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
  --to term_2d7ec4cc-e726-4453-a485-d88d4284f1ec --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_2d7ec4cc-e726-4453-a485-d88d4284f1ec \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_2d7ec4cc-e726-4453-a485-d88d4284f1ec --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
