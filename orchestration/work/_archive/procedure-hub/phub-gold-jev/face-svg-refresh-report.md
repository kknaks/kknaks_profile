# face-svg-refresh 보고 (task_e8f2bb439b4d)

## 수정 파일 (코드 레포 phub-gold-jev, 커밋 없음)
- clinic_chat/consult/templates/_face.svg — 참고 삼면도 왼쪽 얼굴 패널만 벡터화해 교체(48.8KB, path 41개)
- clinic_chat/consult/face_coords.py — point 17 + pair 27 = 44개 좌표 숫자만 조정

## SVG 제작
- 원본 PNG(1448x1086)에서 패널 테두리(x10-11/602-603, y11/1074) 안쪽 590x1060을 잘라냄 → viewBox와 1:1.
- 얼굴 축 x≈296. 왼쪽 반(1..295열)을 x=295 축으로 뒤집어 붙여 완전 좌우 대칭(pair 자동 대칭과 일치).
- 4배 bicubic 확대 + blur 1.2 + 임계 190(옅은 목 주름 선 포함) → potrace(-t 6 -a 1.0 -O 0.4) → 좌표를 viewBox 절대 좌표로 변환(1자리 소수).
- 채운 윤곽이라 `.cs-face__lines`(fill:none 규칙) 대신 `<g fill="var(--ms-gray-600, currentColor)" fill-rule="evenodd">`를 씀. inline `style=`은 test_t24에서 금지라 쓰지 않음. CSS는 손대지 않음.
- 몸 패널, 테두리, 흰 배경 없음. 투명 배경, 요소는 svg/g/path만.

## 좌표 (원본 픽셀 측정 기준)
머리 꼭대기 y103, 눈썹 y370-392, 홍채 (187,438), 외안각 (133,440), 내안각 (238,450), 비익 x≈246 y≈580, 코 밑선 y600, 윗입술 윗선 y643, 입선 y666 · 입꼬리 x216, 아랫입술 아래선 y702, 턱끝 y805, 귀 x18-75 y405-585.
분할 오버레이 확인 뒤 비근부(041)를 432로, 이주(091)를 귀 주름 (64,500)으로 다시 옮김.

## 렌더 (/tmp/facesvg)
- clean.png — 실제 /face-check HTML(TestClient)+medikit/consult CSS, 점 층을 뺀 얼굴만
- check.png — 같은 페이지 + 점 60개(코드 표시)
- z_eyes.png / z_nosemouth.png / z_jawear.png — 부위별 확대 겹침

## 검사
- XML 파싱 OK, 여는 태그 정확히 일치, raster/href/data:/script/rect/style= 없음
- /tmp/face-before-contract.json과 코드·shape·points 길이 동일. pair 왼쪽 x<0.5, 모든 점이 (0,1) 범위 안
- AST 비교(_p/_pair 인자를 0으로 두고): 다른 곳은 같음. 바뀐 줄 44개 모두 숫자만 다름
- pytest tests/test_consult_sites.py tests/test_consult_page.py: 12 passed. tests/test_consult_*.py 전체: 76 passed

## 미결
- 사용자 눈 확인(§8-4)이 남음. 입술(060)은 아랫입술 옆쪽, 눈꺼풀(025)/윗눈꺼풀(027)은 둘 다 쌍꺼풀선 위(바깥/안쪽)에 둠. 해석이 다르면 숫자만 고치면 됨.
- 프로필 레포의 지시서 위치를 찾지 못해 보고서는 /tmp/facesvg에 둠.
