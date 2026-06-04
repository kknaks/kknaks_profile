---
name: youtube-content
description: YouTube ID 하나를 받아 persona/contents/ 에 status: pending 콘텐츠 stub 문서를 만든다. 서버의 content enrich 잡이 pending 문서를 감지해 메타/자막/본문을 채우고 published 로 전환한다.
allowed_tools: [Read, Write, Bash]
runs_scripts:
  - "../../scripts/youtube_content_stub.py"
---

# YouTube Content

YouTube 영상 업로드용 빈 양식을 만든다. 이 스킬의 책임은 **pending stub 생성까지만**이다.

서버는 `persona/contents/C-*.md` 중 `status: pending`인 문서를 감지하고, `youtubeId`로 YouTube 메타데이터와 자막을 가져와 본문을 채운 뒤 `status: published`로 바꾼다.

## When to use

- 사용자가 YouTube ID만 주고 "콘텐츠 올려줘", "유튜브 양식 만들어줘", "pending으로 박아줘"라고 요청할 때
- 영상 교안 본문을 직접 작성하지 않고 서버 enrich 잡에 맡길 때

## Input

필수:

```text
youtubeId: H-jSrhvnaLY
```

선택:

```text
intent: Redis 싱글 스레드 성능 관점으로 강조
```

## What to create

`persona/contents/`에서 가장 큰 `C-NNN` 다음 번호로 파일을 만든다.

```text
persona/contents/C-019-pending.md
```

frontmatter 최소 양식:

```yaml
---
type: content
id: C-019
date: "2026.06.01"
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

제목과 요약은 서버 부팅 검증 통과용 placeholder다. enrich 잡은 pending 문서의 제목/요약/본문을 YouTube 메타와 LLM 결과로 덮어쓴다.

## How to run

```bash
python3 .agent/scripts/youtube_content_stub.py H-jSrhvnaLY
```

intent가 있으면 두 번째 인자로 전달한다.

```bash
python3 .agent/scripts/youtube_content_stub.py H-jSrhvnaLY "Redis 싱글 스레드 성능 관점으로 강조"
```

## Rules

- YouTube ID만 받는다. 전체 URL이 들어오면 `v=` 또는 `youtu.be/` 뒤의 ID만 추출한다.
- 기존 파일을 덮어쓰지 않는다.
- `status`는 반드시 `pending`으로 둔다.
- 본문은 비워 둔다. 서버 enrich 잡이 본문을 생성한다.
- 사람이 직접 YouTube 메타데이터를 추정해 채우지 않는다.
- 생성 후 사용자가 원하면 git commit/push 한다. push 이후 서버 webhook/scheduler가 pending 문서를 처리한다.

## Output

성공 시 생성한 파일 경로와 ID를 보고한다.

```text
created: persona/contents/C-019-pending.md
id: C-019
youtubeId: H-jSrhvnaLY
status: pending
```
