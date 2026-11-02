# 보고 — `origin/main` 을 브랜치에 머지 · 2026-09-15

머지 커밋 `8973791` · push 완료 · **PR #16 은 열린 채로 두었다**(`mergeable: MERGEABLE` · `state: OPEN`).
`gh pr merge` 를 실행하지 않았다.

## 한 줄

**충돌 파일은 하나였다** — `platform/codex_cli.py` 의 모듈 말미 헬퍼 구획. 나머지 아홉은 자동 머지됐다.
그리고 발주가 짚은 위험보다 한 겹 더 있었다: **`af01fa9` 는 `converse` 를 옮긴 것이 아니라 복제했고,
그 새 사본(`claude_cli.py`)에 우리 고침이 없어 옛 버그를 그대로 갖고 있었다.** 우리 수정은 **두 파일**로
갔다.

---

## 1. 충돌 파일 — 무엇 ↔ 무엇 · 어떻게 풀었나

### `backend/src/ax_workspace/platform/codex_cli.py` (유일한 충돌)

**부딪힌 것** — 파일 말미의 모듈 레벨 헬퍼 구획 셋.

| 헬퍼 | 우리(HEAD) | main | 어떻게 풀었나 |
|---|---|---|---|
| `_structured_body` | 갖고 있다 | **`cli_process.structured_body` 로 옮기고 여기서 삭제** | **저쪽을 딴다.** 이미 `structured_body as _structured_body` 로 import 돼 있고, main 의 본문이 우리 것과 **한 글자도 다르지 않다**(직접 대조했다) — 남길 이유가 없다 |
| `_invoke_runner` | 갖고 있다(우리가 만든 것이 아니다) | 같이 `cli_process` 로 옮겼다 | 같다 — **저쪽을 딴다** |
| `_invalid_response_message` | **우리 것만 있다** (`9fbf4f5`) | 없다 | **`cli_process.invalid_response_message` 로 옮겨 공용 헬퍼로 세웠다** — §2 |

세 헬퍼가 한 구획에 붙어 있어 git 이 「우리는 셋을 가졌고 저쪽은 셋을 지웠다」로 읽었다. 기계적으로
양쪽을 붙이면 `structured_body`·`invoke_runner` 가 **import 된 것과 로컬 정의로 두 벌** 서고, 저쪽만
따면 우리 수정이 **`NameError` 로 죽는다.** 그래서 셋을 갈라 각각 판단했다.

`_invalid_response_message` 를 `cli_process` 에 둔 이유 둘 —

1. **main 이 만든 구조의 뜻에 맞다** — 어댑터가 나눠 쓰는 것은 그 파일에 둔다(`structured_body` 가
   그렇게 옮겨졌다).
2. **어댑터 둘이 같은 판정을 한다** (§2). 한쪽에만 두면 다른 쪽이 **조용히 옛 문구로 돌아간다.**

서명을 `request` 에서 `output_schema` 로 좁혔다 — 그 함수가 보는 것이 그 값 하나이고, 공용 모듈이
`AiConversationRequest` 를 알 이유가 없다.

### 자동 머지된 아홉 — 확인한 방법

발주가 「양쪽이 건드렸다」고 짚은 나머지는 전부 자동 머지됐고, **눈으로 합치지 않고 테스트로 확인**했다.

| 파일 | 확인 |
|---|---|
| `backend/.../bootstrap/application.py` | 회의 233 · 대화 82 · architecture 32 통과 |
| `backend/.../entrypoints/http.py` | 같음 (라우트 계약은 `test_operation_inventory.py` 가 AST 로 대조한다) |
| `docs/unified-operations-inventory.json` | **생성물처럼 다루지 않아도 됐다** — 자동 머지 결과가 `test_operation_inventory.py` 를 그대로 통과한다. 그 테스트는 이 JSON 을 **실제 런타임(라우트·MCP 도구·소유 호출)과 AST 로 대조**하므로, 통과하면 손으로 합칠 자리가 없다는 뜻이다. 다시 만드는 명령은 리포에 없다(그 테스트가 곧 검증기다) |
| `frontend/src/App.tsx` · `lib/api.ts` · `lib/viewModels.ts` · `styles/ax.css` | `tsc --noEmit` 무경고 · `vitest` 621/622 · `vite build` 통과 |
| `Makefile` | `.PHONY` 행에 양쪽 타깃이 다 있다. `test_local_stack_targets.py` 통과 |

---

## 2. `codex_cli.py` 수정이 어디로 갔나 — **두 파일이다**

