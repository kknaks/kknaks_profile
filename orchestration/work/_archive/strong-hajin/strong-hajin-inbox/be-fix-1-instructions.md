# [backend] BE 수정 판 1 — BE-1 검수 WARN + BE-3 남은 것 (2026-10-06)

맥락: 너는 BE-1·BE-2 를 짰다. 커밋 78f014f(BE-1) · db57ba7(BE-2·BE-3). 지금 같은 워크트리에서 **frontend 워커가 `frontend/` 를 고치는 중** — `backend/` 와 공용 파일만.

## 고칠 것 — `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/review-be1.md` 의 WARN
- **W-2** OAuth 콜백: 브라우저 세션 쿠키가 있고 state 의 회원과 **다르면 거절**(링크 넘기기로 남의 계정이 붙는 것 차단). 쿠키가 없을 때(데스크톱 외부 브라우저)는 현행 유지 — 사유를 시험으로
- **W-3** OAuthGrant 등 토큰을 담은 객체 `repr=False`(전수 grep)
- **W-4** 토큰 암호화 키가 잘못되면 **부팅 실패**(요청마다 500 아님) · 운영에서 키 없으면 부팅 실패
- **W-5** 카톡 방을 빼면 다음 handshake 가 되살리지 않게
- **W-7** handshake·기기 토큰 발급 동시 경합(유일 제약 + 재시도)
- **W-8** 만료 state 정리
- **W-9** PG NOTIFY · 비활성 회원 기기 토큰 거절 시험
- **답장 전송 내구성**: BE-3 이 `BackgroundTasks`(비내구)로 보낸다 — 프로세스가 죽으면 답장이 사라지고 「보내는 중」에 멈춘다. **보낸 답장 행을 「보내는 중」으로 먼저 저장 → 연동 워커(또는 기존 작업 큐)가 보내고 결과 반영**하는 내구 경로로 바꿔라(재시작 시 「보내는 중」 재시도·실패 표시). 기존 작업 큐 방식이 있으면 그걸 따른다
## 검증
브리프와 같은 Makefile 타겟 · 바뀐 것만. 커밋 금지. 끝나면 §9 로 보고(subject "backend 완료: BE 수정 판 1").
