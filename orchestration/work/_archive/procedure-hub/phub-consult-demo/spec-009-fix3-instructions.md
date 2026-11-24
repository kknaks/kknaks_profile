# [writer] SPEC-009 수정 3 — 재검수 2 FAIL 반영 (0.2.0 → 0.2.1)
검수: 같은 폴더 `review-spec-009-r3.md`(FAIL 3 · WARN 5) — 「고칠 것」 전부 반영.
- R1 `_RESUME` 의 「SPEC-009 범위 = 부위만 · silver 바로 고침 · 이번 판 기본값」 행이 닫은 것(「눈」 합침 안 함 · 침샘 · 쇄골 · 승모근 = site + anatomy_site · 다른 이름은 허브 부위 이름만 · 거미스마일 · 러브핸들 · 측두근 제외 · 근거 = `drafts/clinic-supplement/clinic-a-20261119/user.csv:L<줄>` · 작업 공간 = `$W/silver-model/` 작업 사본)을 결정으로 반영하고 「정할 것」 에서 내린다.
- R2 `_RESUME` 줄 인용을 지금 파일로 다시 맞춘다(`grep -n` 으로 확인 · 결정 행이 늘어 계속 밀린다 — 행 첫 글자로 인용하는 방식도 괜찮다).
- R3 `silver-check.py:30-37` 원장 · step1 경로 낡음 → §3-4 깨지는 자리 · 작업 공간 절에.
- W1 새 부위 넷 자리 = 침샘 → 얼굴 > 턱 · 나비존 → 얼굴 > 볼 · 부유방 → 몸 > 가슴 · 쇄골 → 몸 > 목(3단 조사 결과 · 코디 기본값 · 사용자 확인 대기 표시). W2 근거 종류 식에 `drafts/clinic-supplement/` → 「사용자 제공」. W3 별칭 목록(애교 빼고 · 상완 · 하관전체). W4 겹침 목록 정정. W5 D3 = anatomy_site 로 이어진 같은 이름 짝 허용(코디 기본값).
- 코디는 작업 사본 스크립트에 한해 경로 · 근거 종류 식 · D3 를 고치도록 silver 워커에 지시했다(`silver-site-addendum1.md`) — SPEC 에 그대로 적어라.
- 변경 기록 0.2.1 · 끝나면 2채널 보고(subject 「writer 완료: SPEC-009 0.2.1」).
