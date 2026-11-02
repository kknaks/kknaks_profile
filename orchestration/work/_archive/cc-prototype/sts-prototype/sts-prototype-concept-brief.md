# [researcher · 문서] sts-prototype(cc PoC) 회고를 개념으로 소화한다

너는 **cc-prototype `researcher` 워커**인데 이번 판은 **개념 노트 작성**이다. **맥락이 없다** — 먼저 읽어라:
- 규약 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/para/areas/area.md` **§3 전부**(3.3 규약 · 3.4 맵) · 양식 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/templates/areas/concept.md`
- 회고 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/para/projects/summer-star/cc-prototype/log/2026-10-14-sts-prototype.md` **§2 「적용한 기술·개념」** 일곱 항목(§3 은 참고)
- 선례 커밋: `git -C /Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype show 01a3e9f`(strong-hajin-enhance 회고 소화 — 신규 여섯 · 보강 넷 · 회고 §2 역링크)
- 근거 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/_archive/cc-prototype/sts-prototype/`(research-* · wp* · deploy-* · e2e-feedback-batch-*) · 흐름 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/reference/2026-10-12-cc-prototype/workflow.md`

작업 위치: 코디 워크트리에 직접 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype`

## 할 일
회고 §2 각 항목을 **3.4 맵에서 먼저 찾아**(파일명 + `aliases` grep) 있으면 **보강**(`up:` 에 출처 더하고 본문에 녹임), 없을 때만 **신규**(영문 kebab-case · `up:` 필수 · 3.4 맵 한 줄). 후보(판단은 네가 — 근거 보고):
1. 동선(구조화된 작업)을 메인 데이터로, 자유 메모를 참고 원문으로 — 「오늘 오더 = 동선」
2. 메모 양식 파싱 금지 — 지점마다 양식이 다르다 · 근거 없는 추정 표시(지정 · 위험 단어) 금지
3. 데이터 공개 = 쓰인 시점(사후 스냅샷의 「미래 정보」) · 오늘/과거 분리
4. 목데이터 = 시드(조회 스냅샷) + 이벤트(진행 중 들어오는 것)로 실데이터 대본화
5. 벤더 공개 API vs 웹앱 내부 API(HAR) — 공개 쓰기 범위 확인 · 내부 API 는 근거로만, 연동은 공식 요청
6. 실시간 통역 중계(STT 번역 + TTS 두 WS) · 반이중으로 스피커 되먹임 막기
7. Helm/ArgoCD 배포 함정 — local-path 노드 제약(nodeSelector) · public 레포 데이터는 Secret(평평한 키) · 이미지는 main 빌드만
- 각 항목에 회고 §2 쪽 **`[[개념]]` 역링크**를 단다(회고 파일 수정 허용 — §2 역링크만)
- 사람 실명 · 메일 · 운영 메모 원문 금지(공개 레포)

## allowed_paths
- `para/areas/concept/**` · `para/areas/area.md`(3.4 맵 줄 추가만) · 회고 파일 §2 역링크. 커밋 · push 금지

## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --from term_fa753e4f-11e5-45a9-ad51-23d190571178 --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "researcher 완료: sts-prototype 개념 소화" --body "신규 / 보강 목록(파일) / 건너뛴 것과 이유"
orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --text "[worker_done] researcher 완료 — sts-prototype 개념 소화." --enter
```
