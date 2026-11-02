# 에셋 리포트 — M3D 3D 에셋 확보 · 구조 (researcher 2판)

- 작성: researcher 워커 · 2026-10-21 · 지시서 `assets-instructions.md`
- 다운로드 위치: `reference/2026-10-21-charty-poc/m3d-assets/` (총 290MB, `.gitignore:87` 로 무시됨 — 커밋 안 함)
- 확인용 합성 이미지: `m3d-assets/_check/` (`overlay_crop.jpg`, `overlay_rgb_masks_keypoints.jpg`, `hd_ai_contact.jpg`)
- 경로 표기 `A:` = `m3d-assets/`

---

## 0. 요약

1. `render.v3` 를 다시 호출해 ZIP 4개와 텍스처 15장을 모두 받았다(전부 HTTP 200).
2. **`zip://mask/…` 21종의 파일은 어디에도 없다.** `zips` 에 `mask` 키가 없고, 4개 ZIP 안에도 해당 파일명이 없다. 이 이름들은 `obj/data_all.json` 에 `.png` 로 적혀만 있다.
   **대신 `hd_ai.zip` 에 같은 역할의 마스크가 84장 있다.** 텍스처와 같은 9728×4864 UV 아틀라스다.
3. OBJ 는 Open3D 로 만든 삼각형 140,421개, 정점 70,687개짜리 메시다. 정점은 미터 단위(얼굴 약 21cm)이고 y 가 위, +z 가 정면이다. UV 는 있고, `.mtl` 은 참조만 되어 있고 파일은 없다. 텍스트 20.4MB다.
4. 마스크·텍스처·키포인트가 **같은 UV 좌표계임을 합성으로 확인했다.** OBJ 의 `vt` 는 이미지 좌표를 위아래로 뒤집은 값이라 three.js 기본값(`flipY=true`)과 맞는다.
5. 원본 M3D 뷰어는 three.js OBJLoader 에 커스텀 셰이더를 쓴다. 텍스처 두 장(`texture1` 바탕, `texture2` 오버레이)을 `alpha=(r+g+b)/3` 로 섞으므로 **검정 바탕·흰 전경 마스크를 그대로 덮는 구조**다.

---

## 1. 받은 것

| 대상 | 저장 위치 | 결과 |
|---|---|---|
| `zips.obj` | `A:_zips/obj.zip` → `A:obj/` | 200 · 39.5MB(압축) / 52MB |
| `zips.thumb` | `A:_zips/thumb.zip` → `A:thumb/` | 200 · 13.6MB / 14MB |
| `zips.shape_ai` | `A:_zips/shape_ai.zip` → `A:shape_ai/` | 200 · 8.4MB / 8.7MB |
| `zips.hd_ai` | `A:_zips/hd_ai.zip` → `A:hd_ai/` | 200 · 32.2MB / 66MB |
| `three_dimensional.default` + `mappings[13]` + `extras[1]` | `A:_images/*.jpg` | 15건 모두 200 · 각 9728×4864 · 1.8–13.5MB |

재호출한 `render.v3` 는 code 0 이었고, `zips` 키는 `obj, thumb, shape_ai, hd_ai` 4개로 HAR 때와 같다.

## 2. ZIP별 파일 목록

### obj (6개)

| 파일 | 크기 | 형식·해상도 | 내용 |
|---|---|---|---|
| `Rgb.obj` | 20.4MB | Wavefront OBJ 텍스트 | 얼굴 메시 (§4) |
| `Normal.png` | 31.4MB | PNG 9728×4864 | 노멀맵(UV 아틀라스, 얼굴 영역 51%) |
| `data_all.json` | 8KB | JSON | 특징 29종 + `Mask` 파일명 + 수치 · `Version 5.10.0` (§3) |
| `key_points.txt` / `key_points_raw.json` / `optimized_key_points.json` | 43 / 52 / 10KB | JSON | 얼굴 랜드마크. raw 478개, optimized 92개. 항목 형식 `[u, v, x, y, z, 정점/면 index]` |

### thumb (34개) — 광원 텍스처 축소본

- `<Name>_M.jpg` 3242×1621(풀해상도의 1/3) + `<Name>_Middle_T.jpg` 1024×1024 썸네일이 한 쌍이다.
- `mappings` 13종(RgbCool·Rgb·RedBlood·RedEnhanced·Red·RedHeat·Brown·BrownHeat·BrownEnhanced·Uv·UvEnhanced·Plh·Plv)에 `Old`(노화 시뮬레이션)를 더해 14쌍이다.
- **`mappings` 에 없는 3쌍**도 있다: `Brown_Face`, `Brown_Heat_Face`, `ZongBan_Face`(갈색 색소 계열 얼굴 전체 이미지, `hd_ai_contact.jpg` 마지막 줄).

