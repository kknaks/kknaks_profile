---
created: '2026-07-14'
date: '2026-07-14'
day: Day 62
difficulty: medium
id: A-062
source:
  curated_in:
  - neetcode150
  number: 211
  platform: leetcode
  slug: design-add-and-search-words-data-structure
  url: https://leetcode.com/problems/design-add-and-search-words-data-structure/
status: draft
tags:
- string
- depth-first-search
- design
- trie
title:
  en: Design Add and Search Words Data Structure
  ko: 단어 추가 및 검색 데이터 구조 설계
today: true
type: algorithm
updated: '2026-07-14'
visible: true
---

# 단어 추가 및 검색 데이터 구조 설계

## Data

```yaml
problem:
  title:
    ko: 단어 추가 및 검색 데이터 구조 설계
    en: Design Add and Search Words Data Structure
  statement:
    ko: '새로운 단어를 추가하고 이전에 추가된 문자열과 일치하는지 확인하는 기능을 지원하는 데이터 구조를 설계하세요.


      WordDictionary 클래스를 구현하세요:

      - WordDictionary(): 객체를 초기화합니다.

      - void addWord(word): 데이터 구조에 word를 추가하며, 나중에 검색할 수 있습니다.

      - bool search(word): 데이터 구조에 word와 일치하는 문자열이 있으면 true를, 없으면 false를 반환합니다. word는 도트(''.'')를 포함할 수 있으며, 도트는 어떤 문자와도 일치할 수 있습니다.'
    en: 'Design a data structure that supports adding new words and finding if a string matches any previously added string.


      Implement the WordDictionary class:

      - WordDictionary() Initializes the object.

      - void addWord(word) Adds word to the data structure, it can be matched later.

      - bool search(word) Returns true if there is any string in the data structure that matches word or false otherwise. word may contain dots ''.'' where dots can be matched with any letter.'
  constraints:
  - 1 ≤ word.length ≤ 25
  - word in addWord consists of lowercase English letters
  - word in search consists of '.' or lowercase English letters
  - At most 2 dots in search queries
  - At most 10^4 total calls to addWord and search
  io:
  - input: '["WordDictionary","addWord","addWord","addWord","search","search","search","search"]

      [[],["bad"],["dad"],["mad"],["pad"],["bad"],[".ad"],["b.."]]'
    output: '[null, null, null, null, false, true, true, true]'
clarifying:
  items:
  - q:
      ko: search 메서드에서 도트('.')는 정확히 하나의 문자와 일치하나요, 아니면 0개 이상?
      en: Does a dot '.' in search match exactly one character, or zero or more characters?
    type: good
    why:
      ko: 와일드카드의 범위를 정확히 이해하는 것이 알고리즘 설계의 핵심입니다. 도트는 정확히 하나의 문자만 일치합니다.
      en: Understanding the exact scope of the wildcard is critical for algorithm design. A dot matches exactly one character.
  - q:
      ko: 같은 단어를 여러 번 추가할 수 있나요?
      en: Can the same word be added multiple times?
    type: good
    why:
      ko: 문제 설명에서 명시적으로 금지하지 않았지만, 트라이 구조에서 같은 단어를 다시 추가해도 이미 끝 표시가 되어있으므로 영향을 주지 않습니다.
      en: Although not explicitly prohibited, re-adding the same word to a trie has no effect since it's already marked as a word end.
  - q:
      ko: 이 문제를 해결하기 위해 트라이(Trie) 자료구조를 사용해야 하나요?
      en: Should we use a Trie data structure to solve this problem?
    type: good
    why:
      ko: 트라이는 문자열 접두사를 효율적으로 저장하고, 와일드카드 매칭을 위해 재귀적 탐색을 쉽게 구현할 수 있어 이상적입니다.
      en: A trie efficiently stores string prefixes and enables recursive DFS traversal for wildcard matching.
  - q:
      ko: search 메서드에서 도트를 만나면 모든 자식 노드를 확인해야 하나요?
      en: When encountering a dot in search, should we check all child branches?
    type: good
    why:
      ko: 도트는 어떤 문자와도 일치할 수 있으므로, 현재 노드의 모든 자식을 재귀적으로 탐색하여 하나라도 일치하면 true를 반환합니다.
      en: Since a dot matches any letter, we must recursively explore all child branches and return true if any path matches.
  - q:
      ko: HashSet만 사용하여 이 문제를 해결할 수 있나요?
      en: Can we solve this problem using only a HashSet?
    type: distractor
    why:
      ko: HashSet은 정확한 문자열 매칭에만 효율적이며, 와일드카드 패턴 매칭에는 부적합합니다. 매번 모든 단어를 확인해야 합니다.
      en: A HashSet only works for exact string matching, not wildcard patterns. It would require checking all words for every search.
  - q:
      ko: 정규식(regex)을 사용하면 이 문제를 더 간단하게 해결할 수 있나요?
      en: Would using regex make this problem simpler to solve?
    type: distractor
    why:
      ko: 정규식은 기술적으로 작동하지만, 매번 모든 단어를 정규식으로 검사해야 하므로 성능이 좋지 않습니다. 트라이는 더 효율적인 접근입니다.
      en: Regex works but requires checking all stored words on every search, which is inefficient. Trie provides better performance.
approach:
  items:
  - name:
      ko: 트라이 + DFS 재귀
      en: Trie with DFS Recursion
    complexity: 'addWord: O(L) / search: O(26^d * L) where L=word length, d=dots'
    type: good
    why:
      ko: 트라이는 단어 저장에 최적화되었고, DFS 재귀는 와일드카드를 자연스럽게 처리합니다. 각 도트에서 모든 분기를 탐색합니다.
      en: Trie is optimized for word storage, and DFS recursion naturally handles wildcards by exploring all branches at each dot position.
  - name:
      ko: 트라이 + BFS 반복
      en: Trie with BFS Iteration
    complexity: 'addWord: O(L) / search: O(26^d * L)'
    type: good
    why:
      ko: DFS와 같은 시간복잡도이지만, 반복문으로 구현하여 스택 오버플로우 위험을 줄입니다.
      en: Same complexity as DFS but uses iteration to avoid stack overflow on very deep searches.
  - name:
      ko: HashSet + 정규식
      en: HashSet with Regex
    complexity: 'addWord: O(L) / search: O(N*L) where N=number of words'
    type: distractor
    why:
      ko: 모든 저장된 단어를 정규식으로 검사해야 하므로, 단어가 많을수록 매우 느립니다.
      en: Must check all stored words with regex on every search, making it O(N) per search. Much slower than trie-based approaches.
  - name:
      ko: HashMap 목록 + 선형 탐색
      en: HashMap of Lists with Linear Search
    complexity: 'addWord: O(L) / search: O(N*L) per length-L word'
    type: distractor
    why:
      ko: 각 길이별로 단어를 저장한 후 각 단어를 확인합니다. 와일드카드 매칭이 복잡하고 성능도 좋지 않습니다.
      en: Group words by length, then check each word individually. Wildcard matching is complex and performance degrades with many words.
logic:
  format: slot
  slots:
  - label:
      ko: 트라이 루트 초기화
      en: Initialize Trie root
    indent: 0
    options:
    - code: self.root = TrieNode()
      type: good
      why:
        ko: 데이터 구조의 기초인 루트 노드를 생성합니다. 모든 추가/검색 작업이 이 루트에서 시작됩니다.
        en: Create the root node, the foundation of the entire data structure. All add/search operations start from this root.
    - code: self.root = {}
      type: distractor
      why:
        ko: 딕셔너리로 직접 루트를 만들면 word 플래그를 저장할 수 없습니다.
        en: Using a plain dict loses the ability to set the word marker; need TrieNode objects.
    - code: self.root = None
      type: distractor
      why:
        ko: None으로 초기화하면 이후에 자식 노드를 추가할 수 없습니다.
        en: Initializing to None prevents adding child nodes later.
  - label:
      ko: addWord에서 트라이 순회/구축
      en: Traverse/build trie in addWord
    indent: 1
    options:
    - code: cur = self.root
      type: good
      why:
        ko: 각 문자를 따라가며 필요한 경우 새 노드를 생성합니다. 기존 경로는 재사용하여 메모리를 절약합니다.
        en: Traverse character by character, creating nodes as needed. Reuse existing paths to save space.
    - code: "cur = self.root\nfor c in word:\n    cur.children[c] = TrieNode()"
      type: distractor
      why:
        ko: 존재하는 노드를 확인하지 않고 매번 새로 생성하면 기존 경로를 덮어쓰고 메모리를 낭비합니다.
        en: Always creating a new node overwrites existing paths and wastes memory. Must check if node exists first.
    - code: "while len(word) > 0:\n    c = word.pop(0)\n    cur.children[c] = TrieNode()"
      type: distractor
      why:
        ko: 입력 단어를 수정하면서 구축하는 것은 부작용을 일으키고 매번 새로 생성합니다.
        en: Modifying the input word and always creating new nodes violates the check-before-create pattern.
  - label:
      ko: 단어 끝 표시
      en: Mark end-of-word
    indent: 1
    options:
    - code: cur.word = True
      type: good
      why:
        ko: 마지막 노드의 word 플래그를 True로 설정합니다. 검색 시 정확히 어디서 단어가 끝나는지를 알 수 있습니다.
        en: Set the word flag on the final node. This marks where each word ends for correct search results.
    - code: self.root.word = True
      type: distractor
      why:
        ko: 루트를 표시하면 모든 단어가 루트에서 끝나는 것처럼 취급되어 잘못된 결과가 나옵니다.
        en: Marking the root incorrectly marks every word as ending there.
    - code: cur.children = True
      type: distractor
      why:
        ko: 자식 딕셔너리를 Boolean으로 덮어쓰면 이후 자식 노드를 추가할 수 없습니다.
        en: Overwriting the children dict breaks the ability to store further children.
  - label:
      ko: DFS 재귀 함수 정의
      en: Define DFS recursive function
    indent: 0
    options:
    - code: 'def dfs(j, root):'
      type: good
      why:
        ko: 중첩 함수 dfs(j, root)는 인덱스 j부터 검색을 진행하며, root는 현재 트라이 노드입니다. 와일드카드 처리에 필요한 유연성을 제공합니다.
        en: The nested dfs(j, root) function tracks position j in word and current trie node. This enables exploring all wildcard branches.
    - code: "def search(self, word: str) -> bool:\n    cur = self.root\n    for c in word:\n        if c != '.' and c not in cur.children:\n            return False\n        if c != '.':\n            cur = cur.children[c]"
      type: distractor
      why:
        ko: 반복문만으로는 도트에서 모든 분기를 탐색할 수 없습니다. 재귀 없이 와일드카드 처리가 불가능합니다.
        en: Iterative approach cannot explore all wildcard branches. Recursion is necessary for wildcard matching.
    - code: "for i, c in enumerate(word):\n    if c in cur.children:\n        cur = cur.children[c]"
      type: distractor
      why:
        ko: 기본 순회만으로는 도트를 만났을 때 모든 자식을 시도하고, 각 경로를 독립적으로 검증할 수 없습니다.
        en: Basic iteration cannot backtrack and explore alternative paths for wildcard matching.
  - label:
      ko: 도트 와일드카드 처리
      en: Handle dot wildcard
    indent: 2
    options:
    - code: 'if c == ".":'
      type: good
      why:
        ko: 도트를 만나면 현재 노드의 모든 자식을 재귀적으로 확인합니다. 하나라도 일치하면 true를 반환하고, 모두 실패하면 false를 반환합니다.
        en: When encountering a dot, recursively check all child branches. Return true if any matches, false if all fail.
    - code: "if c == '.':\n    if len(cur.children) > 0:\n        return True"
      type: distractor
      why:
        ko: 자식이 존재하기만 하면 true를 반환하는 것은 잘못된 로직입니다. 나머지 패턴도 일치해야 합니다.
        en: Just checking if children exist is wrong; we must match the rest of the pattern too.
    - code: "if c == '.':\n    for child in cur.children.values():\n        return dfs(i + 1, child)"
      type: distractor
      why:
        ko: 첫 번째 자식에서 false를 반환하면 다른 자식은 확인하지 않습니다. 모든 자식을 다 확인해야 합니다.
        en: Returning on the first child doesn't check all branches. Must check all children before returning false.
  - label:
      ko: 일반 문자 처리
      en: Handle regular character
    indent: 2
    options:
    - code: 'else:'
      type: good
      why:
        ko: 도트가 아닌 문자는 정확히 일치해야 합니다. 자식이 없으면 false, 있으면 그 자식으로 계속 탐색합니다.
        en: Non-dot characters must match exactly. If child doesn't exist, return false; otherwise continue traversing.
    - code: "if c in cur.children:\n    cur = cur.children[c]\nelse:\n    return True"
      type: distractor
      why:
        ko: 문자가 없을 때 true를 반환하는 것은 거짓 긍정을 만듭니다. false를 반환해야 합니다.
        en: Returning true when character doesn't exist creates false positives. Should return false.
    - code: cur = cur.children.get(c, cur)
      type: distractor
      why:
        ko: 없을 때 현재 노드를 유지하면 잘못된 경로를 따라갑니다. 검색 실패해야 합니다.
        en: Keeping the current node when character doesn't exist follows the wrong path. Must fail the search.
  - label:
      ko: 단어 일치 여부 반환
      en: Return word match result
    indent: 1
    options:
    - code: return cur.word
      type: good
      why:
        ko: 루프를 모두 순회한 후 현재 노드의 word 플래그를 반환합니다. 이는 정확히 이 위치에서 단어가 끝나는지를 확인합니다.
        en: After traversing the entire pattern, return the word flag. This ensures the pattern matched an actual word, not just a prefix.
    - code: return True
      type: distractor
      why:
        ko: '모든 패턴을 순회했다고 해서 단어가 있는 것은 아닙니다. 예: "bad" 추가 후 "ba."로 검색하면 "ba"는 단어가 아닙니다.'
        en: Traversing the pattern doesn't mean we found a word; e.g., 'ba' is not a word even if we traverse 'ba.'
    - code: return len(cur.children) > 0
      type: distractor
      why:
        ko: 자식이 있는지만 확인하면, 단어가 아닌 접두사도 true를 반환합니다.
        en: Checking if children exist returns true for prefixes, not just complete words.
trace:
  code:
  - 'class TrieNode:'
  - '    def __init__(self):'
  - '        self.children = {}  # a : TrieNode'
  - '        self.word = False'
  - ''
  - ''
  - 'class WordDictionary:'
  - '    def __init__(self):'
  - '        self.root = TrieNode()'
  - ''
  - '    def addWord(self, word: str) -> None:'
  - '        cur = self.root'
  - '        for c in word:'
  - '            if c not in cur.children:'
  - '                cur.children[c] = TrieNode()'
  - '            cur = cur.children[c]'
  - '        cur.word = True'
  - ''
  - '    def search(self, word: str) -> bool:'
  - '        def dfs(j, root):'
  - '            cur = root'
  - ''
  - '            for i in range(j, len(word)):'
  - '                c = word[i]'
  - '                if c == ".":'
  - '                    for child in cur.children.values():'
  - '                        if dfs(i + 1, child):'
  - '                            return True'
  - '                    return False'
  - '                else:'
  - '                    if c not in cur.children:'
  - '                        return False'
  - '                    cur = cur.children[c]'
  - '            return cur.word'
  - ''
  - '        return dfs(0, self.root)'
  cases:
  - input: '["WordDictionary","addWord","addWord","addWord","search","search","search","search"]

      [[],["bad"],["dad"],["mad"],["pad"],["bad"],[".ad"],["b.."]]'
    expected: '[null, null, null, null, false, true, true, true]'
  worked_example:
    input: '["WordDictionary","addWord","addWord","addWord","search","search","search","search"]

      [[],["bad"],["dad"],["mad"],["pad"],["bad"],[".ad"],["b.."]]'
    steps:
    - ko: WordDictionary() → 루트 노드 생성, 빈 트라이 구조 시작
      en: WordDictionary() → Create empty trie with root node
    - ko: addWord("bad"), addWord("dad"), addWord("mad") → 각각 경로 b→a→d, d→a→d, m→a→d 생성 후 끝 노드에 word=True 표시
      en: addWord('bad','dad','mad') → Build paths b→a→d, d→a→d, m→a→d with word flag set at endings
    - ko: search("pad") → p가 루트의 자식에 없음 → false 반환
      en: search('pad') → 'p' not found as child of root → return false
    - ko: search("bad") → 경로 b→a→d 추적, 최종 노드의 word=True 확인 → true 반환
      en: search('bad') → Follow b→a→d, d.word is true → return true
    - ko: search(".ad") → '.'는 루트의 모든 자식 {b,d,m} 시도, 각각 a→d 경로 검증, 모두 word=True 만족 → true 반환
      en: search('.ad') → '.' branches to b,d,m; all reach d with word=True → return true
    - ko: search("b..") → b 이동, 첫 '.'는 a의 자식들 시도, 두 번째 '.'는 d의 자식들 시도, d에서 word=True 확인 → true 반환
      en: search('b..') → Move to b, first '.' tries all of b's children (a), second '.' matches d with word=True → return true
    answer: '[null, null, null, null, false, true, true, true]'
solution:
  code: "class TrieNode:\n    def __init__(self):\n        self.children = {}  # a : TrieNode\n        self.word = False\n\n\nclass WordDictionary:\n    def __init__(self):\n        self.root = TrieNode()\n\n    def addWord(self, word: str) -> None:\n        cur = self.root\n        for c in word:\n            if c not in cur.children:\n                cur.children[c] = TrieNode()\n            cur = cur.children[c]\n        cur.word = True\n\n    def search(self, word: str) -> bool:\n        def dfs(j, root):\n            cur = root\n\n            for i in range(j, len(word)):\n                c = word[i]\n                if c == \".\":\n                    for child in cur.children.values():\n                        if dfs(i + 1, child):\n                            return True\n                    return False\n                else:\n                    if c not in cur.children:\n                        return False\n                    cur = cur.children[c]\n            return cur.word\n\
    \n        return dfs(0, self.root)\n"
  complexity:
    time: 'addWord: O(L) / search: O(26^d * L) where L=word length, d=number of dots'
    space: O(N*L) where N=number of unique words, L=average word length
  followup:
  - ko: 검색 쿼리에 많은 도트가 있으면 성능이 급격히 떨어집니다(지수적). 이를 최적화할 방법이 있을까요?
    en: Performance degrades exponentially with many dots in search queries. How would you optimize for wildcard-heavy patterns?
  - ko: 트라이 노드를 배열이나 리스트로 자식을 저장할 경우, 딕셔너리 대신 사용하는 것의 장단점은?
    en: How would implementing trie nodes with an array (26 slots) instead of a dict affect time/space complexity?
  - ko: 만약 단어 삭제(deleteWord) 메서드를 추가해야 한다면 어떻게 구현할까요? 불필요한 노드를 정리해야 하나요?
    en: How would you implement a deleteWord method? Should you clean up unused nodes to save space?
```