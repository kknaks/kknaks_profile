# [writer] SPEC-009 수정 4 — 재검수 3 FAIL 반영 (0.2.1 → 0.2.2)
검수: 같은 폴더 `review-spec-009-r4.md` — FAIL · WARN 「고칠 것」 전부.
- silver 작업은 **이미 끝났다**: `silver-site-report.md`(silver-check PASS W5 · gold-check PASS W10 · gold_hash ece5d2be… · aux e0813c0a… · 근거 종류 바뀐 기존 입구 **26** = SITE-120 이름 1 + 이동 부위 기존 별칭 25). SPEC 의 수 · 사실은 이 리포트 실측으로 맞춘다.
- 코디 답(`silver-site-addendum2.md`)을 결정으로 반영하고 정할 것에서 내린다: A1 = 묶음 기준 사본 `archive/silver-before-clinic-a-20261119/` · A3 = 기준 사본에서 supplement + build_site_3tier 재현 대조 · G1 · G3 = 경로 고침 + 작업 사본 밖 변경 WARN · 근거 종류 섞임 받아들임. 고친 스크립트 줄은 silver 리포트 §6 을 인용.
- 변경 기록 0.2.2 · 끝나면 2채널 보고(subject 「writer 완료: SPEC-009 0.2.2」).

## 맥락
- 처음 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo/phub-consult-demo-write-brief.md`(범위는 이후 **부위만**으로 줄었다 — `orchestration/work/phub-consult-demo/spec-009-fix2-instructions.md` · fix3 도 읽어라). 대상 파일 `orchestration/work/phub-consult-demo/SPEC-009-hub-clinic-supplement.md` 하나.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_83f6c682-4ae8-481a-8d8a-15c54a8ffe4a \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 \
  --text "[worker_done] writer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[질문] writer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