### shape_ai (5개)

- `features.json`: 얼굴 비율 측정 83항목(`name`·`value`·`unit mm`·`start_pt/end_pt` 3D 좌표 · 예 「唇高」).
- `curvenatures.vals` / `fine_` / `moderate_` / `big_curvenatures.vals`: 각 2.2MB 바이너리. 정점별 곡률값으로 **추정**(2.2MB ÷ 4B ≈ 565k, 정점 70,687개와는 맞지 않음 — 형식 **확인 안 됨**).

### hd_ai (131개) — 분석 결과와 마스크

- JSON
  - `result.json`: class 4(衰·色·炎·质) · sub_class 10 · feature 33 · keypoints 91(`face_id`·`name`·`uv`·`vertice`).
    값이 measure API 와 같다(Porphyrin_count 5470, Wrinkles_MJ −558.01 → 1판 리포트 C-2) → **measure API 의 원천 데이터로 보인다**.
  - 그 외 `hd_ai_result.json`, `result_shape.json`·`result_shape_big.json`(함몰 7 · 굵은 주름 8), `rough_wrinkle_bounds.json`(FL·LG·MO·QJ 좌/우 픽셀 범위), `pores_info.vals`(898KB 바이너리), `error.json`(빈 파일).
- 이미지: 모두 **9728×4864**(PNG 8bit L 또는 JPG) + `_M.jpg` 3242×1621 미리보기. 이름 규칙이 세 갈래다(`hd_ai_contact.jpg` 로 눈 확인):

| 갈래 | 파일 | 내용 |
|---|---|---|
| **검출 결과**(선·점) | `wrinkle_bi_gen` · `wrinkle_mei_jian` · `wrinkle_yan_di` · `wrinkle_yu_wei` · `wrinkle_tai_tou` · `wrinkle_horizon` · `wrinkle_vertical` · `wrinkle_mixed` · `rough_wrinkle_mask` · `pores` · `blackhead_mask` · `indentation_mask` · `BulgeMask` | 검정 바탕에 흰 선·점 |
| **평가 영역(채움)** | `wrinkle_*_mask` · `wrinkle_mixed_mask` · `skin_pore_mask` · `skin_dermatograin_mask` · `skin_bump_mask` · `skin_uniformity_mask` · `skin_barrier_mask` · `porphyrin_counter_mask` · `skin_color_mask` · `skin_blackhead_mask` | 흰색으로 채운 ROI. 얼굴 전체형(눈·입 제외) / 이마·코·양볼 / 코 / 눈밑·눈가 등 |
| **평가 영역(외곽선)** | `*_region` | ROI 외곽선 |

⚠ `_mask` 접미사가 일관되지 않다. `rough_wrinkle_mask`·`blackhead_mask`·`indentation_mask` 는 검출 결과인데, `skin_*_mask`·`wrinkle_*_mask` 는 평가 영역이다.
그 밖에 `hd_ai/UvEnhanced.jpg`(텍스처 중복)와 `K1.jpg`·`K2.jpg`(9728×4864, 용도 **확인 안 됨**)가 있다.

## 3. `zip://mask/…` 21종의 출처

| 확인 | 결과 | 근거 |
|---|---|---|
| `render.v3.zips` | `mask` 키 없음(obj·thumb·shape_ai·hd_ai) | 재호출 응답 |
| 4개 ZIP 안 | `Wrinkle_Face`·`Acne_Face` 등 21개 파일명 **0건** | `find` 전수 |
| `obj/data_all.json` | **21개 이름이 모두 여기에 있다** — `Features.<키>.Mask` 값(확장자 `.png`). 예 `Acne→Acne_Face.png`, `Pores→Pore_Face.png`, `Porphyrins→Uv_P_Face.png`, `Senstive→Senstive_Face.png`, `BrownStain→Brown_Tag_Face.png`, `UvStain→Uv_Ex_Tag_Face.png`, `NatureLightStain→Rgb_Tag.png`, `Comedones→Comedones_Face.png`, `DarkCircles→Dark_Face.png`, `BloodShot→Bloodshot_Face.png`, `SkinType→Oil_Face.png`, `T_Oil`/`U_Oil`, `Smoothness→Smooth_Face.png`, `Wrinkles→Wrinkle_Face.png`, 부위 주름 6종 | `A:obj/data_all.json` |
| M3D 프론트 코드 | 3D 페이지 청크 2개 중 `index2-QgInnB3z.js` 만 마스크를 쓴다. 이 청크는 `features[].skin_mappings[{flag,has_mask}]`·`skin_mask` 로 `three_dimensional.masks` 를 찾고, 파일명 끝부분(`split("/").pop()`)을 키로 **ZIP 을 푼 IndexedDB 저장소에서 꺼낸다**. 다른 청크 `index2-D6A07O9z.js` 는 `mask` 문자열 0회, 기본 텍스처 `"Rgb.jpg"` | 공개 JS(`m3d-ai-h5.migamedi.co.kr/assets/…`) 읽기 |
| 이번 응답에 `skin_mappings`/`skin_mask` 있나 | **없다** — render.v3·analyze·measure 어디에도 없음 | 1판 추출본 |

