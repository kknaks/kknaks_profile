# Output schema

Return one JSON object with every top-level key below. Use `null` for the inactive payload.

```json
{
  "schema_version": "1.0",
  "kind": "idea",
  "title": "한국어 제목",
  "slug": "lowercase-kebab-case",
  "summary": "핵심 한 줄",
  "tags": ["tag"],
  "intent": null,
  "source": null,
  "idea": {
    "original": "사용자 원문",
    "refined": "정리된 아이디어",
    "problem": "해결하려는 문제",
    "expected_value": "기대 효과",
    "open_questions": ["열린 질문"]
  },
  "reference": null,
  "connection_candidates": [
    {"target": "existing-stem", "reason": "연결 근거", "confidence": 0.8}
  ]
}
```

For `kind=reference`, set `idea` to null and use:

```json
{
  "source": {
    "url": "https://...",
    "type": "youtube",
    "title": "원문 제목",
    "author": "저자 또는 채널",
    "publisher": null,
    "published_at": null,
    "accessed_at": "ISO-8601",
    "external_id": null
  },
  "reference": {
    "overview": "개요",
    "context": "출처와 맥락",
    "key_claims": ["핵심 주장"],
    "concepts": [{"name": "개념", "description": "설명"}],
    "evidence": ["근거와 사례"],
    "applications": ["에이전트 해석임을 드러낸 적용 가능성"],
    "limitations": ["한계와 검증 필요 사항"],
    "notes": "추가 참고"
  }
}
```

All required strings must be non-empty. Confidence must be between 0 and 1.
