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

`inbox/` · `resources/{source,concept}/` 에 노트를 만들거나 고치기 전에 아래를 읽는다.

```text
rules/knowledge-note-pipeline.md     # 작성 규칙 (4층·SoT 위임·개념 성장·up: 방향)
→ templates/knowledge/<타입>.md      # 해당 층의 양식
```

**이 문서들이 양식 원천이다.** 프롬프트는 "무엇을 만들라"만 지시하고, **어떻게 생겼는지는 여기 와서 읽는다** — 규칙을 프롬프트에 복사해 넣지 않는다. 복사하는 순간 양식 원천이 둘이 되고 어긋나기 시작한다.

> **「양식 원천」은 `SoT` 와 다른 말이다**(KDEV-DEC-018 D8). 양식 원천은 *문서가 어떻게 생겼나*, `SoT` 는 *데이터가 어디 사나*를 가리킨다. 한 문서 안에서 둘을 같은 단어로 부르지 않는다.

| 만들 것 | 템플릿 | 경로 |
|---|---|---|
| 미정제 생각 | `templates/knowledge/idea.md` | `inbox/{YYYY-MM-DD}-{slug}.md` |
| 자료 정리 | `templates/knowledge/reference.md` | `resources/source/{YYYY-MM-DD}-{slug}.md` |
| 원자 개념 | `templates/knowledge/concept.md` | `resources/concept/{slug}.md` |

별도 계열 넷:

- 제품 문서(`products/**`) — `rules/product-doc-pipeline.md` + `templates/product/`

  **`10-decision/` 을 쓸 때는 지식층까지 같이 간다.** 결정의 근거가 되는 개념이
  `resources/concept/` 에 없으면 **그 결정을 쓰는 턴에** `resources/source/` 출처 노트와
  `resources/concept/` 개념 노트를 만들어 잇는다 — 「나중에」·「사용자가」로 넘기지 않는다.
  넘긴 개념은 만들어지지 않는다. `product_doc_pipeline.py` 가 `up:` 과 「근거 개념」 절을,
  그래프 L1 이 없는 개념을 가리키는 것을 각각 error 로 막는다.
- 프로젝트 카드(`products/*/showcase.md`) — `templates/product/showcase.md`. 제품 문서와 같은 폴더에 있지만 **성격이 반대다** — 제품 문서는 내부 결정을 쌓는 곳이고 카드는 공개 사이트와 포트폴리오 PDF 에 나가는 한 장이다. 그래서 그래프 노드가 아니고(`persona_loader` 가 제외한다) 4층 모델 대상도 아니다. 관리 화면의 제품 등록이 그 파일을 읽어 카드를 렌더한다 — 형식을 고치려면 여기만 고친다.

  **`category` 만 이 템플릿이 아니라 `persona/_meta.yaml` 이 소유한다.** 목록 밖의 값이 들어가면 파일 하나가 거부되는 게 아니라 persona 로드 전체가 실패하고 사이트가 옛 데이터를 계속 서빙한다.
- 교안(`persona/contents/**`) — `templates/persona/content.md`. 그래프 밖이라 4층 모델 대상이 아니다. 승인 게이트의 `derived` 스테이지와 `content_enrich` 잡이 **둘 다 이 파일을 읽는다** — 형식을 고치려면 여기만 고친다.
- 잔디 산출물(`persona/daily/**` · `persona/career/**`) — `templates/persona/daily.md` · `templates/persona/career.md`. 교안과 같이 그래프 밖이라 4층 모델 대상이 아니고 발행 시 그래프 검증도 받지 않는다. 잔디 파이프라인의 `daily` 게이트 스테이지가 두 파일을 읽어 프롬프트를 만든다 — 형식을 고치려면 여기만 고친다.

  두 문서의 성격이 반대다. **daily 본문은 사이트에 노출되지 않고**(잔디가 쓰는 것은 `counts` 와 `summary[]` 뿐이다) 다음 단계의 입력으로만 쓰이는 반면, **career 본문은 경력 페이지에 그대로 렌더된다.** 그래서 daily 는 재료로 남기고 career 는 압축해 다시 쓴다.

작성 후 그래프 검증(L1~L6)이 pre-commit·부팅에서 자동으로 돈다. 규칙을 어기면 커밋이나 부팅이 막힌다.

## 그래프 밖 디렉토리

지식층도 제품 문서도 아닌 것 둘이 레포 루트에 있다. **주인이 있으니 지우지 않는다.**

| 디렉토리 | 무엇 | 주인 |
|---|---|---|
| `downloads/` | **운영 자산.** 백엔드가 `/download/*` 로 정적 서빙하고 DeskDeck 랜딩이 링크한다. **지우면 다운로드가 죽는다** | mac-remote RB-001 |
| `persona/assets/` | 프로필 이미지 등 | persona |

제품별 작업 보고는 `products/{제품}/30-work/reports/` 에 둔다 — 루트에 두면 어느 제품 것인지 문서로 알 수 없다.

## 지식층 읽기범위

지식 파이프라인 층(KDEV-SPEC-001/003)을 스캔할 때 범위는 아래와 같다.

- 평소 스캔(활성 층): `inbox/` · `resources/source/` · `resources/concept/` + `persona/posts/`
- cold(명시 요청 시에만): `archive/`

`archive/`는 안 쓰게 된 노트·개념의 장기기억이라 평소 스캔에서 제외한다. 사용자가 명시적으로 요청할 때만 읽는다(D-005).

**폴더 이름은 층 이름이고 `type` 이름과 다르다** — `resources/source/` 에 `type: reference` 가 들어간다. 폴더는 층을, `type` 은 frontmatter 계약을 가리켜 축이 다르기 때문이다(KDEV-DEC-018 D1).

`archive/` 가 `resources/` 밖인 것은 **층이 아니라 상태**여서다. `products/{제품}/_archive/`(버전 컷오프 동결본)와는 다른 것이다.
