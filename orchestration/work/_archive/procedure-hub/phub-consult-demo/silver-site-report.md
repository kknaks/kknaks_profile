# silver 부위 3단 — 리포트(워커 · 2026-11-19)

> 브리프 `silver-site-task.md` + 추가 지시 1 · 2(`silver-site-addendum1.md` · `silver-site-addendum2.md`). 작업 사본 `silver-model/` 에서만 고쳤다. 원본 silver-model · 허브 레포 · DB 수정 0 · 커밋 0.
> 병원 이름 · 진료항목 코드 · KOS 값은 공개 silver 에 0이다. 「명동점」 글자는 로컬 근거 파일 `user.csv` 의 basis 칸에만 있다.

## 1. 결과 한 줄

silver 패치를 넣고, 추가 지시 1 · 2 대로 작업 사본 검사 스크립트를 고친 뒤 전부 다시 돌렸다. **silver-check PASS (WARN 5) · gold-check PASS(FAIL 0 · WARN 10)**. WARN 은 전부 작업 사본 밖 git 변경(코디 변경 5 · 데이터 아님)이다. `gold_hash` **ece5d2be…** · `aux_hash` **e0813c0a…**(§4).

## 2. 바뀐 수(원본 대비)

| 무엇 | 전 → 후 | 내용 |
|---|---|---|
| site 행 | 89 → **115** | 새 부위 **26**(SITE-121 ~ 146 = 배치표 추가 24 + 2단 「귀」 SITE-121 · 「기타」 SITE-122) |
| site `parent_code` 이동 | **69** 행 | 배치표 이동 48 + 3단 밖 21 이 자리를 잡음. 「눈」 SITE-018 은 그대로(최상위 · 예외 1) |
| site `description` | **6** 행 | 사지 · 상체 · 체간 · 코안면 = 「묶음 부위(3단 조사 처리).」 · 중안면 「묶음 부위(얼굴 가운데).」 · 하안면 「묶음 부위(하관).」 |
| 깊이 | 1단 3(전신 · 얼굴 · 눈) · 2단 30 · 3단 82 | 깊이 4 이상 0 |
| alias | 980 → **992**(+12) | 넥 · 콧볼 · 힙 · 겨 · 구렛나루 · 풀페이스 · 입술위 · 눈썹뼈 · 상완(의학 용어) · 양볼 · 아이 · 하관전체. **「애교」 는 이미 있어 넣지 않음**(`alias.csv:308`) |
| anatomy_site | 89 → **92**(+3) | ANS-0090 ANA-075↔SITE-144 침샘 · ANS-0091 ANA-106↔SITE-143 쇄골 · ANS-0092 ANA-064↔SITE-140 승모근 |
| source_ref | 48,113 → **48,226**(+113 · 끝에 덧붙임) | `user.csv` 근거 **101**(parent_code 78 = 이동 69 + 원장 근거 새 부위 9 · description 6 · 새 행 전체 17 = 근거 없음 15 + 귀 + 기타) · 원장 포인터 **12**(새 부위 9 · anatomy_site 3) |
| 로컬 근거 파일 | 새로 | `silver-model/drafts/clinic-supplement/clinic-a-20261119/user.csv` 113 줄(+헤더) · 칸 `line,kind,target_table,target_code,name,field,decision,basis,status`(status 는 모두 「확인」) |

