---
type: work
id: WORK-006
title: "W6 — 데스크톱 래퍼: 먼저 재고, 그 다음에 감싼다"
status: in_progress
product: strong-hajin
work_type: new-feature
owner: kknaks
roles:
  pm: kknaks
  design: kknaks
  fe: kknaks
  be: kknaks
  qa: kknaks
  ops: kknaks
progress: 0
created_at: 2026-09-22
updated_at: 2026-09-22
tags:
  - product/strong-hajin
  - doc/work
  - status/in_progress
links:
  baselines: []
  decisions:
    - "[[decision-005-tauri-wrapper|DEC-005]]"
  specs:
    - "[[spec-006-tauri-wrapper|SPEC-006]]"
  works: []
  releases: []
  related: []
---

# W6 — 데스크톱 래퍼: 먼저 재고, 그 다음에 감싼다

배포된 HTTPS 웹을 여는 데스크톱 창 하나와, 그 창이 웹에게 주는 **네이티브 커맨드 넷**을 만든다.
보장하는 것은 하나다 — **회의를 녹음하는 동안 이 기기가 자동으로 잠들지 않는다.**

**만들지 않는 것**: 화면(웹의 것 그대로) · 알림 시스템 · 시스템 오디오 캡처 · 트레이 상주 ·
인증 방식 전환 · 녹음 일시정지 기능.

> 1 파일 = 1 work = **빌드 계획**. SPEC-006 의 외부 계약 본문을 복제하지 않고 `links.specs` 로 연결한다.
> 이 문서가 더하는 것은 **순서 · 소유 · 증거 · 게이트**다.

> **이 work 의 첫 실행 단계는 구현이 아니라 계측이다.** SPEC-006 §6 이 「실물에서만 답이 나는 것」
> 열다섯을 세어 두었고, 그중 하나(M-2 녹음 포맷)는 **답에 따라 이 work 자체가 멈춘다.**
> 그래서 Phase 1~2 가 먼저 서고, Phase 2 끝에 **진행 / 보완 / 중단** 판정이 있다.

---

## Meta

- **Baseline**: 없음 (frontmatter `links.baselines` 비어 있음) — DEC-005 가 사용자 대화에서 직접
  방향을 확정했고 그 앞 단계 baseline 문서를 만들지 않았다. SPEC-006 §1 Meta 와 같다.
- **Covers spec**: SPEC-006 **v0.2.3** (frontmatter `links.decisions`·`links.specs` 와 일치)
- **Depends on work**: **코드 접점이 있다.** `frontend/src/App.tsx` 와 `frontend/src/lib/labels.ts` 는
  WORK-005 가 이미 바꾼 파일이고, 이 work 의 Phase 4 가 **같은 두 파일을 다시 연다**.
  2026-09-22 17:50 KST 읽기 전용 확인: 코드 워크트리 `…/Strong_hajin/strong-hajin-projects` ·
  branch `kknaksss/strong-hajin-projects` · HEAD `a1f6791` · clean ·
  `git log --oneline origin/main..HEAD` = **`a1f6791` 한 건(미머지)** ·
  `git diff --stat origin/main..HEAD` 에 `App.tsx +35` · `labels.ts +126`.
  ⚠ **이 머지 상태는 관측값이지 고정된 사실이 아니다** — 발주 시점에 다시 센다.
- **작업 단위와 워크트리** — 런북 §1 고정 규칙
  - **런북 §1 대로 같은 작업 단위의 기존 코드 워크트리·브랜치에 이어 쌓는다** —
    `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects` · `kknaksss/strong-hajin-projects`.
    **WORK 번호가 늘었다는 이유로 새 워크트리·새 브랜치를 만들지 않는다**(「WORK 번호는 작업 단위가 아니다」).
  - **새 워크트리는 사용자가 새 코디 세션을 띄울 때만 생긴다.** 그때 base 는 **WORK-005 의 코드를
    포함해야 한다** — `origin/main`(머지된 뒤) 또는 `kknaksss/strong-hajin-projects`.
    `config/projects/strong-hajin.json` 의 code repo `base` 는 `origin/main` 이라,
    **미머지 상태에서 `new-work.sh` 를 돌리면 `a1f6791` 이 없는 트리가 뜬다**
    (런북 §1 이 기록한 2026-09-05 사고와 같은 형태).
- **Parallel work**: WORK-004 · WORK-005 의 2루프와 **같은 워크트리를 쓴다.** 접점은
  `App.tsx` · `labels.ts` · `features/meetings/` 이고, 이 work 가 거기 더하는 것은 **호출 배선 몇 줄**이다.
  **같은 브랜치에 이어 쌓으므로 브랜치 간 충돌이 생기지 않는다** — 대신 **순서는 코디가 정한다**
  (동시에 같은 파일을 여는 워커를 두 개 태우지 않는다).
- **Follow-up work**: ① 알림 시스템(별도 decision + spec — SPEC-006 §2.5) ② 녹음 포맷 후보 도입
  (**조건부** — Phase 2 의 M-2 결과가 「안 열린다」일 때만, OQ-T07) ③ 반복 배포 절차(`70-runbook`) ·
  배포 구조(`40-architecture/deploy`) · 릴리즈 노트(`60-release`)
- **External dependency**
  - **Tauri v2** (하한 `2.11.1` — GHSA-7gmj-67g7-phm9). 참조 제품은 `2.11.3`
  - **절전 방지 API**: macOS `IOPMAssertionCreateWithName` / Windows `SetThreadExecutionState`.
    **공식 Tauri 플러그인이 없다** — 직접 짜거나 커뮤니티 크레이트를 고른다(Phase 3 이 결정)
  - **운영 쿠버네티스**: `MediSolveAIDev/k8s_infra_mac`(Mac Studio · 전 노드 arm64 · ArgoCD 는 `main` 추적).
    **기본안은 이 레포를 그대로 쓰는 것**이다 — 클러스터와 ArgoCD 가 이미 이 레포를 본다.
    남는 쟁점은 「**회사 org 레포에 개인 제품 구성을 발행해도 되는가**」 하나이고, 그것은
    **실제로 푸시·PR 하는 시점**의 확인 사항이다 (OQ-W02). 계획·로컬 작성·검증은 막지 않는다
  - **GitHub Releases**: 코드 레포 `kknaks/Strong_hajin` (DEC-005 D-09)
  - **Windows 실기**: 보유 여부 미확인 — OQ-W01. **없으면 Windows 축은 「검증 불가」로 남는다**

### 계약 불변식 — 어느 Phase 도 이것을 바꾸지 않는다

SPEC-006 이 v0.2.0 ~ v0.2.1 두 판에 걸쳐 닫은 구조다. 구현 편의로 되돌리면 **이 work 가 막으려는
사고(녹음 중 절전 방지가 스스로 풀린다)를 다시 연다.** 여덟 줄 전부 Phase 3·4 의 「하지 말 것」에 박는다.

| # | 불변식 | 어디서 왔나 |
|---|---|---|
| **I-1** | 절전 방지 점유의 수명을 **네이티브가 소유**한다 | SPEC §4 「왜 TTL 을 버렸나」 |
| **I-2** | 커맨드는 **넷**이다 — `shell_info` · `wake_guard_acquire` · `wake_guard_release` · `open_external` | SPEC §4 |
| **I-3** | **TTL · 주기적 갱신 · 참조계수를 두지 않는다.** 신호가 안 온다고 풀지 않는다 | SPEC §5 점유의 안전성 |
| **I-4** | 해제는 **«완료» 사건에만** 붙는다 — 요청 단계에서 취소되면 아무것도 풀지 않는다 | L-06 · L-09 · L-11 |
| **I-5** | **취소된 창 닫기는 점유를 보존한다** (`계속 녹음` 을 골랐는데 풀리면 실패) | AC-T36 · `E-12` |
| **I-6** | `degraded` 탈출은 **사건 기반 재무장**이다 — «거는» 방향이지 «푸는» 방향이 아니다 | `E-09` · L-14 |
| **I-7** | **늦게 도착한 획득의 최종 잔존은 0** 이다. 수단은 구현이 고르고 영구 기록을 강제하지 않는다 | AC-T40 · AC-T41 |
| **I-8** | **웹이 살아 있는 채로 멈추면 점유가 남는다** — 이 한계를 「자동 정리된다」로 고쳐 쓰지 않는다 | L-12 · OQ-T08 |

---

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner | kknaks |
| Status | todo |
| Progress | 0% |
| Branch/PR | **기존 작업 단위를 잇는다** — 워크트리 `…/Strong_hajin/strong-hajin-projects` · 브랜치 `kknaksss/strong-hajin-projects` (런북 §1). 새 워크트리를 만들지 않는다 |
| Blocker | 없음 (Phase 1~2 는 미결과 무관하게 착수 가능) |
| Next | Phase 1 — 계측 기반(https fixture + 탐침 셸) 발주. **Phase 6a(운영 설계)는 병행 가능** |

## Role Assignment

**실측이 있는 work 라 「누가 잰다」가 역할의 절반이다.**
**코드·설정·빌드·배포는 워커가 하고 코디가 발주·검증한다 — 사용자에게 명령을 떠넘기지 않는다.**
사용자가 하는 것은 **① 승인 ② 기기 앞에서만 되는 실기 관찰**(절전·덮개·장시간·설치 화면) 둘이다.

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks(코디) | 범위·게이트 판정·미결 승격 | todo |
| Design | — | **새 화면이 없다.** U-2·U-3 두 문구는 SPEC 이 확정했다 | todo |
| FE | `frontend` 워커 | `frontend/` 전부 — **`frontend/src-tauri/` 포함**(셸도 이 경로 아래다) | todo |
| BE | `backend` 워커 | **Phase 5 까지 0줄.** Phase 6b 에서 **운영 프로파일 내부 정리와 arm64 운영 이미지**를 구현한다 — **권한 완화·새 인증이 필요해지면 거기서 멈추고 올린다**(OQ-W05) | todo |
| QA | 코디 + **사용자** | 설정·코드 검사와 fixture 측정은 코디, **실기 관찰(절전·덮개·장시간)은 사용자** | todo |
| Ops | 코디(발주·검증) + **인프라 워커**(P-5 해소 — `roles/strong-hajin/infra`) | 6a 배포 설계 · 6b 차트·Application·values 실물과 배포 실행 · 9 릴리즈 절차. **배포와 Release 발행은 승인 범위 안에서** | todo |

> **워커 설정 갱신이 필요하다.** `orchestration/config/projects/strong-hajin.json` 의 `frontend` 워커
> `verify` 에 **Rust 쪽 검증 명령이 없다**(`cargo check`·`cargo clippy`·`npm run tauri build`).
> `allowed_paths` 는 `frontend/` 라 `src-tauri/` 를 이미 덮는다 — **새 워커 유형은 필요 없다.**
> 갱신은 코디 몫이고 이 문서가 고치지 않는다.

---

## Scope

**포함**

- Tauri 셸 본체: 창 하나 · 원격 운영 주소 열기 · 커맨드 넷 · 네비게이션/커맨드 허용 목록 둘 ·
  연결 실패 화면(U-2) · 절전 방지 네이티브 구현(macOS·Windows)
- 웹 최소 배선: 셸 존재 판정 · 점유 획득/해제 호출 · 사건 기반 재확인 1회 · U-3 한 줄(녹음 두 화면) ·
  외부 링크를 셸로 넘기는 자리 · 회의 라이브의 **세션 키 생성**
- **실측 15건**(M-1 ~ M-14 + M-2b)의 계획·실행·기록. **같은 ID 안에서 fixture 증거와 제품판 증거를 가른다**
- **운영 배포 — 설계(6a)와 실행(6b) 둘 다.** FE 정적 서빙 배선 · 같은 origin API·WS 라우팅 ·
  arm64 운영 이미지 · 차트·Application·values **실물 작성** · **배포 실행** ·
  기존 권한·쿠키 계약을 유지하는 **운영 프로파일 내부 정리** · rollback · 기존 Mediness 와의 분리
- 설치파일 빌드 환경 · fixture 판 검증 · **운영 origin 판 최종 빌드와 그 아티팩트의 검증** ·
  Release 발행 · 버전/태그/기록 · 서버 배포와 셸 배포의 호환 순서

**제외** — 어디로 가는지까지 적는다

| 제외 | 어디로 |
|---|---|
| 알림 시스템(이벤트·푸시·트레이·배지·딥링크 클릭) | **별도 decision + spec.** SPEC-006 §2.5 가 경계만 그었다 |
| 시스템 오디오 캡처 | 만들지 않는다 (DEC-005 Scope Out) |
| 인증 방식 전환(키체인·Bearer) | 만들지 않는다 (D-02) |
| 녹음 일시정지·재개 **기능 신설** | 제품에 없다. 생기면 L-15 가 발효 (OQ-T05) |
| 녹음 포맷 후보 도입(fallback) | **조건부 후속** — Phase 2 의 M-2 가 「안 열린다」일 때만 (OQ-T07) |
| 세션 만료를 열린 스트림·화면에 전파 | 지금 동작이 아니다. 원하면 별도 결정 (OQ-T11) |
| 운영 프로파일의 **권한 완화**(로컬 로그인 개방 등)와 **새 인증 방식 도입**(외부 IdP·OIDC) | **새 제품 계약이다 — 별도 decision.** OQ-W05. ⚠ **운영 프로파일의 «내부 정리»는 제외가 아니라 포함**이다 — 기존 권한 판정·쿠키 계약·HTTPS 운영을 **그대로 둔 채** PRODUCTION 에서 같은 표면이 서게 하는 변경은 Phase 6a 가 설계하고 6b 가 구현한다. **development/test 프로파일로 운영하는 우회는 금지**(SPEC §5) |
| 반복 배포 절차서 · 배포 구조 문서 · 릴리즈 노트 | `70-runbook` · `40-architecture/deploy` · `60-release`. 이 work 는 **무엇을 남길지**만 정한다 |

---

## Code Surface

### 기준 — 조회 시각과 HEAD

| 대상 | 경로 | branch | HEAD | dirty | 조회 |
|---|---|---|---|---|---|
| 적용 코드 | `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects` | `kknaksss/strong-hajin-projects` | `a1f67915aa8eeb551327b858428c5d4c1519e1b4` | **0건 (clean)** | 2026-09-22 17:33 KST |
| 참조 Tauri | `/Users/kknaks/git/toy_pr2/task_management` | `main` | `a720b6ef` | 0건 | 2026-09-22 17:31 KST |
| 인프라 | `/Users/kknaks/git/harness_works/k8s_infra_mac` | — | 읽기 전용 조회 | — | 2026-09-22 17:32 KST |

> ⚠ **조사 문서의 기준 HEAD 와 다르다.** `tauri-implementation-research.md` 는 `e46ce39c`(dirty 69~72)
> 를 읽었고, 지금은 **`a1f6791` 이 깨끗하다.** 이 문서가 인용한 좌표는 **`a1f6791` 에서 다시 확인했다**
> (아래 표의 줄 번호는 전부 이번 확인값). 구현 착수 시점에 또 움직일 수 있으므로 워커는 다시 센다.

### 신규로 생기는 것 — `frontend/src-tauri/` 전부

**지금 코드 레포에 Tauri 가 하나도 없다.** `find . -name 'Dockerfile*'` 이 `delivery/Dockerfile` 하나,
`frontend/` 아래 `src-tauri` 0건. 참조 제품의 `app/front/src-tauri/` 와 **같은 자리**(프론트 아래)에 만든다.

| 경로 (신규) | 역할 | 참조 제품의 대응 |
|---|---|---|
| `frontend/src-tauri/tauri.conf.json` | 제품명·식별자·창 하나·번들 타깃. **`csp` 를 박지 않는다**(원격 문서는 서버 헤더가 정한다) | `app/front/src-tauri/tauri.conf.json` — CSP 절만 **계승하지 않는다** |
| `frontend/src-tauri/Cargo.toml` | `tauri >= 2.11.1`. `keyring` 은 **가져오지 않는다**(D-02) | 같은 파일 — `keyring` 줄만 제외 |
| `frontend/src-tauri/src/lib.rs` | 커맨드 넷 · 창 수명 훅 · 절전 방지 · Windows 마이크 권한 | 같은 파일 — `allow_microphone_on_webview2` 만 계승 |
| `frontend/src-tauri/capabilities/*.json` | **`remote.urls` = 운영 origin 정확히 하나** | 참조는 `core:default` 만 — **원격 설정이 없다.** 이번에 새로 쓴다 |
| `frontend/src-tauri/Info.plist` | `NSMicrophoneUsageDescription` | **계승**(문구는 이 제품 것으로) |
| `frontend/src-tauri/Entitlements.plist` | `com.apple.security.device.audio-input` | **계승** |
| `frontend/src-tauri/icons/` | 아이콘 세트 | **자리만 계승** — 실제 아이콘은 이 제품 것 |
| `frontend/src/lib/shell.ts` | 셸 존재 판정 + 커맨드 넷의 유일한 호출 자리 | 없음 (신규) |

