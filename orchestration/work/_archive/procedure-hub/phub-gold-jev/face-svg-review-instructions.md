# [reviewer_code] 얼굴 SVG와 좌표 읽기 전용 검토

이 구현은 사용자가 직접 승인한 E2E 그림 교체다. 이번 작업의 지시서 `face-svg-refresh-instructions.md`와 완료 리포트 `face-svg-refresh-report.md`를 먼저 읽어라. 그림/좌표 구현 파일은 수정하지 않는다.

## 대상과 소유권

- 앱 워크트리 `/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev`에서 `clinic_chat/consult/templates/_face.svg`와 `clinic_chat/consult/face_coords.py`만 읽기 전용 검토.
- 참고 원본은 사용자 Downloads의 미니멀 인체 해부학 삼면도 PNG(왼쪽 얼굴 패널). 원본 파일명은 유니코드 glob로 찾을 수 있다. 참고 PNG·중간 파일을 레포에 넣지 않는다.
- 보고서만 이 지시서 옆 `face-svg-review-report.md`에 쓴다. 다른 코드/문서/서버/워커 상태 변경 금지.

## 검토 항목

1. 루트가 SVG namespace를 선언하고 class="cs-face__svg", viewBox="0 0 590 1060", aria-hidden="true"를 유지하는지, 래스터 임베딩/외부참조/배경 없이 native vector인지 확인.
2. 실제 `consult.css`를 적용한 렌더가 참고 얼굴 패널과 시각적으로 맞는지 직접 view_image로 확인. 패널 테두리/몸통 패널이 없고 눈·눈썹·귀·코·입·턱·목이 살아 있는가. CSS `.cs-face__lines path` 강제 fill:none 때문에 trace가 안 보이지 않는가.
3. `/tmp/face-before-contract.json` 및 `/tmp/face-before-face_coords.py`와 대조하여 60개 SITE 코드/shape/point수 보존, W/H 보존, `_pair` 자동대칭 보존, 좌표 숫자 외 코드 변경 없음을 확인.
4. 깨끗한 그림과 점 겹침 렌더를 직접 확인해 위치가 명백히 잘못된 부위를 지적. 특히 이마/미간/눈꺼풀/내외안각/눈밑/눈물고랑/광대/코등·코끝·비주/입술/입꼬리/턱끝/귀/목을 보라. 개념도 위치이지 임상 시술 지점이라고 평가하지 않는다.
5. 구현자가 실행한 기존 관련 시험을 검토하고 필요시 좁은 검사만 재현. 광범위 테스트·새 테스트 추가는 하지 않는다.

## 결과

PASS/WARN/FAIL과 파일·부위 근거를 보고서에 남긴다. 바로 고치지 말고 수정을 구현 워커에게 돌릴 수 있도록 구체적으로 지적한다. 사용자에게 실물에서 확인받을 부분이 있으면 짧게 기록. 결론과 검증 증거를 정확한 live dispatch preamble의 `worker_done --outcome`으로 보고한 뒤 종료한다. 커밋·push·PR 금지.

최신 추가 요구: 사용자 파일 단독 미리보기를 위해 Jinja 주석 제거와 xmlns 추가를 허용했다. `face-svg-preview-fix-instructions.md`와 완료 보고도 함께 확인. SVG 파일 원문 그대로 XML 파싱 가능해야 한다. 보고서 절대경로는 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev/face-svg-review-report.md`다.
