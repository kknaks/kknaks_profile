---
type: decision
id: DEC-007
title: "운영 첫 배포 — 로그인·AX·주소·데이터·데스크톱 두 판"
status: accepted
product: strong-hajin
created_at: 2026-10-01
updated_at: 2026-10-01
tags:
  - product/strong-hajin
  - doc/decision
  - status/accepted
links:
  baselines: []
  decisions:
    - "[[decision-005-tauri-wrapper|DEC-005]]"
  specs:
    - "[[spec-006-tauri-wrapper|SPEC-006]]"
  works: []
  releases: []
  related:
    - "[[runbook-002-production-deploy|RUNBOOK-002]]"
up: []
sources:
  - orchestration/work/strong-hajin-deploy/_RESUME.md
  - orchestration/work/strong-hajin-deploy/research-seed-path.md
  - orchestration/work/strong-hajin-deploy/report-infra-deploy.md
  - orchestration/work/strong-hajin-deploy/report-fe-release-dmg.md
  - orchestration/work/strong-hajin-deploy/report-fe-flavors.md
---

# 운영 첫 배포

2026-09-30 ~ 10-01 에 Strong Hajin 을 Mac Studio k8s 에 처음 올리면서 정한 것을 기록한다.
accepted 는 아래가 **실제로 배포되어 돌고 있다**는 뜻이다. 절차는 [RUNBOOK-002](../70-runbook/runbook-002-production-deploy.md)에 있다.

## Context

DEC-005 가 방향(같은 origin 웹을 Tauri 로 감싼다 · Mac Studio k8s 에 올린다)을 정했지만, 배포를 막는 빈칸이 남아 있었다
(`40-architecture/deploy/environments.md` 의 「아직 배포할 수 없는 이유」 일곱).

- 운영 프로파일에 로그인 수단이 하나도 없었다. 이메일/비밀번호 라우트는 개발 프로파일에서만 등록됐고 외부 로그인은 구현되지 않았다(`research-seed-path.md` §5).
- 운영 프로파일에서 AX 대화가 쓰는 도구 서버(MCP)가 거절됐다(`research-seed-path.md` §4 주 2).
- 운영 DB 에 스키마·카탈로그·유저를 넣는 코드 경로가 없었다(`research-seed-path.md` §2.6).
- 호스트·레지스트리·arm64 이미지·서명이 모두 미정이었다.

사용자 목적(2026-09-30): 「백/프론트 다 올릴거고 k8s 환경임 — 나는 앱 빌드된 것만 사람들한테 배포하고 싶어」.

## Decision

