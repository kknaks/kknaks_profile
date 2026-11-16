# -*- coding: utf-8 -*-
"""경우 id ↔ 시험 대응 — @covers(…) 는 정의 때(정적), mark(…) 는 데이터 주도 시험이 경우를 실제로 돌릴 때(동적) 기록한다.
러너(run_tests.py)가 enumerate_cases.py 의 경우 전부가 여기 있는지 본다."""
from collections import defaultdict

COVERED = defaultdict(set)   # case id -> {test 이름}


def covers(*ids):
    def deco(fn):
        for i in ids:
            COVERED[i].add(f"{fn.__module__}.{fn.__qualname__}")
        fn._covers = ids
        return fn
    return deco


def mark(case_id, who):
    COVERED[case_id].add(who)
