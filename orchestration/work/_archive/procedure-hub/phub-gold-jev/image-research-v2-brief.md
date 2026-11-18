# [researcher] 원리 · 방법 그림을 silver → gold → DB → 허브 → 상담 화면으로 잇기 — 조사

너는 **procedure-hub `researcher` 워커**다(read-only). 앞 판의 맥락이 없다 — 아래 「읽을 것」만으로 일한다. 먼저 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/roles/procedure-hub/researcher/role.md`(+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`).

작업 워크트리(코디 워크트리 · 공유): `P=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온` — **리포트 1개 외에는 만들거나 고치지 마라.**

경로: `W=$P/orchestration/work/phub-gold-jev` · 그림 `I=$P/reference/2026-11-17-procedure-images`(미커밋 · 읽기만) · `SM=$P/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model`(gitignore · 로컬) · 허브 `H=/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`(읽기만 · HEAD daa54e3 = 로컬 DB 판) · 앱 `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev`(읽기만 · **0.2 구현 중이라 흔들림**)

## 0. 이번 판(2회차) — 먼저 읽을 것

- 앞 조사 `$W/research-images.md`(1회차 · 11-17) 가 있다. **그 뒤 그림 묶음이 바뀌었다**: 그림 세션 보고 — 「103 코드 전부 새 SVG 완료 · 대표 경로 CODE.svg · image-labels 787행 · 버전 2026-11-17-native-svg-v1 · 해시 명시 · 옛 JPG(MEC-070) 는 legacy-source 로 분리 · 활성 시드 참조 0 · 별칭 83 새 내용 동일 · image-map 에 SVG 제작 상태 열」. 1회차의 「새 70 / 옛 33」 · U-2 · U-3 · U-6 은 낡았을 수 있다 — **다시 센다**.
- 1회차 뒤 정해진 것: 서빙 = 바인드 마운트 1순위(`_RESUME` §2) · 그림 DB 는 0.2 뒤라 멈췄다가 사용자가 다시 엶(지금) · Procedure Hub 데이터는 공개.
- 2회차 리포트는 **바뀐 것 위주**: 1회차 정할 것 U-1~U-11 마다 「그대로 / 바뀜 / 닫힘」 + 새로 생긴 정할 것. 1회차와 같은 내용은 「1회차 §x 그대로」 로 줄인다.

## 1. 배경 · 정해진 것

- 사용자: 원리(mechanism) · 방법(method) 개념도를 **DB 에 넣고 상담 화면에서 그림으로 보여 주고 싶다.** 먼저 조사.
- 원칙(정해짐): **CSV 그대로 DB**(silver CSV 에 칸 · 표를 더하고 → gold · DB · 허브로 같은 길) · 빈칸만 NULL · 판 하나 교체 + 빌드 기록 · Procedure Hub 데이터 · medikit 은 공개.
- 전달 메모가 요구한 것: ① silver mechanism · method 에 이미지 칸 ② 여러 장인 코드를 어떻게 담나(칸에 목록 vs 별도 표) ③ 허브 응답에 그림 경로 ④ 서빙 자리(레포 정적 vs 스토리지) · 주의: **전부 의료 검수 전(medical_review: not_performed) — 상담 화면 노출은 검수된 것만 · 검수 상태 칸 필요** · MEC-070 외부 사진(CC BY-SA 4.0) 여부 · 기기(제품) 사진은 범위 밖.
- 시점: 상담 채팅 0.2 뒤 다음 판. 이번은 **조사만**.

## 2. 읽을 것

- `$I/README.md` · `image-map.csv` · `image-assets.csv` · `image-labels.csv` · `image-validation.json` · `media-coverage-survey.md` · `codex-prompts.md` · `images/` · `previews/`
- silver: `$SM/silver/{mechanism,method}.csv` 와 그 둘을 가리키는 silver 표 전부(grep) · `$SM/notes/silver-erd.md` · `silver-tables.md` · gold: `$SM/gold/{README.md,semantic-map.md,gold-build.py,gold-check.py}` · `g_profile` 등 mechanism/method 코드를 담는 gold 칸
- DB 판: `$W/SPEC-003-hub-gold-db.md` · `$H/backend/app/model/medallion.py` · `$H/backend/app/modules/gold/{silver_contract,medallion_load,inputs,db_inputs,service,repository}.py` · `$H/backend/alembic/versions/b202611170001_*.py` · 허브 정적 파일 서빙 여부(`app/main.py` · `gold_main.py` · `Dockerfile` · `.dockerignore`)
- 허브 계약: `$W/SPEC-001-hub-gold-mcp.md`(facets · 원리/방법 칸 · §3-2a 싣는 칸 은 `$W/SPEC-002-chat-eval.md`)
- 상담: `$W/SPEC-004-consult-chat.md` · `$W/SPEC-005-consult-state.md` · 앱 `consult/` 의 리스트 · 답 그리기(어디에 그림을 붙일 수 있나)

