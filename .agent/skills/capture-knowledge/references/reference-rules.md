# Reference rules

Build a study-quality reference while preserving attribution boundaries.

- `overview`: what the source covers and why it matters.
- `context`: author/channel, publication context, audience, and source scope when available.
- `key_claims`: claims explicitly supported by supplied source material.
- `concepts`: terms required to understand those claims.
- `evidence`: examples, data, demonstrations, or reasoning present in the source.
- `applications`: clearly label deductions or possible uses as interpretation.
- `limitations`: source limitations, missing evidence, conflicts, and facts requiring verification.
- `notes`: references explicitly mentioned by the source; otherwise say that none were identified.

Do not fill missing source facts with plausible guesses. If only metadata is available and substantive
content cannot be read, return the `source_unavailable` error instead of generating a reference.