- 새 부위 자리: 심부볼 · 나비존 = 볼 / 침샘 · 턱밑샘 = 턱 / 귀밑샘 = 귀 / 쇄골 · 뒷목 = 목 / 부유방 · 유륜 = 가슴 / 승모근 = 어깨 / 앞허벅지 · 허벅지 안 · 밖 · 승마 · 발목 = 다리 / 상복부 · 하복부 · 베렛나루 = 복부 / 하완 · 팔꿈치 · 손목 = 팔 / 손가락 = 손 / 발가락 · 발등 = 발 / 관절 SITE-108 = 몸 > 기타.
- 확정 변경 반영: 머리 SITE-088 = 얼굴 2단(두피 · 정수리 · 헤어라인이 아래) · 귀(새) = 얼굴 2단(이개 · 이주 · 이하부 · 귀밑샘) · 팔자주름 · 구레나룻 → 볼 · 마리오네트라인 · 잇몸 · 구강 → 입 · 비강 · 부비동 → 코 · 수염 → 턱 · 중안면 · 하안면 · 코안면 = 얼굴 바로 아래 묶음 · 사지 · 상체 · 체간 = 전신 바로 아래 묶음.
- 원장 근거 새 부위 9 의 `source_ref`(field 빈칸)는 `research-site-tree.md` §3 의 포인터를 그대로 썼다. 심부볼 `anatomy-danger-zones.json:/zones/6/tissue_data/buccal_fat_pad` · 허벅지 안 · 밖 · 승마 `market-pricing.json:/categories/13/items/3/name` · 승모근 `problem-packages.json:/problems/10/complaints/3/cc` · 쇄골 `anatomy-danger-zones.json:/zones/10/tissue_data/platysma_coverage` · 침샘 · 귀밑샘 · 턱밑샘 `anatomy-danger-zones.json:/zones/6/vessels/0/course`. anatomy_site 침샘은 `literature-evidence.json:/categories/M1/adverse_effects/1/patient_ko`(「턱 아래 침샘」)를 썼다.
- 패치는 스크립트로 했다. `drafts/clinic-supplement/clinic-a-20261119/build_site_3tier.py` 가 기준 사본 `archive/silver-before-clinic-a-20261119/silver/` 에서 네 파일과 user.csv 를 다시 쓴다. 다시 돌려도 같은 바이트다(확인함).
- 생성 문서 둘을 다시 뽑았다. `notes/silver-tables.md`(`silver-check.py --write-docs` · 행 수만 바뀜)와 `notes/vocabulary.csv`(`glossary-build.py` · 셈만 바뀜).

## 3. 검사 결과(추가 지시 2 반영 뒤 · 최종)

### silver-check(작업 사본 `drafts/silver-check/silver-check.py`)

```
D3 · S1(user.csv 101 줄 풀림 · 출처 종류 'user' 101) · A1~A8 · D1~D10 · C* · O* · E* · I* · S2 · G1 · G2 : 통과
G3 : FAIL 0 · WARN 5   M .gitignore · M orchestration/config/projects/procedure-hub.json · M orchestration/work/README.md
                       · M para/projects/company/procedure-hub/work-index.md · ?? reference/2026-11-19-myeongdong-kos/
silver 해시 43ff9f45227e74dacb297f0e79912c350a78aee5cee8f271a6279d344fb735c2
PASS (WARN 5)
```

### gold-build → gold-check(작업 사본 `gold/`)

```
A1 · A2 · A3 · K1~K7 · M1 · V1 · Q1 · H1 · G1 : 통과 (15/15)
WARN A2 ×5   silver-check G3 WARN(위 5 줄)
WARN G1 ×5   작업 사본 밖 변경(데이터 아님) — 같은 5 줄
== FAIL 0 · WARN 10
PASS
```

- 부정 시험 1회: SITE-014 name_ko 를 「이마부」 로 바꾸면 A1 FAIL 1(「site SITE-014 칸 name_ko 바뀜」) · A3 FAIL 1(「site.csv 재현 다름(보강 + 묶음)」)로 잡힌다. 되돌린 뒤 build_site_3tier.py 로 다시 쓰고 gold 를 다시 빌드했다. 해시는 §4 와 같다.
- 원본 그대로 돌린 기준 줄: silver-check PASS · gold-check 는 G1 6 만 FAIL(워크트리 변경 · 같은 원인).

## 4. gold · 해시

| 파일 | 행 | 바뀜 |
|---|---|---|
| g_entry | 2642 → **2680**(+38 = 새 부위 이름 26 + 다른 이름 12) | gid 를 빼고 보면 새 38 + **근거 종류만 바뀐 26**(아래). 다만 새 행이 중간에 끼어 gid 가 밀려 바이트로는 1,779 줄이 다르다 |
| g_evidence | 27740 → **27779**(+39) | gold_id 를 빼고 보면 −26 / +65 |
| 나머지 13 표 + questions | 같음 | 바이트 0 차이. **3단 계층은 gold 에 안 보인다**(gold-build 가 `site.parent_code` 를 안 읽음 — 리뷰 F-12) |

