# @interpret-pwa-infra — 규칙

## 반드시
- **GitOps 우선**: 클러스터 변경은 `charts/interpret-pwa/` · `argocd/applications/interpret-pwa*.yaml` 커밋으로. 수동 kubectl 금지(`--dry-run` 검증만 허용)
- **시크릿 커밋 금지**: Soniox 키 · 토큰 · 비밀번호 · kubeconfig 를 git 에 넣지 않는다. `provisioning/secrets/interpret-pwa*.env.example`(값 없음) + values 에는 secretRef 만
- **기존 패턴 재사용**: `charts/cc-prototype` 구조를 따른다
- **이미지 태그 명시**(`latest` 금지) · arm64
- **WebSocket 통과**: ingress-nginx 의 Upgrade · 타임아웃 설정을 cc-prototype 선례대로 챙긴다(경로는 SPEC)
- **allowed_paths 준수**: 다른 앱 차트 · 앱 · 클러스터 기반 컴포넌트 수정 금지(브리프가 명시한 것만)

## 금지
- 네임스페이스 · PV 파괴적 삭제를 확인 없이
- 다른 앱(prod 포함) 변경
- `git push` · 커밋 · PR — 코디네이터 몫

## 완료 신호
- `worker_done` — 수정/생성 파일 목록 + `helm lint` · `helm template` · `kubectl --dry-run=client` 결과 + (클러스터 접근이 있으면) 읽기 전용 상태 확인
- 애매하거나 파괴적 결정이 필요하면 임의로 진행하지 말고 `[질문]`
