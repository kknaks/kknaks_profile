---
type: concept
id: secret-store
title: 비밀 보관소 — 비밀은 레포 밖, 서버는 자기 신원으로 읽는다 (Secret Store · Key Vault)
aliases:
  - Key Vault
  - 키 볼트
  - 비밀 보관소
  - secret manager
  - 레포 env 금지
  - Key Vault 방화벽
  - Android Keystore
  - Keystore
  - EncryptedSharedPreferences
up:
  - 2026-11-12-prod-deploy-re1
  - 2026-11-09-day-data-architecture
  - 2026-11-16-android-app
tags:
  - 인프라
  - 비밀
  - 보안
  - azure
---

# 비밀 보관소 — 비밀은 레포 밖, 서버는 자기 신원으로 읽는다

DB 비밀번호 · 외부 API 키 · 외부 시스템 주소처럼 **레포에 있으면 안 되는 값**을 클라우드 보관소(Azure Key Vault · AWS Secrets Manager 등)에 두고, 앱은 시작할 때 자기 신원으로 읽어 env 로 쓴다. 레포에는 이름만 남는다.

## 정의

1. **레포에는 이름, 값은 보관소** — 설정 파일은 「무엇이 필요한가」 만 적는다 → [[externalized-configuration]]
2. **환경마다 비밀 한 벌** — dev · prod 가 같은 이름의 다른 값을 갖는다. DAY 는 환경당 6개
3. **읽는 쪽은 신원으로** — VM 의 관리 ID 에 「비밀 읽기」 역할만 준다 → [[workload-identity]]
4. **네트워크로도 닫는다** — 보관소 방화벽을 VM 서브넷만 허용으로 두면, 키가 새도 밖에서는 못 읽는다

## 사용 예시

```text
비밀 넣기(사람):  로컬 IP 를 방화벽에 잠깐 추가 → 비밀 set → 바로 제거
비밀 읽기(서버):  VM 신원 → 보관소(서브넷 허용) → env 로 컨테이너에
```

## 왜 중요한가

- **「비밀이 아닌 줄 알았던 값」 이 새는 길이다** — DAY 는 외부 CRM 주소를 레포 env 파일에 뒀다가 「외부 시스템 주소는 레포에 노출하면 안 된다」 는 지적으로 보관소로 옮겼다. 키만 비밀이 아니다. 상대 시스템의 위치 · 테넌트 정보도 레포 밖이다
- **이미 커밋된 것은 지워지지 않는다** — 보관소로 옮겨도 git 이력에는 남는다. 이력을 다시 쓸지는 따로 판단한다(DAY 는 그대로 두기로 했다). 그래서 처음부터 넣지 않는 것이 싸다
- **로컬 비밀 파일도 같은 규칙** — 관리자 접속 정보 파일이 무시 목록 없이 레포 안에 놓인 적이 있다. 바로 무시 목록 · 권한 600 으로 막고, 레포 밖(`~/.pgpass`)으로 옮긴 뒤 원본을 지웠다

## 경계와 오해

- **보관소 ≠ 저장소 Secrets** — CI 의 Secrets 는 파이프라인이 쓰는 값, 보관소는 실행 중인 서버가 읽는 값이다. 서버 비밀을 CI Secrets 에 두면 배포 때마다 값을 실어 나르게 된다 → [[ci-cd]]
- **방화벽을 연 채로 두지 않는다** — 비밀을 넣으려고 연 로컬 IP 는 바로 닫는다. 열어 둔 예외가 쌓이면 서브넷 제한이 의미를 잃는다
- **값을 출력하지 않는다** — 시작 검사는 「있다 · 없다」 만 말하고 값을 로그에 찍지 않는다 → [[fail-fast]]
- **방화벽 뒤 보관소에는 이미 허용된 경로로 들어간다** — 보관소 방화벽이 VM 서브넷만 받고 내 계정에 방화벽 변경 권한이 없을 때, 방화벽을 여는 대신 그 VM 을 SOCKS 터널(`ssh -D`)로 거쳐 내 토큰으로 REST 를 부른다. 방화벽 · 권한은 그대로다. CLI(`az`)는 SOCKS 를 안 타므로 토큰만 CLI 로 받고 호출은 `curl --socks5-hostname` 으로 한다. 값은 파일에서 표준입력으로만 넘긴다
- **없앤 비밀의 이름은 금지 목록에 남긴다** — 선택 비밀 목록에서 줄을 빼면 「그 이름을 Git 일반 설정에 넣지 못하게 막던 검사」도 같이 풀린다. 더 읽지 않는 이름을 따로 「은퇴한 비밀」로 두어 계속 거절한다

