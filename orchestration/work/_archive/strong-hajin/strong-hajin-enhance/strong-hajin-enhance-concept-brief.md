# [writer] strong-hajin-enhance 회고를 개념으로 소화한다

너는 **strong-hajin `writer` 워커**다. **맥락이 없다** — 먼저 읽어라:
- 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-2/orchestration/roles/strong-hajin/planner/role.md`
- 규약 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-2/para/areas/area.md` **§3 전부**(3.3 규약 · 3.4 맵) · 양식 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-2/templates/areas/concept.md`
- 회고 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-2/para/projects/summer-star/strong-hajin/log/2026-10-07-strong-hajin-enhance.md` **§2 「적용한 기술·개념」** 여섯 항목(§3 은 참고)
- 선례 커밋: `git -C /Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-2 show 26e9828` (inbox 회고 소화 — 신규 여덟·보강 넷, 회고 §2 역링크) · 기존 노트 `para/areas/concept/front/webview-attachment-download.md` · `back/ssrf-guarded-proxy.md` 등

작업 위치: 코디 워크트리에 직접 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-2`

## 할 일
회고 §2 의 각 항목을 **3.4 맵에서 먼저 찾아**(파일명 + `aliases` grep) 기존 노트가 있으면 **보강**(`up:` 에 출처 더하고 본문에 녹임), 없을 때만 **신규**(영문 kebab-case · `up:` 필수 · 3.4 맵 한 줄). 후보(판단은 네가 — 근거 보고):
1. CLI 하위 프로세스 프롬프트를 **argv 대신 stdin** 으로 — 리눅스 argv 한 칸 128KiB(`MAX_ARG_STRLEN`) · 운영 CLI 버전 차이는 실호출로 닫는다 · 되돌이(fallback) 가 프로세스 이중 실행을 부른다
2. **AI 맥락 목록 = 테이블 없이 호출 때 DB 조회해 프롬프트에 주입**(도구 조회는 보조) · 세션 첫 턴·새 세션에만 싣기(이어 쓰는 세션에 쌓이지 않게)
3. **STT 정정 pass → 다시 쓰기 + 보정 표**(등급 auto/presumed · 되돌릴 수 있는 쌍) · 「안 돎(null)」 과 「돌았는데 0건([])」 을 가르는 시각 칸
4. **같은 카드의 다음 회차(v+1) — 누가 고치든 같은 수정 경로 · 바뀐 칸만 지금 회차 위에 덮기(모르는 칸 422)** · 위임 경로의 일괄 거절이 수정까지 막은 사례 · 도구 오류는 사유를 실어(ToolError) 모델이 되풀이하지 않게
5. **긴 외부 호출 워커의 lease 셈 = 루프의 실제 최대 호출 수 × timeout + heartbeat** · 세션 기록 CAS 로 경주 막기
6. **운영 마이그레이션을 칸(트랜잭션) → 이미지 → 인덱스(CONCURRENTLY) 로 가르기** · INVALID 인덱스 처리
- 각 항목에 회고 §2 쪽 **`[[개념]]` 역링크**를 단다(회고 파일 수정 허용 — §2 역링크만)
- 사람 실명·메일 금지(공개 레포)

## allowed_paths
- `para/areas/concept/**` · `para/areas/area.md`(3.4 맵 줄 추가만) · 회고 파일 §2 역링크
- 커밋·push 금지

## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_367ca23a-f846-44c0-afc7-07b6655df214 --from <네 워커handle> --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "writer 완료: enhance 개념 소화" --body "신규 / 보강 목록(파일) / 건너뛴 것과 이유"
orca terminal send --terminal term_367ca23a-f846-44c0-afc7-07b6655df214 --text "[worker_done] writer 완료 — enhance 개념 소화." --enter
```
