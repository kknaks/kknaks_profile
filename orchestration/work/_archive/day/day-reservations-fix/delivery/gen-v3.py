import json
BASE="9bfccfb27be0b50820430d4fee01895a63a7b3bb"
OLD_G="행을 넘는 카드 = ⓖ(지나는 아래 줄 띠도 덮고 찬 자리로 셈 · 아래 줄 카드는 행 끝 자름)"
NEW_G="행을 넘는 첫 줄 카드 = ⓖ 두 조각(시작 행 첫 줄 띠 끝에서 자르고 다음 행 첫 줄 띠 안 행 시작 ~ 끝 분 · 시작 행 아래 줄 띠는 덮지 않음 · 다음 행 첫 줄 자리 셈엔 넣음 · 카드 겹침 0 · 띠도 같음 · 아래 줄 카드는 행 끝 자름) · ⓚ y 매핑 하나(분 → y = 각 줄 띠 안 분 비례 · 회색 면 · 현재 시각 선 = 그 행 모든 줄 띠 · [+] · 빈 칸 누르기 y → 시각 같은 식)"
OLD_4="열린 링크 요청 있으면 다시 씀(D44)"
NEW_4="기기 없는 열린(pending · opened) 링크 요청이 여는 시한(`expires_at`) 안이면 다시 씀(D44 · **웹 팝오버만** — 앱 JSON 경로는 늘 새 요청 · F-1)"
OLD_P="pending 줄"  # unused
SCOPE=("2026-11-28 v3 — SPEC PR mediness#971 main 머지(9bfccfb2) 뒤 재결속 · baseline = 머지된 main · 「[계약 원천] 미머지 PR」 줄 뗌. 코드 검수 · e2e 로 바뀐 계약(SPEC 에 반영됨): R45 행 넘는 첫 줄 카드 = 두 조각(시작 행 아래 줄 띠 안 덮음 · 겹침 0 — 코드 검수 F-2) · ⓚ y 매핑 하나(회색 면 · 현재 시각 선 · [+] · 빈 칸 누르기 — W-1) · F-1 앱 JSON 경로는 늘 새 요청 · D44 다시 쓰기 = 여는 시한 안 · W-a [+] · 빈 칸 누르기 시각 단위 = 그 열 그룹 간격(끌어 놓기 30분 그대로) · OQ-D43 닫힘(pending 줄 = 「남은 시간 mm:ss」만) · crm_error 에 KOS 오류 이름 · migration 0032 고객 문진 인덱스. 구현 = CENTURION_DAY#303(dev 머지 7af15621).")
def up(n,extra):
    d=json.load(open(f"{n}-request-v2.json"))
    assert d["target_delta"][0].startswith("[계약 원천]") and d["review_surface"][0].startswith("[계약 원천]")
    d["target_delta"].pop(0); d["review_surface"].pop(0)
    d["contract_version"]=3; d["spec_baseline_revision"]=BASE; d["scope_delta"]=SCOPE
    for k in ("target_delta","review_surface"):
        c=d[k][0]; assert c.startswith("[BE ↔ 웹 · 앱 계약") and OLD_G in c and OLD_4 in c
        d[k][0]=c.replace(OLD_G,NEW_G).replace(OLD_4,NEW_4)
    extra(d); json.dump(d,open(f"{n}-request-v3.json","w"),ensure_ascii=False,indent=1); return d
def be(d):
    i=[k for k,x in enumerate(d["target_delta"]) if x.startswith("팝오버 요청 흐름")][0]
    d["target_delta"][i]+=" · [v3] 다시 쓰기 = 여는 시한 안 · 웹 팝오버만(`reuse` — 앱 JSON 경로 = 늘 새 요청 · F-1) · KOS 제출 실패 `crm_error` 에 KOS 오류 이름(e2e-2 ⓐ) · migration 0032(고객 문진 인덱스)."
def web(d):
    i=[k for k,x in enumerate(d["target_delta"]) if x.startswith("누르기 · 놓기 시각")][0]
    d["target_delta"][i]="~~"+d["target_delta"][i].replace("~~","")+"~~ → [v3] W-a(qa-1 · 코디 기본값 · SPEC-006 U-10 · SPEC-007 표 빈 칸 누르기): **[+] 칸 · 빈 칸 누르기 시각 단위 = 그 열 그룹 간격**(60분 그룹 = 정각만 · 간격 없는 열 = 30분 · 등록 창 시간 늘 골라짐) · **끌어 놓기(옮기기) 단위는 30분 그대로** · y ↔ 분 = ⓚ."
    i=[k for k,x in enumerate(d["target_delta"]) if x.startswith("[문진 QR]")][0]
    d["target_delta"][i]+=" · [v3] 링크 요청 진행 칸 pending 줄 = 「남은 시간 mm:ss」만(카메라 글자 · [QR 닫기] 없앰 · OQ-D43 닫힘 · 사용자 2026-11-28)."
    d["acceptance"]=[a.replace("빈 칸 누르기 · 놓기 시각 30분 단위(1시간 행 안 위 반 · 아래 반)","[+] · 빈 칸 누르기 시각 = 그 열 그룹 간격 · 끌어 놓기 30분(W-a)") for a in d["acceptance"]]
def app(d): pass
for n,f in [("wp1-be",be),("wp2-web",web),("wp3-app",app)]: up(n,f)
c=[json.load(open(f"{n}-request-v3.json"))["target_delta"][0] for n in ("wp1-be","wp2-web","wp3-app")]
print("contract same:",len(set(c))==1)
