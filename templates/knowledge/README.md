# templates/knowledge

지식 노트 4층의 작성 템플릿. 작성 규칙은 `rules/knowledge-note-pipeline.md`.

| 템플릿 | 대상 경로 | `type` | 층 |
|---|---|---|---|
| `idea.md` | `inbox/{YYYY-MM-DD}-{slug}.md` | `idea` | (층 없음) |
| `reference.md` | `reference/{YYYY-MM-DD}-{slug}.md` | `reference` | `source` |
| `concept.md` | `permanent/concept/{slug}.md` | `concept` | `concept` |
| `permanent.md` | `permanent/{slug}.md` | `permanent` | `synthesis` |

**이 파일들은 형식의 SoT다.** 사람도 AI 도 여기를 보고 쓴다.

AI 에이전트는 레포를 읽을 수 있는 상태로 실행되므로(worker 가 repo 마운트, cwd=레포 루트),
**프롬프트에 이 내용을 복사해 넣지 않는다.** 진입 경로는
`CLAUDE.md → agent.md → rules/knowledge-note-pipeline.md → 이 디렉토리`다.
복사해 두면 SoT 가 둘이 되고 한쪽만 고쳐지는 날 어긋난다.

따라서 템플릿이 그래프 검증(L1~L6)을 통과하지 못하면 AI 산출물도 통과하지 못한다 —
템플릿을 고칠 때는 `app/back/core/graph.py`의 규칙과 함께 본다.

`<...>` 자리는 채워야 하는 값, 나머지 구조는 유지한다.
