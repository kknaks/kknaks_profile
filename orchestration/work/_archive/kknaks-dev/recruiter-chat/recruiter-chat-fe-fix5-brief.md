
# [frontend] fix5 — 근거 카드 클릭 = 채팅 안 모달로 md 렌더

너는 WORK-024 의 **kknaks-dev `frontend` 워커**다. owner 판정: 근거 카드는 페이지 이동 대신 **그 자리에서 모달로 근거 문서를 보여준다**(채팅 흐름 유지). spec **v0.0.10** U-5 개정.

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/recruiter-chat`

## 재료 (코디가 확인해 둔 것)

- `components/career/career-view.tsx` 에 **ProductModal + ShowcaseBody** 가 이미 있다 — showcase md 를 remark-gfm·mermaid·assetUrl 재작성까지 갖춰 그린다. career 페이지(스크린샷의 그 모달)가 이걸 쓴다.
- 데이터: `/api/career` 공개 번들(`api.career()`)에 제품 `body`(showcase 본문)가 실려 온다. **chat-tool API 를 쓰지 마라** — 그건 turn 토큰이 필요한 AI 전용이다.

## 수정

1. ProductModal/ShowcaseBody 계열을 **공용 컴포넌트로 추출**(career-view 와 chat 이 같이 쓴다 — 복사 금지, career 페이지 동작 무변경).
2. 근거 카드 클릭 → 유형별로 모달:
   - `company_product`: `api.career()` 번들에서 slug 매칭한 제품의 showcase 렌더.
   - `career` · `problem`: 같은 번들에서 해당 항목의 상세(career-view 가 그리던 내용) 렌더 — 카드 slug(`<company.slug>-<id>` / `problem-<id>`)를 번들 항목과 매칭하는 방법은 번들 구조를 조사해 정하고 보고에 남겨라. 매칭 실패 시 모달 대신 기존 url 이동 폴백.
   - `project` · `note`: 공개 상세 API 가 있으면 모달로 본문 렌더, 조사 결과 마땅치 않으면 기존 페이지 이동 유지 — 판단과 근거를 보고에.
3. url 이 있는 유형은 모달 하단에 「페이지에서 보기 →」 보조 링크.
4. 모달은 채팅 스크롤 계약(fix2)을 깨지 않는다 — 열려 있는 동안 스레드 스크롤 잠금 등은 career 모달 관례를 따른다.

## 검증

```
cd app/front && npx tsc --noEmit (만진 파일 0 에러). 검증은 1회만
```
+ mock dev 로 수동 확인: product 카드 → showcase 모달, 닫기, 보조 링크. career 페이지 회귀 없음(모달 그대로 동작).

## 완료 보고 — 2채널, 핸들은 preamble 우선 (subject "frontend fix5 완료")
orca send: --to term_53806a6d-ced5-4948-88bd-4181b7ba4323
