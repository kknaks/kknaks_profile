---
created: '2026-06-14'
date: '2026-06-14'
day: Day 39
difficulty: medium
id: A-039
source:
  curated_in:
  - neetcode150
  number: 138
  platform: leetcode
  slug: copy-list-with-random-pointer
  url: https://leetcode.com/problems/copy-list-with-random-pointer/
status: draft
tags:
- hash-table
- linked-list
title:
  en: Copy List with Random Pointer
  ko: 랜덤 포인터가 있는 리스트 복사
today: true
type: algorithm
updated: '2026-06-14'
visible: true
---

# 랜덤 포인터가 있는 리스트 복사

## Data

```yaml
problem:
  title:
    ko: 랜덤 포인터가 있는 리스트 복사
    en: Copy List with Random Pointer
  statement:
    en: 'A linked list of length n is given such that each node contains an additional random pointer, which could point to any node in the list, or null.


      Construct a deep copy of the list. The deep copy should consist of exactly n brand new nodes, where each new node has its value set to the value of its corresponding original node. Both the next and random pointer of the new nodes should point to new nodes in the copied list such that the pointers in the original list and copied list represent the same list state. None of the pointers in the new list should point to nodes in the original list.


      For example, if there are two nodes X and Y in the original list, where X.random --> Y, then for the corresponding two nodes x and y in the copied list, x.random --> y.'
    ko: '각 노드에 random 포인터가 추가된 길이 n인 링크드 리스트가 주어집니다. random 포인터는 리스트의 어떤 노드를 가리킬 수도 있고, null을 가리킬 수도 있습니다.


      리스트의 깊은 복사본(deep copy)을 구성하세요. 깊은 복사본은 정확히 n개의 완전히 새로운 노드로 구성되어야 하며, 각 새 노드의 값은 대응하는 원본 노드의 값으로 설정되어야 합니다. 새 노드의 next와 random 포인터는 모두 복사된 리스트의 새 노드를 가리켜야 하므로, 원본 리스트의 포인터와 복사된 리스트의 포인터가 동일한 리스트 상태를 나타냅니다. 새 리스트의 어떤 포인터도 원본 리스트의 노드를 가리키면 안 됩니다.


      예를 들어, 원본 리스트에 X와 Y 두 개의 노드가 있고 X.random --> Y인 경우, 복사된 리스트의 대응하는 두 노드 x와 y에 대해 x.random --> y이어야 합니다.'
  constraints:
  - 0 ≤ n ≤ 1000
  - -10⁴ ≤ Node.val ≤ 10⁴
  - Node.random is null or points to some node in the linked list
  io:
  - input: '[[7,null],[13,0],[11,4],[10,2],[1,0]]'
    output: '[[7,null],[13,0],[11,4],[10,2],[1,0]]'
  - input: '[[1,1],[2,1]]'
    output: '[[1,1],[2,1]]'
  - input: '[[3,null],[3,0],[3,null]]'
    output: '[[3,null],[3,0],[3,null]]'
clarifying:
  items:
  - q:
      ko: 빈 리스트(head = None)를 처리해야 하나요?
      en: Do we need to handle an empty list (head = None)?
    type: good
    why:
      ko: 제약 조건에서 n ≥ 0이므로 빈 리스트도 유효한 입력입니다. 코드가 None을 올바르게 처리하는지 확인이 필요합니다.
      en: The constraint allows n = 0, so empty lists are valid. The algorithm must handle None gracefully.
  - q:
      ko: 한 노드의 random 포인터가 자신을 가리킬 수 있나요?
      en: Can a node's random pointer point to itself?
    type: good
    why:
      ko: 제약 조건에서 random이 '리스트의 어떤 노드'를 가리킬 수 있다고 하므로, 자신을 포함합니다. 이 경우도 올바르게 처리해야 합니다.
      en: Since random can point to any node in the list, self-referencing is valid and the algorithm must handle it.
  - q:
      ko: random 포인터가 null일 수 있나요?
      en: Can a node's random pointer be null?
    type: good
    why:
      ko: '예시들을 보면 일부 노드의 random이 null입니다. 이를 효율적으로 처리하려면 매핑에 {None: None}을 미리 등록하면 됩니다.'
      en: Yes, examples show nodes with random=null. Pre-mapping None→None in the hash map elegantly handles this case.
  - q:
      ko: 새 노드의 포인터가 원본 노드를 가리켜도 되나요?
      en: Can new_node pointers point to original nodes?
    type: distractor
    why:
      ko: '안 됩니다. 문제에서 명시: ''새 리스트의 어떤 포인터도 원본 리스트의 노드를 가리키면 안 됩니다.'''
      en: 'No. The problem explicitly states: ''None of the pointers in the new list should point to nodes in the original list.'''
  - q:
      ko: 원본 리스트를 수정해도 되나요?
      en: Can we modify the original list?
    type: good
    why:
      ko: 문제 문맥상 원본을 건드리지 않는 것이 권장됩니다. 공간 최적화(O(1))가 필요하지 않으면 해시맵으로 충분합니다.
      en: While not explicitly forbidden, it's safer to avoid modifying the original. Hash map approach is clean and non-destructive.
  - q:
      ko: O(n) 공간보다 더 적은 공간을 사용할 수 있나요?
      en: Can we solve this with less than O(n) space?
    type: good
    why:
      ko: 가능합니다. 원본 리스트의 next 포인터를 임시로 수정하여 'interweave' 기법을 사용하면 O(1) 공간으로 해결할 수 있습니다. 이는 고급 최적화입니다.
      en: Yes, by using the interweaving technique (temporarily modifying next pointers). This is an advanced follow-up requiring restoration.
  - q:
      ko: 딕셔너리 대신 다른 자료구조를 사용할 수 있나요?
      en: Can we use a different data structure instead of a hash map?
    type: good
    why:
      ko: 배열 인덱스가 0부터 n-1까지 순차적이면 배열을 사용할 수 있습니다. 하지만 노드 객체를 직접 사용하려면 해시맵이 가장 자연스럽습니다.
      en: If nodes have sequential indices, arrays could work. However, hash maps are most natural for mapping object references.
approach:
  items:
  - name:
      ko: 해시맵 두 번 패스
      en: Hash Map (Two-Pass)
    complexity: O(n) time / O(n) space
    type: good
    why:
      ko: 첫 번째 패스에서 모든 복사 노드를 만들고 매핑을 저장한 후, 두 번째 패스에서 포인터를 설정합니다. 구현이 직관적이고 원본 리스트를 수정하지 않습니다.
      en: First pass creates all copy nodes and stores mapping. Second pass sets pointers. Clean, straightforward, and non-destructive.
  - name:
      ko: Interweaving (O(1) 공간)
      en: Interweaving (O(1) Space-Optimized)
    complexity: O(n) time / O(1) space
    type: good
    why:
      ko: 원본 리스트의 next 포인터를 임시로 수정하여 원본과 복사본을 엮어냅니다. 원본을 복구한 후 포인터를 설정합니다. 공간 효율적이지만 구현이 복잡합니다.
      en: Interleave original and copy by modifying next pointers temporarily. Restore original after setting pointers. More complex but O(1) space.
  - name:
      ko: 재귀 DFS + 메모이제이션
      en: Recursive DFS with Memoization
    complexity: O(n) time / O(n) space
    type: distractor
    why:
      ko: 각 노드를 재귀적으로 방문하며 메모이제이션으로 중복을 방지합니다. 해시맵과 동일한 복잡도이지만 재귀 호출 스택이 추가됩니다.
      en: Recursively visit and memoize. Same complexity as hash map but adds recursion overhead and stack depth risk.
  - name:
      ko: BFS 큐 사용
      en: BFS with Queue
    complexity: O(n) time / O(n) space
    type: distractor
    why:
      ko: 큐를 사용하여 노드들을 순서대로 방문합니다. 해시맵 방식과 동일한 복잡도이지만 불필요한 자료구조 오버헤드를 추가합니다.
      en: Visit nodes using a queue. Same complexity as hash map but with unnecessary data structure overhead.
logic:
  format: slot
  slots:
  - label:
      ko: None을 포함한 매핑 초기화
      en: Initialize mapping with None key
    indent: 0
    options:
    - code: 'oldToCopy = {None: None}'
      type: good
      why:
        ko: 'null 포인터 처리를 단순화합니다. {None: None}이 없으면, null을 만날 때마다 조건 검사가 필요합니다.'
        en: 'Simplifies null pointer handling. Without {None: None}, checking for null pointers in every assignment becomes necessary.'
    - code: oldToCopy = {}
      type: distractor
      why:
        ko: 빈 딕셔너리면 null 포인터 접근 시 KeyError가 발생합니다.
        en: Empty dict causes KeyError when null pointers are accessed.
    - code: 'oldToCopy = {head: None}'
      type: distractor
      why:
        ko: 헤드만 등록하면 None 키 처리가 없고, 다른 노드들의 매핑도 없습니다.
        en: Only registers head; doesn't handle None case or provide mappings for other nodes.
  - label:
      ko: '첫 번째 패스: 모든 복사 노드 생성'
      en: 'First pass: create all copy nodes'
    indent: 0
    options:
    - code: 'while cur:'
      type: good
      why:
        ko: 원본 리스트의 모든 노드를 순회합니다. while cur:은 자동으로 None에서 멈춥니다.
        en: 'Iterate through all original nodes. The while cur: loop naturally terminates at None.'
    - code: 'while cur.next:'
      type: distractor
      why:
        ko: 마지막 노드를 처리하지 못합니다.
        en: Skips the last node of the list.
    - code: 'while cur is not None:'
      type: distractor
      why:
        ko: 기능적으로는 같지만 'while cur:'이 더 간결하고 Pythonic입니다.
        en: Functionally equivalent but less concise than 'while cur:'.
  - label:
      ko: 복사 노드 생성
      en: Create copy node
    indent: 1
    options:
    - code: copy = Node(cur.val)
      type: good
      why:
        ko: 원본의 값으로만 새 노드를 생성합니다. 포인터는 아직 설정하지 않습니다.
        en: Create a fresh node with only the value. Pointers are set later.
    - code: copy = Node(cur)
      type: distractor
      why:
        ko: 원본 노드 자체를 전달하면 얕은 복사가 됩니다.
        en: Passing the entire node object creates a shallow copy, not deep.
    - code: copy = cur
      type: distractor
      why:
        ko: 새 노드를 만들지 않고 원본을 그대로 사용합니다.
        en: Uses the original node directly without creating a new one.
  - label:
      ko: 원본-복사본 매핑 저장
      en: Store original-to-copy mapping
    indent: 1
    options:
    - code: oldToCopy[cur] = copy
      type: good
      why:
        ko: 원본 노드를 키로, 복사본 노드를 값으로 저장합니다. 두 번째 패스에서 빠른 조회를 가능하게 합니다.
        en: Store original as key, copy as value. Enables fast lookup in the second pass.
    - code: oldToCopy[copy] = cur
      type: distractor
      why:
        ko: 키와 값이 반대여서 두 번째 패스의 포인터 설정이 실패합니다.
        en: Reversed mapping breaks pointer assignment in the second pass.
    - code: oldToCopy[cur.val] = copy
      type: distractor
      why:
        ko: 값을 키로 사용하면 중복된 값을 가진 노드들이 섞입니다.
        en: Using node value creates collisions for duplicate values.
  - label:
      ko: '두 번째 패스: 포인터 설정'
      en: 'Second pass: set next and random pointers'
    indent: 0
    options:
    - code: 'while cur:'
      type: good
      why:
        ko: 매핑을 사용하여 두 번째 순회를 시작합니다. 이제 모든 복사본이 만들어졌으므로 포인터를 안전하게 설정할 수 있습니다.
        en: Use the completed mapping to set pointers. All copy nodes are created, so references are safe.
    - code: 'while cur.next:'
      type: distractor
      why:
        ko: 마지막 노드의 포인터를 설정하지 못합니다.
        en: Fails to set pointers for the last node.
    - code: 'while cur:'
      type: distractor
      why:
        ko: 이미 cur이 설정되지 않았다면 새로 설정해야 합니다. (cur = head 필요)
        en: Need to reset cur = head first; cur is already None from first loop.
  - label:
      ko: next 포인터를 매핑으로 설정
      en: Set next pointer using mapping
    indent: 1
    options:
    - code: copy.next = oldToCopy[cur.next]
      type: good
      why:
        ko: oldToCopy[cur.next]를 사용하여 원본의 다음 노드에 대응하는 복사본을 찾습니다. cur.next가 None이면 oldToCopy[None] = None을 반환합니다.
        en: Use the mapping to find the copied version of the next node. Handles null pointers seamlessly.
    - code: copy.next = cur.next
      type: distractor
      why:
        ko: 원본 노드를 직접 가리키므로 깊은 복사 요구사항을 위반합니다.
        en: Points to original nodes, violating deep copy requirement.
    - code: copy.next = oldToCopy.get(cur.next)
      type: distractor
      why:
        ko: cur.next가 oldToCopy에 없으면 None을 반환하지만, 문제의 정의상 이런 경우는 발생하지 않습니다.
        en: Unnecessary defensive coding; all next values are guaranteed to be in the map by problem definition.
  - label:
      ko: random 포인터를 매핑으로 설정
      en: Set random pointer using mapping
    indent: 1
    options:
    - code: copy.random = oldToCopy[cur.random]
      type: good
      why:
        ko: oldToCopy[cur.random]을 사용하여 원본의 random이 가리키는 노드에 대응하는 복사본을 찾습니다.
        en: 'Use mapping to find the copied node that the original''s random pointer targets. Handles null via {None: None}.'
    - code: copy.random = cur.random
      type: distractor
      why:
        ko: 원본 노드를 직접 가리키므로 깊은 복사 요구사항을 위반합니다.
        en: Points to original nodes, violating deep copy requirement.
    - code: copy.random = oldToCopy[cur].random
      type: distractor
      why:
        ko: 복사본의 random을 접근하는 것인데, 이미 방금 설정한 값을 다시 가져오는 것이므로 잘못됩니다.
        en: Accesses the copy's own random pointer, creating circular logic.
trace:
  code:
  - '"""'
  - '# Definition for a Node.'
  - 'class Node:'
  - '    def __init__(self, x: int, next: ''Node'' = None, random: ''Node'' = None):'
  - '        self.val = int(x)'
  - '        self.next = next'
  - '        self.random = random'
  - '"""'
  - ''
  - ''
  - 'class Solution:'
  - '    def copyRandomList(self, head: "Node") -> "Node":'
  - '        oldToCopy = {None: None}'
  - ''
  - '        cur = head'
  - '        while cur:'
  - '            copy = Node(cur.val)'
  - '            oldToCopy[cur] = copy'
  - '            cur = cur.next'
  - '        cur = head'
  - '        while cur:'
  - '            copy = oldToCopy[cur]'
  - '            copy.next = oldToCopy[cur.next]'
  - '            copy.random = oldToCopy[cur.random]'
  - '            cur = cur.next'
  - '        return oldToCopy[head]'
  cases:
  - input: '[[7,null],[13,0],[11,4],[10,2],[1,0]]'
    expected: '[[7,null],[13,0],[11,4],[10,2],[1,0]]'
  - input: '[[1,1],[2,1]]'
    expected: '[[1,1],[2,1]]'
  - input: '[[3,null],[3,0],[3,null]]'
    expected: '[[3,null],[3,0],[3,null]]'
  worked_example:
    input: '[[7,null],[13,0],[11,4],[10,2],[1,0]]'
    steps:
    - ko: '초기화: oldToCopy = {None: None}'
      en: 'Initialize: oldToCopy = {None: None}'
    - ko: '첫 번째 패스: 5개 노드 [7, 13, 11, 10, 1]의 복사본을 만들고 oldToCopy에 저장. 5개의 원본→복사본 매핑이 추가됨.'
      en: 'First pass: Create 5 copy nodes and store original→copy mappings. oldToCopy now has 6 entries (including None→None).'
    - ko: '두 번째 패스: 각 복사 노드의 next와 random을 설정. 예: Copy(13).next = oldToCopy[Node(13).next] = Copy(11), Copy(13).random = oldToCopy[Node(13).random] = Copy(7).'
      en: 'Second pass: Set pointers. For each copy, use mapping to find correct next and random targets. All pointers now reference copied nodes.'
    - ko: '반환: oldToCopy[head] = Copy(7), 즉 복사된 리스트의 헤드'
      en: 'Return: oldToCopy[head] = Copy(7), the head of the deep copied list.'
    answer: '[[7,null],[13,0],[11,4],[10,2],[1,0]]'
solution:
  code: "\"\"\"\n# Definition for a Node.\nclass Node:\n    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):\n        self.val = int(x)\n        self.next = next\n        self.random = random\n\"\"\"\n\n\nclass Solution:\n    def copyRandomList(self, head: \"Node\") -> \"Node\":\n        oldToCopy = {None: None}\n\n        cur = head\n        while cur:\n            copy = Node(cur.val)\n            oldToCopy[cur] = copy\n            cur = cur.next\n        cur = head\n        while cur:\n            copy = oldToCopy[cur]\n            copy.next = oldToCopy[cur.next]\n            copy.random = oldToCopy[cur.random]\n            cur = cur.next\n        return oldToCopy[head]\n"
  complexity:
    time: O(n)
    space: O(n)
  followup:
  - ko: '공간 복잡도를 O(1)로 개선할 수 있나요? (힌트: next 포인터를 이용해 원본과 복사본을 ''interweave''하기)'
    en: 'Can you optimize space complexity to O(1)? (Hint: interweave original and copy using next pointers, then restore)'
  - ko: 'random 포인터가 여러 개면 (예: neighbors)? 어떻게 확장하시겠어요?'
    en: What if nodes had multiple pointer types (e.g., child, parent)? How would you scale this approach?
  - ko: 리스트가 순환 구조라면(cyclic)? 이 알고리즘이 여전히 작동할까요?
    en: What if the list had cycles? Does this algorithm still work and how?
```