# [researcher · 읽기만] 고민을 케이스에 어떻게 연결할 것인가 — 규칙 설계 + 전수 적용 표 (사용자 승인 11-20)

너는 procedure-hub 조사 워커다. 앞 맥락 없음 — 이 문서와 가리킨 파일만으로. **silver · gold · DB · 허브 레포 쓰기 0** · 커밋 0 · 서브에이전트 0 · 사용자 포트(18105 · 18222) 손대지 마라. 산출은 아래 파일뿐.

`P=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇` · `W=$P/orchestration/work/phub-consult-demo` · `S=$W/silver-model/silver` · 원장 = `$P/orchestration/work/_archive/procedure-hub/phub-recommend/bronze/phub-ledger/` · 명동점 매핑 JSON = `/Users/kknaks/git/clinic_chat/data/kos/myeongdong-mapping-20261119.json`

## 목표
상담 봇: 손님이 **고민**(+ 부위 · 시술)을 말하면 → 고민이 붙은 **케이스** → 그 케이스에 매핑된 **병원 진료항목**을 정확히 준다. 반대로 진료항목 → 케이스 → 의학 정보. 허브는 모든 병원이 같이 쓰는 지식 — 명동점은 확인용 첫 사용처.

## 결정(사용자 11-20 — 다시 묻지 마라)
- 케이스 = 단위 시술(시술 + 부위 + 방법 + 조직 + 재료 · 고민 · 제품 연결). **고민은 케이스에만 있다.** 시술 · 계열 · 패키지에 붙은 고민 줄(652)은 케이스로 내리고 원래 줄은 근거(source_ref)로만 남긴다 — 위층 고민 줄은 0 이 목표. 제품 층 고민(허가 · 제조사 적응)은 제품에 둔다.
- 「일반 케이스(부위 · 방법 다 빈 케이스)」 개념은 **폐기** — 단위 시술은 부위와 방법이 반드시 있다. 지금 다른 워커(data · `case-fill-task.md`)가 모든 케이스의 부위 · 방법 · 조직 · 재료를 빈칸 없이 채우는 중이다.
- **우리 데이터는 완전히 채운다** — 모든 케이스는 고민 1 이상. 원장에 없으면 근거 종류 「보충」으로 채우되 근거 글 필수 · 지어내기 금지.
- 효과 · 부작용 · 대처 · 금기 · 회복은 「시술 공통 + 케이스 특성」 물려받기 유지(이번 범위 밖).

## 앞 조사(읽고 출발 — 다시 하지 마라)
`$W/research-concern-to-case.md` · `$W/concern-to-case-map.csv`(652 줄 판정) · `$W/concern-empty-cases.csv`. 그 조사의 약점: 「시술 공통」 302 를 「일반 케이스」로 보내려 했다(폐기) · 계열 · 패키지를 계열에 남기려 했다(폐기).

## 할 일
1. **연결 규칙 설계** `$W/concern-link-rules.md`: 위층 고민 줄 하나를 어느 케이스(들)로 내리는지 규칙 — concern_site · 고민 계층(parent) · site 계층 · 케이스 방법 · 재료 · 원장 문장 · 패키지 구성(package_item) · 계열 구성. 「시술 공통」(원장이 부위 없이 말함)은 **고민의 성격**(부위 고민 / 피부 전체 상태 · 전신 상태)과 **케이스 부위**로 가른다 — 예: 「여드름 · 모공 · 색소」 = 얼굴 피부 상태 → 그 시술의 얼굴(및 얼굴 하위) 케이스 · 「간 해독 · 피로」 = 전신 → 전신 케이스. 고민마다 「어느 부위 고민인가」 를 정하는 표(`$W/concern-scope.csv` — 고민 코드 · 이름 · 고민 부위(concern_site 또는 성격으로) · 근거)를 먼저 만든다. 규칙은 입력 전수 표(고민 꼴 × 케이스 꼴) 로 — 빠진 조합 0.
2. **전수 적용 표** `$W/concern-link-map.csv`: 위층 652 줄 + 기존 케이스 고민 276 줄 각각 → 붙을 케이스 코드들 · 적용 규칙 · 근거. 판정은 `규칙` / `사람 판단`(후보 다 적고 고르지 마라) 둘뿐. **고민 0 인 케이스 목록**도 따로(채울 근거 후보 포함).
   - data 워커의 케이스 보충이 끝나면(`$W/case-fill-report.md` 생김 · silver 바뀜) 그 silver 로 표를 **다시 돌려** 최종본을 낸다. 그 전에는 지금 silver 로 초안. 최종본 기준 silver 해시를 리포트에.
3. **확인 시험** `$W/concern-link-check.md`: 고민 15 개(여드름 · 기미 · 모공 · 입꼬리 처짐 · 팔자주름 · 다한증 · 탄력 저하 · 이중턱 · 눈가주름 · 사각턱 · 셀룰라이트 · 잡티 · 홍조 · 볼륨 손실 · 피부 건조)에 대해 「표 적용 뒤」 고민 → 케이스 → **명동점 진료항목** 목록(지금 vs 적용 뒤) · 엉뚱하게 걸리는 것 · 빠지는 것을 표시.
4. 리포트 `$W/research-concern-link.md`: 규칙 요약 · 규칙 / 사람 판단 수 · 사람 판단 묶음(50 안쪽 · 묶음마다 추천) · 위층 고민 줄 0 이 되는지 · 고민 0 케이스 수 · 확인 시험 요약.

## 검증
652 + 276 줄 전부 표에 · 판정 빈칸 0 · 케이스 코드 전부 silver 실재 · 고민 15 개 시험표 · `git -C $P status --short` 에서 새 파일이 위 것들뿐 · silver 바이트 그대로(내가 고치지 않음).

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_765571d6-d53f-4b23-9c83-023ee8a25d47 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "researcher 완료: 고민 → 케이스 연결 설계" --body "규칙 / 사람 판단 / 시험"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] researcher 완료 — <한 줄>. 상세는 인박스." --enter
```
질문: `orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[질문] researcher: <질문>" --enter`
