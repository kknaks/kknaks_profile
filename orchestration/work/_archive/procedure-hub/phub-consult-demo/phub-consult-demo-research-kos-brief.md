# [researcher] 명동점 KOS 상품 구조 받기 → JSON · 현황 · 허브 gold 1차 대조

너는 **procedure-hub `researcher` 워커**다. **앞 판의 맥락이 하나도 없다** — 아래만으로 일한다. 역할 문서(절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/roles/procedure-hub/researcher/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/상담봇` (코디와 공유 · 아래 allowed_paths 밖 생성 · 수정 0)

`P=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇` · `R=$P/reference/2026-11-19-myeongdong-kos` · `W=$P/orchestration/work/phub-consult-demo`

## 1. SSOT — 먼저 읽을 것

- **`$R/kos-product-json-guide.md` ← 받는 방법 · 출력 JSON 꼴의 정본. 여기 적힌 대로만 한다(§0 지킬 것 전부).**
- `$W/research-start.md` §Q2 ← 허브 쪽 상품 · 제품 사실(앞 조사)
- `$P/orchestration/work/_archive/procedure-hub/phub-recommend/kos-link-research.md` §0 · §2 ← 10-28 open API 스냅샷 기준 앞 매칭(옛 silver 기준 — **수는 비교용만**)
- 허브 호출 안내서 `$P/para/projects/company/procedure-hub/gold-api-guide.md`

## 2. 배경

목표는 **명동점 전용 상담 실장 봇**. 리스트 · 상세(제품 모달)에 「명동점에서 실제로 받을 수 있는 것」을 붙이려면 지금 명동점 판매 현황이 먼저 필요하다. 가이드(KOS 내부 API · 테스트 계정 · 조회만)로 실제 병원(명동점) 상품 구조를 한 번 받아 JSON 으로 남기고, 현황과 지금 허브 gold 와의 1차 대조를 낸다. **매칭 규칙 설계 · 연결 표 설계는 하지 않는다**(다음 단계).

## 3. 계약

출력 JSON 꼴 = 가이드 §4 그대로(이름 · 규칙 · null 규칙 · 정렬). 바꾸지 마라.

## 4. 실행 조건

- 계정: `set -a; . ~/.config/day/kos-test-account.env; set +a` 로만 싣는다(`KOS_TEST_EMAIL` · `KOS_TEST_PASSWORD`). **값 · 토큰 · 테넌트 id 를 화면 · 로그 · 파일 어디에도 찍지 마라.**
- 테넌트: `get-user-tenants` 의 `hospitalName` 으로 **명동점(실제 병원)** 을 고른다 — 데모 지점이 아닌 쪽. 이름이 헷갈리거나 둘 다 실제 병원처럼 보이면 **멈추고 코디에게 물어라**(§9 질문 방식 · 이름만 적고 id 는 적지 마라).
- 기기 5대 제한: 가이드 §2-4 대로 **UA 끝이 ` (product-json)` 인 세션만** 해제. 그 밖의 세션밖에 없으면 멈추고 묻는다. 끝나면 §2-5 로 내 세션 해제.
- 로그인 1번 · 호출 사이 0.3초 이상 · 부를 API = 가이드 §3 A ~ F 뿐(+ 로그인 · 테넌트 목록 · 세션 목록/해제). 고객 · 일정 · 구매 · 시술권 · 선불 잔액 · 처방 · 직원 API 0.
- 허브 gold: 로컬 PG(읽기 · SELECT) docker `phub-medallion-pg` 127.0.0.1:18432 — `set -a; . ~/.config/phub/medallion-pg.env; set +a` · 또는 stg GET `https://api-stg-csp.medisolveai.com/procedure-hub/gold/…`.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `$R/` 안: 수집 스크립트 1개(`fetch_kos_products.py` — 계정 · 토큰 · 테넌트 id 하드코딩 0 · env 로만) · 출력 `myeongdong-kos-products-<YYYYMMDD>.json`(**gitignore 됨 — 커밋 안 됨**) · 대조 결과 `match-gold-<YYYYMMDD>.json`(gitignore)
- 리포트 1개: `$W/research-kos.md` — **공개 레포에 들어간다.** 건수 · 이름 · 코드만. 가격 원값 · 토큰 · 테넌트 id · 사람 이름 0. 가격은 「옵션 n 개 중 가격 있음 n」 같은 셈만.
- 그 밖 생성 · 수정 0. 스크래치는 네 세션 scratchpad.

## 6. 할 일

1. **받기** — 가이드 §2 ~ §4 대로 → `$R/myeongdong-kos-products-<날짜>.json`. 가이드 §5 확인 넷(건수 일치 · single 인데 시술 항목 없는 옵션 수 · 개인정보 0 grep · 세션 해제)을 리포트에 그대로 적는다.
2. **명동점 현황** — 카테고리별 상품 수(이벤트 / 일반 · 닫힘 · 삭제) · 옵션(single / group · 회차 분포 · 수가 유형별 가격 있는 옵션 수 · visitorType 값 종류) · 시술 항목 · 시술(전체 vs 시술 항목이 가리키는 것) · 약품 · 기기 **이름 목록**(약품 · 기기는 전수 · 이름만). 10-28 스냅샷(앞 조사 §0 · 상품 129 · 옵션 454 · 시술 126 · 약제 50 · 장비 22)과 수 비교 — 출처가 달라(open API vs 내부 API) 생기는 차이와 실제 판매 변화를 섞지 말고, 구분 못 하면 「구분 안 됨」.
3. **허브 gold 1차 대조(셈만 · 규칙 설계 금지)**
   - 기기 · 약품 → gold 제품(`s_product` · `g_profile` product 행 · PRD): 정확 일치 / 공백 · 대소문자 · 괄호만 정규화하면 일치 / 안 맞음 — 셋으로 수 + 목록. 정규화 범위는 이 셋만(동의어 · 추정 금지).
   - 시술 항목의 시술(`procedure.name`) → gold 시술(PRC · `s_procedure.name_ko`) · 계열(M): 같은 세 칸.
   - 맞은 제품이 원리 그림(시술 경유 MEC) · 방법 그림(제품 MET)까지 닿는지 수(앞 조사 3-2 · 3차 피드백 경로: 제품 → 케이스 → 시술 → `mechanism_code` · `s_product_method`).
   - 결과 행 = `match-gold-<날짜>.json`(gitignore) · 리포트엔 수 + 안 맞은 이름 목록.
4. 「정할 것」 — 매칭 규칙 · 연결 표 · 데이터 자리 · 공개 범위로 넘길 것(결정 금지).

### 리포트 꼴
머리에 **한눈 표**(받음 건수 · 10-28 비교 · gold 대조 세 칸 수) → 1 ~ 4 → 「확인 안 됨」.

## 7. 범위 제약 — 하지 말 것

- 쓰기 명령 0(세션 해제 예외 · 내 표시 세션만). 가이드 밖 API 0.
- 커밋 · push 0. JSON 을 리포트에 붙이지 마라. 계정 · 토큰 · 테넌트 id 출력 0.
- 허브 · 앱 레포 수정 0 · 18222 앱 프로세스 · 사용자 포트 건드리지 않기.
- 매칭 규칙 · 표준 꼴 · 연결 표 설계 금지(셈과 사실만).
- 서브에이전트(Agent · Explore) 쓰지 마라.

## 8. 검증

```
질문마다 답 + 근거(응답 건수 · 표/칸 · 파일:줄). 확인 못 한 것은 「확인 안 됨」. 결정하지 않고 「정할 것」으로 모은다
```

- 끝에 `git -C $P status --short` 로 변경이 `$R/` 의 스크립트 · 가이드 · `$W/research-kos.md` 뿐이고 JSON 은 안 보이는지(ignore) 확인 · `grep -c` 로 리포트 · 스크립트에 이메일 · 토큰 꼴 0 확인.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다. preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_bd6dd2e2-2c92-45f8-8562-0bf709a0d90c \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[질문] researcher: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