### 기존 파일 중 만지는 곳 — 전수

| 경로:줄 (a1f6791 기준) | 지금 | 이 work 가 더하는 것 |
|---|---|---|
| `frontend/package.json` | Tauri 의존성 0건 | `@tauri-apps/api` · `@tauri-apps/cli` devDependency + `"tauri"` 스크립트 |
| `frontend/src/features/meetings/stream.ts:251` | `startMicrophone(...)` 호출 — **회의 라이브에서** 마이크가 열리는 유일한 자리(제품 전체로는 둘이다 — `microphone.ts:31` 과 `browser/liveTranscription.ts:11` 이 각각 `getUserMedia` 를 부른다) | **L-01 획득**. 이 회차의 **세션 키를 여기서 만든다** |
| `frontend/src/features/meetings/stream.ts:258` | 실패 시 `micDenied: true` | **L-03 — 획득하지 않는다**(더할 것 없음을 확인하는 자리) |
| `frontend/src/features/meetings/stream.ts:317-319` | `onClosed` → `microphone?.stop()` | **L-02 해제** |
| `frontend/src/features/meetings/stream.ts:322` | `closure.kind === "taken"` → `setTakenOver(true)` | **L-05 해제**(자리를 뺏겼다) |
| `frontend/src/features/meetings/stream.ts:327-331` | effect cleanup — `microphone?.stop(); socket.close()` | **L-10 해제**(화면을 떠난다) · **L-14 재확인**의 짝 |
| `frontend/src/features/meetings/stream.ts:234` | `effectiveRole` — `subscribe` 로 내려가는 자리 | **L-04 — 구독은 획득하지 않는다** |
| `frontend/src/features/meetings/MeetingDetailPage.tsx:932` | `{stream.micDenied && <StatusNote tone="danger">…}` | **U-3 이 붙는 자리.** 같은 자리·같은 세기 |
| `frontend/src/lib/labels.ts:772` | `micDenied` 문구 | U-3 문구 **둘**(절전 실패 · 정리 실패)을 같은 자리에 |
| `frontend/src/features/browser/BrowserRecordingPage.tsx:13` | `const [captureId] = useState(() => crypto.randomUUID())` | **이미 회차마다 새 값이다** — 세션 키로 **그대로 쓴다**(AC-T42 의 절반이 이미 만족) |
| `frontend/src/features/browser/BrowserRecordingPage.tsx:47-70` | `start()` | **L-07 획득** |
| `frontend/src/features/browser/BrowserRecordingPage.tsx:71-102` | `stop()` · `interrupt()` · `:30-44` 폴링 | **L-08 해제**(업로드 완료·취소·실패·재시도 중단) |
| `frontend/src/features/browser/BrowserRecordingPage.tsx:22-27` | `beforeunload` 가드 | **M-6 의 대상.** 앱 창 닫기에서 도는지 재고, 안 돌면 셸이 낸다 |
| `frontend/src/features/browser/BrowserRecordingPage.tsx:5-8` | 상태 라벨 여덟 | **U-3 이 붙는 둘째 자리** |
| `frontend/src/App.tsx:684` | `window.open(resource.origin, "_blank", …)` | 셸이 있으면 `open_external` 로. **없으면 지금 그대로** |
| `frontend/src/App.tsx:401` | `window.history.replaceState(...)` | **건드리지 않는다.** L-11 — 해제 트리거가 아님을 셸 쪽에서 지킨다 |

### 세어서 **안** 건드리는 자리

| 자리 | 왜 안 건드리나 |
|---|---|
| `frontend/src/lib/api.ts` — `fetch(` **9곳** (`:103` `:118` `:127` `:277` `:568` `:1022` `:1099` `:1346` `:1371`) | 전부 상대경로 + `same-origin`. 방향 A 에서 **한 줄도 안 바뀐다** |
| `frontend/src/features/meetings/stream.ts:70-74` — WS 주소 조립 | `window.location.protocol/host` 기반. https 로 열면 자동으로 `wss:` |
| `frontend/src/features/meetings/microphone.ts` | **포맷을 바꾸지 않는다.** M-2 결과가 「안 열린다」면 그것은 **별도 후속**(OQ-T07) |
| `backend/` 전부 | **Phase 5 까지 0줄.** 6b 의 **내부 정리**(권한 불변)만 열리고, 권한 완화·새 인증은 별도 결정(OQ-W05) |
| `docs/unified-operations-inventory.json` | HTTP 시그니처·도구 수가 안 바뀐다. **drift 0 이 기준** |
| `delivery/Dockerfile` | 납품용 `linux/amd64` 보호 이미지다. **운영용은 별개로 만든다**(OQ-W03) |

### 인프라 쪽 — 다른 레포다

| 경로 | 지금 | 이 work 가 제안하는 것 |
|---|---|---|
| `k8s_infra_mac/charts/mediness/templates/ingress.yaml` | front·api·mcp **세 호스트** | **그대로 둔다.** Strong Hajin 은 **한 호스트 + 경로 분기**가 필요하다(같은 origin) |
| `k8s_infra_mac/argocd/applications/*.yaml` | 레포 Application **9개**(2026-09-22 클러스터 조회는 **10개**) — `grep targetRevision` 결과 **9개 전부 `main`**, 비-`main` 0건 | 새 Application 도 **`main` 추적**을 기본안으로 (README 의 `k8s-test` 설명은 실물과 다르다) |
| `k8s_infra_mac/charts/strong-hajin/` · `argocd/applications/strong-hajin-prod.yaml` (신규) | 없음 | **Phase 6a 가 설계하고 6b 가 실물로 쓴다.** 이 레포를 쓰는 것이 기본안이고, 남는 쟁점은 **푸시·PR 시점의 org 범위 확인** 하나다 (OQ-W02) |

---

## Domain / Schema

**해당 없음.** SPEC-006 §4 Data Contract 그대로 — **이 work 가 만드는 저장 데이터가 없다.**
점유는 앱이 도는 동안만 메모리에 산다.

- 상태 / invariant: 창 단위 `off` / `on` / `degraded`. 세는 카운터가 아니라 **세션 키의 집합**이다
- Migration 필요 여부: **없다.** 테이블·컬럼·인덱스가 하나도 늘지 않는다
- SPEC 에 환류해야 하는 enum 변경: **없다.** 회의 상태 여섯·녹음 요청 상태 여덟은 기존 것을 그대로 쓴다
- ⚠ **운영 배포(Phase 6a·6b)에서는 새 데이터베이스가 필요하다** — 기존 `mediness` 네임스페이스의
  Postgres 를 공유하지 않는다. 이것은 스키마 변경이 아니라 **배치**의 문제이고 6a 가 설계·6b 가 세운다

---

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| 알림 시스템(후속) | `shell_info().features` | 알림 기능이 생기면 `features` 에 이름 하나가 는다. **`shell_api` 를 올릴지는 그때 판단** |
| 녹음 포맷 후속(조건부) | M-2 측정 결과 | 「안 열린다」면 FE 선언 · STT 설정 · 원본 저장 확장자 **셋이 함께** 움직인다 |
| `70-runbook` / `40-architecture/deploy` / `60-release` | Phase 6a~9 의 산출 | 절차·구조·결과를 각각 받는다. **이 work 는 원료와 첫 실행을 만든다** |

**선행 의존 (이 work 밖에서 와야 하는 것)**

| 필요한 것 | 주인 | 없으면 막히는 Phase |
|---|---|---|
| 운영 도메인 | 사용자 (OQ-T02) | **6b 의 ingress·DNS · 8 · 9** |
| 최소 OS · CPU 아키텍처 · 설치파일 형식 | 사용자 (OQ-T01) | **7 · 8 · 9** |
| 배포 대상 · 서명 · 공증 · 자동 업데이트 범위 | 사용자 (OQ-T03) | **9**(발행) · 8 의 서명본 검증 |
| Windows 실기 | 사용자 (OQ-W01) | **2 · 5 · 7 · 8 의 Windows 축** |
| 회사 org 레포에 개인 제품 구성을 발행해도 되는가 | 사용자 (OQ-W02) | **6b 의 「외부 레포 푸시·PR」 한 지점** — 설계·로컬 작성·검증은 막지 않는다 |
| **권한 완화 · 새 인증 방식** 이 필요해졌을 때만 | 사용자 (OQ-W05) | **그 변경 자체.** 기존 계약을 유지하는 내부 정리는 **막지 않는다** |

**Phase 1 ~ 5 의 macOS 축은 위 어느 것에도 막히지 않는다.** 전부 개발 fixture(로컬)에서 돈다.
**Windows 축은 OQ-W01 에 매인다** — 실기가 없으면 Phase 2·5 의 Windows 절반이 「검증 불가」로 남는다.

---

## Internal Interface Contract

SPEC-006 §4 가 **외부 계약**(커맨드 넷의 이름·인자·응답·에러)을 갖는다. **여기 적는 것은 책임의 배치**다 —
어느 파일이 무엇을 소유하는지. 계약 본문을 복제하지 않는다.

| 책임 | 소유 파일 | 규칙 |
|---|---|---|
| 셸 존재 판정 | `frontend/src/lib/shell.ts` | **여기 한 곳.** 전역 유무로 판정하고, 없으면 **단 한 번도 호출하지 않는다**(`E-01`) |
| 커맨드 넷의 호출 | `frontend/src/lib/shell.ts` | **`shell.ts` 밖에서 `invoke` 를 부르지 않는다.** `api.ts` 밖 `fetch` 금지 규칙과 같은 결 |
| 세션 키 생성 — 회의 라이브 | `stream.ts:251` 부근 | 마이크를 여는 **회차마다 새 값**. 회의 id 를 쓰지 않는다(`E-08`·`E-09` 의 보호가 사라진다) |
| 세션 키 생성 — 브라우저 인터랙션 | `BrowserRecordingPage.tsx:13` | **이미 있다**(`crypto.randomUUID()`). 새로 만들지 않는다 |
| 점유 상태 → 화면 | `MeetingDetailPage.tsx:932` · `BrowserRecordingPage.tsx:5-8` | **마지막으로 확인된 상태**를 보인다. 한 번 뜨고 마는 알림이 아니다 |
| 점유의 수명 | `src-tauri/src/lib.rs` | 창 단위. **L-06·L-09·L-13 셋만 네이티브가 정리한다** |
| OS 절전 방지 호출 | `src-tauri/src/lib.rs` | macOS `…PreventUserIdleSystemSleep` · Windows `ES_CONTINUOUS \| ES_SYSTEM_REQUIRED`. **화면 켜는 플래그를 넣지 않는다** |
| 허용 목록 둘 | `capabilities/*.json`(커맨드) · `lib.rs` 의 네비게이션 훅 | **서로 다른 목록이다.** 같은 것으로 다루지 않는다 |

> ⚠ **Windows 의 실행 상태는 스레드에 매인다** — `SetThreadExecutionState` 는 호출한 스레드의 요구를
> 바꾼다. **걸고 푸는 것이 같은 스레드**여야 한다. 커맨드 핸들러가 어느 스레드에서 도는지에 따라
> 전용 스레드 또는 직렬 채널이 필요하다. **이것은 SPEC 의 계약이 아니라 구현 규칙**이고, Phase 3 이 정한다.

---

## Execution

각 Phase 의 상태는 `TODO / IN_PROGRESS / DONE / BLOCKED / SUPERSEDED` 중 하나다.
Phase 별 `완료 기준`이 완료 조건이고, **이 문서에서 검증 완료를 미리 체크하지 않는다.**

### 단계 순서 — 계측이 먼저, 그러나 순환은 없다

```text
Phase 1 ──▶ Phase 2 ══[판정: 진행 / 보완 / 중단]══▶ Phase 3 ──▶ Phase 4 ──▶ Phase 5
 계측기반      1차 실측 10건                          제품 셸      웹 배선      통합 재측정 4건
 (탐침 셸)     (fixture)                                                        + 인수조건 실행
                                                          │
                          Phase 6a ──▶ Phase 6b ──────────┴──▶ Phase 7 ──▶ Phase 8 ──▶ Phase 9
                          운영 설계     운영 «실행»              설치 빌드     운영 origin   Release
                          (결정·구성안) (실물·이미지·배포)        fixture 판    최종 빌드     발행
                                                                 + M-10        + 검증
```

**실행 순서는 번호 순이다** — `1 → 2 → 3 → 4 → 5 → 6a → 6b → 7 → 8 → 9`.
6a·6b 는 Phase 3·4 와 **병행 가능**하고(파일이 안 겹친다), **6b 의 배포 실행 이후로는 순서**다.

**순환을 만들지 않는 법 — 명시한다.**

- Phase 1 의 **탐침 셸은 계측 수단이지 제품 셸이 아니다.** 폐기해도 되고 Phase 3 이 흡수해도 된다.
  **「제품 셸이 서야 잴 수 있다」는 의존을 만들지 않으려고** 따로 세운다
- 그래서 **모든 실측이 셸 구현 전에 끝나야 한다는 요구는 없다.** 열다섯 중 **열**은 Phase 2 에서
  탐침으로 떨어지고, **넷**(M-11 ~ M-14)은 제품 배선이 있어야 재므로 **Phase 5 로 간다**.
  **하나**(M-10)는 설치파일 두 판이 있어야 재므로 **Phase 7** 이다
- **운영 주소를 실재하게 만드는 것은 Phase 6b 다.** 설계(6a)와 실행(6b)을 갈라서,
  「운영 주소가 있어야 하는 Phase 」가 **주인 없는 선행**에 매달리지 않게 한다
- **발행판의 설정을 사후에 고치지 않는다.** Phase 8 이 **운영 origin 을 박고 최종 빌드까지 한 뒤
  그 아티팩트를 검증**하고, Phase 9 는 **그 아티팩트를 그대로 발행**한다. Phase 7 이 낸 fixture 판은
  **발행 대상이 아니다** — M-10 과 AC-T35 를 재는 판이다
- **Phase 2 가 중단 판정을 내면 Phase 3 이후가 서지 않는다.** 그때 열리는 것은
  「포맷 후보 도입」이라는 **다른 work** 다

> **이 문서를 쓴 워커의 실행 금지는 Phase 1~9 에 적용되지 않는다.** 계획 단계에서 코드·빌드·배포를
> 하지 않은 것은 **문서 워커의 제약**이고, **구현 Phase 의 워커는 자기 범위 안에서 실행한다.**
> 사람이 아니라 워커가 코드를 쓰고, 코디가 발주·검증한다 — **사용자에게 명령 실행을 떠넘기지 않는다.**
> 사용자가 하는 것은 ① **승인** ② **기기 앞에서만 되는 실기 관찰**(절전·덮개·장시간·설치 화면) 둘이다.

---

### Phase 1 — 계측 기반: 개발 fixture 와 탐침 셸

- **Status**: DONE
- **소유**: `frontend` 워커 (탐침 셸·계측 페이지) + 코디 (fixture 기동·기록)
- **파일 범위**: `frontend/src-tauri/**` (신규) · `frontend/package.json` ·
  `frontend/src/dev/` 아래 계측용 페이지 하나. **`frontend/src/features/` · `frontend/src/lib/api.ts` ·
  `backend/` 를 건드리지 않는다**
- **입력**: SPEC-006 §4·§5 · `tauri-implementation-research.md` §3·§4 · 참조 제품
  `app/front/src-tauri/` (읽기 전용)
- **출력**: ① 로컬에서 띄우는 **탐침 셸** ② 커맨드 넷의 **최소 구현**(계약은 SPEC 대로, 화면은 없다)
  ③ **계측 페이지 하나** — `isTypeSupported` · 커맨드 왕복 · 네비게이션 훅 로그 · 장시간 녹음 버튼
  ④ **fixture 둘** — **https fixture**(M-1 의 원격 origin 판정용)와 **평문 `localhost` 스택**(마이크·녹음용)
