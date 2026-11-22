# [planner] 스펙 3차 — 검수 2차 WARN 6 반영 + 사용자 답

같은 워크트리 · 같은 범위 · 같은 제약(브리프 `day-mobile-v2-spec-brief.md`). 앞 변경 위에서 이어서.

- 검수 2차: `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/review-doc-2-report.md` — **R-1 ~ R-6 전부 반영**

## 사용자 답 · 코디 결정 (2026-11-20)

| # | 결정 |
|---|---|
| R-3 / OQ-N17 | **호출 취소 알림은 그 호출이 완전히 닫힐 때만**(남은 줄 0 · `doctor_call.closed_at` 이 채워질 때) 한 번 보낸다. 같은 때 원래 원장 호출 알림을 닫는다(서버 `read_at` · 앱 OS 알림 센터 원래 푸시 지움 · 웹 OS 알림 `tag` 닫기). 일부 줄 취소 = 알림 없음 · 원래 호출 · 알림 그대로. 재호출 사슬은 「닫히는 호출들」 기준으로 같은 규칙. 「알림 받는 사람」과 「닫을 범위」 문장을 갈라 적어라(R-3 b). OQ-N17 닫음 |
| R-4 / OQ-A59 | Android 알림 채널 이름 = 앱에 이미 있는 글자 「원장 호출」 · 「채팅」(`app/lib/notify/notification_model.dart:16`). 호출 취소는 「원장 호출」 채널 |
| R-1 · R-2 · R-5 · R-6 | 리포트 지적대로 고친다(R-5 「담당의 미정」 줄은 웹 글자 · 기존 앱 글자 안에서 누르는 자리만 정하고 새 글자는 짓지 마라) |
| Firebase | 사용자 준비 끝 — 프로젝트 = 기존 GCP 프로젝트에 Firebase 붙임 · 앱 2개 등록 · `google-services.json` 1벌(두 앱 다) · 서비스 계정 키 dev · prod 각 1개(값 · 경로는 레포 밖 — mobile-deployment §8-1 의 「사용자가 만든다」 를 「준비됨(2026-11-20)」으로만 고침 · 파일명 · 키 id · 프로젝트 id 를 문서에 쓰지 마라) |

## 보고
- lint `--strict` products/day ERROR 0
- 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/spec-3-report.md` — R 번호별 반영 위치 · 남은 막는 OQ
- 커밋 · push · PR · Issue 수정 금지. 완료 보고는 dispatch preamble 의 worker_done 그대로.
