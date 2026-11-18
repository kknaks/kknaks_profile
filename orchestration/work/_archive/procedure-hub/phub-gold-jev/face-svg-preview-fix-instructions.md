# 얼굴 SVG 단독 미리보기 수정

사용자가 Orca에서 `_face.svg`를 직접 열었으나 미리보기 실패 화면을 보냈다. 코디가 원본 파일을 그대로 XML 파싱한 결과 첫 줄 Jinja 주석 `{#-`에서 invalid token 오류를 재현했다. 이전 작업의 SVG 자체와 좌표는 이미 코디 검토·관련 12개 시험 통과했다.

## 변경

- 앱 워크트리 `/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev`의 `clinic_chat/consult/templates/_face.svg`만 수정한다.
- 맨 앞 Jinja 주석은 제거한다. 이 주석은 사용자가 삭제를 허용한 영역이다. 필요 설명은 유효 XML 주석으로 대체 가능하다.
- 루트에 `xmlns="http://www.w3.org/2000/svg"`를 추가한다. 기존 `class="cs-face__svg"`, `viewBox="0 0 590 1060"`, `aria-hidden="true"`는 정확히 유지한다. 앞 지시서의 여는 태그 문자 단위 일치 조건은 이번 사용자 미리보기 요구로 대체되며, 세 기존 속성과 viewBox는 그대로여야 한다.
- 그림 path/transform/fill 및 face_coords.py는 변경하지 않는다. 흰 배경을 추가하지 않는다.
- 최종 파일은 손대지 않은 원문 그대로 ET.fromstring으로 파싱되어야 하고, SVG namespace root로 인식되어야 한다. standalone SVG 렌더와 템플릿 include 양쪽을 확인한다. 관련 12개 시험 1회만 실행.
- 래스터 원본/미리보기는 앱 레포에 넣지 않는다. 서버 재시작·커밋·push·PR 금지.

## 보고

보고서 절대경로: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev/face-svg-preview-fix-report.md`.
해당 폴더를 못 찾으면 코디에게 알리고 /tmp 보고서를 명시해도 된다. 이번 live dispatch preamble 명령으로 worker_done을 보낸다. 이전 task/dispatch ID를 재사용하지 않는다.
