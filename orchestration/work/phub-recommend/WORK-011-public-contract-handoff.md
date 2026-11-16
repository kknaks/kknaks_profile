# WORK-011 선택 관계 공개 계약 인계

2026-11-02 · 기준 Hub HEAD `2edc190` + 미커밋 변경 · 격리 Gold build hash `567677edfe7123e9`

## 앱 WP-4가 호출할 계약

- REST `POST /procedure-hub/gold/pairs/selected`; MCP `selected_pair`. 입력: 확정 단위 시술 `a,b`, 선택 `prior`, `sub_condition`, `include_conditional`, `sections`, `cursor`. 응답: `build.build_hash`, `request`, `pair_scope{a,b,build,complete,status}`, `resolved`, `claims[]`, `alternatives[]`, `more`, `next_cursor`. 호출당 64 KiB 상한. `truncated`/`next_cursor`는 같은 build·정규화 요청으로 이어 읽고 `complete=true` 전에는 지원 완료나 부재를 선언하지 않는다.
- REST `POST /procedure-hub/gold/global-claims`; MCP `global_claims`. 입력: `scope`, 선택 `a,b,condition,cursor`. 응답: `build.build_hash`, `request`, `scope_complete`, `status`, `global_claims[]`, `more`, `next_cursor`. 호출당 32 KiB 상한. Q139 scope는 `scope:all#evidence#step8_notes[26]`이며 R8 edge 조회와 별개다.
- 공개 status는 `found|empty|truncated|error`. 사실 인용은 각 행의 `quotable=true`, 출처 `file/path`, 선택 pair/조건의 `applies_to`, 범위 `complete=true`를 함께 확인할 때만 가능하다. `quotable=false`인 다른 전역 원문은 지원 사실로 세지 않는다. 공유 claim은 실제 owner edge와 선택 edge를 모두 보존하며, owner 범위가 선택 pair를 지지하지 않으면 인용하지 않는다.
- REST/MCP는 같은 selected 코어를 사용한다. REST의 4xx와 MCP ToolError는 앱에서 같은 미수신/오류 상태로 정규화한다.

## 현재 증거와 남은 관문

- 격리 메모리 Gold에서 `U5-110/U5-020` 선택 쌍과 Q139 전역 scope의 `build_hash`가 모두 `567677edfe7123e9`이다. 전역 550행은 9쪽으로 전량 재조립했고, claim/대안·조건·출처 음성 시험 및 기존 페이지 회귀는 [Hub 6차 코드 검수](review-hub-selected-code-v6.md)에 기록됐다.
- 사용자 서버 `127.0.0.1:18005`의 새 선택 관계 경로는 현재 HTTP 404다(읽기 전용 호출). 이 서버와 격리 빌드는 동일 코드라고 간주하지 않는다.
- 앱 WP-4 **코드 작성**은 위 고정 응답 계약과 격리 fixture를 사용해 진행한다. 실제 서버·앱의 동일 build hash 및 QID/50문항 재생은 기능 활성화 전에 확인한다. 사용자 서버·포트·컨테이너 갱신은 이 인계에 포함되지 않는다.
