# [reviewer] 코드 검수 고침 확인 — F-1 · F-2 · W-1 ~ W-5 만

같은 터미널이면 앞 맥락 그대로. 같은 워크트리 미커밋 변경. **파일을 고치지 마라.**

## 읽을 것
- 네 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/review-code-1-report.md`
- 정한 것: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/_RESUME.md` §2 맨 위 행(F-2 = 두 조각 · W-1 = ⓚ y 매핑) · SPEC 커밋 `7d99a62e`(mediness#971 spec-006 Rule 15 ⓖ · ⓚ)
- 고침 지시: 같은 폴더 `be-fix-1-instructions.md` · `fe-fix-1-instructions.md` · `mobile-fix-1-instructions.md`

## 볼 것
1. F-1 · F-2 · W-1 ~ W-5 가 고쳐졌나(파일:줄) · 네 F-2 재현을 다시 돌려 겹침 0 · 웹 · 앱 그리기가 서버 두 조각과 같은 그림 · W-1 웹 = 앱 같은 식
2. 고침이 새로 깬 것(누르기 · 끌기 · 툴팁이 두 조각 카드에서 한 카드처럼 · 띠)
3. 검증 각 1회: `./scripts/test.sh --pure -q` · node 테스트(스크래치 `npm ci`) · `flutter analyze` · `flutter test`
그 밖은 다시 파지 마라. 남은 지적 없으면 PASS.

## allowed_paths
- 리포트 1개만: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/review-code-2-report.md`

## 하지 말 것
파일 수정 · 커밋 · push · KOS · dev / prod · 사용자 포트.

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
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_99b025fc-f3ef-403e-8162-509c41545e2e \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_99b025fc-f3ef-403e-8162-509c41545e2e --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
