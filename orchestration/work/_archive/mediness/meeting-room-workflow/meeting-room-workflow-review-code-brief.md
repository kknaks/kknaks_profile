
# [reviewer_code] 검수 — WP-125 백엔드 착지 (예약 승인 → 회의 자동 등록 체인)

너는 **mediness `reviewer_code` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/roles/mediness/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/meeting-room-workflow` (**read-only — backend 워커의 미커밋 변경 위. 수정·stash·checkout 금지. 테스트도 돌리지 않는다** — 코디가 이미 63 passed 독립 확인)

## 1. SSOT — 판정 기준

- `/Users/kknaks/orca/workspaces/mediness-mediness/meeting-room-workflow-spec/products/mediness/30-work/work-125-reservation-meeting-autoregister.md` — 작업서 (P0~P5·비목표·Code Surface)
- `/Users/kknaks/orca/workspaces/mediness-mediness/meeting-room-workflow-spec/products/mediness/20-spec/spec-151-ax-assistant-reservation.md` §7.9 — 계약 (조합표 4행·파생 매핑·동기화 경계)
- `/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/work/meeting-room-workflow/wp125-backend-report.md` — 워커 자체 리포트

리뷰 범위 산정: `git status --porcelain` + `git diff` (untracked 3파일 포함 10파일, +433/−24 근방).

## 2. 검수 관점

1. **계약 대 코드** — 조합표 A~D 가 코드로 정확히 서는가: 실행 축 기록이 체인 뒤인가(외부 성공 시점에 «성공» 안 적는가), D 행이 실행 «성공» 유지 + 회의 미등록 표기인가, 보상이 그 external_id 하나만 취소하는가(조건 재조회 금지).
2. **source 축 한 자리** — 발동(P1)·파급(P3) 판정이 같은 정의를 쓰는가. P3 가드 2겹(연결+source)이 실제로 서는가 — 모달 발 회의가 파급되지 않는 음성 경로 확인.
3. **모달 발 경로 diff 0** — `meeting_v2_service` 의 모달 발 함수·`_reserve_room_now` 동작이 바뀌지 않았는가 (리팩토링 이동 포함해 동작 동형인지).
4. **파생 매핑** — host=requester, 이메일 역해소(정방향 술어 재사용 — 새 술어 발명 없는지), host 미해소만 실패, private, product_tags 빈 배열, 슬롯 반올림 없음.
5. **migration 0135** — 부분 유니크 인덱스가 계약(예약 건당 회의 최대 1)과 맞는가, nullable FK 에 대한 partial index 조건, 다운그레이드 왕복.
6. **신설 금지 목록** — 새 endpoint·leaf·state enum 값·카드 명령·DELETE 표면 0 확인.
7. **allowed_paths** — diff 가 `back/` 밖으로 안 나갔는가 (코디 1차 확인했으나 재확인).
8. **테스트가 계약을 고정하는가** — 34건이 조합표·동기화 분기·멱등·source 게이트·역해소 경계를 실제로 물고 있는지 (돌리지 말고 읽어서).

## 3. 산출물 — 리포트 1개

`/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/work/meeting-room-workflow/review-code-report.md`

- 판정(PASS/WARN/FAIL) + 위반 목록(파일:줄 + 근거 규칙/계약 절). 리포 파일 수정·생성 금지.

## 4. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 값과 preamble 이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_ae5c9156-a854-48b7-8f65-528976906150 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_code 완료: <판정 한 줄>" \
  --body "판정 / 관점별 근거 / 위반 목록 / 미결"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_ae5c9156-a854-48b7-8f65-528976906150 \
  --text "[worker_done] reviewer_code 완료 — <판정>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_ae5c9156-a854-48b7-8f65-528976906150 --text "[질문] reviewer_code: <질문>" --enter`
