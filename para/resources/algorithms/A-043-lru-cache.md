---
created: '2026-06-18'
date: '2026-06-18'
day: Day 43
difficulty: medium
id: A-043
source:
  curated_in:
  - neetcode150
  number: 146
  platform: leetcode
  slug: lru-cache
  url: https://leetcode.com/problems/lru-cache/
tags:
- hash-table
- linked-list
- design
- doubly-linked-list
title:
  en: LRU Cache
  ko: LRU 캐시
today: false
type: algorithm
updated: '2026-06-18'
visible: true
---

# LRU 캐시

## Data

```yaml
problem:
  title:
    ko: LRU 캐시
    en: LRU Cache
  statement:
    ko: 'Least Recently Used (LRU) 캐시의 제약을 따르는 데이터 구조를 설계하세요.


      LRUCache 클래스를 구현하세요:

      - LRUCache(int capacity): 양수 크기의 capacity로 LRU 캐시를 초기화합니다.

      - int get(int key): key가 존재하면 해당 값을 반환하고, 그렇지 않으면 -1을 반환합니다.

      - void put(int key, int value): key가 존재하면 해당 값을 업데이트합니다. 그렇지 않으면 key-value 쌍을 캐시에 추가합니다. 이 작업 후 키의 개수가 capacity를 초과하면 가장 최근에 사용되지 않은 키를 제거합니다.


      get과 put 함수는 각각 O(1) 평균 시간 복잡도로 실행되어야 합니다.'
    en: 'Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.


      Implement the LRUCache class:

      - LRUCache(int capacity): Initialize the LRU cache with positive size capacity.

      - int get(int key): Return the value of the key if the key exists, otherwise return -1.

      - void put(int key, int value): Update the value of the key if the key exists. Otherwise, add the key-value pair to the cache. If the number of keys exceeds the capacity from this operation, evict the least recently used key.


      The functions get and put must each run in O(1) average time complexity.'
  constraints:
  - 1 ≤ capacity ≤ 3000
  - 0 ≤ key ≤ 10^4
  - 0 ≤ value ≤ 10^5
  - At most 2 × 10^5 calls to get() and put()
  - Both get() and put() must achieve O(1) time complexity
  io:
  - input: '["LRUCache","put","put","get","put","get","put","get","get","get"]

      [[2],[1,1],[2,2],[1],[3,3],[2],[4,4],[1],[3],[4]]'
    output: '[null, null, null, 1, null, -1, null, -1, 3, 4]'
clarifying:
  items:
  - q:
      ko: get() 작업이 캐시 순서를 변경해야 하는 이유는 무엇인가요?
      en: Why must the get() operation update the cache recency order?
    type: good
    why:
      ko: 키에 접근하는 것 자체가 '사용(access)'으로 간주되므로, 해당 키를 가장 최근에 사용된 항목으로 표시해야 합니다.
      en: Accessing a key constitutes a 'use' event, so it must be marked as recently used to correctly track LRU ordering.
  - q:
      ko: 센티널 노드(left, right)를 사용하는 목적은 무엇인가요?
      en: What is the purpose of using sentinel nodes (left, right) in the doubly-linked list?
    type: good
    why:
      ko: 센티널 노드는 리스트의 경계를 나타내므로 null 체크 없이 항상 유효한 이웃 노드가 존재합니다.
      en: Sentinel nodes serve as permanent boundary markers, eliminating null checks and edge case handling for first/last node operations.
  - q:
      ko: 해시맵과 이중연결리스트를 결합하는 이유는 무엇인가요?
      en: Why combine a hash map with a doubly-linked list instead of using just one?
    type: good
    why:
      ko: 해시맵은 O(1) 키 조회를 제공하고, 이중연결리스트는 O(1) 노드 이동을 제공하여 두 연산 모두 O(1)을 달성합니다.
      en: Hash map provides O(1) key lookup, and doubly-linked list enables O(1) node repositioning; together they achieve O(1) for both operations.
  - q:
      ko: 시간 스탬프 카운터만 사용하여 O(1) 성능을 얻을 수 있을까요?
      en: Could we use only timestamps/counters to achieve O(1) performance for both operations?
    type: distractor
    why:
      ko: 스탐프만으로는 LRU를 식별한 후 제거하기 위해 O(n) 스캔이 필요하므로 O(1) 보장이 불가능합니다.
      en: Timestamps alone require O(n) scanning to find and evict the LRU element, violating the O(1) requirement.
  - q:
      ko: put()에서 기존 키를 업데이트할 때 노드를 재삽입하지 않으면 어떻게 될까요?
      en: What happens if we update an existing key's value in put() without moving it to the right?
    type: distractor
    why:
      ko: 업데이트된 키는 실제로 가장 최근에 '사용'되었지만, 리스트에서는 여전히 오래된 위치에 있어 LRU 순서가 부정확해집니다.
      en: The updated key is functionally 'recently used' but remains in its old position, breaking LRU invariants and causing incorrect evictions.
approach:
  items:
  - name:
      ko: 해시맵 + 이중연결리스트
      en: Hash Map + Doubly-Linked List
    complexity: O(1) time / O(capacity) space
    type: good
    why:
      ko: 해시맵은 상수 시간 조회를 제공하고, 이중연결리스트는 노드를 상수 시간에 이동시켜 모든 연산이 O(1)입니다.
      en: Hash map enables O(1) key lookup, doubly-linked list allows O(1) node repositioning; both operations achieve O(1) time.
  - name:
      ko: 정렬된 딕셔너리 (타임스탐프)
      en: Sorted Dictionary with Timestamps
    complexity: O(n) time worst case / O(capacity) space
    type: distractor
    why:
      ko: 시간 스탬프 기반 정렬은 매 접근마다 스캔이 필요하거나, 정렬 순서 유지에 O(log n)의 비용이 발생합니다.
      en: Maintaining sort order requires either O(n) scanning to find LRU or O(log n) per operation, violating the O(1) requirement.
  - name:
      ko: 힙 기반 우선순위 큐
      en: Heap-Based Priority Queue
    complexity: O(log n) time / O(capacity) space
    type: distractor
    why:
      ko: 힙 삽입/삭제/감소가 각각 O(log n) 비용이 드므로 O(1) 요구사항을 충족할 수 없습니다.
      en: Heap operations (insert, delete, decrease-key) are O(log n), which exceeds the O(1) requirement.
  - name:
      ko: 배열 선형 탐색
      en: Array with Linear Search
    complexity: O(n) time / O(capacity) space
    type: distractor
    why:
      ko: 배열에서 키를 찾거나 LRU를 식별하려면 매번 O(n) 스캔이 필요합니다.
      en: Finding a key or identifying the LRU element requires O(n) linear scan each time, failing the O(1) time constraint.
logic:
  format: slot
  slots:
  - label:
      ko: 캐시 해시맵 초기화
      en: Initialize cache hash map
    indent: 0
    options:
    - code: 'self.cache = {}  # map key to node'
      type: good
      why:
        ko: 해시맵은 키에서 노드로의 상수 시간 조회를 가능하게 합니다.
        en: Hash map enables O(1) key-to-node lookup instead of scanning.
    - code: self.cache = []
      type: distractor
      why:
        ko: 배열은 키 검색에 O(n)이 필요합니다.
        en: Array requires O(n) search to find a key.
    - code: self.cache = None
      type: distractor
      why:
        ko: 저장 구조 없이 키-값 쌍을 저장할 수 없습니다.
        en: No storage structure to hold key-value mappings.
    - code: self.cache = set()
      type: distractor
      why:
        ko: set은 값을 저장할 수 없고 키만 저장합니다.
        en: Set cannot store values, only keys.
  - label:
      ko: 센티널 노드 생성
      en: Create sentinel nodes for list boundaries
    indent: 0
    options:
    - code: self.left, self.right = Node(0, 0), Node(0, 0)
      type: good
      why:
        ko: 센티널 노드는 리스트의 시작과 끝을 명시하여 모든 노드가 이전/다음 이웃을 가지므로 null 체크를 제거합니다.
        en: Sentinels serve as permanent boundary markers, ensuring every node has valid prev/next neighbors without null checks.
    - code: self.left = self.right = None
      type: distractor
      why:
        ko: 경계를 표시하는 노드가 없어 첫/마지막 노드에서 null 체크가 필요합니다.
        en: No boundary markers require null checks when handling first/last nodes.
    - code: self.left = Node(0, 0); self.right = self.left
      type: distractor
      why:
        ko: left와 right가 같은 노드이므로 리스트를 양쪽 끝으로 분할할 수 없습니다.
        en: Left and right pointing to same node prevents proper list structure.
  - label:
      ko: 노드 연결 해제 (remove)
      en: Disconnect node by updating both directional links
    indent: 0
    options:
    - code: prev.next, nxt.prev = nxt, prev
      type: good
      why:
        ko: 이전/다음 포인터를 동시에 업데이트하여 이중연결 구조를 유지합니다.
        en: Updating both prev.next and nxt.prev maintains bidirectional integrity of the doubly-linked list.
    - code: prev.next = nxt
      type: distractor
      why:
        ko: 앞쪽 링크만 업데이트하면 역방향 순회가 깨집니다.
        en: Updating only forward link breaks backward traversal.
    - code: node.prev = None; node.next = None
      type: distractor
      why:
        ko: 노드 자신만 수정하고 이웃 노드를 업데이트하지 않아 리스트가 단절됩니다.
        en: Modifying only the node without updating neighbors breaks the list structure.
    - code: nxt.prev = prev
      type: distractor
      why:
        ko: 뒤쪽 링크만 업데이트하여 리스트가 일관성을 잃습니다.
        en: Updating only backward link leaves forward links inconsistent.
  - label:
      ko: 노드를 우측 끝에 삽입 (insert)
      en: Connect node at right end (most recent position)
    indent: 0
    options:
    - code: node.next, node.prev = nxt, prev
      type: good
      why:
        ko: 노드를 우측 끝에 삽입하여 가장 최근에 접근된 항목으로 표시합니다.
        en: Inserting at the right end marks the node as most recently used in left-to-right order.
    - code: node.next, node.prev = self.left, self.left.next
      type: distractor
      why:
        ko: 좌측 끝에 삽입하면 새 노드가 가장 오래된 것으로 표시됩니다.
        en: Inserting at left end marks node as least recently used.
    - code: node.prev = self.right; node.next = None
      type: distractor
      why:
        ko: 불완전한 링크로 리스트의 순환 구조가 깨집니다.
        en: Incomplete linking breaks the circular sentinel structure.
    - code: prev.next = node
      type: distractor
      why:
        ko: 앞쪽 링크만 업데이트하면 역방향 연결이 누락됩니다.
        en: Updating only one direction breaks bidirectional traversal.
  - label:
      ko: 'Get: 노드를 제거하여 최근성 업데이트'
      en: 'Get: Remove node to update recency'
    indent: 0
    options:
    - code: self.remove(self.cache[key])
      type: good
      why:
        ko: 키 접근은 그 항목을 최근에 사용된 것으로 표시해야 하므로 먼저 제거한 후 재삽입합니다.
        en: Accessing a key must mark it as recently used, so we remove and re-insert it to move it to the right.
    - code: return self.cache[key].val
      type: distractor
      why:
        ko: 값은 반환하지만 최근성 순서를 업데이트하지 않아 LRU 정확성이 떨어집니다.
        en: Returns value but fails to update recency, breaking LRU correctness.
    - code: self.insert(self.cache[key]); return self.cache[key].val
      type: distractor
      why:
        ko: 제거 단계를 건너뛰면 노드가 중복으로 연결되어 리스트가 손상됩니다.
        en: Skipping remove causes duplicate links and corrupts the list structure.
  - label:
      ko: 'Put: left 다음의 LRU 노드 식별'
      en: 'Put: Identify LRU node as left.next'
    indent: 0
    options:
    - code: lru = self.left.next
      type: good
      why:
        ko: 센티널 left 바로 다음의 노드는 좌에서 우로의 순서에 의해 항상 가장 오래된(LRU) 항목입니다.
        en: The node immediately after the left sentinel is always the least recently used due to left-to-right ordering.
    - code: lru = self.right.prev
      type: distractor
      why:
        ko: 우측의 이전 노드는 가장 최근에 사용된 항목이므로 가장 오래된 것을 잘못 제거합니다.
        en: Right.prev is the most recent, not least recent; evicts the wrong node.
    - code: lru = self.cache[min(self.cache.keys())]
      type: distractor
      why:
        ko: 최소 키 값을 제거하는 것은 최근성 기반이 아닌 키 값 기반이므로 LRU가 아닙니다.
        en: Evicting by minimum key value is not LRU; it's based on key magnitude, not recency.
    - code: lru = list(self.cache.values())[0]
      type: distractor
      why:
        ko: 딕셔너리 순서는 삽입 시간에 기반하므로 접근 시간을 반영하지 않습니다.
        en: Dictionary insertion order doesn't track access recency and may evict wrong element.
trace:
  code:
  - 'class Node:'
  - '    def __init__(self, key, val):'
  - '        self.key, self.val = key, val'
  - '        self.prev = self.next = None'
  - ''
  - ''
  - 'class LRUCache:'
  - '    def __init__(self, capacity: int):'
  - '        self.cap = capacity'
  - '        self.cache = {}  # map key to node'
  - ''
  - '        self.left, self.right = Node(0, 0), Node(0, 0)'
  - '        self.left.next, self.right.prev = self.right, self.left'
  - ''
  - '    # remove node from list'
  - '    def remove(self, node):'
  - '        prev, nxt = node.prev, node.next'
  - '        prev.next, nxt.prev = nxt, prev'
  - ''
  - '    # insert node at right'
  - '    def insert(self, node):'
  - '        prev, nxt = self.right.prev, self.right'
  - '        prev.next = nxt.prev = node'
  - '        node.next, node.prev = nxt, prev'
  - ''
  - '    def get(self, key: int) -> int:'
  - '        if key in self.cache:'
  - '            self.remove(self.cache[key])'
  - '            self.insert(self.cache[key])'
  - '            return self.cache[key].val'
  - '        return -1'
  - ''
  - '    def put(self, key: int, value: int) -> None:'
  - '        if key in self.cache:'
  - '            self.remove(self.cache[key])'
  - '        self.cache[key] = Node(key, value)'
  - '        self.insert(self.cache[key])'
  - ''
  - '        if len(self.cache) > self.cap:'
  - '            # remove from the list and delete the LRU from hashmap'
  - '            lru = self.left.next'
  - '            self.remove(lru)'
  - '            del self.cache[lru.key]'
  cases:
  - input: '["LRUCache","put","put","get","put","get","put","get","get","get"]

      [[2],[1,1],[2,2],[1],[3,3],[2],[4,4],[1],[3],[4]]'
    expected: '[null, null, null, 1, null, -1, null, -1, 3, 4]'
  worked_example:
    input: '["LRUCache","put","put","get","put","get","put","get","get","get"]

      [[2],[1,1],[2,2],[1],[3,3],[2],[4,4],[1],[3],[4]]'
    steps:
    - ko: 'LRUCache(2) 초기화 후 put(1,1), put(2,2) 실행. 캐시={1:1, 2:2}, 리스트 순서(LRU→MRU): 1→2.'
      en: 'Initialize LRUCache(2), then put(1,1) and put(2,2). Cache={1:1, 2:2}, recency list: 1→2.'
    - ko: 'get(1)은 1을 반환하고 1을 우측 끝으로 이동. put(3,3) 시 용량 초과로 LRU 키 2 제거. 캐시={1:1, 3:3}, 순서: 1→3.'
      en: 'get(1) returns 1 and moves it to right end. put(3,3) exceeds capacity, evict LRU key 2. Cache={1:1, 3:3}, order: 1→3.'
    - ko: 'put(4,4) 시 용량 초과로 LRU 키 1 제거. 캐시={3:3, 4:4}, 순서: 3→4. get(2)→-1 (미발견).'
      en: 'put(4,4) exceeds capacity, evict LRU key 1. Cache={3:3, 4:4}, order: 3→4. get(2)→-1 (not found).'
    - ko: 'get(3)→3, get(4)→4. 최종 결과: [null, null, null, 1, null, -1, null, -1, 3, 4].'
      en: 'get(3)→3 and get(4)→4. Final answer: [null, null, null, 1, null, -1, null, -1, 3, 4].'
    answer: '[null, null, null, 1, null, -1, null, -1, 3, 4]'
solution:
  code: "class Node:\n    def __init__(self, key, val):\n        self.key, self.val = key, val\n        self.prev = self.next = None\n\n\nclass LRUCache:\n    def __init__(self, capacity: int):\n        self.cap = capacity\n        self.cache = {}  # map key to node\n\n        self.left, self.right = Node(0, 0), Node(0, 0)\n        self.left.next, self.right.prev = self.right, self.left\n\n    # remove node from list\n    def remove(self, node):\n        prev, nxt = node.prev, node.next\n        prev.next, nxt.prev = nxt, prev\n\n    # insert node at right\n    def insert(self, node):\n        prev, nxt = self.right.prev, self.right\n        prev.next = nxt.prev = node\n        node.next, node.prev = nxt, prev\n\n    def get(self, key: int) -> int:\n        if key in self.cache:\n            self.remove(self.cache[key])\n            self.insert(self.cache[key])\n            return self.cache[key].val\n        return -1\n\n    def put(self, key: int, value: int) -> None:\n        if key in\
    \ self.cache:\n            self.remove(self.cache[key])\n        self.cache[key] = Node(key, value)\n        self.insert(self.cache[key])\n\n        if len(self.cache) > self.cap:\n            # remove from the list and delete the LRU from hashmap\n            lru = self.left.next\n            self.remove(lru)\n            del self.cache[lru.key]\n"
  complexity:
    time: O(1) average per operation
    space: O(capacity)
  followup:
  - ko: 여러 스레드에서 동시에 접근할 경우 어떻게 thread-safe하게 만들까요?
    en: How would you make this thread-safe for concurrent access from multiple threads?
  - ko: 만약 capacity를 동적으로 변경할 수 있다면 어떻게 구현할까요?
    en: How would you handle dynamic capacity resizing after the cache is created?
  - ko: expiration time(TTL)을 지원하는 LRU 캐시로 확장하려면?
    en: How would you extend this to support time-based expiration (TTL) for cached entries?
```