# S11 — /problems/10 P11 얼굴윤곽

[← review.md](review.md) · 범위 /problems/10 및 /problems/10/** 전체 · 소유 노드 231 · 말단 151 · 빈 값 3 · 직접 읽기 done

상위 문맥(공유, S00 소유): 루트 객체 → `/description` = taxonomy P1~P14 하위구조 기반 CC 자동 생성 → `/problems` 배열.

직접 읽기: reading/S11.txt 로 c0~c6 전부(procedures 15·combos 9·alternatives 10) 읽음. c2 의 긴 cc_detail 은 괄호·세미콜론 단위로 다시 읽음. 단서 대조(cue-review) 후 c5·c6 P1 role '장기 콜라겐' 수동 표현 누락을 보강.

## 원문 값 (문서 순서 · 전부)

| # | JSON Pointer | 원본 컬럼명 | 배열 순번 | 자료형 | 원문 값 | 관찰 참조 |
|---|---|---|---|---|---|---|
| 2722 | `/problems/10` | `(problems 원소)` | 10 | object{3} | (객체 · 키: `problem_id`, `problem`, `complaints`) |  |
| 2723 | `/problems/10/problem_id` | `problem_id` |  | string | P11 |  |
| 2724 | `/problems/10/problem` | `problem` |  | string | 얼굴윤곽 |  |
| 2725 | `/problems/10/complaints` | `complaints` |  | array[7] | (배열 · 7개) |  |
| 2726 | `/problems/10/complaints/0` | `(complaints 원소)` | 0 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 2727 | `/problems/10/complaints/0/cc` | `cc` |  | string | 사각턱보톡스 |  |
| 2728 | `/problems/10/complaints/0/cc_detail` | `cc_detail` |  | string | 교근축소 |  |
| 2729 | `/problems/10/complaints/0/cc_group` | `cc_group` |  | string | 사각턱 |  |
| 2730 | `/problems/10/complaints/0/procedures` | `procedures` |  | array[4] | (배열 · 4개) |  |
| 2731 | `/problems/10/complaints/0/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) | OB-S11-01 |
| 2732 | `/problems/10/complaints/0/procedures/0/name` | `name` |  | string | 보톡스 |  |
| 2733 | `/problems/10/complaints/0/procedures/0/category` | `category` |  | string | M1 |  |
| 2734 | `/problems/10/complaints/0/procedures/0/role` | `role` |  | string | 근육 이완 |  |
| 2735 | `/problems/10/complaints/0/procedures/0/products` | `products` |  | array[3] | (배열 · 3개) |  |
| 2736 | `/problems/10/complaints/0/procedures/0/products/0` | `(products 원소)` | 0 | string | 보톡스 |  |
| 2737 | `/problems/10/complaints/0/procedures/0/products/1` | `(products 원소)` | 1 | string | 나보타 |  |
| 2738 | `/problems/10/complaints/0/procedures/0/products/2` | `(products 원소)` | 2 | string | 보툴렉스 |  |
| 2739 | `/problems/10/complaints/0/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2740 | `/problems/10/complaints/0/procedures/1/name` | `name` |  | string | 스킨부스터 |  |
| 2741 | `/problems/10/complaints/0/procedures/1/category` | `category` |  | string | M4 |  |
| 2742 | `/problems/10/complaints/0/procedures/1/role` | `role` |  | string | 피부 재생 |  |
| 2743 | `/problems/10/complaints/0/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 2744 | `/problems/10/complaints/0/procedures/1/products/0` | `(products 원소)` | 0 | string | 리쥬란 HB+ |  |
| 2745 | `/problems/10/complaints/0/procedures/1/products/1` | `(products 원소)` | 1 | string | 쥬베룩 |  |
| 2746 | `/problems/10/complaints/0/procedures/2` | `(procedures 원소)` | 2 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) | OB-S11-01 |
| 2747 | `/problems/10/complaints/0/procedures/2/name` | `name` |  | string | 보톡스 |  |
| 2748 | `/problems/10/complaints/0/procedures/2/category` | `category` |  | string | M1 |  |
| 2749 | `/problems/10/complaints/0/procedures/2/role` | `role` |  | string | 교근 축소 |  |
| 2750 | `/problems/10/complaints/0/procedures/2/products` | `products` |  | array[3] | (배열 · 3개) |  |
| 2751 | `/problems/10/complaints/0/procedures/2/products/0` | `(products 원소)` | 0 | string | 보톡스 |  |
| 2752 | `/problems/10/complaints/0/procedures/2/products/1` | `(products 원소)` | 1 | string | 나보타 |  |
| 2753 | `/problems/10/complaints/0/procedures/2/products/2` | `(products 원소)` | 2 | string | 보툴렉스 |  |
| 2754 | `/problems/10/complaints/0/procedures/3` | `(procedures 원소)` | 3 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2755 | `/problems/10/complaints/0/procedures/3/name` | `name` |  | string | 필러 |  |
| 2756 | `/problems/10/complaints/0/procedures/3/category` | `category` |  | string | M2 |  |
| 2757 | `/problems/10/complaints/0/procedures/3/role` | `role` |  | string | 턱끝 볼륨 |  |
| 2758 | `/problems/10/complaints/0/procedures/3/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 2759 | `/problems/10/complaints/0/procedures/3/products/0` | `(products 원소)` | 0 | string | 쥬비덤 |  |
| 2760 | `/problems/10/complaints/0/combos` | `combos` |  | array[2] | (배열 · 2개) |  |
| 2761 | `/problems/10/complaints/0/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 2762 | `/problems/10/complaints/0/combos/0/name` | `name` |  | string | 보톡스 + 스킨부스터 |  |
| 2763 | `/problems/10/complaints/0/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 2764 | `/problems/10/complaints/0/combos/0/combo/0` | `(combo 원소)` | 0 | string | 보톡스 |  |
| 2765 | `/problems/10/complaints/0/combos/0/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 2766 | `/problems/10/complaints/0/combos/0/reason` | `reason` |  | string | 근이완 + 피부재생 동시 개선 |  |
| 2767 | `/problems/10/complaints/0/combos/0/evidence` | `evidence` |  | string | 근이완(보톡스)과 진피재생(스킨부스터)은 목적이 다른 독립 시술로 병행 | OB-S11-02 |
| 2768 | `/problems/10/complaints/0/combos/1` | `(combos 원소)` | 1 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 2769 | `/problems/10/complaints/0/combos/1/name` | `name` |  | string | 보톡스 + 턱필러 |  |
| 2770 | `/problems/10/complaints/0/combos/1/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 2771 | `/problems/10/complaints/0/combos/1/combo/0` | `(combo 원소)` | 0 | string | 보톡스 |  |
| 2772 | `/problems/10/complaints/0/combos/1/combo/1` | `(combo 원소)` | 1 | string | 필러 |  |
| 2773 | `/problems/10/complaints/0/combos/1/reason` | `reason` |  | string | 교근축소 + 턱끝볼륨 = V라인 | OB-S11-03 |
| 2774 | `/problems/10/complaints/0/combos/1/evidence` | `evidence` |  | string | 위는 줄이고 아래는 늘려서 비율 교정 | OB-S11-03 |
| 2775 | `/problems/10/complaints/0/alternatives` | `alternatives` |  | array[2] | (배열 · 2개) |  |
| 2776 | `/problems/10/complaints/0/alternatives/0` | `(alternatives 원소)` | 0 | string | 효과 부족 시 리프팅기기 추가 |  |
| 2777 | `/problems/10/complaints/0/alternatives/1` | `(alternatives 원소)` | 1 | string | 수술적 방법은 별도 상담 | OB-S11-08 |
| 2778 | `/problems/10/complaints/1` | `(complaints 원소)` | 1 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 2779 | `/problems/10/complaints/1/cc` | `cc` |  | string | 윤곽주사 |  |
| 2780 | `/problems/10/complaints/1/cc_detail` | `cc_detail` |  | string | 지방분해 |  |
| 2781 | `/problems/10/complaints/1/cc_group` | `cc_group` |  | string | 이중턱/턱밑 |  |
| 2782 | `/problems/10/complaints/1/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 2783 | `/problems/10/complaints/1/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2784 | `/problems/10/complaints/1/procedures/0/name` | `name` |  | string | 지방분해 |  |
| 2785 | `/problems/10/complaints/1/procedures/0/category` | `category` |  | string | M14 |  |
| 2786 | `/problems/10/complaints/1/procedures/0/role` | `role` |  | string | 지방 감소 |  |
| 2787 | `/problems/10/complaints/1/procedures/0/products` | `products` |  | array[0] | `[]` (빈 배열) |  |
| 2788 | `/problems/10/complaints/1/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2789 | `/problems/10/complaints/1/procedures/1/name` | `name` |  | string | 리프팅기기 |  |
| 2790 | `/problems/10/complaints/1/procedures/1/category` | `category` |  | string | M9 |  |
| 2791 | `/problems/10/complaints/1/procedures/1/role` | `role` |  | string | 턱라인 타이트닝 |  |
| 2792 | `/problems/10/complaints/1/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 2793 | `/problems/10/complaints/1/procedures/1/products/0` | `(products 원소)` | 0 | string | 울쎄라 |  |
| 2794 | `/problems/10/complaints/1/procedures/1/products/1` | `(products 원소)` | 1 | string | 올리지오 |  |
| 2795 | `/problems/10/complaints/1/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 2796 | `/problems/10/complaints/1/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 2797 | `/problems/10/complaints/1/combos/0/name` | `name` |  | string | 지방분해 + 리프팅기기 |  |
| 2798 | `/problems/10/complaints/1/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 2799 | `/problems/10/complaints/1/combos/0/combo/0` | `(combo 원소)` | 0 | string | 지방분해 |  |
| 2800 | `/problems/10/complaints/1/combos/0/combo/1` | `(combo 원소)` | 1 | string | 리프팅기기 |  |
| 2801 | `/problems/10/complaints/1/combos/0/reason` | `reason` |  | string | 지방감소 + 타이트닝 |  |
| 2802 | `/problems/10/complaints/1/combos/0/evidence` | `evidence` |  | string | 이중턱 원인 해결 |  |
| 2803 | `/problems/10/complaints/1/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 2804 | `/problems/10/complaints/1/alternatives/0` | `(alternatives 원소)` | 0 | string | 수술적 방법은 별도 상담 | OB-S11-08 |
| 2805 | `/problems/10/complaints/2` | `(complaints 원소)` | 2 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 2806 | `/problems/10/complaints/2/cc` | `cc` |  | string | 브이올렛 | OB-S00-06 |
| 2807 | `/problems/10/complaints/2/cc_detail` | `cc_detail` |  | string | 턱밑지방 개선 허가(국내 식약처·데옥시콜산; FDA 승인 제품은 Kybella/벨카이라) | OB-S11-04, OB-S12-02 |
| 2808 | `/problems/10/complaints/2/cc_group` | `cc_group` |  | string | 이중턱/턱밑 |  |
| 2809 | `/problems/10/complaints/2/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 2810 | `/problems/10/complaints/2/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2811 | `/problems/10/complaints/2/procedures/0/name` | `name` |  | string | 지방분해 |  |
| 2812 | `/problems/10/complaints/2/procedures/0/category` | `category` |  | string | M14 |  |
| 2813 | `/problems/10/complaints/2/procedures/0/role` | `role` |  | string | 지방 감소 |  |
| 2814 | `/problems/10/complaints/2/procedures/0/products` | `products` |  | array[0] | `[]` (빈 배열) |  |
| 2815 | `/problems/10/complaints/2/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2816 | `/problems/10/complaints/2/procedures/1/name` | `name` |  | string | 리프팅기기 |  |
| 2817 | `/problems/10/complaints/2/procedures/1/category` | `category` |  | string | M9 |  |
| 2818 | `/problems/10/complaints/2/procedures/1/role` | `role` |  | string | 턱라인 타이트닝 |  |
| 2819 | `/problems/10/complaints/2/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 2820 | `/problems/10/complaints/2/procedures/1/products/0` | `(products 원소)` | 0 | string | 울쎄라 |  |
| 2821 | `/problems/10/complaints/2/procedures/1/products/1` | `(products 원소)` | 1 | string | 올리지오 |  |
| 2822 | `/problems/10/complaints/2/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 2823 | `/problems/10/complaints/2/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 2824 | `/problems/10/complaints/2/combos/0/name` | `name` |  | string | 지방분해 + 리프팅기기 |  |
| 2825 | `/problems/10/complaints/2/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 2826 | `/problems/10/complaints/2/combos/0/combo/0` | `(combo 원소)` | 0 | string | 지방분해 |  |
| 2827 | `/problems/10/complaints/2/combos/0/combo/1` | `(combo 원소)` | 1 | string | 리프팅기기 |  |
| 2828 | `/problems/10/complaints/2/combos/0/reason` | `reason` |  | string | 지방감소 + 타이트닝 |  |
| 2829 | `/problems/10/complaints/2/combos/0/evidence` | `evidence` |  | string | 이중턱 원인 해결 |  |
| 2830 | `/problems/10/complaints/2/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 2831 | `/problems/10/complaints/2/alternatives/0` | `(alternatives 원소)` | 0 | string | 수술적 방법은 별도 상담 |  |
| 2832 | `/problems/10/complaints/3` | `(complaints 원소)` | 3 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 2833 | `/problems/10/complaints/3/cc` | `cc` |  | string | 승모근보톡스 |  |
| 2834 | `/problems/10/complaints/3/cc_detail` | `cc_detail` |  | string | 어깨라인 |  |
| 2835 | `/problems/10/complaints/3/cc_group` | `cc_group` |  | string | 승모근 |  |
| 2836 | `/problems/10/complaints/3/procedures` | `procedures` |  | array[3] | (배열 · 3개) |  |
| 2837 | `/problems/10/complaints/3/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) | OB-S11-01 |
| 2838 | `/problems/10/complaints/3/procedures/0/name` | `name` |  | string | 보톡스 |  |
| 2839 | `/problems/10/complaints/3/procedures/0/category` | `category` |  | string | M1 |  |
| 2840 | `/problems/10/complaints/3/procedures/0/role` | `role` |  | string | 근육 이완 |  |
| 2841 | `/problems/10/complaints/3/procedures/0/products` | `products` |  | array[3] | (배열 · 3개) |  |
| 2842 | `/problems/10/complaints/3/procedures/0/products/0` | `(products 원소)` | 0 | string | 보톡스 |  |
| 2843 | `/problems/10/complaints/3/procedures/0/products/1` | `(products 원소)` | 1 | string | 나보타 |  |
| 2844 | `/problems/10/complaints/3/procedures/0/products/2` | `(products 원소)` | 2 | string | 보툴렉스 |  |
| 2845 | `/problems/10/complaints/3/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2846 | `/problems/10/complaints/3/procedures/1/name` | `name` |  | string | 스킨부스터 |  |
| 2847 | `/problems/10/complaints/3/procedures/1/category` | `category` |  | string | M4 |  |
| 2848 | `/problems/10/complaints/3/procedures/1/role` | `role` |  | string | 피부 재생 |  |
| 2849 | `/problems/10/complaints/3/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 2850 | `/problems/10/complaints/3/procedures/1/products/0` | `(products 원소)` | 0 | string | 리쥬란 HB+ |  |
| 2851 | `/problems/10/complaints/3/procedures/1/products/1` | `(products 원소)` | 1 | string | 쥬베룩 |  |
| 2852 | `/problems/10/complaints/3/procedures/2` | `(procedures 원소)` | 2 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) | OB-S11-01 |
| 2853 | `/problems/10/complaints/3/procedures/2/name` | `name` |  | string | 보톡스 |  |
| 2854 | `/problems/10/complaints/3/procedures/2/category` | `category` |  | string | M1 |  |
| 2855 | `/problems/10/complaints/3/procedures/2/role` | `role` |  | string | 승모근 축소 |  |
| 2856 | `/problems/10/complaints/3/procedures/2/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 2857 | `/problems/10/complaints/3/procedures/2/products/0` | `(products 원소)` | 0 | string | 보톡스 |  |
| 2858 | `/problems/10/complaints/3/procedures/2/products/1` | `(products 원소)` | 1 | string | 나보타 |  |
| 2859 | `/problems/10/complaints/3/combos` | `combos` |  | array[2] | (배열 · 2개) |  |
| 2860 | `/problems/10/complaints/3/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 2861 | `/problems/10/complaints/3/combos/0/name` | `name` |  | string | 보톡스 + 스킨부스터 |  |
| 2862 | `/problems/10/complaints/3/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 2863 | `/problems/10/complaints/3/combos/0/combo/0` | `(combo 원소)` | 0 | string | 보톡스 |  |
| 2864 | `/problems/10/complaints/3/combos/0/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 2865 | `/problems/10/complaints/3/combos/0/reason` | `reason` |  | string | 근이완 + 피부재생 동시 개선 |  |
| 2866 | `/problems/10/complaints/3/combos/0/evidence` | `evidence` |  | string | 근이완(보톡스)과 진피재생(스킨부스터)은 목적이 다른 독립 시술로 병행 |  |
| 2867 | `/problems/10/complaints/3/combos/1` | `(combos 원소)` | 1 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 2868 | `/problems/10/complaints/3/combos/1/name` | `name` |  | string | 승모근 보톡스 |  |
| 2869 | `/problems/10/complaints/3/combos/1/combo` | `combo` |  | array[1] | (배열 · 1개) |  |
| 2870 | `/problems/10/complaints/3/combos/1/combo/0` | `(combo 원소)` | 0 | string | 보톡스 |  |
| 2871 | `/problems/10/complaints/3/combos/1/reason` | `reason` |  | string | 승모근 이완으로 어깨라인 개선 |  |
| 2872 | `/problems/10/complaints/3/combos/1/evidence` | `evidence` |  | string | 3~6개월 유지 | OB-S11-07 |
| 2873 | `/problems/10/complaints/3/alternatives` | `alternatives` |  | array[2] | (배열 · 2개) |  |
| 2874 | `/problems/10/complaints/3/alternatives/0` | `(alternatives 원소)` | 0 | string | 효과 부족 시 리프팅기기 추가 |  |
| 2875 | `/problems/10/complaints/3/alternatives/1` | `(alternatives 원소)` | 1 | string | 수술적 방법은 별도 상담 |  |
| 2876 | `/problems/10/complaints/4` | `(complaints 원소)` | 4 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 2877 | `/problems/10/complaints/4/cc` | `cc` |  | string | 광대축소주사 |  |
| 2878 | `/problems/10/complaints/4/cc_detail` | `cc_detail` |  | string | 보톡스/윤곽주사 | OB-S11-05 |
| 2879 | `/problems/10/complaints/4/cc_group` | `cc_group` |  | string | 광대 |  |
| 2880 | `/problems/10/complaints/4/procedures` | `procedures` |  | array[1] | (배열 · 1개) |  |
| 2881 | `/problems/10/complaints/4/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) | OB-S11-05 |
| 2882 | `/problems/10/complaints/4/procedures/0/name` | `name` |  | string | 지방분해 |  |
| 2883 | `/problems/10/complaints/4/procedures/0/category` | `category` |  | string | M14 |  |
| 2884 | `/problems/10/complaints/4/procedures/0/role` | `role` |  | string | 광대 축소 |  |
| 2885 | `/problems/10/complaints/4/procedures/0/products` | `products` |  | array[0] | `[]` (빈 배열) |  |
| 2886 | `/problems/10/complaints/4/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 2887 | `/problems/10/complaints/4/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) | OB-S11-05 |
| 2888 | `/problems/10/complaints/4/combos/0/name` | `name` |  | string | 광대 축소 |  |
| 2889 | `/problems/10/complaints/4/combos/0/combo` | `combo` |  | array[1] | (배열 · 1개) |  |
| 2890 | `/problems/10/complaints/4/combos/0/combo/0` | `(combo 원소)` | 0 | string | 지방분해 |  |
| 2891 | `/problems/10/complaints/4/combos/0/reason` | `reason` |  | string | 광대 볼륨 감소 |  |
| 2892 | `/problems/10/complaints/4/combos/0/evidence` | `evidence` |  | string | 주사로 간편하게 | OB-S11-09 |
| 2893 | `/problems/10/complaints/4/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 2894 | `/problems/10/complaints/4/alternatives/0` | `(alternatives 원소)` | 0 | string | 수술적 방법은 별도 상담 |  |
| 2895 | `/problems/10/complaints/5` | `(complaints 원소)` | 5 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 2896 | `/problems/10/complaints/5/cc` | `cc` |  | string | 볼볼륨충전 |  |
| 2897 | `/problems/10/complaints/5/cc_detail` | `cc_detail` |  | string | 필러/지방이식/바이오스티뮬레이터 | OB-S11-06 |
| 2898 | `/problems/10/complaints/5/cc_group` | `cc_group` |  | string | 볼/관자놀이 |  |
| 2899 | `/problems/10/complaints/5/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 2900 | `/problems/10/complaints/5/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2901 | `/problems/10/complaints/5/procedures/0/name` | `name` |  | string | 필러 |  |
| 2902 | `/problems/10/complaints/5/procedures/0/category` | `category` |  | string | M2 |  |
| 2903 | `/problems/10/complaints/5/procedures/0/role` | `role` |  | string | 볼륨 충전 |  |
| 2904 | `/problems/10/complaints/5/procedures/0/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 2905 | `/problems/10/complaints/5/procedures/0/products/0` | `(products 원소)` | 0 | string | 쥬비덤 |  |
| 2906 | `/problems/10/complaints/5/procedures/0/products/1` | `(products 원소)` | 1 | string | 레스틸렌 |  |
| 2907 | `/problems/10/complaints/5/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2908 | `/problems/10/complaints/5/procedures/1/name` | `name` |  | string | 바이오스티뮬레이터/콜라겐부스터 |  |
| 2909 | `/problems/10/complaints/5/procedures/1/category` | `category` |  | string | M3 |  |
| 2910 | `/problems/10/complaints/5/procedures/1/role` | `role` |  | string | 장기 콜라겐 |  |
| 2911 | `/problems/10/complaints/5/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 2912 | `/problems/10/complaints/5/procedures/1/products/0` | `(products 원소)` | 0 | string | 스컬트라 |  |
| 2913 | `/problems/10/complaints/5/procedures/1/products/1` | `(products 원소)` | 1 | string | 엘란쎄 |  |
| 2914 | `/problems/10/complaints/5/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 2915 | `/problems/10/complaints/5/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 2916 | `/problems/10/complaints/5/combos/0/name` | `name` |  | string | 필러 + 바이오스티뮬레이터 |  |
| 2917 | `/problems/10/complaints/5/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 2918 | `/problems/10/complaints/5/combos/0/combo/0` | `(combo 원소)` | 0 | string | 필러 |  |
| 2919 | `/problems/10/complaints/5/combos/0/combo/1` | `(combo 원소)` | 1 | string | 바이오스티뮬레이터 | OB-S00-05 |
| 2920 | `/problems/10/complaints/5/combos/0/reason` | `reason` |  | string | 즉각 볼륨 + 장기 재생 |  |
| 2921 | `/problems/10/complaints/5/combos/0/evidence` | `evidence` |  | string | 스컬트라가 자연스러운 볼륨 | OB-S11-09 |
| 2922 | `/problems/10/complaints/5/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 2923 | `/problems/10/complaints/5/alternatives/0` | `(alternatives 원소)` | 0 | string | 수술적 방법은 별도 상담 |  |
| 2924 | `/problems/10/complaints/6` | `(complaints 원소)` | 6 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 2925 | `/problems/10/complaints/6/cc` | `cc` |  | string | 관자놀이충전 |  |
| 2926 | `/problems/10/complaints/6/cc_detail` | `cc_detail` |  | string | 필러/지방이식 | OB-S11-06 |
| 2927 | `/problems/10/complaints/6/cc_group` | `cc_group` |  | string | 볼/관자놀이 |  |
| 2928 | `/problems/10/complaints/6/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 2929 | `/problems/10/complaints/6/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2930 | `/problems/10/complaints/6/procedures/0/name` | `name` |  | string | 필러 |  |
| 2931 | `/problems/10/complaints/6/procedures/0/category` | `category` |  | string | M2 |  |
| 2932 | `/problems/10/complaints/6/procedures/0/role` | `role` |  | string | 볼륨 충전 |  |
| 2933 | `/problems/10/complaints/6/procedures/0/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 2934 | `/problems/10/complaints/6/procedures/0/products/0` | `(products 원소)` | 0 | string | 쥬비덤 |  |
| 2935 | `/problems/10/complaints/6/procedures/0/products/1` | `(products 원소)` | 1 | string | 레스틸렌 |  |
| 2936 | `/problems/10/complaints/6/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2937 | `/problems/10/complaints/6/procedures/1/name` | `name` |  | string | 바이오스티뮬레이터/콜라겐부스터 |  |
| 2938 | `/problems/10/complaints/6/procedures/1/category` | `category` |  | string | M3 |  |
| 2939 | `/problems/10/complaints/6/procedures/1/role` | `role` |  | string | 장기 콜라겐 |  |
| 2940 | `/problems/10/complaints/6/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 2941 | `/problems/10/complaints/6/procedures/1/products/0` | `(products 원소)` | 0 | string | 스컬트라 |  |
| 2942 | `/problems/10/complaints/6/procedures/1/products/1` | `(products 원소)` | 1 | string | 엘란쎄 |  |
| 2943 | `/problems/10/complaints/6/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 2944 | `/problems/10/complaints/6/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 2945 | `/problems/10/complaints/6/combos/0/name` | `name` |  | string | 필러 + 바이오스티뮬레이터 |  |
| 2946 | `/problems/10/complaints/6/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 2947 | `/problems/10/complaints/6/combos/0/combo/0` | `(combo 원소)` | 0 | string | 필러 |  |
| 2948 | `/problems/10/complaints/6/combos/0/combo/1` | `(combo 원소)` | 1 | string | 바이오스티뮬레이터 | OB-S00-05 |
| 2949 | `/problems/10/complaints/6/combos/0/reason` | `reason` |  | string | 즉각 볼륨 + 장기 재생 |  |
| 2950 | `/problems/10/complaints/6/combos/0/evidence` | `evidence` |  | string | 스컬트라가 자연스러운 볼륨 |  |
| 2951 | `/problems/10/complaints/6/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 2952 | `/problems/10/complaints/6/alternatives/0` | `(alternatives 원소)` | 0 | string | 수술적 방법은 별도 상담 |  |

## 잠정 관찰 (원문 칸과 분리)

| ID | 상태 | 위치 | 관찰 |
|---|---|---|---|
| OB-S11-01 | I | `/problems/10/complaints/0/procedures/0`<br>`/problems/10/complaints/0/procedures/2`<br>`/problems/10/complaints/3/procedures/0`<br>`/problems/10/complaints/3/procedures/2` | c0·c3 에서 name '보톡스'(M1) 가 role 을 달리해 두 번 나온다(c0: '근육 이완' / '교근 축소', c3: '근육 이완' / '승모근 축소'). I-07 같은 유형. |
| OB-S11-02 | P | `/problems/10/complaints/0/combos/0/evidence`<br>`/problems/0/complaints/5/combos/0/evidence` | 같은 combo '보톡스 + 스킨부스터'(reason 동일 '근이완 + 피부재생 동시 개선')의 evidence 가 여기서는 '근이완(보톡스)과 진피재생(스킨부스터)은 목적이 다른 독립 시술로 병행', S01 에서는 '... 상호 보완 (... 직접 임상근거는 없음)' 이다. problem 마다 문장이 다르다. |
| OB-S11-03 | P | `/problems/10/complaints/0/combos/1/reason`<br>`/problems/10/complaints/0/combos/1/evidence` | '교근축소 + 턱끝볼륨 = V라인', '위는 줄이고 아래는 늘려서 비율 교정' — 위/아래 대조와 감소/증가 동사. '위'·'아래' 가 각각 어느 부위인지 문장 안에서는 reason 의 교근·턱끝으로만 짐작된다(확정하지 않음). |
| OB-S11-04 | P | `/problems/10/complaints/2/cc_detail` | c2 cc_detail '턱밑지방 개선 허가(국내 식약처·데옥시콜산; FDA 승인 제품은 Kybella/벨카이라)' — 허가 진술·성분·기관·해외 제품명이 괄호와 세미콜론으로 한 값에 들어 있다. 법적·허가 사실로 승인하지 않고 원문으로만 보존. 'Kybella/벨카이라' 는 '/' 로 두 표기 병기(F-02). |
| OB-S11-05 | I | `/problems/10/complaints/4/cc_detail`<br>`/problems/10/complaints/4/procedures/0`<br>`/problems/10/complaints/4/combos/0` | c4 cc '광대축소주사' 의 cc_detail '보톡스/윤곽주사' 중 보톡스는 procedures 에 없고 procedures 는 '지방분해'(role '광대 축소') 하나다(I-03 같은 유형). combo name '광대 축소' 는 원소('지방분해')와 다른 표기(I-02 같은 유형). |
| OB-S11-06 | I | `/problems/10/complaints/5/cc_detail`<br>`/problems/10/complaints/6/cc_detail` | cc_detail '필러/지방이식/바이오스티뮬레이터', '필러/지방이식' 중 '지방이식' 이 procedures 에 없다(I-03 같은 유형). |
| OB-S11-07 | P | `/problems/10/complaints/3/combos/1/evidence` | evidence '3~6개월 유지' — 지속 기간 범위. combo '승모근 보톡스'(원소 1개) 의 evidence 칸이 근거가 아니라 지속기간이다(F-06). |
| OB-S11-08 | P | `/problems/10/complaints/0/alternatives/1`<br>`/problems/10/complaints/1/alternatives/0` | alternatives '수술적 방법은 별도 상담' — 다른 범주(수술)를 상담으로 넘기는 안내. 7개 complaint 모두에 있다. |
| OB-S11-09 | P | `/problems/10/complaints/4/combos/0/evidence`<br>`/problems/10/complaints/5/combos/0/evidence` | '주사로 간편하게', '스컬트라가 자연스러운 볼륨' — 편의·자연스러움 진술. 근거 출처 없음. |

## 수동 복합 표현 (직접 읽기 · 출현별)

| 표현 | 위치(Pointer · 값 내 구간) | 관점(탐색용, 확정 분류 아님) |
|---|---|---|
| 사각턱보톡스 | `/problems/10/complaints/0/cc` [0,6) | 부위+시술명 표현, 붙여 쓴 복합어 |
| 교근축소 | `/problems/10/complaints/0/cc_detail` [0,4) | 부위(근육)+감소, 붙여 쓴 복합어 |
| 지방분해 | `/problems/10/complaints/1/cc_detail` [0,4) | 기전 표현 |
| 턱밑지방 개선 허가(국내 식약처·데옥시콜산; FDA 승인 제품은 Kybella/벨카이라) | `/problems/10/complaints/2/cc_detail` [0,49) | 허가 상태 진술, 괄호 보충, 기호(;), 기호(·), 기호(/), 범위(국내), 기관 표현, 성분 표현, 제품명 표현 |
| FDA 승인 제품은 Kybella/벨카이라 | `/problems/10/complaints/2/cc_detail` [25,48) | 허가 상태 진술, 기관 약어(FDA), 제품명 표현, 기호(/), 혼합 표기 |
| 국내 식약처·데옥시콜산 | `/problems/10/complaints/2/cc_detail` [11,23) | 범위(국내), 기관 표현, 성분 표현, 기호(·) |
| 어깨라인 | `/problems/10/complaints/3/cc_detail` [0,4) | 부위 표현, 붙여 쓴 복합어 |
| 보톡스/윤곽주사 | `/problems/10/complaints/4/cc_detail` [0,8) | 시술명 표현, 기호(/) |
| 필러/지방이식/바이오스티뮬레이터 | `/problems/10/complaints/5/cc_detail` [0,17) | 시술명 표현, 기호(/) |
| 필러/지방이식 | `/problems/10/complaints/6/cc_detail` [0,7) | 시술명 표현, 기호(/) |
| 이중턱/턱밑 | `/problems/10/complaints/1/cc_group` [0,6)<br>`/problems/10/complaints/2/cc_group` [0,6) | 부위·증상 표현, 기호(/) |
| 볼/관자놀이 | `/problems/10/complaints/5/cc_group` [0,6)<br>`/problems/10/complaints/6/cc_group` [0,6) | 부위 표현, 기호(/) |
| 근이완 + 피부재생 동시 개선 | `/problems/10/complaints/0/combos/0/reason` [0,16)<br>`/problems/10/complaints/3/combos/0/reason` [0,16) | 기호(+), 동시성(동시) |
| 근이완(보톡스)과 진피재생(스킨부스터)은 목적이 다른 독립 시술로 병행 | `/problems/10/complaints/0/combos/0/evidence` [0,39)<br>`/problems/10/complaints/3/combos/0/evidence` [0,39) | 괄호 라벨, 대조(목적이 다른), 독립·병행, 층위(진피) |
| 교근축소 + 턱끝볼륨 = V라인 | `/problems/10/complaints/0/combos/1/reason` [0,17) | 공식형 문장, 기호(+), 기호(=), 혼합 표기 |
| 위는 줄이고 아래는 늘려서 비율 교정 | `/problems/10/complaints/0/combos/1/evidence` [0,20) | 위치 대조(위/아래), 감소·증가 동사, 목적 표현 |
| 보톡스 + 턱필러 | `/problems/10/complaints/0/combos/1/name` [0,9) | combo name(원소와 다른 표기), 기호(+) |
| 턱라인 타이트닝 | `/problems/10/complaints/1/procedures/1/role` [0,8)<br>`/problems/10/complaints/2/procedures/1/role` [0,8) | role 표현, 부위 표현 |
| 지방감소 + 타이트닝 | `/problems/10/complaints/1/combos/0/reason` [0,11)<br>`/problems/10/complaints/2/combos/0/reason` [0,11) | 기호(+), 감소 표현 |
| 이중턱 원인 해결 | `/problems/10/complaints/1/combos/0/evidence` [0,9)<br>`/problems/10/complaints/2/combos/0/evidence` [0,9) | 원인 표현, 효과 강도(해결) |
| 승모근 이완으로 어깨라인 개선 | `/problems/10/complaints/3/combos/1/reason` [0,16) | 수단(-으로)+결과, 부위 표현 |
| 3~6개월 유지 | `/problems/10/complaints/3/combos/1/evidence` [0,8) | 범위(~), 수량·단위·시간, 지속 기간 |
| 광대 볼륨 감소 | `/problems/10/complaints/4/combos/0/reason` [0,8) | 부위 표현, 감소 표현 |
| 주사로 간편하게 | `/problems/10/complaints/4/combos/0/evidence` [0,8) | 수단(-로), 편의 표현 |
| 즉각 볼륨 + 장기 재생 | `/problems/10/complaints/5/combos/0/reason` [0,13)<br>`/problems/10/complaints/6/combos/0/reason` [0,13) | 기호(+), 시간 대비(즉각/장기) |
| 스컬트라가 자연스러운 볼륨 | `/problems/10/complaints/5/combos/0/evidence` [0,14)<br>`/problems/10/complaints/6/combos/0/evidence` [0,14) | 제품명 표현, 수식(자연스러운) |
| 효과 부족 시 리프팅기기 추가 | `/problems/10/complaints/0/alternatives/0` [0,16)<br>`/problems/10/complaints/3/alternatives/0` [0,16) | 조건(-시), 부족 표현, 추가 표현 |
| 수술적 방법은 별도 상담 | `/problems/10/complaints/0/alternatives/1` [0,13)<br>`/problems/10/complaints/1/alternatives/0` [0,13)<br>`/problems/10/complaints/2/alternatives/0` [0,13)<br>`/problems/10/complaints/3/alternatives/1` [0,13)<br>`/problems/10/complaints/4/alternatives/0` [0,13)<br>`/problems/10/complaints/5/alternatives/0` [0,13)<br>`/problems/10/complaints/6/alternatives/0` [0,13) | 다른 범주 안내, 상담 지시 |
| 교근 축소 | `/problems/10/complaints/0/procedures/2/role` [0,5) | role 표현, 부위(근육), 감소 표현 |
| 승모근 축소 | `/problems/10/complaints/3/procedures/2/role` [0,6) | role 표현, 부위(근육), 감소 표현 |
| 광대 축소 | `/problems/10/complaints/4/procedures/0/role` [0,5)<br>`/problems/10/complaints/4/combos/0/name` [0,5) | 부위 표현, 감소 표현 |
| 턱끝 볼륨 | `/problems/10/complaints/0/procedures/3/role` [0,5) | role 표현, 부위 표현 |
| 장기 콜라겐 | `/problems/10/complaints/5/procedures/1/role` [0,6)<br>`/problems/10/complaints/6/procedures/1/role` [0,6) | role 표현, 기간 표현(장기), 축약 표현 |

## 이 구획에서 연 미결

- 새로 연 미결 없음(관찰은 기존 미결 유형에 연결).
