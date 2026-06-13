---
type: baseline
id: BASE-001
title: "카톡 대화 로컬 자동 추출 (내보내기 없이)"
status: accepted
product: mykakao
source:
  type: idea
  ref: "사용자 구두 요청 2026-06-12"
links:
  baselines: []
  decisions:
    - "[[decision-001-extraction-approach]]"
  specs: []
  works: []
  releases: []
  related: []
created_at: 2026-06-12
updated_at: 2026-06-12
tags:
  - product/mykakao
  - doc/baseline
  - status/accepted
---

# 카톡 대화 로컬 자동 추출 (내보내기 없이)

macOS 카카오톡의 대화 메시지를 "대화 내용 내보내기" 기능을 쓰지 않고, 로컬에서 자동으로 추출한다.

> 아직 결정하지 않은 날것의 입력이다. 정리보다 보존이 우선이다.

## Raw

- 카톡 대화에서 내 일정들을 뽑아 업데이트하고 싶다.
- 여러 명이 있는 단톡방에 일정이 너무 많아 수작업으로 따라가기 어렵다.
- 카톡 앱 내장 "내보내기"는 쓰고 싶지 않다 (방마다 수동, 반복 불가). 자동으로 긁고 싶다.
- 본인 기기에서 본인만 쓴다. 외부 배포/공유 없음. 보안 걱정은 하지 않아도 됨.
- 최종 목표는 "추출 → 일정 파싱 → 캘린더 업데이트"지만, **이번 범위는 메시지 추출까지만**. 일정 파싱/캘린더 플로우는 다음에 따로 고민한다.

## Context

- 환경: macOS (Apple Silicon), 카카오톡 App Store 샌드박스 버전 v26.1.1.
- 메시지 DB는 컨테이너 안에 암호화되어 저장됨 (직접 열람 불가 상태에서 출발).

## Why It Matters

- 단톡방 다수에 흩어진 일정/약속을 사람이 따라가는 비용이 큼.
- 추출이 자동화되면 그 위에 일정 추출·캘린더 연동 같은 후속 플로우를 얹을 수 있다. 추출이 전체 파이프라인의 병목이자 진입점.

## Possible Direction

- 로컬 메시지 DB를 복호화해 SQL로 전체 대화방/히스토리를 한 번에 조회.
- 또는 화면 접근성(AX) 스크래핑 / 화면 OCR. (대량 히스토리엔 비효율)
- 결정은 [[decision-001-extraction-approach]]에서.