- `gold_hash` **8accbb21… → ece5d2be6e93723fdc4dd6b254ae259aab5ea4e114e0536ab428db612ed39062**(gold 16 파일 · 허브 `inputs.py` 와 같은 식)
- `aux_hash` **93ec89fd… → e0813c0a30fee732a4940f6edc704660cf532564c0161923fbfd2ea9a8e3344b**(source_ref 만 바뀜 · concern · adverse · condition · concern_site · ledger-check-list 는 같음)
- gold-build 끝 줄이 출력하는 「gold 해시」(e07d20cd…)는 다른 식(questions 포함 여부)이라 허브 값과 다르다. 위 두 값을 쓴다.
- 근거 종류: site 입구 186 = 원장 135 · 원장 + 사용자 제공 34 · 사용자 제공 17.
  - 「사용자 제공」 만인 것 = 원장 근거가 없는 새 부위 17(근거 없음 15 + 귀 + 기타).
  - 「원장 + 사용자 제공」 34 가운데 **26 은 기존 입구**(SITE-120 이름 + 이동한 부위의 기존 별칭 25 — 경부 · 하지 · 팔자 · 비순구 …)다. 이 26 행이 위 「근거 종류만 바뀐 26」 이다. 별칭 입구가 자기 근거(field=alias)가 없으면 부위 행 근거 전체를 받는데(`gold-build.py:147`), 그 안에 parent_code 근거 줄이 섞여 들어간 것이다.

## 5. 멈춘 자리 → 코디 답(추가 지시 2)으로 닫음

1. **A1** → (a) 묶음 기준 사본 `archive/silver-before-clinic-a-20261119/silver/` 를 기준으로 삼는다(패치 전 silver · 원본 아카이브 silver 와 바이트 같음 — 확인함). 허용은 다음 셋이다.
   - site: 기존 행은 parent_code 칸과 「묶음 부위」 로 시작하는 description 만 바뀔 수 있고, 새 행은 끝에 덧붙인다.
   - alias · anatomy_site: 기준 바이트 + 끝 덧붙임.
   - source_ref: 기준 바이트 + 끝 덧붙임(ref 머리 `drafts/clinic-supplement/` 또는 대상이 새 site · anatomy_site 행).
   - 그 밖 표 바이트 · 표 목록 · external_code · drafts/gold 는 그대로다.
2. **A3** → `silver-supplement.py` 재현 위에 `build_site_3tier.py <기준> <폴더>` 재현을 겹친다. 그 결과 7 파일 + user.csv 를 바이트로 대조한다.
3. **G1 · G3** → 경로를 `phub-consult-demo/` 로 바꿨다. 작업 사본 밖 변경은 WARN 으로만 남긴다. A2 는 silver-check 의 WARN 이 G3 뿐이면 통과하고, 그 줄을 WARN 으로 옮겨 적는다.
4. **별칭 근거 종류 섞임 → 받아들임(이번 판)**: **이동한 부위의 기존 별칭 25 + SITE-120 이름 입구의 근거 종류가 「원장 + 사용자 제공」** 이다(전에는 「원장」). gold-build 는 고치지 않았다(§4).

## 6. 고친 스크립트 줄(작업 사본만)

### 6-1. 추가 지시 1(고치기 전 사본 `silver-model/archive/scripts-before-addendum1/`)

고치기 전 사본은 `silver-model/archive/scripts-before-addendum1/` 에 있다.

