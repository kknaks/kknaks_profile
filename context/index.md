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
├── company/                  # 회사 코드 작업이 아니라 이력서/포트폴리오용 경험 기록
│   ├── current.md            # 현재 정리 중인 회사 경험, 챌린지, 해결방안, 성과
│   ├── projects.md           # 회사 제품/프로젝트 경험의 목록과 경계
│   └── org.md                # 회사 조직도, 사람, 역할, 협업 관계
└── studio/                   # 여름별컴퍼니 개인사업자 프로젝트 운영
    ├── current.md            # 현재 우선순위, 진행 중 작업, blocker
    ├── projects.md           # 개인 제품/프로젝트 목록과 경계
    ├── org.md                # 여름별컴퍼니 조직 구조와 역할
    └── workflow.md           # 작업 종류와 공통 작업 흐름
```

## 연결 계층

```text
products/
├── README.md                 # 여름별컴퍼니 제품별 SSOT 진입점
└── <product>/README.md       # 특정 제품의 문서 map

rules/
└── product-doc-pipeline.md   # 제품 문서 파이프라인 운영 규칙

templates/
└── product/                  # 제품 문서 작성 템플릿

.agent/
├── hooks/product-doc-pipeline.md
└── scripts/product_doc_pipeline.py
```

## 기본 진입 흐름

항상 모든 context를 읽지 않는다.

```text
CLAUDE.md
→ agent.md
→ context/index.md
→ 필요한 문서 선택
```

## 읽기 범위 원칙

- `context/index.md`는 라우터다. 하위 문서를 요약하지 않는다.
- `context/kknaks.md`는 회사/개인사업자 구분이 필요할 때만 읽는다.
- `context/studio/workflow.md`는 개인 프로젝트의 실제 작업을 만들거나 수정할 때만 읽는다.
- `rules/product-doc-pipeline.md`는 제품 문서를 만들거나 수정할 때만 읽는다.
- `templates/product/**`는 새 문서를 만들 때 필요한 템플릿만 읽는다.
- `products/<product>/`는 요청 대상 제품이 확정된 뒤에 읽는다.

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
- 회사와 개인사업자 구분 기준은 `context/kknaks.md`에 둔다.
- 회사 경험 기록의 현재 상태는 `context/company/current.md`에 둔다.
- 회사 제품/프로젝트 경험의 경계는 `context/company/projects.md`에 둔다.
- 개인사업체 현재 상태는 `context/studio/current.md`에 둔다.
- 개인 프로젝트 목록과 경계는 `context/studio/projects.md`에 둔다.
- 개인 프로젝트 작업 흐름은 `context/studio/workflow.md`에 둔다.
- 새로운 도메인을 추가하기 전에는 기존 `company/`, `studio/` 중 하나에 속하는지 먼저 판단한다.
