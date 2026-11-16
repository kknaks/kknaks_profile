# interpret-pwa 시안 결과 보고

## 상태: done

## Claude Design 프로젝트 — id · 이름 · 화면(파일) 목록

- 이름: **Interpret PWA**
- URL: https://claude.ai/artifact/SjB4gGvRZF7sZ2Wz7yaWSd (id `SjB4gGvRZF7sZ2Wz7yaWSd`) · 마지막 버전 `1792999606-635d`
- 형태: **Claude Design 「Design」 캔버스**(claude.ai artifact). 원래 브리프의 「Claude Design 프로젝트」(claude.ai/design project uuid)와 형태가 다르다. 이유: 이 세션의 DesignSync 도구는 *디자인 시스템* 프로젝트만 만들 수 있고, 화면 시안 제작에는 쓰지 말라고 명시돼 있다. 화면 시안은 Design 캔버스로 만들게 되어 있다. 사용자는 캔버스에서 화면을 하나씩 직접 고칠 수 있다(WYSIWYG · 화면마다 파일 하나).
- 공유: 비공개로 만들어졌다(소유자 = 사용자 계정). 다른 사람이 보려면 페이지 Share 메뉴에서 공유해야 한다.
- 로컬 사본: `interpret-pwa-poc/design/`(`project/` = 캔버스 파일 경로 그대로 · `README.md`)

| # | 파일 | 화면 |
|---|---|---|
| 1-1 | `Main.dc.html` | 로그인 · 기본 |
| 1-2 | `Login-Error.dc.html` | 로그인 · 오류(401) |
| 1-3 | `Login-Locked.dc.html` | 로그인 · 잠금(429) |
| 2-1 | `Interpret-Flipped.dc.html` | 통역 · 외국어 영역 뒤집힘(기본) · 인터랙티브(회전 아이콘 누르면 전환) |
| 2-2 | `Interpret-Upright.dc.html` | 통역 · 외국어 영역 바로 보기 · 인터랙티브 |
| 4 | `Captions.dc.html` | 자막 배치 · 대화 3줄 + 진행 중 1줄 |
| 3-1 | `State-1-Start.dc.html` | #1 시작 전 · 오버레이 |
| 3-2 | `State-2-Error.dc.html` | #2 오류 |
| 3-3 | `State-3-Connecting.dc.html` | #3 연결 중 |
| 3-4a | `State-4a-Speaking-Foreign.dc.html` | #4 영어로 출력 중 |
| 3-4b | `State-4b-Speaking-Korean.dc.html` | #4 한국어로 출력 중 |
| 3-5 | `State-5-Paused.dc.html` | #5 멈춤 |
| 3-6 | `State-6-Listening-Korean.dc.html` | #6 한국어 듣는 중 |
| 3-7 | `State-7-Listening-Foreign.dc.html` | #7 외국어 듣는 중 |
| 3-8 | `State-8-Idle.dc.html` | #8 대기 |
| 5-1 | `Menu.dc.html` | 햄버거 메뉴 |
| 5-2 | `Glossary.dc.html` | 용어집 모달 |

