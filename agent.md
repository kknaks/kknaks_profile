# Agent Entry

이 파일은 에이전트가 `kknaks_profile` 레포에 들어왔을 때 가장 먼저 읽는 진입점이다.

## 시작 흐름

에이전트는 작업을 시작할 때 아래 순서로 진입한다.

```text
CLAUDE.md
→ agent.md
→ context/index.md
→ context/kknaks.md
→ company 또는 studio context
```

`context/index.md`는 사용자 요청을 회사 업무와 개인사업자/개인 프로젝트 업무로 분기하는 최상위 라우터다.

`context/kknaks.md`는 회사 업무와 개인사업자 영역을 구분하는 기준 문서다.

문서 민감도, 접근권한, 승인 게이트 관련 판단을 할 때는 `context/policy.md`를 추가로 읽는다.

## 목적

이 레포는 단순 포트폴리오가 아니라 이건학의 페르소나, 프로젝트, 학습 기록, 콘텐츠, 개발 현황을 하나의 source of truth로 관리하기 위한 작업 공간이다.

최종 목표는 하나의 진입점에서 다음을 모두 파악하고 개발할 수 있게 만드는 것이다.

- 나는 누구인지
- 어떤 프로젝트를 하고 있는지
- 각 프로젝트가 지금 어떤 상태인지
- 무엇을 다음에 개발해야 하는지
- 공개 포트폴리오에는 무엇을 보여줄지

## 응답 종료 전 Hook

에이전트가 아래 경로를 생성하거나 수정했다면, 최종 응답 전에 반드시 product doc pipeline hook을 수행한다.

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

## 지식 노트를 쓸 때

`inbox/` · `reference/` · `permanent/`(+ `permanent/concept/`)에 노트를 만들거나 고치기 전에 아래를 읽는다.

```text
rules/knowledge-note-pipeline.md     # 작성 규칙 (4층·SoT 위임·개념 성장·up: 방향)
→ templates/knowledge/<타입>.md      # 해당 층의 양식
```

**이 문서들이 형식의 SoT다.** 프롬프트는 "무엇을 만들라"만 지시하고, **어떻게 생겼는지는 여기 와서 읽는다** — 규칙을 프롬프트에 복사해 넣지 않는다. 복사하는 순간 SoT가 둘이 되고 어긋나기 시작한다.

| 만들 것 | 템플릿 | 경로 |
|---|---|---|
| 미정제 생각 | `templates/knowledge/idea.md` | `inbox/{YYYY-MM-DD}-{slug}.md` |
| 자료 정리 | `templates/knowledge/reference.md` | `reference/{group}/{YYYY-MM-DD}-{slug}.md` |
| 원자 개념 | `templates/knowledge/concept.md` | `permanent/concept/{slug}.md` |
| 종합 판단 | `templates/knowledge/permanent.md` | `permanent/{slug}.md` |

제품 문서(`products/**`)는 별도 계열이다 — `rules/product-doc-pipeline.md` + `templates/product/`.

작성 후 그래프 검증(L1~L6)이 pre-commit·부팅에서 자동으로 돈다. 규칙을 어기면 커밋이나 부팅이 막힌다.

## 지식층 읽기범위

지식 파이프라인 층(KDEV-SPEC-001/003)을 스캔할 때 범위는 아래와 같다.

- 평소 스캔(활성 층): `inbox/` · `reference/` · `permanent/` · `permanent/concept/` + `persona/posts/`
- cold(명시 요청 시에만): `permanent/archive/`

`permanent/archive/`는 안 쓰게 된 영구노트·개념의 장기기억이라 평소 스캔에서 제외한다. 사용자가 명시적으로 요청할 때만 읽는다(D-005).
