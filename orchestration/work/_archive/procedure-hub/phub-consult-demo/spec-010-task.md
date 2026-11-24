# [spec] SPEC-010 명동점 상담 화면 0.5 — 디자인 시안 + 매핑 JSON v2 + 로컬 허브 (사용자 승인 11-20 「다음 단계로 진행」)

너는 procedure-hub 스펙 워커다. 앞 맥락 없음 — 이 문서와 가리킨 파일만으로. **문서 1 개만 쓴다**(코드 · 데이터 · 허브 · 앱 수정 0) · 커밋 0 · 서브에이전트 0 · 사용자 포트(18105 · 18222) 손대지 마라.

`P=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇` · `W=$P/orchestration/work/phub-consult-demo` · 앱 워크트리(읽기만) `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo`(0.4 · README · `clinic_chat/consult/*` · `prompts/consult.json` · tests) · 앞 스펙 `$P/orchestration/work/_archive/procedure-hub/phub-gold-jev/SPEC-004-consult-chat.md`(0.4 — 문체 · 절 구성 · 계약 꼴 기준)

## 목표(사용자)
**명동점 전용 상담 실장 봇.** 손님이 고민 · 부위 · 시술을 말하면 → 허브 케이스 → **맞는 명동점 진료항목**을 왼쪽에 KOS 시술별로 접고 펼쳐 보여 주고(얼굴 그림에 부위 점), 진료항목을 누르면 모달에 허브 의학 정보(개요 · 원리 · 방법 · 효과 · 부작용) + 병원 정보(제품 · 옵션 · 가격). 「담기」 로 오른쪽 장바구니 · 「최저가 추천(담은 시술 조합 기준)」. LLM 에는 의학 정보(허브) + 병원 정보(진료항목 · 옵션)를 같이 준다. 로컬에서 다 만든 뒤 허브 · 앱 한 번에 배포.

## 정본(이 순서로 우선 — 다시 묻지 마라)
1. **디자인 시안**(사용자 확정 · 정본): `$W/design-consult-20261120.html`(사용자 디자인 아티팩트 사본 · 큰 파일 — 필요한 줄만 읽어라). 화면 구성 · 문구 · 컴포넌트 · 클래스는 시안 그대로. **시안에 없는 화면 문구는 지어 넣지 않는다**(빈칸 + 「시안에 없음」 목록). 기존 0.4 화면은 두고 시안대로 안에 넣는다.
2. 화면 피드백: `$W/gui-feedback.md`(1 ~ 3 차 · 시안이 반영한 것은 시안 우선).
3. 데이터: `/Users/kknaks/git/clinic_chat/data/kos/myeongdong-mapping-20261120.json`(v2 · sha 8ca88c9a · git 무시 자리 — 앱 워크트리에도 같은 파일) — items 324(진료항목 · KOS 칸 · status · note · options[] 가격 · hub 케이스 매핑) · groups · sites 71(얼굴 32 = point / pair 비율 좌표 · viewBox 590×1060 · 몸 39 = list). 얼굴 그림 `$W/design-face-0.svg`. 데이터 결정 · 꼴: `$W/mapping-json-v2-report.md` · `$W/_RESUME.md` §2(11-19 ~ 11-20 행).
4. 허브(로컬 gold · 57b420ad · `http://127.0.0.1:18105/procedure-hub/gold` · 도구 resolve · scope · neighbors · facets · concern-candidates · pair · evidence · coverage · README `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-consult-demo/backend/README.md`) — 케이스 = 단위 시술 · 고민은 케이스에만(facets indication role 「자기」) · 효과 · 부작용은 시술 공통 물려받음 + 케이스 자기.

## 스펙에 담을 것(SPEC-004 꼴 · 번호 붙은 계약)
- 화면: 왼쪽(대화 서랍 · 얼굴 그림 + 부위 점 / 몸 = 그림 아래 「• 전신 · • 팔뚝」 점 목록 · 「감지된 시술 n종 · 진료항목 n개」 KOS 시술별 접기 · 진료항목 카드) · 가운데(채팅 · 원리 그림) · 오른쪽(담은 시술 · 최저가 추천 · 비우기 · 저장) · 모달(탭 · 칸 — 시안 칸 그대로 · 값 출처 칸별로 JSON / 허브 지정).
- **감지 → 진료항목** 규칙: 대화에서 고민 · 부위 · 시술을 허브로 풀고(resolve · concern-candidates 등) → 케이스 → JSON 의 `hub.case_codes` 로 진료항목. 입력 전수 표(말 꼴 × 데이터 조합: 고민만 / 부위만 / 시술만 / 고민 + 부위 / 제품 이름 / 진료항목 이름 / 없는 것) → 각 결과 · 빈 결과 화면.
- status 가 「시술 확인 필요」 · 「제품 확인 필요」 · 「허브 대상 아님」 · 「확인 필요: BBL 필터」 인 진료항목의 화면 처리(지어 넣지 않기).
- 옵션 · 가격: 카드 · 모달 · 장바구니 표시(원본 값) · **최저가 추천 규칙**(담은 진료항목들의 옵션 조합에서 무엇을 최저로 보나 — single / group(compositions) · 회차 · 이벤트 · closed · 옵션 없는 진료항목) — 정할 수 없는 것은 「사용자 결정 필요」 로 올림.
- LLM 컨텍스트: 진료항목 · 옵션 · 케이스 의학 정보를 어떻게 묶어 넘기나 · 답변 규칙(허브 근거만 · 가격은 JSON 값만 · 확인 필요 진료항목 말하기).
- 이미지: 원리 그림(허브 concept_image) 서빙 경로.
- 데이터 읽기(JSON 경로 env · 해시 확인 · 다시 읽기) · 앱 설정 · 시험(WP 별 관련 시험만 · 전체 pytest 금지) · 로컬 e2e 기준(18222 · 실물 허브 18105).
- WP 나누기(코드 워커가 순서대로 할 수 있게) · 각 WP 완료 조건.
- 「사용자 결정 필요」 목록(추천 하나씩 · 50 안쪽) · 「시안에 없음」 문구 목록.

## 산출
`$W/SPEC-010-consult-myeongdong.md`(0.1.0) 하나.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_d630855d-4002-4ea8-94ec-00c387f4b872 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "spec 완료: SPEC-010" --body "절 · WP · 사용자 결정 필요 수"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] spec 완료 — <한 줄>. 상세는 인박스." --enter
```
질문: `orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[질문] spec: <질문>" --enter`
