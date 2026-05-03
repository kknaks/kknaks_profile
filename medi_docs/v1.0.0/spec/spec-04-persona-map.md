---
id: spec-04
type: spec
title: 페르소나 _map.md 빌드 명세 — 옵시디언 호환 자동 인덱스
status: draft
created: 2026-05-01
updated: 2026-05-01
sources:
  - "[[planning-01-portfolio-overview]]"
  - "[[spec-01-persona-md-format]]"
  - "[[adr-03-scheduler-attribution]]"
tags: [spec, persona, map, obsidian, index]
---

# 페르소나 _map.md 빌드 명세

## Summary

`persona/_map.md` 자동 생성 명세. 카테고리별 카운트 + 파일 리스트(위키링크) + notes 그래프 + 백링크 인덱스를 한 페이지에 박아 옵시디언 vault 진입점 역할. 트리거는 git pre-commit hook(사용자 PC, 옵시디언 갱신용) + 백엔드 부팅(홈서버, 메모리 dict와 동시 빌드) 두 곳에서 같은 스크립트 호출. 멱등 — 같은 입력이면 같은 출력.

---

## 1. 빌드 트리거 — pre-commit + 부팅 (멱등)

| 트리거 | 위치 | 목적 |
|---|---|---|
| **git pre-commit hook** | 사용자 PC (`.git/hooks/pre-commit`) | commit 직전 빌드 → 옵시디언이 항상 최신. plan-01에서 hook 설치 단계 명시 |
| **백엔드 부팅 시** | 홈서버 (`back/main.py` `startup`) | 페르소나 로드와 함께 빌드. webhook reload 시에도 자동 갱신 |
| ~~수동 실행~~ | — | 옵션 (디버깅용). 트리거 정책 X |

**같은 스크립트** (`scripts/build_persona_map.py`)를 두 트리거가 호출. 멱등(같은 입력 → 같은 출력)이라 어느 쪽이든 실행 결과 일치.

### 1.1 옵션 비교 (왜 두 트리거인가)

| 옵션 | 옵시디언 갱신 | 백엔드 활용 | 사용자 부담 |
|---|---|---|---|
| 부팅 시만 | ❌ stale | ✅ | 0 |
| pre-commit만 | ✅ | git pull 후 재시작 필요 | hook 1회 셋업 |
| **두 곳 다** | ✅ | ✅ | hook 1회 셋업 |
| 수동만 | △ 까먹음 | ❌ | 매번 |

→ pre-commit + 부팅 두 곳이 옵시디언 친화 + 백엔드 활용 동시 만족. 같은 스크립트라 코드 중복 X.

---

## 2. _map.md 출력 포맷 (옵시디언 호환)

### 2.1 구조 (예시)

```markdown
# persona/_map.md

> 자동 생성 (build_persona_map.py, 2026-05-01 14:32 KST). 수동 편집 X.

_총 38 파일 (profile 1 / career 4 / projects 6 / notes 18 / contents 5 / daily 4)_

## profile
- [[profile]] 이건학 — Backend Engineer

## career (display_order 오름차순)
- [[career/stealth-ai]] Stealth AI Co. (2025.06 — present)
- [[career/ssafy]] SSAFY 12기 (2025.01 — 05)
- [[career/self-study]] 독학 (2024.07 — 12)
- [[career/college]] 비전공 학사 (— 2024.06)

## projects (categories: web 3 · cli 1 · bot 2)
- [[projects/homelab-console]] Homelab Console (web · wip)
- [[projects/vault-sync]] Vault Sync (cli · live)
- ...

## notes (clusters: ai 4 · py 5 · infra 3 · cs 4 · misc 2)
- [[notes/python-asyncio]] Python asyncio 기본기 (py · 2026.04.10)
- [[notes/fastapi-di]] FastAPI Dependency Injection (py · 2026.04.05)
- ...

## contents (총 5개, 최근 5)
- [[contents/C-005-postgres-index]] Day 05 — Postgres 인덱스 (2026.04.30)
- [[contents/C-004-uvicorn]] Day 04 — Gunicorn vs Uvicorn (2026.04.29)
- ...

## daily (총 4개, 최근 5)
- [[daily/2026-04-30]] (2026.04.30)
- [[daily/2026-04-29]] (2026.04.29)
- ...

## 위키링크 그래프 (notes)
- python-asyncio → fastapi-di, asyncio-event-loop
- fastapi-di → python-asyncio, postgres-index
- ...

## 백링크 인덱스 (notes)
- python-asyncio: ← fastapi-di, daily/2026-04-29
- fastapi-di: ← python-asyncio, contents/C-001-fastapi-di
- ...
```

