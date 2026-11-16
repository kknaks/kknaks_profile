# -*- coding: utf-8 -*-
"""ERD v2.1 잎 키 행선지 규칙 — v2(erd_colmap_v2.py) 와 **동일**. v2.1 은 시술 튜플의 what 결정 규칙만 바꾸고 행선지는 바꾸지 않는다.
COLMAP · MOVES(v1.1 → v2 이동 표) · resolve 를 그대로 노출한다. erd_build_v21.py 가 읽는다.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import erd_colmap_v2 as V2  # noqa

COLMAP = V2.COLMAP
MOVES = V2.MOVES
resolve = V2.resolve