- **설명**: Phase 2 가 **무엇으로 재는지**를 만든다. 제품 화면을 아직 건드리지 않는다.

**작업**

1. `frontend/src-tauri/` 를 세운다 — 참조 제품의 **번들 구성·아이콘 자리·플랫폼별 설정 자리만** 계승하고,
   **`keyring` 의존성과 `csp` 절은 가져오지 않는다.**
2. `tauri.conf.json` — 제품명·**Strong Hajin 소유 식별자**(참조와 겹치지 않는다) · 창 하나.
   **원격 주소를 여는 형태**로 잡는다. 개발 단계의 주소는 로컬 fixture 다.
3. `capabilities/` 에 **원격 origin 을 하나만** 넣는다. 개발 단계에서는 **로컬 https fixture 의 origin**
   이고, **와일드카드 서브도메인을 쓰지 않는다** — 값이 임시여도 모양은 최종과 같게 둔다.
4. 커맨드 넷을 **계약대로** 뚫는다. 절전 방지는 이 단계에서 **OS 호출까지** 들어간다
   (M-9 를 재야 하므로). macOS `…PreventUserIdleSystemSleep` · Windows `ES_CONTINUOUS | ES_SYSTEM_REQUIRED`.
5. `Info.plist`(마이크 문구) · `Entitlements.plist` 를 놓는다. **Windows 는 참조의
   `allow_microphone_on_webview2`(`lib.rs:49-88`)를 이식한다** — 없으면 `getUserMedia` 가 **프롬프트 없이** 실패한다.
6. 계측 페이지: **두 녹음 경로의 MIME 판정을 따로** 찍는다 —
   ① 회의 라이브의 고정 MIME(`microphone.ts:17` 의 `audio/webm;codecs=opus`)
   ② 브라우저 인터랙션의 후보 셋(`liveTranscription.ts:13-15`: `audio/webm;codecs=opus` → `audio/webm` → `audio/mp4`)
   중 **어느 후보로 떨어지는가**. 그 밖에 커맨드 넷 왕복 결과 · 네비게이션 훅 발화 로그 ·
   **장시간 녹음 시작/종료** 버튼 · 점유 획득/해제 버튼.
7. **fixture 를 둘로 세우고 무엇에 쓰는지 갈라 문서화한다.**
   - **https fixture** — **M-1 전용**. SPEC §6 M-1 이 「**로컬 https origin** 을 허용 목록에 넣어 본다」로
     프로토콜을 지정했고, **M-1 은 중단 판정의 근거**라 프로토콜이 다르면 판정이 흔들린다.
     지금 개발 서버는 평문이다(`frontend/vite.config.ts` 의 `server.port 5173` + `/api` 프록시 `ws:true`,
     `Makefile` 의 `npm run dev`) → **로컬 인증서로 https 를 세우는 것이 이 작업의 일부**다.
   - **평문 `localhost` 스택** — `make local-stack`(API·워커·프론트). **M-2·M-4 의 마이크·녹음 전용.**
     `localhost` 는 secure context 라 **평문이어도 마이크가 열린다**(MDN).
     **평문 `http://<LAN IP>` 는 안 된다** — `navigator.mediaDevices` 가 아예 없다.

**하지 말 것**

- **제품 화면에 점유 호출을 배선하지 마라.** 그것은 Phase 4 다
- **TTL·타이머·주기 갱신을 넣지 마라**(I-3). 탐침이라도 구조를 흐리면 Phase 3 이 그것을 베낀다
- **운영 도메인을 추측해 박지 마라.** 아직 없다(OQ-T02)
- **서명·공증·CI 를 만들지 마라.** 계승할 선례가 0 건이다

**검증** (이 Phase 에서 실행할 것)

- [ ] `cd frontend && npx tsc --noEmit` 통과
- [ ] `make frontend-test` 가 **기준선 대비 새 실패 0**
- [ ] `cargo check` (또는 `npm run tauri build --debug`)가 `frontend/src-tauri` 에서 성공
- [ ] 탐침 셸이 **뜨고**, 계측 페이지가 커맨드 넷의 응답을 화면에 찍는다

**완료 기준**

- [ ] 탐침 셸이 **로컬 https fixture** 를 열고, 커맨드 넷이 **응답을 돌려준다**(성공/실패 무관 — **왕복이 되는가**)
- [ ] 계측 페이지가 Phase 2 의 열 항목을 **전부 조작할 수 있다**
- [ ] `Cargo.toml` 의 `tauri` 버전이 **2.11.1 이상**이다

**의존**: 없음. **미결 어느 것에도 막히지 않는다** — 단 **macOS 축 기준**이다.
**Windows 쪽 탐침 실행과 마이크 프롬프트(M-4)는 장비 조건에 매인다**(OQ-W01).

**실패 시 다음 조치**

- 커맨드 왕복 자체가 안 되면 → **그것이 곧 M-1 의 답**이다. Phase 2 로 넘기지 말고 **즉시 판정 게이트**를
  연다(원격 https 문서에 IPC 가 닿지 않으면 SPEC-006 의 구조가 성립하지 않는다 — 조사 §3-5 가
  **단정하지 않은** 바로 그 지점이다)
- Rust 빌드 환경이 없으면(툴체인 미설치) → 코디가 환경 준비를 먼저 처리한다. **워커가 사용자 기기에
  설치하지 않는다**

---

### Phase 2 — 1차 실측 (fixture) 열 건과 진행/보완/중단 판정

- **Status**: IN_PROGRESS
- **소유**: **사용자**(실기 관찰) + 코디(기록·판정) + `frontend` 워커(재현용 계측 코드 보완만)
- **파일 범위**: **제품 코드 0줄.** 산출물은
  `orchestration/work/strong-hajin-projects/tauri-measurement-r1.md` **하나**
- **입력**: Phase 1 의 탐침 셸 + 계측 페이지 + 로컬 스택
- **출력**: 측정 기록 1건 — 항목별 **OS 축(macOS / Windows) · 관측값 · 판정 · 근거(로그·스크린샷·시각)**
- **설명**: **이 work 에서 가장 먼저 실행되는 단계**다. 여기서 나온 답이 뒤의 전부를 정한다.

**재는 것 — 열 건** (상세는 §실측 계획)

`M-1` 원격 IPC(**https fixture**) · `M-2` 녹음 포맷(**두 경로 × 3중**) · `M-2b` 만료 넘김 · `M-3` 네비게이션 훅 ·
`M-4` 마이크 권한 프롬프트 · `M-5` 쿠키 지속 · `M-6` 창 닫기 되묻기 · `M-7` 연결 실패 감지 ·
`M-8` 외부 링크 · `M-9` 절전 방지의 경계

**측정 규칙 — 어기면 기록이 거짓이 된다**

- **OS 축을 접지 않는다.** macOS 결과로 Windows 를 대신 쓰지 않는다. **Windows 실기가 없으면
  「검증 불가(장비 없음)」로 남기고**, 그 축에 매인 인수조건은 **끝까지 미통과**로 둔다 (OQ-W01)
- **`isTypeSupported` 가 참인 것으로 M-2 를 닫지 않는다.** 셋을 함께 잰다 —
  ① 지원 여부 ② **장시간 녹음이 끊기지 않는가** ③ **서버가 그 원본을 받아들이는가**
- **M-2 의 두 녹음 경로를 뭉치지 않는다.** 실물이 다르다 —
  **회의 라이브**는 `microphone.ts:17` 의 **단일 MIME 하드코딩**(후보 없음, WS 스트림으로 서버에 간다),
  **브라우저 인터랙션**은 `liveTranscription.ts:13-15` 가 **이미 후보 셋**을 갖고 멀티파트 업로드로 간다.
  뭉치면 ① 브라우저 경로가 mp4 로 살아 있는데 전체를 중단하거나 ② 회의 경로가 죽었는데
  「하나는 됐다」로 넘어간다. **서버 수용도 WS 스트림과 업로드를 각각 확인한다**
- **M-1 은 https fixture 에서 잰다.** 평문 `localhost` 결과로 대신하지 않는다 —
  SPEC §6 M-1 이 프로토콜을 지정했고, 이 항목이 **중단 판정의 근거**다
- **M-9 의 관찰 시간**은 AC-T05~T07 의 기준을 따른다 — 시험 환경에 **실제로 설정된** OS 자동 절전
  대기시간 `T` 에 대해 **`max(3T, 30분)` 이상**. `T` 가 설정되지 않은 환경의 측정은 **무효**다
- **M-2b 는 세션 수명을 짧게 둔 환경에서 잰다.** `DEFAULT_SESSION_TTL` 은 코드 상수(12h)라
  env 로 열려 있지 않다 → **개발 DB 의 세션 행 `expires_at` 을 직접 과거로 당겨** 잰다.
  **제품 코드를 고치지 않는다**(§Open Issues 의 변경 제안 참고)
- **추측을 기록에 섞지 않는다.** 「아마 된다」는 관측이 아니다

**검증**

- [ ] 열 항목 **각각**에 OS 축별 관측값과 근거가 있다. 빈칸이 없다(「검증 불가」도 값이다)
- [ ] M-2 가 **두 경로 × 세 갈래**(지원·장시간·서버 수용)로 **여섯 칸** 기록됐다.
      브라우저 경로는 **어느 후보로 떨어졌는가**가 함께 적혔다
- [ ] M-1 을 **https fixture** 에서 쟀다는 사실이 기록에 있다
- [ ] M-9 의 관찰 시간과 그때의 `T` 값이 **숫자로** 적혔다
- [ ] 제품 코드 diff **0줄**

**완료 기준 — 판정 게이트**

아래 셋 중 하나를 **명시적으로 고르고 근거를 적는다.** 고르지 않고 Phase 3 으로 넘어가지 않는다.

| 판정 | 조건 | 다음 |
|---|---|---|
| **진행** | M-1 왕복 성립(https fixture) **그리고** **회의 라이브 경로**의 M-2 세 갈래 모두 통과 — **그리고 아래 「보완」·「중단」의 어느 조건도 해당하지 않는다** | Phase 3 착수 |
| **보완** | 위 둘은 통과했으나 ① **M-3 ~ M-9 중 일부가 계약과 어긋난다**, 또는 ② **브라우저 인터랙션 경로만** 후보가 내려앉았다(예: mp4 로 떨어졌고 서버가 받는다), 또는 ③ **브라우저 경로가 아예 열리지 않는다**(**후보 셋 전부 실패** 또는 **서버가 그 업로드를 거부**) | ①은 어긋난 항목을 **구현 규칙으로 흡수**하고(예: M-6 이 안 돌면 셸이 되묻기를 낸다) Phase 3 착수. ②는 낙착된 후보를 기록에 남긴다. ③은 **그 사실을 기록하고 `AC-T07`·`AC-T11` 의 브라우저 축을 미통과로 «연 채»** Phase 3 을 착수한다 — **보완 담당과 결과 기록을 따로 세우고**(후보 보강을 별도 work 로 올릴지는 코디가 판단한다), **그 축이 닫히기 전에 「최종 지원판 검증」·「Release 완료」로 넘기지 않는다**. 셸 구현 자체는 브라우저 축과 독립이라 계속 간다 |
| **중단** | M-1 왕복이 성립하지 않는다 **또는** **회의 라이브 경로**(`microphone.ts:17` 의 단일 MIME)가 대상 OS 에서 열리지 않는다 | **Phase 3 이후를 세우지 않는다.** M-1 이면 SPEC-006 의 구조 재검토, M-2 면 **포맷 후보 도입이 선행 work** 로 승격(OQ-T07). **브라우저 경로만 후보가 내려앉은 것은 중단 사유가 아니다** — 그쪽은 이미 후보를 갖고 있다 |

**의존**: Phase 1

**실패 시 다음 조치**: 위 표의 **중단** 열 그대로. **대체 테스트 통과로 덮지 않는다** —
「macOS 에서 됐으니 Windows 도 될 것」·「짧은 녹음이 됐으니 장시간도 될 것」은 관측이 아니다.

---

### Phase 3 — 제품 셸

- **Status**: TODO
- **소유**: `frontend` 워커
- **파일 범위**: `frontend/src-tauri/**` · `frontend/package.json`. **`frontend/src/` 는 Phase 4 다**
- **입력**: Phase 2 의 측정 기록 · SPEC-006 §4·§5 · 계약 불변식 I-1 ~ I-8
- **출력**: 제품 셸 — 창 하나 · 커맨드 넷 · 허용 목록 둘 · U-2 연결 실패 화면 ·
  절전 방지 · 창/문서 수명 정리
- **설명**: 탐침을 **계약대로** 다시 세운다. Phase 2 가 「보완」이면 그 어긋남을 여기서 흡수한다.

**작업**

1. **커맨드 넷만** 노출한다. `invoke_handler` 에 다섯째가 없다. 파일 읽기·쓰기·프로세스 실행·범용 셸·
   `open_path`·`reveal_item_in_dir` 을 **하나도 열지 않는다**.
2. **허용 목록 둘을 가른다** — 커맨드는 `capabilities` 의 `remote.urls` 로 **운영 origin 하나**,
   네비게이션은 창 수명 훅으로 **운영 origin + 인증이 실제로 거치는 주소**. 지금은 인증이 밖으로
   나가지 않으므로 **둘 다 하나**다. 인증 방식이 바뀌면 네비게이션 목록만 넓어진다.
3. **해제 시점을 «완료»에 건다**(I-4) — 창 **닫기 요청**과 **실제 소멸**을 가르고, 네비게이션 **시도**와
   **문서 교체 시작**을 가른다. 취소된 이동·취소된 닫기에서 **아무것도 풀지 않는다**.
4. **재무장을 구현한다**(I-6) — 같은 세션 키의 재요청은 점유를 늘리지 않고, **그 시점에 OS 절전 방지가
   걸려 있지 않으면 다시 건다.** 응답 `state` 는 그때의 실제 상태다.
5. **늦은 획득의 잔존 0**(I-7) — 취소·직렬화·보상 해제 중 하나를 고른다. **영구 기록을 만들지 않는다.**
   고른 수단과 이유를 코드 주석에 남긴다.
6. **Windows 스레드 제약**을 구조로 받는다 — 걸고 푸는 것이 같은 스레드가 되게 한다.
7. **U-2 연결 실패 화면** — M-7 이 알려 준 감지 수단으로. **감지 수단이 없다고 판명되면 조용히 빼지 않고**
   Phase 를 `BLOCKED` 로 돌린다.
8. **외부 링크** — `open_external` 은 `http(s)` 만 받고, 그 밖의 스킴은 열지 않는다.
   **앱 창이 외부 문서로 바뀌지 않고, 두 번째 웹뷰도 뜨지 않는다.**
9. 웹뷰 저장소가 **지워지지 않게** 둔다 — incognito 를 켜지 않는다(켜면 실행마다 로그아웃된다).

**하지 말 것**

- **셸에 데이터·업무 로직·화면을 두지 마라.** 셸이 그리는 것은 U-2 하나다
- **`csp` 를 셸 설정에 박지 마라.** 문서를 내는 것은 원격 서버다
- **앱 식별자를 판마다 바꾸지 마라.** 바뀌면 저장 영역이 새로 잡혀 **사용자가 로그아웃된다**
- **트레이·상주·두 번째 창을 만들지 마라**
- 불변식 I-1 ~ I-8 을 「구현이 어려워서」 바꾸지 마라. 어려우면 **코디에게 올린다**

**검증**

- [ ] `cargo check` · `cargo clippy` 경고 없음 · `npx tsc --noEmit` 통과
- [ ] `make frontend-test` 새 실패 0
- [ ] **설정 파일을 사람이 읽어** 커맨드가 넷뿐임을 보인다 (AC-T23)
- [ ] `Cargo.toml` 의 tauri 하한이 2.11.1 이상 (AC-T25)
- [ ] 탐침 대신 **제품 셸**로 M-1·M-3·M-6·M-7·M-8 을 **한 번 더** 돌려 같은 결과가 나온다

**완료 기준 — 이 Phase 가 닫는 인수조건 15건**

`AC-T12` `AC-T13` `AC-T14` (세션 키의 멱등·격리) · `AC-T15` `AC-T16` `AC-T17` `AC-T18` (네이티브 정리 셋과
그 경계) · `AC-T20` `AC-T21` `AC-T22` `AC-T23` (경계와 권한) · `AC-T25` (버전 하한) · `AC-T31` (U-2) ·
`AC-T33` `AC-T34` (트레이 없음 · 식별자)

