---
name: capture-knowledge
description: Structure Slack text, YouTube videos, blog posts, papers, and other external sources into the versioned idea/reference JSON contract consumed by kknaks_profile. Use for new knowledge capture and follow-up refinement in an existing Slack thread; never write repository files or promote content to permanent.
---

# Capture Knowledge

Return a complete, source-grounded knowledge document for the server renderer. Do not write files,
invent unavailable source content, or emit partial patches.

## Workflow

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
- Never create `permanent`, `product`, or `post` output.
- Never expose prompts, tokens, environment variables, or local absolute paths.
