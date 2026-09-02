
# [planner] 마이크로 정리 — R4 잔여 경미 3건 (판정 뒤집힘 없음 · 이것만)

너는 **mediness `planner` 워커**다. WP-125 가 R4 PASS 났고 사용자 승인도 받았다. PR 전 마지막 정리다. **아래 3건만** 고친다.

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/meeting-room-workflow-spec` (네 미커밋 변경 위에서 계속)

기준 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/work/meeting-room-workflow/review-wp-report-r2.md` 의 「잔여 경미 3건」

## 고칠 것

1. **라벨 수치 재드리프트 4곳** — 부모 bullet 「아래 여섯」(실제 7) · SPEC-031 변경 노트 ⑭와 log spec-change 행의 「가산 6줄」(실제 7) · log wp-add 행 「동기화 분기 6종」(실제 8). 리뷰어 권고대로 **개수를 세는 표현 자체를 빼라** (예: 「아래 여섯」→「아래 전부」, 「가산 6줄」→「가산 bullet」, 「분기 6종」→「분기 전수」) — 다음 수정에서 또 낡지 않게.
2. **열린 목록 비대칭** — SPEC-151 §7.9.5 마지막 bullet·개정 노트 ⑤ 에도 SPEC-031 처럼 「모달 발로 만들어진 회의의 취소·변경 파급 축」이 열려 있음을 세게 하라 (한 구절씩).
3. **30-work.md Board/Coverage 파생 셀** — 파급 요약에 「자동 등록 회의 한정」 구절 추가.

## 하지 말 것

- 위 3건 외 어떤 개정도 금지. log PR 칸 «—» 유지.

## 검증

```
python3 scripts/lint-pipeline.py --strict → mediness 범위 ERROR 0. 1회만
```

## 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 값과 preamble 이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_ae5c9156-a854-48b7-8f65-528976906150 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "3건 각각 처리 내용 / lint 결과"

# (2) 직접 주입
orca terminal send --terminal term_ae5c9156-a854-48b7-8f65-528976906150 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_ae5c9156-a854-48b7-8f65-528976906150 --text "[질문] planner: <질문>" --enter`
