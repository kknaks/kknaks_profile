# [planner] DAY-SPEC-000 개정 — KOS 키 전부 담는 테이블 보충

너는 **day `planner` 워커**다. **맥락이 없다고 가정하라.** 먼저 역할 문서를 읽어라(절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/roles/day/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-cc-mig-spec` (브랜치 `kknaksss/day-cc-mig-spec` · base `origin/main` = `ccede286`)
최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

## 1. SSOT — 먼저 읽을 것

- **사용자 결정**: `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/work/day-cc-mig/_RESUME.md` §2 결정 표 — 2026-11-20 행 전부. 특히:
  - **테이블은 KOS 가 주는 키를 전부 담는다**(이유: 지금 다 만들어 두면 나중에 기능 붙일 때 마이그레이션이 준다). 채우는 건 기존 KOS 동기화 회차 + 매퍼 — 화면 · 입력 기능은 만들지 않는다.
  - 병원 정보 · 기본 운영 시간 · 특별 휴무 · 예약 그룹 휴무는 KOS 값 그대로 DB 에(`S0:278` 「phone · address 두지 않음」 뒤집음). 병원 정보는 `hospital`(brand 1 → hospital N · 병원 = KOS 테넌트)에 붙인다.
  - 미래 일정은 미리 받지 않는다 — 날짜 · 고객 · 예약 단위로 요청 때 받아 저장(이번 스펙은 **칸 · 표만**, 받는 시점은 적어 두기만).
  - `created_at` ← KOS `createdDateTimeUtc`(연동 기간 원장 = KOS).
  - 통화는 KOS 와 같게 — 금액마다 통화.
  - 결제 수단 `CARD` 매핑 추가(`cardConfiguration` 포함). 앱 결제 · 간편결제 문자열은 모른다 — 지어내지 마라(열린 것으로).
  - 기본 휴무 = 운영 시간표 요일 `enabled:false`(따로 표 없음). 특별 휴무 · 예약 그룹 휴무는 KOS 웹에 입력 입구가 없어 키 미관찰 — cc 코드 근거 `{id, startDateTime, endDateTime}` 로 표를 두고 「첫 실값에서 확인」을 OQ 로.
  - 타이머 · 리액션(`taskTimers[]` · `reactions[]`)은 KOS 것을 안 쓴다 → 범위 밖.
  - 문진(`questionnaire_history` 동기화)은 이번 범위 밖(문진표 작업 때).
- **칸 후보의 정본 — 조사 리포트 3개**(키 · 모양 · DAY 대응 · 판정이 다 있다. 다시 조사하지 말고 이걸로 써라):
  - `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/work/day-cc-mig/research-kos-keys-report.md`(2차 — 특히 **K3-2 DB 확장 후보 테이블별** · K2 경로별 키 표 · K6)
  - `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/work/day-cc-mig/research-kos-keys-3-report.md`(3차 — N3 새 키 · N4 예약 · 병원 설정 · N7 갱신 집계 · N8)
  - `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/work/day-cc-mig/research-cc-ext-report.md`(1차 — ext 가 쓰는 칸 · B1)
- **데이터 규칙**: `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/config/projects/day.json` 의 `data_rules`(외부 id 는 `external_ref` 에만 · 동기화 칸은 `external_ref` 에만 · DAY 테이블엔 created_at · updated_at · deleted_at · 메뉴 참조 = id + 그때 값 스냅샷 · 시각 UTC timestamptz · 민감 개인정보 암호화 · 업체 칸 금지 · enum 은 DAY 말).
- **지금 코드(읽기만)**: `git -C /Users/kknaks/git/CENTURION_DAY show origin/dev:backend/day/models/<파일>` (dev = `844eace4`) · prod 는 `origin/prod`. **prod 에 있는 표 · 칸은 이름 · 타입을 바꾸지 않는다 — 새 표 · nullable 새 칸만**(customer-erd 때 규칙과 같음 · `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/work/_archive/day/customer-erd/customer-erd-spec-brief.md` §2).

기대는 개념: 해당 없음.

## 2. 배경 / 무엇을 바꾸나

DAY 는 cc-prototype 의 ext 외부 연동 API 를 옮겨 고도화한다(2단계). 그 전에 1단계로 **KOS 가 주는 키를 전부 담는 테이블을 먼저 만든다.** 조사 결과 KOS 응답 키 2,155개 중 DAY 에 칸이 없거나 미동기화 · 시점이 다른 것이 고유 632키다(3차 N7). 이번 일은 그것을 **SPEC-000 칸 계약**으로 옮기는 것이다.

## 3. 계약

해당 없음(문서 단계). 산출물 = SPEC-000 개정(+ 필요하면 `40-architecture/erd.md` 개략도 · `log.md`).

## 4. 먼저 읽을 핵심 파일 (이 워크트리)

- `products/day/20-spec/spec-000-data-model.md`(1,856줄 · 0.0.1 stable · last_updated 11-19) — §1 범위 · §2 공통 규칙 · §3 주제별 표 형식(묶음 · 필드 · 타입 · 필수 · 설명 · 외부(KOS)) · §6 OQ. **표 형식을 그대로 따른다.**
- `products/day/40-architecture/erd.md` · `products/day/log.md` · `products/day/10-decision.md`(DAY 는 구현 · 계약 결정을 SPEC 본문에 둔다 — DEC 엔티티 없음)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `products/day/` 중 `20-spec/spec-000-data-model.md` · `40-architecture/erd.md` · `log.md`

## 6. 할 일

1. **후보 전수 반영** — 2차 K3-2 + 3차 N7(N3 · N4 새 행 포함)의 DB 확장 후보를 테이블별로 SPEC-000 에 넣는다. 행마다: 칸 이름 · 타입 · nullable · 설명(**뜻 · 출처 시점 · 단위**) · 외부(KOS 키 경로). 판정별로:
   - `칸 있음 · 미동기화` → 칸은 그대로, 외부(KOS) 열에 원천 키를 적고 「동기화로 채움」.
   - `칸 없음` · `칸 없음(시점 다름)` → 새 칸 / 새 표. 시점이 다른 값은 **다른 칸**(예: 일정 단일 상담 정보의 상담사 · 원장 · 메모는 상담 기록과 다른 칸).
   - `일부러 안 둠` → 사용자 「다 저장」으로 **뒤집어 칸을 둔다.** 뒤집은 원래 줄(S0:278 · 311-317 · 360 · 510 · 611 · 892 · 1429 · 1668 · 1698 등)은 본문에서 고치고 변경 이력에 남긴다. 단 「계산으로 대체」는 칸을 두지 않는다(그대로).
   - 번역(`translsMap`)은 메뉴 표처럼 jsonb.
   - 범위 밖: `taskTimers[]` · `reactions[]` · 문진 · 결제 쓰기 · 화면.
2. **표마다 표시** — 「prod 에 있음(칸만 추가) / 새 표」. prod 모델을 직접 열어 확인(추측 금지).
3. **병원** — `hospital` 칸(P25 22키) · 새 표: 병원 기본 운영 시간(P26) · 병원 특별 휴무(P27) · 예약 그룹 휴무(K1-2 #30) · 예약 규칙(3차 #32 · #33 — 표로). 칸별 예약 수 · 예약 칸 · 칸 점유는 **표를 두지 않는다**(정원 + 점유로 계산 — S0:907 · 1002 그대로).
4. **민감 정보** — 주민 · 외국인등록 · 여권번호 등은 암호화 칸(data_rules).
5. **열린 것은 OQ 로** — 미관찰 키(3차 「여전히 확인 안 됨」) · 앱 결제 / 간편결제 문자열 · 특별 휴무 / 그룹 휴무 모양 · 빈 키 처리(3차 N8-13 — 코디 기본값 「단건 전체 응답에서 빠진 키 = 비움」) 등. **지어내지 말 것.**
6. 머리말 version 은 규칙대로(문서 개정 규칙을 role 문서에서 확인), 변경 이력 · `log.md` 에 한 줄.

## 7. 범위 제약 — 하지 말 것

- 코드 · 마이그레이션 · WORK 문서를 쓰지 마라(다음 단계).
- prod 칸 이름 · 타입 변경 금지. 조사 리포트에 없는 칸을 만들지 마라 — 리포트 밖 판단은 OQ.
- ext API 계약(엔드포인트 · 응답)은 이번에 쓰지 않는다(2단계).
- 커밋 · push · PR 하지 마라.

## 8. 검증

```
python3 scripts/lint-pipeline.py --strict → products/day/ 범위 ERROR 0 (타 제품 기존 WARN/ERROR 는 '무관'으로 분리 보고). 근거 없는 정책 0 · 열린 것은 열린 것으로
```

- **반영 대조표**를 완료 보고에 — 3차 N7 의 DB 확장 후보 고유 키 수(테이블별) vs SPEC-000 에 반영한 칸 수 · 뺀 것(사유: 범위 밖 · 계산으로 대체 · OQ). 빠진 키 0.
- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_9a3ce290-f594-459d-a6bc-89f3cf9dccc4 --from term_ec105a90-17de-4228-bf4d-18d2e4b1cef4 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: SPEC-000 테이블 보충 <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_9a3ce290-f594-459d-a6bc-89f3cf9dccc4 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_9a3ce290-f594-459d-a6bc-89f3cf9dccc4 --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
