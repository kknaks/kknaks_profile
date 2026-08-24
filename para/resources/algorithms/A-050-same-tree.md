---
created: '2026-06-25'
date: '2026-06-25'
day: Day 50
difficulty: easy
id: A-050
source:
  curated_in:
  - neetcode150
  number: 100
  platform: leetcode
  slug: same-tree
  url: https://leetcode.com/problems/same-tree/
tags:
- tree
- depth-first-search
- breadth-first-search
- binary-tree
title:
  en: Same Tree
  ko: 같은 트리
today: false
type: algorithm
updated: '2026-06-25'
visible: true
---

# 같은 트리

## Data

```yaml
problem:
  title:
    ko: 같은 트리
    en: Same Tree
  statement:
    ko: '두 이진 트리의 루트 p와 q가 주어질 때, 두 트리가 동일한지 확인하는 함수를 작성하세요.


      두 이진 트리가 같다고 간주되려면 구조적으로 동일하고 노드의 값이 모두 같아야 합니다.'
    en: 'Given the roots of two binary trees p and q, write a function to check if they are the same or not.


      Two binary trees are considered the same if they are structurally identical, and the nodes have the same value.'
  constraints:
  - The number of nodes in both trees is in the range [0, 100]
  - -10⁴ ≤ Node.val ≤ 10⁴
  io:
  - input: '[1,2,3]

      [1,2,3]'
    output: 'true'
  - input: '[1,2]

      [1,null,2]'
    output: 'false'
  - input: '[1,2,1]

      [1,1,2]'
    output: 'false'
clarifying:
  items:
  - q:
      ko: 두 트리가 모두 비어있으면 같다고 봐야 하나요?
      en: If both trees are empty, should we return true?
    type: good
    why:
      ko: 두 개의 빈 트리는 구조가 같고 값도 같으므로 true를 반환해야 합니다.
      en: Two empty trees have identical structure and values, so they should be considered the same.
  - q:
      ko: 한 트리는 null이고 다른 트리는 노드가 있으면 어떻게 되나요?
      en: What if one tree is empty and the other has nodes?
    type: good
    why:
      ko: 구조가 다르므로 false를 반환해야 합니다. 두 트리는 구조적으로 동일해야 같습니다.
      en: They have different structures, so we should return false. Both structure and values must match.
  - q:
      ko: 노드의 값이 같아도 좌우 자식의 위치가 다르면 같은 트리인가요?
      en: If node values are the same but left and right children are swapped, are they the same tree?
    type: good
    why:
      ko: 아니요. 구조가 다르므로 다른 트리입니다. 각 위치의 노드가 정확히 같아야 합니다.
      en: No, they are different because the structure differs. Nodes in each position must match exactly.
  - q:
      ko: 반복적인 방법(iterative)으로 해결할 수 있나요?
      en: Can we solve this using an iterative approach?
    type: good
    why:
      ko: 네, 큐를 사용한 너비 우선 탐색으로도 해결 가능합니다.
      en: Yes, we can use BFS with a queue to compare nodes level by level.
  - q:
      ko: 두 트리를 문자열로 직렬화하고 비교할 수 있나요?
      en: Can we serialize both trees to strings and compare them?
    type: distractor
    why:
      ko: 기술적으로는 가능하지만, 여러 다른 트리가 같은 문자열을 만들 수 있어 실제로는 작동하지 않습니다.
      en: While possible, different tree structures can produce the same serialization, making this approach unreliable.
  - q:
      ko: 중순 순회(inorder traversal) 결과만 비교하면 충분한가요?
      en: Is comparing inorder traversals sufficient?
    type: distractor
    why:
      ko: 아니요. 구조가 다른 두 트리가 같은 중순 순회 결과를 가질 수 있습니다.
      en: No, two structurally different trees can have the same inorder traversal.
approach:
  items:
  - name:
      ko: 재귀 깊이 우선 탐색
      en: Recursive DFS
    complexity: O(min(n, m)) time / O(min(h₁, h₂)) space
    type: good
    why:
      ko: 각 노드를 한 번씩 방문하고, 재귀 스택은 트리의 높이만큼 필요합니다.
      en: Each node is visited once, and recursion stack depth is bounded by tree height.
  - name:
      ko: 반복적 너비 우선 탐색 (큐)
      en: Iterative BFS with Queue
    complexity: O(min(n, m)) time / O(min(n, m)) space
    type: good
    why:
      ko: 큐를 사용하여 레벨 별로 노드를 비교합니다. 스택 오버플로우 걱정이 없습니다.
      en: Compare nodes level by level using a queue. No recursion depth issues.
  - name:
      ko: 전위 순회 직렬화 비교
      en: Preorder Traversal Serialization
    complexity: O(n + m) time / O(n + m) space
    type: distractor
    why:
      ko: 구조 정보를 충분히 담지 못하므로 false positive가 발생할 수 있습니다.
      en: May not capture enough structure information, leading to false positives.
  - name:
      ko: 값 비교만
      en: Value-only Comparison
    complexity: O(n) time / O(h) space
    type: distractor
    why:
      ko: 구조를 비교하지 않기 때문에 구조가 다른 두 트리를 같다고 판정할 수 있습니다.
      en: Ignores structure, so it would incorrectly match trees with different structures.
logic:
  format: slot
  slots:
  - label:
      ko: '기저 사례: 두 노드 모두 null'
      en: 'Base case: both nodes are null'
    indent: 0
    options:
    - code: 'if not p and not q:'
      type: good
      why:
        ko: 두 트리가 모두 비어있으면 구조와 값이 모두 같으므로 true를 반환할 조건입니다.
        en: When both trees are empty, they are identical in both structure and values.
    - code: 'if not p or not q:'
      type: distractor
      why:
        ko: 또는(or) 연산자를 사용하면 한쪽만 null일 때도 true가 되어 잘못된 결과입니다.
        en: Using 'or' would return true when only one is null, which is incorrect.
    - code: 'if p is None and q is None:'
      type: distractor
      why:
        ko: 논리는 맞지만, 파이썬에서 None 체크는 'not'을 사용하는 것이 관례입니다.
        en: Logically correct, but using 'not' is more Pythonic for None checks.
  - label:
      ko: 기저 사례 반환값
      en: Return true for base case
    indent: 1
    options:
    - code: return True
      type: good
      why:
        ko: 두 노드가 모두 null이면 구조와 값이 같으므로 true를 반환합니다.
        en: Both trees being empty means they have the same structure and values.
    - code: return False
      type: distractor
      why:
        ko: 기저 사례에서 false를 반환하면 모든 빈 트리 쌍이 다르다고 판정되므로 잘못된 답입니다.
        en: Returning false would incorrectly consider all empty tree pairs as different.
    - code: continue
      type: distractor
      why:
        ko: continue는 여기서 사용할 수 없고, 재귀 함수에서는 반환값이 필요합니다.
        en: '''continue'' cannot be used in a recursive function; we must return a value.'
  - label:
      ko: '재귀 조건: 두 노드 모두 존재하고 값이 같음'
      en: 'Recursive condition: both nodes exist and have equal values'
    indent: 0
    options:
    - code: 'if p and q and p.val == q.val:'
      type: good
      why:
        ko: 재귀를 계속하려면 두 노드가 모두 존재하고 값이 같아야 합니다. 하나라도 거짓이면 재귀할 이유가 없습니다.
        en: We only recurse if both nodes exist and their values match. Otherwise, comparison fails.
    - code: 'if p or q and p.val == q.val:'
      type: distractor
      why:
        ko: 연산자 우선순위로 인해 잘못 해석되며, 한쪽이 null일 때도 진행될 수 있습니다.
        en: Operator precedence causes incorrect evaluation; would proceed when one node is null.
    - code: 'if p and q and p.val != q.val:'
      type: distractor
      why:
        ko: 부등호를 사용하면 값이 다를 때 재귀하므로 논리가 반대입니다.
        en: Using '!=' reverses the logic; we should recurse when values are equal, not when they differ.
    - code: 'if p and q:'
      type: distractor
      why:
        ko: 노드의 값을 확인하지 않으므로, 값이 다른 경우에도 자식 노드를 계속 확인하게 됩니다.
        en: Skipping the value check means we'd continue comparing children even when values differ.
  - label:
      ko: '재귀 호출: 좌우 부분 트리 비교'
      en: 'Recursive call: compare left and right subtrees'
    indent: 1
    options:
    - code: return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
      type: good
      why:
        ko: 현재 노드가 같으므로, 좌측과 우측 자식도 같은지 재귀적으로 비교합니다. 모두 같아야 true를 반환합니다.
        en: Since current nodes match, we recursively check if both left and right subtrees are identical.
    - code: return self.isSameTree(p.left, q.right) and self.isSameTree(p.right, q.left)
      type: distractor
      why:
        ko: 좌우를 교차하여 비교하므로 구조가 정반대일 때만 true가 되어 잘못된 답입니다.
        en: Swapping left and right only matches mirror images, not identical structures.
    - code: return self.isSameTree(p.left, q.left) or self.isSameTree(p.right, q.right)
      type: distractor
      why:
        ko: 또는(or)을 사용하면 한쪽 부분 트리만 같아도 true가 되어 잘못된 결과입니다.
        en: Using 'or' would return true if only one side matches, but both must match.
    - code: return self.isSameTree(p, q)
      type: distractor
      why:
        ko: 자식 노드를 비교하지 않고 같은 노드를 다시 비교하므로 무한 재귀에 빠집니다.
        en: Comparing the same nodes again causes infinite recursion.
  - label:
      ko: '불일치 경우: false 반환'
      en: 'Mismatch case: return false'
    indent: 0
    options:
    - code: 'else:'
      type: good
      why:
        ko: 위의 두 조건을 만족하지 않으면 (한쪽이 null이거나 값이 다르면) 트리가 다르므로 false를 반환합니다.
        en: If neither base case nor recursive case applies, the trees differ, so return false.
    - code: 'else: return True'
      type: distractor
      why:
        ko: 불일치할 때 true를 반환하면 다른 트리를 같다고 판정하므로 잘못된 답입니다.
        en: Returning true would incorrectly mark different trees as identical.
    - code: 'else: return self.isSameTree(p.right, q.right)'
      type: distractor
      why:
        ko: 우측 부분 트리만 비교하면 좌측 부분 트리의 차이를 놓칠 수 있습니다.
        en: Only checking one side would miss differences in the other side.
trace:
  code:
  - '# Definition for a binary tree node.'
  - '# class TreeNode:'
  - '#     def __init__(self, x):'
  - '#         self.val = x'
  - '#         self.left = None'
  - '#         self.right = None'
  - ''
  - ''
  - 'class Solution:'
  - '    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:'
  - '        if not p and not q:'
  - '            return True'
  - '        if p and q and p.val == q.val:'
  - '            return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)'
  - '        else:'
  - '            return False'
  cases:
  - input: '[1,2,3]

      [1,2,3]'
    expected: 'true'
  - input: '[1,2]

      [1,null,2]'
    expected: 'false'
  - input: '[1,2,1]

      [1,1,2]'
    expected: 'false'
  worked_example:
    input: '[1,2,3]

      [1,2,3]'
    steps:
    - ko: p = [1,2,3], q = [1,2,3] 비교 시작
      en: Start comparing p=[1,2,3] with q=[1,2,3]
    - ko: p와 q 모두 null이 아니고, 값이 1로 같음 → 자식 노드 재귀 비교
      en: Both p and q exist with value 1 → recurse on children
    - ko: '좌측: (2,2) 값이 같음, 우측: (3,3) 값이 같음 → 모두 재귀 계속'
      en: Left subtrees (2,2) match, right subtrees (3,3) match → continue recursion
    - ko: 모든 노드에서 재귀 기저 사례 (둘 다 null)에 도달 → 모두 true 반환
      en: All branches eventually reach base case (both null) → all return true
    answer: 'true'
solution:
  code: "# Definition for a binary tree node.\n# class TreeNode:\n#     def __init__(self, x):\n#         self.val = x\n#         self.left = None\n#         self.right = None\n\n\nclass Solution:\n    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:\n        if not p and not q:\n            return True\n        if p and q and p.val == q.val:\n            return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)\n        else:\n            return False\n"
  complexity:
    time: O(min(n, m))
    space: O(min(h₁, h₂))
  followup:
  - ko: 반복적 방법으로 해결할 수 있나요? (큐 또는 스택 사용)
    en: Can you solve this iteratively using a queue or stack?
  - ko: 세 개 이상의 트리를 비교하려면 어떻게 할까요?
    en: How would you extend this to compare three or more trees?
  - ko: 매우 큰 트리에서 성능을 최적화할 방법이 있을까요?
    en: How could you optimize for comparing very large trees?
```