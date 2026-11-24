# [data] 매핑 JSON v2 — 진료항목 + 옵션(가격) + 케이스 매핑 + 부위 좌표 (사용자 승인 11-20)

너는 procedure-hub 데이터 워커다. 앞 맥락 없음 — 이 문서와 가리킨 파일만으로. 커밋 0 · 서브에이전트 0 · silver · gold · 허브 레포 · DB 수정 0 · 앱 코드 수정 0 · 사용자 포트(18105 · 18222) 손대지 마라 · 키 출력 0.

`P=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇` · `W=$P/orchestration/work/phub-consult-demo` · `R=$P/reference/2026-11-19-myeongdong-kos` · `S=$W/silver-model/silver`(gold 57b420ad) · 앱 워크트리(읽기만) `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo`

## 목표
상담 화면(디자인: 왼쪽 얼굴 그림 + 부위 점 · 진료항목 카드 · 모달 · 「담은 시술」 장바구니 + 최저가 추천)이 JSON 하나로 그려지게 한다. **화면에 보이는 값은 원본 그대로** — 합치거나 지어 넣지 않는다(없으면 빈 값).

## 입력
- 지금 JSON 생성: `$R/build_mapping_json.py` · v5 CSV `$R/myeongdong-kos-medical-services-20261119.v5.csv`
- KOS 상품 · 옵션: `$R/myeongdong-kos-products-20261119-v2.json`(products[].options[] · price · count · type · is_event · closed · deleted · description · treatment_item_kos_id · treatment_items[].code / status)
- 디자인 얼굴 그림: `$W/design-face-0.svg`(viewBox 0 0 590 1060 · 사용자 디자인 아티팩트에서 뽑음)
- 기존 앱 얼굴 좌표표(같은 viewBox · 비율 0~1): `$A/clinic_chat/consult/face_coords.py`(FACE_COORDS · shape point / pair / area / line / none)
- 부위 사전: `$S/site.csv`(계층 · 이번에 「몸」 행 생김)

## 할 일
1. `$R/build_mapping_json.py` 를 고쳐(또는 v2 스크립트) **`myeongdong-mapping-20261120.json`** 생성 — 같은 두 경로(`/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo/data/kos/` · `/Users/kknaks/git/clinic_chat/data/kos/` · git 무시 확인). 옛 파일(-20261119)은 지우지 마라.
2. **items[]**(324 · 지금 칸 유지) 에 더함:
   - `kos_status`(게시여부 원본 값 · treatment_items[].status)
   - `status` · `note`: v5 「상태」 그대로(「매핑됨」 · 「매핑됨(제품 확인 필요)」 · 「매핑됨(확인 필요: BBL 필터)」 · 「시술 확인 필요」 · 「허브 대상 아님」) · note = v5 확인 필요 이유(지금은 빈 note 가 생김 — 고침).
   - `options[]`: 이 진료항목에 연결된 옵션 전부(deleted 제외 · closed 는 칸으로) — `product_title` · `product_is_event` · `option_title` · `type` · `count` · `price_amount` · `supplied_amount` · `vat_amount` · `taxation` · `description` · `closed` · `display_channels`. 원본 값 그대로. 옵션 없는 진료항목은 `[]`(코디 셈: 288 있음 · 36 없음 — 다시 세어 리포트).
3. **sites{}**(부위 표 · 진료항목의 `hub.site_codes` 에 나오는 부위 전부 + 그 조상): `code → {name, region: "face" | "body", shape, points}`.
   - region: site 계층에서 얼굴(SITE-007) 아래 = face · 그 밖 = body.
   - **face**: 좌표 = `face_coords.py` 값 그대로(출처 칸 `face_coords`). 표에 없는 얼굴 부위(예 심부볼 · 나비존 · 귀밑샘 · 침샘 · 턱밑샘 · 턱 등 — 다시 셈)는 `design-face-0.svg` 윤곽을 보고 새로 찍음(출처 `새로 · 워커 초안`) · shape 는 같은 꼴 규칙(가운데 = point · 좌우 = pair · 넓은 영역 = area(점 없음 · 라벨)).
   - **body**: shape `list` · points `[]` — 화면은 얼굴 그림 아래 「• 전신 · • 팔뚝」 처럼 점 + 이름 목록으로 그린다(사용자 결정 11-20).
4. **좌표 미리보기** `$W/face-coords-preview.html`: design-face-0.svg 위에 face 부위 점 전부 + 코드 · 이름 라벨(새로 찍은 것은 다른 색) · 아래에 body 목록 — 사용자가 눈으로 확인.
5. 리포트 `$W/mapping-json-v2-report.md`: JSON 꼴(예시 1 항목 · 1 부위) · 옵션 붙은 / 안 붙은 진료항목 수 · 옵션 없는 36 목록 · status 별 수 · 부위 face / body 수 · 새로 찍은 좌표 목록 · 두 경로 해시.

## 검증
items 324 · 옵션 가격 값이 원본과 같음(표본 10 대조) · deleted 옵션 0 · sites 에 items 의 부위 코드 빠짐 0 · face 부위 중 point / pair 인데 좌표 빈 것 0 · 두 경로 같은 해시 · git 무시 확인.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_d630855d-4002-4ea8-94ec-00c387f4b872 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "data 완료: 매핑 JSON v2" --body "옵션 / 부위 / 새 좌표 / 해시"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] data 완료 — <한 줄>. 상세는 인박스." --enter
```
질문: `orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[질문] data: <질문>" --enter`
