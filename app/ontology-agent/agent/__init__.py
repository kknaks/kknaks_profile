"""에이전트 루프 — 제출 · 폴딩 소비자 · 답변 객체 검증.

실행은 open-kknaks(AgentClient + RedisBroker) 경유다. **LLM SDK 를 직접 import 하지
않는다**(ADR-04) — 이 패키지 어디에도 `anthropic`·`openai` import 가 없고,
`tests/test_w003_submission.py` 가 그것을 검사로 고정한다.

- `prompt` — 시스템 프롬프트. 도구 사용 규칙과 답변 형식만(S-001)
- `submission` — 제출 조립. per-tool `approval_mode` · `features.apps=false`
- `runtime` — 제출 + 소비자 기동
- `consumer` — 이벤트 폴딩(`tool_use_id` 멱등)
- `answer` — 답변 객체 파싱·검증(게이트 5)
- `store` — 채팅 저장소. **온톨로지 DB 와 다른 파일**
"""

from . import answer, consumer, prompt, runtime, store, submission

__all__ = ["answer", "consumer", "prompt", "runtime", "store", "submission"]
