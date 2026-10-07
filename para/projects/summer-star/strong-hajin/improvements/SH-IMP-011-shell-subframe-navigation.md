# SH-IMP-011 — 셸 하위 프레임 이동 허용(about:blank·about:srcdoc)

상태: 미착수  
생성일: 2026-10-07  
갱신일: 2026-10-07  
출처: WORK-011 운영 결함(메일 본문 medi-ax 빈 칸) 후속

## 문제

medi-ax 셸의 on_navigation 허용 목록이 하위 프레임의 about:srcdoc·about:blank 이동도 취소한다(wry 가 하위 프레임 이동도 같은 훅으로 보냄). 메일 본문은 웹에서 우회했지만 같은 종류의 함정이 남아 있다.

## 기대 결과

- 하위 프레임의 about:blank·about:srcdoc 는 허용, 외부 origin 이동 차단은 그대로

## 진행 관리

- [ ] 셸 변경 + 시험 · dmg 재빌드 묶음에 포함

## 완료 기록

- 아직 없음.
