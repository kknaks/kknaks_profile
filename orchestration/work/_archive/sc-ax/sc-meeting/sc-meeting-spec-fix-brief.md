# [planner] SPEC-004 0.3.0 → 0.4.0 — 검수 FAIL 해소 + 결정 D12~D14 반영 + 기획 개정 요청 확장

너는 **sc-ax `planner` 워커**다. 이전 태스크(SPEC-004 0.3.0 재작성)의 후속이다. 역할 문서:

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/roles/sc-ax/planner/role.md` (+ `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/sc-meeting-spec` (branch `kknaksss/sc-meeting-spec`). 워크트리에 네가 만든 0.3.0 변경(3파일 M)이 그대로 있다 — 그 위에 고친다. **커밋·push 금지.**

## 1. SSOT — 먼저 읽을 것

- **검수 리포트**: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/work/sc-meeting/review-01-spec-004-report.md` — §3.2 F-1(FAIL) · §3.3·§4·§5.5·§6.3 WARN 11건 · §7
- **이전 브리프**(결정 D1~D9·범위 규칙 그대로 유효): `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/work/sc-meeting/sc-meeting-spec-brief.md`
- **기획 정본**(변경 없음): `reference/2026-09-10-sc-meeting/plan-004-meeting-note.md` · `screen-005-meeting-note.md` (코디 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/`)
- **시안 리포트**(디자인이 정본에서 벗어난 곳의 목록 — §12 개정 요청의 원료): `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/work/sc-meeting/design/REPORT-회의록-v2.md` §6-0 · `design/REPORT-회의실-v2.md` §6(M1~M14)
- 리포 안: `products/sc-ax/20-spec/spec-004-meeting-note.md`(0.3.0) · `10-decision.md` · `40-architecture/system.md`

## 2. 이번에 반영할 결정 (2026-09-10 사용자) — 재논의 금지

| # | 결정 | SPEC 어디 |
|---|---|---|
| F-1 | **일시정지·재개·마이크 조작은 데모 범위 밖.** §5.2~§5.3 의 해당 셀 3개와 문구 「다른 창에서 기록 중입니다」를 걷어내고 §2.2 「데모 범위 밖」 표에 한 줄로 내린다. WS 프레임에도 pause/resume 을 두지 않는다 | §2.2 · §5.2 · §5.3 |
| D12 | **안건 본문 = 한 줄씩.** 종류 배지 없음. 안건 N. 제목 → 내용 줄 목록(줄 하나 = 짧은 문장 하나) → 「다음 할 일」 테스크 줄 목록(새 후보 + 이미 있는 업무는 「연관 업무 ›」). 메모 = 줄. AI 중간 요약 = 줄 추가·갱신(문단 재작성 아님). 합성 = 안건별 줄 병합 + 중복 접기 + 다음 할 일 추출. 「결론 남/안 남」 유지. OQ-306 종결, 기획 OQ-006 은 우리 범위에서 답함 | §4 · §6 · §7(배치 출력 스키마) · §8 · §13 |
| D13 | **상태 여섯: 예정 · 진행 중 · 정리 중 · 완료 · 실패 · 취소됨.** 정본 「정리됨」 → 「완료」로 이름만. 취소됨 유지(자동 취소 X-185 · [회의 취소]) | §5.1 전체 치환 · §12 에 이름 변경 요청 |
| D14 | **바로 시작 회의.** ① AI 는 자기 트랙에서 **회의 중 즉시** 안건을 세운다 — 기존 안건에 맞으면 그 아래 줄, 안 맞으면 새 안건(안건 출처 값 「AI 정리」 신설). 예약 회의도 같은 규칙(안건은 참고). X-94 「안건 없는 회의는 기타 블록 하나」 폐기. ② 참석자 추측(E61) 없음 — 사람이 조직도/사외 추가로 직접. ③ 제목은 종료 합성 때 AI 가 후보를 내고 사람이 확정(E60 시점 명시). ④ 회의 정보(제목·일시·참석자·**장소 글자**)는 예정·완료 상태의 머리 편집에서 고친다 — I22(예약 모달 재진입) 안 씀, 장소는 회의실 판정 없이 이름표 | §3.1 · §4(출처 값) · §7 · §8(제목 후보) · §12 |
| W | 검수 WARN 중 고칠 것: DEC-015 메뉴명 「회의 목록」 반영(§3 또는 §1) · R-6 근거 보강 · R-8 오독 정정 · R-9 누락 3건 추가 · WS 종료 계약 추가(§5.3) · frontmatter `sources:` 실재 경로로 · 나머지 WARN 은 리포트 §3.3·§5.5·§6.3 을 읽고 타당하면 고친다 | 해당 절 |
| R-12 | 열람 판정 축 문제는 기존 SCAX-ESC-002 에 묶지 말고 **새 escalation 항목**으로 연다(번호는 리포 관행대로 다음 번호) | §12 · 10-decision |

## 3. §12 기획 개정 요청 — 시안에서 확정된 이탈을 추가한다

기존 R-1~R-12 위에 아래를 **R-13~** 로 잇는다. 항목마다 「기획서 어디 · 무엇을 · 왜(결정 번호 또는 시안 리포트 항목)」. 시안 리포트를 읽고 빠진 것이 있으면 더한다.

- SCR-105-E05·§5.7·X-133: 목록 행에 상태 전부 표시(예정·정리 중·완료·실패·취소됨) + 「열람」 배지 (사용자 지시)
- SCR-105-E22·E23: 패널 안건 블록에 내용 줄 + 다음 할 일, 후보 건수 줄 삭제 (D12)
- MOD-102: 칸 순서 주제·일시·목적·안건·참석자·장소 · 반복 필드 삭제 · 사외 참석자를 이름 찾기의 「사외 참석자로 추가」로 · 참석자 조직/이름 찾기 2단 (사용자 지시)
- SCR-106-E64·X-142: 자료는 탭 안 미리보기가 아니라 행 클릭 → 드로어 하나, 데모 형식 PDF·Markdown (사용자 지시)
- SCR-106-E21·E43 등 요소표 표기가 §5.8 문구표에 T-ID 없음 → T-ID 부여 요청 (M9); E43 「업무로 섬」 → 「연관 업무 ›」
- SCR-106-E21 안건 출처 네 값 중 「세트」·「다른 회의에서 파생」은 경로 없음 → 정리 요청 + 「AI 정리」 추가 (M10 · D14)
- §5.7 vs §5.2 변형1: 예정 상태의 회의록 [수정](안건 편집) — 와이어프레임 쪽으로 (M11)
- §5.4 E29 「여러 줄 한 칸 10000자」 → 줄 단위 편집(줄 추가·삭제 요소) (D12 · M13)
- SCR-106-E03·E59: 머리에서 조직 귀속 제거, 일시·장소 칸 신설, I22 미사용 (D14 · M14)
- E60·E61: 참석자 추측 삭제, 제목 후보 시점 (D14)
- X-94: 기타 블록 규칙 폐기 (D14)
- §5.1 상태명 「정리됨」→「완료」 (D13)
- 근거 칩 위치(본문 뒤·다음 할 일 앞)·E31 건수 → 타임칩 (M12, 시안 유지)
- DS 등록 요청(기획 아님 — 별도 절 또는 10-decision 메모): pencil 아이콘 글리프
- **제외**: 삭제 확인 모달 문구·버튼명·× (기획자가 기획안을 직접 갱신 중)

## 4. allowed_paths

- `products/sc-ax/20-spec/spec-004-meeting-note.md` · `products/sc-ax/10-decision.md` · `products/sc-ax/40-architecture/system.md`(§4 만) — **이 3개뿐.** `00-planning/`·`30-work/`·ERD·타 spec 읽기만.

## 5. 작업 순서

1. 검수 리포트 F-1·WARN 을 순서대로 해소한다.
2. D12~D14 를 §2 표의 절에 반영한다. `document_version` 0.3.0 → 0.4.0, 변경 이력 한 줄.
3. §12 를 §3 목록으로 확장하고 §13 Open Question 을 갱신한다(OQ-303·306 종결, 새로 생긴 것 추가 — 예: 합성 시 AI 트랙 안건과 사람 메모 안건의 병합 규칙, 제목 후보 실패 시 기본값).
4. `10-decision.md` 로그에 D12~D14 와 F-1 처리, R-12 escalation 신설을 적는다.
5. `system.md` §4 는 D13 상태명·pause 삭제만 맞춘다.

## 6. 하지 말 것

- 화면 표면(탭·칸 배치·문구)을 새로 정하지 않는다 — 시안 리포트가 정한 것을 인용만.
- `00-planning/` 수정 금지. X-###·D-### 풀지 않는다. WP 만들지 않는다.
- 일시정지·재개를 「나중을 위해」 남겨 두지 않는다 — 완전히 걷어낸다.

## 7. 검증

```
python3 scripts/lint-pipeline.py --strict → products/sc-ax/ 범위 ERROR 0 · WARN 0. git status 가 3파일(M)뿐. grep 으로 「일시정지」·「재개」·「정리됨」(개정 요청 인용 제외)·「다른 창에서」 가 SPEC 본문에 없는지 확인. 검증 1회
```

## 8. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 값과 preamble 이 다르면 preamble 이 맞다.

- **커밋·push·PR 하지 마라.**
- 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_42ca89d6-a384-4ae9-bffb-f8e7378797da --from term_e155b48b-1a1f-4392-99eb-2889228625e7 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: SPEC-004 0.4.0" \
  --body "F-1 해소 위치 / D12~D14 반영 절 / WARN 처리 표 / §12 R-13~ 목록 / §13 종결·신설 / lint / git status"

# (2) 직접 주입
orca terminal send --terminal term_42ca89d6-a384-4ae9-bffb-f8e7378797da \
  --text "[worker_done] planner 완료 — SPEC-004 0.4.0. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_42ca89d6-a384-4ae9-bffb-f8e7378797da --text "[질문] planner: <질문>" --enter`
