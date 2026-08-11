# Products

여름별컴퍼니에서 운영하거나 출시하려는 제품별 **문서** 공간이다. **P(Projects)** 버킷이고 [[context/studio/current|여름별컴퍼니 영역]]에 속한다([[decision-020-para-alignment-area-and-personal|KDEV-DEC-020]] D2).

규칙: `rules/product-doc-pipeline.md`

## 제품 원장은 DB다 — 여기 목록을 두지 않는다

**어떤 제품이 있는지의 원장은 `tracked_repos` 테이블**이다([[decision-014-commit-source-and-repo-registry|KDEV-DEC-014]] D1). 관리 화면에서 등록·비활성한다.

| 무엇 | 어디 |
|---|---|
| 제품·레포 목록, 추적 여부 | `tracked_repos` — `slug` · `type` · `detail` · `product_slug` · `enabled` |
| 공개 카드 (사이트·PDF) | `products/{제품}/showcase.md` |
| 제품 문서 | `products/{제품}/` 아래 스테이지 |
| 제품 하나의 설명·현재 상태 | `products/{제품}/README.md` |

종전에는 이 파일에 목록 표를 두고 제품 등록이 행을 추가했다([[decision-017-product-registry-and-admin-scaffold|KDEV-DEC-017]] D15). **같은 사실을 DB 와 파일 두 곳에 두는 것**이라 지웠다 — 어느 쪽이 맞는지 정할 수 없고, 한쪽만 고쳐지는 날 조용히 어긋난다.

**회사 제품(`mediness`·`linky`·`nexus`·`centurion-*`)은 여기 없다.** 회사 레포는 문서 트리도 공개 카드도 갖지 않고 **잔디 레지스트리에만 등록된다**(DEC-017 D9).

## 디렉토리

```text
products/{제품}/
├── README.md      제품 map — 현재 상태·문서 맵·코드 레포 위치
├── log.md         변경 이력
├── showcase.md    공개 카드 (optional)
├── 00-baseline/   날것 입력
├── 10-decision/   결정 — 근거 개념을 `up:` 으로 갖는다
├── 20-spec/       기능 계약
├── 30-work/       작업 지시
└── 40·60·70/      architecture · release · runbook (optional)
```

제품 하나를 보려면 그 폴더의 `README.md` 부터 읽는다.
