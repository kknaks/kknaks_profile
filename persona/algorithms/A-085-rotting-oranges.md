---
created: '2026-08-12'
date: '2026-08-12'
day: Day 85
difficulty: medium
id: A-085
source:
  curated_in:
  - neetcode150
  number: 994
  platform: leetcode
  slug: rotting-oranges
  url: https://leetcode.com/problems/rotting-oranges/
status: draft
tags:
- array
- breadth-first-search
- matrix
title:
  en: Rotting Oranges
  ko: 썩은 오렌지
today: true
type: algorithm
updated: '2026-08-12'
visible: true
---

# 썩은 오렌지

## Data

```yaml
problem:
  title:
    ko: 썩은 오렌지
    en: Rotting Oranges
  statement:
    ko: 'm × n 격자가 주어집니다. 각 셀은 다음 세 가지 값 중 하나를 가질 수 있습니다:


      - 0: 빈 셀

      - 1: 신선한 오렌지

      - 2: 썩은 오렌지


      매 분마다, 상하좌우로 인접한(4방향) 썩은 오렌지와 접한 신선한 오렌지는 썩게 됩니다.


      신선한 오렌지가 남아있지 않을 때까지 경과해야 하는 최소 분 수를 반환하세요. 만약 신선한 오렌지를 모두 썩게 할 수 없다면 -1을 반환하세요.'
    en: 'You are given an m x n grid where each cell can have one of three values:


      - 0 representing an empty cell,

      - 1 representing a fresh orange, or

      - 2 representing a rotten orange.


      Every minute, any fresh orange that is 4-directionally adjacent to a rotten orange becomes rotten.


      Return the minimum number of minutes that must elapse until no cell has a fresh orange. If this is impossible, return -1.'
  constraints:
  - 1 ≤ m, n ≤ 10
  - grid[i][j] is 0, 1, or 2
  - m == grid.length
  - n == grid[i].length
  io:
  - input: '[[2,1,1],[1,1,0],[0,1,1]]'
    output: '4'
  - input: '[[2,1,1],[0,1,1],[1,0,1]]'
    output: '-1'
  - input: '[[0,2]]'
    output: '0'
clarifying:
  items:
  - q:
      ko: 4방향 인접이란 정확히 무엇을 의미하나요?
      en: What exactly does '4-directionally adjacent' mean?
    type: good
    why:
      ko: 상하좌우(위, 아래, 왼쪽, 오른쪽)를 의미하며, 대각선은 포함하지 않습니다.
      en: It means up, down, left, and right neighbors only—diagonals are not included.
  - q:
      ko: 입력 격자를 수정할 수 있나요?
      en: Can we modify the input grid?
    type: good
    why:
      ko: 네, 신선한 오렌지를 썩은 것으로 표시하면서 동시에 몇 분이 지났는지 추적할 수 있습니다.
      en: Yes, we can mark fresh oranges as rotten while simultaneously tracking how many minutes have passed.
  - q:
      ko: 처음부터 신선한 오렌지가 없다면 답은 무엇인가요?
      en: If there are no fresh oranges initially, what should we return?
    type: good
    why:
      ko: 시간이 지날 필요가 없으므로 0을 반환합니다.
      en: Since no time is needed to rot all oranges, return 0.
  - q:
      ko: 일부 신선한 오렌지에 도달할 수 없다면?
      en: What if some fresh oranges can never be reached?
    type: good
    why:
      ko: 모든 신선한 오렌지를 썩힐 수 없으므로 -1을 반환합니다.
      en: Since we cannot rot all fresh oranges, we return -1.
  - q:
      ko: 오렌지는 대각선 방향으로도 썩나요?
      en: Can oranges rot diagonally?
    type: distractor
    why:
      ko: 아니오, 문제에서 명시적으로 4방향만 언급하고 있습니다.
      en: No, the problem explicitly specifies 4-directional spread only.
  - q:
      ko: 썩는 순서가 결과에 영향을 미치나요?
      en: Does the order in which oranges rot affect the result?
    type: distractor
    why:
      ko: BFS는 동시에 모든 썩은 오렌지에서 시작하므로 순서와 무관하게 최단 시간을 보장합니다.
      en: BFS starts from all rotten oranges simultaneously, guaranteeing minimum time regardless of processing order.
approach:
  items:
  - name:
      ko: 다중 출발점 BFS
      en: Multi-source BFS
    complexity: O(m*n) time / O(m*n) space
    type: good
    why:
      ko: 모든 썩은 오렌지에서 동시에 시작하여 격자를 레벨별로 탐색하면 최소 시간을 찾을 수 있습니다.
      en: Starting simultaneously from all rotten oranges and exploring level-by-level guarantees the minimum time to rot all reachable oranges.
  - name:
      ko: 심층 우선 탐색(DFS)
      en: Depth-First Search (DFS)
    complexity: O(m*n) time / O(m*n) space
    type: distractor
    why:
      ko: DFS로도 모든 오렌지를 찾을 수 있지만, 시간을 추적하기 위해 깊이를 기록해야 하므로 BFS의 자연스러운 레벨 처리보다 복잡합니다.
      en: While DFS can find all oranges, tracking depth for minutes is harder than BFS's natural level-by-level propagation.
  - name:
      ko: 시뮬레이션
      en: Brute Force Simulation
    complexity: O(m*n*max_time) time / O(m*n) space
    type: distractor
    why:
      ko: 매 분마다 모든 셀을 검사하면 작동하지만 비효율적입니다. 실제 시간 값을 미리 알 수 없으므로 검사 범위가 불명확합니다.
      en: Checking every cell every minute works but is inefficient; we don't know the time bound in advance.
  - name:
      ko: 탐욕 알고리즘(한 개의 썩은 오렌지에서 시작)
      en: Greedy (single source)
    complexity: O(m*n) time / O(m*n) space
    type: distractor
    why:
      ko: 하나의 썩은 오렌지를 선택하여 시작하면 다른 썩은 오렌지로부터의 병렬 확산을 무시하므로 최소 시간을 보장하지 않습니다.
      en: Choosing a single rotten orange misses parallel spreading from other sources, failing to find true minimum time.
logic:
  format: slot
  slots:
  - label:
      ko: 큐 초기화
      en: Initialize queue
    indent: 0
    options:
    - code: q = collections.deque()
      type: good
      why:
        ko: BFS를 위해 deque를 사용하면 O(1) 시간에 양쪽 끝에서 추가/제거할 수 있습니다.
        en: Deque allows O(1) append/popleft operations, essential for efficient BFS queue management.
    - code: q = []
      type: distractor
      why:
        ko: 리스트는 작동하지만 popleft()에 해당하는 pop(0)이 O(n)이므로 성능이 좋지 않습니다.
        en: Lists work but pop(0) is O(n), making the overall algorithm slower.
    - code: q = set()
      type: distractor
      why:
        ko: 집합은 순서를 보장하지 않아 BFS의 레벨별 처리가 불가능합니다.
        en: Sets are unordered, breaking the level-by-level property essential to BFS.
  - label:
      ko: 초기 썩은 오렌지 큐에 추가
      en: Queue initial rotten oranges
    indent: 1
    options:
    - code: q.append((r, c))
      type: good
      why:
        ko: 모든 썩은 오렌지(값 2)를 큐에 추가하면 다중 출발점 BFS의 출발점이 되어 동시에 모든 방향으로 확산을 시작할 수 있습니다.
        en: Queueing all rotten oranges allows multi-source BFS to start from all sources simultaneously, modeling real-world parallel spreading.
    - code: q.append([r, c])
      type: distractor
      why:
        ko: 리스트로 추가할 수 있지만, 튜플이 불변이므로 더 효율적입니다.
        en: Lists work but tuples are more memory-efficient for immutable coordinate pairs.
    - code: '# 큐에 추가하지 않음'
      type: distractor
      why:
        ko: 썩은 오렌지를 기록하지 않으면 BFS 출발점이 없어 알고리즘이 실행되지 않습니다.
        en: Without queueing rotten oranges, BFS has no starting points and cannot proceed.
  - label:
      ko: BFS 루프 조건
      en: BFS loop condition
    indent: 0
    options:
    - code: 'while fresh > 0 and q:'
      type: good
      why:
        ko: 신선한 오렌지가 남아있고 큐가 비어있지 않을 때만 반복합니다. 큐가 비었으나 신선한 오렌지가 남으면 일부 오렌지에 도달할 수 없다는 뜻이므로 -1을 반환해야 합니다.
        en: Continue only while fresh oranges remain and the queue is not empty. Queue empty with fresh > 0 means some oranges are unreachable.
    - code: 'while q:'
      type: distractor
      why:
        ko: 신선한 오렌지 확인을 빠뜨리면 큐가 비었을 때 루프가 끝나지만, fresh 상태를 확인하지 않아 -1을 반환해야 하는 경우를 놓칩니다.
        en: This misses the fresh orange check; loop ends when queue is empty, failing to detect unreachable fresh oranges.
    - code: 'while fresh > 0:'
      type: distractor
      why:
        ko: 큐 상태를 확인하지 않으면 큐가 비었을 때도 루프를 계속 실행하려고 시도할 수 있습니다.
        en: This misses the queue check; if queue is empty but fresh > 0, the loop tries to continue without items to process.
  - label:
      ko: 현재 레벨 크기 스냅샷
      en: Snapshot current level size
    indent: 1
    options:
    - code: length = len(q)
      type: good
      why:
        ko: 큐의 현재 길이를 저장하면, 새로운 항목을 추가하면서도 정확히 현재 레벨의 모든 오렌지를 처리한 후에만 시간을 증가시킬 수 있습니다.
        en: Snapshotting queue length ensures we process exactly all oranges at the current generation before incrementing time for the next.
    - code: 'for i in range(len(q)): # 루프 중 길이 변경'
      type: distractor
      why:
        ko: range()는 루프 시작 시 범위를 정하지만, 새 항목 추가 후 i가 범위를 초과할 수 있습니다.
        en: range() fixes the loop count at start, but appending new items can cause index out of range or missed items.
    - code: length = len(q) - 1
      type: distractor
      why:
        ko: off-by-one 오류로 마지막 오렌지를 건너뜁니다.
        en: Off-by-one error skips the last orange in the current level.
  - label:
      ko: 4방향 확인
      en: Check 4 directions
    indent: 2
    options:
    - code: 'for dr, dc in directions:'
      type: good
      why:
        ko: 미리 정의된 방향 배열을 반복하면 4방향을 간결하고 확장성 있게 확인할 수 있습니다.
        en: Iterating through a predefined directions array is clean, avoids repetition, and makes it easy to add 8-directional variants.
    - code: '# (r-1,c), (r+1,c), (r,c-1), (r,c+1)을 각각 4개 if문으로 확인'
      type: distractor
      why:
        ko: 4개의 if 문으로 작동하지만 반복 코드가 많고 유지보수가 어렵습니다.
        en: Using four separate if-statements works but is repetitive and harder to modify for variants.
    - code: 'for dr, dc in [[-1,-1], [-1,0], [-1,1], [0,-1], [0,1], [1,-1], [1,0], [1,1]]:'
      type: distractor
      why:
        ko: 8방향(대각선 포함)을 확인하면 문제 요구사항을 벗어납니다.
        en: Including diagonals violates the 4-directional requirement and produces incorrect results.
  - label:
      ko: 신선한 오렌지 검증 및 표시
      en: Validate and mark fresh orange
    indent: 3
    options:
    - code: and grid[row][col] == 1
      type: good
      why:
        ko: grid[row][col] == 1 확인으로 신선한 오렌지만 처리하고, 이미 썩은 오렌지(2)나 빈 셀(0)은 무시하여 중복 처리를 방지합니다.
        en: Checking grid[row][col] == 1 ensures only fresh oranges are processed; rotten (2) and empty (0) cells are skipped, preventing duplicates.
    - code: 'and grid[row][col] != 0:'
      type: distractor
      why:
        ko: 0이 아닌 모든 값(1과 2)을 포함하므로 이미 썩은 오렌지를 다시 큐에 추가할 수 있습니다.
        en: This matches both fresh (1) and rotten (2), risking duplicate processing of already-rotten oranges.
    - code: 'and grid[row][col] > 0:'
      type: distractor
      why:
        ko: 이 조건도 1과 2를 모두 포함합니다.
        en: This also matches both 1 and 2, causing the same duplicate problem.
  - label:
      ko: 시간 증가
      en: Increment time after level
    indent: 1
    options:
    - code: time += 1
      type: good
      why:
        ko: 각 레벨 처리 후에만 시간을 증가시키므로, 각 세대가 정확히 1분씩 카운트되고 동시 확산이 올바르게 모델링됩니다.
        en: Incrementing after processing the entire level ensures each generation is counted exactly once, correctly modeling simultaneous propagation.
    - code: 'time += 1  # 내부 for 루프 (i in range(length)) 안에서'
      type: distractor
      why:
        ko: 내부 루프 안에서 증가시키면 각 오렌지마다 증가하여 시간이 과다 카운트됩니다.
        en: Incrementing inside the inner loop counts each orange as a time step, greatly over-counting actual minutes.
    - code: '# time 증가 없음'
      type: distractor
      why:
        ko: 시간을 증가시키지 않으면 항상 0을 반환하게 되어 알고리즘이 완전히 실패합니다.
        en: Without incrementing, the algorithm always returns 0 regardless of actual spread duration.
trace:
  code:
  - 'class Solution:'
  - '    def orangesRotting(self, grid: List[List[int]]) -> int:'
  - '        q = collections.deque()'
  - '        fresh = 0'
  - '        time = 0'
  - ''
  - '        for r in range(len(grid)):'
  - '            for c in range(len(grid[0])):'
  - '                if grid[r][c] == 1:'
  - '                    fresh += 1'
  - '                if grid[r][c] == 2:'
  - '                    q.append((r, c))'
  - ''
  - '        directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]'
  - '        while fresh > 0 and q:'
  - '            length = len(q)'
  - '            for i in range(length):'
  - '                r, c = q.popleft()'
  - ''
  - '                for dr, dc in directions:'
  - '                    row, col = r + dr, c + dc'
  - '                    # if in bounds and nonrotten, make rotten'
  - '                    # and add to q'
  - '                    if ('
  - '                        row in range(len(grid))'
  - '                        and col in range(len(grid[0]))'
  - '                        and grid[row][col] == 1'
  - '                    ):'
  - '                        grid[row][col] = 2'
  - '                        q.append((row, col))'
  - '                        fresh -= 1'
  - '            time += 1'
  - '        return time if fresh == 0 else -1'
  cases:
  - input: '[[2,1,1],[1,1,0],[0,1,1]]'
    expected: '4'
  - input: '[[2,1,1],[0,1,1],[1,0,1]]'
    expected: '-1'
  - input: '[[0,2]]'
    expected: '0'
  worked_example:
    input: '[[2,1,1],[1,1,0],[0,1,1]]'
    steps:
    - ko: '초기: (0,0)에 썩은 오렌지 1개, 신선한 오렌지 6개 식별 후 (0,0)을 큐에 추가'
      en: 'Initial: Identify 1 rotten orange at (0,0) and 6 fresh oranges; queue (0,0)'
    - ko: '분 1: (0,0)이 인접한 (0,1), (1,0) 감염 → 신선한 오렌지 4개 남음'
      en: 'Minute 1: (0,0) infects neighbors (0,1) and (1,0) → 4 fresh remain'
    - ko: '분 2: (0,1), (1,0)이 (0,2), (1,1) 감염 → 신선한 오렌지 2개 남음'
      en: 'Minute 2: (0,1) and (1,0) infect (0,2) and (1,1) → 2 fresh remain'
    - ko: '분 3~4: 계속 확산하여 (2,1), (2,2) 감염 → 신선한 오렌지 0개 (답: 4)'
      en: 'Minutes 3–4: Spread continues, infecting (2,1) and (2,2) → 0 fresh remain (return 4)'
    answer: '4'
solution:
  code: "class Solution:\n    def orangesRotting(self, grid: List[List[int]]) -> int:\n        q = collections.deque()\n        fresh = 0\n        time = 0\n\n        for r in range(len(grid)):\n            for c in range(len(grid[0])):\n                if grid[r][c] == 1:\n                    fresh += 1\n                if grid[r][c] == 2:\n                    q.append((r, c))\n\n        directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]\n        while fresh > 0 and q:\n            length = len(q)\n            for i in range(length):\n                r, c = q.popleft()\n\n                for dr, dc in directions:\n                    row, col = r + dr, c + dc\n                    # if in bounds and nonrotten, make rotten\n                    # and add to q\n                    if (\n                        row in range(len(grid))\n                        and col in range(len(grid[0]))\n                        and grid[row][col] == 1\n                    ):\n                        grid[row][col]\
    \ = 2\n                        q.append((row, col))\n                        fresh -= 1\n            time += 1\n        return time if fresh == 0 else -1\n"
  complexity:
    time: O(m*n)
    space: O(m*n)
  followup:
  - ko: 대각선 방향으로도 썩음이 전파된다면 어떻게 달라질까요?
    en: How would the solution change if oranges rot in 8 directions including diagonals?
  - ko: 입력 격자를 수정하지 않으면서 해결할 수 있나요?
    en: Can you solve this without modifying the input grid?
  - ko: 격자의 크기가 매우 크다면 공간을 더 최적화할 수 있나요?
    en: Can space be optimized further for very large grids, or is O(m*n) necessary for BFS?
```