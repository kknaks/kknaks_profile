---
type: decision
id: KDEV-DEC-017
title: "제품 레지스트리 조인 + 관리자 제품 등록(결정적 스캐폴딩)"
status: proposed
product: kknaks-dev
created_at: 2026-08-03
updated_at: 2026-08-03
tags:
  - product/kknaks-dev
  - doc/decision
  - status/proposed
links:
  baselines:
    - "[[baseline-005-product-project-career-link|KDEV-BL-005]]"
  decisions:
    - "[[decision-014-commit-source-and-repo-registry|KDEV-DEC-014]]"
    - "[[decision-012-draft-storage-and-publish-boundary|KDEV-DEC-012]]"
    - "[[decision-009-app-db-foundation-and-admin-auth|KDEV-DEC-009]]"
  specs:
    - "[[spec-014-product-registry-and-admin|KDEV-SPEC-014]]"
  works:
    - "[[work-018-product-registry-admin|KDEV-WORK-018]]"
  releases: []
  related:
    - "[[baseline-004-commit-pipeline-and-career|KDEV-BL-004]]"
    - "[[work-017-grass-commit-pipeline|KDEV-WORK-017]]"
up:
  - foreign-key
  - sql-join
---

# 제품 레지스트리 조인 + 관리자 제품 등록(결정적 스캐폴딩) (ADR-017)

레포와 제품을 잇는 키를 **`tracked_repos.product_slug` 컬럼 하나**로 만들고, 관리자 화면에 **LLM 없는 결정적 제품 등록**을 붙인다. 파일 본문의 SoT 는 그대로 md 이고, 화면은 **부트스트랩**만 한다.

> [[baseline-005-product-project-career-link|KDEV-BL-005]] 의 P1. 잔디 산출물에 product 를 더하는 P2 는 후속 decision 이 다룬다.

## Context

- 관련 baseline: [[baseline-005-product-project-career-link|KDEV-BL-005]]
- **조인 키가 없다.** 제품(`products/{slug}/`)·프로젝트(`showcase.md`)·커리어(`persona/career/`)가 같은 커밋에서 나오는데 셋을 잇는 것이 **디렉토리명 관례**뿐이고, `kknaks-dev`/`kknaks-profile` 에서 이미 깨져 있다.
- **career 축은 이미 데이터가 목적지를 만든다.** `tracked_repos.detail` → `career_attribution()`(`collect_git.py:140`) → `career_map` → `career_targets()`(`daily.py:109`). product 축만 그 대칭이 비어 있다.
- **등록 오타가 하루 숨는다.** `sync_repo`/`sync_all` 을 부르는 곳은 `collect_git.py:92` 하나뿐이다. [[decision-014-commit-source-and-repo-registry|KDEV-DEC-014]] D2 가 자동 시드를 택한 이유가 *"slug 오타가 조용히 '추적 안 됨' 이 되고 로그에도 안 남는다"* 였는데, **손입력 화면이 그 경로를 되살린다.**
- **파일 쓰기는 발행부 독점이 아니다.** `ALLOWED_PREFIXES`(`apply/plan.py:25`)는 **게이트 발행 경로**만 검사한다. `algorithms/main.py`·`content_enrich.py`·`pdf_generate.py` 셋은 이미 `commit_and_push_with_retry` 로 직접 쓰고 push 한다. 다만 그 함수는 **롤백이 없다** — push 실패 시 남은 로컬 커밋을 다음 `reset --hard origin/main` 이 조용히 지운다.
- **로더가 fail-fast 다.** `showcase.md` 의 `category` 가 `_meta.yaml` 의 7종을 벗어나면 `PersonaError` 가 올라와 **persona 로드 전체가 실패**하고, `reload_data` 가 기존 데이터를 유지해 사이트는 옛 데이터를 계속 서빙한다. 파일 하나의 문제로 끝나지 않는다.
- **템플릿 트리에 샘플 문서가 8개 있다.** `templates/product/` 23개 파일 중 `baseline.md`(`id: BASE-001`)·`decision.md`·`spec.md`·`work.md`·`work-release.md`·`release.md`·`runbook.md`·`domain.md` 가 frontmatter 를 갖는다. `_build_graph_nodes` 는 `products/**/*.md` 중 `type` 이 있으면 노드로 잡는다.
- **필수 stage README 는 4개다.** `product_doc_pipeline.py:33 REQUIRED_STAGE_READMES` = `00-baseline`·`10-decision`·`20-spec`·`30-work`. `40-architecture`·`60-release`·`70-runbook` 은 optional.
- **`showcase.md` 템플릿이 없다.** `templates/product/` 에 없고, 형식을 정의한 문서도 없다.
- **`id: P-NN` 채번 주체가 없다.** 현재 `P-02`~`P-14` 13개(`P-01` 결번).
- 회사 5개(`centurion-charty`·`centurion-mso`·`linky`·`mediness`·`nexus`) 디렉토리는 **`showcase.md` 하나뿐**이고 전부 `visible:false` + `(TBD)` 다.

