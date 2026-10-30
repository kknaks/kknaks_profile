---
sot: here
status: active
updated: 2026-10-28
---

# 배포 · TestFlight 업로드 — procedure(ccc)

**순서는 늘 같다: ① 코드 main 머지 → ② 운영 배포(infra 태그 + ArgoCD sync) → ③ 운영 확인 → ④ 앱 빌드(운영 주소) · TestFlight 업로드.**
앱은 운영 서버 `https://ccc.medisolveai.xyz` 에만 붙는다. 맥 로컬 · 같은 Wi-Fi 로 붙이지 않는다. 운영에 안 올라간 코드로 앱을 올리지 않는다.

값(키 · 토큰 · Issuer · 팀 ID)은 여기 쓰지 않는다 — 경로만(public 레포).

## 경로

| 무엇 | 경로 |
|---|---|
| 코드 레포 | `https://github.com/kknaksss/cc-prototype` · 원본 체크아웃 `/Users/kknaks/git/toy_pr2/cc-prototype`(pull · checkout 금지 — fetch 만) |
| 코드 워크트리 | `/Users/kknaks/orca/workspaces/cc-prototype/<slug>` |
| 기능 폴더 | `procedure/back`(FastAPI) · `procedure/front`(Next.js) · `procedure/app`(Flutter iOS) · `procedure/compose.yml` · `procedure/.env`(gitignore) |
| infra 레포 | `https://github.com/MediSolveAIDev/k8s_infra_mac` · 원본 `/Users/kknaks/git/harness_works/k8s_infra_mac` · 워크트리 `/Users/kknaks/orca/workspaces/k8s_infra_mac/<slug>` |
| 차트 · 이미지 태그 | infra 레포 `charts/cc-prototype/values-prod.yaml` 의 `image.tag`(40자 sha) |
| 배포 런북(Secret · DNS 정본) | infra 레포 `docs/cc-prototype-deploy.md` |
| 클러스터 | `ssh medi-me` · kubectl = `/opt/homebrew/bin/kubectl` · ArgoCD 앱 `cc-prototype-prod`(수동 sync) · 네임스페이스 `cc-prototype-prod` |
| 운영 주소 | `https://ccc.medisolveai.xyz` |
| App Store Connect API 키 | `~/.appstoreconnect/private_keys/AuthKey_<키ID>.p8`(키 ID = 파일 이름) |
| App Store Connect Issuer ID | `~/.appstoreconnect/issuer_id`(한 줄 · chmod 600) |
| iOS 서명 설정 | 원본 체크아웃 `procedure/app/ios/Flutter/Signing.xcconfig`(gitignore) — 워크트리로 복사 |
| flutter | `/Users/kknaks/fvm/versions/3.44.8/bin/flutter`(= `fvm flutter`) |

## ① 코드 main 머지

```bash
cd <코드 워크트리>
git push -u origin <branch>
gh pr create --repo kknaksss/cc-prototype --base main --head <branch> --title "..." --body "..."
gh pr merge <PR> --repo kknaksss/cc-prototype --merge      # 사용자가 정한 방식(스쿼시 / 일반)
gh run list --repo kknaksss/cc-prototype --limit 2         # procedure-back image · procedure-front image = success
```

- main push 때만 Actions 가 `ghcr.io/kknaksss/procedure-{back,front}:<40자 sha>` 를 만든다(arm64)

## ② 운영 배포

```bash
cd <infra 워크트리>                    # origin/main 에서 새 브랜치
SHA=$(gh api repos/kknaksss/cc-prototype/commits/<머지 커밋> -q .sha)
# charts/cc-prototype/values-prod.yaml  →  image.tag: "<SHA>"
git commit -am "deploy(cc-prototype): procedure 이미지 <짧은 sha> — <한 줄>"
git push -u origin <infra 브랜치>
gh pr create --repo MediSolveAIDev/k8s_infra_mac --base main --head <infra 브랜치> --title "..." --body "..."
gh pr merge <PR> --repo MediSolveAIDev/k8s_infra_mac --squash

# ArgoCD 수동 sync
ssh medi-me '/opt/homebrew/bin/kubectl -n argocd patch application cc-prototype-prod --type merge \
  -p "{\"operation\":{\"initiatedBy\":{\"username\":\"coord\"},\"sync\":{\"revision\":\"HEAD\"}}}"'
```

