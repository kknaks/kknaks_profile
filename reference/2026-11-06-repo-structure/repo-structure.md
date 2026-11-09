# 이 레포의 구조

이 레포는 나에 관한 기록과 지식, 프로젝트 문서, 이를 보여 주는 앱, 작업 자동화를 함께 관리한다. 중심은 `para/`의 문서이고, `app/`은 이를 서비스하며, `orchestration/`은 워커 작업을 운영한다.

이 문서는 **2026-11-06 현재 파일 구조를 설명하는 안내서**다. 세부 규칙은 아래에 연결한 원문이 갖는다.

## 전체 지도

```text
obsidian/
├── agents.md          에이전트 진입점 — 작업에 맞는 규약으로 안내
├── CLAUDE.md          리뉴얼 배경과 결정 기록
├── para/              나·지식·프로젝트·자료를 담는 문서
│   ├── areas/         지속적으로 쌓는 자기 기록과 개념
│   ├── projects/      진행 중인 프로젝트
│   ├── resources/     출처별 자료와 기록
│   └── archive/       현역에서 내려온 프로젝트
├── app/               문서와 데이터를 서비스하는 코드
│   ├── back/          FastAPI 백엔드
│   ├── front/         Next.js 프론트엔드
│   ├── mcp/           채용담당자 채팅용 MCP 서버
│   └── ontology-agent/ 온톨로지 데모 앱
├── orchestration/     워커 설정·발주·검증·작업 기록
├── templates/         문서와 발주 양식
├── rules/             문서 정합 검사와 Git 훅
├── .agents/skills/     이 레포에서 사용하는 스킬
├── inbox/             들어온 입력이 놓이는 자리
├── reference/         작업별 참고 자료·시안·프로토타입
└── resume/            지원 건별 이력서 자료
```

## 문서의 중심: para/

문서를 어디에 둘지는 [[para/para|para 분류 기준]]에서 시작한다.

| 위치 | 담는 것 | 읽을 문서 |
| --- | --- | --- |
| `para/areas/` | 계속 갱신하는 자기 기록과 재사용 가능한 개념 | [[para/areas/area|areas 규약]] |
| `para/projects/` | 현재 진행 중인 일의 판단과 기록 | [[para/projects/project|projects 규약]] |
| `para/resources/` | 자료 원문·학습 필기·세션 노트 등 개념의 출처 | [[para/resources/resource|resources 규약]] |
| `para/archive/` | 완료했거나 손을 뗀 프로젝트 | [[para/archive/archive|archive 안내]] |

### areas: 나와 내가 아는 것

`personal/`은 회사와 여름별컴퍼니에서의 나를 담는다. 이 중 DB에서 재생성되는 문서는 수동 편집 대상이 아니다. 정확한 범위는 areas 규약이 정한다.

`concept/`은 배운 것을 다른 상황에서도 꺼내 쓸 수 있도록 정리한 개념 노트다. `cs`, `back`, `db`, `front`, `ai`, `infra`, `design`, `pm`, `qa`의 아홉 영역으로 나눈다. 출처는 `up:`으로 연결하고, 개념 목록은 areas 규약의 맵에서 찾는다.

### projects: 지금 하는 일

`company/`는 회사 프로젝트에서의 경험을 남긴다. 기획과 스펙의 원천이 회사 레포에 있으면 여기로 복사하지 않는다.

`summer-star/`는 여름별컴퍼니의 제품 문서를 담는다. 아이디어가 결정, 기능 계약, 구현 작업으로 구체화된다.

```text
00-baseline → 10-decision → 20-spec → 30-work
날것 입력      결정           기능 계약     구현 작업
```

공유 구조는 `40-architecture/`, 릴리즈 결과는 `60-release/`, 반복 절차는 `70-runbook/`에 둔다. 필요한 단계만 만든다. 제품 전체 지도는 `README.md`, 문서 변경 이력은 `log.md`, 작업 회고는 `log/`가 맡는다.

### resources: 지식의 출처

`note/`, `youtube/`, `algorithms/`, `docs/`, `book/`, `article/`, `blog/`, `session/`처럼 출처와 유입 방식으로 나눈다. 자료에서 얻은 지식은 `areas/concept/`에 반영하고, 개념에서 출처를 연결한다.

