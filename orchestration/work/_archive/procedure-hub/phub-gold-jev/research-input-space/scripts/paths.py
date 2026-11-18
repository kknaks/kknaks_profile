"""경로 한 곳 — 스크립트 자리에서 센다. 다른 자리의 gold · 앱을 쓰려면 env 로 바꾼다."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)                                   # research-input-space/
P = os.path.abspath(os.path.join(OUT, "..", "..", "..", ".."))  # 프로필 레포 루트
SM = os.environ.get("INPUT_SPACE_SILVER_MODEL", P + "/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model")
RUN = os.environ.get("INPUT_SPACE_RUN_DIR", os.path.join(OUT, "runs"))   # 실행 원 기록(지금 시스템 장부 · 시안 출력)
CONV = os.path.join(OUT, "conversations.jsonl")
os.makedirs(RUN, exist_ok=True)