```diff
--- drafts/silver-check/silver-check.py
-LEDGER = os.path.join(WORK, 'phub-recommend', 'bronze', 'phub-ledger')
-STEP1 = os.path.join(WORK, 'phub-recommend', 'step1-products.json')
+PHUB_REC = os.path.join(WORK, '_archive', 'procedure-hub', 'phub-recommend')
+LEDGER = os.path.join(PHUB_REC, 'bronze', 'phub-ledger')
+STEP1 = os.path.join(PHUB_REC, 'step1-products.json')
@@ resolve
+    if fn.startswith('drafts/clinic-supplement/') and fn.endswith('/user.csv'):   # L<줄> · status = 확인 줄만
+        rows = list(csv.reader(open(os.path.join(SM, fn), encoding='utf-8-sig')))
+        n = int(re.fullmatch(r'L(\d+)', ptr).group(1))
+        if not 2 <= n <= len(rows): raise KeyError(ref)
+        d = dict(zip(rows[0], rows[n - 1]))
+        if d['status'] != '확인': raise KeyError(ref)
+        return 'user', d['name'] + '\n' + d['decision'] + '\n' + d['basis']
@@ ref_kind
-    if ref.startswith('사용자'):
+    if ref.startswith(('사용자', 'drafts/clinic-supplement/')):
@@ D3
+    linked = {(r['site_code'], r['anatomy_code']) for r in D['anatomy_site']}
     for n, cs in sa.items():
+        if len(cs) == 2 and (cs[0], cs[1]) in linked or len(cs) == 2 and (cs[1], cs[0]) in linked:
+            continue          # anatomy_site 로 이어진 같은 이름 짝 허용
--- gold/gold-build.py  ev_kind  ·  gold/gold-check.py  ev_kind  (같은 한 줄)
-    if ref.startswith('사용자'):
+    if ref.startswith(('사용자', 'drafts/clinic-supplement/')):
--- gold/gold-check.py  g1
-        if 'orchestration/work/phub-ledger-redesign/' not in l or (… 'orchestration/work/phub-ledger-redesign/_RESUME.md'))
+        if 'orchestration/work/phub-consult-demo/' not in l or (… 'orchestration/work/phub-consult-demo/_RESUME.md'))
```

순서 목록(`gold-build.py:100-101` · `gold-check.py` `KINDS`)에는 새 값을 넣지 않았다. 기존 「사용자 제공」 을 쓴다.

### 6-2. 추가 지시 2(고치기 전 사본 `silver-model/archive/scripts-before-addendum2/`)

```diff
--- 추가지시1후/silver-check.py
+++ drafts/silver-check/silver-check.py
@@ -984,10 +984,11 @@
                 if not hashlib.sha256(open(os.path.join(LEDGER, parts[-1]), 'rb').read()).hexdigest().startswith(parts[0]):
                     hit('G2', 'FAIL', parts[-1], '-', '원장 HASHES.txt 와 다름')
         gs = subprocess.run(['git', '-C', REPO, 'status', '--porcelain'], capture_output=True, text=True).stdout.splitlines()
-        bad = [l for l in gs if 'orchestration/work/phub-ledger-redesign/' not in l
-               or (not l.startswith('??') and not l.endswith('orchestration/work/phub-ledger-redesign/_RESUME.md'))]
+        # 작업 사본(phub-consult-demo · 추가 지시 2): 산출물 = phub-consult-demo/ 아래 새 파일. 그 밖(코디 변경 등 데이터 아님)은 WARN 으로만
+        bad = [l for l in gs if 'orchestration/work/phub-consult-demo/' not in l
+               or (not l.startswith('??') and not l.endswith('orchestration/work/phub-consult-demo/_RESUME.md'))]
         for l in bad:
-            hit('G3', 'FAIL', 'git', l, '산출물 밖 변경')
+            hit('G3', 'WARN', 'git', l, '작업 사본 밖 변경(데이터 아님 — WARN)')
 
     # ---- 셈 · 알려진 빈칸
     K = collections.OrderedDict()
```