### 2.2 옵시디언 호환 규칙

- **위키링크**: `[[file-path]]` 또는 `[[id]]` 형식. 옵시디언이 자동 인식 → jump 가능
- **헤딩**: `## category` — 옵시디언 outline 사이드바에 노출
- **그래프 뷰**: `[[id]]` 위키링크가 노드/엣지로 자동 시각화
- **파일 경로**: 옵시디언은 `.md` 확장자 생략 가능. 본 명세는 `[[career/stealth-ai]]` 형식 (확장자 X). 옵시디언 vault root = `persona/`로 가정

### 2.3 정렬 규칙 (멱등 보장)

| 카테고리 | 정렬 |
|---|---|
| career | `display_order` 오름차순 |
| projects | `category` 그룹 → 같은 그룹 내 `date desc` |
| notes | `group` 그룹 → 같은 그룹 내 `id` 알파벳순 |
| contents | `id` 내림차순 (C-005, C-004, ...) |
| daily | `date` 내림차순 |
| 위키링크 그래프 | source `id` 알파벳 → target `id` 알파벳 |
| 백링크 | target `id` 알파벳 → source `id` 알파벳 |

→ 같은 페르소나 상태면 같은 _map.md. git diff 노이즈 최소화.

---

## 3. 빌드 로직 (`scripts/build_persona_map.py`)

### 3.1 입력

`persona/` 전체 순회:
- `profile.md`
- `career/*.md`
- `projects/*.md`
- `notes/*.md`
- `contents/*.md`
- `daily/*.md`
- `_meta.yaml` (카테고리·클러스터 라벨 + 색상 — 본 spec 시점엔 라벨만 사용)

`activity.yaml`은 _map에 박지 않음 (잡 산출물이라 사람 가시성 가치 적음).

### 3.2 의사 코드

```python
from pathlib import Path
import frontmatter, yaml, re
from collections import Counter, defaultdict

PERSONA = Path("persona")
MAP_PATH = PERSONA / "_map.md"
WIKILINK_RE = re.compile(r"\[\[([a-z0-9\-]+)\]\]")

def build_persona_map():
    # 1. Load all
    profile  = frontmatter.load(PERSONA / "profile.md")
    careers  = sorted(_load_dir("career"),  key=lambda p: p.metadata["display_order"])
    projects = _load_dir("projects")
    notes    = _load_dir("notes")
    contents = sorted(_load_dir("contents"), key=lambda p: p.metadata["id"], reverse=True)
    dailies  = sorted(_load_dir("daily"),    key=lambda p: p.metadata["date"], reverse=True)
    meta     = yaml.safe_load((PERSONA / "_meta.yaml").read_text())

    # 2. Aggregations
    cat_counts = Counter(p.metadata["category"] for p in projects)
    grp_counts = Counter(n.metadata["group"]    for n in notes)

    # 3. Wiki-link graph + backlinks
    edges = []
    backlinks: dict[str, list[str]] = defaultdict(list)
    for n in notes:
        nid = n.metadata["id"]
        for target in WIKILINK_RE.findall(n.content):
            edges.append((nid, target))
            backlinks[target].append(nid)

    # 4. Render markdown
    sections = [
        _header(profile, careers, projects, notes, contents, dailies),
        _section_profile(profile),
        _section_careers(careers),
        _section_projects(projects, cat_counts, meta),
        _section_notes(notes, grp_counts, meta),
        _section_contents(contents),
        _section_dailies(dailies),
        _section_graph(edges),
        _section_backlinks(backlinks),
    ]
    MAP_PATH.write_text("\n\n".join(sections), encoding="utf-8")
```

### 3.3 헤더 줄 (timestamp 포함)

```python
def _header(...) -> str:
    now_kst = datetime.now(KST).strftime("%Y-%m-%d %H:%M KST")
    total = 1 + len(careers) + len(projects) + len(notes) + len(contents) + len(dailies)
    return (
        f"# persona/_map.md\n\n"
        f"> 자동 생성 (build_persona_map.py, {now_kst}). 수동 편집 X.\n\n"
        f"_총 {total} 파일 "
        f"(profile 1 / career {len(careers)} / projects {len(projects)} / "
        f"notes {len(notes)} / contents {len(contents)} / daily {len(dailies)})_"
    )
```

### 3.4 섹션 렌더 (예시 — career)

```python
def _section_careers(careers: list) -> str:
    lines = ["## career (display_order 오름차순)"]
    for c in careers:
        m = c.metadata
        slug = c.path.stem
        org_ko = m["org"]["ko"]
        period = m["period"]
        lines.append(f"- [[career/{slug}]] {org_ko} ({period})")
    return "\n".join(lines)
```

