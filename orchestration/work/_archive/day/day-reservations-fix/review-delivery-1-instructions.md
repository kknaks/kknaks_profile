# [reviewer_doc] Delivery 1 검수 — WP 나누기 · Issue #300 · #301 · #302

같은 터미널이면 앞 맥락 그대로. **파일 · Issue 를 고치지 마라.**

## 대상
- 보고: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/delivery-1-report.md`
- request · plan · apply json: 같은 폴더 `delivery/`
- Issue: `gh issue view 300 301 302 -R MediSolveAIDev/CENTURION_DAY`
- SPEC PR mediness#971(`ad317cf4` · `99085866`) · 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservations-fix-spec`
- 코드(읽기만): `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservations-fix`(origin/dev `65506f35`)
- 결정 표: 같은 폴더 `_RESUME.md` §2

## 볼 것
1. **범위 누락**: 결정 표 11-27 행 · SPEC 개정분(spec-006 ⑯ · 007 고침 8 · 000 ④ · 002 · 003)의 규칙이 세 Issue 중 어디엔가 다 들어갔나 — 표로. 특히 F1 ~ F6 · F4 6개월 · KOS 문진 읽기(내부 legacy) · Rule 15 ⓐ ~ ⓙ · 앱 표 · D44 · D45 · D46 ② · D47 · D49
2. **코드 표면 전수**: 고칠 곳을 Issue 가 목록으로만 줬다면 코드에서 직접 grep 해 빠진 입구(예: 상세를 그리는 모든 경로 origin · `reservation_layout` 을 쓰는 모든 곳 · `reservation_table.dart` · 웹 day.js 배치 계산 자리)를 찾아라
3. BE ↔ 웹/앱 계약 이름이 세 Issue 에서 한 글자씩 같나 · SPEC 절과 맞나 · 「칸 이름 = BE 가 정함」 같은 빈칸이 병렬 구현을 막는지
4. 완료 조건이 실물 e2e(로컬 · KOS 데모 지점) 로 검증 가능한가 · migration · 되돌리기
5. baseline = main `b9ac374e` + 계약 원천 줄 방식이 세 Issue 에 다 적혔나
6. 공개(open) KOS 새 호출 0 · 지어낸 화면 문구 0

## allowed_paths
- 리포트 1개만: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/review-delivery-1-report.md`

## 하지 말 것
파일 · Issue 수정 · 커밋 · push · KOS 호출 · dev / prod 접속 · 승인 receipt.

## 리포트 모양
맨 위 판정(PASS / WARN / FAIL) · 지적(Issue/파일:줄 · 근거 · 고칠 방향) → 범위 대조 표 → 코드 표면 grep 표.

## 7. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_99b025fc-f3ef-403e-8162-509c41545e2e --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_99b025fc-f3ef-403e-8162-509c41545e2e \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_99b025fc-f3ef-403e-8162-509c41545e2e --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
