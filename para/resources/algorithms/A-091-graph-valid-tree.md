---
created: '2026-08-19'
date: '2026-08-19'
day: Day 91
difficulty: medium
id: A-091
source:
  curated_in:
  - neetcode150
  number: 261
  platform: leetcode
  slug: graph-valid-tree
  url: https://leetcode.com/problems/graph-valid-tree/
tags:
- depth-first-search
- breadth-first-search
- union-find
- graph
title:
  en: Graph Valid Tree
  ko: 그래프 유효 트리
today: false
type: algorithm
updated: '2026-08-19'
visible: true
---

# 그래프 유효 트리

## Data

```yaml
problem:
  title:
    ko: 그래프 유효 트리
    en: Graph Valid Tree
  statement:
    en: 'You have a graph with n nodes labeled from 0 to n - 1. You are given an array edges where edges[i] = [ai, bi] represents an undirected edge between nodes ai and bi.


      Return true if the edges form a valid tree, or false otherwise.


      A valid tree is an undirected graph in which any two vertices are connected by exactly one path. In other words, any connected graph without simple cycles is a tree.'
    ko: 'n개의 노드가 0부터 n-1까지 레이블이 지정된 그래프가 있습니다. edges 배열이 주어지고, edges[i] = [ai, bi]는 노드 ai와 bi 사이의 무방향 간선을 나타냅니다.


      간선이 유효한 트리를 형성하면 true를 반환하고, 그렇지 않으면 false를 반환합니다.


      유효한 트리는 모든 두 꼭짓점이 정확히 하나의 경로로 연결된 무방향 그래프입니다. 즉, 순환이 없는 모든 연결된 그래프는 트리입니다.'
  constraints:
  - 1 ≤ n ≤ 2000
  - 0 ≤ edges.length ≤ 2000
  - edges[i].length == 2
  - 0 ≤ ai, bi < n
  - ai != bi
  io:
  - input: '5

      [[0,1],[0,2],[0,3],[1,4]]'
    output: 'true'
  - input: '5

      [[0,1],[1,2],[2,3],[1,3],[1,4]]'
    output: 'false'
clarifying:
  items:
  - q:
      ko: 유효한 트리의 필수 조건은 무엇인가요?
      en: What are the necessary and sufficient conditions for a valid tree?
    type: good
    why:
      ko: 트리는 연결되어 있으면서 순환이 없어야 합니다. n개 노드 트리는 정확히 n-1개 간선을 가져야 합니다.
      en: A tree must be connected and acyclic. A tree with n nodes has exactly n-1 edges.
  - q:
      ko: 순환이 없지만 연결되지 않은 그래프는 트리인가요?
      en: Is a disconnected acyclic graph a valid tree?
    type: good
    why:
      ko: 아니요. 유효한 트리는 연결되어 있어야 합니다. 연결되지 않은 비순환 그래프는 숲(forest)입니다.
      en: No. A valid tree must be connected. A disconnected acyclic graph is a forest, not a tree.
  - q:
      ko: DFS에서 부모 노드를 건너뛰는 이유는?
      en: Why do we skip the parent node during DFS?
    type: good
    why:
      ko: 무방향 그래프에서 부모로 돌아가는 것은 순환이 아닙니다. 건너뛰지 않으면 거짓 양성(false cycle)을 감지합니다.
      en: In an undirected graph, returning to the parent is not a cycle. Without skipping, we incorrectly detect a false cycle.
  - q:
      ko: 간선이 정확히 n-1개이면 항상 트리인가요?
      en: If edges.length == n-1, is the graph always a valid tree?
    type: good
    why:
      ko: 아니요. n-1개 간선은 필요 조건이지만 충분하지 않습니다. 그래프가 연결되어 있고 순환이 없어야 합니다.
      en: No. Having n-1 edges is necessary but not sufficient. The graph must be connected and acyclic.
  - q:
      ko: 노드 0부터 DFS를 시작하는 이유는?
      en: Why start DFS from node 0?
    type: good
    why:
      ko: 연결된 그래프라면 어느 노드에서든 시작 가능합니다. 노드 0에서 모든 노드에 도달하면 연결성을 확인할 수 있습니다.
      en: If the graph is connected, we can start from any node. Reaching all nodes from 0 verifies connectivity.
  - q:
      ko: 자기 루프(self-loop)가 있으면 트리가 될 수 있나요?
      en: Can a graph with self-loops be a valid tree?
    type: distractor
    why:
      ko: 문제 제약에서 ai != bi이므로 자기 루프는 불가능합니다.
      en: The constraint ai != bi prevents self-loops in this problem.
  - q:
      ko: Union-Find 방식은 어떻게 순환을 감지하나요?
      en: How does Union-Find detect cycles?
    type: good
    why:
      ko: 두 노드가 이미 같은 집합에 속하면, 그 간선을 추가하면 순환이 생깁니다. Union-Find는 이를 즉시 감지합니다.
      en: If two nodes are already in the same component, adding an edge between them creates a cycle.
  - q:
      ko: n=0일 때는 어떻게 반환해야 하나요?
      en: What should we return when n=0?
    type: good
    why:
      ko: 0개 노드는 빈 트리로 유효하다고 봅니다. 대부분 true를 반환합니다.
      en: An empty graph (0 nodes) is considered a valid tree, so return true.
approach:
  items:
  - name:
      ko: 깊이 우선 탐색(DFS) + 순환 감지
      en: Depth-First Search with Cycle Detection
    complexity: O(n + e) time / O(n) space
    type: good
    why:
      ko: 인접 리스트를 구성하고 DFS로 순환을 감지합니다. 모든 노드 방문 여부로 연결성을 확인합니다.
      en: Build adjacency list and use DFS to detect cycles. Verify connectivity by checking if all nodes were visited.
  - name:
      ko: Union-Find (분리 집합)
      en: Union-Find (Disjoint Set Union)
    complexity: O(e × α(n)) time / O(n) space
    type: good
    why:
      ko: 각 간선마다 두 노드가 이미 연결되어 있는지 확인합니다. 모든 간선 후 1개 컴포넌트가 남으면 트리입니다.
      en: For each edge, check if nodes are already connected. One remaining component after processing all edges means it's a tree.
  - name:
      ko: 너비 우선 탐색(BFS) + 순환 감지
      en: Breadth-First Search with Cycle Detection
    complexity: O(n + e) time / O(n) space
    type: good
    why:
      ko: DFS 대신 BFS를 사용하여 같은 방식으로 동작합니다. 부모 추적으로 거짓 양성을 방지합니다.
      en: Use BFS instead of DFS with the same parent-tracking logic to avoid false cycle detection.
  - name:
      ko: 간선 개수만 확인
      en: Edge Count Only Check
    complexity: O(1) time / O(1) space
    type: distractor
    why:
      ko: 간선이 n-1개인지만 확인하는 것은 불충분합니다. 순환 그래프도 n-1개 간선을 가질 수 있으므로 연결성 확인이 필수입니다.
      en: Checking only edge count is insufficient. Cyclic graphs can also have n-1 edges; connectivity check is essential.
  - name:
      ko: 무차별 대입 경로 탐색
      en: Brute Force All-Paths Search
    complexity: O(2^n) time / O(n) space
    type: distractor
    why:
      ko: 모든 노드 쌍의 경로 개수를 확인하는 지수 시간 알고리즘. 면접에서 권장되지 않습니다.
      en: Exponential-time approach checking path counts for all pairs. Not practical in interviews.
logic:
  format: slot
  slots:
  - label:
      ko: 엣지 케이스 처리
      en: Handle Edge Case
    indent: 0
    options:
    - code: ''
      type: good
      why:
        ko: n이 0이면 빈 트리이므로 true를 반환합니다.
        en: If n is 0, return true (empty graph is a valid tree).
    - code: 'if n == 0: return False'
      type: distractor
      why:
        ko: 빈 그래프는 유효한 트리입니다.
        en: An empty graph is a valid tree.
    - code: 'if len(edges) == 0: return True'
      type: distractor
      why:
        ko: n > 0이면서 간선이 없으면 연결되지 않은 그래프이므로 거짓입니다.
        en: If n > 0 with no edges, the graph is disconnected (false).
  - label:
      ko: 인접 리스트 초기화 및 그래프 구축
      en: Initialize Adjacency List & Build Graph
    indent: 0
    options:
    - code: ''
      type: good
      why:
        ko: 모든 노드에 대해 빈 리스트로 초기화한 후, 각 간선을 양방향으로 추가합니다 (무방향 그래프).
        en: Create an empty list for each node, then add each edge in both directions (undirected).
    - code: adj = [[] for _ in range(n)]; [adj[n1].append(n2) for n1, n2 in edges]
      type: distractor
      why:
        ko: 역방향 간선 (adj[n2].append(n1))을 추가하지 않으면 방향 그래프가 됩니다.
        en: Without adding reverse edges, this creates a directed graph.
    - code: 'adj = {i: [] for i in range(n)}; adj[n1].extend([n2, n1]) for n1, n2 in edges'
      type: distractor
      why:
        ko: n1을 자신에게 추가하면 자기 루프가 생겨 순환을 감지합니다.
        en: Adding n1 to itself creates a self-loop, falsely detecting cycles.
  - label:
      ko: 방문 집합 초기화 및 DFS 함수 정의
      en: Initialize Visited Set & Define DFS
    indent: 0
    options:
    - code: ''
      type: good
      why:
        ko: 방문한 노드를 추적할 집합을 생성하고, 순환 감지를 위한 재귀 함수를 정의합니다 (부모 매개변수 포함).
        en: Create a set to track visited nodes and define a recursive function with a parent parameter for cycle detection.
    - code: 'visit = [False] * n; def dfs(i): ...'
      type: distractor
      why:
        ko: 리스트는 'in' 연산이 O(n)이므로 집합보다 비효율적입니다.
        en: Lists have O(n) membership checks; sets are O(1).
    - code: 'visit = set(); def dfs(i): ...'
      type: distractor
      why:
        ko: 부모 매개변수가 없으면 무방향 간선에서 부모로 돌아갈 때 순환으로 잘못 감지됩니다.
        en: Without parent parameter, returning to parent in undirected graphs falsely detects cycles.
  - label:
      ko: 순환 감지
      en: Detect Cycles
    indent: 1
    options:
    - code: ''
      type: good
      why:
        ko: 노드가 이미 방문되었다면 순환이 존재합니다 (부모를 제외하고). 거짓을 반환합니다.
        en: If a node is already visited (other than parent), a cycle exists. Return false.
    - code: 'if i in visit: return True'
      type: distractor
      why:
        ko: 순환 감지 시 True를 반환하면 논리가 반대가 됩니다.
        en: Returning true reverses the logic.
    - code: 'if i != 0 and i in visit: return False'
      type: distractor
      why:
        ko: 노드 0을 특수하게 처리할 필요가 없습니다. 첫 호출에서만 방문되지 않았습니다.
        en: Node 0 doesn't need special treatment; it's not yet visited at first call.
  - label:
      ko: 현재 노드 방문 표시
      en: Mark Current Node as Visited
    indent: 1
    options:
    - code: ''
      type: good
      why:
        ko: 현재 노드를 방문 집합에 추가합니다. 나중에 같은 노드를 만나면 순환을 감지합니다.
        en: Add current node to visited set to detect cycles if encountered again.
    - code: 'if i not in visit: visit.add(i)'
      type: distractor
      why:
        ko: 앞에서 이미 확인했으므로 조건부 추가는 불필요합니다.
        en: Redundant check; we confirmed above the node isn't visited.
  - label:
      ko: 이웃 노드 탐색 (부모 건너뛰기)
      en: Traverse Neighbors (Skip Parent)
    indent: 1
    options:
    - code: ''
      type: good
      why:
        ko: 각 이웃 노드를 확인합니다. 부모 노드는 건너뛰고 자식 노드만 재귀적으로 탐색합니다.
        en: Check each neighbor. Skip the parent and recursively explore children.
    - code: 'for j in adj[i]: if i != j and not dfs(j, i): return False'
      type: distractor
      why:
        ko: i != j는 자기 루프만 방지합니다. 무방향 그래프에서 부모 추적이 필요합니다.
        en: i != j only prevents self-loops; parent tracking is needed for undirected graphs.
    - code: 'for j in adj[i]: if not dfs(j, i): return False'
      type: distractor
      why:
        ko: 부모를 건너뛰지 않으면 부모로 돌아갈 때 순환으로 거짓 감지합니다.
        en: Without skipping parent, returning to it falsely detects a cycle.
  - label:
      ko: 연결성 및 무순환성 최종 검증
      en: 'Final Validation: Connectivity & No Cycles'
    indent: 0
    options:
    - code: ''
      type: good
      why:
        ko: DFS가 true(순환 없음)를 반환하고, 방문한 노드 수가 n(전체)과 같으면(연결됨) 유효한 트리입니다.
        en: DFS returns true (no cycles) AND all n nodes visited (connected) → valid tree.
    - code: return dfs(0, -1) and len(edges) == n - 1
      type: distractor
      why:
        ko: 간선 개수만 확인하는 것은 불충분합니다. 연결성을 직접 확인해야 합니다.
        en: Edge count alone is insufficient; must verify connectivity.
    - code: return n == len(visit) and dfs(0, -1)
      type: distractor
      why:
        ko: DFS 결과를 먼저 평가하지 않으면 순환이 감지되지 않습니다 (단락 평가).
        en: Evaluating visit count first could skip DFS evaluation (short-circuit issue).
trace:
  code:
  - '# Problem is free on Lintcode'
  - 'class Solution:'
  - '    """'
  - '    @param n: An integer'
  - '    @param edges: a list of undirected edges'
  - '    @return: true if it''s a valid tree, or false'
  - '    """'
  - ''
  - '    def validTree(self, n, edges):'
  - '        if not n:'
  - '            return True'
  - '        adj = {i: [] for i in range(n)}'
  - '        for n1, n2 in edges:'
  - '            adj[n1].append(n2)'
  - '            adj[n2].append(n1)'
  - ''
  - '        visit = set()'
  - ''
  - '        def dfs(i, prev):'
  - '            if i in visit:'
  - '                return False'
  - ''
  - '            visit.add(i)'
  - '            for j in adj[i]:'
  - '                if j == prev:'
  - '                    continue'
  - '                if not dfs(j, i):'
  - '                    return False'
  - '            return True'
  - ''
  - '        return dfs(0, -1) and n == len(visit)'
  - '    '
  - '    '
  - '    '
  - '    # alternative solution via DSU O(ElogV) time complexity and '
  - '    # save some space as we don''t recreate graph\tree into adjacency list prior dfs and loop over the edge list directly'
  - '    class Solution:'
  - '    """'
  - '    @param n: An integer'
  - '    @param edges: a list of undirected edges'
  - '    @return: true if it''s a valid tree, or false'
  - '    """'
  - '    def __find(self, n: int) -> int:'
  - '        while n != self.parents.get(n, n):'
  - '            n = self.parents.get(n, n)'
  - '        return n'
  - ''
  - '    def __connect(self, n: int, m: int) -> None:'
  - '        pn = self.__find(n)'
  - '        pm = self.__find(m)'
  - '        if pn == pm:'
  - '            return'
  - '        if self.heights.get(pn, 1) > self.heights.get(pm, 1):'
  - '            self.parents[pn] = pm'
  - '        else:'
  - '            self.parents[pm] = pn'
  - '            self.heights[pm] = self.heights.get(pn, 1) + 1'
  - '        self.components -= 1'
  - ''
  - '    def valid_tree(self, n: int, edges: List[List[int]]) -> bool:'
  - '        # init here as not sure that ctor will be re-invoked in different tests'
  - '        self.parents = {}'
  - '        self.heights = {}'
  - '        self.components = n'
  - ''
  - '        for e1, e2 in edges:'
  - '            if self.__find(e1) == self.__find(e2):  # ''redundant'' edge'
  - '                return False'
  - '            self.__connect(e1, e2)'
  - ''
  - '        return self.components == 1  # forest contains one tree'
  - ''
  - ''
  cases:
  - input: '5

      [[0,1],[0,2],[0,3],[1,4]]'
    expected: 'true'
  - input: '5

      [[0,1],[1,2],[2,3],[1,3],[1,4]]'
    expected: 'false'
  worked_example:
    input: '5

      [[0,1],[0,2],[0,3],[1,4]]'
    steps:
    - ko: n=5, edges=[[0,1],[0,2],[0,3],[1,4]]로 시작합니다.
      en: Start with n=5 and edges [[0,1],[0,2],[0,3],[1,4]].
    - ko: '인접 리스트 구축: 0→[1,2,3], 1→[0,4], 2→[0], 3→[0], 4→[1]'
      en: 'Build adjacency list: 0→[1,2,3], 1→[0,4], 2→[0], 3→[0], 4→[1]'
    - ko: 'dfs(0, -1): 0을 방문, 이웃 1,2,3 탐색 → 1에서 4 탐색 → 모든 노드 방문, 순환 없음.'
      en: 'dfs(0, -1): visit 0, explore neighbors 1,2,3; from 1 reach 4. All 5 nodes visited, no cycles.'
    - ko: 'DFS 반환값=true, len(visit)=5=n이므로, 최종 반환값: true'
      en: DFS returns true, len(visit)=5=n → return true.
    answer: 'true'
solution:
  code: "# Problem is free on Lintcode\nclass Solution:\n    \"\"\"\n    @param n: An integer\n    @param edges: a list of undirected edges\n    @return: true if it's a valid tree, or false\n    \"\"\"\n\n    def validTree(self, n, edges):\n        if not n:\n            return True\n        adj = {i: [] for i in range(n)}\n        for n1, n2 in edges:\n            adj[n1].append(n2)\n            adj[n2].append(n1)\n\n        visit = set()\n\n        def dfs(i, prev):\n            if i in visit:\n                return False\n\n            visit.add(i)\n            for j in adj[i]:\n                if j == prev:\n                    continue\n                if not dfs(j, i):\n                    return False\n            return True\n\n        return dfs(0, -1) and n == len(visit)\n    \n    \n    \n    # alternative solution via DSU O(ElogV) time complexity and \n    # save some space as we don't recreate graph\\tree into adjacency list prior dfs and loop over the edge list directly\n\
    \    class Solution:\n    \"\"\"\n    @param n: An integer\n    @param edges: a list of undirected edges\n    @return: true if it's a valid tree, or false\n    \"\"\"\n    def __find(self, n: int) -> int:\n        while n != self.parents.get(n, n):\n            n = self.parents.get(n, n)\n        return n\n\n    def __connect(self, n: int, m: int) -> None:\n        pn = self.__find(n)\n        pm = self.__find(m)\n        if pn == pm:\n            return\n        if self.heights.get(pn, 1) > self.heights.get(pm, 1):\n            self.parents[pn] = pm\n        else:\n            self.parents[pm] = pn\n            self.heights[pm] = self.heights.get(pn, 1) + 1\n        self.components -= 1\n\n    def valid_tree(self, n: int, edges: List[List[int]]) -> bool:\n        # init here as not sure that ctor will be re-invoked in different tests\n        self.parents = {}\n        self.heights = {}\n        self.components = n\n\n        for e1, e2 in edges:\n            if self.__find(e1) == self.__find(e2):\
    \  # 'redundant' edge\n                return False\n            self.__connect(e1, e2)\n\n        return self.components == 1  # forest contains one tree\n\n\n"
  complexity:
    time: O(n + e) where n = nodes, e = edges
    space: O(n) for adjacency list and visited set
  followup:
  - ko: Union-Find를 사용하여 풀면 시간 복잡도가 어떻게 달라지나요?
    en: How would time complexity change if you used Union-Find instead?
  - ko: 그래프가 방향 그래프(directed)라면 DFS 로직이 어떻게 달라질까요?
    en: How would the DFS logic change for a directed graph?
  - ko: n이 100만이라면 공간을 더 최적화할 수 있을까요?
    en: Can you optimize space complexity if n were 1 million?
```