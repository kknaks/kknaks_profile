
# 재개 노트 — strong-hajin-deploy (strong-hajin)

**지금**: (10-01) 배포 문서 #66. 아카이브 전 실명 파일 처리 결정 대기 | 전 기능 연결(로그인·AI·STT·회의실) + 서명 dmg 전달 → 사용자 검수(M-5 쿠키 유지 포함). 남은 정리: docs PR·아카이브. | 운영 가동 — https://ax.medisolveai.xyz 200 · 파드 8/8 · 시드 4명. 남음: AX 전용 codex login·dmg(아이콘 진행 중). 이전 기록 → 로컬 데모 가동 — 시드 4명 적재·로그인 200, local-stack(COMPOSE_PROJECT_NAME=strong-hajin-work) 기동, dmg `~/Downloads/Strong Hajin_0.0.1_aarch64_local.dmg`(origin 127.0.0.1:5176 → 이 Mac 에서만 동작). 코드 워크트리 미커밋 FE 6파일(관계탐색 disabled·로그인 테두리·MEDISOLVE·로그아웃 정렬)
**다음**: OQ-5(운영 로그인)·OQ-6(운영 적재 A dump / B 부트스트랩 명령) 결정 → decision 문서 → spec → backend

세팅: `scripts/new-work.sh strong-hajin strong-hajin-deploy` · 설정 SSOT `config/projects/strong-hajin.json`
코디handle: `term_8d586fcb-a104-4f31-9f5f-fd3b659a1d24`

## 워크트리

