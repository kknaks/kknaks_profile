# researcher 2판 — M3D 3D 에셋 확보 · 구조 조사

너의 1판 리포트(`research-report.md`)가 맥락이다. 먼저 읽어라.

## 배경 (사용자 결정 10-21)
- 화면 2개, Next.js, `reference/2026-10-21-charty-poc/web/` 에 만든다(이번 판은 만들지 않는다)
  - ① 큰 스크린(상담사+고객): 좌 **3D 얼굴 + 필터**(잔주름·굵은주름·염증…) / 우 분석 그래프 + 추가된 시술 + 최종 가격
  - ② 상담사 태블릿: 기존 차티 상담 화면, 여기 조작이 ①에 반영
- 리포트 링크는 **살아 있다** — `render.v3?hash=<HAR 첫 요청의 hash>` 재호출 시 새 presigned URL, ZIP 4개 GET 206 확인(코디). 스캔 주인은 사용자 본인(이건학)이다.

## 할 일
1. `render.v3` 를 재호출해 `zips` 4개(obj·thumb·shape_ai·hd_ai)를 받아 `reference/2026-10-21-charty-poc/m3d-assets/<flag>/` 에 푼다(gitignore 처리됨 — 커밋 금지). `three_dimensional.mappings[].url`·`default`·`extras` 도 받을 수 있으면 받는다
2. ZIP별 파일 목록(경로·크기·형식·해상도) 요약
3. **`zip://mask/…` 21종이 어디서 오는지** 찾는다(4개 ZIP 안 / mappings / 다른 경로)
4. OBJ 점검 — 정점·면 수, UV 유무, `.mtl` 유무, 텍스처 연결, 단위·축. **three.js OBJLoader 로 브라우저에서 띄울 수 있는 형태인가**, 용량 때문에 변환(glb·decimate)이 필요한가 — 판단 말고 근거만
5. **필터 연결표**: 사용자가 말한 필터(잔주름·굵은주름·염증/붉은기·색소·모공·피문 …) 각각 → 쓸 텍스처(mappings flag)·마스크(masks flag)·측정 항목(measure features id). 이름 유사성으로 이은 것은 「추정」 표시
6. 마스크가 3D 텍스처 UV 와 같은 좌표계인가(같은 해상도·겹치면 맞는가) — 가능하면 1장 합성해 확인

## 산출
`orchestration/work/charty-consult-mockup/assets-report.md` 1개 + `m3d-assets/` 다운로드. 그 밖 파일·git 상태 변경 금지. 판단은 「정할 것」으로.
완료 보고는 1판과 같은 두 명령(task_id·dispatch_id 는 1판 값).