- [ ] 위 15건 각각에 **증거**(설정 인용 · 로그 · 관찰 기록)가 붙었다
- [ ] `AC-T24` 는 **개발·fixture origin 으로 잠정 확인**만 한다 — **최종 통과는 Phase 8**(운영 origin 판)

**의존**: Phase 2 판정 = 진행 또는 보완

**실패 시 다음 조치**: 계약과 구현이 부딪치면 **구현을 바꾸지 말고 코디에게 올린다.**
SPEC 이 정본이고, 새 사용자 계약이 필요하면 **변경 제안**으로 간다 — 이 work 가 SPEC 을 고치지 않는다.

---

### Phase 4 — 웹 최소 배선

- **Status**: TODO
- **소유**: `frontend` 워커
- **파일 범위**: `frontend/src/lib/shell.ts`(신규) · `frontend/src/lib/labels.ts` ·
  `frontend/src/features/meetings/stream.ts` · `…/MeetingDetailPage.tsx` ·
  `frontend/src/features/browser/BrowserRecordingPage.tsx` · `frontend/src/App.tsx`.
  **`frontend/src/lib/api.ts` 와 `microphone.ts` 를 건드리지 않는다**
- **입력**: Phase 3 의 셸 · SPEC-006 §4 L-01 ~ L-14 · §2 U-3
- **출력**: 웹이 더하는 **둘뿐** — U-3 한 줄과 점유 호출 배선(재확인 1회 포함)
- **설명**: **여기서 더하는 웹 변경이 둘을 넘으면 범위를 넘은 것이다.**

**작업**

1. `shell.ts` — 셸 존재 판정과 커맨드 넷 래퍼. **없으면 한 번도 호출하지 않는다**(`E-01`).
   호출 실패는 `E-14a`/`E-14b`/`E-14c` 세 갈래로 가른다.
2. **회의 라이브 배선** — `stream.ts:251`(마이크가 열린 순간) 획득 · `:317-319`(닫힘) ·
   `:322`(자리 뺏김) · `:327-331`(cleanup) 해제. **세션 키를 여는 회차마다 새로 만든다.**
3. **브라우저 인터랙션 배선** — `BrowserRecordingPage.tsx:47-70` 획득(키는 기존 `captureId`) ·
   `:71-102`·`:30-44` 해제. **업로드 재시도 중에는 유지한다**(L-08).
4. **재확인 1회**(L-14) — 문서가 다시 보이게 될 때와 절전 복귀 뒤 **같은 키로 한 번** 다시 부른다.
   **주기적으로 도는 것을 만들지 않는다**(I-3).
5. **U-3 두 자리** — `MeetingDetailPage.tsx:932` 의 `StatusNote` 옆, 그리고
   `BrowserRecordingPage` 의 상태 문구 자리. 문구 **둘**을 `labels.ts:772` 근처에 둔다
   (절전 실패 / **정리 실패**는 다른 문구다 — `E-14b`).
6. **외부 링크** — `App.tsx:684` 에서 셸이 있으면 `open_external`, 없으면 **지금 그대로**.
7. **세션 키가 회차마다 다름을 코드로 보이게** 둔다(AC-T42) — 회의 id 를 키로 쓰지 않는다.

**하지 말 것**

- **`api.ts` 를 고치지 마라.** 상대경로 9곳은 방향 A 에서 한 줄도 안 바뀐다
- **`microphone.ts` 의 포맷을 바꾸지 마라.** M-2 가 「안 열린다」였다면 그것은 **다른 work** 다
- **전역 401 처리·자동 로그아웃·재인증을 새로 만들지 마라**(`E-10` · OQ-T11)
- **끊긴 녹음을 자동으로 다시 잇지 마라.** 이 제품은 자동 재연결을 두지 않았다
- **녹음이 끝나지 않았는데 푸는 경로를 만들지 마라** — 화면이 잠깐 가려졌다는 이유로 풀지 않는다

**검증**

- [ ] `make frontend-test` 새 실패 0 · `npx tsc --noEmit` 통과
- [ ] **브라우저(셸 없음)로 열었을 때** 콘솔 에러·경고 **0건**, 화면 동작이 지금과 같다
- [ ] 셸 없는 경로에서 `invoke` 호출이 **한 번도 나가지 않는다**(네트워크·로그로 확인)
- [ ] `git diff --stat` 이 **위 파일 범위 밖을 건드리지 않았다**

**완료 기준 — 이 Phase 가 닫는 인수조건 5건**

`AC-T08` (마이크 실패 시 미획득) · `AC-T09` (구독은 미획득) · `AC-T10` (자리 상실 시 해제) ·
`AC-T11` (실패해도 녹음 계속 + 두 화면 어디서든 U-3) · `AC-T42` (세션 키가 회차마다 다르다)

**의존**: Phase 3

**실패 시 다음 조치**: 배선 자리가 SPEC 의 L-번호와 안 맞으면(예: 마이크가 열리는 자리가 하나가
아니다) **코드를 억지로 맞추지 말고** 사실을 보고한다 — SPEC 이 센 전수가 틀렸다는 뜻이다.

---

### Phase 5 — 제품 통합 재측정과 인수조건 실행

- **Status**: TODO
- **소유**: **사용자**(실기 관찰) + 코디(기록·판정) + `frontend` 워커(재현 보조·수정)
- **파일 범위**: 제품 코드는 **수정 발생 시에만** Phase 4 범위 안에서. 산출물은
  `orchestration/work/strong-hajin-projects/tauri-measurement-r2.md`
- **입력**: Phase 3·4 의 결과물 · Phase 2 의 1차 기록
- **출력**: ① 2차 측정 기록(M-11 ~ M-14) ② **인수조건 실행 기록** — Phase 5 가 닫는 21건
- **설명**: **fixture 에서 재던 것을 제품 배선 위에서 다시 잰다.** 1차와 2차를 한 파일에 섞지 않는다 —
  「탐침에서는 됐는데 제품에서 안 된다」가 보여야 한다.

**재는 것 — 새 ID 넷 + 제품판 증거가 필요한 기존 ID 넷** (상세는 §실측 계획)

- **새로 재는 넷**: `M-11` 숨김·최소화·화면 꺼짐 장시간(**두 녹음 화면 각각**) · `M-12` 수동 절전 복귀와
  재무장 · `M-13` 취소된 사건에서의 점유 보존 · `M-14` 늦은 완료와 정리 실패
- **제품판 증거가 더 필요한 넷**: `M-9` · `M-2b` · `M-6` · `M-5`.
  **새 ID 를 만들지 않는다** — 같은 ID 안에서 **「fixture 증거(Phase 2)」와 「제품판 증거(Phase 5)」를
  단계로 가른다.**

**fixture 기록을 제품 AC 의 증거로 쓸 수 있는가 — 항목마다 판단한다**

「fixture 에서 됐으니 제품도 된다」를 **일반 규칙으로 쓰지 않는다.** 아래가 이번 판단이고, 근거는
**그 AC 의 문장이 무엇 위에서 나야 하는 증거인가**다.

| 실측 | 걸린 AC | 제품판 증거가 필요한가 | 근거 |
|---|---|---|---|
| **M-9** | AC-T01 ~ AC-T04 | **필요** | AC-T01 이 「**회의 업스트림으로 마이크가 열린 뒤**」를 조건으로 건다. 탐침의 점유 버튼이 아니라 **제품 녹음 위**에서 나야 하는 증거다. **M-11 과 같은 회차에 재고 그 기록에 병기한다** |
| **M-2b** | AC-T28 · AC-T27 | **AC-T28 만 필요** | AC-T28 은 「녹음이 이어지고 **점유도 유지된다**」라 **배선에 달렸다** → 제품판. AC-T27(만료 뒤 재접속에서 로그인 화면·시각 경과만으로는 안 바뀜)은 **서버·웹 동작이고 «배선»과 무관**하다 → **Phase 2 기록을 인용하고 인용임을 표시한다**. ⚠ **단 이 인용은 Phase 5 시점의 임시 유효다** — **Phase 6b 작업 3 이 인증·세션 경로(`http.py`·`http_auth.py`·`settings.py`)를 고치므로**, 그 변경 뒤 **6b 검증에서 운영 프로파일로 한 번 갱신한다** |
| **M-6** | AC-T32 · AC-T38 | **필요** | 되묻기를 **어느 층이 내는지**를 M-6 결과가 정하고, 그 구현이 Phase 3 또는 4 에서 생긴다. fixture 기록은 「**낼 수 있는가**」까지만 답한다 — 「**하나만 뜨는가**」는 제품판에서만 난다 |
| **M-5** | AC-T26 | **필요 — 단 배선과 무관하다** | 쿠키 지속은 **셸 설정**(식별자·데이터 저장소·incognito)에 달렸고, Phase 3 의 제품 셸은 Phase 1 의 탐침과 **설정이 다르다**. 그래서 **제품 셸판으로 한 번 더** 확인한다. Phase 4 배선이 바뀌어도 결과는 안 변한다 |

**측정 규칙**

- **AC-T05 ~ AC-T07 의 관찰 시간 하한**을 다시 적용한다 — `max(3T, 30분)`. **두 녹음 화면을 따로 잰다**
- **M-9 의 세 갈래(자동 절전 차단·화면 꺼짐·수동 절전 허용)를 제품 배선 위에서 한 번 더 확인하고
  M-11 기록에 병기한다.** 탐침 기록을 AC-T01~T04 의 증거로 쓰지 않는다
- **인용한 증거는 인용임을 표시한다** — 「Phase 2 기록 인용(M-2b, AC-T27)」처럼 **출처와 회차**를 적는다.
  표시 없는 인용은 제품판 관측으로 오해된다
- **증거 갱신 규칙 — 이 work 전체에 건다.** **뒤 Phase 가 그 증거의 전제였던 코드·설정을 고치면,
  앞에서 딴 증거(인용이든 관측이든)를 그 변경 뒤에 한 번 갱신한다.** 갱신하는 자리는 **그 변경을 낸
  Phase 의 검증**이다. 지금 이 규칙이 실제로 걸리는 자리는 **AC-T27 ← Phase 6b** 하나다
- **M-13 은 「풀리지 않는가」를 잰다.** `계속 녹음` 을 고른 **뒤에도** 자동 절전 시간을 넘겨 기기가
  안 잠드는 것까지가 AC-T36 이다
- **M-14 는 최종 잔존만 본다.** 어떤 수단으로 이뤘는지 묻지 않는다
- **AC-T28 은 Phase 2 의 M-2b 환경(세션 행을 당긴 개발 DB)을 그대로 쓰되 «제품 배선 위에서» 다시 잰다**
  — 녹음이 안 끊기는 것과 **점유가 유지되는 것** 둘 다 본다

**검증 — 이 Phase 에서 실행할 것**

- [ ] 새 ID 넷(M-11~M-14)이 **OS 축별로** 기록됐다 (Windows 실기가 없으면 「검증 불가」)
- [ ] **제품판 증거가 필요한 셋**(M-9 · M-2b/AC-T28 · M-6)이 제품 배선 위에서 다시 관측됐고,
      **M-5 는 제품 셸판으로** 확인됐다
- [ ] **인용한 항목**(AC-T27)이 **인용임을 표시**하고 Phase 2 기록의 회차를 가리킨다
- [ ] 아래 21건의 인수조건을 **하나씩 실행하고 증거를 붙였다**
- [ ] 앱에서 회의·메모·안건·자료 업로드·업무 화면이 **브라우저와 같게** 동작한다(회귀)
- [ ] `make verify` 가 기준선 대비 **새 실패 0**

**완료 기준 — 이 Phase 가 닫는 인수조건 21건**

`AC-T01` `AC-T02` `AC-T03` `AC-T04` (절전 방지 핵심) · `AC-T05` `AC-T06` `AC-T07` (비가시·화면 꺼짐 장시간) ·
`AC-T19` (수동 절전 복귀) · `AC-T26` `AC-T27` `AC-T28` (세션) · `AC-T29` `AC-T30` (기존 기능 무변경) ·
`AC-T32` (창 닫기 되묻기) · `AC-T36` `AC-T37` `AC-T38` (취소된 사건) ·
`AC-T39` `AC-T40` `AC-T41` (재무장·늦은 완료) · `AC-T43` (정리 실패)

> `AC-T32`·`AC-T38` 의 **구현 자리**(웹이냐 셸이냐)는 Phase 2 의 M-6 이 정한다. 이 Phase 는
> **확인 창이 하나만 뜨는가**를 잰다.

**의존**: Phase 4

**실패 시 다음 조치**

- 계약과 어긋나면 → Phase 3 또는 4 로 되돌려 **그 Phase 를 `IN_PROGRESS` 로 다시 연다.**
  Phase 5 에서 코드를 고치고 그 자리에서 통과로 적지 않는다
- 플랫폼이 계약을 물리적으로 못 만족하면(예: OS 가 재무장을 거부) → **한계로 기록하고 코디에게 올린다.**
  「사실상 같다」로 통과시키지 않는다

---

### Phase 6a — 운영 배포 설계: 사실 확인과 구성안

- **Status**: TODO
- **소유**: 코디(사실 확인·구성안·발주 준비). **사용자는 승인만** — 명령을 실행하지 않는다
- **파일 범위**: 산출물은 `orchestration/work/strong-hajin-projects/tauri-deploy-design.md` **하나**.
  인프라 레포·제품 코드는 **읽기 전용**
- **입력**: `tauri-deployment-decisions.md` 의 조회 결과 · `k8s_infra_mac` 의 차트·Application(읽기 전용) ·
  SPEC-006 §5 「지원 환경과 반복 배포」
- **출력**: **배포 설계 1건** — 차트·Application·values·ingress·네임스페이스·이미지·프로파일 정리안·
  rollback·데이터 보존 정책. **6b 가 그대로 실물로 옮길 수 있는 수준**이어야 한다
- **설명**: 「창이 열 https 주소」를 실재하게 만들기 **직전까지**. 실행은 6b 다.

**닫아야 하는 것 넷 — 사실 / 구현 기본값 / 진짜 사용자 결정을 가른다**

| # | 사실 (확인됨) | 처분 |
|---|---|---|
| **6-1. 운영 프로파일** | `@app.` 데코레이터 **160개** 중 **159개**가 `http.py:606` 의 `if settings.developer_auth_enabled:` 안. 밖에 있는 것은 `:2530` `/health` 하나. `developer_auth_enabled` = DEVELOPMENT·TEST (`settings.py:125-126`). **`AX_PROFILE=PRODUCTION` 으로 띄우면 로그인도 API 도 없다** | **내부 정리는 구현이고, 계약 변경은 별도 결정이다.** ⟶ **기본안(구현)**: 라우트 등록을 가르는 조건과 **권한 판정**을 분리해, PRODUCTION 에서도 **같은 라우트·같은 권한 판정·같은 쿠키 계약**이 서게 한다. 사용자에게 보이는 권한이 **한 칸도 넓어지지 않는 것**이 조건이다. ⟶ **별도 결정(OQ-W05)**: 권한을 **완화**하거나(로컬 로그인 개방 등) **새 인증 방식**(외부 IdP·OIDC)을 들이는 순간. ⟶ **금지**: development/test 프로파일로 운영하는 우회 (SPEC §5) |
| **6-2. `Secure` 쿠키** | `http_auth.py:106-107` `cookie_secure()` 는 **PRODUCTION 일 때만** 참. 6-1 과 정면으로 부딪친다 | 6-1 의 내부 정리가 이것을 같이 푼다. **`Secure` 가 붙는 조건을 배포 설정으로 분리**하는 것도 같은 부류(권한 불변) — **구현 선택**이다 |
| **6-3. FE 정적 서빙 + 같은 origin** | `http.py` 에 `StaticFiles`·`mount` **0건**. CORS 미들웨어도 0건(같은 origin 이라 필요 없다). 기존 mediness ingress 는 **front·api 가 다른 호스트**라 그대로 못 쓴다 | **정해졌다 — 코디 기본값 A: ingress 경로 분기.** 한 호스트에 `/` → **정적 FE 컨테이너**, `/api` → back. **제품 코드를 안 건드리는 길**이라 사용자 gate 를 두지 않는다. `/api/meetings/{id}/stream` 이 `/api` 아래라 **WS 도 같은 규칙에 실린다** — mediness api ingress 처럼 `proxy-read-timeout`·`proxy-send-timeout: 3600` 을 붙인다. (대안 B — 백엔드가 `StaticFiles` 로 dist 를 내는 길 — 은 제품 코드를 건드리므로 A 가 막힐 때만 본다) |
| **6-4. 서버 아키텍처** | 노드 전부 **arm64**. `delivery/Dockerfile:63` 이 `@openai/codex-linux-x64` / `x86_64-unknown-linux-musl` 을 **하드코딩**하고 `Makefile:25` 가 `PROTECTED_PLATFORM ?= linux/amd64` 다 — 그대로 arm64 로 굽지 못한다. `delivery/README.md` 는 이 이미지의 목적을 **고객 납품**으로 적는다(「고객에게는 검증한 최종 image archive 와 digest·운영 문서·필수 OSS 고지만 전달한다」) | **arm64 운영 이미지를 만드는 것 자체는 구현이다** — 「이미지가 하나 는다」는 이유로 사용자 gate 를 두지 않는다. ⟶ **작업 1 이 먼저 확인한다**: 보호 요구가 **자가 호스팅 운영에도 적용되는가**. ⟶ **적용 대상이 아니면**(납품 경로 전용이면) 운영용 arm64 이미지를 **따로** 만든다 — **납품 경로의 Dockerfile·Makefile·스캐너를 한 줄도 바꾸지 않으므로 기존 보호 요구를 훼손하지 않는다**. ⟶ **적용 대상이면** `delivery/` 를 arm64 로 확장한다(63줄의 codex vendor 를 arm64 로, Nuitka arm64 재검증, 스캐너 재실행). ⟶ **사용자 결정은 하나뿐이다 — 「납품 경로의 보호 수준을 낮추는」 선택을 할 때** |

