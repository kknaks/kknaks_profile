---
concept:
- GitFlow는 main, develop, feature, release, hotfix 5가지 브랜치로 체계적으로 코드를 관리하고 버전 통제한다.
- Trunk-based는 main 브랜치 하나에 짧은 기간(1~2일) feature 브랜치를 만들어 빠르게 병합하고 연속 배포한다.
- GitFlow는 안정성·버전 관리 중심, Trunk-based는 배포 속도·지속적 통합 중심이다.
- 프로젝트 규모, 팀 문화, 배포 빈도에 따라 선택하되 선택의 근거를 명확히 해야 한다.
- 두 전략의 중간 형태(하이브리드, GitHub Flow)와 Feature Flags 같은 보완 기법도 함께 검토할 수 있다.
date: 2026-05-20
day: Day 15
duration: '6:05'
enriched_at: '2026-05-20T13:17:20+09:00'
id: C-015
kind: study
speaker: 코딩애플
status: published
summary:
  en: Compare two Git branching strategies for multi-developer teams—GitFlow for stability
    and Trunk-based for speed—with criteria to choose the right approach.
  ko: 다중 개발자 환경에서 코드 안정성과 빠른 배포를 동시에 달성하기 위한 두 가지 Git 전략을 비교하고 프로젝트에 맞는 선택 기준을 제시한다.
tags:
- '#gitflow'
- '#trunk-based'
- '#git'
- '#collaboration'
- '#branching'
- '#ci-cd'
- '#devops'
title:
  en: 'GitFlow vs Trunk-based: Branching Strategies for Team Collaboration'
  ko: 'GitFlow vs Trunk-based: 팀 협업 브랜칭 전략'
transcript: true
type: content
youtubeId: EV3FZ3cWBp8
---

## 개요

여러 개발자가 함께 작업할 때 누가 무엇을 했는지 추적하기 어렵고, 코드 충돌이 자주 발생하며, 프로덕션 배포가 위험해집니다. 이를 해결하기 위해 체계적인 Git 브랜칭 전략이 필요합니다. 이 문서에서는 업계에서 가장 널리 사용되는 두 가지 접근 방식인 GitFlow와 Trunk-based 개발을 비교하고, 각 전략의 작동 방식과 선택 기준을 제시합니다.

## 배경 / 사전 지식

**브랜치(Branch)**
Git에서 독립적인 개발 라인을 만드는 기능으로, 기존 코드의 영향 없이 새로운 기능을 개발할 수 있습니다.

**병합(Merge)**
한 브랜치의 변경사항을 다른 브랜치에 통합하는 과정입니다. `--no-ff` 옵션으로 병합 이력을 명확히 남길 수 있습니다.

**Pull Request (PR)**
GitHub의 협업 메커니즘으로, 코드 변경을 제안하고 리뷰를 거친 후 병합합니다.

**지속적 통합(CI, Continuous Integration)**
변경사항이 자동으로 테스트되고 통합되는 개발 방식입니다.

**지속적 배포(CD, Continuous Delivery)**
테스트를 거친 코드를 자동으로 프로덕션에 배포하는 프로세스입니다.

**태그(Tag)**
Git의 특정 커밋에 버전 번호를 붙여 릴리스 이력을 관리합니다.

## 핵심 개념

### GitFlow 전략

GitFlow는 Vincent Driessen이 2010년에 제안한 브랜칭 모델로, 5가지 주요 브랜치를 운영하여 체계적으로 코드를 관리합니다.

**1. Main 브랜치 (Master)**

Main 브랜치는 프로덕션에 배포된 안정적인 코드만 포함합니다. 모든 커밋에는 버전 태그(예: v1.0, v1.0.1)가 붙어 배포 이력을 명확히 추적할 수 있습니다. 개발자가 직접 수정하지 않고, 다른 브랜치(Release, Hotfix)에서만 병합받습니다.

**2. Develop 브랜치**

Develop 브랜치는 다음 릴리스를 위한 개발 코드가 모이는 중앙 허브 역할을 합니다. Feature 브랜치에서 완성된 기능들이 병합되고, Release 브랜치의 기반이 됩니다. Main에 비해 불안정할 수 있습니다.

**3. Feature 브랜치**

Feature 브랜치는 Develop에서 분기하여 새로운 기능 하나를 개발합니다. 명명 규칙은 `feature/기능이름`입니다(예: `feature/guild`, `feature/friend`). 여러 개의 Feature 브랜치가 동시에 개발될 수 있으며, 완료 후 Pull Request를 통해 Develop에 병합합니다.

**4. Release 브랜치**

