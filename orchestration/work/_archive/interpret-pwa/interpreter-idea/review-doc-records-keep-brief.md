# [reviewer_doc] 통키 통역 기록 보관 기간 — SPEC 0.7.0 · WORK WP19 · WP20 문서 검수

너는 **interpret-pwa `reviewer_doc` 워커**다. 앞 맥락은 없다. **read-only** — 리포트 파일 1개만 만든다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/roles/interpret-pwa/reviewer/` (`role.md` 외)
작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토` (코디 워크트리 탑승 · 커밋 전 변경을 `git diff` 로 본다) · ⚠ PUBLIC 레포

## 1. 무엇을 검수하나

- 변경: `git diff -- para/projects/summer-star/interpret-pwa/` (DEC · SPEC · WORK · README 들)
- 기준(SoT): DEC-001 **D-42**(10-decision 98줄 근처) · D-41 · 발주 계약 = `orchestration/work/interpreter-idea/interpreter-idea-spec-brief.md` §3 표
- planner 보고 요지: §5.9 보관 기간 env 표 · §2.4 · §9.1 ⑦ ⑨ · §9.6 크기 근거 · 0.7.0 배포 뒤 확인 ①~⑤ · OQ-020 · WP19 · WP20
- **코디가 planner 뒤에 정한 것(워커 잘못 아님)**: §5.9 표 첫 행에 「공백만(앞뒤 공백을 지우고 판정)」 = 비어 있음과 같음을 더했다

## 2. 볼 것

1. D-42 · 브리프 §3 계약과 SPEC 이 한 글자씩 맞나(비었음 · N · 잘못된 값 · 기록 끔 · 운영 ConfigMap 안 넣음 · 로그 문구)
2. **SPEC 안에 0.6.x 「7일 고정」이 현행 규칙처럼 남은 자리**가 없나 — `grep -n "7일\|keep_days\|KEEP_DAYS\|D-41"` 로 전수. 이력(개정 이력 · 배포 기록 · 0.6.x 확인 결과)으로 남긴 것은 이력임이 드러나나
3. §9.1 시험 목록이 계약의 모든 갈래(비었음 · 공백만 · N=7 · 0 · 음수 · 숫자 아님 · 기록 끔 + 값)를 덮나 — backend 가 이것만 보고 시험을 쓸 수 있나
4. WORK WP19 · WP20 이 SPEC 절을 가리키고, 입력 · 산출 · 검증 명령 · 완료 조건이 WP16 · WP18 형식과 같나 · 11-18 기한이 들어 있나
5. 근거 없는 정책(계약 밖 기본값 · 용량 경보 · 압축 등) 0 · OQ-020 이 열린 것으로만 남았나
6. public — 키 · 계정값 · 실명 · 통역 기록 문장 0 (추가된 줄 grep)

## 3. 산출

- 리포트: `orchestration/work/interpreter-idea/review-records-keep-doc-report.md` — 판정 **PASS / WARN / FAIL** · 지적마다 `파일:줄` + 근거(D-번호 · 계약 행)
- 다른 파일 수정 금지

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_0065c22f-b4a3-475e-bf78-3b62bac38378 --from term_c8cb6789-42a2-4146-8929-841e431a054c \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_0065c22f-b4a3-475e-bf78-3b62bac38378 \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_0065c22f-b4a3-475e-bf78-3b62bac38378 --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