## 근거 개념

이 결정이 기대는 개념. 상세는 concept 노트가 갖는다.

- [[foreign-key]] — 레포와 제품을 잇는 키를 **`tracked_repos.product_slug` 컬럼 하나**로 뒀다. 조인 키를 어디에 두느냐가 이 결정의 D1 전부다
- [[sql-join]] — 그 컬럼으로 레포 축(company)과 제품 축(studio)을 **한 테이블에서 함께 끌어온다**

## Options

### 관계 모양

| Option | Description | Pros | Cons |
|---|---|---|---|
| A | `showcase` 본문까지 DB (`project_detail` 테이블) | 화면에서 전부 편집 | **로컬 md 작업을 못 한다.** 그래프·Obsidian 밖으로 나간다 |
| B | `showcase.md` 에 `product_slug` 필드 추가 | DB 무변경 | 조인이 파일에 있어 잡이 파일을 다시 읽는다. DEC-014 D1 되감기 |
| C | `tracked_repos` 에 showcase 경로 저장 | 단순 | 경로는 `slug` 에서 유도된다. 드리프트 원천 추가, 카드 없는 제품은 null |
| **D** | **`tracked_repos.product_slug` 컬럼 1개** | 본문이 파일에 남아 DB 가 담을 것이 조인뿐. `detail`(career)과 대칭 | 제품:레포 1:1 을 전제한다 |

### 제품 등록 방식

| Option | Description | Pros | Cons |
|---|---|---|---|
| A | 사람이 폴더를 파고 화면은 연결만 | 추가 코드 0 | 매번 손. 필수 파일 6개를 빠뜨릴 수 있다 |
| B | AI 에이전트가 스캐폴딩 | 유연 | 워커·예산·비동기 수확이 붙는다. **결정적인 일에 비결정적 수단** |
| **C** | **화면 버튼 + 결정적 복사** | LLM·워커 불필요. 검증을 코드가 보장 | 넷째 쓰기 경로가 생긴다 |

### 스캐폴드 범위

| Option | Description | Pros | Cons |
|---|---|---|---|
| A | `templates/product/` 통째 복사 | 단순 | **샘플 문서 8개가 그래프 노드가 된다.** 제품 둘이면 stem `baseline` 중복 → L2 ERROR → **부팅 차단** |
| **B** | **README 4 + product README + `log.md` = 6 파일** | 검증 통과 최소 집합. 빈 껍데기를 안 만든다 | `40`/`60`/`70` 은 나중에 손으로 |
| C | B + `40-architecture` | 자주 쓴다 | optional 이라 안 쓰는 제품에 빈 트리가 남는다 |

## Decision

### D1. 조인은 `tracked_repos.product_slug` 컬럼 하나다

```text
tracked_repos
  slug           "owner/name"        unique     ← 레포
  type           company | studio
  detail         career 파일 stem               ← company 축 (기존)
  product_slug   products/ 디렉토리명            ← studio 축 (신설)
```

`detail` 이 company 를 career 로 보내듯 `product_slug` 가 레포를 제품으로 보낸다. **별도 `projects` 테이블을 만들지 않는다** — 본문이 md 에 남아 담을 것이 없다.

`product_slug` 는 **company 도 가질 수 있다.** `detail` 처럼 CHECK 로 type 에 묶지 않는다. 회사 레포가 제품 문서를 갖는 경우가 정당하기 때문이다.

### D2. `kknaks-profile` 을 `kknaks-dev` 로 합친다

