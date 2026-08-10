---
type: concept
id: infrastructure-as-code
title: 코드로 만드는 인프라 (Terraform)
aliases:
  - Terraform
  - 테라폼
  - IaC
  - Infrastructure as Code
up:
  - 2025-01-03-Day04
  - 2025-01-13-Day10
tags:
  - 인프라
  - 배포
  - 자동화
---

# 코드로 만드는 인프라 (Terraform)

**서버·네트워크·저장소를 콘솔에서 클릭해 만드는 대신 파일에 선언하고 명령으로 만든다.** 만드는 절차가 아니라 **원하는 상태**를 적는다.

## 정의

```hcl
terraform {
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 4.0" }
  }
}

provider "aws" {
  region = "ap-northeast-2"      # 서울
}

resource "aws_vpc" "example" {
  cidr_block = "10.0.0.0/16"
  tags = { Name = "example" }
}
```

- **provider** — 어느 클라우드를 다룰지
- **resource** — **무엇이 있어야 하는지** (「만들어라」가 아니라 「있어야 한다」)

명령이 넷이다.

| 명령 | 하는 일 |
|---|---|
| `terraform init` | 라이브러리(provider) 내려받기. **소스가 바뀌면 다시** |
| `terraform plan` | **실제로 만들지 않고** 무엇이 바뀔지 보여 준다 |
| `terraform apply` | 리소스를 만든다 (확인 후 `yes`) |
| `terraform destroy` | 만든 것을 지운다 |

접근 권한은 AWS CLI 로 미리 설정한다.

```bash
aws configure          # 액세스 키·시크릿 키·리전 등록
aws configure list     # 등록됐는지 확인
rm -rf ~/.aws          # 지우기
```

## 왜 중요한가

**「내가 저번에 어떻게 만들었더라」가 사라진다.** 콘솔로 만든 인프라는 **기록이 사람의 기억뿐**이고, 같은 것을 다시 만들거나 개발·운영 환경을 맞추는 일이 매번 수작업이다. 파일로 적어 두면 **그 파일이 곧 문서이자 절차**이고, 저장소에 들어가 이력이 남는다 → [[git]] · [[web-application-deployment]]

**그리고 `plan` 이 있다는 것이 크다.** 인프라는 잘못 만들면 되돌리기 어렵고 돈이 든다. **적용 전에 무엇이 바뀔지 보여 주는 단계**가 따로 있는 것이 이 도구의 성격을 정한다.

**선언형이라는 것도 핵심이다.** 「VPC 를 만들어라」가 아니라 「이런 VPC 가 있어야 한다」이므로, 같은 파일을 여러 번 적용해도 **이미 있으면 아무 일도 안 한다** → [[declarative-transaction]] 의 「무엇을」과 같은 방향이다.

## 경계와 오해

- **상태 파일이 진짜 자산이다** — 테라폼은 「무엇을 만들었는지」를 상태 파일에 기록해 두고 그것과 코드를 비교한다. **그 파일을 잃으면 이미 만든 것을 모른다.** 여럿이 쓸 때 상태 파일을 어디에 둘지가 첫 번째 문제가 된다
- **콘솔에서 손으로 고치면 어긋난다** — 코드가 아는 상태와 실제가 달라지고, 다음 `apply` 에서 되돌려 버리거나 실패한다. **한 가지 방법으로만 만져야** 성립하는 도구다
- **`destroy` 는 진짜 지운다** — 실습에서는 편하지만 운영에서는 **한 번의 오타가 서비스 전체**다. `plan` 을 읽는 습관이 그래서 필요하다
- **액세스 키는 `~/.aws` 에 평문으로 남는다** — `rm -rf ~/.aws` 로 지우는 절차를 함께 적어 둔 이유다. 저장소에 올라가는 것만 조심할 것이 아니라 **로컬에도 남는다** → [[externalized-configuration]]
- **자동화가 이해를 대신하지 않는다** — `cidr_block = "10.0.0.0/16"` 이 무엇을 뜻하는지 모르면 코드로 적어도 모르는 것이다. 도구는 **반복을 없앨 뿐 개념을 없애지 않는다** → [[ip-address]] · [[computer-network]]

## 함께 보는 개념

- [[web-application-deployment]] — 이 인프라 위에 올라가는 것
- [[container]] — 애플리케이션 쪽의 같은 발상
- [[git]] — 인프라 정의가 이력을 갖게 되는 곳
- [[externalized-configuration]] — 키와 환경별 값을 다루는 문제
- [[computer-network]] · [[ip-address]] — 선언하는 대상의 실체
- [[build]] — 절차를 파일로 적는다는 같은 성격
- [[ci-cd]] — 만들어 둔 인프라에 코드를 올리는 쪽
- [[computer-network]] — VPC·서브넷·보안그룹이 선언하는 대상

## 출처

- [[2025-01-13-Day10]] — 열흘 뒤. **VPC 하나에서 서비스 한 벌로 커진다.** `aws_vpc` → 서브넷 → 보안 그룹 → IAM 역할·정책 → EC2 인스턴스 → User Data 스크립트까지가 한 `main.tf` 에 선언되고, **인스턴스가 뜨면서 실행할 초기화 스크립트(User Data)까지 코드에 들어간다** — 서버를 만드는 것과 서버 안을 준비하는 것이 같은 파일에 있다. `var.region` 처럼 변수를 쓰는 것도 이 회차에서 나온다. 그리고 IAM 역할을 붙여 둔 덕에 나중에 **SSM 으로 원격 명령을 실행**할 수 있게 되는데, 인프라 설계가 배포 방식을 정하는 자리다 → [[ci-cd]]
- [[2025-01-03-Day04]] — 「Terraform」 절이 **설치부터 첫 리소스까지 한 줄로 이어진다** — AWS CLI 설치(`curl` + `installer`), `aws configure` 로 액세스 키 등록(리전 `ap-northeast-2` 가 서울이라는 주석 포함), 테라폼 CLI 설치, 그리고 `required_providers`·`provider`·`resource` 세 블록으로 VPC 하나를 선언하는 예제. **`terraform` 블록을 「자바의 import 와 비슷함」**이라고 옮겨 적은 주석이 이 문법을 처음 볼 때의 감각을 잘 남겼다. 네 명령(`init`·`plan`·`apply`·`destroy`)에 각각 한 줄 설명이 붙어 있고, 특히 **`plan` 이 「실제 리소스 생성을 하는 것은 아니고 현재 소스코드가 실행 가능한지 검사」**라는 구별이 명확하다. `rm -rf ~/.aws` 로 키를 지우는 방법까지 적은 것도 실전적이다. 다만 상태 파일과 여럿이 함께 쓸 때의 문제는 다루지 않는다