```diff
--- 추가지시1후/gold-check.py
+++ gold/gold-check.py
@@ -34,6 +34,7 @@
 REPO = subprocess.run(['git', '-C', HERE, 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip()
 SEP = ' · '
 FAIL = []
+WARN = []          # 추가 지시 2 — 작업 사본 밖 변경(G1 · A2 의 G3)
 
 
 def bad(c, msg):
@@ -66,41 +67,55 @@
 CS_ADD_IDS = [f'CSI-{n:04d}' for n in range(99, 107)]          # concern_site 보강 8행(사용자 11-17 · WORK-015 §3-2)
 
 
+CLINIC_BASE = os.path.join(SM, 'archive', 'silver-before-clinic-a-20261119', 'silver')          # 묶음 기준 사본(추가 지시 2 · A1 (a))
+CLINIC_REF = 'drafts/clinic-supplement/'
+
+
 def a1():
+    """silver 변경 = 묶음 clinic-a-20261119 허용 목록뿐(기준 = 묶음 기준 사본 · 추가 지시 2).
+    site: 기존 행은 parent_code 칸 · 묶음 부위 description(「묶음 부위」 로 시작) 만 바뀜 · 새 행은 끝에 덧붙임.
+    alias · anatomy_site: 기준 바이트 + 끝 덧붙임. source_ref: 기준 바이트 + 끝 덧붙임(ref 머리 drafts/clinic-supplement/ 또는 대상이 새 행).
+    그 밖 표 바이트 그대로 · 표 목록 같음 · drafts/gold 그대로."""
     import csv as _c, io as _io
-    for fn in sorted(os.listdir(ARC)):
-        a, b = open(os.path.join(ARC, fn), 'rb').read(), open(os.path.join(SILVER, fn), 'rb').read()
-        if fn == 'procedure_relation.csv':
-            la, lb = a.decode('utf-8').split('\n'), b.decode('utf-8').split('\n')
-            if len(la) != len(lb) or lb[0] != la[0] + SAME_DAY_HDR:
-                bad('A1', 'procedure_relation 줄 수 · 헤더가 「끝 칸 2 덧붙임」 아님')
+    def rows(p):
+        return list(_c.reader(_io.StringIO(open(p, 'rb').read().decode('utf-8-sig'), newline='')))
+    for fn in sorted(os.listdir(CLINIC_BASE)):
+        pa, pb = os.path.join(CLINIC_BASE, fn), os.path.join(SILVER, fn)
+        if not os.path.exists(pb):
+            bad('A1', f'{fn} 없어짐')
+            continue
+        a, b = open(pa, 'rb').read(), open(pb, 'rb').read()
+        if fn == 'site.csv':
+            ra, rb = rows(pa), rows(pb)
+            if ra[0] != rb[0] or len(rb) < len(ra):
+                bad('A1', 'site.csv 헤더 · 행 수')
                 continue
-            for x, y in zip(la[1:], lb[1:]):
-                if not x:
-                    ok_ = y == ''
-                else:
-                    ok_ = y.startswith(x + ',') and len(next(_c.reader(_io.StringIO(y[len(x) + 1:])))) == 2
-                if not ok_:
-                    bad('A1', f'procedure_relation 기존 줄이 바뀜 「{x[:40]}」')
-                    break
-        elif fn == 'source_ref.csv':
+            h = ra[0]
+            pc, ds = h.index('parent_code'), h.index('description')
+            for x, y in zip(ra[1:], rb[1:]):
+                for k in range(len(h)):
+                    if x[k] != y[k] and not (k == pc or (k == ds and y[k].startswith('묶음 부위'))):
+                        bad('A1', f'site {x[0]} 칸 {h[k]} 바뀜(허용 = parent_code · 묶음 description)')
+            new_site = {r[0] for r in rb[len(ra):]}
+        elif fn in ('alias.csv', 'anatomy_site.csv'):
             if not b.startswith(a):
-                bad('A1', 'source_ref.csv 앞쪽(기존 행) 바이트가 바뀜')
-            for r in _c.reader(_io.StringIO(b[len(a):].decode('utf-8'))):
-                if not (r[0] == 'product_procedure' or (r[0] == 'procedure_relation' and r[2] == 'same_day_text')
-                        or (r[0] == 'concern_site' and r[2] == '' and r[1] in CS_ADD_IDS)):
-                    bad('A1', f'source_ref 덧붙인 행이 목록 밖 {r}')
-        elif fn == 'concern_site.csv':
-            add = list(_c.reader(_io.StringIO(b[len(a):].decode('utf-8')))) if b.startswith(a) else None
-            if add is None or [r[0] for r in add] != CS_ADD_IDS or any(len(r) != 3 for r in add):
-                bad('A1', 'concern_site.csv 가 「기준 바이트 + 끝 8줄 CSI-0099~0106」 아님')
+                bad('A1', f'{fn} 앞쪽(기존 행) 바이트가 바뀜')
+        elif fn == 'source_ref.csv':
+            continue          # site · anatomy_site 를 본 뒤(아래)
         elif a != b:
             bad('A1', f'{fn} 바뀜')
+    new_site = {r[0] for r in rows(os.path.join(SILVER, 'site.csv'))[1:]} - {r[0] for r in rows(os.path.join(CLINIC_BASE, 'site.csv'))[1:]}
+    new_ans = {r[0] for r in rows(os.path.join(SILVER, 'anatomy_site.csv'))[1:]} - {r[0] for r in rows(os.path.join(CLINIC_BASE, 'anatomy_site.csv'))[1:]}
+    a, b = open(os.path.join(CLINIC_BASE, 'source_ref.csv'), 'rb').read(), open(os.path.join(SILVER, 'source_ref.csv'), 'rb').read()
+    if not b.startswith(a):
+        bad('A1', 'source_ref.csv 앞쪽(기존 행) 바이트가 바뀜')
+    else:
+        for r in _c.reader(_io.StringIO(b[len(a):].decode('utf-8'))):
+            if not (r[3].startswith(CLINIC_REF) or (r[0] == 'site' and r[1] in new_site) or (r[0] == 'anatomy_site' and r[1] in new_ans)):
+                bad('A1', f'source_ref 덧붙인 행이 목록 밖 {r}')
     now = sorted(f for f in os.listdir(SILVER) if f.endswith('.csv'))
-    want = sorted(os.listdir(ARC) + ['product_procedure.csv', 'external_code.csv', 'concept_image.csv', 'concept_image_label.csv'])
-    if now != want:
-        bad('A1', f'silver 표 목록 ≠ archive + product_procedure + external_code + concept_image · concept_image_label: {sorted(set(now) ^ set(want))}')
-    # 용어집 작업(사용자 11-16) — external_code 는 헤더만 · 행 0(설계)
+    if now != sorted(os.listdir(CLINIC_BASE)):
+        bad('A1', f'silver 표 목록 ≠ 묶음 기준 사본: {sorted(set(now) ^ set(os.listdir(CLINIC_BASE)))}')
     if open(os.path.join(SILVER, 'external_code.csv'), 'rb').read() != '\ufeffid,target_table,target_code,system,code,label,relation,note\n'.encode('utf-8'):
         bad('A1', 'external_code.csv 가 헤더만(행 0)이 아님')
     dg = os.path.join(SM, 'drafts', 'gold')
@@ -115,9 +130,23 @@
     tmp = tempfile.mkdtemp(prefix='silver-supp-')
     try:
         subprocess.run([sys.executable, os.path.join(HERE, 'silver-supplement.py'), tmp], capture_output=True, text=True, check=True)
-        for fn in ('procedure_relation.csv', 'product_procedure.csv', 'source_ref.csv', 'concern_site.csv'):
+        # 묶음 clinic-a-20261119(추가 지시 2): 보강 재현 위에 build_site_3tier.py 재현을 겹친다
+        base2 = os.path.join(tmp, 'base2')
+        os.makedirs(base2)
+        for fn in ('site.csv', 'alias.csv', 'anatomy_site.csv'):
+            shutil.copy(os.path.join(ARC, fn), os.path.join(base2, fn))
+        shutil.copy(os.path.join(tmp, 'silver', 'source_ref.csv'), os.path.join(base2, 'source_ref.csv'))
+        out2 = os.path.join(tmp, 'clinic')
+        subprocess.run([sys.executable, os.path.join(SM, 'drafts', 'clinic-supplement', 'clinic-a-20261119', 'build_site_3tier.py'), base2, out2],
+                       capture_output=True, text=True, check=True)
+        for fn in ('procedure_relation.csv', 'product_procedure.csv', 'concern_site.csv'):
             if open(os.path.join(tmp, 'silver', fn), 'rb').read() != open(os.path.join(SILVER, fn), 'rb').read():
                 bad('A3', f'silver {fn} 재현 다름')
+        for fn in ('site.csv', 'alias.csv', 'anatomy_site.csv', 'source_ref.csv'):
+            if open(os.path.join(out2, 'silver', fn), 'rb').read() != open(os.path.join(SILVER, fn), 'rb').read():
+                bad('A3', f'silver {fn} 재현 다름(보강 + 묶음)')
+        if open(os.path.join(out2, 'user.csv'), 'rb').read() != open(os.path.join(SM, 'drafts', 'clinic-supplement', 'clinic-a-20261119', 'user.csv'), 'rb').read():
+            bad('A3', '묶음 근거 파일 user.csv 재현 다름')
         if open(os.path.join(tmp, 'same-day-judgment.csv'), 'rb').read() != open(os.path.join(NOTES, 'same-day-judgment.csv'), 'rb').read():
             bad('A3', 'notes/same-day-judgment.csv 재현 다름')
     finally:
@@ -134,8 +163,15 @@
 def a2():
     out = subprocess.run([sys.executable, os.path.join(SM, 'drafts', 'silver-check', 'silver-check.py')], capture_output=True, text=True).stdout
     last = out.strip().splitlines()[-1] if out.strip() else ''
-    if last != 'PASS (WARN 0)':
-        bad('A2', f'silver-check 끝 줄 「{last}」')
+    if last == 'PASS (WARN 0)':
+        return
+    # 작업 사본 밖 변경 G3 WARN 만 있으면 통과(추가 지시 2) — WARN 으로 옮겨 적는다
+    st = json.load(open(os.path.join(SM, 'drafts', 'silver-check', 'check-stats.json'), encoding='utf-8'))
+    if re.fullmatch(r'PASS \(WARN \d+\)', last) and st['warn'] and all(w[0] == 'G3' for w in st['warn']):
+        for w in st['warn']:
+            WARN.append(('A2', f'silver-check G3 WARN {w[3]}'))
+        return
+    bad('A2', f'silver-check 끝 줄 「{last}」')
 
 
 # ---------------------------------------------------------------- 읽기
@@ -427,7 +463,7 @@
     gs = subprocess.run(['git', '-C', REPO, 'status', '--porcelain'], capture_output=True, text=True).stdout.splitlines()
     for l in gs:
         if 'orchestration/work/phub-consult-demo/' not in l or (not l.startswith('??') and not l.endswith('orchestration/work/phub-consult-demo/_RESUME.md')):
-            bad('G1', f'산출물 밖 변경 {l}')
+            WARN.append(('G1', f'작업 사본 밖 변경(데이터 아님 — WARN) {l}'))          # 추가 지시 2
 
 
 print('== gold-check')
@@ -443,6 +479,8 @@
 print(f'== 구조 문제 {len(STRUCT)}' + (' ' + ' · '.join(STRUCT) if STRUCT else ''))
 for c, m in FAIL[:40]:
     print('  FAIL', c, m)
-print(f'== FAIL {len(FAIL)}')
+for c, m in WARN:
+    print(f'  WARN {c} {m}')
+print(f'== FAIL {len(FAIL)} · WARN {len(WARN)}')
 print('PASS' if not FAIL and not STRUCT else 'FAIL')
 sys.exit(0 if not FAIL and not STRUCT else 1)
```

