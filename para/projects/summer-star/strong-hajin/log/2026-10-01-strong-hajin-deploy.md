# 작업 요약 — strong-hajin-deploy (strong-hajin)

기간: `2026-09-30` ~ `2026-10-01`
결과: 목데이터를 걷어내고 실제 유저 4명으로 Mac Studio 운영(`https://ax.medisolveai.xyz`)에 배포했다. 로그인·AI 대화·STT·회의실을 연결하고, 회사판 데스크톱 앱 `medi-ax` 를 Developer ID 서명·공증해 전달했다. 코드 #5~#8 · infra #5·#6 · 문서 #66 머지.

## 1. 무엇을 했나

배포 전에 예시 회사·데모 계정을 빼고 실제 유저를 넣어야 했는데, PRODUCTION 프로파일에는 로그인 라우트가 아예 없었고 운영 DB 에 유저를 넣는 경로도 없었다. dataset import 경로를 조사해 조직도 9표 양식을 만들고, mediness prod 에서 4명의 조직 정보를 읽기 전용으로 가져와 로컬에 적재한 뒤 그 dump 를 운영에 복원했다. 운영 로그인을 열고(바로가기는 개발만), arm64 이미지·차트·Argo 앱을 세워 수동 sync 로 올렸다. 데스크톱 셸은 개인/회사 두 판으로 갈라 회사판만 운영 origin 으로 굽고 공증했다. 배포 절차는 RUNBOOK-002 로 남겼다.

## 2. 적용한 기술·개념

- **dataset import 로 실제 조직 적재 + pg_dump 로 운영 이관** — 사람·소속·grant·로그인을 한 트랜잭션으로 넣는 유일한 경로를 쓰고, 로컬 전용 가드를 우회하지 않고 dump 로 옮겼다.
  - 왜 이걸 골랐나: import·reset 은 dev 프로파일·localhost `ax_demo` 에서만 돈다. 가드를 풀거나 운영을 dev 로 띄우면 `X-Demo-Persona` 로 아무나 행세할 수 있다. dump 는 코드 변경이 없다.
  - 무엇이 어려웠나: 「유저 정보만」과 「조직도 완벽히」 사이에서 양식 범위가 세 번 바뀌었다. 코드가 읽는 11표 중 프로젝트 둘만 빼고 조직도 9표 전체가 맞았다.
  - 근거: `research-seed-path.md` · `entrypoints/dataset.py:140-148` · `reference/2026-09-30-strong-hain-seed/README.md`
- **라우트 등록과 지름길 노출의 분리** — 이메일/비밀번호 로그인은 모든 프로파일에 등록하고, 데모 계정 목록·데모 비밀번호만 `demo_shortcuts_enabled`(개발) 뒤에 뒀다.
  - 왜 이걸 골랐나: OIDC·프록시 인증은 규모가 크고, 4명 운영에는 로컬 계정이면 충분하다. 개발용 헤더 이음새는 운영에 계속 안 붙는다.
  - 무엇이 어려웠나: 같은 플래그가 「로그인 라우트 존재」와 「데모 목록 노출」을 함께 쥐고 있었다. 하나를 열면 다른 하나가 새는 구조였다.
  - 근거: 코드 #5 `bootstrap/settings.py` · `entrypoints/http.py` · `tests/contract/test_authentication.py`
- **회전식 refresh token 과 전용 인증 홈** — codex 인증을 mediness·로컬 `~/.codex` 와 공유하지 않고 `CODEX_HOME` 을 따로 둬 device-auth 로 한 번 로그인했다.
  - 왜 이걸 골랐나: refresh 때마다 이전 토큰이 무효가 된다. 같은 토큰을 두 곳이 쓰면 한쪽이 갱신하는 순간 다른 쪽(mediness 운영 AX)이 끊긴다.
  - 무엇이 어려웠나: 호스트에 남은 7/2 auth.json 은 이미 회전돼 401. mediness PVC 사본은 최신이지만 쓰면 회사 운영을 깨므로 버렸다.
  - 근거: `report-infra-deploy.md` §B · `infra-04-ai-stt-instructions.md`
- **Tauri 판(flavor) 분리** — 코드 한 벌에 `flavors/<판>/` 오버레이(tauri.conf·shell.config·capabilities)와 `SHELL_FLAVOR` 로 개인 `app.stronghajin.desktop` / 회사 `app.ax.desktop` 을 갈랐다.
  - 왜 이걸 골랐나: identifier 는 저장소 키라 판 안에서 바꾸면 로그아웃된다. 이름만 바꾸면 개인·회사가 같은 앱으로 섞인다.
  - 무엇이 어려웠나: shell.config 가 `include_str!` 로 박혀 빌드 시점에 판이 정해진다. 판이 섞인 빌드를 build.rs 가 막도록 했다.
  - 근거: 코드 #8 · `report-fe-flavors.md`
- **Developer ID 서명·공증·staple** — hardened runtime + notarytool(keychain profile) → staple → `spctl` 로 「Notarized Developer ID」 확인.
  - 근거: `report-fe-release-dmg.md` · `fe-0*-notary.txt`

## 3. 막혔던 것 / 사고

