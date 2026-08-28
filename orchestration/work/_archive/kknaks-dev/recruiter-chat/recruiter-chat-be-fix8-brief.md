
# [backend] fix8 — tool 노출 판정에 공개 표면 조건(visible)을 합류 (실측 결함)

너는 WORK-023 의 **kknaks-dev `backend` 워커**다. owner 실사용에서 결함이 나왔다. spec **v0.0.14** §4 에 판정식이 명시됐다.

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/recruiter-chat`

## 증상 (실측)

`visible=false` 인 프로젝트(`kknaks-dev`)가 `chat_exposed=true` 만으로 `list_projects`/`get_project` 에 실렸고, AI 가 그 showcase 를 읽어 근거 카드를 냈는데 카드 링크(`/projects/kknaks-dev`)는 공개 페이지가 없어 **404**. DEC-027 D3 원칙(「공개 API 가 보여 주는 것 = tool 의 상한」) 위반 — 공개 표면에서 내린 항목이 chat 으로 샜다.

## 수정

1. **판정식 통일**: 모든 chat-tool 조회에서 「그 표면의 공개 조건 ∧ chat_exposed」. project 는 `visible=true` AND `chat_exposed` (목록·상세 둘 다). company_product 는 fix4 에서 이미 visible 을 본다 — 회귀 테스트로 잠가라.
2. **전 유형 감사**: career · problem · note · content · algorithm 각각에 공개 표면 조건(visible 류 컬럼 또는 공개 API 가 쓰는 필터)이 있는지 코드를 대조하고, 있는데 tool 판정에 빠진 것이 있으면 같은 방식으로 합류. 유형별 「공개 조건 = 무엇」 표를 보고에 남겨라(없으면 없음이라고).
3. **테스트**: visible=false ∧ chat_exposed=true 조합이 목록에서 빠지고 상세 404 — project 필수, 감사에서 걸린 유형 전부.

## 검증

```
cd app/back && uv run pytest -q tests/
```

## 완료 보고 — 2채널, 핸들은 preamble 우선 (subject "backend fix8 완료")
orca send: --to term_53806a6d-ced5-4948-88bd-4181b7ba4323
