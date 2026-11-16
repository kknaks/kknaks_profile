"""problem-packages 1차 수집 공통: 원본 경로·해시, 구간 보존 JSON 파서, 구획 정의.

파서는 원문을 코드 포인트 단위로 직접 읽어 각 노드의 파일 구간(JSON 리터럴 구간과
문자열 내용 구간)을 남기고, 객체 키 중복을 감지한다. 원본은 읽기만 한다.
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
SRC_REL = "orchestration/work/phub-recommend/bronze/phub-ledger/problem-packages.json"
SRC = REPO / SRC_REL
OUT_REL = "orchestration/work/phub-ledger-redesign/first-pass/problem-packages"


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def ptr_escape(k):
    return k.replace("~", "~0").replace("/", "~1")


class Node:
    __slots__ = ("pointer", "parent", "key", "index", "type", "value", "lit_cp", "content_cp",
                 "children", "order", "key_cp", "raw_literal", "has_escape")

    def __init__(self):
        self.children = []
        self.key = None
        self.index = None
        self.key_cp = None
        self.content_cp = None
        self.has_escape = False


class SpanParser:
    """RFC 8259 JSON 을 코드 포인트 위치와 함께 파싱. 중복 키는 dup_keys 에 기록."""

    WS = " \t\n\r"

    def __init__(self, text):
        self.t = text
        self.i = 0
        self.nodes = []
        self.dup_keys = []

    def ws(self):
        while self.i < len(self.t) and self.t[self.i] in self.WS:
            self.i += 1

    def parse(self):
        self.ws()
        root = self.value("", None)
        self.ws()
        if self.i != len(self.t):
            raise ValueError(f"trailing data at cp {self.i}")
        return root

    def string(self):
        assert self.t[self.i] == '"'
        start = self.i
        self.i += 1
        out = []
        esc = False
        while True:
            c = self.t[self.i]
            if c == '"':
                self.i += 1
                break
            if c == "\\":
                esc = True
                n = self.t[self.i + 1]
                if n == "u":
                    out.append(chr(int(self.t[self.i + 2:self.i + 6], 16)))
                    self.i += 6
                else:
                    out.append({'"': '"', "\\": "\\", "/": "/", "b": "\b", "f": "\f",
                                "n": "\n", "r": "\r", "t": "\t"}[n])
                    self.i += 2
                continue
            out.append(c)
            self.i += 1
        return "".join(out), (start, self.i), esc

    def value(self, pointer, parent):
        n = Node()
        n.pointer = pointer
        n.parent = parent
        n.order = len(self.nodes)
        self.nodes.append(n)
        self.ws()
        start = self.i
        c = self.t[self.i]
        if c == "{":
            n.type = "object"
            self.i += 1
            self.ws()
            seen = {}
            if self.t[self.i] == "}":
                self.i += 1
            else:
                while True:
                    self.ws()
                    k, kspan, _ = self.string()
                    self.ws()
                    assert self.t[self.i] == ":"
                    self.i += 1
                    if k in seen:
                        self.dup_keys.append({"object_pointer": pointer, "key": k, "key_cp_span": list(kspan)})
                    seen[k] = True
                    child = self.value(pointer + "/" + ptr_escape(k), n)
                    child.key = k
                    child.key_cp = kspan
                    n.children.append(child)
                    self.ws()
                    if self.t[self.i] == ",":
                        self.i += 1
                        continue
                    assert self.t[self.i] == "}"
                    self.i += 1
                    break
            n.value = None
        elif c == "[":
            n.type = "array"
            self.i += 1
            self.ws()
            if self.t[self.i] == "]":
                self.i += 1
            else:
                idx = 0
                while True:
                    child = self.value(pointer + "/" + str(idx), n)
                    child.index = idx
                    n.children.append(child)
                    idx += 1
                    self.ws()
                    if self.t[self.i] == ",":
                        self.i += 1
                        continue
                    assert self.t[self.i] == "]"
                    self.i += 1
                    break
            n.value = None
        elif c == '"':
            s, span, esc = self.string()
            n.type = "string"
            n.value = s
            n.has_escape = esc
            n.content_cp = (span[0] + 1, span[1] - 1)
        else:
            j = self.i
            while j < len(self.t) and self.t[j] not in ",]} \t\n\r":
                j += 1
            lit = self.t[self.i:j]
            self.i = j
            if lit == "true" or lit == "false":
                n.type, n.value = "boolean", lit == "true"
            elif lit == "null":
                n.type, n.value = "null", None
            else:
                v = json.loads(lit)
                n.type = "integer" if isinstance(v, int) else "number"
                n.value = v
        n.lit_cp = (start, self.i)
        n.raw_literal = self.t[start:self.i]
        return n


def load():
    raw = SRC.read_bytes()
    text = raw.decode("utf-8")
    p = SpanParser(text)
    root = p.parse()
    return raw, text, root, p.nodes, p.dup_keys


def cp_to_byte_factory(text):
    """코드 포인트 인덱스 → UTF-8 바이트 오프셋."""
    acc = [0]
    for ch in text:
        acc.append(acc[-1] + len(ch.encode("utf-8")))
    return lambda cp: acc[cp]


def column_name(n):
    """원본 컬럼명: 객체 멤버는 키 그대로, 배열 원소는 '(<부모키> 원소)'."""
    if n.key is not None:
        return n.key
    if n.index is not None:
        pk = n.parent.key if n.parent is not None and n.parent.key is not None else "root"
        return f"({pk} 원소)"
    return "(루트)"


def pattern_of(pointer):
    parts = pointer.split("/")[1:]
    return "/" + "/".join("*" if p.isdigit() else p for p in parts) if parts else ""


def section_of(pointer):
    """S00 = 루트·메타·/problems 컨테이너, S01..S14 = /problems/0..13 전체."""
    parts = pointer.split("/")[1:]
    if len(parts) >= 2 and parts[0] == "problems" and parts[1].isdigit():
        return f"S{int(parts[1]) + 1:02d}"
    return "S00"
