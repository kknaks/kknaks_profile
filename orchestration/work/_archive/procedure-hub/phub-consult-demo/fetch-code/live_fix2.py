"""고침 2 실물 — 73bd 4 턴 · 검수 E3 · E4(새 대화 첫 턴). live3.py 와 같은 길."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import live3
live3.CONVS = {"73bd": live3.CONVS["73bd"],
               "E3": ["지방분해 주사 맞을건데 리프팅이랑 같이 하면 안돼 ?"],
               "E4": ["올리지오는 어떤 시술이야 ? 명동점에서 받을 수 있어 ?"]}
live3.main()
