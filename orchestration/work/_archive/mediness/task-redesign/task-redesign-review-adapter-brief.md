
# [reviewer_code] 어댑터 delta 검수 (back 7파일 — WP-126 P7)

너는 **mediness `reviewer_code` 워커**다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/roles/mediness/reviewer/role.md` (+ 같은 폴더)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/task-redesign` — **read-only.** 검수 범위 = **미커밋 delta 만**(직전 커밋 80f50098 까지는 검수 완료 — 다시 보지 마라). delta = back 7파일(신규: `incident/slack_error_adapter.py`·테스트 2종 / 수정: `routers/slack.py`·`config.py`·`incident/const.py`·`.env.example`).

## 판정 기준

- `/Users/kknaks/orca/workspaces/mediness-mediness/task-redesign-spec/products/mediness/20-spec/spec-152-incident-response-workflow.md` **§인바운드 트리거 IB-1~IB-9** (IB-9 = tenant 사다리, 방금 명문화)
- 같은 레포 `products/mediness/30-work/work-126-incident-workflow-realign.md` §P7
- 발주 브리프: `.../task-redesign-adapter-be-brief.md`

## 체크리스트

1. IB-1 수신 경계 — 채널 allowlist·봇 발신 판정(텍스트 모양 판정 금지)·event_id 멱등 순서. **설정 미주입 시 어댑터 비가동 + 기존 동작 무회귀**(빈 allowlist = 전부 차단)
2. IB-3/IB-6 파서 — 순수 함수·예외 불투과(**어떤 입력에도 raise 유실 없음**), blocks/attachments/text 3경로, 계약 키가 보존 필드를 덮는 방향
3. IB-4 슬러그 — 대소문자 무시 정확 일치·부분 일치 거부·미매칭 시 service 빈 값
4. IB-5 dedupe — trace_id 없으면 비움(합성 금지), event_id 축과 분리
5. IB-7 처분 7종 감사 전부 배선·모든 갈래 200 ack
6. IB-8/IB-9 — 서비스 층 직호출(HTTP 자기호출 0)·기존 decision 슬랙 분기 무수정·tenant 사다리가 IB-9 와 일치
7. 보안 — 서명검증 우회 경로 없음, 새 설정 2종이 비밀값 로깅 안 함
8. allowed_paths(back/ 만)·migration 0·기존 테스트 회귀 위험

## 산출물

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/work/task-redesign/review-adapter-report.md` — 판정 + 위반(파일:줄). 문체 지적 FAIL 금지. 코드 수정·테스트 실행 금지.

## 완료 보고 — 문구 변경 금지

> ⚠ 핸들은 dispatch preamble 값을 믿어라. **커밋·push·PR 금지.**

```bash
orca orchestration send \
  --to term_9fcc736a-df22-4409-adb4-f46292d5bc72 --from term_16e3af88-b956-4e88-b6c9-8166ddb7ff8f \
  --type worker_done \
  --task-id <dispatch preamble 의 taskId> \
  --dispatch-id <dispatch preamble 의 dispatchId> \
  --subject "reviewer(어댑터) 완료: <판정 한 줄>" \
  --body "판정 / 항목별 결과 / 위반(파일:줄) / 미결"

orca terminal send --terminal term_9fcc736a-df22-4409-adb4-f46292d5bc72 \
  --text "[worker_done] reviewer(어댑터) 완료 — <판정 한 줄>. 상세는 인박스." --enter
```
