# Agent Entry

이 파일은 에이전트가 `kknaks_profile` 레포에 들어왔을 때 가장 먼저 읽는 진입점이다.

**이 문서는 라우터다.** 규칙을 여기 적지 않는다 — 어디로 가야 하는지만 가리킨다. 규칙을 진입점에 복사하면 그 순간 원천이 둘이 되고, `context/index.md` 의 「읽기 범위 원칙」과 역할이 겹친다.

## 시작 흐름

```text
CLAUDE.md
→ agent.md            # 여기 — 무엇을 하려는지에 따라 아래로 분기
→ context/index.md    # 최상위 context 라우터
→ context/kknaks.md   # 회사 · 여름별컴퍼니 · 개인 세 영역을 가르는 기준
```

[[context/index|context/index]] → [[kknaks]] 로 내려간다. **경로 문자열이 아니라 링크로** 걸어 옵시디언에서도 같은 길이 보이게 한다.

문서 민감도·접근권한·승인 게이트를 판단할 때는 [[policy]] 를 추가로 읽는다.

## 목적

이 레포는 단순 포트폴리오가 아니라 이건학의 페르소나, 프로젝트, 학습 기록, 콘텐츠, 개발 현황을 하나의 source of truth로 관리하기 위한 작업 공간이다.

최종 목표는 하나의 진입점에서 다음을 모두 파악하고 개발할 수 있게 만드는 것이다.

- 나는 누구인지
- 어떤 프로젝트를 하고 있는지
- 각 프로젝트가 지금 어떤 상태인지
- 무엇을 다음에 개발해야 하는지
- 공개 포트폴리오에는 무엇을 보여줄지

## 무엇을 만들거나 고치나 — 계열별 규칙

**세 계열이 있고 각자 `rules/` 문서가 규칙을 갖는다.** 진입점은 어디로 갈지만 정한다.

| 건드리는 곳 | 규칙 | 양식 |
|---|---|---|
| [[resources/README\|resources]] | [[knowledge-note-pipeline]] | `templates/knowledge/` |
| [[products/README\|products]] | [[rules/product-doc-pipeline\|product-doc-pipeline]] | `templates/product/` |
| `products/*/showcase.md` · `persona/{contents,career,daily}/**` | [[persona-artifacts]] | `templates/persona/` 등 |

**규칙과 양식은 레포에 있다. 프롬프트에 복사하지 않는다** — 복사하는 순간 원천이 둘이 되고 한쪽만 고쳐지는 날 조용히 어긋난다.

**제품 결정을 쓸 때는 지식층까지 같이 간다.** `10-decision/` 의 근거 개념이 `resources/concept/` 에 없으면 **그 결정을 쓰는 턴에** 출처·개념 노트를 만들어 잇는다 — 「나중에」·「사용자가」로 넘기면 그 개념은 만들어지지 않는다. 상세는 두 규칙 문서가 갖는다.

## 응답 종료 전 Hook

아래 경로를 생성하거나 수정했다면, 최종 응답 전에 반드시 product doc pipeline hook을 수행한다.

```text
products/**
templates/product/**
rules/product-doc-pipeline.md
.agent/hooks/product-doc-pipeline.md
.agent/scripts/product_doc_pipeline.py
```

수행 순서:

```text
.agent/hooks/product-doc-pipeline.md 체크리스트 확인
→ python3 .agent/scripts/product_doc_pipeline.py 실행
→ warnings/errors/needs_user_decision 확인
→ 최종 응답에 검증 결과 포함
```

hook이 실패하면 성공처럼 보고하지 않는다. 자동으로 판단할 수 없는 제품 결정은 사용자에게 결정이 필요하다고 보고한다.

지식층(`resources/**`)과 제품 문서는 pre-commit 이 그래프 검증(L1~L6)과 `product_doc_pipeline --strict` 를 돌린다. **ERROR 면 커밋이 막힌다.**
