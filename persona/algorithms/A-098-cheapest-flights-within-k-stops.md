---
created: '2026-08-26'
date: '2026-08-26'
day: Day 98
difficulty: medium
id: A-098
source:
  curated_in:
  - neetcode150
  number: 787
  platform: leetcode
  slug: cheapest-flights-within-k-stops
  url: https://leetcode.com/problems/cheapest-flights-within-k-stops/
status: draft
tags:
- dynamic-programming
- depth-first-search
- breadth-first-search
- graph
- heap-priority-queue
- shortest-path
title:
  en: Cheapest Flights Within K Stops
  ko: K 정거소 이내의 최저 운임
today: true
type: algorithm
updated: '2026-08-26'
visible: true
---

# K 정거소 이내의 최저 운임

## Data

```yaml
problem:
  title:
    ko: K 정거소 이내의 최저 운임
    en: Cheapest Flights Within K Stops
  statement:
    ko: 'n개의 도시가 항공편으로 연결되어 있습니다. 배열 flights가 주어지는데, flights[i] = [from_i, to_i, price_i]는 도시 from_i에서 to_i로 가는 price_i의 비용이 드는 항공편이 있다는 뜻입니다.


      또한 세 정수 src, dst, k가 주어집니다. src에서 dst로 가는 최대 k정거소 이내의 최저 운임을 반환하세요. 그러한 경로가 없으면 -1을 반환하세요.


      참고: "정거소"는 경로에서 거쳐가는 중간 도시의 개수입니다. 예를 들어 직항편은 0정거소, 1개의 중간 도시를 거치면 1정거소입니다.'
    en: 'There are n cities connected by some number of flights. You are given an array flights where flights[i] = [from_i, to_i, price_i] indicates that there is a flight from city from_i to city to_i with cost price_i.


      You are also given three integers src, dst, and k, return the cheapest price from src to dst with at most k stops. If there is no such route, return -1.'
  constraints:
  - 2 ≤ n ≤ 100
  - 0 ≤ flights.length ≤ n(n-1)/2
  - 1 ≤ price_i ≤ 10⁴
  - 0 ≤ src, dst, k < n; src ≠ dst
  io:
  - input: '4

      [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]]

      0

      3

      1'
    output: '700'
  - input: '3

      [[0,1,100],[1,2,100],[0,2,500]]

      0

      2

      1'
    output: '200'
  - input: '3

      [[0,1,100],[1,2,100],[0,2,500]]

      0

      2

      0'
    output: '500'
clarifying:
  items:
  - q:
      ko: 정거소(stop)가 정확히 무엇을 의미하나요?
      en: What exactly does a 'stop' mean in this problem?
    type: good
    why:
      ko: 정거소는 경로에서 거쳐가는 중간 도시의 개수입니다. 직항편은 0정거소, 1개 중간도시는 1정거소입니다.
      en: A stop represents the number of intermediate cities visited. A direct flight = 0 stops; visiting 1 intermediate city = 1 stop.
  - q:
      ko: 반복을 k번이 아닌 k+1번 해야 하는 이유는?
      en: Why do we iterate k+1 times instead of k times?
    type: good
    why:
      ko: i번째 반복 후에는 최대 i정거소의 경로를 찾습니다. 0정거소부터 k정거소까지 처리하려면 k+1번이 필요합니다.
      en: After iteration i, we have the minimum cost with at most i stops. To cover 0 to k stops requires k+1 iterations.
  - q:
      ko: prices를 업데이트하기 전에 복사하는 이유는?
      en: Why do we copy prices before updating in each iteration?
    type: good
    why:
      ko: 같은 반복에서 이미 업데이트된 값을 사용하지 않기 위함입니다. 복사본으로 스냅샷을 만들어 일관성을 유지합니다.
      en: It prevents using already-updated values within the same iteration, ensuring all flights use the same 'generation' of costs.
  - q:
      ko: 경로가 없으면 어떻게 알 수 있나요?
      en: How do we detect if there's no valid path within k stops?
    type: good
    why:
      ko: 목적지의 최종 가격이 무한대이면 도달 불가능합니다. 그러면 -1을 반환합니다.
      en: If the destination's final price remains infinity after all iterations, no path exists, so we return -1.
  - q:
      ko: 같은 도시를 여러 번 방문할 수 있나요?
      en: Can we visit the same city multiple times in a single path?
    type: good
    why:
      ko: 알고리즘이 명시적으로 금지하지 않으므로 가능하지만, 최적 경로에서는 일반적으로 일어나지 않습니다.
      en: The algorithm doesn't explicitly prevent cycles, but revisiting cities is unlikely to yield an optimal solution.
  - q:
      ko: Dijkstra의 알고리즘을 바로 적용할 수 있나요?
      en: Can we use Dijkstra's algorithm directly without modification?
    type: distractor
    why:
      ko: Dijkstra를 사용할 수도 있지만, 정거소 제약을 추적하려면 상태를 (비용, 정거소, 도시)로 확장해야 하므로 더 복잡합니다.
      en: While possible, tracking the k-stops constraint requires modifying the state to (cost, stops, city), making it more complex than this approach.
  - q:
      ko: 음수 운임이 문제를 야기할까요?
      en: Could negative flight prices break this algorithm?
    type: distractor
    why:
      ko: 제약조건에서 1 ≤ price ≤ 10⁴로 모든 가격이 양수이므로 걱정할 필요가 없습니다.
      en: No; constraints guarantee all prices are positive (1 to 10⁴), so this isn't a concern.
  - q:
      ko: 그래프가 항상 연결되어 있나요?
      en: Is the graph always connected?
    type: distractor
    why:
      ko: 아니요. 일부 도시는 도달 불가능할 수 있으며, 이 경우 -1을 반환합니다.
      en: No. Some destinations may be unreachable, in which case we return -1.
approach:
  items:
  - name:
      ko: 동적 프로그래밍 (Bellman-Ford 변형)
      en: Dynamic Programming (Bellman-Ford Variant)
    complexity: O(k × m) time / O(n) space
    type: good
    why:
      ko: Bellman-Ford를 k+1번 반복하여 각 반복마다 최대 i정거소의 최저 가격을 계산합니다. 직관적이고 구현이 간단합니다.
      en: Extends Bellman-Ford by iterating k+1 times. Each iteration progressively builds paths with 0, 1, ..., k stops.
  - name:
      ko: Dijkstra (수정된 상태 추적)
      en: Dijkstra with (cost, stops, city) State
    complexity: O(kn log(kn)) time / O(kn) space
    type: good
    why:
      ko: 우선순위 큐에서 (비용, 정거소, 도시)를 상태로 사용합니다. 더 효율적일 수 있지만 구현이 더 복잡합니다.
      en: Uses priority queue with extended state. More sophisticated but requires careful state management and heap operations.
  - name:
      ko: 깊이 우선 탐색 (DFS 백트래킹)
      en: Depth-First Search (DFS Backtracking)
    complexity: O(n^k) time / O(k) space
    type: distractor
    why:
      ko: 모든 경로를 탐색하므로 k가 크면 지수 시간이 걸립니다. 매우 비효율적입니다.
      en: Explores all possible paths exhaustively, leading to exponential time. Inefficient for larger k values.
  - name:
      ko: Floyd-Warshall 알고리즘
      en: Floyd-Warshall Algorithm
    complexity: O(n³) time / O(n²) space
    type: distractor
    why:
      ko: 모든 쌍 최단 경로를 구하지만, k 제약을 자연스럽게 처리하지 못하고 시간 복잡도가 높습니다.
      en: Computes all-pairs shortest paths but doesn't naturally handle the k constraint and has excessive time complexity.
  - name:
      ko: BFS (가중치 무시)
      en: BFS Ignoring Edge Weights
    complexity: O(n + m) time / O(n) space
    type: distractor
    why:
      ko: BFS는 가중치가 없는 그래프용입니다. 가중치를 무시하면 최저 운임을 찾지 못합니다.
      en: BFS is for unweighted graphs. Ignoring weights won't find the minimum cost path.
logic:
  format: slot
  slots:
  - label:
      ko: 가격 배열 초기화
      en: Initialize price array
    indent: 0
    options:
    - code: prices = [float("inf")] * n
      type: good
      why:
        ko: 모든 도시를 무한 비용으로 설정하여 도달 불가능 상태를 표현합니다.
        en: Set all cities to infinite cost, representing they are initially unreachable.
    - code: prices = [0] * n
      type: distractor
      why:
        ko: 모든 도시의 비용을 0으로 설정하면 잘못된 초기 상태입니다.
        en: Setting all cities to 0 incorrectly suggests they're all reachable at zero cost.
    - code: prices = [float('inf')] * (n + 1)
      type: distractor
      why:
        ko: 배열 크기가 n+1이면 인덱싱이 맞지 않습니다.
        en: Size n+1 doesn't match n cities and causes index errors.
  - label:
      ko: 출발지 비용 설정
      en: Set source cost to zero
    indent: 0
    options:
    - code: prices[src] = 0
      type: good
      why:
        ko: 출발지에서 출발지로의 비용은 0입니다.
        en: The cost to reach the source from itself is zero.
    - code: prices[src] = 1
      type: distractor
      why:
        ko: 출발지의 비용을 1로 설정하면 모든 경로 비용이 틀립니다.
        en: Starting cost of 1 shifts all path costs incorrectly.
    - code: prices[0] = 0
      type: distractor
      why:
        ko: 항상 첫 번째 도시를 출발지로 가정하는데, src가 0이 아닐 수 있습니다.
        en: Assumes source is always city 0, but src can be any city.
  - label:
      ko: k+1번 반복 (0정거소부터 k정거소)
      en: Iterate k+1 times
    indent: 0
    options:
    - code: 'for i in range(k + 1):'
      type: good
      why:
        ko: 각 반복에서 최대 i정거소의 경로를 계산합니다. 0정거소부터 k정거소까지 모두 처리합니다.
        en: Each iteration computes paths with at most i stops. We need k+1 iterations to cover 0 through k.
    - code: 'for i in range(k):'
      type: distractor
      why:
        ko: k번만 반복하면 k정거소까지만 커버되므로 0정거소 경우를 빠뜨립니다.
        en: Only k iterations misses the 0-stops case and covers up to k stops incorrectly.
    - code: 'while prices != tmpPrices:'
      type: distractor
      why:
        ko: 수렴 조건은 정거소 제약을 추적하지 못합니다.
        en: Convergence-based iteration doesn't respect the k-stops constraint.
  - label:
      ko: 현재 가격 상태 스냅샷
      en: Create snapshot of prices
    indent: 1
    options:
    - code: tmpPrices = prices.copy()
      type: good
      why:
        ko: 복사본을 만들어서 이번 반복에서 이미 업데이트된 값을 사용하지 않습니다.
        en: Copying prevents using already-updated values within the same iteration.
    - code: tmpPrices = prices
      type: distractor
      why:
        ko: 참조만 복사하면 같은 객체를 가리키므로 스냅샷 목적을 잃습니다.
        en: Reference assignment means both variables point to the same list, defeating the snapshot purpose.
    - code: tmpPrices = [float('inf')] * n
      type: distractor
      why:
        ko: 매번 무한대로 리셋하면 이전 반복의 정보가 손실됩니다.
        en: Resetting to infinity loses information from the previous iteration.
  - label:
      ko: 모든 항공편 순회
      en: Iterate through all flights
    indent: 1
    options:
    - code: 'for s, d, p in flights:  # s=source, d=dest, p=price'
      type: good
      why:
        ko: 모든 항공편(간선)을 고려하여 경로 이완을 수행합니다.
        en: Process all available flights to relax edges in the graph.
    - code: 'for d, s, p in flights:'
      type: distractor
      why:
        ko: 출발지와 목적지를 바꾸면 역방향 그래프가 됩니다.
        en: Swapping source and destination reverses graph direction.
    - code: 'for s in range(n): for d in range(n):'
      type: distractor
      why:
        ko: 없는 항공편까지 처리하므로 비효율적입니다.
        en: Iterating all city pairs processes non-existent flights unnecessarily.
  - label:
      ko: 도달 불가 항공편 건너뛰기
      en: Skip unreachable sources
    indent: 2
    options:
    - code: 'if prices[s] == float("inf"):'
      type: good
      why:
        ko: 출발지에 도달한 적이 없으면(비용=무한대) 이 항공편을 사용할 수 없습니다.
        en: If the source city is unreachable (cost = infinity), we cannot use this flight.
    - code: 'if prices[s] > 0:'
      type: distractor
      why:
        ko: 0보다 크다는 조건은 도달 불가를 정확히 검사하지 못합니다.
        en: Checking > 0 doesn't accurately detect unreachable cities.
    - code: 'if tmpPrices[s] == float(''inf''):'
      type: distractor
      why:
        ko: tmpPrices는 현재 반복용이므로, 이전 반복의 prices를 확인해야 합니다.
        en: Should check prices (previous state), not tmpPrices (current iteration).
  - label:
      ko: 더 저렴한 경로 조건 확인
      en: Check if cheaper path exists
    indent: 2
    options:
    - code: 'if prices[s] + p < tmpPrices[d]:'
      type: good
      why:
        ko: 출발지 비용 + 항공편 비용이 현재 목적지 비용보다 작으면, 더 저렴한 경로를 찾은 것입니다.
        en: If the path cost through this flight is cheaper than the current best, we found an improvement.
    - code: 'if prices[s] + p <= tmpPrices[d]:'
      type: distractor
      why:
        ko: 같은 비용도 업데이트하면 불필요한 작업이 생깁니다.
        en: Using <= causes unnecessary redundant updates when costs are equal.
    - code: 'if prices[s] + p < prices[d]:'
      type: distractor
      why:
        ko: tmpPrices 대신 prices로 비교하면 같은 반복 내 업데이트를 사용하게 됩니다.
        en: Comparing to prices instead of tmpPrices causes updates within the same iteration.
  - label:
      ko: 목적지 최소 비용 갱신
      en: Record the cheaper cost
    indent: 2
    options:
    - code: tmpPrices[d] = prices[s] + p
      type: good
      why:
        ko: 더 저렴한 경로를 찾았으므로 목적지의 최소 비용을 업데이트합니다.
        en: Store the new minimum cost for reaching this destination city.
    - code: prices[d] = prices[s] + p
      type: distractor
      why:
        ko: prices를 직접 수정하면 같은 반복 내 캐스케이딩 업데이트가 발생합니다.
        en: Modifying prices directly causes cascading updates within the same iteration.
    - code: tmpPrices[d] = p
      type: distractor
      why:
        ko: p만 할당하면 출발지에서의 누적 비용을 잃습니다.
        en: Only storing p loses the cumulative cost from the source.
trace:
  code:
  - 'class Solution:'
  - '    def findCheapestPrice('
  - '        self, n: int, flights: List[List[int]], src: int, dst: int, k: int'
  - '    ) -> int:'
  - '        prices = [float("inf")] * n'
  - '        prices[src] = 0'
  - ''
  - '        for i in range(k + 1):'
  - '            tmpPrices = prices.copy()'
  - ''
  - '            for s, d, p in flights:  # s=source, d=dest, p=price'
  - '                if prices[s] == float("inf"):'
  - '                    continue'
  - '                if prices[s] + p < tmpPrices[d]:'
  - '                    tmpPrices[d] = prices[s] + p'
  - '            prices = tmpPrices'
  - '        return -1 if prices[dst] == float("inf") else prices[dst]'
  cases:
  - input: '4

      [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]]

      0

      3

      1'
    expected: '700'
  - input: '3

      [[0,1,100],[1,2,100],[0,2,500]]

      0

      2

      1'
    expected: '200'
  - input: '3

      [[0,1,100],[1,2,100],[0,2,500]]

      0

      2

      0'
    expected: '500'
  worked_example:
    input: '4

      [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]]

      0

      3

      1'
    steps:
    - ko: '초기화: prices = [0, ∞, ∞, ∞] (출발지 0의 비용은 0)'
      en: 'Initialize: prices = [0, ∞, ∞, ∞] (source city 0 has cost 0)'
    - ko: '반복 0 (0정거소): 항공편 [0→1, 100]로 도시 1에 100 비용으로 도달 → prices = [0, 100, ∞, ∞]'
      en: 'Iteration 0 (0 stops): Flight [0→1] costs 100 → prices = [0, 100, ∞, ∞]'
    - ko: '반복 1 (1정거소): 항공편 [1→3, 600]로 도시 3에 100+600=700 비용으로 도달 → prices = [0, 100, 200, 700]'
      en: 'Iteration 1 (1 stop): Flight [1→3] costs 600, so 100+600=700 to city 3 → prices = [0, 100, 200, 700]'
    - ko: '최종 답: prices[dst]=prices[3]=700'
      en: 'Final: prices[3] = 700'
    answer: '700'
solution:
  code: "class Solution:\n    def findCheapestPrice(\n        self, n: int, flights: List[List[int]], src: int, dst: int, k: int\n    ) -> int:\n        prices = [float(\"inf\")] * n\n        prices[src] = 0\n\n        for i in range(k + 1):\n            tmpPrices = prices.copy()\n\n            for s, d, p in flights:  # s=source, d=dest, p=price\n                if prices[s] == float(\"inf\"):\n                    continue\n                if prices[s] + p < tmpPrices[d]:\n                    tmpPrices[d] = prices[s] + p\n            prices = tmpPrices\n        return -1 if prices[dst] == float(\"inf\") else prices[dst]\n"
  complexity:
    time: O(k × m), m은 항공편 수 / O(k × m) where m = number of flights
    space: O(n) / O(n)
  followup:
  - ko: 음의 가중치가 있다면?
    en: What if flight prices could be negative?
  - ko: Bellman-Ford는 음수를 처리합니다. 이 DP 방식도 k 제약 덕분에 음수 가중치에서도 작동합니다. 단 음의 사이클이 있으면 음의 무한대가 가능합니다.
    en: While Bellman-Ford handles negative weights, this DP approach also works due to the k-stops constraint. Negative cycles could still produce negative infinity.
```