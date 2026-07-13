---
created: '2026-07-13'
date: '2026-07-13'
day: Day 61
difficulty: medium
id: A-061
source:
  curated_in:
  - neetcode150
  number: 208
  platform: leetcode
  slug: implement-trie-prefix-tree
  url: https://leetcode.com/problems/implement-trie-prefix-tree/
status: draft
tags:
- hash-table
- string
- design
- trie
title:
  en: Implement Trie (Prefix Tree)
  ko: 트라이(접두사 트리) 구현
today: true
type: algorithm
updated: '2026-07-13'
visible: true
---

# 트라이(접두사 트리) 구현

## Data

```yaml
problem:
  title:
    ko: 트라이(접두사 트리) 구현
    en: Implement Trie (Prefix Tree)
  statement:
    ko: '트라이(트라이라고 발음하며 "prefix tree"라고도 불림)는 문자열 데이터셋에서 키를 효율적으로 저장하고 검색하기 위한 트리 데이터 구조입니다. 자동 완성(autocomplete)과 철자 검사(spellchecker) 등 다양한 애플리케이션에서 활용됩니다.


      Trie 클래스를 구현하세요:

      - Trie(): 트라이 객체를 초기화합니다.

      - void insert(String word): 문자열 word를 트라이에 삽입합니다.

      - boolean search(String word): 문자열 word가 트라이에 있으면 true를 반환하고, 없으면 false를 반환합니다. (즉, 이전에 삽입된 word여야 합니다)

      - boolean startsWith(String prefix): 이전에 삽입된 문자열 중에서 prefix로 시작하는 문자열이 있으면 true를 반환하고, 없으면 false를 반환합니다.'
    en: 'A trie (pronounced as "try") or prefix tree is a tree data structure used to efficiently store and retrieve keys in a dataset of strings. There are various applications of this data structure, such as autocomplete and spellchecker.


      Implement the Trie class:

      - Trie() Initializes the trie object.

      - void insert(String word) Inserts the string word into the trie.

      - boolean search(String word) Returns true if the string word is in the trie (i.e., was inserted before), and false otherwise.

      - boolean startsWith(String prefix) Returns true if there is a previously inserted string word that has the prefix prefix, and false otherwise.'
  constraints:
  - 1 ≤ word.length, prefix.length ≤ 2000
  - word and prefix consist only of lowercase English letters
  - At most 3 * 10^4 calls in total will be made to insert, search, and startsWith
  io:
  - input: '["Trie","insert","search","search","startsWith","insert","search"]

      [[],["apple"],["apple"],["app"],["app"],["app"],["app"]]'
    output: '[null, null, true, false, true, null, true]'
clarifying:
  items:
  - q:
      ko: search() 메서드와 startsWith() 메서드의 차이는 무엇인가요?
      en: What is the difference between search() and startsWith() methods?
    type: good
    why:
      ko: search()는 정확한 단어의 존재 여부를 확인하고, startsWith()는 접두사로 시작하는 어떤 단어가 존재하는지만 확인합니다. 예를 들어 "apple"을 삽입한 후 search("app")는 false이지만 startsWith("app")는 true입니다.
      en: search() checks if an exact word exists, while startsWith() only checks if any word starts with the given prefix. For example, after inserting "apple", search("app") returns false but startsWith("app") returns true.
  - q:
      ko: 노드에서 어떻게 단어의 끝을 표시해야 하나요?
      en: How should we mark the end of a word in a node?
    type: good
    why:
      ko: '단어의 마지막 문자에 해당하는 노드에 boolean 플래그(예: end, isWord)를 설정합니다. 이를 통해 "app"과 "apple" 모두를 삽입할 때, 각각의 마지막 노드에 플래그를 설정하여 구분할 수 있습니다.'
      en: Set a boolean flag (e.g., end, isWord) on the node representing the last character of the word. This allows distinguishing between "app" and "apple" when both are inserted.
  - q:
      ko: 한 단어가 다른 단어의 접두사가 될 수 있나요?
      en: Can a word be a prefix of another word?
    type: good
    why:
      ko: 네, 가능합니다. 예를 들어 "app"을 먼저 삽입하고 "apple"을 나중에 삽입할 수 있습니다. 이 경우 두 단어의 끝 노드는 서로 다릅니다.
      en: Yes. For example, you can insert "app" first and then "apple". The end nodes of the two words are different.
  - q:
      ko: 자식 노드를 저장할 때 배열과 해시맵 중 어느 것이 더 좋나요?
      en: Is it better to use an array or hash map to store child nodes?
    type: good
    why:
      ko: 소문자 영문만 사용한다면 26개 크기의 배열이 더 효율적입니다. O(1) 접근 시간과 해시 오버헤드가 없습니다. 다양한 문자를 지원해야 한다면 해시맵이 더 유연합니다.
      en: For lowercase English letters only, a 26-element array is more efficient with guaranteed O(1) access. A hash map is more flexible for diverse character sets.
  - q:
      ko: 문자를 배열 인덱스로 변환할 때 ord(c) - ord('a')를 사용하는 이유는 무엇인가요?
      en: Why use ord(c) - ord('a') to convert a character to array index?
    type: good
    why:
      ko: '''a''의 ASCII 값을 기준점으로 삼아, 각 문자를 0~25 범위의 인덱스로 매핑합니다. 예를 들어 ''a''는 0, ''z''는 25가 됩니다.'
      en: Maps each character to an index in the range 0-25 using 'a' as baseline. 'a' becomes 0, 'z' becomes 25.
  - q:
      ko: 경로가 존재하지 않으면 즉시 false를 반환해야 하나요?
      en: Should we return false immediately if a path does not exist?
    type: good
    why:
      ko: 네, search()와 startsWith() 모두에서 순회 중 자식 노드가 없으면 즉시 false를 반환합니다. 불필요한 순회를 피할 수 있습니다.
      en: Yes, both methods return false immediately if a child node is missing during traversal, avoiding unnecessary iterations.
  - q:
      ko: 이미 존재하는 단어를 다시 insert()하면 어떻게 되나요?
      en: What happens if we insert a word that already exists?
    type: distractor
    why:
      ko: 이미 존재하는 경로를 따라 이동하고 마지막 노드의 end 플래그를 다시 설정합니다. 새로운 노드가 생성되지 않으므로 문제가 없습니다.
      en: The existing path is traversed and the end flag is set again on the last node. No new nodes are created.
  - q:
      ko: startsWith()에서 경로가 존재하면 항상 true를 반환해야 하나요?
      en: In startsWith(), should we always return true if the path exists?
    type: distractor
    why:
      ko: 네, startsWith()는 end 플래그를 확인하지 않고 경로만 확인합니다. "apple" 삽입 후 startsWith("ap")는 true를 반환합니다.
      en: Yes, startsWith() returns true if the path exists, regardless of the end flag. After inserting "apple", startsWith("ap") returns true.
approach:
  items:
  - name:
      ko: 26-크기 배열을 사용한 트라이
      en: Trie with 26-element array
    complexity: O(m) per operation (m = word/prefix length); O(n * 26) space where n = unique prefixes
    type: good
    why:
      ko: 소문자 영문자만 지원하는 경우, 각 노드에 26개 크기의 고정 배열을 사용합니다. O(1) 배열 접근으로 매우 효율적입니다.
      en: For lowercase English letters, each node has a fixed 26-element array. Provides O(1) array access and is very efficient.
  - name:
      ko: 해시맵을 사용한 트라이
      en: Trie with hash map
    complexity: O(m) per operation; O(n * k) space where k = average branching factor
    type: good
    why:
      ko: 각 노드에 딕셔너리를 사용하여 자식 노드를 저장합니다. sparse한 경우 메모리를 절약할 수 있고, 다양한 문자 집합을 지원합니다.
      en: Use a dictionary at each node for children. Saves memory in sparse cases and supports diverse character sets.
  - name:
      ko: Brute force - 리스트에 모든 단어 저장
      en: Brute force - store all words in list
    complexity: O(n * m) per search where n = number of inserted words, m = word length
    type: distractor
    why:
      ko: 모든 삽입된 단어를 리스트에 저장하고, search/startsWith 호출 시 리스트를 순회합니다. 트라이에 비해 매우 비효율적입니다.
      en: Store all inserted words in a list and iterate through it for each search. Very inefficient compared to trie.
  - name:
      ko: 정규 표현식 매칭
      en: Regular expression matching
    complexity: O(m) per search but with large constants
    type: distractor
    why:
      ko: 정규 표현식으로 저장된 단어들을 패턴 매칭하는 방식은 구현이 복잡하고 트라이보다 느립니다.
      en: Using regex to pattern-match stored words is complex to implement and slower than trie.
logic:
  format: slot
  slots:
  - label:
      ko: 루트 노드 초기화
      en: Initialize root node
    indent: 0
    options:
    - code: self.root = TrieNode()
      type: good
      why:
        ko: 트라이의 시작점이 되는 루트 노드를 생성합니다. 모든 단어는 이 루트에서 시작하는 경로로 표현됩니다.
        en: Create the root node as the starting point of the trie. All words are represented as paths starting from this root.
    - code: self.root = {}
      type: distractor
      why:
        ko: 딕셔너리는 TrieNode의 구조(children 배열과 end 플래그)를 직접 구현하지 못합니다.
        en: A dictionary doesn't implement the TrieNode structure (children array and end flag).
    - code: self.children = [None] * 26
      type: distractor
      why:
        ko: 이것은 루트 노드의 자식 배열이지, 루트 노드 인스턴스 자체가 아닙니다.
        en: This is the children array, not the TrieNode instance itself.
  - label:
      ko: 문자를 배열 인덱스로 변환
      en: Convert character to array index
    indent: 2
    options:
    - code: i = ord(c) - ord("a")
      type: good
      why:
        ko: 각 문자를 0~25 범위의 인덱스로 변환하여 26-크기 배열에 접근합니다. 'a'는 0, 'z'는 25입니다.
        en: Convert each character to an index in range 0-25 for array access. 'a' maps to 0, 'z' maps to 25.
    - code: i = ord(c)
      type: distractor
      why:
        ko: ASCII 값을 직접 사용하면 0~25 범위를 벗어나 배열 인덱싱에 사용할 수 없습니다.
        en: Using ASCII value directly exceeds the 0-25 range needed for array indexing.
    - code: i = ord(c) - ord('A')
      type: distractor
      why:
        ko: 이 문제는 소문자만 처리하므로 'a'를 기준점으로 사용해야 합니다.
        en: This problem only handles lowercase letters, so 'a' should be the baseline, not 'A'.
  - label:
      ko: insert에서 자식 노드 생성
      en: Create child nodes during insert
    indent: 2
    options:
    - code: curr.children[i] = TrieNode()
      type: good
      why:
        ko: 자식 노드가 존재하지 않으면 새로운 TrieNode를 생성하여 경로를 확장합니다. 이를 통해 단어의 모든 문자에 대한 노드 체인을 구성합니다.
        en: If a child node doesn't exist, create a new TrieNode to extend the path. This builds a node chain for all word characters.
    - code: curr.children[i] = {}
      type: distractor
      why:
        ko: 딕셔너리를 생성하면 children 배열과 end 플래그가 없어서 나중의 순회에서 오류가 발생합니다.
        en: Creating a dictionary loses the children array and end flag structure, causing errors in traversal.
    - code: 'if curr.children[i] is not None: curr.children[i] = TrieNode()'
      type: distractor
      why:
        ko: 조건이 반대입니다. 노드가 이미 존재할 때 덮어씌우면 기존 데이터가 손실됩니다.
        en: The condition is reversed; overwriting an existing node loses previous data.
  - label:
      ko: insert에서 단어의 끝 표시
      en: Mark end of word in insert
    indent: 1
    options:
    - code: curr.end = True
      type: good
      why:
        ko: 모든 문자를 순회한 후 마지막 노드에 end 플래그를 설정합니다. 이를 통해 정확한 단어 완성을 표시합니다.
        en: After traversing all characters, set the end flag on the last node. This marks exact word completion.
    - code: self.root.end = True
      type: distractor
      why:
        ko: 루트 노드의 end를 설정하면 모든 단어가 마치 완성된 것처럼 표시됩니다. 현재 위치 curr의 end를 설정해야 합니다.
        en: Setting root.end marks all words as complete, which is wrong. We must set curr.end.
    - code: curr.children[i].end = True
      type: distractor
      why:
        ko: 마지막 문자의 자식 노드의 end를 설정하므로 잘못된 노드에 플래그를 설정합니다.
        en: This sets the flag on a child of the last character, marking the wrong node.
  - label:
      ko: search에서 단어 완성 확인
      en: Check word completion in search
    indent: 1
    options:
    - code: return curr.end
      type: good
      why:
        ko: 모든 문자에 대한 경로를 순회한 후, 마지막 노드의 end 플래그를 확인합니다. true이면 정확한 단어가 존재하는 것입니다.
        en: After traversing all characters, check the end flag of the last node. If true, an exact word exists.
    - code: return curr is not None
      type: distractor
      why:
        ko: 경로의 존재 여부만 확인하는 것으로, "apple" 삽입 후 search("app")가 true를 반환합니다.
        en: This only checks path existence. After inserting "apple", search("app") would incorrectly return true.
    - code: return True
      type: distractor
      why:
        ko: 항상 true를 반환하므로, 존재하지 않는 단어도 검색되는 것으로 나타납니다.
        en: Always returns true, so non-existent words appear to be found.
  - label:
      ko: startsWith에서 문자 순회
      en: Character traversal in startsWith
    indent: 1
    options:
    - code: 'for c in prefix:'
      type: good
      why:
        ko: 접두사의 각 문자에 대해 순회합니다. search와 달리 마지막 노드의 end 플래그를 확인하지 않습니다.
        en: Traverse each character of the prefix. Unlike search, we don't check the end flag of the final node.
    - code: 'for c in word:'
      type: distractor
      why:
        ko: prefix 대신 word를 사용하면 함수의 잘못된 매개변수로 순회합니다.
        en: Using word instead of prefix iterates over the wrong parameter.
    - code: 'for i in range(len(prefix)): c = prefix[i]'
      type: distractor
      why:
        ko: 이 방식은 동작하지만, 직접 for 루프를 사용하는 것이 더 간단하고 파이썬스럽습니다.
        en: This works but is more verbose than directly iterating with a for loop.
  - label:
      ko: startsWith에서 경로 존재 확인
      en: Return path existence in startsWith
    indent: 1
    options:
    - code: return True
      type: good
      why:
        ko: 접두사에 대한 경로가 존재하면 true를 반환합니다. 경로 순회 중에 None을 만나지 않았다면, 접두사는 어떤 단어의 시작입니다.
        en: Return true if a path for the prefix exists. If no None was encountered during traversal, the prefix is the start of some word.
    - code: return curr.end
      type: distractor
      why:
        ko: end 플래그는 정확한 단어의 완성을 의미합니다. startsWith는 불완전한 접두사도 인정해야 합니다.
        en: The end flag marks exact word completion. startsWith should recognize incomplete prefixes.
    - code: return curr is not None
      type: distractor
      why:
        ko: 이는 중복된 확인입니다. 루프가 종료되었다면 이미 curr이 None이 아님이 보장됩니다.
        en: This is redundant; if we reach here, curr is guaranteed to not be None.
trace:
  code:
  - 'class TrieNode:'
  - '    def __init__(self):'
  - '        self.children = [None] * 26'
  - '        self.end = False'
  - ''
  - ''
  - 'class Trie:'
  - '    def __init__(self):'
  - '        """'
  - '        Initialize your data structure here.'
  - '        """'
  - '        self.root = TrieNode()'
  - ''
  - '    def insert(self, word: str) -> None:'
  - '        """'
  - '        Inserts a word into the trie.'
  - '        """'
  - '        curr = self.root'
  - '        for c in word:'
  - '            i = ord(c) - ord("a")'
  - '            if curr.children[i] is None:'
  - '                curr.children[i] = TrieNode()'
  - '            curr = curr.children[i]'
  - '        curr.end = True'
  - ''
  - '    def search(self, word: str) -> bool:'
  - '        """'
  - '        Returns if the word is in the trie.'
  - '        """'
  - '        curr = self.root'
  - '        for c in word:'
  - '            i = ord(c) - ord("a")'
  - '            if curr.children[i] is None:'
  - '                return False'
  - '            curr = curr.children[i]'
  - '        return curr.end'
  - ''
  - '    def startsWith(self, prefix: str) -> bool:'
  - '        """'
  - '        Returns if there is any word in the trie that starts with the given prefix.'
  - '        """'
  - '        curr = self.root'
  - '        for c in prefix:'
  - '            i = ord(c) - ord("a")'
  - '            if curr.children[i] is None:'
  - '                return False'
  - '            curr = curr.children[i]'
  - '        return True'
  cases:
  - input: '["Trie","insert","search","search","startsWith","insert","search"]

      [[],["apple"],["apple"],["app"],["app"],["app"],["app"]]'
    expected: '[null, null, true, false, true, null, true]'
  worked_example:
    input: '["Trie","insert","search","search","startsWith","insert","search"]

      [[],["apple"],["apple"],["app"],["app"],["app"],["app"]]'
    steps:
    - ko: '1. Trie(): 루트 노드만 있는 빈 트라이를 초기화합니다.'
      en: '1. Trie(): Initialize empty trie with root node only.'
    - ko: '2. insert("apple"): 루트에서 a→p→p→l→e 경로를 생성하고, ''e'' 노드의 end 플래그를 true로 설정합니다.'
      en: '2. insert("apple"): Create path a→p→p→l→e from root and set end flag on ''e'' node.'
    - ko: '3-5. search("apple") = true, search("app") = false, startsWith("app") = true: 경로 순회 로직과 end 플래그 확인의 차이를 보여줍니다.'
      en: '3-5. search("apple") = true, search("app") = false, startsWith("app") = true: Demonstrates path traversal and end flag checking differences.'
    - ko: '6-7. insert("app"): 기존 경로 a→p→p에서 두 번째 ''p'' 노드의 end를 true로 설정. search("app") = true: 이제 "app"도 완성된 단어입니다.'
      en: '6-7. insert("app"): Set end flag on second ''p'' node. Now search("app") = true since "app" is a complete word.'
    answer: '[null, null, true, false, true, null, true]'
solution:
  code: "class TrieNode:\n    def __init__(self):\n        self.children = [None] * 26\n        self.end = False\n\n\nclass Trie:\n    def __init__(self):\n        \"\"\"\n        Initialize your data structure here.\n        \"\"\"\n        self.root = TrieNode()\n\n    def insert(self, word: str) -> None:\n        \"\"\"\n        Inserts a word into the trie.\n        \"\"\"\n        curr = self.root\n        for c in word:\n            i = ord(c) - ord(\"a\")\n            if curr.children[i] is None:\n                curr.children[i] = TrieNode()\n            curr = curr.children[i]\n        curr.end = True\n\n    def search(self, word: str) -> bool:\n        \"\"\"\n        Returns if the word is in the trie.\n        \"\"\"\n        curr = self.root\n        for c in word:\n            i = ord(c) - ord(\"a\")\n            if curr.children[i] is None:\n                return False\n            curr = curr.children[i]\n        return curr.end\n\n    def startsWith(self, prefix: str) ->\
    \ bool:\n        \"\"\"\n        Returns if there is any word in the trie that starts with the given prefix.\n        \"\"\"\n        curr = self.root\n        for c in prefix:\n            i = ord(c) - ord(\"a\")\n            if curr.children[i] is None:\n                return False\n            curr = curr.children[i]\n        return True\n"
  complexity:
    time: O(m) per operation, where m = length of word/prefix
    space: O(n * 26) = O(n), where n = total number of unique character positions across all inserted words
  followup:
  - ko: 대문자와 숫자를 포함하는 문자열을 지원하려면 어떻게 수정하시겠어요?
    en: How would you modify the solution to support uppercase letters and digits?
  - ko: 트라이에서 단어를 삭제하는 메서드를 추가하려면 어떻게 해야 할까요?
    en: How would you implement a delete() method to remove words from the trie?
  - ko: 주어진 접두사로 시작하는 모든 단어를 자동 완성으로 반환하려면 어떻게 할까요?
    en: How would you implement autocomplete to return all words starting with a given prefix?
```