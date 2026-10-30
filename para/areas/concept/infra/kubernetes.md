---
type: concept
id: kubernetes
title: 쿠버네티스 (Kubernetes)
aliases:
  - Kubernetes
  - 쿠버네티스
  - k8s
  - 파드
  - Pod
  - 클러스터
  - kubeadm
  - local-path
  - nodeSelector
  - PVC Pending
  - Secret 파일 마운트
  - /run/secrets
  - automountServiceAccountToken
up:
  - 2025-01-15-Day12
  - 2025-01-17-Day14
  - 2026-10-14-sts-prototype
  - 2026-10-22-myeongdong-poc-v2
  - 2026-10-30-internal-chat
tags:
  - 인프라
  - 배포
  - 오케스트레이션
---

# 쿠버네티스 (Kubernetes)

**컨테이너를 여러 서버에 걸쳐 자동으로 배포·확장·관리하는 플랫폼.** 컨테이너 하나를 띄우는 것이 [[container]] 였다면, **몇 개를 어디에 띄울지 대신 정해 주는 것**이 이것이다.

## 정의

### 클러스터 — 서버 여럿을 하나로

| 노드 | 하는 일 | 구성요소 |
|---|---|---|
| **마스터 노드** | 클러스터를 **관리·결정** | API 서버 · 스케줄러 · 컨트롤러 매니저 · etcd |
| **워커 노드** | 컨테이너를 **실제로 실행** | kubelet · kube-proxy · 컨테이너 런타임 |

- **API 서버** — 모든 요청이 지나는 입구
- **스케줄러** — 새 파드를 **어느 노드에 놓을지** 결정
- **컨트롤러 매니저** — 「있어야 할 상태」와 「지금 상태」를 맞춘다
- **etcd** — 클러스터의 상태를 저장하는 DB
- **kubelet** — 마스터의 지시대로 컨테이너를 띄운다
- **kube-proxy** — 네트워크 규칙과 포워딩

**결정하는 쪽과 실행하는 쪽이 갈려 있다**는 것이 이 구조의 뼈대다.

### 파드 — 배포의 최소 단위

**컨테이너가 아니라 파드가 단위**다. 파드 하나에 컨테이너가 여럿 들어갈 수 있고, 그것들은 **네트워크 네임스페이스·IP·포트 공간·호스트 이름을 공유**한다 — 같은 기계 안에 있는 것처럼 서로 `localhost` 로 부른다 → [[process]] · [[port-number]]

### 서비스 — 파드 집합에 붙는 이름

파드는 죽고 다시 태어나며 **IP 가 바뀐다.** 서비스는 **레이블 셀렉터로 파드를 고르고** 그 앞에 고정된 접점을 둔다 → [[reverse-proxy]] 가 하던 일과 같은 방향이다.

### 클러스터 세우기 — kubeadm

```
kubeadm init (마스터)        사전 검사 → 인증서 생성 → 컨트롤 플레인을 static pod 로 → etcd 초기화
        ↓
컨트롤 플레인 시작            API 서버 → 컨트롤러 매니저 → 스케줄러 순
        ↓
kubeadm join (워커)          조인 토큰으로 마스터에 연결
```

## 왜 중요한가

**「서버 한 대에 컨테이너를 띄운다」에서 「어딘가에 몇 개 떠 있게 한다」로 바뀐다.** 앞 회차의 무중단 배포는 **한 대 안에서 포트를 바꾸는** 방식이었는데, 여기서는 **원하는 상태를 선언하면 클러스터가 맞춘다** → [[zero-downtime-deployment]] · [[infrastructure-as-code]]

**그래서 장애 대응이 자동이 된다.** 파드가 죽으면 컨트롤러가 다시 만들고, 노드가 죽으면 다른 노드에 다시 만든다 — **사람이 알아채기 전에** → [[distributed-processing]]

## 경계와 오해