- 새 env 가 생기면 sync **전에** 클러스터 Secret `cc-prototype-secret` 을 고친다(infra 런북 「Secrets」) — 값은 레포 밖
- back 은 `Recreate` — sync 때 한 번 내려갔다 뜬다. DB · 사진은 PVC(`procedure-db` · `procedure-photos`)라 남는다

- **바뀐 쪽 이미지만 빌드된다**(Actions 는 경로 필터) — back 만 바뀌면 front 이미지가 그 sha 로 없다 → `image.tag` 대신 `back.imageTag` 만 올린다(front 는 그대로). `gh run list` 로 어느 이미지가 빌드됐는지 먼저 본다

## ③ 운영 확인

```bash
ssh medi-me '/opt/homebrew/bin/kubectl -n argocd get application cc-prototype-prod \
  -o jsonpath="{.status.sync.status} {.status.health.status}"'              # Synced Healthy
ssh medi-me '/opt/homebrew/bin/kubectl -n cc-prototype-prod get pods,pvc'   # back · front Running · PVC Bound
ssh medi-me '/opt/homebrew/bin/kubectl -n cc-prototype-prod logs deploy/back --tail=20'  # APNs JWT OK · KOS 직원 · 방
curl -s https://ccc.medisolveai.xyz/api/health                              # {"ok":true,...}
```

- 웹에서 로그인 · 예약 현황 · 시술 현황을 눈으로 본다
- 스크립트로 API 를 부를 땐 `User-Agent` 를 브라우저 값으로 — Cloudflare 가 기본 python UA 를 403 으로 막는다(서버 문제 아님)

## ④ 앱 빌드 · TestFlight 업로드

**release 빌드에는 로그인 화면 「서버 주소」 칸이 없다**(debug 만). `API_BASE` 가 곧 앱이 붙는 서버다 — **반드시 운영 주소**.

```bash
cd <코드 워크트리>/procedure/app
cp /Users/kknaks/git/toy_pr2/cc-prototype/procedure/app/ios/Flutter/Signing.xcconfig ios/Flutter/Signing.xcconfig

fvm flutter build ipa --release \
  --dart-define=API_BASE=https://ccc.medisolveai.xyz \
  --build-number=<앞 빌드 + 1>                     # 같은 번호는 거절

KID=$(basename ~/.appstoreconnect/private_keys/AuthKey_*.p8 .p8 | sed 's/AuthKey_//')
xcrun altool --upload-app --type ios -f build/ios/ipa/*.ipa \
  --apiKey "$KID" --apiIssuer "$(cat ~/.appstoreconnect/issuer_id)"     # UPLOAD SUCCEEDED
```

- App Store Connect 처리 5 ~ 30분 → 내부 그룹(「tester」)은 **자동 배포**라 따로 배정할 것 없음 — 빌드 상태가 `VALID` → `IN_BETA_TESTING` 이 되면 기기 TestFlight 앱에서 업데이트(`READY_FOR_BETA_TESTING` 이면 아직 그룹에 안 붙음 — 몇 분 기다림)
- 상태 조회: App Store Connect API `GET /v1/builds?filter[app]=<앱 id>&sort=-uploadedDate&include=buildBetaDetail` → `processingState` · `internalBuildState`(같은 API 키 · ES256 JWT — `procedure/back` 의 `uv run python` 에 PyJWT 있음)
- 푸시: 운영 차트가 `APNS_ENV=production` — TestFlight 기기에 그대로 간다
- 업로드 전 점검(아이콘 알파 · Info.plist 문구 · 수출 규정 · 서명 · 푸시)은 `procedure/app/README.md` 「서명 · TestFlight」 표
- 시뮬레이터(debug)만 `API_BASE=http://localhost:8700`(로컬 compose) — TestFlight 와 섞지 않는다