다른 섹션도 같은 패턴 — 카테고리 헤딩 + bullet 리스트 + `[[path/slug]]` 위키링크.

### 3.5 그래프 + 백링크 렌더

```python
def _section_graph(edges: list[tuple[str, str]]) -> str:
    lines = ["## 위키링크 그래프 (notes)"]
    by_source = defaultdict(set)
    for s, t in edges:
        by_source[s].add(t)
    for s in sorted(by_source):
        targets = ", ".join(sorted(by_source[s]))
        lines.append(f"- {s} → {targets}")
    return "\n".join(lines)

def _section_backlinks(backlinks: dict) -> str:
    lines = ["## 백링크 인덱스 (notes)"]
    for target in sorted(backlinks):
        sources = ", ".join(sorted(backlinks[target]))
        lines.append(f"- {target}: ← {sources}")
    return "\n".join(lines)
```

---

## 4. 멱등성 (git diff 노이즈 회피)

같은 페르소나 상태면 **바이트 단위로 같은** `_map.md` 출력해야 함:

| 비결정성 원천 | 해결 |
|---|---|
| dict 순회 순서 | `sorted()` 명시 |
| set 순회 순서 | `sorted()` 명시 |
| timestamp (header) | 매 commit마다 변하지만 의도적 — 사람 가시성용. 정 필요하면 git pre-commit hook이 timestamp 라인 제외하고 diff 비교 |

→ timestamp 외엔 결정적. 페르소나 변경 없이 빌드 재실행해도 timestamp 한 줄만 변함.

---

## 5. git pre-commit hook 셋업

`.git/hooks/pre-commit` (실행 권한 필요):

```bash
#!/usr/bin/env bash
set -euo pipefail
python3 scripts/build_persona_map.py
git add persona/_map.md
```

**설치 트리거**: 사용자 PC clone 직후 1회. plan-01 §setup 단계에서 자동 설치 스크립트 제공 (`scripts/install_hooks.sh`).

---

## 6. 백엔드 부팅 시 빌드

```python
# back/main.py
from scripts.build_persona_map import build_persona_map

@app.on_event("startup")
async def startup():
    build_persona_map()   # 부팅 시 한 번. 멱등이라 이미 최신이면 같은 결과
    load_all()            # 메모리 dict 로드
    scheduler.start()
```

부팅 시 빌드 시간: 페르소나 수십~수백 파일 기준 < 1초. 부팅 부담 무시 가능.

---

## 7. 옵시디언 vault 셋업

사용자 PC에서 `persona/` 디렉토리를 옵시디언 vault로 열기:

1. 옵시디언 → "Open another vault" → `persona/` 폴더 선택
2. `_map.md` 가 자동 시작 페이지로 보이도록 옵시디언 옵션 설정 (Settings → Files & Links → Default location for new attachments 등 — vault별)
3. 그래프 뷰 활성화 — `[[id]]` 위키링크가 자동 시각화

**주의**: 옵시디언이 자체적으로 만드는 `.obsidian/` 폴더는 `.gitignore`에 박을지 결정 (plan-01). 박으면 사용자별 옵시디언 설정 분리, 안 박으면 공유.

---

## 8. ADR-03 권한 모델 정합

ADR-03 §2.2 백엔드 write 화이트리스트:
- `persona/activity.yaml` (잡 산출물)
- `persona/_map.md` (본 spec의 산출물)

→ 두 파일 외엔 백엔드가 절대 안 씀. 코드 레벨 가드(spec-03 §9 path whitelist)에 `_map.md` 추가.

---

## 9. 검증 / fail-safe

| 케이스 | 동작 |
|---|---|
| 페르소나 frontmatter 형식 위반 | `frontmatter.load()` 에러 → 빌드 abort + 에러 파일 경로 로그 |
| `_meta.yaml` 누락 | category/group 라벨 None → "(unknown)" 표시. 빌드는 계속 |
| 위키링크 타깃 미존재 | 그래프엔 박되 백링크 인덱스에서 dead link로 표시 (옵시디언이 시각적으로 표시) |
| _map.md write 실패 (권한 등) | 빌드 abort + 로그. 백엔드 부팅은 계속 (메모리 dict는 별개) |

---

## 10. 향후 확장 여지

- _map.md 안에 **활동 잔디** 미리보기 (activity.yaml 최근 7일 추출) — 옵시디언에서 한 눈에
- contents/notes의 **태그 클라우드** 섹션
- 빈 카테고리 섹션 표시 정책 (현재는 빈 섹션도 헤딩만 출력 — 옵션으로 숨김 가능)
- 옵시디언 외 다른 노트 앱(Foam, Logseq 등) 호환 검증
