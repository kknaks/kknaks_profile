# [data · 조사만] 고민을 케이스로 내리기 — 대상 표 (사용자 승인 11-20 · 쓰기 0)

너는 procedure-hub 데이터 워커다. 앞 맥락 없음 — 이 문서와 가리킨 파일만으로. **silver · gold · 허브 레포 · DB 쓰기 0** · 커밋 0 · 서브에이전트 0 · 사용자 포트(18105 · 18222) 손대지 마라. 산출은 아래 파일 3개뿐.

`P=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇` · `W=$P/orchestration/work/phub-consult-demo` · `S=$W/silver-model`(silver 작업 사본 · gold 7b8669b7 · 앞 작업 `$W/case-unit-report.md`) · `R=$P/reference/2026-11-19-myeongdong-kos`

## 결정(사용자 11-20 — 다시 묻지 마라)
- 케이스 = 단위 시술(시술 + 부위 또는 방법 · 재료 + 고민 + 제품). **고민의 정본 = 케이스.** 고민 → 케이스 → 명동점 진료항목 경로는 케이스 고민만 탄다.
- 시술 · 계열(modality) · 패키지에 붙은 고민은 원장이 그 단위로 말한 것 — 근거로 남기되 케이스로 내린다. 제품 층 고민(허가 · 제조사 적응)은 제품에 둔다(이번 대상 아님).
- 지어 붙이기 금지 — 원장 문장 · 기존 표(concern_site · site 계층 · case_method · material)로 근거가 서는 것만 「규칙으로 정해짐」.

## 대상(코디 셈 — 다시 세어 확인)
- `indication` target_table = procedure 306 행(시술 × 고민 쌍 293: 이미 그 시술 케이스에 있음 36 · 고민에 concern_site 부위 있음 31 · 부위 없음 226) · modality 255 · package 91.
- 부위는 있는데 고민이 빈 케이스 73(`case-unit-report.md` 표).

## 산출
1. `$W/concern-to-case-map.csv`(utf-8-sig) — 한 줄 = 위층 indication 행 하나(procedure · modality · package 전부). 칸: `indication_id` · `target_table` · `target_code` · `target_name` · `concern_code` · `concern_name` · `note`(원문 그대로) · `원장 문장`(source_ref 가 가리키는 원장 글 · 있는 만큼 그대로) · `concern_site 부위` · `후보 케이스`(코드 · 이름 · 부위 / 방법 · 재료 — 여럿이면 ` + `) · `판정`(아래 넷 중 하나) · `판정 근거` · `케이스 없음이면 필요한 케이스`(시술 × 부위 또는 방법).
   - 판정: `이미 케이스에 있음` / `규칙으로 정해짐`(concern_site 부위 ↔ 케이스 부위 자기 · 조상 · 자손, 또는 원장 문장이 방법 · 재료를 말해 그 방법 케이스와 맞음) / `사람 판단 필요`(후보 여럿 · 근거 약함 — 후보는 다 적고 고르지 마라) / `내릴 케이스 없음`(맞는 케이스가 허브에 없음 — 필요한 케이스를 적음) / `시술 공통으로 보임`(원장이 부위 · 방법 없이 시술 전체에 말함 — 예 「주름 개선」 · 그 시술 케이스 전부가 후보).
2. `$W/concern-empty-cases.csv` — 고민 빈 케이스 73 각각: 위 표에서 그 케이스로 올 수 있는 고민(판정별) · 여전히 0 이면 그렇다고.
3. `$W/research-concern-to-case.md` — 판정별 수(target_table 별) · 사람 판단 필요 묶음 요약(비슷한 꼴끼리 — 사람이 50 안쪽으로 볼 수 있게 묶어서 · 묶음마다 추천 하나와 이유) · 내릴 케이스 없음 → 새로 필요한 케이스 목록 · 「시술 공통으로 보임」 처리 선택지(그 시술 케이스 전부에 붙이기 / 부위 빈 일반 케이스에만 / 시술에 둠) 와 각 수 · 명동점 진료항목에 닿는 영향(진료항목 수).

## 검증
위층 indication 행 전부(306 + 255 + 91) 가 표에 한 줄씩 · 판정 빈칸 0 · 후보 케이스 코드 전부 silver 에 실재 · `git -C $P status --short` 에서 새 파일이 위 3개뿐 · silver 바이트 그대로(`shasum` 전후 같음).

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_c3f59148-8ca7-4a86-8c2b-1ea060538176 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "data 완료: 고민 → 케이스 조사" --body "판정별 수 / 사람 판단 묶음 / 새 케이스"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] data 완료 — <한 줄>. 상세는 인박스." --enter
```
질문: `orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[질문] data: <질문>" --enter`
