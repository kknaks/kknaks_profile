"""언어별 Soniox context 글자 수 — 통키 back 코드(glossary.build_context · context_size) 그대로.
실행: interpret-pwa/back 에서 `uv run python <이 파일>` > context-chars.json (main 17c26b5). 시드 내용은 출력하지 않는다."""
import json,sys
sys.path.insert(0,'.')
from app.config import SEED_PATH
from app.service.glossary import load_seed, build_context, context_size
from app.service.interpret.langs import APP_LANGS, context_max_chars
g=load_seed(SEED_PATH)
out={'seed_version':g.version,'langs':{}}
for l in APP_LANGS:
    rep={}
    p=build_context(g.terms,l,context_max_chars(l),rep)
    out['langs'][l]={'chars':context_size(p) if p else 0,'max_chars':context_max_chars(l),**rep}
print(json.dumps(out,ensure_ascii=False))
