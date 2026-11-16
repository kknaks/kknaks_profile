# Hub 선택 관계 3차 FAIL 수정 보고

- 기준 HEAD: `2edc190`; 작업: 기존 미커밋 Hub 변경을 유지한 채 `backend/app/modules/gold/selected.py`, `backend/tests/test_gold_selected.py` 수정.
- `/Users/marin/AGENTS.md`는 현재 환경에 없어 읽지 못함. 브리프, SPEC-005 §5-5·§6-9, SPEC-006 §3-4-1-5, WORK-011, 리뷰 전문을 확인함.
- 서버·DB·평가 실행, 커밋·push·PR 없음. 시험은 메모리 Gold와 문서의 SQLite 메모리 URL을 사용함.

## 수정

1. interval의 `source_condition`은 원천 `interval.branches`에 `L-SAMESITE`가 있고 조건 값이 `같은 부위`인 경우에만 `{"부위":"같은 부위"}`에 결속한다. `세션`/`깊이`에 같은 값을 주어도 `quotable=false`. 원천 branch를 확인할 수 없으면 `applies_to.unresolved_condition="interval_dimension"` 및 `quotable=false`. 실물 조건이 있는 R8 fact는 `R8-0180`, `R8-0244` 두 개로 확인했다.
2. 일반·공유 R8 claim 모두 source가 `step8-relations.json`의 `claims[<실제 fact ID>]`인지 검사한다. `R8-0111`의 path를 다른 존재 claim `claims[R8-0144]`로 치환하면 `pair_scope.status=error`, `complete=false`. 기존 공유 owner 양쪽 edge 명시, resolved source, 대안 검증은 유지한다.
3. 위의 두 fact에 올바른 key, 틀린 두 key, branch 미확정 음성 시험을 추가하고 일반 claim의 존재하는 다른 source path 음성 시험을 추가했다.

## §6-9 첫 페이지 기준 비교

HEAD `2edc190`의 `backend/`를 `git archive`로 임시 디렉터리에 추출했다. 같은 Python venv와 실물 입력을 이용해 HEAD·현재 각각 `real_graph(); warm_sections(g)` 뒤 `sorted(g.section_ids)`의 모든 `(node, section)`에 `expand(g,node,sections=[section])`을 호출하고 `facts[].id` 순서를 비교했다. 기준 186개의 특정 호출 목록은 WORK-011에 별도로 고정되어 있지 않으므로 정렬된 첫 186개를 명시적으로 비교했고, 그 상위 집합인 전체 6,626개도 비교했다.

- 양쪽 build hash: `567677edfe7123e9`
- 정렬된 첫 186개 `(node,section,facts[].id)` SHA-256: 양쪽 `a85a256cf86d216de7d81824c66b2e14341f91b41c33f25776f4b0f51df59f12`
- 전체 6,626개 SHA-256: 양쪽 `a413bd933882a457b1b0307a5406c4199c466311ba443650701feefaa24d48a4`
- 불일치: 0개. 따라서 186개가 전체 section 호출 중 어느 부분집합이어도 첫 페이지 ID 순서는 동일하다.

재현: 저장소 루트에서 아래 스크립트를 `backend/.venv/bin/python`으로 실행한다. `git archive`의 기준과 현재를 동일한 실물 입력으로 독립 import한다.

```python
import hashlib, json, os, subprocess, tarfile, tempfile
from pathlib import Path
root = Path.cwd()
python = str(root / "backend/.venv/bin/python")
code = '''import json
from tests.gold_support import real_graph
from app.modules.gold.tools import expand, warm_sections
g = real_graph(); warm_sections(g)
rows = [(n, s, [f["id"] for f in expand(g, n, sections=[s])["facts"]])
        for n, s in sorted(g.section_ids)]
print(json.dumps({"build": g.build["build_hash"], "rows": rows}, ensure_ascii=False))'''
with tempfile.TemporaryDirectory(prefix="phub-head-") as tmp:
    archive = subprocess.run(["git", "archive", "2edc190", "backend"], check=True, stdout=subprocess.PIPE).stdout
    path = Path(tmp) / "head.tar"
    path.write_bytes(archive)
    with tarfile.open(path) as tar:
        tar.extractall(tmp, filter="data")
    def run(where):
        env = os.environ.copy()
        env["PYTHONPATH"] = str(where / "backend")
        raw = subprocess.run([python, "-c", code], cwd=where, env=env,
                             check=True, capture_output=True, text=True).stdout
        return json.loads(raw)
    before, after = run(Path(tmp)), run(root)
    digest = lambda rows: hashlib.sha256(json.dumps(rows, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()
    print("builds", before["build"], after["build"])
    print("sections", len(before["rows"]), len(after["rows"]))
    print("first186", digest(before["rows"][:186]), digest(after["rows"][:186]))
    print("all", digest(before["rows"]), digest(after["rows"]))
    print("mismatches", sum(a != b for a, b in zip(before["rows"], after["rows"])))
```

## 검증

- `backend/.venv/bin/pytest -q backend/tests/test_gold_selected.py`: **24 passed**.
- `cd backend && DATABASE_URL=sqlite+aiosqlite:///:memory: .venv/bin/pytest -q --ignore=tests/integration`: **917 passed, 14 xfailed**.
- 명시 회귀: `test_gold_v33_expand.py::test_line_rule_40_kept_41_cut`, `::test_peek_bytes_equal_rest_expand_body_all_pairs`, `test_gold_selected.py::test_representative_later_pages`: **7 passed**(5개 뒤 페이지 parameter 포함). 기존 시험에서 `facts_uncut` 계약과 `fact_ids` 원문 조회, `safety.management`의 section 이동·peek·expand도 전체 시험으로 확인했다.
- `cd backend && .venv/bin/ruff check app tests scripts`: **All checks passed**.
- `git diff --check`: **통과**.

남은 관문: 이 작업은 코드·시험 수정만 허용되어 서버 배포/앱 어댑터 통합과 전체 평가는 실행하지 않았다. WORK-011의 특정 186호출 원장 목록이 따로 제공되면 그 목록을 직접 재생할 수 있으나, 이번 전체 6,626 section 비교가 그 ID 순서 보존을 포함한다.
