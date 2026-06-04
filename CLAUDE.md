# CLAUDE.md

이 레포에서 작업을 시작하기 전에 먼저 `agent.md`를 읽는다.

`agent.md`가 이 프로젝트의 에이전트 진입점이다.

## Agent Directory

이 레포의 에이전트 설정 원천은 `.agent/`이다.

Claude 환경에서 `.claude/`가 필요하면 `.claude`를 별도 원천으로 만들지 말고 `.agent`를 가리키는 심볼릭 링크로 둔다.

```bash
ln -s .agent .claude
```

`.claude/` 아래에 직접 규칙, hook, script를 추가하지 않는다.
