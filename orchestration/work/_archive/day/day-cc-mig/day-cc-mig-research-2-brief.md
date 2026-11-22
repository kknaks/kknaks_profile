# [researcher] KOS 응답 키 ↔ DAY 칸 전수 대조 (HAR 기준)

너는 **day `researcher` 워커**다. **너는 이 작업의 맥락이 없다고 가정하라** — 아래 파일이 전부다. 먼저 역할 문서를 읽어라:

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/roles/day/researcher/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
- `git -C /Users/kknaks/git/CENTURION_DAY show origin/dev:AGENTS.md`
- **앞 판 리포트**: `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/work/day-cc-mig/research-cc-ext-report.md` — 특히 §B1 「없음 · 시점 다름」 표 · §B3 동기화 주기 표 · §A2-1. 이번 조사는 그 표를 **전수로 넓히는 것**이다.

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig` (코디네이터와 공유 — 리포트 파일 1개 외에는 아무것도 만들거나 고치지 마라)

읽는 레포는 전부 read-only — checkout · pull · 수정 금지. `git fetch` · `git show <ref>:<path>` · `git grep <ref>` 만.

| 원천 | 경로 | 기준 |
|---|---|---|
| DAY 코드 | `/Users/kknaks/git/CENTURION_DAY` | `origin/dev` = `844eace4` (시작할 때 fetch 해서 더 새로우면 새 sha 를 리포트에 적고 그걸 쓴다) |
| DAY 문서 | `/Users/kknaks/git/harness_works/mediness-mediness` | `origin/main` — `products/day/20-spec/spec-000-data-model.md` · `40-architecture/erd.md` |
| HAR (KOS 웹 실물 응답) | `/Users/kknaks/git/toy_pr2/kknaks_profile/reference/` 아래 `*.har` 전부(67개 · 170MB · gitignore 라 git 에는 없고 이 로컬 폴더에만 있다) | 파일 그대로 읽기 |

HAR 폴더(직접 `find /Users/kknaks/git/toy_pr2/kknaks_profile/reference -name "*.har"` 로 다시 세라): `2026-10-12-cc-prototype/`(8) · `2026-10-21-charty-poc/`(1) · `2026-10-23-cc-overall-board/har/`(23) · `2026-11-09-cc-day/har/`(7) · `2026-11-11-cc-product/har/`(1) · `2026-11-16-cc-charty1/har/`(5) · `2026-11-18-day-customer/har/`(22).

## 1. SSOT — 판단 기준

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/config/projects/day.json` 의 `data_rules` — 특히 **「DAY 테이블은 외부 CRM 보다 크다(사용자 2026-11-03): 외부 CRM 이 가진 정보를 처음부터 전부 DAY 칸으로 두고 동기화한다. 「필요할 때 외부를 읽는다」로 비워 두지 않는다」** · 「외부 id · 동기화 칸은 external_ref 에만」 · 「메뉴 참조 = id + 그때 값 스냅샷」 · 「시각 UTC timestamptz」.
- 일부러 안 둔 것의 근거: `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/work/_archive/day/customer-erd/` (`customer-erd-spec-brief.md` §2 — 「KOS 응답에만 있고 DAY 가 계산할 수 있는 값(카드 총액 · 티켓별 가격)은 칸으로 두지 않는다」 · `SUMMARY.md` · `har-check-report*.md` · `kos-sync-research-report.md`) · SPEC-000 의 결정 · OQ.
- 사용자 지시(2026-11-20): **KOS 가 주는 키는 다 저장한다.** 이 대조로 DB 확장 범위를 한 번에 정한다.

기대는 개념: 해당 없음.

## 2. 배경

cc ext API 를 DAY 로 옮기는데(앞 판 리포트), 목표 구조는 「KOS 와는 DAY 만 통신 · 서비스는 DAY DB 에서 받는다」다. 앞 판은 ext 가 쓰는 칸만 대조했다. 이번에는 **KOS 가 주는 응답 키 전부**를 DAY 칸과 맞춘다.

## 3. 계약

해당 없음. 산출물은 리포트 1개.

## 4. 대상 KOS 경로

1. **DAY 가 지금 부르는 KOS 읽기 경로 전부** — `origin/dev` 의 `backend/day/emr/kos/*`(client · mapper* · sale_reads · staff_client · demo 제외) · `backend/day/emr/sync_*.py` · `services/emr_*.py` 에서 grep 으로 경로 상수를 전부 모아라(센 명령을 적어라).
2. **ext 이관에 새로 필요한 경로** — 앞 판 리포트가 「DAY 에 없음」으로 적은 KOS 경로(병원 `get-hospital` · 기본 운영 시간 · `get-reservation-slots-by-groups` · `get-visitor` · 문진 `get-visitor-questionnaire` · `get-questionnaire-submit` · `get-schedules-by-visitor` 등 — 리포트에서 전부 다시 모아라).
3. HAR 에 응답이 있는데 1 · 2 에 없는 **읽기 경로**는 목록만 따로(경로 · HAR 파일 · 무엇인지 한 줄). 대조는 하지 않는다.

쓰기(commands) 경로는 이번 범위 밖 — 목록에도 넣지 않는다.

## 5. allowed_paths

