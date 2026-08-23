# @mediness-infra — 규칙

## 반드시
- **GitOps 우선**: 클러스터 변경은 `charts/`·`argocd/` 매니페스트 커밋으로. 수동 kubectl 변경은 금지(검증 dry-run 제외) 또는 즉시 매니페스트로 환류.
- **dev/prod 분리**: values-dev/prod, argocd applications 를 환경별로. 신규 앱도 준수.
- **시크릿 커밋 금지**: 토큰·비밀번호·kubeconfig 를 git 에 넣지 않는다. provisioning/secrets 방식 사용. values 에는 참조만.
- **기존 패턴 재사용**: 신규 차트/앱은 `charts/mediness`·`charts/private-pypi`·`argocd/applications/*` 의 구조를 따른다(바퀴 재발명 금지).
- **allowed_paths 준수**: 브리프가 지정한 경로(charts/argocd/provisioning 등) 밖은 건드리지 않는다.

## 금지
- 클러스터/네임스페이스/PV 파괴적 삭제를 확인 없이 수행
- 실행 중인 prod 앱을 검증 없이 변경
- 이미지 태그를 `latest` 로 고정(재현성 훼손) — 명시 태그 사용
- `git push`/PR 을 코디네이터 검증 전에

## 완료 신호
- 작업 끝나면 `worker_done` 을 코디네이터에게 — 수정/생성 매니페스트 목록 + `helm lint`/`template`/`--dry-run` 검증 결과 + (클러스터 있으면) sync 상태.
- 애매하거나 파괴적 결정이 필요하면 임의 진행 말고 escalation.
