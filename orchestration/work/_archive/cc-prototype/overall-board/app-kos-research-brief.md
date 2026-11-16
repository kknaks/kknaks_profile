# [researcher] 앱 KOS 확인 — 국적 · 언어 · 여권번호 수정 HAR · 공개 문진 제출 데모 1회

너는 **cc-prototype `researcher` 워커**다. **앞 판 맥락이 없다.** 먼저 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/researcher/role.md`(+ 같은 폴더 rules · skills · tools · workflow)를 읽어라. 작업 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc`(공유 · allowed_paths 밖 금지).

## 배경
① 앱(Flutter · SPEC-004) 다음 판: **신분증 스캐너**(여권 · 국적 스캔 → 기존 고객이면 KOS 고객 정보를 고친다) · **QR 문진**(고객 국적 언어로 자동 표시 → KOS 문진 제출). 결정: `orchestration/work/overall-board/_RESUME.md` §2 2026-10-27 줄(「문진 표시 언어 = 국적」 · 「스캐너」 · 「촬영 가이드 = 마스킹」 · 「앱 범위」).

## SSOT
- 새 HAR(**데모 테넌트 — 코디 확인**): `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-23-cc-overall-board/har/국적_언어_여권번호변경.har` — 사용자가 KOS 웹에서 기존 고객의 **국적 · 언어 · 여권번호**를 고치고 저장. 쓰기 = 내부 `visitor/v2/commands/update-visitor-personal-information` · 읽기 = `get-visitor` · `find-duplicated-visitor`
- 앞 조사: `orchestration/work/overall-board/reservation-visitor-update-report.md`(같은 명령 · 묶음 덮어쓰기 위험 Q-39 · Q-40) · `reservation-questionnaire-report.md`(문진 양식 · 제출 경로 둘 · 「사용 언어」 답) · `reservation-create-report.md`(새 고객 `reserveV2` 여권 · 국적)
- HAR(문진): `har/설문전송.har` · `설문내용.har`
- 인증: `reference/2026-10-12-cc-prototype/workflow-v2.md` 「인증 · 계정」 · 값은 `/Users/kknaks/orca/workspaces/cc-prototype/overall-board/procedure/.env` **읽기만**(출력 금지)

## 할 일
1. **HAR 해부(모양만)**: `update-visitor-personal-information` 본문 — 국적 · **언어**(KOS 고객에 언어 칸이 있나 · 이름 · 값 꼴 · enum) · 여권번호 · 여권 영문명 등 필드 · 묶음 전체를 보내야 하나(빠진 필드 지워짐 — 앞 리포트와 대조) · 응답. `get-visitor` 에 언어 칸이 오나 · 공개 `getVisitor` · 일정 `visitor` 에도 오나
2. **언어 칸이 있다면**: 값 목록(KOS 웹 JS 근거) · 문진 양식 `get-visitor-questionnaire` 의 번역(`transl…`) 언어 목록과 같은 꼴인가 → 「국적 → 언어」 말고 **KOS 언어 칸을 쓸 수 있는지** 판단 재료(결정하지 마라)
3. **문진 양식 언어**: 양식이 지원하는 언어 목록 · 질문별 번역 필드 모양(앞 리포트 + 데모 조회)
4. **데모 실호출 — 허가된 쓰기(이것만)**: 데모 테넌트 assert(값 출력 금지 · 운영 키 `KOS_API_tenent` 금지) · 시험 고객 1명(`[ccc 시험]` — 앞 판이 남긴 시험 고객 재사용 가능)에게 ⓐ `update-visitor-personal-information` 1회(읽은 묶음 전체 + 국적 · 언어 · 여권번호만 바꿈 → 다시 읽어 다른 필드 그대로인지 필드마다 비교) ⓑ **공개 `submitVisitorQuestionnaire`** 1회(양식 그대로 · 시험 답) → `getQuestionnaireSubmit` 으로 확인 · 고객 정보가 바뀌는 칸(앞 리포트 ⓑ)이 공개 경로에서도 같은가
5. 「정할 것」: 결정하지 말고 목록으로(Q-145 부터)

## allowed_paths · 금지
- 보고서 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/app-kos-report.md`. 그 밖 수정 금지 · 코드 · SPEC 금지
- 리포트에 테넌트 id · 고객 id · 이름 · 여권번호 · 전화 등 **값 금지**(모양 · 필드 이름 · 타입만) — public 레포
- 남긴 데모 흔적을 리포트에 목록으로

## 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 커밋·push 금지.
```bash
orca orchestration send --to term_678ac61d-2472-4a9b-ba73-61883337b957 --from term_78b8da0b-795a-41f1-a99b-69d8393d4509 --type worker_done \
  --task-id <preamble 의 taskId> --dispatch-id <preamble 의 dispatchId> \
  --subject "researcher 완료: <한 줄>" --body "보고서 경로 / 요약 / 데모 호출 결과 / 정할 것 / 흔적"
orca terminal send --terminal term_678ac61d-2472-4a9b-ba73-61883337b957 --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
- 막히면: `orca terminal send --terminal term_678ac61d-2472-4a9b-ba73-61883337b957 --text "[질문] researcher: <질문>" --enter`