**작업**

1. **보호 요구의 적용 범위를 확인해 기록한다** — `delivery/README.md` 를 근거로, 이 운영 배포가
   **납품 경로인지 아닌지**를 한 줄로 못박는다. 6-4 의 기본안이 여기서 갈린다.
2. 배포 구성안을 쓴다 — 차트 한 벌 · Application 한 벌 · **`main` 추적**
   (레포 Application **9개** 전부 `main`. 2026-09-22 클러스터 조회는 10개. README 의 `k8s-test` 설명은
   실물과 다르다) · **네임스페이스 분리** · values 한 벌 · ingress(한 호스트 · 경로 둘 · WS 타임아웃).
3. **운영 프로파일 내부 정리안**을 쓴다 — 어느 조건으로 라우트를 가를지, **권한 판정이 어디서도
   넓어지지 않음**을 어떻게 보일지(테스트로), `Secure` 를 어떤 설정에 매달지.
4. **운영 이미지 안**을 쓴다 — 작업 1 의 결과에 따른 기본안 · 빌드 명령 · 태그 규칙 · 누가 굽는지.
   **운영 이미지와 납품 이미지의 저장 자리를 갈라 적는다** — **기존 레지스트리 안에서 image repository 와
   tag namespace 를 나누는 것으로 충분하다**(새 레지스트리 서비스를 세우지 않는다).
   ⚠ **운영용 비보호 이미지가 납품 경로로 나가지 않는 것**이 조건이다 — `delivery/README.md` 의 보호 요구는
   **고객에게 전달되는 아티팩트**에 걸리므로, 두 계열의 이름이 섞이면 그 경계가 흐려진다.
5. **기존 Mediness 와의 분리**를 명시한다 — 네임스페이스 · 도메인 · Argo project · 데이터스토어 ·
   PVC/hostPath 경로. **기존 values·Application 을 한 줄도 고치지 않는다.**
6. **데이터 보존 정책**을 쓴다 — 새 Postgres 를 쓰고 기존 `mediness-*` 의 것을 공유하지 않는다.
   `AX_MATERIALS_DIR`·`AX_RECORDINGS_DIR` 에 해당하는 영속 볼륨을 **따로** 잡고,
   **Application 을 지워도 볼륨이 남는 설정**과 **백업·복구 절차**를 함께 적는다(§Rollback 과 짝).
7. **6b 의 발주 단위를 미리 가른다** — 어느 파일을 어느 워커가 쓰는지(아래 6b 의 표).

**하지 말 것**

- **운영 도메인을 발명하지 마라**(OQ-T02). 값이 없으면 **자리만** 비워 둔다
- **비밀값을 읽지 마라.** 접속 값은 `orchestration/config/projects/mediness.json` 의 `environments` 를
  **참조**하고 복제하지 않는다
- **납품 경로의 보호 수준을 낮추는 안을 기본값으로 쓰지 마라.** 그것만이 사용자 결정이다
- **기술 선택마다 사용자 확인을 만들지 마라.** 권한·계약이 안 바뀌는 선택은 **코디 기본값으로 통보**한다

**검증**

- [ ] 구성안의 모든 값이 **사실 / 구현 기본값 / 사용자 결정** 중 하나로 표시돼 있다. 섞인 칸이 없다
- [ ] 같은 origin 이 성립함을 **경로 단위로** 보였다 — `/`·`/api/*`·`/api/meetings/{id}/stream`
- [ ] **권한 판정이 넓어지지 않음**을 보일 방법(테스트 또는 대조)이 적혀 있다
- [ ] 데이터 **보존** 정책과 **백업·복구** 절차가 rollback 과 갈려 적혀 있다
- [ ] 기존 mediness 차트·Application·values 의 diff **0줄**(읽기만 했다)

**완료 기준**

- [ ] 6-1 ~ 6-4 각각에 처분이 붙었다 — **사용자 결정으로 남은 것은 OQ-T02(도메인) 과, 해당될 때의
      OQ-W05·보호 수준 둘뿐**이다
- [ ] 6b 가 **추가 설계 없이 착수 가능**하다 — 파일·워커·순서가 다 적혀 있다
- [ ] **이 Phase 는 인수조건을 닫지 않는다** — 전제를 세우는 단계다

**의존**: 없음(읽기 전용 설계). Phase 3·4 와 **병행 가능**

**실패 시 다음 조치**: 도메인(OQ-T02)이 안 나오면 **그 자리만 비워 두고 나머지를 닫는다.**
6a 전체를 `BLOCKED` 로 두지 않는다 — 도메인은 값 하나이고 구조는 그것 없이도 선다.

---

### Phase 6b — 운영 배포 실행: 구성 실물 · 이미지 · 정적 서빙 · 배포

- **Status**: TODO
- **소유** — **코딩은 워커, 발주·검증은 코디, 승인은 사용자.** 사용자에게 명령을 떠넘기지 않는다

  | 산출물 | 소유 | 파일 범위 |
  |---|---|---|
  | 차트 · Application · values · ingress | **인프라 워커**(`roles/strong-hajin/infra`, P-5 해소) | `k8s_infra_mac/charts/strong-hajin/**` · `argocd/applications/strong-hajin-*.yaml` |
  | 운영 이미지(arm64) | `backend` 워커 | 6a 작업 1 의 결과에 따라 — 운영용 새 이미지 자리, 또는 `delivery/` arm64 확장 |
  | FE 정적 서빙 산출물 | `frontend` 워커 | `frontend/` 빌드 산출물 + 정적 서빙 컨테이너 정의 |
  | 운영 프로파일 내부 정리 | `backend` 워커 | `backend/src/ax_workspace/entrypoints/http.py` · `…/http_auth.py` · `…/bootstrap/settings.py` |
  | 배포 실행 · 확인 | 코디(발주·검증) | 실행 명령. **승인 범위 안에서** |

- **입력**: Phase 6a 의 설계 1건 · 운영 도메인(OQ-T02)
- **출력**: ① 실물 차트·Application·values ② arm64 운영 이미지 ③ 정적 서빙이 붙은 배포
  ④ **운영 https 주소가 실재한다** ⑤ 배포 기록(이미지 태그·sync 결과·경로별 응답)
- **설명**: **이 Phase 가 Phase 8·9 의 선행을 실재하게 만든다.** 6a 없이 착수하지 않는다.

**작업**

1. **차트·Application·values 를 실물로 쓴다.** 로컬에서 `helm template` 로 렌더까지 확인한다.
2. **운영 이미지를 굽는다** — 6a 작업 1 의 결과에 따른 기본안으로. arm64 노드에서 뜨는 것을 확인한다.
3. **운영 프로파일 내부 정리를 구현한다** — 권한 판정이 **넓어지지 않음**을 테스트로 보인다.
   ⚠ **권한 완화·새 인증이 필요해지면 거기서 멈추고 코디에게 올린다**(OQ-W05).
4. **FE 정적 서빙을 붙인다** — `/` 가 SPA 를, `/api/*` 와 WS 가 back 을 향한다.
5. **외부 레포에 올린다** — ⚠ **여기가 OQ-W02 의 유일한 차단 지점**이다.
   회사 org 레포(`MediSolveAIDev/k8s_infra_mac`)에 개인 제품 구성을 **푸시·PR 하기 전에** 범위를 확인한다.
   **작업 1~4 는 이 확인을 기다리지 않는다.**
6. **배포한다** — ArgoCD sync. **산출물이 준비되고 코디 검증이 끝난 뒤**, **그 세션의 승인 범위 안에서**
   실행한다. 승인 범위 밖이면 사용자 승인을 받고 진행한다.
7. **확인한다** — `/`·`/api/*`·WS 가 각각 응답하고, 쿠키에 `Secure` 가 붙고, 로그인이 선다.

**하지 말 것**

- **기존 mediness 네임스페이스·values·Application 을 고치지 마라**
- **development/test 프로파일로 운영을 띄우지 마라** (SPEC §5)
- **데이터 볼륨을 「초기화」로 지우지 마라.** 배포 실패는 **재배포**로 푼다 (§Rollback)
- **비밀값을 이미지·차트·values 에 넣지 마라** — 주입 수단으로만
- **사용자에게 「이 명령을 실행해 달라」고 넘기지 마라.** 워커가 쓰고 코디가 돌린다

**검증**

- [ ] `helm template` 렌더가 성공하고, 기존 mediness 리소스와 **이름·네임스페이스가 겹치지 않는다**
- [ ] arm64 노드에서 **파드가 Running** 이고 이미지 태그가 의도한 값이다
- [ ] `/`(SPA) · `/api/*`(REST) · `/api/meetings/{id}/stream`(WS) 셋 다 **경로별로 응답**한다
- [ ] 로그인 후 세션 쿠키에 **`Secure` 가 붙는다**
- [ ] **권한 판정이 넓어지지 않았다** — 6a 가 정한 테스트가 통과한다
- [ ] **세션 만료 동작이 그대로다 — AC-T27 의 인용 증거를 여기서 갱신한다.**
      **운영 프로파일의 «격리 검증 환경»** 에서 AC-T27·SPEC §3 S-8 **원문 그대로** 본다 —
      ① 만료된 세션으로 **앱을 다시 열거나 스트림에 새로 붙으면** 로그인 화면으로 돌아간다
      ② **시각이 지났다는 것만으로** 화면이 로그인으로 바뀌거나 **열린 스트림이 닫히지 않는다**.
      ⚠ **운영 DB 의 세션 행을 조작하지 않는다** — 격리 환경에서 잰다.
      ⚠ **SPEC 에 없는 동작을 만들어 확인하지 않는다** — 자동 401 로그인 전환도, 열린 WS 의 자동 종료도
      이 제품에 없다(`E-10`·S-8). **없는 것을 없는 대로 확인하는 것**이 이 항목이다
- [ ] 기존 mediness 워크로드가 **영향을 받지 않았다**(파드 상태·기존 호스트 응답)

**완료 기준**

- [ ] **운영 https 주소가 실재하고 로그인이 선다** — Phase 8 의 입력이 충족됐다
- [ ] 데이터 볼륨과 백업 절차가 **6a 설계대로** 서 있다
- [ ] **이 Phase 는 인수조건을 닫지 않는다** — Phase 8 이 그 위에서 잰다

**의존**: Phase 6a · OQ-T02(도메인). P-5 인프라 워커 정의는 해소됐다.
작업 5 만 OQ-W02 에 매인다

**실패 시 다음 조치**

- 배포가 안 서면 → **되돌리고**(§Rollback) 원인을 6a 설계에 환류한다. **데이터를 지워서 풀지 않는다**
- 권한 완화 없이는 안 되는 자리가 나오면 → **거기서 멈추고 OQ-W05 로 올린다.**
  우회로 development 프로파일을 쓰지 않는다

---

### Phase 7 — 설치파일 빌드 환경과 fixture 판 검증

- **Status**: TODO
- **소유**: `frontend` 워커(빌드 구성·실행) + 코디(절차·검증) + **사용자**(실기 설치 확인)
- **파일 범위**: `frontend/src-tauri/tauri.conf.json`(번들 타깃·판 번호) · `Makefile`(타깃 추가)
- **입력**: OQ-T01(최소 OS·아키텍처·형식) · Phase 5 의 통과 기록
- **출력**: ① 빌드 절차 ② **fixture origin 판 설치파일 두 판**(재설치·판 올림용) ③ **M-10 측정 기록**
- **설명**: **여기서 만든 판은 발행 대상이 아니다.** 운영 origin 을 아직 갖지 않았고,
  M-10 과 AC-T35 를 재기 위한 판이다. **발행은 Phase 9 가 하고, 그 대상은 Phase 8 이 검증한 판이다.**

**작업**

1. **번들 타깃을 정한다** — OQ-T01 이 닫히면 macOS(`dmg`/`app`) · Windows(`msi`/`nsis`) 중 무엇인지.
   **최소 OS 버전과 CPU 아키텍처도 여기서 값이 된다.**
2. **빌드 환경을 가른다** — ⚠ **Tauri 는 크로스 컴파일을 보장하지 않는다.**
   **Mac Studio 가 Windows 설치파일까지 굽는다고 가정하지 않는다.** Windows 설치파일에는
   **Windows 빌드 환경**(실기 또는 러너)이 필요하다 (OQ-W06).
3. **판 번호를 셋으로 묶는 규칙을 세운다** — 코드 레포 태그 `vX.Y.Z` · `tauri.conf.json` 의 `version` ·
   `shell_info().app_version`. **셋이 같은 값**이어야 한다. (태그를 실제로 다는 것은 Phase 9 다)
4. **fixture origin 으로 두 판을 굽는다** — M-10 이 **재설치·판 올림**을 재므로 두 판이 필요하다.
5. **M-10 을 잰다** — 같은 식별자로 재설치·판 올림 뒤 웹뷰가 쿠키를 들고 있는가.
6. **서명·공증·자동 업데이트의 처분 초안을 적는다** — 결정은 OQ-T03 이고, 여기서는
   **무엇을 정해야 하는지**와 미서명일 때의 실행 절차 초안을 남긴다.

**하지 말 것**

- **여기서 Release 를 발행하지 마라.** 이 판은 운영 origin 을 갖지 않는다 — **Phase 9 가 발행한다**
- **서명·공증·CI 가 이미 있다고 쓰지 마라.** 0건이다
- **앱 식별자를 바꾸지 마라** — M-10 이 거짓이 되고 사용자가 로그아웃된다
- **Windows 축을 macOS 결과로 대신하지 마라**

**검증**

- [ ] 설치파일이 **실제로 설치되고 앱이 뜬다**. Windows 실기가 없으면 **「검증 불가」로 남기고
      macOS 결과로 대신하지 않는다**
- [ ] 판 번호 셋이 같다 — 태그 규칙 · `tauri.conf.json` · `shell_info().app_version`
- [ ] **이 판이 fixture origin 을 연다**는 사실이 기록에 있다(발행 대상이 아님을 남긴다)

**완료 기준 — 이 Phase 가 닫는 인수조건 1건**

`AC-T35` (재설치·판 올림 뒤에도 웹뷰가 세션 쿠키를 그대로 들고 있다 — M-10)

**의존**: OQ-T01 · OQ-W01 · OQ-W06 · Phase 5. **운영 주소를 기다리지 않는다**

**실패 시 다음 조치**: **Windows 빌드 환경이 없으면 그 축을 보류한다.**
⚠ **macOS 단독 출시를 기본 행동으로 쓰지 않는다** — D-07 은 양쪽 지원이고, 범위를 줄이는 것은
**OQ-W06 의 처분으로 사용자 승인을 받은 뒤**에만 한다. 승인 전에는 **Windows 축이 열린 채로 남는다.**

---

### Phase 8 — 운영 origin 확정 · 최종 빌드 · 최종 확인