| ID | 결정 | 근거 |
|---|---|---|
| D-01 | **운영 로그인 = 이메일/비밀번호.** 로그인 라우트는 프로파일과 무관하게 등록한다. 개발에만 남는 것은 「바로 로그인」 데모 계정 목록·데모 비밀번호와 `X-Demo-Persona` 이음새다. 쿠키 `Secure` 는 운영에서만 붙는다(종전과 같다) | 사용자 2026-09-30: 「로그인 칸을 만들어야 하는 거 아니야? 개발용이라는 게 말이 돼?」→「응 고쳐」. 코드 PR #5(cdb0f3f) — `settings.local_login_enabled` 삭제 → `demo_shortcuts_enabled`, 운영 로그인 200·Secure·틀린 비번 401 시험 |
| D-02 | **운영 MCP 가드.** 운영 프로파일의 MCP 서버는 AX 한 턴의 도구 서버로 띄워졌을 때(`AX_MCP_CAUSATION_ID` 가 있을 때)만 선다. 이 검사는 「워커가 띄웠다」는 표시이지 인증이 아니다 — 턴 id 를 원장과 대조하지 않으며, 그 프로세스를 띄울 수 있는 쪽은 이미 같은 DB 접속 정보를 갖고 있다 | 사용자: AX 채팅을 운영에서도 쓴다(mediness 처럼). 코드 PR #5. MCP 는 stdio 로만 뜬다(네트워크 입구 없음) |
| D-03 | **운영 호스트 `ax.medisolveai.xyz`.** 호스트 하나에서 `/` 는 프론트, `/api`·WebSocket 은 백엔드 | 사용자 2026-09-30(「medisolveai 가 맞아」). DEC-005 D-08 같은 origin |
| D-04 | **레지스트리 `ghcr.io/kknaksss`.** ~~`ghcr.io/kknaks`~~ 에서 2026-09-30 바뀜 — 이 Mac 의 gh 계정이 `kknaksss` 이고, 레포 협업자 권한으로는 `kknaks` 개인 네임스페이스에 패키지를 올릴 수 없다. 패키지는 private → 클러스터는 `ghcr-pull` 시크릿으로 받는다 | 사용자 2026-09-30 「a 로 가자」. infra PR #5(f04d4cb) · #6(7ba1050, 태그 `cdb0f3f-arm64`) |
| D-05 | **인프라는 회사 org 레포 `MediSolveAIDev/k8s_infra_mac` 에 새 차트·앱으로 더한다.** mediness 파일은 바꾸지 않고, 공유 cloudflared 의 hosts 에 한 줄만 더한다. AppProject `strong-hajin` · ns `strong-hajin-prod` 로 격리한다 | 사용자 2026-09-30 「이게 k8s 레포야」 · 배포 위임. infra PR #5 · AppProject·DNS 승인(`_RESUME.md` §5) |
| D-06 | **운영 데이터 = 로컬 시드 DB 의 dump.** 운영용 적재 명령은 만들지 않았다. 로컬에서 `reset-catalog` → `dataset-import` 한 DB 를 로그인 세션 행만 빼고 dump 해 운영 postgres 에 복원했다 | 사용자 2026-09-30 「운영 방금 만든 시드 쓸 거야」. `report-infra-deploy.md` §6 |
| D-07 | **시드 범위.** 양식은 조직도 전체 9표(조직·직급·직위·직무·사람·보직·추가 소속·직무 배정·로그인)를 받는다. 프로젝트·업무는 유저가 앱에서 만든다. **실제로 넣은 것은 AX 팀 1개와 4명**이다 — CTO 1명은 `executive`, 리더 1명은 `team-lead`, 나머지 2명은 `member`. 입사일은 mediness 기준, 직급·직무는 비웠다 | 사용자 2026-09-30 지시(`_RESUME.md` §2 시드 행 셋) · `reference/2026-09-30-strong-hain-seed/` · 검사 problems 0 |
| D-08 | **AX(AI) = 노드에 설치된 codex·claude 를 읽기 전용으로 마운트 + Strong Hajin 전용 codex 인증.** mediness 와 같은 방식이되 인증 PVC 는 따로 둔다. 인증은 전용 `codex login` 1회로 만들고 mediness·사용자 로컬 `~/.codex` 와 공유하지 않는다 | 사용자 2026-09-30 「맥 스튜디오 호스트에 코덱스 클로드 다 설치되어 있어 — 메디니스 문서 보면 나와」. 호스트 auth.json 복사가 refresh token 만료로 실패한 뒤 전용 로그인(`report-infra-deploy.md` §7·§B) |
| D-09 | **데스크톱 앱 두 판.** 개인판 `Strong Hajin` · `app.stronghajin.desktop` · origin 미정 / 회사판 `medi-ax` · `app.ax.desktop` · `https://ax.medisolveai.xyz`. 지금 배포하는 것은 회사판이다. 판 안에서 identifier 는 바꾸지 않는다(바꾸면 로그아웃) | 사용자 2026-10-01(`_RESUME.md` §2). 코드 PR #8(015bed2) · `report-fe-flavors.md` |
| D-10 | **배포 대상은 서명·공증한 dmg.** 개인 Developer ID 로 서명하고 `AC_NOTARY` 프로필로 공증·staple 한다 | 사용자 2026-09-30 「개인 개발자 서명이 있어 — deskdeck 앱 만들 때 넣었어」. `report-fe-release-dmg.md` · `report-fe-flavors.md` §6 |
| D-11 | **화면 워드마크 `MEDISOLVE`.** 탭 제목·사이드 로고·로그인 화면 워드마크·안내문과 로그인 칩(`M`)을 바꿨다. CSS 이름(`--scax-*`·`.scax-*`)·코드 식별자·주석은 그대로 둔다 | 사용자 지시(writer 3차, 2026-09-30 · 칩 `SC`→`M`). 코드 PR #5 |

