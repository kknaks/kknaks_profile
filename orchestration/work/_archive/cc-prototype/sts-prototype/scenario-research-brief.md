# [researcher] 목데이터 시나리오 만들기 — 실데이터 10-09 대본 → 시드 + 이벤트 파일

너는 **cc-prototype `researcher` 워커**다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/roles/cc-prototype/researcher/role.md` (+ 같은 폴더)

## 1. SSOT
- **형식(계약)**: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/scenario-format.md` — backend 가 이 모양으로 읽는다. 바꾸지 마라
- 흐름: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/reference/2026-10-12-cc-prototype/workflow.md` — 「PoC 범위」 · 2~8단계
- SPEC-001 0.2.1 §0-a: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/para/projects/summer-star/cc-prototype/20-spec/spec-001-cc-poc.md`
- 실데이터: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/reference/2026-10-12-cc-prototype/2026-10-12T161224-5b4603da/raw/` · 직원 `/Users/kknaks/orca/workspaces/cc-prototype/sts-prototype/cc/back/data/kos-staff.json`
- 앞 조사(메모 양식 · 상담사 · 시간 순서): 같은 폴더 `research-patient-detail-report.md` · `research-counselor-trace-report.md`

## 2. 만들 것 — 시나리오 8개(고객 8명)

| # | 장면 | 대본 고르는 기준 |
|---|---|---|
| S1 | 대만 첫 방문 기본: 상담 → 결제 → 시술 3개 | TW · 시술 3~4개 · 상담/오더 메모 있음 |
| S2 | **재내원**: 지난 상담 기록 + **남은 시술권**(예: 10회 중 7회) → 접수 때 시술 선택 | 대본 1개 + `synthetic` 으로 과거 방문 · 시술권 만들기 |
| S3 | 홍콩 고객(광둥어 통역) | HK |
| S4 | 일본 고객 | JP |
| S5 | 수면 시술 고객 | 시술이 많고 리프팅류(수면 여부는 데이터에 없음 — 고르기만, 리포트에 표시) |
| S6 | 중간 귀가(상담만) | 시술 0 또는 상담만 |
| S7 | 시술마다 원장이 다름(보톡스 · 제모 등) | 그날 시술 작업의 `doctors` 가 2명 이상 |
| S8 | 한국 고객(통역 없음) | KR |

- 각 고객: seed.json 의 schedule 1개 + events/<scheduleId>.json. **예약 시각은 10-09 오전~오후로 흩어 놓기**(시연 순서대로 볼 수 있게)
- 대본의 실제 상담 메모 · 오더 메모 · 작업(시술 · 원장 상담) · 결제 품목 · 담당자 메모를 이벤트에 넣는다. 고객 · 동행인 이름만 가짜(D-09). 전화번호는 `010-****-****`
- `scheduleId` · `visitorId` 는 새로 만든 값(UUID)으로 — 실제 id 를 쓰지 마라. 대본 id 는 `scriptFrom` 에만

## 3. allowed_paths
- `/Users/kknaks/orca/workspaces/cc-prototype/sts-prototype/cc/back/data/scenario/` 아래 파일(만들기) — gitignore 폴더
- 리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/scenario-report.md`
- 그 밖 금지 · 커밋 금지 · KOS 호출 금지

## 4. 산출물 · 검증
리포트: 시나리오별 대본(scriptFrom) · 고른 이유 · 시술 수 · 결제 금액 · synthetic 으로 만든 것 목록 · 시연 순서 제안.
검증: `python3 -c` 로 JSON 파싱 · 형식 대조(필수 키) · 시나리오 8개 다 있음 · 실제 고객 이름 0(캡처 visitor.name · 메모 「이름 :」 값 대조) · 실제 scheduleId/visitorId 가 id 칸에 0

## 5. 완료 보고 — **문구 변경 금지**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --from term_92c69c69-0fb5-4f2c-99f6-c189d24e0955 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 요약 / 검증 결과 / 미결·주의점"

orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
