# [writer] DEC-002 — 시술 원장 정의(단위 시술 · 부위 트리 · 이름 원칙)

너는 **procedure-hub `writer` 워커**다. 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/writer/role.md`
작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` (코디 워크트리 공유)

## 1. SSOT

- `orchestration/work/phub-recommend/_RESUME.md` §2 — **2026-10-27 행 4개가 이번 결정의 정본.** 여기 없는 결정을 만들지 마라
- `DEC-001.md`(같은 폴더) — 양식 · 번호 체계 · D-02 메달리온 매핑 · D-13a(노드 단위) · D-13f(부위) — 이번에 대체된다
- 근거 원천(읽기만): stg 저장본 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/` — `taxonomy.json`(modality 하위 분류 · 용도별 항목) · `market-pricing.json`(항목 이름의 부위 표현) · `anatomy-danger-zones.json`(11곳) · `problem-packages.json`(CC 이름)
- `research-report.md` §Q1(canonical `catalog_procedure_concept` 레벨) · `source-fix-list.json`(A2 · D 그룹)
- 양식: `templates/projects/10-decision/decision.md`

## 2. 배경

사용자와 대화(10-27)에서: taxonomy 의 「시술 항목」이 제품(나보타) · 부위(사각턱) · 목적(다한증) · 기법(스킨보톡스) · 패키지(풀페이스큐레이션)를 한 칸에 섞어, 그 위에 지은 그래프 · 원천 수정 제안이 다 흔들린다는 결론. 시술 원장(실버)을 다시 정의한다.

## 3. DEC-002 에 담을 결정 (전부 사용자 확정 — §1 _RESUME 10-27 행)

- **D-01 taxonomy 의 위치** — 시술 원장이 아니라 관리 화면용 분류 트리. 브론즈 원천으로만 쓴다
- **D-02 단위 시술** — 제일 작은 단위 행위 = **무엇을(약제·장비 계열) × 어디에(부위) × 어떻게(기법)**. 예: 「보툴리눔 톡신 · 사각턱 · 근육 내 주입」 · 「보툴리눔 톡신 · 얼굴 전체 · 진피 내 미세 주입(스킨보톡스)」 · 「HA 필러 · 코 · 피하 주입」
- **D-03 축별 자리** — 약제·장비 계열(보톡스 M1 · 필러 M2 · HIFU M9 …) = 「무엇을」 / 제품(나보타 · 써마지FLX) · 용량 · 샷 = 단위 시술의 **속성**(제품 노드는 두고 「쓰는 제품」 엣지) / 목적(주름 · 다한증) = **고민 → 단위 시술 엣지** / 패키지(풀페이스큐레이션) = **단위 시술 묶음**. taxonomy M1(보톡스)의 국산·수입·용도별 항목을 이 표로 나눈 예시 1개를 넣는다(원천 실물)
- **D-04 이름 원칙** — 노드 이름 = 상담 용어 / 해부학 · 기법 의학 용어 = 속성 / 구어 표현 = 동의어. 이유: 질의와 Jev 선택지가 상담 언어, 안전(위험 부위 원장)과 의료진 검수는 해부학 이름
- **D-05 부위 트리** — 쪼개는 규칙 ① 원천 데이터가 따로 부른다(시장가 · 고민 분류 · 용도별 · 위험 부위) ② 가능 시술 · 안전이 달라진다. 둘 다 아니면 쪼개지 않는다. 트리(확정):
  - 얼굴: 이마[이마 · 미간] · 관자놀이 · 눈가[눈가 · 눈밑 · 눈꺼풀] · 코[코 · 코끝] · 볼[볼 · 광대] · 입가[팔자 · 입술 · 입꼬리 · 잇몸] · 턱[턱끝 · 턱선 · 사각턱 · 턱밑] · 얼굴 전체
  - 목[목 · 승모근] · 두피 · 바디[겨드랑이 · 팔뚝 · 복부 · 허벅지 · 종아리 · 전신]
  - 노드마다 **원천 근거 표**(어느 파일 · 어느 이름에서 나왔나)를 단다. 위험 부위 11곳과의 대응(forehead→이마 등)도 표로. 해부학 이름 속성 칸은 두되 값은 비워 OQ 로(의학 용어 확정은 의료진)
- **D-06 시술 ↔ 부위** — 「이 시술을 이 부위에 할 수 있다」 엣지. 예: 「턱쪽에 필러」 → 부위 턱 하위 중 필러 가능 엣지가 있는 턱끝 · 턱선(사각턱 제외) → 외부 LLM 이 되묻기
- **D-07 이름에 붙은 부위 · 고민 분리** — 「팔자주름」= 부위 팔자 + 고민 주름. 「이마 주름(수입)」 같은 시장가 항목도 부위 + 고민 + 제품 등급으로 분리. 「얼굴 전체」는 부위 노드
- **D-08 대체 · 영향** — DEC-001 D-13a(시술군 + 시술 항목 둘 다 노드) · D-13f(위험 부위 11곳만 부위)를 대체. 영향: SPEC-001 §3.2 노드 · §3.3 엣지 개정 필요 · 원천 수정 목록 A2~A6 제안값 재생성 · 그래프 재빌드. 이 문서는 개정 내용을 쓰지 않고 「영향」만 나열
- **다음 단계(한 줄씩)**: taxonomy 항목 → 축 분류표(사용자 답) → SPEC-001 개정 → 재빌드

**열린 것(OQ)** — 결정하지 말고 질문 · 왜 · 영향 D:
「어떻게(기법)」 목록과 세분화(근육 내 / 진피 내 / 피하 등 — 원천에서 보이는 것만 후보로) · 해부학 이름 확정(의료진) · 「무엇을」 계열을 taxonomy 시술군 17개로 그대로 둘지 · canonical `catalog_procedure_concept` 를 확장해 담을지(DEC-001 OQ-103 과 연결) · 패키지 구성 원천

## 4. allowed_paths

- 생성: `orchestration/work/phub-recommend/DEC-002.md`
- 수정: `DEC-001.md` 의 D-13a · D-13f 행만 — 취소선 + 「→ DEC-002 로 대체(2026-10-27)」. 그 밖의 줄 금지

## 5. 제약

- §3 에 없는 결정 추가 금지 — OQ 로. 스키마 · 테이블 · API 설계 금지
- 원천은 저장본만 읽는다(stg 호출 금지). public — 키 · 실명 금지

## 6. 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_92a9e861-40e9-4ab0-bec1-e792cb83801e --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: DEC-002" \
  --body "D 목록 / 부위 노드 수 · 근거 없는 노드 / OQ / DEC-001 수정 줄"

orca terminal send --terminal term_92a9e861-40e9-4ab0-bec1-e792cb83801e \
  --text "[worker_done] writer 완료 — DEC-002. 상세는 인박스." --enter
```
