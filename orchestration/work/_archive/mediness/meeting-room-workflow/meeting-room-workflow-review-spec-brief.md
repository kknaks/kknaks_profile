
# [reviewer_spec] 검수 — SPEC-151 §7.9 신설 (예약 승인 → 회의 자동 등록 체인)

너는 **mediness `reviewer_spec` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/roles/mediness/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/meeting-room-workflow-spec`
base 브랜치: `origin/mediness` → 최종 PR 대상 `mediness` (PR 은 코디네이터가 올린다)

⚠ 이 워크트리는 planner 가 방금 작업을 끝낸 상태다(미커밋 변경 3파일). **read-only 로만 봐라 — stash·checkout·복원 금지.**

## 1. SSOT — 먼저 읽을 것

- 리뷰 대상 diff: `git -C <워크트리> diff` — 변경 3파일(+129/−2): `products/mediness/20-spec/spec-151-ax-assistant-reservation.md`(§7.9 신설 중심) · `products/mediness/20-spec/spec-031-meeting-v2-diarization.md`(§3 가산) · `products/mediness/log.md`(1행)
- `products/mediness/20-spec/spec-151-ax-assistant-reservation.md` — 개정된 본문 전체(특히 §5.3 상태 조합표 · §7.1 게이트 원칙 · §7.2 와의 정합)
- `/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/work/meeting-room-workflow/research-meeting-create-flow.md` — 현행 코드 조사 리포트. 스펙의 코드 사실 주장을 이것과 대조하라

**기대는 개념** — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

planner 가 SPEC-151 에 「채팅 발 예약 승인 실행 성공 → 회의(meeting_v2) 자동 등록」 체인 계약을 §7.9 로 신설했다. 네가 이 산출물을 검수한다. 통과하면 사용자 리뷰로 넘어가고, FAIL 이면 planner 에게 수정 재발주된다.

## 3. 계약 (사용자 확정 6건 — 스펙이 이대로 반영했는지가 검수 기준)

1. 참석자 = payload `participants`(이메일) → organization_member 역해소
2. 자동 생성 회의 visibility 기본 `private`
3. 재시도 없음 — 원자성은 보상(예약 취소)으로. all-or-nothing
4. 수정·취소 동기화 이번 범위 포함
5. 체인 발동은 채팅 발(`source != meeting_modal`)만
6. host = 예약 requester. `product_tags` 빈 배열 기본

추가 확정: 스케줄 테이블(점유 화면)은 범위 제외.

## 4. 검수 관점 — 특히 볼 것

- **§5.3.2 합법 조합표와의 정합** — §7.9.4 의 A~D 행이 기존 35칸에 없는 조합·전이를 쓰지 않는가. 특히 D(보상 실패)의 「실행 축 성공 유지 + 회의 미등록 별도 표기」가 §5.3 규율과 실제로 맞는가.
- **§7.9.5 동기화** — 회의 상태 분기(대기=닫음 / live·ended=연결만 끊음)가 SPEC-031 의 회의 도메인 계약과 충돌하지 않는가. 「참석자는 파급 경로가 없다」는 주장이 §S-4(제목·참석자 변경 = 취소+재예약)와 실제로 일치하는가.
- **소유 경계** — §7.9 가 SPEC-031 소유의 계약(참석자 해소·연결 축)을 중복 서술하거나 어긋나게 쓰지 않았는가. SPEC-031 §3 가산분이 역방향 참조로만 최소인가.
- **코드 사실 대조** — 스펙이 단정한 코드 사실(source 축·participants 가 이메일·연결 축 회의당 1)이 조사 리포트와 일치하는가.
- **사용자 확정 6건 위반 여부** — §3 그대로인가. 재론·확장이 없는가.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `(read-only — 리포 파일 수정·생성 금지. 산출물은 브리프가 지정한 리뷰 리포트 파일 1개뿐)`

## 6. 검수 단계

1. diff 로 변경 범위를 산정한다 (`git diff` + status — untracked 가 있으면 위반으로 기록).
2. §4 검수 관점 5개를 각각 판정하고, 근거를 파일·절 번호로 남긴다.
3. `python3 scripts/lint-pipeline.py --strict` 1회 — mediness 범위 ERROR 0 확인.
4. 리뷰 리포트를 쓴다: `/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/work/meeting-room-workflow/review-spec-report.md` — 판정(PASS/WARN/FAIL) + 위반·우려 목록(절 번호 + 근거 규칙) + 무관 분리.

## 7. 범위 제약 — 하지 말 것

- 리포 파일 수정·생성 금지 — 산출물은 위 리포트 파일 1개뿐(워크트리 밖 절대경로).
- 스펙 취향 첨삭(문체·구성) 금지 — 판정 기준은 §3 확정 위반·기존 계약과의 모순·사실 오류다.
- FAIL 이 아닌데 FAIL 을 주지 마라. 고치면 좋은 정도는 WARN 으로.

## 8. 검증

```
python3 scripts/lint-pipeline.py --strict 실행 → 이번 제품 범위 ERROR 0 확인 (타 제품 기존 WARN/ERROR 는 '무관'으로 분리 보고). 리뷰는 read-only — 문서를 고치지 않는다
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_e8a1a258-210f-466b-8b05-c43a7ec8a7ad --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_spec 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_e8a1a258-210f-466b-8b05-c43a7ec8a7ad \
  --text "[worker_done] reviewer_spec 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_e8a1a258-210f-466b-8b05-c43a7ec8a7ad --text "[질문] reviewer_spec: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
