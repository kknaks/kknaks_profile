# 리뷰 리포트 — agency-settlement / code r4 — SPEC-001 0.5.2 ↔ back/ · front/ (BE4 · BE4 수정 1 · BE5 · FE4 · FE4 수정 1 · FE5) (2026-11-02)

워크트리 `/Users/kknaks/orca/workspaces/agency-settlement/agency-settlement`(커밋 전 · read-only). 운영 PG 5434 · 8800 · 3800 · `back/.env` · 운영 KOS 는 건드리지 않았다. 시험은 testcontainers(postgres:16)로만 돌렸고, PDF 는 가짜 데이터로만 그렸다(scratchpad).

## 판정: FAIL

FAIL 1 · WARN 4 · NOTE 13.

막는 것은 하나다(**F-1**). **[KOS 상품 다시 받기]를 누르면 수수료율을 확정(잠금)한 달의 수수료가 바뀐다.** r7 F-1 은 「잠긴 달 수수료가 바뀌는 길 = [고치기] 하나」로 닫았다. 그런데 0.5.2 의 상품 id 키(BE4 추가 · 수정 1)가 다른 길을 하나 새로 열었다. 상품 받기는 잠긴 달을 포함해 모든 달의 품목 키를 다시 정한다. 키가 바뀌면 그 달 스냅샷의 비율이 새 키에 붙지 않는다. 이미 넣은 비율이 다른 키로 새는 길(볼 것 2)이 실제로 있고, 그 길이 잠긴 달까지 닿는다.

나머지(돈 반올림 · 스냅샷 · J0 · PG 잠금 · 권한 · 쓰기 막기 · 0원 줄 · 묶음 구성 · PDF 줄 맞춤 · 필드 계약)는 닫혀 있다.

**검증 수치**
- back `uv run pytest -q` = **277 passed**(1 warning — testcontainers 사용 중단 예고) · 29.5초 · DB = testcontainers. conftest 가 `_env_file=None` 이라 `back/.env` · 5434 에 닿지 않음을 확인함
- `uv run ruff check .` = All checks passed(`ruff format --check` 는 43 파일 차이 — 레포 규칙 밖 · NOTE)
- 부분 시험(test_fees · product_id · statements · prior_cancel · catalog · channel · composition) 91 passed
- front `npx tsc --noEmit` 0 · `npm run lint` 0
- 재현 시험 1(F-1 · scratchpad `r4tests/test_r4_rekey.py` · 레포 밖): 잠긴 10월 수수료 100 → 상품 받기 뒤 **0** · `unsetItems` 0 → 1 · `fees.locked = true` 그대로
- 가짜 데이터 PDF(31 수납 · 5쪽) 렌더 → 상자 · 요약 · 표 좌우 끝 같은 선 · 테두리 0.75pt 하나 · 기간 한 줄 확인

볼 것 1 ~ 6 요약:

| # | 볼 것 | 결과 |
|---|---|---|
| 1 | 수수료 돈 경로 | 반올림 · 미설정 0 · 스냅샷(GET 이 안 만듦) · 복사 · J0 409 · lock 조건 · 「—」 · 화면 = 결산 = PDF = zip 은 닫힘. **상품 받기가 잠긴 달 수수료를 바꿈 = F-1** |
| 2 | 상품 id 키 | 짝짓기 · 대체 · 같은 이름 다른 id 는 SPEC 과 같다. **키가 바뀔 때 저장된 비율이 고아가 됨 = F-1 · W-1** · `name:` 키 검사 구멍 W-2 |
| 3 | PG | 두 겹 달 잠금 · xact 쓰기 잠금 · 격리 · 권한(시퀀스 USAGE · 기록 표 UPDATE/DELETE 0) · 0001 ↔ 0003 왕복 · json 칸 0 · 로그 수만은 닫힘. 풀 60초 기다림 W-3 |
| 4 | 쓰기 막기 · 확정 달 KOS 0 | Origin · Host · JSON 415 · cross-site GET refresh 403 · J0 KOS 0 · 가드 7 · 경로 10 은 닫힘. GET 의 Host(DNS rebinding) NOTE |
| 5 | 0원 · 묶음 · PDF · 반응형 · 시안 v3 · 피드백 b | b-1 · b-4 · b-5 · b-6 은 반영됨. PDF 의 0원 「미설정」 주황 NOTE · 쪽 넘김 NOTE |
| 6 | schemas ↔ types | `KeyBy` 에 `product_title` 이 빠짐 W-4. 나머지 필드는 하나씩 대조해 같음 |

