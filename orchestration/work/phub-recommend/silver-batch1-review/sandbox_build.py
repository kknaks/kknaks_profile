from pathlib import Path
import sys
sys.path.insert(0,'/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/silver-batch1-migration')
original=Path('/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/silver-batch1-migration/build.py')
code=original.read_text()
code=code.replace("permitted=(BASE/'silver-batch1-candidate').resolve()","permitted=Path('/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/silver-batch1-review/execution-copy').resolve()")
exec(compile(code,str(original),'exec'),{'__name__':'__main__','__file__':str(original)})
