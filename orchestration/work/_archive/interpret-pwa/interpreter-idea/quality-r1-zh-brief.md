# [researcher] 통키 사전 전체 보정 조사 — 중국어권 3개(zh · zh-Hant · yue) (DEC D-46)

너는 **interpret-pwa `researcher` 워커**다. 앞 맥락은 없다. 역할 문서(절대경로): `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/roles/interpret-pwa/researcher/` (`role.md` · `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토` (코디 워크트리 탑승) · **read-only — 아래 §5 의 파일 2개만 만든다.** 커밋 금지 · ⚠ PUBLIC 레포 — 키 · 실명 · 통역 기록 문장 0

## 1. SSOT — 먼저 읽을 것

- DEC **D-46**(이번 결정) + 앞 규칙 **D-35 · D-38 · D-39 · D-40**: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md`
- BASE-001 「확인한 사실 (코디 2026-11-14)」 — 카톡 지적 원인 · 사전 기계 점검 · 눈으로 본 값 오류: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/para/projects/summer-star/interpret-pwa/00-baseline/baseline-001-interpret-pwa.md`
- **지금 사전(배포본 `.6` · 170 term · read-only)**: `/Users/kknaks/orca/workspaces/interpret-pwa/interpreter-idea/back/seed/glossary.json` — term 마다 `ko` · `ko_aliases` · `entries.<lang>` = `name` · `aliases` · `source` · `reviewed` · `raw` · `note`
- **앞 조사 · 처분(선례 — 이미 본 것은 다시 파지 말고 이어서)**:
  - `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/_archive/interpret-pwa/interpret-pwa-v2/research-dispositions.md` — 10-27 처분(의도된 값: 보툴렉스 = 레티보 = 乐提葆 · 한국 전용 제품 = 영문 · 장르어 제거 등). **처분으로 정한 값은 새 근거가 없으면 뒤집지 마라 — 뒤집을 근거가 있으면 표에 「처분과 다름」으로 따로 표시**
  - `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/_archive/interpret-pwa/interpret-pwa-v2/research-r1-zh-report.md` (대륙 zh · 10-27)
  - `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/_archive/interpret-pwa/interpret-pwa-v2/research-r3-th-vi-yue-report.md` (yue 부분)
  - `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/_archive/interpret-pwa/interpret-pwa-seed-tw/research-tresure-report.md` · `research-kr-brands-report.md` (대만 3곳 · 한국 브랜드)
  - 이번에는 **사이트를 언어마다 6곳으로 넓히고 170 전부**를 본다(앞 조사는 일부 term · 일부 사이트)

## 2. 무엇을 하나

D-46: **zh(중국 대륙 · 간체) · zh-Hant(대만 · 번체) · yue(홍콩 · 번체)** 각 언어마다 그 나라 **피부과 · 미용 클리닉 공식 홈페이지 6곳**을 골라 읽고, 사전 **170 term 전부**를 그 나라 클리닉이 실제로 쓰는 표기와 대조한다.

- **규칙 = 현지어 우선 · 현지에 그 말이 없을 때만 영어**(D-46 · D-38 ②). 현지 허가명이 있으면 허가명
- **사이트 고르기**: 시술 메뉴 · 가격표가 있는 현지 클리닉 공식 사이트. 주요 도시 · 체인을 섞어라. **제외** = 블로그 · 중개/리뷰 플랫폼 · **한국 병원의 외국어 페이지**(한국식 직역이 섞인다). 플랫폼(新氧 등)은 6곳에 넣지 말고 필요하면 「보조」로만 표시
- 못 읽은 사이트(차단 · 로그인 · JS)는 목록에 남기고 다른 곳으로 바꿔 6곳을 채운다. 6곳을 못 채우면 몇 곳인지 그대로 적는다
- **지어내지 마라** — 음역을 만들지 마라. 사이트에 없으면 「못 찾음」(지금 값 유지)

## 3. 꼭 볼 것 (BASE-001 확인한 사실 · 카톡 지적)

- **토닝**(`ph-012`): zh `提亮`(밝히기 — 효과지 시술명이 아님 · 카톡 지적 ①) · yue `調色`(색 보정) · zh-Hant `淨膚雷射` — 현지 클리닉의 레이저 토닝 이름
- **울쎄라**(`ph-121`) · **써마지**(`써마지FLX` · `써마지 CPT`): 카톡 지적 ② — 대륙 · 홍콩 · 대만 클리닉 통용명. zh 별칭 `Ultherapy`(역방향 짝으로 들어가 영문 출력을 부추겼을 수 있음)를 남길지 근거
- **보톡스 · 시술 뉘앙스**: 카톡 지적 ③ — 「肉毒术」 같은 표기가 현지에 있는지(없을 것 — 확인만)
- **스컬트라**(`ph-112` zh `塑妍萃`) · **쥬베룩**(`ph-108` zh `Juvelook` · alias `乔雅露`) — 현지 클리닉 표기
- **이름 겹침**: 같은 언어에서 다른 term 이 같은 `name` 인 곳(예 zh `激光` = 레이저 · 레블라이트 · 클라리티2 · 엑셀V · `水光针` = 스킨부스터 · HA(물광)) — 현지 클리닉이 장비 · 제품을 따로 부르면 그 이름. 처분으로 일부러 같게 한 것(乐提葆)은 유지
- **영문만인 값**: 그 나라 글자가 없는 `name` — 현지 표기가 있으면 바꾸고, 현지 클리닉도 영문을 쓰면 「현지도 영문」으로 유지(근거 URL)
- **리투오**(사전에 없음 · 스킨부스터) — 현지 표기가 있으면 새 term 후보로
- **현장 일반어(사전에 넣지 않음 — D-45 context 서술 참고용)**: 그 나라 클리닉이 손님에게 쓰는 「시술」 · 「접수」 · 「상담」 · 「시술 후 불편감」에 해당하는 말과 출처 1개씩. 표 하나로 짧게

## 4. 판정 (term × 언어 칸마다 하나)

| 판정 | 뜻 |
|---|---|
| 유지 | 지금 `name` 이 현지 표기와 같다 |
| 변경 | 현지 표기가 다르다 → 새 `name` (지금 값은 alias 후보로) |
| 별칭 추가 | `name` 은 맞고 현지에서 같이 쓰는 표기가 더 있다 |
| 현지도 영문 | 현지 클리닉도 영문 브랜드명을 쓴다 |
| 현지에 없음 → 영문 | 그 나라에 없는 제품 · 시술(D-38 ②) |
| 못 찾음 | 6곳에 없음 — 지금 값 유지 |
| 처분과 다름 | 10-27 처분 값을 뒤집을 근거 |

- `reviewed` 제안: **독립 출처 2곳 이상**이면 true(D-35)
- 칸마다 출처는 §5 사이트 번호로(예 `S2 · S5`)

## 5. 산출물 — 두 파일만

1. `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/interpreter-idea/quality-r1-zh-report.md`
   - 머리: 조사 날짜 · 언어 · 방법
   - 표 S: 언어별 사이트 6곳(번호 · 이름 · 도시 · URL · 읽음/못 읽음 · 메뉴/가격표 유무)
   - 표 A: **바뀌는 칸만**(판정 ≠ 유지 · 못 찾음) — term id · ko · 언어 · 지금 name · 제안 name · aliases · 판정 · 출처 번호 · reviewed 제안 · 메모
   - 표 B: 언어별 집계(유지 · 변경 · 별칭 추가 · 현지도 영문 · 현지에 없음 · 못 찾음 · 처분과 다름 — 개수)
   - 표 C: 현장 일반어(§3 마지막)
   - 「정할 것」: 결정하지 못한 것(코디 · 사용자가 처분)
2. `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/interpreter-idea/quality-r1-zh-cells.json` — **170 term × 담당 언어 전부**: `[{"id","lang","current","verdict","proposed_name","proposed_aliases","sources":["S1",..],"reviewed_suggest","note"}]` (유지 · 못 찾음도 넣는다 — 기계 대조용)

## 6. 범위 제약

- 사전 · 코드 · 문서를 고치지 마라(리포트 2개만)
- 담당 언어 밖은 보지 마라(en · ja · th · vi 는 다른 워커 몫)
- 결정하지 않는다 — 판정과 근거만

## 8. 검증

```
질문마다 답 + 출처 URL. 사이트에 없는 것은 「못 찾음」. 결정하지 않고 「정할 것」으로 모은다
```

- `cells.json` 이 170 × 담당 언어 수 행인지 세어 보고에 적는다
- 표 A 의 모든 「변경」 · 「별칭 추가」 행에 출처 번호가 1개 이상

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_d181fbae-29f2-43bb-9a41-6bc888ca07de --from term_abd0126a-6243-4b84-9616-3629e04aa7d1 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: quality-r1-zh" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_d181fbae-29f2-43bb-9a41-6bc888ca07de \
  --text "[worker_done] researcher quality-r1-zh 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_d181fbae-29f2-43bb-9a41-6bc888ca07de --text "[질문] researcher quality-r1-zh: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
