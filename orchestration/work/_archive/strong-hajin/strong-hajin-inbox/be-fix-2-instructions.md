# [backend] BE 수정 판 2 — BE-2·BE-3 검수 FAIL 2 · WARN 12 (2026-10-06)

**수정 판 1 과 같은 판에서 이어서**(끝난 것이 있으면 그대로 두고 이것까지). 근거 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/review-be23.md` 전부.

## FAIL (최우선 — 보안)
- **F-1 남의 슬랙 메시지 누출 차단**: 방 추가(`add_rooms`) 때 **그 회원 토큰으로 접근 확인**(conversations.info / is_member · DM·그룹 DM 은 회원이 참여자인지) — 확인 안 되면 거절. **팬아웃 대상 = 그 방에 접근이 확인된 회원의 연동만**(team·channel 만으로 고르지 않는다). 이미 들어간 방도 다음 동기화에서 재확인 · 시험: B 가 A 의 DM id 를 넣으면 거절 · 실시간 이벤트가 B 에게 가지 않음
- **F-2 `GET /api/integrations/slack/available-rooms` 신설**(SPEC-008 §4.3 모양 그대로 — 회원 토큰으로 users.conversations · 채널/비공개/DM/그룹DM · 그룹DM 참여자 실명 · 봇 표시 · 이미 고른 것 표시) — FE-b 방 고르기 창이 이걸 쓴다
## WARN
W-1 답장 내구(수정 판 1 과 합침 · 알 수 없는 예외도 실패로) · **W-2 슬랙 다운로드 host 검사 정확히**(`.slack.com` 점 포함 / 허용 목록) · W-3 Socket Mode 처리 실패 시 gap fill 요청 · W-4 단일 소유 advisory lock · W-5 카톡 첨부는 pending 슬롯만 저장(동영상·음성 거절) · W-6 옛 스레드 답글 메우기 · W-7 토큰 로테이션 꺼짐 전제 확인(켜져 있으면 실패 표시) · W-8 메모리 선읽기 한도 · W-9 WS Origin 검사 · W-10 프로필 키 회원 id 정규식 · W-12 시험 빈칸
(W-11 from→sender 는 문서 쪽 — 코디가 SPEC 정리)

끝나면 §9(subject "backend 완료: BE 수정 판 1·2"). 커밋 금지.
