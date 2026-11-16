# [researcher] 병원 상품(KOS 명동점) ↔ 실버 연결 조사 (read-only)

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 작업 폴더 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/`.
**읽기만**. 산출 `kos-link-research.json` · `kos-link-research.md`.

## 왜(사용자 10-30)
상담 앱: 채팅하면서 왼쪽 얼굴 지도 패널에 그 부위 추천 시술 · 설명 · **이 병원이 파는 상품**이 뜨는 구조(디자인 참고 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-30-chatry-sample/` — S3p-Scenario 11단계). 추천은 허브(실버 · 시맨틱 · 골드)가, 판매 상품은 병원 KOS 가 가진다. **KOS 데이터는 실버와 구조 · 범위가 다르다(실버가 훨씬 넓다 — 사용자)** — 억지로 1:1 로 맞추지 말고 어떻게 다른지 그대로 센다.

## 입력
- KOS 수집 방법 · 환경: `/Users/kknaks/git/ax-clinic-project/scripts/` (kos_collect.py · kos_collect_extra.py · kos_auth_check.py · kos_silver.py · kos_query_catalog.py · kos_flow/ …) — 어떤 API · 어떤 칸 · 인증 방식만 읽어 정리. **API 호출 · 새 수집 금지**(이미 받은 raw 로만). **키 · 토큰 값 출력 · 기록 금지**
- raw(명동점 2026-10-28): `/Users/kknaks/git/ax-clinic-project/para/projects/clinic-myeongdong-ax/sources/internal-data/kos-raw/2026-10-28T172138-b5a14ccb/raw/` — getProducts · getProcedures · getMachines · getMedicines · getCategories · getMedicalServices (+ 필요하면 다른 폴더)
- 실버 · 시맨틱: `step1-products.json`(제품) · `step2-families.json` · `step3-sites.json` · `step5-units.json`(단위 시술) · `step6-packages.json` · `semantic.json`(사전 · id)

## 할 일
1. **KOS 카탈로그 구조**: 상품(카테고리) → 옵션(SINGLE · GROUP · 회차 · 단위 · 가격 · 노출 채널) → 시술(procedure) · 약제 · 장비 — 각 엔드포인트 칸 · 셈 · id 관계 그림
2. **연결 분류(전수)**: KOS 시술 · 약제 · 장비마다 실버의 무엇과 어떻게 닿는지
   - 1:1 · KOS 가 더 굵음(KOS 하나 = 단위 시술 여럿) · KOS 가 더 가늚(회차 · 용량 · 부위 묶음) · 이름만 다름 · **KOS 에만 있음**(수액 · 스킨케어 · 관리 등) · 판단 불가
   - 실버 쪽: 명동점에서 안 파는 단위 시술 · 제품 셈(실버가 넓다는 것 수치로)
   - 연결 근거는 시맨틱 사전 · 1단계 제품 이름 · 5단계 동의어 — 매칭 방식 칸 · 추정 금지(못 맞추면 못 맞춤)
3. **연결 층 모델 추천**: 허브 지식(병원 무관)과 병원 상품(병원마다)을 나누는 연결 테이블 꼴 — 키 · 방향 · 여럿 대응 · 병원 바뀔 때 갱신 방법 · 어디에 둘지(허브 / 앱)
4. 결정 묶음 + 사용자 최종 판단 한 표(진짜 사용자 몫만)
- 실명 · 환자 정보 · 키 금지(상품 · 시술 · 장비 이름 · 가격은 됨) · 가상 문장 금지

## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_f02a79cc-ee30-482f-b349-ea7ecbd45617 --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "researcher 완료: KOS ↔ 실버 연결 조사" --body "KOS 시술 N · 약제장비 N / 1:1 N · 굵음 N · 가늚 N · KOS만 N · 불가 N / 실버만 단위 시술 N"
orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb --text "[worker_done] researcher 완료 — KOS ↔ 실버 연결 조사. 상세는 인박스." --enter
```

## 추가(사용자 10-30) — 병원은 바뀌어도 허브는 안 바뀐다
- 연결 층은 **명동점 전용이 아니라 어느 병원 상품 목록에도 같은 방법으로** 붙는 꼴로 추천: ① 병원 상품 표준 꼴(병원 무관 · 상품 → 옵션 → 시술 · 약제 · 장비 · 가격 · 회차) ② 소스별 어댑터(KOS 가 첫 번째 · 다른 병원 시스템 · 엑셀도 같은 표준 꼴로) ③ 표준 꼴 → 허브 단위 시술 · 제품 연결(시맨틱 사전 · 결정론 · 못 맞춘 건 표시)
- 허브는 병원 데이터로 바뀌지 않는다. 병원에만 있고 허브에 없는 것은 「허브 보강 후보」 목록으로만(허브 갱신은 기존 단계 스킬 절차로 따로)
- 명동점은 이 방법의 첫 시험 대상 — 셈 · 매칭률은 명동점으로 내되, 규칙에 명동점 고유 이름을 박지 말 것