D1 이 제품:레포 1:1 을 전제하는데, 지금 `kknaks/kknaks_profile` 하나에 제품이 둘이라 컬럼으로 표현할 수 없다.

```text
products/kknaks-profile/showcase.md  →  products/kknaks-dev/showcase.md
products/kknaks-profile/             →  삭제 (파일 하나뿐이었다)
```

합치는 쪽을 택한 결정적 이유는 **D5 가 showcase 를 제품 폴더 안에서 생성하기 때문**이다. 새 제품은 문서와 카드가 한 폴더에 생기는데 기존 하나만 두 폴더로 남으면 그것이 영구 예외가 된다.

- `_load_products_showcase()` 는 `products/*/showcase.md` 를 글롭하므로 **경로만 바뀌고 로드는 그대로**다. `id: P-02` 유지.
- showcase 는 그래프 노드가 아니라(`persona_loader.py:238`) 링크 영향이 없다. 레포 전체 검색 결과 FE·백엔드·문서 어디에도 `products/kknaks-profile` 경로 참조가 없다.
- `kknaks-dev` 는 stage 디렉토리가 있으므로 showcase-only 면제 대상이 아니게 되지만, 필수 README 4개를 이미 갖고 있어 검증에 영향이 없다.

### D3. 스캐폴드는 6 파일이다 — 샘플 문서를 복사하지 않는다

```text
products/{slug}/README.md            templates/product/README.md
products/{slug}/log.md               templates/product/log.md
products/{slug}/00-baseline/README.md
products/{slug}/10-decision/README.md
products/{slug}/20-spec/README.md
products/{slug}/30-work/README.md
```

**`baseline.md`·`decision.md`·`spec.md`·`work.md`·`work-release.md`·`release.md`·`runbook.md`·`domain.md` 는 복사하지 않는다.** 이것들은 frontmatter(`type`·`id`)를 갖고 있어 `products/` 아래로 들어가는 순간 그래프 노드가 된다. 제품을 둘 스캐폴드하면 stem `baseline` 이 둘이 되어 **L2 중복 ERROR** 가 나고, WORK-007 이 enforce 를 켜 뒀으므로 `load_persona` 가 raise 해 **백엔드가 부팅되지 않는다.**

`40-architecture`·`60-release`·`70-runbook` 은 optional 이라 만들지 않는다. 필요한 제품에서 손으로 추가한다.

### D4. 등록 화면은 결정적이다 — LLM 을 타지 않는다

```text
[+ 새 제품]
 ① type          company | studio          (company 면 detail 필수 — 기존 CHECK)
 ② slug          studio 일 때만 → D3 스캐폴드
 ③ repo          owner/name → tracked_repos 행 + 백그라운드 sync_repo
 ④ showcase      title·summary·category▾·stack·status▾ → D5 템플릿 렌더
 → 사전 검증 → 커밋 1개 → push
```

전 단계가 복사·치환·검증이다. 워커·예산·비동기 수확이 필요 없고, **백그라운드로 도는 것은 클론 하나뿐**이다.

`category` 는 **자유입력이 아니라 `_meta.yaml` 의 7종 드롭다운**이다(`web`·`frontend`·`backend`·`mobile`·`ai`·`cli`·`bot`). 벗어난 값 하나가 사이트 전체를 옛 데이터에 묶는다.

### D5. `templates/product/showcase.md` 를 신설하고 그것이 형식 SoT 다

지금 showcase 형식을 정의한 문서가 없고, 로더의 `REQUIRED_FIELDS["project"]` 가 사실상 유일한 계약이다. WORK-017 P1 이 `templates/persona/daily.md`·`career.md` 를 만든 것과 같은 이유로 만든다 — **형식을 코드나 프롬프트에 적으면 SoT 가 둘이 된다.**

템플릿이 담을 것: 로더 필수 필드 7종, `category` enum 이 `_meta.yaml` 소유라는 것, `visible`·`thumbnail`·`links` 의 의미, **`links.repo` 는 공개 표시 전용이고 추적은 레지스트리가 소유한다**는 것(DEC-014 D1), 본문 섹션 구조.

### D6. `id: P-NN` 은 코드가 채번한다

기존 `P-NN` 중 최대값 + 1. 현재 `P-14` 이므로 다음은 `P-15` 다. **결번(`P-01`)을 메우지 않는다** — 지워진 카드의 번호를 재사용하면 과거 기록과 어긋난다.

