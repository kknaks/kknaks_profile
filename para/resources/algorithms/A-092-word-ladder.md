---
created: '2026-08-20'
date: '2026-08-20'
day: Day 92
difficulty: hard
id: A-092
source:
  curated_in:
  - neetcode150
  number: 127
  platform: leetcode
  slug: word-ladder
  url: https://leetcode.com/problems/word-ladder/
tags:
- hash-table
- string
- breadth-first-search
- bidirectional-search
title:
  en: Word Ladder
  ko: 단어 사다리
today: false
type: algorithm
updated: '2026-08-20'
visible: true
---

# 단어 사다리

## Data

```yaml
problem:
  title:
    ko: 단어 사다리
    en: Word Ladder
  statement:
    ko: '단어 beginWord에서 단어 endWord로의 변환 수열은 다음 조건을 만족하는 단어들의 수열입니다:


      인접한 단어 쌍은 정확히 한 글자만 다릅니다.

      모든 중간 단어는 wordList에 있어야 합니다. beginWord는 wordList에 없어도 됩니다.

      마지막 단어는 endWord와 같아야 합니다.


      두 단어 beginWord와 endWord, 그리고 사전 wordList가 주어질 때, beginWord에서 endWord로의 최단 변환 수열에 포함된 단어의 개수를 반환하세요. 그러한 수열이 없으면 0을 반환하세요.'
    en: 'A transformation sequence from word beginWord to word endWord using a dictionary wordList is a sequence of words such that:


      Every adjacent pair of words differs by a single letter.

      Every word in the sequence (except the first) must be in wordList. Note that beginWord does not need to be in wordList.

      The last word of the sequence must be endWord.


      Given two words, beginWord and endWord, and a dictionary wordList, return the number of words in the shortest transformation sequence from beginWord to endWord, or 0 if no such sequence exists.'
  constraints:
  - 1 ≤ beginWord.length ≤ 10
  - endWord.length == beginWord.length
  - 1 ≤ wordList.length ≤ 5000
  - All words consist of lowercase English letters
  - beginWord ≠ endWord
  io:
  - input: '"hit"

      "cog"

      ["hot","dot","dog","lot","log","cog"]'
    output: '5'
  - input: '"hit"

      "cog"

      ["hot","dot","dog","lot","log"]'
    output: '0'
clarifying:
  items:
  - q:
      ko: 정확히 한 글자만 다른다는 것은 무엇을 의미하나요?
      en: What does it mean for two words to differ by exactly one letter?
    type: good
    why:
      ko: '두 단어가 정확히 한 위치의 문자가 다르고 나머지는 모두 같아야 함을 확인합니다. 예: ''hit''(i→o) → ''hot''은 인접하지만, ''hit'' → ''dog''(2개 위치 차이)는 인접하지 않습니다.'
      en: Two words are adjacent if they differ at exactly one position. For example, 'hit' and 'hot' differ only at position 1 (i→o), but 'hit' and 'dog' differ at two positions, so they are not adjacent.
  - q:
      ko: 최단 경로 자체를 반환해야 하나요, 아니면 경로의 길이만 반환하나요?
      en: Should we return the actual shortest path or just the length of the path?
    type: good
    why:
      ko: 문제는 '최단 변환 수열에 포함된 단어의 개수'를 명확히 요구하므로 길이만 반환하면 됩니다.
      en: The problem explicitly asks for 'the number of words' in the shortest sequence, not the sequence itself.
  - q:
      ko: 각 단어를 변환 경로에서 두 번 이상 사용할 수 있나요?
      en: Can we use the same word multiple times in a transformation sequence?
    type: good
    why:
      ko: 각 단어는 최대 한 번만 방문해야 하므로 중복 사용은 불가능합니다. visited 집합이 이를 강제합니다.
      en: No. Each word should be visited at most once in a path to avoid cycles. The visited set enforces this constraint.
  - q:
      ko: beginWord가 wordList에 포함되어야 하나요?
      en: Does beginWord need to be in wordList?
    type: distractor
    why:
      ko: 아니요. 문제는 'beginWord는 wordList에 없어도 됩니다'라고 명시합니다. 코드는 wordList.append(beginWord)로 동적으로 추가하여 패턴 매칭을 포함합니다.
      en: No. The problem explicitly states beginWord does not need to be in wordList. The solution adds it dynamically for pattern matching.
  - q:
      ko: 최단 경로가 여러 개 있으면 사전순이 가장 작은 것을 반환해야 하나요?
      en: If multiple shortest paths exist with the same length, should we return the lexicographically smallest one?
    type: distractor
    why:
      ko: 아니요. 모든 최단 경로의 길이가 같으므로 어떤 경로든 상관없이 그 길이만 반환하면 됩니다.
      en: No. Since all shortest paths have the same length, we only return the length, not a specific path.
  - q:
      ko: BFS 대신 DFS를 사용하여 최단 경로를 찾을 수 있나요?
      en: Could we use DFS instead of BFS to find the shortest path?
    type: distractor
    why:
      ko: DFS는 깊이 우선으로 탐색하므로 처음 도달한 경로가 최단이 아닐 수 있습니다. BFS는 레벨별로 탐색하므로 처음 도달한 것이 반드시 최단입니다.
      en: No. DFS explores depth-first and doesn't guarantee shortest path. BFS explores level-by-level, ensuring the first time we reach endWord is via the shortest path.
approach:
  items:
  - name:
      ko: 패턴 매칭을 이용한 BFS
      en: BFS with Wildcard Pattern Matching
    complexity: O(N × L²) time / O(N × L) space
    type: good
    why:
      ko: 각 단어의 각 위치에 *를 대입하여 패턴을 생성합니다. 같은 패턴을 가진 단어들은 한 글자만 차이나므로 인접합니다. BFS로 최단 경로를 보장합니다.
      en: Create wildcard patterns by replacing each position with *. Words with the same pattern differ by exactly one letter. BFS level-by-level exploration guarantees the first time we reach endWord is via the shortest path.
  - name:
      ko: 양방향 BFS
      en: Bidirectional BFS
    complexity: O(N × L²) time / O(N × L) space
    type: good
    why:
      ko: beginWord와 endWord에서 동시에 BFS를 진행합니다. 두 탐색이 중간에서 만날 때까지 진행합니다. 시간복잡도는 같지만 탐색 범위를 크게 줄여 실제로 훨씬 빠릅니다.
      en: Search from both beginWord and endWord simultaneously, meeting in the middle. Same asymptotic complexity but searches fewer nodes in practice since BFS search space grows exponentially.
  - name:
      ko: 모든 단어 쌍 비교
      en: Direct Pairwise Comparison
    complexity: O(N² × L) time / O(N) space
    type: distractor
    why:
      ko: 모든 단어 쌍을 비교하여 한 글자만 다른지 확인합니다. 개념은 간단하지만 N=5000일 때 약 2,500만 번의 비교가 필요하므로 매우 비효율적입니다.
      en: Compare every pair of words to check if they differ by exactly one letter. Simple conceptually, but O(N²) comparisons are prohibitively slow for N=5000.
  - name:
      ko: 깊이 우선 탐색 (DFS)
      en: Depth-First Search
    complexity: O(N!) worst case / O(N) space
    type: distractor
    why:
      ko: DFS는 모든 경로를 탐색하므로 최단 경로를 보장하지 않습니다. 또한 그래프 구조에서는 최악의 경우 지수 시간이 필요합니다.
      en: DFS explores all paths without level-order guarantee, so it doesn't find the shortest path first. Also much slower than BFS for this problem.
  - name:
      ko: 편집 거리 계산
      en: Edit Distance Calculation
    complexity: O(N² × L²) time / O(L²) space
    type: distractor
    why:
      ko: 각 단어 쌍의 편집 거리를 DP로 계산하여 거리가 1인 쌍을 찾습니다. 개념은 같지만 DP 오버헤드로 패턴 매칭보다 느립니다.
      en: Calculate edit distance between word pairs using DP. Conceptually similar but adds DP overhead on top of O(N²) comparisons, making it slower than pattern matching.
logic:
  format: slot
  slots:
  - label:
      ko: endWord 존재 여부 확인
      en: Validate endWord exists
    indent: 0
    options:
    - code: 'if endWord not in wordList:'
      type: good
      why:
        ko: endWord가 wordList에 없으면 경로가 존재할 수 없으므로 즉시 0을 반환합니다. 불필요한 그래프 구축을 피합니다.
        en: If endWord is not in wordList, no transformation sequence can reach it. Return 0 immediately to avoid unnecessary graph construction.
    - code: 'if beginWord not in wordList:'
      type: distractor
      why:
        ko: beginWord는 wordList에 없어도 되므로 이 조건은 필요 없고 오류를 일으킵니다.
        en: beginWord doesn't need to be in wordList (it's added dynamically), so this check is wrong.
    - code: 'if endWord not in wordList or len(wordList) == 0:'
      type: distractor
      why:
        ko: wordList가 비어있으면 어차피 endWord가 없으므로 두 번째 조건은 중복입니다.
        en: If wordList is empty, the first condition already handles it. The second check is redundant.
  - label:
      ko: 와일드카드 패턴 생성
      en: Create wildcard pattern
    indent: 2
    options:
    - code: pattern = word[:j] + "*" + word[j + 1 :]
      type: good
      why:
        ko: '각 위치 j에 *를 대입하여 패턴을 생성합니다. 예: ''hot''에서 ''*ot'', ''h*t'', ''ho*''를 만들어 한 글자 차이 단어들을 그룹화합니다.'
        en: 'Replace character at position j with * to create patterns. For ''hot'': ''*ot'', ''h*t'', ''ho*''. Words sharing a pattern differ by exactly one letter at position j.'
    - code: pattern = word[:j] + "*" + word[j + 2:]
      type: distractor
      why:
        ko: word[j+2:]는 한 글자를 건너뛰므로 패턴이 잘못됩니다. word[j+1:]이 정확합니다.
        en: Skipping to word[j+2:] creates incorrect patterns that skip one character.
    - code: pattern = "*" * len(word)
      type: distractor
      why:
        ko: 모든 위치를 *로 바꾸면 모든 단어가 같은 패턴이 되어 무의미합니다.
        en: Replacing all characters with * makes all words match the same pattern, losing the one-letter-difference constraint.
  - label:
      ko: 시작 단어 방문 표시
      en: Mark start word as visited
    indent: 0
    options:
    - code: visit = set([beginWord])
      type: good
      why:
        ko: beginWord를 visited 집합에 추가합니다. BFS 중에 시작 단어를 다시 방문하는 것을 방지하여 사이클을 막습니다.
        en: Add beginWord to visited set to prevent revisiting it during BFS. Prevents infinite loops where we might return to the start word.
    - code: visit = set(wordList)
      type: distractor
      why:
        ko: wordList의 모든 단어를 미리 방문한 것으로 표시하면 BFS가 진행되지 않습니다.
        en: Marking all words as visited prevents us from exploring any neighbors, making BFS impossible.
    - code: visit = set()
      type: distractor
      why:
        ko: 방문 집합이 비어있으면 같은 단어를 무한히 재방문할 수 있어 무한 루프가 발생합니다.
        en: An empty visited set allows revisiting the same word infinitely, causing infinite loops.
  - label:
      ko: BFS 메인 루프 시작
      en: BFS main loop
    indent: 0
    options:
    - code: 'while q:'
      type: good
      why:
        ko: 큐가 비워질 때까지 계속 반복합니다. 각 루프 반복은 하나의 거리 레벨을 나타내므로 res를 증가시켜 거리를 추적합니다.
        en: Continue while there are words to explore in the queue. Each outer loop iteration represents one distance level, which is why res increments at the end of each iteration.
    - code: 'while len(q) > 0:'
      type: distractor
      why:
        ko: 기능적으로는 동일하지만 파이썬 관례상 'while q:'가 더 간결하고 관례적입니다.
        en: Functionally equivalent but 'while q:' is more Pythonic and idiomatic in Python.
    - code: 'for _ in range(len(wordList)):'
      type: distractor
      why:
        ko: 고정 반복 횟수로는 동적 큐 크기를 추적할 수 없습니다. 미처 탐색하지 못하거나 불필요한 반복이 발생합니다.
        en: A fixed loop over wordList length doesn't track dynamic queue changes. May explore beyond necessary or exit early.
  - label:
      ko: 도착지 확인 및 반환
      en: Check if destination reached
    indent: 2
    options:
    - code: 'if word == endWord:'
      type: good
      why:
        ko: 현재 단어가 endWord와 같으면 최단 경로를 찾은 것입니다. BFS는 레벨별 탐색이므로 처음 도달이 최단입니다. 현재 거리(res)를 반환합니다.
        en: When we reach endWord, we've found the shortest path because BFS explores level-by-level. The first arrival guarantees optimality. Return current distance immediately.
    - code: 'if neiWord == endWord:'
      type: distractor
      why:
        ko: 이웃 단어가 아니라 현재 단어와 비교해야 합니다. 또한 큐에 추가하기 전에 확인하면 더 효율적입니다.
        en: We should check the current word, not neighbors. Checking neighbors before adding to queue would be more efficient.
    - code: 'if word == endWord: res -= 1; return res'
      type: distractor
      why:
        ko: endWord에 도달했을 때 거리를 감소시킬 이유가 없습니다. 현재 res 값이 정확한 거리입니다.
        en: There's no reason to decrement res when endWord is reached. The current res value is the correct distance.
  - label:
      ko: 거리 카운터 증가
      en: Increment distance counter
    indent: 1
    options:
    - code: res += 1
      type: good
      why:
        ko: 현재 레벨의 모든 단어를 처리한 후 다음 레벨의 거리를 1 증가시킵니다. while 루프 본체의 끝, 내부 for 루프 바깥에 위치해야 정확합니다.
        en: After processing all words at the current level, increment distance for the next level. Must be outside the inner loop (inside while loop) to count levels correctly.
    - code: res += len(q)
      type: distractor
      why:
        ko: 큐의 크기를 더하면 거리가 기하급수적으로 증가하여 완전히 잘못된 결과를 줍니다.
        en: Adding queue length causes distance to grow exponentially (multiplicatively), giving completely wrong results.
    - code: res += 1 (inside inner for loop)
      type: distractor
      why:
        ko: 내부 for 루프 안에 있으면 현재 레벨의 각 단어마다 증가되어 거리가 과대 계산됩니다.
        en: If inside the inner loop, res increments for each word in the level, overcounting the distance.
trace:
  code:
  - 'class Solution:'
  - '    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:'
  - '        if endWord not in wordList:'
  - '            return 0'
  - ''
  - '        nei = collections.defaultdict(list)'
  - '        wordList.append(beginWord)'
  - '        for word in wordList:'
  - '            for j in range(len(word)):'
  - '                pattern = word[:j] + "*" + word[j + 1 :]'
  - '                nei[pattern].append(word)'
  - ''
  - '        visit = set([beginWord])'
  - '        q = deque([beginWord])'
  - '        res = 1'
  - '        while q:'
  - '            for i in range(len(q)):'
  - '                word = q.popleft()'
  - '                if word == endWord:'
  - '                    return res'
  - '                for j in range(len(word)):'
  - '                    pattern = word[:j] + "*" + word[j + 1 :]'
  - '                    for neiWord in nei[pattern]:'
  - '                        if neiWord not in visit:'
  - '                            visit.add(neiWord)'
  - '                            q.append(neiWord)'
  - '            res += 1'
  - '        return 0'
  cases:
  - input: '"hit"

      "cog"

      ["hot","dot","dog","lot","log","cog"]'
    expected: '5'
  - input: '"hit"

      "cog"

      ["hot","dot","dog","lot","log"]'
    expected: '0'
  worked_example:
    input: '"hit"

      "cog"

      ["hot","dot","dog","lot","log","cog"]'
    steps:
    - ko: '그래프 구성: 단어 간 연결 관계를 패턴으로 정의합니다. 예: ''hit''↔''hot'' (h*t), ''hot''↔''dot'' (*ot), ''hot''↔''lot'' (*ot), ''dot''↔''dog'' (do*), ''dog''↔''log'' (d*g), ''dog''↔''cog'' (d*g), ''log''↔''lot'' (lo*), ''log''↔''cog'' (*og).'
      en: 'Build pattern graph: ''hit''↔''hot'', ''hot''↔''dot'', ''hot''↔''lot'', ''dot''↔''dog'', ''dog''↔''log'', ''dog''↔''cog'', ''lot''↔''log'', ''log''↔''cog''. Start BFS from ''hit'' with queue=[''hit''], res=1.'
    - ko: '레벨 1 처리: ''hit'' 팝. ''cog''이 아님. 이웃 ''hot'' 발견 및 추가. queue=[''hot''], res=2.'
      en: 'Level 1: Dequeue ''hit'', not endWord. Find neighbor ''hot'', add to queue. queue=[''hot''], res=2.'
    - ko: '레벨 2 처리: ''hot'' 팝. ''cog''이 아님. 이웃 ''dot'', ''lot'' 발견 및 추가. queue=[''dot'',''lot''], res=3.'
      en: 'Level 2: Dequeue ''hot'', not endWord. Find neighbors ''dot'', ''lot'', add them. queue=[''dot'',''lot''], res=3.'
    - ko: '레벨 3 처리: ''dot'' 팝 → ''dog'' 추가, ''lot'' 팝 → ''log'' 추가. queue=[''dog'',''log''], res=4.'
      en: 'Level 3: Dequeue ''dot'' → add ''dog''. Dequeue ''lot'' → add ''log''. queue=[''dog'',''log''], res=4.'
    - ko: '레벨 4 처리: ''dog'' 팝 → ''cog'' 추가, ''log'' 팝 → ''cog'' 이미 방문. queue=[''cog''], res=5.'
      en: 'Level 4: Dequeue ''dog'' → add ''cog''. Dequeue ''log'' → ''cog'' already visited. queue=[''cog''], res=5.'
    - ko: '레벨 5 처리: ''cog'' 팝 → ''cog'' == endWord. 반환: res=5.'
      en: 'Level 5: Dequeue ''cog''. Found endWord! Return res=5.'
    answer: '5'
solution:
  code: "class Solution:\n    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:\n        if endWord not in wordList:\n            return 0\n\n        nei = collections.defaultdict(list)\n        wordList.append(beginWord)\n        for word in wordList:\n            for j in range(len(word)):\n                pattern = word[:j] + \"*\" + word[j + 1 :]\n                nei[pattern].append(word)\n\n        visit = set([beginWord])\n        q = deque([beginWord])\n        res = 1\n        while q:\n            for i in range(len(q)):\n                word = q.popleft()\n                if word == endWord:\n                    return res\n                for j in range(len(word)):\n                    pattern = word[:j] + \"*\" + word[j + 1 :]\n                    for neiWord in nei[pattern]:\n                        if neiWord not in visit:\n                            visit.add(neiWord)\n                            q.append(neiWord)\n            res += 1\n  \
    \      return 0\n"
  complexity:
    time: O(N × L²)
    space: O(N × L)
  followup:
  - ko: '최단 경로의 실제 단어 목록(예: [''hit'',''hot'',''dot'',''dog'',''cog''])을 반환하려면 어떻게 수정하시겠습니까?'
    en: How would you modify the solution to return the actual shortest path (sequence of words) instead of just the count?
  - ko: 양방향 BFS를 구현한다면 성능이 어떻게 개선되고, 코드는 어떻게 변할까요?
    en: How would implementing bidirectional BFS improve performance in practice, and what code changes are needed?
  - ko: 단어 리스트가 100,000개로 매우 커지면 현재 접근법의 주요 병목은 무엇이고, 어떻게 최적화할 수 있을까요?
    en: What would be the main bottleneck if wordList had 100,000 words, and how could you optimize for large dictionaries?
```