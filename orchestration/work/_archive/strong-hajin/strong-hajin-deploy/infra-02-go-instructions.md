# [infra] 단계 2 답 — 진행 (2026-09-30)

- 태그 머지됨: infra #6 `7ba1050` (image.tag cdb0f3f-arm64). 워크트리는 이미 그 브랜치 — 더 고칠 것 없음
- F1 승인: `kubectl apply -f argocd/projects/strong-hajin.yaml` (argocd ns, 이 파일 하나만). whitelist 는 다른 프로젝트와 같은 모양이라 그대로 둔다
- F2 승인: medi-me 에서 `cloudflared tunnel route dns <mediness 와 같은 터널 id> ax.medisolveai.xyz` 한 번. 다른 레코드 건드리지 마라. 이후 dig/curl 로 해석 확인
- 이어서 단계 3~5 진행(시크릿·hostPath·datastores sync·시드 복원·app sync) → 단계 6 중 **https 200 · providers local:true·demo 없음 · WS · 워커 4 Ready** 까지
- F6(AX 인증)·로그인 비밀번호는 사용자 답 대기 — 그 두 실측만 남기고 보고