**결론(근거만):** 21종은 `data_all.json`(스캐너 SW 5.10.0 결과)에 이름만 남아 있고, 파일을 담은 묶음은 이 리포트(P2 · edition 2)에 내려오지 않는다.
마스크를 쓰는 화면 경로도 이 리포트의 응답 형태와 맞지 않는다. 같은 역할을 할 수 있는 이미지는 `hd_ai/` 에 있다(§5).

## 4. OBJ 점검 (`A:obj/Rgb.obj`)

| 항목 | 값 | 근거 |
|---|---|---|
| 생성기 | `# Created by Open3D` | 1행 |
| 정점 / 법선 / UV / 면 | v 70,687 · vn 70,687 · **vt 421,263** · f 140,421(전부 삼각형) | 줄 수 집계 |
| 면 형식 | `f a/b/c` — 위치·UV·법선 인덱스가 각각 따로. vt 수 = 면 수 × 3(코너마다 UV) | 첫 `f` 행 |
| `.mtl` | `mtllib Rgb.mtl`·`usemtl Rgb_0` 참조만 있고 **파일 없음**(ZIP 포함 어디에도) | 5행, 562,645행 |
| 텍스처 연결 | OBJ 안에는 없다. M3D 는 셰이더 uniform 으로 따로 넣는다(§0-5) | `td5-Ckj91az8.js` |
| 단위 | 미터로 보인다 — 바운딩 박스 x 0.212 · y 0.214 · z 0.150 | 정점 min/max |
| 축 | **y = 위**(이마 경계 키포인트 y +0.096, 입술 −0.049) · **+z = 정면**(평균 법선 z +0.454) · x 음수 = 피사체의 오른쪽(「右眶下点」 x −0.032) | `hd_ai/result.json` keypoints ↔ 정점 |
| UV 범위 | u 0.140–0.911 · v 0.006–0.994 | vt min/max |
| 크기 | OBJ 텍스트 20.4MB · Normal.png 31.4MB · 광원 텍스처 풀해상도 1.8–13.5MB · `_M` 0.3–1.7MB | 파일 크기 |
| 원본 뷰어 | three.js `WebGLRenderer` + `OBJLoader.loadAsync` + `OrbitControls` · `ShaderMaterial`(uniform `texture1`·`texture2`·`proportion`·`mirror`·`isz`). `mirror` 면 x < proportion 기준 좌우 비교, 아니면 `texture2` 밝기를 alpha 로 덮기. `isz` 는 z 등고선(파란 줄). ZIP·텍스처는 IndexedDB(localforage)에 캐시 | `td5-Ckj91az8.js`, `db-B4cPsCML.js` |
| 원본이 쓰는 텍스처 해상도 | `mappings[].filename`(= `zip://thumb/*_M.jpg`, **3242×1621**)의 파일명을 키로 꺼낸다(`fl()` 함수) | `index2-QgInnB3z.js` |

브라우저 로딩 판단용 사실만 적는다.
- 표준 OBJLoader 가 읽는 형식(삼각형, v/vt/vn)이다. `.mtl` 이 없으면 기본 재질로 로드된다.
- 풀해상도 텍스처 9728px 는 WebGL `MAX_TEXTURE_SIZE` 가 8192 인 기기에서는 그대로 올라가지 않는다. 대상 기기의 실제 값은 **확인 안 됨**.

## 5. 필터 연결표

열 의미:
- **텍스처**: `render.v3` 의 `mappings` flag → 파일(`thumb/*_M.jpg` 또는 `_images/*.jpg`)
- **오버레이**: `hd_ai/` 의 검출·영역 이미지
- **측정 항목**: measure API 의 `features[].id`(1판 C-2)
- **원본 masks flag**: render.v3 `masks[]` 의 flag (파일 없음)
- 「추정」: 이름·병음 유사성이나 눈 확인으로만 이은 것. 표시가 없으면 응답·코드 필드로 직접 이어진 것

