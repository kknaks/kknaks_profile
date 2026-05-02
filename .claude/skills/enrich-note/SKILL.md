---
name: enrich-note
description: 단일 노트 .md 파일의 본문을 분석해 frontmatter `stack`(기술 스택) + `links`(연관 노트) 자동 채움. 끝나면 `persona/_map.md` 갱신. 단일 책임 — 파일 1개. 폴더 일괄은 외부 loop. 트리거 — 자연어 "노트 풍부화 / 이 파일 enrich / persona/notes/.../X.md 처리해줘" 또는 폴더 단위 "bitcamp 다 돌려" (이때 외부 loop 으로 파일별 호출).
allowed_tools: [Read, Edit, Bash, Glob, Grep]
reads_files:
  - "[[../../../persona/notes/<group>/<file>.md]]"
  - "[[../../../persona/_meta.yaml]]"
writes_files:
  - "[[../../../persona/notes/<group>/<file>.md]] (frontmatter 만 갱신, body 보존)"
  - "[[../../../persona/_map.md]] (build_persona_map.py 가 갱신)"
runs_scripts:
  - "[[scripts/build-map.sh]]"
---

# enrich-note

페르소나 노트 frontmatter 를 본문 기반으로 보강. 단일 파일 단위.

## When to use

- 사용자가 새 노트 .md 박고 "이 파일 처리해줘" / "이 노트 풍부화"
- 레거시 노트 일괄 보강 (외부 loop) — "persona/notes/bitcamp 다 돌려"
- PostToolUse Write hook (추후) — 새 .md 자동 trigger

## How to invoke

자연어 + 파일 경로:

```
이 파일 enrich 해줘 — persona/notes/bitcamp/2025-03-15-spring-mvc.md
```

또는 폴더 일괄 시 외부 loop 가 파일별 호출:

```
for f in persona/notes/bitcamp/*.md; do
  invoke enrich-note "$f"
done
```

## What it does

순서:

1. **Read** — 파일 frontmatter + body 추출
2. **Glob** — 같은 group 폴더의 다른 .md list (link 후보 풀)
3. **Grep** — 후보 파일들의 `^title:` 한 줄씩 추출 (title-only context)
4. **본문 분석** — `stack` + `links` 추론 (rules.md 따라)
5. **Edit** — frontmatter 만 갱신 (`stack`, `links` 추가/덮어쓰기. 다른 필드 보존)
6. **Bash** — `scripts/build-map.sh` 실행 → `persona/_map.md` 갱신

본문이 빈약(< 50자)하거나 추론 어려우면 빈 배열로 두고 skip 메시지.

## Output

처리 결과 한 줄 요약:

```
✓ persona/notes/bitcamp/2025-03-15-spring-mvc.md
  stack: [Java, Spring Boot, JPA]
  links: [2025-03-14-spring-intro, 2025-03-16-spring-jpa]
  map: 갱신 (155 노트)
```

skip:

```
○ persona/notes/.../empty.md — body 빈약, skip
```

## Rules / Examples / Scripts

- 추론 룰 (stack 정의, links 정확도, frontmatter 보존) — [`rules.md`](rules.md)
- before / after 예제 — [`examples/`](examples/)
- _map.md 갱신 helper — [`scripts/build-map.sh`](scripts/build-map.sh)

## 안전 룰셋

- 단일 파일 처리. 일괄은 외부 loop. SKILL 내부에서 폴더 순회 X.
- frontmatter `title` / `date` / `tags` 절대 안 건드림 — `stack` / `links` 만 추가.
- links slug 는 실제 파일 존재 확인 (Glob) — dead link 박지 말 것.
- body 내용 변경 X — frontmatter 만 Edit.
- 백엔드는 .md 변경 자동 reload 라 별도 trigger 불요.
