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

**충돌 전략: (B) reset-first 채택 (2026-07-24, mediness식 — 충돌 원천봉쇄).**

문서화 승인 확정 흐름을 git 락 안에서 감싼다:
1. `async with sync_lock:` (전역 락)
2. `git fetch origin main && git reset --hard FETCH_HEAD` — 원격(사람 교정 포함) 우선으로 워킹트리 정렬(`fetch_and_reset`).
3. `ApplyExecutor.apply()` 가 확정 파일을 write/overwrite/remove (reset 뒤에 쓰므로 유실 없음).
4. `git add -A documents/` → `git commit -m "approve: <doc_path> (gate <id>)"`.
5. `git push`. reject(레이스) → `fetch_and_reset → (재적용 불가 시 커밋 cherry) → push` 1회 재시도, 실패 시 알림.

> 이 순서는 apply 파일 write 가 git fetch/reset "뒤"에 오도록 승인 서비스를 개편해야 한다(현재는 apply 가 먼저 씀). 승인 라우트에서 `sync_lock` 획득 → fetch_and_reset → apply 호출 → commit/push 로 재배치한다.
> (기각안 A: commit-then-rebase — apply 뒤 add/commit 후 fetch+rebase. 침습은 적으나 같은 파일 동시수정 시 rebase 충돌 처리 필요. B가 last-write-wins 로 단순하고 검증됨.)

공통:
- **비치명**: sync의 어떤 실패도 승인 트랜잭션/파일 확정을 되돌리지 않는다. 예외 시 `git reset --hard origin/main`으로 워킹트리 복구(mediness 패턴), 커밋은 다음 승인에 재시도.
- feedback/regenerate/retry(최종 문서 미write)는 sync 대상이 아니다.

## 4. Conflict Contract

- 채택한 (B) reset-first 는 쓰기 전에 원격으로 reset 하므로 **rebase 충돌이 없다**(원격 우선). 사람 교정과 AI 재생성이 같은 파일이면 **AI가 원격 위에 덮어씀**(last-write-wins) — 이 특성을 수용하고, 덮어쓴 경우 알림한다.
- 자동 병합/강제 push 금지. push reject/이상 시 알림(Slack) 후 **정지** — 사람이 수동 해결한다.
- 에러 시 `git reset --hard origin/main` 으로 워킹트리 복구(mediness 패턴), 비치명.

## 5. Correction Loop (human)

- 사람은 서버를 직접 만지지 않고 로컬 clone(`documents/`)에서만 작업한다.
- 흐름: `git pull` → `documents/…` 수정 → `git commit` → `git push`.
- 규칙: pull 먼저, push 거부 시 `pull --rebase` 후 재push. `documents/` 외(코드) 를 만지지 않는다(만지면 CI 발동).

## 6. Reindex Contract (정합)

두 인덱스를 구분한다.

- **qmd 검색(retriever) 인덱스**: qmd 사이드카가 주기적 증분 재인덱싱을 소유한다(AXKG-SPEC-006/011, 2026-07-14 정정). 사람 교정이 서버 파일에 반영되면 다음 주기에 자동 흡수된다(수분 staleness 수용). 추가 조치 불필요.
- **api 그래프 엣지 cache(PostgreSQL)**: markdown에서 재빌드 가능(DEC-002). 서버 `pull --rebase` 가 외부 변경(사람 교정)을 가져오면, **변경된 md 집합에 대해 그래프 index/edge를 재빌드**해야 교정이 그래프에 반영된다.
  - 재빌드는 기존 증분 스캔 경로(content_hash 비교, startup scan/apply 인덱싱)를 재사용한다.
  - 이 재인덱싱 없이는 사람의 관계 문서 교정이 그래프 엣지/노드에 반영되지 않는다(계약 필수).
  - 트리거 시점(pull 직후 동기 vs 별도 잡)은 §9 OQ.

## 7. Credentials & Config

- push 크리덴셜은 `.env`(배포 시크릿):
  - `AXKG_DOCS_GIT_TOKEN` — GitHub PAT(fine-grained, 대상 ax-graph, contents:write).
  - GitHub email·author 이름 — git identity(axkg-bot).
- remote: `https://x-access-token:${AXKG_DOCS_GIT_TOKEN}@github.com/kknaks/ax-graph.git`. **토큰은 커맨드 실행 시에만 URL에 주입, `.git/config`에 영속 금지**(mediness `_remote_url_with_token` 미러). 에러 메시지·로그에서 토큰 마스킹.
- author 이름·email: `AXKG_DOCS_GIT_AUTHOR_NAME`(axkg-bot), `AXKG_DOCS_GIT_AUTHOR_EMAIL`(GitHub email).
- 플래그: `AXKG_DOCS_GIT_SYNC_ENABLED`(기본 off→검증 후 on), `AXKG_DOCS_GIT_REMOTE`, `AXKG_DOCS_GIT_BRANCH=main`.
- 실 배선 위치: 루트 `.env`(런타임) + `apps/api/.env.example`(템플릿, 선언 완료). 시크릿은 커밋 금지.

## 8. Verification

- 스위치오버(sync off): sparse-checkout 마운트 교체 후 api `/health`·qmd 인덱스 정상.
- 사람 교정: 로컬 `documents/` 1파일 수정 push → 서버 pull --rebase → 재인덱싱 반영 확인.
- sync on: 게이트 1건 승인 → github ax-graph main 에 `documents/` 커밋, CI **미발동** 확인.
- 충돌: 같은 파일 양쪽 수정 → 알림·정지, 강제 push 없음 확인.

## 9. Open Questions

- OQ: origin 바이너리(.docx) git-lfs 여부(용량 임계) — DEC-010 OQ-002.
- OQ: 다중 api 레플리카 commit 직렬화 — DEC-010 OQ-003.
- OQ: 재인덱싱 트리거를 pull 직후 동기 실행할지, 별도 잡으로 뺄지.
- ~~충돌 전략 A vs B~~ → **(B) reset-first 결정(2026-07-24)**. §3.
- OQ: mediness식 별도 폴링 `pull --ff-only` 루프(사람 교정 선반영+재인덱싱 구동)를 둘지, 승인 시 흡수만으로 충분할지.
