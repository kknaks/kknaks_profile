---
type: concept
id: ci-cd
title: CI/CD 파이프라인 (GitHub Actions)
aliases:
  - CI/CD
  - GitHub Actions
  - 파이프라인
  - 컨테이너 레지스트리
  - main 빌드만
  - 이미지 태그 = 커밋 sha
  - 전체 sha 태그
  - ArgoCD 수동 sync
  - 폴더별 이미지 빌드
  - imageTag 오버라이드
up:
  - 2025-01-13-Day10
  - 2025-01-17-Day14
  - 2026-08-31-task-redesign
  - 2026-10-14-sts-prototype
  - 2026-10-22-myeongdong-poc-v2
  - 2026-10-27-interpret-pwa-poc
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

**브랜치도 지정한다** — `branches` 를 빼면 모든 브랜치 푸시가 이미지를 굽는다. 태그가 커밋 sha 라 어느 이미지든 배포 값에 넣을 수 있고, 그러면 **리뷰 · 머지 안 된 코드가 배포된다.** cc-prototype 이 그랬다 — 브랜치 빌드가 운영에 올라가 있었고, `branches: [main]` 으로 막은 뒤 main 빌드로 갈아 끼웠다. 이미지를 만드는 조건이 곧 배포할 수 있는 코드의 범위다

**태그는 커밋 전체 sha 하나 — `latest` · `main` 은 밀지 않는다** — 차트의 값(`image.tag`) 하나만 보면 무엇이 떠 있는지 알고, 그 값은 사람이 고르지 않는다. cc-prototype 은 차트에서 `image.tag` 를 `required` 로 걸어 **값이 없으면 렌더가 실패**하게 했다 — 빈 값이나 추측한 태그로 배포가 나가지 않는다. 함정은 길이다 — Actions 는 `github.sha`(40자)로 밀므로 배포 값도 40자여야 하고, PR 제목에 보이는 7자 sha 로는 그 이미지가 없다. 배포(GitOps · ArgoCD)는 **수동 sync** 로 두었다 — ConfigMap 이 바뀌면 back 재시작이 같이 필요해서, 값을 바꾼 PR 머지와 실제 반영 사이에 사람이 한 번 선다

**폴더별로 따로 빌드하면 sha 가 구성 요소마다 갈린다** — 한 레포에 `front/` · `back/` 이 있고 워크플로가 `paths` 로 **바뀐 폴더만** 이미지를 구우면, front 만 바뀐 커밋에는 그 sha 의 back 이미지가 없다. 차트 값이 `image.tag` 하나뿐이면 그 배포를 올릴 수 없다. 통키는 차트에 `front.imageTag` / `back.imageTag` 오버라이드를 두어(있으면 `image.tag` 보다 우선) 구성 요소마다 다른 sha 를 넣었고, 두 폴더가 같은 sha 로 빌드된 배포에서 다시 `image.tag` 하나로 정리했다. 오버라이드는 「지금 무엇이 떠 있나」 를 값 둘로 보게 만드므로 임시로 쓰고 걷는다

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

## 러너를 직접 굴릴 때 — self-hosted

GitHub 이 주는 러너 대신 **내 클러스터의 파드가 잡을 받는** 구성(ARC — Actions Runner Controller). 비용 절감이 목적이지만, 호스팅 러너가 전면 차단됐을 때(결제 실패 등) **배포를 계속 굴릴 수 있는 우회로**이기도 하다.

- **1잡 1파드(ephemeral)** — 잡마다 깨끗한 파드가 뜨고 끝나면 폐기된다. 그래서 「러너에 뭘 설치해 둔다」는 발상이 통하지 않는다 — 호스트에 깔아도 파드에서 안 보이고, 파드에 깔면 잡과 함께 사라진다. 도구가 없으면 ① 워크플로 스텝에서 설치 ② **프로토콜 수준 대체** ③ 러너 이미지에 굽기(장기) 셋 중 하나다
- **프로토콜 대체가 설치보다 낫다** — `az acr login` 은 결국 docker login 이다. 벤더 CLI 가 없다고 CLI 를 까는 대신, 그 CLI 가 **하던 일의 실체**(레지스트리 로그인)를 표준 액션(`docker/login-action` + service principal 자격증명)으로 하면 설치 0·아키 무관이 된다
- **러너의 아키 ≠ 산출물의 아키** — arm64 러너에서도 `platforms: linux/amd64` 로 amd64 이미지를 빌드한다(QEMU 에뮬레이션, `docker/setup-qemu-action` 필수). 느려지지만 서버에 올라가는 이미지는 동일하다. 반대로 산출물이 arm64 면 셀프호스트 arm 이 네이티브라 오히려 빠르다
- **「5초 만에 스텝 0개로 실패」는 러너 문제처럼 보이지만 아니다** — 호스팅 러너의 결제/지출 한도 차단이 이 모양으로 나타난다. 어노테이션(`recent account payments have failed…`)을 봐야 갈린다

