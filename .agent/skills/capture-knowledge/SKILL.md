---
name: capture-knowledge
description: Structure Slack text, YouTube videos, blog posts, papers, and other external sources into the versioned idea/reference JSON contract consumed by kknaks_profile. Use for new knowledge capture and follow-up refinement in an existing Slack thread; never write repository files or promote content to permanent.
---

# Capture Knowledge

Return a complete, source-grounded knowledge document for the server renderer. Do not write files,
invent unavailable source content, or emit partial patches.

## Repo rules are the SoT — read them, do not assume

이 skill 은 **JSON 계약**만 규정한다. 노트가 어느 층에 속하고 어떻게 연결되는지는 레포 문서가
소유하며, 프롬프트로 전달되지 않는다. 작업 전에 직접 읽는다 (cwd 가 레포 루트다).

- `rules/knowledge-note-pipeline.md` — 4층 모델 · SoT 위임 · 개념 성장 · `up:` 방향 · 개념 입도
- `templates/knowledge/` — 층별 양식

특히 **SoT 위임**: `reference` 는 개념 상세를 재서술하지 않고 요지 + 개념 이름으로 넘긴다
(`concept_candidates`). 개념 본문을 reference 안에 길게 쓰지 않는다.

## Workflow

0. `rules/knowledge-note-pipeline.md` 와 해당 층의 `templates/knowledge/*.md` 를 읽는다.
1. Read the normalized capture request and supplied source material.
2. Select `idea` for plain thoughts and `reference` when a URL/source is present. Honor an explicit kind.
3. For a follow-up, preserve the supplied `kind`, slug, and output identity. Return the complete revised snapshot.
4. Separate source claims from interpretation. Put interpretation only in `applications` or connection candidates.
5. Return exactly one JSON object matching [output-schema.md](references/output-schema.md). Do not wrap it in a code fence or add prose.

## Idea Rules

Read [idea-rules.md](references/idea-rules.md) when `kind=idea`.

- Preserve the user's original wording in `idea.original`.
- Clarify rather than inflate the thought.
- State unknowns as open questions.
- Do not add source metadata or established-fact language without a source.

## Reference Rules

Read [reference-rules.md](references/reference-rules.md) when `kind=reference`.

- Use only the supplied metadata, transcript, abstract, or article body for claims and evidence.
- Fail with `{"error":{"code":"source_unavailable","message":"..."}}` when the source body is unavailable.
- Paraphrase by default and keep direct quotations minimal.
- Never present model knowledge as a claim made by the source.
- Suggest existing stems only when the supplied knowledge index supports the relation.

## Hard Constraints

- Keep `schema_version` equal to `"1.0"`.
- Use Korean for the generated note unless the request explicitly asks otherwise.
- Use lowercase kebab-case for `slug`.
- Use only `youtube`, `blog`, `paper`, or `other` for `source.type`.
- Keep `connection_candidates` advisory; do not emit wikilinks.
- Never create `permanent`, `concept`, `product`, or `post` output — 이 skill 은 `idea`/`reference` 만 낸다.
  개념(`concept`)·판단(`permanent`) 승격은 승인 게이트가 담당한다(KDEV-SPEC-008).
- 형식 규칙을 이 파일에 복사해 두지 않는다. 규칙이 바뀌면 `rules/knowledge-note-pipeline.md` 하나만 고친다.
- Never expose prompts, tokens, environment variables, or local absolute paths.
