---
type: baseline
id: KDEV-BL-003
title: "inbox 승인 게이트 파이프라인 + 원자 개념(concept) 층"
status: accepted
product: kknaks-dev
source:
  type: idea
  ref: "kknaks 요청 2026-07-27 — ax 승인 게이트 패턴 각색 + permanent/concept 신설"
links:
  baselines: []
  decisions:
    - "[[decision-010-knowledge-graph-four-layers|KDEV-DEC-010]]"
    - "[[decision-011-approval-gate-chain|KDEV-DEC-011]]"
    - "[[decision-012-draft-storage-and-publish-boundary|KDEV-DEC-012]]"
    - "[[decision-013-slack-bridge-into-backend|KDEV-DEC-013]]"
  specs: []
  works:
    - "[[work-012-slack-bridge-absorb|KDEV-WORK-012]]"
    - "[[work-013-concept-layer|KDEV-WORK-013]]"
    - "[[work-014-queue-and-route-gate|KDEV-WORK-014]]"
    - "[[work-015-youtube-chain-and-executor|KDEV-WORK-015]]"
  releases: []
  related:
    - "[[baseline-001-repo-knowledge-graph|KDEV-BL-001]]"
    - "[[baseline-002-app-db-and-admin|KDEV-BL-002]]"
created_at: 2026-07-27
updated_at: 2026-07-27
tags:
  - product/kknaks-dev
  - doc/baseline
  - status/accepted
---

# inbox 승인 게이트 파이프라인 + 원자 개념(concept) 층

지금 AI가 만든 결과물이 사람 검토 없이 바로 `origin/main`에 커밋된다. 이 경로 전부를 "AI 초안 → 관리자 승인 게이트 → 발행"으로 바꾸고, 그 과정에서 지식의 최소 단위를 담을 `permanent/concept/` 층을 신설한다.

> 아직 결정하지 않은 날것의 입력이다. 정리보다 보존이 우선이다.

## Raw

> kknaks 요청 (2026-07-27)

**하고 싶은 것**

- `ax-knowledge-graph`의 승인 게이트 패턴(AXKG-DEC-001, SPEC-001/002/003/004)을 이 레포에 각색한다.
- 순서: ① 슬랙 리팩토링 — 백엔드로 들어오기, ② 슬랙 inbox → 승인 게이트(경로 설정) → 추가 태스크.
- 게이트는 하나가 아니라 **여러 개가 체인으로** 붙는다. 유튜브를 예로 들면:

  ```text
  inbox → 어드민 게이트 → youtube 콘텐츠 분류 → concept 추출 → content 형식 생성
  ```

  각각에 승인 게이트가 있다.

**concept 층**

- `permanent/` 아래에 `concept/` 디렉토리가 필요하다.
- concept 디렉토리에는 **지식의 최소 단위 개념**들을 넣는다.
- 예: 유튜브에서 STT 개념 영상을 시청하고 inbox에 넣는다 → 내용 요약 → 다음 태스크로 `permanent/concept/`와 `persona/contents/`에 들어가야 하는 것 아닌가.
- 그래야 내 프로덕트를 업데이트할 때 **concept에서 개념을 긁어와서 idea → decision → spec**을 만들 수 있다.

**부수 요구**

- `templates/`에 concept 템플릿이 필요하다.
- `rules/`에 룰이 필요하다.
- 지금 서버에서 push를 하는데, **최종 승인이 나면 업데이트하면서 push해야** 로컬 노트북에서도 받아볼 수 있다.

## Context

작업 착수 시점(2026-07-27) 코드·문서 실측.

### 지금 AI 결과물이 바로 커밋되는 경로가 4개다

| 경로 | 트리거 | 쓰는 것 | 커밋 |
|---|---|---|---|
| `main_job.py` (잔디) | cron 09:05 KST | `daily/{date}.md` | `commit_and_push_with_retry` |
| `algorithms/main.py` | cron 23:00 UTC | `persona/algorithms/A-NNN.md` | 〃 |
| `content_enrich.py` | cron 아님 — `POST /admin/reload` webhook background | `persona/contents/C-*.md` `pending`→`published` | 〃 (파일당 1커밋, 실패도 `status: error`로 커밋) |
| `slack_bridge/runner.py` (지식캡처) | Slack 스레드 | `inbox/*.md` 또는 `reference/{group}/*.md` | `publish()` + `reload_data()` |

- 지식캡처는 "큐에 쌓이는 항목"이 아니라 **이미 잡과 동형인 auto-commit 경로**다. 사람이 개입할 지점이 0개고, 검토는 Slack 회신 한 줄이 전부다.
- 반면 지식캡처만 open-kknaks `session_id`를 저장해 스레드 후속 재생성을 한다(`runner.py:76` `options["resume"]`). 피드백 기반 재생성 배선에 가장 가까운 기존 코드다.
- 다만 그 재생성은 **같은 파일 덮어쓰기 + 커밋 추가**다. 직전 버전이 보존되지 않는다.

### Slack bridge가 별도 컨테이너로 떠 있다

