# Architecture

리뉴얼 이후 이 레포의 구조를 정하는 문서다. 지금은 **루트 계약**만 있다.

여기 적힌 것은 정해진 것이고, 「미정」에 있는 것은 아직 아무것도 아니다. 미정을 추측으로 메우지 않는다.

## 루트 세 갈래


| 루트               | 담는 것                |
| ---------------- | ------------------- |
| `para/`          | 문서 — 사실과 판단이 사는 곳   |
| `app/`           | 코드 — 그것을 서빙하는 것     |
| `orchestration/` | 자동화 — 그것을 채우고 옮기는 것 |


세 갈래를 가르는 축은 **주제가 아니라 역할**이다. 같은 제품 이야기라도 판단은 `para/`, 그 판단을 화면에 띄우는 코드는 `app/`, 그 문서를 기계가 채우는 잡은 `orchestration/` 이다.

이전 구조는 이 축이 없어서 `persona/`·`resources/`·`products/`(문서)와 `app/`(코드)과 `.agent/`·`.github/`(자동화)가 같은 층에 평평하게 놓였고, **한 문서를 사람과 자동화가 같이 쓰는데 그게 구조에 드러나지 않았다**(CLAUDE.md 1번).

## 아직 정하지 않은 것

루트를 셋으로 나눈 것 외에는 정해진 게 없다. 각각은 CLAUDE.md 「이번 리뉴얼에서 정할 것」에 대응한다.


| 미정                                                                                         | 대응     |
| ------------------------------------------------------------------------------------------ | ------ |
| `para/` 내부 구조 — PARA 네 버킷을 그대로 쓸지, 이전 `persona`·`resources`·`products`·`context` 를 어떻게 접을지 | 정할 것 6 |
| `app/` 내부 계층·명명·경계                                                                         | 정할 것 4 |
| `orchestration/` 이 `.agent/`·`.github/`·워커·잡 중 무엇까지 흡수하는지                                  | 정할 것 3 |
| 각 루트 안에서 사람 소유와 자동화 소유가 어디서 갈리는지                                                           | 정할 것 1 |
| 어떤 사실이 문서 원천이고 어떤 사실이 DB 원천인지                                                              | 정할 것 2 |
| 잔디와 회사 경험 기록의 관계                                                                           | 정할 것 5 |


## 규칙

- 루트는 셋이다. 넷째를 만들기 전에 이 문서를 먼저 고친다.
- `_archive/` 는 루트가 아니라 **이전 레포 전체의 동결본**이다. 읽기 전용이고 새 구조의 일부가 아니다.
- 새 구조에 필요한 것은 `_archive/` 에서 끌어올린다. 올릴 때 위 축(문서·코드·자동화)에 맞는 루트로 간다.


```
app/back/
├── [main.py](http://main.py)                  # 앱 팩토리 · lifespan · 라우터 등록만. 로직 없음
├── [config.py](http://config.py)                # pydantic-settings — env 로드
├── pyproject.toml           # uv (레거시와 동일)
├── Dockerfile
├── docker-compose.yml       # 로컬 dev — postgres 포함
├── alembic/                 # 마이그레이션 (스키마 정본은 [erd.md](http://erd.md))
│
├── api/                     # ── 1층 · router — HTTP 만 안다
│   ├── [deps.py](http://deps.py)              #    get_session · get_current_user
│   ├── auth_[router.py](http://router.py)       #    POST /auth/login · logout · me
│   └── profile_[router.py](http://router.py)    #    공개 GET + 어드민 PUT
│
├── service/                 # ── 2층 · 비즈니스 로직 — 클래스
│   ├── auth_[service.py](http://service.py)      #    비밀번호 검증 · 토큰 발급
│   └── profile_[service.py](http://service.py)
│
├── repository/              # ── 3층 · DB 접근 — 클래스, AsyncSession 만 안다
│   ├── base_[repo.py](http://repo.py)         #    제네릭 공통 CRUD (get·create·update·delete)
│   └── profile_[repo.py](http://repo.py)
│
├── models/                  # SQLAlchemy ORM — [erd.md](http://erd.md) 표당 파일 하나
│   ├── [base.py](http://base.py)              #    DeclarativeBase · created_at/updated_at mixin
│   ├── [user.py](http://user.py)
│   └── [profile.py](http://profile.py)
│
├── schemas/                 # ── DTO — 계층 간 이동 + front↔back 계약
│   ├── [auth.py](http://auth.py)              #    LoginRequest · UserMe
│   └── [profile.py](http://profile.py)           #    ProfileRead · ProfileUpdate
│
├── core/                    # 인프라 — 계층 밖\
│   ├── [db.py](http://db.py)                #    create_async_engine · async_sessionmaker
│   ├── [security.py](http://security.py)          #    bcrypt 해시 · JWT 발급/검증
│   └── [exceptions.py](http://exceptions.py)        #    도메인 예외 → HTTP 매핑
│
├── utils/                   # 순수 함수 집합 — 상태 없음
└── tests/
```
```
├── 수집함
│   ├── 자료 캡처        케이스 1 모달 · queue 목록 (처리중 폴링)
│   └── 승인 대기        게이트 1·2 + problem 게이트 — pending 전부 여기
├── 프로필
│   ├── 기본 정보        profile (히어로·about·연락처)
│   └── 사이트 문구      site_config
├── 커리어
│   ├── 회사             company
│   ├── 역할             career
│   ├── 해결한 문제      problem (수동 CRUD — 게이트 승인분은 수집함에서 옴)
│   └── 교육             education
├── 프로젝트
│   ├── 회사 제품        product (visible 토글 — 회사 showcase 3건 검토가 여기)
│   └── 개인 프로젝트    project (등록 시 디렉토리 검증)
├── 리소스
│   ├── 노트             note
│   ├── 콘텐츠           content
│   └── 알고리즘         algorithm (today 토글 · 메타만)
└── 수집 설정
    ├── 레포             repo (enabled · last_error 확인)
    └── 커밋             commit (읽기 전용 — summary 확인용)
```