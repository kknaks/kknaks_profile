# 얼굴 SVG·좌표 읽기 전용 검토 보고 (task_98a3158093de)

**결론: PASS** (막는 문제 없음. 작은 WARN 3개는 사용자 확인용이며 지금 고칠 필요는 없음)

대상: `clinic_chat/consult/templates/_face.svg`, `clinic_chat/consult/face_coords.py` (앱 워크트리 phub-gold-jev). 파일은 수정하지 않음.
검토 렌더(세션 scratchpad): `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-clinic-chat-phub-gold-jev/05a193af-68cd-4ce5-b793-f6b707dc6739/scratchpad/` 의 side.png(참고 패널과 나란히), clean.png, check.png, z_eyes.png, z_nosemouth.png, z_jawear.png, standalone.png

## 1. SVG 루트·native vector — PASS
- 원문 그대로 `ET.fromstring` 성공. root `{http://www.w3.org/2000/svg}svg`, attrib가 정확히 `class="cs-face__svg"`, `viewBox="0 0 590 1060"`, `aria-hidden="true"`.
- 요소는 svg 1 / g 1 / path 41개뿐. `<image`, `href`, `data:`, `<script`, `<rect`, `style=`, `url(`, Jinja 토큰(`{#`, `{{`, `{%`) 모두 없음. 배경 없음.
- `face_check.html`의 `{%- include "_face.svg" %}`가 그대로 동작함(아래 page 시험).

## 2. 렌더와 참고 패널 대조 — PASS
- 실제 medikit+consult CSS로 그린 /face-check 렌더(clean.png)를 참고 PNG 왼쪽 패널 crop(Downloads 원본과 cmp 결과 같음)과 나란히 봄. 머리 윤곽·눈썹 결·눈(홍채/동공 하이라이트/쌍꺼풀선)·귀(안쪽 주름 포함)·코(비익/콧구멍)·입술·입꼬리 점·턱·목·어깨선이 모두 있고 비율·위치가 같음.
- 패널 테두리, 몸통 패널, 흰 캔버스 없음.
- trace는 `.cs-face__lines`가 아니라 `<g fill="var(--ms-gray-600, currentColor)">` 안에 있어서 `fill:none` 규칙에 걸리지 않음. 앱에서는 회색 채움으로 보임.
- 단독 렌더(Chrome으로 파일을 직접 엶)는 currentColor(검정)로 정상 표시됨.

## 3. 좌표 계약 — PASS
- `/tmp/face-before-contract.json`과 현재 코드·shape·points 길이가 같음(60개; point 17 / pair 27 / area 8 / line 4 / none 4).
- W,H = 590,1060 유지.
- 모든 pair가 왼쪽 x<0.5이고 오른쪽 = 1−x, y가 같음(`_pair` 자동 대칭 유지). 모든 점이 (0,1) 안에 있음.
- `/tmp/face-before-face_coords.py`와 AST 비교(숫자 상수를 0으로 두고): 같음. `diff` 결과 바뀐 줄은 `_p`/`_pair` 인자 44줄뿐이고 주석·함수·타입은 그대로.

## 4. 부위 위치 (개념도 기준) — PASS, WARN 3
명백히 잘못 놓인 부위는 없음. 세로 중심선 순서 정수리130 → 이마262 → 미간394 → 비근부432 → 코등505 → 코555 → 코끝580 → 비주598 → 인중623 → 윗입술652 → 입666 → 하순686 → 턱745 → 턱끝788 → 턱밑830 → 목905가 그림과 맞음(턱 아래 윤곽 y≈805, 입선 y≈666).
- 눈: 018 홍채 중심, 031 내안각·032 외안각이 눈 양 끝에 있음. 028 하안검이 아래 속눈썹선, 034 애교살→024 눈밑→033 눈물고랑(안쪽 아래) 순서도 맞음. 026 안와상부는 눈썹과 쌍꺼풀선 사이, 029는 눈썹 위.
- 코·입: 039 비익이 콧볼 바깥선, 040 비주가 코 밑선, 067 입꼬리가 입꼬리 점 위, 046 팔자는 콧볼에서 입꼬리로 가는 선 위, 120 마리오네트는 입꼬리 아래.
- 귀·턱: 089 이개가 귓바퀴 안, 091 이주가 귀 안쪽 주름, 090 이하부가 귓불 아래 얼굴선 안, 086 구레나룻이 귀 앞 머리선, 016 관자놀이가 귀 위 눈썹 높이. 076 사각턱과 075 턱선은 턱 윤곽선 위.

WARN (구현 워커에게 넘길 수 있는 선택 수정, 숫자만 바꾸면 됨):
- W1 SITE-025 눈꺼풀 (160,417)과 SITE-027 윗눈꺼풀 (212,415)이 둘 다 쌍꺼풀선 위에 있어서 바깥/안쪽으로만 구분됨. 해석은 사용자가 확인. 대안: 025를 위 속눈썹선 가운데(≈187,425)로 옮기기.
- W2 SITE-030 눈꼬리 (118,430)가 외안각 032 (133,440)의 바깥 위쪽, 눈 그림 밖에 있음. 틀린 위치는 아니지만 확대하면 떠 보임. 원하면 (124,436) 근처로 바짝 붙이기.
- W3 SITE-060 입술 (262,678)이 아랫입술 옆쪽에 있음. 057/062/064가 중심선을 차지해서 생긴 선택으로 보이며 개념상 문제 없음.
- 그림 참고: 원본 아랫입술 아래의 아주 옅은 턱 주름선(y≈718)은 임계값 때문에 빠짐. 개념도로는 영향 없음.

## 5. 시험 — PASS
- 구현자 보고(refresh 12 passed, consult 전체 76 passed; preview-fix 12 passed)를 확인함.
- 좁게 재현: `uv run pytest -q tests/test_consult_sites.py tests/test_consult_page.py` → 12 passed. 새 시험은 추가하지 않음.

## 사용자에게 실물 확인받을 것
- W1(눈꺼풀/윗눈꺼풀 구분)과 W2(눈꼬리 위치) 해석.
- 앱 렌더는 Chrome에서만 봄. `fill="var(...)"` 프레젠테이션 속성은 다른 브라우저(Safari)를 쓰면 회색으로 나오는지 한 번 확인.