### D7. 검증은 파일을 쓰기 전에 한다. DB CHECK 로는 걸지 않는다

`apply/plan.py` 가 발행 전에 검증하는 것과 같은 규율이다. 커밋 후 부팅에서 잡으면 이미 사이트가 멈춰 있다.

**`product_slug` 가 실재하는 디렉토리인지를 DB 제약으로 만들지 않는다.** `daily.py:151` 이 같은 판단의 근거를 남겨 뒀다 — *"DB 계층이 레포 파일시스템을 알게 되고, 나중에 파일 이름이 바뀌면…"*. 대신 `missing_career()` 와 같은 방식으로 **조회 응답에 실재 여부를 실어 화면이 알린다.** 막지 않고 알린다.

### D8. 커밋은 하나다. 실패하면 되돌린다

스캐폴드 6 파일 + `showcase.md` 를 한 커밋으로 낸다([[decision-012-draft-storage-and-publish-boundary|KDEV-DEC-012]] D3 과 같은 이유 — 나눠 커밋하면 중간 커밋에 검증 실패 상태가 origin 에 남는다).

`commit_and_push_with_retry` 는 롤백이 없으므로 **push 실패 시 로컬 커밋을 되돌린다.** `apply/git.py` 가 발행 경로에서 이미 하는 일을 이 경로에도 적용한다.

### D9. company 는 파일을 만들지 않는다 — 회사 5개 디렉토리를 정리한다

회사 제품 등록은 `tracked_repos` 행 + 클론으로 끝난다. 카드도 문서 트리도 만들지 않는다.

그 결과 기존 회사 5개 디렉토리(`showcase.md` 하나뿐, 전부 `visible:false`+`(TBD)`)는 **역할이 이미 끝난 상태**다. 존재 이유였던 "잔디가 긁을 레포 목록의 원천" 은 DEC-014 가 `tracked_repos` 로 가져갔다. **디렉토리째 삭제한다** — `showcase.md` 만 지우면 빈 디렉토리가 남아 검증 에러가 된다.

`/api/projects` 모집단이 13 → 8 로 줄지만 다섯 모두 `visible:false` 라 **화면 변화는 없다.**

### D10. CRU 다. 삭제는 `enabled=false`

DEC-014 D2 가 `enabled` 컬럼에 *"삭제 대신 끄기"* 로 이미 정했다. 레지스트리 행을 물리 삭제하는 경로를 만들지 않는다.

**제품 문서 삭제도 화면에 없다.** 디렉토리 삭제는 그래프 노드 다수를 한 번에 없애 L1 dead link 를 낼 수 있다. 사람이 로컬에서 판단한다.

### D11. 화면 슬롯은 「프로젝트」다

사이드바 `soon` 여섯 중 **프로젝트**를 쓴다. 「설정」은 토큰·주기·상한처럼 제품과 무관한 값이 생길 때 쓴다.

### D12. 레포 4개를 전부 편입한다 (OQ-1 해소)

로컬 클론의 `origin` 을 실측했다. **넷 다 원격이 실재한다** — 제품 README 의 `Remote: TBD` 가 낡은 정보였다.

| 제품 | 레포 | account | 최근 30일 본인 커밋 | 마지막 커밋 |
|---|---|---|---:|---|
| ax-knowledge-graph | `kknaks/ax-graph` | personal | **48** | 2026-07-28 |
| mini-game | `kknaks/lunch_game` | personal | 6 | 2026-07-18 |
| cloud-file-organizer | `kknaksss/gcs_demo` | personal | 3 | 2026-07-10 |
| mac-remote | `kknaks/mac-remote` | personal | 0 | 2026-06-10 |

**한 달에 57건이 잔디에서 빠지고 있었다.** `ax-graph` 혼자 48건으로, 그 기간 가장 활발한 레포다. 이것이 BL-005 가 말한 *"낡은 것은 카드 내용이 아니라 모집단"* 의 정량이다.

넷 다 `type=studio` · `account=personal` 이다. 레지스트리가 **13 → 17행**이 된다. `mac-remote` 는 최근 활동이 0이지만 `enabled=true` 로 넣는다 — 안 넣으면 다시 활동할 때 조용히 누락되고, 비용은 클론 디스크뿐이다.

