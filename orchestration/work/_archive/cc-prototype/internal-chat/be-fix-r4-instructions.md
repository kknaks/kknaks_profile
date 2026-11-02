# [backend] 코드 리뷰 r3 WARN 수정 (W3-2)

리뷰 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/review-code-r3.md` W3-2: 전달이 원본(첨부 행 · 파일) 확인을 **쓰기 잠금 전에** 해서, 같은 파일의 마지막 참조 삭제와 동시에 오면 파일 없는 전달본이 생길 수 있다. 리뷰 권장대로 원본 확인을 쓰기 트랜잭션(잠금) 안으로 옮기고, 삭제 쪽 셈과 같은 순서로 보게 한다. 시험(가능하면 두 요청 겹침 재현 · 안 되면 순서 단언). 역할 · allowed_paths(`procedure/back/`) · 하지 말 것(커밋 · 서버 · `procedure/app` 금지) · 완료 보고는 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/internal-chat-be-brief.md` 그대로. subject 「backend 수정 r4 완료: …」.

작업 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/internal-chat`(브랜치 `kknaksss/internal-chat-forward` · mobile 이 `procedure/app` 에서 병렬 작업 중 — 건드리지 마라).
검증: `cd procedure/back && uv run ruff check . && uv run pytest -q` 1회