### archive: 현역이 아닌 일

프로젝트가 현역에서 내려오면 `para/archive/`로 옮긴다. `company/`와 `summer-star/` 구분을 유지한다. 제품 내부의 `_archive/`는 버전별 문서 동결본이므로 역할이 다르다.

## 코드: app/

| 위치 | 역할 |
| --- | --- |
| `app/back/` | API와 도메인 로직, DB 접근, 마이그레이션과 자동화 작업 |
| `app/front/` | 사용자 화면과 프론트엔드 구성 요소 |
| `app/mcp/` | 백엔드의 채팅 도구 API를 MCP 도구로 제공 |
| `app/ontology-agent/` | 데이터 계층 구축과 온톨로지 탐색·질의 데모. [[app/ontology-agent/README|앱 안내]] |

백엔드는 API → service → repository로 책임을 나눈다. 제품의 장기 구조와 판단 근거는 해당 프로젝트 문서에서 찾는다. 이 레포 자체와 포트폴리오 사이트의 문서는 [[para/projects/summer-star/kknaks-dev/README|kknaks-dev 프로젝트]]에 있다.

## 자동화: orchestration/

작업 운영 절차는 [[orchestration/runbook|코디네이터 런북]]이 갖는다.

| 위치 | 역할 |
| --- | --- |
| `config/` | 에이전트 실행 명령과 프로젝트별 레포·워커·검증 설정 |
| `roles/` | 프로젝트별 워커 역할과 규약 |
| `scripts/` | 작업 생성과 종료·아카이브 등의 실행 스크립트 |
| `work/<slug>/` | 진행 중 작업의 브리프와 재개 노트 |
| `work/_archive/` | 종료한 작업의 기록 |

재개 시점과 남은 일은 작업 폴더의 `_RESUME.md`에서 찾는다. 종료 회고는 설정에 따라 제품의 `log/` 또는 작업 아카이브에 남는다.

## 양식·검사·보조 디렉토리

`templates/`는 `areas/`, `projects/`, `resources/`, `orchestration/`의 양식을 모은다. 규칙은 각 규약 문서에서, 작성 틀은 이곳에서 찾는다.

`rules/`는 기계로 확인할 수 있는 정합을 검사한다. 개념 파일과 개념 맵의 대응을 확인하는 검사기와 pre-commit 훅이 있으며, 사용법은 [[rules/rules|검사 규칙]]에 있다.

`.agents/skills/`에는 채용공고 분석과 발표 원본 복원 등 이 레포의 작업용 스킬이 있다.

`reference/`에는 현재 작업별 참고 자료, 인터뷰 원본, 화면 시안, 프로토타입 코드 등이 함께 있다. `para/resources/`의 출처별 문서 체계와는 별도로 존재한다. `inbox/`와 `resume/`도 현재 루트에 있으며, 이들의 존재만으로 PARA 분류 기준이 달라지는 것은 아니다.

## 처음 읽는 순서

1. [[agents|에이전트 진입점]]에서 작업 종류에 맞는 규약을 찾는다.
2. 문서를 다루면 [[para/para|para 분류 기준]]과 해당 버킷 규약을 읽는다.
3. 제품 작업이면 제품의 `README.md`에서 현재 문서와 코드를 찾는다.
4. 워커 작업이면 [[orchestration/runbook|런북]]과 해당 작업의 `_RESUME.md`를 읽는다.
5. 구조의 배경이 필요하면 [[CLAUDE|리뉴얼 기록]]을 읽는다.

## 기존 안내와 현재 파일의 차이

기존 진입 문서에는 `app/`이 비어 있다는 설명이 남아 있지만, 현재는 위 네 코드 디렉토리가 존재한다. `para/archive/archive.md`도 현재 존재한다.

`architecture.md`는 현재 루트에 없다. [[CLAUDE|리뉴얼 기록]]에서도 미작성 문서로 명시한다. 따라서 이 안내서는 해당 문서를 링크 대상으로 삼지 않는다. 루트 `_archive/` 역시 현재 체크아웃에는 없으며, 각 하위 디렉토리의 `_archive/`와 구분해서 읽어야 한다.
