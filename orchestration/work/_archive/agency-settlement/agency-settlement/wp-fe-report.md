# WORK-001 WP-FE 결과 보고
## 상태: done

## 수행 — 파일·화면 목록
- 복사(머리 「원본:」 주석): tailwind.config.ts · postcss.config.mjs · eslint.config.mjs · next.config.ts(standalone 뺌) · global.d.ts · app/styles/ceramique-theme.css · app/styles/medikit-patches.css · app/globals.css(html,body · a · .cc-btn 만) · app/layout.tsx(flag-icons 뺌 · 제목 「Céramique 명동점 · 월별 매출」 · robots noindex) · lib/time.ts(pad·toMs·hm + md·mdOfDate·월 계산) · lib/api.ts(API_BASE·CONFIG_ERROR·ApiError + getSales 하나) · public/ceramique-logo-color.svg · tsconfig.json(JSON 이라 주석 없음)
- 새로 만듦: package.json(medikit 1.4.0 · next 16 · 포트 3800 · flag-icons·qrcode 없음) · package-lock.json · .gitignore · .env.example · lib/types.ts(§4.2) · lib/labels.ts(§6.3) · app/page.tsx(?month= · 기본 이번 달 KST) · components/monthly/{MonthlySales,MonthPicker,CountsLine,SalesTable,PurchaseGroup,StatusView}.tsx · format.ts
- 스크린샷(가짜 이름 홍** 등 · 가짜 금액 · scratchpad 의 가짜 back): /private/tmp/claude-501/-Users-kknaks-orca-workspaces-agency-settlement-agency-settlement/caf95cf3-5253-478e-97ea-447abe5563d3/scratchpad/shots/
  - table.png — 묶음 · 품목 줄 · payment 줄 · 음수 cancel/spent 줄 · 「품목은 다른 달에 · 첫 승인 09-15」 · 「시각 없음」 · 「이름 없음」 · ⚠ 결제 ≠ 품목 · ⚠ 통화 섞임 · 품목을 찾지 못했어요 · 제외 1 · (없음) 유입 · 100 USD
  - loading.png · empty.png · error.png(502 kos_unavailable 메시지) · network.png · config.png — §3.4 상태 5종
  - badmonth.png — ?month=2026-13 → back 400 bad_month 메시지 그대로

## 검증
- cd front && npm install && npx tsc --noEmit && npm run lint && npm run build → 전부 통과(오류 0 · 경고 0)
- grep -rn "procedure/\|cc-prototype" front(app components lib · 설정) = 「원본:」 주석만 · localStorage/sessionStorage 0 · fetch 는 lib/api.ts 에만
- 띄워 본 포트 3891(front dev) · 8891(가짜 back) — 끝나고 내림(LISTEN 0 확인)

## WORK-001 WP-FE 완료 조건
- §3.4 상태 5종 스크린샷: 충족
- 묶음 스크린샷: 충족
- payment 줄 스크린샷: 충족
- 음수 줄 스크린샷: 충족
- 경고 배지 2종(⚠ 결제 ≠ 품목 · ⚠ 통화 섞임) 스크린샷: 충족
- cc-prototype import 0(grep = 「원본:」 주석만): 충족
- localStorage · sessionStorage 0: 충족
- 검증 명령 tsc · lint · build: 충족

## 계약 대조
- lib/types.ts 필드 이름 = SPEC §4.2 = back/app/schemas/sales.py(읽기만 대조) — 전부 같음
- nullable 차이: back 은 visitorId · lines[].currency · lines[].paymentType 을 null 허용. §4.2 예시엔 null 이 없음 → front 는 null 도 받게 넓힘(화면 영향 없음). 계약을 좁힐지 넓힐지는 코디 판단
- 오류: {error:{code,message}} 의 message 그대로 표시(§4.3) · 네트워크 = 「back 에 연결하지 못했어요(back 이 떠 있나요?)」 · 설정 = CONFIG_ERROR(front/.env.local 안내)
- 정렬 §3.3 은 front 도 같은 규칙으로 다시 정렬(back 이 정렬해 줘도 결과 같음)

## 이슈 · 코디가 확인할 것(시안 없음 → OQ-113 기본값으로 정한 자리)
1. 결제 수단 이름은 SPEC 에 나온 CARD 카드 · CASH 현금 · PREPAID_CARD 선불카드 만. 스펙 enum 의 PLATFORM · TRANSFER · EASY_PAY · MEDICAL_LOAN 은 KOS 값 그대로 보임 — 이름을 정해 주면 labels.ts 한 곳만 고치면 됨
2. 배지 색: 승인·결제 = primary · 부분 환불 = warning · 환불·취소 = danger · 미수납/그 밖 = neutral · 경고 2종 = warning
3. 안내 한 줄의 `환불` 은 ‘환불’ 로 표시
4. 결제·취소·환불 줄의 paymentType 은 화면에 안 보임(§3.2 에 칸 없음)
5. ?month= 꼴이 틀리면 그대로 back 에 보내 400 bad_month 메시지를 보여 줌 · [›] 는 이번 달 기준
6. 「다시 시도」 는 refresh 없이 · 「다시 불러오기」 만 refresh=1
7. 머리의 「그달 결제」 는 취소만 있는 수납에서도 「그달 결제 0」 으로 보임
8. medikit Loading 은 크기 prop 이 없어 기본 크기(작음)
9. back 과 실제로 붙여 보는 건 아직(WP-BE 뒤 · WP-LIVE)
