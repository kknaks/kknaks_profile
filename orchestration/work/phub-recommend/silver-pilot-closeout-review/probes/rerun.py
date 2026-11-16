"""Execute original scope runner with only output and temporary-copy locations redirected."""
import sys,json,hashlib
from pathlib import Path
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[1]; V=R.parent/'silver-design-pilot-v2'; OUT=R/'results'
sys.path.insert(0,str(V))
import common
text=(V/'scope_rule_probes.py').read_text()
text=text.replace('common.write_original=common.write',"common.write_original=lambda name,obj:(OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\\n')")
text=text.replace("if filename=='source_review.py':", "if filename=='identity_tests.py':text=text.replace(\"scratch=O/'_identity_scratch'\",\"scratch=Path(\"+repr(str(OUT/'identity-scratch'))+\")\")\n if filename=='source_review.py':")
(OUT/'runner-adaptation.json').write_text(json.dumps({'original_sha256':common.sha(V/'scope_rule_probes.py'),'executed_text_sha256':hashlib.sha256(text.encode()).hexdigest(),'changes':['output sink only','identity temporary-copy location only']},indent=2))
exec(compile(text,str(V/'scope_rule_probes.py'),'exec'),{'__file__':str(V/'scope_rule_probes.py'),'__name__':'closeout_rerun','OUT':OUT})