- **Status**: TODO
- **소유**: `frontend` 워커(설정 변경·최종 빌드) + 코디(발주·검증) + **사용자**(실기 확인·승인)
- **파일 범위**: `capabilities/*.json` 의 **운영 origin 값** · `tauri.conf.json` 의 판 번호.
  그 밖의 제품 코드는 **0줄**
- **입력**: **Phase 6b 의 결과 — 운영 https 주소가 실재한다** · Phase 7 의 빌드 절차
- **출력**: ① **운영 origin 을 박은 최종 빌드 아티팩트** ② 그 아티팩트 위의 `AC-T24` 통과
  ③ M-1·M-5 의 **«최종»** 확인 ④ 배포 순서 기록
- **설명**: 순서가 계약이다 — **운영 origin 설정 → 최종 빌드 → 그 아티팩트 검증.**
  **Phase 9 는 이 아티팩트를 고치지 않고 그대로 발행한다.**

**작업**

1. `capabilities` 의 `remote.urls` 를 **운영 origin 정확히 하나**로 바꾼다.
   **와일드카드 서브도메인을 쓰지 않는다.**
2. **네비게이션 허용 목록**을 확정한다 — 인증이 밖으로 나가지 않으면 **하나**다.
   나간다면 그 주소를 더하되, **그 주소에 커맨드를 주지 않는다**(목록이 둘인 이유).
3. **최종 빌드를 굽는다** — 판 번호 셋을 맞춘 채로. **이것이 발행될 아티팩트다.**
4. **그 아티팩트를 검증한다** — `AC-T24`, 그리고 **M-1·M-5 최종 확인**(운영 https 문서에서 커맨드
   왕복이 되는가, 앱 재시작 뒤 쿠키가 남는가).
5. **배포 순서를 기록한다** — **웹(서버) 먼저, 셸 나중**을 권장안으로.
   근거: 웹이 앞서 나가도 브라우저에서는 `E-01` 로 조용하고, 셸이 앞서 나가도 웹이 안 부를 뿐이다
   (`features` 기반 기능 탐지). **어느 쪽이든 안전하지만 하나를 정해 둔다.**
6. **호환 범위를 기록한다** — 이 판의 셸이 여는 주소와 `shell_api` 값. 웹이 새 기능을 내도
   **그 기능만 끄고 나머지는 정상 동작한다.** 「업데이트하세요」로 앱을 막지 않는다.

**하지 말 것**

- **검증한 뒤에 설정을 고치지 마라.** 고쳤으면 **다시 빌드하고 다시 검증한다** — 발행되는 판과
  검증된 판이 달라지는 것이 F-3 이 막으려는 사고다
- **운영 origin 을 커맨드 목록과 네비게이션 목록에 같은 것으로 뭉개지 마라**
- **개발·fixture origin 을 최종 설정에 남기지 마라**

**검증**

- [ ] 운영 origin **밖** 문서가 커맨드를 부르지 못함을 보였다
- [ ] 네비게이션 목록에 다른 주소가 있어도 **그 주소는 커맨드를 못 부른다**
- [ ] M-1·M-5 의 최종 관측값이 fixture 결과와 **같다**(다르면 그 차이가 기록된다)
- [ ] **검증한 아티팩트의 해시(또는 빌드 식별자)가 기록됐다** — Phase 9 가 같은 것을 올린다

**완료 기준 — 이 Phase 가 닫는 인수조건 1건**

`AC-T24` (커맨드를 쓸 수 있는 origin 이 운영 origin 하나뿐이다)

- [ ] Phase 3 에서 **개발 origin 잠정**이었던 AC-T24 가 최종 통과로 갱신됐다
- [ ] **발행 대상 아티팩트가 하나로 정해졌다**

**의존**: Phase 5 · **Phase 6b** · Phase 7

**실패 시 다음 조치**: 운영 origin 에서 IPC 가 안 되면(fixture 에서는 됐는데) → **발행하지 않고**
원인을 기록한다. 흔한 원인은 origin 표기 차이(포트·트레일링 슬래시·서브도메인)다 — **와일드카드로
넓혀서 통과시키지 않는다.**

---

### Phase 9 — Release 발행과 기록

- **Status**: TODO
- **소유**: 코디(절차·검증) + **사용자**(발행 승인)
- **파일 범위**: 코드 레포의 **태그** · GitHub Releases · 프로필 레포 `60-release/`(발행 시점에 생긴다)
- **입력**: **Phase 8 이 검증한 아티팩트** · OQ-T03(배포 대상·서명·공증·업데이트)
- **출력**: ① 태그 ② GitHub Release(설치파일) ③ `60-release/` 릴리즈 문서 ④ 기록 셋
- **설명**: **Phase 8 이 검증한 판을 그대로 올린다.** 여기서 빌드를 다시 하지 않고, 설정을 고치지 않는다.

**작업**

1. **태그를 단다** — `vX.Y.Z`. `tauri.conf.json` 의 `version`·`shell_info().app_version` 과 같은 값.
2. **Release 를 발행한다** — 코드 레포 GitHub Releases 에 **Phase 8 이 검증한 설치파일**.
3. **`60-release/` 릴리즈 문서를 쓴다** — 같은 버전·태그와 **Release 링크로 잇는다**.
4. **기록으로 남길 것 셋**(SPEC §5) — 판 번호 · **그 판이 여는 운영 주소** · `shell_api` 값.
   여기에 **호환 조합**을 함께 적는다 — **그때 서버에 떠 있던 이미지 태그와 웹 빌드**(Phase 6b 의 배포 기록).
   **서버 판과 셸 판은 같은 아티팩트가 아니다** — 둘을 잇는 것은 **같은 운영 origin 과 이 조합 기록**이다.
5. **미서명이면 실행 절차를 문서에 넣는다** — macOS Gatekeeper 경고를 사용자가 어떻게 넘기는지.
6. **Windows 축의 상태를 적는다** — 검증됐으면 검증본으로, 아니면 **「검증 불가」 또는 「보류」**로.
   **검증된 것처럼 쓰지 않는다.**

**하지 말 것**

- **여기서 빌드하지 마라.** 발행 대상은 Phase 8 이 검증한 아티팩트 **그것 하나**다
- **사용자 승인 없이 발행하지 마라**
- **실제 발행 전에 완료 기록을 만들지 마라**
- **아직 없는 명령·주소를 실행 가능한 절차처럼 쓰지 마라**

**검증**

- [ ] 발행한 자산의 **해시(또는 빌드 식별자)가 Phase 8 의 기록과 같다**
- [ ] 판 번호 셋이 같다 — 태그 · `tauri.conf.json` · `shell_info().app_version`
- [ ] Release 자산 목록과 프로필 릴리즈 문서의 링크가 **서로를 가리킨다**
- [ ] Windows 축의 상태가 **사실대로** 적혔다

**완료 기준 — 이 Phase 가 닫는 인수조건: 없음**

인수조건은 Phase 8 까지 전부 닫힌다. 이 Phase 가 닫는 것은 **DEC-005 D-09**
(코드 Releases 에 설치파일 · 프로필 `60-release` 에 문서 · 같은 버전·태그와 링크)다.

**의존**: Phase 8 · OQ-T03

**실패 시 다음 조치**: 발행 후 문제가 드러나면 **Release 를 내리고 기록에 남긴다.**
⚠ **이미 받은 사람의 설치파일은 회수되지 않는다**(§Rollback).

---

## 실측 계획 — M-1 ~ M-14 와 M-2b 전수 (15건)

SPEC-006 §6 의 열다섯을 **하나도 빼지 않고** 배정한다. **ID 를 늘리지 않는다** — 같은 항목을 두 번
재야 하면 **증거 단계**(`① fixture` · `② 제품판` · `③ 운영판`)로 가른다. `어디서` 는 SPEC 이 가른
**「개발 fixture 로 되는 것」과 「운영 주소가 있어야 하는 최종 확인」**을 그대로 옮긴 것이다.

| # | 무엇을 재나 | 증거 단계 (Phase) | 담당 | 방법 | 증거 | 선행조건 | OS 축 |
|---|---|---|---|---|---|---|---|
| **M-1** | 원격 https 문서에서 셸 커맨드 호출이 성립하는가 | ① fixture(**2**) · ③ 운영판(**8**) | 워커+코디 | **로컬 https fixture** origin 을 `remote.urls` 에 넣고 계측 페이지에서 커맨드 넷 왕복 → Phase 8 에서 **운영 origin 을 박은 최종 빌드**로 반복. **평문 `localhost` 로 대신하지 않는다**(SPEC §6 M-1 이 https 를 지정했고 중단 판정의 근거다) | 요청·응답 로그, 실패 시 에러 원문 | ① Phase 1 의 https fixture · ③ **Phase 6b 의 운영 주소** | 둘 다 |
| **M-2** | 이 제품의 녹음 포맷이 열리는가 — **두 경로 × 셋** | ① fixture(**2**) | 사용자+코디 | **경로를 가른다.** ⓐ **회의 라이브** — `microphone.ts:17` 의 **단일 MIME**(`audio/webm;codecs=opus`, 후보 없음): 지원 여부 · **장시간** 녹음 · **WS 스트림으로 서버가 받는가**. ⓑ **브라우저 인터랙션** — `liveTranscription.ts:13-15` 의 **후보 셋**: **어느 후보로 떨어지는가** · 장시간 · **멀티파트 업로드를 서버가 받는가** | 경로별 세 갈래 = **여섯 칸**. ⓑ 는 낙착된 후보 이름 포함 | Phase 1 + 평문 `localhost` 스택 | 둘 다 |
| **M-2b** | 만료 시각을 넘겨 **열린 스트림이 계속 도는가** | ① fixture(**2**) · ② 제품판(**5**, AC-T28 용) | 코디 | 개발 DB 의 세션 행 `expires_at` 을 과거로 당긴 뒤, **이미 열린** 회의 스트림이 닫히는지 본다. **제품 코드 0줄.** ② 에서는 **제품 배선 위에서** 「녹음이 안 끊기고 **점유도 유지되는가**」까지 본다 | 스트림 상태 전이 로그 · 조작한 시각 · ② 는 점유 상태 | 로컬 스택 + 로그인 세션 / ② Phase 4 배선 | 무관 (서버 동작) |
| **M-3** | 앱 내 화면 전환·같은 문서 주소 변경에서 **셸의 네비게이션 훅이 발화하는가** | ① fixture(**2**) | 워커+코디 | 계측 페이지에서 `history.replaceState`·SPA 전환을 일으키고 훅 로그를 본다. **재는 것은 훅이지 점유가 아니다** | 훅 발화 로그(발화/미발화) | Phase 1 | 둘 다 |
| **M-4** | 마이크 권한 프롬프트가 뜨는가 / 별도 처리가 필요한가 | ① fixture(**2**) | 사용자 | 각 OS 의 탐침 셸에서 `getUserMedia` 를 부른다(평문 `localhost` 로 충분 — secure context). macOS 는 `Info.plist`, Windows 는 `PermissionRequested` 핸들러 유무로 갈린다 | 프롬프트 스크린샷 또는 실패 원문 | Phase 1 (plist·핸들러 포함) | 둘 다 |
| **M-5** | 앱 재시작 후 웹뷰가 세션 쿠키를 유지하는가 | ① fixture(**2**) · ② **제품 셸판**(**5**) · ③ 운영판(**8**) | 사용자 | 로그인 → 앱 완전 종료 → 재실행 → 로그인 화면이 뜨는가. ② 가 필요한 이유는 **제품 셸의 식별자·저장소 설정이 탐침과 다르기 때문**이다(Phase 4 배선과는 무관) | 재실행 뒤 화면 · 경과 시간 | ① Phase 1 · ② Phase 3 제품 셸 · ③ Phase 6b 운영 주소 | 둘 다 |
| **M-6** | 웹의 창 닫기 되묻기가 **앱 창 닫기**에서 도는가 | ① fixture(**2**) · ② 제품판(**5**) | 사용자 | ① 브라우저 인터랙션 녹음 중(`beforeunload` 가드가 사는 자리) 앱 창을 닫아 본다 → **어느 층이 낼 수 있는가**. ② 구현된 뒤 **확인 창이 하나만 뜨는가** | ① 확인 창의 유무·출처 / ② 창의 개수 | ① Phase 1 · ② Phase 3 또는 4 의 구현 | 둘 다 |
| **M-7** | 연결 실패를 셸이 **감지할 수 있는가** | ① fixture(**2**) | 워커+코디 | 닿지 않는 주소로 창을 열고 셸이 받을 수 있는 신호를 찾는다. **없으면 구현 차단 사유** | 감지 수단의 이름 또는 「없음」 | Phase 1 | 둘 다 |
| **M-8** | 외부 링크가 웹뷰에서 무엇을 하는가 | ① fixture(**2**) | 워커+코디 | `window.open(…, "_blank")` 를 계측 페이지에서 호출 — 새 웹뷰 / 무반응 / 외부 브라우저 중 무엇인가 | 관측된 동작 | Phase 1 | 둘 다 |
| **M-9** | 절전 방지가 **자동 절전만** 막는가 | ① fixture(**2**) · ② **제품판**(**5**) | **사용자** | 점유를 건 상태로 ① 입력 없이 `max(3T, 30분)` 대기 → 안 잠드는가 ② **화면은 꺼지는가** ③ **직접 잠자기·덮개 닫기는 되는가**. ⚠ **AC-T01~T04 의 증거는 제품판이어야 한다** — AC-T01 이 「회의 업스트림으로 마이크가 열린 뒤」를 조건으로 걸기 때문이다. **M-11 과 같은 회차에 재고 그 기록에 병기한다** | `T` 값 · 관찰 시간 · 셋 각각의 결과 · 단계 표기 | ① Phase 1(OS 호출까지) · ② Phase 4 배선 | 둘 다 |
| **M-10** | 재설치·판 올림 후 웹뷰 저장소가 남는가 | ① fixture 판(**7**) | **사용자** | 같은 식별자로 **fixture origin 판 두 개**를 설치·덮어쓰고 로그인 유지 여부를 본다 | 두 판의 버전 · 재실행 뒤 화면 | **설치파일 두 판** (Phase 7) | 둘 다 |
| **M-11** | **숨김·최소화·화면 꺼짐**으로 장시간 — 녹음이 이어지고 점유가 유지되는가. **두 녹음 화면 각각** | ② 제품판(**5**) | **사용자** | 제품 화면에서 녹음을 걸고 창을 최소화·가림·화면 꺼짐 상태로 `max(3T, 30분)` 이상. **M-9 의 제품판 증거를 여기 병기한다** | 시작·종료 시각 · 스크립트 도착 여부 · 점유 상태 | Phase 4 배선 | 둘 다 |
| **M-12** | 수동 잠자기·덮개 닫기로 재운 뒤 **복귀 상태**, 그리고 **같은 키 재요청으로 다시 걸리는가** | ② 제품판(**5**) | **사용자** | 녹음 중 직접 재우고 깨운 뒤 재확인 1회가 무엇을 돌려주는지 본다 | 복귀 직후 `state` · 재요청 뒤 `state` · U-3 의 등장/소멸 | Phase 4 배선 | 둘 다 |
| **M-13** | **취소된 사건**에서 점유가 유지되는가 | ② 제품판(**5**) | **사용자** | ① 닫기 되묻기에서 `계속 녹음` → **그 뒤 자동 절전 시간을 넘겨도 안 잠드는가** ② 셸이 막은 외부 이동 뒤 점유가 남는가 | 두 경우의 점유 상태 · 절전 관찰 시간 | Phase 3 훅 + Phase 4 배선 | 둘 다 |
| **M-14** | **늦은 완료와 정리 실패** — 최종 잔존이 0 인가, `release` 실패 시 무엇이 남는가 | ② 제품판(**5**) | 워커+사용자 | ① 마이크가 열리기 전 화면 이탈 ② 획득이 날아가는 중 정리 ③ 문서 교체 직전 요청 ④ `release` 를 강제로 실패시킴 | 네 경우의 **최종 잔존** · `release` 실패 뒤 화면 문구 | Phase 4 배선 | 둘 다 |

**합계 15건 — ID 는 늘지 않았다.**

| Phase | 재는 항목 |
|---|---|
| **2** (fixture) | `M-1` `M-2` `M-2b` `M-3` `M-4` `M-5` `M-6` `M-7` `M-8` `M-9` — **열** |
| **5** (제품판) | 새 ID 넷 `M-11` `M-12` `M-13` `M-14` + **제품판 증거가 필요한 기존 넷** `M-9` `M-2b` `M-6` `M-5` |
| **7** (fixture 판 설치) | `M-10` |
| **8** (운영판) | `M-1` `M-5` 의 **최종 확인** |

