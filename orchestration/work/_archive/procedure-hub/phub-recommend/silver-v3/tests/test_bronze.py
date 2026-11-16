# -*- coding: utf-8 -*-
"""브론즈 판(HASHES.txt · CHANGELOG · 1판 ERD 해시 · step1 ERD 해시) · 출처 필수 · 재실행 바이트 동일."""
import filecmp
import json
import os
import subprocess
import sys

from base import HERE, T, build
from registry import covers
import synth
from lib.core import Silver
from lib.load import BuildRefused


def fresh():
    return synth.Workspace()


class Bronze(T):
    @covers("bronze:hashes_txt:match", "bronze:changelog:version")
    def test_match_and_version(self):
        w = fresh()
        try:
            S = w.build()
            self.assertEqual(len(S.ctx["meta"]), 22)
            self.assertEqual((S.ctx["bronze"]["version"], S.ctx["bronze"]["hashes_file"]), (2, "HASHES.txt"))
        finally:
            w.cleanup()

    @covers("bronze:hashes_txt:mismatch")
    def test_mismatch(self):
        w = fresh()
        try:
            w.write_hashes(override={"synergy.json": "0" * 16})
            with self.assertRaises(BuildRefused) as cm:
                w.build()
            self.assertIn("synergy.json", str(cm.exception))
            # 원장 파일을 고치고 HASHES.txt 를 안 고쳐도 거부(판 교체는 HASHES.txt 로만)
            w.write_hashes()
            with open(os.path.join(w.bronze, "complications.json"), "a", encoding="utf-8") as f:
                f.write("\n")
            with self.assertRaises(BuildRefused):
                w.build()
            w.write_hashes()   # 새 판 = 파일 + HASHES.txt 함께 → 빌드
            w.build()
        finally:
            w.cleanup()

    @covers("bronze:hashes_txt:missing_file")
    def test_missing_file(self):
        w = fresh()
        try:
            os.remove(os.path.join(w.bronze, "pih-risk.json"))
            with self.assertRaises(BuildRefused) as cm:
                w.build()
            self.assertIn("pih-risk.json", str(cm.exception))
        finally:
            w.cleanup()

    @covers("bronze:hashes_txt:extra_file")
    def test_extra_file(self):
        w = fresh()
        try:
            with open(os.path.join(w.bronze, "new-ledger.json"), "w", encoding="utf-8") as f:
                f.write("{}")
            with self.assertRaises(BuildRefused) as cm:
                w.build()
            self.assertIn("new-ledger.json", str(cm.exception))
        finally:
            w.cleanup()

    @covers("bronze:v1:erd_hash_without_hashes_txt")
    def test_v1_without_hashes(self):
        w = fresh()
        try:
            os.remove(os.path.join(w.bronze, "HASHES.txt"))
            S = w.build()            # ERD source_files 해시(합성 ERD 는 합성 파일 해시)로 검증
            self.assertIsNone(S.ctx["bronze"])
            with open(os.path.join(w.bronze, "synergy.json"), "a", encoding="utf-8") as f:
                f.write(" ")
            with self.assertRaises(BuildRefused):
                w.build()
        finally:
            w.cleanup()

    @covers("bronze:step1:erd_hash")
    def test_step1_erd_hash(self):
        w = fresh()
        try:
            with open(w.step1, "a", encoding="utf-8") as f:
                f.write(" ")
            with self.assertRaises(BuildRefused) as cm:   # HASHES.txt 가 있어도 step1 은 늘 ERD 해시
                w.build()
            self.assertIn("step1-products.json", str(cm.exception))
        finally:
            w.cleanup()


class Provenance(T):
    @covers("provenance:every_value")
    def test_every_value_has_source(self):
        import test_decisions as TD
        for key, decs in (("plain", ()), ("tuples", TD.TUPLE_DECS), ("dict", TD.DICT_DECS)):
            w, S = build(key, decs)
            bad = []
            for et, recs in S.E.items():
                for rid, rec in recs.items():
                    if not rec["derived_from"] and not any(c.get("prov") for cells in rec["attrs"].values() for c in cells):
                        bad.append((et, rid, "레코드 출처 없음"))
                    for a, cells in rec["attrs"].items():
                        for c in cells:
                            if not c.get("prov") and not c.get("derived_from"):
                                bad.append((et, rid, a))
                    for c in rec["aliases"]:
                        if not c.get("prov") and not c.get("derived_from"):
                            bad.append((et, rid, "alias"))
            for rel, es in S.R.items():
                for e in es:
                    if not e["provenance"] and not e["derived_from"]:
                        bad.append((rel, e["from"]["id"], e["to"]["id"]))
                    for a, c in e["attrs"].items():
                        if not c.get("prov") and not c.get("derived_from"):
                            bad.append((rel, a))
            self.assertEqual(bad, [], key)

    @covers("provenance:value_without_source_fails")
    def test_value_without_source_refused(self):
        S = Silver({})
        rec = S.ent("site", "SIT-0000000000")
        with self.assertRaises(ValueError):
            S.dattr(rec, "kind", "anatomical", [])
        with self.assertRaises(ValueError):
            S.dattr(rec, "kind", "anatomical", [None, ""])


class Determinism(T):
    @covers("determinism:rerun_bytes")
    def test_rerun_bytes(self):
        import test_decisions as TD
        w = fresh()
        try:
            w0, S0 = build("plain")
            w.add_decisions(TD.TUPLE_DECS + TD.DICT_DECS[:2] + TD.late_decs(S0)[:8])
            outs = []
            for i in range(2):
                out = os.path.join(w.root, f"out{i}")
                r = subprocess.run([sys.executable, os.path.join(HERE, "_core_build.py"), w.root, out], capture_output=True, text=True)
                self.assertEqual(r.returncode, 0, r.stderr[-2000:])
                outs.append(out)
            cmp = filecmp.dircmp(outs[0], outs[1])

            def diff(c):
                d = list(c.diff_files) + list(c.left_only) + list(c.right_only)
                for sub in c.subdirs.values():
                    d += diff(sub)
                return d
            self.assertEqual(diff(cmp), [])
            self.assertTrue(os.path.exists(os.path.join(outs[0], "manifest.json")))
            with open(os.path.join(outs[0], "manifest.json"), encoding="utf-8") as f:
                m = json.load(f)
            self.assertEqual(m["inputs_count"], 22)
        finally:
            w.cleanup()