## 함께 보는 개념

- [[workload-identity]] — 보관소를 키 없이 읽는 신원
- [[externalized-configuration]] — 설정을 코드 밖으로 빼는 상위 원칙
- [[ci-cd]] — 파이프라인 쪽 비밀과의 경계
- [[fail-fast]] — 비밀 누락을 시작 때 잡기

## 비밀의 형식이 바뀌는 배포 — 전달 → 확인 → 배포

- 비밀의 **모양**(예: 연동처별 두 줄 → 병원당 한 줄)이 바뀌는 배포는, 새 값을 받을 쪽에 **먼저 전달하고 바꿨다는 확인을 받은 뒤** 보관소 교체와 배포를 같이 한다. 순서를 거꾸로 하면 배포 순간 연동이 전부 401 이 되고, 실패가 쌓여 IP 단위 429 까지 난다(DAY ext 키 · 11-27).
- 새 코드가 옛 모양을 모르는 칸 거부(`extra=forbid`)로 읽으면 **섞인 상태가 없다** — 모양을 같이 바꾸지 않으면 503 이다. 되돌리기 = 보관소 이전 버전 + 이전 이미지.
- 방화벽 뒤 보관소엔 허용된 경로(VM 경유 SOCKS · REST PUT)로 넣는다 · 새 값은 레포 밖 600 파일에만 두고 화면엔 모양(줄 수 · 칸 이름)만.

## 출처

- [[2026-11-09-day-data-architecture]] §2 · §3 — DAY: VM 신원으로 Key Vault 읽기 · 보관소는 VM 서브넷만 · 비밀 넣을 때 로컬 IP 를 잠깐 열고 닫기 · 외부 CRM 주소 레포 env → Key Vault(코드 `1ccc101b`) · 관리자 env 파일 → `~/.pgpass`
- [[2026-11-11-day-app]] §2 — 선택 비밀(채팅 Blob · APNs 키)은 보관소에 없으면 app.env 에 안 넣고 기능만 꺼짐(fail-closed) · 배포는 성공(`scripts/deploy/day_vm.py` OPTIONAL_SECRETS)
- [[2026-11-11-fix]] §2 「방화벽 뒤 비밀 저장소에 허용된 경로로 넣기」 — APNs · Soniox 키를 VM 경유로 Key Vault 에 · `RETIRED_SECRETS`(`be-4-report.md` · `review-doc-3-report.md` W5)
- [[2026-11-12-prod-deploy-re1]] §2 「비밀을 화면에 안 내는 운영 등록」 — 운영 연결 값을 prod 컨테이너 안 `--stdin` 1회로 · 테넌트 id 는 컨테이너에서 받아 로컬 600 파일에만 · 값 파일은 쓰자마자 삭제(`backend/day/register_connection.py` · `be-1-report.md`)
- [[2026-11-27-day-reservation3]] §2 — ext 키 형식 변경 배포 순서 사고 · dev Key Vault VM 경유 교체(§3)

## 모바일 기기 안 — Android Keystore (DAY android-app)

- 앱 세션 묶음(토큰 · 연결 주소 · 만료)을 **AndroidKeyStore 의 AES-256-GCM 키**로 암호화해 앱 전용 prefs 에 암호문 하나로 둔다. 키는 기기 밖으로 꺼낼 수 없고, IV 는 Keystore 가 매번 무작위로 만든다. iOS Keychain `ThisDeviceOnly` 와 같은 자리다.
- Jetpack `EncryptedSharedPreferences` 는 deprecated 라 쓰지 않았다. 플랫폼 API 로 80줄 안팎이면 iOS 구현과 줄 단위로 대조된다.
- **읽기 · 비교 · 삭제(`clearIf`)는 한 직렬 실행기 안에서** 돈다. 사이에 `save` 가 끼면 새 로그인을 지운다. 예외가 나도 답을 꼭 돌려준다 — 안 그러면 호출한 쪽의 로그아웃이 멈춘다.
- 백업 · 기기 이전 대상에서 뺀다(세션이 다른 폰으로 따라가지 않게).
- 출처: [[para/projects/company/day/log/2026-11-16-android-app|android-app 회고]]