## 경계와 오해

- **CI 와 CD 는 다른 것이다** — CI 는 **합치고 검증하는 것**(빌드·테스트), CD 는 **배포하는 것**이다. 테스트 없이 자동 배포만 있으면 「빠르게 틀린 것을 내보내는」 파이프라인이 된다
- **`latest` 태그와 버전 태그를 함께 미는 이유가 있다** — `latest` 만 쓰면 **지금 도는 것이 무엇인지 알 수 없고 되돌릴 수도 없다.** 버전 태그가 있어야 롤백이 가능하다. 한 걸음 더 가면 `latest` 를 아예 안 밀고 커밋 sha 만 쓴다 — 움직이는 태그가 없으면 배포 값이 곧 코드 위치다
- **비밀을 Secrets 에 넣어도 로그로 샐 수 있다** — 스크립트가 값을 출력하면 그대로 남는다. GitHub 이 마스킹해 주지만 **가공된 값은 못 가린다**
- **`paths` 필터는 양날이다** — 배포를 줄여 주지만, 목록에 없는 파일을 고쳤을 때 **배포가 안 되는 것을 모른 채** 지나갈 수 있다. 폴더별 빌드에서는 「이 sha 의 이미지가 구성 요소마다 있나」 가 갈린다 — 태그 = sha 규칙과 만나면 구성 요소별 태그가 필요해진다
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

- [[2026-10-27-interpret-pwa-poc]] §2 — 폴더별 이미지 빌드라 front 만 바뀐 sha 에 back 이미지가 없음 → `front.imageTag` / `back.imageTag` 오버라이드 → 같은 sha 배포에서 하나로 정리(`charts/interpret-pwa/values-prod.yaml` · infra #29 · #30 · #32 · #33)
- [[2026-10-22-myeongdong-poc-v2]] §2 — 이미지 태그 = 커밋 전체 sha(40자) · 차트 `required image.tag` · ArgoCD 수동 sync(`procedure-back-image.yml` · infra #22 · #24)
- [[2026-10-14-sts-prototype]] §2 — 모든 브랜치 푸시에서 이미지가 빌드돼 브랜치 코드가 배포됐다 → 빌드 트리거를 main 으로 막고 main 빌드로 재배포(infra #19)
- [[2026-08-31-task-redesign]] — GitHub 결제 장애로 호스팅 러너가 전면 차단된 날, mediness(arm64 네이티브 빌드)와 CHARTY(QEMU amd64 크로스빌드 → ACR push → ssh 배포)를 사내 ARC 러너로 우회해 **당일 배포를 완주**한 실전. `az` 부재는 설치가 아니라 docker login 치환으로 풀었고, ephemeral 파드라 「서버에 설치」가 무의미하다는 것을 몸으로 확인했다

- [[2025-01-17-Day14]] — 나흘 뒤. **배포하는 방법이 바뀐다** — AWS SSM 으로 서버에 명령을 보내던 것이 **kubeconfig 로 클러스터 API 에 붙어 `kubectl set image` 를 부르는 것**이 된다. 필기가 그 이행을 명시했다(「기존 방식은 aws ssm 을 이용하여 접속하는 방식이었다 / 이번에는 github actions 를 이용하여 마스터 노드에 접근하여 자동배포를 진행한다」). `~/.kube/config` 의 구조(clusters·users·contexts)를 풀어 적고 **그 파일을 통째로 Secrets 에 넣는다**는 것까지 나오는데, 그것은 곧 **클러스터 전체 권한을 워크플로우에 준다**는 뜻이다. 이미지 태그로 앞 잡의 출력(`needs.makeTagAndRelease.outputs.tag_name`)을 쓰는 것도 잡 사이 값 전달의 예다 → [[kubernetes]]
- [[2025-01-13-Day10]] — 「깃허브 액션을 통한 CI/CD 파이프라인 구축」 절이 **여섯 단계를 먼저 글로 적고** 워크플로우 YAML 을 잡 단위로 나눠 실었다 — `makeTagAndRelease`(태그·릴리즈 자동 생성) → `buildImageAndPush`(Buildx·ghcr 로그인·이미지 푸시) → `deploy`(AWS SSM 으로 원격 스크립트 실행). `needs` 로 잡을 잇는 것과 `${{ secrets.* }}` 로 키를 참조하는 것이 코드에 그대로 있다. 앞의 「도커 컨테이너 실행 및 배포(수동)」 절이 **같은 일을 손으로 하는 일곱 단계**를 남겨 둔 것이 이 노트의 값이다 — 자동화가 무엇을 대신하는지가 나란히 보인다. 그중 「docker 에서 접속 시에 `172.17.0.1` 로 접속을 하는데 spring 내부에서 이 아이피에 대한 권한을 설정해줘야 한다」는 **컨테이너 안에서 호스트 DB 에 붙을 때의 실전 함정**이다 → [[container]]
