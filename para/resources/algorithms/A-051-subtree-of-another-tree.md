---
created: '2026-06-26'
date: '2026-06-26'
day: Day 51
difficulty: easy
id: A-051
source:
  curated_in:
  - neetcode150
  number: 572
  platform: leetcode
  slug: subtree-of-another-tree
  url: https://leetcode.com/problems/subtree-of-another-tree/
tags:
- tree
- depth-first-search
- string-matching
- binary-tree
- hash-function
title:
  en: Subtree of Another Tree
  ko: 다른 트리의 부분트리
today: false
type: algorithm
updated: '2026-06-26'
visible: true
---

# 다른 트리의 부분트리

## Data

```yaml
problem:
  title:
    ko: 다른 트리의 부분트리
    en: Subtree of Another Tree
  statement:
    ko: '두 개의 이진 트리의 루트 root와 subRoot가 주어질 때, root의 부분트리 중에 subRoot와 같은 구조와 노드 값을 가진 트리가 있으면 true를, 그렇지 않으면 false를 반환합니다.


      이진 트리 tree의 부분트리는 tree의 한 노드와 그 노드의 모든 자손으로 이루어진 트리입니다. tree 자신도 tree의 부분트리로 간주될 수 있습니다.'
    en: 'Given the roots of two binary trees root and subRoot, return true if there is a subtree of root with the same structure and node values of subRoot and false otherwise.


      A subtree of a binary tree tree is a tree that consists of a node in tree and all of this node''s descendants. The tree tree could also be considered as a subtree of itself.'
  constraints:
  - 1 ≤ nodes in root ≤ 2000
  - 1 ≤ nodes in subRoot ≤ 1000
  - -10^4 ≤ node values ≤ 10^4
  io:
  - input: '[3,4,5,1,2]

      [4,1,2]'
    output: 'true'
  - input: '[3,4,5,1,2,null,null,null,null,0]

      [4,1,2]'
    output: 'false'
clarifying:
  items:
  - q:
      ko: subRoot가 null이면 true를 반환해야 할까?
      en: If subRoot is null, should we return true?
    type: good
    why:
      ko: 네. 공 트리는 정의상 모든 트리의 부분트리이므로, null subRoot는 항상 true를 반환합니다.
      en: Yes. The empty tree is a valid subtree of any tree by definition, so null subRoot always returns true.
  - q:
      ko: 부분트리가 메인 트리의 루트에서 시작해야 할까?
      en: Does the subtree need to start at the root of the main tree?
    type: good
    why:
      ko: 아니요. 부분트리는 어떤 노드에서든 시작할 수 있으며, root의 모든 노드에서 subRoot와의 일치 여부를 확인합니다.
      en: No. A subtree can start at any node; we search every node in root to find a match with subRoot.
  - q:
      ko: root = [4,1,2]이고 subRoot = [4,1,2]이면, subRoot는 root의 부분트리인가?
      en: If root = [4,1,2] and subRoot = [4,1,2], is subRoot a subtree of root?
    type: good
    why:
      ko: 네. 트리는 자기 자신을 부분트리로 간주합니다. 구조와 값이 모두 동일합니다.
      en: Yes. A tree is always considered a subtree of itself. Both the structure and values are identical.
  - q:
      ko: 값이 1과 2를 포함하면 [1,2]는 [4,1,2]의 부분트리인가?
      en: Is [1,2] a subtree of [4,1,2] if both contain values 1 and 2?
    type: distractor
    why:
      ko: 아니요. 값만 아니라 구조도 정확히 일치해야 합니다. [1,2]의 구조는 [4,1,2]의 어떤 부분트리와도 다릅니다.
      en: No. Structure must match exactly, not just values. [1,2] represents a different parent-child structure than any subtree in [4,1,2].
  - q:
      ko: root.val == subRoot.val 확인만 충분한가?
      en: Is it enough to check if root.val == subRoot.val for the root node?
    type: distractor
    why:
      ko: 아니요. 모든 자손이 값과 구조에서 재귀적으로 일치해야 합니다.
      en: No. We must also verify that all descendants have matching values and structure recursively.
  - q:
      ko: root에서 subRoot의 값이 어떤 순서로든 나타나면 찾을 수 있을까?
      en: Can we find subRoot by checking if its values appear in root in any order?
    type: distractor
    why:
      ko: 아니요. 정확한 트리 구조가 중요합니다. 부분트리는 올바른 값을 포함할 뿐만 아니라 동일한 부모-자식 관계에서 나타나야 합니다.
      en: No. The exact tree structure matters. A subtree requires both the correct values and the exact same parent-child relationships.
approach:
  items:
  - name:
      ko: 재귀적 DFS와 트리 비교
      en: Recursive DFS with Tree Comparison
    complexity: O(m*n) time / O(h) space
    type: good
    why:
      ko: root의 각 노드에서 시작하는 부분트리가 subRoot와 일치하는지 재귀적으로 확인합니다. 명확하고 직관적이며 모든 엣지 케이스를 우아하게 처리합니다.
      en: For each node in root, we check if the subtree rooted there matches subRoot using a recursive tree comparison. This is clean, intuitive, and handles all edge cases elegantly.
  - name:
      ko: 직렬화 및 문자열 패턴 매칭
      en: Serialization & String Pattern Matching
    complexity: O(m + n) time / O(m + n) space
    type: distractor
    why:
      ko: 두 트리를 문자열로 직렬화한 후 KMP 또는 Z-알고리즘으로 패턴을 매칭할 수 있습니다. 이론적으로 더 빠르지만 이 제약 조건에서는 과도하며, null 노드 처리 오류가 발생하기 쉽습니다.
      en: You could serialize both trees into strings and use KMP or Z-algorithm for pattern matching. While theoretically faster, it's overengineered for these constraints and prone to implementation errors.
  - name:
      ko: 해시 기반 부분트리 식별
      en: Hash-based Subtree Identification
    complexity: O(m + n) time / O(m + n) space
    type: distractor
    why:
      ko: 두 트리의 모든 부분트리에 대해 해시 값을 미리 계산한 후 매칭합니다. 점근적으로 더 빠르지만 충돌 회피를 위해 신중한 해시 함수 설계가 필요하므로 오류가 발생하기 쉽습니다.
      en: Precompute hash values for every subtree in both trees, then match hashes. This is faster asymptotically but requires careful hash function design to avoid collisions, making it error-prone.
  - name:
      ko: 스택을 사용한 반복적 순회
      en: Iterative Traversal with Explicit Stack
    complexity: O(m*n) time / O(m + n) space
    type: distractor
    why:
      ko: 재귀 대신 명시적 스택으로 root를 순회하며 각 노드를 확인합니다. 재귀 깊이 문제를 피하지만 직관성이 낮고 전체 복잡도는 개선되지 않습니다.
      en: Instead of recursion, use an explicit stack to traverse root and check each node. While it avoids recursion depth issues, it's less intuitive and doesn't improve overall complexity.
logic:
  format: slot
  slots:
  - label:
      ko: 빈 subRoot 확인
      en: Empty subRoot check
    indent: 0
    options:
    - code: 'if not subRoot:'
      type: good
      why:
        ko: subRoot가 null이면 공 트리는 모든 트리의 부분트리이므로 즉시 true를 반환합니다.
        en: If subRoot is null, the empty tree is a trivial subtree of any tree, so return true immediately.
    - code: 'if subRoot: return True'
      type: distractor
      why:
        ko: 논리가 반전되었습니다. subRoot가 null이 아닐 때만 true를 반환합니다.
        en: Logic is inverted; this would return true only when subRoot is NOT null.
    - code: 'if not subRoot: pass'
      type: distractor
      why:
        ko: pass는 아무것도 반환하지 않습니다. 공 부분트리에 대해 true를 반환해야 합니다.
        en: Pass doesn't return anything; we need to return true for the empty subtree.
  - label:
      ko: 빈 root 확인
      en: Empty root check
    indent: 0
    options:
    - code: 'if not root:'
      type: good
      why:
        ko: root가 null이지만 subRoot는 null이 아니면, 부분트리를 찾을 수 없으므로 false를 반환합니다.
        en: If root is exhausted but subRoot isn't, the subtree cannot exist, so return false.
    - code: 'if not root: return True'
      type: distractor
      why:
        ko: 잘못된 반환값입니다. null 트리는 null이 아닌 부분트리를 포함할 수 없습니다.
        en: Wrong return value; a null tree cannot contain a non-null subtree.
    - code: 'if root and not subRoot: return False'
      type: distractor
      why:
        ko: 불필요한 조건입니다. 이 지점에서 subRoot가 null이 아님을 이미 알고 있습니다.
        en: Unnecessary condition; we already know subRoot is non-null at this point.
  - label:
      ko: 현재 노드의 부분트리 비교
      en: Check if current subtree matches
    indent: 0
    options:
    - code: 'if self.isSameTree(root, subRoot):'
      type: good
      why:
        ko: isSameTree를 사용하여 현재 노드를 루트로 하는 전체 트리가 subRoot와 동일한지 확인합니다.
        en: Use isSameTree to verify that the subtree rooted at the current node has the same structure and values as subRoot.
    - code: 'if root.val == subRoot.val:'
      type: distractor
      why:
        ko: 루트 값만 확인합니다. 구조와 자손은 확인하지 않습니다.
        en: Only checks the root value, ignoring structure and descendants.
    - code: 'if self.isSubtree(root, subRoot):'
      type: distractor
      why:
        ko: 무한 재귀가 발생합니다. 이미 isSubtree 함수 내부에 있습니다.
        en: Would cause infinite recursion since we're already inside isSubtree.
  - label:
      ko: 왼쪽과 오른쪽 부분트리 재귀 탐색
      en: Recursively search left and right children
    indent: 0
    options:
    - code: return self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot)
      type: good
      why:
        ko: 현재 노드에서 일치가 없으면, OR을 사용하여 왼쪽 자식과 오른쪽 자식 중 하나에서 subRoot를 찾을 수 있는지 확인합니다.
        en: If no match at the current node, use OR to check if subRoot is a subtree of either the left child or the right child.
    - code: return self.isSubtree(root.left, subRoot) and self.isSubtree(root.right, subRoot)
      type: distractor
      why:
        ko: AND 논리는 양쪽 자식에서 모두 찾아야 한다는 뜻입니다. 하나의 자식에서만 찾으면 됩니다.
        en: AND logic would require subRoot to be in BOTH children, but it should be in EITHER child.
    - code: return self.isSubtree(root, subRoot.left) or self.isSubtree(root, subRoot.right)
      type: distractor
      why:
        ko: 매개변수가 바뀌었습니다. 이것은 subRoot의 부분트리가 root에 있는지 확인하는 것으로, 문제의 반대입니다.
        en: Parameters are swapped; this checks if a subtree of subRoot exists in root, not the other way around.
trace:
  code:
  - '# Definition for a binary tree node.'
  - '# class TreeNode:'
  - '#     def __init__(self, val=0, left=None, right=None):'
  - '#         self.val = val'
  - '#         self.left = left'
  - '#         self.right = right'
  - 'class Solution:'
  - '    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:'
  - '        if not subRoot:'
  - '            return True'
  - '        if not root:'
  - '            return False'
  - ''
  - '        if self.isSameTree(root, subRoot):'
  - '            return True'
  - '        return self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot)'
  - ''
  - '    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:'
  - '        if not p and not q:'
  - '            return True'
  - '        if p and q and p.val == q.val:'
  - '            return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)'
  - '        else:'
  - '            return False'
  cases:
  - input: '[3,4,5,1,2]

      [4,1,2]'
    expected: 'true'
  - input: '[3,4,5,1,2,null,null,null,null,0]

      [4,1,2]'
    expected: 'false'
  worked_example:
    input: '[3,4,5,1,2]

      [4,1,2]'
    steps:
    - ko: '루트 3에서 시작: isSameTree(3, 4)는 3 ≠ 4이므로 실패; 왼쪽 부분트리 확인.'
      en: 'At root 3: isSameTree(3, 4) fails because 3 ≠ 4; check left subtree.'
    - ko: '노드 4에서: isSameTree 비교 시작; 루트 값이 일치합니다 (4 == 4).'
      en: 'At node 4: isSameTree begins; root values match (4 == 4).'
    - ko: '자식들을 재귀적으로 확인: 왼쪽 (1 == 1), 오른쪽 (2 == 2) → isSameTree는 true 반환.'
      en: 'Recursively verify children: left (1 == 1), right (2 == 2) → isSameTree returns true.'
    - ko: true를 반환합니다.
      en: Return true.
    answer: 'true'
solution:
  code: "# Definition for a binary tree node.\n# class TreeNode:\n#     def __init__(self, val=0, left=None, right=None):\n#         self.val = val\n#         self.left = left\n#         self.right = right\nclass Solution:\n    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:\n        if not subRoot:\n            return True\n        if not root:\n            return False\n\n        if self.isSameTree(root, subRoot):\n            return True\n        return self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot)\n\n    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:\n        if not p and not q:\n            return True\n        if p and q and p.val == q.val:\n            return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)\n        else:\n            return False\n"
  complexity:
    time: O(m*n) where m = nodes in root, n = nodes in subRoot
    space: O(h) where h = maximum height of root and subRoot
  followup:
  - ko: 같은 root에서 여러 subRoot 쿼리가 있다면 어떻게 최적화할까요? 전처리 단계가 도움이 될까요?
    en: How would you optimize if you had multiple subRoot queries on the same root? What preprocessing could help?
  - ko: 큐나 스택을 사용한 반복적(iterative) 구현이 가능할까요?
    en: Can you implement this iteratively using a queue or stack?
  - ko: 트리를 문자열로 직렬화하는 방법이 이 문제를 푸는 데 어떻게 도움이 될까요?
    en: How could serialization (converting trees to strings) help solve this problem?
```