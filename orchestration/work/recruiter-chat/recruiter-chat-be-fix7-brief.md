
# [backend] fix7 — company_product 근거 카드 url 을 /career 로 (원라이너)

너는 WORK-023 의 **kknaks-dev `backend` 워커**다. owner 피드백: product 카드가 화살표까지 있는데 안 눌린다. spec v0.0.9 §4 Data Contract 가 개정됐다 — `company_product` 의 url 은 **`/career`**(제품이 속한 회사 경력 표면. fix5 의 None 결정을 owner 가 뒤집음).

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/recruiter-chat`

## 수정
1. `public_url(company_product)` → `"/career"`. fix5 때 남긴 「왜 None 인가」 주석을 「왜 /career 인가(owner 판정 — 눌리는 카드가 우선, 제품의 회사 이력이 있는 표면)」로 교체.
2. 테스트 갱신: url null 단언 → `/career`.

## 검증
```
cd app/back && uv run pytest -q tests/
```

## 완료 보고 — 2채널, 핸들은 preamble 우선 (subject "backend fix7 완료")
orca send: --to term_53806a6d-ced5-4948-88bd-4181b7ba4323
