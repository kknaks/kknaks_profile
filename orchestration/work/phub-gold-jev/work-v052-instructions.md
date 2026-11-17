# WORK-007(허브) · WORK-008(앱) 작성 지시서 — SPEC 0.5.2 구현 계획

**너는 앞 판의 맥락이 없다.** `work-write-instructions.md`(같은 폴더 — 앞 WORK 때 지시)의 역할 · 제약 · 검증 · 완료 보고 꼴을 그대로 따른다(핸들은 preamble 값). allowed_paths = **`WORK-007-hub-v052.md` · `WORK-008-app-v052.md` 두 새 파일만**.

`P=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온` · `W=$P/orchestration/work/phub-gold-jev`

## 읽을 것

1. `$W/SPEC-001-hub-gold-mcp.md` · `$W/SPEC-002-chat-eval.md`(0.5.2) — 변경 기록 0.5.2 · SPEC-001 §5-9 HG1~HG3 · §9 T20~T23 · §10 · SPEC-002 §9-3d · §11
2. `$W/review-spec-v052.md` — **WARN 3(W-1 T22 문장 · W-2 수 둘 · W-3 HG2 (iii) 묶음 꼴) · NOTE 6 을 WORK 에 한 줄씩**
3. `$W/_RESUME.md` §2 맨 위 세 행(**U-1~U-4 사용자 결정 = 전부 추천** · 답 키 검토 · v05 앱 검수 뒤)
4. `$W/app-key-fix1-report.md`(키 전용 기준 대상 `key_upper_entries` · `key_lower_entries` — HG1 · HG2 뒤 빼고 다시 뽑아 대조)
5. 지금 코드(이어서 고친다): 허브 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev/backend/app/modules/gold/` · 앱 `/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev/clinic_chat/` · 앞 계획 `$W/WORK-005-hub-v05.md` · `$W/WORK-006-app-v05.md`

## 쓸 것

- **WORK-007 허브**: HG1(행 0 고민 → 가장 가까운 윗고민 · `inherited_from` · `hier.match` = 상위) · HG2(「하위 *」 = 자손 전부 · HG2-2 자기 · 물려받음 holder 에서 안 내려감) · HG3(보조 입력 ③ `concern_site` · `GOLD_HIERARCHY_DIR` · `aux_hash` · `site_match[]`) · 되적기 중 허브 몫(상품 셈 식 · 제품 offer inherited=0 · covered_by) · 시험 T20~T23 + 앞 시험 안 깨짐 · §4-9 lower 수 T16 으로 다시 셈. 확인은 18106(18105 는 코디 것).
- **WORK-008 앱**: U-1 · U-2 세트 칸 · 허브 HG1~HG3 뒤 **답 키 다시 뽑기**(키 전용 기준 대상 빼고 → 행 같은지 대조 · 다르면 보고) · key-table.md · SPEC-002 0.5.2 되적기 중 아직 코드에 없는 것(있으면 「이미 있음 · 파일:줄」) · §9-3d 구멍 묶음 문항 **draft 꼴만**(문장은 사용자 확인 — W-3 반영) · 실물 확인(「이마에 주름이 많아서 걱정이에요」 · 「볼 주름에 뭐 해?」 · Q12 꼴 · 표정주름 → B · C 종료 상태 · 나온 시술 수).
- 순서: 허브 먼저 → 앱의 키 다시 뽑기는 허브 뒤(앱의 나머지는 병행 가능). 완료 조건 · 검증 명령(앞 WORK 꼴).

## 검증

SPEC 0.5.2 변경 절 ↔ WP 대응표(미대응 0) · WARN 3 · NOTE 6 반영 줄 · 파일 경로 실재 · 공개 grep.
