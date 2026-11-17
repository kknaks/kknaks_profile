# pencil 정정 1 — 2026-11-12 (사용자 지시)

**화면은 회색 와이어가 아니라 메디킷 디자인을 다 입힌 화면이다.** 맵 형식([화면] ─(버튼)→ [화면] + 정책 메모)은 그대로.

브리프에서 바뀌는 것:
- §7 「메디킷 색 · 컴포넌트를 입히지 마라」 → **삭제.** §6-4 와이어 스타일(회색 박스) → **삭제.**
- 화면 안 요소는 **메디킷 컴포넌트 인스턴스**로 짓는다. 만드는 법은 보류된 브리프 `cc-procedure-map-pencil-components-brief.HOLD.md` §3(이름 규칙 계약) · §6-2~4(키트 소스에서 값 · 변수 바인딩 · 스크립트 · 멱등)를 그대로 따른다. 키트: `/Users/kknaks/git/harness_works/medikit/src/ui/` + 스크린샷 `ds-bundle/_screenshots/`.
- 컴포넌트는 `medikit.fig` 의 새 페이지 「components」 에, 스크립트는 `reference/2026-11-12-open-pencil/medikit/components/` 에(allowed_paths 추가). 「Page 1」 · 「medikit」 페이지는 여전히 건드리지 않는다.
- **순서: 1절(시술 현황 보기)에 필요한 컴포넌트만 먼저 만들고 → 1절 화면을 인스턴스로 렌더 → [질문] 으로 확인 요청.** 나머지 컴포넌트는 승인 뒤 2~7절에 필요한 만큼.
- 색 · 글자는 `medikit` 변수 · Pretendard · 타이포 단계(medikit-preset.json)대로. 키트에 없는 요소(research §4 「메디킷에 없음」 — 보드 칸 · 타이머 등)는 토큰만 써서 그리고 노드 이름에 `custom/` 접두.
- 기존 시술현황 페이지 · 시안 열람 금지는 그대로. 화면 문구는 기획안 그대로, 없으면 비운다.
