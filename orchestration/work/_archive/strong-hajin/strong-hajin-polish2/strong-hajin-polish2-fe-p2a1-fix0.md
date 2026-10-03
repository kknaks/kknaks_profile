# [frontend] WORK-009 Phase 2a-1 — 코디 판단 반영 (fix0, 검수 전)

미결 ① — **채팅 경로의 「저장」 실패는 창 안에만** 낸다(SPEC-002 §2.9 「실패하면 서버 문장을 창 안에」). `save_draft` 실패일 때 App 전역 오류 띠(`decideConversationAction` 의 setError)를 세우지 않는다. confirm·reject 의 기존 동작은 그대로.
미결 ② — 낡음 영문 문장은 confirm 과 같은 처리 그대로(범위 밖). 보고에만 남긴다.
테스트 1건(저장 실패 → 전역 띠 없음, 창 안 문구 있음). 보고 subject 「frontend 완료: WORK-009 Phase 2a-1 fix0」.
