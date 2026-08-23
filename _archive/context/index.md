# Context Index

이 문서는 `kknaks_profile`의 최상위 context 라우터다.

에이전트는 레포에 들어오면 `CLAUDE.md` 또는 `agent.md`를 통해 이 문서로 진입하고, 사용자 요청의 성격에 따라 하위 context로 단방향 분기한다.

## 목적

`context/`는 회사 경험 기록과 개인사업체/개인 프로젝트 운영을 구분해서 탐색하기 위한 라우팅 계층이다.

이 문서는 상세 내용을 담지 않는다. 요청을 어느 하위 context에서 처리할지 결정한다.

## 문서 계층

```text
context/
├── index.md                  # 최상위 context 라우터
├── kknaks.md                 # 회사 경험 기록과 개인사업자 영역의 구분 기준
├── policy.md                 # 문서 민감도, 접근권한, 승인 게이트 정책
├── company/                  # 회사 코드 작업이 아니라 이력서/포트폴리오용 경험 기록
│   ├── current.md            # 현재 정리 중인 회사 경험, 챌린지, 해결방안, 성과
│   ├── projects.md           # 회사 제품/프로젝트 경험의 목록과 경계
│   └── org.md                # 회사 조직도, 사람, 역할, 협업 관계
├── studio/                   # 여름별컴퍼니 개인사업자 프로젝트 운영
│   ├── current.md            # 현재 우선순위, 진행 중 작업, blocker
│   ├── org.md                # 여름별컴퍼니 조직 구조와 역할
│   └── workflow.md           # 작업 종류와 공통 작업 흐름
└── personal/                 # 사람 본인 — 배움(자료·개념)과 이력(그날 한 일)
    ├── current.md            # 지금 무엇을 배우고 있나
    └── projects.md           # 학습 갈래
```

**영역이 셋이다** — 회사·여름별컴퍼니는 **역할**이고 개인은 **사람 본인**이다([[decision-020-para-alignment-area-and-personal|KDEV-DEC-020]] D1). 구분 기준은 [[kknaks]] 가 갖는다.

`personal/current.md` 는 **잔디 대상이 아니다.** 회사·studio 의 `## 진행 중` 은 커밋이 말하지만 개인은 커밋 축이 아니라 배움 축이라 사람이 쓴다([[decision-022-grass-updates-current|KDEV-DEC-022]]).

## 연결 계층

```text
products/
├── README.md                 # 여름별컴퍼니 제품별 SSOT 진입점
└── <product>/README.md       # 특정 제품의 문서 map

resources/
├── source/                   # 자료 기록 (type: reference)
└── concept/                  # 원자 개념 (type: concept)

rules/
├── product-doc-pipeline.md   # 제품 문서 파이프라인 운영 규칙
├── knowledge-note-pipeline.md # 지식 노트(inbox·resources) 작성 규칙
└── persona-artifacts.md      # showcase·교안·잔디 (그래프 밖 계열)

templates/
├── product/                  # 제품 문서 작성 템플릿
├── knowledge/                # 지식 노트 작성 템플릿
└── persona/                  # 교안·잔디 템플릿

.agent/
├── hooks/product-doc-pipeline.md
└── scripts/product_doc_pipeline.py
```

PARA 버킷의 루트는 아래 넷이다 — 코드블록 안 경로는 옵시디언이 링크로 읽지 않으므로 여기 따로 건다([[decision-020-para-alignment-area-and-personal|KDEV-DEC-020]] D2).

| 버킷 | 루트 | 소속 영역 |
|---|---|---|
| **P** | [[products/README\|products]] | 여름별컴퍼니 |
| **R** | [[resources/README\|resources]] | 개인 |
| **A** | `persona/` | 세 영역의 **귀결** — 공개 표면 |
| **Archive** | [[archive/README\|archive]] | 상태(비어 있음) |

## 기본 진입 흐름

항상 모든 context를 읽지 않는다.

```text
CLAUDE.md
→ agent.md
→ context/index.md
→ 필요한 문서 선택
```

## 읽기 범위 원칙

- [[context/index|context/index]] (이 문서)는 라우터다. 하위 문서를 요약하지 않는다.
- [[kknaks]]는 회사/개인사업자/개인 구분이 필요할 때만 읽는다. **세 영역의 진입점**이다.
- [[policy]]는 문서 민감도, 접근권한, 승인 게이트 관련 판단이 필요할 때만 읽는다.
- [[context/studio/workflow|studio/workflow]]는 개인 프로젝트의 실제 작업을 만들거나 수정할 때만 읽는다.
- [[rules/product-doc-pipeline|product-doc-pipeline]]은 제품 문서를 만들거나 수정할 때만 읽는다.
- [[knowledge-note-pipeline]]은 [[resources/README|resources]]에 노트를 만들거나 수정할 때 읽는다. **제품 결정(`10-decision/`)을 쓸 때도 읽는다** — 근거 개념이 없으면 그 턴에 만들어야 하기 때문이다.
- [[persona-artifacts]]는 `showcase.md`·교안·잔디 산출물을 건드릴 때만 읽는다.
- `templates/product/**`는 새 문서를 만들 때 필요한 템플릿만 읽는다.
- [[products/README|products]]의 개별 제품은 요청 대상이 확정된 뒤에 읽는다.

## context의 역할

`context/`는 작업을 시작하기 위한 단방향 라우터다.

최상위 라우터는 하위 문서의 내용을 복사하지 않는다. 회사 경험 기록은 `company/`에서, 개인사업체와 개인 프로젝트 운영은 `studio/`에서 탐색한다.

## SSOT 규칙

- 하나의 사실은 한 곳에만 둔다.
- 같은 정보를 여러 문서에 복사하지 않는다.
- 다른 문서에서 필요하면 원문을 다시 쓰지 말고 링크하거나 참조한다.
- 현재 상태처럼 자주 바뀌는 정보와, 정체성/프로젝트 경계처럼 잘 바뀌지 않는 정보를 섞지 않는다.
- 상위 index는 하위 내용을 요약하지 않고 위치만 가리킨다.
- 에이전트는 정보를 수정하기 전에 그 정보의 SSOT가 어디인지 먼저 확인한다.
- SSOT가 아직 정해지지 않은 정보는 임의로 새 위치를 만들지 않고, 먼저 구조를 제안한다.

## 작성 원칙

- 이 문서에는 최상위 분기 규칙만 둔다.
- 회사·개인사업자·개인 구분 기준은 [[kknaks]]에 둔다.
- 문서 민감도, 접근권한, 승인 게이트 정책은 [[policy]]에 둔다.
- 회사 경험 기록의 현재 상태는 [[context/company/current|company/current]]에 둔다.
- 회사 제품/프로젝트 경험의 경계는 [[context/company/projects|company/projects]]에 둔다.
- 개인사업체 현재 상태는 [[context/studio/current|studio/current]]에 둔다.
- 개인 프로젝트 작업 흐름은 [[context/studio/workflow|studio/workflow]]에 둔다.
- 새로운 도메인을 추가하기 전에는 기존 `company/`, `studio/` 중 하나에 속하는지 먼저 판단한다.
