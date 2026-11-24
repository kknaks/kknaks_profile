## 회차 요약

| 회차 | 이해 호출 | 2차 규칙 | 바꾼 것 | 자료 토큰(지금 697,892) | 감소 | 빠짐 | 얇아진 인용(이름만) | JSON 깨짐 | 이해 ms 중앙 / 최대 |
|---|---|---|---|---:|---:|---:|---:|---:|---|
| r1_rules1 | 호출 1 | 1 | 초안 1 · 2차 1판(명동점 밖 하위 뺌 · layers 그대로) | 236,618 | 66.1% | 22/276 (8.0%) | — | 0 | 2609 / 5352 |
| r1_rules2 | 호출 1 | 2 | 같은 JSON · 2차 2판(명동점 닿는 하위 늘 · 밖은 이름만) | 343,474 | 50.8% | 5/276 (1.8%) | — | 0 | 2609 / 5352 |
| r2_rules2 | 호출 2 | 2 | 초안 2(offer · layers 기본 sub · 밖 이어 묻기 all) · 2차 2판 | 360,121 | 48.4% | 0/276 (0.0%) | — | 1 | 2566 / 5667 |
| r2_rules3 | 호출 2 | 3 | 같은 JSON · 2차 3판(부위만 턴 = 주제 진료항목 대상만 · 이름만 줄은 머리도 이름만) | 268,141 | 61.6% | 0/276 (0.0%) | — | 1 | 2566 / 5667 |
| r3_rules3 | 호출 3 | 3 | 초안 2 그대로 다시 호출(흔들림 확인) · 2차 3판 ← **채택** | 268,141 | 61.6% | 0/276 (0.0%) | 24 | 0 | 2646 / 6270 |
| r3_rules4 | 호출 3 | 4 | 같은 JSON · 2차 4판(안 — 명동점 밖 하위의 안전 줄도 이름만) | 248,279 | 64.4% | 0/276 (0.0%) | 28 | 0 | 2646 / 6270 |

## 턴별(채택 r3_rules3)

