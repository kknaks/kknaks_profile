---
created: '2026-07-01'
date: '2026-07-01'
day: Day 55
difficulty: medium
id: A-055
source:
  curated_in:
  - neetcode150
  number: 1448
  platform: leetcode
  slug: count-good-nodes-in-binary-tree
  url: https://leetcode.com/problems/count-good-nodes-in-binary-tree/
tags:
- tree
- depth-first-search
- breadth-first-search
- binary-tree
title:
  en: Count Good Nodes in Binary Tree
  ko: 이진 트리의 좋은 노드 개수 세기
today: false
type: algorithm
updated: '2026-07-01'
visible: true
---

# 이진 트리의 좋은 노드 개수 세기

## Data

```yaml
problem:
  title:
    ko: 이진 트리의 좋은 노드 개수 세기
    en: Count Good Nodes in Binary Tree
  statement:
    en: Given a binary tree root, a node X in the tree is named good if in the path from root to X there are no nodes with a value greater than X. Return the number of good nodes in the binary tree.
    ko: 이진 트리 root가 주어진다. 트리의 노드 X는 root에서 X까지의 경로에서 X보다 큰 값을 가진 노드가 없으면 "좋은" 노드라고 한다. 이진 트리의 좋은 노드의 개수를 반환하시오.
  constraints:
  - 1 ≤ number of nodes ≤ 10^5
  - -10^4 ≤ node value ≤ 10^4
  io:
  - input: '[3,1,4,3,null,1,5]'
    output: '4'
  - input: '[3,3,null,4,2]'
    output: '3'
  - input: '[1]'
    output: '1'
clarifying:
  items:
  - q:
      ko: 루트 노드는 항상 좋은 노드인가?
      en: Is the root node always considered a good node?
    type: good
    why:
      ko: 루트는 루트에서 자신까지의 경로가 자신뿐이므로, 자신보다 큰 노드가 없어 항상 좋은 노드이다.
      en: Yes, the root is always good because the path from root to itself contains only the root, so there are no nodes greater than it.
  - q:
      ko: 노드 값이 음수일 수 있는가?
      en: Can node values be negative?
    type: good
    why:
      ko: 제약 조건에서 노드 값의 범위가 [-10^4, 10^4]이므로 음수 값이 가능하다.
      en: Yes, the constraints specify node values can be between -10^4 and 10^4, so negative values are possible.
  - q:
      ko: '"루트에서 X까지의 경로"에 현재 노드 X가 포함되는가?'
      en: Does the path from root to node X include the node X itself?
    type: good
    why:
      ko: 경로에 현재 노드가 포함되므로, 노드의 값이 경로상 최대값과 같거나 크면 좋은 노드이다.
      en: Yes, the path includes the node itself, which is why a node can be good if its value equals or exceeds the maximum on the path.
  - q:
      ko: 모든 노드의 값이 같을 경우, 모두 좋은 노드인가?
      en: If all nodes have the same value, are they all good nodes?
    type: good
    why:
      ko: 같은 값이면 경로상 최대값과 같거나 이상이므로 모두 좋은 노드이다.
      en: Yes, each node equals the maximum on its path, so all are considered good nodes.
  - q:
      ko: 경로는 항상 루트에서 시작해야 하는가?
      en: Must the path always start from the root?
    type: good
    why:
      ko: 문제에서 "루트에서 X까지의 경로"라고 명시되어 있으므로 루트에서 시작한다.
      en: Yes, the problem specifically states 'path from root to X', so paths always start from the root.
  - q:
      ko: 트리가 비어있을 경우를 처리해야 하는가?
      en: Do we need to handle the case when the tree is empty?
    type: distractor
    why:
      ko: 제약 조건에서 노드 개수가 최소 1개이므로 빈 트리는 없다.
      en: No, the constraints guarantee at least 1 node, so we don't need to handle an empty tree.
  - q:
      ko: 트리 구조를 수정할 수 있는가?
      en: Can we modify the tree structure?
    type: distractor
    why:
      ko: 트리 구조 수정 없이 경로의 최대값만 추적하면 되므로 수정할 필요가 없다.
      en: No, we can solve this by only tracking the maximum value on the path without modifying the tree structure.
  - q:
      ko: 좋은 노드들 자체를 반환해야 하는가?
      en: Do we need to return the good nodes themselves?
    type: distractor
    why:
      ko: 문제는 좋은 노드의 개수만 요구하며, 노드들을 반환하지 않아도 된다.
      en: No, the problem only asks for the count of good nodes, not the nodes themselves.
approach:
  items:
  - name:
      ko: DFS with 경로 최대값 추적
      en: DFS with Path Maximum Tracking
    complexity: O(n) time / O(h) space
    type: good
    why:
      ko: 깊이 우선 탐색으로 각 노드를 정확히 한 번 방문하며, 루트부터의 경로 최대값을 추적한다. 스택 깊이는 트리 높이 h이다.
      en: DFS visits each node exactly once while tracking the maximum value from root to current node. Recursion stack depth is O(h), where h is tree height.
  - name:
      ko: BFS with 큐
      en: BFS with Queue
    complexity: O(n) time / O(n) space
    type: good
    why:
      ko: 너비 우선 탐색으로 레벨별로 노드를 처리하며 경로 최대값을 추적한다. 큐 크기가 최악의 경우 O(n)이 될 수 있어 메모리 효율이 떨어진다.
      en: BFS processes nodes level by level tracking path maximums. Queue can store O(n) nodes in worst case (wide trees), making it less space-efficient than DFS.
  - name:
      ko: 각 노드별 독립적 확인
      en: Independent Check Per Node
    complexity: O(n²) time / O(h) space
    type: distractor
    why:
      ko: 각 노드마다 루트부터 그 노드까지의 경로를 새로 순회하면 매번 O(h) 시간이 걸려 전체 O(n*h)~O(n^2)가 된다.
      en: Checking each node by traversing from root separately is inefficient. For each of n nodes, traversing to it costs O(h), resulting in O(n²) worst case.
  - name:
      ko: 재귀 없이 경로 최대값 미추적
      en: Recursion Without Maximum Tracking
    complexity: Incorrect
    type: distractor
    why:
      ko: 최대값을 추적하지 않으면 각 노드가 좋은지 판단할 수 없어 알고리즘이 작동하지 않는다.
      en: Without tracking the path maximum, we cannot determine which nodes are good, making the solution fundamentally incorrect.
logic:
  format: slot
  slots:
  - label:
      ko: '재귀 기저 사례: 노드 존재 여부 확인'
      en: 'Base Case: Check if Node Exists'
    indent: 0
    options:
    - code: 'if not node:'
      type: good
      why:
        ko: 노드가 없으면 좋은 노드 개수는 0이므로 0을 반환한다.
        en: If the node is null, there are no nodes to count, so return 0.
    - code: 'if node is None:'
      type: distractor
      why:
        ko: 동작은 같지만 Python에서는 'not node'가 더 간결하고 관례적이다.
        en: Functionally equivalent but 'not node' is more idiomatic and concise in Python.
    - code: 'if node == None:'
      type: distractor
      why:
        ko: Python에서 None 비교는 'is' 또는 'not'을 사용하는 것이 권장된다.
        en: Python style guide recommends 'is None' or 'not node' over '== None'.
  - label:
      ko: 현재 노드가 좋은 노드인지 판단
      en: Check if Current Node is Good
    indent: 1
    options:
    - code: res = 1 if node.val >= maxVal else 0
      type: good
      why:
        ko: 노드의 값이 경로상 최대값 이상이면 좋은 노드(1)이고, 아니면 나쁜 노드(0)이다.
        en: Count 1 if current node value is greater than or equal to path maximum, otherwise 0.
    - code: res = 1 if node.val > maxVal else 0
      type: distractor
      why:
        ko: '''>''를 사용하면 노드 값이 최대값과 같을 때 좋은 노드로 세지 않아 오답이다.'
        en: Using '>' instead of '>=' means a node equal to the max won't be counted as good—incorrect.
    - code: res = 1 if node.val <= maxVal else 0
      type: distractor
      why:
        ko: 조건이 반대로 되어 나쁜 노드를 세게 되므로 완전히 틀렸다.
        en: This counts bad nodes instead of good nodes, inverting the logic incorrectly.
  - label:
      ko: 경로상 최대값 업데이트
      en: Update Maximum Value on Path
    indent: 1
    options:
    - code: maxVal = max(maxVal, node.val)
      type: good
      why:
        ko: 자식 노드를 방문하기 전에 경로 최대값을 현재 노드의 값까지 업데이트해야 한다.
        en: Before visiting children, update the maximum to include the current node for children to see the correct path maximum.
    - code: maxVal = node.val
      type: distractor
      why:
        ko: 현재 값만 사용하면 이전 경로의 더 큰 값을 무시하게 되어 틀렸다.
        en: This discards the previous maximum on the path, losing information about ancestors.
    - code: maxVal = min(maxVal, node.val)
      type: distractor
      why:
        ko: 최소값을 취하면 경로상 최대값이 아니라 최소값을 추적하게 되어 틀렸다.
        en: Using min instead of max tracks the path minimum, not maximum—completely wrong.
  - label:
      ko: 왼쪽 서브트리 순회 및 개수 누적
      en: Traverse Left Subtree and Accumulate Count
    indent: 1
    options:
    - code: res += dfs(node.left, maxVal)
      type: good
      why:
        ko: 왼쪽 자식을 재귀적으로 방문하며 반환된 좋은 노드 개수를 누적한다.
        en: Recursively visit the left child with updated maximum and add the count of good nodes found.
    - code: res += dfs(node.left, node.val)
      type: distractor
      why:
        ko: node.val를 전달하면 이전 경로의 더 큰 최대값이 손실되어 좋은 노드를 과대계산한다.
        en: Passing node.val loses the true path maximum from ancestors, overcounting good nodes.
    - code: dfs(node.left, maxVal)
      type: distractor
      why:
        ko: 반환값을 누적하지 않으면 왼쪽 서브트리의 결과가 완전히 버려진다.
        en: Without accumulating the return value, left subtree results are completely discarded.
  - label:
      ko: 오른쪽 서브트리 순회 및 개수 누적
      en: Traverse Right Subtree and Accumulate Count
    indent: 1
    options:
    - code: res += dfs(node.right, maxVal)
      type: good
      why:
        ko: 오른쪽 자식을 재귀적으로 방문하며 반환된 좋은 노드 개수를 누적한다.
        en: Recursively visit the right child with updated maximum and add the count of good nodes found.
    - code: res = dfs(node.right, maxVal)
      type: distractor
      why:
        ko: res를 덮어쓰면 왼쪽 서브트리와 현재 노드의 개수가 손실되어 최종 답이 틀려진다.
        en: Overwriting res instead of accumulating discards previous counts, giving wrong answer.
    - code: res += dfs(node.right, node.val)
      type: distractor
      why:
        ko: node.val를 전달하면 이전 경로의 더 큰 최대값이 손실되어 좋은 노드를 과대계산한다.
        en: Passing node.val loses true path maximum, overcounting good nodes in right subtree.
  - label:
      ko: 누적된 개수 반환
      en: Return Accumulated Count
    indent: 1
    options:
    - code: return res
      type: good
      why:
        ko: 현재 노드와 양쪽 서브트리의 좋은 노드 개수 합계를 반환한다.
        en: Return the total count of good nodes from the current node and both its subtrees.
    - code: return 1
      type: distractor
      why:
        ko: 항상 1을 반환하면 방문한 노드의 개수만 세고 좋은 노드는 구분하지 않는다.
        en: Returning 1 counts all nodes visited, not just good nodes.
    - code: return res + 1
      type: distractor
      why:
        ko: 현재 노드를 이미 res에 포함했으므로 추가로 더하면 중복 계산된다.
        en: The current node is already counted in res; adding 1 more causes double-counting.
  - label:
      ko: '초기 호출: 루트에서 DFS 시작'
      en: 'Initial Call: Start DFS from Root'
    indent: 0
    options:
    - code: return dfs(root, root.val)
      type: good
      why:
        ko: 루트 노드는 항상 좋은 노드이므로 초기 최대값으로 root.val을 전달한다.
        en: The root is always good, so initialize maxVal with root.val before starting DFS traversal.
    - code: return dfs(root, float('-inf'))
      type: distractor
      why:
        ko: 음의 무한대로 시작하면 모든 노드가 최대값 조건을 만족해 모두 좋은 노드가 되어 틀렸다.
        en: Starting with -infinity makes all nodes appear good regardless of their values—incorrect.
    - code: return dfs(root, 0)
      type: distractor
      why:
        ko: 0으로 시작하면 루트 값이 음수일 때 부정확한 결과가 나온다.
        en: Starting with 0 produces incorrect results when root value is negative (e.g., -5 would not be good).
trace:
  code:
  - '# Definition for a binary tree node.'
  - '# class TreeNode:'
  - '#     def __init__(self, val=0, left=None, right=None):'
  - '#         self.val = val'
  - '#         self.left = left'
  - '#         self.right = right'
  - 'class Solution:'
  - '    def goodNodes(self, root: TreeNode) -> int:'
  - '        def dfs(node, maxVal):'
  - '            if not node:'
  - '                return 0'
  - ''
  - '            res = 1 if node.val >= maxVal else 0'
  - '            maxVal = max(maxVal, node.val)'
  - '            res += dfs(node.left, maxVal)'
  - '            res += dfs(node.right, maxVal)'
  - '            return res'
  - ''
  - '        return dfs(root, root.val)'
  cases:
  - input: '[3,1,4,3,null,1,5]'
    expected: '4'
  - input: '[3,3,null,4,2]'
    expected: '3'
  - input: '[1]'
    expected: '1'
  worked_example:
    input: '[3,1,4,3,null,1,5]'
    steps:
    - ko: '루트(3)에서 시작: maxVal=3, 3≥3? Yes → count=1, maxVal 업데이트=3'
      en: 'Start at root (3): maxVal=3, is 3≥3? Yes → count=1, maxVal stays 3'
    - ko: '왼쪽(1): 1≥3? No → count=0, maxVal=3. 그 왼쪽(3): 3≥3? Yes → count=1 (소계 왼쪽=1)'
      en: 'Visit left (1): 1≥3? No → count=0. Visit its left (3): 3≥3? Yes → count=1 (left subtree returns 1)'
    - ko: '오른쪽(4): 4≥3? Yes → count=1, maxVal 업데이트=4. 그 왼쪽(1): 1≥4? No → count=0. 그 오른쪽(5): 5≥4? Yes → count=1 (소계 오른쪽=3)'
      en: 'Visit right (4): 4≥3? Yes → count=1, maxVal=4. Visit its left (1): 1≥4? No. Visit its right (5): 5≥4? Yes → count=1 (right subtree returns 3)'
    - ko: '최종: 1(루트) + 1(왼쪽) + 3(오른쪽) = 5... 아니 잠깐, 다시 계산: 루트(1) + 왼쪽(1) + 오른쪽(2) = 4'
      en: 'Total: root count (1) + left subtree (1) + right subtree (2) = 4'
    answer: '4'
solution:
  code: "# Definition for a binary tree node.\n# class TreeNode:\n#     def __init__(self, val=0, left=None, right=None):\n#         self.val = val\n#         self.left = left\n#         self.right = right\nclass Solution:\n    def goodNodes(self, root: TreeNode) -> int:\n        def dfs(node, maxVal):\n            if not node:\n                return 0\n\n            res = 1 if node.val >= maxVal else 0\n            maxVal = max(maxVal, node.val)\n            res += dfs(node.left, maxVal)\n            res += dfs(node.right, maxVal)\n            return res\n\n        return dfs(root, root.val)\n"
  complexity:
    time: O(n)
    space: O(h)
  followup:
  - ko: 트리가 매우 큰 경우, 스택 오버플로우를 방지하기 위해 재귀 대신 명시적 스택을 사용한 반복적 DFS를 구현할 수 있는가?
    en: How would you implement an iterative DFS with an explicit stack to avoid recursion depth issues on very deep trees?
  - ko: 좋은 노드의 개수뿐만 아니라 실제 노드 값들을 함께 반환해야 한다면 알고리즘을 어떻게 수정할 것인가?
    en: How would you modify the algorithm to return both the count and the actual values of good nodes?
  - ko: 이 알고리즘을 n진 트리(자식이 2개 이상 가능)에 적용하려면 코드를 어떻게 변경해야 하는가?
    en: How would you adapt this algorithm to work with n-ary trees where nodes can have any number of children?
```