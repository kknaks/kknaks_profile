# [writer] SPEC-006 이전 메모 우선 충돌 수정

너는 procedure-hub 문서 수정 워커다. Orca dispatch preamble의 완료 보고 명령을 우선한다.

## 읽을 것

- `orchestration/roles/procedure-hub/writer/`의 역할 문서
- `orchestration/work/phub-recommend/review-info-absence-spec005006.md`의 FAIL F-1과 WARN W-3
- `orchestration/work/phub-recommend/SPEC-005.md`, `SPEC-006.md`, `info-absence-spec-proposal.md`
- 이전 메모 `orchestration/work/phub-recommend/phub-recommend-walk-fix3.md` (읽기 전용)

## 작업

1. `SPEC-006.md`의 이전 메모 우선 문구가 0.3.9의 후속 fill `page≥2` 규칙을 덮지 못하도록 **적용 범위와 우선순위를 명시**한다. 걸음 중 첫 페이지 1쪽 규칙과 걸음 후 fill 뒤 페이지 규칙을 구별한다.
2. `SPEC-006.md`의 005 v3.3/0.3.4를 현재 정본이라고 부르는 문구와 「걸음은 1쪽만」의 과도한 일반화를 역사적 기록과 현 계약으로 구분한다. `SPEC-005.md`의 오래된 006 v2 참조도 역사적 맥락임을 명시한다.
3. 기존 0.3.9 신규 계약·8/20/15KB·Jev 역할·W-4 결정을 바꾸지 않는다. 새 기능 설계를 추가하지 않는다.

## 경계와 완료

- 수정 허용: `orchestration/work/phub-recommend/SPEC-005.md`, `SPEC-006.md` 두 파일만. 코드·DB·서버·평가 기록은 읽기 전용.
- 변경 전후 해당 조항과 검수 F-1/W-3 대응을 보고한다. 커밋·push·PR 하지 않는다.
- 완료 시 dispatch preamble에 따라 `worker_done`을 정확히 한 번 보내고 종료한다.
