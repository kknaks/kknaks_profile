# [researcher] 상담사가 남긴 정보 추적 — KOS 캡처 전수

너는 **cc-prototype `researcher` 워커**다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/roles/cc-prototype/researcher/role.md` (+ 같은 폴더)
작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype` (코디 워크트리 — 리포트 1개 말고 아무것도 만들지 · 고치지 마라)

## 1. SSOT

- **실제 데이터**: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/reference/2026-10-12-cc-prototype/2026-10-12T161224-5b4603da/` (`manifest.json` · `raw/<API>/*.json` 전부)
- 흐름 정리 중인 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/reference/2026-10-12-cc-prototype/workflow.md` — 4단계(상담)까지
- 앞 조사: `orchestration/work/sts-prototype/research-patient-detail-report.md`(메모 다섯 종) · `kos-staff-api-report.md`(직원 22명 · roleTags — 상담사 = COUNSELOR)
- KOS 스펙(필드 뜻 확인용): `/Users/kknaks/git/ax-clinic-project/para/archive/inbox_archive/2026-09-18-kos-openapi.yaml`

## 2. 배경

상담은 앞으로 우리 차티(Charty) 프로그램으로 한다. 그 전에 **지금 KOS 에서 상담사가 무엇을 · 어디에 · 언제 남기는지**를 데이터로 알아야 관제가 무엇을 받아 보여 주고 차티가 무엇을 대신할지 정한다. **추정은 추정이라고 표시하고, 데이터에 있는 것만 사실로 적는다.**

## 3. 조사할 것

1. **상담사와 연결된 모든 칸** — 캡처의 모든 API 응답에서 상담사(COUNSELOR 태그 직원 id · 이름)가 등장하는 필드를 전수로: 경로 · 건수 · 그 칸의 뜻(스펙 설명). 예: `consultations[].counselors` · `consultation.counselor` · 통계 API 의 `counselorNames` · 결제(`getPurchase*`)의 담당 · 작업 담당 등. **빠짐없이 grep/전수 순회로**
2. **상담 기록 `consultations[]`** — 칸별 내용 실측: `content.text`(양식 · 길이) · **`consultationProcedures`(구조 · 무엇이 들어 있나 · 상품 옵션/시술/시술권 id 와 어떻게 이어지나)** · `consultationDoctors` · 시각(`consultationStartedDateTimeUtc` · `createdDateTimeUtc` · `updatedDateTimeUtc`)
3. **시간 순서** — 한 방문에서 접수 → 상담 시작 → 상담 기록 생성/수정 → 결제(결제 시각) → 시술권 생성 → 시술 작업 ready 의 순서를 시각 필드로 재보기. 「상담사가 결제 · 오더를 같이 하나」를 데이터로 볼 수 있는 만큼(담당 칸 · 시각)
4. **오더 메모 `orderMemo` 와의 관계** — 상담 기록 `content.text` 아래쪽 사본과의 일치(앞 조사 87/137), 오더 메모를 누가 쓰는지 데이터로 알 수 있는 칸이 있나(없으면 「데이터에 없음」)
5. **결제와 상담사** — 결제 · 결제 품목 데이터의 상담사 칸(`counselorNames` 등)이 그 방문의 상담사와 같은가, 상담 기록의 `consultationProcedures` 와 결제 품목이 얼마나 겹치나
6. **회차** — 같은 고객의 여러 방문에 상담 기록이 어떻게 쌓이나(캡처에 있는 만큼)

## 4. allowed_paths

- `(read-only — 브리프가 지정한 리포트 파일 1개만 생성)`

## 5. 산출물

`/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/research-counselor-trace-report.md`

```markdown
# 상담사가 남긴 정보 추적 (<날짜>)
## 결론 한 장 — 상담사가 남기는 것 목록(어디 · 무엇 · 언제) · 사실/추정 구분
## 1. 상담사와 연결된 모든 칸 (표: API · 경로 · 건수 · 뜻)
## 2. 상담 기록 consultations[] — consultationProcedures 구조 포함
## 3. 한 방문의 시간 순서 (예시 일정 2~3개 + 전체 통계)
## 4. 오더 메모와의 관계
## 5. 결제와 상담사
## 6. 회차
## 정할 것 — 관제 · 차티 경계 판단 재료(결정하지 말 것)
## 출처 목록
```

## 6. 범위 제약

- 고객 이름만 `<고객>` 으로 가린다. 직원 이름 · 메모 원문 · 시술명은 그대로 써도 된다. 메모 속 전화번호는 `<전화>`
- KOS API 호출 금지(캡처 · 스펙만). 데이터 복사 · 가공 파일 저장 금지(분석은 `python3 -c` 실행만). 커밋 금지
- 결정하지 마라 — 사실 · 추정 구분까지

## 7. 검증

```
조사할 것 1~6 전부 답(없으면 「데이터에 없음」). 1번은 전수 순회 방법을 적는다. 사실마다 파일 경로 · 필드 경로 · 건수. 리포트에 고객 이름 0건(캡처 visitor.name 전부와 대조해 확인)
```

## 8. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**

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

- 막히면 `orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --text "[질문] researcher: <질문>" --enter`
