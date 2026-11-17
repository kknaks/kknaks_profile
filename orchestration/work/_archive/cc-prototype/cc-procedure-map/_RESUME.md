
# 재개 노트 — cc-procedure-map (cc-prototype)

**지금**: 맵 1루프 완료 — 「시술현황 맵」 56화면 · 엣지 79(고아 0) · 메모 173(source 0 누락) · 5053노드 멱등 · 린트(3규칙 제외) 0. 사용자 화면 확인 대기
**다음**: 사용자 피드백 모아 2루프 한 브리프(긴 화살표 얽힘 · 결정 충돌 3곳(U2 · U8 · U12) · 레일 아이콘 등)

세팅: `scripts/new-work.sh cc-prototype cc-procedure-map` · 설정 SSOT `config/projects/cc-prototype.json`
코디handle: `term_5f3a0622-cf65-40e8-bc2f-fdd1174707c9`

프로젝트·회고·당시 문서의 탐색은 이 폴더의 작업 목차(`README.md`)가 맡는다.
`sync-work-links.py`로 생성하며, 종료 후에도 프로젝트에서 같은 작업을 찾을 수 있어야 한다.

## 워크트리



## 1. 지금

열린 것만 둔다. 닫히면 지우고 §5 이력으로 내린다.

- [~] pencil — 와이어 맵(`cc-procedure-map-pencil-brief.md`) · 1절 확인 관문
- 컴포넌트 세트 + 인스턴스로(정정 3)
- [!] **기존 시술현황 페이지(DAY · cc-prototype 등)는 절대 참고 금지** — 원천은 cc 기획안 + 메디킷 키트뿐
- [!] OpenPencil 0.16.0 = 공식 문서(개발판)와 API 다름 · headless PNG 는 Pretendard 를 Inter 로 대체 — 검수 기준으로 쓰지 않는다
- [!] 자동화(CLI·MCP)는 앱 UI 탭이 아니라 보이지 않는 문서를 잡을 수 있다 — 그릴 때 사용자 화면에 뜨는지 먼저 확인

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-11-12 | 캔버스 도구 = OpenPencil 0.16.0(데스크톱 앱 + bun 전역 CLI·MCP) | 사용자 |
| 2026-11-12 | DS = 메디킷 1.4.0, primary = CRM blue `#1d8bff` | 사용자 |
| 2026-11-12 | 토큰 문서 = `reference/2026-11-12-open-pencil/medikit/medikit.fig`(색 변수 29 · 타이포 28 · 그림자 3) | 코디 |
| 2026-11-12 | 컴포넌트는 시술현황에 필요한 것만 먼저 들여온다(전체 40종 아님) | 사용자(추천안 승인) |
| 2026-11-12 | 기존 시술현황 페이지 참고 금지 | 사용자 |
| 2026-11-12 | research §6 기본값 9건 확정(#1 #3 #4 #5 #6 #8 #9 #11 #12) · #2 #7 #10 은 기획 담당자 확인 전 빈 자리 | 사용자 「응 넣어」 |
| 2026-11-12 | 맵 형식 = [화면] ─(버튼)→ [화면] + 화면 옆 정책 · 기획 메모(마커 번호별 원문 인용 + 줄). 와이어 먼저, 컴포넌트는 그 뒤 | 사용자 |
| 2026-11-12 | 맵은 데이터(screens · edges · notes .json) 원본 + 렌더러, `reference/2026-11-12-open-pencil/cc-procedure-map/` · 캔버스는 medikit.fig 「시술현황 맵」 페이지 | 코디 |
| 2026-11-12 | 화면은 메디킷 디자인 입힌 결과물 · 컴포넌트 라이브러리 별도 제작 불필요 · 전체를 한 번에(관문 없음) — `pencil-correction-1.md` · `-2.md` | 사용자 「디자인 된 전체 결과만 있으면 돼」 |
| 2026-11-12 | 컴포넌트까지 만든다 — 화면은 인스턴스(정정 2 의 「선택」을 뒤집음) — `pencil-correction-3.md` | 사용자 「컴포넌트까지 다 넣고 가는거지?」 |
| 2026-11-12 | 구조: 코디 → pencil 리드 → 섹션별 서브에이전트 n. 기본 디자인(컴포넌트 · _lib · 데이터 · layout.json) 먼저, 섹션 병렬, 리드가 합치고 연결 — `pencil-correction-5.md` · 린트 정리도 완료 조건(`-4.md`) | 사용자 |
| 2026-11-12 | **디자인 정본 = 사용자 제공 시안 `reference/2026-11-03-cc-day/screen/시술현황_프로토타입 (1).html`(3차 v11)** — 「기존 페이지 참고 금지」의 예외(사용자가 직접 지정) | 사용자 |
| 2026-11-12 | 컴포넌트부터. 일을 쪼개 리드 + 그룹별 서브에이전트. 린트 오류 · 경고 0 — 대비 규칙과 시안 색이 충돌하면 색 바꾸기 전 코디 질문 | 사용자 |
| 2026-11-12 | 앞 pencil 워커(정정 1~5 누적) 종료 · 새 브리프로 재발주. 산출물(screens 56 · edges 66 · notes 173 · _lib.js)은 남김 | 코디 |
| 2026-11-12 | eval 은 리드만 · 직렬 · 20초 이내 — 병렬 eval 로 앱 고장(Out of bounds memory access) → 앱 재시작, 사용자가 UI 에서 medikit.fig 재오픈 | 코디(워커 질문 답) |
| 2026-11-12 | **앱 모드 eval 금지 → headless(`eval <파일> -w`)** — 앱 WASM 이 생성·삭제 반복에 메모리 오류(3회). 사용자는 결과를 앱에서 연다 | 코디 |
| 2026-11-12 | 린트: 시안 값 그대로 · 앱 설정 `designCheck.disabledRules` = color-contrast · min-text-size · touch-target-size 끔(앱 설정이라 이 PC 에만) | 사용자 「응 꺼줘」 |
| 2026-11-12 | 맵 = 디자인 페이지(시안) 배치 기준 · 컴포넌트 인스턴스 · 화면 → 화면 연결 · 정책 메모(원문 + 줄) — `cc-procedure-map-pencil-map-brief.md` | 사용자 「디자인 페이지 기준으로」 |
| 2026-11-12 | OpenPencil 전용 워커 `pencil` 신설(config · roles/cc-prototype/pencil) — designer 는 DesignSync 용 | 코디 |

뒤집힌 결정은 지우지 않는다. ~~취소선~~ 을 긋고 같은 행에 뒤집은 날짜와 사유를 남긴다 —
지우면 왜 그렇게 갔는지가 사라져서 같은 논의를 다시 한다.

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| pencil 맵 | `term_07bf9667-f34f-4a9a-8aa0-e5a03d5ab36d` | `task_b884ee5e9ad2` | `ctx_4de3b341aaae` | `cc-procedure-map-pencil-map-brief.md` | 완료 · 해제 (run `run_19183a522baf`) |
| pencil v2 | `term_157697f5-19a1-4c11-bc8f-0c991dcc2eef` | `task_fc6b6cd1bc0d` | `ctx_25fe68113c2b` | `cc-procedure-map-pencil-components-v2-brief.md` | 완료 · 해제 (run `run_19183a522baf`) |

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.** 워커 보고는 dispatch preamble 의 값을 따르므로
여기 옛 핸들을 남겨 두면 어느 것이 산 것인지 판단이 안 된다.

## 4. 산출물

- spec PR: <링크>
- code PR: <링크>
- 리포트: `<review-*-report.md>` · `<research-*.md>`
- 커밋: `<sha>` — <한 줄>

## 5. 이력 (최신이 위)

- `2026-11-12` 맵 완료 · 코디 대조(info 4p/6518 · 맵 5053 · screens 56 · edges 79 고아 0 · notes 173 · lint 3규칙 제외 0) · 해제 · 앱 열어 둠
- `2026-11-12` 린트 3규칙 끔 · 맵 발주(앱 닫음)
- `2026-11-12` pencil v2 완료 · 코디 대조(info 1465 · 세트 26 · 변수 64 · lint 55/33/357 · 금지 출처 0) · 해제
- `2026-11-12` 시안 받음 → pencil 종료(worker_done failed · 교체) · 해제 → pencil v2 발주
- `2026-11-12` 정정 1~5 전달 후 사용자 「멈춰」 → 워커 중지 확인
- `2026-11-12` 컴포넌트 발주 보류 → 와이어 맵 pencil 발주
- `2026-11-12` researcher 완료 · 코디 대조(P:L68 · L87/L656 · notify L10 · 56행) 일치 · 워커 해제
- `2026-11-12` 작업 시작 · researcher 발주 · 정정 1(기존 페이지 참고 금지) 전달·수신 확인

이 절은 **재개에 필요한 만큼만** 쓴다. 회고·배운 것은 `SUMMARY.md` 몫이다.
