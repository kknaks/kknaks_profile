# -*- coding: utf-8 -*-
"""실버 메모리 모델 — 레코드 · 칸(cell) · 엣지 · provenance.

레코드: {id, type, status, attrs{name: [cell]}, aliases[cell], derived_from[loc], provenance[P]}
칸(cell): {value, prov:[P]} — 원장 잎 값 그대로(⑤ 빈값 규칙 적용) 또는 {value, derived_from:[loc]} — 파생 값(원 locator 를 가리킨다)
P = {file, path, rec} · loc = "file:path@rec" (provenance.loc) · ERD 정의 값은 "<erd 파일>#/<json pointer>"(빌드 입력 · 기본 erd-v3.json) · 결정은 "DEC-…"
엣지: {relation, from{type,id}, to{type,id}, attrs{name: cell}, provenance[P], derived_from[loc]}
"""
import json
import re
from collections import OrderedDict, defaultdict

from .provenance import P, loc
from .util import mkid, norm

EXPLICIT_EMPTY = {("step1-products.json", "items[].6_companies.conflicts")}  # 「명시적으로 없다」 — 빈 목록 유지(ERD 컬럼 표)


def clean(file, path, v):
    """⑤ 빈값: 키 없음·null·빈 배열·빈 객체·빈 문자열 = null. 명시적 빈 목록만 []."""
    if (file, path) in EXPLICIT_EMPTY and v == []:
        return []
    if v is None or v == "" or v == [] or v == {}:
        return None
    return v


class Silver:
    def __init__(self, ctx):
        self.ctx = ctx
        self.E = defaultdict(OrderedDict)
        self.R = defaultdict(list)
        self.conflicts = []
        self.unresolved = []          # gate ⑨ 행
        self.apply_log = []
        self.notes = []               # 해석 보류
        self.excluded = []

    # ------------------------------------------------------------------ 레코드
    def ent(self, etype, eid, derived_from=None):
        r = self.E[etype].get(eid)
        if r is None:
            r = {"id": eid, "type": etype, "status": "active", "attrs": OrderedDict(), "aliases": [], "derived_from": []}
            self.E[etype][eid] = r
        for d in derived_from or []:
            if d not in r["derived_from"]:
                r["derived_from"].append(d)
        return r

    def attr(self, rec, name, value, prov, raw_value=None):
        cell = {"value": value, "prov": [prov]}
        if raw_value is not None and raw_value != value:
            cell["raw"] = raw_value
        rec["attrs"].setdefault(name, []).append(cell)
        return cell

    def dattr(self, rec, name, value, derived_from, replace=True):
        """파생 값 — derived_from 은 원 locator 목록(비면 안 된다)."""
        df = [d for d in dict.fromkeys(derived_from) if d]
        if not df:
            raise ValueError(f"derived_from 없음: {rec['type']}.{name}")
        cell = {"value": value, "derived_from": df}
        if replace:
            rec["attrs"][name] = [cell]
        else:
            rec["attrs"].setdefault(name, []).append(cell)
        return cell

    def alias(self, rec, value, prov):
        if value is None:
            return
        for a in rec["aliases"]:
            if a["value"] == value:
                if prov not in a["prov"]:
                    a["prov"].append(prov)
                return
        rec["aliases"].append({"value": value, "prov": [prov]})

    def dalias(self, rec, value, derived_from):
        """키 이름에서 온 alias(섹션 키 등) — 값이 잎 값이 아니라 경로의 키라 derived_from 으로."""
        for a in rec["aliases"]:
            if a["value"] == value:
                for d in derived_from:
                    if d not in a.setdefault("derived_from", []):
                        a["derived_from"].append(d)
                return
        rec["aliases"].append({"value": value, "derived_from": list(derived_from)})

    def leaf_cell(self, rec, name, file, path, r, v):
        cv = clean(file, path, v)
        return self.attr(rec, name, cv, P(file, path, r), raw_value=(v if cv is None and v is not None else None))

    # ------------------------------------------------------------------ 엣지
    def edge(self, rel, ftype, fid, ttype, tid, prov, attrs=None, derived_from=None, **extra):
        e = OrderedDict([("relation", rel), ("from", {"type": ftype, "id": fid}), ("to", {"type": ttype, "id": tid}), ("attrs", OrderedDict()), ("provenance", []), ("derived_from", [])])
        for p in prov or []:
            if p not in e["provenance"]:
                e["provenance"].append(p)
        for d in derived_from or []:
            if d not in e["derived_from"]:
                e["derived_from"].append(d)
        for k, v in (attrs or {}).items():
            e["attrs"][k] = v
        e.update(extra)
        self.R[rel].append(e)
        return e

    # ------------------------------------------------------------------ 충돌
    def conflict(self, kind, rule_ref, target_type, target_id, field, values, resolution_rule, status, chosen_value=None, extra=None):
        """values: [{value, source_file, source_path, rec, trust_tier}] — stable_key = {kind, locators 정렬}."""
        locs = sorted({f"{v['source_file']}:{v['source_path']}@{v['rec']}" for v in values if v.get("source_file")} | set((extra or {}).get("extra_locators", [])))
        sk = {"kind": kind, "locators": locs}
        if kind == "unregistered_value":
            sk["value"] = (extra or {}).get("fragment")  # ⑧ 은 같은 위치에 조각이 여럿 — 조각 값까지 안정 키(해석 보류 기록)
        if (extra or {}).get("pair") and (extra or {}).get("pair", {}).get("erd_key"):
            sk["pair"] = extra["pair"]["erd_key"]   # v3.2 ⑦ 노드 쌍 — ERD 안정 키 duplicate_candidate|adverse_event_type|가|나(같은 자리 집합의 다른 쌍을 가른다)
        skey = json.dumps(sk, ensure_ascii=False, sort_keys=True)
        idx = self.__dict__.setdefault("_sk", {})
        if skey in idx:
            # 같은 사실(같은 kind · 같은 출처 쌍)은 레코드 하나 — 다른 규칙으로도 잡히면 also 에 덧붙인다
            c0 = idx[skey]
            c0.setdefault("also", []).append({"target_type": target_type, "target_id": target_id, "field": field, "resolution_rule": resolution_rule})
            return c0
        cid = mkid("CFL", f"{target_type}|{target_id}|{field}|{'|'.join(locs)}|{kind}")
        c = OrderedDict([("id", cid), ("kind", kind), ("rule_ref", rule_ref), ("target_type", target_type), ("target_id", target_id), ("field", field),
                         ("stable_key", sk), ("values", values), ("resolution_rule", resolution_rule), ("chosen_value", chosen_value), ("close_verdict", None),
                         ("status", status), ("decision_id", None)])
        for k, v in (extra or {}).items():
            if k != "extra_locators":
                c[k] = v
        self.conflicts.append(c)
        idx[skey] = c
        return c

    def unresolved_ref(self, relation, slot, label, hint, provs, reason, fragments, partial=None, candidates=None, ref_id=None):
        """⑨ unresolved_reference — 끝이 없는 참조. 엣지를 만들지 않고 이 레코드로 남긴다."""
        from .conflicts import V
        vals = [V(self, label, p["file"], p["path"], p["rec"]) for p in provs]
        return self.conflict("unresolved_reference", "⑨", relation, None, f"참조 「{label}」" + (f" @{hint}" if hint else ""), vals,
                             f"§1.3 ⑨ — {reason}", "open",
                             extra={"relation": relation, "slot": slot, "label": label, "hint": hint, "reason": reason, "fragments": list(fragments or []),
                                    "partial": list(partial or []), "candidates": candidates or {}, "ref_id": ref_id})

    def unresolved_code(self, file, root, r, code):
        from .provenance import rec_str
        self.unresolved_ref("modality(소속)", f"{file}:{root}", code, None, [{"file": file, "path": root, "rec": rec_str(r)}], "레코드 키가 taxonomy 계열 코드에 없다", [])

    def note(self, where, text):
        self.notes.append({"where": where, "text": text})