---

## FAIL

### F-1 상품 받기가 잠긴(확정) 달의 상품 키를 바꾼다 → 확정 달 수수료 · 명세서가 소리 없이 바뀐다

- **코드**
  - `back/app/repository/settings_store.py:56` — 상품 받기 쓰기 트랜잭션이 `link_products(c)` 를 **범위 없이**(`purchase_id=None`) 부른다
  - `back/app/repository/store.py:56-83` `link_products`
    - `:64` 이 모든 `product_via='product_title'` 행을 NULL 로 지운 뒤 다시 맞춘다
    - `:65` 은 새 목록에 들어온 옵션을 `by=option`(키 `product:`)으로 다시 잇는다
    - `:67-83` 는 목록 밖 옵션을 「⑦ title 이 하나로 맞을 때만」 `product_title` 로 잇는다
    - 어느 단계에도 달 · 잠금(`fee_rate_months.locked_at`) 조건이 없다
  - `back/app/service/sales.py:665-668` `line_of` — 키는 읽을 때 `items.product_id/product_via` 로 다시 만든다. 비율은 그 키로 그 달 스냅샷(`rates.get(key.key)`)에서 찾는다
- **SPEC · DEC**
  - §6.10 「잠금 = 비율 + 그 달 매출 다시 받기 막음 … 잠긴 달의 품목 줄 · 금액 · 수수료는 바뀌지 않는다」 · 「잠긴 달은 비율도 금액도 바뀔 길이 『[고치기] → 풀기』 하나뿐」
  - §4.4.1 「상품 받기는 … 수수료율 표는 건드리지 않는다」 — 표는 안 건드리지만 품목의 키가 바뀌어 같은 결과가 된다
  - D-20(확정 달 잠금) · D-21 · r7 F-1(같은 불변식을 [전체 다시 받기] 쪽에서 막음)
- **실패 길**(가짜 값 · 재현 시험 통과)
  1. 10월 품목 X = `option:o-old`(그때 팔린 옵션이 지금 목록에 없음 — 9월 914 줄과 같은 꼴) · 설정에서 10% 저장 · [이 달 확정] · 명세서 발행 · 수수료 100
  2. 그 뒤 KOS 에 title 이 같은 상품이 생기거나(이름 정리 · 재등록) 옵션이 목록에 돌아옴 → 사람이 설정에서 [KOS 상품 다시 받기]
  3. X 의 키가 `product:<id>`(`by = product_title` 또는 `product`)로 바뀐다. 10월 스냅샷엔 이 키가 없다 → **10월 수수료 0 · 「미설정」 · `unsetItems` +1**. `fees.locked = true` 그대로라 PUT 409 — 풀지 않으면 고칠 수도 없다
  4. 반대 방향
     - `product_title` 로 이어졌던 줄은 같은 title 상품이 하나 더 생기거나 title 이 바뀌면 `option:<id>` 로 돌아가 비율을 잃는다(`:64` 가 늘 지우고 다시 맞춤)
     - `option:O` 에 비율을 따로 넣었던 줄은 O 가 목록에 돌아오면 그 상품의 다른 비율로 바뀐다(값이 **틀린 비율로** 바뀌는 쪽)
- **코디 실물 숫자와 같은 꼴**: 9월 option 1,002 → (수정 1 뒤) option 914 + product_title 88. 그 88 줄이 이미 한 번 키를 바꿨다. 그 전에 `option:` 키로 비율을 저장했다면 그 비율은 지금 붙지 않는다. 사용자가 10월에 152 키를 저장했다 → 다음 상품 받기에서 바뀌는 줄이 있으면 잠긴 · 안 잠긴 달 모두 영향을 받는다
- **잠기지 않은 달도 조용히 틀린다**
  - 옛 키 비율은 고아 줄로 남는다. `fees.py:177-186` 의 「스냅샷 키」 합집합으로 설정 줄에는 계속 보인다
  - 새 달 복사(`settings_store.py:112-117`)로 뒤 달에도 따라간다. 화면에는 「미설정」이나 다른 키의 비율만 보이고 경고는 없다
