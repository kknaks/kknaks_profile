# [researcher] 대만 · 대륙 현지 시술명 조사 — 통키 용어집 시드(zh-Hant · zh 구어 별칭)

너는 interpret-pwa researcher 다. 역할(절대경로): `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/roles/interpret-pwa/researcher/role.md` (+ rules · skills · tools · workflow). **read-only** — 리포트 1개만 쓴다. 커밋 금지.

## 무엇
통키 용어집 시드 `/Users/kknaks/orca/workspaces/interpret-pwa/interpret-pwa-poc/back/seed/glossary.json`(157 term · read-only)의 **zh-Hant(대만) 항목은 대륙명을 s2twp 로 바꾼 초안**이라 대만 손님이 실제로 부르는 이름이 없다. 예: 울쎄라 — 대만 손님은 「美國音波」라고 말했는데 시드는 「美版超聲刀」라 통역이 직역했다(사용자 폰 테스트 2026-10-26). 대륙(zh)도 짧은 구어(「超声刀」 · 「热玛吉」)가 울쎄라/슈링크 · 써마지/올리지오 중 어디인지 모호하다.

## 조사할 것 (WebSearch · WebFetch)
1. 시드의 **157 term 전부**에 대해 대만 현지명: 대만 클리닉 · 의원 · 의학미용 매체(.tw 도메인 · 대만 클리닉 블로그 · PIXNET · Dcard 등은 비공식 표시)에서 그 시술/기기/제품을 부르는 이름. 상표명이면 대만 표기(예 Thermage → 鳳凰電波 여부를 확인), 일반 시술명이면 대만 용어. **우선순위**: 기기 리프팅 · 레이저 · 필러 · 보톡스 · 스킨부스터 · 실리프팅 → 그다음 나머지
2. 같은 것을 부르는 대만 별칭(여럿이면 전부 · 많이 쓰는 순)
3. 대륙(zh) 구어 별칭: 「超声刀」 · 「热玛吉」 · 「韩版超声刀」 등 짧게 부르는 이름이 **어느 시술을 가리키는지**(대륙 클리닉 · 新氧 등 출처) — 울쎄라 · 슈링크유니버스 · 써마지FLX · 올리지오 중심
4. 근거: 이름마다 **출처 URL 최소 1개, 가능하면 서로 다른 출처 2개**. 출처를 못 찾으면 「찾지 못함」(지어내지 마라 · 대륙명을 번체로만 바꾼 것을 대만명이라고 쓰지 마라)

## 산출물
`/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-poc/research-tw-names-report.md` — 표: `term id · ko · 지금 시드 zh-Hant · 대만 현지명 · 대만 별칭[] · 출처 수 · 출처 URL · 확신(높음=독립 출처 2+ / 보통=1 / 없음)` + 대륙 구어 별칭 표(`구어 · 가리키는 시술 · 출처`) + 조사 날짜 · 못 찾은 목록. 결정하지 않는다 — 시드 반영 규칙은 코디가 정한다.

## 완료 보고 (두 명령 모두)
코디 handle 은 보고 직전 `orca terminal list --json` 에서 제목에 'Interpretation PWA' 가 든 것.
`orca orchestration send --to <코디> --from <너> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "researcher 완료: 대만 현지명 <찾은 수>/157" --body "…"` + `orca terminal send --terminal <코디> --text "[worker_done] researcher 대만 현지명 조사 완료 — <한 줄>" --enter`