Release 브랜치는 Develop에서 분기하여 출시 준비를 수행합니다. 명명 규칙은 `release/버전번호`입니다(예: `release/1.0`). 최종 테스트, QA, 버그 수정을 이 브랜치에서 진행한 후, Main에 병합하여 배포하고, 동시에 Develop에도 병합하여 변경사항을 반영합니다.

**5. Hotfix 브랜치**

Hotfix 브랜치는 Main에서 직접 분기하여 프로덕션의 긴급 버그를 수정합니다. 명명 규칙은 `hotfix/버그이름`입니다(예: `hotfix/gold-duplication`). 수정 완료 후 Main과 Develop 모두에 병합하여 모든 개발 라인에 버그 수정 사항을 반영합니다.

### Trunk-based 개발

Trunk-based 개발은 하나의 메인 브랜치(Trunk, 또는 Main)를 중심으로 모든 개발을 진행하는 단순하고 빠른 방식입니다.

**기본 개념**

Trunk-based에서는 메인 브랜치 하나를 중심으로 운영합니다. Feature 브랜치를 만들지만, 매우 짧은 기간(보통 1~2일) 동안만 유지하고 빠르게 메인 브랜치로 병합합니다. 병합된 메인 브랜치의 코드는 지속적으로 배포되어 사용자에게 전달됩니다. GitHub Flow도 이와 유사한 전략입니다.

**작업 흐름**

1. 메인 브랜치에서 Feature 브랜치 생성
2. 코드 작업 수행 (짧은 기간)
3. 메인 브랜치로 병합
4. 자동 CI/CD 파이프라인이 테스트와 배포 실행

## 작동 원리

### GitFlow 상세 프로세스

**단계 1: 초기 상태**

Main 브랜치에 0.9 버전의 안정적인 코드가 있습니다. 개발자들이 직접 수정하는 것은 위험하므로 다른 브랜치에서 개발을 시작합니다.

**단계 2: 개발 시작**

Main에서 Develop 브랜치를 생성합니다. 이 Develop 브랜치에서 여러 Feature 브랜치를 분기하여 병렬로 개발을 진행합니다. 예를 들어:
- `feature/guild`에서 길드 기능 개발
- `feature/friend`에서 친구 기능 개발

각 기능이 완성되면 Pull Request를 통해 Develop으로 병합합니다.

**단계 3: 출시 준비**

Develop 브랜치의 코드가 충분히 완성되면 Release 브랜치를 생성합니다(예: `release/1.0`). 이 브랜치에서 최종 테스트, QA, 버그 수정을 수행합니다. 안정화 완료 후:
- Main으로 병합하여 배포
- 동시에 Develop으로도 병합하여 개발 라인 동기화

**단계 4: 긴급 버그 수정**

프로덕션(Main)에서 버그가 발견되면(예: 골드 무한 복사), Main에서 직접 Hotfix 브랜치를 생성합니다. 버그를 수정한 후:
- Main으로 병합하여 즉시 배포
- Develop으로도 병합하여 개발 중인 다음 버전에 반영

### Trunk-based 개발 상세 프로세스

**단계 1: 기본 상태**

Main 브랜치 하나만 운영합니다. 이 브랜치는 항상 배포 가능한 상태(production-ready)여야 합니다.

**단계 2: 새 기능 또는 버그 수정**

필요한 작업마다 Main에서 Feature 브랜치를 생성합니다. 예를 들어 새로운 아이템 시스템이 필요하면 `feature/new-item` 브랜치를 만듭니다. 코드 작업은 매우 짧은 기간(1~2일) 동안만 진행되며, 완료되면 즉시 Main으로 병합합니다.

**단계 3: 배포**

Main 브랜치의 모든 코드는 자동 테스트를 거쳐 자동으로 배포됩니다. 개발자가 수동으로 배포 시점을 결정할 필요가 없습니다.

## 코드 예시

### GitFlow 명령어

```bash
# 1. Develop 브랜치 생성 (최초 1회)
git checkout -b develop main

# 2. Feature 브랜치에서 기능 개발
git checkout -b feature/guild develop
# (코드 작성)
git add .
git commit -m "Add guild system"
git push origin feature/guild

# 3. Feature를 Develop으로 병합
# Pull Request를 통해 리뷰 후 병합
git checkout develop
git merge --no-ff feature/guild  # --no-ff는 병합 이력을 명확히 남김
git push origin develop

# 4. Release 브랜치 생성 및 테스트
git checkout -b release/1.0 develop
# (테스트, 버그 수정, 버전 정보 업데이트)
git commit -m "Bump version to 1.0"

# 5. Release를 Main으로 병합하고 태그 지정
git checkout main
git merge --no-ff release/1.0
git tag -a v1.0 -m "Version 1.0 release"
git push origin main --tags

# 6. Release 내용을 Develop으로 다시 병합 (중요!)
git checkout develop
git merge --no-ff release/1.0
git push origin develop

# 7. 프로덕션 버그 발생 시 Hotfix
git checkout -b hotfix/gold-duplication main
# (버그 수정)
git commit -m "Fix gold duplication bug"

# 8. Hotfix를 Main과 Develop 모두에 병합
git checkout main
git merge --no-ff hotfix/gold-duplication
git tag -a v1.0.1 -m "Hotfix v1.0.1"
git push origin main --tags

git checkout develop
git merge --no-ff hotfix/gold-duplication
git push origin develop
```