- `app/back/service/slack_bridge/`(라이브러리) + `app/slack_bridge/run.py`(entrypoint)로 분리돼 있고, compose의 `slack-bridge` 서비스가 `Dockerfile.back` **같은 이미지**로 `run.py`를 실행한다.
- 분리 근거는 `OKK-SPEC-011` §4의 "별도 장기 실행 프로세스로 운용한다" 한 줄뿐이고, 왜인지는 어디에도 없다.
- back은 `--workers 1` 하드락 + `_check_single_worker()` raise로 이미 APScheduler를 in-process로 돌린다. Socket Mode는 아웃바운드 웹소켓이라 포트도 필요 없다.
- 유지비는 실재한다: `sys.path` 해킹, `service/slack_bridge` ↔ `app/slack_bridge` 이름 충돌, env 이중 관리, repo 쓰기 마운트 2곳, git push 소유권 분산.
- 결정적으로 **`slack-bridge` 서비스에 `DATABASE_URL`이 없다.** 이 프로세스는 Postgres에 붙지 못한다.

### 미커밋 md를 작업트리에 둘 수 없다

`reload.py:77`의 `_git_pull_rebase()`가 `git reset --hard origin/main`이다. webhook 한 번에 미커밋 변경이 사라진다. 승인 대기 초안은 반드시 DB에 있어야 한다.

### 목적지(루트 디렉토리) 계약은 있으나 concept 층이 없다

`KDEV-SPEC-001` §4 기준 현행 목적지:

| 목적지 | 경로 | `type` | 그래프 노드 |
|---|---|---|---|
| idea 보존 | `inbox/` | `idea` | ○ (`up:` 대상 아님) |
| 자료 정리 | `reference/{group}/` | `reference` | ○ |
| 영구 생각 | `permanent/` | `permanent` | ○ |
| 제품 아이디어 | `products/{제품}/00-baseline/` | product 계열 | ○ |
| 유튜브 콘텐츠 | `persona/contents/` | `content` | **✗** (KDEV-DEC-008) |
| 발행글 | `persona/posts/` | `post` | ○ (**디렉토리 미존재**, 실 발행물 0) |

- **원자 개념 층이 없다.** `permanent/`는 파일 1개 + `archive/`뿐이다.
- `reference/`는 목적지가 2단이다 — reference로 갈지 + `persona/_meta.yaml`의 13개 group 중 어디로 갈지. 그런데 `runner.py:106`이 `group="study"`로 하드코딩해서, Slack으로 들어온 reference는 전부 `reference/study/`로 간다. `_allowed_groups()`로 클러스터를 읽어오면서 쓰지 않는다.
- `inbox/README.md`는 *"주기적으로 리뷰해 종착지로 분류하면 원본 idea는 폐기(inbox는 항상 미분류만 보유)"*를 규정하는데, **그 리뷰·분류·폐기 단계가 구현에 없다.** inbox는 쌓이기만 한다.

### concept가 contents를 출처로 가리킬 수 없다

- `graph.py:20` `ALLOWED_NODE_TYPES`에 `concept`가 없다.
- `graph.py:33` `KNOWLEDGE_NODE_TYPES = {reference, permanent, post, product}`.
- `graph.py:36` `_TYPE_RANK`는 `reference/permanent/baseline/product = 4`로 동급이다.
- KDEV-DEC-008에 따라 contents는 `_build_graph_nodes`에 전달되지 않는다 → `nodes`에 없다 → concept에서 `[[C-012]]`를 걸면 `graph.py:196`의 **L1 dead link ERROR**가 나고 `reload_data()`가 거부한다.

### 규칙·템플릿이 지식노트 쪽만 비어 있다

| | 규칙 | 템플릿 |
|---|---|---|
| 제품 문서 | `para/projects/project.md` (20KB) | `templates/product/` 24개 |
| 지식노트 | **없음** — 디렉토리 README quick-rule + SPEC-001~004에 산재 | **없음** |

### DB는 `users` 한 테이블이다

- Alembic `0001_create_users`, async SQLAlchemy 2.0 + psycopg3(KDEV-DEC-009 v2).
- `products/kknaks-dev/40-architecture/`의 database·system README는 **빈 템플릿**이다. `users`조차 적혀 있지 않다.
- admin FE 사이드바는 콘텐츠·노트·프로젝트·알고리즘·커리어·설정이 전부 `ready: false` "soon"으로 자리만 잡혀 있다(`components/admin/sidebar.tsx`).

## Why It Matters

