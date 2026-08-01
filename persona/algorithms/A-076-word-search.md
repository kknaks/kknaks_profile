---
created: '2026-08-01'
date: '2026-08-01'
day: Day 76
difficulty: medium
id: A-076
source:
  curated_in:
  - neetcode150
  number: 79
  platform: leetcode
  slug: word-search
  url: https://leetcode.com/problems/word-search/
status: draft
tags:
- array
- string
- backtracking
- depth-first-search
- matrix
title:
  en: Word Search
  ko: 단어 검색
today: true
type: algorithm
updated: '2026-08-01'
visible: true
---

# 단어 검색

## Data

```yaml
problem:
  title:
    ko: 단어 검색
    en: Word Search
  statement:
    ko: 'm×n 크기의 문자 그리드 board와 문자열 word가 주어질 때, word가 그리드에 존재하면 true를 반환하세요.


      단어는 순차적으로 인접한 셀의 문자들로 구성될 수 있으며, 인접한 셀은 수평 또는 수직으로 이웃한 셀입니다. 같은 문자 셀은 한 번의 검색 경로 내에서 두 번 이상 사용될 수 없습니다.'
    en: 'Given an m x n grid of characters board and a string word, return true if word exists in the grid.


      The word can be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once.'
  constraints:
  - 1 ≤ m, n ≤ 6
  - 1 ≤ word.length ≤ 15
  - board and word consist of only English letters
  io:
  - input: '[["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]

      "ABCCED"'
    output: 'true'
  - input: '[["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]

      "SEE"'
    output: 'true'
  - input: '[["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]

      "ABCB"'
    output: 'false'
clarifying:
  items:
  - q:
      ko: 같은 셀을 한 단어 검색 경로 내에서 여러 번 사용할 수 있나요?
      en: Can the same cell be used multiple times within a single word search path?
    type: good
    why:
      ko: 아니요. 각 셀은 한 번의 경로 내에서 최대 한 번만 사용될 수 있습니다. 이것이 DFS에서 backtracking이 필수인 이유입니다.
      en: No. Each cell can be used at most once per path. This is why backtracking is essential in the DFS solution.
  - q:
      ko: 대각선 인접도 포함되나요?
      en: Are diagonal adjacencies allowed?
    type: good
    why:
      ko: 아니요. 오직 수평(좌우) 또는 수직(상하) 인접만 허용됩니다.
      en: No. Only horizontal (left/right) and vertical (up/down) adjacencies are allowed.
  - q:
      ko: 검색은 특정 셀에서 시작해야 하나요?
      en: Must the search start from a specific cell?
    type: good
    why:
      ko: 아니요. 보드의 모든 셀에서 시작을 시도하며, 하나라도 단어를 찾으면 true를 반환합니다.
      en: No. We try starting from every cell in the board; if any cell finds the word, we return true.
  - q:
      ko: 시간 복잡도를 개선할 수 있는 방법이 있나요?
      en: Is there a way to reduce time complexity?
    type: good
    why:
      ko: 네. 단어의 첫 문자가 마지막 문자보다 더 자주 나타나면 단어를 역순으로 바꿔서 시작점을 줄일 수 있습니다.
      en: Yes. If the first character appears more frequently than the last, reverse the word to reduce starting points.
  - q:
      ko: 방문한 셀을 추적하기 위해 2D 배열을 반드시 사용해야 하나요?
      en: Must we use a 2D array to track visited cells?
    type: distractor
    why:
      ko: 아니요. 집합(set)을 사용하면 O(1) 조회와 배열보다 간단한 구현을 얻습니다.
      en: No. Using a set provides O(1) lookup and simpler implementation than a 2D array.
  - q:
      ko: 각 재귀 단계에서 4개 방향을 모두 탐색해야 하나요?
      en: Do we need to explore all 4 directions at each recursion level?
    type: distractor
    why:
      ko: 네, 모든 경로를 탐색해야 합니다. 단, OR 연산자로 하나가 성공하면 즉시 반환됩니다.
      en: Yes, we explore all paths. However, the OR operator returns immediately if one succeeds.
  - q:
      ko: backtracking(방문 표시 제거)을 빠뜨리면 어떻게 되나요?
      en: What if we forget to backtrack (remove from visited path)?
    type: distractor
    why:
      ko: 셀을 다시 사용할 수 없으므로 다른 경로 탐색에서 잘못된 결과를 얻게 됩니다.
      en: Cells won't be reusable for other paths, causing incorrect results in alternative explorations.
approach:
  items:
  - name:
      ko: DFS와 Backtracking
      en: DFS with Backtracking
    complexity: O(N × M × 4^L) time / O(L) space
    type: good
    why:
      ko: 각 셀에서 시작하여 4개 방향을 탐색하며, 방문을 추적하고 되돌립니다. 가장 직관적이고 효율적입니다.
      en: Starting from each cell, explore 4 directions while tracking and undoing visits. Most intuitive and efficient.
  - name:
      ko: BFS (너비 우선 탐색)
      en: BFS (Breadth-First Search)
    complexity: O(N × M × 4^L) time / O(L) space
    type: distractor
    why:
      ko: 작동하지만 DFS보다 불필요하게 복잡합니다. 단어 매칭은 깊이 정보 추적이 필요하므로 BFS의 계층 구조가 어울리지 않습니다.
      en: Works but unnecessarily complex compared to DFS. Word matching needs depth tracking; BFS's level-by-level nature doesn't fit.
  - name:
      ko: 동적 프로그래밍 (Memoization)
      en: Dynamic Programming (Memoization)
    complexity: O(N × M × 2^L) time / O(N × M × L) space
    type: distractor
    why:
      ko: 겹치는 부분문제가 드물기 때문에 memoization 오버헤드가 이점을 상쇄합니다. 대부분의 경로가 독립적입니다.
      en: Overlapping subproblems are rare; memoization overhead negates benefits. Most paths are independent.
  - name:
      ko: Trie 자료구조와 DFS
      en: Trie with DFS
    complexity: O(N × M × L × 4^L) time / O(alphabet) space
    type: distractor
    why:
      ko: 여러 단어를 검색할 때 유용하지만, 단일 단어에는 오버엔지니어링입니다. 전처리 비용이 이점을 상쇄합니다.
      en: Useful for searching multiple words, but over-engineered for single word search. Preprocessing cost outweighs benefits.
logic:
  format: slot
  slots:
  - label:
      ko: 방문 추적 초기화
      en: Initialize path tracker
    indent: 0
    options:
    - code: path = set()
      type: good
      why:
        ko: 현재 탐색 경로의 방문한 셀을 저장할 집합을 생성합니다. O(1) 조회를 제공합니다.
        en: Create a set to store visited cells in current path. Provides O(1) membership checking.
    - code: path = []
      type: distractor
      why:
        ko: 리스트는 O(n) 시간이 필요하므로 비효율적입니다.
        en: List requires O(n) lookup time, making it inefficient.
    - code: visited = [[False] * len(board[0]) for _ in range(len(board))]
      type: distractor
      why:
        ko: 2D 배열은 backtracking 시 상태 복사가 필요해 복잡합니다.
        en: 2D array complicates backtracking; state copying is needed.
  - label:
      ko: '기저 사례: 단어 완성'
      en: 'Base case: word completed'
    indent: 1
    options:
    - code: 'if i == len(word):'
      type: good
      why:
        ko: 단어의 모든 문자를 매칭했음을 감지합니다. 인덱스가 단어 길이에 도달하면 true를 반환합니다.
        en: Detect when all characters are matched. Return true when index reaches word length.
    - code: 'if i == len(word) - 1:'
      type: distractor
      why:
        ko: 오프바이원 오류입니다. 마지막 문자 매칭 후 i는 len(word)이 됩니다.
        en: Off-by-one error. After matching last char, i becomes len(word).
    - code: 'if i > len(word):'
      type: distractor
      why:
        ko: 초과 검사는 절대 일어나지 않습니다(i는 i+1씩만 증가). == 를 사용하세요.
        en: Overflow never occurs (i increments by 1). Use == instead.
  - label:
      ko: 위치와 문자 검증
      en: Validate position and character
    indent: 1
    options:
    - code: if (
      type: good
      why:
        ko: 경계 범위, 문자 일치, 방문 여부를 확인합니다. 하나라도 실패하면 이 경로는 불가능합니다.
        en: Check bounds, character match, and visited status. Any failure means this path is invalid.
    - code: 'if r < 0 or c < 0 or r >= ROWS or c >= COLS:'
      type: distractor
      why:
        ko: 경계만 검사하고 문자 매칭을 빠뜨립니다. 틀린 셀에 진입할 수 있습니다.
        en: Only checks bounds, missing character match. Wrong cells can be entered.
    - code: 'if word[i] != board[r][c]:'
      type: distractor
      why:
        ko: 경계 검사를 빠뜨려 인덱스 오류가 발생할 수 있습니다.
        en: Missing bounds check causes potential index errors.
  - label:
      ko: 현재 셀 방문 표시
      en: Mark current cell as visited
    indent: 1
    options:
    - code: path.add((r, c))
      type: good
      why:
        ko: 현재 셀을 경로에 추가하여 이 탐색 경로에서 재사용되지 않도록 합니다.
        en: Add current cell to path to prevent reuse within this exploration path.
    - code: path.add(r, c)
      type: distractor
      why:
        ko: 집합의 add() 메서드는 한 개의 객체(튜플)를 받습니다. 구문 오류입니다.
        en: Set's add() takes one object (tuple). Syntax error with two arguments.
    - code: visited[r][c] = True
      type: distractor
      why:
        ko: 2D 배열은 backtracking 시 상태를 복구해야 해서 복잡합니다.
        en: 2D array requires state recovery during backtracking, adding complexity.
  - label:
      ko: 4개 인접 셀 재귀 탐색
      en: Explore all 4 adjacent cells recursively
    indent: 1
    options:
    - code: dfs(r + 1, c, i + 1)
      type: good
      why:
        ko: 상하좌우 4개 방향을 재귀적으로 탐색합니다. OR 연산자로 하나라도 성공하면 즉시 true를 반환합니다.
        en: Recursively explore up, down, left, right. OR operator returns true immediately if any succeeds.
    - code: dfs(r + 1, c, i + 1) only
      type: distractor
      why:
        ko: 한 방향만으로는 모든 가능한 경로를 찾을 수 없습니다.
        en: Single direction cannot find all possible paths.
    - code: dfs(r + 1, c, i) or dfs(r - 1, c, i) or dfs(r, c + 1, i) or dfs(r, c - 1, i)
      type: distractor
      why:
        ko: 단어 인덱스를 증가시키지 않으면 무한 루프에 빠집니다.
        en: Without incrementing word index, infinite loops occur.
  - label:
      ko: Backtrack - 셀 방문 해제
      en: Backtrack - unmark cell
    indent: 1
    options:
    - code: path.remove((r, c))
      type: good
      why:
        ko: 재귀 반환 전에 현재 셀을 경로에서 제거합니다. 다른 탐색 경로에서 이 셀을 사용할 수 있게 합니다.
        en: Remove current cell from path before returning. Allows other search paths to use this cell.
    - code: path.discard((r, c))
      type: distractor
      why:
        ko: discard도 작동하지만, 존재하지 않을 시 에러를 발생시키지 않습니다. remove가 더 명시적입니다.
        en: discard works but doesn't error if missing. remove is more explicit.
    - code: '# No backtracking'
      type: distractor
      why:
        ko: Backtracking이 없으면 같은 셀을 다른 경로에서 사용할 수 없어 틀린 결과를 얻습니다.
        en: Without backtracking, cells can't be reused across paths, causing wrong results.
  - label:
      ko: '최적화: 단어 역순 처리'
      en: 'Optimization: reverse word if needed'
    indent: 0
    options:
    - code: count = sum(map(Counter, board), Counter())
      type: good
      why:
        ko: 첫 문자가 마지막 문자보다 더 자주 나타나면 단어를 뒤집습니다. 시작점을 줄여 탐색 공간을 감소시킵니다.
        en: If first character appears more often than last, reverse word. Reduces starting points, shrinking search space.
    - code: 'if count[word[0]] < count[word[-1]]: word = word[::-1]'
      type: distractor
      why:
        ko: 반대 조건입니다. 마지막 문자가 더 자주 나타날 때 역순하는 것도 동일한 효과를 냅니다.
        en: Opposite condition. Reversing when last is more common has the same effect.
    - code: 'if len(word) > 5: word = word[::-1]'
      type: distractor
      why:
        ko: 단어 길이는 최적화 판단과 관계없습니다. 문자 빈도만이 의미 있습니다.
        en: Word length is irrelevant to optimization. Only character frequency matters.
trace:
  code:
  - 'class Solution:'
  - '    def exist(self, board: List[List[str]], word: str) -> bool:'
  - '        ROWS, COLS = len(board), len(board[0])'
  - '        path = set()'
  - ''
  - '        def dfs(r, c, i):'
  - '            if i == len(word):'
  - '                return True'
  - '            if ('
  - '                min(r, c) < 0'
  - '                or r >= ROWS'
  - '                or c >= COLS'
  - '                or word[i] != board[r][c]'
  - '                or (r, c) in path'
  - '            ):'
  - '                return False'
  - '            path.add((r, c))'
  - '            res = ('
  - '                dfs(r + 1, c, i + 1)'
  - '                or dfs(r - 1, c, i + 1)'
  - '                or dfs(r, c + 1, i + 1)'
  - '                or dfs(r, c - 1, i + 1)'
  - '            )'
  - '            path.remove((r, c))'
  - '            return res'
  - ''
  - '        # To prevent TLE,reverse the word if frequency of the first letter is more than the last letter''s'
  - '        count = sum(map(Counter, board), Counter())'
  - '        if count[word[0]] > count[word[-1]]:'
  - '            word = word[::-1]'
  - '            '
  - '        for r in range(ROWS):'
  - '            for c in range(COLS):'
  - '                if dfs(r, c, 0):'
  - '                    return True'
  - '        return False'
  - ''
  - '    # O(n * m * 4^n)'
  cases:
  - input: '[["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]

      "ABCCED"'
    expected: 'true'
  - input: '[["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]

      "SEE"'
    expected: 'true'
  - input: '[["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]

      "ABCB"'
    expected: 'false'
  worked_example:
    input: '[["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]

      "ABCCED"'
    steps:
    - ko: 'i=0, word[0]=''A'': 보드에서 (0,0)의 ''A'' 발견. 매칭 ✓, 경로에 추가.'
      en: 'i=0, word[0]=''A'': Find ''A'' at (0,0). Match ✓, add to path.'
    - ko: 'i=1, word[1]=''B'': (0,0)에서 이웃 (0,1) 확인. ''B'' 매칭 ✓, 경로에 추가.'
      en: 'i=1, word[1]=''B'': Check neighbor (0,1) from (0,0). Match ✓, add to path.'
    - ko: 'i=2, word[2]=''C'': (0,1)에서 이웃 (0,2) 확인. ''C'' 매칭 ✓, 경로에 추가.'
      en: 'i=2, word[2]=''C'': Check neighbor (0,2) from (0,1). Match ✓, add to path.'
    - ko: 'i=3, word[3]=''C'': (0,2)에서 이웃 (1,2) 확인. ''C'' 매칭 ✓, 경로에 추가.'
      en: 'i=3, word[3]=''C'': Check neighbor (1,2) from (0,2). Match ✓, add to path.'
    - ko: 'i=4, word[4]=''E'': (1,2)에서 이웃 (2,2) 확인. ''E'' 매칭 ✓, 경로에 추가.'
      en: 'i=4, word[4]=''E'': Check neighbor (2,2) from (1,2). Match ✓, add to path.'
    - ko: 'i=5, word[5]=''D'': (2,2)에서 이웃 (2,1) 확인. ''D'' 매칭 ✓, i == len(word) → true 반환.'
      en: 'i=5, word[5]=''D'': Check neighbor (2,1) from (2,2). Match ✓, i == len(word) → return true.'
    answer: 'true'
solution:
  code: "class Solution:\n    def exist(self, board: List[List[str]], word: str) -> bool:\n        ROWS, COLS = len(board), len(board[0])\n        path = set()\n\n        def dfs(r, c, i):\n            if i == len(word):\n                return True\n            if (\n                min(r, c) < 0\n                or r >= ROWS\n                or c >= COLS\n                or word[i] != board[r][c]\n                or (r, c) in path\n            ):\n                return False\n            path.add((r, c))\n            res = (\n                dfs(r + 1, c, i + 1)\n                or dfs(r - 1, c, i + 1)\n                or dfs(r, c + 1, i + 1)\n                or dfs(r, c - 1, i + 1)\n            )\n            path.remove((r, c))\n            return res\n\n        # To prevent TLE,reverse the word if frequency of the first letter is more than the last letter's\n        count = sum(map(Counter, board), Counter())\n        if count[word[0]] > count[word[-1]]:\n            word = word[::-1]\n\
    \            \n        for r in range(ROWS):\n            for c in range(COLS):\n                if dfs(r, c, 0):\n                    return True\n        return False\n\n    # O(n * m * 4^n)\n"
  complexity:
    time: O(N × M × 4^L) where N=rows, M=cols, L=word.length
    space: O(L) for recursion call stack depth and path set
  followup:
  - ko: 여러 단어를 동시에 검색해야 한다면? Trie 자료구조를 사용하여 단일 DFS 탐색으로 여러 단어를 병렬로 매칭할 수 있습니다.
    en: How to search for multiple words simultaneously? Use a Trie to match all words in parallel during a single DFS traversal.
  - ko: '보드가 매우 크다면 (예: 1000×1000)? 시작점을 줄이기 위해 첫/마지막 문자 빈도 휴리스틱을 강화하거나, 희소 인덱싱을 추가할 수 있습니다.'
    en: For very large boards (e.g., 1000×1000)? Enhance character frequency heuristics or add sparse indexing to reduce starting points.
  - ko: 공간을 O(1)로 줄일 수 있을까? 보드 셀을 직접 수정하여 방문 표시하고, 재귀 후 원래 값을 복원하면 추가 공간 없이 해결됩니다.
    en: Can we reduce space to O(1)? Mark visited cells directly on the board and restore them after recursion.
```