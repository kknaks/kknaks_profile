# WORK-001 WP8 결과 보고 — 이미지 빌드 워크플로

## 상태: done

커밋 · push 없음. 실제 Actions 실행은 main 머지 뒤.

## 수행 — 파일·모듈 목록

| 파일 | 무엇 |
|---|---|
| `.github/workflows/back-image.yml` | `back/` → `ghcr.io/kknaksss/interpret-pwa-back:${{ github.sha }}` |
| `.github/workflows/front-image.yml` | `front/` → `ghcr.io/kknaksss/interpret-pwa-front:${{ github.sha }}` · 빌드 인자 `NEXT_PUBLIC_API_BASE_URL=https://tongky.medisolveai.xyz`(워크플로 `env.API_BASE_URL` 에 박음 · 공개 값) |

원형(cc-prototype `origin/main` `procedure-back-image.yml` · `procedure-front-image.yml`)을 그대로 본떴다.
- 트리거: `push` 는 `main` 만 · `paths` = 자기 폴더 + 자기 워크플로 파일 · `workflow_dispatch`(수동)
- 러너 `ubuntu-24.04-arm`(GitHub 호스트 arm64 · 네이티브 빌드). **원형에 QEMU 가 없어** 이쪽도 넣지 않았다(`setup-buildx-action@v3` 만)
- GHCR 로그인 = `docker/login-action@v3` · `GITHUB_TOKEN` · `permissions: contents: read · packages: write`
- `docker/build-push-action@v6` · `platforms: linux/arm64` · 태그는 **sha 하나만**(`latest` · `main` 없음) · gha 캐시(scope 를 back · front 따로)
- `concurrency` 로 같은 ref 의 앞 실행 취소(원형 그대로)
- 원형과 다른 점: front 의 `permissions` 를 job 단위가 아니라 워크플로 맨 위에 둬 back 과 모양을 맞췄다(권한 내용은 같음)

## 검증 — 명령과 수치

| 명령 | 결과 |
|---|---|
| `actionlint .github/workflows/*.yml` | 오류 0 |
| `docker buildx build --platform linux/arm64 -t interpret-pwa-back:wp8-check back` | 성공 · 11초(캐시) · 이미지 arch `arm64` · 57 MB |
| `docker buildx build --platform linux/arm64 --build-arg NEXT_PUBLIC_API_BASE_URL=https://tongky.medisolveai.xyz -t interpret-pwa-front:wp8-check front` | 성공 · 1분 58초 · 이미지 arch `arm64` · 76 MB |

- 푸시 없음 · 확인용 로컬 이미지 2개는 지웠다. Dockerfile 은 고칠 것이 없었다.
- 로컬 맥이 arm64 라 네이티브 빌드다(Actions 러너와 같은 조건).
- front 빌드는 지금 워크트리의 `front/`(frontend 워커가 WP6 작업 중인 상태)로 했다 — 읽기만 했다. 머지 시점의 front 로 다시 빌드되는지는 첫 Actions 실행에서 확인된다.

## 계약 대조 — DEC-001 D-26

| 항목 | 판정 |
|---|---|
| 이미지 이름 `ghcr.io/kknaksss/interpret-pwa-{back,front}:<sha>` | 같음 |
| arm64 · Actions · main 빌드만 | 같음(+ `workflow_dispatch` — 브리프 요청) |
| `latest` 금지 | 같음 |
| front back 주소 `https://tongky.medisolveai.xyz` (한 호스트 · `/api` → back) | 같음 — 브라우저가 `https://tongky.medisolveai.xyz/api/...` · `wss://tongky.medisolveai.xyz/api/interpret` 로 간다 |

## 이슈 · 코디가 확인할 것

1. **GHCR 패키지 공개 여부** — 첫 푸시 때 패키지는 비공개로 생긴다. 클러스터가 받으려면 패키지를 공개로 돌리거나 pull Secret 이 필요하다(원형 procedure 때와 같은 처리).
2. **`workflow_dispatch` 는 main 이 아닌 브랜치에서도 수동으로 돌릴 수 있다**(원형도 같음). 브랜치에서 돌리면 그 커밋 sha 로 이미지가 올라간다 — main 만 엄격히 원하면 job 에 `if: github.ref == 'refs/heads/main'` 한 줄을 더한다.
3. 레포 Settings → Actions → Workflow permissions 가 「Read repository contents」 기본이어도 워크플로 `permissions: packages: write` 로 충분하다. 단, 조직 정책이 막으면 첫 실행에서 403 이 난다.
