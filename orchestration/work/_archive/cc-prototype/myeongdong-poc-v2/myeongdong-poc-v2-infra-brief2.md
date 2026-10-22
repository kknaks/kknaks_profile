# [infra] WP10 — ccc.medisolveai.xyz 를 procedure 로 교체(차트 · Secret · ingress)

너는 cc-prototype `infra` 워커다. 역할(절대경로): `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/orchestration/roles/cc-prototype/infra/role.md` (+ 같은 폴더)
작업 워크트리: `/Users/kknaks/orca/workspaces/k8s_infra_mac/myeongdong-poc-v2`(MediSolveAIDev/k8s_infra_mac). **배포 먼저**(사용자 · 데모라 접근 제한은 나중).

## SSOT
- `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/para/projects/summer-star/cc-prototype/30-work/work-004-procedure-app.md` WP10 · `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/para/projects/summer-star/cc-prototype/20-spec/spec-004-procedure-app.md` §2(env 이름 · 포트) · `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/para/projects/summer-star/cc-prototype/20-spec/spec-003-procedure-board.md` §2 · 코드 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/myeongdong-poc-v2/procedure`(read-only — Dockerfile · .env.example · compose 가 env 이름 정본)
- 기존 차트: `charts/cc-prototype` · `argocd/applications/cc-prototype-prod.yaml` · `provisioning/secrets/cc-prototype-prod.env.example` · `docs/cc-prototype-deploy.md`(1 · 2차 배포 방식 · 함정: local-path PVC 는 lima-worker-1 nodeSelector)

## 할 일
1. 차트를 procedure 로: 이미지 `ghcr.io/kknaksss/procedure-back` · `procedure-front`(태그는 코디가 main 빌드 뒤 values-prod 에 넣는다 — 자리만) · back env(.env.example 의 이름 전부 — 값은 Secret) · **APNs 키 파일 = Secret 을 파일로 /run/secrets/apns.p8 마운트(ro)** · APNS_ENV=production · SQLite PVC(/data) · nodeSelector
2. **같은 도메인**: `ccc.medisolveai.xyz/` → front, `/api` → back(통역 **wss** `/api/interpret` 포함). ingress · cloudflared 에서 **SSE `/api/board/stream` 버퍼링 끄기 · 유휴 시간 길게(10분 이상)** · WebSocket 업그레이드
3. Secret: `provisioning/secrets/cc-prototype-prod.env.example` 를 새 env 이름으로(값 0) — 실제 Secret 생성은 코디가 클러스터에서
4. docs 의 cc-prototype 문단 갱신(새 이미지 · Secret 목록 · 재배포 · 재시드 없음)
- allowed_paths: `charts/cc-prototype/` · `argocd/applications/cc-prototype*.yaml` · `provisioning/secrets/cc-prototype*.env.example` · `docs/` 의 cc-prototype 문단
- 검증: helm lint · helm template -f values-prod.yaml · kubectl apply --dry-run=client 각 1회 · 다른 앱 무수정 · 시크릿 값 0 · 클러스터 실제 적용 · sync 는 하지 마라(코디) · 커밋 금지

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "infra 완료: procedure 배포 차트" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de \
  --text "[worker_done] infra 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --text "[질문] infra: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
