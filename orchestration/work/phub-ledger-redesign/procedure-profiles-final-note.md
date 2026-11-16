# procedure-profiles 1차 — 최종 기록 보완 (재검토 W1·W2)

- 작업: researcher 워커, task `task_b7dbfe6293a4` / dispatch `ctx_8807fc1633a5`, 2026-11-09
- 근거: [재검토 리포트](./procedure-profiles-rereview-report.md) — 판정 **WARN(경미)**, W1·W2
- 수정한 파일: `first-pass/procedure-profiles/` 의 issues.md · validation.md · review.md, 그리고 `_RESUME.md`. JSON·코드·토큰은 재생성하지 않았다.

## W1(b) — 범위 밖 알려진 오분절 2출현을 기록 (표시는 하지 않음)

| 위치 | 값 기준 구간 | 파일 코드포인트 | 원문 | 원시 Kiwi 토큰 | 후속 위험 |
|---|---|---|---|---|---|
| `/profiles/13/aftercare/0` | [6,8) 「발적」 | [10509,10511) | 시술 부위 발적/부종 1-2주 가능 | 발/NNG [6,7) + 적/XSN [7,8) | 형태소 기반 부위 후보에 **거짓 부위 「발」** |
| `/profiles/2/practicalNotes/2` | [66,68) 「수화」 | [2605,2607) | …핵심은 희석·수화·주입 깊이) | 수/NNG [66,67) + 화/XSN [67,68) | 거짓 용어 「수」. 같은 원장의 「재수화」 표시(SR14)와 비일관 |

- 기록 위치: issues.md A1-W1, validation.md §2b 끝, review.md §6.
- 두 값의 기존 `segmentation_review` 표시(SR33·SR32)는 다른 토큰에 대한 것이다.
- 표현 후보는 표면형 기준이라 이 두 오분절의 영향을 받지 않는다.
- 문서에 다음 한계를 적었다: 원시 형태소 출력에는 알려진 오류가 남아 있고, 지정 품사(MAG·MM·NR·NP·MAJ)와 서명 16종 밖의 정확성은 보장하지 않는다.

## W2 — 미판정 근거 토큰 46건을 명시

- modifier_phrase 근거 토큰 96개의 품사: MAG 39 · MM 11 · VA 24 · VA-I 6 · XR 14 · VCN 2.
- VA·VA-I·XR·VCN 46건은 출현 판정 범위 밖이다. 직접 세어 확인했다(unjudged 46).
- verify.py 는 판정 목록에 없는 근거 토큰을 **correct 로 간주**하도록 구현돼 있다. 「양방향」 검사는 범위 안 50건에만 성립한다.
- 재검토자는 46건을 문맥과 대조했고, 현재 추가 오태깅은 없었다고 보고했다. 이것은 사람 대조 결과이며 verify 가 보장하는 것이 아니다. validation.md §2c 에 이 둘을 구분해 적었다.

## 검증

```sh
python3 orchestration/work/phub-ledger-redesign/first-pass/procedure-profiles/verify.py   # exit 0, failure_count 0
shasum -a 256 orchestration/work/phub-recommend/bronze/phub-ledger/procedure-profiles.json
# a1fe389d83430002f3d78e7c07ead4a7675d4afcfb68d28f9ac94042a5423f3e  (불변)
```

## 상태

- **1차 수집 범위**: 재검토가 제시한 조건부 종료 요건(W1 기록)을 기록으로 충족했다. **코디 확인 전이다.**
- **원장 전체**: 미완료다. 남은 것은 B 10묶음 · 잠정 2 · 보류 2(전 C1·C2, 사용자 결정 아님) · 후속 9이며, 의미 조사·정규화는 실행하지 않았다.
- 모든 토큰이 정확하다고 보장하지 않는다.
