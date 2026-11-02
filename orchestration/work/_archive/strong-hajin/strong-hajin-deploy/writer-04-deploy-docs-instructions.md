# [writer 4차] 배포 문서 정리 (2026-10-01, 사용자 지시 「이번 목적은 배포 — 배포 문서 정리, 고도화는 다음」)

너는 맥락이 없을 수 있다. 원천은 **파일**이다 — 기억으로 쓰지 마라:
- `orchestration/work/strong-hajin-deploy/_RESUME.md` §2 결정 표 · §4 산출물(PR 번호) · §5 이력
- 리포트: `report-infra-deploy.md` · `report-fe-release-dmg.md` · `report-fe-flavors.md` · `report-fe-icon.md` · `research-seed-path.md`
- 지시서: `infra-0*-*.md` · `fe-0*-*.md`
- 기존 문서 형식: `para/projects/summer-star/strong-hajin/70-runbook/runbook-001-local-tauri.md` · `10-decision/decision-005-tauri-wrapper.md` · `40-architecture/deploy/environments.md` · 각 폴더 README.md

## 쓸 것 (이 파일들만)
1. **`70-runbook/runbook-002-production-deploy.md`** (신규, RUNBOOK-001 형식) — 다음 세션이 이것만 보고 재배포한다
   - 구성도(ax.medisolveai.xyz → cloudflared → ns strong-hajin-prod: front·back·worker4·postgres·redis), 레포 3개와 역할
   - **코드 변경 → 운영 반영**: main 머지 → arm64 이미지 빌드·push(`deploy/k8s/*.Dockerfile`, `ghcr.io/kknaksss/strong-hajin-{back,front}:<sha>-arm64`) → infra `values-prod.yaml` image.tag 커밋·PR → Argo **수동 sync**(automated 꺼 둔 이유)
   - 최초 1회(이미 했음, 재구축 때): AppProject apply · DNS route · ns·ghcr-pull·postgres-secret·strong-hajin-secret(키 이름만: SONIOX_API_KEY·TDL_EMAIL·TDL_PASSWORD 등) · hostPath · datastores sync · 시드 dump 복원 · codex-home PVC auth.json
   - **비밀값 다루는 법**: 파이프로만, 출력 금지. codex 인증은 전용 CODEX_HOME 로그인 1회, mediness·로컬 ~/.codex 와 공유 금지(refresh token 회전) — 왜인지 한 줄
   - **데스크톱 앱 두 판**: 표(개인 Strong Hajin/app.stronghajin.desktop/origin 미정 · 회사 medi-ax/app.ax.desktop/ax.medisolveai.xyz), `SHELL_FLAVOR`·`make shell-build`, Developer ID 서명 → notarytool(AC_NOTARY) → staple → spctl 확인, preflight M-5, identifier 를 판 안에서 바꾸면 로그아웃
   - 상태 확인 명령(curl·kubectl get pods·Argo 상태)과 알려진 함정: medi-me SSH 끊김(nohup), Mac 잠자기로 워커 사망, 노드 codex 0.146, 인증서 만료 **2026-11-28**, dmg Finder 꾸밈 없음(헤드리스)
   - 실제 실행한 명령만. 값(비밀번호·토큰·DB URL)은 절대 적지 않는다
2. **`40-architecture/deploy/environments.md`** 갱신 — 운영 「가동」으로, 「아직 배포할 수 없는 이유」 절을 「해소 기록」으로 바꾸고 각 항목이 어디서 닫혔는지(PR·결정). 남은 것(로그인 시도 제한 없음, M-5 사용자 확인, 개인판 origin 미정, 실명 시드 운영 DB 등)은 「남은 것」 절
3. **`10-decision/decision-007-production-deploy.md`** (신규, DEC-005 형식) — 이번 작업의 결정들: 운영 로그인 = 이메일/비밀번호(프로파일 무관, 바로가기는 개발만) · MCP 운영 가드 · host·registry · 운영 데이터 = 로컬 시드 dump · AI = 노드 마운트 + 전용 codex 인증 · 앱 두 판 · 워드마크 MEDISOLVE · 시드 범위(조직도 전체 9표, 실제 투입은 AX 1팀 4명). 각 결정에 근거(사용자 지시·PR·리포트). 실명·메일 쓰지 마라(「4명」으로)
4. README 색인: `70-runbook/README.md` · `10-decision/README.md` · `40-architecture/README.md`(있으면) 에 행 추가
5. `log.md`·index 는 건드리지 않는다(아카이브가 한다)

## 하지 말 것
- 코드·infra·config 수정(config 는 코디가 고친다) · 실명·이메일·비밀값 기재 · 커밋
- 결정을 새로 만들지 마라 — `_RESUME.md` §2 와 리포트에 있는 것만. 없으면 Open Questions

## 보고
두 채널. task `task_b12450b8e256` · dispatch `ctx_9d693170f05a` · 코디 `term_8d586fcb-a104-4f31-9f5f-fd3b659a1d24`.
