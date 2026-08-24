---
created: '2026-05-07'
date: '2026-05-07'
day: Day 04
difficulty: medium
id: A-004
source:
  curated_in:
  - neetcode150
  number: 49
  platform: leetcode
  slug: group-anagrams
  url: https://leetcode.com/problems/group-anagrams/
tags:
- array
- hash-table
- string
- sorting
title:
  en: Group Anagrams
  ko: 애너그램 그룹화
today: false
type: algorithm
updated: '2026-05-07'
visible: true
---

# 애너그램 그룹화

## Data

```yaml
problem:
  title:
    en: Group Anagrams
    ko: 애너그램 그룹화
  statement:
    en: Given an array of strings strs, group the anagrams together. You can return the answer in any order.
    ko: 문자열 배열 strs가 주어졌을 때, 애너그램끼리 그룹화하여 반환하세요. 답은 어떤 순서로든 반환할 수 있습니다.
  constraints:
  - 1 ≤ strs.length ≤ 10^4
  - 0 ≤ strs[i].length ≤ 100
  - strs[i] consists of lowercase English letters
  io:
  - input: '["eat","tea","tan","ate","nat","bat"]'
    output: '[["eat","tea","ate"],["tan","nat"],["bat"]]'
  - input: '[""]'
    output: '[[""]]'
  - input: '["a"]'
    output: '[["a"]]'
clarifying:
  items:
  - q:
      en: What makes two strings anagrams of each other?
      ko: 두 문자열이 애너그램이 되는 조건은 무엇인가요?
    type: good
    why:
      en: Understanding the definition of anagrams is fundamental to solving this problem.
      ko: 애너그램의 정의를 이해하는 것이 문제 해결의 기초입니다.
  - q:
      en: How can we create a unique signature that identifies all anagrams of a string?
      ko: 문자열의 모든 애너그램을 식별하는 고유한 서명을 어떻게 만들 수 있나요?
    type: good
    why:
      en: Finding a canonical representation directly leads to using it as a hash map key for grouping.
      ko: 표준 형태를 찾으면, 그것을 해시맵의 키로 사용하여 그룹화하는 전략이 도출됩니다.
  - q:
      en: Which data structure allows us to group strings by a shared signature efficiently?
      ko: 문자열들을 공유 서명으로 효율적으로 그룹화할 수 있는 자료구조는?
    type: good
    why:
      en: A hash map provides O(1) lookup and insertion, making it ideal for grouping by signature.
      ko: 해시맵은 O(1) 조회와 삽입을 제공하여 서명 기반 그룹화에 이상적입니다.
  - q:
      en: Does the order of groups in the output matter?
      ko: 출력에서 그룹들의 순서가 중요한가요?
    type: good
    why:
      en: The problem explicitly states 'any order', allowing us to skip unnecessary sorting.
      ko: 문제에서 '어떤 순서로든'이라고 명시했으므로, 정렬할 필요가 없습니다.
  - q:
      en: Is it necessary to sort the input array before processing?
      ko: 입력 배열을 먼저 정렬할 필요가 있나요?
    type: distractor
    why:
      en: Pre-sorting adds O(n log n) complexity with no benefit; hashing is faster and sufficient.
      ko: 사전 정렬은 O(n log n) 복잡도를 추가하지만 이점이 없습니다.
  - q:
      en: Must each group's strings be sorted before returning?
      ko: 반환 전 각 그룹의 문자열들을 정렬해야 하나요?
    type: distractor
    why:
      en: The problem doesn't require internal group sorting, so this would be unnecessary work.
      ko: 문제에서 그룹 내 정렬을 요구하지 않으므로, 이는 불필요한 작업입니다.
  - q:
      en: Can we use sorted strings as keys instead of character frequencies?
      ko: 문자 빈도 대신 정렬된 문자열을 키로 사용할 수 있나요?
    type: good
    why:
      en: Yes, sorting each string to create a canonical key is a simpler but slightly less efficient alternative.
      ko: 네, 각 문자열을 정렬하여 표준 키를 만드는 것도 유효한 대안입니다 (다만 조금 느림).
approach:
  items:
  - name:
      en: Hash map with character frequency signature
      ko: 문자 빈도 기반 해시맵
    complexity: O(n*k) time / O(n*k) space
    type: good
    why:
      en: Count character frequencies per string and use a sorted tuple as the key. Since the alphabet is fixed (26 letters), key creation is O(1), making this optimal.
      ko: 각 문자열의 문자 빈도를 세고, 정렬된 튜플을 키로 사용합니다. 알파벳이 26으로 고정되어 키 생성이 O(1)이므로 최적입니다.
  - name:
      en: Hash map with sorted string key
      ko: 정렬된 문자열 기반 해시맵
    complexity: O(n*k*log(k)) time / O(n*k) space
    type: good
    why:
      en: Sort each string to create a canonical form. More intuitive but slower due to O(k log k) sorting per string.
      ko: 각 문자열을 정렬하여 표준 형태를 만듭니다. 직관적이지만 문자열당 O(k log k) 정렬로 인해 느립니다.
  - name:
      en: Brute force with pairwise comparison
      ko: 완전 탐색 (쌍 비교)
    complexity: O(n²*k*log(k)) time / O(n*k) space
    type: distractor
    why:
      en: Comparing every pair of strings is inefficient and doesn't scale; hash-based grouping is far superior.
      ko: 모든 문자열 쌍을 비교하는 것은 비효율적입니다. 해시 기반이 훨씬 빠릅니다.
  - name:
      en: Sort input then group sequentially
      ko: 입력 정렬 후 순차 그룹화
    complexity: O(n*k*log(k) + n*k*log(n)) time / O(n*k) space
    type: distractor
    why:
      en: Pre-sorting the input adds unnecessary O(n log n) complexity without benefit.
      ko: 입력 사전 정렬은 불필요한 O(n log n) 복잡도를 추가합니다.
logic:
  format: slot
  slots:
  - label:
      en: Initialize result dictionary
      ko: 결과 딕셔너리 초기화
    indent: 0
    options:
    - code: groups = {}
      type: good
      why:
        en: Create an empty dictionary to store groups keyed by their character signature.
        ko: 문자 서명을 키로 하는 애너그램 그룹들을 저장할 빈 딕셔너리를 만듭니다.
    - code: groups = collections.defaultdict(list)
      type: distractor
      why:
        en: While functional, it hides the hash structure; explicit is better than implicit.
        ko: 작동하지만 해시 구조를 감춥니다. 명시적이 암묵적보다 낫습니다.
    - code: groups = []
      type: distractor
      why:
        en: Lists don't support string/tuple keys; we need a hash map for efficient O(1) grouping.
        ko: 리스트는 문자열/튜플 키를 지원하지 않습니다. 효율적인 그룹화를 위해 해시맵이 필요합니다.
  - label:
      en: Iterate through each string
      ko: 각 문자열을 순회
    indent: 0
    options:
    - code: 'for s in strs: # O(m)'
      type: good
      why:
        en: Process each string to extract and group its character signature.
        ko: 각 문자열을 처리하여 문자 서명을 추출하고 그룹화합니다.
    - code: 'for i in range(len(strs)): s = strs[i]'
      type: distractor
      why:
        en: Works but unnecessarily verbose; Python's for-in is more idiomatic and readable.
        ko: 작동하지만 불필요하게 장황합니다. Python의 직접 순회가 더 관용적입니다.
    - code: 'for s in strs[::-1]:'
      type: distractor
      why:
        en: Iterates in reverse, which is unnecessary since output order doesn't matter.
        ko: 역순 순회는 불필요합니다. 출력 순서가 중요하지 않기 때문입니다.
  - label:
      en: Count character frequencies
      ko: 문자 빈도 계산
    indent: 1
    options:
    - code: count[char] = count.get(char, 0) + 1
      type: good
      why:
        en: Increment count for each character using .get() to handle first occurrences automatically.
        ko: .get()을 사용하여 각 문자의 빈도를 증가시킵니다. 첫 등장을 자동으로 처리합니다.
    - code: count[char] += 1
      type: distractor
      why:
        en: Raises KeyError on first character occurrence since the key doesn't exist yet.
        ko: 첫 등장 시 KeyError가 발생합니다. 키가 아직 존재하지 않기 때문입니다.
    - code: count[char] = 1
      type: distractor
      why:
        en: Overwrites count to 1 each time, losing counts of previous character occurrences.
        ko: 매번 1로 덮어써 이전 빈도들이 손실됩니다.
  - label:
      en: Create canonical key from counts
      ko: 빈도로부터 표준 키 생성
    indent: 1
    options:
    - code: 'tup = tuple(sorted(count.items())) # O(1) because there is limited amount of possible keys in the alphabet -> O(26) + O(26*log26) + O(26)'
      type: good
      why:
        en: Convert sorted character frequencies to a tuple (hashable). All anagrams of the same string produce identical tuples.
        ko: 정렬된 문자 빈도를 튜플(해시 가능)로 변환합니다. 같은 문자열의 모든 애너그램은 동일한 튜플을 생성합니다.
    - code: tup = sorted(count.items())
      type: distractor
      why:
        en: Sorted lists are not hashable and cannot be dictionary keys in Python.
        ko: 정렬된 리스트는 해시 불가능하므로 딕셔너리 키로 사용할 수 없습니다.
    - code: tup = tuple(count.keys())
      type: distractor
      why:
        en: Only includes character names without frequencies. "aab" and "abc" would incorrectly hash to the same key.
        ko: 문자 이름만 포함하고 빈도는 미포함합니다. "aab"와 "abc"가 같은 키로 해시됩니다 (틀림).
  - label:
      en: Add string to group
      ko: 문자열을 그룹에 추가
    indent: 1
    options:
    - code: groups[tup].append(s)
      type: good
      why:
        en: Append the string to its group if the key exists. The if-else structure handles both new and existing groups correctly.
        ko: 문자열을 해당 그룹에 추가합니다. if-else는 새 그룹과 기존 그룹을 올바르게 처리합니다.
    - code: groups[tup] = [s]
      type: distractor
      why:
        en: Unconditionally overwrites the group with a single-element list, losing all previously grouped strings.
        ko: 항상 단일 요소 리스트로 덮어써 이전의 모든 문자열들이 손실됩니다.
    - code: groups.append((tup, s))
      type: distractor
      why:
        en: If groups were a list, this adds tuples, but then we lose O(1) hash table lookup for future strings.
        ko: 리스트면 튜플을 추가하지만, 이후 O(1) 해시 조회를 잃게 됩니다.
  - label:
      en: Return grouped results
      ko: 그룹화된 결과 반환
    indent: 0
    options:
    - code: return list(groups.values())
      type: good
      why:
        en: Extract all group lists (values) from the dictionary and convert to a list of lists.
        ko: 딕셔너리의 모든 그룹(값)을 추출하여 리스트의 리스트로 변환합니다.
    - code: return groups
      type: distractor
      why:
        en: Returns a dictionary, not the expected list-of-lists format required by the problem.
        ko: 딕셔너리를 반환합니다. 문제가 요구하는 리스트의 리스트 형식이 아닙니다.
    - code: return list(groups.keys())
      type: distractor
      why:
        en: Returns only the signature keys, not the actual grouped strings from the input.
        ko: 서명 키만 반환합니다. 실제 입력 문자열들이 반환되지 않습니다.
trace:
  code:
  - 'class Solution:'
  - '    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:'
  - '        groups = {}'
  - ''
  - '        # Iterate over strings'
  - '        for s in strs: # O(m)'
  - '            count = {}'
  - ''
  - '            # Count frequency of each character'
  - '            for char in s: # O(n)'
  - '                count[char] = count.get(char, 0) + 1'
  - ''
  - '            # Convert count Dict to List, sort it, and then convert to Tuple (we cannot use dicts or lists as keys in a hashmap)'
  - '            tup = tuple(sorted(count.items())) # O(1) because there is limited amount of possible keys in the alphabet -> O(26) + O(26*log26) + O(26)'
  - ''
  - '            if tup in groups:'
  - '                groups[tup].append(s)'
  - '            else:'
  - '                groups[tup] = [s] '
  - '            '
  - '        return list(groups.values())'
  - '    '
  - '    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:'
  - '        ans = collections.defaultdict(list)'
  - ''
  - '        for s in strs:'
  - '            count = [0] * 26'
  - '            for c in s:'
  - '                count[ord(c) - ord("a")] += 1'
  - '            ans[tuple(count)].append(s)'
  - '        return list(ans.values())'
  cases:
  - input: '["eat","tea","tan","ate","nat","bat"]'
    expected: '[["eat","tea","ate"],["tan","nat"],["bat"]]'
  - input: '[""]'
    expected: '[[""]]'
  - input: '["a"]'
    expected: '[["a"]]'
  worked_example:
    input: '["eat","tea","tan","ate","nat","bat"]'
    steps:
    - en: 'Process "eat": count chars {e:1, a:1, t:1}, create key K1 = ((a,1), (e,1), (t,1)). groups = {K1: ["eat"]}.'
      ko: '"eat" 처리: 문자 {e:1, a:1, t:1}, 키 K1 = ((a,1), (e,1), (t,1)) 생성. groups = {K1: ["eat"]}'
    - en: 'Process "tea" and "ate": same character frequencies, same key K1. Both append to existing group. groups = {K1: ["eat", "tea", "ate"]}.'
      ko: '"tea"와 "ate" 처리: 같은 문자 빈도, 같은 K1. groups = {K1: ["eat", "tea", "ate"]}'
    - en: 'Process "tan": count {t:1, a:1, n:1}, new key K2. groups = {K1: [...], K2: ["tan"]}.'
      ko: '"tan" 처리: 빈도 {t:1, a:1, n:1}, 새로운 키 K2. groups는 이제 2개 항목 보유'
    - en: 'Process "nat": same key K2 as "tan", append. Process "bat": unique key K3. Final: 3 anagram groups.'
      ko: '"nat" 처리: K2로 추가. "bat" 처리: K3 생성. 최종: 3개의 애너그램 그룹'
    answer: '[["eat","tea","ate"],["tan","nat"],["bat"]]'
solution:
  code: "class Solution:\n    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:\n        groups = {}\n\n        # Iterate over strings\n        for s in strs: # O(m)\n            count = {}\n\n            # Count frequency of each character\n            for char in s: # O(n)\n                count[char] = count.get(char, 0) + 1\n\n            # Convert count Dict to List, sort it, and then convert to Tuple (we cannot use dicts or lists as keys in a hashmap)\n            tup = tuple(sorted(count.items())) # O(1) because there is limited amount of possible keys in the alphabet -> O(26) + O(26*log26) + O(26)\n\n            if tup in groups:\n                groups[tup].append(s)\n            else:\n                groups[tup] = [s] \n            \n        return list(groups.values())\n    \n    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:\n        ans = collections.defaultdict(list)\n\n        for s in strs:\n            count = [0] * 26\n            for c in s:\n\
    \                count[ord(c) - ord(\"a\")] += 1\n            ans[tuple(count)].append(s)\n        return list(ans.values())\n"
  complexity:
    time: O(n*k) where n = number of strings and k = max string length
    space: O(n*k) to store all strings in output, plus O(26) for character count dictionary
  followup:
  - en: What if the input contains uppercase letters or special characters?
    ko: 입력에 대문자나 특수 문자가 포함되어 있다면?
  - en: How would you modify the solution to return only the largest anagram group?
    ko: 가장 큰 애너그램 그룹만 반환하도록 솔루션을 수정하려면?
  - en: Can you optimize space further if you're allowed to modify the input array?
    ko: 입력 배열 수정이 허용된다면 공간을 더 최적화할 수 있을까?
```