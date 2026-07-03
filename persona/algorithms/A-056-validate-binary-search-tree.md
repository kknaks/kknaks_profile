---
created: '2026-07-02'
date: '2026-07-02'
day: Day 56
difficulty: medium
id: A-056
source:
  curated_in:
  - neetcode150
  number: 98
  platform: leetcode
  slug: validate-binary-search-tree
  url: https://leetcode.com/problems/validate-binary-search-tree/
status: draft
tags:
- tree
- depth-first-search
- binary-search-tree
- binary-tree
title:
  en: Validate Binary Search Tree
  ko: 이진 탐색 트리 검증
today: false
type: algorithm
updated: '2026-07-02'
visible: true
---

# 이진 탐색 트리 검증

## Data

```yaml
problem:
  title:
    ko: 이진 탐색 트리 검증
    en: Validate Binary Search Tree
  statement:
    ko: '이진 트리의 루트가 주어졌을 때, 이것이 유효한 이진 탐색 트리(BST)인지 판단하세요.


      유효한 BST는 다음과 같이 정의됩니다:

      - 노드의 왼쪽 서브트리는 노드의 키보다 작은 키를 가진 노드들만 포함합니다.

      - 노드의 오른쪽 서브트리는 노드의 키보다 큰 키를 가진 노드들만 포함합니다.

      - 왼쪽 서브트리와 오른쪽 서브트리도 모두 이진 탐색 트리여야 합니다.'
    en: 'Given the root of a binary tree, determine if it is a valid binary search tree (BST).


      A valid BST is defined as follows:

      - The left subtree of a node contains only nodes with keys strictly less than the node''s key.

      - The right subtree of a node contains only nodes with keys strictly greater than the node''s key.

      - Both the left and right subtrees must also be binary search trees.'
  constraints:
  - 1 ≤ number of nodes ≤ 10⁴
  - -2³¹ ≤ Node.val ≤ 2³¹ - 1
  io:
  - input: '[2,1,3]'
    output: 'true'
  - input: '[5,1,4,null,null,3,6]'
    output: 'false'
clarifying:
  items:
  - q:
      ko: 엄격한 부등호(< 및 >)는 중복값이 허용되지 않는다는 의미인가요?
      en: Does 'strictly less than' and 'strictly greater than' mean duplicate values are not allowed?
    type: good
    why:
      ko: 맞습니다. 엄격한 부등호는 중복값을 명시적으로 배제합니다.
      en: Yes. Strict inequalities explicitly exclude duplicate values.
  - q:
      ko: 왼쪽 서브트리 전체가 조건을 만족해야 하나요, 아니면 직접 자식만 확인하면 되나요?
      en: Must the entire left subtree satisfy the condition, or just the immediate left child?
    type: good
    why:
      ko: 전체 왼쪽 서브트리가 조건을 만족해야 합니다. 이는 재귀적으로 검증됩니다.
      en: The entire left subtree must satisfy the condition, which is verified recursively.
  - q:
      ko: 트리가 비어있거나 노드가 하나만 있으면 유효한 BST로 간주되나요?
      en: Should an empty tree or a single-node tree be considered valid?
    type: good
    why:
      ko: 네, 공 노드와 단일 노드는 모두 유효한 BST입니다.
      en: Yes, empty nodes and single-node trees are valid BSTs.
  - q:
      ko: 음수 값을 가진 노드도 검증할 수 있나요?
      en: Can we handle nodes with negative values?
    type: good
    why:
      ko: 네. 제약 조건에서 노드 값은 -2³¹부터 2³¹-1까지이므로 음수도 포함됩니다.
      en: Yes. Constraints allow values from -2³¹ to 2³¹-1, including negatives.
  - q:
      ko: 검증 중에 트리의 구조를 수정할 수 있나요?
      en: Can we modify the tree structure during validation?
    type: distractor
    why:
      ko: 아니요. 우리는 트리를 단지 검증만 하므로 구조를 변경하지 않습니다.
      en: No. We only validate the tree without modifying its structure.
  - q:
      ko: 검증 결과로 유효하지 않은 노드의 목록을 반환해야 하나요?
      en: Should we return a list of invalid nodes?
    type: distractor
    why:
      ko: 아니요. 우리는 단순히 트리가 유효한 BST인지 여부를 나타내는 불린값을 반환합니다.
      en: No. We simply return a boolean indicating whether the tree is a valid BST.
  - q:
      ko: 범위(left, right)가 가능한 모든 값을 포함해야 하나요?
      en: Should the range (left, right) account for all possible node values?
    type: good
    why:
      ko: 예, 초기 범위는 -무한대에서 +무한대로 설정하여 모든 가능한 값을 포함합니다.
      en: Yes, initial range is -infinity to +infinity to include all possible values.
  - q:
      ko: 트리의 높이를 계산해야 하나요?
      en: Do we need to calculate the height of the tree?
    type: distractor
    why:
      ko: 아니요. 검증만 필요하므로 높이 계산은 필요하지 않습니다.
      en: No. We only need validation, not height calculation.
approach:
  items:
  - name:
      ko: 범위 기반 DFS (권장)
      en: Range-based DFS (Recommended)
    complexity: O(n) time / O(h) space
    type: good
    why:
      ko: 각 재귀 호출에서 유효한 범위를 추적하므로, 모든 조상의 제약을 자동으로 고려합니다.
      en: Track valid range for each recursive call, automatically respecting all ancestor constraints.
  - name:
      ko: 중위 순회
      en: In-order Traversal
    complexity: O(n) time / O(h) space
    type: good
    why:
      ko: 유효한 BST의 중위 순회는 엄격히 증가하는 수열을 생성합니다.
      en: Valid BST's in-order traversal produces strictly increasing sequence.
  - name:
      ko: 직접 자식만 비교 (잘못된 접근)
      en: Immediate Children Comparison Only
    complexity: O(n) time / O(h) space
    type: distractor
    why:
      ko: '각 노드의 직접 자식만 비교하면, 더 깊은 서브트리의 위반을 놓칠 수 있습니다. 예: [5,1,4,null,null,3,6]에서 3은 오른쪽 서브트리에 있지만 5보다 작습니다.'
      en: Checking only immediate children misses violations in deeper subtrees. E.g., in [5,1,4,null,null,3,6], value 3 in right subtree violates BST.
  - name:
      ko: 전역 Min/Max 추적
      en: Global Min/Max Tracking
    complexity: O(n) time / O(h) space
    type: distractor
    why:
      ko: 전역 변수로 최소/최대값을 추적하면, 병렬 재귀 호출에서 상태가 충돌할 수 있습니다.
      en: Global min/max variables cause state conflicts in parallel recursive calls.
  - name:
      ko: 정렬된 배열과 비교
      en: Sorted Array Comparison
    complexity: O(n log n) time / O(n) space
    type: distractor
    why:
      ko: 정렬 비교도 가능하지만, 정렬에 O(n log n)이 필요하므로 비효율적입니다.
      en: While possible, sorting requires O(n log n), making it unnecessarily inefficient.
logic:
  format: slot
  slots:
  - label:
      ko: 헬퍼 함수 정의
      en: Define helper function
    indent: 0
    options:
    - code: 'def valid(node, left, right):'
      type: good
      why:
        ko: 좌우 경계값을 추적하기 위해 추가 매개변수를 가진 헬퍼 함수를 정의합니다.
        en: Define a helper with additional parameters to track left and right boundaries.
    - code: 'def isValid(node):'
      type: distractor
      why:
        ko: 경계 정보 없이는 각 노드가 유효한 범위에 있는지 검증할 수 없습니다.
        en: Without boundary info, we cannot determine if nodes are within valid ranges.
    - code: 'def check(node, limit):'
      type: distractor
      why:
        ko: 상한과 하한을 모두 추적해야 하므로, 하나의 매개변수로는 부족합니다.
        en: We need both upper and lower bounds, so a single parameter is insufficient.
  - label:
      ko: '기저 케이스: 공 노드 처리'
      en: 'Base case: empty node'
    indent: 1
    options:
    - code: return True
      type: good
      why:
        ko: 공 노드는 유효한 BST이므로 true를 반환합니다.
        en: Empty nodes are valid BSTs, so return true.
    - code: return False
      type: distractor
      why:
        ko: 공 노드가 거짓이면 모든 리프 노드가 거짓이 되어 모든 트리가 무효합니다.
        en: If empty is false, all leaf nodes fail, making all trees invalid.
    - code: return node is not None
      type: distractor
      why:
        ko: 이것은 거짓(None)을 반환하므로, 기저 케이스 처리가 잘못됩니다.
        en: This returns false for empty nodes, breaking base case logic.
  - label:
      ko: 현재 노드 범위 검증
      en: Validate current node in range
    indent: 1
    options:
    - code: 'if not (left < node.val < right):'
      type: good
      why:
        ko: 노드 값이 할당된 범위(left < node.val < right)를 만족하지 않으면 false를 반환합니다.
        en: Return false if node value doesn't satisfy strict bounds left < value < right.
    - code: 'if not (left <= node.val <= right):'
      type: distractor
      why:
        ko: ≤/≥를 사용하면 중복값을 허용하게 되어, 엄격한 부등호 조건을 위반합니다.
        en: Using ≤/≥ allows duplicates, violating the strict inequality requirement.
    - code: 'if node.val < left and node.val > right:'
      type: distractor
      why:
        ko: AND 연산자는 항상 거짓입니다. OR을 사용해야 합니다.
        en: AND operator is always false. Should use OR for correct logic.
  - label:
      ko: 왼쪽 서브트리 검증
      en: Validate left subtree
    indent: 1
    options:
    - code: return valid(node.left, left, node.val) and valid(
      type: good
      why:
        ko: 왼쪽 자식은 현재 값보다 작아야 하므로, 상한(upper bound)을 현재 노드의 값으로 업데이트합니다.
        en: Left subtree must be smaller, so update upper bound to current node's value.
    - code: valid(node.left, left, node.left)
      type: distractor
      why:
        ko: 상한을 노드의 왼쪽 자식값으로 설정하면, 더 깊은 노드들이 부정확하게 제한됩니다.
        en: Using child's value as bound incorrectly constrains deeper nodes.
    - code: valid(node.left, node.val, right)
      type: distractor
      why:
        ko: 상한(right)을 업데이트하지 않으면, 왼쪽 서브트리가 현재 값보다 큰 값을 허용합니다.
        en: Not updating upper bound allows left subtree to have values larger than current.
  - label:
      ko: 오른쪽 서브트리 검증
      en: Validate right subtree
    indent: 1
    options:
    - code: node.right, node.val, right
      type: good
      why:
        ko: 오른쪽 자식은 현재 값보다 커야 하므로, 하한(lower bound)을 현재 노드의 값으로 업데이트합니다.
        en: Right subtree must be larger, so update lower bound to current node's value.
    - code: valid(node.right, node.right, right)
      type: distractor
      why:
        ko: 하한을 노드의 오른쪽 자식값으로 설정하면, 더 깊은 노드들이 부정확하게 제한됩니다.
        en: Using child's value as bound incorrectly constrains deeper nodes.
    - code: valid(node.right, left, node.val)
      type: distractor
      why:
        ko: 하한(left)을 업데이트하지 않으면, 오른쪽 서브트리가 현재 값보다 작은 값을 허용합니다.
        en: Not updating lower bound allows right subtree to have values smaller than current.
  - label:
      ko: 무한 경계로 재귀 시작
      en: Start recursion with infinite bounds
    indent: 0
    options:
    - code: return valid(root, float("-inf"), float("inf"))
      type: good
      why:
        ko: 모든 노드는 처음에 -무한대에서 +무한대 사이에 있으므로, 이 범위로 검증을 시작합니다.
        en: All nodes initially fall between -infinity and +infinity, so start with this range.
    - code: return valid(root, 0, float('inf'))
      type: distractor
      why:
        ko: 0을 하한으로 사용하면, 모든 음수 노드가 검증에 실패합니다.
        en: Using 0 as lower bound rejects all negative node values.
    - code: return valid(root, float('-inf'), 0)
      type: distractor
      why:
        ko: 0을 상한으로 사용하면, 모든 양수 노드가 검증에 실패합니다.
        en: Using 0 as upper bound rejects all positive node values.
trace:
  code:
  - '# Definition for a binary tree node.'
  - '# class TreeNode:'
  - '#     def __init__(self, val=0, left=None, right=None):'
  - '#         self.val = val'
  - '#         self.left = left'
  - '#         self.right = right'
  - 'class Solution:'
  - '    def isValidBST(self, root: TreeNode) -> bool:'
  - '        def valid(node, left, right):'
  - '            if not node:'
  - '                return True'
  - '            if not (left < node.val < right):'
  - '                return False'
  - ''
  - '            return valid(node.left, left, node.val) and valid('
  - '                node.right, node.val, right'
  - '            )'
  - ''
  - '        return valid(root, float("-inf"), float("inf"))'
  cases:
  - input: '[2,1,3]'
    expected: 'true'
  - input: '[5,1,4,null,null,3,6]'
    expected: 'false'
  worked_example:
    input: '[2,1,3]'
    steps:
    - ko: 'Root 2를 범위 (-∞, ∞)로 검증: -∞ < 2 < ∞ ✓'
      en: 'Validate root 2 in range (-∞, ∞): -∞ < 2 < ∞ ✓'
    - ko: '왼쪽 자식 1을 범위 (-∞, 2)로 검증: -∞ < 1 < 2 ✓ (자식 없음)'
      en: 'Validate left child 1 in range (-∞, 2): -∞ < 1 < 2 ✓ (no children)'
    - ko: '오른쪽 자식 3을 범위 (2, ∞)로 검증: 2 < 3 < ∞ ✓ (자식 없음)'
      en: 'Validate right child 3 in range (2, ∞): 2 < 3 < ∞ ✓ (no children)'
    - ko: 모든 노드가 유효하므로 true 반환
      en: All nodes valid, return true
    answer: 'true'
solution:
  code: "# Definition for a binary tree node.\n# class TreeNode:\n#     def __init__(self, val=0, left=None, right=None):\n#         self.val = val\n#         self.left = left\n#         self.right = right\nclass Solution:\n    def isValidBST(self, root: TreeNode) -> bool:\n        def valid(node, left, right):\n            if not node:\n                return True\n            if not (left < node.val < right):\n                return False\n\n            return valid(node.left, left, node.val) and valid(\n                node.right, node.val, right\n            )\n\n        return valid(root, float(\"-inf\"), float(\"inf\"))\n"
  complexity:
    time: O(n)
    space: O(h)
  followup:
  - ko: 매우 큰 트리에서 재귀 스택 공간을 최적화하려면 어떻게 해야 할까요?
    en: How can you optimize stack space for very large trees?
  - ko: 중위 순회를 사용하여 이 문제를 어떻게 풀 수 있을까요?
    en: How could you solve this using in-order traversal?
  - ko: 트리가 중복값을 허용한다면 어떻게 수정해야 할까요?
    en: How would the solution change if duplicate values were allowed?
```