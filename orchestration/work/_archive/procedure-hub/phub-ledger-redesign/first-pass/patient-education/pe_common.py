"""patient-education.json 1차 조사 공용 — 위치 추적 JSON 파서·경로 상수.

build.py 가 쓴다. verify.py 는 이 모듈을 import 하지 않는다(독립 재구현).
"""
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *[".."] * 5))
SRC_REL = "orchestration/work/phub-recommend/bronze/phub-ledger/patient-education.json"
SRC = os.path.join(REPO, SRC_REL)


def ptr_escape(k):
    return k.replace("~", "~0").replace("/", "~1")


def read_source():
    raw = open(SRC, "rb").read()
    text = raw.decode("utf-8")
    return raw, text, hashlib.sha256(raw).hexdigest()


class Parser:
    """원문 문자열(코드포인트)을 직접 훑어 모든 노드의 위치를 남긴다.

    node: pointer, parent, key(객체 키 또는 배열 인덱스), type, value(말단), literal_cp(원문 리터럴 [s,e)),
    value_cp(문자열이면 따옴표 안쪽 [s,e)), key_cp(객체 멤버면 키 리터럴 [s,e)), order(문서 순서), child_count
    이스케이프가 있으면 value_cp 안쪽 길이와 디코딩 길이가 달라지므로 has_escape 로 표시한다.
    """

    def __init__(self, text):
        self.t = text
        self.i = 0
        self.nodes = []
        self.duplicates = []

    def ws(self):
        while self.i < len(self.t) and self.t[self.i] in " \t\r\n":
            self.i += 1

    def string(self):
        assert self.t[self.i] == '"'
        s = self.i
        self.i += 1
        esc = False
        while True:
            c = self.t[self.i]
            if c == "\\":
                esc = True
                self.i += 2
                continue
            if c == '"':
                break
            self.i += 1
        self.i += 1
        lit = self.t[s:self.i]
        return json.loads(lit), (s, self.i), esc

    def value(self, pointer, parent, key, key_cp=None):
        self.ws()
        c = self.t[self.i]
        node = {"pointer": pointer, "parent": parent, "key": key, "key_cp": key_cp, "order": len(self.nodes)}
        self.nodes.append(node)
        start = self.i
        if c == "{":
            node["type"] = "object"
            self.i += 1
            seen = set()
            n = 0
            self.ws()
            if self.t[self.i] == "}":
                self.i += 1
            else:
                while True:
                    self.ws()
                    k, kcp, _ = self.string()
                    if k in seen:
                        self.duplicates.append({"pointer": pointer, "key": k, "key_cp": list(kcp)})
                    seen.add(k)
                    self.ws()
                    assert self.t[self.i] == ":"
                    self.i += 1
                    self.value(pointer + "/" + ptr_escape(k), pointer, k, list(kcp))
                    n += 1
                    self.ws()
                    if self.t[self.i] == ",":
                        self.i += 1
                        continue
                    assert self.t[self.i] == "}"
                    self.i += 1
                    break
            node["child_count"] = n
        elif c == "[":
            node["type"] = "array"
            self.i += 1
            n = 0
            self.ws()
            if self.t[self.i] == "]":
                self.i += 1
            else:
                while True:
                    self.value(pointer + "/" + str(n), pointer, n)
                    n += 1
                    self.ws()
                    if self.t[self.i] == ",":
                        self.i += 1
                        continue
                    assert self.t[self.i] == "]"
                    self.i += 1
                    break
            node["child_count"] = n
        elif c == '"':
            v, cp, esc = self.string()
            node["type"] = "string"
            node["value"] = v
            node["value_cp"] = [cp[0] + 1, cp[1] - 1]
            node["has_escape"] = esc
        else:
            j = self.i
            while j < len(self.t) and self.t[j] not in ",]} \t\r\n":
                j += 1
            lit = self.t[self.i:j]
            v = json.loads(lit)
            node["type"] = "null" if v is None else "boolean" if isinstance(v, bool) else "number"
            node["value"] = v
            self.i = j
        node["literal_cp"] = [start, self.i]
        return node

    def parse(self):
        self.value("", None, None)
        self.ws()
        assert self.i == len(self.t)
        return self.nodes


def cp_to_byte(text):
    """코드포인트 인덱스 → UTF-8 바이트 오프셋 표 (len+1)."""
    out = [0]
    b = 0
    for ch in text:
        b += len(ch.encode("utf-8"))
        out.append(b)
    return out


def segment_of(pointer):
    """구획 소유 규칙. S00=상위 메타(/ · /version · /updated · /categories 컨테이너), S01~S17=/categories/0~16 하위."""
    parts = pointer.split("/")
    if len(parts) >= 3 and parts[1] == "categories":
        return "S%02d" % (int(parts[2]) + 1)
    return "S00"