- **고칠 것**(BE — planner · 코디 결정 한 줄 필요)
  - (권장) `link_products` 가 **품목 달(`month_purchases.items_here = true` 인 달)이 잠긴 품목은 다시 잇지 않는다**(달 잠금 = 키도 얼림). 풀린 달만 다시 잇는다
  - 함께: 키가 바뀐 줄의 비율을 옮기지 않으면 설정 화면에 「키가 바뀐 줄 n」(옛 키 → 새 키)을 보이거나, 상품 받기 응답에 수를 싣는다(`kosCalls` 옆 `rekeyedItems`) — 「미설정으로 드러남」(r7 상품 키 판단 근거)을 지키려면 적어도 수로는 드러나야 한다
  - 다른 길: 바뀐 키로 비율을 옮겨 쓰고 `fee_rate_changes` 에 기록. 잠긴 달엔 쓰지 못하므로 위 「얼림」과 같이 가야 한다
  - 시험: 「10월 잠금 → 상품 받기(옵션이 목록에 돌아옴 · 같은 title 둘 · title 하나 생김) → 10월 `feeTotal` · `unsetItems` · PDF 합 그대로」 · 「풀린 달은 다시 이어지고 수가 보임」

---

## WARN

### W-1 다른 달 받기 · `backfill_compositions` 가 잠긴 달 품목의 키 원천(`purchase_options`)을 갈아 끼운다 — F-1 이 다음 상품 받기에서 터질 원료

- **코드**
  - `store.py:549` · `:559` `_replace_options` — 받은 달 ① 에 나온 수납 전부의 ⑤ `purchase_options`(title · `product_title` · amount · option_type · 구성)를 갈아 끼운다. 그 안에는 품목이 잠긴 앞 달에 있는 수납(예: 11월 「앞 달 결제 취소」의 10월 수납)도 있다
  - `backfill_compositions.py:62` 도 그 달 저장 수납 전부를 지금 ⑤ 로 갈아 끼운다(⑤ 가 옵션을 안 주면 지움)
  - `link_products` 는 이 `purchase_options.product_title` 을 읽는다(`store.py:71`)
- **SPEC**: §4.5 「다른 달 … 건드리지 않는다」 · §6.11 「backfill … 금액 · 품목 · 판정 · 수수료 · 잠금과 무관」 — 지금 돈은 안 바뀐다. 다만 F-1 경로(다음 상품 받기)의 입력이 바뀌어 잠긴 달 키 · 「구성: …」 글자가 바뀔 수 있다
- **고칠 것**: F-1 을 「잠긴 달 품목은 다시 잇지 않음」으로 고치면 돈 쪽은 같이 닫힌다. 구성 글자는 NOTE 로 둔다

### W-2 `PUT /api/fee-rates` 가 설정 줄에 없는 `name:` 키 · 3판 `{kind, name}` 꼴을 받는다

- **코드**
  - `back/app/service/fees.py:61-68` — `key` 가 없으면 3판 `{kind, name}` 꼴로 받는다
  - `fees.py:73-77` — `name:<종류>:<이름>` 은 꼴만 본다
  - `settings_store.py:139-141` · `:161-176` `_display` — `product:` · `option:` 키만 이름을 찾아 본다
- **SPEC**: §4.3 `bad_rate` 「`key` 가 §5.5 꼴이 아니거나 **설정 줄(`rows`)에 없는 키**」 · §4.8 「모르는 key = 400 bad_rate」
- **실패 길**
  - `{"rates":[{"key":"name:PRODUCT_OPTION:오타","rateBp":1000}]}` → 200 · 고아 비율 + `set` 기록이 남는다
  - 고아 줄은 「스냅샷 키」 합집합으로 설정 줄에 생기고, 뒤 달로 복사된다
  - `test_logs_050.py:31-32` 가 아직 3판 꼴 본문을 보내 이 구멍을 가린다
- **고칠 것**: `key` 를 받는 줄 범위(§4.8 「줄 범위」)와 대조 · 3판 꼴은 400 · 시험 1

### W-3 풀 연결 기다림 60초 → 500 — 여러 달을 동시에 받으면 설정 · 다른 요청이 1분 멈춘 뒤 실패

- **코드**
  - `store.py:124` — 풀 `timeout=60`
  - `store.py:192` · `sales.py:322` — 달 세션이 KOS 를 받는 내내 연결 하나를 쥔다
