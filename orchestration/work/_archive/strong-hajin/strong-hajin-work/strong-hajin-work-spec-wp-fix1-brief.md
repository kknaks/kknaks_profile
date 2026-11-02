# SPEC/WP 수정 재발주 — 최종 업무·요청 프레임

## 1. 너는 누구인가
너는 `strong-hajin-work` 문서 워커다. 현재 코디네이터는 `term_30dfd82f-6173-466e-ae5c-d291b46c4a55`다. 이전 SPEC+WP 통합 결과에 대해 reviewer가 FAIL/WARN을 냈다. 코드를 수정하지 말고 문서만 고친다.

## 2. 목표
`review-spec-wp-report.md`의 F-1~F-3을 반드시 해소하고, 같은 리포트의 W-1~W-7도 이번 수정에서 닫는다. 계약·데이터 모델·결정 내용을 새로 설계하지 않는다. 확정된 D-21/U-6 프레임을 문서 전체에 일관되게 반영한다.

## 3. 허용 파일
반드시 아래 파일만 수정한다.
- `para/projects/summer-star/strong-hajin/10-decision/decision-001-work-page.md`
- `para/projects/summer-star/strong-hajin/20-spec/spec-001-work-management.md`
- `para/projects/summer-star/strong-hajin/30-work/work-003-inbox-predecessor-and-create-frame.md`
- `para/projects/summer-star/strong-hajin/30-work/README.md`
- `para/projects/summer-star/strong-hajin/log.md`

## 4. 정확한 수정 항목
리뷰 리포트 `orchestration/work/strong-hajin-work/review-spec-wp-report.md`를 먼저 읽고 아래를 실물로 수정한다.

### FAIL
1. `spec-001`의 S-1/S-2/Flow 잔재를 D-21과 맞춘다.
   - S-1: 업무 갈래는 담당자 칸이 없고 서버가 현재 사용자를 담당자로 기록한다고 쓴다.
   - S-2: 머리 토글을 요청으로 바꾼 뒤 요청 갈래 담당자에서 동료를 고른다고 쓴다.
   - Flow: `업무 만들기 · 갈래=요청 + 담당자=동료`로 정정한다.
2. `spec-001` frontmatter `works`는 `[]`로 되돌리고, 본문 실행 WP 문장에서 WORK-003 wikilink를 제거한다. ID 서술은 허용한다.
3. frontmatter 밖의 중복 wikilink를 ID 서술로 낮춘다.
   - `decision-001`: SPEC-003 두 곳, WORK-003 한 곳
   - `spec-001`: SPEC-003 두 곳
   - 이번 diff 밖으로 분류된 `spec-001:33`의 기존 부채도 같은 규칙을 깨끗하게 닫아도 된다.

### WARN도 이번에 닫기
4. CTA 문구를 §2와 §3에서 같은 갈래별 문구로 맞춘다. 확정 프레임의 버튼 명칭을 기준으로 한다.
5. 제목/내용 두 화면 필드가 실제 payload의 `title`/`description`으로 가는 매핑을 Request/Response에 한 줄 추가한다. 기존 `content` 계약을 임의로 재설계하지 않는다. 공통 한 벌 목록에는 `reference_task_ids`를 추가하고, 만들기 창에서는 받지 않는다는 점을 명시한다.
6. `WORK_RECIPIENT_NOT_ALLOWED`/`WORK_RECIPIENT_INACTIVE` 표시 위치를 `생성 창 요청 갈래의 담당자 필드`로 좁힌다. 관련 `생성 창의 담당 후보` 표현도 같은 방식으로 고친다.
7. 요청 갈래 결재자는 한쪽으로 고정한다. OQ-M 자체는 보존하되, WORK-003 Phase 3 구현 지시는 `필드를 열지 않는다(보내면 extra='forbid'로 422)`로 고정한다. 양자택일 문장을 남기지 않는다.
8. `30-work/README.md`의 Status Board/Work List/Spec Coverage에 WORK-003 행을 추가하고 `log.md`에 2026-09-19 문서 작업 완료/리뷰 수정 기록을 추가한다. 기존 행과 양식을 먼저 읽고 형식을 맞춘다.

## 5. 보존 규칙
- D-1~D-21, 기존 SPEC-001 계약, SPEC-003 연계, OQ-M/OQ-N 및 기존 미결을 삭제·약화·임의 확정하지 않는다.
- 참고 업무는 UI에서 내린다는 결정과 계약/저장/detail 보존을 유지한다.
- 링크 규칙은 frontmatter만 관계 링크를 소유한다. 본문은 일반 ID 표기만 쓴다.
- WORK-003 phase/allowed paths/acceptance criteria는 유지하고 필요한 문장만 고친다.

## 6. 검증
- 허용 파일 외 변경 0건 확인.
- F-1~F-3, W-1~W-7 각각 해소 여부를 줄 번호와 함께 보고한다.
- frontmatter, 상태, 태그, wikilink 규칙을 재확인한다. 없는 lint 스크립트는 실행했다고 쓰지 말고 unavailable로 기록한다.

## 7. 완료 보고
작업 요약·변경 파일·검증 결과·남은 WARN/미결을 보고한다. 커밋/push/PR은 하지 않는다. 완료 시 현재 dispatch의 `worker_done`을 코디 handle로 보내고, 같은 요약을 코디 터미널에도 직접 주입한다.