- **선언형이라는 것이 핵심이다** — 「띄워라」가 아니라 **「세 개가 떠 있어야 한다」**를 적고, 컨트롤러가 계속 그 상태로 맞춘다. 테라폼의 선언형과 같은 발상이 **실행 중에도 계속** 돌아가는 형태다 → [[infrastructure-as-code]]
- **파드 ≠ 컨테이너** — 대개 1:1 로 쓰지만 개념이 다르다. **파드가 죽고 살아나는 단위**이고, 그 안의 컨테이너들은 함께 움직인다
- **파드의 IP 는 믿을 수 없다** — 재생성될 때마다 바뀌므로 **파드끼리 IP 로 부르면 안 된다.** 서비스 이름으로 부르는 이유다 → [[domain-name-system]]
- **쿠버네티스가 컨테이너를 대신하지 않는다** — 이미지를 만들고 레지스트리에 올리는 일은 그대로다. **그 위에서 배치를 맡을 뿐**이다 → [[ci-cd]]
- **작은 서비스에는 과하다** — 마스터 노드·etcd·네트워크 설정까지 유지해야 하므로, **운영 비용이 애플리케이션보다 클 수 있다.** 서버 한두 대면 컨테이너만으로 충분하다
- **볼륨이 노드에 묶이면 파드도 묶인다** — local-path 프로비저너는 설정된 노드(nodePathMap)에만 볼륨을 만든다. cc-prototype 은 PVC 를 쓰는 back 만 **Pending** 이었다 — 스케줄러가 다른 노드를 고르자 그 노드에 볼륨을 못 만든 것. `nodeSelector` 로 그 노드에 고정하고, 이미 다른 노드가 찍힌(`selected-node`) Pending PVC 는 지우고 다시 만든다(파괴적)
- **Secret 을 볼륨으로 꽂으면 키 하나가 파일 하나다** — 키에 `/` 를 못 쓰니 하위 폴더가 안 된다. `events/<id>.json` 은 `event-<id>.json` 처럼 평평하게 넣는다. 공개 레포의 앱이 실데이터를 읽어야 하면 이미지 · git 이 아니라 Secret 으로 들어간다 → [[externalized-configuration]]
- **Secret 을 꽂는 경로가 kubelet 의 경로와 겹치면 파드가 안 뜬다** — APNs 키(`.p8`)를 Secret 으로 `/run/secrets` 에 통째로 읽기 전용 마운트하자 back 이 CrashLoop(`mkdirat … read-only file system`) 했다. 컨테이너에서 `/var/run` 은 `/run` 이고, kubelet 은 서비스계정 토큰을 `/var/run/secrets/kubernetes.io/serviceaccount` 에 꽂는다 — 그 부모를 우리가 ro 로 덮어 하위 폴더를 못 만든 것. 앱 전용 경로(`/etc/apns`)로 옮기고, k8s API 를 안 쓰는 앱이라 `automountServiceAccountToken: false` 로 토큰 마운트 자체를 껐다. 「도커에서 흔히 쓰는 `/run/secrets`」 가 k8s 에서는 예약된 자리다
- **etcd 가 클러스터의 기억 전부다** — 상태가 거기 있으므로 **그것을 잃으면 클러스터를 잃는다** → [[database-schema]]
- **local-path PVC 크기는 한도가 아니다**(cc-prototype 내부 채팅) — local-path 는 quota 가 없어 1Gi PVC 도 1Gi 넘게 써지고, StorageClass 에 `allowVolumeExpansion` 이 없어 값을 키우면 API 서버가 거절해 ArgoCD sync 만 실패로 남는다. 실제 한도는 노드 디스크 — 값은 두고 주석으로 · [[2026-10-30-internal-chat]]

## 함께 보는 개념

- [[container]] — 클러스터가 실행하는 것
- [[kubernetes-workload]] — 파드를 몇 개 어떻게 유지할지 정하는 층
- [[microservice-architecture]] — 이 도구가 겨냥하는 배치
- [[distributed-processing]] — 여러 노드에 걸치는 문제
- [[infrastructure-as-code]] — 선언형이라는 같은 성격
- [[reverse-proxy]] — 서비스가 하는 일의 앞선 형태
- [[zero-downtime-deployment]] — 한 대 안에서 하던 같은 목적
- [[distributed-session]] — 파드가 여럿일 때 세션이 깨지는 문제
- [[ci-cd]] — 클러스터에 새 이미지를 밀어 넣는 쪽

## 출처

- [[2026-10-22-myeongdong-poc-v2]] §2 — APNs 키 Secret 을 `/run/secrets` 에 마운트해 SA 토큰 마운트가 막힘 → back CrashLoop → `/etc/apns` + SA 토큰 automount 끔(infra #23 · SPEC-004 §2.3 `APNS_KEY_PATH`)
- [[2026-10-14-sts-prototype]] §2 — cc-prototype 을 Helm + ArgoCD(수동 sync)로 Mac k8s 에 올리며 겪은 것: local-path 볼륨 노드 제약 → nodeSelector · 데이터는 평평한 키의 Secret(`deploy-infra-report.md` fix1)
- [[2025-01-17-Day14]] — 이틀 뒤. **클러스터에 실제로 애플리케이션을 올리면서 딸려 오는 것들**이 나온다 — 비공개 이미지를 받으려면 `kubectl create secret docker-registry` 로 레지스트리 자격을 클러스터에 등록해야 하고, 밖에서 들어오는 트래픽은 마스터 노드의 프록시가 **도메인:포트 → 서비스:포트** 로 넘긴다(HTTP 뿐 아니라 DB·Redis 포트도 stream 으로). 그리고 **파드가 라운드로빈으로 갈리기 때문에 세션이 깨진다**는 것이 이 환경의 첫 실전 문제로 나타난다 → [[distributed-session]]
- [[2025-01-15-Day12]] — 「kubernetes의 기본용어」 절이 **클러스터 → 마스터노드 → 워커노드 → 파드 → 서비스** 순으로 정의하며, 마스터·워커의 구성요소를 각각 넷·셋으로 나눠 한 줄씩 설명했다(API 서버·스케줄러·컨트롤러 매니저·etcd / kubelet·kube-proxy·컨테이너 런타임). **파드가 「동일한 네트워크 네임스페이스, IP 주소, 포트 공간, IPC 네임스페이스, 호스트 이름을 공유한다」**는 정의가 파드와 컨테이너의 차이를 정확히 짚는다. 「클러스터 생성과정」이 `kubeadm init` → 컨트롤 플레인 시작 → `kubeadm join` 세 걸음을 **각 단계에서 실제로 일어나는 일**과 함께 적었고, 특히 컨트롤 플레인이 **static pod 로 뜬다**는 것과 시작 순서(API 서버 먼저)까지 남겼다. 다만 「API 서버」와 「컨트롤러 매니저」의 설명이 같은 문장으로 반복된다 → [[kubernetes-workload]]
- [[2026-10-30-internal-chat]] §2 「업로드 한도는 앞단부터」 · `infra-report.md`
