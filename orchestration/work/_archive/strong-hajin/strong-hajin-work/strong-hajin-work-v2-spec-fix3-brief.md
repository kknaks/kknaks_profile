# [writer] WORK002 직전 최소 정정 — 재조사 금지

## 1. 역할/근거
기존 strong-hajin-work-v2-spec-fix2-brief.md의 규칙·역할·원문·BE+FE 승인 유지. review-v2-spec-report.md 재검수2차 WARN8건만. 신규 정책·전수 조사 금지.

## 2. 필수정정
RW2-W1 DEC OQ203의 같은 complete 문구를 기존 completion-report 제출명령 검사로 정정.
RW2-W2 SPEC003 남은 spec001:443/460/498 줄번호 제거하고 절/인용으로 특정.
RW2-W5 UX에 담당변경 제안과 새담당 수락/거절을 부를 자리 명시, U9에도 명령 포함. 권한은 기존 API계약 그대로.

## 3. 동시 문구정정
RW2-W3 DEC에 01 OQ06 행을 넣어 기존계약 보존/화면자리 WORK에서 결정 연결.
RW2-W6 OQ202의 프론트 개편 때 표현을 이번 WORK002 화면설계로 갱신.
RW2-W7 SPEC002 상단 중복문장 제거.
RW2-W8 코디판단: 안내문 수정일 updated_at은 2026-09-17로 정렬 허용, 기존 W1 계약본문 버전은 유지(안내만 갱신). SPEC003은 patch버전 갱신.
RW2-W4 전면조사 없이 SPEC002 종류칩 실물과 비교하여 업무/참고 분류축 및 답장/원문확인 단추의 기존계약 유무를 기록. 기존계약 없으면 좁은 미설계+WORK002 선행확인 항목으로, 존재하지 않는 명령을 만들었다고 쓰지 않음. 사용자 질문 신설 금지, 기술결정은 WORK에서.

## 4. 범위
기존 SPEC003/DEC002/SPEC001/002 상단안내 및 updated_at만. BASE수정 불필요. WORK002는 아직 쓰지 말 것. 이 정정완료를 코디 확인한 뒤 바로 WORK002 발주하므로 전수검수 루프 확대 금지.

## 5. allowed_paths
para/projects/summer-star/strong-hajin/10-decision/decision-002-task-lifecycle-v2.md
para/projects/summer-star/strong-hajin/20-spec/spec-003-task-lifecycle-v2.md
para/projects/summer-star/strong-hajin/20-spec/spec-001-work-management.md (상단안내+updated_at만)
para/projects/summer-star/strong-hajin/20-spec/spec-002-action-item-review.md (상단안내+updated_at만)
orchestration/work/strong-hajin-work/v2-spec-fix3-report.md

## 6. 보고
8건 정정 자리와 인용문구, 변경 전후 짧게 보고. OQ203/206은 답대기 그대로. 최소정정 diff로 코디가 검증할 수 있게 작성.

## 7. 금지
코드/DB/테스트/빌드/원문/index/log/커밋/push/PR/stash/reset/checkout 없음.

## 8. 완료
문구정합만 검증. 실행0. 완료 후 쓰기 종료.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_29f98b02-b4b2-4735-8daa-81708cb3dfdc --from term_b9531982-afbb-4da8-b54c-122d11643219 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_29f98b02-b4b2-4735-8daa-81708cb3dfdc \
  --text "[worker_done] writer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_29f98b02-b4b2-4735-8daa-81708cb3dfdc --text "[질문] writer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