**부수 작업**: 제품 README 세 곳의 `Remote: TBD` 를 실제 값으로 고친다(ax-knowledge-graph·mini-game·mac-remote). 문서가 코드보다 낡아 있었다.

### D13. showcase 형식은 **하나**다 — studio 케이스 스터디 형식 (OQ-2 해소)

두 형식이 경쟁하는 줄 알았는데 실측해 보니 아니었다. **PDF 케이스 스터디 필드(`problem`·`approach`·`impact`·`learnings`·`troubles`)를 가진 8개가 정확히 studio 8개**이고, `개요/기술스택/주요기능` 만 있는 스텁 5개가 정확히 company 5개다.

D9 이 company 파일을 없애므로 **남는 것은 studio 8개, 전부 같은 형식**이다. 고를 것이 없다.

```text
frontmatter
  필수(로더)     type · id · title{ko,en} · summary{ko,en} · category · status · stack[]
  표시           org · date · visible · thumbnail · links{repo,live}
  PDF 전용       problem · approach · impact · learnings · troubles[]   ← 비면 PDF 미표시
본문
  필수 3         # 개요 · # 기술스택 · # 주요기능
  선택 4         # 아키텍처 · # 핵심 구현 · # 마주친 문제 · # 회고
```

**본문 섹션은 계약이 아니라 관례다** — `/api/projects` 가 `body` 를 통째로 넘기고 FE 가 마크다운으로 렌더한다. 그래서 템플릿이 관례를 고정하는 유일한 자리다. 반면 **PDF 필드는 계약이다** — `print.py:98-102` 가 이름으로 읽는다.

스캐폴드는 필수 3섹션을 헤딩만 넣고 비워 둔다. PDF 블록은 **넣지 않는다** — 케이스 스터디는 제품이 어느 정도 진행된 뒤에 쓰는 것이고, 빈 필드가 있으면 PDF 에 빈 칸이 나가는 게 아니라 사람이 "채워야 할 것" 을 착각한다.

### D14. `visible` 은 파일에 남긴다 (OQ-3 해소) — **D18 로 개정**