## 3. 질문 — 답마다 근거(파일:줄 · 셈 명령과 결과)

**Q1. 그림 묶음 실태** — 103 코드 × 그림 수(여러 장 12) · 파일 크기 · 형식 · 라벨 528 의 쓰임 · 검증 결과 · **MEC-070 등 외부 · 권리 표기 필요한 것 전수**(image-assets 의 출처 · 라이선스 칸) · 의료 검수 칸이 어디 있나(없으면 없다고) · silver mechanism 54 / method 49 와 코드 대조(빠진 코드 · 남는 코드).

**Q2. silver → gold 경로** — mechanism · method 코드가 gold 어디에 들어가나(표 · 칸 · 행 수) · 상담에서 원리 · 방법이 재료로 실리는 자리(SPEC-002 §3-2a · 앱 걷기의 정보 종류) · 그림이 「그 행 옆」 에 붙으려면 무엇으로 잇나.

**Q3. 담는 꼴 선택지** — (a) silver mechanism · method 에 칸(`image_path` 목록 · `image_status`) (b) 새 silver 표(예: `concept_image(code, seq, path, kind, license, medical_review, …)`) (c) 그 밖 — 각각 「CSV 그대로 · 담을 칸 없는 값 0」 · FK · gold-check · silver-check · SPEC-003 테이블 · 적재기 · 해시(aux) 에 미치는 영향 · 행 수. 라벨(528)을 DB 에 둘지.

**Q4. 허브 응답** — 어느 도구 응답에 어떤 꼴로(경로 · 검수 상태 · 라이선스 표기) · 「검수된 것만」 거르기를 허브가 하나 앱이 하나 · SPEC-001 계약 변경 범위.

**Q5. 서빙** — 허브 레포 정적 파일 · 앱 정적 파일 · 스토리지 — 지금 허브가 정적 파일을 내는지 · 이미지(Dockerfile/.dockerignore) · stg 길 · 크기(8.7MB) · 공개 레포 여부(허브는 PRIVATE · 앱 · 프로필은 PUBLIC).

**Q6. 상담 화면** — 그림을 어디에(답 옆 카드 · 리스트 행 · 원리 질문일 때만) · 언제(묻지 않은 것 안 붙임 원칙과의 관계) · 검수 안 된 것의 처리.

**Q7. 정할 것** — 리포트 머리에 요약(질문당 2~3줄) + 「정할 것」 표(사용자가 고를 것만 · 각각 추천 · 근거 · 위험). 결정하지 마라.

## 4. allowed_paths

- **쓰기: `$W/research-images-v2.md` 1개만.** 임시 파일은 네 scratchpad 에만.

## 5. 하지 말 것

- 결정하지 마라. 외부 API · CLI 호출 금지 · `.env` · 접속 값 파일 열지 마라. DB · 서버 띄우거나 내리지 마라(18105 · 18222 · 18432 등 — GET 도 하지 마라 · 파일만 읽는다). 레포 작업 트리 바꾸지 마라(stash · checkout · fetch 금지). 큰 파일 만들지 마라.

## 6. 검증

질문마다 답 + 근거. 확인 못 한 것은 「확인 안 됨」. 끝내기 전 `git -C $P status --porcelain` 에서 네 변경이 리포트 1개뿐인지.

## 7. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**

```bash
orca orchestration send \
  --to term_a88e896b-403c-4d2d-9bcc-4388724b3418 --from <네 터미널 핸들> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "researcher(그림) 완료: <한 줄>" \
  --body "변경 파일 / 요약 / 정할 것 개수 / 미결·주의점"

orca terminal send --terminal term_a88e896b-403c-4d2d-9bcc-4388724b3418 \
  --text "[worker_done] researcher(그림) 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