- **AI 첫 판단이 곧 SoT가 되고 있다.** 잘못된 분류·연결·본문이 그대로 커밋되고, 되돌리려면 git 히스토리를 건드려야 한다. 지식 베이스의 정합성이 AI 1회 출력 품질에 직결돼 있다.
- **피드백이 파괴적이다.** 스레드 후속으로 고치면 직전 버전이 사라진다. 어떤 지적이 무엇을 바꿨는지 추적할 수 없다.
- **개념이 재사용 단위로 서 있지 않다.** 지금은 자료 정리(reference)와 영구 생각(permanent) 2층뿐이라, 같은 개념이 여러 자료에 걸쳐 나와도 합류할 자리가 없다. 제품 문서를 쓸 때 "이 개념 어디 적어놨더라"를 매번 다시 찾는다.
- **`inbox/README.md`가 약속한 리뷰 단계가 코드에 없다.** 승인 게이트는 새 개념이 아니라 이미 문서로만 존재하는 계약을 채우는 일이다.
- **Slack bridge가 DB에 못 붙는다.** 승인 큐를 DB에 두는 순간 이 프로세스 경계가 곧바로 막힌다. 파이프라인의 선행 조건이다.

## Possible Direction

아직 결정은 아니다. decision에서 확정한다.

### 지식 4층 모델과 concept 층

`ax-knowledge-graph` SPEC-004 §4가 같은 문제에 도달해 4층 모델을 세웠다. 우리 루트에 대응시키면:

| 층 | 정체성 | 단위 | 수명 | ax | 우리 |
|---|---|---|---|---|---|
| 출처 기록 | "이 자료가 무엇을 말했나" | 자료 하나 | 생성 후 고정 | `resources/` | `reference/{group}/` |
| 원자 개념 | "이 개념은 무엇인가" — 사실의 SoT, 출처 독립 | 개념 하나 | 출처가 합류하며 성장 | `permanent/concepts/` | `permanent/concept/` (신설) |
| 종합 노트 | "내 판단/전략" — 개념을 엮은 것 | 영역 하나 | 개념 유입마다 성장 | `permanent/` 루트 | `permanent/` 루트 |
| 실행 문서 | 프로젝트 문서 | 프로젝트 | — | `projects/` | `products/{제품}/00-baseline/` |

동반되는 규율 후보:

- **SoT 위임** — 개념 상세는 concept 한 곳. reference와 permanent는 재서술하지 않고 `[[concept]]`로 위임한다.
- **개념 성장** — 같은 개념에 두 번째 출처가 오면 새 파일이 아니라 기존 concept를 보충한다. 이게 없으면 `stt.md`·`speech-to-text.md`가 따로 쌓인다. `graph.py:44` `build_alias_index`가 frontmatter `aliases`를 이미 지원하므로 개념 매칭의 재료는 있다.
- **rank 배치** — `concept: 4`로 두면 `concept → reference`(출처)와 `permanent → concept`(구성 개념) 양방향 `up:`이 모두 L4를 통과한다.

### 유튜브 하나에서 나오는 산출물

concept가 출처를 그래프 안에서 가리켜야 하는데 contents는 노드가 아니다(L1 ERROR). 따라서 후보는:

- (A) `contents` + `concept` — 요청 원안. concept의 출처 추적이 그래프에서 끊긴다.
- (B) `reference` + `concept` + `contents`(선택) — reference가 출처 기록을 맡고, contents는 "사이트에 전시할 것"만 추가로 낸다.
- (C) contents를 그래프 노드로 승격 — KDEV-DEC-008 뒤집기.

### 게이트 체인 모델

ax는 `gate_kind`가 `classification`/`documentation` 2개 고정 enum이다. 여기서는 목적지마다 스테이지 체인 길이가 달라지므로 **파이프라인 정의 자체가 데이터**여야 한다(`item` + `stage` 축). revision(v1 read-only + v2 박제)·feedback·ai_task·session resume·형제 supersede sweep 규칙은 AXKG-SPEC-002를 그대로 재사용할 여지가 있다.

### 저장·발행 경계

- draft = DB(박제), 확정 = md. KDEV-DEC-009 D1의 "운영 데이터는 DB, 지식그래프는 파일 SoT" 경계를 그대로 따른다.
- AI는 파일·DB를 직접 건드리지 않고 apply plan만 낸다. 별도 executor가 검증 후 실행한다(ax 원칙).
- **승인 단위 = 커밋 단위.** 유튜브 하나 승인 시 나오는 md 2~3장을 한 커밋으로 묶는다(지금 `content_enrich`는 파일당 1커밋).
- push 실패가 조용히 묻히면 안 된다. `commit_and_push_with_retry`는 3회 재시도 후 `False`를 반환할 뿐이다(`git_push.py:134`). apply 결과 상태와 재푸시 경로가 필요하다.

### 프로세스 경계

Slack bridge를 back의 lifespan으로 흡수한다(`RUN_SCHEDULER`와 같은 자리). 그러면 DB 세션·executor·git push가 한 프로세스에 모여 쓰기 소유권 문제가 사라지고, repo 마운트를 읽기 전용으로 낮출 수 있다.

### 문서 산출물

- `rules/knowledge-note-pipeline.md` — `product-doc-pipeline.md`의 대칭. 4층 모델·SoT 위임·개념 성장·경로/frontmatter 규칙.
- `templates/knowledge/` — idea·reference·concept·permanent 4종.
- 위 둘은 **work 산출물**이다. decision·spec이 확정한 계약의 파생물이지 선행물이 아니다.
