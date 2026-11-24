# [silver] 추가 지시 2 — 멈춘 자리 넷 답(코디)

1. **A1 → (a)** 묶음 기준 사본 `archive/silver-before-clinic-a-20261119/` 로 기준을 바꾸고, 허용 = 리포트 §5-1 (a) 목록대로. 기준 사본은 패치 전 silver(원본 아카이브와 바이트 같은 것)로 만든다.
2. **A3** → 기준 사본에서 `silver-supplement.py` 재현 + `build_site_3tier.py` 재현을 차례로 돌린 결과와 대조하도록.
3. **G3 · G1** → 경로를 `phub-consult-demo/` 로 고치고, **작업 사본(`silver-model/`) 밖 변경은 G 검사에서 뺀다(WARN 으로만)** — 코디 변경(.gitignore · config · README · work-index · reference/)은 데이터가 아니다. A2 도 다시 돌려라.
4. **별칭 근거 종류 섞임 → 받아들인다**(이번 판). 리포트에 「이동한 부위 별칭 25 + SITE-120 의 근거 종류가 원장 + 사용자 제공」 으로 남겨라. gold-build 는 고치지 마라.
- 고친 스크립트 줄은 전부 리포트에 diff. 다시 silver 검사 → gold 빌드 → gold-check 전부 돌리고 PASS/WARN/FAIL 줄 · 새 해시로 리포트 갱신. 그 뒤 완료 2채널 보고.
