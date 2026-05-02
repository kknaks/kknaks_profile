---
type: project
id: P-01
title:
  ko: "Homelab Console"
  en: "Homelab Console"
summary:
  ko: "홈서버 메트릭 + 컨테이너 상태를 실시간으로 보여주는 대시보드."
  en: "Realtime dashboard for homelab metrics and container status."
category: web
status: wip
date: "2026.04"
stack:
  - Next.js
  - FastAPI
  - WebSocket
  - Prometheus
links:
  repo: "github.com/kknaks/homelab-console"
  live: "https://homelab.kknaks.dev"
---

# Homelab Console

(mock 본문 — 추후 실제 포스트모템으로 교체)

## 왜 만들었나

홈서버에서 컨테이너 5-6개를 띄우다 보니 `docker ps` 매번 치는 게 귀찮아졌습니다.
Grafana는 무겁고, 단순 status + CPU/Memory 그래프 정도면 충분해서 직접 만들었습니다.

## 어떻게 풀었나

- FastAPI가 호스트의 `/proc`, Docker socket을 읽어 메트릭 노출
- WebSocket으로 1초 주기 push (REST polling 대비 부담 줄임)
- Next.js 프론트는 단일 페이지 — 카드 그리드 + 미니 차트

## 배운 점

- WebSocket의 connection lifecycle 관리 (reconnect, heartbeat)
- Docker socket 권한 모델 (root 회피 — `docker.sock` group 활용)
- Prometheus exporter 컨벤션
