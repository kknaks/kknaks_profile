
# [backend] fix3 — 회사 제품 showcase.md 를 공개 문서 루트에 넣는다

너는 WORK-023 의 **kknaks-dev `backend` 워커**다. owner 판정이다. 이것만 고친다.

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/recruiter-chat`
spec **v0.0.7** §4 「공개 문서 루트」가 신설됐다:
`/Users/kknaks/orca/workspaces/kknaks_profile/agent/para/projects/summer-star/kknaks-dev/20-spec/spec-017-recruiter-chat.md`

## 배경 (owner 실사용 피드백)

「회사 프로젝트는 안 했니?」에 AI 가 「내부 상세는 공개하지 않는다」로 과하게 사렸다.
원인: `core/chat_detail.py` 의 허용 루트에서 `para/projects/company/` 가 통째로 빠져
있어, **회사 제품의 showcase.md** 를 `get_project` 가 404 로 받는다. 그런데 showcase.md
는 사이트 projects 카드가 이미 가리키는 **공개 자료**다 — chat 만 못 읽을 이유가 없다.

## 수정 (spec v0.0.7 계약)

1. `core/chat_detail.py` 허용 루트에 **company 제품의 `showcase.md` 한 파일만** 추가.
   `para/projects/company/<제품>/showcase.md` 는 통과, 같은 제품의 `log/`(작업 회고) ·
   `README.md` · 그 외 어떤 파일도 여전히 404. summer-star 쪽 기존 규칙은 무변경.
2. 판정 축은 그대로다 — 제품 행의 `chat_exposed` 옵트인 + 이 경로 가드. 새 축을 만들지 마라.
3. 테스트: company showcase 통과 · 같은 디렉토리의 showcase 아닌 파일(log/·README) 404 ·
   `..` 이탈 여전히 404.

## 검증

```
cd app/back && uv run pytest -q tests/
```

## 완료 보고 — 2채널, 핸들은 preamble 우선

```bash
orca orchestration send --to term_53806a6d-ced5-4948-88bd-4181b7ba4323 --from <네 워커handle> \
  --type worker_done --task-id <preamble taskId> --dispatch-id <preamble dispatchId> \
  --subject "backend fix3 완료: <한 줄>" --body "수정 요약 / 테스트 수치"
orca terminal send --terminal term_53806a6d-ced5-4948-88bd-4181b7ba4323 \
  --text "[worker_done] backend fix3 완료 — <한 줄>. 상세는 인박스." --enter
```
