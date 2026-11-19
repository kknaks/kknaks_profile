# [researcher] KOS HAR 6개로 고객 · 결제 · 시술권 · 선불카드 ERD 초안의 미확인 4건 실물 확인

너는 **day `researcher` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/roles/day/researcher/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

코디네이터와 같은 워크트리다. 리포트 파일 1개 말고 아무 파일도 만들거나 고치지 마라(특히 `erd-draft.md`).

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/reference/2026-11-18-day-customer/erd-draft.md` ← 확인 대상인 ERD 초안 v0. 「받을 HAR」 1~4 · 「아직 응답 모양을 못 본 것」이 이번 질문이다. **고치지 말고 읽기만.**
- `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/reference/2026-11-18-day-customer/customer-erd.md` — 지금 prod 의 customer 연결 ERD
- `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/reference/2026-11-03-cc-day/erd/README.md` — 데이터 공통 규칙(외부 id 는 `external_ref` 에만 · 참조 + 스냅샷 · 소프트 딜리트)
- `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/reference/2026-11-03-cc-day/erd/04-1-menu.md` · `03-visit.md` · `05-task.md` — 메뉴 · 방문 · 작업 1차 설계

**기대는 개념**: 해당 없음. 기준은 「HAR 값 중 초안 ERD 에 담을 칸이 없는 것 0」이다. 칸이 없으면 「담을 칸 없음」으로 모아라.

## 2. 배경 / 무엇을 바꾸나

예약을 DAY 에서 하게 되면 DAY 가 고객 · 결제 데이터의 원천이 되고, DAY 테이블 값을 KOS 로 보낸다(사용자 11-18).
그래서 고객 · 메뉴 · 구매 · 시술권 · 선불카드 테이블 초안(`erd-draft.md`)을 사용자와 정했다.
정할 것은 다 닫혔다. 남은 것은 **KOS 실물 응답으로만 닫히는 4건**이다. 사용자가 데모 테넌트에서 그 동작을 하고 HAR 을 떠 줬다.
너는 HAR 을 읽고 사실만 보고한다. ERD 를 정하거나 고치지 않는다.

## 3. 계약

해당 없음.

## 4. 입력 — HAR (`/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/reference/2026-11-18-day-customer/har/`)

새로 받은 것(이번 대상):
- `다회권구매.har` — 다회권 구매
- `결제 취소.har` · `재결제.har` — 결제 취소 · 다시 결제
- `선불카드.har` · `선불카드 결제.har` — 선불카드 조회 · 선불카드로 결제
- `용량,수량변경.har` — 담은 항목의 용량 · 수량 변경

비교 기준(이미 본 것): `고객정보조회 .har` · `상품 수납.har` · `수납.har` · `고객상세.har`

HAR 은 JSON 이다. `python3 -I` 로 읽어라. 요청 경로(`/tenants/<id>/` 뒤) · 요청 body 키 · 응답 키 구조 · 상태값 · 개수 · 금액 · 상품/옵션/시술 이름만 뽑는다.

## 5. allowed_paths — 이 밖은 건드리지 마라

- 리포트 1개만 생성: `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/har-check-report.md`
- 그 밖은 전부 읽기만.

## 6. 할 일 — 질문별

각 질문마다 **관련 경로 전부**(요청 순서대로)와 응답 구조를 보고, 답 + 근거(HAR 파일 · 경로 · 키)를 적어라.

**Q1 다회권** (`다회권구매.har`)
- 옵션 `count` · 단위와 `get-ticket-bundles` 의 `ticketSets[].tickets[]` 행 수의 관계 — 10회권이면 티켓 10행인가, 아니면 1행 + 남은 횟수 칸인가.
- 티켓마다 가격이 어떻게 나뉘나(합 = 번들 가격? 나머지 처리).
- 티켓 상태값 목록 · 구매 직후 상태. `ticketConfiguration.round`(current · total)가 어디서 오나.

**Q2 취소 · 재결제** (`결제 취소.har` · `재결제.har`)
- 쓰는 명령 경로 전부. 취소가 구매 전체인지 항목 단위인지. `revokingItems` · `refundingItems` 에 언제 무엇이 들어가나.
- 취소 뒤 `purchase.status` · `process` 값 목록(INITIALIZED · ACCEPTED 말고 새 값 전부).
- 재결제가 같은 구매를 다시 여는지, 새 구매를 만드는지. 일정 `purchaseIds[]` 변화.
- `transactions[]` 한 건의 전체 키 구조(결제 수단 · 금액 · 승인 · 취소 표시).
- 취소된 구매의 시술권(티켓)이 어떻게 되나.

**Q3 선불카드** (`선불카드.har` · `선불카드 결제.har`)
- `get-prepaid-card-summaries` `data[]` 구조 · 선불카드 충전이 구매(구매 항목)로 남는지.
- 충전 · 사용 · 포인트 이력 조회 경로가 있나 — 있으면 구조.
- 선불카드로 결제할 때 `transactions[]` 에 어떻게 남나 · 잔액 응답(`get-visitor-prepaid-card-balance`) 변화.

**Q4 용량 · 수량 변경** (`용량,수량변경.har`)
- `change-pending-purchase-items-option-unit` 등 변경 명령의 요청 body 와 응답.
- 바뀐 용량 · 수량이 구매 항목 · 시술권 세트 · 티켓 중 어디에 남나. 원래 옵션 값(스냅샷)과 바뀐 값이 둘 다 남나.
- 가격이 같이 바뀌나(`priceV2` · `basePrice`).
- 참고 단서: `고객상세.har` 「[오픈] 올리디아 120 1CC」 번들의 세트가 「올리디아 120 4cc」.

**Q5 초안 ERD 대조**
- Q1~Q4 에서 나온 값 중 `erd-draft.md` 테이블에 **담을 칸이 없는 것** 목록(값 · 어느 테이블 후보).
- 초안과 **어긋나는 사실** 목록(예: 초안은 「상태는 purchase 에」인데 항목 상태가 따로 있다 등). 고칠 안은 「정할 것」으로만, 결정하지 마라.

## 7. 범위 제약 — 하지 말 것

- **개인정보 · 비밀값을 리포트에 옮기지 마라** — 고객 이름 · 연락처 · 생년월일 · 주민 · 외국인등록 · 여권번호 · 주소 · 메모 · 토큰 · 쿠키 · Authorization · 테넌트 id · 계정 이메일. 키 이름 · 타입 · 상태값 · 개수 · 메뉴 이름 · 금액만. id 는 「id(str)」로만.
- KOS 호출 금지(HAR 만 읽는다). 파일 수정 · 커밋 · push 금지. `erd-draft.md` 수정 금지.
- ERD 를 정하지 마라. 추천도 「정할 것」 안에서만.
- HAR 원본을 다른 곳으로 복사하지 마라.

## 8. 검증

```
질문마다 답 + 근거(파일:줄 · git ref · 문서 URL). 확인 못 한 것은 「확인 안 됨」. 결정하지 않고 「정할 것」으로 모은다
```

- 리포트 마지막에 `grep` 로 개인정보 점검 1회: 리포트에 전화번호 · 주민번호 꼴 · 이메일 · `Bearer` · 테넌트 id(24자리 hex) 가 0건인지. 결과를 리포트에 적는다.
- HAR 에 표본이 없어 못 닫은 질문은 「확인 안 됨 — 필요한 HAR: …」로.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_3d82d3ad-3bc3-4cdc-8cbd-0e98fbc89591 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_3d82d3ad-3bc3-4cdc-8cbd-0e98fbc89591 \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_3d82d3ad-3bc3-4cdc-8cbd-0e98fbc89591 --text "[질문] researcher: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
