
# [backend] fix5 — 근거 카드에 company_product 유형 추가 (마지막 다듬기)

너는 WORK-023 의 **kknaks-dev `backend` 워커**다. 네가 fix4 에서 남긴 spec 환류 후보가 채택됐다 — spec **v0.0.9**: `source.type` 에 `company_product` 추가, **url 은 null**(공개 페이지 없음).

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/recruiter-chat`

## 수정
1. 소비자의 문서 계열 tool 집합에 `get_company_product` 추가 — tool_result 에서 `{type: "company_product", slug, title, url: null}` 로 sources 추출.
2. 테스트: company_product tool_result → 카드 추출(url null) · 목록 tool 은 여전히 카드 안 만듦.

## 검증
```
cd app/back && uv run pytest -q tests/
```

## 완료 보고 — 2채널, 핸들은 preamble 우선 (기존 fix 와 동일 형식, subject "backend fix5 완료")
orca send: --to term_53806a6d-ced5-4948-88bd-4181b7ba4323
