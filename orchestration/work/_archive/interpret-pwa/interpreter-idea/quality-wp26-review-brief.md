# [reviewer] WP23 · WP24 · WP26 코드 검수 — 시드 `.7` · `.8` · 한도 표 · 시술명 바로잡기 (D-53 ~ D-60 · SPEC 0.9.1)

너는 **interpret-pwa `reviewer` 워커**다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/roles/interpret-pwa/reviewer/` · 작업 워크트리 `/Users/kknaks/orca/workspaces/interpret-pwa/interpreter-idea` · **read-only** — 리포트 1개. 앞 맥락 없음(WP21 은 다른 리뷰어가 봤다 — `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/interpreter-idea/review-wp21-code-report.md`)

## 1. SSOT

- SPEC 0.9.1(코디 커밋 `b37783db`): §4.2 · §4.2.4 · §4.2.5 · §4.6(D-56 표) · **§5.12** · §5.9(`fixed` · `translation_before`) · §9.1 「바로잡기」 ① ~ ⑭
- DEC D-53 ~ D-60 · 처분 `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/interpreter-idea/quality-research-dispositions.md` §11 ~ §13
- backend 보고: `wp23-be-report.md` · `wp24-be-report.md` · `wp26-be-report.md`(수정 1 포함) — 같은 폴더
- 변경: `git -C /Users/kknaks/orca/workspaces/interpret-pwa/interpreter-idea diff 37aafa9` + 새 파일(`git status`)

## 2. 볼 것

1. **바로잡기가 좋은 번역을 망가뜨리지 않나** — 직접 함수에 넣어 시험: en · vi 한 → 외에서 ③ 이 안 도나 · 일상 낱말(later · face · lift 등)이 안 바뀌나 · 맞는 이름 · 별칭이 있으면 안 건드리나 · 다른 term 의 이름을 안 바꾸나 · 한 발화 여러 term · 외 → 한 같은 현지명 묶음(W-1) · 숫자 · 조사 · 띄어쓰기 경계
2. 자리: `final:true` 만 · 빈 원문이면 안 부름 · 자막 · TTS · 기록이 같은 글 · `fixed` 가 WS 로 안 샘 · `translation_before` 는 바뀐 발화에만
3. 시드 `.7` · `.8` — 변환 스크립트가 처분 · SPEC 대로(재실행 같은 바이트) · 검사 8 · 틀린 꼴 39 + §13 · D-60 · D-54 뺌 · 한도 표 D-56 값
4. `api/interpret.py` 한 줄 · `test_api_surface` 예외가 그 한 줄뿐인가
5. 조용히 통과하는 자리 · 관문 `cd back && uv run ruff check . && uv run pytest -q` 직접 1회
6. 실물에서 사용자가 만날 자리 한두 줄

## 3. 산출

- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/interpreter-idea/review-wp26-code-report.md` — PASS / WARN / FAIL · `파일:줄` + 근거

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_d181fbae-29f2-43bb-9a41-6bc888ca07de --from term_15cca63d-5a2d-4753-a247-cde1162df48f \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_d181fbae-29f2-43bb-9a41-6bc888ca07de \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_d181fbae-29f2-43bb-9a41-6bc888ca07de --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
