---
created: '2026-08-25'
date: '2026-08-25'
day: Day 97
difficulty: hard
id: A-097
source:
  curated_in:
  - neetcode150
  number: 269
  platform: leetcode
  slug: alien-dictionary
  url: https://leetcode.com/problems/alien-dictionary/
status: draft
tags:
- array
- string
- depth-first-search
- breadth-first-search
- graph
- topological-sort
- directed-acyclic-graph
title:
  en: Alien Dictionary
  ko: 외계인 사전
today: true
type: algorithm
updated: '2026-08-25'
visible: true
---

# 외계인 사전

## Data

```yaml
problem:
  title:
    ko: 외계인 사전
    en: Alien Dictionary
  statement:
    ko: '외계인 언어로 쓰인 단어들의 정렬된 목록이 주어진다. 이 외계인 언어에서 문자들의 순서(알파벳 순서)를 결정하라.


      예를 들어, 외계인 언어에서 문자 순서가 "wertf"일 때, ["wrt", "wrf", "er", "ett", "rftt"]가 정렬된 순서가 된다.


      만약 유효한 문자 순서가 없으면 빈 문자열을 반환하라. 예를 들어, 입력이 ["z", "x", "z"]라면 "z"가 "x"보다 나오고 동시에 "x"가 "z"보다 나와야 하므로 불가능하다.'
    en: 'Given a sorted list of words in an alien language, determine the order of characters in the alien alphabet. In the alien language, characters follow a specific order that is different from the English alphabet.


      For example, if the alien alphabet order is "wertf", then the words ["wrt", "wrf", "er", "ett", "rftt"] would appear in sorted order.


      Return a string representing the character order in the alien language. If no valid character order exists (i.e., the input is contradictory or forms a cycle), return an empty string.'
  constraints:
  - 1 ≤ words.length ≤ 100
  - 1 ≤ words[i].length ≤ 20
  - words[i] contains only lowercase English letters
  - The input is already sorted according to the alien language order
  io:
  - input: '["wrt","wrf","er","ett","rftt"]'
    output: wertf
  - input: '["z","x"]'
    output: zx
  - input: '["z","x","z"]'
    output: ''
clarifying:
  items:
  - q:
      ko: 어떻게 단어 목록에서 문자의 순서를 결정하나?
      en: How do we determine character order from a list of sorted words?
    type: good
    why:
      ko: 연속된 단어들을 비교하여 첫 번째로 다른 문자를 찾으면, 그 관계가 순서를 정의한다.
      en: By comparing consecutive words and finding the first differing character, we establish the ordering relationship between those two characters.
  - q:
      ko: 만약 한 단어가 다른 단어의 접두사이면서 뒤에 나오면 어떻게 되나?
      en: What if a word is a prefix of another word but appears later in the list?
    type: good
    why:
      ko: '이는 불가능한 순서를 의미하므로 빈 문자열을 반환해야 한다. 예: ["ab", "a"]에서는 불가능'
      en: This is an invalid ordering because a longer word cannot come before its prefix in a valid dictionary. Return an empty string in this case.
  - q:
      ko: 순환 의존성을 어떻게 감지하나?
      en: How do we detect cycles in the character ordering?
    type: good
    why:
      ko: DFS 중 현재 경로에 있는 노드를 다시 방문하면 순환이 있음을 의미한다. 방문 상태를 True(진행 중), False(완료)로 추적한다.
      en: 'Using DFS with state tracking: mark a node as True when entering, and False when exiting. If we encounter a node marked True, we''ve found a cycle.'
  - q:
      ko: 모든 단어 쌍을 비교해야 하나?
      en: Do we need to compare all pairs of words?
    type: distractor
    why:
      ko: 아니다. 연속된 단어들만 비교하면 된다. 목록이 이미 정렬되어 있으므로 인접한 쌍의 순서만 확인하면 충분하다.
      en: No. Since the words are already sorted according to the alien alphabet, we only need to compare adjacent pairs. All other constraints are implied by transitivity.
  - q:
      ko: 외계인 언어에서 모든 영문자가 사용되나?
      en: Must all 26 letters appear in the character order?
    type: distractor
    why:
      ko: 아니다. 입력에서 나타나는 문자들만 포함하면 된다. 나타나지 않은 문자는 결과에 포함될 필요가 없다.
      en: No. Only the characters that appear in the input words need to be included in the result. Unused characters can be omitted.
  - q:
      ko: 여러 개의 유효한 순서가 있을 수 있나?
      en: Can there be multiple valid character orders?
    type: distractor
    why:
      ko: 예, 일부 문자들 사이의 순서가 명시되지 않을 수 있다. 문제는 유효한 순서 하나를 반환하면 된다.
      en: Yes, possible. If the ordering between some characters is not constrained by the input, multiple valid orderings exist. Returning any one of them is acceptable.
approach:
  items:
  - name:
      ko: 그래프 구축 + 위상 정렬 (DFS)
      en: Graph Construction + Topological Sort (DFS)
    complexity: O(N + C + E) where N = total chars, C = unique chars, E = edges
    type: good
    why:
      ko: 연속된 단어 쌍에서 순서 관계를 그래프로 구축하고, DFS를 사용한 위상 정렬로 순환을 감지하면서 올바른 순서를 찾는다.
      en: Build a directed graph from consecutive word pairs (each edge represents a character ordering constraint), then use DFS-based topological sort to detect cycles and find a valid ordering.
  - name:
      ko: 그래프 구축 + 위상 정렬 (BFS/Kahn)
      en: Graph Construction + Topological Sort (BFS/Kahn's Algorithm)
    complexity: O(N + C + E) where N = total chars, C = unique chars, E = edges
    type: good
    why:
      ko: DFS 대신 BFS 기반 위상 정렬(Kahn의 알고리즘)을 사용할 수 있다. 진입 차수를 추적하여 순환을 감지하고 순서를 결정한다.
      en: 'Alternative to DFS: use Kahn''s algorithm with in-degree tracking. Process nodes with in-degree 0, and if any node remains after processing all, a cycle exists.'
  - name:
      ko: 전수 비교 + 정렬
      en: All-Pairs Comparison + Sorting
    complexity: O(W² × L log W) where W = number of words, L = max word length
    type: distractor
    why:
      ko: 모든 단어 쌍을 비교하여 순서 관계를 도출하는 방식. 비효율적이고 위상 정렬 문제의 본질을 놓친다.
      en: Compare every pair of words to infer ordering, then sort. This is inefficient (quadratic) and doesn't properly model the topological sorting problem.
  - name:
      ko: 단순 어휘 재정렬
      en: Simple Lexicographic Re-sorting
    complexity: O(N log N) for sorting but incorrect
    type: distractor
    why:
      ko: 입력을 그냥 정렬하면 되나라고 생각하는 오류. 우리는 미지의 외계인 알파벳 순서를 찾아야 하는데, 단순 비교로는 불가능하다.
      en: Attempting to sort the words again using standard comparison doesn't solve the problem. We need to extract the alien alphabet order from the input, not re-sort it.
logic:
  format: slot
  slots:
  - label:
      ko: 그래프 초기화 (모든 문자 포함)
      en: Initialize graph with all characters
    indent: 0
    options:
    - code: 'adj = {char: set() for word in words for char in word}'
      type: good
      why:
        ko: 입력의 모든 고유 문자를 그래프 노드로 생성. 각 문자는 빈 인접 집합으로 시작하여 나중에 엣지가 추가된다.
        en: Create a graph node for each unique character in the input, initialized with an empty adjacency set. Ensures all characters appear in the result.
    - code: adj = {}
      type: distractor
      why:
        ko: 빈 딕셔너리에서 시작하면 나중에 새로운 문자를 추가할 때 KeyError 위험이 있다.
        en: Starting with empty dict risks KeyError when adding edges to non-existent character nodes.
    - code: 'adj = {chr(ord(''a'') + i): set() for i in range(26)}'
      type: distractor
      why:
        ko: 입력에 없는 모든 26글자를 포함하면 불필요한 메모리를 낭비하고 결과를 오염시킨다.
        en: Including all 26 letters wastes space and includes unused characters in the result.
  - label:
      ko: 연속 단어 쌍 순회
      en: Iterate through consecutive word pairs
    indent: 0
    options:
    - code: 'for i in range(len(words) - 1):'
      type: good
      why:
        ko: 정렬된 입력에서 인접한 두 단어만 비교하면 모든 필요한 순서 관계를 얻을 수 있다.
        en: Since the input is already sorted, comparing only adjacent pairs is sufficient to extract all character ordering constraints.
    - code: "for i in range(len(words)):\n    for j in range(i + 1, len(words)):"
      type: distractor
      why:
        ko: 모든 쌍을 비교하면 O(n²) 시간이 걸리고 불필요한 반복이 많다.
        en: Comparing all pairs is O(n²) and unnecessary—transitivity means adjacent pairs suffice.
  - label:
      ko: '유효성 검사: 접두사 순서 확인'
      en: 'Validate: check if longer word comes after its prefix'
    indent: 1
    options:
    - code: 'if len(w1) > len(w2) and w1[:minLen] == w2[:minLen]:'
      type: good
      why:
        ko: 한 단어가 다른 단어의 접두사이면서 뒤에 나오면 불가능한 순서이므로, 이를 조기에 감지하여 빈 문자열을 반환한다.
        en: If a longer word comes after its prefix, the input is contradictory. Detect this early and return empty string to indicate invalid input.
    - code: 'if len(w1) > len(w2):'
      type: distractor
      why:
        ko: 길이 비교만으로는 부족하다. w1이 실제로 w2의 접두사인지도 확인해야 한다.
        en: Length check alone isn't sufficient—must verify w1 actually starts with w2.
  - label:
      ko: 첫 다른 문자 찾기 및 엣지 추가
      en: Find first differing character and add directed edge
    indent: 1
    options:
    - code: 'for j in range(minLen):'
      type: good
      why:
        ko: 각 쌍에서 첫 번째로 다른 위치의 문자 관계를 엣지로 그래프에 추가. break로 다음 쌍으로 이동.
        en: For each pair, find the first position where they differ and add a directed edge from the first character to the second. Break immediately—one constraint per pair.
    - code: "for j in range(len(w1)):\n    if w1[j] != w2[j]:\n        adj[w1[j]].add(w2[j])"
      type: distractor
      why:
        ko: break가 없으면 같은 쌍에서 여러 엣지가 추가될 가능성이 있다.
        en: Without break, multiple edges could be added for the same pair (though set handles duplicates).
  - label:
      ko: 방문 상태 맵 초기화
      en: Initialize visited state map for cycle detection
    indent: 0
    options:
    - code: 'visited = {}  # {char: bool} False visited, True current path'
      type: good
      why:
        ko: visited 딕셔너리에서 True는 '현재 DFS 경로 상'을, False는 '완전히 처리됨'을 의미. 순환 감지를 위해 필수.
        en: Use a dict where True = 'in current DFS path', False = 'fully processed'. This dual-state tracking enables cycle detection.
    - code: visited = set()
      type: distractor
      why:
        ko: 단순 set으로는 '현재 경로 중'과 '완료' 상태를 구분할 수 없어 순환 감지가 작동하지 않는다.
        en: A simple set can't distinguish between 'in current path' and 'fully processed', breaking cycle detection logic.
  - label:
      ko: 'DFS: 순환 감지 및 위상 정렬'
      en: DFS with cycle detection and post-order appending
    indent: 0
    options:
    - code: 'def dfs(char):'
      type: good
      why:
        ko: DFS 진입 시 True, 퇴출 시 False로 표시. 이미 True인 노드를 방문하면 순환 발견. 퇴출 시 결과에 추가하면 역위상 정렬 순서 얻음.
        en: Mark True on entry, False on exit. Revisiting a True node indicates a cycle. Post-order appending gives reverse topological order (must reverse later).
    - code: "visited = set()\nif char in visited:\n    return False\nvisited.add(char)\nfor neighChar in adj[char]:\n    if not dfs(neighChar):\n        return False\nres.append(char)\nreturn True"
      type: distractor
      why:
        ko: 단순 set을 사용하면 '현재 경로' 상태를 추적할 수 없으므로 실제 순환을 감지하지 못한다.
        en: A simple set can't track nodes currently in the path, so this fails to detect actual cycles.
  - label:
      ko: 모든 문자에서 DFS 실행 및 순환 확인
      en: Run DFS from all unvisited characters, check for cycles
    indent: 0
    options:
    - code: 'for char in adj:'
      type: good
      why:
        ko: 그래프의 모든 노드에서 DFS를 시작하여 모든 경로를 탐색. 순환 발견 시 (반환값 True) 즉시 빈 문자열 반환.
        en: Start DFS from each unvisited character to ensure all graph components are explored. If any DFS returns True (cycle found), immediately return empty string.
    - code: "for char in adj:\n    dfs(char)"
      type: distractor
      why:
        ko: 모든 문자에 대해 항상 DFS를 호출하면 이미 방문한 노드를 불필요하게 다시 처리하게 된다.
        en: Always calling DFS on every character re-processes already-visited nodes and is inefficient (though results would still be correct).
  - label:
      ko: 결과 역순 처리 및 반환
      en: Reverse result and return final answer
    indent: 0
    options:
    - code: res.reverse()
      type: good
      why:
        ko: DFS post-order 순서는 위상 정렬의 역순이므로, 역순 처리하면 올바른 위상 순서(외계인 알파벳)를 얻는다.
        en: DFS post-order gives reverse topological order. Reversing yields the correct topological order—the alien alphabet sequence.
    - code: return ''.join(res)
      type: distractor
      why:
        ko: 역순 처리 없이 반환하면 문자의 순서가 완전히 반대가 된다.
        en: Without reversing, the character order would be completely inverted.
trace:
  code:
  - 'class Solution:'
  - '    def alienOrder(self, words: List[str]) -> str:'
  - '        adj = {char: set() for word in words for char in word}'
  - ''
  - '        for i in range(len(words) - 1):'
  - '            w1, w2 = words[i], words[i + 1]'
  - '            minLen = min(len(w1), len(w2))'
  - '            if len(w1) > len(w2) and w1[:minLen] == w2[:minLen]:'
  - '                return ""'
  - '            for j in range(minLen):'
  - '                if w1[j] != w2[j]:'
  - '                    print(w1[j], w2[j])'
  - '                    adj[w1[j]].add(w2[j])'
  - '                    break'
  - ''
  - '        visited = {}  # {char: bool} False visited, True current path'
  - '        res = []'
  - ''
  - '        def dfs(char):'
  - '            if char in visited:'
  - '                return visited[char]'
  - ''
  - '            visited[char] = True'
  - ''
  - '            for neighChar in adj[char]:'
  - '                if dfs(neighChar):'
  - '                    return True'
  - ''
  - '            visited[char] = False'
  - '            res.append(char)'
  - ''
  - '        for char in adj:'
  - '            if dfs(char):'
  - '                return ""'
  - ''
  - '        res.reverse()'
  - '        return "".join(res)'
  cases:
  - input: '["wrt","wrf","er","ett","rftt"]'
    expected: wertf
  - input: '["z","x"]'
    expected: zx
  - input: '["z","x","z"]'
    expected: ''
  worked_example:
    input: '["wrt","wrf","er","ett","rftt"]'
    steps:
    - ko: '그래프 초기화: 모든 문자 {w, r, t, f, e}를 노드로 생성, 빈 인접 집합으로 시작'
      en: 'Initialize graph: create nodes for all characters {w, r, t, f, e} with empty adjacency sets'
    - ko: '"wrt" vs "wrf" 비교: 인덱스 2에서 첫 다름 (t vs f) → 엣지 t→f 추가'
      en: 'Compare "wrt" vs "wrf": differ at index 2 (t vs f) → add edge t→f'
    - ko: '"wrf" vs "er" 비교: 인덱스 0에서 첫 다름 (w vs e) → 엣지 w→e 추가'
      en: 'Compare "wrf" vs "er": differ at index 0 (w vs e) → add edge w→e'
    - ko: '"er" vs "ett" 비교: 인덱스 1에서 첫 다름 (r vs t) → 엣지 r→t 추가'
      en: 'Compare "er" vs "ett": differ at index 1 (r vs t) → add edge r→t'
    - ko: '"ett" vs "rftt" 비교: 인덱스 0에서 첫 다름 (e vs r) → 엣지 e→r 추가'
      en: 'Compare "ett" vs "rftt": differ at index 0 (e vs r) → add edge e→r'
    - ko: 'DFS 위상 정렬: w에서 시작 → e → r → t → f 순서 방문. 퇴출 시 결과에 추가 후 역순 처리'
      en: 'Topological sort via DFS from w: visit order w→e→r→t→f. Append in post-order, then reverse to get "wertf"'
    answer: wertf
solution:
  code: "class Solution:\n    def alienOrder(self, words: List[str]) -> str:\n        adj = {char: set() for word in words for char in word}\n\n        for i in range(len(words) - 1):\n            w1, w2 = words[i], words[i + 1]\n            minLen = min(len(w1), len(w2))\n            if len(w1) > len(w2) and w1[:minLen] == w2[:minLen]:\n                return \"\"\n            for j in range(minLen):\n                if w1[j] != w2[j]:\n                    print(w1[j], w2[j])\n                    adj[w1[j]].add(w2[j])\n                    break\n\n        visited = {}  # {char: bool} False visited, True current path\n        res = []\n\n        def dfs(char):\n            if char in visited:\n                return visited[char]\n\n            visited[char] = True\n\n            for neighChar in adj[char]:\n                if dfs(neighChar):\n                    return True\n\n            visited[char] = False\n            res.append(char)\n\n        for char in adj:\n            if dfs(char):\n\
    \                return \"\"\n\n        res.reverse()\n        return \"\".join(res)\n"
  complexity:
    time: O(N) where N = sum of all word lengths (build graph + DFS on chars)
    space: O(1) or O(26) = O(1) since at most 26 lowercase English letters
  followup:
  - ko: 입력이 매우 크고 메모리 제약이 있다면? 단어를 스트리밍으로 처리할 수 있나?
    en: If the input is very large with memory constraints, can we process words in a streaming fashion without storing all of them?
  - ko: DFS 대신 BFS 기반 위상 정렬(Kahn 알고리즘)로 구현할 수 있나? 장단점은?
    en: Can you implement this using BFS-based topological sort (Kahn's algorithm)? What are the pros and cons compared to DFS?
  - ko: 여러 개의 유효한 답이 있을 때, 사전식 순서(lexicographically smallest)로 선택할 수 있나?
    en: If multiple valid solutions exist, can we select the lexicographically smallest one? How would the algorithm change?
```