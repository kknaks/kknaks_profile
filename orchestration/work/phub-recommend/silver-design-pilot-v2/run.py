"""Offline rebuild and full pilot checks. Never refreshes the protected baseline."""
import subprocess,sys,os
from pathlib import Path
root=Path(__file__).resolve().parent
env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
for script in ['build.py','schema.py','project.py','validate.py','source_review.py','positive_controls.py','probes.py','semantic_probes.py','identity_tests.py','finish.py','report.py']:
 subprocess.run([sys.executable,str(root/script)],check=True,cwd=root,env=env)