- `code`: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-deploy` (branch `kknaksss/strong-hajin-deploy`, base `origin/main` → PR `main`)
- `infra`: `/Users/kknaks/orca/workspaces/k8s_infra_mac/strong-hajin-deploy-infra` (branch `kknaksss/strong-hajin-deploy-infra`, base `origin/main` → PR `main`)

## 1. 지금

열린 것만 둔다. 닫히면 지우고 §5 이력으로 내린다.

- [x] 시드 양식 채움 완료 (writer, research-mediness-org.md 근거)
- [x] 운영 가동·로그인 확인 (ax.medisolveai.xyz)
- [x] ~~Developer ID 인증서 만료 2026-11-28~~ 정정: Developer ID 는 2031-05-26 까지. 2026-11-28 은 ax.medisolveai.xyz TLS(Cloudflare 엣지, Google Trust WE1 — 자동 갱신) · dmg 는 Finder 꾸밈 없음(헤드리스)
- [x] 회사판 `~/Downloads/medi-ax_0.0.1_arm64.dmg`(app.ax.desktop, 코디 spctl·stapler·codesign·Info.plist 확인) — 사용자 검수 대기
- [x] ~~운영 dmg `~/Downloads/StrongHajin_0.0.1_arm64.dmg` 서명·공증(코디 spctl·stapler 확인, sha256 3d90bbf0…) · origin PR #7 머지 · [ ] M-5(설치 후 쿠키 유지) 사용자 검수
- [x] AI·STT·회의실 연결 (infra-04): A·B 완료 — Soniox 200 · 회의실 7 · codex AX 턴 PONG 5.1s(노드 0.146)
- [x] ~~Mac Studio k8s 배포 준비(백·프론트, 사용자에겐 dmg 만) — 사용자↔writer 결정 중: D-1 host · D-2 registry · D-4 로그인 · 운영 적재 방식 · AI provider 인증
- [!] canonical k8s_infra_mac 에 strong-hajin 차트·argocd 3·datastores values 가 **untracked**(사용자 체크아웃, 출처 추정 p6b). infra 워크트리는 비어 있음 → 옮길지 사용자 확인. canonical 은 건드리지 않는다
- [x] arm64 Dockerfile(deploy/k8s/) · MCP 운영 가드(AX_MCP_CAUSATION_ID) · production 스모크 — writer, 미커밋
- [x] infra 워크트리: canonical untracked 복사 + values-prod · cloudflared hosts 1줄. 코디 helm lint OK
- [x] registry = ghcr.io/kknaksss (gh 계정 kknaksss 확인)
- [!] infra push = 회사 org(MediSolveAIDev) + 공유 cloudflared 차트 1줄 — config 상 공유 리소스 변경 금지 조항, 사용자 명시 승인 필요
- [ ] 배포 남은 순서: ①사용자 ghcr write 권한(gh auth refresh -s write:packages + docker login) ②main cdb0f3f 로 arm64 이미지 push·infra 태그 커밋 ③클러스터 준비(ns·ghcr-pull·strong-hajin-secret·pg 비번·hostPath) ④Cloudflare DNS ax ⑤datastores sync→시드 dump 복원→app sync ⑥https 로그인 스모크 ⑦origin https://ax.medisolveai.xyz 로 dmg 빌드·Developer ID 서명·공증(인증서·AC_NOTARY 확인됨)
- [x] ~~커밋/PR: code(BE 로그인·MCP·deploy/ + FE 6) · infra · docs(결정/스펙 기록) — 사용자 승인 대기. canonical k8s_infra_mac untracked 는 머지 후 사용자가 정리~~ → code·infra 머지. canonical untracked 는 사용자 정리 대기
- [!] 팀원 기기용 dmg 는 아직 없음 — origin 이 loopback. 터널(https) 또는 운영 배포 주소로 재빌드 필요
- [ ] 코드 워크트리 미커밋: App.tsx 관계 탐색 탭 disabled(데모) · screens-a.css `.login-local input` 규칙 삭제(이중 테두리). writer 가 사용자 직접 지시로 수정(역할 밖). 커밋·PR 여부 사용자 확인. FE 테스트 1092 중 3 실패(단독 통과 주장 — 코디 미재현)
- [!] 결정 대기: 운영 로그인(리포트 §5 1~4) · 운영 DB 적재(§2.6 A~C) · 관리자 · 조직 루트 이름 · 양식 Git 보관(OQ-7 — 폴더 현재 gitignore 아님)
- [ ] 이후 decision → spec → work → backend/frontend → infra (직렬). code 워커 터미널은 그때 띄운다
- [x] 운영 로그인 열림(미커밋 BE: settings·http·테스트 3) — 코디 재실행 auth·route·architecture 38 pass
- [!] ~~(확인됨 http.py:643) 로그인: PRODUCTION 프로파일은 local_login·developer_auth 둘 다 꺼짐, oidc=False → **운영에서 로그인할 길이 없다** (environments.md「아직 배포할 수 없는 이유」2번). 실제 유저를 넣어도 이게 안 정해지면 못 들어온다~~ → 해소
- [!] 사용자에게 물을 것: 실제 유저 누구·몇 명 / 로그인 방식 / 목데이터 「지우기」 범위 / 운영 호스트명

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-09-30 | 배포 전 목데이터 제거 + 실제 유저 투입을 이번 작업 범위로 | 사용자 지시 |
| 2026-10-01 | 앱 두 판: 개인 `Strong Hajin`/`app.stronghajin.desktop`(origin 미정) · 회사 `medi-ax`/`app.ax.desktop`/`https://ax.medisolveai.xyz`. 지금 배포는 회사판 | 사용자 지시 |
| 2026-09-30 | 배포 결정: host `ax.medisolveai.xyz` · registry `ghcr.io/kknaks`(토큰 사용자 대기) · 운영 데이터 = 로컬 시드 DB dump · AI = 노드 `/opt/codex`·`/opt/claude` 마운트(mediness 방식) · dmg 서명 Developer ID + AC_NOTARY · 운영 로그인 = 이메일/비밀번호(프로파일 무관), 바로가기는 개발만 | 사용자↔writer 직접 |
| 2026-09-30 | 시드 채움: 조직 AX(team) 1개 · 4명 key 1~4(구성원A·구성원B·구성원C·구성원D) · 구성원C executive(CTO) · 구성원D team-lead(리더) · 구성원A·구성원B member · 입사일 mediness · 직급·직무 없음. 비밀번호는 적재 때 사용자에게 받아 env 로 | 사용자↔writer 직접 결정, 코디 validate problems 0 |
| 2026-09-30 | 시드는 조직도 전체 9표(조직·직급·직위·직무·사람·보직·추가소속·직무배정·로그인). 프로젝트·업무는 유저가 앱에서 만든다 — 양식 폴더에서 빈 projects 2표·manifest 제거, 적재 때 코디가 덧붙임(validation missing_file 때문) | 사용자 지시 |
| 2026-09-30 | 사용자는 유저 정보만 준다 — 양식은 코디가 만들어 `reference/2026-09-30-strong-hain-seed/` 에 둔다 | 사용자 지시 |

뒤집힌 결정은 지우지 않는다. ~~취소선~~ 을 긋고 같은 행에 뒤집은 날짜와 사유를 남긴다 —
지우면 왜 그렇게 갔는지가 사라져서 같은 논의를 다시 한다.

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| writer | `term_cf521fc4-003a-408b-82be-d586abf9597f` | `task_b12450b8e256` | `ctx_9d693170f05a` | `strong-hajin-deploy-write-brief.md` + 02·03·04 지시 | 완료 — 배포 문서 |
| frontend | `term_0b24189f-a312-4c9e-9aa5-f50bb1d20908` | `task_caf7deed5841` | `ctx_1dcfe15df5b9` | `strong-hajin-deploy-fe-brief.md` + fe-02 | 진행 — 운영 origin dmg 빌드·서명·공증 |
| infra | `term_8246ef20-5da7-4ec6-b39f-e867feb3ee64` | `task_6c94c10eb391` | `ctx_4753ad0883ad` | `strong-hajin-deploy-infra-brief.md` + infra-04 | 완료 |

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.** 워커 보고는 dispatch preamble 의 값을 따르므로
여기 옛 핸들을 남겨 두면 어느 것이 산 것인지 판단이 안 된다.

## 4. 산출물

