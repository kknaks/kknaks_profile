---
type: concept
id: ci-cd
title: CI/CD 파이프라인 (GitHub Actions)
aliases:
  - CI/CD
  - GitHub Actions
  - 파이프라인
  - 컨테이너 레지스트리
up:
  - 2025-01-13-Day10
  - 2025-01-17-Day14
tags:
  - 배포
  - 자동화
  - 인프라
---

# CI/CD 파이프라인 (GitHub Actions)

**푸시 한 번으로 빌드·이미지 생성·배포까지 이어지게 만드는 것.** 사람이 서버에 들어가 하던 절차를 **저장소에 적어 두고 이벤트가 실행한다.**

## 정의

이 회차가 만든 파이프라인이 여섯 걸음이다.

```
1. main 에 푸시
2. GitHub Actions 가 빌드·테스트
3. 도커 이미지를 만들어 레지스트리(ghcr.io)에 푸시
4. AWS SSM 으로 EC2 에 배포 스크립트 실행
5. 비어 있는 포트에 새 버전 컨테이너를 띄움
6. 포트를 전환해 무중단 배포 → [[zero-downtime-deployment]]
```

### 언제 도나 — 트리거

```yaml
on:
  push:
    paths: ['src/**', 'build.gradle', 'Dockerfile', 'infraScript/**']
    branches: ['main']
```

**경로까지 지정한다** — 문서만 고친 푸시로 배포가 도는 것을 막는다.

### 무엇을 하나 — 잡과 의존

```yaml
jobs:
  makeTagAndRelease:  ...                      # 버전 태그·릴리즈 생성
  buildImageAndPush:  needs: makeTagAndRelease # 앞이 끝나야 시작
  deploy:             needs: [buildImageAndPush]
```

`needs` 가 **순서를 만든다** — 셋이 사슬로 이어지고, 앞이 실패하면 뒤가 안 돈다.

### 비밀은 어디에

```yaml
password: ${{ secrets.GITHUB_TOKEN }}
aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
```

**저장소의 Secrets 에 두고 이름으로만 참조한다** — 워크플로우 파일은 공개돼도 키는 안 드러난다 → [[externalized-configuration]]

### 원격 실행 — SSM

배포는 서버에 SSH 로 들어가지 않고 **AWS SSM 이 명령을 대신 실행**한다.

```yaml
command: |
  curl -o /dockerProjects/blog/zero_downtime_deploy.py https://.../zero_downtime_deploy.py
  chmod +x /dockerProjects/blog/zero_downtime_deploy.py
  /dockerProjects/blog/zero_downtime_deploy.py
```

**서버에 열린 SSH 포트가 필요 없다**는 것이 이 방식의 이점이다 → [[infrastructure-as-code]]

## 왜 중요한가

**배포가 사람의 기억에서 파일로 옮겨 간다.** 손으로 하던 여섯 단계(로그인·클론·설정·빌드·실행·확인)는 **누가 하느냐에 따라 달라지고 한 단계를 빠뜨리면 조용히 틀린다.** 파일에 적혀 있으면 언제나 같은 순서로 돈다 → [[infrastructure-as-code]] · [[build]]

**그리고 이미지가 배포 단위가 된다.** 서버에서 소스를 받아 빌드하던 것을 **미리 만든 이미지를 받아 실행하는 것**으로 바꾸면, 「빌드 환경이 서버마다 다르다」는 문제가 사라진다 → [[container]]

## 경계와 오해

- **CI 와 CD 는 다른 것이다** — CI 는 **합치고 검증하는 것**(빌드·테스트), CD 는 **배포하는 것**이다. 테스트 없이 자동 배포만 있으면 「빠르게 틀린 것을 내보내는」 파이프라인이 된다
- **`latest` 태그와 버전 태그를 함께 미는 이유가 있다** — `latest` 만 쓰면 **지금 도는 것이 무엇인지 알 수 없고 되돌릴 수도 없다.** 버전 태그가 있어야 롤백이 가능하다
- **비밀을 Secrets 에 넣어도 로그로 샐 수 있다** — 스크립트가 값을 출력하면 그대로 남는다. GitHub 이 마스킹해 주지만 **가공된 값은 못 가린다**
- **`paths` 필터는 양날이다** — 배포를 줄여 주지만, 목록에 없는 파일을 고쳤을 때 **배포가 안 되는 것을 모른 채** 지나갈 수 있다
- **파이프라인이 실패했는데 배포가 반쯤 된 상태가 가능하다** — 이미지는 올라갔는데 SSM 명령이 실패하는 식이다. **각 단계가 되돌릴 수 있는지**를 따로 생각해야 한다 → [[transaction]] 과 같은 물음이 인프라에서 반복된다
- **원격 실행 권한이 곧 서버 권한이다** — SSM 으로 임의 명령을 돌릴 수 있다는 것은 그 키를 가진 사람이 **서버에서 무엇이든 할 수 있다**는 뜻이다

## 함께 보는 개념

- [[zero-downtime-deployment]] — 파이프라인의 마지막 걸음
- [[container]] — 배포 단위가 되는 것
- [[infrastructure-as-code]] — 서버를 만드는 쪽의 같은 발상
- [[build]] · [[gradle]] — 이미지 안에서 도는 것
- [[externalized-configuration]] — 비밀을 다루는 자리
- [[git]] — 이벤트가 나오는 곳
- [[reverse-proxy]] — 배포된 것 앞에 서는 것
- [[kubernetes]] — 배포 대상이 클러스터가 될 때

## 출처

- [[2025-01-17-Day14]] — 나흘 뒤. **배포하는 방법이 바뀐다** — AWS SSM 으로 서버에 명령을 보내던 것이 **kubeconfig 로 클러스터 API 에 붙어 `kubectl set image` 를 부르는 것**이 된다. 필기가 그 이행을 명시했다(「기존 방식은 aws ssm 을 이용하여 접속하는 방식이었다 / 이번에는 github actions 를 이용하여 마스터 노드에 접근하여 자동배포를 진행한다」). `~/.kube/config` 의 구조(clusters·users·contexts)를 풀어 적고 **그 파일을 통째로 Secrets 에 넣는다**는 것까지 나오는데, 그것은 곧 **클러스터 전체 권한을 워크플로우에 준다**는 뜻이다. 이미지 태그로 앞 잡의 출력(`needs.makeTagAndRelease.outputs.tag_name`)을 쓰는 것도 잡 사이 값 전달의 예다 → [[kubernetes]]
- [[2025-01-13-Day10]] — 「깃허브 액션을 통한 CI/CD 파이프라인 구축」 절이 **여섯 단계를 먼저 글로 적고** 워크플로우 YAML 을 잡 단위로 나눠 실었다 — `makeTagAndRelease`(태그·릴리즈 자동 생성) → `buildImageAndPush`(Buildx·ghcr 로그인·이미지 푸시) → `deploy`(AWS SSM 으로 원격 스크립트 실행). `needs` 로 잡을 잇는 것과 `${{ secrets.* }}` 로 키를 참조하는 것이 코드에 그대로 있다. 앞의 「도커 컨테이너 실행 및 배포(수동)」 절이 **같은 일을 손으로 하는 일곱 단계**를 남겨 둔 것이 이 노트의 값이다 — 자동화가 무엇을 대신하는지가 나란히 보인다. 그중 「docker 에서 접속 시에 `172.17.0.1` 로 접속을 하는데 spring 내부에서 이 아이피에 대한 권한을 설정해줘야 한다」는 **컨테이너 안에서 호스트 DB 에 붙을 때의 실전 함정**이다 → [[container]]
