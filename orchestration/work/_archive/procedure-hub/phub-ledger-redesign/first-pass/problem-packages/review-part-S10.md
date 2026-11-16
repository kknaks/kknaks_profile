# S10 — /problems/9 P10 제모

[← review.md](review.md) · 범위 /problems/9 및 /problems/9/** 전체 · 소유 노드 98 · 말단 60 · 빈 값 0 · 직접 읽기 done

상위 문맥(공유, S00 소유): 루트 객체 → `/description` = taxonomy P1~P14 하위구조 기반 CC 자동 생성 → `/problems` 배열.

직접 읽기: reading/S10.txt 로 c0~c3 전부(procedures 5·combos 5·alternatives 4) 읽음.

## 원문 값 (문서 순서 · 전부)

| # | JSON Pointer | 원본 컬럼명 | 배열 순번 | 자료형 | 원문 값 | 관찰 참조 |
|---|---|---|---|---|---|---|
| 2624 | `/problems/9` | `(problems 원소)` | 9 | object{3} | (객체 · 키: `problem_id`, `problem`, `complaints`) |  |
| 2625 | `/problems/9/problem_id` | `problem_id` |  | string | P10 |  |
| 2626 | `/problems/9/problem` | `problem` |  | string | 제모 |  |
| 2627 | `/problems/9/complaints` | `complaints` |  | array[4] | (배열 · 4개) |  |
| 2628 | `/problems/9/complaints/0` | `(complaints 원소)` | 0 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 2629 | `/problems/9/complaints/0/cc` | `cc` |  | string | 인중/구레나룻 | OB-S10-05 |
| 2630 | `/problems/9/complaints/0/cc_detail` | `cc_detail` |  | string | 제모레이저 |  |
| 2631 | `/problems/9/complaints/0/cc_group` | `cc_group` |  | string | 얼굴 |  |
| 2632 | `/problems/9/complaints/0/procedures` | `procedures` |  | array[1] | (배열 · 1개) |  |
| 2633 | `/problems/9/complaints/0/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2634 | `/problems/9/complaints/0/procedures/0/name` | `name` |  | string | 제모레이저 |  |
| 2635 | `/problems/9/complaints/0/procedures/0/category` | `category` |  | string | M8 |  |
| 2636 | `/problems/9/complaints/0/procedures/0/role` | `role` |  | string | 모근 파괴 |  |
| 2637 | `/problems/9/complaints/0/procedures/0/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 2638 | `/problems/9/complaints/0/procedures/0/products/0` | `(products 원소)` | 0 | string | 클라리티2 |  |
| 2639 | `/problems/9/complaints/0/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 2640 | `/problems/9/complaints/0/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 2641 | `/problems/9/complaints/0/combos/0/name` | `name` |  | string | 제모 시리즈 | OB-S10-03 |
| 2642 | `/problems/9/complaints/0/combos/0/combo` | `combo` |  | array[1] | (배열 · 1개) | OB-S10-03 |
| 2643 | `/problems/9/complaints/0/combos/0/combo/0` | `(combo 원소)` | 0 | string | 제모레이저 |  |
| 2644 | `/problems/9/complaints/0/combos/0/reason` | `reason` |  | string | 다회차 시술로 영구적 모발 감소(반영구) | OB-S10-01 |
| 2645 | `/problems/9/complaints/0/combos/0/evidence` | `evidence` |  | string | 5~8회 시리즈 권장; 완전·영구 제거를 보장하지 않으며 주기적 유지관리가 필요할 수 있음 | OB-S10-02 |
| 2646 | `/problems/9/complaints/0/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 2647 | `/problems/9/complaints/0/alternatives/0` | `(alternatives 원소)` | 0 | string | IPL 제모도 대안 | OB-S10-07 |
| 2648 | `/problems/9/complaints/1` | `(complaints 원소)` | 1 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 2649 | `/problems/9/complaints/1/cc` | `cc` |  | string | 겨드랑이/팔/다리 | OB-S10-05 |
| 2650 | `/problems/9/complaints/1/cc_detail` | `cc_detail` |  | string | 제모레이저 |  |
| 2651 | `/problems/9/complaints/1/cc_group` | `cc_group` |  | string | 바디(여성) |  |
| 2652 | `/problems/9/complaints/1/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 2653 | `/problems/9/complaints/1/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2654 | `/problems/9/complaints/1/procedures/0/name` | `name` |  | string | 제모레이저 |  |
| 2655 | `/problems/9/complaints/1/procedures/0/category` | `category` |  | string | M8 |  |
| 2656 | `/problems/9/complaints/1/procedures/0/role` | `role` |  | string | 모근 파괴 |  |
| 2657 | `/problems/9/complaints/1/procedures/0/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 2658 | `/problems/9/complaints/1/procedures/0/products/0` | `(products 원소)` | 0 | string | 클라리티2 |  |
| 2659 | `/problems/9/complaints/1/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2660 | `/problems/9/complaints/1/procedures/1/name` | `name` |  | string | 보톡스 |  |
| 2661 | `/problems/9/complaints/1/procedures/1/category` | `category` |  | string | M1 |  |
| 2662 | `/problems/9/complaints/1/procedures/1/role` | `role` |  | string | 다한증 완화 | OB-S10-04 |
| 2663 | `/problems/9/complaints/1/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 2664 | `/problems/9/complaints/1/procedures/1/products/0` | `(products 원소)` | 0 | string | 보톡스 |  |
| 2665 | `/problems/9/complaints/1/procedures/1/products/1` | `(products 원소)` | 1 | string | 나보타 |  |
| 2666 | `/problems/9/complaints/1/combos` | `combos` |  | array[2] | (배열 · 2개) |  |
| 2667 | `/problems/9/complaints/1/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 2668 | `/problems/9/complaints/1/combos/0/name` | `name` |  | string | 제모 시리즈 |  |
| 2669 | `/problems/9/complaints/1/combos/0/combo` | `combo` |  | array[1] | (배열 · 1개) |  |
| 2670 | `/problems/9/complaints/1/combos/0/combo/0` | `(combo 원소)` | 0 | string | 제모레이저 |  |
| 2671 | `/problems/9/complaints/1/combos/0/reason` | `reason` |  | string | 다회차 시술로 영구적 모발 감소(반영구) |  |
| 2672 | `/problems/9/complaints/1/combos/0/evidence` | `evidence` |  | string | 5~8회 시리즈 권장; 완전·영구 제거를 보장하지 않으며 주기적 유지관리가 필요할 수 있음 |  |
| 2673 | `/problems/9/complaints/1/combos/1` | `(combos 원소)` | 1 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 2674 | `/problems/9/complaints/1/combos/1/name` | `name` |  | string | 제모 + 다한증보톡스 | OB-S10-04 |
| 2675 | `/problems/9/complaints/1/combos/1/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 2676 | `/problems/9/complaints/1/combos/1/combo/0` | `(combo 원소)` | 0 | string | 제모레이저 |  |
| 2677 | `/problems/9/complaints/1/combos/1/combo/1` | `(combo 원소)` | 1 | string | 보톡스 |  |
| 2678 | `/problems/9/complaints/1/combos/1/reason` | `reason` |  | string | 털 제거 + 땀 감소 |  |
| 2679 | `/problems/9/complaints/1/combos/1/evidence` | `evidence` |  | string | 동시 시술 가능 |  |
| 2680 | `/problems/9/complaints/1/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 2681 | `/problems/9/complaints/1/alternatives/0` | `(alternatives 원소)` | 0 | string | IPL 제모도 대안 |  |
| 2682 | `/problems/9/complaints/2` | `(complaints 원소)` | 2 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 2683 | `/problems/9/complaints/2/cc` | `cc` |  | string | 비키니 |  |
| 2684 | `/problems/9/complaints/2/cc_detail` | `cc_detail` |  | string | 제모레이저 |  |
| 2685 | `/problems/9/complaints/2/cc_group` | `cc_group` |  | string | 바디(여성) |  |
| 2686 | `/problems/9/complaints/2/procedures` | `procedures` |  | array[1] | (배열 · 1개) |  |
| 2687 | `/problems/9/complaints/2/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2688 | `/problems/9/complaints/2/procedures/0/name` | `name` |  | string | 제모레이저 |  |
| 2689 | `/problems/9/complaints/2/procedures/0/category` | `category` |  | string | M8 |  |
| 2690 | `/problems/9/complaints/2/procedures/0/role` | `role` |  | string | 모근 파괴 |  |
| 2691 | `/problems/9/complaints/2/procedures/0/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 2692 | `/problems/9/complaints/2/procedures/0/products/0` | `(products 원소)` | 0 | string | 클라리티2 |  |
| 2693 | `/problems/9/complaints/2/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 2694 | `/problems/9/complaints/2/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 2695 | `/problems/9/complaints/2/combos/0/name` | `name` |  | string | 제모 시리즈 |  |
| 2696 | `/problems/9/complaints/2/combos/0/combo` | `combo` |  | array[1] | (배열 · 1개) |  |
| 2697 | `/problems/9/complaints/2/combos/0/combo/0` | `(combo 원소)` | 0 | string | 제모레이저 |  |
| 2698 | `/problems/9/complaints/2/combos/0/reason` | `reason` |  | string | 다회차 시술로 영구적 모발 감소(반영구) |  |
| 2699 | `/problems/9/complaints/2/combos/0/evidence` | `evidence` |  | string | 5~8회 시리즈 권장; 완전·영구 제거를 보장하지 않으며 주기적 유지관리가 필요할 수 있음 |  |
| 2700 | `/problems/9/complaints/2/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 2701 | `/problems/9/complaints/2/alternatives/0` | `(alternatives 원소)` | 0 | string | IPL 제모도 대안 |  |
| 2702 | `/problems/9/complaints/3` | `(complaints 원소)` | 3 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 2703 | `/problems/9/complaints/3/cc` | `cc` |  | string | 수염/가슴/등 | OB-S10-05 |
| 2704 | `/problems/9/complaints/3/cc_detail` | `cc_detail` |  | string | 제모레이저 · Nd:YAG | OB-S10-06 |
| 2705 | `/problems/9/complaints/3/cc_group` | `cc_group` |  | string | 남성 |  |
| 2706 | `/problems/9/complaints/3/procedures` | `procedures` |  | array[1] | (배열 · 1개) |  |
| 2707 | `/problems/9/complaints/3/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2708 | `/problems/9/complaints/3/procedures/0/name` | `name` |  | string | 제모레이저 |  |
| 2709 | `/problems/9/complaints/3/procedures/0/category` | `category` |  | string | M8 |  |
| 2710 | `/problems/9/complaints/3/procedures/0/role` | `role` |  | string | 모근 파괴 |  |
| 2711 | `/problems/9/complaints/3/procedures/0/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 2712 | `/problems/9/complaints/3/procedures/0/products/0` | `(products 원소)` | 0 | string | 클라리티2 |  |
| 2713 | `/problems/9/complaints/3/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 2714 | `/problems/9/complaints/3/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 2715 | `/problems/9/complaints/3/combos/0/name` | `name` |  | string | 제모 시리즈 |  |
| 2716 | `/problems/9/complaints/3/combos/0/combo` | `combo` |  | array[1] | (배열 · 1개) |  |
| 2717 | `/problems/9/complaints/3/combos/0/combo/0` | `(combo 원소)` | 0 | string | 제모레이저 |  |
| 2718 | `/problems/9/complaints/3/combos/0/reason` | `reason` |  | string | 다회차 시술로 영구적 모발 감소(반영구) |  |
| 2719 | `/problems/9/complaints/3/combos/0/evidence` | `evidence` |  | string | 5~8회 시리즈 권장; 완전·영구 제거를 보장하지 않으며 주기적 유지관리가 필요할 수 있음 |  |
| 2720 | `/problems/9/complaints/3/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 2721 | `/problems/9/complaints/3/alternatives/0` | `(alternatives 원소)` | 0 | string | IPL 제모도 대안 |  |

## 잠정 관찰 (원문 칸과 분리)

| ID | 상태 | 위치 | 관찰 |
|---|---|---|---|
| OB-S10-01 | P | `/problems/9/complaints/0/combos/0/reason` | reason '다회차 시술로 영구적 모발 감소(반영구)' — 본문은 '영구적', 괄호는 '반영구' 로 한 값 안에서 정도가 서로 다르게 표현된다. evidence 도 '완전·영구 제거를 보장하지 않으며' 로 영구성을 부정한다. 어느 쪽이 원문의 뜻인지 정하지 않는다(I-08). |
| OB-S10-02 | P | `/problems/9/complaints/0/combos/0/evidence` | evidence 는 세미콜론으로 두 진술: '5~8회 시리즈 권장' ; '완전·영구 제거를 보장하지 않으며 주기적 유지관리가 필요할 수 있음'. 회차 범위(~)·권장·부정(않으며)·가능성(필요할 수 있음)이 들어 있다. |
| OB-S10-03 | P | `/problems/9/complaints/0/combos/0/name`<br>`/problems/9/complaints/0/combos/0/combo` | combo name '제모 시리즈' 는 원소 1개(제모레이저) 단독 묶음이다. 회차 표현(시리즈)이 name 에 들어 있다(README: 회차는 일정 수식어). |
| OB-S10-04 | P | `/problems/9/complaints/1/procedures/1/role`<br>`/problems/9/complaints/1/combos/1/name` | c1 의 보톡스 role 은 '다한증 완화', combo name 은 '제모 + 다한증보톡스' 로 원소('보톡스')와 표기가 다르다(I-02 같은 유형). evidence '동시 시술 가능' — 가능성·동시성 진술. |
| OB-S10-05 | P | `/problems/9/complaints/0/cc`<br>`/problems/9/complaints/1/cc`<br>`/problems/9/complaints/3/cc` | cc 가 부위 나열('인중/구레나룻', '겨드랑이/팔/다리', '수염/가슴/등')이고 cc_detail 이 시술('제모레이저'), cc_group 이 대상 집단('얼굴', '바디(여성)', '남성') 이다. cc_group 에 성별 표현이 들어 있다(F-03 같은 유형). |
| OB-S10-06 | K | `/problems/9/complaints/3/cc_detail` | cc_detail '제모레이저 · Nd:YAG' — 'Nd:YAG' 에 콜론이 포함된 장비 표기. 형태소 분절 확인(K-04). |
| OB-S10-07 | P | `/problems/9/complaints/0/alternatives/0` | alternatives 'IPL 제모도 대안' — 대안 표현. 'IPL 제모' 는 procedures 에 없다. |

## 수동 복합 표현 (직접 읽기 · 출현별)

| 표현 | 위치(Pointer · 값 내 구간) | 관점(탐색용, 확정 분류 아님) |
|---|---|---|
| 인중/구레나룻 | `/problems/9/complaints/0/cc` [0,7) | 부위 표현, 기호(/) |
| 겨드랑이/팔/다리 | `/problems/9/complaints/1/cc` [0,9) | 부위 표현, 기호(/) |
| 수염/가슴/등 | `/problems/9/complaints/3/cc` [0,7) | 부위 표현, 기호(/) |
| 바디(여성) | `/problems/9/complaints/1/cc_group` [0,6)<br>`/problems/9/complaints/2/cc_group` [0,6) | 부위 표현, 대상 집단(성별), 괄호 보충 |
| 제모레이저 · Nd:YAG | `/problems/9/complaints/3/cc_detail` [0,14) | 시술·장비 표현, 기호(· 띄어 씀), 혼합 표기 |
| 다회차 시술로 영구적 모발 감소(반영구) | `/problems/9/complaints/0/combos/0/reason` [0,22)<br>`/problems/9/complaints/1/combos/0/reason` [0,22)<br>`/problems/9/complaints/2/combos/0/reason` [0,22)<br>`/problems/9/complaints/3/combos/0/reason` [0,22) | 회차(다회차), 수단(-로)+결과, 정도 수식(영구적), 괄호 보충(반영구), 값 내부 정도 불일치 |
| 5~8회 시리즈 권장 | `/problems/9/complaints/0/combos/0/evidence` [0,11)<br>`/problems/9/complaints/1/combos/0/evidence` [0,11)<br>`/problems/9/complaints/2/combos/0/evidence` [0,11)<br>`/problems/9/complaints/3/combos/0/evidence` [0,11) | 범위(~), 회차, 권고(권장) |
| 5~8회 | `/problems/9/complaints/0/combos/0/evidence` [0,4)<br>`/problems/9/complaints/1/combos/0/evidence` [0,4)<br>`/problems/9/complaints/2/combos/0/evidence` [0,4)<br>`/problems/9/complaints/3/combos/0/evidence` [0,4) | 범위(~), 회차 |
| 완전·영구 제거를 보장하지 않으며 주기적 유지관리가 필요할 수 있음 | `/problems/9/complaints/0/combos/0/evidence` [13,50)<br>`/problems/9/complaints/1/combos/0/evidence` [13,50)<br>`/problems/9/complaints/2/combos/0/evidence` [13,50)<br>`/problems/9/complaints/3/combos/0/evidence` [13,50) | 부정(않으며), 가능성(-ㄹ 수 있음), 주기 표현(주기적), 기호(·) |
| 털 제거 + 땀 감소 | `/problems/9/complaints/1/combos/1/reason` [0,11) | 기호(+), 감소 표현 |
| 동시 시술 가능 | `/problems/9/complaints/1/combos/1/evidence` [0,8) | 동시성(동시), 가능성(가능) |
| 제모 + 다한증보톡스 | `/problems/9/complaints/1/combos/1/name` [0,11) | combo name(원소와 다른 표기), 기호(+) |
| 다한증 완화 | `/problems/9/complaints/1/procedures/1/role` [0,6) | role 표현, 증상 표현, 감소 표현(완화) |
| IPL 제모도 대안 | `/problems/9/complaints/0/alternatives/0` [0,10)<br>`/problems/9/complaints/1/alternatives/0` [0,10)<br>`/problems/9/complaints/2/alternatives/0` [0,10)<br>`/problems/9/complaints/3/alternatives/0` [0,10) | 대안 표현, 약어(IPL), 추가(도) |
| 모근 파괴 | `/problems/9/complaints/0/procedures/0/role` [0,5)<br>`/problems/9/complaints/1/procedures/0/role` [0,5)<br>`/problems/9/complaints/2/procedures/0/role` [0,5)<br>`/problems/9/complaints/3/procedures/0/role` [0,5) | role 표현, 기전 표현 |

## 이 구획에서 연 미결

- **I-08** (I) 한 combo 안에서 '영구적 모발 감소' 와 '(반영구)' 와 '완전·영구 제거를 보장하지 않으며' 가 함께 나온다. — 영향: 효과 지속성 정보를 한 값으로 뽑으면 서로 맞지 않는 정도가 섞인다.
