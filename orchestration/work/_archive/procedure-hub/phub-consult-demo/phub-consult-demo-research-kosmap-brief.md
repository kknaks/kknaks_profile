# [researcher] 명동점 KOS 시술 124 → 허브 매핑: 검수용 리스트 · 선택지 · 기본 추천안 초안

너는 **procedure-hub `researcher` 워커**다. 앞 판 맥락이 없다고 보고 아래만으로 일한다. 역할 문서(절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/roles/procedure-hub/researcher/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/상담봇` (코디와 공유 · allowed_paths 밖 생성 · 수정 0)

`P=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇` · `R=$P/reference/2026-11-19-myeongdong-kos` · `W=$P/orchestration/work/phub-consult-demo`

## 1. SSOT — 먼저 읽을 것

- `$W/research-kos.md` ← 앞 판(명동점 받기 · 현황 · gold 1차 대조) — 특히 §2-4 · §3 · §4 정할 것 M-1 ~ M-3 · L-1
- `$R/myeongdong-kos-products-20261119.json` ← 명동점 원자료(가이드 §4 꼴 · `$R/kos-product-json-guide.md`) — **KOS API 다시 부르지 마라**
- `$R/match-gold-20261119.json` ← 앞 판 대조 행
- 허브 gold/silver: 로컬 PG(SELECT 만) docker `phub-medallion-pg` 127.0.0.1:18432 — `set -a; . ~/.config/phub/medallion-pg.env; set +a` · 접속 값 출력 금지
- 앞 조사(옛 silver · 참고만): `$P/orchestration/work/_archive/procedure-hub/phub-recommend/kos-link-research.md` §2 · §3(L3 clinic_link · K4 · K5)
- 상담 앱이 허브 코드를 받는 자리(읽기만): `/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo/clinic_chat/consult/` — 이해 호출이 내는 코드 종류(고민 CON · 시술 PRC · 부위 SITE · 제품 PRD · 계열 M) · 리스트 `listing.py`

## 2. 배경

목표 = 명동점 전용 상담 실장 봇. 사용자 결정(11-19): **사람이 맞출 곳은 「KOS 시술 → 허브」 한 군데** — KOS 안에서는 시술 → 시술 항목 → 옵션(가격 · 회차 · 이벤트가) → 상품이 id 로 이미 이어져 있으니, KOS 시술 124(지금 옵션이 가리키는 것 = 판매 중)만 허브에 매달면 상담 앱이 허브 코드 → 명동점 옵션 · 상품으로 거꾸로 닿는다. LLM 은 지금처럼 허브 코드만 내고 매핑은 표 조회(결정론).

**사용자가 124 줄을 직접 검수한다.** 그래서 너는 ① 124 리스트 ② 허브에 매다는 방식 선택지 ③ 기본 추천안 ④ 그 추천안으로 124 줄 전부를 채운 초안을 낸다.

## 3. 계약

해당 없음(조사 · 초안). 확정은 사용자 검수 뒤.

## 4. 사실(코디 실측 11-19 — 너도 다시 확인)

- 허브 시술 `s_procedure` 138(부위 없는 기술 단위 · `modality_code` · `mechanism_code`) · 계열 `s_modality` 18 · 부위 `s_site` 89 · 제품 `s_product` 315.
- 허브 **케이스 `s_procedure_case` 268 = 시술 × 부위(× 재료)** — `procedure_code` · `site_code`(71 채움) · `material_code`(43) · `name_ko`(일부만 · 예 CAS-003 「눈가보톡스」 = PRC-001 + SITE-019). KOS 「부위 + 시술」 이름과 가장 가까운 허브 단위일 수 있다 — 선택지로 반드시 따져라.
- 케이스 ↔ 제품 `s_case_product` · 제품 ↔ 시술 `s_product_procedure` · 제품 ↔ 계열 `s_product_modality` · 제품 방법 `s_product_method` · 원리 그림은 시술 `mechanism_code`.
- KOS 시술 이름 꼴(앞 판 §3-2): 「부위 + 시술」(미간보톡스 · 팔지방분해주사 · 턱제모) · 「제품 이름」(포텐자 · 써마지FLX · 볼뉴머) · 허브에 없는 것(리도카인 마취 · 모델링팩 · 회원권 가입비) 등.
- KOS 시술마다 시술 항목의 약품 · 기기(앞 판 대조로 26 이 허브 제품에 맞음)도 매핑의 근거로 쓸 수 있다.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `$W/research-kos-map.md` — **검수 문서(공개 레포에 들어감)**: 이름 · 코드 · 수만. 가격 원값 · 토큰 · 테넌트 id 0.
- `$R/kos-procedure-map-draft-20261119.csv` — 124 줄 초안(검수용 · gitignore 아님 — **가격 칸 넣지 마라**). 칸은 §6-4.
- `$R/` 안 보조 스크립트 1개(`build_procedure_map.py` — 키 · 계정 0) 와 보조 산출 JSON(gitignore 됨 — `*.json`).
- 그 밖 생성 · 수정 0.

## 6. 할 일

1. **124 리스트** — KOS 시술 124 각각: 이름 · 시술 항목 수 · 그 항목들의 약품 · 기기 이름(고유) · 단위 종류 · 그 시술을 가리키는 옵션 수 · 상품 카테고리(고유) · 판매 중지 상품만 가리키는지. 정렬은 카테고리 → 이름.
2. **선택지** — 허브에 무엇으로 매다나. 최소 아래를 따지고, 선택지마다 **124 중 몇 줄이 그 방식으로 깔끔히 닿는지(셈)** · 상담 흐름에서 쓰이는 길(이해 호출 코드 → 표 조회) · 약점을 적는다.
   - (A) 허브 시술 PRC + 부위 SITE(+ 제품 PRD 있으면)
   - (B) 허브 케이스 CAS(= 시술 × 부위) + 제품 PRD
   - (C) 계열 M 만(+ 부위)
   - (D) 약품 · 기기 → 제품 PRD 만
   - 그 밖에 데이터에서 보이는 길이 있으면 더해라. 한 KOS 시술이 허브 여럿에 닿는 경우(굵음)와 허브 하나에 KOS 여럿(가늚 · 부위 · 제품별)이 닿는 경우를 어떻게 담는지도.
3. **기본 추천안** — 하나를 고르고 근거(셈 · 상담 흐름 · 검수 부담). 「허브에 없음」 줄(마취 · 팩 · 회원권 등)의 처리도 추천에 넣는다.
4. **초안 124 줄** — 추천안으로 전부 채운다. CSV 칸:
   `kos_procedure_name, kos_procedure_kos_id(넣지 마라 — 빈칸 · id 는 보조 JSON 에만), category, n_items, medicines, machines, hub_procedure_code, hub_procedure_name, hub_site_code, hub_site_name, hub_case_code, hub_product_codes, hub_product_names, hub_modality_code, status(확실 | 애매 | 허브 없음 | 시술 아님), basis(근거 한 줄 — 어떤 규칙 · 어떤 표/칸으로 닿았나), note`
   - **추정 금지**: 원천(KOS 이름 · 약품/기기 · 허브 이름 · 케이스 · 연결 표)에서 바로 닿는 것만 「확실」. 낱말을 떼거나 동의어를 썼으면 「애매」 + basis 에 무엇을 썼는지. 허브에 그 부위 · 시술이 없으면 「허브 없음」(비슷한 것으로 채우지 마라).
   - 규칙은 하나씩 패치하지 말고 **124 줄을 꼴별로 먼저 나눈 표**(부위+시술 · 제품 이름 · 시술만 · 허브 밖 …) → 꼴마다 규칙 → 한 번에 적용. 꼴별 수를 문서에 남긴다.
5. **검수 문서 `research-kos-map.md`** — 머리에 한눈 표(선택지별 닿는 수 · 추천 · 초안 status 별 수) → 선택지 비교 → 추천 → 꼴별 표 → **사용자가 볼 것**: 「애매」 · 「허브 없음」 줄 목록(그대로 표로) · 「확실」 은 수 + CSV 경로 → 정할 것 → 확인 안 됨.

## 7. 범위 제약

- KOS API 호출 0 · 허브 · 앱 레포 수정 0 · DB 쓰기 0 · 커밋 0.
- 결정하지 않는다 — 추천은 추천, 확정은 사용자.
- 서브에이전트(Agent · Explore) 쓰지 마라.

## 8. 검증

- CSV 가 정확히 124 줄(+ 머리) · status 4 값 합 = 124 · `hub_*_code` 가 전부 실제 허브 표에 있는 코드(SELECT 로 대조 · 0 누락) · CSV · 문서에 가격 · 이메일 · 토큰 꼴 0(grep).
- `git -C $P status --short` 로 변경이 allowed_paths 뿐인지.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**

- **커밋·push·PR 하지 마라.**
- 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_bd6dd2e2-2c92-45f8-8562-0bf709a0d90c \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 요약 / 검증 결과(수치) / 미결·주의점"

orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[질문] researcher: <질문>" --enter`
