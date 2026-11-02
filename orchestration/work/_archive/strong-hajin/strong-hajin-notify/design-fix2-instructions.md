# [architect] 알림 시안 수정 2 — DEC-010 「시안 고칠 것」 반영

정본: `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/projects/summer-star/strong-hajin/10-decision/decision-010-notifications.md` 「## 시안 고칠 것」 ①~⑥ · 사건 × 관계 표. 같은 방식(시작 전 원격=로컬 확인 · Claude Design `7e839512` 쓰기 · 로컬 사본 같은 바이트 · cmp). 사용자 승인 받음(2026-10-08 「응 가자」).

## 바꿀 것
1. 알림 목록 꼬리표 신설 — ① 「메일」(To/CC 어디에도 내가 없는 메일) · ② 「공유받음」(회의 공유 받은 사람) · ③ 「배정자」(담당 수락·거절을 받는 배정자). 목데이터에 ①③ 각 한 줄씩 더한다(가상 인물)
2. ④ 목데이터 a07 — CC 가 완료 보고를 받는 줄을 **요청자 꼬리표의 완료 보고 줄**로 바꾼다
3. ⑤ 목데이터 a19 — 회의 공유 줄 꼬리표 「참석자」 → 「공유받음」
4. ⑥ 설정 업무 `change` 설명 — 「내 업무의 기한·조건이 바뀌거나 취소·재개되면」 (철회·취소·재개·취소 제안이 이 항목으로 온다 — 표 참고)
5. 안 읽음 수·필터 수·날짜 구간이 늘어난 줄과 맞게

## 손대지 않는 것
- 틀·사이드바(점)·다른 화면·다른 설정 항목

## 끝나면
- `design-change-3.md` (같은 폴더) — 바꾼 것 · 파일별 바이트·sha256 앞 12 · cmp
- 커밋·push 금지
- 완료 보고는 브리프 §9 와 같은 두 명령. 코디handle `term_aa9fb9af-eed1-45ee-baad-95e52082321d` · subject 「architect 완료: 알림 시안 수정 2」 · text 「[worker_done] architect 완료 — 알림 시안 수정 2. 상세는 design-change-3.md」