- code PR: https://github.com/kknaks/Strong_hajin/pull/5 (MERGED cdb0f3f) · #6 아이콘 (MERGED b0eb4b4) · #7 운영 origin (MERGED e575194) · #8 두 판 flavors (MERGED 015bed2)
- infra PR #6 태그 (MERGED 7ba1050)
- infra PR: https://github.com/MediSolveAIDev/k8s_infra_mac/pull/5 (MERGED f04d4cb, image.tag 비움·Argo 수동 sync)
- docs PR: https://github.com/kknaks/kknaks_profile/pull/66 (RUNBOOK-002·DEC-007·environments·config)
- 리포트: `research-seed-path.md` · 양식 `reference/2026-09-30-strong-hain-seed/`
- 커밋: `<sha>` — <한 줄>

## 5. 이력 (최신이 위)

- `2026-10-01` writer 4차 완료 → docs #66. 남은 마감: 실명 파일 처리(시드 CSV·research-mediness-org) 사용자 결정 → archive-work.sh → 워커 정리
- `2026-10-01` writer 4차 — 배포 문서 정리 발주(사용자: 이번 목적은 배포, 고도화는 다음 세션)
- `2026-10-01` 두 판 #8 머지 · medi-ax dmg 서명·공증
- `2026-10-01` 앱 두 판 결정 → fe-04(fe-03 대체). 사용자 /Applications 의 Strong Hajin.app 은 9/30 로컬 ad-hoc 판(서명 깨짐) — 터짐 원인 후보
- `2026-10-01` infra 2차 완료: AX 턴 성공·STT·회의실. 로컬 codex-home/auth.json 은 PVC 와 같은 refresh token — 로컬 사용 금지
- `2026-10-01` 운영 dmg 서명·공증 · origin #7 머지 · STT·회의실 연결 · codex 전용 로그인(사용자)
- `2026-10-01` 아이콘 #6 머지 → frontend 2차(운영 dmg) 발주
- `2026-10-01` 사용자 웹 로그인 확인(운영) — 로그인 실측 닫힘
- `2026-10-01` infra 완료: 운영 가동(코디 재확인: / 200 · providers local:true demo 없음 · 틀린 로그인 401 · 파드 8/8). AX 실패 — 호스트 codex refresh token 만료 → 전용 codex login 필요 · SONIOX·TDL 미설정(STT·회의실 비활성)
- `2026-10-01` frontend 발주 — 앱 아이콘 교체(원본 mediness-rust/src-tauri/icons-prod/icon.png, 사용자 지시 「크기 좀만 줄여서」)
- `2026-10-01` F6 = (a) medi-me 호스트 ~/.codex/auth.json(7/2). (b) mediness PVC 복사 금지 — refresh token 회전으로 mediness AX 끊길 위험. 실패 시 전용 codex login 사용자 결정
- `2026-10-01` infra 워커 잠자기로 사망(AppProject·DNS route 까지 완료, ns 리소스 0) → 재개 지시 infra-03 · F6 = Mac Studio codex auth 복사(사용자)
- `2026-09-30` infra 단계2 완료 → 태그 PR #6 머지(7ba1050) · F1 AppProject apply·F2 DNS route 승인(사용자 배포 위임 범위)
- `2026-09-30` writer 인계: 시드 dump → `~/strong-hajin-deploy-data/strong-hajin-seed.dump`(git 밖·600) · 노드 codex 0.146 vs 0.158 · ax NXDOMAIN → infra-01-handoff-notes.md
- `2026-09-30` 코디 핸들 stale → term_8d586fcb 로 전 파일 갱신 · infra 발주(배포 2~6) · 사용자 ghcr 로그인 완료
- `2026-09-30` code #5 · infra #5 머지 (코디 검증: FE 1092 pass·tsc 0·BE unit 389·auth 38·helm lint)
- `2026-09-30` writer(사용자 지시 '고쳐'): 운영 로그인 개방 BE 수정 · 배포 결정 5건
- `2026-09-30` writer(사용자 직접): k8s 배포 준비 조사 — 수정 없음
- `2026-09-30` writer 3차: 화면 SCAX→MEDISOLVE(title·meta·사이드 로고·로그인 2곳·테스트 1) · 로그아웃 가운데 정렬. 코디 diff 확인. 로그인 칩 SC→M(사용자 지시)
- `2026-09-30` writer(사용자 직접 지시): reset-catalog → 시드 적재 → 4명 로그인 200 → local-stack → loopback dmg 빌드 · FE 2건 수정
- `2026-09-30` writer 2차 — mediness prod 4명(구성원A·구성원C·구성원B·구성원D) 조직 정보 조회 가능성 (read-only, `writer-02-mediness-org-instructions.md`)
- `2026-09-30` writer 완료 — 경로는 dataset import, 운영 적재·운영 로그인 둘 다 코드에 없음
- `2026-09-30` writer 발주 — 시드 조사·양식
- `2026-09-30` new-work.sh (writer·backend·frontend·infra) · writer 터미널 생성

이 절은 **재개에 필요한 만큼만** 쓴다. 회고·배운 것은 `SUMMARY.md` 몫이다.
