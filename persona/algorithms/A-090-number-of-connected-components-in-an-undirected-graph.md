---
created: '2026-08-18'
date: '2026-08-18'
day: Day 90
difficulty: medium
id: A-090
source:
  curated_in:
  - neetcode150
  number: 323
  platform: leetcode
  slug: number-of-connected-components-in-an-undirected-graph
  url: https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/
status: draft
tags:
- depth-first-search
- breadth-first-search
- union-find
- graph
title:
  en: Number of Connected Components in an Undirected Graph
  ko: 무방향 그래프의 연결 요소 개수
today: true
type: algorithm
updated: '2026-08-18'
visible: true
---

# 무방향 그래프의 연결 요소 개수

## Data

```yaml
problem:
  title:
    ko: 무방향 그래프의 연결 요소 개수
    en: Number of Connected Components in an Undirected Graph
  statement:
    ko: 'n개의 노드를 가진 무방향 그래프가 주어집니다. 노드는 0부터 n-1까지 번호가 매겨져 있습니다. 간선 리스트가 주어질 때, 그래프의 연결 요소(connected component)의 개수를 반환하세요.


      연결 요소란 두 노드 간의 경로가 존재하는 노드들의 부분집합입니다. 간선이 없는 고립된 노드도 자신만의 연결 요소를 이룹니다.'
    en: 'Given n nodes labeled from 0 to n-1 and a list of undirected edges (each edge is a pair of nodes), return the number of connected components in this graph.


      A connected component is a subset of nodes in which there is a path between every two nodes. Isolated nodes (nodes with no edges) each form their own connected component.'
  constraints:
  - 1 ≤ n ≤ 2000
  - 0 ≤ edges.length ≤ n * (n - 1) / 2
  - 0 ≤ a, b < n
  - a ≠ b (no self-loops)
  io:
  - input: '5

      [[0,1],[1,2],[3,4]]'
    output: '2'
  - input: '5

      [[0,1],[1,2],[2,3],[3,4]]'
    output: '1'
clarifying:
  items:
  - q:
      ko: 간선이 없을 수도 있나요?
      en: Can the edge list be empty?
    type: good
    why:
      ko: 간선이 없으면 각 노드가 독립적인 연결 요소가 되어 답은 n이 됩니다.
      en: If there are no edges, each node is its own component, so the answer would be n.
  - q:
      ko: 같은 간선이 여러 번 나타날 수 있나요?
      en: Can the same edge appear multiple times?
    type: good
    why:
      ko: Union-Find는 이미 연결된 노드를 다시 union해도 결과가 변하지 않습니다.
      en: Union-Find handles duplicates correctly—unioning already-connected nodes doesn't affect the result.
  - q:
      ko: 간선의 순서가 최종 답에 영향을 미치나요?
      en: Does the order of edges affect the answer?
    type: good
    why:
      ko: 순서는 중요하지 않습니다. 최종 연결 구조만이 결과를 결정합니다.
      en: Order doesn't matter; only the final connectivity structure determines the answer.
  - q:
      ko: 연결된 노드들의 실제 리스트를 반환해야 하나요?
      en: Should we return the actual nodes in each component?
    type: distractor
    why:
      ko: 문제는 연결 요소의 개수만 요구합니다. 각 요소의 내용은 필요 없습니다.
      en: The problem only asks for the count of components, not their contents.
  - q:
      ko: 무방향 간선 [0,1]은 0→1과 1→0을 동시에 의미하나요?
      en: Does undirected edge [0,1] mean both directions of connection?
    type: good
    why:
      ko: 네, 무방향이므로 양방향 연결입니다. 따라서 한 번의 union으로 충분합니다.
      en: Yes, undirected means bidirectional. One union operation suffices.
  - q:
      ko: 노드가 자기 자신과 연결된 간선이 있을 수 있나요?
      en: Can a node have a self-loop (edge to itself)?
    type: distractor
    why:
      ko: 제약 조건 a ≠ b가 자기 루프를 명시적으로 금지합니다.
      en: The constraint a ≠ b explicitly prohibits self-loops.
  - q:
      ko: 모든 노드가 한 번은 간선에 나타나야 하나요?
      en: Must every node appear in at least one edge?
    type: good
    why:
      ko: 아니요, 어떤 노드는 간선 리스트에 나타나지 않을 수 있습니다. 그런 노드들은 각각 자신만의 연결 요소입니다.
      en: No, some nodes may not appear in any edge. They form their own single-node components.
approach:
  items:
  - name:
      ko: Union-Find (Disjoint Set Union)
      en: Union-Find (Disjoint Set Union)
    complexity: O(n + m·α(n)) time / O(n) space
    type: good
    why:
      ko: 각 간선을 한 번씩 처리하여 노드들을 연결합니다. 경로 압축을 사용하면 거의 O(1) 시간에 작동합니다. 마지막에 고유한 부모의 개수를 세면 답입니다.
      en: Process each edge once with union operations. Path compression makes operations nearly O(1). Count unique roots at the end.
  - name:
      ko: DFS (깊이 우선 탐색)
      en: DFS (Depth-First Search)
    complexity: O(n + m) time / O(n) space
    type: good
    why:
      ko: 인접 리스트를 먼저 구성한 후, 방문하지 않은 각 노드에서 DFS를 시작합니다. 각 DFS 호출이 하나의 연결 요소를 찾습니다.
      en: Build adjacency list, then start DFS from each unvisited node. Each DFS finds one component.
  - name:
      ko: BFS (너비 우선 탐색)
      en: BFS (Breadth-First Search)
    complexity: O(n + m) time / O(n) space
    type: good
    why:
      ko: DFS와 동일한 아이디어를 BFS로 구현합니다. 각 미방문 노드에서 BFS를 시작하면 연결 요소의 개수를 셀 수 있습니다.
      en: Same idea as DFS but using BFS. Start from each unvisited node and count the number of BFS traversals.
  - name:
      ko: 브루트 포스 (모든 쌍 확인)
      en: Brute Force (Check All Pairs)
    complexity: O(n²) time / O(n²) space
    type: distractor
    why:
      ko: 모든 노드 쌍에 대해 연결 여부를 확인하면 비효율적이고, n이 클 때 실행 불가능합니다.
      en: Checking all pairs doesn't scale well and is inefficient for large n.
  - name:
      ko: 위상 정렬 (Topological Sort)
      en: Topological Sort
    complexity: O(n + m) time / O(n) space
    type: distractor
    why:
      ko: 위상 정렬은 방향 그래프의 순서를 정하기 위해 설계되었습니다. 무방향 그래프 문제에는 과도하게 복잡합니다.
      en: Topological sort is designed for directed graphs and is unnecessarily complex here.
logic:
  format: slot
  slots:
  - label:
      ko: Union-Find 구조 생성
      en: Create Union-Find Structure
    indent: 0
    options:
    - code: dsu = UnionFind()
      type: good
      why:
        ko: 각 노드의 부모 정보를 저장하기 위한 데이터 구조를 초기화합니다.
        en: Initialize a data structure to store parent relationships between nodes.
    - code: parent = list(range(n))
      type: distractor
      why:
        ko: 배열 기반 접근도 가능하지만, 솔루션은 클래스를 사용합니다.
        en: Array-based approach works but the solution uses a class with methods.
    - code: dsu = {}
      type: distractor
      why:
        ko: 빈 딕셔너리는 union()과 findParent() 메서드가 없어서 작동하지 않습니다.
        en: A plain dict lacks union() and findParent() methods needed for the algorithm.
  - label:
      ko: 모든 간선 순회
      en: Iterate Through All Edges
    indent: 0
    options:
    - code: 'for a, b in edges:'
      type: good
      why:
        ko: 주어진 모든 간선에 대해 루프를 돌며, 각 간선이 연결하는 두 노드를 처리합니다.
        en: Loop through each edge to process the nodes it connects.
    - code: 'for a in edges:'
      type: distractor
      why:
        ko: 각 간선은 [a, b] 형태이므로, 두 값 모두를 언팩해야 합니다.
        en: Edges are [a, b] pairs; you need to unpack both values with a, b.
    - code: 'for i in range(len(edges)):'
      type: distractor
      why:
        ko: 인덱스로 접근하는 것보다 직접 값을 언팩하는 것이 더 깔끔합니다.
        en: Direct unpacking is cleaner and more Pythonic than indexing.
  - label:
      ko: 두 노드 연결
      en: Union Two Nodes
    indent: 1
    options:
    - code: dsu.union(a, b)
      type: good
      why:
        ko: 간선의 두 노드를 같은 연결 요소에 속하도록 합칩니다.
        en: Merge the two nodes into the same connected component.
    - code: dsu.union(a, a)
      type: distractor
      why:
        ko: 같은 노드를 스스로와 연결하면 아무 의미 없는 작업입니다.
        en: Unioning a node with itself does nothing and is pointless.
    - code: dsu.f[a] = b
      type: distractor
      why:
        ko: 직접 할당하면 경로 압축(path compression) 같은 최적화를 누락합니다.
        en: Direct assignment skips optimizations like path compression.
  - label:
      ko: 고유한 부모 개수 세기
      en: Count Unique Root Parents
    indent: 0
    options:
    - code: return len(set(dsu.findParent(x) for x in range(n)))
      type: good
      why:
        ko: 모든 노드의 최종 부모를 찾습니다. 고유한 부모의 개수가 곧 연결 요소의 개수입니다.
        en: Find the root parent of each node. Each unique root represents one connected component.
    - code: return len(dsu.f)
      type: distractor
      why:
        ko: dsu.f에는 모든 부모 매핑이 있지만, 같은 부모를 여러 노드가 가질 수 있습니다. 고유한 것만 세어야 합니다.
        en: dsu.f contains all parent mappings but includes duplicates; only count unique parents.
    - code: return len([dsu.findParent(x) for x in range(n)])
      type: distractor
      why:
        ko: 리스트에는 중복된 부모가 있습니다. 고유한 값만 세기 위해 set()으로 변환해야 합니다.
        en: Lists can contain duplicate parent IDs; convert to a set first.
trace:
  code:
  - 'class UnionFind:'
  - '    def __init__(self):'
  - '        self.f = {}'
  - ''
  - '    def findParent(self, x):'
  - '        y = self.f.get(x, x)'
  - '        if x != y:'
  - '            y = self.f[x] = self.findParent(y)'
  - '        return y'
  - ''
  - '    def union(self, x, y):'
  - '        self.f[self.findParent(x)] = self.findParent(y)'
  - ''
  - ''
  - 'class Solution:'
  - '    def countComponents(self, n: int, edges: List[List[int]]) -> int:'
  - '        dsu = UnionFind()'
  - '        for a, b in edges:'
  - '            dsu.union(a, b)'
  - '        return len(set(dsu.findParent(x) for x in range(n)))'
  cases:
  - input: '5

      [[0,1],[1,2],[3,4]]'
    expected: '2'
  - input: '5

      [[0,1],[1,2],[2,3],[3,4]]'
    expected: '1'
  worked_example:
    input: '5

      [[0,1],[1,2],[3,4]]'
    steps:
    - ko: '초기 상태: DSU 생성, 각 노드는 자신을 부모로 설정'
      en: 'Initialize: Create DSU where each node''s parent is itself.'
    - ko: '간선 [0,1] 처리: union(0,1) → 노드 0과 1이 같은 집합에 속함'
      en: 'Process [0,1]: union(0,1) → nodes 0 and 1 now belong to the same component.'
    - ko: '간선 [1,2] 처리: union(1,2) → 노드 0, 1, 2가 모두 같은 집합에 속함'
      en: 'Process [1,2]: union(1,2) → nodes 0, 1, and 2 are now in one component.'
    - ko: '간선 [3,4] 처리: union(3,4) → 노드 3과 4가 같은 집합에 속함'
      en: 'Process [3,4]: union(3,4) → nodes 3 and 4 form another component.'
    - ko: '최종 계산: 모든 노드 0~4의 부모를 찾으면, 고유한 부모는 2개 (한 개는 {0,1,2}의 부모, 다른 하나는 {3,4}의 부모)'
      en: 'Final count: Finding parents of all 5 nodes yields 2 unique roots—one for {0,1,2} and one for {3,4}.'
    answer: '2'
solution:
  code: "class UnionFind:\n    def __init__(self):\n        self.f = {}\n\n    def findParent(self, x):\n        y = self.f.get(x, x)\n        if x != y:\n            y = self.f[x] = self.findParent(y)\n        return y\n\n    def union(self, x, y):\n        self.f[self.findParent(x)] = self.findParent(y)\n\n\nclass Solution:\n    def countComponents(self, n: int, edges: List[List[int]]) -> int:\n        dsu = UnionFind()\n        for a, b in edges:\n            dsu.union(a, b)\n        return len(set(dsu.findParent(x) for x in range(n)))\n"
  complexity:
    time: O(n + m·α(n))
    space: O(n)
  followup:
  - ko: DFS나 BFS를 사용하여 이 문제를 풀 수 있을까요? 시간 복잡도는 어떻게 됩니까?
    en: Can you solve this using DFS or BFS? What would be the time complexity?
  - ko: Union-Find에서 union by rank나 union by size를 사용하면 성능이 개선되나요?
    en: How would union by rank or union by size improve the Union-Find performance?
  - ko: 만약 간선이 동적으로 추가된다면, 연결 요소 개수를 어떻게 효율적으로 유지할 수 있을까요?
    en: If edges are added dynamically, how would you efficiently maintain the component count?
```