| 대화 | 턴 | 말 | JSON kinds | about / layers / scope / lineup | 지금 → 새 토큰 | 감소 | 인용 | 빠짐 | 얇아진 | 이해 ms | 이해 출력 tok |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 03b8 | 1 | 팔자주름에 대해서 고민이돼 | [] | targets / sub / branch / none | 606 → 606 | 0.0% | 8 | 0 | 0 | 2672 | 147 |
| 03b8 | 2 | 미간에 주름도 고민이야 | [] | targets / sub / branch / none | 403 → 403 | 0.0% | 5 | 0 | 0 | 2729 | 179 |
| 03b8 | 3 | 얼굴에 탄력이 좀 떨어지는거 같은데 | [] | targets / sub / branch / none | 1,168 → 1,168 | 0.0% | 14 | 0 | 0 | 2788 | 179 |
| 03b8 | 4 | 그중에서 소프웨이브, 써마지, 울쎄라만 관심이 잇어 | [] | targets / sub / branch / none | 6,149 → 6,149 | 0.0% | 23 | 0 | 0 | 2638 | 189 |
| 03b8 | 5 | 고주파 원리가 머야 ? | mechanism, overview | targets / sub / branch / none | 7,098 → 4,629 | 34.8% | 5 | 0 | 0 | 2420 | 165 |
| 03b8 | 6 | 응 고주파에 대해서 전반적으로 설명해줘 | indication, lineup, mechanism, outcome, overview | targets / sub / branch / names | 41,217 → 25,454 | 38.2% | 10 | 0 | 3 | 2614 | 188 |
| fixE | 1 | 요즘 피부 탄력이 저하 되서 고민이야 | [] | targets / sub / branch / none | 1,157 → 1,157 | 0.0% | 4 | 0 | 0 | 2400 | 147 |
| fixE | 2 | 얼굴에 | [] | topic / sub / branch / none | 198,080 → 16,423 | 91.7% | 0 | 0 | 0 | 2405 | 159 |
| fixE | 3 | 얼굴에 | [] | topic / sub / branch / none | 193,287 → 13,928 | 92.8% | 5 | 0 | 0 | 2616 | 159 |
| 73bd | 1 | 얼굴에 피부 탄력이 없어져서 걱정이야 | [] | targets / sub / branch / none | 1,157 → 1,157 | 0.0% | 3 | 0 | 0 | 2807 | 180 |
| 73bd | 2 | 아 주름이 눈가 입꼬리에 잇어 | [] | targets / sub / branch / none | 625 → 625 | 0.0% | 4 | 0 | 0 | 5627 | 661 |
| 73bd | 3 | 아 눈가는 볼뉴머 이ㅃ고리는 필러를 맞고 싶어 | [] | targets / sub / branch / none | 398 → 398 | 0.0% | 2 | 0 | 0 | 3156 | 278 |
| 3016 | 2 | 보톡스 효과가 없어 ? | indication, outcome | targets / sub / branch / none | 17,126 → 10,381 | 39.4% | 7 | 0 | 0 | 3038 | 164 |
| 3016 | 3 | 부작용은 ? | adverse, recovery | targets / sub / branch / none | 79,884 → 79,884 | 0.0% | 33 | 0 | 0 | 2536 | 166 |
| a7d7 | 1 | 팔자 주름이 고민이야 | [] | targets / sub / branch / none | 606 → 606 | 0.0% | 7 | 0 | 0 | 2779 | 158 |
| a7d7 | 2 | 미간에 주름도 너무 깊어 | [] | targets / sub / branch / none | 403 → 403 | 0.0% | 5 | 0 | 0 | 2697 | 179 |
| a7d7 | 3 | 보톡스로 맞고 싶어서 | [] | targets / sub / branch / none | 17,904 → 13,682 | 23.6% | 8 | 0 | 0 | 2427 | 150 |
| a7d7 | 6 | 팔자주름에 보톡스 말고 다른 시술은 없어서 그대로 둔거 | indication | targets / sub / branch / none | 3,099 → 1,363 | 56.0% | 1 | 0 | 0 | 6270 | 738 |
| a7d7 | 8 | 볼뉴머가 머야 | indication, lineup, mechanism, outcome, overview | targets / sub / branch / names | 11,438 → 11,240 | 1.7% | 9 | 0 | 0 | 2951 | 185 |
| a578 | 2 | 지금 턱이 이중턱이 됫어 ㅠㅠ | [] | targets / sub / branch / none | 628 → 628 | 0.0% | 6 | 0 | 0 | 2862 | 179 |
| a578 | 4 | 기기 리프팅이지 그럼 | [] | targets / sub / branch / none | 23,105 → 9,542 | 58.7% | 5 | 0 | 0 | 2567 | 145 |
| a578 | 5 | 아니 기기 리프팅 추천 해줘 | indication, lineup | targets / sub / branch / names | 20,959 → 14,260 | 32.0% | 5 | 0 | 2 | 2692 | 156 |
| a578 | 7 | 슈링크로 턱라인 타이트닝이 돼 ? | indication, outcome | targets / sub / branch / none | 427 → 427 | 0.0% | 2 | 0 | 0 | 2874 | 194 |
| 5bce | 2 | 턱 보톡스 맞고 싶다고 | [] | targets / sub / branch / none | 1,965 → 1,965 | 0.0% | 3 | 0 | 0 | 2687 | 184 |
| 5bce | 3 | 턱이 이중턱이라고 | [] | targets / sub / branch / none | 1,058 → 1,058 | 0.0% | 5 | 0 | 0 | 2664 | 180 |
| 5bce | 4 | 볼살도 너무 많아 | [] | targets / sub / branch / none | 148 → 148 | 0.0% | 2 | 0 | 0 | 2543 | 179 |
| 5bce | 5 | 미간 주름도 잇어 | [] | targets / sub / branch / none | 634 → 634 | 0.0% | 4 | 0 | 0 | 2457 | 158 |
| 5bce | 6 | 미간주름에 보톡스만 가능해 ? | combo, indication | targets / sub / branch / none | 27,455 → 21,906 | 20.2% | 6 | 0 | 3 | 2627 | 194 |
| dc78 | 1 | 볼에 살이 많아서 고민이돼 | [] | targets / sub / branch / none | 146 → 146 | 0.0% | 2 | 0 | 0 | 2650 | 179 |
| dc78 | 3 | 그럼 지방 분해주사 뭐뭐 잇어 ? | lineup | targets / sub / branch / names | 1,257 → 585 | 53.4% | 9 | 0 | 8 | 2538 | 154 |
| dc78 | 4 | 응 어떤 원리인지 어떤 시술인지 궁금해 | indication, lineup, mechanism, outcome, overview | targets / sub / branch / names | 13,831 → 5,502 | 60.2% | 4 | 0 | 2 | 2646 | 176 |
| dc78 | 5 | 그럼 미간 주름은 어떻게 없애 ? | indication | targets / sub / branch / none | 634 → 634 | 0.0% | 6 | 0 | 0 | 3035 | 185 |
| dc78 | 6 | 그럼 기기 리프팅 뭐 하면 좋을까 ? | indication, lineup | targets / sub / branch / names | 3,538 → 1,580 | 55.3% | 8 | 0 | 6 | 2514 | 159 |
| dc78 | 7 | 써마지 받아보고 싶어 | [] | targets / sub / branch / none | 1,665 → 1,665 | 0.0% | 4 | 0 | 0 | 2348 | 147 |
| dc78 | 8 | 응 써마지 몇샷 맞아야해 ? | offer, outcome | targets / sub / branch / none | 648 → 648 | 0.0% | 2 | 0 | 0 | 2554 | 162 |
| 02af | 1 | 얼굴 타이트닝을 받아야 하는데 어떤 시술이 잇어 ? | indication, lineup | targets / sub / branch / names | 2,836 → 2,836 | 0.0% | 12 | 0 | 0 | 2890 | 194 |
| 02af | 2 | 아 눈가에는 써마지 받고 싶어서 | [] | targets / sub / branch / none | 284 → 284 | 0.0% | 1 | 0 | 0 | 5991 | 640 |
| 02af | 3 | 그럼 실 리프팅은 없어 명동점에 ? | lineup | targets / sub / branch / names | 637 → 0 | 100.0% | 0 | 0 | 0 | 2370 | 153 |
| 02af | 4 | 아 그럼 써마지로 안내해줘 | [] | targets / sub / branch / none | 1,574 → 1,574 | 0.0% | 3 | 0 | 0 | 2556 | 147 |
| 02af | 5 | 입꼬리에는 어떤 시술들이 잇어 ? 주름이 고민이야 | indication, lineup | targets / sub / branch / names | 298 → 298 | 0.0% | 3 | 0 | 0 | 4478 | 483 |
| 02af | 6 | 이마에 주름이 많으면 어떤 시술을 받아 ? | indication | targets / sub / branch / none | 392 → 392 | 0.0% | 5 | 0 | 0 | 2564 | 185 |
| 7897 | 1 | 팔자 주름이 고민이야 | [] | targets / sub / branch / none | 606 → 606 | 0.0% | 7 | 0 | 0 | 2461 | 158 |
| 7897 | 2 | 볼뉴머에 대해서 설명해줄래 ? | indication, lineup, mechanism, outcome, overview | targets / sub / branch / names | 11,362 → 11,167 | 1.7% | 19 | 0 | 0 | 2604 | 185 |
| **합** | 43 | | | | **697,892 → 268,141** | **61.6%** | 276 | **0** | 24 | 중앙 2646 | 9247 |