```diff
--- 추가지시1후/build_site_3tier.py
+++ build_site_3tier.py
@@ -5,13 +5,16 @@
 다시 돌려도 같은 바이트. 다른 silver 표는 건드리지 않는다.
 
   python3 drafts/clinic-supplement/clinic-a-20261119/build_site_3tier.py      # silver-model/ 기준
+  python3 …/build_site_3tier.py <기준 silver 폴더> <폴더>   # <폴더>/silver · <폴더>/user.csv 로만 씀(gold-check A3 재현 대조용)
 """
-import csv, io, os
+import csv, io, os, sys
 
 HERE = os.path.dirname(os.path.abspath(__file__))
 SM = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
-BASE = os.path.join(SM, 'archive', 'silver-before-clinic-a-20261119', 'silver')
-OUT = os.path.join(SM, 'silver')
+BASE = sys.argv[1] if len(sys.argv) > 2 else os.path.join(SM, 'archive', 'silver-before-clinic-a-20261119', 'silver')
+OUTDIR = sys.argv[2] if len(sys.argv) > 2 else None
+OUT = os.path.join(OUTDIR, 'silver') if OUTDIR else os.path.join(SM, 'silver')
+USER_OUT = os.path.join(OUTDIR, 'user.csv') if OUTDIR else os.path.join(HERE, 'user.csv')
 BUNDLE = 'clinic-a-20261119'
 UREF = f'drafts/clinic-supplement/{BUNDLE}/user.csv'
 BASIS = '사용자 결정 2026-11-19 · 명동점 KOS 진료항목명'          # 로컬 근거 파일에만(공개 silver 에는 자리만)
@@ -116,6 +119,7 @@
 
 
 def main():
+    os.makedirs(OUT, exist_ok=True)
     site, alias, ans, sref = rd('site'), rd('alias'), rd('anatomy_site'), rd('source_ref')
     H = site[0]
     ci = {c: i for i, c in enumerate(H)}
@@ -184,7 +188,8 @@
     wr(os.path.join(OUT, 'alias.csv'), alias)
     wr(os.path.join(OUT, 'anatomy_site.csv'), ans)
     wr(os.path.join(OUT, 'source_ref.csv'), sref)
-    wr(os.path.join(HERE, 'user.csv'), U)
+    os.makedirs(OUT, exist_ok=True)
+    wr(USER_OUT, U)
     print(f'이동 {len(moved)} · 새 부위 {len(NEW)} · alias +{len(ALIAS)} · anatomy_site +{len(ANS)} · source_ref +{len(NEW_SR)} · user.csv {len(U) - 1}줄')
 
 
```

