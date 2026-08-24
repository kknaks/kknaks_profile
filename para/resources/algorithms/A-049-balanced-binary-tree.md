---
created: '2026-06-24'
date: '2026-06-24'
day: Day 49
difficulty: easy
id: A-049
source:
  curated_in:
  - neetcode150
  number: 110
  platform: leetcode
  slug: balanced-binary-tree
  url: https://leetcode.com/problems/balanced-binary-tree/
tags:
- tree
- depth-first-search
- binary-tree
title:
  en: Balanced Binary Tree
  ko: 균형 이진 트리
today: false
type: algorithm
updated: '2026-06-24'
visible: true
---

# 균형 이진 트리

## Data

```yaml
problem:
  title:
    ko: 균형 이진 트리
    en: Balanced Binary Tree
  statement:
    ko: '이진 트리가 주어졌을 때, 해당 트리가 높이 균형(height-balanced)을 만족하는지 판단하세요.


      높이 균형 트리는 모든 노드에서 왼쪽 부분 트리의 높이와 오른쪽 부분 트리의 높이 차이의 절댓값이 1 이하인 이진 트리입니다.'
    en: 'Given a binary tree, determine if it is height-balanced.


      A height-balanced binary tree is defined as a binary tree in which the absolute difference between the heights of the left and right subtrees of every node is at most 1.'
  constraints:
  - The number of nodes in the tree is in the range [0, 5000].
  - -10⁴ ≤ Node.val ≤ 10⁴
  io:
  - input: '[3,9,20,null,null,15,7]'
    output: 'true'
  - input: '[1,2,2,3,3,null,null,4,4]'
    output: 'false'
  - input: '[]'
    output: 'true'
clarifying:
  items:
  - q:
      ko: 높이 균형이란 무엇을 의미하나요?
      en: What does height-balanced mean?
    type: good
    why:
      ko: 문제의 핵심 정의를 이해해야 합니다. 각 노드에서 왼쪽과 오른쪽 부분 트리의 높이 차이가 1 이하여야 합니다.
      en: This is the core definition. For every node, the absolute difference between left and right subtree heights must be at most 1.
  - q:
      ko: 빈 트리는 균형 잡혀 있나요?
      en: Is an empty tree height-balanced?
    type: good
    why:
      ko: 예, 빈 트리(root = null)는 높이 균형을 만족합니다. 테스트 케이스 3에서 확인할 수 있습니다.
      en: Yes, an empty tree (root = null) is height-balanced by definition. Test case 3 confirms this.
  - q:
      ko: 단일 노드는 균형 잡혀 있나요?
      en: Is a single node height-balanced?
    type: good
    why:
      ko: 예, 단일 노드는 왼쪽/오른쪽 자식이 없어 높이 차이가 0이므로 균형을 만족합니다.
      en: Yes, a single node has no children, so the height difference is 0, which satisfies the balanced condition.
  - q:
      ko: 모든 부분 트리가 균형을 만족하면 전체 트리도 균형을 만족하나요?
      en: If all subtrees are balanced, is the whole tree balanced?
    type: good
    why:
      ko: 예, 이것이 DFS 접근의 핵심입니다. 모든 노드에서 조건을 만족하면 전체 트리가 균형을 만족합니다.
      en: Yes, this is the key insight for the DFS approach. If every node satisfies the condition, the entire tree is balanced.
  - q:
      ko: 한 번의 순회로 답을 구할 수 없고 여러 번 높이를 계산해야 하나요?
      en: Do we need to recalculate heights multiple times?
    type: distractor
    why:
      ko: 아니요, DFS에서 리턴 값으로 [균형, 높이]를 함께 반환하면 한 번의 순회로 충분합니다.
      en: No, returning both balance status and height in one pass is sufficient. Recalculating would be O(n²).
  - q:
      ko: 완전 이진 트리(complete binary tree)는 항상 균형을 만족하나요?
      en: Is a complete binary tree always height-balanced?
    type: distractor
    why:
      ko: 완전 이진 트리가 항상 높이 균형을 만족하는 것은 아닙니다. 이것은 더 약한 조건입니다.
      en: Not necessarily. A complete binary tree can have nodes where height difference exceeds 1.
approach:
  items:
  - name:
      ko: DFS (깊이 우선 탐색) - 상향식
      en: DFS (Depth-First Search) - Bottom-Up
    complexity: O(n) time / O(h) space (h = height)
    type: good
    why:
      ko: 각 노드를 한 번씩 방문하며 높이와 균형 여부를 동시에 계산합니다. 리턴 값으로 [균형, 높이]를 함께 반환하는 최적화된 방식입니다.
      en: Visit each node once, computing both height and balance status simultaneously. Return both values in one tuple for efficiency.
  - name:
      ko: DFS (깊이 우선 탐색) - 하향식
      en: DFS (Depth-First Search) - Top-Down
    complexity: O(n²) time / O(h) space
    type: distractor
    why:
      ko: 각 노드에서 높이를 매번 새로 계산하면 같은 부분 트리를 여러 번 방문하게 되어 비효율적입니다.
      en: Recalculating heights at each node leads to visiting subtrees multiple times, resulting in O(n²) complexity.
  - name:
      ko: BFS (너비 우선 탐색)
      en: BFS (Breadth-First Search)
    complexity: O(n²) time / O(n) space
    type: distractor
    why:
      ko: BFS로 각 레벨을 순회하면서 높이를 계산하면 DFS보다 복잡하고 공간 효율성이 떨어집니다.
      en: BFS with height recalculation at each level is more complex and wastes space storing entire levels.
logic:
  format: slot
  slots:
  - label:
      ko: '기저 사례: 빈 노드 확인'
      en: 'Base case: Check for null node'
    indent: 1
    options:
    - code: 'if not root:'
      type: good
      why:
        ko: 재귀의 종료 조건입니다. 빈 노드는 균형을 만족하며 높이는 0입니다.
        en: Termination condition for recursion. A null node is balanced with height 0.
    - code: 'if not root.left and not root.right:'
      type: distractor
      why:
        ko: 이것은 잎 노드(leaf node)를 확인하는 것이지, 빈 노드를 확인하는 것이 아닙니다.
        en: This checks for leaf nodes, not null nodes. Doesn't terminate recursion properly.
    - code: 'if root == None:'
      type: distractor
      why:
        ko: 기능적으로 같지만, 'not root'가 파이썬에서 더 관용적인 표현입니다.
        en: Functionally equivalent, but 'not root' is more Pythonic.
  - label:
      ko: '기저 사례: 반환값 [균형, 높이]'
      en: 'Base case: Return [balanced, height]'
    indent: 1
    options:
    - code: return [True, 0]
      type: good
      why:
        ko: 빈 노드의 기본값입니다. True는 균형을 만족, 0은 높이 0을 의미합니다.
        en: Default values for null node. True (balanced) and 0 (height).
    - code: return [True, 1]
      type: distractor
      why:
        ko: 높이가 1이면 부모 노드에서 높이를 잘못 계산합니다. 빈 노드의 높이는 0입니다.
        en: Incorrect height for null node. Null node has height 0, not 1.
    - code: return (True, 0)
      type: distractor
      why:
        ko: 리스트 대신 튜플을 반환하면 인덱싱 시 문제가 생길 수 있습니다.
        en: Tuple vs list can cause type inconsistency in indexing later.
  - label:
      ko: '재귀 호출: 왼쪽과 오른쪽 부분 트리 탐색'
      en: 'Recursive calls: Explore both subtrees'
    indent: 1
    options:
    - code: left, right = dfs(root.left), dfs(root.right)
      type: good
      why:
        ko: 각 부분 트리에 대해 DFS를 수행하여 [균형, 높이]를 얻습니다. 왼쪽과 오른쪽을 동시에 계산합니다.
        en: Recursively get balance status and height from both subtrees in one line.
    - code: left, right = dfs(root.right), dfs(root.left)
      type: distractor
      why:
        ko: 왼쪽과 오른쪽을 바꿔서 할당하므로, 이후 로직에서 오류를 초래합니다.
        en: Swaps left and right, causing incorrect balance checks.
    - code: 'if dfs(root.left) and dfs(root.right):'
      type: distractor
      why:
        ko: 리턴 값을 변수에 저장하지 않아 높이 정보를 사용할 수 없습니다.
        en: Doesn't store the returned values, losing the height information needed later.
  - label:
      ko: '균형 검증: 세 가지 조건 확인'
      en: 'Validate balance: Check three conditions'
    indent: 1
    options:
    - code: balanced = left[0] and right[0] and abs(left[1] - right[1]) <= 1
      type: good
      why:
        ko: (1) 왼쪽 부분 트리 균형, (2) 오른쪽 부분 트리 균형, (3) 높이 차이 ≤ 1. 모두 만족해야 균형입니다.
        en: 'Check: left subtree balanced AND right subtree balanced AND height difference ≤ 1.'
    - code: balanced = abs(left[1] - right[1]) <= 1
      type: distractor
      why:
        ko: 높이 차이만 확인하면, 부분 트리가 균형을 만족하지 않을 수 있습니다. 불완전한 검증입니다.
        en: Only checking height difference ignores whether subtrees themselves are balanced.
    - code: balanced = left[0] and right[0] and abs(left[1] - right[1]) < 1
      type: distractor
      why:
        ko: 부등호가 '<' 이아닌 '<=' 이어야 합니다. 높이 차이가 정확히 1인 경우도 허용됩니다.
        en: Should be '<=' not '<'. Height difference of exactly 1 is allowed.
  - label:
      ko: '현재 노드 반환: [균형, 높이 업데이트]'
      en: 'Return current node: [balanced, updated height]'
    indent: 1
    options:
    - code: return [balanced, 1 + max(left[1], right[1])]
      type: good
      why:
        ko: 높이는 자식 높이의 최댓값에 1을 더합니다. 이를 통해 부모는 정확한 높이를 알 수 있습니다.
        en: Height = 1 + max(left height, right height). Parent nodes use this to calculate their height.
    - code: return [balanced, 1 + left[1] + right[1]]
      type: distractor
      why:
        ko: 두 높이를 더하면 안 됩니다. 트리의 높이는 가장 긴 한 경로의 길이입니다.
        en: Adding both heights is wrong. Tree height is the longest path, not sum of both sides.
    - code: return [balanced, max(left[1], right[1])]
      type: distractor
      why:
        ko: 현재 노드 자신을 포함해야 하므로 +1이 필요합니다.
        en: Missing +1 for current node. Must account for this level.
  - label:
      ko: '최종 반환: 루트의 균형 여부 추출'
      en: 'Final return: Extract root''s balance status'
    indent: 0
    options:
    - code: return dfs(root)[0]
      type: good
      why:
        ko: dfs(root)은 [균형, 높이]를 반환하므로, 인덱스 [0]으로 균형 여부만 추출하여 반환합니다.
        en: dfs(root) returns [balanced, height]. Index [0] extracts only the balance boolean.
    - code: return dfs(root)[1]
      type: distractor
      why:
        ko: 높이를 반환하면 안 됩니다. 문제에서 요구하는 것은 부울 값입니다.
        en: Returns height instead of balance status. Need boolean return.
    - code: return dfs(root)
      type: distractor
      why:
        ko: '[균형, 높이] 리스트를 반환하면 안 됩니다. 함수는 부울 값을 반환해야 합니다.'
        en: Returns [balanced, height] instead of just the boolean.
trace:
  code:
  - '# Definition for a binary tree node.'
  - '# class TreeNode:'
  - '#     def __init__(self, val=0, left=None, right=None):'
  - '#         self.val = val'
  - '#         self.left = left'
  - '#         self.right = right'
  - 'class Solution:'
  - '    def isBalanced(self, root: Optional[TreeNode]) -> bool:'
  - '        def dfs(root):'
  - '            if not root:'
  - '                return [True, 0]'
  - ''
  - '            left, right = dfs(root.left), dfs(root.right)'
  - '            balanced = left[0] and right[0] and abs(left[1] - right[1]) <= 1'
  - '            return [balanced, 1 + max(left[1], right[1])]'
  - ''
  - '        return dfs(root)[0]'
  cases:
  - input: '[3,9,20,null,null,15,7]'
    expected: 'true'
  - input: '[1,2,2,3,3,null,null,4,4]'
    expected: 'false'
  - input: '[]'
    expected: 'true'
  worked_example:
    input: '[3,9,20,null,null,15,7]'
    steps:
    - ko: 루트 3에서 시작. 왼쪽 자식 9와 오른쪽 자식 20을 재귀적으로 탐색합니다.
      en: Start at root 3. Recursively explore left child (9) and right child (20).
    - ko: '노드 9: 자식이 없으므로 [True, 1] 반환 (균형 O, 높이 1)'
      en: 'Node 9: No children, returns [True, 1] (balanced, height 1)'
    - ko: '노드 20: 왼쪽 자식 15 [True, 1], 오른쪽 자식 7 [True, 1]. 높이 차이 = 0 ≤ 1 → [True, 2] 반환'
      en: 'Node 20: left child 15 [True, 1], right child 7 [True, 1]. Height diff = 0 ≤ 1 → returns [True, 2]'
    - ko: '루트 3: 왼쪽 [True, 1], 오른쪽 [True, 2]. 높이 차이 = 1 ≤ 1, 모두 균형 O → True'
      en: 'Root 3: left [True, 1], right [True, 2]. Height diff = 1 ≤ 1, both balanced → True'
    answer: 'true'
solution:
  code: "# Definition for a binary tree node.\n# class TreeNode:\n#     def __init__(self, val=0, left=None, right=None):\n#         self.val = val\n#         self.left = left\n#         self.right = right\nclass Solution:\n    def isBalanced(self, root: Optional[TreeNode]) -> bool:\n        def dfs(root):\n            if not root:\n                return [True, 0]\n\n            left, right = dfs(root.left), dfs(root.right)\n            balanced = left[0] and right[0] and abs(left[1] - right[1]) <= 1\n            return [balanced, 1 + max(left[1], right[1])]\n\n        return dfs(root)[0]\n"
  complexity:
    time: O(n)
    space: O(h) where h = tree height
  followup:
  - ko: 균형이 깨진 첫 번째 노드를 찾으세요. 균형이 깨진 노드가 있으면 해당 노드의 값을, 없으면 -1을 반환하세요.
    en: Find the first unbalanced node. Return its value, or -1 if the tree is balanced.
  - ko: n개의 노드를 가진 균형 이진 트리의 최소 높이와 최대 높이는 각각 무엇인가요?
    en: What are the minimum and maximum possible heights for a balanced tree with n nodes?
  - ko: 트리를 회전(rotation)을 통해 균형 잡힌 트리로 변환할 수 있나요? (AVL 트리와의 유사성)
    en: How would you modify an unbalanced tree to make it balanced using rotations? (Similar to AVL tree)
```