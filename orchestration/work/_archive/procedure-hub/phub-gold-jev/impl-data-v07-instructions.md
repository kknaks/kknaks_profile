# [backend] 데이터 판 구현 — WORK-015(concern_site 보강 + 그림 데이터 · 재빌드 한 번)

**너는 앞 판의 맥락이 없다.** `phub-gold-jev-be-brief.md`(같은 폴더)의 역할 · 제약 · §9 완료 보고 꼴만 써라(핸들은 preamble 값 · 그 브리프의 WORK-001 · 18105 문구는 옛 판). Procedure Hub 데이터 · 그림 공개. 비밀값 · 접속 문자열 찍지 마라.

**이번 일 = `WORK-015-data-v07.md` WP ① ~ ④**(⑤ 37 키 대조 · 재시작은 코디). 계약 = `SPEC-007-image-data.md` · `research-concern-site.md`(넣을 8 행) · `SPEC-001` 0.7.2 · `SPEC-003`. 검수 `review-spec-007.md` · `review-work-015.md` 반영 · `_RESUME.md` §2 맨 위 「WORK-015 B 코디 답」.

## 작업 자리(allowed_paths)

- 데이터: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model/`(gitignore 로컬 — silver · gold · 스크립트 · notes) — **백업은 코디가 떠 둠**(`silver-model.bak-pre-v07data/` · 건드리지 마라).
- 허브: `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev/backend/` + 레포 루트 `assets/procedure-images/`(대표 SVG 103 만) · HEAD 3a5da4a(0.7.2 커밋됨) 위 · 커밋 금지.
- 그림 원천(읽기만): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/reference/2026-11-17-procedure-images/`.

## ⚠ 시험 — 사용자 지시

**WP 마다 그 WP 시험만 · 전체 pytest 금지.** 돌린 파일 · 통과 수 보고.
- **W-2**: WP-3 이 `tests/medallion_fixture.py` 를 고치면 그 fixture 를 쓰는 4 파일(`test_gold_tools_synthetic.py` · `test_gold_rest.py` · `test_gold_mcp.py` · `test_gold_v07_resolve.py`)도 그 WP 에서 돈다.
- **W-1**: 보강으로 바뀌는 실물 기대값(리포트 W-1 목록 — `test_gold_v07_site.py:247-251` · `test_gold_v07_descend.py:283` 등 박힌 수 전부)을 **시험을 돌리기 전에 네 재셈 스크립트로 먼저 셈해** 표(옛 값 → 새 값)로 보고하고, 그 값으로 기대를 고친다. 시험이 낸 수를 그대로 옮겨 적지 마라.

## 순서 · 판정

1. ① silver — concern_site 8 행은 **`silver-supplement.py` 안에 넣는다**(재생성에 안 지워짐 · WARN 1) · 그림 두 표 + 시드→silver 스크립트 · silver-check(git 필터 탓 G3 밖 FAIL 0 = 통과 · silver-check 따로 한 번 더).
2. ② gold 재빌드 · gold-check(A1 보탬 · A3 재현 · G1 · A2 는 git 필터 탓이면 통과) · 해시 표(gold_hash 는 그대로여야 하나? WORK 표대로 — 다르면 멈추고 `[질문]`).
3. ③ 허브 — 계약 상수 · 모델 · alembic(74→76 · 새 revision) · 적재기 V13 · 에셋 103.
4. ④ 로컬 DB 재적재: 접속 값은 `~/.config/phub/medallion-pg.env` 를 `set -a; . 파일; set +a` 로만 · DB `phub_medallion` · **alembic upgrade → dry-run → 적재** · 18107 에 띄워 health · 턱살(CON-168) · 「볼 + 탄력 저하」 · 「흉터 + 볼」(113 그대로) 확인 후 내림. **18105 는 건드리지 마라**(코디가 재시작).

## 보고

WP 끝마다 `[진행] backend: …` 한 줄 · 완료에 「코디: 18105 재시작 · 37 키 대조 필요」 · 기준 키(코디가 0.7.2 로 뽑음 — v06 과 차이 0)는 앱 `data/eval-set/_v072_pre_data/`.
