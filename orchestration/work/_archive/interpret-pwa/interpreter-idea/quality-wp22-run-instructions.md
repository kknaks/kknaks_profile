# WP22 ② ~ ⑦ 실행 지시 — 규칙 파일 확인 끝 (코디 · 2026-11-14)

- `reference/2026-11-12-interpreter-idea/test-rules.json` 43 규칙을 코디가 목록과 한 줄씩 대조했다 — **그대로 승인**(바꾸지 않음). `made` 는 「코디 확인 2026-11-14」 로 고쳐도 된다. **이제부터 규칙 파일을 바꾸지 마라**(바꾸면 A · B 다시 판정).
- WORK WP22 ③ ~ ⑥ 을 실행:
  - ③ 조합 **A**(v5 · 시드 `.6` · 문안 없음 · 막기 없음) · **B**(v6 · 나머지 A 와 같음)로 T01 ~ T33 — 같은 음성 파일
  - ④ A 의 언어별 context 글자 수 = 운영 main `e0fbda8` 값(수치)
  - ⑤ 울쎄라 가르기 8칸 — T02 · T03 × zh `Ultherapy` 역방향 짝 있음/없음(`--drop-reverse`) × A · B
  - ⑥ 3절(T23 ~ T26) 조각 수 · 지연 A · B 따로
- 결과: 레포용 JSON → `orchestration/work/interpreter-idea/`(번호 · 판정 · 수치만) · 로컬용 → `reference/2026-11-12-interpreter-idea/quality-run/`(git 제외)
- 완료 조건: A · B 막힌 빈 원문 0 · `text` 0 · 오류 행(`machine=error`) 수를 따로 보고 · 레포용 JSON 에 문장 · FAIL 문구 0(grep)
- 보고: `wp22-be-report.md` 에 「② ~ ⑥」 절 — 절별 기계 FAIL 수 A 대 B · 가르기 8칸 표 · 조각 수 · 지연. ⑦ 사람 판정은 코디가 한다(로컬 결과 경로만 알려 줘)
