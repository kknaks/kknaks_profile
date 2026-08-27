---
created: '2026-08-08'
date: '2026-08-08'
day: Day 81
difficulty: medium
id: A-081
source:
  curated_in:
  - neetcode150
  number: 133
  platform: leetcode
  slug: clone-graph
  url: https://leetcode.com/problems/clone-graph/
tags:
- hash-table
- depth-first-search
- breadth-first-search
- graph
title:
  en: Clone Graph
  ko: 그래프 복제
today: false
type: algorithm
updated: '2026-08-08'
visible: true
---

# 그래프 복제

## Data

```yaml
problem:
  title:
    ko: 그래프 복제
    en: Clone Graph
  statement:
    ko: "연결된 무방향 그래프의 한 노드에 대한 참조가 주어집니다.\n\n그래프의 깊은 복제(deep copy, clone)를 반환하세요.\n\n그래프의 각 노드는 정수 값(int)과 이웃 노드들의 리스트(List[Node])를 포함합니다.\n\nclass Node {\n    public int val;\n    public List<Node> neighbors;\n}\n\n테스트 케이스 형식:\n편의상 각 노드의 값은 해당 노드의 인덱스(1-indexed)와 같습니다. 예를 들어 첫 번째 노드는 val == 1, 두 번째 노드는 val == 2 등입니다. 그래프는 인접 리스트(adjacency list)를 사용하여 표현됩니다.\n\n인접 리스트는 유한 그래프를 나타내기 위해 사용되는 순서 없는 리스트들의 모음입니다. 각 리스트는 그래프의 한 노드의 이웃들을 설명합니다.\n\n주어진 노드는 항상 val = 1인 첫 번째 노드입니다. 복제된 그래프의 주어진 노드의 복사본을 참조로 반환해야 합니다."
    en: "Given a reference of a node in a connected undirected graph.\n\nReturn a deep copy (clone) of the graph.\n\nEach node in the graph contains a value (int) and a list (List[Node]) of its neighbors.\n\nclass Node {\n    public int val;\n    public List<Node> neighbors;\n}\n\nTest case format:\nFor simplicity, each node's value is the same as the node's index (1-indexed). For example, the first node with val == 1, the second node with val == 2, and so on. The graph is represented in the test case using an adjacency list.\n\nAn adjacency list is a collection of unordered lists used to represent a finite graph. Each list describes the set of neighbors of a node in the graph.\n\nThe given node will always be the first node with val = 1. You must return the copy of the given node as a reference to the cloned graph."
  constraints:
  - The number of nodes in the graph is in the range [0, 100].
  - 1 ≤ Node.val ≤ 100
  - Node.val is unique for each node.
  - There are no repeated edges and no self-loops in the graph.
  io:
  - input: '[[2,4],[1,3],[2,4],[1,3]]'
    output: '[[2,4],[1,3],[2,4],[1,3]]'
  - input: '[[]]'
    output: '[[]]'
  - input: '[]'
    output: '[]'
clarifying:
  items:
  - q:
      ko: 깊은 복제(deep copy)란 정확히 무엇을 의미하나요?
      en: What exactly does 'deep copy' mean in this context?
    type: good
    why:
      ko: 깊은 복제는 모든 노드와 간선을 새로 생성해야 함을 의미합니다. 단순히 참조를 복사하는 것이 아니며, 복제본을 수정해도 원본 그래프에 영향을 미치지 않아야 합니다.
      en: Deep copy means creating entirely new nodes and edges, not just copying references. The original graph must remain unaffected by any modifications to the clone.
  - q:
      ko: 그래프에 사이클이 있으면 어떻게 무한 루프를 방지할 수 있나요?
      en: How do we prevent infinite loops when the graph contains cycles?
    type: good
    why:
      ko: 메모이제이션(memoization)을 사용하여 이미 복제한 노드를 추적해야 합니다. 같은 노드를 다시 방문하려고 할 때는 이미 생성된 복제본을 반환합니다.
      en: We use memoization to track already-cloned nodes. When we encounter a node we've already processed, we return its existing clone instead of reprocessing it.
  - q:
      ko: 새 노드를 생성한 후, 이웃을 처리하기 전에 메모에 등록해야 하나요, 아니면 후에 등록해야 하나요?
      en: Should we register the new node in memo before processing neighbors or after?
    type: good
    why:
      ko: 반드시 이웃을 처리하기 전에 등록해야 합니다. 그래야 사이클로 인해 이웃이 이 노드를 다시 방문할 때 이미 생성된 복제본을 참조할 수 있습니다.
      en: Must register before processing neighbors. This ensures that if a cycle causes a neighbor to reference back to this node, we return the already-created clone instead of creating a duplicate.
  - q:
      ko: 이 문제를 푸는 데 BFS가 DFS보다 낫나요?
      en: Is BFS better than DFS for solving this problem?
    type: distractor
    why:
      ko: 둘 다 같은 시간/공간 복잡도 O(V+E)를 가지며 이 문제를 모두 해결할 수 있습니다. 선택은 개인의 선호도와 구현 스타일에 따릅니다.
      en: Both have identical time and space complexity O(V+E) and both solve this problem correctly. The choice depends on personal preference and implementation style.
  - q:
      ko: 메모 맵 대신 방문한 노드를 추적하는 집합(set)만 사용할 수 있나요?
      en: Can we just use a set to track visited nodes instead of a memo map?
    type: distractor
    why:
      ko: 아니요. 집합은 노드가 방문되었는지만 확인하지만, 복제된 노드 자체를 저장하지 않습니다. 이웃들을 연결할 때 실제 복제 노드가 필요합니다.
      en: No. A set only tracks whether a node was visited, but doesn't store the actual cloned node. We need the cloned nodes themselves to connect neighbors properly.
  - q:
      ko: 입력 노드가 null인 경우는 어떻게 처리하나요?
      en: How should we handle a null input node?
    type: good
    why:
      ko: '조건부 검사(예: `return dfs(node) if node else None`)를 사용하여 null 입력을 처리합니다. 이는 노드가 없는 빈 그래프 케이스를 나타냅니다.'
      en: Use a conditional check (e.g., `return dfs(node) if node else None`) to handle null input, which represents an empty graph with no nodes.
  - q:
      ko: 원본 그래프를 수정하지 않으면서 복제할 수 있나요?
      en: Can we clone the graph without modifying the original?
    type: good
    why:
      ko: 네, 메모이제이션 접근 방식은 원본 그래프를 건드리지 않습니다. 오직 새로운 노드와 간선만 생성되므로 원본은 완전히 독립적으로 유지됩니다.
      en: Yes, the memoization approach doesn't modify the original graph at all. Only new nodes and edges are created, so the original remains completely independent.
approach:
  items:
  - name:
      ko: 깊이 우선 탐색(DFS) + 메모이제이션
      en: Depth-First Search (DFS) with Memoization
    complexity: O(V + E) time / O(V) space
    type: good
    why:
      ko: 각 노드와 간선을 정확히 한 번씩 방문합니다. 메모를 통해 사이클을 효율적으로 처리하고 중복을 방지합니다. 재귀는 직관적이고 구현이 간단합니다.
      en: Visits each node and edge exactly once. Memoization efficiently handles cycles and prevents duplicate work. Recursion is intuitive and straightforward to implement.
  - name:
      ko: 너비 우선 탐색(BFS) + 메모이제이션
      en: Breadth-First Search (BFS) with Memoization
    complexity: O(V + E) time / O(V) space
    type: good
    why:
      ko: DFS와 같은 복잡도를 가지지만 반복적(iterative) 접근을 사용합니다. 큐를 사용하여 노드를 처리하며, 깊은 재귀 호출 스택을 피합니다.
      en: Same complexity as DFS but uses an iterative approach with a queue. Avoids deep recursive call stacks and can be more suitable for very large graphs.
  - name:
      ko: 메모이제이션 없는 순수 재귀
      en: Pure Recursion Without Memoization
    complexity: O(∞) time / O(∞) space
    type: distractor
    why:
      ko: 사이클이 있는 그래프에서 무한 루프에 빠져 런타임 오류나 타임아웃이 발생합니다. 메모이제이션이 필수적입니다.
      en: Will infinite loop on graphs with cycles, causing timeout or stack overflow. Memoization is essential to break cycles and enable proper termination.
  - name:
      ko: 얕은 복제(Shallow Copy)
      en: Shallow Copy
    complexity: O(V) time / O(V) space
    type: distractor
    why:
      ko: 노드 값은 복사하지만 이웃 리스트는 원본을 참조합니다. 깊은 복제 요구사항을 위반하며, 복제본의 이웃을 수정하면 원본에도 영향을 미칩니다.
      en: Copies node values but shares the neighbors list with the original. Violates the deep copy requirement and modifications to the clone affect the original graph.
  - name:
      ko: 두 단계 접근(노드 생성 → 간선 연결)
      en: Two-Pass Approach (Create Nodes First, Link Edges Later)
    complexity: O(V + E) time / O(V) space
    type: distractor
    why:
      ko: 작동하지만 불필요하게 복잡합니다. 먼저 모든 노드를 생성한 후 간선을 연결하면 추가 반복문이 필요하며, 단일 DFS 패스보다 덜 우아합니다.
      en: Works but unnecessarily complex. Creating all nodes first, then linking edges requires an extra pass and is less elegant than the single DFS traversal.
logic:
  format: slot
  slots:
  - label:
      ko: 메모이제이션 맵 초기화
      en: Initialize Memoization Map
    indent: 0
    options:
    - code: oldToNew = {}
      type: good
      why:
        ko: 원본 노드에서 복제된 노드로의 매핑을 저장할 딕셔너리를 생성합니다. 이를 통해 중복 처리를 방지하고 사이클을 감지할 수 있습니다.
        en: Create a dictionary to store mappings from original nodes to their clones. This prevents duplicate processing and enables cycle detection.
    - code: visited = set()
      type: distractor
      why:
        ko: 집합은 방문 여부만 추적하지만 실제 복제 노드를 저장하지 않습니다. 이웃을 연결할 때 복제 노드 자체가 필요합니다.
        en: A set only tracks visited status but doesn't store the cloned nodes. We need the actual cloned nodes to connect neighbors.
    - code: oldToNew = []
      type: distractor
      why:
        ko: 리스트는 연속적인 인덱스가 필요하며, 노드 값이 항상 0부터 시작하지 않습니다. 딕셔너리의 O(1) 조회가 더 효율적입니다.
        en: A list requires consecutive indices, but node values may not start from 0. Dictionary lookup is O(1) and more appropriate here.
  - label:
      ko: 메모에서 확인 (이미 복제됨)
      en: Check Memo (Already Cloned)
    indent: 1
    options:
    - code: 'if node in oldToNew:'
      type: good
      why:
        ko: 노드가 메모에 있으면 이미 생성된 복제본을 즉시 반환합니다. 무한 재귀를 방지하고 중복 작업을 피합니다.
        en: If the node is in memo, return its existing clone immediately. Prevents infinite recursion and avoids redundant work.
    - code: 'if node in visited: continue'
      type: distractor
      why:
        ko: 재귀 함수에서 continue를 사용할 수 없습니다. 대신 복제 노드를 반환해야 합니다.
        en: Cannot use 'continue' in a recursive function. Must return the cloned node to stop reprocessing.
    - code: 'if node.val in oldToNew: return oldToNew[node.val]'
      type: distractor
      why:
        ko: 노드 객체 자체를 키로 사용해야 합니다. node.val을 사용하면 같은 값을 가진 서로 다른 노드들이 충돌합니다.
        en: Must use the node object itself as the key, not node.val. Different node objects with the same value would incorrectly collide.
  - label:
      ko: 새 노드 생성
      en: Create New Node
    indent: 1
    options:
    - code: copy = Node(node.val)
      type: good
      why:
        ko: 원본 노드와 동일한 값을 가진 새로운 Node 객체를 생성합니다. 이웃 리스트는 처음에는 비어있습니다.
        en: Create a new Node object with the same value as the original. The neighbors list is initially empty.
    - code: copy = Node()
      type: distractor
      why:
        ko: 값을 지정하지 않으면 node.val이 복사되지 않습니다. 생성자에 값을 전달해야 합니다.
        en: Without specifying a value, the node's val attribute won't be copied. Must pass node.val to the constructor.
    - code: copy = node
      type: distractor
      why:
        ko: 이것은 같은 객체를 참조하는 얕은 복사입니다. 새로운 Node 객체를 만들어야 깊은 복제입니다.
        en: This is a reference to the same object (shallow copy), not a deep clone. Must create a new Node object.
  - label:
      ko: 메모에 등록 (사이클 처리)
      en: Register in Memo (Handle Cycles)
    indent: 1
    options:
    - code: oldToNew[node] = copy
      type: good
      why:
        ko: 이웃을 재귀 처리하기 *전에* 메모에 매핑을 저장합니다. 이렇게 하면 사이클이 이 노드로 돌아올 때 이미 생성된 복제본을 참조할 수 있습니다.
        en: Store the mapping in memo *before* recursively processing neighbors. This way, if a cycle leads back to this node, we can reference the already-created clone.
    - code: oldToNew[copy] = node
      type: distractor
      why:
        ko: 매핑 방향이 반대입니다. 원본을 키로, 복제본을 값으로 사용해야 합니다.
        en: Reversed mapping direction. Should map original to clone, not clone to original.
    - code: '# Register after processing neighbors loop'
      type: distractor
      why:
        ko: 이웃 처리 후에 등록하면 사이클이 있을 때 무한 재귀에 빠집니다. 반드시 먼저 등록해야 합니다.
        en: If registered after processing neighbors, cycles cause infinite recursion. Must register before to break the cycle.
  - label:
      ko: 이웃 노드 재귀 복제
      en: Recursively Clone Neighbors
    indent: 1
    options:
    - code: 'for nei in node.neighbors:'
      type: good
      why:
        ko: 원본 노드의 각 이웃에 대해 dfs를 재귀적으로 호출하여 복제한 후, 복제 노드의 이웃 리스트에 추가합니다.
        en: For each neighbor of the original node, recursively call dfs to clone it, then add the cloned neighbor to the copy's neighbors list.
    - code: copy.neighbors = [dfs(nei) for nei in node.neighbors]
      type: distractor
      why:
        ko: 리스트 컴프리헨션도 작동하지만, 명시적인 루프와 append가 알고리즘의 의도를 더 명확하게 표현합니다.
        en: While list comprehension works, explicit loop with append more clearly expresses the algorithm's intent in this context.
    - code: copy.neighbors.extend(node.neighbors)
      type: distractor
      why:
        ko: 원본 이웃을 직접 추가하면 깊은 복제가 아닙니다. 이웃들도 재귀적으로 복제해야만 진정한 깊은 복제입니다.
        en: Directly adding original neighbors doesn't create a deep clone. Neighbors must be recursively cloned for a true deep copy.
  - label:
      ko: 복제된 노드 반환
      en: Return Cloned Node
    indent: 1
    options:
    - code: return copy
      type: good
      why:
        ko: 이 함수에서 생성하고 처리한 복제 노드를 반환합니다. 호출자는 이 노드를 자신의 이웃 리스트에 추가합니다.
        en: Return the cloned node that was created and processed in this call. The caller will add this to its own neighbors list.
    - code: return node
      type: distractor
      why:
        ko: 원본 노드를 반환하면 복제가 아닙니다. 복제본을 반환해야 합니다.
        en: Must return the clone, not the original node.
    - code: return copy.neighbors
      type: distractor
      why:
        ko: 이웃 리스트가 아니라 복제된 노드 객체 자체를 반환해야 합니다.
        en: Must return the cloned node object itself, not its neighbors list.
  - label:
      ko: null 입력 처리
      en: Handle Null Input
    indent: 0
    options:
    - code: return dfs(node) if node else None
      type: good
      why:
        ko: 입력 노드가 null일 수 있습니다(빈 그래프). 조건부 표현식으로 이 엣지 케이스를 처리하여 None을 반환합니다.
        en: Input node can be null (empty graph). Use conditional expression to handle this edge case and return None appropriately.
    - code: return dfs(node)
      type: distractor
      why:
        ko: node가 None일 때 오류가 발생합니다. 먼저 None 체크를 해야 합니다.
        en: Will crash if node is None. Must check for None before calling dfs.
    - code: "if node: dfs(node) \nreturn None"
      type: distractor
      why:
        ko: 항상 None을 반환하므로 복제 결과를 잃습니다. node가 있을 때 dfs의 결과를 반환해야 합니다.
        en: Always returns None and loses the cloned node. Must return the result of dfs when node is not None.
trace:
  code:
  - 'class Solution:'
  - '    def cloneGraph(self, node: "Node") -> "Node":'
  - '        oldToNew = {}'
  - ''
  - '        def dfs(node):'
  - '            if node in oldToNew:'
  - '                return oldToNew[node]'
  - ''
  - '            copy = Node(node.val)'
  - '            oldToNew[node] = copy'
  - '            for nei in node.neighbors:'
  - '                copy.neighbors.append(dfs(nei))'
  - '            return copy'
  - ''
  - '        return dfs(node) if node else None'
  cases:
  - input: '[[2,4],[1,3],[2,4],[1,3]]'
    expected: '[[2,4],[1,3],[2,4],[1,3]]'
  - input: '[[]]'
    expected: '[[]]'
  - input: '[]'
    expected: '[]'
  worked_example:
    input: '[[2,4],[1,3],[2,4],[1,3]]'
    steps:
    - ko: 'dfs(node1) 호출: node1은 메모에 없음. copy1 생성, node1 → copy1 등록'
      en: 'Call dfs(node1): node1 not in memo. Create copy1, register node1 → copy1'
    - ko: 'node1의 이웃 [node2, node4] 순회: dfs(node2) 호출. copy2 생성, node2 → copy2 등록. node2의 이웃 [node1, node3]: node1은 이미 메모에서 copy1 반환, node3은 새로 처리'
      en: 'Process node1''s neighbors [node2, node4]: Call dfs(node2). Create copy2, register. Process node2''s neighbors [node1, node3]: node1 already in memo → return copy1, node3 is new → process recursively'
    - ko: 'node3 처리: copy3 생성, node3 → copy3 등록. node3의 이웃 [node2, node4]: node2는 메모에서 copy2 반환, node4는 새로 생성'
      en: 'Process node3: Create copy3, register. node3''s neighbors [node2, node4]: node2 already in memo → copy2, node4 is new → create copy4'
    - ko: 'node4 처리: copy4 생성, node4 → copy4 등록. node4의 이웃 [node1, node3]: 모두 메모에서 반환. 모든 노드와 간선 처리 완료. copy1 반환'
      en: 'Process node4: Create copy4, register. node4''s neighbors [node1, node3]: both already in memo. All nodes and edges processed. Return copy1'
    answer: '[[2,4],[1,3],[2,4],[1,3]]'
solution:
  code: "class Solution:\n    def cloneGraph(self, node: \"Node\") -> \"Node\":\n        oldToNew = {}\n\n        def dfs(node):\n            if node in oldToNew:\n                return oldToNew[node]\n\n            copy = Node(node.val)\n            oldToNew[node] = copy\n            for nei in node.neighbors:\n                copy.neighbors.append(dfs(nei))\n            return copy\n\n        return dfs(node) if node else None\n"
  complexity:
    time: O(V + E)
    space: O(V)
  followup:
  - ko: BFS를 사용하여 이 문제를 반복적으로(iteratively) 어떻게 해결할 수 있을까요?
    en: How would you solve this problem iteratively using BFS instead of DFS?
  - ko: 그래프가 매우 크면서 노드를 요청 시에만(on-demand) 복제해야 한다면 어떻게 설계할까요?
    en: How would you design a solution to clone nodes on-demand if the graph is extremely large?
  - ko: 이것이 방향 그래프(directed graph)라면 알고리즘이 어떻게 달라질까요?
    en: How would the algorithm change if this were a directed graph instead of undirected?
```