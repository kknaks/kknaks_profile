# [writer] WORK-008 SPEC 반영 — 검수 FAIL 재수정 (fix1)

너는 앞서 WORK-008 SPEC 반영을 한 **strong-hajin `writer` 워커**다. 같은 위치(코디 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화`)에서 이어서 고친다.
역할·규칙은 앞 브리프(`orchestration/work/strong-hajin-polish/strong-hajin-polish-write-brief.md`)와 같다.

## 1. 입력

- 검수 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/work/strong-hajin-polish/review-spec-report.md` — **FAIL 4 · WARN 8 전부** 처리한다. 권장 수정이 있으면 그것을 따른다
- 결정 SoT: `…/30-work/work-008-polish.md` · `…/_RESUME.md`

## 2. 코디가 닫은 Open Questions (이대로 반영하고 OQ 를 닫는다)

| OQ | 결정 | 근거 |
|---|---|---|
| OQ-710 | 담당자 변경 **사유는 선택**. 낡은 쪽 문장(SPEC-001 §4 Validation·`WORK_REASON_REQUIRED` 의 담당자 변경, SPEC-003 reassign reason 필수)을 고친다 | 사용자 「내용은 지금 그대로」 + 서버 코드 reason 선택(`assignments.py:222`, `task_commands.py:39`) |
| OQ-O | 「AX 제안 N」은 **다른 칩과 같은 필터 칩**이다 — 0건이면 「AX 제안 0」으로 선다. 켜면 목록이 **AX 초안 줄**로 좁아지고, 줄을 누르면 요약 카드(SPEC-002 §2.9)가 뜬다. 순서는 `받은 요청` 바로 뒤, `기한 지남` 은 **늘 맨 끝 유지**. 하나만 켜지는 규칙도 그대로 | 코디 기본값(2026-10-01) — 칩 규칙을 깨지 않는 쪽 |
| OQ-P | 「범위 밖 업무면 넓힘」은 **오늘 기준 첫 화면에만** 적용. ‹ › 는 5주 창을 1주씩 밀기만 한다. 범위 계산은 기준 주를 인자로 받는 **한 함수** | 코디 기본값 · 리뷰 권장 |
| OQ-608 | 넓히는 단위는 **주 경계** — 업무 끝날이 속한 주의 일요일(앞쪽은 시작날이 속한 주의 월요일)까지 | 코디 기본값 · 리뷰 권장 |

이 넷 때문에 FAIL-1(칩 규칙 충돌)이 닫히는 방향이다 — 「목록을 좁히지 않고 카드를 띄운다」 문장은 위 OQ-O 대로 고친다.

## 3. 줄 번호 포인터 (FAIL-4)

- 이번 판에서 SPEC 줄이 밀려 **줄 번호로 SPEC 을 가리키는 포인터**가 엉뚱한 문장을 가리킨다
- `20-spec/` 안의 포인터는 전부 고친다. 가능하면 **줄 번호 대신 절 번호·결정 ID** 로 바꾼다
- `00-baseline/`·`10-decision/` 의 SPEC 줄 포인터도 **포인터 문자열만** 고쳐도 된다(이번 fix 에 한해 allowed). 본문 의미는 바꾸지 마라
- 전부 grep 으로 센다: `spec-00[1-7][^ ]*:[0-9]` 류. 고친 개수와 남긴 개수(사유)를 보고한다

## 4. allowed_paths

- `para/projects/summer-star/strong-hajin/20-spec/` (SPEC-003 포함)
- `para/projects/summer-star/strong-hajin/00-baseline/`·`10-decision/` — **SPEC 줄 포인터 문자열만**
- 그 밖은 읽기만. `30-work/`·`orchestration/`(리포트 제외) 금지

## 5. 하지 말 것

- 커밋·push·PR 금지. 새 결정 발명 금지. 실명·메일 금지

## 6. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**

```bash
orca orchestration send \
  --to term_7941dbc9-8078-4818-8d3d-bfd5545cce31 --from <네 워커handle> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "writer 완료: WORK-008 SPEC fix1" \
  --body "FAIL 1~4·WARN 1~8 각각 처리 위치 / OQ 넷 반영 위치 / 포인터 고친 수·남긴 수 / 남은 미결"

orca terminal send --terminal term_7941dbc9-8078-4818-8d3d-bfd5545cce31 \
  --text "[worker_done] writer 완료 — SPEC fix1. 상세는 인박스." --enter
```
