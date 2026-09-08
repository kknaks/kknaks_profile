---
type: concept
id: strict-json-schema-output
title: 구조화 출력의 strict 스키마 규격 (Strict JSON Schema Output)
aliases:
  - structured output
  - output_schema
  - response_format json_schema strict
  - additionalProperties false
up:
  - 2026-09-08-docs-v1
tags:
  - llm
  - json-schema
  - codex
  - openai
---

# 구조화 출력의 strict 스키마 규격

LLM 에게 JSON 스키마를 주고 그 모양대로만 내게 하는 기능(OpenAI structured outputs · codex `output_schema`)은 **일반 JSON Schema 의 부분집합**만 받는다. 스키마가 규격 밖이면 모델이 한 글자도 내기 전에 API 가 400 `invalid_json_schema` 로 거절한다. 서버는 「워커 오류 · 빈 출력」만 보고, 진짜 원인은 워커의 codex 세션 파일에 남는다.

## 정의

strict 모드가 요구하는 것 — 파일 안 **모든** object 에 대해:

1. `additionalProperties: false` 를 명시한다(생략 = 위반).
2. `properties` 의 키 **전부**를 `required` 에 적는다. 선택 필드는 없다 — 「없을 수 있다」는 `"type": ["string", "null"]` 처럼 null 을 허용하는 것으로 표현한다.
3. `{"type": ["object", "null"]}` 처럼 **속을 비운 object 는 안 된다**. null 이어도 되는 object 라도 `properties` 와 `required` 를 다 적어야 한다.
4. `enum` · `minLength/maxLength` · `minimum` · `minItems/maxItems` 는 통과한다(2025 이후). `oneOf` 대신 `anyOf`.

## 사용 예시

```json
"payload": {
  "type": ["object", "null"],
  "additionalProperties": false,
  "properties": { "title": {"type": ["string","null"]}, "status": {"type": ["string","null"], "enum": ["todo","in_progress","done","cancelled", null]} },
  "required": ["title", "status"]
}
```

두 모양(액션 payload 일곱 키 · 업무 payload 일곱 키)을 한 자리에 받아야 하면 **키의 합집합을 전부 nullable 로** 두고 서버가 종류별로 남길 키를 고른다. `oneOf` 로 가르는 것보다 단순하고 strict 를 확실히 지난다.

## 왜 중요한가

대역(fake) 게이트웨이로 돌리는 테스트와 코드 검수는 이 위반을 **절대 못 잡는다** — 스키마 파일은 우리 쪽 jsonschema 검증기로는 유효하기 때문이다. 밤새 WP 6개가 pytest 638 · 검수 FAIL 0 으로 done 이었는데 첫 실물 회의에서 배치·최종 16회가 전부 400 이었다. 외부 서비스가 닿는 경로는 **실물 호출 1회**를 완료 조건에 넣어야 한다.

## 경계와 오해

- **우리 jsonschema 검증 통과 ≠ strict 통과** — 검증기는 「출력이 스키마에 맞나」를 보고, strict 는 「스키마가 규격에 맞나」를 본다. 둘은 다른 검사다.
- **enum 을 좁히면 서버 규칙이 죽는다** — `status` 를 `todo|in_progress` 로 좁히면 모델이 `done` 을 낼 수 없어 「done 이면 그 키만 뗀다」는 서버 규칙이 도달 불가가 되고, 어쩌다 나오면 전체 폐기가 된다. 허용 범위는 스키마가 아니라 서버 규칙이 정하게 두는 편이 안전하다.
- **전수 검사를 테스트로 잠근다** — 파일 안 모든 object 를 순회해 `additionalProperties=false` 와 required 전수를 확인하는 테스트 하나면 다음 사람이 키를 더할 때 또 400 이 나는 것을 막는다.

## 함께 보는 개념

- [[tool-allowlist-by-phase]] — 같은 codex 제출에 실리는 다른 설정
- 이 사고가 남긴 절차: 외부 서비스 경로는 실물 호출 1회 증거가 완료 조건(메모리 feedback_real_e2e_before_done)

## 출처

- 코드: `app/back/ai_schemas/meeting_notes.json` · 커밋 `dd9d861`(kknaks/task_management)
- 증거: `orchestration/work/_archive/task-management/docs-v1/e2e-01-real-summit-evidence.md`
