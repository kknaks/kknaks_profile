# WORK-006 Phase 9 최종 문구 보정 — 코드 8 을 Makefile 주석에 싣는다

- **작성**: 2026-09-23 **00:40 KST**
- **코드 워크트리**: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects` · HEAD `a1f6791`(변동 없음)
- **변경**: `Makefile` **주석 1줄 → 3줄**(주석 아닌 변경 **0줄**) + 이 보고서
- **하지 않은 것**: 스크립트 · 제품 · 설정 · 빌드 · Release · 태그 · push **전부 무편집**

---

## 1. 한 줄 결론

직전 회차에서 스크립트에 **코드 8**(대조 불가 자산)을 신설했는데, **Makefile 주석의 코드 목록은
7 에서 끊긴 채였다.** 목록을 보고 자동화를 짜는 사람이 **8 을 모르는 코드로 만나게 된다** —
그 한 줄을 채웠다. **관문 동작은 한 글자도 바뀌지 않았다.**

---

## 2. 고친 것

### 전

```make
# (0 동일 · 2 돌릴 수 없음 · 3 미검증 manifest · 4 아티팩트 없음 · 5 집합 불일치 ·
#  6 해시 불일치 · 7 조합 불일치) 인데, **GNU make 가 nonzero 를 모두 2 로 감싼다.**
```

### 후

```make
# (0 동일 · 2 돌릴 수 없음 · 3 미검증 manifest · 4 아티팩트 없음 · 5 집합 불일치 ·
#  6 해시 불일치 · 7 조합 불일치 · 8 대조 불가 자산 — candidate 에 있는데 기록에 해시가
#  없다(디렉터리 번들 `.app`). 「해시가 없다」를 「같다」로 바꾸지 않는다) 인데,
#  **GNU make 가 nonzero 를 모두 2 로 감싼다.**
```

**번호만 붙이지 않고 «무엇이 원인인지»와 «규칙»까지 한 줄에 실었다** — 목록만 보고 8 을 만난 사람이
`.app` 을 어떻게 해야 하는지(해시를 낼 수 있는 형태로 싸야 한다) 짐작할 수 있어야 한다.

---

## 3. 「한 줄 변경」 확인 — 이번 회차만의 diff

`Makefile` 의 이 타깃은 HEAD 에 없으므로 `git diff` 는 Phase 7·8·9 블록을 통째로 보여 준다.
그래서 **이번 편집만 되돌린 사본**을 scratchpad 에 만들어 그것과 비교했다(저장소는 건드리지 않았다):

```diff
 # (0 동일 · 2 돌릴 수 없음 · 3 미검증 manifest · 4 아티팩트 없음 · 5 집합 불일치 ·
-#  6 해시 불일치 · 7 조합 불일치) 인데, **GNU make 가 nonzero 를 모두 2 로 감싼다.**
+#  6 해시 불일치 · 7 조합 불일치 · 8 대조 불가 자산 — candidate 에 있는데 기록에 해시가
+#  없다(디렉터리 번들 `.app`). 「해시가 없다」를 「같다」로 바꾸지 않는다) 인데,
+#  **GNU make 가 nonzero 를 모두 2 로 감싼다.**
 # 코드를 읽어야 하는 쪽은 직접 부른다:
 #   cd frontend && node scripts/verify-release-artifact.mjs --manifest <path> --candidate <dir>
 shell-release-preflight:
```

```
주석 아닌 변경 줄: 0
```

`make -n shell-release-preflight` 출력 **불변** — **레시피는 그대로다.**

---

## 4. 검증 — 주석이 말하는 대로 실제로 도는가

| # | 실행 | 결과 |
|---|---|---|
| **C-1** | 기록된 `.app` 이 candidate 에 있는 fixture | **exit 8** · `**candidate 에 대조할 수 없는 자산이 있다** — 기록에는 있지만 **해시가 없다.**` |
| **C-2** | **현재 저장소** · 인자 없음 | **exit 2** |
| **C-3** | **현재 저장소** · 정상 fixture manifest | **exit 7** · `origin — manifest=https://app.example.com · 트리(shell.config.json)=null` |
| **C-4** | `make shell-release-preflight` | **exit 2** — 주석이 경고한 대로 **코드가 뭉개진다** |

**C-1 은 주석에 적은 숫자가 실제 동작과 같다는 확인**이고, **C-4 는 그 주석의 다른 절반
(「자동화는 이 타깃을 쓰지 말 것」)이 여전히 사실이라는 확인**이다.
코드 상수도 대조했다 — `verify-release-artifact.mjs:66  const EXIT_UNVERIFIABLE_ASSET = 8;`

---

## 5. 현재 저장소는 **여전히 통과할 수 없다**

C-2(2) · C-3(7) 이 그대로다. 이유도 그대로다: **Phase 8 관문이 아직 exit 0 이 아니고**
(운영 origin 미정), **아무것도 굽지 않아** `artifacts` 가 빌 수밖에 없다. **nonzero 가 옳은 상태다.**

---

## 6. 남은 미결 — 유지

| 항목 | 상태 |
|---|---|
| **운영 origin**(OQ-T02) | **미정** — `operationalOrigin: null` · capability `.invalid` |
| **D-4** PRODUCTION 로그인 수단 | **미결** |
| **M-10** | **미측정** — 이 관문의 통과를 설치 성공으로 쓰지 않는다 |
| **Windows 자산 전부** | **미검증** — 통과 화면에서도 «미검증»으로 적힌다 |
| **M-1** · **M-5** | **미측정** |
| 서명 · 공증 · 업데이트 | **범위 밖** |
| **N-2 프론트 스위트 불안정** | **이월** — 이번 회차는 `frontend/src` 를 건드리지 않았고 **재실행하지 않았다** |
| **잔여 우회**(스크립트를 옮기면 통과를 만들 수 있다) | Phase 8 §6 · Phase 9 §6-1 과 동일하게 **남아 있다** |

---

## 7. 금지 사항 준수

| 금지 | 확인 |
|---|---|
| 스크립트 수정 | **없음** — `frontend/scripts/verify-release-artifact.mjs` 무편집(`git status` 상 `??` 그대로) |
| 제품 · 설정 수정 | **없음** — `git diff --stat frontend/src-tauri/` 출력 0줄 |
| 빌드 · Release · 태그 · push | **없음** — `git tag --points-at HEAD` 출력 없음 · HEAD `a1f6791` |
| Makefile 레시피 변경 | **없음** — 주석만. `make -n` 출력 불변 · 주석 아닌 변경 **0줄** |
| 허용 파일 외 변경 | 없다 — `Makefile`(주석) · 보고서 1 |
