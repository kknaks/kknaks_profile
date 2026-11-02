# [frontend] WP3·WP4 ↔ 실제 back 계약 대조 (WP5 전 준비)

목업이 아니라 **실제 `cc/back`** 을 임시 포트로 띄워 front 가 쓰는 응답 모양이 맞는지 대조하고, **front 쪽에서** 맞춘다.

- back 은 지금 backend 워커가 WP2(통역 WS)를 작업 중이다 — `cc/back/` 파일은 **읽기만**, 고치지 마라. 실행은 해도 된다:
  `cd cc/back && CC_BACK_PORT=18621 CC_FRONT_ORIGIN=http://localhost:13621 uv run python -m app.seed build --date 2026-10-09 --at 14:45` 후 서버 기동 명령은 `cc/back/README.md` 대로(포트 18621). `CC_DB_PATH` 는 `data/contract-check.db` 처럼 **별도 파일**로(사용자 E2E 용 `data/cc.db` · `seed.json` 을 건드리지 마라 — seed build 가 seed.json 을 덮어쓰면 끝나고 원래대로 다시 build 해 둔다)
- front 는 `NEXT_PUBLIC_API_BASE_URL=http://localhost:18621` 로 임시 포트 13621 dev
- 대조: `GET /api/staff` · `/api/board` · `/api/staff/{의사}/home` · `/api/staff/{코디}/home` · `/api/patients/{id}`(⚠ 주의 있는 고객 포함) · SSE · `assign` → 의사 home 갱신 · `start`/`finish` · `reset` — 각 응답을 `lib/types.ts` 와 필드 단위로 대조, headless 크롬으로 /login → /desk · /staff · 환자 상세 화면이 실데이터로 깨짐 없이 그려지는지
- 다른 곳은 **front 를 고쳐** 맞춘다. back 이 계약(addendum · types.ts)과 다르게 준 것 중 front 로 흡수할 수 없는 것만 리포트 「back 수정 필요」에
- 끝나면 두 임시 프로세스만 종료. 사용자 포트 3600 · 8600 금지. 커밋 금지
- 검증: `npx tsc --noEmit` · `npm run lint` · `npm run build` 1회씩
- 리포트: 같은 폴더 `contract-check-fe-report.md` — 엔드포인트별 같음/다름/고친 것 · back 수정 필요 목록 · 화면 캡처 확인 결과
- 완료 보고는 WP4 브리프 §5 와 같은 두 명령(subject 「frontend 완료: 계약 대조 …」)
