# [backend] 허브 수정 1 지시서

**너는 앞 판의 맥락이 없다.** `phub-gold-jev-be-brief.md`(같은 폴더) 전체를 읽어라 — 역할 · SSOT · allowed_paths · 제약 · 검증 · §9 완료 보고 그대로. 워크트리 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`(앞 판 변경이 작업 트리에 있다 — 이어서 고친다).

## 읽을 것

`/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev/review-code-hub.md`(WARN 2 · NOTE 10) · `_RESUME.md` §2 맨 위 행(코디 결정 「허브 검수 뒤」)

## 할 것

- **W-1(코디 결정 = 리뷰 추천 (a) + (c))**: 상품 범위에서 제품 노드의 offer 조회 role = **자기 + 하위 제품**(물려받음 holder 의 상품을 그 제품 상품으로 내지 않음 — semantic-map §5 · gold-build `ans_offer` 와 같게). 응답 `counts` 에 `distinct_rows` 추가 · `total` 뜻은 그대로. 다른 대상(시술 · 케이스 · 계열)의 offer role 은 바꾸지 않는다 — 바뀌는 곳이 있으면 보고. 시험 추가(Q31 · Q34 꼴 — 제품 노드 상품 행이 그 제품 · 하위 제품의 것뿐).
- **W-2**: `.env.example` 의 빈 선택 값이 복사돼도 죽지 않게(빈 문자열 = 미설정으로 읽거나 예시에서 주석 처리 — 리뷰 첫 선택지).
- **NOTE**: 리뷰 「고칠 방향」 이 코드 몇 줄인 것만 고친다(MCP 타입 오류 문구 · site 빈 문자열 · GOLD_EXPECTED_HASH 미설정 경고 등). uv.lock 의 무관 패키지 버전 상승은 되돌릴 수 있으면 `mcp` 추가에 필요한 것만 남긴다. 나머지 NOTE 는 「안 고침 · 이유」 로 보고.
- 로컬 확인은 **18106** 에서 띄웠다 내린다(18105 는 코디 것 — 건드리지 마라). 끝나면 코디가 18105 를 재시작한다.

## 검증

be-brief §8 그대로 + W-1 전후 셈(제품 노드 offer 행 수 · distinct) 보고.
