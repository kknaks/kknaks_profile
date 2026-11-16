# [researcher] KOS 시술 · 상품 메뉴(procedure-menu) — 어느 깊이까지 오나 실호출 조사

너는 **cc-prototype `researcher` 워커**다. **앞 맥락이 없다** — 이 브리프만 믿어라. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/orchestration/roles/cc-prototype/researcher/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2` (코디 워크트리 — **리포트 1개 외 아무것도 고치지 마라**)
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

코디네이터가 같은 워크트리에 있다. 다른 파일은 건드리지 마라.

## 1. SSOT — 먼저 읽을 것

- 앞 조사(10-20): `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/reference/2026-10-12-cc-prototype/kos-demo-api.md` — §1(접속 · 쓸 키 · **쓰지 말 키**) · §2 E(시술 메뉴 16개) · §3.1 · §3.5(모양 요약 한 줄). 이번 조사는 이 §3.5 를 **중첩 끝까지** 펼치는 것
- KOS 사용법(private · read-only): `/Users/kknaks/git/ax-clinic-project/para/resources/technology/2026-09-18-kos-developers-api-guide.md` §3(인증 · 헤더 · 오류)
- 호출 코드(read-only · 참고): `/Users/kknaks/git/ax-clinic-project/scripts/kos_collect.py` — `.env` 읽기 · 토큰 교환
- 키: `/Users/kknaks/git/ax-clinic-project/scripts/.env` 의 **`KOS_API_tenent_dev` 만**(운영 호스트의 데모 테넌트). **`KOS_API_tenent` 는 실제 지점 키 — 절대 쓰지 않는다**
- 공식 스펙: `https://developers.kos-solution.com/openapi.yaml` (받아서 스키마 대조)

**따를 개념** — 확인 · 스펙 · 추정을 구분해 적는다(앞 조사와 같은 표기). 정할 것은 정하지 않고 모은다.

## 2. 배경 / 무엇을 알아내나

협업자가 「시술 · 상품 종류 API」를 요청했다. 우리 back(procedure)은 KOS 공개 API 를 이미 부르지만 `procedure-menu` 는 아직 안 쓴다. 이걸 감싸 우리 API 로 내주기 전에, **KOS 가 어느 수준(깊이 · 칸 · 관계)까지 주는지** 사용자가 보고 범위를 정하려 한다.

## 3. 알아낼 것 (질문마다 답)

조회(`/queries/`)만, 작업당 한두 번. 쓰기(`/commands/`) 0건.

1. **작업별 전체 키 트리** — `getCategories` · `getProducts` · `getProduct` · `getProductOptions` · `searchProductOptionSummaries` · `getProcedures` · `getMachines` · `getMedicines` · `getMedicalServices` · `getTargetCountries`. 응답의 **모든 중첩 키를 끝까지**(배열 안 객체 · 객체 안 객체), 각 키의 타입 · null 비율 · 관찰된 enum 값. 데모에서 비어 있던 칸은 스펙 스키마로 채우고 「스펙」 표기
2. **관계 · 깊이** — 카테고리 → 상품 → 옵션 → 구성(compositions) → 시술 / 진료항목 / 기기 · 약물: 몇 단계이고 각 단계를 잇는 키가 무엇인가. 옵션 안의 `procedure` · `compositions[].procedure` 가 `getProcedures` 의 id 와 같은 id 체계인지(실제 대조). `type` `SINGLE` · `GROUP` 이 구조를 어떻게 바꾸는지. 프로모션(`includePromotions`) · 노출 채널(`displayChannels`) · 다국어(`translsMap`) · 타겟 국가가 어디에 붙는지
3. **가격** — 어디에 몇 종류(정가 · 할인 · 세금 · 단위)가 있나
4. **상태 · 개수** — `closed` · `deleted` · `isEvent` · `opened` 건수 · 정렬(`order`) · 페이징 유무(전부 한 번에 오나)
5. **우리 쪽과의 접점** — 지금 back 이 일정 · 수납 응답에서 받는 `productOptionConfiguration{optionId, optionTitle, productTitle, procedure{id,name}}` 의 id 가 위 메뉴 id 와 맞는지(데모 일정 1~2건으로 대조. 일정 조회는 앞 조사 §2 A 의 조회 작업)
6. **응답 크기 · 속도** — 작업별 바이트 · 건수 · 응답 시간(1시간 캐시 판단용)

## 4. 산출물

리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/orchestration/work/api-swagger-docs/research-procedure-menu.md`
- 맨 위 요약: 「깊이 그림」(트리 다이어그램 한 장) + 질문 1~6 한 줄 답
- 작업별 키 트리 표(키 경로 · 타입 · null · 값 예시는 **모양만**)
- 정할 것(결정하지 않고 모음)

## 5. allowed_paths — 이 밖은 건드리지 마라

- 위 리포트 1개만 생성. 원 응답 덤프가 필요하면 네 scratchpad 에만(레포에 두지 마라)

## 7. 범위 제약 — 하지 말 것

- **public 레포다** — 키 · 토큰 · 테넌트 id · 사람 이름 · 연락처 · 이메일을 리포트에 쓰지 않는다. 상품 · 시술 **이름 원문도 쓰지 않는다**(건수 · 모양 · 가짜 예시만)
- 쓰기 호출 · 운영 지점 키 금지. 우리 운영 서버(ccc) · 클러스터 무접촉
- 코드 · 설계를 정하지 않는다

## 8. 검증

질문마다 답 + 공식 문서 URL. 문서에 없는 것은 「문서에 없음」. 결정하지 않고 「정할 것」으로 모은다. 리포트를 public 기준으로 grep(키 · 이메일 · 전화 패턴 0).

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_2be25447-14e8-4dcf-9ed4-6b05f0fb0e46 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_2be25447-14e8-4dcf-9ed4-6b05f0fb0e46 \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_2be25447-14e8-4dcf-9ed4-6b05f0fb0e46 --text "[질문] researcher: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
