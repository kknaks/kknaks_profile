---
created: '2026-08-16'
date: '2026-08-16'
day: Day 89
difficulty: medium
id: A-089
source:
  curated_in:
  - neetcode150
  number: 684
  platform: leetcode
  slug: redundant-connection
  url: https://leetcode.com/problems/redundant-connection/
status: draft
tags:
- depth-first-search
- breadth-first-search
- union-find
- graph
title:
  en: Redundant Connection
  ko: 중복된 연결
today: false
type: algorithm
updated: '2026-08-16'
visible: true
---

# 중복된 연결

## Data

```yaml
problem:
  title:
    ko: 중복된 연결
    en: Redundant Connection
  statement:
    ko: '트리는 연결된 무방향 그래프이며 사이클이 없습니다.


      n개의 노드가 1부터 n까지 라벨을 가진 트리에서 시작하여 하나의 간선이 추가되었습니다. 추가된 간선은 1부터 n 사이의 서로 다른 두 정점을 선택했으며, 기존에 없던 간선입니다. 그래프는 edges 배열로 표현되며, edges[i] = [ai, bi]는 그래프의 노드 ai와 bi 사이에 간선이 있음을 나타냅니다.


      n개의 노드로 이루어진 트리가 되도록 제거할 수 있는 간선 하나를 반환하세요. 여러 답이 있다면, 입력에서 마지막에 나타나는 간선을 반환하세요.'
    en: 'In this problem, a tree is an undirected graph that is connected and has no cycles.


      You are given a graph that started as a tree with n nodes labeled from 1 to n, with one additional edge added. The added edge has two different vertices chosen from 1 to n, and was not an edge that already existed. The graph is represented as an array edges of length n where edges[i] = [ai, bi] indicates that there is an edge between nodes ai and bi in the graph.


      Return an edge that can be removed so that the resulting graph is a tree of n nodes. If there are multiple answers, return the answer that occurs last in the input.'
  constraints:
  - n == edges.length
  - 3 ≤ n ≤ 1000
  - No repeated edges
  - The graph is connected
  io:
  - input: '[[1,2],[1,3],[2,3]]'
    output: '[2,3]'
  - input: '[[1,2],[2,3],[3,4],[1,4],[1,5]]'
    output: '[1,4]'
clarifying:
  items:
  - q:
      ko: 문제에서 "중복된"이란 무엇을 의미하나요?
      en: What does "redundant" mean in this problem?
    type: good
    why:
      ko: 트리에 간선을 하나 추가하면 정확히 하나의 사이클이 생기고, 그 사이클을 끊는 간선이 중복된 간선입니다.
      en: Adding one edge to a tree creates exactly one cycle, and the edge creating that cycle is redundant.
  - q:
      ko: '"입력에서 마지막"이라는 말은 정확히 무엇을 의미하나요?'
      en: What does "occurs last in the input" mean exactly?
    type: good
    why:
      ko: 여러 개의 간선이 사이클을 형성할 수 있을 때, edges 배열에서 가장 뒤에 있는 간선을 반환해야 합니다.
      en: When multiple edges could form a cycle, return the edge that appears latest in the edges array.
  - q:
      ko: 그래프는 방향 그래프인가요, 무방향 그래프인가요?
      en: Is the graph directed or undirected?
    type: good
    why:
      ko: 문제에서 명시된 대로 무방향 그래프입니다. [1,2]와 [2,1]은 같은 간선입니다.
      en: The graph is undirected as stated in the problem. [1,2] and [2,1] represent the same edge.
  - q:
      ko: 왜 Union-Find가 이 문제에 적합한가요?
      en: Why is Union-Find suitable for this problem?
    type: good
    why:
      ko: Union-Find는 간선을 처리하면서 동시에 사이클을 감지할 수 있습니다. 두 노드가 이미 같은 집합에 있으면 사이클이 생깁니다.
      en: Union-Find detects cycles as edges are processed. If two nodes are already in the same set, adding an edge creates a cycle.
  - q:
      ko: 경로 압축(Path Compression)은 어떤 역할을 하나요?
      en: What does path compression do?
    type: good
    why:
      ko: find() 호출 시 루트를 찾는 경로의 모든 노드를 루트에 직접 연결하여 다음 호출을 빠르게 만듭니다.
      en: During find(), connect all nodes on the path directly to the root, making subsequent calls faster.
  - q:
      ko: 여러 트리가 형성될 수 있나요?
      en: Can multiple disconnected components exist?
    type: distractor
    why:
      ko: 아니요, 문제 조건에서 그래프가 연결되어 있다고 명시했습니다.
      en: No, the problem guarantees the graph is connected.
  - q:
      ko: 사이클을 형성하는 모든 간선을 반환해야 하나요?
      en: Should we return all edges that form a cycle?
    type: distractor
    why:
      ko: 아니요, 하나의 간선만 반환해야 합니다. 추가된 간선(가장 마지막 것)이 그 대상입니다.
      en: No, return only one edge - the redundant one added to the tree (the last one found).
approach:
  items:
  - name:
      ko: Union-Find (Disjoint Set Union)
      en: Union-Find (Disjoint Set Union)
    complexity: O(n*α(n)) ≈ O(n) time / O(n) space
    type: good
    why:
      ko: 간선을 순서대로 처리하면서 사이클을 감지합니다. 두 노드가 이미 같은 집합에 있으면 그 간선이 중복입니다. 마지막 중복 간선을 자연스럽게 반환합니다.
      en: Process edges sequentially and detect cycles as they form. When two nodes already belong to the same set, the edge is redundant. Returns the last one naturally.
  - name:
      ko: DFS 후 간선 제거
      en: DFS with Edge Removal
    complexity: O(n²) time / O(n) space
    type: good
    why:
      ko: 역순으로 간선을 제거하고 DFS로 연결성을 확인합니다. 마지막부터 확인하므로 "마지막" 조건을 만족합니다.
      en: Remove edges in reverse order and verify connectivity with DFS. Checking from last edge satisfies the requirement.
  - name:
      ko: BFS 후 간선 제거
      en: BFS with Edge Removal
    complexity: O(n²) time / O(n) space
    type: good
    why:
      ko: DFS 대신 BFS를 사용하는 동일한 접근법입니다. 같은 시간 복잡도를 가집니다.
      en: Same principle as DFS but using BFS instead. Same O(n²) complexity with identical logic.
  - name:
      ko: 완전 탐색 (모든 조합 확인)
      en: Brute Force (Check All Combinations)
    complexity: O(n²) time / O(n) space
    type: distractor
    why:
      ko: 각 간선을 제거하고 모두 확인하는 것은 비효율적이며 Union-Find나 DFS보다 나을 게 없습니다.
      en: Checking all edge combinations for validity is inefficient and provides no advantage.
  - name:
      ko: 인접 행렬 (Adjacency Matrix)
      en: Adjacency Matrix
    complexity: O(n²) time / O(n²) space
    type: distractor
    why:
      ko: O(n²) 메모리를 사용하며, n ≤ 1000일 때 공간 낭비이고 필요 이상으로 느립니다.
      en: Uses O(n²) memory which is wasteful for this problem size and adds unnecessary overhead.
logic:
  format: slot
  slots:
  - label:
      ko: 부모 배열 초기화
      en: Initialize parent array
    indent: 0
    options:
    - code: par = [i for i in range(len(edges) + 1)]
      type: good
      why:
        ko: 각 노드가 초기에는 자신을 부모로 가집니다. 이것이 Union-Find의 기초입니다.
        en: Each node initially points to itself. This is the foundation of Union-Find.
    - code: par = [i for i in range(len(edges))]
      type: distractor
      why:
        ko: 노드가 1부터 n까지이므로 배열 크기는 len(edges)+1이어야 합니다.
        en: Nodes are labeled 1 to n, so array size must be len(edges)+1.
    - code: par = list(range(len(edges)))
      type: distractor
      why:
        ko: 인덱스 0은 사용하지 않으므로 배열이 너무 작습니다.
        en: Index 0 is unused; array is too small for 1-indexed nodes.
  - label:
      ko: 계수(Rank) 배열 초기화
      en: Initialize rank array
    indent: 0
    options:
    - code: rank = [1] * (len(edges) + 1)
      type: good
      why:
        ko: 각 집합의 크기를 추적하여 union by rank 최적화를 구현합니다.
        en: Tracks set size to implement union by rank optimization.
    - code: rank = [0] * (len(edges) + 1)
      type: distractor
      why:
        ko: 0으로 초기화하면 rank 비교와 업데이트가 제대로 작동하지 않습니다.
        en: Zero initialization breaks rank comparison and update logic.
    - code: rank = list(range(len(edges) + 1))
      type: distractor
      why:
        ko: Rank는 휴리스틱이지, 노드 인덱스와 상관없어야 합니다.
        en: Rank is a heuristic for balance, not related to node indices.
  - label:
      ko: Find 함수 (경로 압축 포함)
      en: Find function (with path compression)
    indent: 1
    options:
    - code: 'def find(n):'
      type: good
      why:
        ko: 노드의 루트를 찾으면서 경로를 압축하여 이후 조회를 빠르게 합니다.
        en: Find root while compressing the path for faster future lookups.
    - code: "def find(n):\n    if par[n] != n:\n        par[n] = find(par[n])\n    return par[n]"
      type: distractor
      why:
        ko: 재귀 방식도 경로 압축이 되지만, 스택 오버플로우 위험이 있고 반복문이 더 안전합니다.
        en: Recursive version works but risks stack overflow; iterative is safer.
    - code: "def find(n):\n    while par[n] != n:\n        n = par[n]\n    return n"
      type: distractor
      why:
        ko: 경로 압축이 없으면 최악의 경우 O(n) 시간이 걸립니다.
        en: Without path compression, worst case becomes O(n) per find.
  - label:
      ko: Union 함수 (Rank 기반 병합)
      en: Union function (merge by rank)
    indent: 1
    options:
    - code: 'def union(n1, n2):'
      type: good
      why:
        ko: 두 집합을 합치되, 작은 트리를 큰 트리에 붙여 높이를 최소화합니다.
        en: Merge two sets by attaching smaller tree to larger one to minimize height.
    - code: "def union(n1, n2):\n    p1, p2 = find(n1), find(n2)\n    if p1 != p2:\n        par[p1] = p2\n    return p1 != p2"
      type: distractor
      why:
        ko: Rank를 무시하고 항상 p2에 연결하면 편향된 트리가 될 수 있습니다.
        en: Always attaching to p2 ignores rank and can create skewed trees.
    - code: "def union(n1, n2):\n    par[n1] = n2\n    return True"
      type: distractor
      why:
        ko: find를 호출하지 않고 직접 연결하면 경로 압축의 이점을 잃습니다.
        en: Direct connection without find loses path compression benefits.
  - label:
      ko: 사이클 감지 조건
      en: Cycle detection condition
    indent: 2
    options:
    - code: 'if p1 == p2:'
      type: good
      why:
        ko: 두 노드의 루트가 같으면 이미 연결되어 있다는 뜻이고, 이 간선을 추가하면 사이클이 생깁니다.
        en: If both nodes share the same root, they're already connected; adding edge creates cycle.
    - code: 'if n1 == n2:'
      type: distractor
      why:
        ko: n1과 n2는 항상 다릅니다(문제 조건). 루트를 비교해야 합니다.
        en: n1 and n2 are always different (problem constraint). Must compare roots.
    - code: 'if find(n1) != find(n2):'
      type: distractor
      why:
        ko: 조건이 반대입니다. 같은 루트를 가진 경우가 사이클입니다.
        en: Logic is inverted. Same root means cycle exists.
  - label:
      ko: 모든 간선 순회 및 결과 반환
      en: Iterate edges and return redundant one
    indent: 0
    options:
    - code: 'for n1, n2 in edges:'
      type: good
      why:
        ko: 모든 간선을 순서대로 처리하고, 사이클을 만드는 마지막 간선을 반환합니다.
        en: Process edges sequentially and return the last one that creates a cycle.
    - code: 'for i, (n1, n2) in enumerate(edges):'
      type: distractor
      why:
        ko: 인덱스를 추적할 필요가 없습니다. 간단한 반복으로 충분합니다.
        en: Index tracking is unnecessary; simple iteration suffices.
    - code: 'for n1, n2 in reversed(edges):'
      type: distractor
      why:
        ko: 역순으로 처리하면 마지막이 아닌 첫 번째 중복 간선을 찾을 수 있습니다.
        en: Reversed iteration would find first duplicate, not last.
trace:
  code:
  - 'class Solution:'
  - '    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:'
  - '        par = [i for i in range(len(edges) + 1)]'
  - '        rank = [1] * (len(edges) + 1)'
  - ''
  - '        def find(n):'
  - '            p = par[n]'
  - '            while p != par[p]:'
  - '                par[p] = par[par[p]]'
  - '                p = par[p]'
  - '            return p'
  - ''
  - '        # return False if already unioned'
  - '        def union(n1, n2):'
  - '            p1, p2 = find(n1), find(n2)'
  - ''
  - '            if p1 == p2:'
  - '                return False'
  - '            if rank[p1] > rank[p2]:'
  - '                par[p2] = p1'
  - '                rank[p1] += rank[p2]'
  - '            else:'
  - '                par[p1] = p2'
  - '                rank[p2] += rank[p1]'
  - '            return True'
  - ''
  - '        for n1, n2 in edges:'
  - '            if not union(n1, n2):'
  - '                return [n1, n2]'
  cases:
  - input: '[[1,2],[1,3],[2,3]]'
    expected: '[2,3]'
  - input: '[[1,2],[2,3],[3,4],[1,4],[1,5]]'
    expected: '[1,4]'
  worked_example:
    input: '[[1,2],[1,3],[2,3]]'
    steps:
    - ko: '초기화: par=[0,1,2,3], rank=[1,1,1,1]'
      en: 'Initialize: par=[0,1,2,3], rank=[1,1,1,1]'
    - ko: '간선 [1,2]: find(1)=1, find(2)=2 → 다름 → union 성공, par=[0,2,2,3]'
      en: 'Edge [1,2]: find(1)=1, find(2)=2 → different → union succeeds, par=[0,2,2,3]'
    - ko: '간선 [1,3]: find(1)=2, find(3)=3 → 다름 → union 성공, par=[0,2,2,2]'
      en: 'Edge [1,3]: find(1)=2, find(3)=3 → different → union succeeds, par=[0,2,2,2]'
    - ko: '간선 [2,3]: find(2)=2, find(3)=2 → 같음! → 사이클 발견 → [2,3] 반환'
      en: 'Edge [2,3]: find(2)=2, find(3)=2 → same root! → cycle detected → return [2,3]'
    answer: '[2,3]'
solution:
  code: "class Solution:\n    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:\n        par = [i for i in range(len(edges) + 1)]\n        rank = [1] * (len(edges) + 1)\n\n        def find(n):\n            p = par[n]\n            while p != par[p]:\n                par[p] = par[par[p]]\n                p = par[p]\n            return p\n\n        # return False if already unioned\n        def union(n1, n2):\n            p1, p2 = find(n1), find(n2)\n\n            if p1 == p2:\n                return False\n            if rank[p1] > rank[p2]:\n                par[p2] = p1\n                rank[p1] += rank[p2]\n            else:\n                par[p1] = p2\n                rank[p2] += rank[p1]\n            return True\n\n        for n1, n2 in edges:\n            if not union(n1, n2):\n                return [n1, n2]\n"
  complexity:
    time: O(n*α(n)) ≈ O(n)
    space: O(n)
  followup:
  - ko: 경로 압축이 없다면 시간 복잡도는 어떻게 될까요?
    en: What would the time complexity be without path compression?
  - ko: Rank 대신 높이(Height)를 사용할 수 있을까요? 어떤 차이가 있나요?
    en: Could we use height instead of rank? What's the difference?
  - ko: 만약 여러 간선을 제거할 수 있다면 어떻게 해야 할까요?
    en: How would the solution change if we could remove multiple edges?
```