---
created: '2026-08-14'
date: '2026-08-14'
day: Day 87
difficulty: medium
id: A-087
source:
  curated_in:
  - neetcode150
  number: 207
  platform: leetcode
  slug: course-schedule
  url: https://leetcode.com/problems/course-schedule/
status: draft
tags:
- depth-first-search
- breadth-first-search
- graph
- topological-sort
- directed-acyclic-graph
title:
  en: Course Schedule
  ko: 코스 스케줄
today: false
type: algorithm
updated: '2026-08-14'
visible: true
---

# 코스 스케줄

## Data

```yaml
problem:
  title:
    ko: 코스 스케줄
    en: Course Schedule
  statement:
    ko: '총 numCourses개의 강좌를 수강해야 하며, 강좌는 0부터 numCourses - 1까지 표시됩니다. prerequisites 배열이 주어지는데, prerequisites[i] = [ai, bi]는 ai 강좌를 수강하려면 먼저 bi 강좌를 완료해야 한다는 의미입니다.


      예를 들어, [0, 1] 쌍은 강좌 0을 수강하려면 먼저 강좌 1을 완료해야 한다는 뜻입니다.


      모든 강좌를 완료할 수 있으면 true를 반환하고, 그렇지 않으면 false를 반환합니다.'
    en: 'There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai.


      For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.


      Return true if you can finish all courses. Otherwise, return false.'
  constraints:
  - 1 ≤ numCourses ≤ 2000
  - 0 ≤ prerequisites.length ≤ 5000
  - prerequisites[i].length = 2
  - All prerequisite pairs are unique
  io:
  - input: '2

      [[1,0]]'
    output: 'true'
  - input: '2

      [[1,0],[0,1]]'
    output: 'false'
clarifying:
  items:
  - q:
      ko: 선행과목 쌍 [a, b]의 의미를 정확히 이해했나요?
      en: Do you understand that [a, b] means 'take b before a', not the other way around?
    type: good
    why:
      ko: 이 방향성을 혼동하면 그래프를 잘못 구성하게 됩니다. 선행과목 관계를 올바르게 해석하는 것이 핵심입니다.
      en: Confusing the direction leads to an incorrectly constructed graph. Correctly interpreting prerequisites is essential.
  - q:
      ko: 순환이 있으면 왜 모든 강좌를 완료할 수 없나요?
      en: Why does a cycle in prerequisites make it impossible to finish all courses?
    type: good
    why:
      ko: 순환은 A → B → A 같은 상황을 의미하며, A를 시작하려면 B를 먼저 해야 하고 B를 하려면 A를 먼저 해야 하므로 불가능합니다.
      en: 'A cycle creates a deadlock: A requires B, and B requires A. Neither can be taken without the other.'
  - q:
      ko: 강좌는 여러 개의 선행과목을 가질 수 있나요?
      en: Can a course have multiple prerequisites?
    type: good
    why:
      ko: 네, 문제에서 여러 쌍이 같은 강좌를 대상으로 할 수 있으므로 여러 선행과목이 가능합니다.
      en: Yes, multiple prerequisites[i] pairs can have the same ai value, giving one course multiple prerequisites.
  - q:
      ko: DFS 방식과 BFS(위상정렬) 방식 중 어느 것이 더 효율적인가요?
      en: Is DFS or BFS (topological sort via Kahn's algorithm) more efficient for this problem?
    type: distractor
    why:
      ko: 둘 다 O(V+E) 시간에 작동하므로 효율성은 동일하며, 구현의 복잡도나 직관성이 더 중요한 차이입니다.
      en: Both have the same O(V+E) time complexity. The difference is in implementation simplicity, not efficiency.
  - q:
      ko: 모든 강좌를 한 번 이상 DFS로 시작해야 하나요?
      en: Must we call DFS from every course in the main loop?
    type: good
    why:
      ko: 그래프가 연결되어 있지 않을 수 있으므로 모든 강좌에서 시작해야 모든 순환을 감지할 수 있습니다.
      en: The prerequisite graph may have disconnected components, so we must start DFS from every course to detect all cycles.
  - q:
      ko: visited와 visiting 두 개의 상태를 모두 추적해야 하나요?
      en: Do we need to track both 'visited' and 'visiting' states separately?
    type: distractor
    why:
      ko: 이 해답에서는 visiting만 사용하고, 선행과목 목록을 비워서 완료한 강좌를 표시합니다. 따라서 별도의 visited는 필요하지 않습니다.
      en: This solution uses only visiting and clears the prerequisite list to mark completion. A separate visited set is unnecessary.
approach:
  items:
  - name:
      ko: DFS를 이용한 순환 감지
      en: DFS with Cycle Detection
    complexity: O(numCourses + prerequisites.length) time / O(numCourses) space
    type: good
    why:
      ko: 각 노드와 간선을 한 번씩 방문하며, visiting 집합으로 현재 경로의 순환을 감지합니다. 직관적이고 효율적입니다.
      en: Visits each course and edge once. Uses a visiting set to detect back edges (cycles) in the current DFS path. Intuitive and efficient.
  - name:
      ko: BFS/위상정렬(Kahn 알고리즘)
      en: BFS/Topological Sort (Kahn's Algorithm)
    complexity: O(numCourses + prerequisites.length) time / O(numCourses) space
    type: good
    why:
      ko: 진입차수(in-degree) 기반으로 순환이 없는 노드부터 제거합니다. 위상정렬의 표준 알고리즘이며 실제 순서도 얻을 수 있습니다.
      en: Removes courses with zero in-degree iteratively. Standard topological sort; also produces the actual valid course order if one exists.
  - name:
      ko: 모든 순열 시도 (브루트포스)
      en: 'Brute Force: Try All Permutations'
    complexity: O(n! × n) time / O(n) space
    type: distractor
    why:
      ko: 모든 가능한 순서를 확인하는 것은 factorial 시간이 소요되므로 매우 비효율적입니다.
      en: Checking all possible orderings takes factorial time, making it impractical for numCourses up to 2000.
  - name:
      ko: '탐욕(Greedy): 선행과목이 적은 강좌부터 수강'
      en: 'Greedy: Take Courses with Fewest Prerequisites First'
    complexity: O(numCourses²) time / O(numCourses) space
    type: distractor
    why:
      ko: 이 방식은 선행과목의 간접적 의존성을 고려하지 않으며, 순환을 감지하지 못할 수 있습니다.
      en: This approach ignores transitive dependencies and fails to detect cycles hidden in prerequisite chains.
logic:
  format: slot
  slots:
  - label:
      ko: '그래프 초기화: 각 강좌별 선행과목 목록'
      en: 'Build Graph: Initialize course-to-prerequisites mapping'
    indent: 0
    options:
    - code: 'preMap = {i: [] for i in range(numCourses)}'
      type: good
      why:
        ko: 각 강좌의 선행과목들을 빠르게 조회할 수 있도록 딕셔너리로 초기화합니다.
        en: Initialize a dictionary so we can quickly look up prerequisites for any course.
    - code: preMap = {}
      type: distractor
      why:
        ko: 빈 딕셔너리로 초기화하면 선행과목이 없는 강좌가 누락됩니다.
        en: An empty dict won't account for courses with no prerequisites.
    - code: preMap = [[] for _ in range(numCourses)]
      type: distractor
      why:
        ko: 리스트로도 작동하지만 딕셔너리가 의도를 더 명확하게 전달합니다.
        en: A list works but a dict better clarifies the course-to-prerequisites mapping.
  - label:
      ko: '그래프 구성: 선행과목 관계 추가'
      en: 'Populate Graph: Add prerequisite edges'
    indent: 1
    options:
    - code: 'for crs, pre in prerequisites:'
      type: good
      why:
        ko: 각 prerequisites[i] = [crs, pre]를 읽어 crs가 pre를 선행과목으로 하도록 저장합니다.
        en: For each [crs, pre] pair, add pre to course crs's prerequisites.
    - code: preMap[pre].append(crs)
      type: distractor
      why:
        ko: 이렇게 하면 관계 방향이 뒤바뀌어 선행과목을 잘못 저장합니다.
        en: This reverses the direction; it marks crs as a prerequisite for pre.
    - code: preMap[crs] = pre
      type: distractor
      why:
        ko: 여러 선행과목을 저장할 수 없습니다. append를 사용해야 합니다.
        en: This overwrites previous prerequisites. We must append to support multiple prerequisites.
  - label:
      ko: '순환 감지 준비: 현재 경로 추적'
      en: 'Initialize Cycle Detection: Track current DFS path'
    indent: 0
    options:
    - code: visiting = set()
      type: good
      why:
        ko: visiting 집합으로 현재 DFS 경로에 있는 노드들을 추적하여 역간선(순환)을 감지합니다.
        en: The visiting set tracks nodes in the current DFS path. If we revisit a node, a cycle exists.
    - code: visited = set()
      type: distractor
      why:
        ko: 완료한 노드만 추적하는 visited로는 순환 감지가 불충분합니다.
        en: Tracking only fully-visited nodes doesn't detect cycles in the current path.
    - code: 'visiting = {i: 0 for i in range(numCourses)}'
      type: distractor
      why:
        ko: 상태를 저장할 필요가 없습니다. 집합으로 충분합니다.
        en: Storing states in a dict is overkill; a simple set suffices.
  - label:
      ko: '순환 확인: 현재 경로에서 강좌를 만났는가?'
      en: 'Check: Has this course already been visited in the current path?'
    indent: 1
    options:
    - code: 'if crs in visiting:'
      type: good
      why:
        ko: 현재 경로(visiting)에서 강좌를 다시 만나면 순환이 있다는 뜻입니다.
        en: If a course is in visiting, we've found a back edge—a cycle in the current path.
    - code: 'if crs in visited:'
      type: distractor
      why:
        ko: 완료한 노드는 순환을 의미하지 않습니다. visiting을 확인해야 합니다.
        en: Encountering a fully-processed node doesn't indicate a cycle.
    - code: 'if preMap[crs] == []: return True'
      type: distractor
      why:
        ko: 이것은 다른 기저 사례입니다. 순환 체크와는 다릅니다.
        en: This checks for the base case; it's not a cycle detection check.
  - label:
      ko: '기저 사례: 선행과목이 없으면 강좌 완료 가능'
      en: 'Base Case: No prerequisites means course can be taken'
    indent: 1
    options:
    - code: 'if preMap[crs] == []:'
      type: good
      why:
        ko: 선행과목이 없으면 이 강좌를 즉시 완료할 수 있으므로 true를 반환합니다.
        en: A course with no prerequisites can be taken immediately, so return true.
    - code: 'if len(preMap[crs]) == 0:'
      type: distractor
      why:
        ko: len() 비교도 작동하지만 직접 비교가 더 간단합니다.
        en: Checking length works but direct comparison is simpler.
    - code: 'if not preMap[crs]:'
      type: distractor
      why:
        ko: 이것도 작동하지만 빈 리스트와의 명시적 비교가 가독성이 좋습니다.
        en: Truthy check works but explicit comparison is clearer.
  - label:
      ko: '경로 기록: 현재 강좌를 방문 중으로 표시'
      en: 'Mark: Add course to visiting set before recursing'
    indent: 1
    options:
    - code: visiting.add(crs)
      type: good
      why:
        ko: 선행과목들을 확인하기 전에 현재 강좌를 visiting에 추가하여 순환을 감지할 수 있게 합니다.
        en: Add the course to visiting before checking prerequisites. This allows us to detect if we loop back to it.
    - code: visiting.add(crs) after recursion
      type: distractor
      why:
        ko: 재귀 호출 후 추가하면 순환 감지 시점이 늦습니다.
        en: Adding after recursive calls misses the opportunity to detect back edges.
    - code: visited.add(crs)
      type: distractor
      why:
        ko: 완료 표시는 역추적 후에 해야 합니다. 재귀 전이 아닙니다.
        en: Mark as fully visited only after recursion, not before.
  - label:
      ko: '역추적: 강좌를 경로에서 제거하고 완료 표시'
      en: 'Backtrack: Remove from visiting and clear prerequisites'
    indent: 1
    options:
    - code: visiting.remove(crs)
      type: good
      why:
        ko: 재귀에서 돌아오면 visiting에서 제거(역추적)하고, 최적화를 위해 선행과목 목록을 비워서 이후 조회를 O(1)로 만듭니다.
        en: After recursion returns, remove from visiting (backtrack) and clear the prerequisite list. This marks the course as processed and optimizes future checks.
    - code: '# visiting.remove(crs)'
      type: distractor
      why:
        ko: 역추적하지 않으면 다른 분기의 강좌들이 순환으로 잘못 감지될 수 있습니다.
        en: Skipping removal leads to false cycle detection in other branches.
    - code: preMap[crs] = -1
      type: distractor
      why:
        ko: 특정 값을 저장할 수 있지만, 빈 리스트로 초기화하는 것이 조건문과 일치합니다.
        en: A sentinel value works but clearing (making it empty) aligns with the base case check.
trace:
  code:
  - 'class Solution:'
  - '    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:'
  - '        # dfs'
  - '        preMap = {i: [] for i in range(numCourses)}'
  - ''
  - '        # map each course to : prereq list'
  - '        for crs, pre in prerequisites:'
  - '            preMap[crs].append(pre)'
  - ''
  - '        visiting = set()'
  - ''
  - '        def dfs(crs):'
  - '            if crs in visiting:'
  - '                return False'
  - '            if preMap[crs] == []:'
  - '                return True'
  - ''
  - '            visiting.add(crs)'
  - '            for pre in preMap[crs]:'
  - '                if not dfs(pre):'
  - '                    return False'
  - '            visiting.remove(crs)'
  - '            preMap[crs] = []'
  - '            return True'
  - ''
  - '        for c in range(numCourses):'
  - '            if not dfs(c):'
  - '                return False'
  - '        return True'
  cases:
  - input: '2

      [[1,0]]'
    expected: 'true'
  - input: '2

      [[1,0],[0,1]]'
    expected: 'false'
  worked_example:
    input: '2

      [[1,0]]'
    steps:
    - ko: '입력: numCourses=2, prerequisites=[[1,0]]'
      en: 'Input: numCourses=2, prerequisites=[[1,0]]'
    - ko: 'preMap 구성: {0: [], 1: [0]} (강좌 0은 선행과목 없음, 강좌 1은 강좌 0을 선행과목으로 함)'
      en: 'After building graph: preMap = {0: [], 1: [0]}'
    - ko: 'dfs(0): preMap[0]은 빈 리스트 → true 반환'
      en: 'dfs(0): preMap[0] is empty → return true immediately'
    - ko: 'dfs(1): preMap[1] = [0], visiting에 1 추가 → dfs(0) 호출 → true 반환, visiting에서 1 제거 → true 반환'
      en: 'dfs(1): preMap[1] has [0], add 1 to visiting → call dfs(0) → returns true → remove 1 from visiting → return true'
    - ko: 모든 강좌 순회 완료, 순환 감지되지 않음 → true 반환
      en: All courses processed without cycles → return true
    answer: 'true'
solution:
  code: "class Solution:\n    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:\n        # dfs\n        preMap = {i: [] for i in range(numCourses)}\n\n        # map each course to : prereq list\n        for crs, pre in prerequisites:\n            preMap[crs].append(pre)\n\n        visiting = set()\n\n        def dfs(crs):\n            if crs in visiting:\n                return False\n            if preMap[crs] == []:\n                return True\n\n            visiting.add(crs)\n            for pre in preMap[crs]:\n                if not dfs(pre):\n                    return False\n            visiting.remove(crs)\n            preMap[crs] = []\n            return True\n\n        for c in range(numCourses):\n            if not dfs(c):\n                return False\n        return True\n"
  complexity:
    time: O(numCourses + prerequisites.length)
    space: O(numCourses)
  followup:
  - ko: 모든 강좌를 완료할 수 있다면, 실제 수강 순서(위상정렬)는 어떻게 구하나요?
    en: If courses can all be completed, how would you find an actual valid course order (topological sort)?
  - ko: Kahn 알고리즘(진입차수 기반 BFS)으로 이 문제를 풀면 어떤 장단점이 있나요?
    en: What are the pros and cons of using Kahn's algorithm (in-degree based BFS) instead of DFS for this problem?
  - ko: 매우 큰 그래프(numCourses=10⁶)에서 메모리 효율을 어떻게 개선할 수 있나요?
    en: How would you optimize memory usage if numCourses were very large (e.g., 10⁶)?
```