- **SPEC**: §4.4.3(달 잠금 두 겹 — 이건 지켜짐 · 교착 아님) · §4.3 `store_failed`
- **실패 길**
  - `DB_POOL_MAX=5` 에서 다섯 달을 동시에 받으면(예: 9 · 10 · 11월 [전체 다시 받기] + 내보내기) 연결이 모두 잡힌다
  - 그사이 `GET` 의 `before` 읽기(`sales.py:339`) · PUT · lock · 상품 받기가 60초 기다린 뒤 500 `store_failed`
  - 시험 #81(풀 2 · 같은 달 4)은 통과 — 같은 달은 asyncio 잠금이 막아 연결을 안 쥔다
  - 둘째 프로세스에서는 `pg_advisory_lock` 대기가 연결을 쥔다(`store.py:196-197` · SPEC 「프로세스 둘 = 시험만」 범위라 README 한 줄로)
- **고칠 것**: 받기 동시 달 수를 `DB_POOL_MAX − 1` 로 제한(달 세션용 세마포어)하거나 풀 기다림을 `DB_LOCK_TIMEOUT_SEC` 꼴로 줄이고 문구를 남긴다 · README 에 「프로세스 둘이면 풀 연결을 쥔 채 기다림」

### W-4 front `KeyBy` 에 `product_title` 이 없다 — 계약 어긋남

- **코드**: `front/lib/types.ts:91` `KeyBy = 'product' | 'option' | 'name'` ↔ `back/app/schemas/sales.py:87` `"product" | "product_title" | "option" | "name"`
- **SPEC**: §4.2 `productKey.by` = `product · product_title · option · name` · §5.5 ②
- **실패 길**: 지금 화면은 `lines[].productKey.by` 로 가르지 않아 깨지지 않는다(설정 `rows[].by` 는 카탈로그 줄이라 늘 `product` — `fees.py:157`). 다음에 `by` 로 배지 · 셈을 가르는 코드가 들어오면 `product_title` 줄이 조용히 빠진다(타입이 막지 않음)
- **고칠 것**: `types.ts` 에 `'product_title'` 더함(FE 한 줄)

---

## NOTE

1. **lock 이 스냅샷을 만들지 않는다**
   - `settings_store.py:181-183` 은 스냅샷이 없으면 `cannot_lock` 을 낸다
   - SPEC 은 두 군데가 서로 다르다: §6.10 「PUT · `lock` 이 … 먼저 만든다」 ↔ §4.3 · §4.8 「스냅샷이 없는 달을 lock → `cannot_lock`」
   - 코드는 §4.3 · §4.8 을 따름. planner 정리 몫
2. **SPEC alembic 번호**: §4.4.2 · WORK WP-BE5 「0.5.2 = 새 판 `0002`」 ↔ 코드 `0002_product_via.py` + `0003_compositions.py`(파일 머리에 까닭) · `SCHEMA_HEAD="0003"`(`store.py:42`). SPEC · WORK 동기 몫
3. **옵션 짝짓기 경계**: `product_key.py:91-100` — 같은 title 후보 하나를 쓴 뒤 남은 하나는 금액이 달라도(부분 환불 · ② ≠ ⑤) `key_match="name"` 으로 짝지어진다. 「⑤ 옵션 하나는 한 줄에만」으로 보면 맞지만, 금액 검사 실패가 드러나지 않는다
4. **PDF 줄 갈래**: `statements.py:118` — `itemsHere = false` 이고 `netTotal != 0` 이면 먼저 「앞 달 결제 취소」 줄이 된다
   - `itemsNowhere` 이면서 실결제 ≠ 0 인 수납도 「품목이 어느 달에도 없어요」가 아니라 「앞 달 결제 취소」로 나온다
   - `netTotal = None`(통화 섞임)도 `!= 0` 이라 같은 갈래
   - 화면 `format.ts:56` 도 같은 조건이라 셋(화면 · PDF · zip 확인 창)이 서로는 같다
