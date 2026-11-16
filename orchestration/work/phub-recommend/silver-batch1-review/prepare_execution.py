"""Recreate only the review-local execution copy; refuse to replace an existing copy."""
from pathlib import Path
import shutil
R=Path(__file__).resolve().parent
shutil.copytree(R.parent/'silver-batch1-candidate',R/'execution-copy')
shutil.copyfile(R/'protected-start.json',R/'execution-copy/protected-start.json')
