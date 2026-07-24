---
type: spec
id: AXKG-SPEC-015
title: "문서 SoT git 동기화 계약"
status: draft
product: ax-knowledge-graph
version: 0.0.1
created_at: 2026-07-24
updated_at: 2026-07-24
tags:
  - product/ax-knowledge-graph
  - doc/spec
  - status/draft
links:
  baselines:
    - "[[baseline-001-ax-knowledge-graph-from-curated-sources|AXKG-BL-001]]"
  decisions:
    - "[[decision-002-markdown-sot-postgres-storage|AXKG-DEC-002]]"
    - "[[decision-010-documents-git-versioning-and-correction-loop|AXKG-DEC-010]]"
  specs:
    - "[[spec-004-documentation-approval-gate|AXKG-SPEC-004]]"
    - "[[spec-005-document-link-graph-contract|AXKG-SPEC-005]]"
  works: []
  releases: []
  related: []
---

# 문서 SoT git 동기화 계약

문서 SoT를 `ax-graph` 레포 `documents/` 로 버전관리하고, 서버 AI는 문서화 승인 시점에 자동 commit+push, 사람은 로컬 clone에서 pull→수정→push 로 교정한다.

> 파일 write 자체는 SPEC-004(문서화 승인 게이트)가 SSOT다. 이 spec은 그 write 뒤에 붙는 **git 동기화**(커밋 시점·pull rebase·충돌·재인덱싱·크리덴셜)만 계약한다.

## 1. Context

- SoT는 Markdown 파일이다(AXKG-DEC-002). 운영에서 root는 bind mount.
- 확정 문서 write는 문서화 승인 시 `ApplyExecutor.apply()`가 수행한다(AXKG-SPEC-004): create/overwrite/remove.
- 서버는 코드 레포 체크아웃이 없다(이미지 pull 실행). 이 spec으로 SoT를 코드 레포의 sparse-checkout 워킹트리로 만든다.
- 작성자는 서버 AI(주)와 사람(교정자) 둘이다(AXKG-DEC-010).

## 2. Repository & Mount Contract

- 문서는 `ax-graph` 레포 **top-level `documents/`** 하위에만 둔다. 상대 경로는 markdown root 기준(SPEC-005/004와 동일).
- 서버 SoT는 코드 레포의 **cone sparse-checkout**(`documents/`만) 워킹트리다. 코드(`apps/`·`packages/`)는 체크아웃하지 않는다.
- 바인드 마운트는 이 워킹트리의 `documents/` 를 api(rw)·qmd(ro) `/workspace` 로 연결한다.
- CI 트리거(`deploy-prod.yml`)에 `documents/**` 를 포함하지 않는다. 문서 push는 이미지 재빌드를 유발하지 않는다.
- root 소유 트리이므로 `safe.directory` 를 설정한다.

## 3. Sync Contract (server, commit-on-approval)

**참고 구현**: `harness_works/mediness-app` `back/app/services/publish/`(GitClient·BasePublisher·lock)를 미러한다. 아래 메커니즘은 그 검증된 패턴을 따른다.

공통 메커니즘(mediness GitClient 미러):
- **PAT는 커맨드마다 remote URL에 주입**하고 `.git/config`에 남기지 않는다: `https://x-access-token:${AXKG_DOCS_GIT_TOKEN}@github.com/kknaks/ax-graph.git`.
- 모든 git 커맨드에 **`git -c safe.directory=<repo>`** prepend(root 소유 트리 대응).
- author/committer는 env(`GIT_AUTHOR_*`/`GIT_COMMITTER_*`) + `-c user.name/email`로 주입. AXKG 서버 커밋은 **단일 author=committer=bot**(사람 교정은 로컬 git에서 사람이 author).
- 직렬화: 전역 `asyncio.Lock`(mediness `publish_lock` 미러) — 승인 동시성 직렬화(단일 컨테이너 전제, 다중 레플리카는 DEC-010 OQ-003).
- 시작 시 `fetch_and_reset`로 다운타임 중 놓친 상태 복구(mediness startup 패턴).

**충돌 전략: (A) commit-then-rebase-push 구현 (2026-07-24). B에서 정정.**

> **B(reset-first) 기각 이유(구현 중 발견):** AXKG 승인은 "DB 상태변경 + 파일 write"가 한 몸이다. B의 `reset --hard`는 push가 한 번이라도 실패(비치명)하면 다음 sync 때 미커밋/미푸시 문서를 되돌려, 승인은 됐는데 파일이 사라지는 불일치를 만든다. mediness는 push 실패를 치명(publish 실패)으로 막지만, AXKG에선 github 장애가 문서 승인을 막는 꼴이라 부적합. A는 push 실패해도 커밋이 로컬에 누적·파일 유실 없음.

`ApplyExecutor.apply()`가 확정 파일을 write한 뒤(현행 유지), 문서화 게이트 승인이면 background로 `sync_after_approval`:
1. `async with _git_lock:` (전역 asyncio.Lock)
2. `git add -A documents/`. staged 없으면 no-op.
3. `git commit -m "approve: gate <id>"` (author=committer=bot).
4. `git fetch <token-url> main` → `git rebase FETCH_HEAD` — 사람 교정 위로 우리 커밋 replay.
5. `git push <token-url> HEAD:main`.
- **비치명**: rebase 충돌 → `rebase --abort`(커밋 로컬 유지) + 경고. push 실패 → 커밋 로컬 유지, 다음 승인에 재시도. 워킹트리 reset/복구 안 함(전략 A 핵심 — 파일 유실 없음).
- feedback/regenerate/retry(최종 문서 미write)는 sync 대상이 아니다.
- 구현: `apps/api/axkg/services/git_sync.py` `GitClient.commit_rebase_push` / `sync_after_approval`. 훅: `approval_gates.approve_gate`(gate_kind==documentation & sync on).

