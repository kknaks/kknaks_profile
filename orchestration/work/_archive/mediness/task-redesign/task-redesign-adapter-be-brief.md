
# [backend] WP-126 P7 — 슬랙 에러 채널 어댑터 구현 (back/ 만)

너는 **mediness `backend` 워커**다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/roles/mediness/backend/role.md` (+ 같은 폴더)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/task-redesign` — 브랜치 `task-redesign`(WP-125+126 커밋 위). 이 delta 는 PR #136 에 얹힌다.

## 1. SSOT

- `/Users/kknaks/orca/workspaces/mediness-mediness/task-redesign-spec/products/mediness/20-spec/spec-152-incident-response-workflow.md` **§인바운드 트리거(IB-1~IB-8)** ← 계약 정본. 여기 없는 건 발명하지 마라
- 같은 레포 `products/mediness/30-work/work-126-incident-workflow-realign.md` **§P7** — 빌드 계획(Code Surface·검증 항목·OI-10~13)
- `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/work/task-redesign/research-slack-error-adapter.md` — 실물 샘플 필드 (파서 테스트 픽스처 소재)

## 2. 할 것 (P7)

1. `/slack/events` 에 `message.channels` 분기 — #900 채널 + "Error Alert" 봇 발신만(IB-1). 채널·봇 식별값은 설정 키로(하드코딩 금지 — OI-10: 실측값 미확보라 env 로 주입)
2. 파서 모듈 — 형식 2종(HTTP/TASKIQ) 라벨 기반 필드 매핑(IB-3), **파싱 실패 시 raw 본문으로 raise**(IB-6 유실 금지)
3. 제품 슬러그 검색 해소(IB-4) — 헤더 제품명 → product 카탈로그 대소문자 무시 매칭, 미매칭 시 scope 비움
4. raise 배선 — 서비스 층 직호출, `source=slack_error_channel`, dedupe 키(request_id/task_id, IB-5)
5. 감사·수신 처분 매트릭스(IB-7) 대로
6. 테스트 — WP P7 목록(7종). 샘플 2건을 픽스처로

## 3. 검증

```
cd back && uv run pytest -q <네가 만들거나 고친 테스트 파일만> (전체 스위트 금지. 테스트 DB = localhost:25434/mediness_test). 1회만
```

## 4. 하지 말 것

- `front/`·`mcp/`·문서 레포 수정 금지 · **커밋·push·PR 금지**
- `/raise` HTTP 계약·declare 게이트·기존 decision 슬랙 분기 수정 금지 (어댑터는 기존 진입점의 호출자다 — IB-8)
- 계약과 어긋나는 실물 발견 시 코드로 우회하지 말고 §9 질문 채널로

## 9. 완료 보고 — 문구 변경 금지

> ⚠ 핸들은 dispatch preamble 값을 믿어라. **커밋·push·PR 금지.**

```bash
orca orchestration send \
  --to term_9fcc736a-df22-4409-adb4-f46292d5bc72 --from term_cbbf7ec7-c416-47ec-b5d1-88d61e824a86 \
  --type worker_done \
  --task-id <dispatch preamble 의 taskId> \
  --dispatch-id <dispatch preamble 의 dispatchId> \
  --subject "backend(어댑터) 완료: <한 줄>" \
  --body "변경 파일 / 구현 요약 / 검증 수치 / 계약 준수 / 미결"

orca terminal send --terminal term_9fcc736a-df22-4409-adb4-f46292d5bc72 \
  --text "[worker_done] backend(어댑터) 완료 — <한 줄>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_9fcc736a-df22-4409-adb4-f46292d5bc72 --text "[질문] backend(어댑터): <질문>" --enter`
