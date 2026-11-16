# 상태 박스 SPEC/WP 범위 최소 정정

기존 status-box-spec-brief.md와 같은 역할/소유/안전경계. 직전 완료 task_1bca8d3f2090/ctx_11827145689e 산출물에서 코디가 05:12~15에 보낸 msg_8b0c1ac0cbd9/msg_8e028282c03f/msg_ac0b6a17bef2가 미반영. 이것은 새 기능이 아니라 코디가 늦게 명료화한 범위다. 반드시 지금 처리.
1) 이번 수정은 RoomCard._nowBox 4상태만. 호출 _callBox/_callLine, 수락영역, 귀가영역은 그대로다. SPEC003 U3 호출뒤카드 본문·A30은 git show cdde456a 원문 그대로 되돌림(전체파일reset금지), 개정③ 요약/시술명집계/OQ/코드적응/JSON v4 모든 곳에서 호출박스2줄/mm:ss/집계 변경 제거. 호출우선 기존정책은그대로둠. WPv4 A18 호출정의는v3그대로, 이번onlycurrentbox라고명시.
2) 시술중 대표는 서버순서 첫 doing행이고 그행의 title/startedAt/doctor.name을 같이사용. 담당의없으면담당의미정. doing추가행만 외N개. 대기/마취는done아닌행서버순서+기존첫담당의fallback. 시간·담당의가다른시술을설명하면안됨. 앱 표시선택일뿐새업무판정아님. SPEC/JSON 일치.
3) 룸헤더가운데정렬은기록만, 구현요구추가없음. scope변경없음. 이전step로그보존. 보고 status-box-spec-fix-report.md, lint/schema최소정정후각1회. 코드/GitHubwrite/commit/push/merge/하위위임0. 끝에메일check·livepreamble정확ID/outcome/report-path로worker_done1회뒤idle. 다른작업없음.
