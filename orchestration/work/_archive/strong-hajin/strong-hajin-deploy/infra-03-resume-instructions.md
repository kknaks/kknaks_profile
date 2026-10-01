# [infra] 재개 (2026-10-01) — 코디 확인 상태 기준

## 된 것 (다시 하지 마라)
- AppProject `strong-hajin` apply · `ax.medisolveai.xyz` DNS route (해석됨, 지금은 404 — 앱 없음)
- `strong-hajin-prod` 네임스페이스: 리소스 0 (코디 kubectl 확인)

## 할 것 — 단계 3~6
브리프 §6 의 3→5→6 그대로. 먼저 `report-infra-deploy.md` 에 위 상태를 반영해 두고 시작(죽어도 이어지게 단계마다 갱신).

## F6 답 (사용자): Mac Studio 에 있는 codex 인증을 복사해 쓴다
- medi-me 에 이미 있는 codex `auth.json`(mediness 가 쓰는 것 — `mediness-prod` codex-home PVC 또는 medi-me 호스트의 codex 홈, 어느 쪽인지 먼저 확인)을 strong-hajin-prod 의 codex-home PVC 로 복사
- 값은 **파이프로만** 옮긴다. 화면·로컬 파일·리포트에 내용 출력 금지. mediness 쪽 파일·PVC 는 읽기만
- 복사 후 AX 턴 1회 실측(워커 로그로 codex 호출 성공 확인). codex 0.146 이라 실패하면 멈추고 보고

## SSH 가 자주 끊긴다
- 명령을 짧게, 멱등으로. 긴 것은 원격에서 `nohup … > /tmp/sh-*.log` 로 띄우고 로그를 읽어라
- 로그인 비밀번호는 여전히 사용자 답 대기 — 그 실측만 남기고 보고