각 명령어의 의미:
- `git checkout -b [브랜치명] [기반브랜치]`: 새 브랜치 생성 및 전환
- `git merge --no-ff`: 병합을 별도의 커밋으로 기록하여 이력을 명확히 유지
- `git tag -a`: 주석이 있는 태그 생성 (배포 버전 기록)
- `git push --tags`: 태그 정보도 함께 원격 저장소에 푸시

### Trunk-based 명령어

```bash
# 1. Feature 브랜치 생성 (짧은 수명)
git checkout -b feature/new-item main

# 2. 코드 작업 (1~2일 내 완료)
# (코드 작성)
git add .
git commit -m "Add new item system"
git push origin feature/new-item

# 3. Main으로 빠르게 병합
git checkout main
git merge feature/new-item
git push origin main

# 4. 자동 CI/CD 파이프라인
# (Main 푸시 후 자동으로 테스트 및 배포 실행)
# - 자동 테스트 실행
# - 빌드 성공 확인
# - 자동 배포 실행
# - 모니터링 및 로깅
```

중요 포인트:
- Feature 브랜치를 만들지만 매우 짧은 기간만 유지
- Pull Request 없이 직접 병합할 수도 있음 (팀의 신뢰도에 따라)
- Main 브랜치는 항상 배포 가능한 상태여야 함
- 자동 테스트가 필수적

## 함정·실수

### GitFlow 사용 시 주의사항

**함정 1: 브랜치 관리 복잡도**

5개 브랜치를 동시에 관리해야 하므로 관리 부담이 증가합니다. 팀원들이 올바른 브랜치 구조를 이해하지 못하면 실수가 발생합니다. 예를 들어 Feature에서 Main으로 직접 병합하거나, Release에서 병합할 브랜치를 잘못 선택하는 경우가 있습니다.

**회피법**: 브랜치 정책을 문서화하고, GitHub의 branch protection rules로 정책 강제. Pull Request 템플릿으로 필수 체크리스트 자동 표시.

**함정 2: Release와 Hotfix 모두에 병합 필요**

Release나 Hotfix에서 버그를 수정했을 때 Main과 Develop 모두에 병합해야 합니다. 한쪽에만 병합하면 버그가 다시 발생합니다.

**회피법**: 병합 체크리스트를 만들어 Main→Develop 또는 Main+Develop 병합이 필수임을 명시.

**함정 3: Release 브랜치 필수성 오판**

모든 프로젝트에서 Release 브랜치가 필요한 것은 아닙니다. 작은 팀이나 빠른 배포가 필요한 경우 Release 단계를 생략하고 Develop에서 직접 Main으로 병합할 수 있습니다.

**회피법**: 프로젝트 특성에 맞게 "필요한 브랜치"만 사용. Release 브랜치가 필요 없다면 제거해도 됨.

### Trunk-based 개발 사용 시 주의사항

**함정 1: Feature 브랜치 장시간 유지**

Trunk-based의 핵심은 짧은 기간만 브랜치를 유지하는 것입니다. 하지만 부정확한 작업 추정이나 복잡한 기능으로 인해 Feature 브랜치가 며칠 이상 유지되면, Main과의 차이가 커져 병합 충돌이 증가합니다.

**회피법**: 
- 기능을 더 작은 단위로 분할
- "1일 = 1 병합"을 목표로 설정
- 기능을 먼저 병합한 후 Feature Flags로 숨기기 (아래 참고)

**함정 2: 자동 테스트 부족**

Main 브랜치의 모든 코드가 바로 배포되므로, 자동화된 테스트가 부족하면 버그가 프로덕션으로 직접 배포될 위험이 높습니다.

**회피법**: 
- 단위 테스트(unit test) 커버리지 70% 이상 유지
- CI 파이프라인에서 자동 테스트 필수화
- 배포 후 자동 모니터링 및 이상 감지 시스템

**함정 3: 배포 자동화 없이 시작**