5. **`Counts.keysBy`**(`schemas/sales.py:37`) — SPEC §4.2 · front 타입에 없는 더한 필드(더하기만 · 깨지지 않음). SPEC 에 적거나 뺀다
6. **PDF · 미리보기에서 0원 미설정 줄이 주황 「미설정」**: `statements.py:299-300` · `StatementPreview.tsx:46`. 화면(`PurchaseGroup.tsx:30`)은 흐리게만, 주석 ② · `unsetItems` 는 0원을 빼서 「미설정 0줄」인데 주황 글자가 보인다. §6.11 「0원 … 배지 0 · `unsetItems` 안 셈」 결 — 0원 줄은 율 칸도 흐린 「—」 또는 흐린 「미설정」 권장
7. **PDF 쪽 넘김이 수납을 가른다**(`statements.py:304` — `repeatRows=1` 만): 2쪽이 손님 이름 · 결제일 없이 묶음 줄로 시작함(샘플 PDF 확인) · 묶음 줄과 「구성:」 줄이 쪽에서 갈릴 수 있음. SPEC 이 막지 않음 · 읽기 문제
8. **손님 0 채널의 [PDF] 버튼 꺼짐**(`SalesScreen.tsx:283` · `SettleTable.tsx:39`): §4.10 은 그 채널 PDF 를 「빈 명세서」로 준다고 정함 → 화면에서 닿을 길이 없다. zip 규칙과 같은 쪽이라 선택으로 봄
9. **설정 화면 브라우저 뒤로가기**(`SettingsScreen.tsx:99-108`): `beforeunload` · 메뉴 · 달 바꿈은 확인함. popstate(뒤로 · 앞으로)는 저장 안 한 변경을 묻지 않음(§3.0.5 「달 · 메뉴를 바꾸거나 페이지를 떠나면」)
10. **배지 범위**: 「KOS 목록에 없음」 = `by === 'option'` 만(`SettingsScreen.tsx:201`) — `by=product` · `inCatalog=false`(전에 받은 상품이 목록에서 빠짐 · `fees.py:166-170`) 줄엔 배지 없음. id 끝 4자리는 같은 이름이 둘일 때만(`:34-35` — fe4-fix-1 「구분용」 뜻엔 맞음 · 글자보다 좁음)
11. **GET 은 Host 검사를 안 한다**(`main.py:115` — 쓰기만): DNS rebinding 페이지는 same-origin 이라 `Sec-Fetch-Site` 막기(`api/sales.py:23`)도 안 걸리고 `GET /api/sales` 로 이름을 읽을 수 있다. §7.4 는 쓰기만 정함 → SPEC 빈칸 · OQ 로 올리기 권장(모든 경로 Host 검사 한 줄)
12. **`close_month` 의 예외 갈래**(`store.py:209-212`): 「연결을 버림」 로그 뒤에도 `putconn` 으로 풀에 돌려준다 — 잠금 풀기 실패 + 연결이 살아 있으면 세션 잠금을 쥔 연결이 풀로 돌아갈 수 있음(autocommit · 드묾)
13. **기타**
    - `migrate_sqlite` 로 옮긴 `items` 엔 `option_id` · `key_match` 가 없다(`migrate_sqlite.py:42-43` — 코디가 9 ~ 11월 [전체 다시 받기]를 이미 함 · 그 뒤 달은 해당 없음)
    - `compose.db.yaml:17-18` 이 앱 계정 비밀번호를 컨테이너 env 로 넘긴다(`docker inspect` 로 보임 · 로컬만)
    - `ruff format` 차이 43 파일

---

## 확인함 (같음)

- **돈**
  - 수수료 `(amount*bp+5000)//10000` 정수 · 미설정 0 · 1,005 × 12.5% = 126 · 0.5 경계 시험(`fees.py:51-57` · `test_fees.py:59-70`)
  - `bad_rate` 는 정수 0 ~ 10000(bool 거부) · 중복 · 500 · note 200 으로 막는다(`fees.py:81-107`)
- **스냅샷**
  - GET 쓰기 0(`sales.py:761` · `settings_store.py:73-79` 미리 보기)
  - `_ensure` = 앞의 가장 늦은 스냅샷의 저장값 복사 · 쓰기 잠금 안 · `ON CONFLICT DO NOTHING` · 검사보다 먼저 · 409 면 되돌림(`settings_store.py:109-130`)
- **J0 · lock**
  - J0 = KOS 전에 409(`sales.py:343-344`) + 쓰기 트랜잭션 안 다시 확인(`store.py:534-537`) · #91
  - lock = 지난 달 · 스냅샷 · 안 잠김 · `closed` 를 한 쓰기 트랜잭션 안에서 본다(`settings_store.py:176-193`) · `canLock` 같은 규칙(`fees.py:229`)
