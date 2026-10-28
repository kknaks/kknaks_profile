# [researcher] 앱 WP-KOS 게이트 — 데모 실호출 K1 ~ K4

너는 **cc-prototype `researcher` 워커**다. **앞 판 맥락이 없다.** 먼저 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/researcher/role.md`(+ 같은 폴더 rules · skills · tools · workflow)를 읽어라. 작업 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc`(공유).

## 계약 · 근거
- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/30-work/work-009-app-v2.md` **WP-KOS** 줄(K1 ~ K4) · `20-spec/spec-004-procedure-app.md` 0.4.0 §8.0(#8 · #21 ~ #23) · OQ-619 · OQ-622
- 앞 리포트: `orchestration/work/overall-board/app-kos-report.md` · `reservation-consultation-report.md` · `reservation-create-report.md`(이미지 · `registerVisitorImages`) · 웹 상담사 지정이 이미 데모에서 확인됐는지 `reservation-kos-probe-report.md` · `reservation-e2e-batch*-backend-report.md` 먼저 찾아라(있으면 K1 은 그것으로 닫고 호출 안 함)
- 인증 `reference/2026-10-12-cc-prototype/workflow-v2.md` 「인증 · 계정」 · 값 `/Users/kknaks/orca/workspaces/cc-prototype/overall-board/procedure/.env` **읽기만**(출력 금지)

## 허가된 쓰기 (사용자 「데모 쓰기 시험은 허가됨」 · 이것만)
- 데모 테넌트 assert · 운영 키 `KOS_API_tenent` 금지
- 시험 고객 = 앞 판 `[ccc 시험]` 고객 재사용 · **시험 사진 = 지어낸 그림(실제 신분증 · 사람 얼굴 금지 — 단색 + 「TEST」 글자 PNG)**
- K1 `update-reservation{counselor}` 상담 대기 · 상담 진행 일정 각 1 · K2 `update-visitor-personal-information` 에 `passportExpiryDate`(`yyyy-MM-dd`) 1 · K3 공개 `generateUploadingImageUrl` → PUT → `registerVisitorImages`(분류 · 장비 코드는 `get-codes` 로 골라 근거) 1 · K4 내부 `get-visitor-files` 조회
- 각 결과: 상태 · 오류 className · 바뀐 필드 · 화면 근거 — **게이트 판정(받음 / 거절 / 모양 다름)**

## 산출
- 보고서 1개 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/app-wp-kos-report.md`(값 · id · 이름 금지 · 남긴 데모 흔적 목록). 코드 · SPEC 금지

## 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 커밋·push 금지.
```bash
orca orchestration send --to term_678ac61d-2472-4a9b-ba73-61883337b957 --from term_e85d9857-fb49-4bbc-b7b3-44e57787c808 --type worker_done \
  --task-id <preamble 의 taskId> --dispatch-id <preamble 의 dispatchId> \
  --subject "researcher 완료: <한 줄>" --body "보고서 경로 / 요약 / 검증 수치 / FAIL·WARN · 정할 것 · 흔적"
orca terminal send --terminal term_678ac61d-2472-4a9b-ba73-61883337b957 --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
- 막히면: `orca terminal send --terminal term_678ac61d-2472-4a9b-ba73-61883337b957 --text "[질문] researcher: <질문>" --enter`
