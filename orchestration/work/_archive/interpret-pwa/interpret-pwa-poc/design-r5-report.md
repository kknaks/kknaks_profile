# interpret-pwa 시안 r5 결과 보고 — 자막 메신저 말풍선 (D-24)

## 상태: done

## Claude Design 캔버스
- https://claude.ai/artifact/SjB4gGvRZF7sZ2Wz7yaWSd · 버전 `1793001275-5abf`(r4 `1793000949-2cd7`) · 게시 충돌 없음

## 바꾼 화면: `Captions.dc.html` 1개

자막이 그려진 화면은 `Captions`뿐이다. `Interpret-Flipped/Upright` · `State-1~8` · `Menu` · `Glossary`의 자막 영역은 비어 있어서 바꿀 줄이 없다(그대로). 말풍선 규칙은 README와 아래 표로 남겨 frontend가 모든 화면에 같이 쓴다.

| 영역 | 말풍선 | 위치(그 영역을 보는 사람 기준) | 색 |
|---|---|---|---|
| 한국어 영역 | side=me 한국어 원문(내 말) | 오른쪽 · `align-self: flex-end` | `bg-primary-100`(ceramique #e9f5f8) |
| 한국어 영역 | side=them 한국어 번역(상대 말) | 왼쪽 · `flex-start` | `bg-ms-gray-200`(#f3f3f3) |
| 외국어 영역(180°) | side=them 외국어 원문(내 말) | 오른쪽(바로 선 기준으로 짜고 카드째 회전 → 환자 눈에 오른쪽) | `bg-purple-100`(#f8f0ff) |
| 외국어 영역(180°) | side=me 외국어 번역(상대 말) | 왼쪽 | `bg-ms-gray-200` |

- 공통: `max-width: 80%` · 패딩 8px 12px · 모서리 16px, 말한 쪽 아래 모서리만 4px(꼬리 느낌) · 말풍선 사이 8px(이전 줄 간격 10px) · 글자 `text-typo-title-sm-500 text-ms-gray-800` 그대로.
- final:false(외국어 영역 마지막 「Is there any downtime after the」): 말풍선 위치·색은 같고 글자만 `text-ms-gray-600`.
- 자막 내용·줄 수(외국어 8 · 한국어 7)와 D-16(각 영역에는 자기 언어만)은 그대로.
- 상대 말 회색은 `ms-gray-100`(#fbfbfb)이 흰 카드에서 거의 안 보여서 `ms-gray-200`을 골랐다.

## 검증
- 캔버스 `Captions.dc.html` 9276B가 로컬과 같다. 나머지 파일은 r4 그대로.
- 쓴 클래스 `bg-primary-100` · `bg-purple-100` · `bg-ms-gray-200`은 모두 medikit 번들에 있다. 새 hex는 없다.

## 코디가 확인할 것
- SPEC §7.5(자막 배치)에 D-24 말풍선 규칙(위 표)을 더해야 한다. 「바로 보기」 모드에서도 외국어 영역의 오른쪽 = 외국어 원문이다.
- 말풍선 글자가 18px라 140px 원 줄 기준 한 영역에 4~5개쯤 보인다. 더 많이 보이게 하려면 16px(`text-typo-heading-md-500`)을 검토할 수 있다(이번엔 바꾸지 않음).
- **r5 후속(코디 채택 · 버전 `1793001322-415f`)**: Captions 말풍선 글자를 18px `text-typo-title-sm-500`에서 16px `text-typo-heading-md-500`으로 바꿈(15개 모두 · 색·위치·final:false gray-600 그대로).
