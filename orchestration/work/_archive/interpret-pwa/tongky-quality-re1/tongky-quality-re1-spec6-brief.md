# [planner] 마감 문서 — DEC D-71 닫기 · SPEC 0.9.6(context 고유명사만 · 실기기 결과) · WORK WP30 ~ 34 상태

너는 **interpret-pwa `planner` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/roles/interpret-pwa/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선` (코디 워크트리 그대로 · 미커밋 변경이 이미 있다 — 그 위에 쓴다)
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

## 1. 배경 — 이미 일어난 것(사실 · 다시 정하지 않는다)

- **코드 · 배포는 끝났다** — 문서가 뒤따라 맞춘다.
  - 0.9.5 세 참여자: 코드 #14 `c7a582f` · infra #57 · #58 · 배포 2026-11-16
  - D-71 context: 코드 #15 `56e43a0`(시드 `.11`) · infra #59(back 태그만) · 배포 2026-11-16 KST 19:19 · 되돌리기 = back 태그 `c7a582f`
- **사용자 결정(D-71 에 덧붙일 것)** — 2026-11-16:
  - 애매 35개(성분명 · 기술 약어 · 기법 별명 · 보톡스 · 원내 프로그램)도 **뺀다** → 고유명사 74개(`dict-classification.md` ①)
  - `translation_terms` = 74개의 **정방향 + 역방향만 · 별칭 짝 0**(사용자 「정 역 방향에 고유 명사만 넣으면 안 돼? 지금 너무 자세하게 쓰니까 충돌 나는 거지」)
  - `terms`(받아쓰기 힌트)도 **74개 ko 이름만**(사용자 「170개 하지 말고 74개만 해」)
  - 바로잡기는 170개 · 별칭 · wrong 그대로(context 만 줄임) · 시드 term 키 `proper`(bool · 선택)
- 실측 · 검수 근거:
  - `orchestration/work/tongky-quality-re1/wp33-context-report.md`(합성 144세션 · zh 울쎄라 18/18 · 리쥬란 힐러 0/6 → 6/6)
  - `review-wp33-code-report.md`(WARN · **「문서 고칠 자리」 D-1 ~ D-10 표 — 이번 SPEC 고칠 목록의 원천** · W-1 zh-Hant `雷射`)
  - `research-proper-noun-dict-report.md` · `research-translation-terms-report.md` · `dict-classification.md`
- **실기기 결과(수치만 · 문장 0)**
  - 0.9.5(WP32 · 15:53 zh · 11발화): 차례가 깔끔하게 번갈아 남 · 조각 0 · 차례 기다림 ≈ 1.0 ~ 1.05 s · 되울림 버림 0 · 자기 번역 0 · 사용자 「끼어들기는 훌륭한데 언어 품질이 문제」(직원 울쎄라 · 써마지 → 사전 이름 0회) → D-71
  - D-71 배포 뒤(19:20 ~ 19:37 · zh-Hant 1 · zh 3(하나는 연결 시간 초과로 0발화) · en 1 · ja 2 · 발화 69):
    - 울쎄라 사전 이름: zh 4/4 · en 2/2 · ja 3/3
    - 써마지: zh `超声刀` 4/4 ✗(바로잡기 못 잡음 · 열린 것) · en 2/2 · ja 받아쓰기 「서마지」(합성 AI 음성으로 사용자 판단 「어쩔 수 없지」)
    - 쥬베룩: zh · en · ja 맞음
    - 손님 `超声刀` → 「초음파(기)」 = 손님이 넓은 말을 한 것(사용자 확인 · 고칠 대상 아님 · 열린 것으로만)
    - 제모: 실기기 3/3 「제모」(합성 음성의 「제목」은 실기기에서 안 남)
- 요금: `reference/2026-11-12-interpreter-idea/price-v2.md`(연결 1회 실측 42.4원 → 14.55원 · agent text 별도 과금 $4/100만 · 청구액 3.5%) — SPEC 에는 넣지 않는다. DEC D-71 근거 칸에 한 줄만 써도 된다.

## 2. 할 일

A. **DEC**(`10-decision/decision-001-interpret-pwa.md`): D-71 을 닫는다 — 위 사용자 결정 · 시드 `.11` · 배포 · 실측(합성 · 실기기) 수치. 「열린 것」 에 새 OQ 둘: ① zh 써마지 → `超声刀`(실기기 4/4 · 바로잡기 못 잡음) ② zh-Hant `雷射` 역방향(리뷰 W-1 · 클라리티2 · 엑셀V 이름) — 처분 없이 열린 것으로. OQ-035 는 0.9.5 실기기 수치로 닫는다.
B. **SPEC 0.9.5 → 0.9.6**(`20-spec/spec-001-interpret-pwa.md` · `20-spec/README.md`):
   - 리뷰 「문서 고칠 자리」 D-1 ~ D-10 전부(§4.2 `proper` 키 · `.11` 판 · §4.5 재료 · 칸 표 · 역방향 중복 · §4.6 줄이기 순서 · 글자 수 표 등)
   - §9.1 앞 코드 리뷰 r2 몫(`_RESUME.md` §1 「SPEC 문장 맞출 자리」 — `review-wp30-31-code-r2-report.md` 참고): FAIL-1 시험 줄 · WARN-3 로그 줄 · WARN-4 세션 끝 줄 · WARN-1 「가짜 시계」 대신 상수 덮어쓰기
   - §9.6 「배포 뒤 확인 결과 (0.9.5)」 · 「(0.9.6)」 — 위 실기기 수치 · 판정 한 줄씩 · §9.5 배포 기록 표에 행(#14 · #57 · #58 / #15 · #59)
   - §10 OQ — 닫힘 · 새것 반영
C. **WORK**(`30-work/work-001-interpret-pwa.md` · `30-work/README.md`): WP30 · WP31 · WP32 상태 = done(실제 PR · 수치) · **WP33**(back context 고유명사만 · done · #15) · **WP34**(배포 · 실기기 · done · infra #59) 행 더함 · 그림 줄.
D. 머리말 · 근거 목록(SPEC `sources` · DEC 표 머리 요약 줄)에 D-71 · 새 리포트 이름.

## 3. 쓰는 법

- 기존 문체 그대로(짧은 문장 · 「·」 나열 · 근거 칸). 코드 · 시드 · 기록 문장을 문서에 옮기지 않는다(수치만 · 시드 term 이름은 이미 문서에 있는 수준까지).
- 결정하지 않는다 — 위에 없는 것은 「열린 것」 으로.

## 4. allowed_paths — 이 밖은 건드리지 마라

- `para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md`
- `para/projects/summer-star/interpret-pwa/20-spec/spec-001-interpret-pwa.md` · `20-spec/README.md`
- `para/projects/summer-star/interpret-pwa/30-work/work-001-interpret-pwa.md` · `30-work/README.md`

## 5. 범위 제약 — 하지 말 것

- 코드 · infra · reference/ · BASE · `orchestration/` 수정 금지. 커밋 금지.

## 8. 검증

```
리뷰 D-1 ~ D-10 · §9.1 네 자리 · OQ 반영을 한 표로(자리 → SPEC 줄). 버전 · 머리 요약 · README 버전 줄이 0.9.6 으로 맞음. 실기기 문장 0 · 키 0
```

- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_0cdc063d-4b42-4e5f-bc41-65528f81e60f --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_0cdc063d-4b42-4e5f-bc41-65528f81e60f \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_0cdc063d-4b42-4e5f-bc41-65528f81e60f --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
