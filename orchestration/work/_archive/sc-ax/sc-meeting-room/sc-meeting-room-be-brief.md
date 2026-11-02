# [backend] 자기 스키마를 넘기는 AI 경로가 전부 깨져 있다

너는 **sc-ax `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting-redesign/orchestration/roles/sc-ax/backend/role.md`
  (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: **`/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting-room`**
(branch `kknaksss/sc-meeting-room`, 커밋 `852e58a` 위)

⚠ **같은 워크트리에 다른 워커가 있다** — `.design-sync/` 를 만지는 designer 세션이 대기 중이다.
너는 `backend/` 만 만지므로 안 겹치지만, **`.design-sync/` 와 `frontend/` 는 건드리지 마라.**
커밋도 하지 마라 — 코디가 갈라서 커밋한다.

## 1. 증상 — 실물로 확인했다

회의 중간 요약이 **한 번도 성공하지 못한다.** 로컬 DB 실측:

```
meeting_batch_runs:  seq 1~11 전부 failed
reason:              「답변 형식을 확인하지 못했습니다. 다시 요청해 주세요.」
```

회의 종료 합성도 같다 — `meetings.status='failed'`,
`failure_reason='회의록을 만들지 못했습니다 — 잠시 뒤 다시 시도해 주세요'`,
워커 로그에 `ProviderRequestFailed: Codex CLI conversation failed` 3회 재시도 후 포기.

## 2. 원인 — 코디가 좁혀 뒀다. **다만 네가 다시 확인해라**

`backend/src/ax_workspace/platform/codex_cli.py:240~249`

```python
payload = json.loads(output_path.read_text(encoding="utf-8"))
document = AnswerDocument.model_validate({"body": payload["body"], "elements": payload["elements"]})
...
for item in payload["follow_up_candidates"]
except (OSError, ValueError, KeyError, TypeError) as error:
    raise ProviderResponseInvalid("답변 형식을 확인하지 못했습니다. 다시 요청해 주세요.", provenance)
```

**응답을 읽는 쪽이 대화 계약(`body`·`elements`·`follow_up_candidates`)을 고정으로 기대한다.**

그런데 같은 함수가 **부르는 쪽이 준 스키마를 강제**한다(:205~209 주석: 「스키마는 언제나 건다. 부르는 쪽이
자기 것을 주면 그것이고(회의 배치·합성이 그렇다), 주지 않으면 대화 계약」).

- 회의 배치 → `modules/meetings/schemas/ai_batch_output.json` — 최상위 `properties` 가 **`agendas` 하나뿐**
- 회의 합성 → `bootstrap/application.py:471` 의 `FINAL_OUTPUT_SCHEMA`

즉 **LLM 은 시킨 대로 `{"agendas":[…]}` 를 정확히 돌려주는데 파서가 `payload["body"]` 를 찾다가 `KeyError`** 를
내고, 그것이 `ProviderResponseInvalid` 로 바뀐다. **100% 실패다.**

코디 확인: Codex CLI 를 손으로 부르면(같은 모델·같은 인자·**같은 스키마**) `turn.completed` 로 성공한다.
CLI·인증·모델·스키마 자체는 멀쩡하다 — **응답 파싱만 틀렸다.**

**언제 들어왔나**: `git log -S'payload["follow_up_candidates"]'` → **`42e4335` (#3 SCAX 채팅창 인터랙션을 고도화한다)**.
채팅용 파싱을 공용 경로에 박으면서 회의 배치·합성이 같이 깨진 것으로 보인다.

**이 전제를 그대로 믿지 마라.** 네가 코드를 읽고 재현해서 확인한 뒤 고쳐라. 다르면 다르다고 보고해라.

## 3. 고치는 방향 — 판단은 네가

원칙만 준다. 설계는 네가 정하고 근거를 보고해라.

- **응답 파싱이 요청한 스키마를 따라야 한다.** 대화 계약을 안 준 경우에만 `body`/`elements`/`follow_up_candidates` 를 기대한다
- **부르는 쪽이 자기 스키마를 줬으면, 파싱도 그 쪽이 책임지게** 하는 것이 자연스럽다 —
  `converse()` 가 원문(payload)을 돌려주고 대화 경로만 `AnswerDocument` 로 감싸는 식
- **채팅 경로를 깨뜨리지 마라.** 지금 도는 것이 계속 돌아야 한다

## 4. 경계

| | |
|---|---|
| **`frontend/` 를 건드리지 마라** | 이 버그는 백엔드다. 프론트는 실패 메시지를 그대로 보여줄 뿐이다 |
| **스키마 파일을 고쳐서 우회하지 마라** | `ai_batch_output.json` 에 `body` 를 억지로 넣는 식은 오답이다. **파서를 고쳐라** |
| **프롬프트로 때우지 마라** | 「`body` 도 같이 내라」고 시키는 것도 오답이다 |
| **재시도 횟수를 늘리지 마라** | 100% 실패라 재시도로 안 풀린다 |

## 5. allowed_paths

- `backend/` · `docker-compose.yml` · `Makefile`

## 6. 검증

```
cd backend && uv run pytest -q <네가 만들거나 고친 테스트 파일만> -m 'not integration'
cd backend && uv run pytest -q tests/architecture        # 경계 테스트는 항상
```

전체 스위트·integration 마커 금지(사용자 방침). 검증은 1회만.

**★ 이 버그는 단위 테스트가 못 잡았다.** 자기 스키마를 넘기는 경로에 **파싱까지 도는 테스트가 없었다**는 뜻이다.
고치면서 **그 구멍을 막는 테스트를 새로 걸어라** — 배치 스키마로 부른 응답이 제대로 파싱되는지.

자기점검(역할문서 rules):
- `modules/*/domain.py`·`application.py` 가 `fastapi`/`mcp`/`sqlalchemy` 를 import 하지 않는가
- `entrypoints` 가 platform 구현을 직접 import 하지 않는가
- 스키마 변경을 `reset_demo` 밖에서 하지 않았는가

## 7. 실물 확인 — 이것까지가 완료 조건

단위 테스트로는 부족하다. **로컬 스택이 지금 떠 있다**(API 8001 · 워커 3 · postgres 54329) — **바로 이 워크트리에서 돌고 있다.**
**절대 죽이거나 재기동하지 마라.** 사용자가 쓰는 중이다. 네 코드 변경은 API 재기동 전까지 반영되지 않는다
(`make local-stack` API 는 `--reload` 가 없다) — 재기동이 필요하면 **코디에게 말해라.**

네가 할 수 있는 실물 확인:
- 네 워크트리에서 **Codex CLI 를 배치 스키마로 직접 호출**해 응답을 받아, 고친 파서에 통과시켜 봐라
- 코디가 재현에 쓴 인자는 이렇다(그대로 쓰면 된다):
  ```
  codex exec --skip-git-repo-check --ignore-user-config --ignore-rules \
    -c 'shell_environment_policy.inherit="none"' -m gpt-5.6-terra \
    -c 'service_tier="fast"' -c 'model_reasoning_effort="low"' \
    --json --output-schema <스키마> --output-last-message <출력> "<프롬프트>"
  ```
- **스택 재기동이 필요하면 코디에게 말해라.** 네가 하지 마라

## 8. 보고

- **원인 확정** — 코디 전제가 맞았는지, 틀렸으면 무엇이 진짜인지
- 고친 설계와 **왜 그 설계인지**
- **새로 건 테스트** — 이 구멍을 어떻게 막았는지
- 실물 호출 결과 (배치 스키마 응답이 파싱되는지)
- `pytest` 결과
- 채팅 경로가 안 깨졌음을 무엇으로 확인했는지
- 같은 뿌리로 깨져 있던 **다른 경로가 있으면 그것**(`platform/reports.py:864` 도 `output_schema` 를 넘긴다)