Continuous Delivery(CD) 없이 Trunk-based만 도입하면 개발은 빨라도 배포는 여전히 느립니다.

**회피법**: 
- Trunk-based와 CI/CD 자동화는 함께 구축
- 자동화 인프라(Jenkins, GitHub Actions, GitLab CI 등) 먼저 구성

## 베스트 프랙티스

### GitFlow를 선택해야 할 때

- **버전 관리가 중요한 경우**: 게임, 대형 소프트웨어처럼 여러 버전을 동시에 지원해야 함
- **정기적 릴리스**: 월 1회, 분기별 등 정해진 일정에 배포
- **팀 규모가 큼**: 10명 이상의 개발자가 복잡한 작업을 진행
- **프로덕션 안정성 최우선**: 배포 전 충분한 테스트와 검증 필요
- **출시 후 핫픽스 빈번**: 프로덕션 버그가 자주 발생하여 빠른 수정 필요

**GitFlow 사용 프로젝트 예**: 게임 개발, 금융 소프트웨어, 의료 시스템

### Trunk-based를 선택해야 할 때

- **빠른 배포 중요**: 웹 서비스, SaaS, 모바일 앱 같이 사용자에게 빠르게 기능 전달 필요
- **CI/CD 인프라 구축됨**: GitHub Actions, Jenkins 등으로 자동화 환경 준비됨
- **팀 규모 작음**: 5~10명 이하, 빠른 의사결정 가능
- **코드 충분히 안정화**: 자동 테스트가 잘 갖춰져 있음
- **작은 단위 배포**: 매일 여러 번 배포하는 문화

**Trunk-based 사용 프로젝트 예**: 웹 서비스(e-commerce, SNS), SaaS, 지속적 개선 필요한 서비스

### 하이브리드 및 변형 접근

**변형 GitFlow**

모든 프로젝트가 5개 브랜치를 모두 필요로 하는 것은 아닙니다. 프로젝트 특성에 맞게 조정할 수 있습니다:
- Release 브랜치 제거: Develop에서 테스트 후 직접 Main으로 병합
- Hotfix 간소화: 긴급 버그도 Feature 브랜치로 처리

**GitHub Flow**

GitHub 중심의 간단한 워크플로우:
1. Main 브랜치만 운영
2. 기능마다 Feature 브랜치 생성
3. Pull Request로 코드 리뷰
4. 승인 후 병합 및 자동 배포

GitFlow와 Trunk-based의 중간 형태로, 웹 개발에 가장 널리 사용됩니다.

**Feature Flags (Feature Toggle)**

Trunk-based에서 미완성 기능을 배포 시에도 숨기는 기법:
```javascript
// 배포는 되었지만 기능은 비활성화
if (featureFlags.isGuildEnabled) {
  renderGuildUI();
}
```

이를 통해:
- 개발과 배포를 분리 (개발은 계속, 기능 활성화는 나중에)
- 위험 감소 (문제 발생 시 즉시 비활성화)
- A/B 테스트 가능

### 중요한 원칙

**원칙 1: 선택의 책임**

선택한 브랜칭 전략에 대해 합리적인 근거를 제시할 수 있어야 합니다. "다른 팀이 하니까" 또는 "강의에서 배웠으니까"는 이유가 아닙니다. "우리 팀은 매일 배포해야 하니 Trunk-based를 채택합니다" 같은 명확한 이유가 필요합니다.

**원칙 2: 유연성 유지**

프로젝트가 변하면 전략도 변경할 수 있습니다. 초기에는 GitFlow였지만 팀이 성장하고 자동화가 구축되면 Trunk-based로 전환할 수 있습니다. 교리적 접근("이것만 써야 한다")은 피할 것.

**원칙 3: 자동화 우선**

선택한 전략과 무관하게 CI/CD 자동화 구축이 필수입니다. 테스트, 빌드, 배포 자동화로 휴먼 에러를 최소화합니다. 자동화 없이는 어떤 전략도 제대로 작동하지 않습니다.

**원칙 4: 팀 문화 중시**

기술보다 팀의 협업 방식이 더 중요합니다. 모두가 이해하기 쉽고, 실제로 따르기 용이하며, 문제 발생 시 쉽게 개선할 수 있는 전략을 선택하세요.

## 참고

- Vincent Driessen, "A successful Git branching model" (2010) — GitFlow의 원본 제안 블로그 글
- Trunkbaseddevelopment.com — Trunk-based 개발 관련 기술 문서
- GitHub Flow — GitHub 공식 브랜칭 모델 가이드
- 코딩애플 Git 강의: https://codingapple.com/course/git-and-github/