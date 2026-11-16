#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""검산 ①~⑨ + V3 + V3.1 — out/ 과 원장·ERD 를 독립으로 대조한다. 실패가 하나라도 있으면 exit 1.

V3 항목(ERD v3 §11 V3-1~V3-10): 수식 칸·식별자(v3.1 세 칸) · 회사 괄호 · stopwords · `+`/`/`·multi_tuple · layer 금지 · canonical_rename ·
description/media_refs · R5 하위분류 · 결정 anchor 확장 · fold_approve 의 ⑦ 닫힘. 결정 적용 뒤 사전(out/dictionaries.json)으로 분해를 다시 돌려 대조한다.
V3.1 항목(ERD v3.1 §11 V3.1-1~10): product_reclassify · R32 · dictionary_remove · 조건 단위 · 회·차 · stopwords 겹침 · 필수 고지 · 안전 문구 수식어 · 단위 세 칸·경과 엣지(원칙 C) · 문구 사전·부록.

python3 check.py [--out out/] [--skip-rebuild]   (④ 는 빌드를 두 번 새로 돌려 out/ 과 바이트 대조 — 임시 폴더는 --tmp)
"""
import argparse
import filecmp
import json
import os
import re
import subprocess
import sys
import tempfile
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ERD_DIR = os.path.dirname(HERE)

from lib.adverse31 import adverse_phrases31, condition_occurrences, run_adverse31, run_condition  # noqa: E402
from lib import v32 as V32  # noqa: E402
from lib.decompose import run_procedure, site_kind_of, tids_of  # noqa: E402
from lib.load import bronze_hashes, bronze_info, expected_hash, hash_ok, load_bronze, load_json  # noqa: E402
from lib.provenance import parse_loc, resolve  # noqa: E402
from lib.util import mkid, norm, sha256_file  # noqa: E402
from collections import Counter  # noqa: E402,F811

DERIVED = re.compile(r"\b(PRC|ADV|CFL)-[0-9a-f]{10}\b")


def OrderedDictish(pairs):
    return list(pairs)


def jl(p):
    with open(p, encoding="utf-8") as f:
        return [json.loads(x) for x in f if x.strip()]


class Checker:
    def __init__(self, a):
        self.a = a
        self.out = a.out
        self.erd = load_json(a.erd)
        self.dic = load_json(a.dict)
        self.L, self.meta = load_bronze(self.erd, a.bronze, a.step1)
        self.results = []
        self.ents = {f[:-6]: jl(os.path.join(self.out, "entities", f)) for f in sorted(os.listdir(os.path.join(self.out, "entities")))}
        self.rels = {f[:-6]: jl(os.path.join(self.out, "relations", f)) for f in sorted(os.listdir(os.path.join(self.out, "relations")))}
        self.manifest = load_json(os.path.join(self.out, "manifest.json"))
        self.dec_ids = {r["id"] for r in self.ents["decision"]}
        self.outdic = load_json(os.path.join(self.out, "dictionaries.json"))
        self.prev = load_json(a.tuples_prev) if a.tuples_prev and os.path.exists(a.tuples_prev) else None
        self.erd_name, self.dict_name = os.path.basename(a.erd), os.path.basename(a.dict)
        self.log = {x["id"]: x for x in self.manifest["decisions"]["apply_log"]}
        bi = bronze_info(a.bronze)
        self.bver = (bi or {}).get("version") or 1
        self._post = None
        self.is33 = self.erd.get("erd_version") == "v3.3"
        self.is32 = self.erd.get("erd_version") in ("v3.2", "v3.3")
        self.an = None
        if self.is33:
            from lib.analyzer import Analyzer
            self.an = Analyzer(a.kiwi_cache, a.kiwi_python)

    def res(self, no, name, ok, detail):
        self.results.append((no, name, ok, detail))

    # -------------------------------------------------------------- 공통: locator 검증
    def ref_ok(self, ref, cache={}):
        if ref in cache:
            return cache[ref]
        ok = False
        try:
            if ref.startswith(self.erd_name + "#/"):
                ok = self._ptr(self.erd, ref.split("#/", 1)[1])
            elif ref.startswith(self.dict_name + "#/"):
                ok = self._ptr(self.dic, ref.split("#/", 1)[1])
            elif ref.startswith("dict:"):
                # 사전 안정 키 — dict:<사전>|<정준값>[|<필드>] · 동결 사전 또는 적용된 사전(out/dictionaries.json)
                name, canon = ref[5:].split("|")[:2]
                ok = any(d["name"] == name and any(e["canonical"] == canon for e in d["entries"]) for dd in (self.dic, self.outdic) for d in dd["dictionaries"])
            elif ref.startswith("decision:"):
                ok = ref[9:] in self.dec_ids and ref[9:] in {x["id"] for x in self.manifest["decisions"]["apply_log"] if x.get("result") in ("applied", "recorded")}
            elif ref.startswith("erd:source_files/"):
                parts = ref[len("erd:source_files/"):].split("/")
                ok = any(x["file"] == parts[0] and (len(parts) == 1 or parts[1] in x) for x in self.erd["source_files"])
            elif ref.startswith("erd:decisions/"):
                ok = any(x["id"] == ref[len("erd:decisions/"):] for x in self.erd["decisions"])
            elif ref.startswith("DEC-"):
                ok = ref in self.dec_ids
            elif ref.startswith("decisions/"):
                ok = os.path.exists(os.path.join(self.a.decisions, ref[len("decisions/"):]))
            elif ".json:" in ref:
                p = parse_loc(ref)
                if p["file"] in self.L:
                    resolve(self.L[p["file"]], p["path"], p["rec"])
                    ok = True
        except (KeyError, ValueError, IndexError, TypeError):
            ok = False
        cache[ref] = ok
        return ok

    @staticmethod
    def _ptr(doc, pointer):
        v = doc
        for part in pointer.split("/"):
            part = part.replace("~1", "/").replace("~0", "~")
            v = v[int(part)] if isinstance(v, list) else v[part]
        return True

    def prov_ok(self, p, value=None, check_value=False):
        try:
            v = resolve(self.L[p["file"]], p["path"], p["rec"])
        except (KeyError, ValueError, IndexError, TypeError):
            return False, "locator 해석 불가"
        if check_value and not isinstance(v, (dict, list)) and value is not None and value != v:
            return False, f"값 불일치 {str(value)[:30]} ≠ 원장 {str(v)[:30]}"
        return True, ""

    # -------------------------------------------------------------- ①
    def c1(self):
        bad = []
        hashes = bronze_hashes(self.a.bronze)  # 브론즈 폴더 HASHES.txt 가 있으면 원장 21 은 그것으로(2판~), 없으면 ERD source_files(1판)
        for s in self.erd["source_files"]:
            p = self.a.step1 if s["kind"] == "research_artifact" else os.path.join(self.a.bronze, s["file"])
            h = sha256_file(p)
            want, _ = expected_hash(s, hashes)
            if not hash_ok(h, want) or self.manifest["inputs"].get(s["file"], {}).get("sha256") != h:
                bad.append(s["file"])
        info = bronze_info(self.a.bronze)
        ver_ok = (self.manifest.get("bronze_version") == info) if info else ("bronze_version" not in self.manifest)
        n = len(self.erd["source_files"])
        self.res("①", "입력 해시 22 일치", not bad and ver_ok and n == 22 and self.manifest["inputs_count"] == 22,
                 f"{n - len(bad)}/{n} 일치({'원장 ' + info['label'] + ' HASHES.txt' if info else '원장 ERD 해시'}) · manifest {self.manifest['inputs_count']}" + ("" if ver_ok else " · bronze_version 불일치") + (f" · 불일치 {bad}" if bad else ""))

    # -------------------------------------------------------------- ②
    def c2(self):
        n_cells = n_bad = 0
        bad = []

        def cell(c, where):
            nonlocal n_cells, n_bad
            n_cells += 1
            if c.get("prov"):
                for p in c["prov"]:
                    ok, why = self.prov_ok(p, c.get("value") if "raw" not in c else None, check_value=isinstance(c.get("value"), (str, int, float, bool)))
                    if not ok:
                        n_bad += 1
                        bad.append(f"{where}: {why} {p}")
                        return
            elif c.get("derived_from"):
                for d in c["derived_from"]:
                    if not self.ref_ok(d):
                        n_bad += 1
                        bad.append(f"{where}: derived_from 해석 불가 {d}")
                        return
            else:
                n_bad += 1
                bad.append(f"{where}: provenance·derived_from 없음")

        n_recs = 0
        for t, rows in self.ents.items():
            for r in rows:
                n_recs += 1
                if not r.get("provenance") and not r.get("derived_from"):
                    n_bad += 1
                    bad.append(f"{t}:{r['id']} 레코드 provenance 없음")
                for k, cells in r["attrs"].items():
                    for c in cells:
                        cell(c, f"{t}:{r['id']}.{k}")
                for a in r.get("aliases", []):
                    cell(a, f"{t}:{r['id']}.alias")
        n_edges = 0
        for rel, es in self.rels.items():
            for e in es:
                n_edges += 1
                if not e["provenance"] and not e["derived_from"]:
                    n_bad += 1
                    bad.append(f"{rel} 엣지 provenance 없음")
                for p in e["provenance"]:
                    ok, why = self.prov_ok(p)
                    if not ok:
                        n_bad += 1
                        bad.append(f"{rel}: {why} {p}")
                for d in e["derived_from"]:
                    if not self.ref_ok(d):
                        n_bad += 1
                        bad.append(f"{rel}: derived_from {d}")
                for k, c in e["attrs"].items():
                    cell(c, f"{rel}.{k}")
        for c in jl(os.path.join(self.out, "conflicts.jsonl")):
            for v in c["values"]:
                if v.get("source_file"):
                    ok, why = self.prov_ok({"file": v["source_file"], "path": v["source_path"], "rec": v["rec"]})
                    if not ok:
                        n_bad += 1
                        bad.append(f"conflict {c['id']}: {why}")
            if not c["stable_key"]["locators"]:
                n_bad += 1
                bad.append(f"conflict {c['id']}: stable_key locators 없음")
        self.res("②", "provenance 없는 값 0 (locator 해석 · 원장 값 일치)", n_bad == 0, f"레코드 {n_recs} · 엣지 {n_edges} · 칸 {n_cells} 검사 · 실패 {n_bad}" + (f" · 예 {bad[:3]}" if bad else ""))

    # -------------------------------------------------------------- ③
    def c3(self):
        if self.is32:
            return self.c3_v32()
        ref = load_json(self.a.tuples)
        P = run_procedure(self.dic, self.erd["resolve_rules"], self.L, prev_tuples=None, bronze_version=self.bver)
        A = run_adverse31(P["ids"], self.erd["tuple_rules"], self.L, self.prev)
        C = run_condition(self.dic, self.erd["tuple_rules"]["condition"], self.L)
        self._pre = (P, A, C)
        diff = []
        nkeys = 0
        for part, mine in (("procedure", P["summary"]), ("adverse", A["summary"]), ("condition", C["summary"])):
            keys_ref = set(ref[part]["summary"])
            keys_me = {k for k in mine if not k.startswith("_")}
            nkeys += len(keys_me)
            for k in sorted(keys_ref ^ keys_me):
                diff.append(f"{part}.{k}(키 없음)")
            for k, v in mine.items():
                if k.startswith("_"):
                    continue
                if json.loads(json.dumps(v, ensure_ascii=False, default=str)) != ref[part]["summary"].get(k):
                    diff.append(f"{part}.{k}")
        # 행 단위(튜플·단위 id 등록 순서 · 이름 → 단위 · 문구 사전 항목 · R15 · 조건 단위 · 분류 항목 → 튜플)
        if [t for t in P["PT"].tuples] != [t["id"] for t in ref["procedure"]["tuples"]]:
            diff.append("procedure.tuple_ids(순서)")
        if [t["id"] for t in A["tuples"]] != [t["id"] for t in ref["adverse"]["tuples"]]:
            diff.append("adverse.tuple_ids(순서)")
        if [(r["locator"], r["unit_ids"]) for r in A["complications"]] != [(r["locator"], r["unit_ids"]) for r in ref["adverse"]["complications"]]:
            diff.append("adverse.complications")
        if [(e["id"], e["status"], e["units"], e["locators"]) for e in A["phrase_dictionary"]] != [(e["id"], e["status"], e["units"], e["locators"]) for e in ref["adverse"]["phrase_dictionary"]]:
            diff.append("adverse.phrase_dictionary")
        jn = lambda x: json.loads(json.dumps(x, ensure_ascii=False, default=str))  # noqa: E731
        if jn([(e["from_"], e["unit"], e["courses"], e["source_phrases"]) for e in A["edges"]]) != jn([(e["from_"], e["unit"], e["courses"], e["source_phrases"]) for e in ref["adverse"]["edges"]]):
            diff.append("adverse.edges")
        if [(u["id"], len(u["phrases"])) for u in C["units"]] != [(u["id"], len(u["phrases"])) for u in ref["condition"]["units"]]:
            diff.append("condition.units")
        if [(r["family"], r["name"], r.get("procedure_id"), r["status"]) for r in P["cat_recs"]] != [(r["family"], r["name"], r.get("procedure_id"), r["status"]) for r in ref["procedure"]["catalog"]]:
            diff.append("procedure.catalog")
        changed = [x for x in self.manifest["decisions"]["apply_log"] if x.get("result") == "applied" and x.get("stage") in ("⓪", "①", "②", "③", "④")]
        extra = ""
        if not changed:
            out_p = {r["id"] for r in self.ents["procedure"]}
            out_a = {r["id"] for r in self.ents["adverse_effect"]}
            out_c = {r["id"] for r in self.ents["person_condition"]}
            if out_p != {t["id"] for t in ref["procedure"]["tuples"]}:
                diff.append("out procedure id 집합")
            if out_a != {t["id"] for t in ref["adverse"]["tuples"]}:
                diff.append("out adverse_effect id 집합")
            if out_c != {u["id"] for u in ref["condition"]["units"]}:
                diff.append("out person_condition id 집합")
            r26 = {(e["to"]["id"], e["from"]["id"]) for e in self.rels["R26"]}
            want = {(r["catalog_item_id"], r["procedure_id"]) for r in ref["procedure"]["catalog"]}
            if r26 != want:
                diff.append("R26(항목→튜플)")
            extra = f" · out 레코드 대조(튜플 {len(out_p)} · 부작용 {len(out_a)} · 조건 {len(out_c)} · R26 {len(r26)})"
        self.res("③", f"결정 적용 전 수치 = {os.path.basename(self.a.tuples)} 요약(차이 0)", not diff, f"요약 키 {nkeys}(시술·부작용·조건) + 행 대조 8 · 차이 {len(diff)}{extra}" + (f" · {diff[:5]}" if diff else ""))

    def c3_v32(self):
        """v3.2 — 사전 파일의 파생 항목을 뺀 ERD 사전(V32.base_dictionary)으로 분해(V32.run_v32) → erd-v3.2-tuples.json 요약(시술 · 부작용 · 조건) + 행 대조.
        v3.3: ERD 실측(erd-v3.3-tuples.py)은 분석기 없이 돈다 — 분해도 analyzer=None(목록 규칙)으로 대조한다(분석기 분해 수치는 report §16 · V3.3-B 검산)."""
        ref = load_json(self.a.tuples)
        P, A, C, X = V32.run_v32(V32.base_dictionary(self.dic), self.erd, self.L, bronze_version=self.bver, analyzer=None)
        self._pre = (P, A, C)
        jn = lambda x: json.loads(json.dumps(x, ensure_ascii=False, default=str))  # noqa: E731
        diff, nkeys = [], 0
        for part, mine in (("procedure", P["summary"]), ("adverse", A["summary"]), ("condition", C["summary"])):
            keys_ref, keys_me = set(ref[part]["summary"]), {k for k in mine if not k.startswith("_")}
            nkeys += len(keys_me)
            diff += [f"{part}.{k}(키 없음)" for k in sorted(keys_ref ^ keys_me)]
            diff += [f"{part}.{k}" for k, v in mine.items() if not k.startswith("_") and jn(v) != ref[part]["summary"].get(k)]
        ra, rp, rc = ref["adverse"], ref["procedure"], ref["condition"]
        rows = OrderedDictish([
            ("procedure.tuple_ids(순서)", ([t for t in P["PT"].tuples], [t["id"] for t in rp["tuples"]])),
            ("procedure.catalog", ([(r["family"], r["name"], r.get("procedure_id"), r["status"]) for r in P["cat_recs"]], [(r["family"], r["name"], r.get("procedure_id"), r["status"]) for r in rp["catalog"]])),
            ("adverse.tuple_ids(순서)", ([t["id"] for t in A["tuples"]], [t["id"] for t in ra["tuples"]])),
            ("adverse.complications", ([(r["locator"], r["unit_ids"]) for r in A["complications"]], [(r["locator"], r["unit_ids"]) for r in ra["complications"]])),
            ("adverse.phrase_dictionary", ([(e["id"], e["status"], e["units"], e["locators"]) for e in A["phrase_dictionary"]], [(e["id"], e["status"], e["units"], e["locators"]) for e in ra["phrase_dictionary"]])),
            ("adverse.memo_phrases", ([(e["id"], e["status"], e["locators"]) for e in A["memo_phrases"]], [(e["id"], e["status"], e["locators"]) for e in ra["memo_phrases"]])),
            ("adverse.edges", (jn([(e["from_"], e["unit"], e["courses"], e["source_phrases"], e["timeline_refs"], e["emergency_sign_refs"], e["inheritance"], e["layer"]) for e in A["edges"]]),
                               jn([(e["from_"], e["unit"], e["courses"], e["source_phrases"], e["timeline_refs"], e["emergency_sign_refs"], e["inheritance"], e["layer"]) for e in ra["edges"]]))),
            ("adverse.ledger_events", (jn([(n["id"], n["canonical"], n["locators"]) for n in A["ledger_events"]]), jn([(n["id"], n["canonical"], n["locators"]) for n in ra["ledger_events"]]))),
            ("adverse.duplicate_pairs", (jn([(d["stable_key"], d["grade"], d["rules"]) for d in A["duplicate_pairs"]]), jn([(d["stable_key"], d["grade"], d["rules"]) for d in ra["duplicate_pairs"]]))),
            ("adverse.timeline_lines", ([(l["locator"], l["adverse_ref"], l["ref_status"]) for T in A["timelines"] for p_ in T["phases"] for l in p_["lines"]], [(l["locator"], l["adverse_ref"], l["ref_status"]) for T in ra["timelines"] for p_ in T["phases"] for l in p_["lines"]])),
            ("adverse.emergency_signs", ([(x["id"], x["adverse_ref"], x["ref_status"], x["locators"]) for x in A["emergency_signs"]], [(x["id"], x["adverse_ref"], x["ref_status"], x["locators"]) for x in ra["emergency_signs"]])),
            ("adverse.disclosures", ([(x["locator"], x["adverse_ref"], x["ref_status"]) for x in A["disclosures"]], [(x["locator"], x["adverse_ref"], x["ref_status"]) for x in ra["disclosures"]])),
            ("adverse.literature", ([(x["id"], x["adverse_ref"], x["ref_status"]) for x in A["literature"]], [(x["id"], x["adverse_ref"], x["ref_status"]) for x in ra["literature"]])),
            ("adverse.r34·r35", (jn([A["r34"], A["r35"]]), jn([ra["r34"], ra["r35"]]))),
            ("condition.units", ([(u["id"], len(u["phrases"])) for u in C["units"]], [(u["id"], len(u["phrases"])) for u in rc["units"]])),
            ("equipment.products", ([p_["id"] for p_ in X["equipment"]["products"]], [p_["id"] for p_ in ref["equipment"]["products"]])),
            ("r33", (jn([{k: v for k, v in x.items() if k != "ref_id"} for x in X["r33"]]), ref["r33"])),
            ("tokenizer.hits", (X["tokenizer"]["hits"], ref["tokenizer"]["hits"])),
            ("gloss_pairs", (jn(A["gloss_pairs"] + X["gloss_pairs_other"]), jn(ra["gloss_pairs"] + ref["gloss_pairs_other"]))),
        ])
        for k, (a_, b_) in rows:
            if a_ != b_:
                diff.append(k)
        self.res("③", f"결정 적용 전 수치 = {os.path.basename(self.a.tuples)} 요약(차이 0)" + ("(분석기 없는 목록 규칙 · ERD 실측 조건)" if self.is33 else ""), not diff, f"요약 키 {nkeys}(시술·부작용·조건) + 행 대조 {len(rows)} · 차이 {len(diff)}" + (f" · {diff[:5]}" if diff else ""))

    # -------------------------------------------------------------- ④
    def c4(self):
        if self.a.skip_rebuild:
            self.res("④", "재실행 바이트 동일", None, "건너뜀(--skip-rebuild)")
            return
        if self.a.tmp:
            os.makedirs(self.a.tmp, exist_ok=True)
        base = tempfile.mkdtemp(prefix="silver-v3-", dir=self.a.tmp)
        outs = []
        for i in (1, 2):
            o = os.path.join(base, f"run{i}")
            cmd = [sys.executable, os.path.join(HERE, "build.py"), "--bronze", self.a.bronze, "--step1", self.a.step1, "--erd", self.a.erd, "--dict", self.a.dict,
                   "--tuples", self.a.tuples, "--tuples-prev", self.a.tuples_prev or "", "--colmap", self.a.colmap, "--decisions", self.a.decisions, "--out", o,
                   "--kiwi-cache", self.a.kiwi_cache, "--kiwi-python", os.path.join(base, "no-venv-here")]   # v3.3: 재실행은 캐시만으로(venv 경로를 없는 곳으로 — 캐시에 없는 문구가 있으면 빌드 거부 = ④ FAIL)
            subprocess.run(cmd, check=True, capture_output=True)
            outs.append(o)

        def tree(d):
            return sorted(os.path.relpath(os.path.join(r, f), d) for r, _, fs in os.walk(d) for f in fs)
        t1, t2, t0 = tree(outs[0]), tree(outs[1]), tree(self.out)
        diff = [f for f in t1 if f not in t2 or not filecmp.cmp(os.path.join(outs[0], f), os.path.join(outs[1], f), shallow=False)]
        diff0 = [f for f in t1 if f not in t0 or not filecmp.cmp(os.path.join(outs[0], f), os.path.join(self.out, f), shallow=False)]
        self.res("④", "재실행 바이트 동일", not diff and t1 == t2 and not diff0 and t1 == t0, f"파일 {len(t1)} · 두 번 새로 빌드 간 차이 {len(diff)} · out/ 과 차이 {len(diff0)}" + (f" · {(diff + diff0)[:3]}" if diff or diff0 else "") + f" · 임시 {base}")

    # -------------------------------------------------------------- ⑤
    def c5(self):
        boot = sorted(f[:-5] for f in os.listdir(os.path.join(self.a.decisions, "_bootstrap")) if f.endswith(".json"))
        log = {x["id"]: x for x in self.manifest["decisions"]["apply_log"]}
        missing = [b for b in boot if b not in log or log[b]["result"] not in ("applied", "recorded")]
        proposed_ids = []
        for root, _, fs in os.walk(self.a.decisions):
            for f in fs:
                if f.endswith(".json") and not f.startswith("_"):
                    d = load_json(os.path.join(root, f))
                    if isinstance(d, dict) and d.get("status") == "proposed":
                        proposed_ids.append(d["id"])
        applied_prop = [p for p in proposed_ids if p in log]
        erd_appr = sorted(d["id"] for d in self.erd["decisions"] if d["status"] == "approved")
        self.res("⑤", "_bootstrap 19 전부 적용 로그 · proposed 0 적용", len(boot) == 19 and boot == erd_appr and not missing and not applied_prop,
                 f"_bootstrap {len(boot)}(ERD approved {len(erd_appr)}) · 로그 누락 {len(missing)} · proposed {len(proposed_ids)} 중 적용 {len(applied_prop)}")

    # -------------------------------------------------------------- ⑥
    def c6(self):
        bad = []
        for root, _, fs in os.walk(self.a.decisions):
            for f in fs:
                if f.endswith(".json") and not f.startswith("_"):
                    d = load_json(os.path.join(root, f))
                    m = DERIVED.search(json.dumps(d.get("target"), ensure_ascii=False))
                    if m:
                        bad.append((os.path.relpath(os.path.join(root, f), self.a.decisions), m.group(0), d.get("status")))
        applied_bad = [b for b in bad if b[2] == "approved"]
        inv = self.manifest["decisions"]["invalid"]
        self.res("⑥", "파생 id(PRC-/ADV-/CFL-) target 결정 0", not bad, f"저장소 결정 중 파생 id target {len(bad)} · 그중 approved {len(applied_bad)} · 빌드가 거부한 결정 {len(inv)}")

    # -------------------------------------------------------------- ⑦
    def c7(self):
        exist = {t: {r["id"] for r in rows} for t, rows in self.ents.items()}
        dic_ids = {e["id"] for d in self.outdic["dictionaries"] for e in d["entries"]} | {d["name"] for d in self.outdic["dictionaries"]}
        erd_refs = {d["target"].get("erd_ref") for d in self.erd["decisions"]}
        broken = []
        n = 0
        for rel, es in self.rels.items():
            for e in es:
                n += 1
                for side in ("from", "to"):
                    t, i = e[side]["type"], e[side]["id"]
                    if t in exist:
                        ok = i in exist[t]
                    elif t == "dictionary":
                        ok = i in dic_ids
                    elif t == "erd":
                        ok = i in erd_refs
                    else:
                        ok = False
                    if not ok:
                        broken.append(f"{rel} {side} {t}:{i}")
        cs = jl(os.path.join(self.out, "conflicts.jsonl"))
        n9 = sum(1 for c in cs if c["kind"] == "unresolved_reference")
        self.res("⑦", "엣지 끝이 존재하는 레코드(깨진 참조 0 · 미해결은 ⑨)", not broken, f"엣지 {n} · 깨진 끝 {len(broken)} · ⑨ 레코드 {n9}" + (f" · 예 {broken[:3]}" if broken else ""))

    # -------------------------------------------------------------- ⑧
    def c8(self):
        bad = []
        n = 0
        for d in self.outdic["dictionaries"]:
            for e in d["entries"]:
                n += 1
                if not e.get("sources"):
                    bad.append(f"{d['name']}:{e['canonical']}")
                for s in e.get("synonyms", []):
                    n += 1
                    if not s.get("sources"):
                        bad.append(f"{d['name']}:{e['canonical']}/{s['value']}")
        self.res("⑧", "사전 값마다 출처", not bad, f"사전 {len(self.outdic['dictionaries'])} · 값·동의어 {n} · 출처 없음 {len(bad)}" + (f" · {bad[:3]}" if bad else ""))

    # -------------------------------------------------------------- ⑨
    def c9(self):
        g = os.path.join(self.out, "gate")
        u9 = len(load_json(os.path.join(g, "unresolved_references.json")))
        u8 = len(load_json(os.path.join(g, "unregistered_fragments.json")))
        md = open(os.path.join(g, "conflicts.md"), encoding="utf-8").read()
        m = re.search(r"## ⑦ duplicate_candidate \((\d+)\)\n\n(.*?)\n\n", md, re.S)
        u7 = int(m.group(1)) if m else -1
        rows7 = len([x for x in m.group(2).splitlines() if re.match(r"^\| \d+ \|", x)]) if m else -1
        cs = jl(os.path.join(self.out, "conflicts.jsonl"))
        c = Counter(x["kind"] for x in cs)
        want = c["duplicate_candidate"] + c["unregistered_value"] + c["unresolved_reference"]
        sk = Counter(json.dumps(x["stable_key"], sort_keys=True, ensure_ascii=False) for x in cs)
        dup_sk = sum(1 for v in sk.values() if v > 1)
        self.res("⑨", "gate 목록 합 = conflicts ⑦⑧⑨ 수", u7 + u8 + u9 == want and rows7 == u7 and u7 == c["duplicate_candidate"] and u8 == c["unregistered_value"] and u9 == c["unresolved_reference"] and dup_sk == 0,
                 f"gate ⑦ {u7}(표 행 {rows7}) + ⑧ {u8} + ⑨ {u9} = {u7 + u8 + u9} · conflicts.jsonl ⑦ {c['duplicate_candidate']} + ⑧ {c['unregistered_value']} + ⑨ {c['unresolved_reference']} = {want} · 겹치는 stable_key {dup_sk}")


    # ============================================================== V3 (ERD v3 §11)
    def post(self):
        """결정 적용 뒤 사전(out/dictionaries.json)으로 분해를 다시 돌린 결과 — 빌드와 독립 재실행."""
        if self._post is None:
            if self.is32:   # v3.2: 결정 뒤 사전(파생 항목은 빼고 분해가 다시 세운다) · v3.3: 분석기(캐시)로
                P = V32.run_v32(V32.base_dictionary(self.outdic), self.erd, self.L, bronze_version=self.bver, analyzer=self.an)[0]
            else:
                P = run_procedure(self.outdic, self.erd["resolve_rules"], self.L, bronze_version=self.bver)
            self._post = P
        return self._post

    def attr(self, r, k):
        c = r["attrs"].get(k)
        return c[0]["value"] if c else None

    def v1(self):
        """V3-1 수식 칸(v3.1 세 칸 · V3.1-9) — 사전 단위 id = ADV-sha(event|site|qualifier) · qualifier 는 사전 adverse_qualifier 값 또는 none · raw_name 은 none/none · 경과 칸 없음."""
        D = {d["name"]: d for d in self.outdic["dictionaries"]}
        qids = {e["id"]: e["canonical"] for e in D["adverse_qualifier"]["entries"]}
        bad, nq = [], 0
        for r in self.ents["adverse_effect"]:
            a = {k: self.attr(r, k) for k in ("event_kind", "event_id", "site_ref_id", "site_ref_kind", "qualifier", "qualifier_id", "anchor")}
            if "course" in r["attrs"] or "course_id" in r["attrs"]:
                bad.append(f"{r['id']} 경과 칸이 있다(v3.1 은 R15 속성)")
            if a["qualifier_id"] is None:
                bad.append(f"{r['id']} qualifier_id 없음")
                continue
            if a["event_kind"] in ("dict", "ledger"):   # v3.2: 원장 사건 노드(ledger)도 세 칸 사전 값 식별자
                if mkid("ADV", f"{a['event_id']}|{a['site_ref_id']}|{a['qualifier_id']}") != r["id"]:
                    bad.append(f"{r['id']} 식별자 ≠ 세 칸 해시")
                if a["qualifier_id"] != "none":
                    nq += 1
                    if qids.get(a["qualifier_id"]) != a["qualifier"]:
                        bad.append(f"{r['id']} qualifier 가 사전 값 아님")
            else:
                if a["qualifier_id"] != "none" or a["site_ref_id"] != "none":
                    bad.append(f"{r['id']} raw_name 인데 칸 값")
                if mkid("ADV", f"RAW:{a['anchor']}|none|none|{a['anchor']}") != r["id"]:
                    bad.append(f"{r['id']} raw 식별자 ≠ RAW:anchor")
        self.res("V3-1", "부작용 수식 칸 — 세 칸 식별자(v3.1 · v3.2 원장 사건 노드 포함) · qualifier 사전 값 · raw_name none/none · 경과 칸 없음", not bad,
                 f"단위 {len(self.ents['adverse_effect'])} · qualifier≠none {nq} · 어긋남 {len(bad)}" + (f" · {bad[:3]}" if bad else ""))

    def v2(self):
        """V3-2 괄호 안 회사·제품 — 재분해에서 적용된 라벨마다 what=product 이고 그 제품 레코드가 out 에 있다."""
        P = self.post()
        prods = {r["id"] for r in self.ents["product"]}
        T = P["PT"].tuples
        bad, n = [], 0
        rows = [r for v in P["ref_rows"].values() for r in v] + P["mk_rows"] + P["cat_recs"]
        for r in rows:
            if str(r.get("what_basis", "")).startswith("company_paren"):
                n += 1
                for x in tids_of(r):
                    if T[x]["what_kind"] != "product" or T[x]["what_id"] not in prods:
                        bad.append(str(r.get("label") or r.get("name")))
        ca = {(x["label"], x["company"]) for x in P["PT"].company_applied}
        self.res("V3-2", "괄호 안 회사·제품 규칙 — 적용 라벨의 what = 실버 제품", not bad, f"적용 레코드 {n} · 라벨 {len(ca)}(회사 {sum(1 for x in ca if x[1])} · 괄호 안 제품 {sum(1 for x in ca if not x[1])}) · 어긋남 {len(bad)}" + (f" · {bad[:3]}" if bad else ""))

    def v3(self):
        """V3-3 stopwords — 미등록 조각(gate ⑧ 시술 축)에 stopword 0 · qualifier_text 가 있는 참조의 엣지에 qualifier_text 속성."""
        words = {norm(w["word"]) for w in self.erd["resolve_rules"]["step2_decompose"]["stopwords"]["words"]}
        g8 = load_json(os.path.join(self.out, "gate", "unregistered_fragments.json"))
        leak = [r["fragment"] for r in g8 if r["axis"] == "procedure_fragment" and norm(r["fragment"]) in words]
        P = self.post()
        qt = sum(1 for v in P["ref_rows"].values() for r in v if r.get("qualifier_text") and r["result"] in ("tuple", "combo_ref", "multi_tuple"))
        e_qt = sum(1 for rel in ("R9", "R12", "R17", "R18") for e in self.rels[rel] if any(k.endswith("qualifier_text") for k in e["attrs"]))
        sess = sum(1 for e in self.rels["R12"] if "session_index" in e["attrs"])
        self.res("V3-3", "stopwords — 미등록 조각에 stopword 0 · qualifier_text 엣지 속성", not leak and (qt == 0 or e_qt > 0),
                 f"stopword 단어 {len(words)} · 미등록 조각 중 stopword {len(leak)} · qualifier_text 가진 해결 참조 {qt} · 그 엣지 {e_qt}(R9/R12/R17/R18) · R12 session_index {sess}" + (f" · {leak[:3]}" if leak else ""))

    def v4(self):
        """V3-4 `+`/`/` — multi_tuple 참조의 부위별 anchor(#s<i>)가 실버 시술 anchors 에 있다 · member_mode ∈ {and, or}."""
        P = self.post()
        anchors = {a for r in self.ents["procedure"] for a in (self.attr(r, "anchors") or [])}
        mts = [r for v in P["ref_rows"].values() for r in v if r["result"] == "multi_tuple"] + [r for r in P["mk_rows"] if r["result"] == "multi_tuple"] + [r for r in P["cat_recs"] if r["result"] == "multi_tuple"]
        miss = [a for r in mts for a in r["member_anchors"] if a not in anchors and not any(a in (x.get("folded") or []) for x in self.log.values())]
        modes = Counter(e["attrs"]["member_mode"]["value"] for rel in ("R9", "R12", "R17", "R18") for e in self.rels[rel] if "member_mode" in e["attrs"])
        badm = [m for m in modes if m not in ("and", "or")]
        alts = sum(1 for v in P["ref_rows"].values() for r in v if r.get("alternatives"))
        self.res("V3-4", "조합 기호 — multi_tuple #s<i> anchor 실버에 있음 · member_mode and|or", not miss and not badm,
                 f"multi_tuple 참조 {len(mts)}(부위별 anchor {sum(len(r['member_anchors']) for r in mts)}) · 실버에 없는 anchor {len(miss)} · 엣지 member_mode {dict(modes)} · 괄호 안 대안 참조 {alts}" + (f" · {miss[:3]}" if miss else ""))

    def v5(self):
        """V3-5 layer 금지 — 시술 튜플 site 칸에 layer 0 · site 레코드마다 kind ∈ enum · 사전 kind 와 같다."""
        D = {d["name"]: d for d in self.outdic["dictionaries"]}
        kind = {mkid("SIT", e.get("zone_id") if e.get("site_kind") == "backbone" else e["canonical"]): site_kind_of(e) for e in D["site"]["entries"]}
        layer_proc = [r["id"] for r in self.ents["procedure"] if kind.get(self.attr(r, "site_id")) == "layer"]
        bad = [r["id"] for r in self.ents["site"] if self.attr(r, "kind") not in ("anatomical", "layer", "region") or self.attr(r, "kind") != kind.get(r["id"])]
        nl = sum(1 for v in kind.values() if v == "layer")
        la = sum(1 for r in self.ents["adverse_effect"] if kind.get(self.attr(r, "site_ref_id")) == "layer")
        self.res("V3-5", "layer 는 시술 site 금지 · site.kind", not layer_proc and not bad, f"부위 {len(self.ents['site'])}(layer {nl}) · layer site 시술 {len(layer_proc)} · kind 어긋남 {len(bad)} · layer site 부작용 단위 {la}")

    def v6(self):
        """V3-6 canonical_rename — 사전 id = DIC-sha(사전|새 정준값) · renamed_from 에 옛 id · 옛 정준값 동의어(link=renamed_from) · 코드 기반 개체 id 그대로."""
        D = {d["name"]: d for d in self.outdic["dictionaries"]}
        bad, n = [], 0
        for x in self.log.values():
            if x["kind"] != "canonical_rename" or x["result"] != "applied":
                continue
            n += 1
            old, new = x["renamed"]
            e = next((e for e in D[x["dictionary"]]["entries"] if e["canonical"] == new), None)
            if e is None or e["id"] != mkid("DIC", f"{x['dictionary']}|{new}") or x["old_id"] not in [r["id"] for r in e.get("renamed_from", [])] or not any(s["value"] == old and s.get("link") == "renamed_from" for s in e["synonyms"]):
                bad.append(x["id"])
        mods = {r["id"] for r in self.ents["modality"]}
        want = {mkid("MOD", m["id"]) for m in self.L["taxonomy.json"]["modality"]}
        self.res("V3-6", "canonical_rename — DIC id 재계산 · renamed_from · 옛 정준값 동의어 · MOD-<code> 불변", not bad and mods == want,
                 f"적용 {n} · 어긋남 {len(bad)} · modality id = taxonomy 코드 {len(mods & want)}/{len(want)}" + (f" · {bad}" if bad else ""))

    def v7(self):
        """V3-7 description · media_refs — 값이 있으면 출처(locator) 필수(② 와 같은 규칙) · 지금 원천 없음."""
        cells = [(t, r["id"], k, r["attrs"][k]) for t in ("product", "technique") for r in self.ents[t] for k in ("description", "media_refs") if k in r["attrs"]]
        bad = [c[:3] for c in cells if not all(x.get("prov") or x.get("derived_from") for x in c[3])]
        srcs = [s["file"] for s in self.erd["source_files"] if s["kind"] == "research_artifact" and s["file"] != "step1-products.json"]
        self.res("V3-7", "description·media_refs — 값마다 출처 · 새 브론즈 원천 없으면 값 0", not bad and (cells == [] or srcs),
                 f"값 {len(cells)} · 출처 없는 값 {len(bad)} · 등록된 새 원천(research_artifact · step1 제외) {len(srcs)}")

    def v8(self):
        """V3-8 R5 — 엣지마다 basis ∈ {ledger, canonical_mapping} · 하위분류 from 은 적용된 canonical_mapping(R5:<하위분류>) 결정에서만."""
        bad = []
        nsub = 0
        for e in self.rels["R5"]:
            b = e["attrs"].get("basis", {}).get("value")
            if b not in ("ledger", "canonical_mapping"):
                bad.append("basis")
            if e["from"]["type"] == "modality_subcategory":
                nsub += 1
                d = e["attrs"].get("decision_id", {}).get("value")
                x = self.log.get(d) or {}
                if b != "canonical_mapping" or x.get("kind") != "canonical_mapping" or x.get("result") != "applied":
                    bad.append(f"{d}")
            elif e["from"]["type"] != "modality":
                bad.append(e["from"]["type"])
        self.res("V3-8", "R5 from modality|modality_subcategory · basis", not bad, f"R5 {len(self.rels['R5'])} · 하위분류 from {nsub} · 어긋남 {len(bad)}")

    def v9(self):
        """V3-9 결정 anchor 확장 — tuple_assign(_multi)·adverse_tuple_assign 가 anchor·locator 부재로 거부된 것 0 · 결정이 세운 ⑨ 닫힘은 그 결정이 적용됐다."""
        kinds = ("tuple_assign", "tuple_assign_multi", "adverse_tuple_assign")
        rej = [x["id"] for x in self.log.values() if x["kind"] in kinds and x["result"] == "rejected" and ("anchor" in str(x.get("why")) or "locator" in str(x.get("why")))]
        est = [x["id"] for x in self.log.values() if x["kind"] in kinds and x.get("established")]
        cs = jl(os.path.join(self.out, "conflicts.jsonl"))
        r9 = [c for c in cs if c["kind"] == "unresolved_reference" and c["status"] == "resolved"]
        bad9 = [c["id"] for c in r9 if (self.log.get(c.get("decision_id")) or {}).get("result") != "applied"]
        self.res("V3-9", "미해결·조합 anchor 에도 결정 적용(anchor 부재 거부 0)", not rej and not bad9,
                 f"③ 결정 {sum(1 for x in self.log.values() if x['kind'] in kinds)} · anchor·locator 부재 거부 {len(rej)} · 결정이 세운 자리 {len(est)} · 결정으로 닫힌 ⑨ {len(r9)}(적용 안 된 결정 {len(bad9)})")

    def v10(self):
        """V3-10 fold_approve 가 ⑦ 을 닫음 — resolved ⑦ 마다 decision_id 가 적용된 fold_approve · close_verdict 없음 · 수 = apply_log closed_duplicates 합."""
        cs = jl(os.path.join(self.out, "conflicts.jsonl"))
        r7 = [c for c in cs if c["kind"] == "duplicate_candidate" and c["status"] == "resolved"]
        bad = [c["id"] for c in r7 if (self.log.get(c.get("decision_id")) or {}).get("kind") != "fold_approve" or c.get("close_verdict")]
        want = sum(x.get("closed_duplicates") or 0 for x in self.log.values() if x["kind"] == "fold_approve")
        n7 = sum(1 for c in cs if c["kind"] == "duplicate_candidate")
        o7 = sum(1 for c in cs if c["kind"] == "duplicate_candidate" and c["status"] == "open")
        d7 = sum(1 for c in cs if c["kind"] == "duplicate_candidate" and c["status"] == "dismissed")
        self.res("V3-10", "fold_approve 가 ⑦ 을 닫음(resolved · decision_id)", not bad and len(r7) == want,
                 f"⑦ {n7} · fold 로 닫힘 {len(r7)}(apply_log 합 {want}) · conflict_close 로 닫힘 {d7} · open {o7} · 어긋남 {len(bad)}")

    # ============================================================== V3.1 (ERD v3.1 §11)
    def dic_of(self, name):
        return next((d for d in self.outdic["dictionaries"] if d["name"] == name), {"entries": []})

    def w1(self):
        """V3.1-1 product_reclassify — 새 PRD- 레코드 · 옛 id 는 alias(reclassified_from) · 옛 id 레코드 없음 · 사전 code = 새 계열 · R4 는 새 계열에서."""
        prods = {r["id"]: r for r in self.ents["product"]}
        mods = {m["id"]: mkid("MOD", m["id"]) for m in self.L["taxonomy.json"]["modality"]}
        bad, n = [], 0
        for x in self.log.values():
            if x["kind"] != "product_reclassify" or x["result"] != "applied":
                continue
            n += 1
            nr = prods.get(x["new_id"])
            if nr is None or x["old_id"] in prods or x["old_id"] not in [a["value"] for a in nr["aliases"]]:
                bad.append(f"{x['id']} 레코드/alias")
            e = next((e for e in self.dic_of("product_name")["entries"] if e["canonical"] == x["product"]), None)
            if e is None or str(e.get("code")) != x["to_code"]:
                bad.append(f"{x['id']} 사전 code")
            r4 = [e_ for e_ in self.rels["R4"] if e_["to"]["id"] == x["new_id"]]
            if any(e_["from"]["id"] == mods[x["from_code"]] for e_ in r4) or not any(e_["from"]["id"] == mods[x["to_code"]] for e_ in r4):
                bad.append(f"{x['id']} R4")
            if mkid("PRD", f"{x['to_code']}|{x['product']}") != x["new_id"]:
                bad.append(f"{x['id']} id 재계산")
        self.res("V3.1-1", "product_reclassify — PRD- 재계산 · 옛 id alias · 사전 code · R4 새 계열", not bad, f"적용 {n} · 어긋남 {len(bad)}" + (f" · {bad[:3]}" if bad else ""))

    def w2(self):
        """V3.1-2 R32 — from clinical_rule · to product|technique|proc_axis · scope/severity/basis 열거형 · source_locator 해석 · edge_create 는 적용된 결정 · ledger 는 고지 문장."""
        en = self.erd["enums"]
        bad = []
        ok_to = {"product", "technique", "procedure", "modality", "modality_subcategory"}
        rules = {r["id"]: r for r in self.ents["clinical_rule"]}
        by = Counter()
        for e in self.rels.get("R32", []):
            a = {k: v.get("value") for k, v in e["attrs"].items()}
            by[a.get("basis")] += 1
            if e["from"]["type"] != "clinical_rule" or e["from"]["id"] not in rules or e["to"]["type"] not in ok_to:
                bad.append(f"끝 {e['from']['type']}→{e['to']['type']}")
            if a.get("scope") not in en["R32.scope"] or a.get("severity") not in en["R32.severity"] or a.get("basis") not in en["R32.basis"]:
                bad.append(f"열거형 {a.get('scope')}/{a.get('severity')}/{a.get('basis')}")
            if not self.ref_ok(str(a.get("source_locator"))):
                bad.append(f"source_locator {a.get('source_locator')}")
            if a.get("basis") == "edge_create" and (self.log.get(a.get("decision_id")) or {}).get("result") != "applied":
                bad.append(f"decision {a.get('decision_id')}")
            if a.get("basis") == "ledger" and self.attr(rules.get(e["from"]["id"], {"attrs": {}}), "kind") != "disclosure":
                bad.append("ledger 인데 disclosure 아님")
        self.res("V3.1-2", "R32 rule_applies_to — 끝 · scope/severity/basis · source_locator · 값의 두 길(ledger · edge_create)", not bad, f"R32 {len(self.rels.get('R32', []))}({dict(by)}) · 어긋남 {len(bad)}" + (f" · {bad[:3]}" if bad else ""))

    def w3(self):
        """V3.1-3 dictionary_remove — 뺀 동의어·값이 사전에 없고 이력(removed_synonyms · removed_entries)에 있다 · 거부(in_use)는 사전이 그대로."""
        bad, n = [], 0
        for x in self.log.values():
            if x["kind"] != "dictionary_remove":
                continue
            d = self.dic_of(x.get("dictionary"))
            if x["result"] != "applied":
                continue
            n += 1
            if x.get("removed_synonym"):
                e = next((e for e in d["entries"] if e["canonical"] == x["canonical"]), None)
                if e is None or any(norm(s_["value"]) == norm(x["removed_synonym"]) for s_ in e["synonyms"]) or not any(h["decision_id"] == x["id"] for h in d.get("removed_synonyms") or []):
                    bad.append(x["id"])
            else:
                if any(e["canonical"] == x["removed_entry"] for e in d["entries"]) or not any(h["decision_id"] == x["id"] for h in d.get("removed_entries") or []):
                    bad.append(x["id"])
        self.res("V3.1-3", "dictionary_remove — 사전에서 빠짐 · 이력 기록", not bad, f"적용 {n} · 어긋남 {len(bad)}")

    def w4(self):
        """V3.1-4 조건 단위 — id = CND-sha(kind|정준값)(사전) / CND-sha(RAW:kind|norm(원문))(raw) · 문장 자리 471 전부 부록 · R16/R17 끝 = 단위 · source_phrases."""
        bad = []
        occ = condition_occurrences(self.L)
        seen = set()
        for r in self.ents["person_condition"]:
            k, nk, nm = self.attr(r, "kind"), self.attr(r, "name_kind"), self.attr(r, "name")
            want = mkid("CND", f"{k}|{nm}") if nk == "dict" else mkid("CND", f"RAW:{k}|{norm(nm)}")
            if want != r["id"]:
                bad.append(f"{r['id']} 식별자")
            for ph in self.attr(r, "phrases") or []:
                seen.add(ph["locator"])
        if len(seen) != len(occ):
            bad.append(f"부록 문장 자리 {len(seen)} ≠ 원장 {len(occ)}")
        cids = {r["id"] for r in self.ents["person_condition"]}
        for rel in ("R16", "R17"):
            for e in self.rels[rel]:
                side = "to" if rel == "R16" else "from"
                if e[side]["id"] not in cids or ("source_phrases" not in e["attrs"] and "decision_id" not in e["attrs"]):
                    bad.append(f"{rel} 끝·source_phrases")
                    break
        nd = sum(1 for r in self.ents["person_condition"] if self.attr(r, "name_kind") == "dict")
        self.res("V3.1-4", "조건 단위 — 식별자 · 문장 부록 전수 · R16/R17 끝 단위 + source_phrases", not bad, f"단위 {len(cids)}(사전 {nd} · raw {len(cids) - nd}) · 문장 자리 {len(seen)}/{len(occ)} · 어긋남 {len(bad)}" + (f" · {bad[:3]}" if bad else ""))

    def w5(self):
        """V3.1-5 회·차 — R12 자리의 session_index/session_count 가 엣지 속성 · R9/R17/R18 엣지에 session_* 없음."""
        P = self.post()
        want_c = sum(1 for slot, v in P["ref_rows"].items() for r in v if r.get("session_relation") == "R12" and r.get("session_count") is not None)
        got_c = sum(1 for e in self.rels["R12"] if "session_count" in e["attrs"])
        got_i = sum(1 for e in self.rels["R12"] if "session_index" in e["attrs"])
        leak = sum(1 for rel in ("R9", "R17", "R18") for e in self.rels[rel] if any(k.endswith(("session_count", "session_index")) for k in e["attrs"]))
        ss = P["summary"]["session_summary"]
        self.res("V3.1-5", "회·차 — R12 session_count/index · 다른 자리는 qualifier_text", leak == 0 and (want_c == 0 or got_c > 0), f"규격 토큰 {ss['total']}(R12 차 {ss['r12_session_index']} · 회 {ss['r12_session_count']} · qualifier_text {ss['to_qualifier_text']}) · 회 있는 R12 참조 {want_c} · 엣지 count {got_c} · index {got_i} · R9/R17/R18 누출 {leak}")

    def w6(self):
        """V3.1-6 stopwords 겹침 — 실측(값 사전 전수) = ERD 규칙 데이터 overlap."""
        P = self.post()
        got = [o["word"] for o in P["summary"]["stopwords"].get("overlap", [])]
        want = [o["word"] for o in self.erd["resolve_rules"]["step2_decompose"]["stopwords"].get("overlap", [])]
        P0 = self._pre[0] if getattr(self, "_pre", None) else None
        got0 = [o["word"] for o in P0["summary"]["stopwords"]["overlap"]] if P0 else got
        note = ""
        if self.is32:
            # v3.2 json 의 overlap 필드는 빈 목록(ERD 생성기가 실측 전 명세 값을 실었다) — 실측 정본은 erd-v3.2-tuples.json 요약
            meas = [o["word"] for o in load_json(self.a.tuples)["procedure"]["summary"]["stopwords"]["overlap"]]
            note = f" · ERD json overlap 필드 {want}(실측 전 값 · ERD 쪽 기록 · 실측 정본은 tuples 요약)"
            want = meas
        self.res("V3.1-6", "stopwords 겹침 — 결정 전 실측 = ERD overlap(" + ("erd-v3.2-tuples.json 실측" if self.is32 else "ERD 목록") + ")", got0 == want, f"ERD {want} · 결정 전 {got0} · 결정 뒤 사전 {got}({P['summary']['stopwords'].get('dictionaries_checked')} 사전)" + note)

    def w7(self):
        """V3.1-7 필수 고지 — clinical_rule(disclosure) = 정규화 문장 distinct · R32 ledger = 고지 자리 수 · modality.mandatory_disclosures 없음 · phrase_ids 가 문구 사전 항목."""
        cats = self.L["consent-checklist.json"]["categories"]
        n = sum(len(c.get("mandatory_disclosures") or []) for c in cats)
        distinct = {norm(x) for c in cats for x in c.get("mandatory_disclosures") or []}
        disc = [r for r in self.ents["clinical_rule"] if self.attr(r, "kind") == "disclosure"]
        led = [e for e in self.rels.get("R32", []) if e["attrs"].get("basis", {}).get("value") == "ledger"]
        mod_attr = sum(1 for r in self.ents["modality"] if "mandatory_disclosures" in r["attrs"])
        if self.is32:
            # v3.2(V3.2-0): 고지는 자기 테이블 — adverse_ref(이미 있는 단위만) · ref_status · phrase_ids 없음
            units = {r["id"] for r in self.ents["adverse_effect"]}
            en = set(self.erd["enums"].get("table_line.ref_status", [])) | {"ref", "ref_partial", "none"}
            badp = [r["id"] for r in disc if "phrase_ids" in r["attrs"] or self.attr(r, "ref_status") not in en or any(u not in units for u in (self.attr(r, "adverse_ref") or []))]
            what = "adverse_ref · ref_status(v3.2)"
        else:
            pids = {e["id"] for e in self.dic_of("phrase_dictionary")["entries"]}
            badp = [r["id"] for r in disc if not self.attr(r, "phrase_ids") or any(p_ not in pids for p_ in self.attr(r, "phrase_ids"))]
            what = "phrase_ids"
        ok = len(disc) == len(distinct) and len(led) == n and mod_attr == 0 and not badp
        self.res("V3.1-7", f"필수 고지 — clinical_rule(disclosure) · R32 ledger · 계열 속성 없음 · {what}", ok, f"고지 {n}(distinct {len(distinct)}) · disclosure 레코드 {len(disc)} · R32 ledger {len(led)} · modality 속성 {mod_attr} · {what} 어긋남 {len(badp)}")

    def w8(self):
        """V3.1-8 안전 문구 수식어 — 단어·패턴마다 locator ≥1(ERD 데이터) · 게이트 ⑧ 부작용 조각에 수식어 단어 0 · 문구 사전 parsed 에 보존."""
        aw = self.erd["tuple_rules"]["adverse"]["adverse_stopwords"]
        words = {norm(w["word"]) for w in aw["words"]}
        noloc = [w["word"] for w in aw["words"] if not w.get("locators")] + [p_["regex"] for p_ in aw["patterns"] if not p_.get("locators")]
        g8 = load_json(os.path.join(self.out, "gate", "unregistered_fragments.json"))
        leak = [r["fragment"] for r in g8 if r["axis"] == "adverse_fragment" and norm(r["fragment"]) in words]
        kept = sum(1 for e in self.dic_of("phrase_dictionary")["entries"] for k in ("degree", "timing", "incidence", "condition", "connector", "misc") for _ in e["parsed"].get(k, []))
        self.res("V3.1-8", "안전 문구 수식어 — 단어·패턴 locator · 미등록 조각에 수식어 0 · parsed 보존", not noloc and not leak, f"단어 {len(aw['words'])} · 패턴 {len(aw['patterns'])} · locator 없음 {len(noloc)} · ⑧ 누출 {len(leak)} · parsed 수식어 토큰 {kept}" + (f" · {leak[:3]}" if leak else ""))

    def w9(self):
        """V3.1-9 단위 세 칸 · 경과는 R15 엣지 — R31 끝 site 만 · R15.course ⊆ 경과 사전 · 문구 유래 R15.course ⊆ 그 단위 후보의 경과(원칙 C · S-1) · 문구가 세운 단위는 세 칸 전부 사전 값."""
        courses = {e["canonical"] for e in self.dic_of("course")["entries"]}
        ph = {e["id"]: e for e in self.dic_of("phrase_dictionary")["entries"]}
        bad = []
        if any(e["to"]["type"] != "site" for e in self.rels["R31"]):
            bad.append("R31 끝 site 아님")
        nco = 0
        for e in self.rels["R15"]:
            co = (e["attrs"].get("course") or {}).get("value") or []
            if co:
                nco += 1
            if any(c not in courses for c in co):
                bad.append(f"R15 course 사전 밖 {co}")
            sp = (e["attrs"].get("source_phrases") or {}).get("value") or []
            if self.is32 and any((e["attrs"].get(k) or {}).get("value") for k in ("names", "timeline_refs", "decision_ids")):
                continue   # v3.2: (출발, 단위) 엣지 하나에 이름·타임라인 줄(결정)의 경과가 함께 — 문구 후보 대조는 문구만 낸 엣지에서
            if sp and not e["attrs"].get("decision_id"):
                uid = e["to"]["id"]
                pool = set()
                for pid in sp:
                    x = ph.get(pid) or {}
                    if x.get("mapped_courses") is not None:
                        pool |= set(x["mapped_courses"])
                    else:
                        pool |= {c for cd in x.get("candidates", []) if cd.get("unit_id") == uid or mkid("ADV", f"{cd.get('event_id')}|{cd.get('site_id')}|{cd.get('qualifier_id')}") == uid for c in cd.get("courses") or []}
                if set(co) - pool:
                    bad.append(f"R15 경과가 단위 후보 밖 {e['to']['id']} {co}")
        created = [r for r in self.ents["adverse_effect"] if self.attr(r, "created_by_phrase")]
        badc = [r["id"] for r in created if not self.attr(r, "all_dict_values") or self.attr(r, "unregistered_fragments")]
        self.res("V3.1-9", "단위 세 칸 · 경과는 R15 엣지(원칙 C) · R31 site 만 · 문구가 세운 단위 세 칸 사전 값", not bad and not badc,
                 f"R15 {len(self.rels['R15'])} · 경과 있는 엣지 {nco} · 문구가 세운 단위 {len(created)}(위반 {len(badc)}) · 어긋남 {len(bad)}" + (f" · {bad[:3]}" if bad else ""))

    def w10(self):
        """V3.1-10 문구 사전 — adverse_expression·R29 없음 · 원장 문구 자리 전부가 항목 하나에 · 부록 합(R15 source_phrases · 단위 explanations · 게이트 unlinked) = 항목 수."""
        bad = []
        if "adverse_expression" in self.ents or "R29" in self.rels:
            bad.append("adverse_expression/R29 산출")
        E = self.dic_of("phrase_dictionary")["entries"]
        locs = [l for e in E for l in e["locators"]]
        if len(locs) != len(set(locs)):
            bad.append("한 자리가 두 항목에")
        on_edge = {p_ for e in self.rels["R15"] for p_ in ((e["attrs"].get("source_phrases") or {}).get("value") or [])}
        on_unit = {x["phrase_id"] for r in self.ents["adverse_effect"] for x in (self.attr(r, "explanations") or [])}
        gate = {r["phrase_id"] for r in load_json(os.path.join(self.out, "gate", "unlinked_phrases.json"))}
        none_ = {e["id"] for e in E if (e["status"] == "approved" and not e["units"]) or e["status"] in ("note", "sentence")}   # v3.2 메모·설명문은 단위 없음
        lost = [e["id"] for e in E if e["id"] not in on_edge | on_unit | gate | none_]
        wrong_gate = [e["id"] for e in E if (e["id"] in gate) != (e["status"] == "unlinked")]
        st = Counter(e["status"] for e in E)
        self.res("V3.1-10", "문구 사전 — 표현 개체·R29 없음 · 자리 하나 = 항목 하나 · 부록(엣지·단위·게이트) 합 = 항목", not bad and not lost and not wrong_gate,
                 f"항목 {len(E)}({dict(st)}) · 자리 {len(locs)} · 엣지 부록 {len(on_edge)} · 단위 부록 {len(on_unit)} · 게이트 {len(gate)} · 부작용 아님 {len(none_)} · 빠진 항목 {len(lost)} · 게이트 어긋남 {len(wrong_gate)}" + (f" · {bad}" if bad else ""))

    # ============================================================== V3.2 (ERD v3.2 §11 · 발주서 silver-build-7-brief.md A)
    def x0(self):
        """V3.2-0 문구 종류 — 부작용 문구 자리(safety.*) 전부가 문구 사전(부작용 · 메모) 항목 하나에 · 미연결(unlinked) 0 · 단위에 닿는 항목은 단위가 있다 · 메모·설명문은 단위 없음 · 이름 단위(raw_name) 0."""
        occ = [s_["locator"] for k, t, s_ in adverse_phrases31(self.L) if k == "safety_phrase"]
        E = self.dic_of("phrase_dictionary")["entries"]
        locs = [l for e in E for l in e["locators"]]
        st = Counter(e["status"] for e in E)
        bad = []
        if sorted(locs) != sorted(occ):
            bad.append(f"자리 {len(locs)} ≠ 원장 부작용 문구 {len(occ)}")
        if st.get("unlinked") or st.get("auto"):
            bad.append("v3.1 status")
        bad += [e["id"] for e in E if e["status"] in ("exact", "new") and not e["units"]]
        bad += [e["id"] for e in E if e["status"] in ("note", "sentence") and e["units"]]
        raw = [r["id"] for r in self.ents["adverse_effect"] if self.attr(r, "event_kind") not in ("dict", "ledger")]
        enum = set(self.erd["enums"]["phrase_dictionary.status"])
        bad += [f"status 열거 밖 {k}" for k in st if k not in enum]
        g = load_json(os.path.join(self.out, "gate", "unlinked_phrases.json"))
        self.res("V3.2-0", "문구 종류 — 부작용 문구만 문구 사전 · unlinked 0 · 이름 단위 0", not bad and not raw and not g,
                 f"부작용 문구 자리 {len(occ)} · 항목 {len(E)}({dict(st)}) · 이름 단위 {len(raw)} · 게이트 unlinked {len(g)} · 어긋남 {len(bad)}" + (f" · {bad[:3]}" if bad else ""))

    def x1(self):
        """V3.2-0 노드 원칙 — 원장 사건 노드(adverse_event_type origin=ledger) 마다 locator·문맥(설명) · status unreviewed · 노드 단위는 그 노드의 id 로 · ⑦ 노드 쌍 = 분해 실측(strong/weak) · 추정 매칭 0(규칙 이름만)."""
        E = self.dic_of("adverse_event_type")["entries"]
        nodes = [e for e in E if e.get("origin") == "ledger"]
        if self.is33:   # v3.3: 정식 노드 — status 필드 없음 · category 없음
            bad = [e["canonical"] for e in nodes if not e.get("locators") or not e.get("contexts") or "status" in e or "category" in e or e["id"] != mkid("DIC", f"adverse_event_type|{e['canonical']}")]
        else:
            bad = [e["canonical"] for e in nodes if not e.get("locators") or not e.get("contexts") or e.get("status") != "unreviewed" or e["id"] != mkid("DIC", f"adverse_event_type|{e['canonical']}")]
        nid = {e["id"] for e in nodes}
        lu = [r for r in self.ents["adverse_effect"] if self.attr(r, "event_kind") == "ledger"]
        bad += [r["id"] for r in lu if self.attr(r, "event_id") not in nid or not self.attr(r, "event_origin_locators")]
        cs = [c for c in jl(os.path.join(self.out, "conflicts.jsonl")) if c["kind"] == "duplicate_candidate" and c["target_type"] == "adverse_event_type"]
        rules = {"paren_pair", "word_contains", "jamo1", "substring", "first_syllable"}
        badr = [c["id"] for c in cs if not c.get("pair") or not c["stable_key"].get("pair") or any(not (r in rules or r.startswith(("suffix_", "prefix"))) for r in c["pair"]["rules"]) or c["pair"]["grade"] not in ("strong", "weak")]
        gr = Counter((c["pair"]["grade"], c["status"]) for c in cs if c.get("pair"))
        self.res("V3.2-0b", "원장 사건 노드 — locator·설명·" + ("정식(status 없음)" if self.is33 else "unreviewed") + " · 단위 event_kind=ledger · ⑦ 노드 쌍 규칙만(strong/weak)", not bad and not badr,
                 f"노드 {len(nodes)} · 노드 단위 {len(lu)} · ⑦ 노드 쌍 {len(cs)}({dict(gr)}) · 어긋남 {len(bad) + len(badr)}" + (f" · {(bad + badr)[:3]}" if bad or badr else ""))

    def x2(self):
        """V3.2-1/2 토큰화·병기 — 뗀 조사·어미·문법 낱말은 보존(문구 parsed.grammar · 시술 grammar_tokens · 버림 0) · 결정 뒤 재분해의 grammar 조각 = 실버 시술 grammar_tokens."""
        P = self.post()
        rows = [r for v in P["ref_rows"].values() for r in v] + P["mk_rows"] + P["cat_recs"]
        rows = [r for r in rows if r.get("result") in ("tuple", "multi_tuple", "combo_ref") or "catalog_item_id" in r]   # 튜플을 낸 자리(미해결은 ⑨ 레코드가 조각을 든다)
        want = Counter(g for r in rows for g in (r.get("grammar_tokens") or []))
        got = Counter()
        for r in self.ents["procedure"]:
            got.update(self.attr(r, "grammar_tokens") or [])
        miss = [g for g in want if g not in got]
        E = self.dic_of("phrase_dictionary")["entries"]
        ng = sum(len(e["parsed"].get("grammar") or []) for e in E)
        ngl = sum(len(e["parsed"].get("gloss") or []) for e in E)
        self.res("V3.2-1", "토큰화·병기 — grammar 조각 보존(시술 grammar_tokens · 문구 parsed.grammar · gloss)", not miss and (not want or got),
                 f"재분해 grammar 조각 distinct {len(want)} · 실버 시술에 없는 조각 {len(miss)} · 문구 parsed.grammar {ng} · gloss {ngl}" + (f" · {miss[:3]}" if miss else ""))

    def x3(self):
        """V3.2-5/6 장비 제품 · 성분 what — origin=taxonomy 제품은 사전 항목(origin=taxonomy)마다 · 출처 taxonomy 항목 이름 · R4(계열 → 제품) · 성분 what 튜플은 성분 사전 id."""
        pn = {mkid("PRD", f"{e['code']}|{e['canonical']}"): e for e in self.dic_of("product_name")["entries"] if e.get("origin") == "taxonomy"}
        prods = {r["id"]: r for r in self.ents["product"]}
        bad = [pid for pid in pn if pid not in prods or self.attr(prods[pid], "origin") != "taxonomy"]
        r4 = {e["to"]["id"] for e in self.rels["R4"] if (e["attrs"].get("basis") or {}).get("value") == "equipment_auto"}
        bad += [f"R4 {pid}" for pid in pn if pid not in r4]
        ing = {e["id"] for e in self.dic_of("ingredient_material")["entries"]}
        iw = [r for r in self.ents["procedure"] if self.attr(r, "what_kind") == "ingredient"]
        bad += [r["id"] for r in iw if self.attr(r, "what_id") not in ing]
        r27 = {e["from"]["id"] for e in self.rels["R27"]}
        bad += [f"R27 {r['id']}" for r in iw if r["id"] in r27]
        self.res("V3.2-5", "장비 = 제품 자동 등록(origin=taxonomy · R4) · 성분 what(사전 id · R27 없음)", not bad, f"장비 제품 {len(pn)} · R4 장비 {len(r4)} · 성분 what 튜플 {len(iw)} · 어긋남 {len(bad)}" + (f" · {bad[:3]}" if bad else ""))

    def x4(self):
        """V3.2-8 R15 상속 — 엣지마다 inheritance 8 속성 · basis ∈ 열거 · 값 복사 0 · ref 가 가리키는 것이 있다(원장 locator · R15:계열→단위 · 단위.general_management) · layer ∈ 열거 · v3.1 속성(period·phase_label·reaction_level·disclosure) 없음."""
        en_b, en_l = set(self.erd["enums"]["R15.inheritance.basis"]), set(self.erd["enums"]["R15.layer"])
        units = {r["id"]: r for r in self.ents["adverse_effect"]}
        fam = {(e["attrs"].get("names") or {}).get("value") and None for e in self.rels["R15"]}
        fam_keys = set()
        for e in self.rels["R15"]:
            if e["from"]["type"] == "modality":
                fam_keys.add((e["from"]["id"], e["to"]["id"]))
        mods = {r["attrs"]["code"][0]["value"] if "code" in r["attrs"] else None: r["id"] for r in self.ents["modality"]}
        mod_by_code = {m["id"]: mkid("MOD", m["id"]) for m in self.L["taxonomy.json"]["modality"]}
        bad, n = [], 0
        bb = Counter()
        for e in self.rels["R15"]:
            if "pih_risk" in e["attrs"]:
                continue
            n += 1
            a = e["attrs"]
            if any(k in a for k in ("period", "phase_label", "reaction_level", "disclosure")):
                bad.append("v3.1 속성")
            if (a.get("layer") or {}).get("value") not in en_l:
                bad.append("layer")
            inh = (a.get("inheritance") or {}).get("value") or []
            if len(inh) != 8:
                bad.append(f"inheritance {len(inh)}")
            for x in inh:
                bb[x.get("basis")] += 1
                if x.get("basis") not in en_b or "value" in x:
                    bad.append("basis/value")
                ref = x.get("ref")
                if x["basis"] in ("item", "family") and str(ref).startswith("R15:"):
                    code, uid = ref[4:].split("→")
                    if (mod_by_code.get(code), uid) not in fam_keys or not self.ref_ok(x.get("ref_locator", "")):
                        bad.append(f"ref {ref}")
                elif x["basis"] in ("item", "family") and not self.ref_ok(str(ref)):
                    bad.append(f"ref {ref}")
                elif x["basis"] == "unit" and not (units.get(str(ref).split(".")[0]) and self.attr(units[str(ref).split(".")[0]], "general_management")):
                    bad.append(f"unit ref {ref}")
        self.res("V3.2-8", "R15 상속 — inheritance 8 · basis 열거 · 값 복사 0 · ref 존재 · layer · v3.1 속성 없음", not bad, f"R15(pih 제외) {n} · basis {dict(bb)} · 어긋남 {len(bad)}" + (f" · {bad[:3]}" if bad else ""))

    def x5(self):
        """V3.2-9 타임라인 · 응급 징후 — 타임라인 레코드 = 원장 timelines · 줄 = 원장 줄 전부 · 줄 adverse_ref ⊆ 단위 · R34 = 참조 합 · R33 타임라인마다 하나 이상 · 응급 징후 = 정규화 문장 distinct · R35 = 참조 합."""
        tls = self.L["post-procedure-timeline.json"]["timelines"]
        n_lines = sum(len(ph.get(k) or []) for t in tls for ph in t["phases"] for k in ("normal", "abnormal", "caution", "emergency"))
        units = {r["id"] for r in self.ents["adverse_effect"]}
        T = self.ents.get("post_procedure_timeline", [])
        lines = [ln for r in T for ln in (self.attr(r, "lines") or [])]
        bad = [ln["locator"] for ln in lines if any(u not in units for u in ln["adverse_ref"]) or ln["ref_status"] not in self.erd["enums"]["table_line.ref_status"]]
        refs = sum(len(ln["adverse_ref"]) for ln in lines)
        r33 = Counter(e["to"]["id"] for e in self.rels.get("R33", []))
        sg = self.ents.get("emergency_sign", [])
        distinct = {norm(x) for c in self.L["consent-checklist.json"]["categories"] for x in c.get("emergency_signs") or []}
        srefs = sum(len(self.attr(r, "adverse_ref") or []) for r in sg)
        ok = len(T) == len(tls) and len(lines) == n_lines and not bad and refs == len(self.rels.get("R34", [])) and set(r33) == {r["id"] for r in T} and len(sg) == len(distinct) and srefs == len(self.rels.get("R35", []))
        self.res("V3.2-9", "타임라인(줄 전부 · R34 · R33) · 응급 징후(R35) — 참조만", ok,
                 f"타임라인 {len(T)}/{len(tls)} · 줄 {len(lines)}/{n_lines} · 줄 참조 {refs} · R34 {len(self.rels.get('R34', []))} · R33 {sum(r33.values())} · 응급 징후 {len(sg)}/{len(distinct)} · 참조 {srefs} · R35 {len(self.rels.get('R35', []))} · 어긋남 {len(bad)}")

    def x6(self):
        """V3.2-7 메모·설명문 · 문헌 — 메모 항목은 R15 source_phrases 에 없다 · 문헌 adverse_effects = evidence_statement(kind=adverse_effects) · adverse_ref ⊆ 단위 · 단위 general_description 이 그 레코드를 가리킨다."""
        E = self.dic_of("phrase_dictionary")["entries"]
        memo = {e["id"] for e in E if e["status"] in ("note", "sentence")}
        on_edge = {p_ for e in self.rels["R15"] for p_ in ((e["attrs"].get("source_phrases") or {}).get("value") or [])}
        n_lit = sum(len(c.get("adverse_effects") or []) for c in self.L["literature-evidence.json"]["categories"].values())
        ev = [r for r in self.ents["evidence_statement"] if self.attr(r, "kind") == "adverse_effects"]
        units = {r["id"]: r for r in self.ents["adverse_effect"]}
        bad = [r["id"] for r in ev if any(u not in units or r["id"] not in [x["ref"] for x in self.attr(units[u], "general_description") or []] for u in self.attr(r, "adverse_ref") or [])]
        self.res("V3.2-7", "메모·설명문(R15 없음) · 문헌 adverse_effects 근거 문장 · general_description 참조", not (memo & on_edge) and len(ev) == n_lit and not bad,
                 f"메모·설명문 항목 {len(memo)} · R15 에 오른 메모 {len(memo & on_edge)} · 문헌 adverse_effects {len(ev)}/{n_lit} · 참조 어긋남 {len(bad)}")

    def x7(self):
        """정의 표 · 개체 22 · 관계 34 — 산출 개체·관계 = ERD 목록 · 이름 단위(raw_name) 속성 없음 · 결정 게이트 5(batch5) 옵션 결정 본문 검증 · 원문 읽기 실패 0."""
        from lib.decisions import validate
        ents = {e["key"] for e in self.erd["entities"]}
        rels = {r["id"] for r in self.erd["relations"]}
        bad = []
        if set(self.ents) != ents:
            bad.append(f"개체 {sorted(set(self.ents) ^ ents)}")
        if set(self.rels) != rels:
            bad.append(f"관계 {sorted(set(self.rels) ^ rels)}")
        bad += [r["id"] for r in self.ents["adverse_effect"] if any(k in r["attrs"] for k in ("raw_reason", "candidate_name", "dict_tuples"))]
        gp = os.path.join(self.out, "gate", "batch6.json" if self.is33 else "batch5.json")
        nl = no = nf = 0
        if os.path.exists(gp):
            items = load_json(gp)
            rp = os.path.join(self.out, "gate", "batch5-reduced.json")
            red = load_json(rp) if os.path.exists(rp) else []
            for it in red:   # 축소본 — 일괄 옵션(decision_payloads · exclude_payloads)까지 결정 본문 검증
                for s_ in it.get("subitems") or [it]:
                    for o in s_["options"]:
                        for pl in list(o.get("decision_payloads") or []) + list((o.get("exclude_payloads") or {}).values()):
                            no += 1
                            pl = {k: v for k, v in pl.items() if k not in ("_store", "seed_value")}
                            if [x for x in validate(dict(pl, decided_by="x")) if "decided_by" not in x]:
                                bad.append(f"축소본 {s_['id']} {o['key']}")
            rule_files = os.path.join(self.a.decisions, "batch5-rule")
            for f in sorted(os.listdir(rule_files)) if os.path.isdir(rule_files) else []:
                d = load_json(os.path.join(rule_files, f))
                if not str(d.get("decided_by", "")).startswith("rule:") or d.get("rule_id") not in str(d.get("reason")):
                    bad.append(f"규칙 결정 {f} decided_by·사유")
            for it in items:
                for s_ in it.get("subitems") or [it]:
                    nl += 1
                    for e in s_["evidence"]:
                        if str(e["text"]).startswith("<읽기 실패"):
                            nf += 1
                    for o in s_["options"]:
                        if o["decision_payload"]:
                            no += 1
                            errs = [x for x in validate(dict(o["decision_payload"], decided_by="x")) if "decided_by" not in x]
                            if errs:
                                bad.append(f"{s_['id']} {o['key']}")
        else:
            bad.append(("batch6" if self.is33 else "batch5") + ".json 없음")
        gname = "게이트 6" if self.is33 else "게이트 5(원본 · 축소본 · 규칙 결정)"
        self.res("V3.2-10", f"개체 22 · 관계 {len(self.erd['relations'])} · raw_name 속성 없음 · {gname} 결정 본문 · 원문 읽기 실패 0", not bad and nf == 0,
                 f"개체 {len(self.ents)} · 관계 {len(self.rels)} · {gname} 자리 {nl} · 결정 본문 {no} · 읽기 실패 {nf} · 어긋남 {len(bad)}" + (f" · {bad[:3]}" if bad else ""))

    # ============================================================== V3.3 (ERD v3.3 §11 · 발주서 silver-build-8-brief.md)
    def y1(self):
        """V3.3-A 제품 구성품 — product.kind ∈ enum · 전부 product(원장 칸 없음) · component_of/component_kind null · R36 파일 있음 · 엣지 0 · what_kind=component 튜플 0 · R27 끝 product."""
        en = set(self.erd["enums"].get("product.kind", []))
        bad = []
        kinds = Counter()
        for r in self.ents["product"]:
            k = self.attr(r, "kind")
            kinds[k] += 1
            if k not in en or self.attr(r, "component_of") is not None or self.attr(r, "component_kind") is not None:
                bad.append(r["id"])
        r36 = self.rels.get("R36")
        comp = [r["id"] for r in self.ents["procedure"] if self.attr(r, "what_kind") == "component"]
        if r36 is None:
            bad.append("R36.jsonl 없음")
        self.res("V3.3-A", "제품 구성품 — product.kind(product 전부 · 값 0) · R36 파일(엣지 0) · what_kind=component 0", not bad and not comp and r36 == [],
                 f"product {len(self.ents['product'])} · kind {dict(kinds)} · R36 {len(r36 or [])} · component 튜플 {len(comp)} · 어긋남 {len(bad)}" + (f" · {bad[:3]}" if bad else ""))

    def y2(self):
        """V3.3-B 분석기 — out/kiwi-cache.json(판 0.24 고정 · 등록 사전 해시 · 문구) · 정본 캐시가 산출 항목 전부를 품음 · 결정 뒤 재분해(캐시만 · 워커 호출 0)가 out 의 사건 노드와 같다."""
        p = os.path.join(self.out, "kiwi-cache.json")
        bad = []
        if not os.path.exists(p):
            self.res("V3.3-B", "분석기 캐시 · 판 고정 · 재분해 일치", False, "out/kiwi-cache.json 없음")
            return
        kc = load_json(p)
        ver = kc.get("kiwi_version") or ""
        pinned = str(self.erd["resolve_rules"]["tokenize"]["analyzer"]["version_pinned"])
        if not ver.startswith(pinned):
            bad.append(f"판 {ver} ≠ 고정 {pinned}")
        n_ent = sum(d["n_entries"] for d in kc["dicts"].values())
        store = self.an.store
        missing = sum(1 for dh, d in kc["dicts"].items() for t in d["entries"] if t not in store.get("dicts", {}).get(dh, {}).get("entries", {}))
        if missing:
            bad.append(f"정본 캐시에 없는 산출 항목 {missing}")
        calls0 = self.an.calls
        from lib import decisions as DC
        approved = [d for f_, d in DC.load_store(self.a.decisions) if d.get("status") == "approved" and not DC.validate(d)]
        folds, excl, _ = DC.node_decisions(approved)
        P, A, C, X = V32.run_v32(V32.base_dictionary(self.outdic), self.erd, self.L, bronze_version=self.bver, analyzer=self.an, node_folds=folds, not_adverse=excl)
        got = sorted(n["canonical"] for n in A["ledger_events"])
        want = sorted(e["canonical"] for e in self.dic_of("adverse_event_type")["entries"] if e.get("origin") == "ledger")
        if got != want:
            bad.append(f"재분해 사건 노드 {len(got)} ≠ out {len(want)} · 예 {sorted(set(got) ^ set(want))[:3]}")
        if self.an.calls != calls0:
            bad.append(f"재분해가 워커를 {self.an.calls - calls0} 번 불렀다(캐시 밖 문구)")
        self.res("V3.3-B", "분석기 캐시(out/kiwi-cache.json) · 판 고정 · 정본 캐시 포함 · 캐시만으로 재분해 = out 사건 노드", not bad,
                 f"kiwipiepy {ver}(고정 {pinned}) · 산출 항목 {n_ent}(사전 묶음 {len(kc['dicts'])}) · 정본 캐시 항목 {sum(len(d['entries']) for d in store.get('dicts', {}).values())} · 재분해 노드 {len(got)} · 워커 호출 {self.an.calls - calls0} · 어긋남 {len(bad)}" + (f" · {bad[:3]}" if bad else ""))

    def y3(self):
        """V3.3-C R2 사전 값 · 부위 — 옛 표면형 「혈관 폐색」 0 · (폐색, 혈관) 단위 있음 · (혈관 폐색, none) 0 · 폐색↔색전 공유 동의어 0 · 한 단위에 둘 0 · 부위 사전 동맥·정맥·안동맥(parent) · 6-A 부위 15 · 성분 6."""
        D = {d["name"]: d for d in self.outdic["dictionaries"]}
        ev = D["adverse_event_type"]["entries"]
        bad = []
        old = sum(1 for e in ev for v in [e["canonical"]] + [s_["value"] for s_ in e.get("synonyms", [])] if norm(v) == norm("혈관 폐색"))
        if old:
            bad.append(f"옛 표면형 혈관 폐색 {old}")
        for r in self.erd["tuple_rules"]["adverse"].get("event_decomposed_v33", []):
            e = next((x for x in ev if x["canonical"] == r["event"]), None)
            if e is None or (e.get("decomposed_from") or {}).get("value") != r["old"]:
                bad.append(f"분해 꼴 {r['old']} → {r['event']} 사전 기록 없음")
        units = {(self.attr(r, "event"), self.attr(r, "site") or "none"): r["id"] for r in self.ents["adverse_effect"]}
        if ("폐색", "혈관") not in units:
            bad.append("(폐색, 혈관) 단위 없음")
        if any(k[0] == "혈관 폐색" for k in units):
            bad.append("(혈관 폐색, …) 단위 있음")
        occ = next((x for x in ev if x["canonical"] == "폐색"), {})
        emb = next((x for x in ev if x["canonical"] == "색전"), {})
        shared = {norm(s_["value"]) for s_ in occ.get("synonyms", [])} & {norm(s_["value"]) for s_ in emb.get("synonyms", [])}
        if shared:
            bad.append(f"폐색↔색전 공유 동의어 {shared}")
        site = {e["canonical"]: e for e in D["site"]["entries"]}
        for v, par in (("동맥", "혈관"), ("정맥", "혈관"), ("안동맥", "동맥")):
            if v not in site or site[v].get("parent") != par:
                bad.append(f"부위 {v}(parent {par}) 없음")
        seeds = self.erd["tuple_rules"]["seed"]["approved_v33"]
        miss_s = [s["value"] for s in seeds["site"] if s["value"] not in site or site[s["value"]].get("parent") != s["parent"] or site[s["value"]].get("kind") != s["kind"]]
        ing = {e["canonical"] for e in D["ingredient_material"]["entries"]}
        miss_i = [s["value"] for s in seeds["ingredient_material"] if s["value"] not in ing]
        if miss_s or miss_i:
            bad.append(f"승인 씨앗 빠짐 site {miss_s} · ingredient {miss_i}")
        occ_units = sorted(k[1] for k in units if k[0] == "폐색")
        self.res("V3.3-C", "R2 사전 값(혈관 폐색 → 폐색+혈관) · 폐색≠색전 · 부위 동맥·정맥·안동맥 · 승인 씨앗 21", not bad,
                 f"폐색 단위 부위 {occ_units} · 옛 표면형 {old} · 공유 동의어 {len(shared)} · 부위 사전 {len(site)} · 성분 {len(ing)} · 어긋남 {len(bad)}" + (f" · {bad[:3]}" if bad else ""))

    def y4(self):
        """V3.3-D 접미사 쌍 20 — 결정 6-A(fold_approve 19 · canonical_rename 1) 전부 applied · 접미 꼴 이름의 노드 0 · 쌍마다 ⑦ resolved 또는 쌍 자체 없음 · 대표 이름이 사전/노드에 있음."""
        pairs = self.erd["tuple_rules"]["phrase_kinds"]["suffix_pairs_v33"]
        log6 = [x for x in self.manifest["decisions"]["apply_log"] if x["id"].startswith("DEC-2026-11-06-B6A")]
        bad = []
        if len(log6) != 48 or any(x["result"] != "applied" for x in log6):
            bad.append(f"6-A {len(log6)} · applied {sum(1 for x in log6 if x['result'] == 'applied')}")
        D = {d["name"]: d for d in self.outdic["dictionaries"]}
        ev = D["adverse_event_type"]["entries"]
        surf = {norm(v): e for e in ev for v in [e["canonical"]] + [s_["value"] for s_ in e.get("synonyms", [])]}
        nodes = {norm(e["canonical"]) for e in ev if e.get("origin") == "ledger"}
        cs = jl(os.path.join(self.out, "conflicts.jsonl"))
        for p in pairs:
            a, b = norm(p["a"]), norm(p["b"])
            if a in nodes:
                bad.append(f"접미 꼴 노드 남음 {p['a']}")
            if b not in surf and b not in nodes:
                bad.append(f"대표 {p['b']} 없음")
            opens = [c for c in cs if c["kind"] == "duplicate_candidate" and (c.get("pair") or {}).get("node") and {norm(c["pair"]["node"]), norm(c["pair"]["other"])} == {a, b} and c["status"] == "open"]
            if opens:
                bad.append(f"⑦ open {p['a']}↔{p['b']}")
        rn = next((x for x in log6 if x["kind"] == "canonical_rename"), {})
        if rn.get("renamed") != ["자극감", "자극"] or not any(s_["value"] == "자극감" and s_.get("link") == "renamed_from" for s_ in (surf.get(norm("자극")) or {}).get("synonyms", [])):
            bad.append("자극감 → 자극 rename")
        self.res("V3.3-D", "접미사 쌍 20 — 6-A 48 전부 applied · 접미 꼴 노드 0 · ⑦ open 0 · 자극감→자극 rename", not bad,
                 f"6-A {len(log6)} · fold {sum(1 for x in log6 if x['kind'] == 'fold_approve')} · rename {sum(1 for x in log6 if x['kind'] == 'canonical_rename')} · 어긋남 {len(bad)}" + (f" · {bad[:3]}" if bad else ""))

    def y5(self):
        """V3.3-E category 삭제 — out/ 전부(개체·엣지·사전·충돌·게이트·결정 레코드)에서 event_category · 사건 사전 category/category_review 0 · 결정 new_value category 가 사전에 들어간 자리 0."""
        n = 0
        for r in self.ents["adverse_effect"]:
            n += sum(1 for k in r["attrs"] if k in ("event_category", "category"))
        for d in self.outdic["dictionaries"]:
            if d["name"] == "adverse_event_type":
                n += sum(1 for e in d["entries"] for k in e if k in ("category", "category_review"))
        txt = 0
        for root, _, fs in os.walk(self.out):
            for f in fs:
                if f.endswith((".json", ".jsonl", ".md")):
                    with open(os.path.join(root, f), encoding="utf-8") as fh:
                        txt += fh.read().count("event_category")
        self.res("V3.3-E", "category 삭제 — 단위 event_category 0 · 사전 category/category_review 0 · out/ 텍스트 event_category 0", n == 0 and txt == 0, f"단위·사전 자리 {n} · out/ 텍스트 event_category {txt}")

    def y6(self):
        """V3.3-B 문구 — 부작용 문구 자리 전부 항목 하나 · exact/new 는 단위 있음 · sentence(분석기)는 단위 없음·원문 raw_variants 보존 · 문장꼴(b)·애매 수 = 게이트 6 자리 수."""
        E = self.dic_of("phrase_dictionary")["entries"]
        bad = [e["id"] for e in E if e["status"] in ("exact", "new") and not e["units"]]
        bad += [e["id"] for e in E if e["status"] in ("sentence", "note") and (e["units"] or not e["raw_variants"])]
        an_s = Counter((e.get("why") or {}).get("analyzer") for e in E if e["status"] == "sentence")
        g6 = load_json(os.path.join(self.out, "gate", "batch6.json"))
        by = {it["id"]: len(it.get("subitems") or [it]) for it in g6}
        amb_phr = sum(1 for it in g6 if it["id"] == "ambiguous" for s in it["subitems"] if s["id"].startswith("ambiguous/PHR"))
        if by.get("sentence-b", 0) != an_s.get("sentence_b", 0) or amb_phr != an_s.get("ambiguous", 0):
            bad.append(f"게이트 자리 ≠ 문구(sentence-b {by.get('sentence-b')} vs {an_s.get('sentence_b', 0)} · 애매 {amb_phr} vs {an_s.get('ambiguous', 0)})")
        self.res("V3.3-B2", "문구 — exact/new 단위 있음 · sentence/note 단위 없음·원문 보존 · 문장꼴(b)·애매 = 게이트 6 자리", not bad,
                 f"항목 {len(E)} · sentence 까닭 {dict(an_s)} · 게이트 sentence-b {by.get('sentence-b')} · 애매 문구 {amb_phr} · 어긋남 {len(bad)}" + (f" · {bad[:3]}" if bad else ""))



def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "out"))
    ap.add_argument("--bronze", default=os.path.join(ERD_DIR, "bronze", "phub-ledger"))  # 원장의 집(2판~) · 1판 = /Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26
    ap.add_argument("--step1", default=os.path.join(ERD_DIR, "step1-products.json"))
    ap.add_argument("--erd", default=os.path.join(ERD_DIR, "erd-v3.3.json"))
    ap.add_argument("--dict", default=os.path.join(ERD_DIR, "erd-v3.3-dictionaries.json"))
    ap.add_argument("--colmap", default=os.path.join(ERD_DIR, "erd-v3.3-column-map.md"))
    ap.add_argument("--tuples", default=os.path.join(ERD_DIR, "erd-v3.3-tuples.json"))
    ap.add_argument("--tuples-prev", default=os.path.join(ERD_DIR, "erd-v3.2-tuples.json"))
    ap.add_argument("--kiwi-cache", default=os.path.join(HERE, "cache", "kiwi-cache.json"))
    ap.add_argument("--kiwi-python", default=os.path.join(HERE, ".venv-kiwi", "bin", "python"))
    ap.add_argument("--decisions", default=os.path.join(HERE, "decisions"))
    ap.add_argument("--tmp", default=os.environ.get("SILVER_TEST_TMP", "/private/tmp/claude-501/-Users-kknaks-orca-workspaces-kknaks-profile-----------/f4798840-05cc-4695-94d0-decfad37f126/scratchpad"))
    ap.add_argument("--skip-rebuild", action="store_true")
    a = ap.parse_args()
    C = Checker(a)
    for f in (C.c1, C.c2, C.c3, C.c4, C.c5, C.c6, C.c7, C.c8, C.c9, C.v1, C.v2, C.v3, C.v4, C.v5, C.v6, C.v7, C.v8, C.v9, C.v10,
              C.w1, C.w2, C.w3, C.w4, C.w5, C.w6, C.w7, C.w8, C.w9, C.w10):
        f()
    if C.is32:
        for f in (C.x0, C.x1, C.x2, C.x3, C.x4, C.x5, C.x6, C.x7):
            f()
    if C.is33:
        for f in (C.y1, C.y2, C.y3, C.y4, C.y5, C.y6):
            f()
    ok = all(r[2] is not False for r in C.results)
    for no, name, r, d in C.results:
        print(f"{no} {'PASS' if r else ('SKIP' if r is None else 'FAIL')} {name} — {d}")
    print(f"검산 {'PASS' if ok else 'FAIL'} {sum(1 for r in C.results if r[2])}/{len(C.results)}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