> **Phase 5 의 「기존 넷」은 새 측정 항목이 아니라 같은 ID 의 둘째 증거 단계다.**
> 어느 것을 **다시 재고** 어느 것을 **인용**하는지는 Phase 5 의 판단표가 갖는다 —
> 이번 판단으로 **인용으로 끝나는 것은 AC-T27 하나**다.

---

## 인수조건 추적 — AC-T01 ~ AC-T43 전수 (43건)

**어느 Phase 가 닫나 · 무엇으로 닫나.** 「증거」는 그 Phase 의 완료 기록에 붙는 것이고,
**이 문서에서 미리 체크하지 않는다.**

### Phase 3 — 제품 셸 (15건)

| AC | 무엇 | 방법 | 실측 |
|---|---|---|---|
| AC-T12 | 같은 세션 키 중복 획득이 점유를 늘리지 않고 한 번에 풀린다 | 셸 단독 조작 | M-1 |
| AC-T13 | 지난 녹음의 늦은 해제가 지금 녹음을 풀지 않는다 | 셸 단독 조작 | M-1 |
| AC-T14 | 모르는·이미 푼 키로 풀어도 에러가 없다 | 셸 단독 조작 | M-1 |
| AC-T15 | 해제를 못 부른 채 창이 닫혀도 풀린다 | 창 닫기 관찰 | M-1 |
| AC-T16 | 문서가 통째로 바뀌면 풀린다 | 새로고침·재로드 | M-1 |
| AC-T17 | 앱 내 전환·같은 문서 주소 변경을 **문서 교체로 보지 않는다**(훅을 잰다) | 훅 로그 | **M-3** |
| AC-T18 | 프로세스가 끝나면 OS 절전 방지가 남지 않는다 | 강제 종료 뒤 OS 상태 조회 | M-1 |
| AC-T20 | 허용 네비게이션 밖으로 창이 가지 않고 기본 브라우저가 연다 | 이동 시도 | — |
| AC-T21 | 외부 링크가 OS 브라우저에서 열리고 창 안에 앉지 않는다 | 링크 클릭 | **M-8** |
| AC-T22 | `http(s)` 아닌 주소는 열리지 않는다 | 스킴 주입 | M-1 |
| AC-T23 | 커맨드가 넷뿐 — 파일·프로세스·셸 권한 0 | **설정 파일 사람이 읽기** | — |
| AC-T25 | 셸 프레임워크 2.11.1 이상 | `Cargo.toml` 검사 | — |
| AC-T31 | 닿지 못하면 U-2 가 보이고 `다시 시도` 가 동작 | 주소 차단 뒤 관찰 | **M-7** |
| AC-T33 | 트레이·상주·추가 창이 없다 | 설정 + 실행 관찰 | — |
| AC-T34 | 앱 식별자가 다른 제품과 겹치지 않는다 | 설정 대조(참조 제품 포함) | — |

### Phase 4 — 웹 배선 (5건)

| AC | 무엇 | 방법 | 실측 |
|---|---|---|---|
| AC-T08 | 마이크가 안 열리면 획득하지 않는다 | 권한 거부 상태로 회의 진입 | M-1 |
| AC-T09 | 구독 역할은 획득하지 않는다 | 구독으로 붙기 | M-1 |
| AC-T10 | 자리를 뺏겨 구독이 되면 풀린다 | 두 창에서 같은 회의 | M-1 |
| AC-T11 | 실패해도 녹음은 계속되고 **두 화면 어디서든** U-3 한 줄 | `degraded`·호출 실패를 강제 주입 | M-1 |
| AC-T42 | 세션 키가 회차마다 다르다 | **코드 읽기** — 회의 id 를 키로 쓰지 않는다 | — |

### Phase 5 — 제품 통합 재측정 (21건)

**「실측」 칸의 단계 표기** — `제품판` 은 **이 Phase 에서 다시 재는 것**, `인용` 은 **Phase 2 의
fixture 기록을 출처와 회차를 적어 쓰는 것**이다. 근거는 Phase 5 의 판단표가 갖는다.

| AC | 무엇 | 방법 | 실측 |
|---|---|---|---|
| AC-T01 | 마이크가 열린 뒤 자동 절전 시간을 넘겨도 잠들지 않고 녹음·스크립트가 이어진다 | **제품 녹음 위** 실기 장시간 | **M-9 제품판** |
| AC-T02 | 같은 상태에서 **화면은 꺼진다** | **제품 녹음 위** 실기 관찰 | **M-9 제품판** |
| AC-T03 | 직접 잠자기·덮개 닫기는 **잠든다** | **제품 녹음 위** 실기 조작 | **M-9 제품판** |
| AC-T04 | 끝난 뒤 평소 자동 절전으로 돌아간다 | **제품 녹음 위** 실기 관찰 | **M-9 제품판** |
| AC-T05 | **비가시 상태**로 `max(3T,30분)` — 녹음 유지·점유 유지 | 실기 장시간 | **M-11** |
| AC-T06 | **화면 꺼짐** 상태로 같은 시간 | 실기 장시간 | **M-11** |
| AC-T07 | **두 녹음 화면 각각**에서 T05·T06 성립 | 두 화면 따로 | **M-11** |
| AC-T19 | 수동 절전 복귀 뒤 재확인 — 이어지면 `on` 재무장, 끝났으면 해제 | 실기 조작 | **M-12** |
| AC-T26 | 앱 재시작 뒤 만료 전이면 로그인 유지 | **제품 셸**로 실기(탐침과 셸 설정이 다르다) | **M-5 제품 셸판** |
| AC-T27 | 만료 뒤에는 재실행·재접속에서 로그인 화면. **시각 경과만으로 바뀌지 않는다** | 세션 조작 — **배선과 무관한 서버·웹 동작** | **M-2b 인용**(Phase 2 기록, 회차 표기) |
| AC-T28 | 녹음 중 만료 시각이 지나도 녹음·점유가 이어진다 | 세션 조작 — **점유 유지가 배선에 달렸다** | **M-2b 제품판** |
| AC-T29 | 앱에서 회의·메모·안건·자료·업무가 브라우저와 같게 동작 | 회귀 통과 | — |
| AC-T30 | 브라우저로 열면 지금과 완전히 같다 — 에러·경고 0 | 브라우저 회귀 | — |
| AC-T32 | 녹음 중 닫기 요청에 되묻기가 뜨고 즉시 닫히지 않는다 | 실기 조작 | **M-6 제품판** |
| AC-T36 | `계속 녹음` 이면 창·녹음·**점유가 남고**, 그 뒤 절전 시간을 넘겨도 안 잠든다 | 실기 장시간 | **M-13** |
| AC-T37 | 셸이 막은 이동 뒤 점유가 유지된다 | 이동 시도 | **M-13** |
| AC-T38 | 되묻기가 **하나만** 뜬다 | 실기 관찰 — **구현된 뒤에만 답이 난다** | **M-6 제품판** |
| AC-T39 | `degraded` 에서 사건 재요청으로 재무장되고 U-3 이 사라진다. 실패하면 남고 녹음은 계속 | 실기 조작 | **M-12** |
| AC-T40 | 마이크 열리기 전 이탈·요청 중 정리에서 **최종 잔존 0** | 경합 유도 | **M-14** |
| AC-T41 | 문서 교체 뒤 이전 문서의 획득이 새 점유를 만들지 않는다 | 경합 유도 | **M-14** |
| AC-T43 | `release` 실패 시 녹음이 다시 켜지지 않고 사실이 드러난다. 창 닫으면 정리된다 | 실패 주입 | **M-14** |

### Phase 7 — 설치 빌드와 fixture 판 검증 (1건)

| AC | 무엇 | 방법 | 실측 |
|---|---|---|---|
| AC-T35 | 재설치·판 올림 뒤에도 웹뷰가 세션 쿠키를 들고 있다 | **fixture origin 판 두 개**를 설치·덮어쓴다 | **M-10** |

### Phase 8 — 운영 origin 판 최종 확인 (1건)

| AC | 무엇 | 방법 | 실측 |
|---|---|---|---|
| AC-T24 | 커맨드를 쓸 수 있는 origin 이 **운영 origin 하나**뿐 | 설정 + 외부 origin 호출 시도. **대상은 「운영 origin 을 박고 최종 빌드한 아티팩트」** — Phase 9 가 그것을 그대로 발행한다 | **M-1 운영판** |

### Phase 6a · 6b · 9 — 닫는 인수조건 0건

세 Phase 는 **전제를 세우거나 결과를 내보내는 단계**라 인수조건을 닫지 않는다.
6a·6b 는 **Phase 8 의 입력**(운영 주소)을 만들고, 9 는 **DEC-005 D-09**(Releases·`60-release`·링크)를 닫는다.

**합계**: 15 + 5 + 21 + 1 + 1 + 0 = **43건. 누락 0 · 중복 0.**

---

## DEC-005 결정 추적 — D-01 ~ D-09 전수

| ID | 결정 | 이 work 가 받는 자리 | 상태 |
|---|---|---|---|
| **D-01** | 기존 웹의 데스크톱 래퍼 | Phase 3·4 — 웹 변경은 **둘뿐**(U-3 한 줄 + 점유 배선). §Code Surface 의 「안 건드리는 자리」가 그 증명 | **받음** |
| **D-02** | 세션 쿠키 유지, 키체인·Bearer 아님 | Phase 3 — `Cargo.toml` 에서 `keyring` 을 **가져오지 않는다**. `Secure` 요건은 **6a 가 설계하고 6b 가 구현한다**(권한 불변 — 구현 선택) | **받음** |
| **D-03** | 시작·재개에 방지, 일시정지·종료에 해제. 화면 꺼짐 허용, 수동 절전 안 막음 | Phase 3 의 OS 플래그 선택 · Phase 5 의 AC-T01~T03 | **부분** — **일시정지가 제품에 없다.** L-15 는 조건부이고 이 work 가 그 기능을 만들지 않는다 (OQ-T05) |
| **D-04** | OS 알림 연결은 래퍼 책임, 시스템 자체는 후속 | **자리만 비워 둔다** — `features` 에 이름 하나가 늘 자리. 이번에 만들지 않는다 | **경계만** |
| **D-05** | 참조 제품의 빌드 구성 계승, 이름·식별자·아이콘·주소는 분리 | Phase 1·3 의 계승표 · AC-T34 | **받음** |
| **D-06** | 일회성이 아니라 구조·절차·판별 결과를 문서화 | Phase 9 의 「기록으로 남길 것 셋」 · 6a 의 배포 설계 · 절차서는 `70-runbook` 으로 | **부분** — 절차서 작성은 후속 |
| **D-07** | macOS·Windows 둘 다 | 모든 실측의 **OS 축** · Phase 7 의 빌드 환경 · Phase 9 의 상태 표기 | **받음 — 양쪽 지원을 유지한다.** ⚠ **Windows 실기·빌드 환경 둘 다 미확인**(OQ-W01·OQ-W06)이면 **그 축을 보류**한다. **macOS 단독 출시는 기본 행동이 아니고**, 범위를 줄이려면 OQ-W06 처분으로 **사용자 승인**을 받는다 |
| **D-08** | Mac Studio 의 기존 k8s 에 FE·BE | **Phase 6a(설계) · 6b(실행)** | **받음** — 6b 가 **실제로 세운다**. 남은 gate 는 **도메인 값**(OQ-T02)과 **외부 레포 푸시 범위**(OQ-W02) 둘 |
| **D-09** | 코드 Releases 에 설치파일, 프로필 `60-release` 에 문서 | **Phase 9 전체** | **받음** — 발행 대상은 **Phase 8 이 검증한 아티팩트**이고, 실제 발행은 사용자 승인 뒤 |

---

## 미결 게이트 — 무엇이 어느 Phase 를 막나

**막는 범위 밖의 작업은 이것 때문에 멈추지 않는다.** 그리고 **「진짜 결정」과 「구현 선택」을 가른다** —
권한·계약·비용·장비가 걸리지 않는 기술 선택은 **코디 기본값으로 통보하고 진행**한다.
사용자가 뒤집으면 그때 바꾼다.

### 사용자 결정 — 문서로 답이 안 나는 것

| ID | 질문 | 주인 | 막는 Phase | 막지 **않는** 것 |
|---|---|---|---|---|
| **OQ-T01** | 최소 OS · CPU 아키텍처 · 설치파일 형식 | 사용자 | **7 · 8 · 9**(빌드 타깃) | 1~5·6a·6b (개발자 자기 기기로 잰다) |
| **OQ-T02** | **운영 도메인** — 소유한 이름이 있어야 한다 | 사용자 | **6b 의 ingress·DNS · 8 · 9** | 1~5 · **6a 의 구조 설계 전체**(값 자리만 비운다) · 7 |
| **OQ-T03** | 배포 대상 · 서명 · 공증 · 자동 업데이트 | 사용자 | **9**(발행) · 8 의 서명본 검증 | 앱이 도는 것 · 1~7 |
| **OQ-T04** | 로그인 유지 기간(12시간을 바꿀 것인가) | 사용자 | **없음** | 전부. AC-T26·T27 은 현재 값(12h)으로 잰다 |
| **OQ-T05** | 녹음 일시정지·재개를 만들 것인가 | 사용자 | **없음** | 전부. L-15 는 이 work 의 인수조건에 **들어 있지 않다** |
| **OQ-T09** | 브라우저·앱의 로컬 초안이 서로 안 보이는 것 | 사용자 | **없음** | 전부 |
| **OQ-T11** | 세션 만료를 열린 스트림·화면에 전파할 것인가 | 사용자 | **없음** | 전부. 지금 동작을 그대로 계약했다 |
| **OQ-W01** | **Windows 실기를 갖고 있는가** | 사용자 | **2 · 5 · 7 · 8 의 Windows 축** | macOS 축 전부 |
| **OQ-W02** | **회사 org 레포**(`MediSolveAIDev/k8s_infra_mac`)**에 개인 제품 구성을 발행해도 되는가** | 사용자 | **6b 작업 5 — 「외부 레포 푸시·PR」 한 지점** | **6a 전체 · 6b 작업 1~4**(로컬 작성·렌더·이미지·정리)와 그 밖의 Phase. **권장안: 그 레포를 그대로 쓴다** — 클러스터와 ArgoCD 가 이미 이 레포를 본다 |
| **OQ-W05** | **권한 완화**(로컬 로그인 개방 등) 또는 **새 인증 방식**(외부 IdP·OIDC) 도입 | 사용자 | **그 변경 자체.** 필요해졌을 때만 열린다 | **기존 권한·쿠키 계약을 유지하는 내부 정리는 막지 않는다** — 6a 가 설계하고 6b 가 구현한다. ⚠ **development/test 프로파일로 운영하는 우회는 금지** |
| **OQ-W06** | Windows 설치파일 **빌드 환경**(실기 / 러너 / 없음), 그리고 **없을 때 범위를 줄일 것인가** | 사용자 | **7 · 8 · 9 의 Windows 축** | macOS 축 전부. ⚠ **승인 전에는 Windows 축이 「보류」로 열린 채 남는다** — macOS 단독 출시를 기본 행동으로 쓰지 않는다 |

### 실측이 답하는 것

| ID | 질문 | 막는 Phase | 비고 |
|---|---|---|---|
| **OQ-T07** | 대상 OS·웹뷰에서 녹음 포맷이 열리는가 | **Phase 2 의 판정** | **이것이 중단 사유다.** 단 중단 조건은 **회의 라이브 경로**에 한정한다 — 브라우저 경로는 이미 후보 셋을 갖는다 |

### 구현이 고르는 것 — **사용자 gate 가 아니다**

코디 기본값으로 진행하고, 결과를 통보한다. **기술 선택마다 사용자 확인을 만들지 않는다.**

