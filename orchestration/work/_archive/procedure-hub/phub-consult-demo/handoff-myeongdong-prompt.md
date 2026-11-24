procedure-hub 새 작업을 시작한다. 너는 메인 코디네이터다(Orca 오케스트레이션).

## 목표
**명동점 전용 상담 실장 봇**의 데이터 바닥 — 명동점이 실제로 파는 것(KOS 상품 · 옵션 · 회차 · 가격 · 이벤트가 · 진료 항목 · 약제 · 장비)을 받아 지금 허브 gold(시술 · 계열 · 제품 · 부위)와 매핑한다. 상담 화면은 이 결과를 읽어 「명동점에서 받을 수 있는 것」만 보여 준다(화면은 다른 세션 몫 — 아래 「옆 작업」).

## 먼저 읽어라
- 옆 작업(진행 중): `orchestration/work/phub-consult-demo/` — `_RESUME.md` · `research-start.md`(§Q2 상품 있음/없음 · U-21~30 질문) · `gui-feedback.md`(2 · 3차 = 시술 리스트 탭 · 카드 · 제품 모달 — 이 매핑을 읽을 쪽)
- 앞 조사(10-30 · 옛 silver 기준): `orchestration/work/_archive/procedure-hub/phub-recommend/kos-link-research.md`(+ `.json`) — KOS 카탈로그 구조(§1) · 연결 분류(§2) · **연결 층 모델 L1 표준 꼴 / L2 어댑터 / L3 clinic_link(§3) · 결정 묶음 K1~K8 · 사용자 판단 U1 · U2(열림)**
- 회고: `para/projects/company/procedure-hub/log/2026-10-30-gold-decisions.md:167-173`(「kos 는 일단 기록만」 · U1 · U2) · `log/2026-11-18-phub-gold-jev.md`
- 허브 호출 안내서: `para/projects/company/procedure-hub/gold-api-guide.md`

## 지금 상태(코디가 11-19 확인)
- KOS **공식 open API** 수집기가 이미 있다: `/Users/kknaks/git/ax-clinic-project/scripts/kos_query_catalog.py`(조회 전용 · 경로 화이트리스트 · 쓰기 차단) · `kos_collect.py` 등. 크롤링 아님.
- 명동점 스냅샷: `/Users/kknaks/git/ax-clinic-project/para/projects/clinic-myeongdong-ax/sources/internal-data/kos-raw/`(최신 2026-10-28 · 9 개) — 상품 129(이벤트 59 · 일반 70) · 옵션 454(회차 · 가격 · 이벤트가) · 진료 항목 316 · 시술 126 · 약제 50 · 장비 22 · 카테고리 16.
- **앞 매칭은 그대로 못 쓴다** — 11-16 재설계 전 옛 silver(단위 시술 162 · semantic.json 사전) 기준. 지금 gold 는 시술 138 · 제품 315(PRC · PRD · M 코드 · stg `api-stg-csp.medisolveai.com/procedure-hub/gold`).
- 허브 데이터 사실(옆 작업 실측): 제품 315 전부 설명 있음 · 원리는 시술 단위(제품은 케이스 → 시술 → MEC 로 닿음 295/315) · 방법은 제품 단위(직접 62 · 케이스 경유 88).
- 사용자가 **KOS 관련 문서**를 준다 — 받기 전에 새 꼴을 추측해 만들지 마라.

## 0. 세팅
1. new-work.sh 로 새 slug(제안 `phub-myeongdong-link` — 대상-내용 꼴)를 만든다. 레포는 조사 뒤 정한다 — 연결 층 자리(K1 추천 = 앱 · 허브는 병원 데이터로 안 바뀜)에 따라 clinic_chat(공개 레포!) · ax-clinic-project · 허브 중 어디가 되는지가 갈린다.
2. 로컬 PG docker `phub-medallion-pg`(127.0.0.1:18432 · 접속 값 `~/.config/phub/medallion-pg.env` 를 set -a 로만).
3. KOS 키는 ax-clinic-project 쪽 `.env`(값 찍지 말 것). 새 스냅샷 수집은 사용자 승인 뒤.

## 할 일(순서는 조사 뒤 추천)
1. 사용자 문서 받기 → 조사 워커: 앞 조사 §1 의 KOS 꼴이 지금도 같은가 · 문서와 다른 칸 · 새 스냅샷이 필요한가.
2. 지금 gold 기준 재매칭 — 표준 꼴(L1) · 연결 표(L3) 설계는 앞 조사 §3 · K1~K8 을 출발점으로 사용자와 닫는다(스펙 → WORK → 구현).
3. 결과물 = 상담 앱이 읽을 「명동점 판매 ↔ 허브 코드」 연결 + 조회 함수(시술 · 제품 코드 → 명동점 상품 · 옵션 · 최저가 · 이벤트).
4. 열린 사용자 판단: 앞 조사 U1(허브 보강 후보 — 명동점에만 있는 부위 · 제품 · 시술) · U2(판단 불가 28 · 굵음 14 확인 주체) · 옆 작업 U-21~30(상품 한 줄 단위 · 최저가 기준 · 이벤트 기간 · 공개 레포에 명동점 가격 · 허브 시장 참고 가격 `g_offer` 와 관계).

## 옆 작업과의 경계
- `phub-consult-demo`(다른 코디 세션)가 clinic_chat 상담 **화면**을 고친다(① 리스트 뺀 화면 → ③ 시술 리스트 탭 · 카드 · 제품 모달 + 그림). 이 작업은 **데이터 · 매핑 · 조회 함수까지** — 화면 템플릿(`clinic_chat/consult/templates` · `static`)은 건드리지 않는다.
- 같은 clinic_chat 레포를 쓰면 브랜치가 갈린다 — 조회 함수 꼴(입력 = PRC · PRD 코드 · 출력 칸)은 정해지는 대로 `phub-consult-demo/_RESUME.md` 에 포인터를 남겨 화면 쪽이 맞춰 쓰게 한다.

## 일하는 방식(지켜라)
- 문서 · 조사 · 검수 · 코드 워커 전부 opus. 단계 끝나면 묻지 말고 자동 검수. 발주 전에는 나에게 승인.
- 이름 매칭 규칙은 증상 패치 금지 — 입력 전수 표(KOS 이름 × 허브 사전) → 실패 층 → 설계 한 번 · 완료 = 표 통과율. 원천에 없는 정보를 추정해 채우지 않는다(그대로 / 가공 / 추정 구분 · 추정 금지).
- 시험은 WP 마다 그 WP 파일만 · 전체 pytest 금지.
- 공개 레포(clinic_chat · kknaks_profile)에 키 · 명동점 원자료 본문 · 가격을 올리는지는 나에게 먼저 묻는다.
- 허브 레포 · stg 는 이번 범위에서 읽기만(허브 보강은 U1 결정 뒤 별도).

먼저 0 세팅을 하고, 앞 조사 · 지금 gold · 수집기 상태에서 무엇이 있고 무엇이 없는지 조사 워커로 정리해 보고해라. KOS 문서는 내가 곧 준다.
