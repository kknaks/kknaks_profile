# [researcher · 문서] cc-nav-resv(cc 2차) 회고를 개념으로 소화한다

너는 **cc-prototype `researcher` 워커**인데 이번 판은 **개념 노트 작성**이다. **맥락이 없다** — 먼저 읽어라:
- 규약 `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/para/areas/area.md` **§3 전부**(3.3 규약 · 3.4 맵) · 양식 `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/templates/areas/concept.md`
- 회고 `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/para/projects/summer-star/cc-prototype/log/2026-10-19-cc-nav-resv.md` **§2 「적용한 기술·개념」** 여섯 항목(§3 은 참고)
- 선례: 1차 회고 `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/para/projects/summer-star/cc-prototype/log/2026-10-14-sts-prototype.md` §2 의 `[[개념]]` 역링크 모양 · 그때 만든 개념(`no-inference-from-free-text` · `public-vs-internal-api` · `seed-data` · `as-of-visibility` · `structured-work-as-primary-data` 등)
- 근거: `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/orchestration/work/_archive/cc-prototype/cc-nav-resv/`(브리프 · 리포트 · e2e-feedback-batch-1~5) · `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/para/projects/summer-star/cc-prototype/`(BASE-007 · DEC-004 · SPEC-002)

작업 위치: 코디 워크트리에 직접 `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입`

## 할 일
회고 §2 각 항목을 **3.4 맵에서 먼저 찾아**(파일명 + `aliases` grep) 있으면 **보강**(`up:` 에 출처 더하고 본문에 녹임), 없을 때만 **신규**(영문 kebab-case · `up:` 필수 · 3.4 맵 한 줄). 후보(판단은 네가 — 근거 보고):
1. 기획 피드백을 데이터 채움률로 거르기 — 화면 칸마다 원천 필드가 있나 · 있으면 시드를 고쳐서라도(→ 1차 `no-inference-from-free-text` · `seed-data` 보강 후보)
2. 쓸 수 있는 API 표면이 기능 범위를 정한다 — 읽기 가능 ≠ 쓰기 가능(→ `public-vs-internal-api` 보강 후보)
3. 경과 시간 = 상태가 시작된 뒤 · 상태와 시간을 같은 칸에 두 줄로
4. 소모성 자원(시술권)의 「예정」과 「사용」 분리 — 차감은 완료 시점(취소 · 노쇼 되돌림)
5. 데모 버튼으로 외부 연동 자리 대신 + 등록 순간 스냅샷 — 상태 전이는 실제와 같게
6. 기존 디자인 무변경과 예외 범위 · 디자인 토큰 실재 대조(없는 클래스 → 흰 글자) · 옛 맥락 값(z-index) 재사용 함정(→ `design-system` 보강 후보)
- 각 항목에 회고 §2 쪽 **`[[개념]]` 역링크**를 단다(회고 파일 수정 허용 — §2 역링크만)
- 사람 실명 · 메일 · 운영 메모 원문 금지(공개 레포)

## allowed_paths
- `para/areas/concept/**` · `para/areas/area.md`(3.4 맵 줄 추가만) · 회고 파일 §2 역링크. 커밋 · push 금지

## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_59709c96-62c1-4f26-8957-1cc21920e5de --from <네 워커handle> --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "researcher 완료: cc-nav-resv 개념 소화" --body "신규 / 보강 목록(파일) / 건너뛴 것과 이유"
orca terminal send --terminal term_59709c96-62c1-4f26-8957-1cc21920e5de --text "[worker_done] researcher 완료 — cc-nav-resv 개념 소화." --enter
```
