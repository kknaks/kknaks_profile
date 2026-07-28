# permanent/concept

지식의 최소 단위. 여기 놓이는 노트의 타입: `concept`, 층: `concept`.

한 파일 = 한 개념. **flat** — 하위 디렉토리를 두지 않는다(개념은 분류 트리가 아니라 링크 그래프로 조직된다).

## 여기 두는 것
- "이 개념은 무엇인가"에 답하는 노트. **사실의 SoT**이며 출처에 독립적이다.
- 여러 자료에 걸쳐 나오는 재사용 가능한 개념.

## 여기 두지 않는 것
- "이 자료가 뭐라고 했나" → `reference/`.
- "내 판단·전략" → `permanent/` 루트.
- 안 쓰게 된 개념 → `permanent/archive/`.

## quick-rule
- **`aliases` 필수.** 같은 개념의 다른 이름을 모두 적는다(`stt` → `[Speech-to-Text, 음성인식, ASR]`). 없으면 같은 개념이 두 파일로 갈라져 SoT가 둘이 된다.
- **`up:` 필수.** 자신이 나온 출처(`reference`)를 가리킨다. 출처 없는 개념은 성립하지 않는다.
- **개념은 성장한다.** 같은 개념에 두 번째 출처가 오면 새 파일을 만들지 말고 **기존 노트를 보충**한다 — `up:`과 본문 `[[]]`에 새 출처를 더한다.
- **SoT 위임** — 개념 상세는 여기 한 곳에만 쓴다. `reference`와 `permanent`는 재서술하지 않고 `[[concept]]`로 위임한다.

## 작성 규약 (SSOT)
- 작성 규칙: `rules/knowledge-note-pipeline.md`
- 디렉토리 계약: [[spec-001-directory-structure|KDEV-SPEC-001]]
- 검증 규칙: [[spec-004-graph-validation|KDEV-SPEC-004]]