| 필터 | 텍스처 (근거: analyze `instances[].atlas`) | 오버레이 (`hd_ai/`) | 측정 항목 | 원본 masks flag(파일 없음) |
|---|---|---|---|---|
| **잔주름** | 잔주름(241) atlas: `gray`·`rgb_cool`·`wrinkles` — `gray`·`wrinkles` 는 type 1 분석 레이어라 **mappings 에 텍스처가 없다** · 사용 가능 텍스처 `rgb_cool`(RgbCool), 편광 `plh`(추정) | 검출: `wrinkle_bi_gen`(코뿌리) · `wrinkle_mei_jian`(미간) · `wrinkle_yan_di`(눈밑) · `wrinkle_yu_wei`(눈가) · `wrinkle_tai_tou`(이마), 합본 `wrinkle_mixed` · 영역: 각 `_mask`·`_region` — **부위 대응은 병음 일치로 추정**(鼻根 BG·眉间 MJ·眼底 YD·鱼尾 YW·抬头 TT. `result.json` feature 제목은 일치) | `basic_241` → measures `Wrinkles_BG/MJ/YD/YW/TT` | `nose_root_wrinkles` · `between_wrinkles` · `below_eye_wrinkles` · `fish_tail_wrinkles` · `forehead_wrinkles` · `wrinkle_face` · `nasal_wrinkles`(추정) |
| **굵은주름** | 굵은 주름(242) atlas: `gray`·`rgb_cool`·`wrinkles_thick`(type 1, 텍스처 없음) → `rgb_cool` | 검출: `rough_wrinkle_mask`(팔자·눈물고랑·광대 선, 눈 확인) · 범위: `rough_wrinkle_bounds.json`(FL·LG·MO·QJ 좌우) · 3D 곡률: `shape_ai/*curvenatures.vals`(추정) | `basic_242` → `Wrinkles_LG/FL/QJ` (hd_ai 에는 마리오넷 `Wrinkles_MO` 도 있으나 measure 에는 없음) | `nasal_wrinkles`(法令纹=팔자, 추정) |
| **함몰** | 노화 atlas 의 `concavity`(type 1, 텍스처 없음) | `indentation_mask`(검출, 추정) · `result_shape.json` Concavity 7부위 | measure 에 없음(hd_ai `Concavity_*` 만) | — |
| **염증·붉은기** | 염증&민감(247) atlas: `red`(Red) · `red2_face`(RedEnhanced) · `red2_heat`(RedHeat) · `red2_ex_face`(RedBlood) · `rgb_cool` · `uv` | 붉은기 검출 이미지는 **없다** — `RedHeat` 텍스처가 히트맵 자체 · 영역: `porphyrin_counter_mask`/`_region`(얼굴 전체형 ROI) | `Red` | `senstive_face` · `bloodshot_face` · `acne_face`(추정) |
| **포르피린** | `uv`(Uv) | 검출 이미지 없음 · 영역 `porphyrin_counter_mask` | `Porphyrin` | `uv_p_face`(data_all `Porphyrins→Uv_P_Face.png`) |
| **색소** | 피부톤(246) atlas: `brown`(Brown) · `brown_heat`(BrownHeat) · `brown_enhanced`(BrownEnhanced) · `plv`(Plv) · `uv`, 그리고 `uv_ex_face`(UvEnhanced, 추정) · mappings 밖 `thumb/Brown_Face`·`Brown_Heat_Face`·`ZongBan_Face` | 검출 없음 · 영역 `skin_color_mask`(이마·코·양볼) | `Pigment` | `brown_tag_face` · `uv_ex_tag_face` · `rgb_tag`(data_all 로 확인) |
| **밝기/톤** | 피부톤 atlas `rgb`·`rgb_cool` · `gray`(type 1, 텍스처 없음) | 영역 `skin_uniformity_mask`(추정) | `Grayscale` · `Pantone` · `SeasonColor` | `dark_face`(다크서클, 추정) |
| **모공** | 피부결(245) atlas: `gray`·`rgb_cool`·`plh`(Plh)·`pore`(type 1) | 검출: `pores`(점, 얼굴 4.4% 덮음) · 영역 `skin_pore_mask` · 블랙헤드 검출 `blackhead_mask` + 영역 `skin_blackhead_mask`(코) | `Pore` (블랙헤드는 hd_ai `Blackhead` count 137, measure 에 없음) | `pore_face` · `comedones_face` |
| **피문** | 피부결 atlas `plh` · `dermatograin`(type 1) | 검출 이미지 **확인 안 됨**(`BulgeMask` 는 皮凸=skin bump, 피문 아님) · 영역 `skin_dermatograin_mask` | `Dermatograin` | `smooth_face`(추정) |
| (참고) 노화 시뮬레이션 | `extras.old` → `_images/Old.jpg`, `thumb/Old_M.jpg` | — | — | — |
| (참고) 유분 | — | — | measure 에 없음 | `oil_face` · `t_oil_face` · `u_oil_face` |

