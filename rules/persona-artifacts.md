# Persona Artifacts

`persona/` 아래 산출물의 작성 규칙. `rules/product-doc-pipeline.md`(제품 문서)·`rules/knowledge-note-pipeline.md`(지식 노트)와 나란한 세 번째 계열이다.

**이 계열은 그래프 밖이다.** 4층 모델(`source → concept → execution`) 대상이 아니고, 발행 시 그래프 검증(L1~L6)도 받지 않는다. 그래서 `up:`·`aliases` 같은 계보 필드가 없다.

> 종전에는 이 내용이 `agent.md` 에 있었다. 진입점이 라우터가 아니라 규칙 문서가 되면서
> `context/index.md` 의 「읽기 범위 원칙」과 역할이 겹쳤고, 「한 곳 원칙」을 진입점이
> 스스로 어기고 있었다. 계열별 규칙은 각자의 `rules/` 문서가 갖는다.

| 만들 것 | 템플릿 | 경로 |
|---|---|---|
| 프로젝트 카드 | `templates/product/showcase.md` | `products/{제품}/showcase.md` |
| 교안 | `templates/persona/content.md` | `persona/contents/**` |
| 잔디 — 그날 | `templates/persona/daily.md` | `persona/daily/{YYYY-MM-DD}.md` |
| 잔디 — 누적 | `templates/persona/career.md` | `persona/career/{stem}.md` |

## 프로젝트 카드 (`showcase.md`)

제품 문서와 같은 폴더에 있지만 **성격이 반대다** — 제품 문서는 내부 결정을 쌓는 곳이고, 카드는 **공개 사이트와 포트폴리오 PDF 에 나가는 한 장**이다. 그래서 그래프 노드가 아니며(`persona_loader` 가 제외한다) 4층 모델 대상도 아니다.

관리 화면의 제품 등록이 이 파일을 읽어 카드를 렌더한다 — **형식을 고치려면 여기만 고친다.**

**`category` 만 이 템플릿이 아니라 `persona/_meta.yaml` 이 소유한다.** 목록 밖의 값이 들어가면 파일 하나가 거부되는 게 아니라 **persona 로드 전체가 실패하고 사이트가 옛 데이터를 계속 서빙한다.**

## 교안 (`persona/contents/**`)

승인 게이트의 `derived` 스테이지와 `content_enrich` 잡이 **둘 다 이 파일을 읽는다** — 형식을 고치려면 여기만 고친다.

## 잔디 산출물 (`persona/daily/**` · `persona/career/**`)

잔디 파이프라인의 `daily` 게이트 스테이지가 두 템플릿을 읽어 프롬프트를 만든다 — 형식을 고치려면 여기만 고친다.

**두 문서의 성격이 반대다.**

| | 사이트 노출 | 쓰임 |
|---|---|---|
| `daily` | **안 된다** (잔디가 쓰는 것은 `counts` 와 `summary[]` 뿐) | 다음 단계의 **입력** |
| `career` | **본문이 경력 페이지에 그대로 렌더된다** | 최종 산출 |

그래서 daily 는 재료로 남기고 career 는 압축해 다시 쓴다.

## 그래프 밖 디렉토리

지식층도 제품 문서도 아닌 것 둘이 레포 루트에 있다. **주인이 있으니 지우지 않는다.**

| 디렉토리 | 무엇 | 주인 |
|---|---|---|
| `downloads/` | **운영 자산.** 백엔드가 `/download/*` 로 정적 서빙하고 DeskDeck 랜딩이 링크한다. **지우면 다운로드가 죽는다** | mac-remote RB-001 |
| `persona/assets/` | 프로필 이미지 등 | persona |

제품별 작업 보고는 `products/{제품}/30-work/reports/` 에 둔다 — 루트에 두면 어느 제품 것인지 문서로 알 수 없다.