> **2026-08-03 개정.** 이 결정이 기각한 것은 **DB 이관**이지 "화면에서 못 고친다" 가
> 아니었다. 선택지를 A(읽기 전용)와 B(DB 이관) 둘로만 봤고, **C — 화면이 파일을 고치고
> 커밋한다** 를 빠뜨렸다. 아래 근거 둘은 B 에 대해서만 유효하다. C 는 [[#D18. `visible` 토글은 파일을 고친다|D18]] 이 채택한다.

이관하지 않는다. 근거 둘.

1. **A안(부트스트랩)의 원칙이다.** 화면은 최초 생성만 하고 그 뒤로는 파일이 SoT 다. `visible` 만 DB 로 빼면 한 문서의 필드가 두 곳에 살고, Obsidian 에서 고친 값과 화면 값이 갈라진다.
2. **공개 API 가 Postgres 를 읽는 첫 사례가 된다.** 지금 `/api/projects`·`/api/print` 는 전부 in-memory dict 다. 토글 하나를 위해 공개 경로에 DB 의존을 넣으면 부팅·reload·장애 경로가 전부 바뀐다.

~~화면에는 **읽기 전용으로 표시**한다.~~ → D18 이 편집을 연다. 다만 **값이 사는 곳은 여전히 파일**이다.

### D15. `products/README.md` 제품 목록은 스캐폴드가 갱신한다 (OQ-4 해소)

지금 **18개 중 9개만** 적혀 있다. 손으로 두면 계속 어긋난다 — 이미 어긋나 있는 것이 증거다.

- 새 제품 등록 시 **스캐폴드가 행을 추가한다.** D8 의 같은 커밋에 포함한다.
- 기존 누락분은 **work 에서 1회 채운다.** D2(통합)·D9(회사 5개 삭제) 반영 후의 목록이 기준이다.
- 표를 통째로 재생성하지 않고 **행만 추가**한다. `Context` 열에 사람이 적은 메모가 있을 수 있다.

### D16. showcase 를 그래프 노드로 승격하지 않는다 (OQ-5 해소)

`persona_loader.py:238` 이 *"product-as-node 는 SPEC-002 후속"* 으로 남겨 둔 것을 여기서 닫는다. **승격하지 않는다.**

- **showcase 는 공개 카드지 지식 노드가 아니다.** 그래프의 단위는 개념과 결정이고, 카드는 그 제품 문서들이 이미 노드로 들어가 있다.
- **D2·D9 이후 8장으로 줄어** 노드화 이득이 더 작아진다.
- stem 중복은 `product_slug` 로 풀 수 있게 됐지만, **풀 수 있다는 것이 풀어야 할 이유는 아니다.** 노드가 되면 L1~L6 검증 대상이 되어 카드 한 장의 링크 오타가 부팅을 막는다.

필요해지면 재개할 수 있다 — `product_slug` 가 그 재료를 남긴다.

### D17. 미등록 레포를 화면이 발견해서 알린다

**D12 만으로는 재발을 못 막는다.** 오늘 발견한 4개를 채울 뿐, 다음 달에 레포를 하나 더 파면 같은 일이 반복된다.

근본 원인은 **레지스트리가 `showcase.md` 에서 시드돼 그 사각지대를 그대로 물려받았다**는 것이다(`repo_registry.py` — *"한 번만 긁어 온다. 그 뒤로는 레지스트리가 SoT"*). 그리고 그 뒤로 **발견 장치가 없다** — 모듈에 있는 것은 `seed_from_showcase`(1회)와 `enabled_repos`(조회)뿐이다.

실패가 침묵한다는 것이 문제의 본질이다.

| 단계 | 상태 | 알림 |
|---|---|---|
| 새 레포를 판다 | 레지스트리에 없음 | 없음 |
| 커밋을 쌓는다 | 조사 대상이 아님 | **없음** |
| 09:05 잔디가 돈다 | 등록된 것만 긁고 **성공으로 끝난다** | 없음 |

WORK-017 결함 ④(*"시드 함수는 있는데 프로덕션 호출부가 0 — 매일 `NO_ACTIVITY` 로 끝나고 실패로 보이지 않는다"*)와 같은 종류의 침묵이다.

```text
GET /user/repos          personal 토큰 (kknaks · kknaksss)
GET /orgs/{org}/repos    company 토큰
  → tracked_repos 와 diff
  → 화면 상단 "미등록 레포 N건" 배너 · 클릭하면 등록 폼이 채워진 채로 열린다
```

- **거른다**: `owner` 가 `gh_accounts()` 의 계정이 아닌 것 · `fork: true` · `archived: true`. 안 거르면 배너가 소음이 되고, 소음이 되면 아무도 안 본다.
- **화면 진입 시 조회한다.** 별도 스케줄을 만들지 않는다 — 배너를 볼 사람이 화면에 있을 때만 의미가 있다.
- **막지 않고 알린다.** D7 과 같은 원칙이고 `missing_career()` 와 같은 형태다. 자동 등록하지 않는다 — 무엇을 추적할지는 사람이 정한다.

이것이 붙어야 D12 가 **일회성 정정**에서 **재발 방지**로 바뀐다.

### D18. `visible` 토글은 파일을 고친다 — DB 로 옮기지 않는다

화면에서 노출을 못 바꾸는 것이 실제로 걸렸다(로컬 확인 중 사용자 지적). D14 는 그것을
"파일이 SoT 라 어쩔 수 없는 비용" 으로 뒀는데, **그 전제가 틀렸다.**

```text
showcase.md 읽기 → frontmatter 의 `visible` 한 줄만 치환 → 커밋 1개 → push
```

**admin 은 이미 파일을 쓰고 커밋한다.** 제품 등록이 골격 6 파일 + 카드를 `publish_atomic`
으로 한 커밋에 낸다(D4·D8). `visible` 토글은 그 기계의 훨씬 작은 버전이라 새 경로가
생기지 않는다.

이 방식이 지키는 것 셋.

| | |
|---|---|
| 파일이 SoT | 값이 사는 곳이 안 바뀐다. Obsidian 에서 고쳐도 충돌하지 않는다 |
| 공개 API 무변경 | `/api/projects`·`/api/print` 는 계속 in-memory dict 만 읽는다 |
| 이력이 남는다 | 언제 공개/비공개로 바꿨는지가 git 에 남는다. DB 였으면 마지막 값만 남는다 |

**`frontmatter.loads()` → `dumps()` 왕복을 쓰지 않는다.** WORK-017 결함 ⑩ 이 정확히 그
함정이었다 — 값은 보존되지만 **주석이 사라지고 키가 알파벳순으로 재정렬**돼, 한 줄을
바꾸려던 발행이 42 insertions / 38 deletions 를 냈다. `render_career` 가 그래서 텍스트를
그대로 이어 붙인다. `visible` 도 **그 한 줄만 치환**한다.

- `visible` 키가 없으면 로더 기본값이 `true` 다(`projects.py:18`). 그때는 줄을 **추가**한다.
- 카드가 없는 제품(`card_visible: null`)은 토글이 없다. 만들 대상이 없기 때문이다.
- 커밋 실패는 `publish_atomic` 이 되돌린다 — 반쯤 바뀐 파일이 남지 않는다.

### 기각

- **`project_detail` 테이블 신설** — 본문이 파일에 남으면 담을 것이 조인뿐이다. 테이블 둘은 13~18행에 과하다(DEC-014 D2 와 같은 판단).
- **`showcase.md` 에 `product_slug` 필드 추가** — 조인이 파일에 있으면 잡이 다시 파일을 읽는다. DEC-014 D1 이 없앤 의존을 되살린다.
- **`tracked_repos` 에 showcase 파일 경로 저장** — 경로는 `slug` 에서 유도된다. 파생값을 컬럼으로 박으면 드리프트 원천이 하나 는다.
- **AI 에이전트 스캐폴딩** — 결정적인 복사·치환에 비결정적 수단을 쓴다. 워커·예산·비동기 수확이 따라붙는다.
- **`templates/product/` 통째 복사** — 샘플 문서가 그래프 노드가 되어 부팅을 막는다.
- **`visible` 을 DB 로 이관** — 한 문서의 필드가 두 곳에 살고, 공개 API 가 Postgres 를 읽는 첫 사례가 된다(D14).
- **showcase 를 그래프 노드로 승격** — 카드 한 장의 링크 오타가 부팅을 막게 된다(D16).
- **`products/README.md` 표 전체 재생성** — `Context` 열의 사람 메모가 날아간다. 행만 추가한다(D15).
- **`mac-remote` 를 레지스트리에서 제외** — 최근 활동이 0이지만, 빼면 다시 활동할 때 조용히 누락된다(D12).
- **미등록 레포 자동 등록** — 무엇을 추적할지는 사람이 정한다. 발견해서 알리는 데서 멈춘다(D17).
- **미등록 레포 발견을 스케줄 잡으로** — 배너를 볼 사람이 화면에 있을 때만 의미가 있다. 화면 진입 시 조회한다(D17).

## Rationale

- **판단 기준** — 본문의 SoT 를 파일에 두기로 한 이상(*"결과 문서는 md로 계속 관리해야, 내가 로컬에서 md 작업 하지 않을까"*), DB 가 가질 수 있는 것은 **조인과 운영 상태**뿐이다. 그래서 스키마 변경이 컬럼 하나로 끝난다.
- **화면의 역할이 부트스트랩인 이유** — 제품 스펙은 작업하면서 손으로 쓰인다. 화면이 계속 소유하면 Obsidian 편집분이 다음 렌더에 덮인다. **최초 생성만 하고 그 뒤로는 파일이 이긴다.**
- **대안 대비** — 사람이 폴더를 파는 A안은 코드가 0이지만 필수 6 파일을 빠뜨리기 쉽고, 빠뜨린 결과가 `product_doc_pipeline` 에러로만 나타난다. 화면이 만들면 그 집합이 코드로 고정된다.
- **P2 의 선행조건이다.** `product_slug` 없이는 `product_map` 을 만들 수 없고, 그러면 잔디가 studio 커밋을 제품으로 보낼 방법이 없다.
- **리스크**
  - **넷째 쓰기 경로가 생긴다.** 잡 셋에 더해 admin 이 파일을 쓴다. D8 의 롤백이 유일한 방어다.
  - **스캐폴드가 그래프를 깰 수 있다.** D3 이 그 경로를 막지만, 템플릿에 새 샘플 문서가 추가되면 복사 목록이 조용히 어긋난다 — 복사 목록을 **화이트리스트**로 두고 테스트로 고정한다.
  - **`product_slug` 오타.** DB 가 막지 않으므로(D7) 화면 표시와 P2 의 `missing_product()` 가 유일한 감지 장치다.
  - **D2 이관 중 사고.** `showcase.md` 이동은 git mv 한 번이지만, 옮기는 도중 로더가 두 경로에서 같은 `P-02` 를 보면 안 된다. 한 커밋으로 처리한다.

## Scope

- **In** — `tracked_repos.product_slug` 컬럼 + 마이그레이션 `0009` · **17행** 시드 매핑(기존 13 + D12 의 4) · `templates/product/showcase.md` 신설 · 관리자 제품 등록(스캐폴드·레포 등록·클론·showcase 렌더) · 레지스트리 CRU(`enabled` 토글 · `product_slug`/`detail` 편집 · 수동 sync) · 사전 검증 · 커밋 1개 + 롤백 · `kknaks-profile` → `kknaks-dev` 통합 · 회사 5개 디렉토리 삭제 · `products/README.md` 목록 1회 정정 + 스캐폴드 자동 추가 · 제품 README 3곳의 `Remote: TBD` 정정 · **미등록 레포 발견 배너**(D17) · 프로젝트 슬롯 FE.
- **Out** — 잔디 산출물에 product 추가(P2, 후속 decision) · `visible` DB 이관(D14 기각) · showcase 그래프 노드 승격(D16 기각) · 제품 문서 본문 편집/삭제 · `algorithms`·`_map.md`·`contents` DB화(별도 후속) · 케이스 스터디 필드 초안 생성.
- **영향을 받는 spec 후보** — 신규 spec(제품 레지스트리와 등록), [[spec-011-commit-collection|KDEV-SPEC-011]](레지스트리 스키마 확장), [[spec-001-directory-structure|KDEV-SPEC-001]] §5(제품 형태 계약 — showcase-only 정의가 D9 로 바뀐다).

## Open Questions

**없다.** 다섯 건을 2026-08-03 에 전부 닫았다. 둘은 실측이 답을 줬고, 하나는 D9 의 결과로 저절로 해소됐다.

### 해소됨

| ID | Question | 결론 |
|---|---|---|
| ~~OQ-1~~ | 레포 4개 편입 범위 | **전부 편입 — 13 → 17행** (D12). 로컬 클론 `origin` 실측 결과 **넷 다 원격 실재**(README 의 `Remote: TBD` 가 낡았다). **한 달에 57건이 잔디에서 빠지고 있었다** — `ax-graph` 혼자 48건 |
| ~~OQ-2~~ | `showcase.md` 본문 섹션 구조 | **형식은 하나다** (D13). 두 형식이 경쟁하는 줄 알았으나 **케이스 스터디 필드 보유 8개 = studio 8개**, 스텁 5개 = company 5개였다. D9 이 company 파일을 없애므로 남는 것은 전부 같은 형식 |
| ~~OQ-3~~ | `visible` 을 DB 로 올릴지 | **파일 유지 — 이관하지 않는다** (D14). 한 문서의 필드가 두 곳에 살고, 공개 API 가 Postgres 를 읽는 첫 사례가 된다. 화면은 읽기 전용 표시 |
| ~~OQ-4~~ | `products/README.md` 갱신 주체 | **스캐폴드가 행을 추가한다** (D15). 기존 누락분(18개 중 9개만 기재)은 work 에서 1회. 표 전체 재생성은 안 한다 |
| ~~OQ-5~~ | showcase 를 그래프 노드로 승격할지 | **승격하지 않는다** (D16). 카드는 지식 노드가 아니고, 노드가 되면 링크 오타 하나가 부팅을 막는다. `product_slug` 가 재료를 남기므로 필요해지면 재개 가능 |

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| [[spec-014-product-registry-and-admin\|KDEV-SPEC-014]] | **create (완료 2026-08-03)** | 등록 흐름 · 스캐폴드 최소집합 · 사전 검증과 사유 코드 · 커밋/롤백 계약 · 미등록 발견 · admin API |
| [[spec-011-commit-collection\|KDEV-SPEC-011]] | update | 레지스트리 행에 `product_slug` 추가 |
| [[spec-001-directory-structure\|KDEV-SPEC-001]] | update | §5 제품 형태 — company 는 파일을 갖지 않는다(D9), showcase 는 제품 폴더 안에 있다(D2) |
