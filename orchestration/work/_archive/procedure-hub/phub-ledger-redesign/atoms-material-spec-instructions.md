# 확정본 추가 수정 — 파장 칸을 material_spec 테이블로 (사용자 승인 2026-11-10 · 안 B)

대상: `silver-model/silver/material.csv` → 새 파일 `silver-model/silver/material_spec.csv`

## 할 일
1. `material_spec.csv` 를 만든다(UTF-8 BOM). 칼럼: `material_code` · `property` · `value` · `unit` · `basis`.
   - `property` 는 정해진 값만: `파장` · `농도` · `온도` · `주파수` · `깊이` · `분자량` · `입자 크기`. 이 밖이 필요하면 쓰지 말고 notes 에 후보로만.
   - `value` 는 원문 수치 그대로(범위 `10~50`, 여럿 `1540;1550`, 비교 `≤4` 처럼 원문 비교어는 살린다). 원문에 없는 수치를 만들지 않는다.
2. `material.csv` 의 `wavelength_nm` 값을 전부 `material_spec.csv` 로 옮긴다(property=파장 · unit=nm · basis=그 행의 basis 중 파장이 나온 포인터). 그다음 `material.csv` 에서 `wavelength_nm` 칼럼을 지운다. 다른 칼럼·행은 그대로.
3. 그 밖의 수치: 그 **재료 자체**에 대해 원장이 적은 수치만 추가한다(예: TCA 농도 · 하이드로퀴논 최대 농도 · 냉각 온도 · RF 주파수). 특정 제품·장비·케이스(부위·용량)의 사양은 넣지 않는다(제품·케이스 단계의 일). 각 행 basis 필수. 확실하지 않은 것은 넣지 말고 notes 에 후보로.
4. `atoms-notes.md` 에 절 추가: material_spec 행 수(property 별), 옮긴 파장 행 수, 추가한 그 밖의 수치 목록, 넣지 않은 후보.
5. 다른 파일(mechanism·tissue·method-candidates·modality)은 건드리지 않는다.

## 완료
`material.csv` 에 `wavelength_nm` 이 없고, 옮긴 파장 수 = 기존 wavelength_nm 채워진 행 수인지 확인. `git status` 로 다른 변경 없음 확인 후 코디 터미널에 한 줄:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "atoms material_spec 완료" --enter`
(worker_done 은 다시 보내지 않는다.)
