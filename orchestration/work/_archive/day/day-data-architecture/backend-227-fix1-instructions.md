# [backend] #227 검수 WARN 반영(fix1) — W1 ~ W4

너는 #227 backend 워커다. 같은 워크트리 · 미커밋 그대로. 앞 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/backend-227-brief.md` 규칙 그대로(KOS 쓰기 금지 · 비밀값 금지 · 커밋 금지 · 포트 11040 · 11042 · 11043).
읽을 것: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-227-report.md` W1 ~ W4 · 「조용히 통과」.
1. **W1** — 임시 토큰을 원자적으로 꺼낸다(`GETDEL` 또는 Lua get+del · Redis 버전 확인). 검증 실패면 남은 TTL 로 되돌림. 테스트: 같은 토큰 동시 2요청 → 세션 1개(infra).
2. **W2** — 토큰 · 비밀값을 가진 dataclass 의 repr 에서 값 숨김(`field(repr=False)` 등) · 테스트(DB 없이).
3. **W3** — 로그인 경로는 연결 설정에서 필요한 값만 복호화(시스템 비밀번호를 풀지 않음) — 리뷰어 방향대로.
4. **W4** — DB 가 필요 없는 매트릭스 줄을 DB 없는 단위 테스트로 옮긴다(레포 AGENTS.md 「테스트」).
5. 리포트의 그 밖 낮은 지적이 있으면 리뷰어 방향대로.
검증: `uv run pytest -m "not infra"` · compose `up -d --wait postgres redis` → `scripts/test.sh -q` · ruff · 끝나면 `down`. KOS 실물 호출 없음.
리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/backend-227-fix1-report.md`. 완료는 preamble 의 worker_done 절차대로(둘 다).
