# [backend] be-fix-2 — review-code-2 F1 · BW1 ~ BW8

너는 day `backend` 워커다. 역할 · 워크트리 공유 · 검증 · 완료 보고는 `be-2-instructions.md`(같은 폴더)를 그대로 잇는다(먼저 읽어라 · allowed_paths · 금지 같음). 대상 코드 = 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-app-re1` HEAD `fb08fe4e`. mobile 워커가 같은 때 `app/` 을 고친다 — 너는 `app/` 금지. 커밋 금지.

읽을 것: `review-code-2-report.md`(같은 폴더) F1 · BW1 ~ BW8 전부(재현 · 고칠 방향).

## 고칠 것

1. **F1(FAIL)** — 「제출 1회」를 DB 가 보장하게: 원자 UPDATE(상태 조건) + 필요하면 partial unique(migration 은 0029 에 합치지 말고 새 revision 이 아니라 **0029 를 고쳐도 된다** — 아직 어디에도 배포 안 됨 · 이유 적기). 취소 덮어쓰기 · 중복 행 재현 시험(PostgreSQL · 동시 제출)
2. BW1 ~ BW5 · BW7 — 리포트 고칠 방향대로. BW2 는 고객 응답이 KOS 를 기다리지 않게(DAY 저장 = 200 · KOS 는 뒤에서 · 상태로 보임) — SPEC 007 「DAY 먼저 → KOS」 결정 안에서. 정책이 새로 필요하면 멈추고 리포트에 질문으로
3. BW6 — 기록만(코드 그대로) · 리포트에 처분
4. BW8 — 비어 있는 시험을 채운다(GET 30/IP · 틀린 토큰 10번 막음 · `X-Day-Client-IP` 믿는 규칙 · `phoneticName` · 모르는 키 · 60분 시한 · 동시 제출 · 기기 거르기 · 다른 병원 404)

## 검증 · 보고

새로 고친 시험 파일 + `scripts/check.sh` 1회. 리포트 `be-fix-2-report.md`(같은 폴더 · 처분표 · 바꾼 파일:줄 · 시험 수치). 완료 보고 = dispatch preamble 의 `worker_done` + 브리프 §9 (2) 직접 주입(subject 「backend 완료: be-fix-2」).