| ID | 무엇 | 코디 기본값 | 왜 gate 가 아닌가 |
|---|---|---|---|
| **OQ-T06** | 커맨드 허용 origin 의 **값** | 운영 origin 정확히 하나(값은 OQ-T02 가 준다) | 모양은 Phase 3 에서 확정됐다. 값은 결정이 아니라 대입이다 |
| **OQ-T08** | 웹이 살아 있는 채 멈춘 경우의 점유(L-12) | 탐지하지 않는다 — 계약이 이미 그렇게 닫혔다 | 계약이 「탐지 안 함·남음」으로 닫혀 있다 |
| **OQ-T10** | 창을 닫으면 프로세스가 끝나는가 | OS 관례를 따른다 | AC-T33 의 해석만. 어느 쪽이든 L-06 이 푼다 |
| **OQ-W03** | 운영 서버 **arm64 이미지** | **6a 작업 1 의 확인 결과를 따른다** — 보호 요구가 **납품 경로 전용**이면 운영용 arm64 이미지를 **따로** 만들고(납품 경로 파일을 한 줄도 안 고치므로 **보호 요구를 훼손하지 않는다**), **운영에도 적용되면** `delivery/` 를 arm64 로 확장한다 | **arm64 이미지를 만드는 것 자체는 운영 목표에 필요한 구현**이다. 「이미지가 하나 는다」는 비용만으로 gate 를 만들지 않는다. **사용자 결정은 「납품 경로의 보호 수준을 낮출 때」 하나뿐**이고, 기본안은 그것을 하지 않는다 |
| **OQ-W04** | FE 정적 서빙 방식 | **A — ingress 경로 분기**(한 호스트 · `/` → 정적 FE 컨테이너 · `/api`·WS → back) | **제품 계약을 바꾸지 않는 구현 선택**이다. 제품 코드를 건드리지 않는 쪽이 A 다. 대안 B(백엔드 `StaticFiles`)는 A 가 막힐 때만 본다 |

> **`OQ-W01` ~ `OQ-W06` 은 이 work 가 여는 미결이다.** DEC-005·SPEC-006 의 OQ 번호와 겹치지 않게
> `W` 를 붙였다. **DEC·SPEC 을 고치지 않았다** — 승격이 필요하면 코디가 판단한다.
>
> **1차 계획 대비 줄어든 것**: `OQ-W03`·`OQ-W04` 를 **사용자 결정에서 구현 선택으로** 내렸고,
> `OQ-W02` 의 차단을 **6 전체 → 6b 의 푸시 한 지점**으로, `OQ-W05` 의 차단을
> **6·8 전체 → 「권한 완화·새 인증이 필요해진 때」**로 좁혔다. **사용자 결정 7 → 5**(T01·T02·T03·W01·W06)
> 에 **조건부 둘**(W02 의 푸시 범위 · W05 가 열릴 때)이다.

---

## Pre-deploy Check

배포·외부 연동 활성화 **직전**에만 본다. Phase 완료 조건을 복제하지 않고 **운영 리스크만** 둔다.

- [ ] **기존 Mediness 에 영향이 없다** — 네임스페이스 · Argo Application · values · ingress 호스트 ·
      데이터스토어가 전부 분리돼 있고, 기존 파일의 diff 가 0줄이다
- [ ] **커맨드 허용 origin 에 개발·fixture 주소가 남아 있지 않다**
- [ ] **운영 세션 쿠키에 `Secure` 가 붙는다** — 안 붙으면 배포하지 않는다
- [ ] **권한 판정이 넓어지지 않았다** — 운영 프로파일 내부 정리가 권한을 한 칸도 열지 않았다
- [ ] **development/test 프로파일로 운영을 띄우지 않았다**
- [ ] **비밀값이 이미지·차트·설정에 들어가 있지 않다.** 설치 환경의 주입 수단으로만 전달된다
- [ ] **영속 볼륨이 지정돼 있고, 백업이 한 번 이상 확보돼 있다** — 기본값(작업 디렉토리 아래)으로 뜨면
      교체 시 데이터가 사라진다
- [ ] **발행 대상이 「Phase 8 이 검증한 아티팩트」 그것 하나다** — 검증 뒤에 설정을 고치지 않았다
- [ ] **설치파일이 여는 주소가 운영 주소다.** 판 번호 셋(태그·설정·`app_version`)이 같다
- [ ] **서명·공증을 하지 않았다면 그 사실과 실행 절차가 릴리즈 문서에 있다**
- [ ] **Windows 축이 「검증 불가」 또는 「보류」라면 그 사실이 릴리즈 문서에 있다** —
      검증된 것처럼 쓰지 않고, **범위 축소에는 사용자 승인이 있어야 한다**

## Rollback

**되돌리는 것(코드·설정·배포판)과 지키는 것(데이터)을 가른다.**
⚠ **데이터 삭제는 rollback 절차가 아니다.** 아래 어느 칸에도 「볼륨을 지운다 · DB 를 초기화한다」가
없고, 그것이 의도다 — 배포 실패는 **재배포**로 푼다.

### A. 되돌리는 것 — rollback 절차

| 무엇을 되돌리나 | 방법 | 기존 기능 영향 |
|---|---|---|
| **웹 배선(Phase 4)** | 해당 커밋 revert. `shell.ts` 는 셸이 없으면 아무것도 하지 않으므로 **브라우저 동작은 처음부터 불변**이다 | **없음.** U-3 한 줄과 호출이 사라질 뿐 |
| **셸(Phase 3)** | `frontend/src-tauri/` 제거 또는 빌드 중단. **웹은 그대로 돈다** | **없음.** 셸은 웹의 의존이 아니다 |
| **운영 프로파일 내부 정리(Phase 6b)** | 해당 커밋 revert → 이전 이미지 태그로 되돌린다 | **없음**(권한이 넓어지지 않았으므로 되돌려도 좁아지지 않는다) |
| **운영 이미지 · 차트 · values(Phase 6b)** | values 의 이미지 태그를 이전 값으로 되돌리고 ArgoCD 가 sync 하게 둔다 | 워크로드만 이전 판으로. **볼륨·DB 는 그대로 남는다** |
| **설치파일(Phase 7·9)** | 이전 판을 다시 설치한다. **식별자가 같으므로 웹뷰 저장소가 남아 로그인이 유지된다**(M-10 이 그 전제를 잰다) | 없음 |
| **부분 revert** | **셸만 되돌리는 것은 안전하다**(웹이 셸 없이 돈다). **웹만 되돌리는 것도 안전하다**(셸이 커맨드를 갖고만 있게 된다) | 두 방향 모두 안전. 이것이 `features` 기반 기능 탐지를 둔 이유다 |

### B. 지키는 것 — 보존 · 백업 · 복구

**rollback 으로 다루지 않는다.** 되돌릴 수 없고, 되돌리려 시도하는 것 자체가 사고다.

| 데이터 | 어디 | 보존 | 백업 | 복구 증거 |
|---|---|---|---|---|
| **녹음 원본** | `AX_RECORDINGS_DIR` 가 가리키는 영속 볼륨 | Application 을 지워도 **볼륨이 남는 설정**으로 둔다(6a 작업 6) | 배포 **전에** 한 벌. 이후 주기는 6a 가 정한다 | **복구를 한 번 해 보고** 파일이 열리는 것을 확인한 기록 |
| **업무·회의 자료** | `AX_MATERIALS_DIR` 가 가리키는 영속 볼륨 | 같다 | 같다 | 같다 |
| **DB** | 새 Postgres(기존 `mediness-*` 와 공유하지 않는다) | PVC 를 Application 수명과 분리한다 | 배포 전 덤프 한 벌 | 덤프를 **빈 DB 에 넣어 본 기록** |

**규칙 넷**

1. **배포 실패를 데이터 삭제로 풀지 않는다.** 재배포·이전 태그 복귀가 먼저다
2. **볼륨·PVC 를 지우는 것은 rollback 이 아니라 «파기»다** — 사용자 승인 없이 하지 않는다
3. **백업이 없으면 배포하지 않는다**(Pre-deploy Check)
4. **복구를 한 번도 해 보지 않은 백업은 백업이 아니다** — 증거 칸이 그래서 있다

### C. 되돌릴 수 없는 것 — 미리 적는다

- **앱 식별자**를 바꾼 뒤에는 되돌려도 그 사이 만들어진 웹뷰 저장소가 갈린다 → **판을 넘어 고정한다**
- **발행된 GitHub Release** — 지울 수는 있으나 **이미 받은 사람의 설치파일은 회수되지 않는다**
- **PVC·hostPath 를 지운 뒤의 녹음 원본·자료 파일**(`AX_RECORDINGS_DIR`·`AX_MATERIALS_DIR`)과
  **DB 볼륨** — 백업이 없으면 끝이다. 그래서 B 가 rollback 과 갈려 있다

## Done Criteria

- [ ] **Phase 1 ~ 9 가 전부** `DONE` 또는 `SUPERSEDED` 다 (6a·6b 포함)
- [ ] **SPEC-006 의 인수조건 43건이 전부 통과이거나, 통과하지 못한 것이 「검증 불가」 또는 「보류」
      사유와 함께 명시돼 있다.** 「사실상 통과」로 적은 항목이 하나도 없다
- [ ] **실측 15건의 기록이 남았다** — 같은 ID 안에서 **fixture 증거 · 제품판 증거 · 운영판 증거**가
      단계로 갈려 있고, **인용한 것은 인용임이 표시**돼 있다
- [ ] 계약 불변식 **I-1 ~ I-8** 이 코드에서 지켜진 것을 보였다
- [ ] DEC-005 의 D-01 ~ D-09 각각에 받은 자리와 상태가 적혔다
- [ ] **Phase 8 이 검증한 설치파일과 Phase 9 가 발행한 설치파일이 같다** —
      **해시(또는 빌드 식별자)가 일치**한다. **해시를 맞출 대상은 이 둘뿐이다**
- [ ] **6b 의 배포 판과 그 셸 판의 호환 조합**이 Phase 9 의 기록에 함께 적혔다 —
      **운영 origin · `shell_api` · 그때 서버에 떠 있던 이미지 태그·웹 빌드 · 셸 판 번호**.
      **서버 아티팩트와 설치파일은 같은 것이 아니다** — 둘을 잇는 것은 **같은 운영 origin 과 이 조합 기록**이다
- [ ] **데이터 백업과 복구 증거**가 §Rollback B 대로 남았다
- [ ] product `log.md` 와 `30-work/README.md` 가 갱신됐다
- [ ] 릴리즈가 있었다면 `60-release/` 문서와 GitHub Release 가 **서로를 가리킨다**
- [ ] **Windows 축의 상태가 사실대로 적혔다** — 검증본 / 검증 불가 / 보류 중 하나이고,
      범위를 줄였다면 **사용자 승인 기록**이 있다

---

## Open Issues

### 사용자 결정 — **다섯**(+ 조건부 둘)

`OQ-T01`(최소 OS·아키텍처·형식) · `OQ-T02`(운영 도메인) · `OQ-T03`(배포 대상·서명·공증·업데이트) ·
`OQ-W01`(Windows 실기) · `OQ-W06`(Windows 빌드 환경과 범위 축소 승인).
**조건부 둘** — `OQ-W02`(외부 레포 푸시 시점의 org 범위) · `OQ-W05`(권한 완화·새 인증이 **필요해졌을 때만**).

`OQ-W03`(arm64 이미지) · `OQ-W04`(FE 서빙)는 **구현 선택으로 내렸다** — 코디 기본값으로 진행한다.
내용·근거·차단 범위는 §미결 게이트가 갖는다.

### 변경 제안 — SPEC 을 고치지 않고 올리는 것

| # | 무엇 | 지위 |
|---|---|---|
| **P-1** | **운영 프로파일** — `PRODUCTION` 에 라우트가 없고(`http.py:606` 의 조건 밖은 `/health` 하나) `Secure` 쿠키는 그 프로파일에서만 붙는다(`http_auth.py:106-107`) | **둘로 갈랐다.** ⟶ **기존 권한·쿠키 계약을 유지하는 내부 정리는 구현**이다 — 6a 설계 · 6b 구현. SPEC-006 의 계약 표면이 안 바뀌므로 **SPEC 환류가 필요 없다**. ⟶ **권한 완화·새 인증 도입만 별도 decision**(OQ-W05) |
| **P-2** | **운영 arm64 이미지** — `delivery/Dockerfile:63` 이 `codex-linux-x64` 를, `Makefile:25` 가 `linux/amd64` 를 박는다. 노드는 전부 arm64 | **구현으로 내렸다.** 6a 작업 1 이 **보호 요구의 적용 범위**를 확인하고, 그 결과에 따라 기본안이 정해진다. **어느 쪽이든 납품 경로의 보호 수준을 낮추지 않는다** — 낮춰야 할 때만 사용자 결정 |
| **P-3** | **M-2b 측정 수단** — 세션 TTL 이 코드 상수(12h, `auth_sessions.py:12`)라 env 로 짧게 둘 수 없다 | **제품 변경 없이** 개발 DB 의 `expires_at` 을 직접 당겨 잰다. TTL 을 env 로 여는 것은 제품 변경이므로 **제안하지 않는다** |
| **P-4** | **`frontend` 워커 설정** — `verify` 에 Rust 검증 명령이 없다(`cargo check`·`clippy`·tauri 빌드) | `allowed_paths` 는 이미 `frontend/` 라 `src-tauri/` 를 덮는다. **새 워커 유형은 필요 없고** `verify` 문구만 는다. **코디 몫 — 사용자 gate 아님** |
| **P-5** | **인프라 레포 워커 정의** — `config/projects/strong-hajin.json` 에 `infra` 레포(`k8s_infra_mac`)와 `roles/strong-hajin/infra`가 추가됐다 | **해소.** `allowed_paths`는 Strong Hajin 차트·Application·AppProject로 제한되고, helm lint/template 및 실제 GitOps 적용 분리 규칙이 설정됐다. Phase 6b 선행 차단에서 제거한다. |

### index 갱신안 — 이 문서가 고치지 않았다

`allowed_paths` 밖이라 **제안만** 남긴다. 적용은 코디 몫이다.

- `30-work/README.md` **Status Board** 에 행 추가:
  `| 1–9 | WORK-006 데스크톱 래퍼 | SPEC-006 전절 | todo | kknaks | 미산정 | 미정 | 미정 | 없음 | Phase 1 발주 |`
- `30-work/README.md` **Work List** 에 행 추가:
  `| WORK-006 | 데스크톱 래퍼 | new-feature | kknaks | todo | 0% | work-006-tauri-wrapper.md | SPEC-006 |`
- `30-work/README.md` **Spec Coverage** 에 행 추가: `| SPEC-006 | WORK-006 | todo |`
- `30-work/README.md` 의 「최종 수정」을 `2026-09-22` 로
- `log.md` 에 행 추가: `| 2026-09-22 | WORK-006 계획: 실측 15건·인수조건 43건을 10 Phase(1~5·6a·6b·7·8·9)에 배정.
  계측 우선 · Phase 2 판정 게이트 · 운영 설계(6a)와 실행(6b) 분리 · 운영 origin 판을 검증한 뒤 발행(8→9).
  구현·실측·빌드·배포 미착수 | [작업](30-work/work-006-tauri-wrapper.md) |`
- `20-spec/README.md` 의 SPEC-006 행은 **status `draft` 그대로 둔다** — 구현·실측이 남았다

### 아직 답이 없어 이 문서가 비워 둔 것

- **Phase 기간·목표일** — 실측 시간(항목당 `max(3T, 30분)`)이 장비와 설정에 달려 있어 산정하지 않았다
- **절전 방지 구현 수단** — 직접 구현이냐 커뮤니티 크레이트냐. **공식 플러그인이 없다**는 사실만
  확정이고, 선택은 Phase 3 이 한다
- **`AC-T32`·`AC-T38` 을 어느 층이 구현하나** — M-6 의 결과가 정한다
- **운영 프로파일 내부 정리의 «수단»** — 어느 조건으로 라우트를 가를지는 6a 가 설계한다.
  **권한이 넓어지지 않는 것**만이 이 문서가 거는 조건이다

---

## Related

- SPEC: frontmatter `links.specs` 참조
- Decision: frontmatter `links.decisions` 참조
- 조사: `orchestration/work/strong-hajin-projects/tauri-implementation-research.md` ·
  `…/research-task-management-tauri.md` · `…/tauri-audio-comparison-note.md` ·
  `…/tauri-deployment-decisions.md`
- 검수: `…/review-tauri-wp-report.md`(이 계획의 1차 검수 — FAIL 3·WARN 8) ·
  `…/tauri-wp-fix1-report.md`(그 처분) · `…/review-tauri-spec-r3-report.md` ·
  `…/tauri-spec-fix2-report.md` · `…/tauri-spec-finalization.md`
- 규약: `orchestration/runbook.md` §1 고정 규칙 — 작업 단위 · 워크트리 · 브랜치
