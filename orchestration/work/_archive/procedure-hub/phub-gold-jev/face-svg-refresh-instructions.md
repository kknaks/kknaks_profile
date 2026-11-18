# [face-svg] 참고 얼굴 패널 SVG 교체와 부위 좌표 조정

너는 이 작업의 구현 워커다. 앞 판 맥락은 없다. 현재 사용자 요구는 이미 승인된 화면 E2E 수정이며, 별도 스펙·WORK 추가나 PR 작업을 하지 않는다. 원래 run의 상담 워커와 이 두 파일의 소유권을 분리해 통지했다. 작업한 두 파일은 사용자가 지정한 기존 앱 워크트리에 직접 남긴다.

## 1. SSOT와 입력

- 최신 사용자 요구: 참고 이미지의 **왼쪽 얼굴 부위만** 네이티브 SVG로 바꾼다. 얼굴 윤곽·눈썹·눈동자·귀·코·입·목과 어깨선을 참고 이미지에 충실하게 유지한다. 몸 앞/뒤 패널·패널 테두리·흰 캔버스는 넣지 않는다.
- 참고 PNG(read-only): `/Users/kknaks/Downloads/미니멀 인체 해부학 삼면도.png` (파일명이 유니코드 분해일 수 있음; glob로 찾기). 원본이나 중간 래스터를 레포에 저장하지 않는다.
- 작업 경로: `/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev`.
- 기존 계약: 같은 문서 폴더의 `SPEC-004-consult-chat.md` §8, `WORK-011-consult-chat.md` 얼굴 부분. 최신 사용자 요구가 우선한다. 도면 자체는 potrace 네이티브 벡터화 가능(설치됨).
- CSS(read-only): `clinic_chat/consult/static/consult.css`. 기존 `.cs-face__lines path`는 fill:none/stroke 규칙을 강제하므로, 채워진 trace path를 쓰면 이 클래스에 넣지 말고 `fill="var(--ms-gray-600, currentColor)"` 등을 적용한 별도 그룹을 쓴다. CSS 수정 금지.

## 2. 반드시 유지할 계약

- 여는 태그 **정확히** `<svg class="cs-face__svg" viewBox="0 0 590 1060" aria-hidden="true">`. xmlns/width/height는 미리보기에서만 추가.
- SVG 네이티브 path, 투명 배경. PNG 임베딩, 외부 파일 참조, script, 캔버스 배경 사각형 금지.
- `face_coords.py`는 `FACE_COORDS` 내부 `_p(x,y)` / `_pair(x,y)`의 **숫자만** 변경. W,H=590,1060, SITE 코드 집합(60), shape(17point/27pair/8area/4line/4none), 함수·타입·주석·나머지 코드는 변경 금지.
- `_pair`는 왼쪽 좌표 한 점만 적고 오른쪽은 자동 대칭. 왼쪽 x<295, 점은 캔버스 내부. 각 부위의 실제 위치와 맞춰 조정한다(이마·미간·눈·안검·광대·볼·코·입술·턱·귀·목·정수리 등).
- 미간·눈·눈썹·내외안각·입술·입꼬리·비주·비근·비익이 해부학적으로 구별되어야 한다. point/pair가 아닌 항목의 빈 points는 그대로.
- 그림은 좌우 대칭을 유지하거나 부위 좌표의 대칭과 시각적으로 어긋나지 않게 정리한다.

## 3. allowed_paths

코드 레포에서 이 두 파일만 변경한다:
- `clinic_chat/consult/templates/_face.svg`
- `clinic_chat/consult/face_coords.py`

보고서는 프로필 레포의 이 지시서 옆 `face-svg-refresh-report.md`에 작성 가능. 다른 앱 파일·CSS·템플릿·테스트·README·커밋·push·PR·서버·기존 워커 상태는 건드리지 않는다. 진행 중인 다른 변경은 절대 되돌리지 않는다.

## 4. 실행

1. 참고 원본과 기존 두 파일을 직접 확인. 필요하면 pillow + mkbitmap/potrace로 왼쪽 얼굴만 벡터화한다. 임시파일은 /tmp에만. 최신 요구는 참고 그림의 얼굴과 닮는 것이므로 단순 얼굴 아이콘으로 대체하지 않는다.
2. 외곽 패널 테두리/노이즈 제거. 기존 SVG 슬롯에 맞춰 선 색/두께를 확인. 눈동자와 눈썹 결은 너무 두꺼워 뭉치지 않게.
3. 새 SVG 위치에 맞춰 44개 point/pair 부위 숫자 조정.
4. 실제 CSS와 같은 선 스타일의 **깨끗한 얼굴 렌더**, 그리고 부위 코드·점이 있는 **좌표 겹침 렌더**를 생성해 직접 view_image로 검토. 모든 점을 켠 그림이 혼잡하면 눈/코입/턱귀 분할 이미지로 확인. 미리보기 PNG·임시 SVG는 /tmp에만.
5. XML 파싱, 정확한 root/class/viewBox, no-raster/투명배경 확인. 수정 전 계약 `/tmp/face-before-contract.json`과 코드/shape/points 길이 동일을 확인. AST 비교 등으로 face_coords의 숫자 외 수정 없음 확인. 해당 앱의 기존 `tests/test_consult_sites.py`와 얼굴 관련 page 테스트를 필요한 범위에서 실행한다. 무관 실패는 분리 보고. 테스트 추가·수정은 하지 않는다.

## 5. 검토 증거와 완료

`face-svg-refresh-report.md`에 수정 파일, SVG 제작 방식, 좌표 조정 개수, 원본과의 매칭, 렌더 경로, 실행한 검사와 결과, 미결을 짧게 기록한다. 사용자 홈 경로를 앱 코드에 넣지 않는다. 프로젝트 코드를 이미지 프롬프트나 외부에 전송하지 않는다.

완료 보고는 **이번 dispatch의 live preamble에 있는 정확한 명령과 task/dispatch ID**로 `worker_done --outcome succeeded|failed`를 보내고 끝낸다. 오래된 다른 브리프의 코디 핸들/run을 쓰지 않는다. 질문도 이번 preamble의 ask를 사용한다. 워커는 커밋·push·PR하지 않는다.