## Rationale

- 로그인(D-01): 외부 로그인을 붙일 때까지 운영에 들어올 길이 없는 상태는 배포를 막는다. 이메일/비밀번호 경로는 이미 개발에서 쓰이던 같은 코드이고, 위험한 것은 로그인이 아니라 개발 전용 지름길(공용 데모 비밀번호 목록·헤더 이음새)이므로 그것만 개발에 묶었다.
- MCP 가드(D-02): 예전 가드(개발 전용)는 운영에서 AX 를 막을 뿐 데이터를 지키지 못했다. 도구 서버를 띄우는 AI CLI 가 이미 DB 접속 정보를 환경으로 받기 때문이다. 그래서 가드는 「워커가 턴을 위해 띄운 경우」로 좁혔다.
- 데이터(D-06): 운영 적재 명령을 새로 만들면 가드·멱등성·파괴 범위를 새로 설계해야 한다. 4명 시드는 로컬에서 이미 검사·로그인 확인이 끝났으므로 그 DB 를 그대로 옮기는 편이 확인된 상태를 그대로 싣는다.
- 전용 codex 인증(D-08): codex 는 쓸 때마다 refresh token 을 돌린다. 같은 토큰을 두 곳에서 쓰면 한쪽이 다른 쪽을 끊는다. 실제로 호스트에서 복사한 인증은 이미 만료돼 있었다.

## 근거 개념

없음 — 이 제품의 배포 조건과 사용자 지시에 따른 적용 결정이다.

## Scope

- In: 운영 로그인 경로, 운영 MCP 가드, 운영 이미지(`deploy/k8s/`), 차트·Argo 앱, 시드 복원, AX·STT·회의실 연결, 회사판 dmg 서명·공증.
- Out: 외부 로그인(OIDC), 운영 적재 명령, 로그인 시도 제한, GitHub Releases 발행, Windows 설치파일, Argo automated sync, 백업 정책.

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| OQ-D7-01 | 로그인 시도 제한(무차별 대입 방어)을 둘 것인가 — 지금 없다 | 사용자·코디 | 다음 세션(고도화) |
| OQ-D7-02 | M-5: 서명본을 설치한 뒤 로그인 → 종료 → 재실행에서 로그인이 유지되는가 | 사용자 | 실기 확인 후 preflight 증거에 기록 |
| OQ-D7-03 | 개인판의 운영 origin | 사용자 | 정해지기 전까지 개인판은 「서버 주소가 설정되지 않았습니다」 |
| OQ-D7-04 | 운영 DB 에 실명·회사 메일이 들어 있다 — 보관·백업·접근 정책 | 사용자 | 백업 정책(배포 설계 D-5)과 함께 |
| OQ-D7-05 | 노드 codex 0.146 을 올릴 것인가(기록 필드가 빈다). mediness 와 공유 자원이다 | 사용자 | — |
| OQ-D7-06 | GitHub Releases 발행과 `60-release` 기록(DEC-005 D-09) | 사용자·코디 | 다음 릴리스 때 |

## Resulting Spec

이 결정의 일부는 SPEC-006(데스크톱 래퍼)의 미결을 닫는다 — 운영 주소·인증 경로(OQ-T02)와 서명·공증(OQ-T03 일부). SPEC 본문 갱신은 이 문서의 범위가 아니다.
