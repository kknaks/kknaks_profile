# [writer] strong-hajin-notify 회고를 개념으로 소화한다

너는 **strong-hajin `writer` 워커**다. **맥락이 없다** — 먼저 읽어라:
- 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/roles/strong-hajin/planner/role.md`
- 규약 `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/areas/area.md` **§3 전부**(3.3 규약 · 3.4 맵) · 양식 `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/templates/areas/concept.md`
- 회고 `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/projects/summer-star/strong-hajin/log/2026-10-10-strong-hajin-notify.md` **§2 「적용한 기술·개념」**(§3 막혔던 것도 소재)
- 선례 커밋: `git -C /Users/kknaks/orca/workspaces/kknaks_profile/beluga log --oneline -5 -- para/areas/concept` 중 「enhance 회고를 개념으로 소화」 · 이미 있는 노트 `para/areas/concept/cs/server-sent-events.md` · `cs/websocket.md` · `back/application-event.md` · `back/per-user-fanout.md`

작업 위치: 코디 워크트리에 직접 `/Users/kknaks/orca/workspaces/kknaks_profile/beluga` (브랜치 `kknaksss/strong-hajin-notify-concept`)

## 할 일
회고 §2 · §3 의 각 항목을 **3.4 맵에서 먼저 찾아**(파일명 + `aliases` grep) 기존 노트가 있으면 **보강**(`up:` 에 출처 · 본문에 녹임), 없을 때만 **신규**(영문 kebab-case · `up:` 필수 · 3.4 맵 한 줄). 후보(판단은 네가 — 근거 보고):
1. **SSE 재연결의 실제 동작** — `EventSource` 는 비-200 이면 영구히 닫히고 상태 코드·새 인스턴스의 `Last-Event-ID` 가 없다 → 세션 확인으로 가르기 · 화면 백오프 · 쿼리로 마지막 id · 「둘째 ready = 다시 읽기」 · 겹침 창으로 커밋 순서 어긋남 메우기 · 멈춤 조건은 인증 200 + 스트림 실패만 (→ `server-sent-events` 보강 1순위)
2. **같은 트랜잭션 NOTIFY + 짧은 페이로드(id 만) · 게시하는 프로세스 늘리기** (→ `application-event` · `per-user-fanout`)
3. **사건 × 관계 알림 생성** — 원칙 셋 · 관계 우선순위 하나 · **만들 때 설정으로 거름** · 행 id 로 전수 시험
4. **「내가 보낸 줄」 판정 재료를 저장 칸 하나로**(표시 이름이 id 를 덮은 버그 · 원천마다 다른 재료)
5. **데스크톱 OS 알림을 네이티브 API 로 셸이 직접**(공식 플러그인의 데스크톱 한계 · 권한·클릭 · 앱이 켜져 있을 때만 · 웹이 받아 셸이 띄움)
6. **OS 알림 줄이기** — 보고 있으면 생략 · 합친 줄은 처음만 · 창·문턱 묶음(coalescing)
7. **의존성 올림의 실행 회귀** — 시험이 덮지 않는 웹뷰 동작 변화(wry `elementFullscreenEnabled`) · 바뀐 동작을 diff 전수로 좁히기
8. **모델과 수동 SQL 의 어긋남을 구조 시험이 잡는다** — 처음 까는 DB 용 정의 · 운영 ALTER 둘 다 맞추기
- 각 항목에 회고 §2 쪽 **`[[개념]]` 역링크**를 단다(회고 파일 수정 허용 — §2 · §3 역링크만)
- 사람 실명·메일·카톡 방 id 금지(공개 레포)

## allowed_paths
- `para/areas/concept/**` · `para/areas/area.md`(3.4 맵 줄 추가만) · 회고 파일 역링크
- 커밋·push 금지

## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_aa9fb9af-eed1-45ee-baad-95e52082321d --from <네 워커handle> --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "writer 완료: notify 개념 소화" --body "신규 / 보강 목록(파일) / 건너뛴 것과 이유"
orca terminal send --terminal term_aa9fb9af-eed1-45ee-baad-95e52082321d --text "[worker_done] writer 완료 — notify 개념 소화." --enter
```
