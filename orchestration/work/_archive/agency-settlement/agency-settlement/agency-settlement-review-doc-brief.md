# [reviewer_doc] SPEC-007 · WORK-011 월별 매출 리스트 검수

너는 **cc-prototype `reviewer_doc` 워커**다. **맥락이 하나도 없다고 가정하고** 먼저 역할 문서를 읽어라:

- `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/roles/cc-prototype/reviewer/role.md` (+ 같은 폴더 `rules.md`) — 코드 리뷰어 역할 문서다. 이번엔 대상이 문서라는 점만 다르다(판정 · 근거 형식은 같다)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터` (코디 워크트리 — **read-only**, 리포트 1개만 만든다)
base 브랜치: `origin/main` → 최종 PR 대상 `main`

## 1. SSOT — 대조 기준

- `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/cc-prototype/10-decision/decision-009-monthly-sales-list.md` ← 결정의 SoT
- `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/_RESUME.md` §2 — 결정 원천(DEC-009 와 다르면 이쪽)
- `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/research-agency-attribution.md` — 운영 KOS 조사(필드 · 건수)
- 공식 스펙 `https://developers.kos-solution.com/openapi.yaml` — 작업 · 필드가 실제로 있는지

기대는 개념:
- `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/areas/concept/cs/no-inference-from-free-text.md` — 자유 텍스트 추정 규칙이 SPEC 에 있으면 FAIL

## 2. 배경

planner 가 운영 명동점 KOS 결제를 월 단위로 품목 한 줄씩 보여 주는 `sales/` 기능의 계약을 썼다. 이 계약대로 BE · FE 워커가 구현한다. 구현 전에 계약이 결정과 맞는지, KOS 에 없는 필드를 기대하지 않는지 본다.

## 3. 검수 대상

- `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/cc-prototype/20-spec/spec-007-monthly-sales-list.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/cc-prototype/30-work/work-011-monthly-sales-list.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/cc-prototype/20-spec/README.md` · `30-work/README.md` 인덱스 줄

## 4. 볼 것

1. **DEC-009 D-01~D-09 가 빠짐없이 · 바뀌지 않고** 계약에 들어갔나. 결정에 없는 정책이 OQ 밖에 들어갔나
2. **KOS 필드 실재** — SPEC §5 매핑의 작업 · 필드 경로 · 조인 키(`purchaseId`)가 공식 스펙에 있나. 특히 `findScheduleByPurchaseId` 응답의 이름 · 예약 시작, `lastUpdatedPaymentDateTimeUtc`, `visitorFunnelName`, `prepaidCardName` · `etceteraProductName`, 품목 통계 필터 필드
3. **돈이 맞나** — 취소 · 환불 · 선불카드 · 분할 결제 · 달 넘는 결제에서 한 품목이 두 번 세지거나 빠지는 길이 있나(리포트 Q5 · Q6 숫자와 대조)
4. **조회 전용 가드** — `/commands/` 로 가는 길이 계약에 없나
5. **public 레포** — 실제 고객 이름 · 에이전시 이름 · 실제 금액 · 키 · 테넌트 id 가 문서에 없나(grep)
6. **BE↔FE 계약**이 구현 가능할 만큼 필드명 · shape · 오류까지 닫혔나. WORK-011 WP 마다 완료 조건 · 시험이 있나
7. **사용자가 실물에서 만날 자리** — 막히진 않는데 화면에서 이상해 보일 곳을 따로 모은다

## 5. allowed_paths — 이 밖은 건드리지 마라

- `(read-only — 브리프가 지정한 리뷰 리포트 파일 1개만 생성)`

## 6. 단계

1. SSOT 와 검수 대상을 읽는다
2. §4 를 하나씩 본다. 지적마다 `파일:줄` + 근거(DEC 줄 · 리포트 절 · 스펙 스키마명)
3. 리포트를 쓴다: `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/review-spec-007-report.md` — 머리에 판정(PASS/WARN/FAIL) · 지적 목록(FAIL/WARN/NOTE) · §4-7 목록

## 7. 범위 제약 — 하지 말 것

- 검수 대상 · 어떤 레포 파일도 고치지 마라(리포트 1개만)
- 운영 KOS 를 호출하지 마라(공개 openapi.yaml 만)
- 커밋 · push · PR 금지

## 8. 검증

```
SPEC · WORK 를 DEC-009 에 대조. 각 지적에 파일:줄 + 근거. 판정 FAIL/WARN/PASS
```

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_d291ae3b-f96b-492e-8274-6c3e14da473f --from term_35713e41-9a3a-45b1-b65c-235452e0d6d5 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_d291ae3b-f96b-492e-8274-6c3e14da473f \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_d291ae3b-f96b-492e-8274-6c3e14da473f --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
