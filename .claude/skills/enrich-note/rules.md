# enrich-note 룰

## 1. stack 추론

### 정의
**기술 스택만** — 라이브러리 / 프레임워크 / 언어 / DB / 인프라 / 도구.

### 포함 (stack)
- 언어: `Java`, `Python`, `TypeScript`, `JavaScript`, `Kotlin`, `Go`, `Rust` 등
- 프레임워크: `Spring Boot`, `FastAPI`, `Django`, `Next.js`, `React`, `Vue`, `Express` 등
- DB: `PostgreSQL`, `MySQL`, `MongoDB`, `Redis`, `pgvector` 등
- 인프라: `Docker`, `Kubernetes`, `AWS`, `NCP`, `GitHub Actions`, `nginx` 등
- 도구: `Git`, `JPA`, `Hibernate`, `pytest`, `Jest`, `gRPC` 등

### 제외 (tags 영역)
- 개념 / 패턴: `MVC`, `REST`, `OOP`, `polling`, `SSE`, `웹소켓` 등
- 도메인: `채팅`, `결제`, `주문`, `회원가입` 등
- 학습 메타: `독학`, `부트캠프`, `회고` 등

→ 위 항목들은 `tags`에 박힐 수 있어도 `stack` 아님. 추론하지 말 것.

### 형식

```yaml
stack: [Java, Spring Boot, JPA]
```

- list of string. 빈 list 가능 (`stack: []`).
- 표기 일관: `Spring Boot` (공백 포함, PascalCase 단어), `JavaScript` (한 단어), `PostgreSQL` (제품명 그대로).
- 본문에 명확히 등장하지 않으면 추측하지 말고 빈 list.

## 2. links 추론

### 정의
**같은 group(폴더) 안의 의미적으로 강하게 연결된 노트들의 slug**.

### 포함 (links)
- 본문에 다른 노트의 핵심 키워드 / 주제가 직접 언급
- 시리즈 패턴: `chapter1` → `chapter2` (시간순 인접 + 동일 시리즈)
- 같은 학습 흐름의 인접 노트 (예: `Day05` → `Day06`, `Day07`)
- 공통 라이브러리 / 도구를 함께 다루는 노트

### 제외
- 같은 group 안이라는 이유만으로는 안 박음 (의미 약함)
- 같은 카테고리 키워드만 공유하면 안 박음 (`Java` 가 둘 다 있다고 link X)
- 약한 연결 (모호) — 빈 list 가 낫다

### 갯수
- 강한 연결만 — **최대 5개**, 보통 2-3개. 0개도 OK.

### 형식

```yaml
links: [2025-03-14-spring-intro, 2025-03-16-spring-jpa]
```

- slug = 파일명에서 `.md` 제외 (예: `2025-03-15-spring-mvc.md` → `2025-03-15-spring-mvc`).
- 대상 파일 **실제 존재 확인** (Glob `persona/notes/<group>/<slug>.md`). 없으면 박지 말 것.
- 자기 자신 slug 박지 말 것 (self-link).

## 3. frontmatter 보존

### 절대 안 건드림
- `title` / `date` / `tags` — 사용자 명시 영역. 추론 결과로 덮어쓰지 말 것.
- body — markdown 본문 변경 X.

### 추가 / 갱신
- `stack: [...]` — 기존 비어있으면 추론 결과로 채움. 기존 있으면 유지 (사용자 명시 우선).
- `links: [...]` — 동일.

### 결정 기준 (기존 stack/links 박혀있을 때)
| 기존 상태 | 동작 |
|---|---|
| `stack: []` (빈 list) | 추론 결과로 채움 |
| `stack: [...]` (값 있음) | 유지 (사용자 명시) |
| `stack` 키 자체 없음 | 추론 결과로 추가 |

links 도 동일 패턴.

## 4. 본문 빈약 판정

### Skip 조건
- body 가 **50자 이하** (heading + 짧은 한 줄만)
- body 가 비어있음 (`#` 만 있고 본문 X)
- 의미 추론 어려움 (TODO 만 박혀있음)

### Skip 동작
- frontmatter 안 건드림
- `stack: []` / `links: []` 빈 list 라도 추가하지 말 것 (사용자가 차차 박음)
- 짧은 메시지 출력: `○ <path> — body 빈약, skip`

## 5. _map.md 갱신

### 언제
SKILL 동작 마지막 단계. 단일 파일 enrich 후 매번 갱신.

### 어떻게
```bash
bash "${CLAUDE_PROJECT_DIR}/.claude/skills/enrich-note/scripts/build-map.sh"
```

내부적으로 `back/.venv/bin/python scripts/build_persona_map.py` 호출.

### 일괄 처리 시
외부 loop 가 N 파일 호출하면 N 번 갱신 (느림). 일괄 시 마지막에만 갱신하는 fast path 옵션:
- 환경 변수 `ENRICH_SKIP_MAP=1` 설정 시 _map.md 갱신 skip
- loop 끝나면 외부에서 직접 `build-map.sh` 1번

## 6. 안전 / 보안

- frontmatter Edit 시 `Edit` 도구로 정확한 영역만 교체. `Write` 로 통째 덮어쓰지 말 것 (body 손실 위험).
- 외부 입력 (파일 경로) 은 Read 시 절대 경로 사용. shell injection 방지.
- LLM 추론 결과 (stack/links) 는 형식 검증 후 박음:
  - stack 원소: 영문/숫자/공백/하이픈/점 만 허용 (한글 X)
  - links 원소: kebab-case slug (`^[a-z0-9._\-]+$`)

검증 실패 시 해당 원소만 drop, 나머지는 박음.
