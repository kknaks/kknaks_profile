---
created: '2026-07-25'
date: '2026-07-25'
day: Day 69
difficulty: medium
id: A-069
source:
  curated_in:
  - neetcode150
  number: 355
  platform: leetcode
  slug: design-twitter
  url: https://leetcode.com/problems/design-twitter/
tags:
- hash-table
- linked-list
- design
- heap-priority-queue
title:
  en: Design Twitter
  ko: 트위터 설계
today: false
type: algorithm
updated: '2026-07-25'
visible: true
---

# 트위터 설계

## Data

```yaml
problem:
  title:
    ko: 트위터 설계
    en: Design Twitter
  statement:
    en: 'Design a simplified version of Twitter where users can post tweets, follow/unfollow another user, and is able to see the 10 most recent tweets in the user''s news feed.


      Implement the Twitter class:

      - Twitter() Initializes your twitter object.

      - void postTweet(int userId, int tweetId) Composes a new tweet with ID tweetId by the user userId. Each call to this function will be made with a unique tweetId.

      - List<Integer> getNewsFeed(int userId) Retrieves the 10 most recent tweet IDs in the user''s news feed. Each item in the news feed must be posted by users who the user followed or by the user themself. Tweets must be ordered from most recent to least recent.

      - void follow(int followerId, int followeeId) The user with ID followerId started following the user with ID followeeId.

      - void unfollow(int followerId, int followeeId) The user with ID followerId started unfollowing the user with ID followeeId.'
    ko: '사용자가 트윗을 작성하고, 다른 사용자를 팔로우/언팔로우하며, 사용자의 뉴스 피드에서 10개의 가장 최근 트윗을 볼 수 있는 간단한 버전의 트위터를 설계하세요.


      Twitter 클래스를 구현하세요:

      - Twitter() 트위터 객체를 초기화합니다.

      - void postTweet(int userId, int tweetId) 사용자 userId가 ID tweetId를 가진 새 트윗을 작성합니다. 이 함수를 호출할 때마다 고유한 tweetId가 전달됩니다.

      - List<Integer> getNewsFeed(int userId) 사용자의 뉴스 피드에서 10개의 가장 최근 트윗 ID를 검색합니다. 뉴스 피드의 각 항목은 사용자가 팔로우한 사용자나 사용자 자신이 작성한 것이어야 합니다. 트윗은 가장 최근부터 가장 오래된 순서로 정렬되어야 합니다.

      - void follow(int followerId, int followeeId) ID가 followerId인 사용자가 ID가 followeeId인 사용자를 팔로우하기 시작합니다.

      - void unfollow(int followerId, int followeeId) ID가 followerId인 사용자가 ID가 followeeId인 사용자를 언팔로우하기 시작합니다.'
  constraints:
  - 1 ≤ userId, followerId, followeeId ≤ 500
  - 0 ≤ tweetId ≤ 10^4
  - All tweets have unique IDs
  - At most 3*10^4 calls will be made to postTweet, getNewsFeed, follow, and unfollow
  - A user cannot follow themselves
  io:
  - input: '["Twitter","postTweet","getNewsFeed","follow","postTweet","getNewsFeed","unfollow","getNewsFeed"]

      [[],[1,5],[1],[1,2],[2,6],[1],[1,2],[1]]'
    output: '[null, null, [5], null, null, [6, 5], null, [5]]'
clarifying:
  items:
  - q:
      ko: 사용자가 자신의 트윗을 뉴스 피드에서 볼 수 있나요?
      en: Should a user see their own tweets in their news feed?
    type: good
    why:
      ko: 사용자는 자신을 자동으로 팔로우하지 않으므로 명시적으로 포함해야 합니다.
      en: Users don't automatically follow themselves, so their own tweets must be explicitly included.
  - q:
      ko: 뉴스 피드에서 반환할 트윗의 최대 개수는 얼마인가요?
      en: What is the maximum number of tweets to return in the news feed?
    type: good
    why:
      ko: 문제에서 10개의 가장 최신 트윗을 명시하고 있으므로 피드 크기 제한을 이해해야 합니다.
      en: The problem specifies exactly 10 most recent tweets, which is crucial for algorithm design.
  - q:
      ko: 자신을 팔로우할 수 있나요?
      en: Can a user follow themselves?
    type: good
    why:
      ko: 제약 조건에서 사용자는 자신을 팔로우할 수 없다고 명시되어 있습니다.
      en: Constraints explicitly state a user cannot follow themselves, avoiding circular reference issues.
  - q:
      ko: 이미 팔로우하고 있는 사용자를 다시 팔로우하면 어떻게 되나요?
      en: What happens if we follow someone we're already following?
    type: good
    why:
      ko: 집합을 사용하므로 중복 팔로우는 자동으로 무시되고 안전하게 처리됩니다.
      en: Using a set for followers automatically handles duplicate follows without issues.
  - q:
      ko: 모든 트윗 ID가 고유한가요?
      en: Are all tweet IDs guaranteed to be unique?
    type: good
    why:
      ko: 제약 조건에서 모든 트윗이 고유한 ID를 가지므로 트윗을 직접 식별할 수 있습니다.
      en: Constraints guarantee unique tweet IDs, so no collision handling is needed.
  - q:
      ko: 오래된 트윗을 자동으로 삭제해야 하나요?
      en: Should we automatically delete old tweets?
    type: distractor
    why:
      ko: 문제는 저장된 모든 트윗을 보존해야 한다고 하며, 단지 피드에서만 10개로 제한합니다.
      en: The problem requires storing all tweets; we only limit what appears in the feed, not what we store.
  - q:
      ko: 데이터를 파일에 저장해야 하나요?
      en: Do we need to persist data to disk?
    type: distractor
    why:
      ko: 인메모리 구현으로 충분하며, 추가 영속성 요구사항이 명시되지 않았습니다.
      en: In-memory storage is sufficient for this design problem without explicit persistence requirements.
  - q:
      ko: 입력값 검증이 필요한가요?
      en: Do we need to validate input parameters?
    type: distractor
    why:
      ko: LeetCode 스타일의 문제는 입력이 항상 유효하다고 가정하므로 방어적 검증은 불필요합니다.
      en: LeetCode problems assume valid input per constraints, so defensive validation is unnecessary.
approach:
  items:
  - name:
      ko: 해시맵 + 최소 힙을 이용한 병합 정렬
      en: Hash map + Min Heap for merging feeds
    complexity: O(N log 10) per getNewsFeed where N = followee count; O(1) for others
    type: good
    why:
      ko: 각 팔로우 대상의 최신 트윗들을 최소 힙에서 효율적으로 병합하여 정렬 상태를 유지합니다.
      en: Maintains a min-heap of latest tweets from each followee, efficiently extracting the top 10 in sorted order.
  - name:
      ko: 팔로우 관계 해시맵 (집합 기반)
      en: Hash map for follow relationships using sets
    complexity: O(1) for follow/unfollow operations
    type: good
    why:
      ko: 집합을 사용하면 팔로우 관계를 O(1)에 추가/삭제 가능하고 중복을 자동 처리합니다.
      en: Set-based storage enables O(1) follow/unfollow and automatically prevents duplicate relationships.
  - name:
      ko: 전체 트윗 수집 후 정렬 (브루트 포스)
      en: 'Brute force: collect all tweets and sort'
    complexity: O(T log T) where T = total tweets from all followees
    type: distractor
    why:
      ko: 모든 팔로우 대상의 모든 트윗을 모아서 정렬하면 불필요하게 느리며, 특히 팔로우 수가 많을 때 비효율적입니다.
      en: Collecting and sorting all tweets is inefficient, especially when users follow many people with many tweets.
  - name:
      ko: 중앙 집중식 타임라인 데이터베이스
      en: Centralized timeline database with indexing
    complexity: Database-dependent implementation
    type: distractor
    why:
      ko: 실제 트위터 백엔드에는 필요하지만, 인터뷰 문제의 범위를 벗어나고 과도한 설계입니다.
      en: Appropriate for production but over-engineered for an interview problem with in-memory constraints.
  - name:
      ko: 팔로우 그래프를 통한 BFS 탐색
      en: BFS traversal on follow graph
    complexity: O(U) where U = all users
    type: distractor
    why:
      ko: 팔로우 관계를 그래프로 탐색하면 불필요한 연산을 추가하며, 직접 팔로우만 필요합니다.
      en: BFS adds unnecessary traversal overhead; we only need direct followees, not graph exploration.
logic:
  format: slot
  slots:
  - label:
      ko: 타임스탬프 카운터 초기화
      en: Initialize timestamp counter
    indent: 0
    options:
    - code: self.count = 0
      type: good
      why:
        ko: 각 트윗에 순서 번호를 부여하여 시간 순서를 추적합니다.
        en: Assigns each tweet an order number to track chronological sequence.
    - code: self.timestamp = 1
      type: distractor
      why:
        ko: 증가 방식으로는 최신 트윗이 더 큰 값을 가져 최소 힙이 오래된 것을 먼저 반환합니다.
        en: Incrementing makes newer tweets have larger values, causing min-heap to return older tweets first.
    - code: self.time = {}
      type: distractor
      why:
        ko: 카운터를 딕셔너리로 만들면 전체 트윗의 순서를 비교하기 어렵습니다.
        en: Using a dict instead of a scalar makes comparing tweet order across users difficult.
  - label:
      ko: 카운터 감소로 최신순 정렬 보장
      en: Decrement counter to ensure reverse chronological order
    indent: 0
    options:
    - code: self.count -= 1
      type: good
      why:
        ko: 각 트윗 후 카운터를 감소시키므로 최신 트윗이 가장 작은 값을 가지며, 최소 힙이 최신부터 반환합니다.
        en: Decrementing ensures newer tweets have smaller values, enabling min-heap to return most recent first.
    - code: self.count += 1
      type: distractor
      why:
        ko: 증가시키면 최신 트윗이 더 큰 값을 가져 최소 힙에서 오래된 트윗이 먼저 추출됩니다.
        en: Incrementing causes the min-heap to extract older tweets first instead of newer ones.
    - code: '# No counter update'
      type: distractor
      why:
        ko: 카운터를 변경하지 않으면 모든 트윗의 타임스탬프가 같아 순서를 구분할 수 없습니다.
        en: Without updating the counter, all tweets have identical timestamps and relative order is lost.
  - label:
      ko: 사용자를 자신의 팔로우 목록에 추가
      en: Add user to their own followees
    indent: 0
    options:
    - code: self.followMap[userId].add(userId)
      type: good
      why:
        ko: 사용자 자신을 팔로우 목록에 포함시켜 자신의 트윗도 뉴스 피드에 나타나도록 합니다.
        en: Including the user in their own followees ensures their tweets appear in their news feed.
    - code: '# Don''t add user to followees'
      type: distractor
      why:
        ko: 사용자를 제외하면 자신의 트윗이 피드에 나타나지 않으므로 요구사항을 위반합니다.
        en: Excluding the user causes their own tweets to be missing from the feed, violating requirements.
    - code: 'if userId not in self.followMap[userId]: self.followMap[userId].add(userId)'
      type: distractor
      why:
        ko: 불필요한 조건 검사로 복잡성을 추가합니다. 집합은 자동으로 중복을 처리합니다.
        en: Unnecessary conditional check adds complexity; sets automatically handle duplicate additions.
  - label:
      ko: 모든 팔로우 대상의 최신 트윗을 힙에 추가
      en: Initialize heap with latest tweet from each followee
    indent: 1
    options:
    - code: heapq.heappush(minHeap, [count, tweetId, followeeId, index - 1])
      type: good
      why:
        ko: 각 팔로우 대상의 가장 최신 트윗을 힙에 넣어 병합 정렬의 초기 후보로 만듭니다.
        en: Each followee's most recent tweet enters the heap as the initial merge candidate.
    - code: heapq.heappush(minHeap, [tweetId, followeeId])
      type: distractor
      why:
        ko: 타임스탬프(count)를 제외하면 트윗 간 시간 순서를 올바르게 비교할 수 없습니다.
        en: Omitting the timestamp loses the ability to compare tweets by recency across users.
    - code: minHeap.append([count, tweetId, followeeId, index - 1])
      type: distractor
      why:
        ko: heappush 대신 append를 사용하면 힙 불변식이 깨져 정렬이 보장되지 않습니다.
        en: Using append instead of heappush breaks the heap property, losing sorted order guarantee.
  - label:
      ko: 최소 힙에서 가장 최신 트윗 추출
      en: Extract most recent tweet from min-heap
    indent: 1
    options:
    - code: count, tweetId, followeeId, index = heapq.heappop(minHeap)
      type: good
      why:
        ko: 최소 힙에서 팝하면 모든 팔로우 대상 중 가장 작은 타임스탬프(가장 최신)의 트윗을 얻습니다.
        en: Popping the min-heap returns the tweet with the smallest timestamp (most recent) among all followees.
    - code: count, tweetId, followeeId, index = minHeap[0]
      type: distractor
      why:
        ko: 힙에서 팝하지 않으면 같은 트윗이 반복되고 다른 사용자의 트윗을 볼 수 없습니다.
        en: Without popping, the same tweet repeats forever and other users' tweets never appear.
    - code: heapq.heapreplace(minHeap, [newCount, newTweetId, followeeId, newIndex])
      type: distractor
      why:
        ko: 현재 트윗을 추출하지 않고 즉시 다음 트윗으로 교체하므로 순서 불일치가 발생합니다.
        en: Replacing without popping skips the current tweet, resulting in wrong feed order.
  - label:
      ko: 같은 사용자의 다음 오래된 트윗을 힙에 추가
      en: Push next older tweet from same user to heap
    indent: 2
    options:
    - code: heapq.heappush(minHeap, [count, tweetId, followeeId, index - 1])
      type: good
      why:
        ko: 현재 트윗을 뺀 후 같은 사용자의 다음 트윗을 힙에 넣어 올바른 시간순 처리를 보장합니다.
        en: After popping a user's tweet, pushing their next older tweet maintains correct chronological order.
    - code: heapq.heappush(minHeap, [count, tweetId, followeeId, index])
      type: distractor
      why:
        ko: 인덱스를 감소시키지 않으면 같은 트윗을 반복 추가하여 무한 루프가 발생합니다.
        en: Not decrementing the index causes the same tweet to be pushed repeatedly, creating an infinite loop.
    - code: 'if index > 0: heapq.heappush(minHeap, [count, tweetId, followeeId, index - 1])'
      type: distractor
      why:
        ko: index > 0으로 검사하면 마지막 트윗(index=0)이 힙에 추가되지 않습니다.
        en: Using > instead of >= leaves the last tweet at index 0 unpushed.
trace:
  code:
  - 'class Twitter:'
  - '    def __init__(self):'
  - '        self.count = 0'
  - '        self.tweetMap = defaultdict(list)  # userId -> list of [count, tweetIds]'
  - '        self.followMap = defaultdict(set)  # userId -> set of followeeId'
  - ''
  - '    def postTweet(self, userId: int, tweetId: int) -> None:'
  - '        self.tweetMap[userId].append([self.count, tweetId])'
  - '        self.count -= 1'
  - ''
  - '    def getNewsFeed(self, userId: int) -> List[int]:'
  - '        res = []'
  - '        minHeap = []'
  - ''
  - '        self.followMap[userId].add(userId)'
  - '        for followeeId in self.followMap[userId]:'
  - '            if followeeId in self.tweetMap:'
  - '                index = len(self.tweetMap[followeeId]) - 1'
  - '                count, tweetId = self.tweetMap[followeeId][index]'
  - '                heapq.heappush(minHeap, [count, tweetId, followeeId, index - 1])'
  - ''
  - '        while minHeap and len(res) < 10:'
  - '            count, tweetId, followeeId, index = heapq.heappop(minHeap)'
  - '            res.append(tweetId)'
  - '            if index >= 0:'
  - '                count, tweetId = self.tweetMap[followeeId][index]'
  - '                heapq.heappush(minHeap, [count, tweetId, followeeId, index - 1])'
  - '        return res'
  - ''
  - '    def follow(self, followerId: int, followeeId: int) -> None:'
  - '        self.followMap[followerId].add(followeeId)'
  - ''
  - '    def unfollow(self, followerId: int, followeeId: int) -> None:'
  - '        if followeeId in self.followMap[followerId]:'
  - '            self.followMap[followerId].remove(followeeId)'
  cases:
  - input: '["Twitter","postTweet","getNewsFeed","follow","postTweet","getNewsFeed","unfollow","getNewsFeed"]

      [[],[1,5],[1],[1,2],[2,6],[1],[1,2],[1]]'
    expected: '[null, null, [5], null, null, [6, 5], null, [5]]'
  worked_example:
    input: '["Twitter","postTweet","getNewsFeed","follow","postTweet","getNewsFeed","unfollow","getNewsFeed"]

      [[],[1,5],[1],[1,2],[2,6],[1],[1,2],[1]]'
    steps:
    - ko: 'Twitter() 초기화: count=0, tweetMap={}, followMap={}'
      en: 'Twitter() initialize: count=0, tweetMap={}, followMap={}'
    - ko: 'postTweet(1,5): 사용자1이 트윗5 게시 (count=0); count를 -1로 감소'
      en: 'postTweet(1,5): User 1 posts tweet 5 with count=0; decrement to count=-1'
    - ko: 'getNewsFeed(1): 사용자1 자신만 팔로우; 트윗5 반환'
      en: 'getNewsFeed(1): Only user 1 in followees; return tweet 5'
    - ko: 'follow(1,2): 사용자1이 사용자2를 팔로우; postTweet(2,6): 사용자2가 트윗6 게시 (count=-1)'
      en: 'follow(1,2): User 1 follows user 2; postTweet(2,6): User 2 posts tweet 6 with count=-1'
    - ko: 'getNewsFeed(1): 힙에 트윗5 (count=0), 트윗6 (count=-1); -1이 작으므로 트윗6 먼저, 그 다음 트윗5'
      en: 'getNewsFeed(1): Heap has tweet 5 (count=0) and tweet 6 (count=-1); -1 is smaller, so pop tweet 6 first, then tweet 5'
    - ko: 'unfollow(1,2): 사용자1이 사용자2를 언팔로우; getNewsFeed(1): 사용자1 자신만 남음; 트윗5 반환'
      en: 'unfollow(1,2): User 1 unfollows user 2; getNewsFeed(1): Only user 1 remains; return tweet 5'
    answer: '[null, null, [5], null, null, [6, 5], null, [5]]'
solution:
  code: "class Twitter:\n    def __init__(self):\n        self.count = 0\n        self.tweetMap = defaultdict(list)  # userId -> list of [count, tweetIds]\n        self.followMap = defaultdict(set)  # userId -> set of followeeId\n\n    def postTweet(self, userId: int, tweetId: int) -> None:\n        self.tweetMap[userId].append([self.count, tweetId])\n        self.count -= 1\n\n    def getNewsFeed(self, userId: int) -> List[int]:\n        res = []\n        minHeap = []\n\n        self.followMap[userId].add(userId)\n        for followeeId in self.followMap[userId]:\n            if followeeId in self.tweetMap:\n                index = len(self.tweetMap[followeeId]) - 1\n                count, tweetId = self.tweetMap[followeeId][index]\n                heapq.heappush(minHeap, [count, tweetId, followeeId, index - 1])\n\n        while minHeap and len(res) < 10:\n            count, tweetId, followeeId, index = heapq.heappop(minHeap)\n            res.append(tweetId)\n            if index >= 0:\n\
    \                count, tweetId = self.tweetMap[followeeId][index]\n                heapq.heappush(minHeap, [count, tweetId, followeeId, index - 1])\n        return res\n\n    def follow(self, followerId: int, followeeId: int) -> None:\n        self.followMap[followerId].add(followeeId)\n\n    def unfollow(self, followerId: int, followeeId: int) -> None:\n        if followeeId in self.followMap[followerId]:\n            self.followMap[followerId].remove(followeeId)\n"
  complexity:
    time: O(N log 10) per getNewsFeed where N = number of followees (heap size capped at 10); O(1) for other operations
    space: O(U + T) where U = number of users and T = total number of tweets posted
  followup:
  - ko: 만약 사용자가 100만 명이고 각자 1000명씩 팔로우한다면, getNewsFeed의 성능을 어떻게 최적화할 수 있을까요?
    en: How would you optimize getNewsFeed if you have 1 million users each following 1000 people?
  - ko: 뉴스 피드 페이지네이션을 구현하려면 어떻게 해야 할까요? (첫 10개, 다음 10개, ...)
    en: How would you implement pagination for the news feed (first 10 tweets, next 10, etc.)?
  - ko: 특정 사용자가 매우 자주 트윗을 하면서 다른 사용자가 타임아웃 없이 피드를 볼 수 있도록 하려면 어떻게 할까요?
    en: How would you handle a user posting extremely frequently without causing timeout for other users viewing their feed?
```