---
created: '2026-08-15'
date: '2026-08-15'
day: Day 88
difficulty: medium
id: A-088
source:
  curated_in:
  - neetcode150
  number: 210
  platform: leetcode
  slug: course-schedule-ii
  url: https://leetcode.com/problems/course-schedule-ii/
tags:
- depth-first-search
- breadth-first-search
- graph
- topological-sort
title:
  en: Course Schedule II
  ko: 강의 일정 II
today: false
type: algorithm
updated: '2026-08-15'
visible: true
---

# 강의 일정 II

## Data

```yaml
problem:
  title:
    ko: 강의 일정 II
    en: Course Schedule II
  statement:
    ko: '총 numCourses개의 강의를 이수해야 합니다. 강의는 0부터 numCourses-1로 번호가 매겨져 있습니다. prerequisites 배열이 주어지는데, prerequisites[i] = [a, b]는 강의 a를 들으려면 먼저 강의 b를 완료해야 함을 의미합니다.


      예를 들어, [0, 1]은 강의 0을 들으려면 먼저 강의 1을 들어야 합니다는 뜻입니다.


      모든 강의를 마칠 수 있도록 강의를 들어야 하는 순서를 반환하세요. 가능한 순서가 여러 개라면 그 중 어느 것이든 반환해도 됩니다. 모든 강의를 마칠 수 없다면 빈 배열을 반환하세요.'
    en: 'There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [a, b] indicates that you must take course b first if you want to take course a.


      For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.


      Return the ordering of courses you should take to finish all courses. If there are many valid answers, return any of them. If it is impossible to finish all courses, return an empty array.'
  constraints:
  - 1 ≤ numCourses ≤ 2000
  - 0 ≤ prerequisites.length ≤ numCourses × (numCourses - 1)
  - prerequisites[i].length == 2
  - 0 ≤ a_i, b_i < numCourses
  io:
  - input: '2

      [[1,0]]'
    output: '[0,1]'
  - input: '4

      [[1,0],[2,0],[3,1],[3,2]]'
    output: '[0,2,1,3]'
  - input: '1

      []'
    output: '[0]'
clarifying:
  items:
  - q:
      ko: prerequisites[i] = [a, b]에서 어느 강의를 먼저 들어야 하나요?
      en: In prerequisites[i] = [a, b], which course must be taken first?
    type: good
    why:
      ko: 문제 이해의 핵심입니다. b를 먼저 들어야 a를 들 수 있습니다.
      en: Critical for understanding. Course b must be completed before taking course a.
  - q:
      ko: 모든 강의를 들을 수 없는 경우는 언제인가요?
      en: When is it impossible to take all courses?
    type: good
    why:
      ko: '순환 의존성(사이클)이 있을 때입니다. 예: 0→1→0이면 불가능합니다.'
      en: When a cycle exists in dependencies. For example, course 0 requires 1 and 1 requires 0.
  - q:
      ko: 여러 개의 유효한 순서가 있을 때, 어떤 것을 반환해야 하나요?
      en: If multiple valid orderings exist, which should be returned?
    type: good
    why:
      ko: 문제에서 '어느 것이든 반환해도 된다'고 명시합니다.
      en: The problem explicitly states any valid ordering is acceptable.
  - q:
      ko: 선수 과목이 없는 강의는 어디든 배치할 수 있나요?
      en: Can courses with no prerequisites be placed anywhere?
    type: good
    why:
      ko: 네, 제약이 없으므로 어디든 배치 가능합니다.
      en: Yes, such courses have no ordering constraints and can be placed anywhere.
  - q:
      ko: 탐욕 알고리즘으로 먼저 들을 수 있는 강의를 선택하면 항상 해결되나요?
      en: Will selecting available courses greedily always work?
    type: distractor
    why:
      ko: 아니요. 탐욕은 사이클을 감지하지 못합니다.
      en: No, greedy approaches cannot detect cycles and may produce invalid results.
  - q:
      ko: 반환 배열의 강의들이 정렬된 순서여야 하나요?
      en: Must courses be returned in sorted order?
    type: distractor
    why:
      ko: 아니요. 의존성 조건만 만족하면 됩니다.
      en: No, only prerequisite dependencies need to be satisfied.
approach:
  items:
  - name:
      ko: DFS 기반 위상정렬 (사이클 감지 포함)
      en: DFS with Cycle Detection
    complexity: O(V + E) time / O(V + E) space
    type: good
    why:
      ko: 각 노드와 간선을 한 번씩 방문하며, 현재 경로에서 사이클을 감지합니다.
      en: Visits each node and edge once while detecting back edges in the current DFS path.
  - name:
      ko: BFS 위상정렬 (칸의 알고리즘)
      en: BFS Topological Sort (Kahn's Algorithm)
    complexity: O(V + E) time / O(V + E) space
    type: good
    why:
      ko: 진입 차수를 이용하여 레벨별로 처리하면서 사이클을 감지합니다.
      en: Uses in-degree to process nodes level-by-level, naturally detecting cycles.
  - name:
      ko: 모든 순열 확인 (브루트 포스)
      en: Brute Force - Check All Permutations
    complexity: O(n! × n) time / O(n) space
    type: distractor
    why:
      ko: 모든 순열을 생성하고 검증합니다. 매우 비효율적입니다.
      en: Generates all permutations and validates. Extremely inefficient.
  - name:
      ko: 메모이제이션 (사이클 감지 없음)
      en: Memoization Without Cycle Detection
    complexity: O(V + E) time / O(V + E) space
    type: distractor
    why:
      ko: 사이클 입력에서 무한 루프에 빠집니다.
      en: Will hang on cyclic inputs due to lack of cycle detection.
logic:
  format: slot
  slots:
  - label:
      ko: 그래프 구성
      en: Build Adjacency List
    indent: 0
    options:
    - code: 'prereq = {c: [] for c in range(numCourses)}'
      type: good
      why:
        ko: 각 강의의 선수 과목 리스트를 딕셔너리로 저장합니다.
        en: Maps each course to its prerequisite list for efficient lookup.
    - code: adj = [[] for _ in range(numCourses)]
      type: distractor
      why:
        ko: 순방향 간선으로 만들어 역방향 의존성 추적이 어렵습니다.
        en: Creates forward edges instead of reverse dependencies.
    - code: prereq = defaultdict(list)
      type: distractor
      why:
        ko: 모든 강의를 명시적으로 초기화하지 않아 누락될 수 있습니다.
        en: Doesn't explicitly initialize all courses, risking missed nodes.
  - label:
      ko: 상태 추적 초기화
      en: Initialize Tracking Sets
    indent: 0
    options:
    - code: visit, cycle = set(), set()
      type: good
      why:
        ko: 방문(visit)과 현재 경로(cycle)를 구분하여 메모이제이션과 사이클 감지를 동시에 수행합니다.
        en: Separates visited nodes from current DFS path for both memoization and cycle detection.
    - code: visited = set()
      type: distractor
      why:
        ko: 사이클 감지가 불가능합니다.
        en: Cannot detect cycles without tracking the current path.
    - code: visit, cycle = [False]*numCourses, [False]*numCourses
      type: distractor
      why:
        ko: 리스트는 O(n) 조회 시간을 가집니다.
        en: Lists have O(n) lookup time instead of O(1) set operations.
  - label:
      ko: 현재 경로의 사이클 감지
      en: Detect Cycle in Current Path
    indent: 1
    options:
    - code: 'if crs in cycle:'
      type: good
      why:
        ko: 현재 DFS 경로에서 노드를 다시 만나면 뒤로 가는 간선(사이클)입니다.
        en: Finding a node already in the current path indicates a back edge (cycle).
    - code: 'if crs in visit: return False'
      type: distractor
      why:
        ko: 이미 처리된 노드는 사이클이 아니므로 잘못된 판정입니다.
        en: Previously visited nodes don't indicate cycles in the current path.
    - code: 'if not crs in cycle: return False'
      type: distractor
      why:
        ko: 논리가 반전되었습니다.
        en: Inverted logic detects cycles only when absent.
  - label:
      ko: 방문 완료 노드 건너뛰기
      en: Skip Already Processed Nodes
    indent: 1
    options:
    - code: 'if crs in visit:'
      type: good
      why:
        ko: 이미 완료된 노드는 메모이제이션을 통해 바로 참을 반환합니다.
        en: Returns True immediately for already-completed nodes (memoization).
    - code: 'if crs in cycle: return True'
      type: distractor
      why:
        ko: 현재 경로의 노드를 처리하면 사이클 감지가 불가능합니다.
        en: Treating current path nodes as complete prevents cycle detection.
    - code: 'if crs not in visit: return True'
      type: distractor
      why:
        ko: 미방문 노드를 참으로 반환하면 의존성을 탐색하지 않습니다.
        en: Returning True for unvisited nodes skips dependency exploration.
  - label:
      ko: 현재 탐색 경로에 표시
      en: Mark as Being Explored
    indent: 1
    options:
    - code: cycle.add(crs)
      type: good
      why:
        ko: 현재 DFS 경로에 노드를 추가합니다. 나중에 같은 경로에서 다시 만나면 사이클입니다.
        en: Adds node to current path. Meeting it again in the same path indicates a cycle.
    - code: visit.add(crs)
      type: distractor
      why:
        ko: 아직 탐색이 끝나지 않았는데 방문 완료로 표시하면 사이클 감지 실패입니다.
        en: Marking as visited too early prevents cycle detection in the current path.
    - code: cycle.append(crs)
      type: distractor
      why:
        ko: 리스트는 O(n) 조회 시간을 가집니다.
        en: List append/lookup is O(n) instead of O(1).
  - label:
      ko: 선수 과목 재귀 탐색
      en: Recursively Explore Prerequisites
    indent: 1
    options:
    - code: 'for pre in prereq[crs]:'
      type: good
      why:
        ko: 각 선수 과목에 대해 DFS를 수행하여 의존성 체인 전체를 탐색합니다.
        en: Recursively processes each prerequisite to explore the full dependency chain.
    - code: 'for pre in visit: dfs(pre)'
      type: distractor
      why:
        ko: 이미 방문한 노드를 반복하므로 실제 선수 과목을 탐색하지 않습니다.
        en: Iterates over visited nodes instead of actual prerequisites.
    - code: all(dfs(pre) for pre in prereq[crs])
      type: distractor
      why:
        ko: 모든 선수 과목을 탐색한 후 검사하므로 조기 사이클 감지가 불가능합니다.
        en: Checks return values only after exploring all, missing early cycle detection.
  - label:
      ko: 역추적 및 결과 기록
      en: Backtrack and Record
    indent: 1
    options:
    - code: visit.add(crs)
      type: good
      why:
        ko: 현재 경로에서 제거하고, 방문 완료로 표시하고, 결과에 추가합니다(후위 순서).
        en: Removes from current path, marks as visited, and records in post-order (dependencies first).
    - code: output.append(crs); cycle.remove(crs)
      type: distractor
      why:
        ko: visit.add를 빼먹으면 나중에 다시 탐색됩니다.
        en: Without marking visited, nodes may be reprocessed.
    - code: cycle.remove(crs); visit.add(crs)
      type: distractor
      why:
        ko: output.append를 빼먹으면 강의 순서가 기록되지 않습니다.
        en: Without recording to output, the course order is lost.
trace:
  code:
  - 'class Solution:'
  - '    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:'
  - '        prereq = {c: [] for c in range(numCourses)}'
  - '        for crs, pre in prerequisites:'
  - '            prereq[crs].append(pre)'
  - ''
  - '        output = []'
  - '        visit, cycle = set(), set()'
  - ''
  - '        def dfs(crs):'
  - '            if crs in cycle:'
  - '                return False'
  - '            if crs in visit:'
  - '                return True'
  - ''
  - '            cycle.add(crs)'
  - '            for pre in prereq[crs]:'
  - '                if dfs(pre) == False:'
  - '                    return False'
  - '            cycle.remove(crs)'
  - '            visit.add(crs)'
  - '            output.append(crs)'
  - '            return True'
  - ''
  - '        for c in range(numCourses):'
  - '            if dfs(c) == False:'
  - '                return []'
  - '        return output'
  cases:
  - input: '2

      [[1,0]]'
    expected: '[0,1]'
  - input: '4

      [[1,0],[2,0],[3,1],[3,2]]'
    expected: '[0,2,1,3]'
  - input: '1

      []'
    expected: '[0]'
  worked_example:
    input: '2

      [[1,0]]'
    steps:
    - ko: '그래프 생성: prereq = {0: [], 1: [0]}'
      en: 'Build graph: prereq = {0: [], 1: [0]}'
    - ko: 'DFS(0): 선수 과목 없음 → output = [0]'
      en: 'DFS(0): No prerequisites → output = [0]'
    - ko: 'DFS(1): 선수 과목 0 탐색 → DFS(0)은 이미 방문됨 → output = [0, 1]'
      en: 'DFS(1): Explore prerequisite 0 → DFS(0) already visited → output = [0, 1]'
    - ko: 모든 강의 처리 완료, 사이클 없음 → [0, 1] 반환
      en: All courses processed, no cycles → return [0, 1]
    answer: '[0,1]'
solution:
  code: "class Solution:\n    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:\n        prereq = {c: [] for c in range(numCourses)}\n        for crs, pre in prerequisites:\n            prereq[crs].append(pre)\n\n        output = []\n        visit, cycle = set(), set()\n\n        def dfs(crs):\n            if crs in cycle:\n                return False\n            if crs in visit:\n                return True\n\n            cycle.add(crs)\n            for pre in prereq[crs]:\n                if dfs(pre) == False:\n                    return False\n            cycle.remove(crs)\n            visit.add(crs)\n            output.append(crs)\n            return True\n\n        for c in range(numCourses):\n            if dfs(c) == False:\n                return []\n        return output\n"
  complexity:
    time: O(V + E) where V = numCourses, E = prerequisites.length
    space: O(V + E) for graph, visited/cycle sets, and recursion stack
  followup:
  - ko: BFS 기반 칸의 알고리즘으로도 같은 시간 복잡도로 풀 수 있습니다. 어떻게 구현할까요?
    en: Can you implement Kahn's algorithm (BFS) to achieve the same time complexity?
  - ko: 만약 전체 순서가 아니라 사이클 존재 여부만 확인한다면 어떻게 최적화할까요?
    en: If you only need to detect a cycle without building the full order, how would you optimize?
  - ko: 재귀 대신 명시적 스택을 사용한 반복적 DFS로 어떻게 구현할까요?
    en: How would you implement iterative DFS with an explicit stack instead of recursion?
```