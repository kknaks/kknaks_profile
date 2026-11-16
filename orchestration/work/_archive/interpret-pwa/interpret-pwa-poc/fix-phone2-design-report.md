# 폰 피드백 2 — designer 결과 보고 (D-28 · D-29 · D-30)

## 상태: done

## Claude Design 캔버스
- https://claude.ai/artifact/SjB4gGvRZF7sZ2Wz7yaWSd · 버전 `1793003735-78bb`(전 `1793001322-415f`) · 게시 충돌 없음 · 게시 전에 live `canvas.json`을 읽어 대조함(바뀐 것 없음)
- 아트보드 17 → 19개

## 바꾼 화면

| 화면 | 결정 | 내용 |
|---|---|---|
| `State-5-Paused.dc.html`(수정) | D-29 | 원 오른쪽에 「초기화」 단추. 한국어만 · 원 줄 안(상담사 쪽) · 회전 없음. medikit Button outlined gray · size s 모양(h33 · px12 · rounded 6 · `bg-ms-white border-ms-gray-300 text-ms-gray-700 text-typo-body-500`) + 되돌리기 아이콘 14px. 원 줄을 3칸 grid(`1fr 92px 1fr`)로 바꿔 원은 가운데 그대로. 원 위아래 안내 · 높이 140px 그대로 |
| `Login-Demo.dc.html`(새로 · 1-4) | D-30 | 로그인 카드: 아이콘 · 「통키」 · 부제 + 「로그인」 solid 50px 하나. 아이디 · 비밀번호 칸 없음 |
| `Language-List.dc.html`(새로 · 2-3) | D-28 | 대기 화면에서 외국어 드롭다운을 펼친 상태. 목록 7개: English(선택 · primary-100 + 체크) · 日本語 · **中国 · 简体中文** · **臺灣 · 繁體中文** · ไทย · Tiếng Việt · 廣東話. 순서는 front `lib/langs.ts`의 `LANGS`. 목록은 외국어 카드 안에 그려 카드와 함께 180° 뒤집힘(환자가 읽는 방향) |
| `canvas.json` | — | 두 아트보드 추가(1-4는 로그인 줄 x=1410 · 2-3은 배치 줄 x=1880) · 줄 제목 폭만 늘림 |

- 다른 화면의 닫힌 드롭다운은 「English」 선택 상태라 표기가 바뀌지 않는다(그대로).
- 「대만어로 출력 중」 같은 한국어 이름(D-28)은 front 문구라 시안에서 따로 그리지 않았다(시안 예시는 영어 기준).

## 검증
- 캔버스와 로컬의 바이트 수가 같다: `canvas.json` 3806 · `State-5-Paused` 5918 · `Login-Demo` 2005 · `Language-List` 7258. 나머지 파일은 전과 같음. `.dc.html` 19개.
- 새로 쓴 클래스(`border-primary` · `text-typo-heading-sm-400` · `text-typo-body-500` 등)는 모두 medikit 번들에 있다. 새 hex는 없다(팝오버 그림자 `rgba(0,0,0,.12)`는 Menu와 같은 값).
- 실명 · 키 없음. 커밋 안 함.

## 코디 · frontend가 볼 것
- SPEC §7.2 언어 표시 이름(D-28)과 §7.3 #5에 「초기화」를, §7.1에 데모 모드 화면을 더해야 한다.
- 실제 medikit ComboBox 펼친 목록은 Popover로 body에 붙어 뒤집히지 않을 수 있다(OQ-010). 시안은 의도(환자 쪽으로 뒤집힘)로 그렸다.
