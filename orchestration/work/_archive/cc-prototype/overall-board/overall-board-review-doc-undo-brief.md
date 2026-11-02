# [reviewer_doc] SPEC-003 0.4.3 · 0.5.0 · SPEC-004 0.3.2 · WORK-006 검수

너는 **cc-prototype `reviewer_doc` 워커**다. **앞 판의 맥락이 없다.** 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/reviewer/role.md` (+ 같은 폴더 나머지). 작업 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc` — **read-only**, 산출물 1개.

## 기준
- 결정 정본 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/_RESUME.md` §2 — **2026-10-25 · 10-26 줄 전부**(취소선 = 뒤집힘)
- 코드(0.4.3 은 코드가 먼저 감 — 코드와 맞는지가 기준): `/Users/kknaks/orca/workspaces/cc-prototype/overall-board/procedure/` (커밋 9a317a2 · PR #6)
- 앞 검수 `review-doc-r3.md`(0.4.2 PASS) — 0.4.2 까지 PASS 난 곳은 다시 보지 마라

## 대상
- SPEC-003 0.4.2 → 0.4.3(`(r4)` · 부록 H) → 0.5.0(`(r5)` · §5.13 · §10.1 · 부록 I) — `git -C /Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc diff 2da68e7 -- para/` 가 0.5.0 변경, `git -C /Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc show 2da68e7 -- para/` 가 0.4.3 변경
- SPEC-004 0.3.2 · WORK-006 새 파일 · README

## 할 일 — 각 지적 `파일:줄` + 근거 + FAIL/WARN/PASS
1. 0.4.3: 10-25 결정(카드 방 type 무관 · 규칙 하나 · 「방 배정」 = 방 붙은 ETCETERA + 호출 이력 없음 · isRoomTask)이 코드와 같은가.
2. 0.5.0: 10-26 결정(되돌리기 · 아이콘 위치 · 웹 정본 · 앱 후속 · KOS 실호출 확인)이 빠짐없이 · 정확히 들어갔나. 기본값(부록 I.3)이 표시됐나. 근거 없는 정책.
3. 되돌리기 계약 완결성: API · 409 코드 · 스냅샷 두 필드 · KOS op(`complete:false` · flow-step 뒤로) · 대체 규칙(`superseded` · `statusNot`) · 동시성 · 귀가 대기 · 「방 배정」 · 토스트(마지막 조작만 · 5초) · 아이콘(아무 때나) · BE/FE 가 따로 구현 가능한가.
4. WORK-006: WP-KOS 맨 앞 · 게이트 · 완료 조건 · 검증 명령.
5. public: 실명 · 키 · KOS id 0.

## 산출
`/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/review-doc-r4.md` — 맨 위 종합 판정 · FAIL/WARN 수. 사용자 결정 필요한 것은 따로.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_ef44ce2a-44a4-42b6-9e71-309c0dbab728 --from term_94eec081-cd84-4084-9adb-6e5003afc9f2 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_ef44ce2a-44a4-42b6-9e71-309c0dbab728 \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_ef44ce2a-44a4-42b6-9e71-309c0dbab728 --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
