# [frontend 조사 추가 1] SH-IMP-018 — 메일 본문 이미지 깨짐

기존 브리프·allowed_paths·하지 말 것은 그대로다. 같은 리포트 `fe-survey-report.md` 에 **절 하나를 더한다**(번호는 마지막 항목 뒤).

먼저 읽을 것: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-2/para/projects/summer-star/strong-hajin/improvements/SH-IMP-018-mail-body-images.md`

증상: 메일 본문(예: vercel[bot] GitHub 알림 메일)의 이미지가 깨진 아이콘·빈 칸으로 나온다. 링크·텍스트는 정상.

물음:
1. 메일 본문이 화면에 그려지기까지의 경로 전부(서버 응답 → 정제 → `MailFrame.tsx` iframe 에 써 넣기) — 파일:줄
2. 외부 `<img src="https://…">` 가 막히는 지점 후보 전부 — iframe `sandbox` 속성 · CSP(`img-src`, 웹 index.html/서버 헤더 · Tauri `tauri.conf.json` flavor 별 csp) · 서버나 프론트 정제(sanitize)에서 `src` 를 지우거나 바꾸는지 · `referrerpolicy`
3. 외부 이미지 차단이 **의도된 정책**인가 — SPEC-008(`para/.../20-spec/spec-008-external-channels.md`)·코드 주석 근거
4. 인라인 이미지(`cid:`) 처리
5. 웹과 데스크톱 앱(medi-ax)이 다르게 막는지

백엔드 정제 코드도 필요하면 읽어라(고치지 마라).

## 추가 (사용자 화면 비교 2026-10-07)

같은 vercel[bot] 메일에서 — Gmail 원본: 상단 vercel 삼각형 · Project 칸 「N」 아이콘 · Deployment 주황 점 **모두 보임**. 웹: 삼각형만 보이고 Project 아이콘은 빈 칸, Deployment 는 대체 텍스트 「Building」 만. 앱: 삼각형만 보이고 Project 빈 칸, Deployment 는 깨진 「?」 아이콘.

6. **일부만 막힌다** — 뜨는 것(삼각형)과 안 뜨는 것(Project·Deployment 이미지)의 차이를 코드로 설명하라: 출처 호스트 · 형식(svg/png/gif) · `width`/`height`·`style` · 정제 규칙이 무엇을 남기고 무엇을 지우는지. 실제 메일 HTML 은 볼 수 없으니 GitHub/Vercel 알림 메일이 흔히 쓰는 모양을 가정하지 말고, **정제·CSP 규칙이 어떤 입력을 통과시키고 어떤 입력을 막는지**를 규칙 단위로 적어라
7. 웹(대체 텍스트)과 앱(깨진 아이콘)의 표시 차이가 어디서 나오나