## 4. Conflict Contract

- (A) rebase 충돌(같은 파일 AI+사람 동시 수정)은 드묾(사람은 보통 AI가 만드는 것과 다른 문서를 교정). 발생 시 `rebase --abort`, 커밋 로컬 유지, push 보류, 경고(Slack 후속).
- 자동 병합/강제 push 금지. push reject는 다음 승인 push가 재조정.

## 5. Correction Loop (human)

- 사람은 서버를 직접 만지지 않고 로컬 clone(`documents/`)에서만 작업한다.
- 흐름: `git pull` → `documents/…` 수정 → `git commit` → `git push`.
- 규칙: pull 먼저, push 거부 시 `pull --rebase` 후 재push. `documents/` 외(코드) 를 만지지 않는다(만지면 CI 발동).

## 6. Reindex Contract (정합)

두 인덱스를 구분한다.

- **qmd 검색(retriever) 인덱스**: qmd 사이드카가 주기적 증분 재인덱싱을 소유한다(AXKG-SPEC-006/011, 2026-07-14 정정). 사람 교정이 서버 파일에 반영되면 다음 주기에 자동 흡수된다(수분 staleness 수용). 추가 조치 불필요.
- **api 그래프 엣지 cache(PostgreSQL)**: markdown에서 재빌드 가능(DEC-002). `pull_reindex_loop`(main lifespan)가 주기적으로(`AXKG_DOCS_GIT_PULL_INTERVAL_SECONDS`, 기본 300s) `fetch_ff`로 사람 교정을 pull하고, 실제 변경이 있으면 `run_startup_scan`(content_hash 비교 증분)으로 그래프를 재빌드한다.
  - 구현: `git_sync.pull_reindex_loop` → `workers.graph_rebuild.run_startup_scan`.
  - 이 재인덱싱 없이는 사람의 관계 문서 교정이 그래프 엣지/노드에 반영되지 않는다(계약 필수).
  - `fetch_ff`는 미푸시 로컬 커밋으로 diverge면 skip(다음 승인 push가 조정) — 강제 안 함.

## 7. Credentials & Config

- push 크리덴셜은 `.env`(배포 시크릿):
  - `AXKG_DOCS_GIT_TOKEN` — GitHub PAT(fine-grained, 대상 ax-graph, contents:write).
  - GitHub email·author 이름 — git identity(axkg-bot).
- remote: `https://x-access-token:${AXKG_DOCS_GIT_TOKEN}@github.com/kknaks/ax-graph.git`. **토큰은 커맨드 실행 시에만 URL에 주입, `.git/config`에 영속 금지**(mediness `_remote_url_with_token` 미러). 에러 메시지·로그에서 토큰 마스킹.
- author 이름·email: `AXKG_DOCS_GIT_AUTHOR_NAME`(axkg-bot), `AXKG_DOCS_GIT_AUTHOR_EMAIL`(GitHub email).
- 플래그: `AXKG_DOCS_GIT_SYNC_ENABLED`(기본 off→검증 후 on), `AXKG_DOCS_GIT_REMOTE`, `AXKG_DOCS_GIT_BRANCH=main`, `AXKG_DOCS_GIT_PULL_INTERVAL_SECONDS`(기본 300).
- **마운트**: api 컨테이너가 `.git`을 보려면 **repo 루트를 마운트**한다 — `/mnt/data/axkg/repo:/workspace`, `AXKG_MARKDOWN_ROOT=/workspace/documents`, `AXKG_DOCS_GIT_REPO_ROOT=/workspace`(compose environment override, 버전관리). qmd는 `/mnt/data/axkg/repo/documents:/workspace:ro`.
- 배선 위치: **프로덕션은 GitHub Secret `ENV_PROD`**(배포 시 서버 `.env` 재생성)에 `AXKG_DOCS_GIT_SYNC_ENABLED`·`AXKG_DOCS_GIT_TOKEN`·`AXKG_DOCS_GIT_AUTHOR_EMAIL` 추가. `apps/api/.env.example`은 템플릿(선언 완료). 시크릿은 레포 커밋 금지.
- **서버 클론**: `/mnt/data/axkg/repo`는 **full 클론**이어야 한다(blobless면 rebase가 promisor 인증으로 실패). sparse-checkout=`documents/`.

## 8. Verification

- 스위치오버(sync off): sparse-checkout 마운트 교체 후 api `/health`·qmd 인덱스 정상.
- 사람 교정: 로컬 `documents/` 1파일 수정 push → 서버 `pull_reindex_loop` fetch_ff → `run_startup_scan` 반영 확인.
- sync on: 게이트 1건 승인 → github ax-graph main 에 `documents/` 커밋, CI **미발동** 확인.
- 충돌: 같은 파일 양쪽 수정 → rebase abort·커밋 로컬 유지, 강제 push 없음 확인.

## 9. Open Questions

- OQ: origin 바이너리(.docx) git-lfs 여부(용량 임계) — DEC-010 OQ-002.
- OQ: 다중 api 레플리카 commit 직렬화 — DEC-010 OQ-003.
- ~~충돌 전략 A vs B~~ → **(A) commit-then-rebase-push 구현(2026-07-24, B에서 정정)**. §3.
- ~~폴링 루프 둘지~~ → **폴링 `pull_reindex_loop` 구현**(주기 fetch_ff + run_startup_scan). §6.
- OQ: 재인덱싱을 pull 루프(현재) 외에 승인 push 후에도 트리거할지(사람 교정 즉시성 vs 부하).
