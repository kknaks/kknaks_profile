---
created: '2026-08-21'
date: '2026-08-21'
day: Day 93
difficulty: hard
id: A-093
source:
  curated_in:
  - neetcode150
  number: 332
  platform: leetcode
  slug: reconstruct-itinerary
  url: https://leetcode.com/problems/reconstruct-itinerary/
status: draft
tags:
- array
- string
- depth-first-search
- graph
- sorting
- heap-priority-queue
- eulerian-circuit
- eulerian-path
- semi-eulerian-graph
title:
  en: Reconstruct Itinerary
  ko: 여행 경로 재구성
today: true
type: algorithm
updated: '2026-08-21'
visible: true
---

# 여행 경로 재구성

## Data

```yaml
problem:
  title:
    ko: 여행 경로 재구성
    en: Reconstruct Itinerary
  statement:
    ko: '항공사 티켓 목록 tickets이 주어지며, 각 tickets[i] = [from_i, to_i]는 한 항공편의 출발지와 도착지 공항을 나타냅니다. 경로를 순서대로 재구성하여 반환하세요.


      모든 티켓은 "JFK"에서 출발하는 한 사람에게 속하므로, 경로는 "JFK"로 시작해야 합니다. 유효한 경로가 여러 개 있으면, 단일 문자열로 읽을 때 사전식 순서가 가장 작은 경로를 반환해야 합니다.


      예를 들어, 경로 ["JFK", "LGA"]는 ["JFK", "LGB"]보다 사전식 순서가 작습니다.


      모든 티켓이 유효한 경로를 형성한다고 가정할 수 있습니다. 각 티켓을 정확히 한 번만 사용해야 합니다.'
    en: 'You are given a list of airline tickets where tickets[i] = [from_i, to_i] represent the departure and the arrival airports of one flight. Reconstruct the itinerary in order and return it.


      All of the tickets belong to a man who departs from "JFK", thus, the itinerary must begin with "JFK". If there are multiple valid itineraries, you should return the itinerary that has the smallest lexical order when read as a single string.


      For example, the itinerary ["JFK", "LGA"] has a smaller lexical order than ["JFK", "LGB"].


      You may assume all tickets form at least one valid itinerary. You must use all the tickets once and only once.'
  constraints:
  - 1 ≤ tickets.length ≤ 300
  - tickets[i].length == 2
  - from_i and to_i consist of uppercase English letters, each of length 3
  - from_i ≠ to_i
  - All tickets form at least one valid itinerary
  io:
  - input: '[["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]'
    output: '["JFK","MUC","LHR","SFO","SJC"]'
  - input: '[["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"],["ATL","SFO"]]'
    output: '["JFK","ATL","JFK","SFO","ATL","SFO"]'
clarifying:
  items:
  - q:
      ko: 모든 티켓을 정확히 한 번씩 사용해야 하나요?
      en: Must we use all tickets exactly once?
    type: good
    why:
      ko: 네, 문제에서 각 티켓을 정확히 한 번만 사용하도록 명시됩니다. 이는 오일러 경로(Eulerian path) 문제입니다.
      en: Yes, the problem explicitly states each ticket must be used exactly once. This is an Eulerian path problem.
  - q:
      ko: 공항이 경로에서 여러 번 나타날 수 있나요?
      en: Can an airport appear multiple times in the itinerary?
    type: good
    why:
      ko: 네, 같은 공항으로 여러 항공편이 있으면 여러 번 나타납니다. 예제 2를 보면 ATL과 JFK가 각각 여러 번 나타납니다.
      en: Yes, if there are multiple flights from/to an airport, it will appear multiple times. Example 2 shows this.
  - q:
      ko: '"사전식 순서가 가장 작다"는 무엇을 의미하나요?'
      en: What does 'smallest lexical order' mean?
    type: good
    why:
      ko: 경로를 단일 문자열로 연결했을 때의 문자열 비교입니다. "JFKLGA" < "JFKLGB"입니다.
      en: String comparison when the path is concatenated. "JFKLGA" < "JFKLGB" lexicographically.
  - q:
      ko: JFK가 아닌 다른 공항에서 출발할 수 있나요?
      en: Can we start from an airport other than JFK?
    type: distractor
    why:
      ko: 아니요, 문제에서 모든 티켓이 JFK에서 출발한다고 명시합니다.
      en: No, the problem states all tickets belong to a person departing from JFK.
  - q:
      ko: 탐욕 알고리즘으로 각 단계마다 사전식 최소 도착지를 선택하면 되나요?
      en: Can we greedily pick the lexicographically smallest destination at each step?
    type: distractor
    why:
      ko: 아니요, 탐욕 선택이 막다른 길로 이어질 수 있습니다. 모든 티켓을 사용하기 전에 끝날 수 있습니다.
      en: No, greedy choices can lead to dead ends before using all tickets. Example 2 fails with greedy approach.
  - q:
      ko: 노드가 아닌 간선(티켓)을 정확히 한 번 사용해야 합니다. 이게 중요한 이유는?
      en: Why is it important that we use edges (flights), not nodes (airports), exactly once?
    type: good
    why:
      ko: 같은 공항으로 여러 항공편이 있을 수 있으므로, 간선 기반 사용이 필수입니다.
      en: Multiple flights can exist from the same airport, so edge-based tracking is essential.
approach:
  items:
  - name:
      ko: Hierholzer 알고리즘 (DFS 기반, 후위 순회)
      en: Hierholzer's Algorithm (DFS with post-order)
    complexity: O(E log E) time / O(V + E) space
    type: good
    why:
      ko: 오일러 경로를 효율적으로 찾는 표준 알고리즘입니다. 목적지를 정렬하면 사전식 순서를 보장하고, 후위 순회가 올바른 경로 순서를 만듭니다.
      en: Standard algorithm for Eulerian paths. Sorting ensures lexical order; post-order traversal ensures correct path order.
  - name:
      ko: 탐욕 알고리즘 (각 단계에서 최소 도착지 선택)
      en: Greedy (always pick lexicographically smallest next destination)
    complexity: O(E log E) time / O(E) space
    type: distractor
    why:
      ko: 탐욕 선택이 막다른 길로 이어질 수 있습니다. 예제 2에서 JFK→SFO로 시작하면 모든 티켓을 사용하지 못합니다.
      en: Greedy can hit dead ends. In Example 2, starting JFK→SFO prevents using all tickets.
  - name:
      ko: 전수 탐색 (모든 순열 시도)
      en: Brute Force (try all permutations)
    complexity: O(E! × E) time / O(E) space
    type: distractor
    why:
      ko: 300개의 간선으로는 계산 불가능합니다. 시간 제한 초과.
      en: With up to 300 edges, factorial permutations are infeasible. Time limit exceeded.
  - name:
      ko: 위상 정렬 (Topological Sort)
      en: Topological Sort
    complexity: O(V + E) time / O(V + E) space
    type: distractor
    why:
      ko: 위상 정렬은 비순환 그래프(DAG)에만 적용됩니다. 이 문제는 사이클을 포함할 수 있으므로 적용 불가능합니다.
      en: Topological sort only works on DAGs. This graph may have cycles, so it doesn't apply.
logic:
  format: slot
  slots:
  - label:
      ko: 인접 리스트 초기화 - 모든 출발지 사전 등록
      en: Initialize adjacency list with all sources
    indent: 0
    options:
    - code: 'adj = {src: [] for src, dst in tickets}'
      type: good
      why:
        ko: 모든 출발지 공항을 미리 등록하면, 나중에 존재하지 않는 키에 접근할 때 KeyError를 방지합니다.
        en: Pre-registering all sources prevents KeyError when accessing later. Ensures clean graph structure.
    - code: adj = {}
      type: distractor
      why:
        ko: 빈 딕셔너리에서 adj[src]에 직접 접근하면 KeyError 발생
        en: Accessing non-existent keys causes KeyError
    - code: adj = defaultdict(list)
      type: distractor
      why:
        ko: 작동하지만 명시적으로 모든 키를 초기화하는 것이 더 명확합니다
        en: Works but less explicit than pre-initialization
  - label:
      ko: 그래프 구축 - 각 티켓을 간선으로 추가
      en: Build graph - add each ticket as an edge
    indent: 1
    options:
    - code: adj[src].append(dst)
      type: good
      why:
        ko: 각 티켓을 출발지→도착지 방향 간선으로 추가합니다. 같은 경로에 여러 항공편이 있을 수 있으므로 다중 간선을 허용해야 합니다.
        en: Adds directed edge for each flight. Multiple edges allowed between same airports.
    - code: adj[dst].append(src)
      type: distractor
      why:
        ko: 역방향 간선을 만들어 완전히 잘못된 경로를 생성합니다
        en: Creates reverse edges, generates wrong path
    - code: adj[src] = [dst]
      type: distractor
      why:
        ko: 기존 도착지를 덮어써서 일부 티켓을 잃어버립니다
        en: Overwrites previous destinations, loses tickets
  - label:
      ko: 사전식 순서를 위해 도착지 정렬
      en: Sort destinations lexicographically
    indent: 1
    options:
    - code: adj[key].sort()
      type: good
      why:
        ko: 각 출발지의 도착지 리스트를 정렬하면, DFS가 사전식으로 가장 작은 경로를 자동으로 찾습니다.
        en: Sorting ensures DFS explores smallest destinations first, guaranteeing lexicographically smallest itinerary.
    - code: adj[key].reverse()
      type: distractor
      why:
        ko: 역순이 되어 사전식 최대 경로를 찾게 됩니다
        en: Results in largest lexical order
    - code: '# sorted는 인플레이스 작동하지 않으므로 정렬 생략'
      type: distractor
      why:
        ko: 정렬하지 않으면 임의의 도착지 순서로 탐색하여 조건을 만족하지 못합니다
        en: Without sorting, arbitrary order doesn't guarantee lexical minimum
  - label:
      ko: DFS 안전성 검사 - 출발지가 그래프에 있는지 확인
      en: DFS safety check - verify source exists in graph
    indent: 1
    options:
    - code: 'if src in adj:'
      type: good
      why:
        ko: 출발지가 그래프에 없으면(나가는 간선이 없으면) 바로 결과에 추가합니다. 이 검사가 없으면 잘못된 동작이 발생할 수 있습니다.
        en: Nodes with no outgoing flights are immediately added. Prevents errors from accessing missing keys.
    - code: 'if True:'
      type: distractor
      why:
        ko: 조건 없이 진행하면 존재하지 않는 키 접근 시 에러 발생
        en: Accessing non-existent key causes error
    - code: 'while len(adj.get(src, [])) > 0:'
      type: distractor
      why:
        ko: 간선이 남아있으면 자동으로 처리되지만, 선택적 조건 검사가 더 명확합니다
        en: Works but less explicit than direct condition
  - label:
      ko: 간선 제거 및 재귀 - 사용한 항공편 추적
      en: Remove edge and recurse - mark flight as used
    indent: 3
    options:
    - code: adj[src].pop(0)
      type: good
      why:
        ko: 도착지를 탐색하기 전에 간선을 제거합니다. 이것이 각 티켓을 정확히 한 번만 사용하는 핵심입니다. 다중 간선이 있어도 모두 사용됩니다.
        en: Removes edge before visiting. This ensures each flight is used exactly once. Multiple flights to same destination all get used.
    - code: dfs(adj, dest)
      type: distractor
      why:
        ko: 간선을 제거하지 않으면 무한 루프에 빠집니다
        en: Without removing, infinite loop on multiple edges
    - code: adj[src].remove(dest); dfs(adj, dest)
      type: distractor
      why:
        ko: remove()는 O(n) 비용이 들고, 다중 간선 중 하나만 제거합니다
        en: remove() is O(n) and only removes first occurrence
  - label:
      ko: 후위 순회 - 자식 방문 후 노드 추가
      en: Post-order processing - append after visiting children
    indent: 1
    options:
    - code: res.append(src)
      type: good
      why:
        ko: 모든 나가는 간선을 탐색한 후에 노드를 결과에 추가합니다. 이 역순 처리가 오일러 경로 알고리즘의 핵심이며, 나중에 역순으로 뒤집습니다.
        en: Appends after visiting all outgoing edges. Post-order produces path in reverse—we reverse it later. This is the core of Hierholzer's algorithm.
    - code: res.insert(0, src)
      type: distractor
      why:
        ko: 앞에 삽입하면 매번 O(n) 비용이 들어 비효율적입니다
        en: Inserting at front is O(n), very inefficient
    - code: 'res.append(src) # DFS 시작 시'
      type: distractor
      why:
        ko: 전위 순회는 다른 순서의 경로를 만들어 역순이 되지 않습니다
        en: Pre-order doesn't produce reverse path
  - label:
      ko: 결과 역순 처리 - 후위 순회의 역순 보정
      en: Reverse result - correct post-order reversal
    indent: 0
    options:
    - code: res.reverse()
      type: good
      why:
        ko: 후위 순회로 역순으로 구성된 경로를 올바른 순서로 뒤집습니다. 이 한 줄이 경로를 올바른 순서로 변환합니다.
        en: Post-order builds path in reverse. One reverse() call corrects it to proper order.
    - code: res.sort()
      type: distractor
      why:
        ko: 정렬하면 사전식 순서는 맞지만 경로 순서가 완전히 달라집니다
        en: Sorting changes path sequence entirely
    - code: 'pass # 역순이 맞는 답이라고 가정'
      type: distractor
      why:
        ko: 역순이 그대로 반환되므로 검증 실패
        en: Validation fails; path length will be wrong
trace:
  code:
  - 'class Solution:'
  - '    def findItinerary(self, tickets: List[List[str]]) -> List[str]:'
  - '        adj = {src: [] for src, dst in tickets}'
  - '        res = []'
  - ''
  - '        for src, dst in tickets:'
  - '            adj[src].append(dst)'
  - ''
  - '        for key in adj:'
  - '            adj[key].sort()'
  - ''
  - '        def dfs(adj, src):'
  - '            if src in adj:'
  - '                destinations = adj[src][:]'
  - '                while destinations:'
  - '                    dest = destinations[0]'
  - '                    adj[src].pop(0)'
  - '                    dfs(adj, dest)'
  - '                    destinations = adj[src][:]'
  - '            res.append(src)'
  - ''
  - '        dfs(adj, "JFK")'
  - '        res.reverse()'
  - ''
  - '        if len(res) != len(tickets) + 1:'
  - '            return []'
  - ''
  - '        return res'
  cases:
  - input: '[["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]'
    expected: '["JFK","MUC","LHR","SFO","SJC"]'
  - input: '[["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"],["ATL","SFO"]]'
    expected: '["JFK","ATL","JFK","SFO","ATL","SFO"]'
  worked_example:
    input: '[["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]'
    steps:
    - ko: '티켓 정렬 후 인접 리스트: JFK→[MUC], MUC→[LHR], LHR→[SFO], SFO→[SJC]'
      en: 'After building and sorting: JFK→[MUC], MUC→[LHR], LHR→[SFO], SFO→[SJC]'
    - ko: 'JFK에서 DFS 시작. 경로 따라가며 간선 제거: JFK 제거 후 MUC로, MUC 제거 후 LHR로, ... SJC 도착(막다른 곳)'
      en: 'Start DFS from JFK, removing edges: JFK→MUC→LHR→SFO→SJC (dead end, no outgoing flights)'
    - ko: '후위로 역순 추가: res = [SJC, SFO, LHR, MUC, JFK]'
      en: 'Post-order adds in reverse: res = [SJC, SFO, LHR, MUC, JFK]'
    - ko: '역순 처리: res.reverse() → [JFK, MUC, LHR, SFO, SJC] ✓'
      en: 'Reverse to correct order: [JFK, MUC, LHR, SFO, SJC] ✓'
    answer: '["JFK","MUC","LHR","SFO","SJC"]'
solution:
  code: "class Solution:\n    def findItinerary(self, tickets: List[List[str]]) -> List[str]:\n        adj = {src: [] for src, dst in tickets}\n        res = []\n\n        for src, dst in tickets:\n            adj[src].append(dst)\n\n        for key in adj:\n            adj[key].sort()\n\n        def dfs(adj, src):\n            if src in adj:\n                destinations = adj[src][:]\n                while destinations:\n                    dest = destinations[0]\n                    adj[src].pop(0)\n                    dfs(adj, dest)\n                    destinations = adj[src][:]\n            res.append(src)\n\n        dfs(adj, \"JFK\")\n        res.reverse()\n\n        if len(res) != len(tickets) + 1:\n            return []\n\n        return res\n"
  complexity:
    time: O(E log E)
    space: O(V + E)
  followup:
  - ko: 목적지를 정렬하지 않으면 어떤 경로를 얻나요? 추가 정렬 단계 없이 사전식 최소를 보장할 수 있나요?
    en: What itinerary do we get without sorting? Can we guarantee lexicographic minimum without sorting?
  - ko: 유효한 경로가 없는 경우를 감지하려면? (검증 조건 len(res) == len(tickets) + 1의 의미는?)
    en: How do we detect if no valid itinerary exists? Why check len(res) == len(tickets) + 1?
  - ko: 재귀 대신 명시적 스택을 사용해 반복적으로 구현할 수 있나요? 재귀 깊이 제한을 피하려면?
    en: Can we implement iteratively with an explicit stack instead of recursion? How to handle recursion depth limits?
```