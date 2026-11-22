# [reviewer_doc] DAY-SPEC-000 §4A 「KOS 키 보충」 검수

너는 **day `reviewer_doc` 워커**다. **맥락이 없다고 가정하라.** 먼저 역할 문서를 읽어라:

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-cc-mig-spec` — **read-only.** planner 가 남긴 미커밋 변경(`git diff` — spec-000 +598/-32 · erd.md · log.md)이 검수 대상이다. 파일을 고치지 마라.

## 1. 기준

- 사용자 결정: `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/work/day-cc-mig/_RESUME.md` §2 결정 표의 2026-11-20 행 전부(특히 「테이블은 KOS 키 전부 · 기능은 ext 만」 · 병원 정보 · 휴무 · created_at ← KOS · 통화 · CARD · 범위 밖 목록).
- 칸 후보 정본: `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/work/day-cc-mig/research-kos-keys-report.md`(2차 K3-2 · K2) · `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/work/day-cc-mig/research-kos-keys-3-report.md`(3차 N3 · N4 · N7).
- planner 브리프: `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/work/day-cc-mig/day-cc-mig-spec-brief.md` §6 · §7.
- 데이터 규칙: `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/config/projects/day.json` `data_rules`.
- prod 모델: `git -C /Users/kknaks/git/CENTURION_DAY show origin/prod:backend/day/models/<파일>` · dev: `origin/dev`.

## 2. 볼 것

1. **반영 누락 0** — 3차 N7 고유 632키 vs §4A.10 대조표. planner 가 뺀 2키 · 16행 · 1키(사유: OQ-4A-4 · 5 · 6 · zoneIds)가 정당한지. 표본 추출이 아니라 테이블별 수 대조 + 무작위 20키 역추적(리포트 키 → SPEC 칸).
2. **prod 불변** — prod 에 있는 표 · 칸의 이름 · 타입이 바뀐 곳 0. 새 칸은 nullable. 「prod 있음 / dev 에만 / 새 표」 표시가 실제 모델과 맞는지(직접 열어 확인).
3. **data_rules 위반** — 외부 id · 동기화 칸이 `external_ref` 밖에 있는지 · 업체(KOS) 칸이 핵심 테이블에 있는지 · enum 이 KOS 문자열 그대로인지 · 시각 UTC · 민감 정보 암호화 표시 · JSON 목록 금지 규칙.
4. **시점 구분** — 「칸 없음(시점 다름)」 키가 같은 칸에 섞이지 않았는지(일정 단일 상담 정보 vs 상담 기록 · 산 시점 스냅샷 vs 지금 메뉴).
5. **planner 가 리뷰를 청한 판단** — ① `visit.reservation_group_id` 를 사본으로 둔 것(06 「두지 않음」 뒤집음 · OQ-4A-7) ② 병원 KOS 테넌트 정보를 `crm_connection.tenant_info` 에 둔 것이 사용자 결정 「병원 정보는 `hospital` 에 붙인다」와 맞는지 ③ `medicine_machine_ref`(owner_type + owner_id) ④ 뒤집은 원래 줄(S0:278 · 311-317 · 360 · 510 · 611 · 892 · 1668 · 1698)이 본문 · 변경 이력에 일관되게 고쳐졌는지.
6. **지어낸 것** — 리포트에 없는 칸 · 값 · enum 문자열(특히 앱 결제 · 간편결제) 0.
7. **범위 밖 침범** — 타이머 · 리액션 · 문진 · 수납 · 예약 칸/점유 표 · ext 계약 · 코드가 들어가 있지 않은지.

## 3. 계약

해당 없음.

## 5. allowed_paths

- `(read-only — 리포 파일 수정·생성 금지. 산출물은 브리프가 지정한 리뷰 리포트 파일 1개뿐)`
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/work/day-cc-mig/review-spec-000-4a-report.md`

## 7. 하지 말 것

- 파일 수정 · 커밋 금지. 새 설계 제안은 지적의 「고칠 방향」 한 줄까지만.
- 서버 · KOS 실호출 금지.

## 8. 검증

```
SPEC·WORK 를 DEC·baseline 에 대조. lint-pipeline --strict 로 products/day/ ERROR 0. 각 지적에 파일:줄 + 근거. 판정 FAIL/WARN/PASS
```

- 리포트 머리: 판정 · FAIL 수 · WARN 수 · 2절 항목별 결과.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_9a3ce290-f594-459d-a6bc-89f3cf9dccc4 --from term_7db2ce1e-b152-4bfc-9263-4ee84d622668 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: SPEC-000 §4A 검수 <판정>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_9a3ce290-f594-459d-a6bc-89f3cf9dccc4 \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_9a3ce290-f594-459d-a6bc-89f3cf9dccc4 --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
