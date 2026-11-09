
# [planner] DAY 데이터 아키텍처 — 사용자와 확정한 테이블 설계를 mediness products/day 문서로 옮긴다

너는 **day `planner` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/roles/day/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**너는 앞 맥락이 없다.** 아래 「읽을 것」 순서대로 읽고 시작해라. 같은 워크트리에 다른 워커는 없다(리뷰어는 네가 끝난 뒤 직렬로 탄다).

`products/day/` 는 코디네이터가 `scripts/scaffold-product.sh day DAY DAY` 로 방금 스캐폴드했다(placeholder 상태 · 미커밋).

## 1. SSOT — 먼저 읽을 것

**원천 = 사용자와 2026-11-03 하루 동안 칸 단위로 확정한 테이블 설계.** 여기 없는 건 발명하지 마라. 열린 것은 열린 것으로 옮긴다.

- `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/README.md` ← 1차 범위 · 주제 순서 · **모든 테이블 공통 규칙** · 전체 관계도(mermaid). 가장 먼저.
- `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/01-hospital.md` — 브랜드 · 병원 · 외부 CRM 연결
- `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/02-customer.md` — 고객 · external_ref · 코드 테이블
- `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/03-visit.md` — 예약+방문(visit 한 테이블) · 희망 시술 · 상담 · 단계 이력 · 시술 개념 셋
- `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/04-staff.md` — 계정 · 직원 · 직무(=역할) · 권한 · 로그인(KOS sign-in) · 세션
- `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/04-1-menu.md` — 상품 · 시술 메뉴(**설계만 · 1차에서 만들지 않음**)
- `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/05-task.md` — 시술 현황(작업) · 의사 호출 · 마취 · 카드 순서 · 동작 기록 · 외부 쓰기 큐
- `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/06-room.md` — 구역 · 방 · 예약 그룹 · 방문이 잡은 예약 칸
- `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/07-misc.md` — 알림 · 접수 · 채팅(cc 직접 기능)
- `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/config/projects/day.json` 의 `data_rules` — 위 공통 규칙의 요약

이 폴더는 public 레포(kknaks_profile)에 커밋돼 있다. `har/` 는 gitignore — 읽지 마라(운영 데이터).

**기대는 개념** — 이 작업이 따를 판단 기준. 안 주면 워커가 매번 처음부터 정하고,
같은 결정이 작업마다 달라진다. 없으면 "해당 없음".

해당 없음 — 판단 기준은 위 원천 README 「모든 테이블에 공통」 표가 전부다.

## 2. 배경 / 무엇을 바꾸나

DAY 는 병원 직원용 CRM 이다. 기존 CENTURION_DAY(v0.1)는 아카이브하고 v2 를 처음부터 짓는다(코드 레포 `MediSolveAIDev/CENTURION_DAY` `v2-dev` — 이 작업에서는 읽지 않는다).
1차 범위: 데스크는 KOS(외부 CRM), 시술실 · 의국은 DAY 를 쓴다 — DAY 는 KOS 를 폴링해 사본을 두고, DAY 에서 고친 것은 KOS 에 먼저 쓴다.

데이터 설계는 사용자와 코디네이터가 주제 7개를 칸 단위로 검토(승인/반려)해 확정했고, 그 결과가 원천 폴더다.
이번 작업은 **그 결과를 mediness 문서 파이프라인 모양으로 옮기는 것**이다. 새로 설계하지 않는다.

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

해당 없음 — 이 SPEC 이 이후 BE · FE · 앱 워커의 계약이 된다.

## 4. 먼저 읽을 핵심 파일

- `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec/AGENTS.md` · `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec/rules/document-pipeline.md` — 문서 파이프라인 · frontmatter · 각 폴더에 무엇을 두고 무엇을 두지 않는지(특히 §「40-architecture 에 쓰지 않는 것」 — schema 전문 · 컬럼 전체 목록 금지)
- `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec/products/day/` — 스캐폴드(placeholder)
- `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec/products/selly/20-spec/spec-000-data-model.md` — 이 레포에서 **데이터 모델 SPEC** 을 쓰는 선례
- `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec/products/nexus/40-architecture/` — architecture(README · system · erd) 를 채운 선례
- `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec/templates/spec.md` · `templates/architecture-*.md` · `templates/product-readme.md` · `templates/decision.md`
- `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec/context/products.md` 의 DAY 행 — 제품 정의(읽기만)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `products/day/`

## 6. 구현 단계