analyze `instances` 의 atlas 목록은 1판 C-2 표에 있다. `comprehensive.atlas` = `rgb_cool, red, brown, gray`.

## 6. 마스크와 3D 텍스처의 좌표계

| 확인 | 결과 |
|---|---|
| 해상도 | 광원 텍스처 풀해상도, `Normal.png`, hd_ai 마스크 모두 **9728×4864**. `_M` 미리보기는 모두 3242×1621 |
| 합성 | `_images/Rgb.jpg` 위에 `wrinkle_mixed_mask`(빨강) · `rough_wrinkle_mask`(청록) · `porphyrin_counter_mask`(노랑)를 덮었다 → `_check/overlay_crop.jpg`. 얼굴 ROI 가 눈·입 구멍까지 사진과 정확히 겹친다. 눈밑·눈가 ROI 도 제자리에 있다 |
| 키포인트 | `hd_ai/result.json` keypoints 91개를 그렸다. `y = v × H`(위→아래)로 그리면 입꼬리·눈꼬리·입술 중앙에 정확히 붙는다(분홍 원). `y = (1−v) × H` 는 어긋난다(초록 원) |
| OBJ `vt` 와의 관계 | 키포인트의 `face_id` 면을 OBJ 에서 찾아보면 정점은 키포인트 `vertice` 와 1mm 안에서 일치한다. `vt.u` ≈ 키포인트 u, **`vt.v` ≈ 1 − 키포인트 v**(예 唇谷 키포인트 v 0.674 ↔ vt 0.329, 发际线中点 0.030 ↔ 0.968). 즉 OBJ 는 표준 OBJ 규약(v 아래→위), 이미지는 위→아래 |
| 결론(사실) | 텍스처·노멀맵·hd_ai 마스크는 **같은 UV 아틀라스**다. OBJ 의 UV 로 붙이면 이미지 원점 규약 차이만 맞추면 된다(three.js `TextureLoader` 기본 `flipY=true` 가 이 규약) |

## 정할 것 (워커가 정하지 않음)

1. **오버레이 소스** — 원본 21종(파일 없음) 대신 `hd_ai/` 검출·영역 이미지를 필터 오버레이로 쓸지. 쓴다면 「검출(선·점)」, 「영역(채움)」, 「외곽선」 중 무엇을 보일지
2. **필터 목록 확정** — 위 표의 행 중 화면 ①에 올릴 것. 붉은기·색소·포르피린은 검출 이미지가 없어서 텍스처를 바꾸는 방식이 된다
3. **추정 연결을 확정할지** — 병음 기반 주름 부위 대응, 피문 검출 이미지 부재, `indentation_mask`=함몰
4. **해상도·용량** — 텍스처를 풀(9728) / `_M`(3242, 원본 뷰어가 쓰는 것) 중 무엇으로 할지. OBJ 20MB 를 그대로 쓸지, glb·압축·간소화로 바꿀지. 대상 큰 스크린 기기의 `MAX_TEXTURE_SIZE`
5. **에셋 공급 방식** — 목업이 `m3d-assets/`(gitignore)를 직접 읽을지, `web/public` 로 복사·가공할지. 이건 커밋 여부와도 이어진다(사용자 본인 얼굴 데이터)
6. **presigned URL 의존** — 링크가 살아 있는 동안 받은 파일로 고정할지(이번에 전부 받아 둠), 실시간 재호출 경로를 남길지
7. **노멀맵·노화 시뮬레이션·좌우 비교(mirror)·등고선(isz)** — 원본 뷰어 기능 중 무엇을 가져갈지

## 확인 안 됨

- 원본 `zip://mask/` 묶음을 내려주는 API·조건(다른 report type·edition 일 가능성)
- `shape_ai/*curvenatures.vals`, `hd_ai/pores_info.vals` 바이너리 형식
- `hd_ai/K1.jpg`·`K2.jpg` 용도, 피문 검출 이미지 유무
- 원본 뷰어에서 type 1 분석 레이어(`gray`·`pore`·`wrinkles` 등)를 어떻게 그리는지
