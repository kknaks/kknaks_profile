"""Rebuild/recheck pilot artifacts only. Inputs-start is intentionally never refreshed."""
import subprocess,sys,os
from pathlib import Path
root=Path(__file__).resolve().parent
env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
for script in ['build.py','schema.py','project.py','validate.py','report.py']:
 subprocess.run([sys.executable,str(root/script)],check=True,cwd=root,env=env)
