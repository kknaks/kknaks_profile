---
name: import-project
description: 외부 레포 디렉토리 1개를 분석해 persona/projects/<slug>.md 를 spec-01 §3.3 형식으로 신규 생성. frontmatter (id/title/summary/category/status/stack/date/links/visible) 자동 추출 + 본문 7섹션 (개요/기술스택/주요기능/아키텍처/핵심 구현/마주친 문제/회고) 자동 분석. 풀스택 레포 정석적 분석 — 프론트(라우트/컴포넌트), 백엔드(API/비즈니스 로직), 인프라(Docker/CI/CD), DB 스키마 모두 봄. 단일 책임 — 레포 1개. 일괄은 외부 loop. 트리거 — "이 레포 import — workspace/foo-app" 또는 "workspace 다 돌려" (외부 loop).
allowed_tools: [Read, Glob, Grep, Bash, Write, Edit]
reads_files:
  - "[[<repo-dir>/README.md]]"
  - "[[<repo-dir>/package.json]] (Node 프로젝트)"
  - "[[<repo-dir>/pyproject.toml]] · [[<repo-dir>/requirements.txt]] (Python)"
  - "[[<repo-dir>/build.gradle]] · [[<repo-dir>/pom.xml]] (Java)"
  - "[[<repo-dir>/Dockerfile]] · [[<repo-dir>/docker-compose.yml]]"
  - "[[<repo-dir>/.github/workflows/*.yml]]"
  - "[[<repo-dir>/.git/config]] (remote URL)"
  - "[[../../../persona/_meta.yaml]] (category enum)"
  - "[[../../../persona/projects/]] (기존 P-NN id)"
writes_files:
  - "[[../../../persona/projects/<slug>.md]] (신규 생성)"
runs_scripts: []
---

# import-project

외부 레포 디렉토리 1개 → `persona/projects/<slug>.md` 신규 생성. 풀스택 정석 분석.

## When to use

- 사용자가 `workspace/` 에 레포 clone 후 "이 레포 import 해줘"
- 폴더 일괄 import 시 외부 loop 이 1개씩 호출

## How to invoke

자연어 + 디렉토리 경로 (필수):

```
이 레포 import — workspace/wine-log
```

옵션 인자:
- `--hidden` — 강제 `visible: false` (회사 레포 등). heuristic 무시.
- `--slug <name>` — 파일명 slug 강제 지정 (default: 디렉토리명 kebab-case)

폴더 일괄:

```
for d in workspace/*/; do
  invoke import-project "$d"
done
```

## What it does

순서:

1. **검증** — 디렉토리 존재 + `.git/` 존재 (Git 레포 가정). 미존재면 abort.
2. **frontmatter 추출** — `rules.md` §1
   - `id` — `persona/projects/*.md` 의 P-NN 최댓값 + 1
   - `slug` — 디렉토리명 kebab-case (또는 `--slug` 인자)
   - `title` — README h1 > package.json/pyproject.toml name > 디렉토리명
   - `summary` — README 첫 단락 첫 문장 > package.json description (한 줄, 80자 이내)
   - `stack` — deps 분석 (`rules.md` §2)
   - `category` — heuristic (`rules.md` §3)
   - `status` — `live` (배포 URL 있으면) > `wip` (default) > `archived` (1년+ 무업데이트)
   - `date` — `git log --reverse --format="%ad" --date=format:"%Y.%m" | head -1`
   - `links.repo` — `git remote get-url origin` (ssh→https 변환)
   - `links.live` — README 내 deployed URL heuristic (`https://...` 첫 매치, kknaks.dev 도메인 우선)
   - `visible` — `rules.md` §4 (owner heuristic + `--hidden` override)
3. **본문 분석** — `rules.md` §5. 7섹션 자동 채움:
   - **`# 개요`** — README intro 단락
   - **`# 기술스택`** — 프론트/백엔드/인프라 분리. deps + Dockerfile + .github/workflows
   - **`# 주요기능`** — 라우트 (`app/*`, `pages/*`, `routes/*`) + 핵심 페이지/CLI 명령
   - **`# 아키텍처`** — 디렉토리 트리 + 모듈 분리 + DB 스키마 + 외부 의존
   - **`# 핵심 구현`** — API 라우터 (FastAPI/Express/Spring) + 주요 컴포넌트
   - **`# 마주친 문제`** — `git log --grep="fix|bug|issue"` 패턴 + commit msg
   - **`# 회고`** — README 회고 섹션 (있으면) + commit msg 빈도 패턴
4. **Write** — `persona/projects/<slug>.md` 생성. 기존 파일 존재 시 abort (overwrite X).
5. **출력** — frontmatter 요약 + 분석한 섹션 list + 검토 권장 마커

## Output

성공:

```
✓ persona/projects/wine-log.md (P-02)
  title:    Wine.Log
  category: mobile
  status:   wip
  visible:  true (owner: kknaks)
  stack:    [React Native, TypeScript, Expo, FastAPI, Postgres]
  본문 7섹션 자동 채움 (검토 필수):
    1. 개요         ← README intro 발췌 ✓
    2. 기술스택     ← 자동 분석 ✓
    3. 주요기능     ← 라우트 8개 추출 ✓
    4. 아키텍처     ← 디렉토리 구조 분석 ✓
    5. 핵심 구현    ← API 5개 + 주요 컴포넌트 3개 추출 ✓
    6. 마주친 문제  ← (자동 추론 — 검토 필요)
    7. 회고         ← (자동 추론 — 검토 필요)
```

skip / 에러:

```
○ persona/projects/foo.md — 이미 존재. abort. (--force 옵션 X)
× workspace/bar — .git 없음. Git 레포 아님. abort.
× workspace/baz/README.md 없음. summary 추출 불가. frontmatter TBD 박고 진행.
```

## Rules / Examples

- 추출 룰 (frontmatter / stack / category / visible / 본문 분석) — [`rules.md`](rules.md)
- before / after 예 — [`examples/`](examples/) (TBD — 첫 사용 후 추가)

## 안전 룰셋

- **단일 디렉토리 처리.** 일괄은 외부 loop. SKILL 내부에서 폴더 순회 X.
- **기존 `persona/projects/<slug>.md` 존재 시 overwrite X.** 사용자가 직접 정정하거나 다른 slug 사용.
- **외부 레포 코드 변경 X.** read-only.
- **본문 7섹션 *순서·제목* 고정** (spec-01 §3.3). 사용자 임의 추가·삭제 X.
- **`# 마주친 문제` / `# 회고`는 LLM 추론** — 거짓 박힐 위험. 출력에 "(자동 추론 — 검토 필요)" 마커 박음.
- **`visible: false` 가 default가 아님** — heuristic 으로 owner 본인이면 true. 회사 레포면 사용자가 `--hidden` 박는 책임.
- **assets** — 레포 안 스크린샷이 있으면 `persona/assets/projects/<P-NN>/` 으로 복사 권장 (수동, 본 skill 범위 밖).
- 백엔드는 .md 변경 자동 reload 라 별도 trigger 불요.
