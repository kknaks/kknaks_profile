#!/usr/bin/env bash
# .git/hooks/pre-commit 설치 — 매 commit 직전 문서 파이프라인/페르소나 검증.
# product docs pipeline + spec-04 §5 + spec-01 §6 (사전 차단).

set -euo pipefail

REPO=$(git rev-parse --show-toplevel)
HOOK="$REPO/.git/hooks/pre-commit"

cat > "$HOOK" <<'HOOK_EOF'
#!/usr/bin/env bash
# Auto-installed by app/scripts/install_hooks.sh — DO NOT edit manually.
# Behavior:
#   1) product docs pipeline strict check
#   2) persona/_map.md 빌드 (spec-04)
#   3) (app/back/.venv 있으면) 페르소나 검증 (spec-01 §6)
#   4) 변경된 _map.md 를 스테이징

set -euo pipefail
REPO=$(git rev-parse --show-toplevel)
cd "$REPO"

if git diff --cached --name-only | grep -Eq '^(products/|templates/product/|rules/product-doc-pipeline\.md|\.agent/hooks/|\.agent/scripts/product_doc_pipeline\.py$|\.agent/settings\.json$)'; then
  python3 .agent/scripts/product_doc_pipeline.py --strict
fi

# 페르소나 변경이 없으면 _map 재빌드 의미 없음 — 빠른 path
if ! git diff --cached --name-only | grep -q '^persona/'; then
  exit 0
fi

# 1. _map 빌드 (uv가 transient deps를 한 번에 설치)
uv run --quiet --with python-frontmatter --with pyyaml \
  python3 app/scripts/build_persona_map.py

# 2. 검증 (app/back/.venv 셋업되어 있을 때만 — M0/M2 끝났는지)
if [ -d "app/back/.venv" ]; then
  (cd app/back && uv run python -c "
from pathlib import Path
from service.persona_loader import load_persona, PersonaError
try:
    load_persona(Path('../../persona'))
    print('persona validation: ok')
except PersonaError as e:
    print(f'persona validation FAILED: {e}')
    raise SystemExit(1)
")
fi

# 3. 갱신된 _map.md 스테이징
git add persona/_map.md
HOOK_EOF

chmod +x "$HOOK"
echo "installed: $HOOK"
echo "   trigger: product docs 또는 persona/** 변경 포함된 commit 시 자동 실행"
echo "   actions: product_doc_pipeline.py --strict + build_persona_map.py + (app/back/.venv 있으면) loader 검증 + git add persona/_map.md"
