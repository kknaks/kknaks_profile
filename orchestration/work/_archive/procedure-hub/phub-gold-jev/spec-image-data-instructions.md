# SPEC-007 0.1 — 원리 · 방법 그림 데이터(silver → DB) · 출력은 범위 밖

**너는 앞 판의 맥락이 없다.** `phub-gold-jev-write-brief.md`(같은 폴더)의 역할 · 제약 · §9 완료 보고 그대로(핸들은 preamble 값). **이번 allowed_paths = `$W/SPEC-007-image-data.md` 새 파일 1개만.** 같은 폴더에서 검수 워커 둘이 다른 파일을 본다 — 손대지 마라. Procedure Hub 데이터 · 그림 공개. 외부 호출 금지.

`W=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev` · 그림 `I=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/reference/2026-11-17-procedure-images`(읽기만) · `SM=$W/../_archive/procedure-hub/phub-ledger-redesign/silver-model` · 허브 `H=/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`(읽기만)

## 읽을 것

`$W/_RESUME.md` §2 11-17 그림 행들(맨 위 「정정 — 그림은 DB 까지 이번 판 · 출력은 다음 스펙」 · 「그림 결정」 U-4 검수 게이트 없음 · U-7 한국어 · 라벨 DB 둠 · U-10 공개 · PROCEDURE-HUB 에셋 폴더가 원천 · 바인드 마운트 · legacy-source 안 옮김 · 나머지 추천) · `$W/research-images.md` · `$W/research-images-v2.md`(정할 것 U-1~U-11 · N-1~N-3 — 추천대로) · `$W/SPEC-003-hub-gold-db.md`(테이블 · 적재 · 해시 · CSV=DB) · `$I/README.md` · `image-map.csv` · `image-assets.csv` · `image-labels.csv` · silver `mechanism` · `method` · 용어집.

## 정해진 것

- 이번 판 = **데이터만**: silver 에 그림 표 + 라벨 표(코드 1 = 그림 1 · 대표 SVG 103 · 라벨 787 · 한국어만 쓰나 표는 언어 칸 둠) · 시드 칸은 골라서(N-1 추천 — kind 는 `mechanism`/`method` · 검수 값 칸은 둠(값 「검수 전」 · 게이트 없음) · 판 값 · sha256) · DB 테이블 추가(SPEC-003 꼴 · `s_*` · 문자열 · 빈칸 NULL · FK) · 적재기 · 해시(그림 표가 aux 에 드는지 · 그림 파일 묶음 해시를 어디에) · **그림 파일은 PROCEDURE-HUB 레포 에셋 폴더로 옮김**(자리 · 대표 103 SVG 만 · 별칭 · 미리보기 · legacy-source 안 옮김) · silver CSV 를 시드 CSV 에서 짓는 스크립트(전례 `silver-supplement.py`).
- **범위 밖(다음 스펙)**: 허브 도구 · 정적 서빙 · 바인드 마운트 실행 · 앱 화면. 이 문서는 「다음 스펙이 읽을 자리」 만 적는다.
- gold 에 그림을 넣을지(원리는 `g_profile.mechanism_code` 로 닿음 · 방법은 gold 에 코드 없음 — research §2)는 정할 것으로(추천 붙임).
- concern_site 보강(research-concern-site.md 추천 7고민 8행)과 **같은 재빌드 한 번**에 들어간다 — 순서 · 37 키 대조 · 해시 바뀜을 한 절로.

## 할 것

표 꼴(칸 · PK · FK · 행 수) · 시드 → silver 스크립트 · silver-check 보탬 · gold(넣나) · DB 마이그레이션 · 적재기 · 해시 · 에셋 폴더 자리 · 재빌드 순서(보강과 묶음) · 시험(그 WP 만) · 열린 것 · WORK 전 사용자 결정(최소 · 추천).

## 검증

재셈(103 · 787 · sha 일치) · 결정 행 → 문서:줄 · 공개 grep.
