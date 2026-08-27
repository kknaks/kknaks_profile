---
created: '2026-06-19'
date: '2026-06-19'
day: Day 44
difficulty: hard
id: A-044
source:
  curated_in:
  - neetcode150
  number: 23
  platform: leetcode
  slug: merge-k-sorted-lists
  url: https://leetcode.com/problems/merge-k-sorted-lists/
tags:
- linked-list
- divide-and-conquer
- heap-priority-queue
- merge-sort
title:
  en: Merge k Sorted Lists
  ko: k개 정렬 리스트 병합
today: false
type: algorithm
updated: '2026-06-19'
visible: true
---

# k개 정렬 리스트 병합

## Data

```yaml
problem:
  title:
    ko: k개 정렬 리스트 병합
    en: Merge k Sorted Lists
  statement:
    ko: 'k개의 링크드 리스트로 이루어진 배열 lists가 주어집니다. 각 링크드 리스트는 오름차순으로 정렬되어 있습니다.


      모든 링크드 리스트를 하나의 정렬된 링크드 리스트로 병합하고 반환하세요.'
    en: 'You are given an array of k linked-lists lists, each linked-list is sorted in ascending order.


      Merge all the linked-lists into one sorted linked-list and return it.'
  constraints:
  - 0 ≤ k ≤ 10^4 (number of lists)
  - 0 ≤ lists[i].length ≤ 500 (per-list node count)
  - -10^4 ≤ lists[i][j] ≤ 10^4 (node values range)
  - Each list sorted in ascending order
  - Total nodes across all lists ≤ 10^4
  io:
  - input: '[[1,4,5],[1,3,4],[2,6]]'
    output: '[1,1,2,3,4,4,5,6]'
  - input: '[]'
    output: '[]'
  - input: '[[]]'
    output: '[]'
clarifying:
  items:
  - q:
      ko: 각 리스트가 가장 작은 값부터 가장 큰 값 순서로 정렬되어 있다는 의미인가요?
      en: Does 'ascending order' mean smallest-to-largest for each linked list?
    type: good
    why:
      ko: 리스트의 정렬 방향을 명확히 해야 노드 비교 로직을 올바르게 구현할 수 있습니다.
      en: Critical for understanding comparison direction when merging—directly affects which node to pick at each step.
  - q:
      ko: 입력 배열이 완전히 비어있는 경우(k=0)는 어떻게 처리하나요?
      en: What if the input lists array is completely empty (k=0)?
    type: good
    why:
      ko: 엣지 케이스로, 아무 리스트도 없을 때의 반환값을 정의해야 합니다.
      en: Critical edge case—function must handle when there are no lists to merge at all.
  - q:
      ko: '개별 리스트가 비어있을 수 있나요(예: lists = [[]])?'
      en: Can individual lists be empty (e.g., lists = [[]])?
    type: good
    why:
      ko: 일부 리스트에 노드가 없을 수 있으므로, 이 경우를 처리하는 방법을 알아야 합니다.
      en: Important edge case—some lists may have zero nodes while array itself is non-empty.
  - q:
      ko: 노드의 값이 음수일 수 있나요?
      en: Can node values be negative?
    type: good
    why:
      ko: 값의 범위를 알면 비교 연산이 모든 범위에서 올바르게 작동하는지 확인할 수 있습니다.
      en: Constraint clarification—ensures algorithm handles full range including negatives in comparisons.
  - q:
      ko: 모든 리스트의 총 노드 수 최댓값은?
      en: What is the maximum total nodes across all lists?
    type: good
    why:
      ko: 알고리즘 선택과 시간 복잡도 분석에 영향을 주는 제약 조건입니다.
      en: Key constraint for complexity analysis—helps assess which approach is optimal.
  - q:
      ko: 입력 리스트에 사이클이 있을 수 있나요?
      en: Can the input lists contain cycles?
    type: distractor
    why:
      ko: 문제에서 리스트가 '정렬된 오름차순'이라고 명시했으므로 사이클은 불가능합니다.
      en: Distractor—sorted linked lists cannot contain cycles by definition.
  - q:
      ko: 결과는 내림차순으로 정렬되어야 하나요?
      en: Should output be in descending order?
    type: distractor
    why:
      ko: 문제에서 명확히 '정렬된 링크드 리스트'를 반환하라 했으므로 오름차순이어야 합니다.
      en: Distractor—problem explicitly asks for 'sorted,' matching input order (ascending).
  - q:
      ko: 원본 입력 리스트를 수정할 수 없나요?
      en: Can we modify the original input lists in-place?
    type: distractor
    why:
      ko: 문제에서 명시하지 않은 사항이므로 해결 방법을 제약하지 않습니다.
      en: Distractor—problem doesn't specify, so it's not a primary concern for correctness.
approach:
  items:
  - name:
      ko: 분할 정복 (쌍별 병합)
      en: Divide and Conquer (Pairwise Merge)
    complexity: O(n log k) time / O(1) space (excluding output)
    type: good
    why:
      ko: k개 리스트를 두 개씩 쌍으로 병합하여 라운드마다 개수를 반으로 줄입니다. 총 log k 라운드이고 각 라운드에서 모든 n개 노드를 한 번씩 처리합니다.
      en: Repeatedly merge pairs of lists, halving count each round. Takes log k rounds, each processing all n nodes once—optimal balance.
  - name:
      ko: 최소 힙 / 우선순위 큐
      en: Min Heap / Priority Queue
    complexity: O(n log k) time / O(k) space
    type: good
    why:
      ko: 각 리스트의 헤드를 힙에 넣고, 최솟값을 반복 추출하며 다음 노드를 삽입합니다. 힙은 최대 k개 원소를 유지하므로 O(log k) 연산이 n번 반복됩니다.
      en: Maintain heap of k list heads. Repeatedly extract min and insert next node. Same time complexity as pairwise merge but different space-time tradeoff.
  - name:
      ko: 순차 병합 (첫 번째→두 번째→...)
      en: Sequential Merge
    complexity: O(n*k) time / O(1) space
    type: distractor
    why:
      ko: 첫 번째와 두 번째를 병합한 뒤, 결과에 세 번째를 병합하고... 반복합니다. 각 라운드마다 점점 커지는 리스트와 새로운 리스트를 병합하므로 최악의 경우 O(n*k)가 됩니다.
      en: Merge 1st + 2nd, then result + 3rd, etc. Growing list size each iteration causes quadratic behavior—much slower than log k rounds.
  - name:
      ko: 평탄화 후 정렬
      en: Flatten and Sort
    complexity: O(n log n) time / O(n) space
    type: distractor
    why:
      ko: 모든 노드 값을 배열에 추출하고 정렬한 후 새 리스트로 재구성합니다. 입력이 이미 정렬되어 있다는 정보를 낭비하므로 O(n log n)이 되어 비효율적입니다.
      en: Extract all values, sort them, rebuild list. Ignores the fact that inputs are already sorted—O(n log n) > O(n log k) for small k.
  - name:
      ko: 모든 노드를 힙에 삽입
      en: Heap with All Nodes Upfront
    complexity: O(n log n) time / O(n) space
    type: distractor
    why:
      ko: 모든 n개 노드를 한 번에 힙에 삽입합니다. 힙은 n개를 유지해야 하므로 O(log n) 연산이 필요하여, k개만 유지하는 것보다 느립니다.
      en: Insert all n nodes upfront. Heap size becomes n, making operations O(log n) instead of O(log k)—slower than selective heap approach.
logic:
  format: slot
  slots:
  - label:
      ko: 빈 입력 처리
      en: Handle empty input
    indent: 0
    options:
    - code: 'if not lists or len(lists) == 0:'
      type: good
      why:
        ko: 입력이 None이거나 빈 배열인지 먼저 확인하고 None을 반환합니다. 이 검사가 없으면 이후 코드가 에러를 발생시킵니다.
        en: Checks both None and empty array before processing. Prevents crashes and handles base case where there are no lists.
    - code: 'if len(lists) == 0:'
      type: distractor
      why:
        ko: '''not lists'' 체크가 없으면 lists가 None일 때 len() 호출로 에러 발생합니다.'
        en: Missing 'not lists' check—will crash with TypeError if lists is None.
    - code: 'if lists:'
      type: distractor
      why:
        ko: 논리가 반대로 되어 리스트가 있을 때 None을 반환하고 없을 때 계속 진행하게 됩니다.
        en: Inverted logic—returns None when lists exist and tries to process when empty.
  - label:
      ko: 병합 반복 루프 조건
      en: Loop until one list remains
    indent: 0
    options:
    - code: 'while len(lists) > 1:'
      type: good
      why:
        ko: 리스트가 2개 이상일 때만 반복합니다. 1개 남으면 최종 결과이므로 루프를 빠져나옵니다. 이것이 분할 정복의 핵심입니다.
        en: Continues merging while 2+ lists remain. Exits when exactly one list is left—the merged result. Core of divide-and-conquer strategy.
    - code: 'while len(lists) > 0:'
      type: distractor
      why:
        ko: 1개 리스트가 남아도 계속 반복하려고 하므로, range(0, 1, 2)는 i=0만 생성하고 lists[1]에 접근할 때 에러가 발생합니다.
        en: Would attempt to merge single list with itself—IndexError when accessing lists[i+1].
    - code: 'while len(lists) >= 1:'
      type: distractor
      why:
        ko: '>= 1은 1개 이상을 의미하므로 1개일 때도 루프 본문을 실행하려고 합니다.'
        en: Same issue as > 0—continues when only one list remains, causing index error.
  - label:
      ko: 2씩 증가하는 인덱스 반복
      en: Iterate by step of 2
    indent: 1
    options:
    - code: 'for i in range(0, len(lists), 2):'
      type: good
      why:
        ko: range의 세 번째 인자 2로 인해 0, 2, 4, ... 를 방문합니다. 각 i마다 lists[i]와 lists[i+1]의 쌍을 처리하는 방식입니다.
        en: step=2 generates indices 0, 2, 4,... Each i pairs lists[i] with lists[i+1]. This is how pairwise merge groups adjacent lists.
    - code: 'for i in range(0, len(lists)):'
      type: distractor
      why:
        ko: 모든 인덱스 0, 1, 2, 3, ...를 방문하므로 각 리스트를 개별적으로 처리하게 되어 올바른 쌍을 만들 수 없습니다.
        en: Visits all indices—pairs become (0,1), (1,2), (2,3)... overlapping and illogical.
    - code: 'for i in range(len(lists)//2):'
      type: distractor
      why:
        ko: 0, 1, 2, ...를 방문하므로 lists[0], lists[1]을 계속 처리하고 나머지 리스트들은 건너뜁니다.
        en: Generates 0, 1, 2... only accessing lists[0] and lists[1] repeatedly—ignores rest of array.
  - label:
      ko: 홀수 개 리스트 경계 처리
      en: Handle odd count boundary
    indent: 2
    options:
    - code: l2 = lists[i + 1] if (i + 1) < len(lists) else None
      type: good
      why:
        ko: 다음 인덱스가 배열 범위를 벗어나는지 확인합니다. 범위 내면 lists[i+1]을, 범위 밖이면 None을 할당합니다. 홀수 개일 때 마지막 리스트는 None과 병합되어 그대로 다음 라운드로 전달됩니다.
        en: Safely checks if next index exists. Odd-count last list pairs with None instead of crashing. Unchanged list passes to next round.
    - code: l2 = lists[i + 1]
      type: distractor
      why:
        ko: 경계 체크가 없어서 i+1이 범위를 벗어나면 IndexError가 발생합니다.
        en: No boundary check—crashes with IndexError when i+1 >= len(lists).
    - code: l2 = lists[i + 1] if i + 1 < len(lists) - 1 else None
      type: distractor
      why:
        ko: off-by-one 에러입니다. 예를 들어 2개 리스트일 때 i=0이고 조건은 '1 < 1'이 되어 False이므로 None을 할당하게 됩니다.
        en: Off-by-one error—last valid pair is incorrectly rejected (e.g., with 2 lists, i=0 gives '1 < 1' = False).
  - label:
      ko: 병합 결과를 새 배열에 저장
      en: Append merged result
    indent: 2
    options:
    - code: mergedLists.append(self.mergeList(l1, l2))
      type: good
      why:
        ko: 두 리스트를 병합한 결과를 mergedLists에 추가합니다. 원본 lists를 수정하지 않으므로 루프의 반복 로직이 올바르게 작동합니다.
        en: Stores merged pair in new array, preserving loop integrity. If you appended to lists instead, loop indices would become invalid mid-iteration.
    - code: lists.append(self.mergeList(l1, l2))
      type: distractor
      why:
        ko: 반복 중인 원본 배열을 수정하므로 len(lists)가 변하고 반복 인덱스가 잘못됩니다.
        en: Modifies lists while iterating over it—changes len(lists), corrupting loop indices.
    - code: mergedLists.extend([l1, l2])
      type: distractor
      why:
        ko: 병합하지 않은 원본 두 개를 추가하므로 알고리즘 목표가 무효화됩니다.
        en: Adds unpaired originals instead of merged result—defeats entire purpose of merging.
  - label:
      ko: 다음 라운드 입력 준비
      en: Update for next round
    indent: 1
    options:
    - code: lists = mergedLists
      type: good
      why:
        ko: 방금 생성한 mergedLists (크기가 반으로 줄어든)를 lists에 할당합니다. 다음 while 반복에서는 이 새로운 mergedLists를 입력으로 사용하여 다시 쌍으로 병합합니다.
        en: Replaces lists with merged pairs for next iteration. Halves list count each round—total rounds = log k.
    - code: mergedLists = lists
      type: distractor
      why:
        ko: 할당이 역순입니다. 병합 결과를 잃고 원본으로 덮어씌웁니다.
        en: Inverted assignment—loses merged results and reverts to originals.
    - code: lists.extend(mergedLists)
      type: distractor
      why:
        ko: 원본과 병합 결과를 모두 유지하므로 다음 라운드에서 리스트 개수가 증가하여 루프가 제대로 작동하지 않습니다.
        en: Keeps both originals and merged—doubles count each round, breaking the halving logic.
trace:
  code:
  - '# Definition for singly-linked list.'
  - '# class ListNode:'
  - '#     def __init__(self, val=0, next=None):'
  - '#         self.val = val'
  - '#         self.next = next'
  - 'class Solution:'
  - '    def mergeKLists(self, lists: List[ListNode]) -> ListNode:'
  - '        if not lists or len(lists) == 0:'
  - '            return None'
  - ''
  - '        while len(lists) > 1:'
  - '            mergedLists = []'
  - '            for i in range(0, len(lists), 2):'
  - '                l1 = lists[i]'
  - '                l2 = lists[i + 1] if (i + 1) < len(lists) else None'
  - '                mergedLists.append(self.mergeList(l1, l2))'
  - '            lists = mergedLists'
  - '        return lists[0]'
  - ''
  - '    def mergeList(self, l1, l2):'
  - '        dummy = ListNode()'
  - '        tail = dummy'
  - ''
  - '        while l1 and l2:'
  - '            if l1.val < l2.val:'
  - '                tail.next = l1'
  - '                l1 = l1.next'
  - '            else:'
  - '                tail.next = l2'
  - '                l2 = l2.next'
  - '            tail = tail.next'
  - '        if l1:'
  - '            tail.next = l1'
  - '        if l2:'
  - '            tail.next = l2'
  - '        return dummy.next'
  cases:
  - input: '[[1,4,5],[1,3,4],[2,6]]'
    expected: '[1,1,2,3,4,4,5,6]'
  - input: '[]'
    expected: '[]'
  - input: '[[]]'
    expected: '[]'
  worked_example:
    input: '[[1,4,5],[1,3,4],[2,6]]'
    steps:
    - ko: '3개 리스트로 시작: lists = [[1→4→5], [1→3→4], [2→6]]. len(lists)=3 > 1이므로 루프 진입'
      en: 'Start: lists has 3 lists, condition len=3 > 1 is True, enter loop'
    - ko: '라운드 1: i=0에서 [1→4→5]와 [1→3→4] 병합 → [1→1→3→4→4→5]. i=2에서 [2→6]과 None 병합 → [2→6]. mergedLists = [[1→1→3→4→4→5], [2→6]], 이제 lists = mergedLists (2개 리스트)'
      en: 'Round 1: Merge pairs (i=0) [1→4→5]+[1→3→4]→[1→1→3→4→4→5], (i=2) [2→6]+None→[2→6]. Now lists = [[1→1→3→4→4→5], [2→6]]'
    - ko: '라운드 2: len(lists)=2 > 1이므로 계속. i=0에서 [1→1→3→4→4→5]와 [2→6] 병합 → [1→1→2→3→4→4→5→6]. mergedLists = [[1→1→2→3→4→4→5→6]], 이제 lists = mergedLists (1개 리스트)'
      en: 'Round 2: len=2 > 1, continue. Merge (i=0) [1→1→3→4→4→5]+[2→6]→[1→1→2→3→4→4→5→6]. Now lists = [[1→1→2→3→4→4→5→6]]'
    - ko: len(lists)=1이므로 1 > 1 조건이 False. 루프 종료. return lists[0] = [1→1→2→3→4→4→5→6]
      en: len=1, condition 1 > 1 is False, exit loop. Return lists[0] = [1→1→2→3→4→4→5→6]
    answer: '[1,1,2,3,4,4,5,6]'
solution:
  code: "# Definition for singly-linked list.\n# class ListNode:\n#     def __init__(self, val=0, next=None):\n#         self.val = val\n#         self.next = next\nclass Solution:\n    def mergeKLists(self, lists: List[ListNode]) -> ListNode:\n        if not lists or len(lists) == 0:\n            return None\n\n        while len(lists) > 1:\n            mergedLists = []\n            for i in range(0, len(lists), 2):\n                l1 = lists[i]\n                l2 = lists[i + 1] if (i + 1) < len(lists) else None\n                mergedLists.append(self.mergeList(l1, l2))\n            lists = mergedLists\n        return lists[0]\n\n    def mergeList(self, l1, l2):\n        dummy = ListNode()\n        tail = dummy\n\n        while l1 and l2:\n            if l1.val < l2.val:\n                tail.next = l1\n                l1 = l1.next\n            else:\n                tail.next = l2\n                l2 = l2.next\n            tail = tail.next\n        if l1:\n            tail.next = l1\n\
    \        if l2:\n            tail.next = l2\n        return dummy.next\n"
  complexity:
    time: O(n log k)
    space: O(1)
  followup:
  - ko: 우선순위 큐(최소 힙)를 사용해도 시간 복잡도는 같습니다. 어떤 상황에서 힙 방식이 더 나을까요?
    en: How would a min-heap approach work? When might it be preferable despite the same time complexity?
  - ko: 순차 병합(첫 번째→두 번째→세 번째...) 방식을 사용하면 시간 복잡도가 어떻게 되나요?
    en: What happens to time complexity if you merge sequentially (1st+2nd, result+3rd, etc.) instead of pairwise?
  - ko: k개 리스트 대신 3개씩 병합한다면(재귀 깊이가 log₃ k) 시간 복잡도는 어떻게 변할까요?
    en: If you merged 3 lists at a time (recursive depth log₃ k), how would overall complexity change?
```