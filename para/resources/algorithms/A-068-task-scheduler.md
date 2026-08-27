---
created: '2026-07-20'
date: '2026-07-20'
day: Day 68
difficulty: medium
id: A-068
source:
  curated_in:
  - neetcode150
  number: 621
  platform: leetcode
  slug: task-scheduler
  url: https://leetcode.com/problems/task-scheduler/
tags:
- array
- hash-table
- greedy
- sorting
- heap-priority-queue
- counting
title:
  en: Task Scheduler
  ko: CPU 작업 스케줄링
today: false
type: algorithm
updated: '2026-07-20'
visible: true
---

# CPU 작업 스케줄링

## Data

```yaml
problem:
  title:
    ko: CPU 작업 스케줄링
    en: Task Scheduler
  statement:
    ko: 'A부터 Z까지의 레이블이 있는 CPU 작업 배열이 주어집니다. 또한 정수 n이 주어집니다. 각 CPU 구간은 유휴 상태이거나 하나의 작업을 완료할 수 있습니다. 작업은 어떤 순서로든 완료될 수 있지만, 같은 레이블의 두 작업 사이에는 최소 n개의 구간만큼의 간격이 있어야 합니다.


      모든 작업을 완료하는 데 필요한 최소 CPU 구간 수를 반환하세요.'
    en: 'You are given an array of CPU tasks, each labeled with a letter from A to Z, and a number n. Each CPU interval can be idle or allow the completion of one task. Tasks can be completed in any order, but there''s a constraint: there has to be a gap of at least n intervals between two tasks with the same label.


      Return the minimum number of CPU intervals required to complete all tasks.'
  constraints:
  - 1 ≤ tasks.length ≤ 10⁴
  - tasks[i] is an uppercase English letter
  - 0 ≤ n ≤ 100
  io:
  - input: '["A","A","A","B","B","B"]

      2'
    output: '8'
  - input: '["A","C","A","B","D","B"]

      1'
    output: '6'
  - input: '["A","A","A", "B","B","B"]

      3'
    output: '10'
clarifying:
  items:
  - q:
      ko: 같은 레이블의 작업 사이에 'n개의 구간 간격'은 정확히 무엇을 의미하나요?
      en: What exactly does 'a gap of at least n intervals' between two tasks with the same label mean?
    type: good
    why:
      ko: 한 작업을 실행한 후, 같은 작업을 다시 실행하기 전에 n개의 다른 구간(작업 또는 유휴)이 반드시 지나야 합니다.
      en: After executing a task, at least n other intervals (whether other tasks or idle) must pass before executing the same task again.
  - q:
      ko: 가장 빈번한 작업을 우선으로 처리하면 왜 최적해를 보장하나요?
      en: Why does always executing the most frequent available task lead to an optimal solution?
    type: good
    why:
      ko: 가장 빈번한 작업이 전체 스케줄의 경계를 결정합니다. 이 작업을 효율적으로 조율하지 못하면 다른 작업들의 배치도 최적이 될 수 없습니다.
      en: The most frequent task determines the overall schedule structure and idle time. If we cannot schedule it efficiently, no other arrangement will be better.
  - q:
      ko: 모든 작업이 서로 다르면 답은 어떻게 되나요?
      en: What is the answer if all tasks are different from each other?
    type: good
    why:
      ko: 모든 작업이 서로 다르면 어떤 작업도 반복되지 않으므로 냉각 제약이 없습니다. 답은 단순히 작업의 개수입니다.
      en: If all tasks are different, no task repeats, so cooling constraints do not apply. The answer is simply the total number of tasks.
  - q:
      ko: n=0이면 답은 무엇인가요?
      en: If n = 0, what is the answer?
    type: good
    why:
      ko: 냉각 시간이 없으므로 모든 작업을 연속으로 실행할 수 있습니다. 답은 작업의 총 개수입니다.
      en: No cooling period is needed, so tasks can be executed back-to-back. The answer is the total number of tasks.
  - q:
      ko: 큐에 저장되는 [cnt, time + n] 값은 무엇을 의미하나요?
      en: What do the values [cnt, time + n] stored in the queue represent?
    type: good
    why:
      ko: cnt는 해당 작업의 남은 실행 횟수이고, time + n은 그 작업을 다시 실행할 수 있는 가장 빠른 시간입니다.
      en: cnt is the remaining count of that task, and time + n is the earliest time when that task can be executed again.
  - q:
      ko: Python의 heapq가 최소 힙인데 왜 음수를 사용하여 최대 힙을 만드나요?
      en: Why do we use negative values if we need a max-heap and Python's heapq provides a min-heap?
    type: good
    why:
      ko: Python의 heapq는 기본적으로 최소 힙만 지원합니다. 값을 음수로 저장하면 최소 힙이 최대값을 우선으로 처리하게 됩니다.
      en: Python's heapq only provides min-heap. By storing negative values, the min-heap effectively acts as a max-heap.
  - q:
      ko: 시간을 q[0][1]로 점프하는 것은 언제 발생하고 왜 필요한가요?
      en: When and why do we jump time to q[0][1]?
    type: distractor
    why:
      ko: 힙이 비어있고 어떤 작업도 즉시 실행할 수 없을 때, 다음 작업이 준비되는 시간으로 점프하여 불필요한 유휴 반복을 피합니다.
      en: When the heap is empty and no task can execute immediately, we skip ahead to when the next task becomes available to avoid unnecessary idle iterations.
  - q:
      ko: 1 + heappop() 후 cnt가 0이 되면 그 작업은 완전히 완료된 건가요?
      en: If cnt becomes 0 after 1 + heappop(), does that mean all instances of that task are complete?
    type: distractor
    why:
      ko: 네, cnt = 0이면 해당 작업의 모든 인스턴스가 실행되었으므로 큐에 추가할 필요가 없습니다.
      en: Yes, cnt = 0 means all instances have been executed, so we don't add it back to the queue.
approach:
  items:
  - name:
      ko: 최대 힙 + 큐 시뮬레이션
      en: Max Heap + Queue Simulation
    complexity: O(n log k) where k is the number of unique tasks
    type: good
    why:
      ko: 각 시간 단계에서 가장 빈번한 작업을 선택하고, 냉각이 끝난 작업을 복원합니다. 힙 연산은 O(log k)의 비용입니다.
      en: At each time step, select the most frequent available task and restore tasks whose cooling has finished. Heap operations cost O(log k).
  - name:
      ko: 수학적 공식 접근
      en: Mathematical Formula
    complexity: O(n) where n is the total number of tasks
    type: good
    why:
      ko: '최대 빈도를 이용하여 직접 계산: (max_count - 1) * (n + 1) + max_count의 개수. 시뮬레이션을 완전히 건너뜁니다.'
      en: 'Directly calculate from maximum frequency: (max_count - 1) * (n + 1) + count_of_tasks_with_max_freq. No simulation needed.'
  - name:
      ko: 우선순위 큐 정렬
      en: Priority Queue with Pre-sorting
    complexity: O(n log n)
    type: distractor
    why:
      ko: 모든 작업을 미리 정렬하는 것은 작업이 실행되면서 변하는 빈도에 동적으로 대응하지 못합니다.
      en: Pre-sorting all tasks doesn't adapt to the changing frequencies as tasks execute, making it inefficient.
  - name:
      ko: 라운드 로빈 스케줄링
      en: Round-Robin Scheduling
    complexity: O(n²) in worst case
    type: distractor
    why:
      ko: 매 회차마다 모든 남은 작업을 확인하면 시간 복잡도가 급격히 증가합니다.
      en: Checking all remaining tasks each round leads to quadratic time complexity in worst case.
  - name:
      ko: 그리디 (최빈도 우선 + 수학)
      en: Greedy with Mathematical Optimization
    complexity: O(n)
    type: good
    why:
      ko: 최대 빈도만 필요하므로 매우 우아합니다. 수학적 공식의 변형으로, 시뮬레이션의 복잡성을 완전히 제거합니다.
      en: Only requires computing the maximum frequency, making it very elegant. It's the mathematical variant that eliminates simulation complexity.
logic:
  format: slot
  slots:
  - label:
      ko: 각 작업의 빈도 계산
      en: Count task frequencies
    indent: 0
    options:
    - code: count = Counter(tasks)
      type: good
      why:
        ko: Counter를 사용하여 각 작업이 몇 번 나타나는지 계산합니다. 이는 스케줄링 결정의 기초가 됩니다.
        en: Use Counter to determine how many times each task appears. This frequency distribution drives all scheduling decisions.
    - code: count = set(tasks)
      type: distractor
      why:
        ko: set은 각 작업이 몇 번 나타나는지 알려주지 않습니다. 빈도 정보를 잃게 됩니다.
        en: A set only tells us which tasks exist, not their frequencies. We lose critical frequency information.
    - code: 'count = {task: len([t for t in tasks if t == task]) for task in set(tasks)}'
      type: distractor
      why:
        ko: 기술적으로 작동하지만 비효율적입니다. Counter가 이미 최적화되어 있습니다.
        en: Technically works but is inefficient. Counter is already optimized for this exact use case.
  - label:
      ko: 최대 힙 구성 (음수 변환)
      en: Build max heap with negation
    indent: 0
    options:
    - code: maxHeap = [-cnt for cnt in count.values()]
      type: good
      why:
        ko: Python의 최소 힙을 최대 힙으로 변환하기 위해 빈도를 음수로 변환합니다. 가장 빈번한 작업이 최우선 순위를 갖습니다.
        en: Negate frequencies to convert Python's min-heap into a max-heap behavior. Most frequent tasks get highest priority.
    - code: maxHeap = list(count.values())
      type: distractor
      why:
        ko: 음수 없이는 최소 힙이 되어, 가장 빈도가 낮은 작업을 우선으로 처리하게 됩니다.
        en: Without negation, we get a min-heap that prioritizes the least frequent tasks—opposite of what we need.
    - code: maxHeap = sorted([-cnt for cnt in count.values()], reverse=True)
      type: distractor
      why:
        ko: 정렬은 불필요합니다. heapify()가 O(n) 시간에 힙 구조를 구성합니다.
        en: Sorting is unnecessary overhead. heapify() builds the heap structure in O(n) time without sorting.
  - label:
      ko: 주 시뮬레이션 루프
      en: Main simulation loop
    indent: 0
    options:
    - code: 'while maxHeap or q:'
      type: good
      why:
        ko: 힙이나 큐에 작업이 남아있는 동안 계속 시뮬레이션을 진행합니다. 둘 다 비어야 모든 작업이 완료된 것입니다.
        en: Continue while tasks remain in either the heap or queue. Only when both are empty have all tasks been scheduled.
    - code: 'while maxHeap:'
      type: distractor
      why:
        ko: 큐에 남은 작업도 처리해야 합니다. 둘 다 비어야 루프를 종료할 수 있습니다.
        en: Must also process tasks in the queue. The loop should continue until both heap and queue are empty.
    - code: 'while q:'
      type: distractor
      why:
        ko: 힙에 남은 작업도 처리해야 합니다.
        en: Must also process tasks in the heap.
  - label:
      ko: 시간 관리 및 유휴 처리
      en: Manage time and handle idle intervals
    indent: 1
    options:
    - code: time = q[0][1]
      type: good
      why:
        ko: 힙이 비어있으면 (실행할 작업이 없으면) 다음 작업이 준비되는 시간으로 점프하여 불필요한 유휴 반복을 건너뜁니다.
        en: When the heap is empty (no task available to execute), jump time directly to when the next task becomes ready, skipping idle iterations.
    - code: time += n
      type: distractor
      why:
        ko: 항상 n만큼 증가시키는 것은 잘못되었습니다. 다음 작업이 준비되는 정확한 시간으로 점프해야 합니다.
        en: Always incrementing by n is incorrect. We need to jump to the exact time the next task becomes available.
    - code: 'if not maxHeap: time += 1'
      type: distractor
      why:
        ko: 한 번에 1씩 증가시키면 많은 유휴 반복을 통과하게 되어 비효율적입니다.
        en: Incrementing by 1 forces us through many idle iterations, defeating the optimization.
  - label:
      ko: 가장 빈번한 작업 실행
      en: Execute most frequent task
    indent: 1
    options:
    - code: cnt = 1 + heapq.heappop(maxHeap)
      type: good
      why:
        ko: 힙에서 가장 빈번한 작업을 꺼내고, +1을 더한 후 1을 감소시킵니다. 이는 해당 작업이 한 번 실행되고 남은 횟수를 계산합니다.
        en: Pop the most frequent task from the heap, add 1 to convert negative back to positive, then decrement by 1 to reflect execution.
    - code: cnt = heapq.heappop(maxHeap)
      type: distractor
      why:
        ko: +1을 잊으면 음수 값을 직접 처리하게 되어 논리가 틀립니다.
        en: Without +1, we're working with the negated value, breaking the decrement logic.
    - code: cnt = 1 + heapq.heappop(maxHeap) - 1
      type: distractor
      why:
        ko: +1과 -1이 서로 상쇄되므로 실제로는 작업 빈도 감소가 없습니다.
        en: The +1 and -1 cancel out, so the task frequency doesn't actually decrease.
  - label:
      ko: 냉각 제약 관리 및 작업 복원
      en: Manage cooldown and restore ready tasks
    indent: 1
    options:
    - code: 'if q and q[0][1] == time:'
      type: good
      why:
        ko: 큐의 첫 작업이 현재 시간에 냉각 완료되면, 그 작업을 힙으로 복원하여 다시 실행할 수 있게 합니다.
        en: When a queued task's cooldown has finished (q[0][1] == time), restore it to the heap so it can be executed again.
    - code: 'if q and q[0][1] < time:'
      type: distractor
      why:
        ko: < 연산자를 사용하면 준비 시간을 놓칠 수 있습니다. 정확한 == 비교가 필요합니다.
        en: Using < instead of == might restore tasks before they're ready, violating the cooldown constraint.
    - code: 'while q and q[0][1] == time:'
      type: distractor
      why:
        ko: while를 사용하면 같은 시간에 여러 작업을 복원할 수 있지만, 시뮬레이션의 정확성을 해칩니다.
        en: Using while might restore multiple tasks at once, which could violate the single-task-per-interval constraint.
trace:
  code:
  - 'class Solution:'
  - '    def leastInterval(self, tasks: List[str], n: int) -> int:'
  - '        count = Counter(tasks)'
  - '        maxHeap = [-cnt for cnt in count.values()]'
  - '        heapq.heapify(maxHeap)'
  - ''
  - '        time = 0'
  - '        q = deque()  # pairs of [-cnt, idleTime]'
  - '        while maxHeap or q:'
  - '            time += 1'
  - ''
  - '            if not maxHeap:'
  - '                time = q[0][1]'
  - '            else:'
  - '                cnt = 1 + heapq.heappop(maxHeap)'
  - '                if cnt:'
  - '                    q.append([cnt, time + n])'
  - '            if q and q[0][1] == time:'
  - '                heapq.heappush(maxHeap, q.popleft()[0])'
  - '        return time'
  - ''
  - ''
  - '# Greedy algorithm'
  - 'class Solution(object):'
  - '    def leastInterval(self, tasks: List[str], n: int) -> int:'
  - '        counter = collections.Counter(tasks)'
  - '        max_count = max(counter.values())'
  - '        min_time = (max_count - 1) * (n + 1) + \'
  - '                    sum(map(lambda count: count == max_count, counter.values()))'
  - '    '
  - '        return max(min_time, len(tasks))'
  cases:
  - input: '["A","A","A","B","B","B"]

      2'
    expected: '8'
  - input: '["A","C","A","B","D","B"]

      1'
    expected: '6'
  - input: '["A","A","A", "B","B","B"]

      3'
    expected: '10'
  worked_example:
    input: '["A","A","A","B","B","B"]

      2'
    steps:
    - ko: '입력: tasks=[A,A,A,B,B,B], n=2 → 각 작업 3개, 냉각 기간 2'
      en: 'Input: tasks=[A,A,A,B,B,B], n=2 → 3 of each task, cooldown=2'
    - ko: count={A:3, B:3}, maxHeap=[-3,-3] → 두 작업이 동일한 우선순위로 시작
      en: count={A:3, B:3}, maxHeap=[-3,-3] → Both tasks start with equal priority
    - ko: '시간 1: A 실행 (A 남은:2, 시간 3에 준비), 시간 2: B 실행 (B 남은:2, 시간 4에 준비)'
      en: 'Time 1: Execute A (remaining:2, ready at 3), Time 2: Execute B (remaining:2, ready at 4)'
    - ko: '시간 3: 힙이 비었으므로 유휴 → 시간 4로 점프, A 복원. 시간 4: A 실행 (남은:1, 준비:6), B 복원'
      en: 'Time 3: Heap empty, jump to time 4. Time 4: Execute A (remaining:1, ready at 6), restore B'
    - ko: '시간 5: B 실행 (남은:1, 준비:7). 시간 6: 힙이 비었으므로 유휴 → 시간 7로 점프, A 복원'
      en: 'Time 5: Execute B (remaining:1, ready at 7). Time 6: Jump to time 7, restore A'
    - ko: '시간 7: A 실행 (남은:0), B 복원. 시간 8: B 실행 (남은:0) → 완료'
      en: 'Time 7: Execute A (remaining:0), restore B. Time 8: Execute B (remaining:0) → Done'
    answer: '8'
solution:
  code: "class Solution:\n    def leastInterval(self, tasks: List[str], n: int) -> int:\n        count = Counter(tasks)\n        maxHeap = [-cnt for cnt in count.values()]\n        heapq.heapify(maxHeap)\n\n        time = 0\n        q = deque()  # pairs of [-cnt, idleTime]\n        while maxHeap or q:\n            time += 1\n\n            if not maxHeap:\n                time = q[0][1]\n            else:\n                cnt = 1 + heapq.heappop(maxHeap)\n                if cnt:\n                    q.append([cnt, time + n])\n            if q and q[0][1] == time:\n                heapq.heappush(maxHeap, q.popleft()[0])\n        return time\n\n\n# Greedy algorithm\nclass Solution(object):\n    def leastInterval(self, tasks: List[str], n: int) -> int:\n        counter = collections.Counter(tasks)\n        max_count = max(counter.values())\n        min_time = (max_count - 1) * (n + 1) + \\\n                    sum(map(lambda count: count == max_count, counter.values()))\n    \n        return\
    \ max(min_time, len(tasks))"
  complexity:
    time: O(n log k) for heap simulation where k is unique tasks, or O(n) for mathematical formula approach
    space: O(k) for heap and queue where k is the number of unique tasks
  followup:
  - ko: n이 매우 크면 유휴 시간이 많아집니다. 시뮬레이션 대신 수학적 공식을 사용하면 어떤 이점이 있을까요?
    en: If n is very large, many intervals will be idle. What are the advantages of using the mathematical formula (max_count - 1) * (n + 1) + count_of_max instead of simulation?
  - ko: 일부 작업이 다른 작업보다 우선순위가 높다면 어떻게 해결하겠습니까?
    en: How would you modify the solution if some tasks have higher priority than others?
  - ko: 각 작업에 실행 시간이 다르다면 (어떤 작업은 2개 구간, 어떤 작업은 1개 구간) 어떻게 해결하겠습니까?
    en: How would you solve this if each task takes a different amount of time to execute (e.g., some take 1 interval, others take 2)?
```