---
type: concept
id: kubernetes-workload
title: Deployment · ReplicaSet · Pod
aliases:
  - Deployment
  - ReplicaSet
  - 롤링 업데이트
  - 레이블 셀렉터
  - resource requests
  - Insufficient cpu
  - Pending
  - WaitForFirstConsumer
up:
  - 2025-01-15-Day12
  - 2026-10-28-interpret-pwa-v2
tags:
  - 인프라
  - 배포
  - 쿠버네티스
---

# Deployment · ReplicaSet · Pod

**「몇 개가 떠 있어야 하는가」와 「어떤 버전이어야 하는가」를 나눠 맡은 세 층.** 위가 아래의 수명을 관리한다.

## 정의

```
Deployment  — 어떤 버전을 어떻게 바꿔 갈 것인가 (롤링 업데이트·롤백·이력)
    ↓
ReplicaSet  — 몇 개가 떠 있어야 하는가 (개수 유지)
    ↓
Pod         — 실제로 도는 것
```

### ReplicaSet — 개수를 지킨다

```yaml
kind: ReplicaSet
spec:
  replicas: 3                 # 원하는 복제본 수
  selector:
    matchLabels: { app: example }   # 이 라벨을 가진 파드를 내 것으로 본다
  template: ...                     # 없으면 이 모양으로 만든다
```

- 파드가 죽으면 **새로 만든다**
- 노드가 죽으면 **다른 노드에 다시 만든다**
- 수를 바꾸면 **늘리거나 줄인다**

**레이블 셀렉터로 관리 대상을 고른다**는 것이 핵심이다 — 이름이 아니라 **조건으로 묶는다** → [[kubernetes]]

### Deployment — 버전을 바꾼다

```yaml
kind: Deployment
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1           # 목표보다 최대 몇 개 더 띄울 수 있나
      maxUnavailable: 1     # 최대 몇 개까지 없어도 되나
```

업데이트가 도는 모양이 이렇다.

```
Deployment 수정 → 새 ReplicaSet 생성 → 새 Pod 생성 → 이전 Pod 제거
                                                    → 이전 ReplicaSet 은 남긴다(롤백용)
```

**이전 ReplicaSet 을 지우지 않는 것**이 롤백을 가능하게 한다.

### Pod 가 노드에 앉는 기준 — requests 합

스케줄러는 노드의 **실제 사용량이 아니라 그 노드에 앉은 Pod 들의 `requests` 합**으로 자리를 잰다. 합이 노드 용량에 닿으면 실제로 한가해도 새 Pod 는 `Pending`(이벤트 「Insufficient cpu」)이다.

- **저장 공간이 Pod 를 노드에 묶는다** — `local-path` 같은 노드 로컬 PV 는 한 노드의 디스크에만 생긴다. 저장이 필요한 앱이 전부 그 노드로 몰리고(nodeSelector), 그 노드의 requests 가 먼저 찬다
- **PVC 도 같이 Pending** — `WaitForFirstConsumer` 는 Pod 가 노드에 잡힌 뒤에야 PV 를 만든다. Pod 가 못 앉으면 PVC 도 Bound 가 안 된다. 원인은 PVC 가 아니라 Pod 스케줄링이다
- **롤링 업데이트라 끊김은 없다** — 새 Pod 가 못 떠도 옛 ReplicaSet 의 Pod 가 계속 응답한다. 배포는 멈춰 있고 서비스는 옛 버전이다
- **푸는 길** — 우리 Pod 의 request 를 실제 필요만큼 낮춘다(통키 back 100m → 50m · limit 은 그대로). 다른 앱의 requests 를 줄이거나 노드 자원을 늘리는 것은 그 노드를 쓰는 다른 주인의 판단이다

## 왜 중요한가

**무중단 배포가 기능으로 들어와 있다.** 앞 회차에서 두 포트를 번갈아 쓰고 `socat` 을 죽였다 살리는 스크립트를 손으로 썼는데, 여기서는 **`strategy` 두 줄**이 그 일을 한다 — `maxSurge`/`maxUnavailable` 이 「한 번에 몇 개씩 갈아 낄지」를 정한다 → [[zero-downtime-deployment]]

**그리고 원하는 상태만 적으면 된다.** 「세 개」라고 적어 두면 하나가 죽어도 다시 세 개가 된다 — **복구를 사람이 하지 않는다** → [[infrastructure-as-code]]

**층이 나뉜 이유도 분명하다.** 개수 유지(ReplicaSet)와 버전 전환(Deployment)은 **다른 이유로 바뀌는 관심사**라, 붙여 두면 하나를 고칠 때 다른 하나가 흔들린다 → [[cohesion]]