## 기록

| 날짜 | 무엇 | 빌드 · 커밋 |
|---|---|---|
| 2026-10-21 | 웹 첫 배포(procedure) · TestFlight 빌드 1 | infra #23 |
| 2026-10-27 | 웹 배포(전체현황판 예약 현황) | 코드 #6 · infra #31 |
| 2026-10-28 | TestFlight 빌드 4 — **잘못**: `API_BASE` 를 맥 로컬 IP 로 · 운영 배포 전에 올림 → 「서버에 연결할 수 없어요」 | 코드 #7 `f8a3751` |
| 2026-10-28 | 운영 배포(앱 v2 · 사진 PVC) · ArgoCD sync | infra #37 `1b325c5` |
| 2026-10-28 | TestFlight **빌드 5** — `API_BASE=https://ccc.medisolveai.xyz` | 코드 `f8a3751` |
| 2026-10-28 | 앱 실기기 E2E batch 1 — 코드 #8 머지 · 운영 배포 · TestFlight **빌드 6**(운영 주소) | 코드 `333f30f` · infra #38 `181febb` |
| 2026-10-28 | 앱 실기기 E2E batch 2 — 코드 #9 머지 · back 만 배포(`back.imageTag`) · TestFlight **빌드 7** | 코드 `affac41` · infra #39 `5fc1c56` |
| 2026-10-28 | 여권 사진 KOS `scheduleId`(일정 「사진 · 펜차트」에 보이게) — back 만 | 코드 #10 `fad8b56` · infra `eb9276e` |
| 2026-10-28 | 여권 사진 KOS 분류 「여권」(있는 지점만) — back 만 | 코드 #11 `96441df` · infra `1284c5c` |
| 2026-10-28 | 고객 문진 웹 /q(back · front) · `back.imageTag` 덮어쓰기 뺌 · TestFlight **빌드 8** | 코드 #12 `00853e1` · infra `6dacdb6` |
| 2026-10-28 | 앱만 — 시작 · 복귀 때 기기 등록 · SSE 다시 붙임(업데이트 뒤 띄우기 안 열림) · TestFlight **빌드 9**(서버 배포 없음) | 코드 #13 `113c5e1` |
| 2026-10-28 | 웹 예약 상세 자동 저장 · 유입 채널 · 여권 사진 삭제 · 앱 헤더 한 줄 · QR 읽기 뺌 — back · front · TestFlight **빌드 10** | 코드 #14 `4d48421` · infra `6fb7b36` |
| 2026-10-28 | 앱만 — 화면 다듬기(헤더 · 상세 · 날짜 줄 · 칩 · 입력 · 예약 상세 자동 저장) · TestFlight **빌드 11** | 코드 #15 `9c69b0f` |
| 2026-10-29 | 직원 앱 내부 채팅(1:1 · 그룹 · 사진 · 동영상 · 수정 · 푸시) — back 만 배포(`back.imageTag`) · ingress 업로드 한도 100m · TestFlight **빌드 12**(운영 주소) | 코드 #17 `a6c4123` · infra #44 `d9041ed` |
| 2026-10-29 | 채팅 [공유] = 앱 안 전달 · 시스템 공유 걷어냄 · 파일 마지막 참조 삭제 · 통역 드로어 높이 결함 · 바텀 시트 10곳 — back 만 · TestFlight **빌드 13** | 코드 #18 `b988f21` · infra #45 `f67ac5d` |
| 2026-10-29 | 채팅 모아보기 · 초대(1:1 → 새 그룹) · 들어온 뒤 대화만(DB 열 추가 · 배포 전 운영 DB 사본 `/data/procedure.db.bak-20261029-invite`) · 시트 정렬 — back 만 · TestFlight **빌드 14** | 코드 #19 `bf30db4` · infra #46 `15a1b39` |