발주는 「파일이 쪼개졌으니 우리 수정이 어느 파일로 가야 하는지 다시 판단하라」고 했다. 판단 결과는
**「한 곳이 아니라 두 곳」**이다.

### `af01fa9` 는 `converse` 를 옮긴 것이 아니라 **복제했다**

```
main:codex_cli.py:173   def converse(...)      ← 그대로 있다 (우리 수정이 붙는 자리)
main:claude_cli.py:143  def converse(...)      ← 새로 생겼다 (같은 모양 · 우리 수정 없음)
```

두 `converse` 가 **같은 결함을 공유한다** — `request.output_schema` 가 걸려 있어도
`payload["body"]`·`payload["elements"]`·`payload["follow_up_candidates"]` 를 무조건 읽는다. 그것이
`9fbf4f5` 가 고친 바로 그 버그이고, 회의 AI 요약을 100% 실패시켰던 자리다.

### 왜 두 곳 다 고쳐야 하나

`Settings.ai_provider` **한 줄이 어느 어댑터를 쓸지 정한다**:

```python
_AI_PROVIDER_FACTORIES = {"codex": create_codex_cli_provider, "claude": create_claude_cli_provider}
```

회의 배치·합성은 그 설정을 모르고 `AiProvider` 포트로만 부른다. **`codex_cli` 만 고치면 provider 를
`claude` 로 두는 순간 회의가 다시 통째로 깨진다** — 그리고 그때의 증상이 `9fbf4f5` 가 실측한 것과
똑같다(`meeting_batch_runs` 전부 failed · 합성 3회 재시도 후 `status='failed'`).

### 무엇을 넣었나

| 파일:줄 | 무엇 |
|---|---|
| `cli_process.py:59 invalid_response_message` | 공용 헬퍼. 자기 스키마를 건 호출과 대화의 문구를 가른다 |
| `codex_cli.py:237`·`:256` | 우리 원래 수정이 **자동 머지로 살아남았다**(`converse` 본문은 충돌하지 않았다). 헬퍼 호출만 공용 것으로 바꿨다 |
| `claude_cli.py:198-227` | **같은 판정을 새로 넣었다** — `output_schema` 가 있으면 payload 를 그대로 `body` 로 돌려주고, 없으면 종전 대화 파싱 그대로 |

`claude_cli` 쪽은 payload 를 얻는 자리가 다르다(`ingest.structured_payload` → 없으면
`ingest.final_text` 파싱). 그 차이는 그대로 두고 **분기만 같은 자리에 넣었다** — 기계적으로 붙이지
않고 그 파일의 흐름에 맞췄다.

### 거는 테스트

`test_codex_cli.py` 는 우리 브랜치 것이 그대로 통과한다(13 passed). **`test_claude_cli.py` 에는 그
자리를 거는 것이 하나도 없었으므로** 셋을 새로 세웠다 —

- `test_a_conversation_that_asked_for_its_own_schema_gets_that_structure_back` — 배치 스키마를 걸고
  **실제 파서(`parse_output`)까지** 지난다
- `test_a_conversation_that_asked_for_the_final_notes_schema_parses_as_final_notes` — 합성 스키마
- `test_an_invalid_response_says_something_the_reader_of_that_turn_can_use` — 문구가 읽는 사람에 맞는다

**main 의 `claude_cli.py` 로 되돌리면 셋 다 실패하는 것을 확인했다** (`3 failed, 5 passed`).
되돌리고 다시 복원해 8 passed 로 돌아오는 것까지 봤다.

---

## 3. 버린 것

**기능은 하나도 버리지 않았다.** `af01fa9` 의 대화 목록·이력 기능은 그대로이고 대화 테스트 82개가
전부 통과한다(그쪽이 새로 들여온 `test_conversation_pagination.py`·`test_claude_stream_adapter.py`
11개 포함).

버린 것은 **코드 사본 둘**이다 — `codex_cli.py` 의 `_structured_body`·`_invoke_runner` 로컬 정의.
이유: main 이 그 둘을 `cli_process` 로 옮겨 공용화했고 **본문이 우리 것과 동일**하므로, 남기면 같은
함수가 두 벌 서고 import 와 로컬 정의가 이름을 다툰다. **동작은 한 글자도 바뀌지 않는다.**

---

## 4. 테스트 결과 — 기준선 대조

### 머지 전 기준선

```
6 failed · 1242 passed (311s)
```

그중 하나는 **flaky 가 아니라 내 것이었다** — `test_final_inventory_has_no_implicit_or_unverified_product_surface`.
`f89de32`(스트림 프레임) 이 `update_meeting_agenda`·`remove_meeting_agenda` 에 push 를 더했는데
`unified-operations-inventory.json` 의 `owning_calls` 를 따라 고치지 않았다. **머지 전에 별도 커밋
`e0b1b55` 로 고쳤다** — 그래서 대조 기준선은 **5 failed(전부 `material_*`)** 다.

