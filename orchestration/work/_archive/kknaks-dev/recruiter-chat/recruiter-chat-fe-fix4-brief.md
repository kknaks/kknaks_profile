
# [frontend] fix4 — 근거 카드 company_product 유형 (마지막 다듬기)

너는 WORK-024 의 **kknaks-dev `frontend` 워커**다. spec **v0.0.9**: `source.type` 에 `company_product` 가 추가됐다(url null — 링크 없는 카드는 fix1 때 이미 처리했지).

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/recruiter-chat`

## 수정
1. `ChatSourceType`(lib/chat-types.ts)에 `"company_product"` 추가.
2. 근거 카드 태그 라벨: 다른 유형과 같은 관례로 표기(태그 텍스트가 "company_product" 그대로면 길다 — 카드 컴포넌트의 기존 라벨 처리 방식을 보고 `product` 또는 `회사 제품` 식으로 짧게. 기존 유형 표기와 일관되게 네가 정하고 보고에 남겨라).
3. mock 에도 한 장 추가(있는 관례대로).

## 검증
```
cd app/front && npx tsc --noEmit (만진 파일 0 에러). 검증은 1회만
```

## 완료 보고 — 2채널, 핸들은 preamble 우선 (기존 fix 와 동일 형식, subject "frontend fix4 완료")
orca send: --to term_53806a6d-ced5-4948-88bd-4181b7ba4323
