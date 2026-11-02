# [infra] writer 인계 — 브리프 보충 (2026-09-30)

- 시드 dump(auth_sessions 제외, writer 가 만든 것): `~/strong-hajin-deploy-data/strong-hajin-seed.dump` (git 밖, 600). 단계 5 에서 이걸 써도 되고, 로컬 DB 에서 다시 떠도 된다 — 어느 쪽을 썼는지 리포트에 적어라. 실명·메일·비밀번호 해시가 들어 있다: 노드에 올렸으면 복원 후 지운다
- 노드 codex **0.146** vs 개발 **0.158** — AI 마운트가 옛 버전을 준다. AX 턴이 도는지 실측하고, 안 되면 멈추고 보고(노드 업그레이드는 공유 자원이라 사용자 결정)
- 노드 `/mnt/mac` = `~/mediness-data` — hostPath 경로를 이 기준으로 확인
- `ax.medisolveai.xyz` 는 현재 **NXDOMAIN** — 단계 4 에서 DNS 레코드가 필요하다. mediness 호스트가 어떻게 잡혔는지 먼저 확인
- ghcr: 사용자 로그인 완료(write:packages). writer 의 「미완」은 옛 정보
- 코드·infra 변경은 이미 머지됐다(code #5 cdb0f3f · infra #5 f04d4cb). writer 인계의 「미커밋」은 옛 정보