## 7. 확인 필요

- **다른 이름 12 의 근거는 user.csv 에 기록만** 했다(source_ref 없음 · 해당 줄 kind 「다른 이름(기록만 · source_ref 없음)」). 처음에는 `(site, code, alias)` 근거를 달았다. 그런데 gold-build 가 그 부위의 **기존 별칭 입구 17 개 근거까지** 그 user.csv 줄로 바꿨다(안면부 · 눈가 · 뺨 · 경부 …). source_ref 는 별칭 낱말별로 가를 수 없어서 뺐다. 지금 새 별칭 입구는 부위 행 근거를 받는다. 기존 site 별칭도 alias 근거가 있는 부위는 5 곳(SITE-036 · 070 · 073 · 077 · 120)뿐이고, 나머지는 이 꼴이다.
- 「팔 상완」 → `상완`(kind 의학 용어) · 「하관(전체)」 → `하관전체`(괄호는 A6 금지) — 추가 지시 1 대로.
- `site.parent_code` 의 스키마 뜻은 「원장이 포함 관계로 적은 것만」 인데, 이번 이동은 사용자 결정이다. 근거는 field=parent_code 줄로 user.csv 에 있다. 스키마 문구(`silver-schema.json`)는 안 고쳤다.
- 입구 글자 겹침(표를 건넘 · resolve `ambiguous`): 이번에 **새로 생긴** 것 = 「기타」(concern CON-278) · 「승모근」(anatomy ANA-064 + offer OFR-0009) · 「쇄골」(ANA-106) · 「침샘」(ANA-075). 원래 있던 것(팔자주름 · 사각턱 · 이중턱 · 전신 · 마리오네트라인 …)도 그대로다.
- 새 부위 name_en 은 표준 표기를 「보충」 으로 채웠고, 모르는 4 는 빈칸이다(기타 · 심부볼 · 베렛나루 · 나비존).
- 검사를 돌리려고 원본에서 **복사(수정 없음)** 해 온 것이 있다. `drafts/{silver-check,glossary,gold,external-research}` 와 `archive/silver-before-gold-final` 이다. 작업 사본에는 이것이 없어서 검사가 못 돌았다. 모두 gitignore 아래에 있다.
