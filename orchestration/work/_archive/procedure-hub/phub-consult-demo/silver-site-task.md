# [silver] 허브 부위 3단 — silver 수정 → silver 검사 → gold 빌드 → gold-check

너는 procedure-hub 데이터 워커다. 앞 맥락 없음 — 이 문서만으로 일한다. 결정은 이미 끝났다(사용자 11-19) — **다시 묻지 말고 그대로 반영**. 막히면 질문(§완료 보고의 질문 방식).

`P=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇` · `W=$P/orchestration/work/phub-consult-demo` · `S=$W/silver-model`(**작업 사본** — silver 59 · gold(빌드 스크립트 포함) · notes · gitignore · 여기서만 고친다) · 원본 `/Users/kknaks/git/toy_pr2/kknaks_profile/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model/` 은 **읽기만**.

## 입력(결정)
- **3단 배치표**: `$P/reference/2026-11-19-myeongdong-kos/hub-site-tree-draft.csv`(허브 89 + 추가 24 · 1단 · 2단 · 3단 · 이동 · 다른 이름) + 리포트 `$W/research-site-tree.md`.
- **확정 변경**(배치표보다 우선): 1단 = 얼굴(SITE 「얼굴」) / 몸(SITE-001 「전신」) · 머리(두피 · 정수리 · 머리) · 귀(이개 · 이주 · 이하부) = 얼굴 2단(「귀」 2단 부위는 새로) · 귀밑샘 = 귀 아래 · 턱밑샘 = 턱 아래 · 침샘 = 턱 아래 · 팔자주름 → 볼 3단 · 마리오네트라인 → 입 3단 · 헤어라인 → 머리(두피) 3단 · 잇몸 · 구강 → 입 3단 · 비강 · 부비동 → 코 3단 · 구레나룻 → 볼 3단 · 수염 → 턱 3단 · 하안면 · 중안면 = 얼굴 2단 묶음 부위 · 사지 · 상체 · 체간 · 코안면 = 묶음 부위(1단 아래 · description 에 「묶음」) · 관절 → 몸 > 「기타」(2단 「기타」 새로) · 나비존 → 얼굴 > 볼 · 부유방 → 몸 > 가슴 · 쇄골 → 몸 > 목 · 원장 근거 없는 추가 15 도 넣음.
- **이번 판 기본값(코디)**: ① 「눈 → 눈 주변 다른 이름」 은 **이번 판에서 하지 않는다** — SITE-018 「눈」 은 지금 위 부위 그대로 두고 3단 밖 예외 1 로 기록. ② 침샘 · 쇄골 · 승모근(anatomy 와 같은 이름 — gold-check D3)은 **site 로 만들고** `anatomy_site` 로 ANA-075 · ANA-106 · ANA-064 와 잇는다 — D3 가 FAIL 이면 그 검사 규칙을 어떻게 바꿔야 하는지 보고(검사 코드는 고치지 말고 멈춰서 질문). ③ 다른 이름은 **허브 부위의 다른 이름만**(넥 → 목 · 콧볼 → 비익 · 힙 → 엉덩이 · 애교 → 애교살 · 겨 → 겨드랑이 · 구렛나루 → 구레나룻 · 풀페이스 → 얼굴 · 입술위 → 윗입술 · 눈썹뼈 → 안와상부 · 팔 상완 → 팔뚝 · 양볼 → 볼 · 아이 → 눈 주변 · 하관(전체) → 하안면) — 거미스마일 · 러브핸들 · 측두근 은 **넣지 않는다**(진료항목 쪽 판정).
- **새 부위 근거**: 원장 근거 있는 것(심부볼 · 승모근 · 허벅지 안 · 밖 · 승마 · 쇄골 · 침샘 · 귀밑샘 · 턱밑샘)은 그 원장 경로를 `source_ref` 에(기존 꼴 · `research-site-tree.md` §3 의 원장 · 키 경로). **원장 근거 없는 15** 와 「귀」 · 「기타」 2단 · 위치 이동은 근거를 **로컬 근거 파일** `$S/drafts/clinic-supplement/clinic-a-20261119/user.csv`(새로 · 줄마다 부위 · 결정 · 근거 글 「사용자 결정 2026-11-19 · 명동점 KOS 진료항목명」)에 적고 `source_ref.ref` = `drafts/clinic-supplement/clinic-a-20261119/user.csv:L<줄>` — 앞 사례 `notes/external-fill-notes.md`(외부 출처 → `drafts/external-research/external-research.csv:L<줄>`)와 같은 꼴. **병원 이름 · 진료항목 코드 · KOS 값은 공개 silver 에 넣지 마라**(묶음 키는 `clinic-a-20261119`).

## 할 일
1. `$S/silver/site.csv` — `parent_code` 를 3단대로 · 새 부위 행(코드는 기존 꼴로 다음 번호) · name_en(모르면 빈칸 · name_en_source 규칙 따름) · description(묶음 부위는 「묶음 부위」 · 기타).
2. `$S/silver/alias.csv`(다른 이름) · `anatomy_site.csv`(침샘 · 쇄골 · 승모근) · `source_ref.csv`(새 행 근거) — 각 표의 기존 꼴 그대로.
3. silver 검사 → `$S/gold/gold-build.py` 로 gold 빌드 → `gold-check.py`. 실행 경로 · 인자는 스크립트와 `$S/gold/README.md` 를 읽고 **작업 사본 경로로** 돌린다(원본 경로를 쓰지 마라). gold-check 가 깨지는 자리(검수 `review-spec-009.md` 가 짚은 A1 · A3 · G1 · D3 · T2-1 SITE-120)는 **스크립트를 고치지 말고** 무엇이 왜 깨졌는지 · 어떻게 고쳐야 하는지 보고하고 멈춰라(질문).
4. 원본 대비 바뀐 것 셈: site 행(이동 · 새) · alias · anatomy_site · source_ref 줄 수 · gold 파일별 바뀐 행 · `gold_hash` · `aux_hash`(새 값).

## 산출
- `$S/` 안 수정본 · 짧은 리포트 `$W/silver-site-report.md`(바뀐 수 · 검사 결과(PASS/FAIL 줄) · 해시 · 멈춘 자리 · 확인 필요).

## 하지 말 것
허브 레포 · 원본 silver-model · DB 수정 0 · 커밋 0 · 서브에이전트 0 · 검사 스크립트 수정 0 · 병원 이름 · 코드 공개 칸에 0.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_aa56ab2d-a03b-4bc8-bf48-1f2d0f33c00e --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "silver 완료: 부위 3단" --body "바뀐 수 / 검사 / 해시 / 멈춘 자리"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] silver 완료 — <한 줄>. 상세는 인박스." --enter
```
질문: `orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[질문] silver: <질문>" --enter`
