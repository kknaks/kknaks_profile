
# [planner] 슬랙 에러 채널 어댑터 — 스펙 반영 + WP-126 P7 추가 (incident 트리거 완결)

너는 **mediness `planner` 워커**다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/roles/mediness/planner/role.md` (+ 같은 폴더)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/task-redesign-spec` (spec PR #661 커밋들 위에서 작업)

## 배경

incident 재정비의 정본 흐름은 「슬랙 이슈 채널 이벤트 → AI 수집 → is_lead 게이트 → …」인데, 트리거(인바운드) 계약이 OQ-10(실전 스키마)·OQ-15(어댑터)로 열려 있었다. **사용자가 실물 샘플을 제공하고 결정을 확정**해 이제 닫을 수 있다 — 이게 이 작업(incident 재정비)의 마지막 조각이다.

## 1. SSOT

- `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/work/task-redesign/research-slack-error-adapter.md` — **소재 + 확정 결정.** 형식 실측 2종·채널·전건 자동·prod만·Events API 구독·source 확장
- `products/mediness/20-spec/spec-152-incident-response-workflow.md` — 붙일 자리 (트리거 절·OQ-10·OQ-15)
- `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/work/task-redesign/_RESUME.md` §2 — 결정 SoT
- (실물 대조) `/Users/kknaks/orca/workspaces/mediness-app/task-redesign` — 코드 read-only: `back/app/routers/slack.py`(Events API·서명검증 인프라), `POST /incidents/raise` 입력 계약, **product 원장(슬러그 검색 대상 테이블·조회)**

## 2. 반영할 계약 (사용자 확정 — 발명 금지)

1. **수신**: 봇을 #900-prod-error-alerts 에 초대, Events API `message.channels` 구독(기존 `/slack/events` 라우터·서명검증 재사용). "Error Alert" 봇 메시지만 대상(사람 잡담 제외). **stg(#901) 제외**
2. **승격 = 전건 자동** — 메시지가 쌓이면 그대로 raise → 기존 흐름(AI 수집 → is_lead 게이트). **사전 필터 없음 — 게이트가 사람 필터다**
3. **파싱**: 형식 2종(HTTP/TASKIQ — research 문서의 필드 표)을 라벨 기반 파싱. 제품별 필드 가변은 raw 보존으로 흡수. **파싱 실패여도 raw 본문으로 raise — 유실 금지**
4. **제품 슬러그 = 검색 해소** — 헤더의 제품명(WATCH·CHARTY·…)을 product 원장에서 검색(대소문자 무시 매칭)해 **해당 제품의 이슈로 등록**한다. 미매칭이면 scope 비워 raise(AI 수집이 추정 — 기존 축). 전 제품 수용
5. **진입** = `POST /incidents/raise` + `source=slack_error_channel` (이미 열린 확장 축)
6. 중복 처리: `request_id`/`task_id` 를 dedupe 키로 — 규칙(같은 키 재게시 시 처분)은 실물 기준으로 네가 제안하되 단순하게
7. **OQ-10·OQ-15 를 이 절로 닫는다** (해소 기장)

## 3. 할 것

1. spec-152 에 「인바운드 트리거 — 슬랙 에러 채널」 절 신설 (위 계약 + 케이스 매트릭스·필드 표). 개정 노트 1:1
2. **WP-126 에 P7(어댑터) 추가** — Code Surface(slack.py 분기·파서·raise 배선·슬러그 검색·테스트)·검증 항목·Pre-deploy(봇 채널 초대·이벤트 구독 설정) 포함. Board/3표·log.md 동기
3. `python3 scripts/lint-pipeline.py --strict` — mediness ERROR 0

## 4. 하지 말 것

- 코드 레포 수정 금지(read-only 실물 대조만) · 이 절 밖 SPEC 본문 수정 금지 · 결정 밖 발명 금지(애매하면 OQ)

## 9. 완료 보고 — 문구 변경 금지

> ⚠ 핸들은 dispatch preamble 값을 믿어라. **커밋·push·PR 금지.**

```bash
orca orchestration send \
  --to term_9fcc736a-df22-4409-adb4-f46292d5bc72 --from term_6eccf444-6f74-430e-98fb-cdc9ee0f011e \
  --type worker_done \
  --task-id <dispatch preamble 의 taskId> \
  --dispatch-id <dispatch preamble 의 dispatchId> \
  --subject "planner(어댑터) 완료: <한 줄>" \
  --body "변경 파일 / 계약 요약 / 검증 수치 / 미결"

orca terminal send --terminal term_9fcc736a-df22-4409-adb4-f46292d5bc72 \
  --text "[worker_done] planner(어댑터) 완료 — <한 줄>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_9fcc736a-df22-4409-adb4-f46292d5bc72 --text "[질문] planner(어댑터): <질문>" --enter`
