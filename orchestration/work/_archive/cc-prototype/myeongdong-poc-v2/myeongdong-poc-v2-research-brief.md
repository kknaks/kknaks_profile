
# [researcher] KOS 데모 지점 접속 정보 · 시술 관련 API 참고 문서

너는 **cc-prototype `researcher` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/orchestration/roles/cc-prototype/researcher/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

⚠ 코디네이터가 같은 워크트리에서 문서를 쓰고 있다 — **산출물 파일 1개 말고는 아무것도 만들거나 고치지 마라.**

## 1. SSOT — 먼저 읽을 것

**KOS 연동의 메인 참고처는 ax-clinic-project(private)다.** 키 값과 사용법은 거기 있고, 이 레포(public)에는 옮기지 않고 가리킨다.

- 키 값: `/Users/kknaks/git/ax-clinic-project/scripts/.env` — `KOS_API_tenent_dev` 만 쓴다
- 사용법(메인): `/Users/kknaks/git/ax-clinic-project/para/resources/technology/2026-09-18-kos-developers-api-guide.md` — 호스트 · 인증 · 오류 · 작업 목록. 이 문서와 겹치는 내용은 **다시 쓰지 말고 절 번호로 링크**한다. 2026-09-18 스냅샷이라 현재 스펙과 다른 점(새 작업 등)만 산출물에 적는다
- 호출 코드(메인): `/Users/kknaks/git/ax-clinic-project/scripts/kos_collect.py` — 인증 · .env 읽기 · 호출을 이 코드의 방식대로 한다
- KOS 공개 OpenAPI 스펙(현재본): `https://developers.kos-solution.com/openapi.yaml` ← 필드 · 작업 사실의 SoT. **여기 없는 필드 · 작업은 발명하지 마라.** 코디가 받아 둔 사본 `/private/tmp/claude-501/kos-openapi.yaml` 이 있으면 써도 되지만 URL 원본이 우선
- 공식 문서: `https://developers.kos-solution.com/docs/openapi` · 인증 `https://developers.kos-solution.com/docs/openapi/authorization`
- 1차 때 정리(내부 API 와 공개 API 구분): `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/orchestration/work/_archive/cc-prototype/sts-prototype/research-kos-har-report.md` · 같은 폴더 `kos-staff-api-report.md`
- v1 업무 흐름(시술 단계가 어디 있는지): `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/reference/2026-10-12-cc-prototype/workflow.md` §6 · §7 · §8 · 「KOS 반영 표」

**기대는 개념** — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

명동 PoC v2 는 **시술 현황판**이다. 전제: 고객이 수납까지 끝냈고, 수납이 끝나면 KOS 에 시술 목록이 올라간다. v1 은 KOS 를 한 번도 부르지 않았지만 v2 는 **KOS 데모 지점에 실제로 붙여 테스트**한다.

코디가 2026-10-20 확인한 사실(다시 확인하고 문서에 적어라):

- 키: `/Users/kknaks/git/ax-clinic-project/scripts/.env` 의 `KOS_API_tenent_dev` = **데모 지점**. 이름과 달리 dev 서버가 아니다 — `https://open-api.kos-solution.dev` 는 `400 apiKey NotFound`, **`https://open-api.kos-solution.com`(운영 호스트)** 에서만 토큰이 나온다
- 같은 파일의 `KOS_API_tenent` = **실제 운영 명동점**. **이 키는 절대 쓰지 마라**
- 인증: `POST /open/authorization/commands/exchange-token` body `{"key": <키>}` → `{"token": ...}` → 이후 `Authorization: <token>`(Bearer 없음). 작업은 전부 POST
- 데모 식별: `getZones` = `4층`(id `6a793cd9bb2d7899923714ed`, 기본) + `미사용` / `getAccounts` 77건, `KOS-DEMO` 계정 있음(운영엔 없음)

이것을 앞으로 시술 현황판을 만들 때 계속 볼 **참고 문서 한 장**으로 모은다. 흐름(v2 workflow)은 아직 사용자가 설명 중이라 **API 를 고르지 않는다 — 후보를 전부 모은다.**

## 3. 계약

해당 없음. 산출물 하나:

**`/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/reference/2026-10-12-cc-prototype/kos-demo-api.md`**

