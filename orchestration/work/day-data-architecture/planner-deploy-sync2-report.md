# planner-deploy-sync2 — done (미커밋 · lint --strict 0 error · IP 0)
1. 검수 남은 것 ① VM 행 = Docker 29.9 · compose v5.7 · python3.12 · 로그 회전(json-file 10m × 5) · azureuser docker 그룹 설치됨 ② 머리말 「배포 파일 없음」 → 「#233(937dbb68)으로 들어옴(workflow 넷 · compose · compose.edge · scripts/deploy · PR #228 dev 머지 전)」 ③ ACR Reader = 부여됨(2026-11-09 · ACR 권한 · 배포 계정 두 행).
2. DNS = 준비됨(2026-11-09 · 가비아 · A 레코드 `day-dev` · `day` → VM 공인 IP · 반영 확인 · 값 안 적음) — 준비 표 · 40-architecture/README 줄(「DNS 남음」 제거) 같이.
3. log 한 줄. 남은 사용자 준비 = GitHub Environments · Actions 변수 · Key Vault 비밀 6.
