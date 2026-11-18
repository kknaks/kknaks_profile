# WORK-015 작성 지시서 — 데이터 판: concern_site 보강 + 그림 데이터(SPEC-007) 재빌드 한 번

**너는 앞 판의 맥락이 없다.** `work-write-instructions.md`(같은 폴더)의 역할 · 제약 · 검증 · 완료 보고 꼴 그대로(핸들은 preamble 값). allowed_paths = **`WORK-015-data-v07.md` 새 파일 하나만**. Procedure Hub 데이터 · 그림 공개.

`W=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev` · `SM=$W/../_archive/procedure-hub/phub-ledger-redesign/silver-model`(gitignore 로컬) · 그림 `I=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/reference/2026-11-17-procedure-images` · 허브 `H=/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`(읽기만 — **지금 다른 워커가 0.7.2 를 구현 중** · 이 WORK 의 허브 쪽 WP 는 그 뒤에 돈다고 적어라) · 앱 `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev`(답 키 대조 · 읽기만)

## 읽을 것

`$W/SPEC-007-image-data.md`(재빌드 11단계 · 표 · 적재기 V13 · 에셋 폴더) · `$W/review-spec-007.md`(**WARN 1: 재빌드에 gold-check A3(silver-supplement source_ref 재현) 빠짐 — WORK 에 한 줄** · NOTE 6) · `$W/research-concern-site.md`(추천 7고민 8행 · 근거 경로 표) · `$W/_RESUME.md` §2 11-17 맨 위 행들(concern_site 판정 = 추천 · 규칙 0.7.2 · SPEC-007 U7-1~3 = 추천 · **시험은 그 WP 것만 · 전체 금지**) · `$W/SPEC-003-hub-gold-db.md` · `$W/SPEC-001-hub-gold-mcp.md` 0.7.2 · 앞 WORK 꼴 `$W/WORK-010-hub-db.md`.

## 쓸 것

- WP 순서: ① silver — concern_site 8 행(근거 경로 표 그대로) · 그림 시드→silver 스크립트 · 두 표 · silver-check(새 층) ② gold 재빌드 · gold-check(**A1 고정 기대값 보탬 · A3 재현 — WARN 1**) · 해시(gold_hash · aux_hash 어느 것이 바뀌나) ③ 허브: 모델 · alembic(74→76) · 계약 상수 · 적재기 V13 · 에셋 폴더(`assets/procedure-images/` · 대표 103) — **0.7.2 구현 뒤** ④ DB 재적재(로컬 18432) ⑤ 37 답 키 대조(앱 · 백업 폴더 먼저 · 바뀌는 문항 보고) · 0.7.2 SP 재셈 다시(보강 뒤 filter 짝 · 흉터+볼 113)
- 각 WP 의 시험 파일 · 명령(전체 금지) · 누가(데이터 스크립트 = 데이터 워커 · 허브 = backend 워커 · 키 대조 · 재시작 = 코디) · 되돌리기(silver · gold 백업 · DB 판).
- 데이터는 gitignore 로컬 — 커밋 대상 아님(서버 시드 결정 전) · 허브 레포에는 코드 + 에셋만.

## 검증

SPEC-007 · research-concern-site 대응 미대응 0 · 경로 실재 · 공개 grep.