## 4. 산출물 구성

1. **접속 정보** — 맨 위에 「키 값 · 사용법 메인 = ax-clinic-project」 세 경로(§1). 그 아래 이 PoC 에만 해당하는 것: 데모 지점은 운영 호스트 `.com`(`.dev` 아님 — 확인 결과 그대로), 키 **이름과 파일 위치만**, 운영 키 금지, 데모 식별값(구역 id · `KOS-DEMO` 계정 유무). 인증 흐름은 가이드 절 링크로. 확인한 날짜
2. **시술 관련 작업 전수표** — 스펙 전체를 `grep` 으로 훑어 아래에 **닿는 작업을 전부** 넣는다(목록을 미리 주지 않는다 — 스펙에서 세라): 시술(procedure · task · procedure-task) · 일정(schedule · flowStep · reservation 중 시술 진행에 닿는 것) · 수납(purchase · transaction · 시술 목록이 수납에서 생기는 지점) · 시술 메뉴(product · procedure · machine · medicine · medical-service) · 구역 · 직원 · 내원객. 각 줄: operationId · 경로 · 조회/쓰기 · 한 줄 용도 · 요청 필수 필드 · 공식 문서 URL · deprecated 여부 · 데모 호출 결과(아래 3). 몇 개를 셌는지와 grep 에 쓴 단어를 문서에 적어라
3. **데모 실호출(조회만)** — 2 의 **조회 작업**을 데모 키로 각 1회. 필수 파라미터가 필요하면 다른 조회 응답에서 얻은 id 를 쓴다(예: 일정 목록 → 일정 id → 상세). 기록: 성공/HTTP 코드 · 응답 **모양**(필드 이름 · 타입 · 중첩, 건수). 값은 enum · 상태 코드처럼 사람 정보가 아닌 것만
4. **「수납 → 시술 목록」이 어디서 보이나** — 수납이 끝난 건의 시술 목록이 어느 작업 응답의 어느 필드에 실리는지. 데모에 해당 건이 없으면 「데모에 없음 — 수납 완료 건 필요」로 적는다
5. **쓰기 작업** — 시술 진행 · 완료 · 배정 · 이동에 닿을 법한 `/commands/` 작업을 표로만(호출 안 함). 스펙에 없는 조작은 「스펙에 없음」
6. **정할 것** — 결정하지 말고 모은다

## 5. allowed_paths — 이 밖은 건드리지 마라

- `reference/2026-10-12-cc-prototype/kos-demo-api.md` (새 파일 1개)
- 그 외 전부 read-only. 원시 응답을 파일로 저장하지 마라(필요하면 `/private/tmp/claude-501/` 아래에만, 끝나면 지운다)

## 6. 단계

1. 스펙 받아 grep 으로 후보 전수 → 표
2. 토큰 교환(데모 키) → 조회 작업 각 1회
3. 문서 작성 → §8 자가 점검

## 7. 범위 제약 — 하지 말 것

- **`/commands/` 쓰기 작업 호출 금지.** 데모 지점이어도 운영 시스템이다
- **운영 키 `KOS_API_tenent` 사용 금지**, dev 서버 재시도 불필요(1회 확인은 해도 됨)
- **이 레포는 public 이다.** 키 값 · 토큰 · 사람 이름 · 전화번호 · 이메일 · 생년월일 · 메모 원문을 문서에 넣지 마라. 직원 · 내원객 응답은 필드 이름과 건수만
- 흐름(v2 workflow) · 화면 · 결정을 정하지 마라. 「어떤 API 를 쓸지」도 고르지 마라 — 후보와 사실만
- 커밋 · push · PR 금지

## 8. 검증

```
질문마다 답 + 공식 문서 URL. 문서에 없는 것은 「문서에 없음」. 결정하지 않고 「정할 것」으로 모은다
```

- 표의 각 작업에 공식 문서 URL. 호출 결과는 실제로 부른 것만 「확인」, 못 부른 건 사유와 「미확인」
- 끝나기 전 산출물에 `grep` 으로 키 · 토큰 형태 문자열(긴 hex · uuid · `eyJ`)과 한글 이름이 없는지 확인하고 결과를 보고에 적어라
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
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --text "[질문] researcher: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
