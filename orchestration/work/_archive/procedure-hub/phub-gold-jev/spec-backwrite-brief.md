# [writer] 마감 SPEC 되적기 — SPEC-001 · SPEC-003 · SPEC-008

너는 **procedure-hub `writer` 워커**다. 앞 판 맥락이 없다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/roles/procedure-hub/writer/role.md`. `W=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev`. 회사 레포 — 내부 IP · VM 이름 · 접속 값 쓰지 마라(자리표시).

근거: `$W/_RESUME.md` §2 맨 위 11-18 행 전부 · `$W/stg-runbook.md`(실행 기록) · `$W/review-code-hub-stg.md` · `$W/review-code-hub-v081.md` · `$W/review-code-app-v04.md` · 허브 코드 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`(d3d078c — 구현 결과가 정본) · 앱 `/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev`(296cb2c).

## 고칠 것(변경 기록에 한 줄씩 · 본문은 구현대로 — 새로 정하지 마라)

1. **SPEC-001** → 0.8.2: 오류 표에 `unavailable` · REST 503 · MCP HTTP 503(gold 꺼짐 — SPEC-003 §11) · 설정 `GOLD_MCP_ALLOWED_HOSTS` · `_ORIGINS`(DNS rebinding 보호 켠 채 허용 목록 · **Gateway 는 Host 를 백엔드 내부 주소로 넘기므로 그 값도 둔다**) · `GOLD_LOAD_TIMEOUT_SECONDS` · O-S1 · O-S2 닫음 · 검수 Low 3(옛 줄임 주석) 남은 것으로 표시.
2. **SPEC-003** → 0.2.1: §11 에 검수 R-1~R-4 반영 문장(503 본문 = F 코드 + 사유만 · 시간 한도 lifespan 안 · 데몬 스레드 · 켜짐 판정 = gold/health 200) · 절차서 실측(적재 6.3초 · 재시작 뒤 health 약 8초 · 컨테이너 154 → 225MB · VM 여유 약 210MB · swap 0 — 다음 판 주의) · env 재생성 = Bastion 의 배포 스크립트(docker restart 아님) · MCP 허용 호스트 두 값 · 백업 자리(경로 꼴만).
3. **SPEC-008** → 0.2.1: 구현에서 달리 받은 것(코드 검수 · WORK B 표 · app fix1: L-1 withdraw_only = talk · VF11 을 VF6 앞 · offer_name 길 없음 · site_index 캐시 키 · pick 머리 글자 9 · E8-0 CLI thinking 못 끔 → SDK 몫 · M-1 answer_ref 분모 밖) · E8 결과(v04c/v04d 3검사 94.3/95.3 · 8검사 88.7/90.9 · 비결정 폭 · 「이 정도면 받음」 사용자 결정) · 남은 것(다음 작업): SDK thinking 끔 · pick 확정 · 막힘/새 대화 문구 · answer_ref 사람 검수 · JSON 덧붙임 · 시간 한도.

## allowed_paths

쓰기: `$W/SPEC-001-hub-gold-mcp.md` · `$W/SPEC-003-hub-gold-db.md` · `$W/SPEC-008-consult-entry.md` 셋만.

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_a88e896b-403c-4d2d-9bcc-4388724b3418 --from <네 터미널 핸들> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "writer(spec-backwrite) 완료: <한 줄>" \
  --body "변경 파일 / 판 / 주의점" \
  --outcome succeeded

orca terminal send --terminal term_a88e896b-403c-4d2d-9bcc-4388724b3418 \
  --text "[worker_done] writer(spec-backwrite) 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
