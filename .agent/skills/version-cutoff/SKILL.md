---
name: version-cutoff
description: 제품이 한 버전으로 배포·심사 나간 시점에 현재 제품 문서 전체(00~70)를 `products/<product>/_archive/vX.Y.Z/`로 동결(스냅샷)할 때. 복사본 frontmatter를 status archived로 마킹하고, 파일명·wikilink에 `v1_0_1-` 버전 prefix를 달아 Obsidian graph에서 live와 충돌 없이 자기완결적으로 탐색되게 한다. live 문서는 그대로 두고 다음 버전 작업을 이어간다. 트리거 "버전 컷오프" / "스펙 아카이브" / "vX.Y.Z 동결".
allowed_tools: [Read, Bash]
runs_scripts:
  - "../../scripts/product_version_cutoff.py"
---

# version-cutoff — 버전 컷오프 (제품 문서 동결)

## When to use

제품이 한 버전으로 **배포되거나 심사에 나간 시점**에, 그 버전의 제품 문서 상태를 동결해 두고 싶을 때. live spec/decision/work는 다음 버전 작업으로 계속 바뀌므로, "이 버전에 무엇이 나갔는가"를 트리에서 바로 볼 수 있게 스냅샷을 남긴다.

- 결과: `products/<product>/_archive/vX.Y.Z/`에 컷오프 시점 제품 문서 전체(00~70) 동결본 + `_archive/README.md` 인덱스
- 동결본 frontmatter는 `status: archived` + `original_status` + `archived_version` + `archived_at`로 마킹된다 (tags의 `status/*`도 `status/archived`로)
- 동결본 `.md` 파일명과 내부 링크(wikilink·마크다운 상대링크)에 버전 prefix `v1_0_1-`가 붙는다 → basename이 전역 유니크해져 Obsidian graph에서 live 문서와 충돌하지 않고, 아카이브 내부 링크는 같은 버전 사본을 가리켜 과거 버전 그래프가 자기완결적으로 탐색된다

## When NOT to use

- **이미 지나간 과거 버전**(예: 이미 1.0.1까지 나온 상태에서 1.0.0을 동결): live 트리는 최신 상태라 과거 버전을 재현할 수 없다. 과거 버전은 git tag/commit에서 `git checkout` 후 동결하거나, 동결하지 않고 git 이력으로만 둔다. 이 skill은 **현재 트리 상태**를 현재 버전으로 동결한다.
- release **노트**만 필요할 때 → `60-release/release-*.md` (문서 스냅샷 아님). 컷오프는 노트와 별개로 문서 전체를 굳히는 것.

## Input

| 인자 | 의미 | 예 |
|---|---|---|
| `product` | 제품 slug | `mac-remote` |
| `version` | 버전 (v 접두 자동 정규화) | `1.0.1` → `v1.0.1` |
| `--date` | (선택) archived_at, 기본 오늘 KST | `2026-06-08` |
| `--no-assets` | (선택) 70-runbook/assets 등 바이너리 제외, 텍스트 문서만 | — |
| `--dry-run` | (선택) 복사 없이 계획만 출력 | — |

> 자산(아이콘·스크린샷)은 버전마다 중복 복사되어 용량이 커질 수 있다. 문서만 동결하면 되는 경우 `--no-assets`로 가볍게 가져간다.

## Flow

1. **dry-run으로 확인** — 대상 경로·파일 수·source commit·자산 포함 여부를 먼저 본다.
   ```bash
   python3 .agent/scripts/product_version_cutoff.py mac-remote 1.0.1 --dry-run
   ```
2. **컷오프 실행** — 전체 트리를 `_archive/vX.Y.Z/`로 복사하고 frontmatter를 archived로 마킹, 인덱스 갱신.
   ```bash
   python3 .agent/scripts/product_version_cutoff.py mac-remote 1.0.1 --date 2026-06-08
   ```
3. **파이프라인 검증** — 아카이브가 검증을 깨지 않는지 확인.
   ```bash
   python3 .agent/scripts/product_doc_pipeline.py --strict
   ```
4. **보고** — 동결 버전, 복사 용량, 마킹된 문서 수, 인덱스 경로.

## Rules

- **읽기 전용 규약**: 동결본(`_archive/vX.Y.Z/`)은 수정하지 않는다. 오타·갱신은 live 문서에서 하고, 필요하면 다음 컷오프에 반영된다.
- **덮어쓰지 않음**: 같은 버전 폴더가 이미 있으면 스크립트가 중단한다. 다시 동결하려면 기존 폴더를 의도적으로 지운 뒤 실행.
- **live는 그대로**: 컷오프는 복사만 한다. live 문서의 `status`(implemented/released 등)는 바뀌지 않는다.
- **검증 안전성**: 검증기(`product_doc_pipeline.py`)는 `products/` 최상위만 제품으로 순회하고 release/work/runbook 글롭이 모두 비재귀라, 중첩된 `_archive/` 동결본은 재검증되지 않는다. 그래서 `status: archived` 마킹이 release/runbook 검증을 깨지 않는다. (검증기에 재귀/wikilink 검증을 추가할 때는 `_archive/`를 제외해야 한다.)

## Output

```text
Product Version Cutoff
- product: mac-remote
- version: v1.0.1
- archived_at: 2026-06-08
- source commit: a5676d0
- dest: products/mac-remote/_archive/v1.0.1
- copied: 2.3M
- marked archived: 34 md files
- index: products/mac-remote/_archive/README.md
- done
```

## Related

- 스크립트: `.agent/scripts/product_version_cutoff.py`
- 검증: `.agent/scripts/product_doc_pipeline.py`
- 규칙: `rules/product-doc-pipeline.md`
- release 노트(별개): `products/<product>/60-release/release-*.md`
