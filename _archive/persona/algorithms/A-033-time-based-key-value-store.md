---
created: '2026-06-08'
date: '2026-06-08'
day: Day 33
difficulty: medium
id: A-033
source:
  curated_in:
  - neetcode150
  number: 981
  platform: leetcode
  slug: time-based-key-value-store
  url: https://leetcode.com/problems/time-based-key-value-store/
status: draft
tags:
- hash-table
- string
- binary-search
- design
title:
  en: Time Based Key-Value Store
  ko: 시간 기반 키-값 저장소
today: false
type: algorithm
updated: '2026-06-08'
visible: true
---

# 시간 기반 키-값 저장소

## Data

```yaml
problem:
  title:
    ko: 시간 기반 키-값 저장소
    en: Time Based Key-Value Store
  statement:
    ko: '같은 키에 대해 서로 다른 시간에 여러 값을 저장하고, 특정 시간에 해당하는 키의 값을 검색할 수 있는 시간 기반 키-값 데이터 구조를 설계하세요.


      TimeMap 클래스를 구현하세요:

      - TimeMap() 데이터 구조의 객체를 초기화합니다.

      - void set(String key, String value, int timestamp) 주어진 시간 timestamp에서 key 키와 value 값을 저장합니다.

      - String get(String key, int timestamp) 이전에 set이 호출되었으며, timestamp_prev <= timestamp를 만족하는 값을 반환합니다. 이러한 값이 여러 개 있다면, 가장 큰 timestamp_prev와 관련된 값을 반환합니다. 값이 없으면 빈 문자열 ""을 반환합니다.'
    en: 'Design a time-based key-value data structure that can store multiple values for the same key at different time stamps and retrieve the key''s value at a certain timestamp.


      Implement the TimeMap class:

      - TimeMap() Initializes the object of the data structure.

      - void set(String key, String value, int timestamp) Stores the key key with the value value at the given time timestamp.

      - String get(String key, int timestamp) Returns a value such that set was called previously, with timestamp_prev <= timestamp. If there are multiple such values, it returns the value associated with the largest timestamp_prev. If there are no values, it returns "".'
  constraints:
  - 1 ≤ key.length, value.length ≤ 100
  - All timestamps in set() are strictly increasing
  - 1 ≤ timestamp ≤ 10^7
  - At most 2 × 10^5 calls to set() and get()
  io:
  - input: '["TimeMap","set","get","get","set","get","get"]

      [[],["foo","bar",1],["foo",1],["foo",3],["foo","bar2",4],["foo",4],["foo",5]]'
    output: '[null, null, "bar", "bar", null, "bar2", "bar2"]'
clarifying:
  items:
  - q:
      ko: 주어진 키에 대해 set() 호출이 없을 때 get()은 무엇을 반환해야 합니까?
      en: What should get() return if no set() call has been made for the given key?
    type: good
    why:
      ko: 빈 경우의 정확한 처리가 경계 조건을 올바르게 처리하는 데 중요합니다.
      en: Understanding the empty case is critical for correct boundary handling.
  - q:
      ko: 두 개의 set() 호출 사이의 타임스탐프로 get()을 호출하면 어느 값을 반환해야 합니까?
      en: If get() is called with a timestamp between two set() calls, which value should be returned?
    type: good
    why:
      ko: 이것은 '가장 큰 timestamp_prev <= timestamp' 요구사항을 이해하는지 테스트합니다.
      en: This tests whether you understand the 'largest timestamp_prev <= timestamp' requirement.
  - q:
      ko: 타임스탐프가 각 키에 대해 엄격히 증가하도록 보장됩니까?
      en: Are timestamps guaranteed to be strictly increasing for each key?
    type: good
    why:
      ko: 이 제약 조건으로 인해 정렬할 필요가 없으며 리스트에서 직접 이진 탐색을 사용할 수 있습니다.
      en: This constraint allows us to avoid sorting and use binary search directly on the list.
  - q:
      ko: 같은 키가 서로 다른 타임스탐프에서 여러 값을 가질 수 있습니까?
      en: Can the same key have multiple values at different timestamps?
    type: good
    why:
      ko: 이것은 우리가 값을 덮어쓰지 않고 각 키에 대해 시계열을 저장한다는 것을 명확히 합니다.
      en: This clarifies that we're storing a time series per key, not overwriting values.
  - q:
      ko: 값들을 저장한 후 타임스탐프를 정렬해야 합니까?
      en: Do we need to sort the timestamps after storing them?
    type: distractor
    why:
      ko: 타임스탐프가 엄격히 증가하도록 보장되므로 정렬이 불필요합니다.
      en: Sorting is unnecessary because timestamps are guaranteed to be strictly increasing.
  - q:
      ko: 정확히 같은 타임스탐프를 가진 여러 값의 경우를 처리해야 합니까?
      en: Is it necessary to handle the case where multiple values have the exact same timestamp?
    type: distractor
    why:
      ko: 타임스탐프가 엄격히 증가하기 때문에 이는 문제가 아닙니다.
      en: This is not a concern because timestamps are strictly increasing; each timestamp is unique per key.
approach:
  items:
  - name:
      ko: 해시맵 + 리스트 + 이진 탐색
      en: Hash map + List + Binary search
    complexity: O(1) set, O(log n) get
    type: good
    why:
      ko: 엄격히 증가하는 타임스탐프를 활용하여 이진 탐색으로 조건을 만족하는 최대 타임스탐프를 효율적으로 찾을 수 있습니다.
      en: Exploits strictly increasing timestamps; binary search finds the largest qualifying timestamp optimally.
  - name:
      ko: 선형 탐색 (브루트 포스)
      en: Brute force linear search
    complexity: O(1) set, O(n) get
    type: distractor
    why:
      ko: 최적화가 없으며, 각 쿼리에서 전체 리스트를 스캔합니다.
      en: No optimization; scans entire list on each query without leveraging the sorted timestamp property.
  - name:
      ko: 직접 타임스탐프 키를 사용하는 해시맵
      en: Hash map with direct timestamp keys
    complexity: O(1) set, O(1) get
    type: distractor
    why:
      ko: 이 접근 방식은 조건에 맞는 최대 타임스탐프 찾기를 효율적으로 처리하지 못합니다.
      en: Doesn't efficiently find 'largest timestamp <= query_time'; misses the problem's core requirement.
  - name:
      ko: 키당 세그먼트 트리
      en: Segment tree per key
    complexity: O(log n) set, O(log n) get
    type: distractor
    why:
      ko: 과도하게 복잡합니다. 정렬된 리스트 + 이진 탐색이 더 간단하고 같은 효율성을 제공합니다.
      en: Over-engineered; sorted array + binary search is simpler and equally efficient.
logic:
  format: slot
  slots:
  - label:
      ko: 데이터 구조 초기화
      en: Initialize data structure
    indent: 0
    options:
    - code: 'self.keyStore = {}  # key : list of [val, timestamp]'
      type: good
      why:
        ko: 해시맵을 생성하여 각 키를 [value, timestamp] 쌍의 리스트로 매핑합니다.
        en: Creates the hash map that maps each key to its list of [value, timestamp] pairs.
    - code: self.keyStore = []
      type: distractor
      why:
        ko: 리스트는 키 기반 조회를 지원하지 않습니다.
        en: A list doesn't support efficient key-based lookups.
    - code: self.keyStore = set()
      type: distractor
      why:
        ko: 세트는 순서를 보존하지 않으며 타임스탐프 정렬을 유지할 수 없습니다.
        en: A set doesn't preserve order and can't maintain timestamp ordering.
  - label:
      ko: 키 존재 여부 확인 및 초기화
      en: Check and initialize key
    indent: 1
    options:
    - code: 'if key not in self.keyStore:'
      type: good
      why:
        ko: 키가 이미 존재하는지 확인하여 새 리스트를 생성할지 결정합니다.
        en: Checks if the key doesn't exist to decide whether to create a new list.
    - code: 'if key in self.keyStore:'
      type: distractor
      why:
        ko: 논리가 반전되어 있습니다.
        en: Inverted logic; would overwrite existing lists.
    - code: 'if self.keyStore.get(key):'
      type: distractor
      why:
        ko: 공 리스트는 거짓으로 평가되므로 기존 빈 리스트를 덮어쓸 수 있습니다.
        en: Empty list evaluates to False, risking unintended overwrite.
  - label:
      ko: 값-타임스탐프 쌍 추가
      en: Append value-timestamp pair
    indent: 1
    options:
    - code: self.keyStore[key].append([value, timestamp])
      type: good
      why:
        ko: 값과 타임스탐프를 함께 저장합니다. 타임스탐프가 증가하도록 보장되므로 정렬할 필요가 없습니다.
        en: Stores both value and timestamp together; guaranteed increasing order means no sorting needed.
    - code: self.keyStore[key] = [value, timestamp]
      type: distractor
      why:
        ko: 값을 덮어쓰므로 이전 기록을 잃게 됩니다.
        en: Overwrites instead of appending, losing all previous records.
    - code: self.keyStore[key].append(value)
      type: distractor
      why:
        ko: 타임스탐프 정보를 잃어 나중에 쿼리할 수 없습니다.
        en: Loses timestamp information needed for queries.
  - label:
      ko: 검색 초기화 및 값 리스트 조회
      en: Initialize search and retrieve values
    indent: 0
    options:
    - code: res, values = "", self.keyStore.get(key, [])
      type: good
      why:
        ko: 키의 값 리스트를 가져옵니다. 결과를 빈 문자열로 초기화하여 '값 없음' 경우를 처리합니다.
        en: Gets the list of values for the key; initializes result as empty string for the 'no value' case.
    - code: res, values = None, self.keyStore.get(key, [])
      type: distractor
      why:
        ko: None은 문제에서 요구하는 빈 문자열이 아닙니다.
        en: None is not the empty string required by the problem.
    - code: values = self.keyStore[key]
      type: distractor
      why:
        ko: 키가 존재하지 않으면 KeyError가 발생합니다.
        en: Raises KeyError if the key doesn't exist.
  - label:
      ko: 이진 탐색 경계 설정
      en: Set binary search bounds
    indent: 0
    options:
    - code: l, r = 0, len(values) - 1
      type: good
      why:
        ko: 엄격히 증가하는 타임스탐프에 대해 이진 탐색을 수행하기 위해 포인터를 초기화합니다.
        en: Initializes left and right pointers for binary search over strictly increasing timestamps.
    - code: l, r = 0, len(values)
      type: distractor
      why:
        ko: 범위를 벗어난 오류입니다. 마지막 유효 인덱스는 len(values) - 1입니다.
        en: Off-by-one error; last valid index is len(values) - 1.
    - code: l, r = 1, len(values) - 1
      type: distractor
      why:
        ko: 첫 번째 요소를 건너뛰며, 첫 번째 타임스탐프의 값을 찾을 수 없습니다.
        en: Skips the first element, potentially missing an answer at index 0.
  - label:
      ko: '이진 탐색: 조건 맞는 최대 타임스탐프 찾기'
      en: 'Binary search: Find largest timestamp <= query'
    indent: 1
    options:
    - code: 'if values[m][1] <= timestamp:'
      type: good
      why:
        ko: 현재 타임스탐프가 조건을 만족하면 결과를 업데이트하고 오른쪽 절반에서 더 큰 타임스탐프를 탐색합니다.
        en: If current timestamp fits, update result and search right; otherwise search left.
    - code: 'if values[m][1] < timestamp:'
      type: distractor
      why:
        ko: 엄격한 부등호는 정확히 일치하는 타임스탐프의 값을 놓칩니다.
        en: Strict inequality misses exact timestamp matches.
    - code: 'if values[m][0] <= timestamp:'
      type: distractor
      why:
        ko: 값이 아닌 타임스탐프를 비교해야 합니다. (인덱스 0은 값, 인덱스 1은 타임스탐프)
        en: Compares value instead of timestamp; values[m][0] is the value, [1] is the timestamp.
trace:
  code:
  - 'class TimeMap:'
  - '    def __init__(self):'
  - '        """'
  - '        Initialize your data structure here.'
  - '        """'
  - '        self.keyStore = {}  # key : list of [val, timestamp]'
  - ''
  - '    def set(self, key: str, value: str, timestamp: int) -> None:'
  - '        if key not in self.keyStore:'
  - '            self.keyStore[key] = []'
  - '        self.keyStore[key].append([value, timestamp])'
  - ''
  - '    def get(self, key: str, timestamp: int) -> str:'
  - '        res, values = "", self.keyStore.get(key, [])'
  - '        l, r = 0, len(values) - 1'
  - '        while l <= r:'
  - '            m = (l + r) // 2'
  - '            if values[m][1] <= timestamp:'
  - '                res = values[m][0]'
  - '                l = m + 1'
  - '            else:'
  - '                r = m - 1'
  - '        return res'
  cases:
  - input: '["TimeMap","set","get","get","set","get","get"]

      [[],["foo","bar",1],["foo",1],["foo",3],["foo","bar2",4],["foo",4],["foo",5]]'
    expected: '[null, null, "bar", "bar", null, "bar2", "bar2"]'
  worked_example:
    input: '["TimeMap","set","get","get","set","get","get"]

      [[],["foo","bar",1],["foo",1],["foo",3],["foo","bar2",4],["foo",4],["foo",5]]'
    steps:
    - ko: 'TimeMap() 객체 생성 및 빈 해시맵 초기화: keyStore = {}'
      en: 'Create TimeMap() and initialize empty hash map: keyStore = {}'
    - ko: 'set(''foo'', ''bar'', 1): ''foo'' 키에 [[''bar'', 1]] 저장. keyStore = {''foo'': [[''bar'', 1]]}'
      en: 'set(''foo'', ''bar'', 1): Store [[''bar'', 1]] for key ''foo''. keyStore = {''foo'': [[''bar'', 1]]}'
    - ko: 'get(''foo'', 1) 및 get(''foo'', 3): 리스트 [[''bar'', 1]]에서 이진 탐색. 쿼리 1에서 타임스탐프 1과 정확히 일치하여 ''bar'' 반환. 쿼리 3에서 3 이하의 최대 타임스탐프는 1이므로 ''bar'' 반환.'
      en: 'get(''foo'', 1) and get(''foo'', 3): Binary search in [[''bar'', 1]]. Query 1: exact match, return ''bar''. Query 3: largest timestamp ≤ 3 is 1, return ''bar''.'
    - ko: 'set(''foo'', ''bar2'', 4): [[''bar2'', 4]]를 ''foo''에 추가. keyStore = {''foo'': [[''bar'', 1], [''bar2'', 4]]}'
      en: 'set(''foo'', ''bar2'', 4): Append [[''bar2'', 4]] to ''foo''. keyStore = {''foo'': [[''bar'', 1], [''bar2'', 4]]}'
    - ko: 'get(''foo'', 4) 및 get(''foo'', 5): 리스트 [[''bar'', 1], [''bar2'', 4]]에서 이진 탐색. 쿼리 4에서 타임스탐프 4와 정확히 일치하여 ''bar2'' 반환. 쿼리 5에서 5 이하의 최대 타임스탐프는 4이므로 ''bar2'' 반환.'
      en: 'get(''foo'', 4) and get(''foo'', 5): Binary search in [[''bar'', 1], [''bar2'', 4]]. Query 4: exact match, return ''bar2''. Query 5: largest timestamp ≤ 5 is 4, return ''bar2''.'
    answer: '[null, null, "bar", "bar", null, "bar2", "bar2"]'
solution:
  code: "class TimeMap:\n    def __init__(self):\n        \"\"\"\n        Initialize your data structure here.\n        \"\"\"\n        self.keyStore = {}  # key : list of [val, timestamp]\n\n    def set(self, key: str, value: str, timestamp: int) -> None:\n        if key not in self.keyStore:\n            self.keyStore[key] = []\n        self.keyStore[key].append([value, timestamp])\n\n    def get(self, key: str, timestamp: int) -> str:\n        res, values = \"\", self.keyStore.get(key, [])\n        l, r = 0, len(values) - 1\n        while l <= r:\n            m = (l + r) // 2\n            if values[m][1] <= timestamp:\n                res = values[m][0]\n                l = m + 1\n            else:\n                r = m - 1\n        return res\n"
  complexity:
    time: O(1) set, O(log n) get where n = number of values for each key
    space: O(n) where n = total number of set() calls
  followup:
  - ko: 타임스탐프가 엄격히 증가하지 않는다면 어떻게 처리하시겠습니까?
    en: How would you handle the case where timestamps are not strictly increasing?
  - ko: 특정 (key, timestamp) 쌍을 삭제해야 한다면 어떻게 수정하시겠습니까?
    en: How would you modify the solution to support deleting a (key, timestamp) pair?
  - ko: get() 호출이 set() 호출보다 훨씬 더 많이 이루어진다면 추가 최적화가 가능합니까?
    en: Can you optimize the solution if get() is called much more frequently than set()?
```