---
created: '2026-07-05'
date: '2026-07-05'
day: Day 59
difficulty: hard
id: A-059
source:
  curated_in:
  - neetcode150
  number: 124
  platform: leetcode
  slug: binary-tree-maximum-path-sum
  url: https://leetcode.com/problems/binary-tree-maximum-path-sum/
status: draft
tags:
- dynamic-programming
- tree
- depth-first-search
- binary-tree
title:
  en: Binary Tree Maximum Path Sum
  ko: 이진 트리 최대 경로 합
today: true
type: algorithm
updated: '2026-07-05'
visible: true
---

# 이진 트리 최대 경로 합

## Data

```yaml
problem:
  title:
    ko: 이진 트리 최대 경로 합
    en: Binary Tree Maximum Path Sum
  statement:
    ko: '이진 트리의 경로는 인접한 노드 쌍이 간선으로 연결된 노드의 수열입니다. 각 노드는 수열에 최대 한 번만 나타날 수 있습니다. 경로가 반드시 루트를 지나야 하는 것은 아닙니다.


      경로의 경로 합은 경로에 포함된 노드 값들의 합입니다.


      이진 트리의 루트가 주어질 때, 임의의 0이 아닌 경로의 최대 경로 합을 반환하세요.'
    en: 'A path in a binary tree is a sequence of nodes where each pair of adjacent nodes in the sequence has an edge connecting them. A node can only appear in the sequence at most once. Note that the path does not need to pass through the root.


      The path sum of a path is the sum of the node''s values in the path.


      Given the root of a binary tree, return the maximum path sum of any non-empty path.'
  constraints:
  - The number of nodes in the tree is in the range [1, 3 * 10^4]
  - -1000 ≤ Node.val ≤ 1000
  io:
  - input: '[1,2,3]'
    output: '6'
  - input: '[-10,9,20,null,null,15,7]'
    output: '42'
clarifying:
  items:
  - q:
      ko: 경로가 루트를 반드시 포함해야 하나요?
      en: Does the path need to include the root?
    type: good
    why:
      ko: 아니요, 경로는 트리의 어느 노드에서든 시작하고 끝날 수 있습니다. 예제 2에서 최적 경로 15→20→7은 루트 -10을 포함하지 않습니다.
      en: No, the path can start and end at any node in the tree. In Example 2, the optimal path 15→20→7 does not include the root -10.
  - q:
      ko: 경로가 한 노드에서 양쪽 자식으로 동시에 갈 수 있나요?
      en: Can a path go through both left and right children of a node?
    type: good
    why:
      ko: 네, 경로는 한 노드에서 분기할 수 있습니다. 예를 들어 예제 1의 최적 경로 2→1→3이 그렇습니다.
      en: Yes, a path can branch at a node. Example 1's optimal path 2→1→3 demonstrates this.
  - q:
      ko: 음수 노드 값이 있을 때 그것을 건너뛸 수 있나요?
      en: Can we skip negative node values when they would decrease the sum?
    type: good
    why:
      ko: 경로는 연속된 노드들이어야 하므로 건너뛸 수 없습니다. 하지만 음수 서브트리로의 확장을 피할 수 있습니다.
      en: No, paths must be contiguous, so we cannot skip nodes. However, we can avoid extending paths into negative subtrees.
  - q:
      ko: 단일 노드만 있는 경로도 유효한가요?
      en: Is a single-node path a valid answer?
    type: good
    why:
      ko: 네, 문제에서 '0이 아닌 경로'를 요구하므로 단일 노드도 경로입니다.
      en: Yes, a single node is a valid path per the problem's 'non-empty path' requirement.
  - q:
      ko: DFS 함수는 왜 '분기 경로'의 합을 반환하지 않고 '선형 경로'의 합을 반환하나요?
      en: Why does DFS return the linear-path sum instead of the branched-path sum?
    type: distractor
    why:
      ko: 분기 경로(양쪽 자식 포함)는 부모로 확장될 수 없습니다. 부모 노드가 경로를 계속 확장할 수 있으려면 한쪽 자식만 포함한 선형 경로를 반환해야 합니다.
      en: A branched path (including both children) cannot be extended to the parent. We return a linear path (one child) so the parent can continue extending upward.
  - q:
      ko: 왜 음수 부경로를 0으로 '리셋'합니까?
      en: Why set negative subpath sums to 0 instead of keeping them?
    type: distractor
    why:
      ko: 음수 부경로는 확장 경로의 합을 감소시킵니다. 0으로 리셋하는 것은 그 방향으로 경로를 확장하지 않는 것과 동치입니다.
      en: Negative subpaths would decrease the extended path sum. Setting to 0 is equivalent to not extending the path in that direction.
approach:
  items:
  - name:
      ko: 깊이 우선 탐색(DFS) + 전역 변수 추적
      en: Depth-First Search (DFS) + Global Variable Tracking
    complexity: O(n) time / O(h) space (h = tree height)
    type: good
    why:
      ko: '각 노드를 정확히 한 번 방문하며, 각 노드에서 두 가지를 추적합니다: (1) 부모로 확장 가능한 최대 경로, (2) 이 노드에서 분기할 때의 최대 경로. 재귀 깊이는 트리 높이입니다.'
      en: 'Visit each node exactly once and track two values per node: (1) max path extendable to parent, (2) max path if branching at this node. Recursion depth is tree height.'
  - name:
      ko: 후순위 재귀 순회
      en: Post-order Recursive Traversal
    complexity: O(n) time / O(h) space
    type: good
    why:
      ko: 후순위 순회(자식 먼저 처리)는 자식의 결과가 필요할 때 이미 계산되어 있도록 보장합니다. 이것이 DFS의 핵심입니다.
      en: Post-order traversal (process children first) ensures child results are available when needed. This is why DFS works here.
  - name:
      ko: 모든 경로 열거(브루트 포스)
      en: Enumerate All Paths (Brute Force)
    complexity: O(n²) time / O(n) space
    type: distractor
    why:
      ko: 모든 가능한 경로를 명시적으로 나열하고 각각을 계산할 수 있지만, 중복 계산이 많아 비효율적입니다.
      en: Explicitly enumerate and sum all paths works but has redundant calculations. DFS memoization avoids this.
  - name:
      ko: 반복적 후순위 순회(스택 사용)
      en: Iterative Post-order with Stack
    complexity: O(n) time / O(h) space
    type: distractor
    why:
      ko: 반복적 구현도 O(n)을 달성할 수 있지만, 명시적 스택 관리가 복잡하며 재귀 버전이 더 직관적입니다.
      en: Iterative post-order can also achieve O(n), but managing explicit stacks is complex. Recursion is more intuitive here.
logic:
  format: slot
  slots:
  - label:
      ko: 초기값 설정
      en: Initialize result with root value
    indent: 0
    options:
    - code: res = [root.val]
      type: good
      why:
        ko: 최대 경로 합은 최소한 루트 노드의 값이어야 합니다. 리스트로 감싸면 DFS 내부에서 값을 업데이트할 수 있습니다.
        en: The maximum path sum is at least the root's value. Using a list allows the nested DFS function to update it.
    - code: res = float('-inf')
      type: distractor
      why:
        ko: 음수 무한대도 작동하지만, 루트 값으로 초기화하면 첫 반복에서 불필요한 비교를 줄입니다.
        en: This would work but initializing with root.val saves an unnecessary comparison.
    - code: res = [0]
      type: distractor
      why:
        ko: 0으로 초기화하면 모든 음수 트리에서 오류가 발생합니다.
        en: Initializing to 0 would fail for all-negative trees.
  - label:
      ko: DFS 함수 정의
      en: Define recursive DFS function
    indent: 0
    options:
    - code: 'def dfs(root):'
      type: good
      why:
        ko: 중첩 함수를 정의하여 외부 'res' 변수에 접근 가능하게 합니다.
        en: Define a nested function with access to the outer 'res' variable via closure.
    - code: 'def dfs(root, res):'
      type: distractor
      why:
        ko: res를 매개변수로 전달해도 작동하지만, 클로저가 파이썬에서 더 표준적입니다.
        en: Passing res as a parameter would work but closures are more idiomatic.
    - code: "def dfs(root):\n    global res"
      type: distractor
      why:
        ko: 전역 변수도 가능하지만, 클로저가 더 캡슐화되어 있습니다.
        en: Global would work but is less encapsulated than a closure.
  - label:
      ko: 좌우 서브트리에서 최대 확장 경로 계산
      en: Recursively compute max extension from each child
    indent: 1
    options:
    - code: leftMax = dfs(root.left)
      type: good
      why:
        ko: 왼쪽과 오른쪽 자식에서 재귀적으로 최대 확장 경로를 구합니다. 이 값들은 음수일 수 있습니다.
        en: Recursively get the max extension from left and right children. These can be negative.
    - code: 'leftMax = max(dfs(root.left), 0)

        rightMax = max(dfs(root.right), 0)'
      type: distractor
      why:
        ko: 음수를 즉시 0으로 리셋하면 작동하지만, 별도 단계가 명확성을 높입니다.
        en: Resetting to 0 immediately works but separate steps are clearer.
    - code: leftMax = dfs(root.left) + dfs(root.right)
      type: distractor
      why:
        ko: 양쪽을 더하면 논리가 틀립니다. 각각 독립적으로 계산되어야 합니다.
        en: Summing both is incorrect; they must be computed independently.
  - label:
      ko: 음수 기여도를 0으로 리셋
      en: Ignore negative subpaths by clamping to 0
    indent: 1
    options:
    - code: leftMax = max(leftMax, 0)
      type: good
      why:
        ko: 음수 부경로는 합을 감소시키므로, 경로를 확장하지 않는 것과 같습니다. 0으로 설정하면 '이 방향으로 확장하지 않음'을 의미합니다.
        en: Negative subpaths decrease the sum, so we treat them as not extending the path (set to 0).
    - code: leftMax = max(leftMax, -1000)
      type: distractor
      why:
        ko: 임의의 음수로 제한하면 음의 기여도를 완전히 무시하지 못합니다.
        en: Clamping to an arbitrary negative value doesn't fully ignore negative contributions.
    - code: "if leftMax < 0:\n    leftMax = 0"
      type: distractor
      why:
        ko: 조건 분기로도 작동하지만, max() 함수가 더 간결합니다.
        en: An if-statement works but max() is more concise.
  - label:
      ko: 이 노드에서 분기하는 경로로 전역 최대값 업데이트
      en: Update global max with path branching at this node
    indent: 1
    options:
    - code: res[0] = max(res[0], root.val + leftMax + rightMax)
      type: good
      why:
        ko: 현재 노드 값 + 왼쪽 최대값 + 오른쪽 최대값으로 이 노드를 정점으로 하는 경로 합을 계산합니다.
        en: Compute the sum of current node + both child paths (branched path with this node as apex).
    - code: res[0] = max(res[0], leftMax + rightMax)
      type: distractor
      why:
        ko: 현재 노드 값을 빼먹으면 경로 합이 불완전합니다.
        en: Omitting root.val gives an incomplete path sum.
    - code: res[0] = root.val + leftMax + rightMax - 1
      type: distractor
      why:
        ko: 임의의 수정은 계산을 왜곡합니다.
        en: Arbitrary modifications corrupt the calculation.
  - label:
      ko: 부모로 확장 가능한 경로 반환
      en: Return the maximum path extendable to parent
    indent: 1
    options:
    - code: return root.val + max(leftMax, rightMax)
      type: good
      why:
        ko: 현재 노드 + 더 큰 자식 경로를 반환합니다. 부모에서 이 반환값을 받아 자신과 함께 확장할 수 있습니다.
        en: Return current node plus the larger child's extension so the parent can include this in its path.
    - code: return root.val + leftMax + rightMax
      type: distractor
      why:
        ko: 양쪽을 모두 포함하면 경로가 분기되어 부모로 단일 경로로 확장될 수 없습니다.
        en: Including both children creates a branched path that cannot extend linearly to the parent.
    - code: return max(leftMax, rightMax)
      type: distractor
      why:
        ko: 현재 노드를 빼먹으면 경로가 단절됩니다.
        en: Omitting the current node breaks path continuity.
trace:
  code:
  - '# Definition for a binary tree node.'
  - '# class TreeNode:'
  - '#     def __init__(self, val=0, left=None, right=None):'
  - '#         self.val = val'
  - '#         self.left = left'
  - '#         self.right = right'
  - 'class Solution:'
  - '    def maxPathSum(self, root: TreeNode) -> int:'
  - '        res = [root.val]'
  - ''
  - '        # return max path sum without split'
  - '        def dfs(root):'
  - '            if not root:'
  - '                return 0'
  - ''
  - '            leftMax = dfs(root.left)'
  - '            rightMax = dfs(root.right)'
  - '            leftMax = max(leftMax, 0)'
  - '            rightMax = max(rightMax, 0)'
  - ''
  - '            # compute max path sum WITH split'
  - '            res[0] = max(res[0], root.val + leftMax + rightMax)'
  - '            return root.val + max(leftMax, rightMax)'
  - ''
  - '        dfs(root)'
  - '        return res[0]'
  cases:
  - input: '[1,2,3]'
    expected: '6'
  - input: '[-10,9,20,null,null,15,7]'
    expected: '42'
  worked_example:
    input: '[1,2,3]'
    steps:
    - ko: 'DFS(노드 2): 리프 노드 → leftMax=0, rightMax=0 (리셋 후) → 결과=max(1, 2+0+0)=2 → 반환 2+max(0,0)=2'
      en: 'DFS(node 2): Leaf → leftMax=0, rightMax=0 → res=max(1,2)=2 → return 2'
    - ko: 'DFS(노드 3): 리프 노드 → leftMax=0, rightMax=0 (리셋 후) → 결과=max(2, 3+0+0)=3 → 반환 3+max(0,0)=3'
      en: 'DFS(node 3): Leaf → leftMax=0, rightMax=0 → res=max(2,3)=3 → return 3'
    - ko: 'DFS(노드 1): leftMax=2, rightMax=3 → 분기 경로=1+2+3=6 → 결과=max(3, 6)=6 → 반환 1+max(2,3)=4'
      en: 'DFS(node 1): leftMax=2, rightMax=3 → branched path = 1+2+3=6 → res=6 → return 4'
    answer: '6'
solution:
  code: "# Definition for a binary tree node.\n# class TreeNode:\n#     def __init__(self, val=0, left=None, right=None):\n#         self.val = val\n#         self.left = left\n#         self.right = right\nclass Solution:\n    def maxPathSum(self, root: TreeNode) -> int:\n        res = [root.val]\n\n        # return max path sum without split\n        def dfs(root):\n            if not root:\n                return 0\n\n            leftMax = dfs(root.left)\n            rightMax = dfs(root.right)\n            leftMax = max(leftMax, 0)\n            rightMax = max(rightMax, 0)\n\n            # compute max path sum WITH split\n            res[0] = max(res[0], root.val + leftMax + rightMax)\n            return root.val + max(leftMax, rightMax)\n\n        dfs(root)\n        return res[0]\n"
  complexity:
    time: O(n)
    space: O(h) where h is the height of the tree (recursion call stack)
  followup:
  - ko: 경로가 반드시 루트를 포함해야 한다면 어떻게 수정하겠습니까?
    en: How would you modify the solution if the path must pass through the root?
  - ko: 모든 노드가 음수인 트리에서 최대 경로 합은 항상 가장 큰(가장 0에 가까운) 음수입니까?
    en: For a tree with only negative values, is the maximum path sum always the largest (least negative) single node?
  - ko: 최대 합을 가진 경로의 실제 노드들을 추적하려면 어떻게 수정하겠습니까?
    en: How would you modify the solution to return the actual nodes on the maximum-sum path?
```