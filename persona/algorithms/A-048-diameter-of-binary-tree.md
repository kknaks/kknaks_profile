---
created: '2026-06-23'
date: '2026-06-23'
day: Day 48
difficulty: easy
id: A-048
source:
  curated_in:
  - neetcode150
  number: 543
  platform: leetcode
  slug: diameter-of-binary-tree
  url: https://leetcode.com/problems/diameter-of-binary-tree/
status: draft
tags:
- tree
- depth-first-search
- binary-tree
title:
  en: Diameter of Binary Tree
  ko: 이진 트리의 지름
today: true
type: algorithm
updated: '2026-06-23'
visible: true
---

# 이진 트리의 지름

## Data

```yaml
problem:
  title:
    ko: 이진 트리의 지름
    en: Diameter of Binary Tree
  statement:
    ko: '이진 트리의 루트가 주어졌을 때, 트리의 지름의 길이를 반환하세요.


      이진 트리의 지름은 트리의 임의의 두 노드 사이의 가장 긴 경로의 길이입니다. 이 경로는 루트를 지날 수도 있고 지나지 않을 수도 있습니다.


      두 노드 사이 경로의 길이는 그 사이의 간선(edge)의 개수로 표현됩니다.'
    en: 'Given the root of a binary tree, return the length of the diameter of the tree.


      The diameter of a binary tree is the length of the longest path between any two nodes in a tree. This path may or may not pass through the root.


      The length of a path between two nodes is represented by the number of edges between them.'
  constraints:
  - The number of nodes in the tree is in the range [1, 10^4]
  - -100 ≤ Node.val ≤ 100
  io:
  - input: '[1,2,3,4,5]'
    output: '3'
  - input: '[1,2]'
    output: '1'
clarifying:
  items:
  - q:
      ko: 지름 경로는 반드시 루트를 지나야 하나요?
      en: Must the diameter path always pass through the root?
    type: good
    why:
      ko: 아니요. 지름은 트리의 임의의 두 노드 사이의 가장 긴 경로이므로 루트를 지나지 않을 수도 있습니다.
      en: No. The diameter is the longest path between any two nodes, which may not include the root.
  - q:
      ko: 경로의 길이는 노드 개수로 세나요, 간선 개수로 세나요?
      en: Is the path length measured by number of nodes or number of edges?
    type: good
    why:
      ko: 간선 개수로 셉니다. 예를 들어 [4,2,1,3] 경로는 3개의 간선(4→2, 2→1, 1→3)을 가집니다.
      en: By number of edges. For example, the path [4,2,1,3] has 3 edges (4→2, 2→1, 1→3).
  - q:
      ko: 노드가 1개인 트리의 지름은 얼마인가요?
      en: What is the diameter of a tree with only one node?
    type: good
    why:
      ko: 0입니다. 단일 노드 트리는 경로가 없으므로 지름은 0입니다.
      en: 0. A single-node tree has no paths, so its diameter is 0.
  - q:
      ko: DFS 재귀에서 각 노드가 반환해야 할 값은 무엇인가요?
      en: What should each node return in the DFS recursion?
    type: good
    why:
      ko: 각 노드는 자신을 거치는 가장 깊은 경로의 길이(높이)를 반환합니다. 이를 이용해 지름을 계산합니다.
      en: Each node should return its height (length of the longest path from it to a leaf). This is used to calculate diameter at each node.
  - q:
      ko: 지름의 최댓값은 각 노드에서 어떻게 계산되나요?
      en: How is the maximum diameter calculated at each node?
    type: good
    why:
      ko: 각 노드에서 지름은 왼쪽 자식 높이 + 오른쪽 자식 높이입니다. 이는 두 서브트리를 연결하는 경로입니다.
      en: At each node, the diameter is left_height + right_height, representing the longest path connecting the two subtrees.
  - q:
      ko: 시간 복잡도를 O(1)로 개선할 수 있나요?
      en: Can the time complexity be improved to O(1)?
    type: distractor
    why:
      ko: 아니요. 모든 노드를 방문해야 하므로 최소한 O(n)의 시간이 필요합니다.
      en: No. We must visit all nodes, so O(n) time is necessary.
  - q:
      ko: 지름이 트리의 높이와 같을 수 있나요?
      en: Can the diameter be equal to the tree height?
    type: distractor
    why:
      ko: 경우에 따라 다릅니다. 한쪽으로 치우친 트리에서는 지름이 높이와 같을 수 있습니다.
      en: It depends. In a skewed tree with nodes on one side only, the diameter can equal the height.
approach:
  items:
  - name:
      ko: 깊이 우선 탐색 (DFS)
      en: Depth-First Search (DFS)
    complexity: O(n) time / O(h) space
    type: good
    why:
      ko: 각 노드를 한 번씩 방문하면서 높이를 계산하고 지름을 추적합니다. 공간은 재귀 스택 깊이만큼 필요합니다.
      en: Visit each node once, computing heights and tracking maximum diameter. Space is proportional to the recursion stack depth (height).
  - name:
      ko: 너비 우선 탐색 (BFS)
      en: Breadth-First Search (BFS)
    complexity: O(n^2) time / O(n) space
    type: distractor
    why:
      ko: 각 노드에서 BFS를 시작하여 가장 긴 경로를 찾으면 매우 비효율적입니다.
      en: Starting BFS from each node to find the longest path is very inefficient.
  - name:
      ko: 모든 경로 저장
      en: Store all paths
    complexity: O(n^2) time / O(n^2) space
    type: distractor
    why:
      ko: 트리의 모든 경로를 저장하고 비교하는 것은 불필요한 추가 메모리를 사용합니다.
      en: Storing and comparing all tree paths uses unnecessary extra memory.
  - name:
      ko: 노드 쌍 비교 (브루트 포스)
      en: Node pair comparison (brute force)
    complexity: O(n^2) time / O(1) space
    type: distractor
    why:
      ko: 모든 노드 쌍 사이의 거리를 계산하면 O(n^2) 시간이 필요하여 비효율적입니다.
      en: Computing distance between all node pairs requires O(n^2) time and is inefficient.
logic:
  format: slot
  slots:
  - label:
      ko: 결과 변수 초기화
      en: Initialize result variable
    indent: 0
    options:
    - code: res = 0
      type: good
      why:
        ko: 지름의 최댓값을 추적하기 위해 res를 0으로 초기화합니다.
        en: Initialize res to 0 to track the maximum diameter found so far.
    - code: res = -1
      type: distractor
      why:
        ko: 음수로 시작하면 나중에 max 비교에서 문제가 될 수 있습니다.
        en: Starting with negative value can cause issues in max comparisons later.
    - code: res = float('inf')
      type: distractor
      why:
        ko: 최솟값을 찾는 것이 아니므로 무한대로 초기화할 필요가 없습니다.
        en: There's no need to initialize to infinity since we're finding a maximum, not minimum.
  - label:
      ko: DFS 함수 정의
      en: Define DFS function
    indent: 0
    options:
    - code: 'def dfs(root):'
      type: good
      why:
        ko: 재귀적으로 각 노드를 방문하고 높이를 계산하는 헬퍼 함수를 정의합니다.
        en: Define a helper function to recursively visit nodes and compute heights.
    - code: 'def bfs(root):'
      type: distractor
      why:
        ko: BFS는 이 문제에 필요한 깊이 정보를 효율적으로 제공하지 못합니다.
        en: BFS doesn't provide the depth information needed for this problem efficiently.
    - code: 'def diameter(root):'
      type: distractor
      why:
        ko: 함수 이름은 지름을 의미하지만, 실제로는 높이를 반환해야 합니다.
        en: The function name suggests diameter, but it actually returns height.
  - label:
      ko: 재귀 종료 조건
      en: Recursion base case
    indent: 1
    options:
    - code: 'if not root:'
      type: good
      why:
        ko: 노드가 없으면 높이는 0입니다. 이것이 재귀의 기저 사례입니다.
        en: If a node is null, its height is 0. This is the base case for recursion.
    - code: 'if root is None: return -1'
      type: distractor
      why:
        ko: -1을 반환하면 나중의 높이 계산에서 오류가 발생합니다.
        en: Returning -1 causes errors in height calculations later.
    - code: 'if not root.left and not root.right: return 1'
      type: distractor
      why:
        ko: 이것은 리프 노드를 체크하는 것이므로 기저 사례가 아닙니다.
        en: This checks for leaf nodes, which is not the correct base case.
  - label:
      ko: 왼쪽/오른쪽 자식 높이 계산
      en: Compute left and right subtree heights
    indent: 1
    options:
    - code: left = dfs(root.left)
      type: good
      why:
        ko: 각 자식 서브트리의 높이를 재귀적으로 계산합니다. 이 값들이 현재 노드의 지름 계산에 사용됩니다.
        en: Recursively compute the height of each child subtree. These values are used to calculate the diameter at the current node.
    - code: left = dfs(root.left) + 1
      type: distractor
      why:
        ko: 여기서 +1을 하면 중복 계산이 되어 나중에 높이 반환 시 오류가 발생합니다.
        en: Adding 1 here causes double-counting since we add 1 again in the return statement.
    - code: right = root.right.val
      type: distractor
      why:
        ko: 노드의 값을 읽는 것이지 높이가 아닙니다.
        en: This reads the node's value, not its height.
  - label:
      ko: 지름 최댓값 갱신
      en: Update maximum diameter
    indent: 1
    options:
    - code: res = max(res, left + right)
      type: good
      why:
        ko: 현재 노드에서의 지름(왼쪽 높이 + 오른쪽 높이)이 지금까지의 최댓값을 초과하면 res를 갱신합니다.
        en: If the diameter at this node (left_height + right_height) exceeds the current maximum, update res.
    - code: res = left + right
      type: distractor
      why:
        ko: max()를 사용하지 않으면 항상 덮어씌워져서 이전 최댓값을 잃을 수 있습니다.
        en: Without max(), we always overwrite, losing the previous maximum.
    - code: res += left + right
      type: distractor
      why:
        ko: 누적하면 안 되고, 최댓값을 추적해야 합니다.
        en: We should track the maximum, not accumulate values.
  - label:
      ko: 현재 노드의 높이 반환
      en: Return height of current subtree
    indent: 1
    options:
    - code: return 1 + max(left, right)
      type: good
      why:
        ko: 부모 노드가 자신의 높이를 계산할 수 있도록 현재 노드를 거치는 가장 깊은 경로의 길이를 반환합니다.
        en: Return the length of the longest path from the current node to any leaf so that the parent can use it in its calculations.
    - code: return max(left, right)
      type: distractor
      why:
        ko: 노드 자신을 경로에 포함하지 않으므로 높이가 잘못됩니다.
        en: This doesn't account for the current node in the path, giving incorrect height.
    - code: return left + right
      type: distractor
      why:
        ko: 이것은 지름이지 높이가 아닙니다. 높이는 한쪽 경로의 길이여야 합니다.
        en: This is diameter, not height. Height should be the length of one path, not both.
trace:
  code:
  - '# Definition for a binary tree node.'
  - '# class TreeNode:'
  - '#     def __init__(self, val=0, left=None, right=None):'
  - '#         self.val = val'
  - '#         self.left = left'
  - '#         self.right = right'
  - 'class Solution:'
  - '    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:'
  - '        res = 0'
  - ''
  - '        def dfs(root):'
  - '            nonlocal res'
  - ''
  - '            if not root:'
  - '                return 0'
  - '            left = dfs(root.left)'
  - '            right = dfs(root.right)'
  - '            res = max(res, left + right)'
  - ''
  - '            return 1 + max(left, right)'
  - ''
  - '        dfs(root)'
  - '        return res'
  cases:
  - input: '[1,2,3,4,5]'
    expected: '3'
  - input: '[1,2]'
    expected: '1'
  worked_example:
    input: '[1,2,3,4,5]'
    steps:
    - ko: '트리 구조: 1을 루트로 하고, 2(왼쪽)와 3(오른쪽)을 자식으로, 2의 자식은 4와 5입니다.'
      en: 'Tree structure: root is 1, with left child 2 and right child 3; node 2 has children 4 and 5.'
    - ko: 'DFS(4): 리프, left=0, right=0, res는 0, 높이 1 반환.'
      en: 'DFS(4): leaf node, left=0, right=0, diameter=0, returns height 1.'
    - ko: 'DFS(5): 리프, left=0, right=0, res는 0, 높이 1 반환.'
      en: 'DFS(5): leaf node, left=0, right=0, diameter=0, returns height 1.'
    - ko: 'DFS(2): left=1, right=1, res=max(0, 1+1)=2, 높이 1+max(1,1)=2 반환.'
      en: 'DFS(2): left=1, right=1, update res=max(0,2)=2, returns height 1+max(1,1)=2.'
    - ko: 'DFS(3): 자식 없음, left=0, right=0, diameter=0, 높이 1 반환.'
      en: 'DFS(3): no children, left=0, right=0, diameter=0, returns height 1.'
    - ko: 'DFS(1): left=2, right=1, res=max(2, 2+1)=3, 결과는 3입니다.'
      en: 'DFS(1): left=2, right=1, update res=max(2,3)=3. Final answer is 3.'
    answer: '3'
solution:
  code: "# Definition for a binary tree node.\n# class TreeNode:\n#     def __init__(self, val=0, left=None, right=None):\n#         self.val = val\n#         self.left = left\n#         self.right = right\nclass Solution:\n    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:\n        res = 0\n\n        def dfs(root):\n            nonlocal res\n\n            if not root:\n                return 0\n            left = dfs(root.left)\n            right = dfs(root.right)\n            res = max(res, left + right)\n\n            return 1 + max(left, right)\n\n        dfs(root)\n        return res\n"
  complexity:
    time: O(n)
    space: O(h)
  followup:
  - ko: '후속: 반복문 기반 후위 순회(post-order traversal)로 이 문제를 풀 수 있나요?'
    en: 'Follow-up: How would you solve this using an iterative post-order traversal instead of recursion?'
  - ko: '후속: 트리가 극도로 비균형이라면(모든 노드가 한쪽에만 있다면) 성능은 어떻게 될까요?'
    en: 'Follow-up: What happens to space complexity if the tree is extremely skewed with all nodes on one side?'
  - ko: '후속: 여러 개의 지름 경로가 있을 때, 모든 경로의 끝점(노드들)을 찾을 수 있나요?'
    en: 'Follow-up: If multiple paths have the maximum diameter, can you find the endpoint nodes of all such paths?'
```