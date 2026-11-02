# 루프2 문서 검수 — 사용자 지시가 계약으로 정확히 내려왔나

**read-only.** 문서·코드 수정 0건. 커밋·테스트·서버 금지.
**쓰는 파일 하나**: `orchestration/work/strong-hajin-projects/review-loop2-doc-report.md`

## 검수 대상 셋

- `para/projects/summer-star/strong-hajin/10-decision/decision-004-projects.md` (D-28~D-38 신규, D-12 뒤집힘)
- `para/projects/summer-star/strong-hajin/20-spec/spec-005-projects.md` (v0.2.0, 인수조건 L-01~L-48 추가)
- `para/projects/summer-star/strong-hajin/30-work/work-005-projects.md` (2루프 Phase BE-3 → FE-4 → FE-5)

## 상위 근거 — 이것이 기준이다

- **`loop2-backlog.md`** ← **사용자 지시 11건의 정본.** 계약이 이것과 다르면 FAIL
- **`loop2-survey-report.md`** (428줄) ← 조사. **범위 판정·비용 수치**의 출처
- 1루프 산출물: `spec-005` 기존 76줄 인수조건 · `work-005` 1루프 Phase · `review-*-report.md` 넷

## 판정

**FAIL**(사용자 지시와 다르다 · 코드 사실과 다르다 · 내부 모순) / **WARN**(구현자가 둘로 읽는다) / **PASS**.
**각 지적에 `파일:줄` + 근거.** 근거 없는 지적은 쓰지 마라.

## 반드시 확인할 것

1. **사용자 지시 11항목이 전부 내려왔나** — `loop2-backlog.md` 의 A-1 · B-1~B-11 을
   **하나씩 대조**하라. 특히 **코디가 잘못 적었다가 조사로 바로잡은 둘**(B-1 헤더는 이미 등록돼
   있었다 · B-9 체크리스트는 버그가 아니었다)이 **정정된 사실로** 반영됐는가
2. **D-12 뒤집힘이 온전한가** — 취소선·사유·대체(D-28)가 있고 **본문이 지워지지 않았나.**
   그리고 **그 번호를 가리키는 다른 자리 전부**(분류표·In Scope·기각·Resulting Spec 등)가
   같이 갱신됐나. **한 곳이라도 옛 뜻으로 남아 있으면 FAIL**
3. **계약 변경이 하나뿐인가** — 체크리스트·업무 내용 읽기 범위(D-29). 그 밖에 **몰래 바뀐 계약이
   없는지** 확인하라. 특히 자동 초대 게이트 제거가 **「업무를 올리는 게이트」까지 건드리지 않았나**
4. **가르는 방식 ⓑ 의 근거가 서는가** — 「`access` 3분화를 기각하고 `checklist` 싣는 조건만 따로」.
   그 판단의 근거(「접근 값은 이미 밖으로 나가는 계약이라 읽는 곳 전부가 움직인다」)를
   **코드로 확인하라** — `access` 를 읽는 자리를 grep 으로 세어 그 주장이 맞나
5. **SPEC-003 에 안 닿는다는 주장이 맞나** — 작성자는 「`access` 라는 값이 SPEC-001·002·003·004
   어디에도 없다」고 했다. **직접 grep 해서 확인하라.** 틀리면 FAIL
6. **인수조건 배정** — WORK 가 **48줄 전수 배정(BE-3 12 / FE-4 8 / FE-5 27 / 문서 1)** 이라 주장한다.
   **네가 직접 세어** 대조하라. 그리고 **기존 76줄이 재배열되지 않았나**(1루프 문서가 그 번호를 가리킨다)
7. **직렬 순서가 적혔나** — BE-3 → FE-4 → FE-5. `Dependency` 절에 **왜 병렬이 아닌지**
   (D-29 가 FE 응답을 바꾼다)가 있나. FE 를 둘로 쪼갠 근거가 서는가 —
   작성자는 「`projects.css` 한 장과 `ProjectRail.tsx` 를 둘 다 만지므로 직렬」이라 했다.
   **그 파일 중복이 사실인가**
8. **빈 상태에서도 생성 버튼이 선다**는 계약이 **실현 가능한가** — 지금 `noProjects` 갈래는
   `Empty` 만 그리고 레일도 헤더도 안 세운다(`ProjectPage.tsx:230-235·292-298`).
   **그 사실이 SPEC·WORK 에 반영됐나** (안 되면 구현이 막힌다)
9. **새 결정을 만들지 않았나** — 백로그에 없는 판단이 `(확정)` 으로 달려 있으면 FAIL.
   `(제안)`·`(도출)` 로 구분됐는지 보라
10. **저장 구조 서술이 SPEC 에 없나** · WORK `Domain/Schema` 의 「2루프는 저장 구조를 바꾸지 않는다」가 맞나

## 범위 밖 — 지적하지 마라

- 루프3 으로 미룬 것(관리 모달 정리 · 리드 권한 화면 · 떼는 자리 #4 표면)
- Phase 0(닫혔다) · 1루프 Phase 들(done 기록)
- 문서 말투·표 서식 취향

## 리포트 형식

판정 한 줄(FAIL n · WARN n) → 지적마다
`[FAIL-n] 제목 / 무엇이 / 파일:줄 / 무엇과 어긋나나 / 한 줄 수정안`
→ **§「반드시 확인할 것」 10항목 각각의 결과** → **사용자 지시 11항목 대조표**(항목 → 내려온 자리 → 판정).

## 역할·맥락

너는 **strong-hajin `reviewer` 워커**다. 먼저 읽어라:
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/reviewer/role.md` (+ 같은 폴더 `.md`)
- `loop2-backlog.md` · `loop2-survey-report.md` · 검수 대상 셋

워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin` (코디가 함께 있다).
코드는 read-only: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`

## 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_bdba055b-758b-4dc9-85c3-7836d56b615a --from term_70ef2907-3a7e-4ae1-9da9-88378ab099e8 \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "reviewer 완료: 루프2 문서 검수" \
  --body "판정(FAIL n·WARN n) / 큰 지적 3개 / 10항목 결과 / 사용자 지시 11항목 누락 유무 / git status"

orca terminal send --terminal term_bdba055b-758b-4dc9-85c3-7836d56b615a \
  --text "[worker_done] reviewer 완료 — 루프2 문서 검수. 상세는 인박스." --enter
```