def dref(name, entry, field=None):
    """사전 값의 안정 키 — 인덱스가 아니라 (사전 이름, 정준값). 결정으로 들어온 값이면 decision:<id> + 그 결정의 source_refs locator."""
    decs = [x for x in entry.get("sources", []) if x.get("kind") == "decision"]
    if decs:
        out = []
        for x in decs:
            out.append(f"decision:{x['decision_id']}")
            out += [r["ref"] for r in x.get("source_refs", []) if r.get("kind") == "ledger" and ".json:" in r.get("ref", "")]
        return out
    return [f"dict:{name}|{entry['canonical']}" + (f"|{field}" if field else "")]


def eref(kind, key, field=None):
    """동결 ERD 의 안정 키 — erd:source_files/<파일>[/<필드>] · erd:decisions/<id>."""
    return f"erd:{kind}/{key}" + (f"/{field}" if field else "")


ERD_FILES = {"erd": "erd-v3.json", "dict": "erd-v3-dictionaries.json"}


def set_erd_files(erd_path, dict_path):
    """ERD·사전 JSON pointer locator 의 파일 이름(빌드 입력의 basename)."""
    import os
    ERD_FILES["erd"] = os.path.basename(erd_path)
    ERD_FILES["dict"] = os.path.basename(dict_path)


def ptr(*parts):
    """ERD JSON pointer locator."""
    return ERD_FILES["erd"] + "#/" + "/".join(str(p).replace("~", "~0").replace("/", "~1") for p in parts)


def dptr(*parts):
    return ERD_FILES["dict"] + "#/" + "/".join(str(p).replace("~", "~0").replace("/", "~1") for p in parts)


def compile_sources(erd):
    """ERD entities[].attrs[].sources → {entity: [(file_pat, path_regex, attr)]}."""
    out = defaultdict(list)
    for ent in erd["entities"]:
        for a in ent["attrs"]:
            for s in a["sources"]:
                f, p = s.split(":", 1)
                if p.endswith(".*"):
                    rx = re.escape(p[:-2]) + r"\..+"
                else:
                    rx = re.escape(p)
                if rx.startswith(r"\*\."):
                    rx = r"[^.\[\]]+\." + rx[4:]
                out[ent["key"]].append((f, re.compile("^" + rx + "$"), a["name"]))
    return out