> **내 실수 하나를 적어 둔다.** 그 커밋의 전체 결과를 `tail -8` 로 읽어 이 실패가 화면 밖으로 밀려
> 나갔고, 「실패는 전부 material flaky 다」로 보고했다. 목록을 자른 채로 결론을 낸 것이다.

### 머지 후

```
5 failed · 1263 passed (286s)
```

| | 머지 전 | 머지 후 |
|---|---|---|
| 통과 | 1242 | **1263** (+21: main 의 새 테스트 11 + 내 claude 테스트 3 + 나머지) |
| 실패 | 5 (`material_*`) | **5 (`material_*` — 같은 군)** |

실패 5건은 전부 `test_material_search.py` · `test_material_folders.py` ·
`test_material_worker_recovery.py` 이고 **그 세 파일만 따로 돌리면 25개가 전부 통과한다**
(`25 passed in 54.19s`). 병렬 부하에서 리스·시각 경합에 걸리는 기존 flaky 군이고, 실행마다 이름이
바뀐다. **머지가 건드린 코드 경로가 아니다.**

### 발주가 따로 보라고 한 것

| 무엇 | 결과 |
|---|---|
| **회의** | `tests/unit/test_meeting_*.py` + `tests/contract/test_meeting_*.py` → **233 passed** |
| **대화(저쪽 기능)** | `-k "conversation or chat or codex or claude"` → **82 passed** |
| **`test_codex_cli.py`** | **13 passed** (따로 확인) |
| `test_claude_cli.py` | **8 passed** (셋은 이번에 새로 걸었다) |
| architecture | **32 passed** — 인벤토리가 런타임과 맞는다 |

### 프론트

| 무엇 | 결과 |
|---|---|
| `npx tsc --noEmit` | **통과**(출력 없음) |
| `npx vitest run` | **621 / 622** — 실패 1건은 **실행마다 다른 파일**이다(1회차 `MyWorkPage.test.tsx`, 2회차 `TaskReferences.test.tsx`). 그 두 파일만 따로 돌리면 **25 passed**. 양쪽 머지가 손대지 않은 work 모듈이고 부하에서 흔들리는 자리다 |
| `npx vite build` | **통과** (1.19s) |

---

## 5. 하지 않은 것 (경계 확인)

- **리베이스하지 않았다** — `git merge origin/main` 하나다. 커밋 22개가 스쿼시로 접힐 것이므로 충돌을
  한 번만 풀었다.
- **`gh pr merge` 를 실행하지 않았다.** PR #16 은 `OPEN` 이고 `mergeable: MERGEABLE` 이다 —
  사용자 최종 검수를 기다린다.
- **force push 하지 않았다** — 평범한 `git push` 하나(`65a580c..8973791`).
- **「우리 것으로 덮기」도 「저쪽 것으로 덮기」도 하지 않았다** — 헬퍼 셋을 갈라 각각 판단했고, 그중
  둘은 저쪽을 따고 하나는 공용 자리로 옮겼다. 줄 수를 맞추려고 남의 기능을 지운 자리는 없다.
- **`git add .` 쓰지 않았다** — 해소한 파일 넷만 경로로 지정했다(자동 머지분은 git 이 이미 스테이징했다).
  **`git stash` 도 쓰지 않았다**(워크트리 공유).
- **로컬 스택·DB 무접촉** — API·워커·postgres·vite 를 건드리지 않았고 DB 에 아무것도 돌리지 않았다.

---

## 6. 열린 물음

1. **`claude_cli.py` 와 `codex_cli.py` 의 `converse` 가 사실상 같은 함수 두 벌이다.** 이번에 같은
   판정을 두 곳에 넣었고 테스트도 두 곳에 걸었지만, **다음 사람이 한쪽만 고치면 다시 갈라진다** —
   이번 버그가 정확히 그렇게 생겼다. `cli_process` 에 「payload → AiConversationResult」 한 자리를
   두고 둘이 부르는 모양이 옳아 보이는데, 그것은 `af01fa9` 의 구조를 다시 손보는 일이라 머지 범위
   밖으로 두었다. **스펙·리팩터 발주로 올릴 자리다.**
2. `material_*` flaky 군(백엔드)과 work 모듈 flaky 둘(프론트)은 여전히 남아 있다. 머지와 무관하지만
   「전체 초록」을 근거로 쓰기 어렵게 만드는 상시 잡음이다.
