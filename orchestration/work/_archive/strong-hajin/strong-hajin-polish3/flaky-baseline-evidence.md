# 착수 전 기준선 — strong-hajin-polish3

- 측정: 2026-10-04 18:50 · 코드 `d1b5137`(origin/main, 변경 없음) · 코디 직접 실행
- 명령: `cd frontend && npx vitest run --no-file-parallelism`
- 결과: **Test Files 2 failed | 81 passed (83) · Tests 5 failed | 1227 passed (1232)**

## 기존 실패 5건 (이번 변경과 무관 — 직전 판 RESUME 의 「날짜 의존 실패 5건 기준선」과 같은 파일)

```
CreateWork.test.tsx > 업무 갈래의 시작일과 마감일 > 시작일이 마감일보다 늦으면 보내기 전에 막는다
CreateWork.test.tsx > 업무 갈래의 시작일과 마감일 > 적어 둔 시작일을 그대로 실어 보낸다
CreateWork.test.tsx > 요청 갈래의 시작일과 마감일 > 시작일이 마감일보다 늦으면 보내기 전에 막는다
CreateWork.test.tsx > 요청 갈래의 시작일과 마감일 > 앞뒤가 맞으면 그대로 나간다 — 막는 것은 뒤집힌 경우뿐이다
CreateWorkLayout.test.tsx > 기본 정보의 참조자와 결재자 > 요청 갈래에도 시작일이 서고 그대로 실려 나간다
```
(src/features/work/ 아래, 두 파일만 다시 돌려도 같은 5건 재현)

판정: 시작일 달력에서 날짜 칸을 찾지 못함(`querySelector` null) — 실행 날짜에 따라 달력 칸 구성이 바뀌는 날짜 의존 실패. 이후 워커·검수는 이 5건을 「기준선」으로 인용하고, 이 밖의 실패만 이번 변경의 실패로 본다.
