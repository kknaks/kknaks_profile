# Product Doc Pipeline Hook

## 목적

AI가 제품 문서를 생성하거나 수정한 뒤 실행해야 하는 후처리 절차를 정의한다.

문서 작성 규칙의 원천은 `rules/product-doc-pipeline.md`다.

## Trigger

아래 경로가 생성되거나 수정되면 실행한다.

```text
products/**
templates/product/**
rules/product-doc-pipeline.md
.agent/hooks/product-doc-pipeline.md
.agent/scripts/product_doc_pipeline.py
```

## 실행 흐름

```text
AI 문서 작업 완료
→ 변경된 product 문서 감지
→ 문서 유형 판별
→ frontmatter / ID / mapping / Obsidian link 정합성 검증
→ index README 갱신
→ product README 갱신
→ product log.md 갱신
→ 재검증
→ 결과 보고
```

## Hook이 해도 되는 일

- 단계별 README index 갱신
- 제품 README map 갱신
- 제품 `log.md`에 기계적 변경 entry 추가
- frontmatter 필수 필드 누락 보고
- ID 형식과 파일명 불일치 보고
- BASE → DEC → SPEC → WORK 연결 누락 보고
- SPEC → Architecture → WORK 연결 누락 보고
- frontmatter `links` 필드의 Obsidian wikilink 누락/깨짐 보고
- `tags`의 `product/*`, `doc/*`, `status/*` 누락 보고
- 명백한 상태 변경 제안

## Hook이 하면 안 되는 일

- 제품 결정 자체를 임의로 내리기
- baseline을 임의로 채택하거나 기각하기
- spec의 기능 계약을 임의로 변경하기
- architecture를 이유로 spec 계약을 우회하기
- work의 구현 범위를 임의로 바꾸기
- 사용자의 의도 없이 새 제품이나 새 문서 유형 만들기

## 검증 항목

- `products/<product>/README.md` 존재
- `products/<product>/log.md` 존재
- `00-baseline/`, `10-decision/`, `20-spec/`, `30-work/` 존재
- `40-architecture/`는 optional. 존재하면 하위 README와 mermaid 기준 검증
- `60-release/`는 optional. 존재하면 release index와 release note frontmatter/섹션 검증
- `70-runbook/`는 optional. 존재하면 runbook index와 runbook frontmatter/필수 섹션(목적/절차) 검증
- 각 단계의 `README.md` 존재
- 개별 문서 frontmatter 필수 필드 존재
- ID 형식 검사
- 파일명과 ID 번호 일치 검사
- baseline → decision → spec → work 참조 무결성 검사
- spec → architecture → work 참조 무결성 검사
- `work_type: release` work의 필수 섹션(심사 체크리스트/제출 기록/심사 결과) 검사
- frontmatter `links` 필드의 Obsidian wikilink 정합성 검사
- frontmatter `tags` 패턴 검사
- 단계 README index와 실제 파일 목록 동기 검사
- `log.md` 변경 entry 누락 검사

## 실행 체크리스트

AI가 제품 문서 작업을 끝낸 뒤 아래 체크리스트를 순서대로 확인한다.

### 1. 변경 감지

- [ ] 변경된 파일이 `products/**`, `templates/product/**`, `rules/product-doc-pipeline.md`, `.agent/hooks/product-doc-pipeline.md`, `.agent/scripts/product_doc_pipeline.py` 중 어디인지 확인했다.
- [ ] 변경된 제품 slug를 확인했다.
- [ ] 변경된 문서 유형을 확인했다: `baseline`, `decision`, `spec`, `work`, `architecture`, `release`, `runbook`, `index`, `log`.

### 2. 구조 검증

- [ ] `products/<product>/README.md`가 있다.
- [ ] `products/<product>/log.md`가 있다.
- [ ] `00-baseline/README.md`가 있다.
- [ ] `10-decision/README.md`가 있다.
- [ ] `20-spec/README.md`가 있다.
- [ ] `30-work/README.md`가 있다.
- [ ] `40-architecture/`가 있으면 `README.md`, `database/README.md`, `system/README.md`, `deploy/README.md`를 확인했다.
- [ ] `60-release/`가 있으면 `README.md`를 확인했다.
- [ ] `70-runbook/`가 있으면 `README.md`와 각 runbook의 필수 섹션(목적/절차)을 확인했다.

### 3. Frontmatter 검증

- [ ] 개별 문서에 `type`, `id`, `title`, `status`, `product`, `created_at`, `updated_at`, `tags`, `links`가 있다.
- [ ] `tags`에 `product/*`, `doc/*`, `status/*`가 있다.
- [ ] `links` 하위에 `baselines`, `decisions`, `specs`, `works`, `releases`, `related`가 있다.
- [ ] `links` 값이 있으면 Obsidian wikilink 형식이다.

### 4. 매핑 검증

- [ ] baseline이 decision으로 연결되는지 확인했다.
- [ ] decision이 baseline/spec으로 연결되는지 확인했다.
- [ ] spec이 decision/work로 연결되는지 확인했다.
- [ ] work가 spec으로 연결되는지 확인했다.
- [ ] `work_type: release` work는 필수 섹션(심사 체크리스트/제출 기록/심사 결과)이 있고, 출시 완료 시 release 연결을 확인했다.
- [ ] architecture가 있으면 관련 spec/work와 연결되는지 확인했다.
- [ ] release가 있으면 관련 spec/work/release와 연결되는지 확인했다.

### 5. Index 갱신

- [ ] baseline 추가/변경 시 `00-baseline/README.md`를 갱신했다.
- [ ] decision 추가/변경 시 `10-decision/README.md`를 갱신했다.
- [ ] spec 추가/변경 시 `20-spec/README.md`를 갱신했다.
- [ ] work 추가/변경 시 `30-work/README.md`와 Spec Coverage를 갱신했다.
- [ ] architecture 추가/변경 시 `40-architecture/README.md` 또는 하위 index를 갱신했다.
- [ ] release 추가/변경 시 `60-release/README.md`를 갱신했다.
- [ ] 제품 전체 상태가 바뀌면 `products/<product>/README.md`를 갱신했다.

### 6. Log 갱신

- [ ] `products/<product>/log.md`에 변경 entry를 추가했다.
- [ ] entry에 날짜, 종류, 관련 ID, 요약, 링크가 있다.

### 7. 재검증과 보고

- [ ] `.agent/scripts/product_doc_pipeline.py`를 실행했다.
- [ ] warnings/errors를 확인했다.
- [ ] 자동으로 판단할 수 없는 결정은 `needs_user_decision`에 남겼다.

## 실행 스크립트

실제 검증/갱신은 아래 스크립트가 담당한다.

```bash
python3 .agent/scripts/product_doc_pipeline.py
```

strict 검증이 필요하면 아래 모드를 사용한다.

```bash
python3 .agent/scripts/product_doc_pipeline.py --strict
```

## 결과 보고 형식

hook 실행 후 AI는 아래 항목을 보고한다.

```text
Product Doc Pipeline
- checked:
- updated:
- warnings:
- errors:
- needs_user_decision:
```
