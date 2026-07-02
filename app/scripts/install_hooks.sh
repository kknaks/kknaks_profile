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
#   2) persona/_map.md 빌드 (spec-04, persona 변경 시)
#   3) (app/back/.venv 있으면) 페르소나 + 그래프 enforce 검증 (spec-01 §6 + KDEV-WORK-007)
#   4) 변경된 _map.md 를 스테이징 (persona 변경 시)

set -euo pipefail
REPO=$(git rev-parse --show-toplevel)
cd "$REPO"

CHANGED=$(git diff --cached --name-only)

if echo "$CHANGED" | grep -Eq '^(products/|templates/product/|rules/product-doc-pipeline\.md|\.agent/hooks/|\.agent/scripts/product_doc_pipeline\.py$|\.agent/settings\.json$)'; then
  python3 .agent/scripts/product_doc_pipeline.py --strict
fi

# 그래프 노드 출처 = persona + reference + products (KDEV-WORK-007). 셋 중 하나라도 변경 시
# load_persona 로 graph enforce 검증. 하나도 안 바뀌면 빠른 path.
persona_changed=0
if echo "$CHANGED" | grep -q '^persona/'; then persona_changed=1; fi
graph_changed=0
if echo "$CHANGED" | grep -Eq '^(persona|reference|products)/'; then graph_changed=1; fi

if [ "$graph_changed" = 0 ]; then
  exit 0
fi

# 1. _map 빌드 (persona 변경 시에만 — _map 은 persona 전용)
if [ "$persona_changed" = 1 ]; then
  uv run --quiet --with python-frontmatter --with pyyaml \
    python3 app/scripts/build_persona_map.py
fi

# 2. 검증 (app/back/.venv 셋업되어 있을 때만 — M0/M2 끝났는지).
#    GRAPH_ENFORCE=1 강제 — GraphEnforcementError 는 PersonaError 서브클래스라 같이 catch.
if [ -d "app/back/.venv" ]; then
  (cd app/back && GRAPH_ENFORCE=1 uv run python -c "
from pathlib import Path
from service.persona_loader import load_persona, PersonaError
try:
    load_persona(Path('../../persona'))
    print('persona+graph validation: ok')
except PersonaError as e:
    print(f'persona+graph validation FAILED: {e}')
    raise SystemExit(1)
")
fi

# 3. 갱신된 _map.md 스테이징 (persona 변경 시)
if [ "$persona_changed" = 1 ]; then
  git add persona/_map.md
fi
HOOK_EOF

chmod +x "$HOOK"
echo "installed: $HOOK"
echo "   trigger: product docs 또는 persona/** 변경 포함된 commit 시 자동 실행"
echo "   actions: product_doc_pipeline.py --strict + build_persona_map.py + (app/back/.venv 있으면) loader 검증 + git add persona/_map.md"