## 경계와 오해

- **웹 애플리케이션 「배치」와 이름만 같다** — 여기서는 **파드를 몇 개 굴리고 어떻게 교체할지** 정하는 오브젝트이고, 그쪽은 war 를 컨테이너에 올리는 일이다 → [[web-application-deployment]]
- **Pod 를 직접 만들면 안 된다** — 죽어도 아무도 다시 만들어 주지 않는다. 필기의 정리대로 **「직접 Pod 생성 < ReplicaSet < Deployment」**이고, 실무는 거의 언제나 Deployment 다
- **ReplicaSet 을 직접 만질 일도 드물다** — Deployment 가 만들어 주므로, **손으로 만든 ReplicaSet 은 롤백 이력을 못 갖는다**
- **셀렉터와 템플릿의 라벨이 어긋나면 무한히 만든다** — 만든 파드가 셀렉터에 안 걸리면 「아직 부족하다」로 보고 계속 만든다. **조건으로 묶는 방식의 대가**다
- **`maxUnavailable: 1` 은 그동안 용량이 준다는 뜻이다** — 세 개 중 하나가 빠진 상태로 트래픽을 받으므로, **여유가 없으면 배포 중에 느려진다** → [[little-law]]
- **롤백은 이미지 버전으로 돌아가는 것이지 데이터까지 되돌리는 것이 아니다** — 스키마를 바꾼 배포는 롤백해도 DB 가 옛 상태가 아니다 → [[db-normalization]] · [[transaction]]
- **requests ≠ 사용량** — 「노드가 꽉 찼다」 는 예약(requests 합 98%)이 꽉 찬 것일 수 있다. 메트릭 서버가 없으면 사용량은 아예 안 보인다. `kubectl describe node` 의 `Allocated resources` 가 스케줄러가 보는 숫자다
- **차트 검증은 스케줄링을 못 본다** — `helm lint` · `template` · kubeconform 이 다 통과해도 「그 노드에 자리가 있나」 는 클러스터에서만 드러난다. 노드에 묶이는 볼륨을 새로 붙이는 배포는 그 노드의 `Allocated resources` 를 먼저 본다
- **`replicas: 3` 이 「세 배 빠름」은 아니다** — 상태를 공유하지 않는 애플리케이션이어야 늘린 만큼 처리한다. 세션·파일을 서버에 두면 **늘리는 순간 깨진다** → [[jwt]] · [[object-storage]]

## 함께 보는 개념

- [[kubernetes]] — 이 리소스들이 사는 곳
- [[zero-downtime-deployment]] — 손으로 만들던 같은 목적
- [[container]] — Pod 안에서 도는 것
- [[ci-cd]] — 새 이미지를 밀어 넣는 쪽
- [[infrastructure-as-code]] — 선언형이라는 같은 성격
- [[distributed-processing]] — 여러 복제본이 만드는 문제

## 출처

- [[2025-01-15-Day12]] — 「Deployment, ReplicaSet, Pod」 절이 **셋의 계층과 사용 순위를 함께** 정리했다. Deployment 의 주요 기능 다섯(롤링 업데이트·롤백·배포 이력·스케일링·일시 중지/재개)과 ReplicaSet 의 넷(개수 유지·파드 장애 시 재생성·노드 장애 시 다른 노드에 재생성·수평 확장)이 각각 나열돼 **무엇이 어느 층의 책임인지**가 갈린다. YAML 두 벌이 `replicas`·`selector.matchLabels`·`template` 의 대응을 보이고, Deployment 쪽에는 `strategy.rollingUpdate` 의 `maxSurge`·`maxUnavailable` 이 주석과 함께 있다. 「세 리소스의 관계」 절의 **업데이트 프로세스 다이어그램**이 특히 값지다 — 새 ReplicaSet 생성 → 새 Pod → 이전 Pod 제거 → **이전 ReplicaSet 보존(롤백 가능)** 까지가 한 흐름으로 그려져 있다. 「직접 Pod 생성 < ReplicaSet 사용 < Deployment 사용」이라는 한 줄도 실전 지침으로 남았다
- [[2026-10-28-interpret-pwa-v2]] §2 — 통역 기록용 local-path PVC 로 back 을 한 노드에 고정하자 새 Pod 가 「Insufficient cpu」 Pending(requests 합 98% · 사용량 아님) · PVC 는 WaitForFirstConsumer 로 같이 Pending · 롤링이라 옛 Pod 가 응답해 무중단 · back request 100m → 50m 로 해소(`wp17-infra-report.md` · infra #36)
