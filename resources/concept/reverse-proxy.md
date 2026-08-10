---
type: concept
id: reverse-proxy
title: 리버스 프록시 (Nginx Proxy Manager)
aliases:
  - 리버스 프록시
  - reverse proxy
  - Nginx
  - Nginx Proxy Manager
up:
  - 2025-01-13-Day10
tags:
  - 인프라
  - web
  - 배포
---

# 리버스 프록시 (Nginx Proxy Manager)

**바깥의 요청을 먼저 받아 안쪽 서버로 넘겨 주는 서버.** 도메인·인증서·포트가 전부 여기서 정리되고, 애플리케이션은 **안쪽 포트만 신경 쓴다.**

## 정의

```
브라우저 ──80/443──▶ [Nginx Proxy Manager] ──▶ 8081 ──▶ 애플리케이션
                       도메인 매칭
                       SSL 종료
```

컨테이너 하나로 띄운다.

```bash
docker run -d --name npm_1 --restart unless-stopped \
  -p 80:80 -p 443:443 -p 81:81 \
  -e TZ=Asia/Seoul \
  -v /dockerProjects/npm_1/volumes/data:/data \
  -v /dockerProjects/npm_1/volumes/etc/letsencrypt:/etc/letsencrypt \
  jc21/nginx-proxy-manager:latest
```

- **80·443** — HTTP·HTTPS 를 받는 자리
- **81** — 관리 화면
- **볼륨 둘** — 설정과 **SSL 인증서**를 컨테이너 밖에 남긴다 → [[container]]

`--restart unless-stopped` 는 **손으로 멈춘 것이 아니면 다시 띄운다**는 정책이다.

### 웹 서버가 하는 일

필기가 정리한 셋이 그대로 이 층의 역할이다.

- **정적 콘텐츠 제공** — HTML·CSS·이미지 → [[static-and-dynamic-content]]
- **로드 밸런싱** — 여러 서버로 트래픽 분배 → [[distributed-processing]]
- **HTTP 요청 처리** — 받아서 응답을 돌려준다 → [[http-message]]

## 왜 중요한가

**애플리케이션이 도메인과 인증서를 몰라도 된다.** HTTPS 를 여기서 끝내면(SSL 종료) 안쪽은 평범한 HTTP 로 돌고, **인증서 갱신도 한 곳에서** 한다.

**그리고 포트를 감춘다.** 사용자는 `example.com` 만 알고, 안쪽이 8081 이든 8082 든 상관없다 — **[[zero-downtime-deployment]] 의 포트 전환이 밖에서 안 보이는 이유**가 이것이다 → [[port-number]]

**여러 서비스를 한 서버에 올릴 수 있다.** 도메인이나 경로로 갈라 각각 다른 컨테이너로 보내면 **80 포트 하나로 여럿을 서비스**한다 → [[url]]

## 경계와 오해

- **리버스 프록시 ≠ 프록시** — 보통의(정방향) 프록시는 **클라이언트를 대신해** 나가고, 리버스 프록시는 **서버를 대신해** 받는다. 방향이 반대다 → [[proxy-pattern]]
- **SSL 을 여기서 끝내면 안쪽은 평문이다** — 같은 서버 안이라 대개 괜찮지만, **네트워크를 건너간다면 그 구간은 보호되지 않는다**
- **관리 화면(81 포트)을 열어 두면 안 된다** — 프록시 설정 전체를 바꿀 수 있는 자리다. 기본 계정을 바꾸고 접근을 막는 것이 첫 일이다 → [[spring-security]]
- **볼륨을 안 붙이면 인증서가 사라진다** — 컨테이너를 다시 만들면 안의 파일은 없어지므로, `letsencrypt` 디렉토리를 밖에 두는 것이 필수다. **컨테이너는 사라지는 것을 전제한다**는 원칙이 여기서 실물로 나온다 → [[container]]
- **프록시가 죽으면 전부 멈춘다** — 모든 트래픽이 지나는 지점이라 **단일 실패 지점**이다. `--restart` 정책이 최소한의 대비다
- **Nginx Proxy Manager 는 Nginx 자체가 아니다** — 설정 파일을 손으로 쓰는 대신 화면으로 관리하게 해 주는 도구다. **감춰진 것이 Nginx 설정**이라, 세밀한 조정은 결국 그쪽을 알아야 한다

## 함께 보는 개념

- [[web-server]] — 이 층이 맡는 역할
- [[zero-downtime-deployment]] — 안쪽 포트가 바뀌어도 밖이 그대로인 이유
- [[container]] — 이것도 컨테이너로 띄운다
- [[port-number]] — 감추고 매핑하는 대상
- [[proxy-pattern]] — 방향이 반대인 같은 이름
- [[static-and-dynamic-content]] — 정적 파일을 여기서 내주는 선택

## 출처

- [[2025-01-13-Day10]] — 「Nginx 설치 및 설정」 절이 `docker run` 한 줄을 실은 뒤 **옵션 하나하나를 여섯 갈래로 풀어 적었다** — `-d`·`--name`·`--restart unless-stopped`(「수동으로 중지한 경우에는 재시작하지 않음」까지)·포트 매핑 셋(80·443·81 각각의 용도)·`-e TZ`·볼륨 둘(설정 데이터와 **SSL 인증서**). 이 주석 묶음이 `docker run` 을 처음 읽을 때 필요한 것을 다 담고 있다. 이어지는 「nginx proxy manager 관리콘솔에 접속」이 **웹 서버의 역할 셋**(정적 콘텐츠 제공·로드 밸런싱·HTTP 요청 처리)을 정의로 적어, 이 컨테이너가 무엇을 하는 자리인지 자리매김한다 → [[web-server]] · [[container]]