- `(read-only — 브리프가 지정한 리포트 파일 1개만 생성)`
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/work/day-cc-mig/research-kos-keys-report.md`
- HAR 를 파싱하는 일회용 스크립트가 필요하면 **네 scratchpad** 에 두고 워크트리에 남기지 마라. 스크립트 · 명령은 리포트 부록에 적어라(재현용).

## 6. 조사

- **K1. 경로 목록** — §4 의 1 · 2 경로마다: 경로 · 공개/내부 · DAY 가 부르나(파일:줄) · 주기(앞 판 §B3) · 응답이 있는 HAR 파일#엔트리(여러 개면 전부 — 키가 응답마다 다를 수 있다).
- **K2. 키 전수 대조** — 경로마다 HAR 응답 JSON 의 **모든 키를 경로식으로 펼쳐**(예: `data[].reservation.counselor.name`) 여러 HAR 응답의 합집합을 만든다. 키마다 한 행:
  - 키 경로 · 타입 · 예시 값의 **모양만**(값 자체 금지 — 아래 §7)
  - DAY 칸(`테이블.칼럼` · 근거 `models/*.py:줄` + 채우는 매퍼 `파일:줄`) 또는 `external_ref`
  - 판정 하나: `저장됨` / `칸 있음 · 미동기화`(칼럼은 있는데 매퍼가 안 채움) / `칸 없음` / `일부러 안 둠`(근거 문서:줄 필수 — 근거 없으면 `칸 없음`) / `계산으로 대체`(DAY 가 다른 칸으로 계산 — 계산식) / `해당 없음`(페이지 · count · 커서 같은 응답 껍데기)
  - **같은 이름 다른 시점** 이면(예: 일정의 `reservation.counselor` vs `consultations[].counselors` vs `consultation.counselor`) DAY 칸이 같은 시점을 담는지까지 본다 — 다르면 `칸 없음(시점 다름)`.
- **K3. 집계** — 경로별 · 판정별 수. 그리고 「DB 확장 후보」 표: `칸 있음 · 미동기화` · `칸 없음` · `칸 없음(시점 다름)` 키를 **DAY 테이블별로** 묶어 — 대상 테이블(있는 표 / 새 표 필요) · 키 목록 · KOS 경로 · 민감 정보 여부(data_rules 암호화 대상인지).
- **K4. 동기화 범위** — 키가 아니라 범위 때문에 비는 것(미래 일정 · 오늘 안 오는 고객의 시술권/카드 · 칸 정원)을 따로 표로. 앞 판 §B3 를 근거로.
- **K5. HAR 로 확인 안 되는 것** — DAY 가 부르는데 HAR 에 응답이 없는 경로, 응답이 비어 키를 다 못 본 배열 등. 「확인 안 됨」으로 모은다.
- **K6. 정할 것** — 사용자 판단이 필요한 것만(질문 · 선택지 · 근거). 결정하지 않는다. 앞 판 C1 ~ C21 과 겹치면 그 번호를 적는다.

## 7. 범위 제약 — 하지 말 것

- **HAR 에는 실제 환자 개인정보 · 토큰 · 쿠키가 있다.** 리포트에 **값을 한 글자도 옮기지 마라** — 키 경로 · 타입 · 모양(예: `string(uuid)` · `string(ISO UTC)` · `number` · `enum: A|B|C`(KOS 코드값 enum 만 허용 — 이름 · 전화 · 이메일 · 주소 · 메모 · 번호 같은 자유 값은 절대 안 됨))만. 요청 헤더 · Authorization · Cookie 는 읽지도 적지도 않는다.
- HAR 파일 이동 · 복사 · 수정 금지. 워크트리 · scratchpad 에 HAR 내용 사본을 남기지 마라(파싱 결과 키 목록만 메모리에서 다룬다).
- KOS · DAY 서버 실호출 금지(DB · ssh · curl 포함).
- 어떤 레포도 수정 · 커밋 금지. 스키마 설계안 · 마이그레이션 초안을 쓰지 마라 — K3 은 후보 목록이지 설계가 아니다.
- 근거 없는 판정 금지 — 「확인 안 됨」.

## 8. 검증

```
질문마다 답 + 근거(파일:줄 · git ref · HAR 파일#엔트리). 확인 못 한 것은 「확인 안 됨」. 결정하지 않고 「정할 것」으로 모은다
```

- K1 의 경로 수 = grep 으로 센 수(명령 기재). K2 의 경로별 키 행 수 = 파싱 스크립트가 낸 합집합 키 수(경로마다 둘을 나란히 적어 대조 — 빠진 키 0).
- 리포트 맨 위 요약: 경로 수(DAY 부름 / 새로 필요 / HAR 에만) · 키 총수 · 판정별 수 · DB 확장 후보 키 수(테이블별) · 확인 안 됨 수 · 정할 것 수.
- 리포트에서 이메일 · 전화 · 한글 이름 꼴 값 grep 0 (명령과 결과를 부록에).

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_9a3ce290-f594-459d-a6bc-89f3cf9dccc4 --from term_2a6739ed-9738-40ed-9da2-6e34838812e9 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료(2차 · KOS 키 전수): <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_9a3ce290-f594-459d-a6bc-89f3cf9dccc4 \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_9a3ce290-f594-459d-a6bc-89f3cf9dccc4 --text "[질문] researcher: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
