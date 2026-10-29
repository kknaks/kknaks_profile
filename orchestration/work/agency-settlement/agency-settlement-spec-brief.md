# [planner] 월별 매출 리스트(`sales/`) — SPEC-007 · WORK-011 작성

너는 **cc-prototype `planner` 워커**다. **맥락이 하나도 없다고 가정하고** 아래를 먼저 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/roles/cc-prototype/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
- `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/AGENTS.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터` (코디 워크트리 — 아래 allowed_paths 만)
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/cc-prototype/10-decision/decision-009-monthly-sales-list.md` ← **결정의 SoT. 여기 없는 정책은 발명하지 마라**(정할 것은 OQ 로, 기본값과 함께)
- `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/_RESUME.md` §2 — 결정 원천(DEC-009 와 다르면 이쪽이 맞다)
- `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/research-agency-attribution.md` — 운영 KOS 조사(필드 경로 · 건수 · 결제/취소 모양). **필드 · 연결 근거는 여기서 인용**
- `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/reference/2026-10-12-cc-prototype/kos-demo-api.md` — KOS OpenAPI 작업표 · 인증 · 응답 모양
- 공식 스펙: `https://developers.kos-solution.com/openapi.yaml` (1.0.1 · 작업 77) — 작업별 요청/응답 필드는 여기서 확인
- 형식 본보기: `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/cc-prototype/20-spec/spec-006-customer-questionnaire-web.md` · `30-work/work-010-customer-questionnaire-web.md`

기대는 개념:
- `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/areas/concept/cs/no-inference-from-free-text.md` — 에이전시 · 상품은 구조화 필드로만. 자유 텍스트에서 추정하는 규칙을 SPEC 에 넣지 마라

## 2. 배경 / 무엇을 바꾸나

새 기능 폴더 `sales/`(코드 레포 `/Users/kknaks/git/toy_pr2/cc-prototype`) — **운영 명동점 KOS 결제를 월 단위로 조회해 품목 한 줄씩 보여 주는 페이지**. 병원 · 에이전시 수수료 정산의 첫 판이고, 이번 판은 **리스트만**이다(수수료 · 에이전시 필터 · 엑셀은 밖 — DEC-009 D-01). 디자인은 cc-prototype `procedure/front` 것을 복사해 쓴다(D-08).

산출물:
1. `20-spec/spec-007-monthly-sales-list.md` — 기능 계약: 화면(월 선택 · 수납별 묶음 · 품목 줄 · 칸 D-03 · 상태 · 빈 달 · 오류) · BE API(경로 · 요청 · 응답 shape · 오류) · KOS 원천 매핑(칸마다 어느 작업 · 어느 필드 · 조인 키) · 월 경계(KST) · 취소 · 환불 · 선불카드 · 상품명 빈 품목 · 조회 전용 가드 · env · 로컬 실행. 열린 것은 `§ OQ` 에 기본값과 함께
2. `30-work/work-011-monthly-sales-list.md` — WP 단위 작업 순서(BE → FE, 각 WP 의 완료 조건 · 시험). **마지막 WP 에 운영 KOS 실물 조회 1회(10월)로 리스트가 뜨는 것**을 완료 조건으로
3. `20-spec/README.md` · `30-work/README.md` 인덱스 줄 추가. DEC-009 frontmatter `links` 는 코디가 고친다(건드리지 마라)

## 3. 계약

해당 없음(이 문서가 계약을 만든다). BE↔FE 계약은 SPEC 안에 필드명 · shape 까지 적는다.

## 4. 먼저 읽을 핵심 파일 (코드 — 읽기만)

- `/Users/kknaks/git/toy_pr2/cc-prototype/README.md` — 기능 폴더 규칙(기능끼리 공유 · import 금지)
- `/Users/kknaks/git/toy_pr2/cc-prototype/procedure/back/app/kos/client.py` — KOS 호출 · 토큰 교환 방식(복사 대상)
- `/Users/kknaks/git/toy_pr2/cc-prototype/procedure/back/app/` 의 `api/` · `service` · `repository/` · `domain/` — 계층 모양
- `/Users/kknaks/git/toy_pr2/cc-prototype/procedure/front/tailwind.config.ts` · `app/globals.css` · `app/styles/` · `components/common/` — 디자인 토큰 · 공통 컴포넌트(`sales/front` 로 복사할 목록을 SPEC 에 적는다)
- `/Users/kknaks/git/ax-clinic-project/scripts/kos_collect.py` — 운영 키 이름 · 조회 전용 가드(허용 경로 + `/queries/` 만) 본보기. **키 값은 읽지도 적지도 마라**

## 5. allowed_paths — 이 밖은 건드리지 마라

- `para/projects/summer-star/cc-prototype/20-spec/`
- `para/projects/summer-star/cc-prototype/30-work/`
- `reference/2026-10-12-cc-prototype/workflow-v2.md`

## 6. 단계

1. SSOT · 핵심 파일을 읽는다
2. SPEC-007 을 쓴다. 칸마다 KOS 원천(작업 · 필드 경로)을 리포트 · 공식 스펙으로 근거를 단다
3. WORK-011 을 쓴다
4. 인덱스 갱신 · §8 검증

## 7. 범위 제약 — 하지 말 것

- 수수료율 · 에이전시별 필터 · 엑셀 · 배포를 계약에 넣지 마라(OQ 로 「다음 판」만 적는다)
- **이 레포는 public 이다.** 실제 고객 이름 · 실제 매출 금액 · 운영 키 · 테넌트 id 를 문서에 쓰지 마라. 예시는 가짜 값(`홍**`, `1,000,000`)으로. 에이전시 이름은 예시에 쓰지 말고 「(에이전시) 코드」처럼 쓴다
- KOS 쓰기(`/commands/`)를 계약에 넣지 마라
- 코드 레포 · allowed_paths 밖 파일 수정 금지. 커밋 · push · PR 금지

## 8. 검증

```
SPEC 의 모든 절이 DEC-009 · _RESUME §2 · 조사 리포트 · 공식 스펙 중 하나를 근거로 가리킨다. 근거 없는 정책 0 · 열린 것은 OQ 로.
링크 · 인덱스 갱신. public — 키 · 실명 · 실제 금액 0 (grep 으로 확인해 보고에 적는다)
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_d291ae3b-f96b-492e-8274-6c3e14da473f --from term_d3e67a5e-3ebf-4410-b129-6e9c3058b7f3 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_d291ae3b-f96b-492e-8274-6c3e14da473f \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_d291ae3b-f96b-492e-8274-6c3e14da473f --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
