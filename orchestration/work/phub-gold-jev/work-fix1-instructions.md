# WORK-001 · WORK-002 수정 1 지시서

**너는 앞 판의 맥락이 없다.** `work-write-instructions.md`(같은 폴더)의 역할 · 제약 · 검증 · 완료 보고를 그대로 적용한다. allowed_paths = `WORK-001-hub.md` · `WORK-002-app.md` 두 파일만(SPEC 은 고치지 마라).

`W=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev`

## 읽을 것

`$W/review-work-001-002.md`(WORK-001 W2 · N6 / WORK-002 F1 · W6 · N7) · `$W/_RESUME.md` §2 맨 위 행(코디 결정 11-16 「WORK 검수 뒤」)

## 할 것

- **F-1**: `--allow-unconfirmed` 를 **뺀다**. E6 · WP-8 완료 조건 3 은 **합성 키**(가짜 코드 · 가짜 이름으로 만든 키 — 배관 확인용 · 결과는 채점 수치로 쓰지 않음 표시)로 바꾼다. 실제 채점은 사용자 확인된 키로만(SPEC-002 §9-5 절차 4).
- **W2-1(코디 결정)**: 범위 밖 · 입구 없음 · 실행 중단에서도 단계 ⑤ 를 부른다 — `end_state` 와 빈 verified 를 넘겨 그 상태를 말하게 함(세 열 같은 조건 · 앱이 문구를 지어 넣지 않음). 문구는 답 프롬프트 초안에 · e2e 보고 때 사용자 확인(C-1).
- **W2-2**: C-1 이 SPEC O-9 「답 프롬프트 WP 앞」 과 다름을 WORK-002 에 명시하고 근거 = `_RESUME` §2 「진행 순서」 행 · 결과에 「프롬프트 미확정」 표시.
- 그 밖 W1-1 · W1-2 · W2-3 ~ W2-6 · N 전부 = 리포트 「고칠 방향」 첫 선택지. N1-1(SPEC 빈 자리 — pair 에 b 없이 package_kinds)은 WORK-001 열린 것에 제안 + 「SPEC 0.4.2 때 반영」 표시.
- 두 문서 0.2.0 · 변경 기록.

## 검증

지적 → 문서:줄 표 · SPEC 대응표 다시(미대응 0) · 공개 grep.
