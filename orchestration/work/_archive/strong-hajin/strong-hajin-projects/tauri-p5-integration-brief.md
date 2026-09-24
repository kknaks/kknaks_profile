# WORK-006 Phase 5 — 제품 통합 재측정·자동검증

## 목적

Phase 4 웹 배선이 들어간 현재 코드에서 제품판 검증을 준비하고, 오늘 실행 가능한 자동·정적 검증과 내일 필요한 실기 측정을 분리해 기록한다. 설치 파일 발행이나 운영 서버 배포는 이 작업에 포함하지 않는다.

## 작업 위치

- 코드 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`
- 결과 보고서: `orchestration/work/strong-hajin-projects/tauri-measurement-r2.md`
- 참고: `work-006-tauri-wrapper.md` Phase 5, SPEC-006 v0.2.1, Phase 2 측정 기록, Phase 4 최종 검수 보고서

## 허용 범위

- Phase 4 변경 상태를 기준으로 tsc, 관련 테스트, 전체 프론트 검증을 재실행한다.
- AC-T01~T07, T19, T26~T30, T32, T36~T41, T43의 코드·테스트 연결을 표로 점검한다.
- M-11~M-14, M-9, M-2b, M-6, M-5의 제품판 증거 표를 만들고, 실제 장비·서버·설치가 필요한 칸은 `미측정/내일 실기 필요`로 명시한다.
- M-1, Windows, 운영 origin, 실제 절전·마이크·서버 E2E를 통과로 쓰지 않는다.
- Phase 4 범위 안에서 실제 결함이 자동검증으로 재현될 때만 수정 제안을 보고한다. Phase 5에서 임의로 코드를 고쳐 통과 처리하지 않는다.
- 커밋·push·PR·Release·배포·비밀값 열람 금지.

## 보고서 필수 내용

1. 실행 명령과 결과(성공/실패/기준선 불안정 구분)
2. AC 21건별 증거 상태와 미측정 이유
3. 제품판 측정표(M-9, M-2b, M-5, M-6, M-11~M-14)
4. Phase 4 이월 WARN(screen wiring test, open_external 사용자 표시, M-1) 추적
5. 다음 Phase 6a로 넘길 차단·미결 목록

## 완료 보고

worker_done으로 변경 파일과 검증 수치, `미측정` 항목을 요약한다. 이 작업은 실기 설치 검증 완료를 의미하지 않는다.
