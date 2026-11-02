# [frontend WP1 추가 1] SH-IMP-020 — 회의 헤더 「회의 시작」 → 「빠른 회의」

WP1-FE 에 한 건을 더한다. 규칙·allowed_paths 는 그대로, 같은 리포트 `W/fe-wp1-report.md` 에 절 하나를 더한다.

- 근거: `P/improvements/SH-IMP-020-quick-meeting-label.md`
- 위치: 회의 목록 페이지 머리 `header.scax-page-header > .scax-page-header__actions` 의 주 단추(재생 아이콘 + 「회의 시작」, 옆에 「회의 생성」)
- 할 일: 문구를 **「빠른 회의」** 로. 아이콘·모양·동작은 그대로
- **「회의 시작」 문구를 쓰는 곳을 전부 grep** 해(라벨 상수 `labels.ts` 등 · aria-label · 시험) 표로 보고하라. **바꾸는 것은 위 머리 단추 한 곳**(그 문구가 공유 상수면 이 단추만 새 라벨을 쓰게 가른다). 같은 단추를 가리키는 다른 입구(빈 상태 화면·AX 안내 문구 등)가 있으면 바꾸지 말고 목록에 「같은 동작 다른 입구」 로 적어라 — 코디가 사용자에게 묻는다
- 시험: 머리 단추 문구 시험 갱신