- **수수료 · 결산 · PDF**
  - `priorFee` 는 늘 None · `feeTotal` = 줄 합 · 통화 섞이면 None(`sales.py:737,779`)
  - `unsetItems` = 금액 > 0 · 율 null 만 — 화면 · 채널 · PDF 같음(`sales.py:795` · `channels.py:69` · `statements.py:129`)
  - 율 = 품목 달 스냅샷(#78)
  - 한 원천: 채널 · 합계 · PDF · zip = 한 `build_month` 결과(`statements.py:220-264,302` — PDF 가 다시 셈하지 않음)
  - zip = 손님 > 0 채널만 · 없으면 409 `nothing_to_export`(`statements.py:343-346`)
- **상품 키**
  - 차례 product → product_title → option → name · UNSPECIFIED · `none` 키 없음 · `nameKeyedItems` = PRODUCT_OPTION 만(`product_key.py:66-78` · `sales.py:796`)
  - 같은 이름 다른 id 따로 줄(`fees.py:150-162`)
  - 코디 9월 숫자(product 1,367 · option 914 · product_title 88 · name 110)는 코드와 맞는다(914 + 88 = 수정 1 전 option 1,002)
- **PG 잠금 · 트랜잭션**
  - 두 겹 달 잠금(asyncio → 세션 advisory · shield · finally — `sales.py:319-333` · `store.py:188-212`)
  - 쓰기 · 읽기는 그 연결에서 · KOS 동안 트랜잭션 0(autocommit) · 줄 선 요청 `(fetched_at, xmin)` 비교(`store.py:228-233`)
  - 내보내기도 달 잠금
  - 쓰기 `pg_advisory_xact_lock(41002,0)` + `lock_timeout` · 쓰기 READ COMMITTED · 읽기 REPEATABLE READ READ ONLY · `statement_timeout` 30초(`store.py:125,163-198`)
- **PG 기동 · 권한 · 마이그레이션**
  - `DATABASE_URL` 비거나 로컬 아니면 안 뜸(값 안 찍음 — `store.py:90-100`) · alembic head 다르면 안 뜸(`:132-139`)
  - 앱 계정 = 표 SELECT/INSERT/UPDATE/DELETE · `fee_rate_changes` 는 SELECT/INSERT 만 · 시퀀스 USAGE(`0001_initial.py:196-205`) · 0003 GRANT(`0003_compositions.py:43`)
  - base ↔ head 왕복 시험(`test_store_pg.py:113`) · json/jsonb 칸 0(`:51-54`)
- **⑤ · 로그**
  - ⑤ 에서 꺼내는 칸 = SPEC §7.3 목록만(`sales.py:130-165` — 가격 · 할인 · 기기 · 약물 · 메모 0)
  - 로그 = 수 · 오류 이름만 · httpx/psycopg WARNING · 접근 로그 쿼리 떼냄(`main.py:32-62`)
- **쓰기 막기 · 가드**
  - Host · Origin · JSON 415 가 POST · PUT 넷 모두에(`main.py:69-79,112-119`) · CORS GET/POST/PUT · `Content-Type` 만(`:122`)
  - cross-site GET `refresh` 403(`api/sales.py:23-24`)
  - 가드 7 · 전부 `/queries/`(`client.py:26-37`) · 경로 10 · docs 꺼짐(`main.py:104-105`)
- **도구**
  - `migrate_sqlite`: `mode=ro` · `user_version 2` · PG 비어 있지 않으면 멈춤 · 한 쓰기 트랜잭션 · 커밋 전 대조 · 출력 수만 · KOS 클라이언트 0(`migrate_sqlite.py:109-172`)
  - `backfill_compositions`: ⑤ 만 · 달 잠금 안(`backfill_compositions.py:48-62`)
- **0원 · 묶음 (0.5.2)**
  - 0원 줄 = ② 차례 그대로 · 옮기기 0 · 「ㄴ」 0 · 들여쓰기 0 · 흐리게만 · 배지 0(`PurchaseGroup.tsx:144,221`) — feedback b-1 · b-3
  - 「구성: …」 = 월별 · 유입채널 · 폰 카드 · PDF 미리보기 · PDF(`PurchaseGroup.tsx:205,267` · `StatementPreview.tsx:49`) — b-5 · b-6
  - 글 규칙 §6.11 같음(`labels.ts:81-92` · `labels.py:81-95`) · 단위 표 21 키 front = back(스크립트 대조) · `300샷`(정수)
- **PDF 줄 맞춤 (b-4)**: 머리 · 두 상자 · 요약 · 표 = 한 폭(`doc.width − 2×FRAME_PAD`) · 표 칸 비율 합 1.00 · 요약 테두리 0.75pt 하나 · 기간 31% 칸 한 줄 + 글자 줄임 · 0원 줄 포함 · 소계 · 「앞 달 결제 취소」 줄 빨강 「—」 · 주석 ① ~ ⑤ 조건 · 파일 이름 `_` · zip `_2` · 머리 줄 되풀이 · 바닥 「병원 · 번호 · n / N」
- **front**
  - 「—」 조건 `!itemsHere && netTotal !== 0`(`format.ts:56`) = PDF = zip 확인 창
  - ⚠ = `mismatch` 만 · 합 칸 ⚠ = null · 「미설정」 주황
  - 잠긴 달 [전체 다시 받기] 꺼짐 + 문구 · `exists=false` → `PUT rates: []` 한 번 · [이 달 확정] = `canLock` · 저장 안 한 변경이면 꺼짐 · 풀기 확인 창
  - `parseRate("12.35") === 1235`(정수 셈 · r7 구현 18) · 셋째 자리 · 100 초과 막음
  - `/agency` → `/channel?month=` · 폭 1280 / 768 · 미리보기 ≥ 1024 · 「세라미크」 · 「명동」 하드코딩 0(`clinicName` 만)
  - `api.ts` 쓰기 = JSON · PUT `{rates:[{key,rateBp}], note}` · lock `{}` · unlock `{confirm:true}` · `bad_origin` 「localhost:3800 으로」 안내(r7 구현 16)
- **필드 계약**: `SalesResponse` · `Purchase` · `Line` · `Counts` · `FeeRatesResponse` · `ProductsRefreshResponse` 필드 이름 · null · 타입이 하나씩 같다(W-4 · NOTE 5 빼고)
- **정리 · public**
  - `agency` 잔재: `back/app` 은 직렬화 이름 `agency`(SPEC §4.2 `channels[].agency`)뿐 · front 는 `/agency` 넘김 · `types.ts:77` 뿐
  - public: 키 · 비밀번호 · 접속 문자열 값 0 · KOS 호스트는 `.env.example` · README 예시뿐
  - allowed_paths: 바뀐 파일은 `back/**` · `front/**` · `README.md`(WP-BE4 범위) 안

## 고객이 실물에서 만날 자리

- **(F-1)** 10월 수수료율을 확정하고 명세서를 보낸 뒤 설정에서 [KOS 상품 다시 받기]를 눌렀더니, 10월 일부 품목이 「미설정 · 수수료 0」이 되거나 다른 비율로 바뀜. 잠긴 달이라 고치려면 [고치기]로 풀어야 함 — 사용자가 이미 10월 152 키를 저장했으므로 다음 상품 받기가 곧 이 자리다
- **(F-1 · W-1)** 9월 「KOS 목록에 없음」(option 키) 줄에 넣은 비율이 다음 상품 받기 뒤 사라짐(키가 product_title 로 바뀜) — 설정에는 옛 키 줄이 남아 「넣었는데 왜 미설정?」
- **(W-2)** 오타 · 옛 꼴 요청이 200 으로 받아져 설정 목록에 모르는 줄이 생기고 다음 달로 복사됨
- **(W-3)** 여러 달을 동시에 다시 받는 동안 설정 [저장]이 1분 멈춘 뒤 「저장소를 쓰지 못했어요」
- (NOTE 6) 명세서에 0원 품목 줄이 주황 「미설정」으로 찍히는데 주석은 「미설정 0줄」
- (NOTE 7) 명세서 2쪽이 손님 이름 · 결제일 없이 중간 품목 줄로 시작
- (NOTE 9) 설정에서 비율을 고치다 브라우저 뒤로가기 → 묻지 않고 사라짐

## 참고(기존 부채)

- r7 F-1(잠긴 달 [전체 다시 받기]) · W-1(GET 이 스냅샷 만듦) · W-2(풀 교착) · W-5(고정점) 는 코드에서 닫힘. W-3(양수 「앞 달 결제 취소」 수수료 「—」)은 OQ-153 · L31 그대로 열림
- OQ-132(합 기준) · OQ-154(서비스 표시 — 병원 담당자) · OQ-155(저장된 달 구성 채우기) 열림
- testcontainers 사용 중단 경고 1(시험 도구 · 동작 무관)
