# DEC-003 배포 — front 이미지 · GitHub Actions 결과 보고 (frontend)

## 상태: done

`cc/front` 배포 이미지(Dockerfile)와 arm64 → GHCR 워크플로를 만들었다. 커밋 · push 없음. 바꾼 곳은 `cc/front/` 와 `.github/workflows/cc-front-image.yml` 하나뿐이다(같은 폴더의 `cc-back-image.yml` 은 backend 몫 — 손대지 않음).

## 수행 — 파일

| 파일 | 내용 |
|---|---|
| `cc/front/Dockerfile` (신규) | 3단계(deps `npm ci` → build `npm run build` → run). node 20 alpine · Next standalone · **비루트 `node`(uid 1000)** · `PORT=3600` `HOSTNAME=0.0.0.0` · `node server.js`. 빌드 인자 `NEXT_PUBLIC_API_BASE_URL`(기본 `https://ccc.medisolveai.xyz`). 플랫폼은 `--platform linux/arm64`(워크플로 `platforms`)로 정한다 |
| `cc/front/.dockerignore` (신규) | `node_modules` · `.next` · `.env*`(예시 제외) 등 |
| `cc/front/next.config.ts` | `output: 'standalone'` 추가 |
| `cc/front/README.md` | 「배포」 문단 — 이미지 · 빌드 인자 · WS 주소 · CI · 로컬 확인 |
| `.github/workflows/cc-front-image.yml` (신규) | 트리거 = `cc/front/**`(+ 이 파일) 변경 push · `workflow_dispatch`. `ubuntu-24.04-arm`(GitHub 호스트 arm64, 공개 레포 무료) · `GITHUB_TOKEN`(`packages: write`)으로 GHCR 로그인 · `docker/build-push-action@v6` `platforms: linux/arm64` · 빌드 인자 = `https://ccc.medisolveai.xyz` · 태그 **`ghcr.io/kknaksss/cc-prototype-front:${{ github.sha }}` 하나(latest 없음)** · gha 캐시 · 같은 ref 동시 실행은 앞 것 취소 |

## 검증

| 항목 | 결과 |
|---|---|
| `npx tsc --noEmit` | 통과 |
| `npm run lint` | 통과(0/0) |
| `npm run build` | 통과 — `.next/standalone/server.js` 생성 |
| `docker build --platform linux/arm64 --build-arg NEXT_PUBLIC_API_BASE_URL=https://ccc.medisolveai.xyz` | 성공 · 경고 0(처음 넣은 `FROM --platform` 상수 경고 3건은 빼서 해결) · 이미지 arm64 · User `node` · 76 MB |
| 임시 포트 13641 로 실행 | `/` · `/login` · `/desk` · `/staff` · `/staff/patient/x` 모두 **200**. 컨테이너 `id` = `uid=1000(node)`. 확인 뒤 그 컨테이너만 멈추고 이미지도 지웠다(3600 · 8600 무관) |
| API 주소 박힘 | 번들에 `"https://ccc.medisolveai.xyz"` 있음 · `localhost:8600` 없음 |
| 통역 WS 주소 | 번들 코드 `new WebSocket(pY.replace(/^http/,"ws")+"/api/interpret")`, `pY="https://ccc.medisolveai.xyz"` → **`wss://ccc.medisolveai.xyz/api/interpret`**(https→wss 변환 확인) |
| 워크플로 문법 | YAML 파싱 OK(실제 Actions 실행은 push 뒤 — pending) |

## 계약 · 범위

- SSE · 조작 · 통역 모두 `NEXT_PUBLIC_API_BASE_URL` 하나에서 나온다(`lib/api.ts`) — 같은 출처 배포에서 `/api/*` · `/api/events` · `wss …/api/interpret` 로 간다
- 데이터 · 키는 이미지에 없다(front 는 시드 · 직원 데이터를 갖지 않음, D-05)

## 이슈 · 코디가 확인할 것

1. **Actions 실행은 pending** — 커밋 · push 뒤 첫 실행에서 확인. GHCR 패키지가 처음 생기면 기본 비공개일 수 있다 → 클러스터가 받으려면 패키지를 공개로 바꾸거나 imagePullSecret 필요
2. 공개 레포라 `ubuntu-24.04-arm` 을 썼다(mediness 는 사내 self-hosted `medisolve-arm64`). 레포가 비공개로 바뀌면 러너를 바꿔야 한다
3. `NEXT_PUBLIC_API_BASE_URL` 은 빌드 때 박히므로 도메인이 바뀌면 워크플로 `env.API_BASE_URL` 을 고치고 다시 빌드
4. 컨테이너 헬스체크용 별도 경로는 없다 — k8s probe 는 `GET /login`(200)을 쓰면 된다
