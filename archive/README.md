# archive

안 쓰게 된 노트의 cold 장기기억. **층이 아니라 상태**라 `resources/` 밖 최상위에 있다([[decision-018-resources-layout-and-sot-naming|KDEV-DEC-018]]).

여기 놓이는 노트는 **원래 타입을 유지**한다(`reference`·`concept`). 폴더가 바뀔 뿐 타입은 그대로다.

## 여기 두는 것

- 현재 안 쓰지만 버리기는 아까운 노트. **inbound 링크 보존을 위해 stem 을 유지한 채** 폴더만 내린다.

## 여기 두지 않는 것

- 현역 개념 → `resources/concept/`
- 현역 자료 → `resources/source/`
- 제품 버전 동결본 → `products/{제품}/_archive/` (**다른 것이다** — 그쪽은 버전 컷오프 스냅샷이라 제품 폴더 안에 남는다)

## quick-rule

- 내릴 때 **파일명 stem 을 바꾸지 않는다**(stem 기반 링크라 보존된다).
- 부활 = 원래 층 폴더로 되돌린다(`resources/concept/` 또는 `resources/source/`).
- 평소 스캔에서 archive 를 **제외한다**(cold). 명시 요청 시에만 읽는다(D-005).
- 활성 노트가 archived 를 `up:` 하면 L6 WARN 이다 — 계보가 죽은 것을 딛고 서 있다는 신호다.

## 작성 규약 (SSOT)

- 작성 규칙: `rules/knowledge-note-pipeline.md`
- 디렉토리 계약: [[spec-001-directory-structure|KDEV-SPEC-001]]
- 생명주기: [[spec-003-knowledge-workflow|KDEV-SPEC-003]]
