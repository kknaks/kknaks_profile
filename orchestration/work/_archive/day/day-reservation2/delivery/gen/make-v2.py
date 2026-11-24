import json, os
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "29480cfd9062e4d40ab0d273874ac42193dce98d"
SRC = ("SPEC 원천 = DAY-SPEC-007(stable · 고침 4) + DAY-SPEC-006 개정 ⑫ · ⑬ · DAY-SPEC-002 개정 ㉙(#960 이 ㉘ 을 먼저 써서 ㉘ → ㉙ 로 바꿈) · DAY-SPEC-000 2026-11-24 개정 ② — Mediness main 29480cfd(PR #961 · #962 머지 · SPEC-007 stable · spec-baseline ready). "
       "구현 = Code PR CENTURION_DAY#280(dev 스쿼시 머지 55e60aa4 · dev 배포 성공 · migration head 0028_visit_discharge_reason · 판 1 ~ 4 를 한 PR 이 덮음)")
DELTA = ("2026-11-24 재결속 — baseline = 머지된 Mediness main 29480cfd(PR #961 · #962 — SPEC-007 stable · spec-baseline:pending 뗌). 1판 화면 확인(e2e-1-feedback B1 ~ B41 · 사용자 · 코디 · 검수)으로 바뀐 계약 = DAY-SPEC-007 고침 4 · DAY-SPEC-002 개정 ㉙(#960 과 번호 겹침으로 ㉘ → ㉙ · 단계 바꾸기도 즉시 확인 B28 · 상담 대기 관리실 = 방 배정 없으면 만듦 B20 · 관리실 목록 = 방 옮기기 부품 B24 · B26 · B27) · DAY-SPEC-006 개정 ⑬(SSE 신호 = 보이는 값이 바뀐 때만 · 다시 받기 합침 B11 · B41): "
         "이전 방문 = 이번 방문 시작보다 앞선 방문(같은 날 포함 B14) · 관리실 = 접수 구역 방만 · 빈 방 먼저 · 오른쪽 「비어 있음」(B15 · B23 · B24 · B26 · B27) · 모달 다시 그릴 때 담은 값 유지(B16) · 시술 목록 = KOS 시술권 카드 모양(옵션 머리 › 구성 · n = 전체 − 남음 · 시술권 id 로 자기 줄 · 구매 전 수납 필요 시술 · 오늘 묶음 먼저 · 상품 합계 + 옵션가 B18 · B19 · B31 ~ B33) · 「시술 종료」(B36) · 「예약그룹」(B22) · 예약 단계 「오늘」 ✓(B29) · 오더 메모 = 시술 목록 아래 · 시술 대기부터 숨김(B30) · 바닥 줄 `□시술만 진행 [상담사 ▴] [관리실 ▴] [단계 버튼]` · [예약 취소] = [예약 변경] 옆 · 평소 회색(B37 ~ B40) · 초진 / 재진 = KOS isNew 그대로(B5 · B9 · B12 · B13 철회) · migration 0026 ~ 0028(rebase · dev 0024 · 0025 뒤). "
         "B42(SSE 연결 한도)는 열림 OQ-D26 · 범위 밖. 한 Code PR #280 이 판 1 ~ 4 를 덮음")
ADD = {
 "p1-reservation": ["고침 4(1판 화면 확인): 「예약그룹」 칸 이름(B22) · [예약 취소] = 「예약 정보」 줄 [예약 변경] 옆(B38) · 이전 방문 = 이번 방문 시작보다 앞선 방문 · 같은 날 포함 · 취소 · 노쇼 뺌(B14) · 초진 / 재진 = KOS isNew 그대로(B13 등 철회) · SSE `reservation` 신호 = 보이는 값이 바뀐 때만(오늘 회차 바뀜 없음 · 쓰기 큐 waiting · sent = 신호 아님 · 다른 날짜 = 지문 달라질 때만) · 다시 받기 = 받는 중 신호는 끝난 뒤 한 번으로 합침(B11 · B41) · 모달 다시 그릴 때 화면에 담은 값 유지(B16) · 모든 쓰기 즉시 확인에 change-flow-step 포함(B28 · SPEC-002 ㉙) · migration 번호 0027_detail_permission"],
 "p2-reception": ["고침 4(1판 화면 확인): 왼쪽 상담 정보 칸 없앰 → 바닥 줄 `□시술만 진행 [상담사 ▴] [관리실 ▴] [접수 / 상담 대기]`(예약 · 접수 = 고름 · 상담 대기 = 바로 KOS · 상담 진행부터 = 비활성 · 평소 회색 · 빠진 칸은 누를 때만 깜빡 B37 · B39 · B40) · [관리실 ▴] = 시술 현황 방 고르기 부품 · 그 방문 접수 구역 방만 · 빈 방 먼저 → 사용 중 · 방 순서 · 오른쪽 「비어 있음」(B15 · B23 · B24 · B26 · B27) · 상담 대기 관리실 = 「방 배정」 없으면 W8 로 만들고 방 지정 · 거절 = 공용 토스트 + 서버 값으로 다시 그림(B20 · SPEC-002 ㉙) · 단계 바꾸기(CONSULTATION_WAITING · COMPLETED)도 보낸 즉시 확인(B28) · migration 번호 0028_visit_discharge_reason"],
 "p3-procedure": ["고침 4(1판 화면 확인): 시술 목록 = KOS 시술권 카드 모양 — 묶음 머리 = 옵션 이름 › 구성 시술 · n/m = (전체 − 남음) / 전체 · 출처 = 그 고객 시술권(남은 회차 · 오늘 쓰는 것) + 구매 전 수납 필요 오늘 시술(회차 없음) · 오늘 작업은 시술권 id 로 자기 줄(새 줄 없음 · 사본 늦으면 같은 옵션 묶음) · 순서 = 오늘 받는 묶음 먼저 → 남은 시술권(B18 · B31 ~ B33) · 상태 「시술 종료」(B36) · 상품 합계 = 할인 전 가격 합 + 구매 전 수납 필요 옵션가(B19) · 「오늘」 ✓ = 오늘 ∧ 예약 · 접수 ∧ 시술만 켬(예약 단계 포함 B29) · 오더 메모 = 시술 목록 아래 · 예약 · 접수만 · 시술 대기부터 숨김 · W17 화면에서 안 씀(B30) · migration 번호 0026_purchase_base_price"],
 "p4-discharge": ["고침 4(1판 화면 확인): [귀가 처리] = 진한 회색 btn-solid-gray(B35) · 귀가 대기 바닥 줄 셀렉터 비활성 · 오더 메모 칸 숨김(B30 · B37) · COMPLETED 단계 바꾸기도 보낸 즉시 확인(B28 · SPEC-002 ㉙)"],
}
def fix(x):
    if isinstance(x,str): return x.replace("개정 ㉘","개정 ㉙").replace("002 ㉘","002 ㉙")
    if isinstance(x,list): return [fix(i) for i in x]
    if isinstance(x,dict): return {k:fix(v) for k,v in x.items()}
    return x
for n,add in ADD.items():
    r=json.load(open(f"{D}/request-{n}.json",encoding="utf-8"))
    r=fix(r)
    r["contract_version"]=2
    r["spec_baseline_revision"]=BASE
    r["scope_delta"]=DELTA
    r["review_surface"][0]=SRC
    r["target_delta"]+=add
    json.dump(r,open(f"{D}/request-v2-{n}.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
    print(n, r["title"])
