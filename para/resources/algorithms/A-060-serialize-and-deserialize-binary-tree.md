---
created: '2026-07-06'
date: '2026-07-06'
day: Day 60
difficulty: hard
id: A-060
source:
  curated_in:
  - neetcode150
  number: 297
  platform: leetcode
  slug: serialize-and-deserialize-binary-tree
  url: https://leetcode.com/problems/serialize-and-deserialize-binary-tree/
tags:
- string
- tree
- depth-first-search
- breadth-first-search
- design
- binary-tree
title:
  en: Serialize and Deserialize Binary Tree
  ko: 이진 트리의 직렬화와 역직렬화
today: false
type: algorithm
updated: '2026-07-06'
visible: true
---

# 이진 트리의 직렬화와 역직렬화

## Data

```yaml
problem:
  title:
    ko: 이진 트리의 직렬화와 역직렬화
    en: Serialize and Deserialize Binary Tree
  statement:
    en: 'Serialization is the process of converting a data structure or object into a sequence of bits so that it can be stored in a file or memory buffer, or transmitted across a network connection link to be reconstructed later in the same or another computer environment.


      Design an algorithm to serialize and deserialize a binary tree. There is no restriction on how your serialization/deserialization algorithm should work. You just need to ensure that a binary tree can be serialized to a string and this string can be deserialized to the original tree structure.


      Clarification: The input/output format is the same as how LeetCode serializes a binary tree. You do not necessarily need to follow this format, so please be creative and come up with different approaches yourself.'
    ko: '직렬화는 데이터 구조나 객체를 비트 수열로 변환하여 파일이나 메모리 버퍼에 저장하거나 네트워크 연결을 통해 전송한 후, 같은 또는 다른 컴퓨터 환경에서 재구성할 수 있도록 하는 과정입니다.


      이진 트리를 직렬화하고 역직렬화하는 알고리즘을 설계하세요. 직렬화/역직렬화 알고리즘이 어떻게 작동하는지에 대한 제한은 없습니다. 이진 트리를 문자열로 직렬화할 수 있고, 이 문자열을 원래의 트리 구조로 역직렬화할 수 있도록 하면 됩니다.


      참고: 입출력 형식은 LeetCode가 이진 트리를 직렬화하는 방식과 동일합니다. 이 형식을 반드시 따를 필요는 없으므로, 창의적으로 다양한 접근 방식을 시도해 보세요.'
  constraints:
  - 0 ≤ number of nodes ≤ 10^4
  - -1000 ≤ node.val ≤ 1000
  io:
  - input: '[1,2,3,null,null,4,5]'
    output: '[1,2,3,null,null,4,5]'
  - input: '[]'
    output: '[]'
clarifying:
  items:
  - q:
      ko: 직렬화된 문자열의 형식에 제한이 있나요?
      en: Is there any restriction on the format of the serialized string?
    type: good
    why:
      ko: 문제에서 '직렬화/역직렬화 알고리즘이 어떻게 작동하는지에 대한 제한은 없습니다'라고 명시했으므로, 형식은 자유롭게 선택할 수 있습니다.
      en: The problem explicitly states there is no restriction on how the algorithm works, so you can choose any format as long as serialization and deserialization are consistent.
  - q:
      ko: null 노드를 어떻게 표현해야 하나요?
      en: How should null nodes be represented in the serialized string?
    type: good
    why:
      ko: 'null 노드의 명시적 표현이 없으면 역직렬화 중에 트리 구조를 정확하게 재구성할 수 없습니다. null을 특정 마커(예: ''N'')로 표현하는 것이 필수적입니다.'
      en: Without explicitly representing null nodes, the deserializer cannot distinguish between different tree structures. A marker like 'N' is necessary to preserve the tree structure.
  - q:
      ko: 트리 순회의 어떤 순서를 사용해야 하나요?
      en: Which tree traversal order is most suitable for this problem?
    type: good
    why:
      ko: 전위(pre-order) 순회는 부모 노드가 자식 노드보다 먼저 나타나므로, 역직렬화할 때 현재 값을 읽고 즉시 노드를 생성할 수 있습니다.
      en: Pre-order traversal (parent before children) allows the deserializer to create nodes immediately upon reading values, making reconstruction straightforward.
  - q:
      ko: 노드의 값이 음수일 수 있나요?
      en: Can node values be negative?
    type: good
    why:
      ko: 제약 조건에서 '-1000 ≤ node.val ≤ 1000'이므로 음수 값이 가능합니다. 따라서 null 마커로는 숫자가 아닌 문자('N' 등)를 사용해야 합니다.
      en: Yes, the constraints show that node values range from -1000 to 1000, including negatives. This requires a non-numeric marker like 'N' for null nodes.
  - q:
      ko: 공트리(빈 트리)는 어떻게 처리하나요?
      en: How should an empty tree be handled?
    type: good
    why:
      ko: root가 None이면 직렬화는 'N'을 반환하고, 역직렬화 시 'N'을 읽으면 None을 반환해야 합니다.
      en: When root is None, serialize should return 'N', and deserialize should return None when it encounters 'N' at the start.
  - q:
      ko: 순환 구조(cycle)가 있는 그래프도 처리할 수 있나요?
      en: Can this algorithm handle cyclic graphs?
    type: distractor
    why:
      ko: 문제는 '이진 트리'를 다루며, 트리는 정의상 순환이 없습니다. 순환 처리는 고려할 필요가 없습니다.
      en: The problem specifically states it's a binary tree, which by definition has no cycles. Cycle handling is not necessary.
  - q:
      ko: 직렬화된 문자열이 반드시 사람이 읽을 수 있어야 하나요?
      en: Must the serialized format be human-readable?
    type: distractor
    why:
      ko: 문제에서 가독성에 대한 요구사항이 없습니다. 효율성이나 간결성을 위해 이진 형식도 사용할 수 있습니다.
      en: There is no requirement for human readability. The format can be binary, compressed, or any format that allows faithful reconstruction.
approach:
  items:
  - name:
      ko: 전위 순회(Pre-order DFS) + null 마커
      en: Pre-order DFS with null markers
    complexity: O(n) time / O(n) space
    type: good
    why:
      ko: 전위 순회는 부모 노드를 먼저 방문하므로, 역직렬화 시 값을 읽는 순서대로 노드를 생성할 수 있습니다. null 마커는 트리 구조를 보존합니다.
      en: Pre-order visits parents before children, allowing deserialization to reconstruct nodes in the same order values are read. Null markers preserve the complete tree structure.
  - name:
      ko: 레벨 순서 순회(BFS) + 큐
      en: Level-order BFS with queue
    complexity: O(n) time / O(n) space
    type: good
    why:
      ko: BFS는 각 레벨의 노드를 순차적으로 처리하므로, null 위치 정보가 명확하고, 역직렬화 시도 큐를 사용하여 자연스럽게 재구성됩니다.
      en: BFS processes nodes level by level, making null positions clear during serialization. Deserialization naturally reconstructs using a queue for child assignment.
  - name:
      ko: 중위 순회(In-order)
      en: In-order traversal
    complexity: O(n) time / O(n) space
    type: distractor
    why:
      ko: 중위 순회는 부모 노드가 자식 노드 사이에 위치하므로, 값만으로는 트리 구조를 복원할 수 없습니다.
      en: In-order places parents between children, making it impossible to reconstruct the tree unambiguously from values alone.
  - name:
      ko: 후위 순회(Post-order)
      en: Post-order traversal
    complexity: O(n) time / O(n) space
    type: distractor
    why:
      ko: 후위 순회는 자식 노드 후에 부모 노드가 나타나므로, 역직렬화 시 현재 값만으로 노드 생성 여부를 판단할 수 없어 구현이 복잡합니다.
      en: Post-order places parents after children, requiring complex lookahead logic during deserialization. Pre-order is more natural for this problem.
logic:
  format: slot
  slots:
  - label:
      ko: '직렬화 초기화: 결과 리스트'
      en: 'Serialize initialization: Create result list'
    indent: 0
    options:
    - code: ''
      type: good
      why:
        ko: 결과를 누적할 리스트를 초기화합니다. 직렬화 프로세스 전체에서 노드와 null 값을 저장할 컨테이너입니다.
        en: Initialize a list to accumulate serialized values. This container stores all nodes and null markers throughout the traversal.
    - code: res = ""
      type: distractor
      why:
        ko: 문자열로 시작하면 append 시 성능이 떨어집니다. 리스트를 사용하고 나중에 join하는 것이 더 효율적입니다.
        en: String concatenation is inefficient. Using a list and joining at the end is better for performance.
    - code: 'res = []  # Initialize with root value'
      type: distractor
      why:
        ko: root를 미리 추가하면 DFS 함수가 root를 다시 처리할 때 중복이 발생합니다.
        en: Pre-adding root causes duplication when the DFS function processes it.
  - label:
      ko: '기본 사례: null 노드 표현'
      en: 'Base case: Represent null nodes'
    indent: 1
    options:
    - code: ''
      type: good
      why:
        ko: null 노드를 만나면 'N' 마커를 추가합니다. 이를 통해 역직렬화 시 트리 구조를 정확하게 복원할 수 있습니다.
        en: When encountering a null node, append a marker ('N'). This preserves tree structure information needed for deserialization.
    - code: 'if not node: return'
      type: distractor
      why:
        ko: return을 사용하면 null 위치 정보가 손실되어 역직렬화 시 트리를 복원할 수 없습니다.
        en: Using return without appending a marker loses the information about null positions.
    - code: 'if node is None: res.append(0)'
      type: distractor
      why:
        ko: 0을 마커로 사용하면 실제 노드 값 0과 구분할 수 없습니다.
        en: Using 0 as a marker conflicts with actual node value 0.
  - label:
      ko: '재귀 사례: 현재 노드 값 저장'
      en: 'Recursive case: Store current node value'
    indent: 1
    options:
    - code: ''
      type: good
      why:
        ko: null이 아닌 노드에 대해 현재 노드의 값을 먼저 추가합니다. 전위 순회의 핵심으로, 역직렬화 시 현재 값을 읽고 즉시 노드를 생성할 수 있게 합니다.
        en: 'For non-null nodes, append the current value first. This is the essence of pre-order: deserializer can create the node immediately upon reading the value.'
    - code: dfs(node.left); res.append(str(node.val)); dfs(node.right)
      type: distractor
      why:
        ko: 이는 중위 순회입니다. 값이 자식 노드 사이에 위치하므로 역직렬화가 복잡해집니다.
        en: This is in-order traversal. With the value between children, deserialization becomes ambiguous.
    - code: res.append(str(node.val)); dfs(node.right); dfs(node.left)
      type: distractor
      why:
        ko: 좌우 순서를 바꾸면 직렬화 순서가 달라져서 역직렬화 시 잘못된 구조가 만들어집니다.
        en: Swapping the order produces a different serialization, leading to incorrect reconstruction.
  - label:
      ko: '전위 순회: 좌우 자식 재귀'
      en: 'Pre-order traversal: Recurse on left and right'
    indent: 1
    options:
    - code: ''
      type: good
      why:
        ko: 현재 노드 값을 추가한 후 좌측 서브트리, 우측 서브트리 순서로 재귀합니다. 이 순서가 역직렬화 시 값을 올바른 순서대로 소비할 수 있게 합니다.
        en: After processing the current node, recurse left then right. This order ensures the deserializer consumes values in the correct sequence for reconstruction.
    - code: dfs(node.right); dfs(node.left)
      type: distractor
      why:
        ko: 좌우 순서를 바꾸면 트리가 거울상으로 뒤집힙니다.
        en: Reversing the order creates a mirror image of the tree.
    - code: 'if node.left: dfs(node.left); if node.right: dfs(node.right)'
      type: distractor
      why:
        ko: null 자식을 건너뛰면 null 마커가 추가되지 않아 구조 정보가 손실됩니다.
        en: Skipping null children prevents null markers from being added, losing structure information.
  - label:
      ko: '직렬화 마무리: 컴마로 결합'
      en: 'Serialize finalization: Join with comma'
    indent: 0
    options:
    - code: ''
      type: good
      why:
        ko: 리스트의 모든 요소를 쉼표로 구분된 문자열로 변환합니다. 역직렬화 시 이 형식으로 쉽게 분할할 수 있습니다.
        en: Convert the list into a comma-separated string. This allows deserialization to easily split the string back into components.
    - code: return res
      type: distractor
      why:
        ko: 리스트를 그대로 반환하면 문자열이 아니라 문제의 요구 사항과 맞지 않습니다.
        en: Returning a list instead of a string doesn't meet the serialization requirement.
    - code: return '|'.join(res)
      type: distractor
      why:
        ko: 다른 구분자를 사용해도 작동하지만, 코드 일관성을 위해 쉼표를 사용하는 것이 표준입니다.
        en: While other delimiters work, using comma is the standard and ensures consistency with deserialization.
  - label:
      ko: '역직렬화 초기화: 문자열 분할'
      en: 'Deserialize initialization: Split string'
    indent: 0
    options:
    - code: ''
      type: good
      why:
        ko: 쉼표로 구분된 문자열을 리스트로 변환합니다. 이 리스트를 순차적으로 pop하면서 트리를 재구성합니다.
        en: Convert the comma-separated string into a list of values. This list is consumed sequentially during reconstruction.
    - code: vals = list(data)
      type: distractor
      why:
        ko: 각 문자로 분할되므로 멀티자리 숫자가 개별 문자로 나뉩니다.
        en: This splits by character, not by comma, breaking multi-digit numbers.
    - code: vals = data.split('N')
      type: distractor
      why:
        ko: '''N''으로 분할하면 노드 값들이 분리되어 구조 정보가 왜곡됩니다.'
        en: Splitting by 'N' separates values and distorts the structure information.
  - label:
      ko: '재귀적 재구성: 값 팝과 노드 생성'
      en: 'Recursive reconstruction: Pop value and create node'
    indent: 1
    options:
    - code: ''
      type: good
      why:
        ko: 리스트의 앞에서 값을 하나씩 pop하면서, 'N'이면 None 반환, 아니면 새 노드를 생성하고 좌우 자식을 재귀적으로 채웁니다. 전위 순회의 역순이므로 올바른 구조가 복원됩니다.
        en: Pop values sequentially from the front. If 'N', return None; otherwise create a node and recursively fill children. This mirrors the serialization order, ensuring correct reconstruction.
    - code: 'val = vals.pop(); if val == ''N'': return None; node = TreeNode(int(val)); node.right = dfs(); node.left = dfs(); return node'
      type: distractor
      why:
        ko: 리스트 끝에서 pop하고 좌우 순서를 바꾸면 트리가 거울상으로 뒤집히고 순서도 틀립니다.
        en: Popping from the end and reversing left/right creates an inverted, incorrect tree.
    - code: 'val = vals.pop(0); if val != ''N'': node = TreeNode(int(val)); node.left = dfs(); node.right = dfs(); return node'
      type: distractor
      why:
        ko: 조건문을 반대로 사용하면 null인 경우 재귀가 일어나지 않아 리스트 소비 순서가 틀려집니다.
        en: Inverting the condition logic prevents proper value consumption, breaking the reconstruction sequence.
trace:
  code:
  - '# Definition for a binary tree node.'
  - '# class TreeNode(object):'
  - '#     def __init__(self, x):'
  - '#         self.val = x'
  - '#         self.left = None'
  - '#         self.right = None'
  - ''
  - ''
  - 'class Codec:'
  - '    def serialize(self, root):'
  - '        res = []'
  - ''
  - '        def dfs(node):'
  - '            if not node:'
  - '                res.append("N")'
  - '                return'
  - '            res.append(str(node.val))'
  - '            dfs(node.left)'
  - '            dfs(node.right)'
  - ''
  - '        dfs(root)'
  - '        return ",".join(res)'
  - ''
  - '    def deserialize(self, data):'
  - '        vals = data.split(",")'
  - ''
  - '        def dfs():'
  - '            val = vals.pop(0)'
  - '            if val == "N":'
  - '                return None'
  - '            node = TreeNode(val=int(val))'
  - '            node.left = dfs()'
  - '            node.right = dfs()'
  - '            return node'
  - ''
  - '        return dfs()'
  cases:
  - input: '[1,2,3,null,null,4,5]'
    expected: '[1,2,3,null,null,4,5]'
  - input: '[]'
    expected: '[]'
  worked_example:
    input: '[1,2,3,null,null,4,5]'
    steps:
    - ko: 노드 1 방문 → 'serialize'에서 "1" 추가, 좌측 서브트리로 이동
      en: Visit node 1 → Append "1", move to left subtree
    - ko: 노드 2 방문 → "2" 추가, 좌측 자식 null → "N" 추가, 우측 자식 null → "N" 추가, 우측 서브트리로 이동
      en: Visit node 2 → Append "2", left child null → Append "N", right child null → Append "N", backtrack to node 1
    - ko: 노드 3 방문 → "3" 추가, 좌측에서 노드 4 방문 → "4,N,N" 추가, 우측에서 노드 5 방문 → "5,N,N" 추가
      en: 'Visit node 3 → Append "3", left subtree: visit 4 → Append "4,N,N", right subtree: visit 5 → Append "5,N,N"'
    - ko: '결과 리스트: [1,2,N,N,3,4,N,N,5,N,N] → 쉼표로 결합'
      en: 'Result list: [1,2,N,N,3,4,N,N,5,N,N] → Join with commas'
    answer: '"1,2,N,N,3,4,N,N,5,N,N"'
solution:
  code: "# Definition for a binary tree node.\n# class TreeNode(object):\n#     def __init__(self, x):\n#         self.val = x\n#         self.left = None\n#         self.right = None\n\n\nclass Codec:\n    def serialize(self, root):\n        res = []\n\n        def dfs(node):\n            if not node:\n                res.append(\"N\")\n                return\n            res.append(str(node.val))\n            dfs(node.left)\n            dfs(node.right)\n\n        dfs(root)\n        return \",\".join(res)\n\n    def deserialize(self, data):\n        vals = data.split(\",\")\n\n        def dfs():\n            val = vals.pop(0)\n            if val == \"N\":\n                return None\n            node = TreeNode(val=int(val))\n            node.left = dfs()\n            node.right = dfs()\n            return node\n\n        return dfs()\n"
  complexity:
    time: O(n)
    space: O(n)
  followup:
  - ko: 매우 큰 트리가 메모리에 맞지 않으면 어떻게 하나요? 스트리밍 방식으로 직렬화할 수 있을까요?
    en: How would you handle very large trees that don't fit in memory? Can you implement streaming serialization?
  - ko: BFS(레벨 순서)를 사용한 직렬화 방식의 장단점은 무엇인가요?
    en: What are the pros and cons of using BFS (level-order) serialization instead of DFS?
  - ko: 직렬화된 문자열 크기를 최소화하려면 어떻게 할까요?
    en: How can you minimize the size of the serialized string?
```