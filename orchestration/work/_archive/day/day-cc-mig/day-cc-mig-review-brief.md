# [reviewer] #264 코드 검수 — 마이그레이션 0012 · KOS 키 매퍼 · 병원 단계 · kos_keys 업데이트

너는 **day `reviewer` 워커**다. **맥락이 없다고 가정하라.** 먼저 읽을 것:

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
- 코드 레포 `AGENTS.md`(이 워크트리)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-cc-mig` — **read-only.** backend 의 미커밋 변경(`git status` · `git diff` · 새 파일)이 검수 대상. base `origin/dev` = `844eace4`.

## 1. 기준

- 계약: SPEC-000 §4A — `/Users/kknaks/orca/workspaces/mediness-mediness/day-cc-mig-spec/products/day/20-spec/spec-000-data-model.md` (mediness #954)
- Delivery: `MediSolveAIDev/CENTURION_DAY#264` D-1 ~ D-5 · A1 ~ A7 · non_goals
- 사용자 결정: `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/work/day-cc-mig/_RESUME.md` §2(2026-11-20 행)
- backend 브리프 · 지시: `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/work/day-cc-mig/day-cc-mig-be-brief.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/work/day-cc-mig/be-fix-1-instructions.md`
- backend 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/work/day-cc-mig/be-1-report.md`(1차 + 「고침 1」)
- 앞 사례 검수(같은 꼴): `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/work/_archive/day/customer-erd/review-code-1-report.md` ~ `review-code-6-report.md`

## 2. 볼 것

1. **prod 무중단 · 더하기만** — 0012 가 지금 표 · 칸 이름 · 타입 · 제약을 바꾸는 곳 0. 새 칸 nullable. downgrade 가 지금 칸을 건드리지 않음. 0011 에 이어짐. enum 추가 방식이 PG 에서 안전한지(트랜잭션 안 `ADD VALUE` 등).
2. **SPEC 대조** — §4A 표별 칸 vs 모델 · 마이그레이션(빠진 칸 · 지어낸 칸 0). enum 값 · 매핑이 SPEC · 고침 1 지시와 같은지.
3. **기존 회차 격리** — 새 보충 · 병원 단계가 실패해도 지금 일정 10초 · 기준 정보 1시간 · 판매 회차(시술현황 판)가 그대로인지. 별 트랜잭션 · 예외 · 타임아웃 · 잠금. 지금 함수 동작 · 반환 · KOS 호출 수 변경(특히 `Refs.link` coalesce 한 줄 — 다른 뜻 변화 없는지).
4. **목록 밖 값 규칙** — 새 enum 칸: 행 유지 · 칸 null · 경고 1줄. CARD 매핑. `payment_type`(NOT NULL) 은 OQ-4A-1 대로 모르는 수단 = 그 거래 제외로 남은 것이 맞는지.
5. **data_rules** — 외부 id 는 `external_ref` 에만 · 동기화 칸 · 시각 UTC · 민감 정보 암호화(여권 · 주민 · 외국인등록) · 물리 DELETE 0 · 소프트 딜리트 · JSON 목록 금지.
6. **업데이트 경로(`runtime.backfill --stage kos_keys`)** — `--dry-run` DB 쓰기 0 · `--resume` · KOS 1초 1회 · 자기 세션만 해제 · 멱등 · dev 서버에서 돌려도 안전한지(호출량 · 잠금 · 지금 회차와 동시 실행).
7. **조용히 통과하는 자리** — 예외를 삼켜 데이터가 비어도 아무도 모르는 곳 · 경고가 로그 폭주(매 회차 반복)하는 곳 · 테스트가 실제 DB 아닌 가짜로만 확인하는 곳.
8. 테스트 · ruff · mypy 를 **직접 한 번** 돌려 수치 확인(바꾼 테스트 파일 + migrations · emr 관련 · 로컬 compose 만 · 사용자 포트 금지).

## 3. 계약

해당 없음.

## 5. allowed_paths

- `(read-only — 리포 파일 수정 금지. 산출물은 브리프가 지정한 리포트 파일 1개뿐)`
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/work/day-cc-mig/review-code-1-report.md`

## 7. 하지 말 것

- 파일 수정 · 커밋 금지. KOS · dev/prod 서버 · 공유 DB 접속 금지(DEMO 실물은 backend 리포트로 본다).

## 8. 검증

```
각 지적에 파일:줄 + 근거(SPEC 절 · DEC D-번호). 판정 FAIL · WARN · PASS. 「조용히 통과하는 자리」를 따로 본다
```

- 리포트 머리: 판정 · FAIL 수 · WARN 수 · 2절 항목별 결과.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_9a3ce290-f594-459d-a6bc-89f3cf9dccc4 --from term_eb269d60-3506-49e8-a774-8c76121da6dd \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: #264 코드 검수 <판정>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_9a3ce290-f594-459d-a6bc-89f3cf9dccc4 \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_9a3ce290-f594-459d-a6bc-89f3cf9dccc4 --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