1. **README.md** — 제품 지도. DAY 가 무엇인지 · 1차 범위(KOS = 데스크, DAY = 시술실 · 의국) · 원장 두 단계 · 관련 레포(코드 `CENTURION_DAY` `v2-dev` · 참고 cc-prototype · centurion) · 문서 진입점.
2. **20-spec/spec-000-data-model.md (DAY-SPEC-000)** — 데이터 모델 계약. 이 레포 관례상 컬럼 수준 계약은 SPEC 에 둔다(selly SPEC-000 선례).
   - §공통 규칙: 원천 README 「모든 테이블에 공통」 전부(DB · uuid · UTC · hospital_id · external_ref 한 테이블 · 원장 두 단계 · 동기화 · DAY 테이블이 더 크다 · 민감 정보 암호화 · 참조 + 스냅샷(1차 스냅샷만) · 생성/수정/삭제 시각 · 소프트 딜리트).
   - 주제별 절(01 ~ 07): 테이블마다 필드 · 타입 · 필수 · 설명 · 외부(KOS) 원본. 원천 문서의 표를 그대로 옮기고, 각 절에 원천 파일을 `sources` 로 단다.
   - 04-1 메뉴는 「1차 범위 밖 — 자체 운영 단계 설계」로 구분해 둔다.
   - 원천 문서의 「정할 것 · 확인할 것 · 논의 중」은 SPEC 의 OQ 로 옮긴다(결정하지 마라).
3. **20-spec.md** — 인덱스에 SPEC-000 한 줄(본문 미러 규칙대로).
4. **40-architecture/** — `README.md`(핵심 도메인 표 · 승격 기준) · `system.md`(KOS ↔ DAY 1차 구조 · 폴링 주기 · 쓰기 큐 · 원장 두 단계 · KOS 를 뗄 때 지우는 것: external_ref · external_session · external_outbox · crm_connection · emr/) · `erd.md`(원천 README 의 관계도 수준 — 테이블 · 관계 · 핵심 키만. **컬럼 전체 목록은 쓰지 마라 → SPEC-000 링크**).
   `domains/` 는 비워 둔다(승격 기준 미충족).
5. **10-decision.md** — 이 레포에서 DEC 는 escalation board 다. 원천의 「법적 검토 필요」(신분증 · 여권 사진 · 고객 문진 · 직원 채팅의 고객 정보 — 보관 기간 · 열람 기록)만 ESC 후보로 `## 미완료` 에 올린다. 그 밖의 결정은 SPEC 본문에 둔다.
6. **log.md** — 2026-11-03 한 줄(데이터 아키텍처 SPEC-000 초안).
7. 남은 placeholder(`<…>`)가 `products/day/` 안에 없게 한다. 쓰지 않는 스캐폴드 파일(30-work.md · 21-html · 21-screen 등)은 템플릿 상태로 두되 lint 를 통과하게.

## 7. 범위 제약 — 하지 말 것

- `products/day/` 밖 수정 금지 — `context/products.md` 라우팅 추가가 필요하면 보고에 적어라(코디가 판단).
- **설계를 바꾸지 마라.** 이름 · 타입 · 관계가 이상해 보여도 고치지 말고 보고의 「미결 · 주의점」에 적어라.
- 원천에 없는 테이블 · 칸 · 정책을 더하지 마라. 원천의 「보류」·「범위 밖」은 그대로 보류 · 범위 밖으로.
- KOS 키 · 토큰 · 테넌트 id · 실명을 문서에 넣지 마라.
- WP(30-work) · 코드 · migration 은 이번 작업이 아니다.
- 커밋 · push · PR 금지.

## 8. 검증

리포트를 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-report.md` 에 써라(역할 rules.md 의 리포트 형식). 원천 테이블 · 칸이 SPEC-000 에 빠짐없이 옮겨졌는지 **주제별 개수 대조표**를 리포트에 넣어라.

```
python3 scripts/lint-pipeline.py --strict → products/day/ 범위 ERROR 0 (타 제품 기존 WARN/ERROR 는 '무관'으로 분리 보고). 근거 없는 정책 0 · 열린 것은 열린 것으로
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
  --to term_70b6f193-86a2-4c1d-8965-4e2220cef9b3 --from term_8117e457-5427-4f0c-9dd5-6fc68f77f6f4 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: DAY SPEC-000 데이터 모델 · architecture" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_70b6f193-86a2-4c1d-8965-4e2220cef9b3 \
  --text "[worker_done] planner 완료 — DAY SPEC-000 · architecture. 상세는 인박스 · 리포트 work/day-data-architecture/planner-report.md"  --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_70b6f193-86a2-4c1d-8965-4e2220cef9b3 --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
