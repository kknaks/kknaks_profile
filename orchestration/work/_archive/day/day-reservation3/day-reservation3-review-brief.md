# [reviewer] SPEC-008 예약 요청 스레드 코드 1차 검수 (Delivery #297 · WP-0 ~ 3)

너는 **day `reviewer` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation3/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation3`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

**너는 앞 맥락이 없다.** 이 워크트리의 **미커밋 변경**(`git status` · `git diff origin/dev`)이 검수 대상이다. 파일을 고치지 마라(stash · checkout · reset 금지). backend · frontend 워커는 지금 쉬고 있다.

## 1. SSOT — 먼저 읽을 것

- Delivery Issue #297(`gh issue view 297 --repo MediSolveAIDev/CENTURION_DAY` — Acceptance A1 ~ A7 · Non-Goals)
- SPEC-008 `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation3-spec/products/day/20-spec/spec-008-reservation-request.md` + 같은 폴더 006 ⑭ · 005 · 007 고침 6 · 000 ③
- **SPEC 뒤에 사용자가 바꾼 것(정본 · SPEC 보다 우선)** — `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation3/orchestration/work/day-reservation3/_RESUME.md` §2 의 11-26 뒷줄: ① 요청 고객 = 이름 필수 + 연락처 · SNS · 이메일 · 생년월일 중 하나 이상(생년월일 필수 아님) ② 같은 고객 판정 = 이름(대소문자 · 띄어쓰기 무시) ∧ 요청에 온 구분 값 하나라도 같음 ∧ 국적은 양쪽 있을 때만 ③ OQ-Q15 확정 스레드 다른 고객 `change` = 400 `customer_changed` ④ 문구 「답변 대기중」 · [철회] · [다시 시도] · [KOS 등록 실패](접음) ⑤ ext 키 배포 = 새 병원 키 ⑥ 실물: `reserve` 최상위 `counselor` 됨 → 생성 묶음에 W18 불필요
- 계약 `delivery-1-report.md` · backend 리포트 `be-1-report.md` · 실물 `be-probe-1-report.md`(모두 이 폴더) · 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation3/reference/2026-11-26-reservation-request/reservation-request-decisions.md` · 시안 v15 `design/20261126_예약현황_시연_v15.html`
- 문서 검수 리포트 `review-doc-1 ~ 4-report.md`(이 폴더) — 이중 예약 길(F1 · F2 · N1 · M1 · V1)이 코드에서도 막혔는지

## 2. 배경

링키가 ext 로 예약 요청 → 병원 스레드 → 버튼 한 번으로 DAY · KOS 반영. ext 키 병원당 하나로 바뀜. 코드 PR 전에 SPEC · 결정 · 실물 · 기존 코드 관례에 대조해 판정한다.

## 3. 계약

해당 없음.

## 4. 볼 것 (판정 축)

1. **이중 예약 · 상태 구멍**: 확인 대기 유지 · 접음 · 스레드 retry · 공용 retry 409 · 같이 누름 409(행 잠금) · `visit_id` = W3 확인 때 · 철회 · 자동 닫힘 · 생성 전 `change`/`cancel` — 코드 경로를 하나씩 따라가 표로
2. **ext 키 병원당 하나**: `git grep -n partner` 전수 — 남은 partner 의존 · 한도 · outbox 유일키 · migration 0031(중복 행 멈춤 · up/down) · 기존 ext 경로 회귀 · `_charty` 막음 없어짐
3. **ext E1 ~ E8**: 본문 검증(길이 · phone · 구분 값 하나 이상 · 1000자 · id 존재) · 오류 코드 · Idempotency-Key · `updated_since` · 버전 번호 · 판정(위 ②) · `customer_changed`
4. **KOS 쓰기**: `write_open` 새 조건(reserve `counselor` · W4 메모 · 유입 · W2 email) · 확인(expect) · 메모 합치기 형식 · 순서 묶음 · 담당자 = 누른 직원
5. **알림 · SSE**: 새 종류 앱 unread · 목록에서 빠짐 · 받는 사람 ADMIN · COORDINATOR · target · `announce_unread` · `day.js` 갈래
6. **화면**: 시안 v15 · U-5 버튼 규칙이 서버 상태 그대로 · 문구 = SPEC 임시 목록 + 사용자 문구만(지어낸 글자 0) · 인라인 스크립트 · 손 CSS 0
7. **권한 · 보안**: ext 키 · 병원 격리(다른 병원 스레드 접근) · 웹 권한 키 · 입력 이스케이프
8. **테스트**: 위 1 ~ 5 를 덮나 · 빠진 경우
9. **사용자가 실물에서 만날 자리**(막히진 않는데 이상해 보일 곳)를 따로 모아라

## 5. allowed_paths

- (read-only — 리포 파일 수정 금지. 산출물 = `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation3/orchestration/work/day-reservation3/review-code-1-report.md` 하나)

## 6. 리포트

맨 위 판정(PASS / WARN / FAIL) · FAIL n · WARN n 표(번호 · 파일:줄 · 무엇이 · 근거 · 고칠 방향 · 몫 BE/FE). 그 아래 축별 표 · 「실물에서 만날 자리」.

## 7. 하지 말 것

파일 수정 · 커밋 · stash · KOS 실제 호출 · 로컬 스택 · 사용자 포트. 테스트 실행은 필요한 파일만 1회.

## 8. 검증

```
각 지적에 파일:줄 + 근거(SPEC 절 · DEC D-번호). 판정 FAIL · WARN · PASS. 「조용히 통과하는 자리」를 따로 본다
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
  --to term_5c196973-a9ec-4982-81c2-655361f18aec --from term_6b6092c9-dd33-4818-875b-3704fbe81c82 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_5c196973-a9ec-4982-81c2-655361f18aec \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_5c196973-a9ec-4982-81c2-655361f18aec --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
