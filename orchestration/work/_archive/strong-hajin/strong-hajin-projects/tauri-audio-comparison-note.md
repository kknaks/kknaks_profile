# SPEC-006 추가 확인 — 음성 입력 차이

사용자가 두 제품의 음성 입력 차이를 질문했다. 코디가 실물 비교한 사실:
- task_management app/front/src/features/meetings/hooks/audioCapture.ts: getUserMedia + MediaRecorder, 250ms. isTypeSupported로 webm/opus → webm → mp4 → ogg/opus 후보 선택, 없으면 기본값. 선언 format:auto. pause/resume 존재.
- Strong_hajin frontend/src/features/meetings/microphone.ts: 같은 웹 API, 250ms. audio/webm;codecs=opus 고정. 16kHz/mono 요청·선언(실제 장치 출력 보장과 구분). 64KB 청크 분할. 핸들에 stop만 있음.
- Strong_hajin frontend/src/features/meetings/stream.ts: 주석 및 계약상 pause/resume 범위 밖. task_management useMeetingStream.ts는 pause/resume·트랙 ended 처리가 있음.
- 양쪽 내 마이크만, 시스템 오디오 캡처 아님.

스펙에 반드시 현재/변경을 구분하라. DEC-005의 일시정지·재개 요구를 기존에 있는 기능이라고 취급하면 안 된다. 새 제어를 도입할지, 기존 기능이 생길 때까지 조건부 계약인지 미결/범위 영향을 명시. 포맷 fallback은 FE 한 줄 변경으로 완료라고 하지 말고 서버 Soniox 설정·원본 저장 수용과 함께 확인. 플랫폼별 지원 여부는 실측 전 보장 금지.
