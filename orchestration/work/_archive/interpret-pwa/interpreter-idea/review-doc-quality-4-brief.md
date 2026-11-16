# [reviewer_doc] 통키 품질 개선 — SPEC 0.8.3 재검수 (0.8.2 검수 F-1 · W-1 ~ W-3 처분 확인)

너는 **interpret-pwa `reviewer_doc` 워커**다. 0.8.0 ~ 0.8.2 는 다른 리뷰어 터미널이 검수했다 — 맥락이 없으니 아래부터. **read-only** — 리포트 1개만.
작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토` · ⚠ PUBLIC

## 1. 읽을 것

- 앞 리포트: `orchestration/work/interpreter-idea/review-quality-doc-report-3.md`
- 수정 발주: `orchestration/work/interpreter-idea/quality-spec-fix3-brief.md` · planner 보고 `quality-spec-report.md` 끝 「0.8.3」 절(미결 2 — planner 가 읽은 자리 셋)
- 처분 §4 ~ §6 · DEC D-54

## 2. 볼 것

1. F-1 · W-1 ~ W-3 이 처분대로 닫혔나(`파일:줄`) · 개수(199 · 214 · 343 · F 뒤 zh-Hant 22,392 · ja · th 추정)를 다시 계산해 맞나
2. planner 미결 2 의 세 자리(yue ph-034 칸 · 옛 zh-Hant name 7개 근거 판정 · 「넘는다」 의 뜻)가 처분 · DEC 와 어긋나지 않나 — 어긋나면 코디 처분이 필요하다고 표시
3. WP23 이 backend 가 바로 짤 수 있게 닫혔나(입력 네 파일 · D-54 순서 · 멈춤 조건)
4. 새 어긋남 · 근거 없는 값 · public 0

## 3. 산출

- 리포트: `orchestration/work/interpreter-idea/review-quality-doc-report-4.md` — PASS / WARN / FAIL

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_d181fbae-29f2-43bb-9a41-6bc888ca07de --from term_93cf4aa2-57e5-430b-8fb4-89738c55defa \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_d181fbae-29f2-43bb-9a41-6bc888ca07de \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_d181fbae-29f2-43bb-9a41-6bc888ca07de --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
