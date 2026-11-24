# [data] 새 그림 18 등록 — 허브 그림 표(concept_image) · 이미지 목록 · gold 재빌드 (사용자 요청 11-20)

너는 procedure-hub 데이터 워커다. 앞 맥락 없음. 커밋 0 · 서브에이전트 0 · 허브 레포 커밋 0 · DB · stg 0 · 사용자 포트(18105 · 18222) 손대지 마라(18105 재시작은 코디가 한다).

`P=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇` · `W=$P/orchestration/work/phub-consult-demo` · `S=$W/silver-model`(gold 57b420ad) · 그림 시드 `I=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/reference/2026-11-17-procedure-images`(README 먼저) · 허브 워크트리 `H=/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-consult-demo`

## 배경
사용자가 새 그림 18 장을 만들고 미리보기를 확인했다(`$I/previews/2026-11-20.html`): 방법 17(MET-008 · MET-110 ~ 125 → `$I/images/method/<코드>.svg`) · 원리 1(MEC-108 → `$I/images/mechanism/MEC-108.svg`) · 라벨 162 행은 `$I/image-labels.csv` 에 추가됨. 제작 지시 `$W/image-prompts-20261120.csv`. **`image-map.csv` · `image-assets.csv` 는 아직 갱신 안 됨.**

## 할 일
1. `$I/image-map.csv` · `$I/image-assets.csv` 에 18 행을 기존 꼴 그대로 더한다(sha256 · 크기 · 텍스트 수는 파일에서 실측 · artwork_version 은 새 값(예 `2026-11-20-native-svg-v1`) · review 「구조·한영 렌더 확인 / 의료 검수 전」). `$I/README.md` 의 수(103 → 121)와 `image-validation.json` 검사 스크립트가 있으면 다시 돌려 PASS 확인.
2. silver 작업 사본 `$S/silver/concept_image.csv` 에 18 행(기존 꼴 · target_table method / mechanism · svg_path · sha256 · artwork_version · medical_review 「검수 전」) + source_ref(기존 그림 행과 같은 꼴). silver-check I2 의 「묶음 4 새 방법 예외」 · MEC-108 그림 예외를 **지운다**(이제 그림 있음). build 스크립트 `build_batch7.py`(재현) · 기준 사본 `archive/silver-before-clinic-a-20261119-b7/`.
3. silver-check → gold-build → gold-check PASS · 새 gold_hash · aux_hash.
4. 허브가 그림을 어디서 읽는지 확인(허브 README · gold_main · 설정)하고, 로컬 18105 가 새 그림을 줄 수 있게 필요한 자리에 18 파일을 둔다(예 `$H/assets/procedure-images/images/...` — 허브 워크트리 파일 추가는 커밋하지 말고 리포트에 「배포 때 반영할 파일」 목록으로).
5. 매핑 JSON v2(`/Users/kknaks/git/clinic_chat/data/kos/myeongdong-mapping-20261120.json` · 앱 워크트리 같은 파일) meta 의 hub_gold_hash · hub_aux_hash 만 새 값으로 다시 만든다(`$P/reference/2026-11-19-myeongdong-kos/build_mapping_json_v2.py` · items · groups · sites 바이트 같음 확인).
6. 리포트 `$W/image-register-report.md`: 바뀐 파일 · 행 수 · 검사 · 해시 · 허브가 읽는 그림 자리 · 명동점 화면 기준 그림 빠짐 수(원리 · 방법 — 0 이어야) · JSON 새 sha.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_55eba57e-07c1-4210-b8b4-f44cf7865f50 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "data 완료: 그림 18 등록" --body "검사 / 해시 / 그림 빠짐"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] data 그림 등록 완료 — <한 줄>. 상세는 인박스." --enter
```
