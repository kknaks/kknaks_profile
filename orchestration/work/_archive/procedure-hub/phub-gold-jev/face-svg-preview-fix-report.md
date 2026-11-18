# face-svg 단독 미리보기 수정 보고 (task_42edf2cf7d77)

## 수정 파일
- `clinic_chat/consult/templates/_face.svg` (앱 워크트리 phub-gold-jev, 커밋 없음)

## 변경
- 맨 앞 Jinja 주석(`{#- … -#}`, 3줄)을 지움. XML 주석으로 바꾸지 않음. 한글 주석이 `<!-- -->`로 들어가면 페이지 출력에 그대로 실리고 T17(템플릿 한글 0, Jinja 주석만 예외) 시험이 깨지기 때문.
- 루트를 `<svg xmlns="http://www.w3.org/2000/svg" class="cs-face__svg" viewBox="0 0 590 1060" aria-hidden="true">`로 바꿈. 기존 세 속성 값은 그대로.
- `<g fill=…>` 이하 path 41개는 바이트 단위로 같음(수정 전 사본과 비교함). face_coords.py는 손대지 않음. 흰 배경 없음.

## 확인
- 고치지 않은 원문 그대로 `ET.fromstring`: root tag `{http://www.w3.org/2000/svg}svg`, attrib {class, viewBox, aria-hidden}, SVG namespace path 41개.
- 단독 렌더: Chrome headless로 파일을 직접 열어 /tmp/facesvg/standalone.png 확인. CSS 변수가 없으니 currentColor(검정)로 그려짐.
- 템플릿 include 렌더: TestClient의 /face-check + 실제 CSS → /tmp/facesvg/check2.png. 회색 선과 점 71개 겹침이 전과 같음.
- `uv run pytest -q tests/test_consult_sites.py tests/test_consult_page.py`: 12 passed (1회).

## 미결
- 없음. 단독 미리보기에서는 선이 검정, 앱에서는 --ms-gray-600 회색으로 보임(fill 변수 fallback 동작).