- 코디 핸들이 세션 도중 두 번 stale → 워커 보고가 유실될 뻔 → `terminal list` 에서 세션 제목으로 찾아 브리프·_RESUME 일괄 갱신. writer 핸들도 두 번 바뀌어 `terminal_handle_stale` 로 발견했다.
- infra 워커가 Mac 잠자기로 2시간 15분 만에 사망 → 파드 0·404 로 발견 → 화면 tail 로 진행 지점(AppProject·DNS 까지) 확인 후 재개 지시. 장시간 작업 전 `caffeinate`.
- medi-me SSH 가 Cloudflare 경유라 자주 끊김 → 원격 `nohup` + 로그 읽기, 멱등 명령으로 재시도.
- 사용자 Mac 에서 앱이 시스템 리포트와 함께 종료 → `/Applications/Strong Hajin.app` 이 9/30 로컬 ad-hoc 판(127.0.0.1, 서명 깨짐)이었다 → 공증판으로 교체 안내.
- 코디가 「Developer ID 인증서 만료 2026-11-28」 로 잘못 전달 → writer 가 키체인 실측으로 정정(Developer ID 2031-05-26, 11-28 은 Cloudflare 엣지 TLS).
- writer 가 사용자 직접 지시로 역할 밖 코드(FE·BE)를 고쳤다 → 코디가 사후에 diff·테스트로 검증 후 PR. 문서→코드 직렬 파이프라인을 거치지 않았다.
- 시드 양식 범위를 사용자 의도(조직도 완전)보다 좁게 잡아 세 번 되돌렸다 — 「최소」가 아니라 「제품이 받는 전부」가 기준이었다.

## 4. 결정

| 날짜 | 결정 | 왜 |
|---|---|---|
| 2026-09-30 | 시드 = 조직도 9표(조직·직급·직위·직무·사람·보직·추가소속·직무배정·로그인), 프로젝트·업무는 앱에서 | 사용자 지시 |
| 2026-09-30 | 실제 투입 = AX 팀 1·4명, 비밀번호는 적재 시 env | 사용자 ↔ writer |
| 2026-09-30 | 운영 로그인 = 이메일/비밀번호(프로파일 무관), 바로가기 개발만 | 사용자 「고쳐」 · 코드 #5 |
| 2026-09-30 | host `ax.medisolveai.xyz` · registry `ghcr.io/kknaksss` · 운영 데이터 = 로컬 시드 dump · AI 노드 마운트 | 사용자 결정 · DEC-007 |
| 2026-09-30 | ~~registry `ghcr.io/kknaks`~~ → `kknaksss` (2026-09-30, gh 로그인 계정 확인) | 코디 확인 |
| 2026-10-01 | codex 인증 = 전용 CODEX_HOME 로그인, mediness PVC 복사 금지 | refresh token 회전 |
| 2026-10-01 | 앱 두 판: 개인 Strong Hajin/app.stronghajin.desktop · 회사 medi-ax/app.ax.desktop | 사용자 지시 · 코드 #8 |
| 2026-10-01 | 실명 시드 CSV 는 Git 밖(공개 레포), 작업 리포트는 실명 가림 | 레포 PUBLIC |

## 5. 날짜별 로그

- `2026-09-30` 시드 경로 조사·조직도 양식 · mediness prod 4명 조회 · 로컬 적재 · 운영 로그인·MCP 가드·arm64 Dockerfile · 코드 #5·infra #5 머지 · 이미지 push·태그 #6
- `2026-10-01` 클러스터 준비·시드 복원·sync(파드 8/8) · STT·회의실·codex 연결 · 아이콘 #6 · origin #7 · 두 판 #8 · medi-ax dmg 공증 · 배포 문서 #66

## 6. 산출물

- code PR: kknaks/Strong_hajin #5(cdb0f3f) · #6(b0eb4b4) · #7(e575194) · #8(015bed2)
- infra PR: MediSolveAIDev/k8s_infra_mac #5(f04d4cb) · #6(7ba1050)
- docs PR: kknaks/kknaks_profile #66(583a03f) — RUNBOOK-002 · DEC-007 · environments · config
- 리포트: `research-seed-path.md` · `research-mediness-org.md`(실명 가림) · `report-infra-deploy.md` · `report-fe-icon.md` · `report-fe-release-dmg.md` · `report-fe-flavors.md`
- 앱: `medi-ax_0.0.1_arm64.dmg` (Developer ID + 공증)

## 7. 잔여

- M-5 — 설치본 재시작 후 로그인 유지: 사용자 검수
- 로그인 시도 횟수 제한 없음(인터넷 노출)
- 개인판 origin 미정 · GitHub Release 미발행 · Windows 빌드 없음
- 노드 codex 0.146(개발 0.158) — provenance 일부 필드 None
- 운영 이미지는 cdb0f3f(웹). #6~#8 은 데스크톱 셸만이라 재배포 불필요
- **공개 레포 노출 점검**: `reference/2026-09-04-SC-org_data/` 의 회사 조직도 CSV(169행, 인사 정보)가 PUBLIC 레포에 추적 중 — 사용자 판단 필요
