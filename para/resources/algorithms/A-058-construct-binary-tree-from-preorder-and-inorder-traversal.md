---
created: '2026-07-04'
date: '2026-07-04'
day: Day 58
difficulty: medium
id: A-058
source:
  curated_in:
  - neetcode150
  number: 105
  platform: leetcode
  slug: construct-binary-tree-from-preorder-and-inorder-traversal
  url: https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/
tags:
- array
- hash-table
- divide-and-conquer
- tree
- binary-tree
title:
  en: Construct Binary Tree from Preorder and Inorder Traversal
  ko: 전위 순회와 중위 순회로부터 이진 트리 구성하기
today: false
type: algorithm
updated: '2026-07-04'
visible: true
---

# 전위 순회와 중위 순회로부터 이진 트리 구성하기

## Data

```yaml
problem:
  title:
    ko: 전위 순회와 중위 순회로부터 이진 트리 구성하기
    en: Construct Binary Tree from Preorder and Inorder Traversal
  statement:
    ko: '정수 배열 두 개가 주어집니다: preorder는 이진 트리의 전위 순회이고, inorder는 같은 트리의 중위 순회입니다. 이 두 배열로부터 이진 트리를 구성하여 반환하세요.'
    en: Given two integer arrays preorder and inorder where preorder is the preorder traversal of a binary tree and inorder is the inorder traversal of the same tree, construct and return the binary tree.
  constraints:
  - 1 ≤ preorder.length ≤ 3000
  - inorder.length == preorder.length
  - -3000 ≤ preorder[i], inorder[i] ≤ 3000
  - All values in preorder and inorder are unique
  io:
  - input: '[3,9,20,15,7]

      [9,3,15,20,7]'
    output: '[3,9,20,null,null,15,7]'
  - input: '[-1]

      [-1]'
    output: '[-1]'
clarifying:
  items:
  - q:
      ko: 전위 순회와 중위 순회는 각각 무엇입니까?
      en: What are preorder and inorder traversals?
    type: good
    why:
      ko: 이 문제를 풀기 위해 각 순회 방식의 의미를 이해하는 것이 필수적입니다. 전위는 (루트, 좌, 우), 중위는 (좌, 루트, 우) 순서입니다.
      en: Understanding the properties of each traversal is essential. Preorder visits nodes in (root, left, right) order, while inorder visits them in (left, root, right) order.
  - q:
      ko: 전위 순회에서 첫 번째 원소가 항상 루트가 되는 이유는?
      en: Why is the first element of preorder always the root?
    type: good
    why:
      ko: 전위 순회의 정의에 따라 루트를 가장 먼저 방문하므로, preorder[0]은 항상 루트입니다.
      en: By definition, preorder traversal visits the root node first, so preorder[0] is always the root of the tree.
  - q:
      ko: 중위 배열에서 루트의 위치를 찾은 후 그 인덱스를 어떻게 활용합니까?
      en: After finding the root's position in inorder, how do you use that index to split the arrays?
    type: good
    why:
      ko: 중위 순회에서 루트의 좌측 원소는 모두 좌측 부분트리, 우측 원소는 모두 우측 부분트리입니다. 이를 이용해 배열을 분할할 수 있습니다.
      en: In inorder traversal, elements to the left of the root belong to the left subtree, and elements to the right belong to the right subtree. This correctly partitions both arrays.
  - q:
      ko: 좌우 부분트리의 preorder와 inorder 부분배열 길이가 반드시 같아야 하는 이유는?
      en: Why must corresponding subarrays in preorder and inorder have the same length?
    type: good
    why:
      ko: 같은 부분트리를 두 가지 순회 방식으로 표현하므로, 같은 노드 집합을 포함하며 따라서 길이가 같아야 합니다.
      en: Both arrays represent the same subtree from different perspectives, so they must contain the same nodes and have equal length.
  - q:
      ko: 전위 순회 배열만으로 원본 트리를 유일하게 복원할 수 있습니까?
      en: Can you reconstruct the tree uniquely from just preorder alone?
    type: distractor
    why:
      ko: 아니요. 예를 들어 [1,2]는 1의 좌식이 2인 경우와 1의 우식이 2인 경우 두 가지 모두 가능하므로, 중위 정보 없이는 구분할 수 없습니다.
      en: No. For example, [1,2] could represent 1 with left child 2 or 1 with right child 2. Without inorder, you cannot distinguish them.
  - q:
      ko: preorder와 inorder가 실제로 같은 트리를 나타내는지 검증해야 합니까?
      en: Should you validate that preorder and inorder represent the same tree?
    type: distractor
    why:
      ko: 문제 조건에서 입력의 유효성이 보장되므로 검증은 불필요합니다.
      en: The problem guarantees valid inputs, so validation is unnecessary.
  - q:
      ko: 배열 슬라이싱으로 인한 공간 복잡도는 O(n)입니까?
      en: Does array slicing affect the overall space complexity?
    type: good
    why:
      ko: 파이썬에서 슬라이싱은 새로운 배열을 생성합니다. 모든 부분배열의 합은 O(n)이므로 공간복잡도는 O(n)입니다.
      en: Python slicing creates new arrays. Summing all subarrays across recursion gives O(n) auxiliary space.
approach:
  items:
  - name:
      ko: 재귀적 분할 정복 (기본 구현)
      en: Recursive Divide and Conquer
    complexity: O(n²) time / O(n) space
    type: good
    why:
      ko: 각 재귀 호출에서 inorder.index()가 O(n)이고 총 O(n)번 호출되므로 O(n²)입니다. 공간은 재귀 스택과 슬라이싱 오버헤드로 O(n)입니다.
      en: Each recursive call uses inorder.index() (O(n)), and there are O(n) calls, resulting in O(n²) time. Space is O(n) for recursion depth and array copying.
  - name:
      ko: 재귀 + 해시맵 최적화
      en: Recursive with HashMap Optimization
    complexity: O(n) time / O(n) space
    type: good
    why:
      ko: inorder를 미리 해시맵으로 변환하면 루트 위치 조회가 O(1)이 되어 전체 시간복잡도가 O(n)입니다.
      en: Pre-building a HashMap of inorder indices allows O(1) root lookup per call, reducing total time to O(n).
  - name:
      ko: 재귀 + 인덱스 포인터
      en: Recursive with Index Pointers (No Slicing)
    complexity: O(n) time / O(h) space
    type: good
    why:
      ko: 배열 슬라이싱 대신 시작/종료 인덱스를 추적하면 배열 복사가 없어져 보조 공간이 O(h)(트리 높이)로 줄어듭니다.
      en: Tracking indices instead of slicing eliminates array copies. Auxiliary space becomes O(h) where h is tree height.
  - name:
      ko: 반복문 + 스택
      en: Iterative with Stack
    complexity: O(n) time / O(n) space
    type: distractor
    why:
      ko: 스택 기반 반복 구현도 가능하지만, 전위 순회 특성을 정확히 추적해야 하므로 재귀보다 구현이 훨씬 복잡합니다.
      en: Possible with a stack, but requires careful tracking of preorder properties and is harder to implement correctly.
  - name:
      ko: 중위 + 후위 순회로부터 구성
      en: Construct from Postorder and Inorder
    complexity: O(n) time / O(n) space
    type: distractor
    why:
      ko: 후위 순회를 사용하는 알고리즘도 존재하지만, 이 문제에서는 전위가 주어지므로 불필요합니다.
      en: While valid with postorder, it does not apply since this problem provides preorder traversal.
logic:
  format: slot
  slots:
  - label:
      ko: '기저 사례: 빈 배열 확인'
      en: 'Base case: Check for empty arrays'
    indent: 0
    options:
    - code: 'if not preorder or not inorder:'
      type: good
      why:
        ko: 배열이 비어있으면 부분트리가 없으므로 재귀를 종료해야 합니다. 이 조건이 없으면 preorder[0]에서 IndexError가 발생합니다.
        en: If either array is empty, there are no more nodes. Without this check, accessing preorder[0] causes an IndexError.
    - code: 'if preorder and inorder:'
      type: distractor
      why:
        ko: 논리가 반대입니다. 이는 배열이 비어있지 않을 때 분기를 타므로 조건이 뒤집혀 있습니다.
        en: This inverts the logic—it only proceeds when arrays are NOT empty, opposite of what we need.
    - code: 'if len(preorder) == 0 or len(inorder) == 0:'
      type: distractor
      why:
        ko: 작동하지만 파이썬 관례상 단순 truthy/falsy 체크가 더 깔끔합니다.
        en: Functionally correct but verbose. Pythonic style prefers `if not` for empty sequences.
    - code: 'if preorder is None or inorder is None:'
      type: distractor
      why:
        ko: 빈 리스트는 None이 아닙니다. 이 체크는 None만 감지하므로 빈 배열을 놓칩니다.
        en: Empty lists are not None. This only catches None references, not empty lists.
  - label:
      ko: 루트 노드 생성
      en: Create root node
    indent: 0
    options:
    - code: root = TreeNode(preorder[0])
      type: good
      why:
        ko: 전위 순회의 정의에 따라 첫 번째 원소는 항상 현재 부분트리의 루트입니다.
        en: By definition of preorder traversal, the first element is always the root of the current subtree.
    - code: root = TreeNode(inorder[0])
      type: distractor
      why:
        ko: 중위에서 첫 원소는 좌측 부분트리의 가장 왼쪽 노드이지, 루트가 아닙니다.
        en: In inorder, the first element is the leftmost node of the left subtree, not the root.
    - code: root = TreeNode(preorder[-1])
      type: distractor
      why:
        ko: 전위의 마지막 원소는 우측 부분트리의 가장 오른쪽 노드입니다.
        en: The last element of preorder is the rightmost node of the right subtree.
    - code: root = TreeNode((preorder[0] + inorder[0]) // 2)
      type: distractor
      why:
        ko: 노드 값을 평균내는 것은 의미가 없습니다. 루트는 항상 preorder[0]입니다.
        en: Averaging node values has no meaning. The root is explicitly preorder[0].
  - label:
      ko: '분할점 찾기: 중위에서 루트의 위치'
      en: 'Find partition point: root position in inorder'
    indent: 0
    options:
    - code: mid = inorder.index(preorder[0])
      type: good
      why:
        ko: 중위 순회에서 루트의 위치가 분할점입니다. 그 좌측은 좌측 부분트리, 우측은 우측 부분트리입니다.
        en: In inorder, the root's position divides left and right subtrees. Elements before are left subtree; elements after are right subtree.
    - code: mid = preorder.index(root.val)
      type: distractor
      why:
        ko: 루트는 항상 preorder[0]에 있으므로 이 호출은 항상 0을 반환합니다. 의미가 없습니다.
        en: The root is always at preorder[0], so this always returns 0, which is useless.
    - code: mid = len(inorder) // 2
      type: distractor
      why:
        ko: 배열의 중간에서 분할하면 균형 잡힌 트리를 가정합니다. 실제 루트는 어디든 있을 수 있습니다.
        en: This assumes a balanced tree. The actual root can be at any position.
    - code: mid = inorder.index(preorder[mid])
      type: distractor
      why:
        ko: 변수 mid가 아직 정의되지 않았으므로 NameError가 발생합니다.
        en: Variable mid is not yet defined, causing a NameError.
  - label:
      ko: 좌측 부분트리 재귀 구성
      en: Recursively construct left subtree
    indent: 0
    options:
    - code: 'root.left = self.buildTree(preorder[1 : mid + 1], inorder[:mid])'
      type: good
      why:
        ko: 좌측 부분트리는 preorder[1:mid+1](전위)과 inorder[:mid](중위)에 포함됩니다. 두 범위는 같은 노드 집합을 나타냅니다.
        en: Left subtree nodes are preorder[1:mid+1] in preorder and inorder[:mid] in inorder. Both ranges represent the same set of nodes.
    - code: root.left = self.buildTree(preorder[1:mid], inorder[:mid])
      type: distractor
      why:
        ko: preorder[1:mid]는 마지막 요소를 제외하므로, 좌측 부분트리의 마지막 노드가 누락됩니다.
        en: preorder[1:mid] excludes the last left node. Should be preorder[1:mid+1].
    - code: root.left = self.buildTree(preorder[1:], inorder[:mid])
      type: distractor
      why:
        ko: preorder[1:]은 남은 모든 원소(좌측과 우측)를 포함하므로 범위가 너무 깁니다.
        en: preorder[1:] includes both left and right subtrees. Range is too large.
    - code: root.left = self.buildTree(preorder[1:mid+1], inorder[:mid+1])
      type: distractor
      why:
        ko: inorder[:mid+1]은 루트를 포함하므로 두 배열의 크기가 맞지 않습니다.
        en: inorder[:mid+1] includes the root, causing a length mismatch with preorder.
  - label:
      ko: 우측 부분트리 재귀 구성
      en: Recursively construct right subtree
    indent: 0
    options:
    - code: root.right = self.buildTree(preorder[mid + 1 :], inorder[mid + 1 :])
      type: good
      why:
        ko: 우측 부분트리는 preorder[mid+1:]과 inorder[mid+1:]에 포함됩니다. 두 범위는 같은 노드 집합을 나타냅니다.
        en: Right subtree nodes are preorder[mid+1:] and inorder[mid+1:]. Both ranges represent the same set of nodes.
    - code: root.right = self.buildTree(preorder[mid:], inorder[mid+1:])
      type: distractor
      why:
        ko: preorder[mid:]는 루트를 포함하므로 inorder[mid+1:]과 크기가 맞지 않습니다.
        en: preorder[mid:] includes the root, causing a length mismatch with inorder[mid+1:].
    - code: root.right = self.buildTree(preorder[mid+1:], inorder[mid:])
      type: distractor
      why:
        ko: inorder[mid:]는 루트를 포함하므로 두 배열이 같은 노드 집합을 나타내지 않습니다.
        en: inorder[mid:] includes the root, causing arrays to represent different node sets.
    - code: root.right = self.buildTree(preorder[mid:], inorder[mid:])
      type: distractor
      why:
        ko: 두 배열 모두 루트를 포함하므로 일치하지 않습니다.
        en: Both ranges include the root, breaking the correspondence.
  - label:
      ko: 구성한 트리 반환
      en: Return constructed tree
    indent: 0
    options:
    - code: return root
      type: good
      why:
        ko: 루트 노드를 반환하면 그 아래의 모든 부분트리가 함께 반환됩니다. 이진 트리는 루트 노드로 완전히 정의되기 때문입니다.
        en: Returning the root node returns the entire subtree, since a binary tree is fully defined by its root.
    - code: return root.val
      type: distractor
      why:
        ko: 값만 반환하면 트리 구조가 모두 손실됩니다. TreeNode 객체를 반환해야 합니다.
        en: Returning just the value loses the tree structure. Must return the TreeNode object.
    - code: return None
      type: distractor
      why:
        ko: 항상 None을 반환하면 구성한 전체 트리가 버려집니다.
        en: Returning None always discards the constructed tree.
    - code: return root.left, root.right
      type: distractor
      why:
        ko: 자식 노드만 반환하면 루트 자신이 손실됩니다.
        en: This returns only children, losing the root node itself.
trace:
  code:
  - 'class Solution:'
  - '    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:'
  - '        if not preorder or not inorder:'
  - '            return None'
  - ''
  - '        root = TreeNode(preorder[0])'
  - '        mid = inorder.index(preorder[0])'
  - '        root.left = self.buildTree(preorder[1 : mid + 1], inorder[:mid])'
  - '        root.right = self.buildTree(preorder[mid + 1 :], inorder[mid + 1 :])'
  - '        return root'
  cases:
  - input: '[3,9,20,15,7]

      [9,3,15,20,7]'
    expected: '[3,9,20,null,null,15,7]'
  - input: '[-1]

      [-1]'
    expected: '[-1]'
  worked_example:
    input: '[3,9,20,15,7]

      [9,3,15,20,7]'
    steps:
    - ko: '루트: preorder[0]=3, inorder에서 인덱스=1. 좌측 [9], 우측 [15,20,7]'
      en: 'Root is 3 (preorder[0]). Find 3 in inorder at index 1. Left: [9], Right: [15,20,7]'
    - ko: '좌측 재귀: preorder=[9], inorder=[9] → 단일 노드 9 (자식 없음)'
      en: 'Left subtree: preorder=[9], inorder=[9] → single node 9 with no children'
    - ko: '우측 재귀: preorder=[20,15,7], inorder=[15,20,7] → 루트=20, 인덱스=1. 좌측 [15], 우측 [7]'
      en: 'Right subtree: preorder=[20,15,7], inorder=[15,20,7] → root 20 at index 1. Left: [15], Right: [7]'
    - ko: '20의 자식들: 좌식=15 (단일), 우식=7 (단일). 최종 트리: 3(좌:9, 우:20(좌:15, 우:7))'
      en: 'Node 20''s children: left=15, right=7 (both single nodes). Final tree structure complete.'
    answer: '[3,9,20,null,null,15,7]'
solution:
  code: "class Solution:\n    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:\n        if not preorder or not inorder:\n            return None\n\n        root = TreeNode(preorder[0])\n        mid = inorder.index(preorder[0])\n        root.left = self.buildTree(preorder[1 : mid + 1], inorder[:mid])\n        root.right = self.buildTree(preorder[mid + 1 :], inorder[mid + 1 :])\n        return root\n"
  complexity:
    time: O(n²) with naive list index lookup; O(n) with HashMap optimization
    space: O(n) for recursion stack and array slicing overhead
  followup:
  - ko: 해시맵을 사용하여 inorder의 인덱스를 미리 저장하면 어떻게 O(n)으로 최적화할 수 있습니까?
    en: How can you optimize to O(n) time by storing inorder indices in a HashMap?
  - ko: 후위 순회와 중위 순회가 주어진다면 알고리즘이 어떻게 달라집니까?
    en: How would the algorithm change if you were given postorder and inorder instead?
  - ko: 배열 슬라이싱 대신 시작/종료 인덱스를 사용하면 공간복잡도를 O(h)로 개선할 수 있습니까?
    en: How can you reduce space complexity to O(h) by using index pointers instead of slicing?
```