17개 화면 · 390×844. 캔버스는 행 4개(로그인 / 배치·자막 / 상태 #1–#8 / 메뉴·용어집)에 제목 메모와 색 규칙 메모가 있다.

## 화면 대조 — SPEC-001 §7 항목별 있음/없음

| SPEC | 항목 | 시안 | 비고 |
|---|---|---|---|
| §7.1 | 제목 「통역」 · 아이디 · 비밀번호 · 로그인 단추(가득) · 오류 한 줄(red) | 있음 | 401 = 입력칸 테두리 red + 한 줄 · 429 = red-100 박스(시계 아이콘). 아이디 칸은 비움 |
| §7.1 | 네트워크 실패 「서버에 연결하지 못했어요」 | 없음(별도 화면 안 만듦) | 1-2와 같은 모양에 문구만 다름 |
| §7.2 | 헤더 햄버거(뒤집히지 않음) | 있음 | |
| §7.2 | 외국어 영역: 드롭다운 · 화면 전환 아이콘 · 안내 · 자막, 기본 180° | 있음 | 아이콘은 사용자 요청대로 **회전 화살표**(기기 + 원형 화살표 두 개). ⇅는 쓰지 않았다 |
| §7.2 | 뒤집힘 ↔ 바로 보기 | 있음(2-1 · 2-2) | 바로 보기에서는 아이콘 단추를 primary-100으로 칠해 「기본이 아님」을 보여 줌(제안) |
| §7.2 | 가운데 원 줄 고정 높이 · 두 영역 반씩 | 있음 | 원 줄 196px |
| §7.3 | #1 시작 전 오버레이 「탭해서 통역 시작」 + 외국어 「Tap to start」 | 있음 | 오버레이를 위아래로 나눠 위쪽(외국어)은 뒤집어 놓음 |
| §7.3 | #2 오류 bg-red · 오류 문구 + [다시 연결] · 외국어 ErrorIcon + 「Connection error」 | 있음 | 한국어 문구 「연결이 끊겼어요」는 예시. 실제는 오류 종류별 문구 |
| §7.3 | #3 연결 중 gray-300 · 「연결 중…」 · 「Connecting…」 | 있음 | |
| §7.3 | #4 출력 중 · 외국어 = purple / 한국어 = primary · 맥박 | 있음(4a · 4b) | 맥박은 링 두 겹으로 표현 |
| §7.3 | #5 멈춤 gray-300 · 「멈춤 · 원을 눌러 다시 듣기」 · 「Paused」 | 있음 | |
| §7.3 | #6 한국어 듣는 중 primary · 음량 크기 | 있음 | 외국어 영역 안내 없음(SPEC 「—」 그대로). 크기 1.3배 예시 |
| §7.3 | #7 외국어 듣는 중 purple · 「영어 듣는 중」 · 「Listening」 | 있음 | |
| §7.3 | #8 대기 gray-400 · 「말씀하세요」 · 「Please speak」 | 있음 | |
| §7.5 | 각 영역에 자기 언어만 · final:false 흐림 · 최신이 읽는 쪽 끝 · 빈 번역은 줄 없음 | 있음 | 진행 중 영어 줄은 한국어 영역에 줄이 없음 |
| §7.6 | 햄버거 → Popover · 용어집 · 로그아웃 | 있음 | |
| §7.6 | 용어집 BaseModal 「용어집 · 〈언어〉」 · 표 3칸 · 닫기 | 있음 | 실제 matrix(`2026-07-01-reviewed-v5`, 158행 · 공개)에서 카테고리마다 첫 행 15개를 넣음 |
| §7.6 | `loaded=false` 문구 | 없음 | 모달 표 자리에 한 줄만 들어감 |

### 브리프 §8 검증

| 항목 | 결과 |
|---|---|
| 프로젝트에 브리프 화면 목록이 전부 있다 | 통과: 위 17개(로그인 3 · 배치 2 · 상태 8(+#4 두 벌) · 자막 1 · 메뉴 1 · 용어집 1) |
| 로컬 `design/` 사본이 프로젝트와 같다 | 통과: 캔버스 `project/` 파일 23개와 로컬 23개의 경로 · 바이트 수가 모두 같음(`list scope=files` 대조) |
| medikit + ceramique 테마 토큰만 쓴다 | 통과: 쓴 색 · 글자 클래스 38개 모두 `_ds_bundle.css`에 있음(빠진 것 0). 클래스 밖 색은 ① 원 링 `rgba` = primary · purple · red · gray-400 토큰 값에 투명도만 준 것 ② 카드 그림자 `rgba(0,0,0,.04)` = ccc 시안과 같은 값 ③ 링크색 `#2498bd/#1d7f9e` = ccc 시안 helmet과 같은 값 ④ 오버레이 위 흰 선 `rgba(255,255,255,…)` |
| 가짜 값만(실명 · 키 0) | 통과: 사람 이름 · 계정값 · 키 없음. 로그인 칸은 빈 placeholder. 자막은 지어낸 상담 문장, 용어는 공개 용어집 실데이터 |
| 기존 ccc 프로젝트는 읽기만 | 통과: ccc 프로젝트는 열지 않음. 로컬 git 사본(`cc-prototype origin/main:_archive/cc/design/`)만 읽음 |

## 제안 · 코디가 확인할 것

1. **색: SPEC §6과 충돌.** SPEC §6은 「`data-product` 두지 않음 · medikit 기본 파랑」이다. 시안은 사용자 피드백대로 `data-product="ceramique"`(primary `#2498bd`)를 쓴다. SPEC §6 · §7.3의 「primary」 정의를 고쳐야 한다. 구현 때는 `ceramique-theme.css`를 가져오고 루트에 `data-product="ceramique"`를 둔다.
2. **외국어 색 = `purple`(#ac47ff).** 근거: ① SPEC §7.3 기본값과 같다. ② ccc 「Ceramique 의사 모바일」에서 primary 옆 두 번째 강조색으로 쓴다(「다음 환자」 · 헤더 점). ③ medikit 토큰에 실재한다. ④ 청록 #2498bd와 색상과 명도(상대휘도 약 0.27 대 0.19)가 모두 달라 구분된다.
3. **화면 전환 아이콘**: 기기 사각형 + 시계 반대 방향 원형 화살표 두 개(인라인 SVG · 24px · stroke 1.8). medikit에 없는 아이콘이라 인라인(SPEC §7.2 그대로).
4. **시안에서 더한 것(SPEC에 없음 · 결정 필요)**: 로그인 카드 위 말풍선 아이콘과 부제 「상담 통역을 시작하려면 로그인하세요」 · 원 안 글리프(듣는 중/대기 = 마이크, 출력 중 = 스피커, 멈춤 = ‖, 연결 중 = 점 셋, 오류 = !) · 외국어 안내 앞 색 점(외국어 = purple · 한국어 출력 = primary · 회색 상태 = gray-600) · 용어집 모달 부제 「158개 · 읽기 전용」 · 메뉴 「로그아웃」 빨간 글자.
5. **대비(WCAG) 주의**: SPEC §7.5의 `final:false` = `text-ms-gray-500`(#cfcfcf)는 흰 바탕에서 약 1.6:1이라 거의 안 보인다. 시안은 SPEC대로 뒀다. `text-ms-gray-600`(약 2.6:1)이나 더 진한 값을 제안한다. `text-red` on `bg-red-100`(잠금 · 오류 박스)도 약 3:1이다(ccc 시안과 같은 조합).
6. **medikit JS 번들이 없음**: Button · Input · ComboBox · Popover · BaseModal은 medikit 1.4.0 `dist/index.js`의 클래스 값(Input xl = h50 · rounded 8 · border gray-300 / Button solid blue = bg-primary · text-white · h50 · rounded 8 등)을 옮긴 마크업이다. 실제 컴포넌트를 캔버스에 마운트하려면 medikit을 Design System으로 등록해야 한다(지금은 계정에 없음).
7. 출력 중(#4) 원은 「고정 크기」, 듣는 중(#6 · #7)은 1.3배 예시, 대기는 SPEC 「작게」를 따라 100px이다(기본 96px · 듣는 중 124px).
8. 네트워크 실패 로그인 · 용어집 `loaded=false` · 오프라인 화면(§8)은 시안에 없다. 필요하면 추가한다.
