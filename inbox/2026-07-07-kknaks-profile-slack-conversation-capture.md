---
type: idea
id: 2026-07-07-kknaks-profile-slack-conversation-capture
title: kknaks_profile에 슬랙 대화를 지식 입력 소스로 추가
created_at: '2026-07-07T08:46:04+09:00'
source: slack
slack_event_id: Ev0BFNEXHHD2
slack_thread_ts: '1783381533.263029'
tags:
- kknaks_profile
- slack
- 지식관리
- 캡처
- 워크플로우
---

# kknaks_profile에 슬랙 대화를 지식 입력 소스로 추가

## 원문

kknaks_profile에 슬랙 대화 넣자 지금 인박스만 넣고 잇는데?

## 정리된 아이디어

kknaks_profile의 지식 캡처 범위를 인박스 항목에서 슬랙 대화(채널·DM 포함)까지 확장하자는 제안. 현재는 인박스만 입력 소스로 사용되어 슬랙에서 오가는 대화의 인사이트가 프로필에 반영되지 않고 있다.

## 해결하려는 문제

슬랙 대화에서 생성되는 지식과 아이디어가 인박스 외의 경로로는 kknaks_profile에 유입되지 않아 지식 축적이 불완전하다.

## 기대 효과

슬랙 대화를 입력 소스로 추가하면 실시간 대화에서 발생하는 인사이트도 체계적으로 캡처되어 kknaks_profile의 지식 커버리지가 넓어진다.

## 열린 질문

- 어떤 채널 또는 DM 범위를 캡처 대상으로 할 것인가?
- 슬랙 대화 캡처 트리거를 앱 멘션, 특정 이모지 반응, 키워드 중 무엇으로 할 것인가?
- 슬랙 대화와 인박스 항목의 처리·분류 방식을 동일하게 가져갈 것인가, 별도 파이프라인으로 분리할 것인가?
