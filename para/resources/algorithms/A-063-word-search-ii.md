---
created: '2026-07-15'
date: '2026-07-15'
day: Day 63
difficulty: hard
id: A-063
source:
  curated_in:
  - neetcode150
  number: 212
  platform: leetcode
  slug: word-search-ii
  url: https://leetcode.com/problems/word-search-ii/
tags:
- array
- string
- backtracking
- trie
- matrix
title:
  en: Word Search II
  ko: 단어 검색 II
today: false
type: algorithm
updated: '2026-07-15'
visible: true
---

# 단어 검색 II

## Data

```yaml
problem:
  title:
    ko: 단어 검색 II
    en: Word Search II
  statement:
    ko: m × n 크기의 문자 보드와 문자열 목록이 주어졌을 때, 보드에 있는 모든 단어를 반환하세요. 각 단어는 인접한 셀(가로 또는 세로로 이웃한)의 문자로 순서대로 구성되어야 합니다. 같은 문자 셀을 한 단어에 두 번 이상 사용할 수 없습니다.
    en: Given an m x n board of characters and a list of strings words, return all words on the board. Each word must be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once in a word.
  constraints:
  - 1 ≤ m, n ≤ 12
  - board[i][j] is a lowercase English letter
  - 1 ≤ words.length ≤ 3 × 10⁴
  - 1 ≤ words[i].length ≤ 10
  io:
  - input: '[["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]]

      ["oath","pea","eat","rain"]'
    output: '["eat","oath"]'
  - input: '[["a","b"],["c","d"]]

      ["abcb"]'
    output: '[]'
clarifying:
  items:
  - q:
      ko: 한 단어를 검색할 때 같은 셀을 두 번 이상 사용할 수 있나요?
      en: Can we use the same cell more than once when searching for a single word?
    type: good
    why:
      ko: 각 단어마다 셀 재사용이 불가능하기 때문에 백트래킹에서 visited 집합이 필수입니다.
      en: This clarifies the visited set requirement—each cell can only be used once per word path.
  - q:
      ko: 인접(adjacent)이란 상하좌우만 해당하나요, 대각선도 포함하나요?
      en: Does 'adjacent' mean only horizontal and vertical (4-directional) or include diagonals?
    type: good
    why:
      ko: 대각선을 포함하지 않는다면 DFS에서 4가지 방향만 탐색하면 되므로 정확한 구현이 중요합니다.
      en: This determines the branching factor in DFS—only 4 neighbors instead of 8 significantly reduces complexity.
  - q:
      ko: 보드에서 한 단어가 여러 번 나타나면 여러 번 반환해야 하나요?
      en: If a word appears multiple times on the board, should we return it multiple times?
    type: good
    why:
      ko: 결과를 집합으로 관리하는 이유를 이해하려면 각 단어는 한 번만 반환해야 함을 알아야 합니다.
      en: This justifies using a set for results—each unique word appears in output exactly once.
  - q:
      ko: Trie의 'refs' 카운터는 왜 필요한가요?
      en: Why do we need a 'refs' counter in each Trie node?
    type: good
    why:
      ko: '''refs'' 값이 0이면 그 경로로는 어떤 단어도 완성될 수 없으므로 조기 종료(pruning) 가능합니다.'
      en: 'It enables early termination: if refs < 1, no word can be completed via this prefix, so we stop exploring.'
  - q:
      ko: 단어를 찾은 후 'removeWord'를 호출하는 이유는?
      en: Why do we call removeWord after finding a word?
    type: good
    why:
      ko: 이를 통해 같은 경로를 다시 탐색할 때 이미 찾은 단어를 건너뛸 수 있고, refs 감소로 불필요한 경로 탐색을 줄입니다.
      en: This prevents duplicate results and reduces redundant exploration—when refs drop to 0, we skip that branch immediately.
  - q:
      ko: 왜 대신 'isWord = False'만 설정하고 removeWord는 호출하지 않으면 안 되나요?
      en: Why can't we just set isWord = False without calling removeWord?
    type: distractor
    why:
      ko: isWord만 변경하면 다른 단어들의 refs 값이 감소하지 않아, 불필요한 브랜치 탐색이 계속 일어납니다.
      en: Without updating refs across the Trie, other words' reference counts won't decrease, defeating the pruning optimization.
  - q:
      ko: DFS에서 4가지 방향 호출 순서가 중요한가요?
      en: Does the order of the 4 DFS directional calls matter?
    type: distractor
    why:
      ko: 순서는 결과에 영향을 주지 않습니다. 중요한 것은 4가지 방향을 모두 탐색하는 것입니다.
      en: Order doesn't affect correctness—only matters that all 4 neighbors are explored before backtracking.
approach:
  items:
  - name:
      ko: Trie + 백트래킹 (조기 종료 최적화)
      en: Trie + Backtracking with Early Termination
    complexity: O(m × n × 4^L) time / O(T + m × n) space
    type: good
    why:
      ko: Trie의 'refs' 카운터로 불필요한 경로를 조기에 제거하므로 실제 성능이 매우 우수합니다. 각 보드 위치에서 DFS를 시작하되, 지금까지 본 접두사로 어떤 단어도 만들 수 없으면 즉시 되돌아갑니다.
      en: 'Trie with reference counting enables pruning: if no word can be completed via a prefix, stop exploring immediately. This dramatically reduces redundant exploration compared to naive backtracking.'
  - name:
      ko: HashMap 기반 접근
      en: HashMap/HashSet Prefix Checking
    complexity: O(m × n × 4^L) time / O(W × L) space
    type: distractor
    why:
      ko: 모든 가능한 접두사를 미리 추출하여 집합에 저장한 후, 백트래킹 중 검사합니다. Trie보다 구현은 간단하지만 메모리 오버헤드가 크고 해시 계산이 느릴 수 있습니다.
      en: Precompute all prefixes of all words into a set, then check during DFS. Simpler but higher memory overhead and hash lookups are slower than Trie traversal.
  - name:
      ko: 완전 탐색 (최적화 없음)
      en: Brute Force DFS (No Pruning)
    complexity: O(m × n × 4^(m×n)) time / O(m × n) space
    type: distractor
    why:
      ko: 모든 가능한 경로를 탐색하고 주어진 단어 리스트와 비교합니다. 전체 보드를 탐색할 수 있으므로 시간 복잡도가 지수적으로 증가하여 실용적이지 않습니다.
      en: Explore all possible paths from each cell without pruning, then check if each path matches any word. No early termination means exploring exponential paths—infeasible for larger boards.
  - name:
      ko: 재귀적 백트래킹 (재방문 감지 없음)
      en: Recursive Backtracking without Visited Tracking
    complexity: O(4^(m×n)) time / O(1) space
    type: distractor
    why:
      ko: 같은 셀을 여러 번 방문하는 것을 허용하면 무한 루프나 같은 경로를 반복 탐색하게 됩니다. visited 집합 없이는 기본 요구사항(같은 셀 재사용 금지)을 충족할 수 없습니다.
      en: Without visited tracking, cells can be revisited infinitely, violating the core constraint. Leads to exponential redundant exploration and infinite loops.
logic:
  format: slot
  slots:
  - label:
      ko: Trie에 모든 단어 추가
      en: Add All Words to Trie
    indent: 0
    options:
    - code: root.addWord(w)
      type: good
      why:
        ko: 각 단어를 Trie에 추가하면 공통 접두사를 공유하여 메모리 효율성을 높이고, 나중에 DFS 중 접두사 기반 조기 종료가 가능해집니다.
        en: Adding words to a Trie enables prefix-based pruning during search and shares common prefixes for space efficiency.
    - code: 'words_set = set(words); word_dict = {w: True for w in words}'
      type: distractor
      why:
        ko: 단순 집합/딕셔너리는 접두사 정보를 저장하지 않아 DFS 중 조기 종료 불가능합니다.
        en: HashSet/dict don't store prefix info, preventing early pruning during DFS traversal.
    - code: 'for w in sorted(words): root.addWord(w)'
      type: distractor
      why:
        ko: 단어를 정렬하는 것은 불필요하고 O(W log W) 시간을 낭비합니다.
        en: Sorting words wastes O(W log W) time with no correctness benefit.
    - code: 'for w in words: root.addWord(w[::-1])'
      type: distractor
      why:
        ko: 단어를 역순으로 추가하면 원래 방향의 단어를 찾을 수 없습니다.
        en: Reversing words prevents finding them forward on the board—incorrect logic.
  - label:
      ko: 검색 상태 초기화
      en: Initialize Search State
    indent: 0
    options:
    - code: res, visit = set(), set()
      type: good
      why:
        ko: '''set()''을 사용하면 결과 중복 제거 (O(1) 조회)와 방문 셀 빠른 확인 (O(1) 검색)이 가능합니다.'
        en: Using set() provides O(1) lookup for both checking visited cells and ensuring unique results.
    - code: res, visit = [], set()
      type: distractor
      why:
        ko: 리스트는 'in' 연산이 O(n)이고, 중복 제거도 수동으로 해야 합니다.
        en: List has O(n) lookup; requires manual deduplication instead of set's automatic handling.
    - code: res, visit = set(), []
      type: distractor
      why:
        ko: 리스트 기반 visit는 (r, c)의 멤버십 검사가 O(n)으로 느립니다.
        en: List-based visited set has O(n) membership checking instead of O(1).
    - code: res, visit, found_words = set(), set(), set()
      type: distractor
      why:
        ko: 세 번째 집합은 중복되며, 이미 res와 found_words가 같은 목적을 수행합니다.
        en: Third data structure is redundant—already tracking results in res.
  - label:
      ko: 경계 및 가지 제거 검사
      en: Boundary & Pruning Check
    indent: 1
    options:
    - code: or node.children[board[r][c]].refs < 1
      type: good
      why:
        ko: node.children[board[r][c]].refs < 1은 Trie의 조기 종료 최적화 핵심입니다. 만약 현재 접두사로부터 어떤 단어도 완성될 수 없다면 (refs = 0), 이 경로 이하로 탐색할 필요가 없습니다.
        en: 'The refs check is the key optimization: if no word can be completed via this prefix, prune immediately. Without this, we explore many dead-end branches.'
    - code: or node.children[board[r][c]].refs == 0
      type: distractor
      why:
        ko: 같은 의미이지만 refs가 음수가 될 수 있다면 안전하지 않습니다. '<1'이 더 명확합니다.
        en: Semantically similar but less safe if refs could become negative; 'refs < 1' is more defensive.
    - code: or board[r][c] not in node.children
      type: distractor
      why:
        ko: 이 검사는 문자 존재 여부만 확인하며, refs 값은 확인하지 않아 불완전한 가지 제거입니다.
        en: Only checks if character exists, not whether any word can be completed—misses pruning opportunities.
    - code: or len(node.children) == 0
      type: distractor
      why:
        ko: 노드에 자식이 있는지 여부만 확인하며, 그 자식으로 단어를 완성할 수 있는지는 확인하지 않습니다.
        en: Checks if node has any children, but doesn't verify if the specific path leads to a word.
  - label:
      ko: 발견한 단어 제거 및 처리
      en: Remove Found Word from Trie
    indent: 1
    options:
    - code: root.removeWord(word)
      type: good
      why:
        ko: root.removeWord(word)는 단어의 경로에서 refs를 감소시키므로, 나중에 같은 접두사를 탐색할 때 조기 종료 가능성이 높아집니다. 또한 중복 결과를 방지합니다.
        en: removeWord decrements refs along the path, enabling pruning in future searches. Also prevents duplicate results since isWord is already set to False.
    - code: 'node.isWord = False  # without removeWord'
      type: distractor
      why:
        ko: isWord 플래그만 변경하면 다른 단어들의 refs 값이 감소하지 않아 불필요한 탐색 경로가 남습니다.
        en: Without removeWord, refs aren't decremented, so future searches still explore this dead branch.
    - code: res.add(word); visit.clear()
      type: distractor
      why:
        ko: visit 집합 전체를 지우면 모든 이전 경로가 초기화되어 다른 단어 검색에 영향을 줍니다.
        en: Clearing the entire visited set corrupts state for other word searches.
    - code: 'res.discard(word)  # remove from result?'
      type: distractor
      why:
        ko: 단어를 결과에서 제거하는 것은 논리적 오류입니다. 발견한 단어는 유지해야 합니다.
        en: Removing found words from results is logically incorrect—we want to keep found words.
  - label:
      ko: 모든 인접 셀 탐색
      en: Explore All 4 Neighbors
    indent: 1
    options:
    - code: dfs(r + 1, c, node, word)
      type: good
      why:
        ko: 4가지 방향(상하좌우) 모두를 탐색해야 보드의 모든 가능한 경로를 찾을 수 있습니다. 대각선은 포함하지 않습니다.
        en: All 4 directions (up, down, left, right) must be explored. Diagonals are excluded per problem definition.
    - code: 'dfs(r + 1, c, node, word); dfs(r - 1, c, node, word)  # only vertical'
      type: distractor
      why:
        ko: 수평 방향(좌우)을 탐색하지 않으면 오른쪽/왼쪽 인접 셀의 단어를 놓칩니다.
        en: Missing horizontal directions causes us to miss words extending left or right.
    - code: 'dfs(r + 1, c + 1, node, word)  # diagonal'
      type: distractor
      why:
        ko: 대각선은 문제에서 인접으로 정의되지 않습니다.
        en: Diagonals are not defined as adjacent in the problem.
    - code: '# only dfs(r + 1, c, node, word)'
      type: distractor
      why:
        ko: 한 방향만 탐색하면 대부분의 단어를 찾을 수 없습니다.
        en: Single direction exploration misses words in 3 other directions.
  - label:
      ko: 상태 복원 (백트래킹)
      en: Backtrack—Restore State
    indent: 1
    options:
    - code: visit.remove((r, c))
      type: good
      why:
        ko: visit.remove((r, c))는 현재 경로를 벗어날 때 셀을 미방문 상태로 돌려놓습니다. 이를 통해 다른 경로에서 같은 셀을 사용할 수 있게 됩니다.
        en: Removing from visited allows sibling branches to use this cell. Without backtracking, all sibling paths think this cell is occupied, causing missed words.
    - code: '# no visit.remove — missing backtrack'
      type: distractor
      why:
        ko: 백트래킹이 없으면 형제 경로가 이 셀을 다시 사용할 수 없어 많은 단어를 놓칩니다.
        en: Without backtracking, sibling paths can't reuse this cell, causing incorrect results.
    - code: 'visit = set()  # clear entire visited set'
      type: distractor
      why:
        ko: 전체 visited 집합을 지우면 현재 DFS의 조상 노드도 미방문 상태가 되어 순환이 발생합니다.
        en: Clearing all visited state allows cycles and revisits in the current path.
    - code: 'if (r, c) in visit: visit.remove((r, c))'
      type: distractor
      why:
        ko: 불필요한 조건문입니다. visit.remove()는 항상 안전하게 작동합니다.
        en: Unnecessary guard; remove is idempotent in this context and always succeeds.
trace:
  code:
  - 'class TrieNode:'
  - '    def __init__(self):'
  - '        self.children = {}'
  - '        self.isWord = False'
  - '        self.refs = 0'
  - ''
  - '    def addWord(self, word):'
  - '        cur = self'
  - '        cur.refs += 1'
  - '        for c in word:'
  - '            if c not in cur.children:'
  - '                cur.children[c] = TrieNode()'
  - '            cur = cur.children[c]'
  - '            cur.refs += 1'
  - '        cur.isWord = True'
  - ''
  - '    def removeWord(self, word):'
  - '        cur = self'
  - '        cur.refs -= 1'
  - '        for c in word:'
  - '            if c in cur.children:'
  - '                cur = cur.children[c]'
  - '                cur.refs -= 1'
  - ''
  - ''
  - 'class Solution:'
  - '    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:'
  - '        root = TrieNode()'
  - '        for w in words:'
  - '            root.addWord(w)'
  - ''
  - '        ROWS, COLS = len(board), len(board[0])'
  - '        res, visit = set(), set()'
  - ''
  - '        def dfs(r, c, node, word):'
  - '            if ('
  - '                r not in range(ROWS) '
  - '                or c not in range(COLS)'
  - '                or board[r][c] not in node.children'
  - '                or node.children[board[r][c]].refs < 1'
  - '                or (r, c) in visit'
  - '            ):'
  - '                return'
  - ''
  - '            visit.add((r, c))'
  - '            node = node.children[board[r][c]]'
  - '            word += board[r][c]'
  - '            if node.isWord:'
  - '                node.isWord = False'
  - '                res.add(word)'
  - '                root.removeWord(word)'
  - ''
  - '            dfs(r + 1, c, node, word)'
  - '            dfs(r - 1, c, node, word)'
  - '            dfs(r, c + 1, node, word)'
  - '            dfs(r, c - 1, node, word)'
  - '            visit.remove((r, c))'
  - ''
  - '        for r in range(ROWS):'
  - '            for c in range(COLS):'
  - '                dfs(r, c, root, "")'
  - ''
  - '        return list(res)'
  cases:
  - input: '[["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]]

      ["oath","pea","eat","rain"]'
    expected: '["eat","oath"]'
  - input: '[["a","b"],["c","d"]]

      ["abcb"]'
    expected: '[]'
  worked_example:
    input: '[["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]]

      ["oath","pea","eat","rain"]'
    steps:
    - ko: 모든 단어 ["oath","pea","eat","rain"]를 Trie에 추가합니다.
      en: Add all words ["oath","pea","eat","rain"] to the Trie with reference counting.
    - ko: 각 보드 셀(0,0)부터 시작하여 DFS를 실행합니다. (0,0)의 'o' → (0,1) 'a' → (1,1) 't' → (2,1) 'h'로 이동하면 "oath"를 발견합니다.
      en: 'Start DFS from (0,0): path o→a→t→h (coordinates: (0,0)→(0,1)→(1,1)→(2,1)) finds "oath".'
    - ko: (1,0)의 'e'에서 시작하여 DFS를 실행합니다. (1,0) 'e' → (0,1) 'a' → (1,1) 't'로 이동하면 "eat"를 발견합니다.
      en: 'Start DFS from (1,0): path e→a→t (coordinates: (1,0)→(0,1)→(1,1)) finds "eat".'
    - ko: '"pea"는 ''p''가 보드에 없고, "rain"은 인접 경로가 없어 발견되지 않습니다. 결과: ["eat", "oath"]'
      en: '"pea" has no ''p'' on board; "rain" has no valid adjacent path. Final result: ["eat", "oath"]'
    answer: '["eat","oath"]'
solution:
  code: "class TrieNode:\n    def __init__(self):\n        self.children = {}\n        self.isWord = False\n        self.refs = 0\n\n    def addWord(self, word):\n        cur = self\n        cur.refs += 1\n        for c in word:\n            if c not in cur.children:\n                cur.children[c] = TrieNode()\n            cur = cur.children[c]\n            cur.refs += 1\n        cur.isWord = True\n\n    def removeWord(self, word):\n        cur = self\n        cur.refs -= 1\n        for c in word:\n            if c in cur.children:\n                cur = cur.children[c]\n                cur.refs -= 1\n\n\nclass Solution:\n    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:\n        root = TrieNode()\n        for w in words:\n            root.addWord(w)\n\n        ROWS, COLS = len(board), len(board[0])\n        res, visit = set(), set()\n\n        def dfs(r, c, node, word):\n            if (\n                r not in range(ROWS) \n                or c not in\
    \ range(COLS)\n                or board[r][c] not in node.children\n                or node.children[board[r][c]].refs < 1\n                or (r, c) in visit\n            ):\n                return\n\n            visit.add((r, c))\n            node = node.children[board[r][c]]\n            word += board[r][c]\n            if node.isWord:\n                node.isWord = False\n                res.add(word)\n                root.removeWord(word)\n\n            dfs(r + 1, c, node, word)\n            dfs(r - 1, c, node, word)\n            dfs(r, c + 1, node, word)\n            dfs(r, c - 1, node, word)\n            visit.remove((r, c))\n\n        for r in range(ROWS):\n            for c in range(COLS):\n                dfs(r, c, root, \"\")\n\n        return list(res)\n"
  complexity:
    time: O(m × n × 4^L) where m,n are board dimensions and L is the maximum word length
    space: O(T + m × n) where T is the total size of the Trie (sum of all word lengths)
  followup:
  - ko: 만약 같은 셀을 한 단어 내에서 여러 번 사용할 수 있다면 어떻게 해결하겠습니까?
    en: How would the solution change if the same cell could be reused multiple times within a single word?
  - ko: Trie의 refs 최적화 없이도 수용 가능한 성능을 낼 수 있는 다른 가지 제거 전략이 있습니까?
    en: What alternative pruning strategies could achieve acceptable performance without the refs counter in the Trie?
  - ko: 보드가 100×100처럼 매우 크고 단어 목록이 매우 길 경우, 이 알고리즘을 어떻게 최적화하거나 병렬화할 수 있을까요?
    en: How would you optimize or parallelize this algorithm for a very large board (100×100) and large word list?
```