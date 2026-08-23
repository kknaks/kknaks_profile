---
name: youtube-content
description: YouTube 링크(또는 ID) 하나를 받아 persona/contents/ 에 status: pending 콘텐츠 stub 문서를 만들고 origin/main 에 푸쉬한다. 서버의 content enrich 잡이 pending 문서를 감지해 메타/자막/본문을 채우고 published 로 전환한다.
allowed_tools: [Read, Write, Bash]
runs_scripts:
  - "../../scripts/youtube_content_stub.py"
  - "../../scripts/youtube_content_publish.sh"
---

# YouTube Content

YouTube 링크만 주면 **pending stub 생성 → 커밋 → 푸쉬**까지 자동으로 한다.

서버는 `persona/contents/C-*.md` 중 `status: pending`인 문서를 감지하고, `youtubeId`로 YouTube 메타데이터와 자막을 가져와 본문(8개 H2 섹션)·title·summary·tags를 채운 뒤 `status: published`로 바꾼다. 이 스킬은 본문을 직접 쓰지 않는다 — 빈 양식을 박아 enrich 잡에 맡긴다.

## When to use

- 사용자가 YouTube 링크/ID만 주고 "이거 유튜브 콘텐츠로 만들고 푸쉬해줘", "콘텐츠 올려줘", "pending으로 박아줘"라고 요청할 때
- 영상 교안 본문을 직접 작성하지 않고 서버 enrich 잡에 맡길 때

## Input

필수 — YouTube 링크 또는 ID (둘 다 받음):

```text
https://www.youtube.com/watch?v=H-jSrhvnaLY
https://youtu.be/H-jSrhvnaLY
H-jSrhvnaLY
```

선택 — intent (영상에서 강조하고 싶은 점 한 줄, enrich LLM 에 1순위 컨텍스트로 주입):

```text
Redis 싱글 스레드 성능 관점으로 강조
```

## Flow

1. **stub 생성** — `youtube_content_stub.py` 가 `persona/contents/`에서 가장 큰 `C-NNN` 다음 번호로 `C-NNN-pending.md` 를 만든다. URL 이면 `v=` / `youtu.be/` / `shorts/` 뒤의 ID 만 추출한다.
2. **커밋 + 푸쉬** — `youtube_content_publish.sh` 가 `git add` → `git commit` → fetch/rebase → push 한다. 커밋 시 pre-commit 훅이 `persona/_map.md` 를 재빌드·스테이징하고 persona 검증을 돌린다 (`--no-verify` 쓰지 말 것).
3. **서버 enrich** — push 후 서버 scheduler(10분 interval)가 pending 문서를 잡아 본문을 채우고 `published` 로 커밋·푸쉬한다.

frontmatter 최소 양식 (stub 스크립트가 생성):

```yaml
---
type: content
id: C-019
date: "2026.06.05"
day: "Day 19"
title:
  ko: "Pending YouTube Content"
  en: "Pending YouTube Content"
summary:
  ko: "YouTube enrich 대기 중"
  en: "Pending YouTube enrich"
youtubeId: H-jSrhvnaLY
status: pending
intent: ""
---
```

제목·요약은 서버 부팅 검증 통과용 placeholder다. enrich 잡이 YouTube 메타와 LLM 결과로 덮어쓴다.

## How to run

링크만 받았으면 두 스크립트를 순서대로 실행한다.

```bash
# 1) stub 생성 — 출력의 created 경로를 받아둔다
python3 .agent/scripts/youtube_content_stub.py "https://www.youtube.com/watch?v=H-jSrhvnaLY"

# 2) 그 경로로 커밋 + 푸쉬
.agent/scripts/youtube_content_publish.sh persona/contents/C-019-pending.md
```

intent 가 있으면 stub 스크립트 두 번째 인자로 넘긴다.

```bash
python3 .agent/scripts/youtube_content_stub.py "https://youtu.be/H-jSrhvnaLY" "Redis 싱글 스레드 성능 관점으로 강조"
```

## Rules

- 링크/ID 외엔 사람이 YouTube 메타데이터를 추정해 채우지 않는다. 빈 양식만 박는다.
- `status` 는 반드시 `pending`. 본문은 비워 둔다 — 서버가 채운다.
- stub 스크립트는 기존 파일을 덮어쓰지 않는다 (id 충돌 시 그대로 종료).
- 커밋은 훅을 거친다 (`--no-verify` 금지). 훅이 `_map.md` 재빌드·스테이징과 persona 검증을 담당한다.
- **rebase 충돌 가드** — 서버가 같은 브랜치에 푸쉬하므로 자동 생성물 `persona/_map.md` 에서 충돌날 수 있다. publish 스크립트는 unmerged 가 `persona/_map.md` **단독일 때만** 재빌드로 해소하고, 그 외(예: stub id 충돌)면 `rebase --abort` 후 **푸쉬하지 않고 중단**한다. 중단되면 사용자에게 충돌 경로를 보고하고 수동 대응을 요청한다.

## Output

성공 시 생성·푸쉬 결과를 보고한다.

```text
created: persona/contents/C-019-pending.md
id: C-019
youtubeId: H-jSrhvnaLY
status: pending
pushed: persona/contents/C-019-pending.md (chore: content C-019 pending (youtubeId H-jSrhvnaLY))
```

push 가 충돌로 중단되면 충돌 경로를 그대로 전달하고 멈춘다.
