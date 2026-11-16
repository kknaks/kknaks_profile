# S12 — /problems/11 P12 바디

[← review.md](review.md) · 범위 /problems/11 및 /problems/11/** 전체 · 소유 노드 271 · 말단 165 · 빈 값 9 · 직접 읽기 done

상위 문맥(공유, S00 소유): 루트 객체 → `/description` = taxonomy P1~P14 하위구조 기반 CC 자동 생성 → `/problems` 배열.

직접 읽기: reading/S12.txt 로 c0~c10 전부(procedures 18·combos 11·alternatives 11) 읽음. c4 의 긴 cc_detail 은 세미콜론·마침표 단위로 다시 읽음.

## 원문 값 (문서 순서 · 전부)

| # | JSON Pointer | 원본 컬럼명 | 배열 순번 | 자료형 | 원문 값 | 관찰 참조 |
|---|---|---|---|---|---|---|
| 2953 | `/problems/11` | `(problems 원소)` | 11 | object{3} | (객체 · 키: `problem_id`, `problem`, `complaints`) |  |
| 2954 | `/problems/11/problem_id` | `problem_id` |  | string | P12 |  |
| 2955 | `/problems/11/problem` | `problem` |  | string | 바디 |  |
| 2956 | `/problems/11/complaints` | `complaints` |  | array[11] | (배열 · 11개) |  |
| 2957 | `/problems/11/complaints/0` | `(complaints 원소)` | 0 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 2958 | `/problems/11/complaints/0/cc` | `cc` |  | string | 쿨스컬프팅 |  |
| 2959 | `/problems/11/complaints/0/cc_detail` | `cc_detail` |  | string | 냉각지방분해 |  |
| 2960 | `/problems/11/complaints/0/cc_group` | `cc_group` |  | string | 지방감소 |  |
| 2961 | `/problems/11/complaints/0/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 2962 | `/problems/11/complaints/0/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) | OB-S12-01 |
| 2963 | `/problems/11/complaints/0/procedures/0/name` | `name` |  | string | 크라이오 |  |
| 2964 | `/problems/11/complaints/0/procedures/0/category` | `category` |  | string | M14 |  |
| 2965 | `/problems/11/complaints/0/procedures/0/role` | `role` |  | string | 지방 동결 파괴 |  |
| 2966 | `/problems/11/complaints/0/procedures/0/products` | `products` |  | array[0] | `[]` (빈 배열) |  |
| 2967 | `/problems/11/complaints/0/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2968 | `/problems/11/complaints/0/procedures/1/name` | `name` |  | string | 인모드 | OB-S12-05 |
| 2969 | `/problems/11/complaints/0/procedures/1/category` | `category` |  | string | M9 |  |
| 2970 | `/problems/11/complaints/0/procedures/1/role` | `role` |  | string | RF 타이트닝 |  |
| 2971 | `/problems/11/complaints/0/procedures/1/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 2972 | `/problems/11/complaints/0/procedures/1/products/0` | `(products 원소)` | 0 | string | 인모드 | OB-S12-05 |
| 2973 | `/problems/11/complaints/0/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 2974 | `/problems/11/complaints/0/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 2975 | `/problems/11/complaints/0/combos/0/name` | `name` |  | string | 크라이오 + 인모드 |  |
| 2976 | `/problems/11/complaints/0/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 2977 | `/problems/11/complaints/0/combos/0/combo/0` | `(combo 원소)` | 0 | string | 크라이오 |  |
| 2978 | `/problems/11/complaints/0/combos/0/combo/1` | `(combo 원소)` | 1 | string | 인모드 |  |
| 2979 | `/problems/11/complaints/0/combos/0/reason` | `reason` |  | string | 지방파괴 + 피부타이트닝 |  |
| 2980 | `/problems/11/complaints/0/combos/0/evidence` | `evidence` |  | string | 지방 빼고 피부 조임 |  |
| 2981 | `/problems/11/complaints/0/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 2982 | `/problems/11/complaints/0/alternatives/0` | `(alternatives 원소)` | 0 | string | 운동·식단 병행 필수 | OB-S12-07 |
| 2983 | `/problems/11/complaints/1` | `(complaints 원소)` | 1 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 2984 | `/problems/11/complaints/1/cc` | `cc` |  | string | 지방분해주사(PPC/DC) | OB-S12-08 |
| 2985 | `/problems/11/complaints/1/cc_detail` | `cc_detail` |  | string | 포스파티딜콜린/데옥시콜산 |  |
| 2986 | `/problems/11/complaints/1/cc_group` | `cc_group` |  | string | 지방감소 |  |
| 2987 | `/problems/11/complaints/1/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 2988 | `/problems/11/complaints/1/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) | OB-S12-01 |
| 2989 | `/problems/11/complaints/1/procedures/0/name` | `name` |  | string | 크라이오 |  |
| 2990 | `/problems/11/complaints/1/procedures/0/category` | `category` |  | string | M14 |  |
| 2991 | `/problems/11/complaints/1/procedures/0/role` | `role` |  | string | 지방 동결 파괴 |  |
| 2992 | `/problems/11/complaints/1/procedures/0/products` | `products` |  | array[0] | `[]` (빈 배열) |  |
| 2993 | `/problems/11/complaints/1/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 2994 | `/problems/11/complaints/1/procedures/1/name` | `name` |  | string | 인모드 |  |
| 2995 | `/problems/11/complaints/1/procedures/1/category` | `category` |  | string | M9 |  |
| 2996 | `/problems/11/complaints/1/procedures/1/role` | `role` |  | string | RF 타이트닝 |  |
| 2997 | `/problems/11/complaints/1/procedures/1/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 2998 | `/problems/11/complaints/1/procedures/1/products/0` | `(products 원소)` | 0 | string | 인모드 |  |
| 2999 | `/problems/11/complaints/1/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 3000 | `/problems/11/complaints/1/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 3001 | `/problems/11/complaints/1/combos/0/name` | `name` |  | string | 크라이오 + 인모드 |  |
| 3002 | `/problems/11/complaints/1/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 3003 | `/problems/11/complaints/1/combos/0/combo/0` | `(combo 원소)` | 0 | string | 크라이오 |  |
| 3004 | `/problems/11/complaints/1/combos/0/combo/1` | `(combo 원소)` | 1 | string | 인모드 |  |
| 3005 | `/problems/11/complaints/1/combos/0/reason` | `reason` |  | string | 지방파괴 + 피부타이트닝 |  |
| 3006 | `/problems/11/complaints/1/combos/0/evidence` | `evidence` |  | string | 지방 빼고 피부 조임 |  |
| 3007 | `/problems/11/complaints/1/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 3008 | `/problems/11/complaints/1/alternatives/0` | `(alternatives 원소)` | 0 | string | 운동·식단 병행 필수 |  |
| 3009 | `/problems/11/complaints/2` | `(complaints 원소)` | 2 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 3010 | `/problems/11/complaints/2/cc` | `cc` |  | string | HPL주사 |  |
| 3011 | `/problems/11/complaints/2/cc_detail` | `cc_detail` |  | string | 고농도 지방분해 |  |
| 3012 | `/problems/11/complaints/2/cc_group` | `cc_group` |  | string | 지방감소 |  |
| 3013 | `/problems/11/complaints/2/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 3014 | `/problems/11/complaints/2/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) | OB-S12-01 |
| 3015 | `/problems/11/complaints/2/procedures/0/name` | `name` |  | string | 크라이오 |  |
| 3016 | `/problems/11/complaints/2/procedures/0/category` | `category` |  | string | M14 |  |
| 3017 | `/problems/11/complaints/2/procedures/0/role` | `role` |  | string | 지방 동결 파괴 |  |
| 3018 | `/problems/11/complaints/2/procedures/0/products` | `products` |  | array[0] | `[]` (빈 배열) |  |
| 3019 | `/problems/11/complaints/2/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 3020 | `/problems/11/complaints/2/procedures/1/name` | `name` |  | string | 인모드 |  |
| 3021 | `/problems/11/complaints/2/procedures/1/category` | `category` |  | string | M9 |  |
| 3022 | `/problems/11/complaints/2/procedures/1/role` | `role` |  | string | RF 타이트닝 |  |
| 3023 | `/problems/11/complaints/2/procedures/1/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 3024 | `/problems/11/complaints/2/procedures/1/products/0` | `(products 원소)` | 0 | string | 인모드 |  |
| 3025 | `/problems/11/complaints/2/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 3026 | `/problems/11/complaints/2/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 3027 | `/problems/11/complaints/2/combos/0/name` | `name` |  | string | 크라이오 + 인모드 |  |
| 3028 | `/problems/11/complaints/2/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 3029 | `/problems/11/complaints/2/combos/0/combo/0` | `(combo 원소)` | 0 | string | 크라이오 |  |
| 3030 | `/problems/11/complaints/2/combos/0/combo/1` | `(combo 원소)` | 1 | string | 인모드 |  |
| 3031 | `/problems/11/complaints/2/combos/0/reason` | `reason` |  | string | 지방파괴 + 피부타이트닝 |  |
| 3032 | `/problems/11/complaints/2/combos/0/evidence` | `evidence` |  | string | 지방 빼고 피부 조임 |  |
| 3033 | `/problems/11/complaints/2/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 3034 | `/problems/11/complaints/2/alternatives/0` | `(alternatives 원소)` | 0 | string | 운동·식단 병행 필수 |  |
| 3035 | `/problems/11/complaints/3` | `(complaints 원소)` | 3 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 3036 | `/problems/11/complaints/3/cc` | `cc` |  | string | BNLS주사 |  |
| 3037 | `/problems/11/complaints/3/cc_detail` | `cc_detail` |  | string | 식물추출 지방분해 |  |
| 3038 | `/problems/11/complaints/3/cc_group` | `cc_group` |  | string | 지방감소 |  |
| 3039 | `/problems/11/complaints/3/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 3040 | `/problems/11/complaints/3/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) | OB-S12-01 |
| 3041 | `/problems/11/complaints/3/procedures/0/name` | `name` |  | string | 크라이오 |  |
| 3042 | `/problems/11/complaints/3/procedures/0/category` | `category` |  | string | M14 |  |
| 3043 | `/problems/11/complaints/3/procedures/0/role` | `role` |  | string | 지방 동결 파괴 |  |
| 3044 | `/problems/11/complaints/3/procedures/0/products` | `products` |  | array[0] | `[]` (빈 배열) |  |
| 3045 | `/problems/11/complaints/3/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 3046 | `/problems/11/complaints/3/procedures/1/name` | `name` |  | string | 인모드 |  |
| 3047 | `/problems/11/complaints/3/procedures/1/category` | `category` |  | string | M9 |  |
| 3048 | `/problems/11/complaints/3/procedures/1/role` | `role` |  | string | RF 타이트닝 |  |
| 3049 | `/problems/11/complaints/3/procedures/1/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 3050 | `/problems/11/complaints/3/procedures/1/products/0` | `(products 원소)` | 0 | string | 인모드 |  |
| 3051 | `/problems/11/complaints/3/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 3052 | `/problems/11/complaints/3/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 3053 | `/problems/11/complaints/3/combos/0/name` | `name` |  | string | 크라이오 + 인모드 |  |
| 3054 | `/problems/11/complaints/3/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 3055 | `/problems/11/complaints/3/combos/0/combo/0` | `(combo 원소)` | 0 | string | 크라이오 |  |
| 3056 | `/problems/11/complaints/3/combos/0/combo/1` | `(combo 원소)` | 1 | string | 인모드 |  |
| 3057 | `/problems/11/complaints/3/combos/0/reason` | `reason` |  | string | 지방파괴 + 피부타이트닝 |  |
| 3058 | `/problems/11/complaints/3/combos/0/evidence` | `evidence` |  | string | 지방 빼고 피부 조임 |  |
| 3059 | `/problems/11/complaints/3/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 3060 | `/problems/11/complaints/3/alternatives/0` | `(alternatives 원소)` | 0 | string | 운동·식단 병행 필수 |  |
| 3061 | `/problems/11/complaints/4` | `(complaints 원소)` | 4 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 3062 | `/problems/11/complaints/4/cc` | `cc` |  | string | 브이올렛 | OB-S00-06 |
| 3063 | `/problems/11/complaints/4/cc_detail` | `cc_detail` |  | string | 턱밑 지방 전용 국내 허가(데옥시콜산); 바디·체간 지방 사용은 허가 외. FDA 승인 제품은 미국 Kybella이며 동일 성분 Belkyra는 국가별 허가를 구분 | OB-S12-02, OB-S12-03 |
| 3064 | `/problems/11/complaints/4/cc_group` | `cc_group` |  | string | 지방감소 | OB-S12-03 |
| 3065 | `/problems/11/complaints/4/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 3066 | `/problems/11/complaints/4/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) | OB-S12-01 |
| 3067 | `/problems/11/complaints/4/procedures/0/name` | `name` |  | string | 크라이오 |  |
| 3068 | `/problems/11/complaints/4/procedures/0/category` | `category` |  | string | M14 |  |
| 3069 | `/problems/11/complaints/4/procedures/0/role` | `role` |  | string | 지방 동결 파괴 |  |
| 3070 | `/problems/11/complaints/4/procedures/0/products` | `products` |  | array[0] | `[]` (빈 배열) |  |
| 3071 | `/problems/11/complaints/4/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 3072 | `/problems/11/complaints/4/procedures/1/name` | `name` |  | string | 인모드 |  |
| 3073 | `/problems/11/complaints/4/procedures/1/category` | `category` |  | string | M9 |  |
| 3074 | `/problems/11/complaints/4/procedures/1/role` | `role` |  | string | RF 타이트닝 |  |
| 3075 | `/problems/11/complaints/4/procedures/1/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 3076 | `/problems/11/complaints/4/procedures/1/products/0` | `(products 원소)` | 0 | string | 인모드 |  |
| 3077 | `/problems/11/complaints/4/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 3078 | `/problems/11/complaints/4/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 3079 | `/problems/11/complaints/4/combos/0/name` | `name` |  | string | 크라이오 + 인모드 |  |
| 3080 | `/problems/11/complaints/4/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 3081 | `/problems/11/complaints/4/combos/0/combo/0` | `(combo 원소)` | 0 | string | 크라이오 |  |
| 3082 | `/problems/11/complaints/4/combos/0/combo/1` | `(combo 원소)` | 1 | string | 인모드 |  |
| 3083 | `/problems/11/complaints/4/combos/0/reason` | `reason` |  | string | 지방파괴 + 피부타이트닝 |  |
| 3084 | `/problems/11/complaints/4/combos/0/evidence` | `evidence` |  | string | 지방 빼고 피부 조임 |  |
| 3085 | `/problems/11/complaints/4/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 3086 | `/problems/11/complaints/4/alternatives/0` | `(alternatives 원소)` | 0 | string | 운동·식단 병행 필수 |  |
| 3087 | `/problems/11/complaints/5` | `(complaints 원소)` | 5 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 3088 | `/problems/11/complaints/5/cc` | `cc` |  | string | 컷슬린 |  |
| 3089 | `/problems/11/complaints/5/cc_detail` | `cc_detail` |  | string | 지방분해 주사 |  |
| 3090 | `/problems/11/complaints/5/cc_group` | `cc_group` |  | string | 지방감소 |  |
| 3091 | `/problems/11/complaints/5/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 3092 | `/problems/11/complaints/5/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) | OB-S12-01 |
| 3093 | `/problems/11/complaints/5/procedures/0/name` | `name` |  | string | 크라이오 |  |
| 3094 | `/problems/11/complaints/5/procedures/0/category` | `category` |  | string | M14 |  |
| 3095 | `/problems/11/complaints/5/procedures/0/role` | `role` |  | string | 지방 동결 파괴 |  |
| 3096 | `/problems/11/complaints/5/procedures/0/products` | `products` |  | array[0] | `[]` (빈 배열) |  |
| 3097 | `/problems/11/complaints/5/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 3098 | `/problems/11/complaints/5/procedures/1/name` | `name` |  | string | 인모드 |  |
| 3099 | `/problems/11/complaints/5/procedures/1/category` | `category` |  | string | M9 |  |
| 3100 | `/problems/11/complaints/5/procedures/1/role` | `role` |  | string | RF 타이트닝 |  |
| 3101 | `/problems/11/complaints/5/procedures/1/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 3102 | `/problems/11/complaints/5/procedures/1/products/0` | `(products 원소)` | 0 | string | 인모드 |  |
| 3103 | `/problems/11/complaints/5/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 3104 | `/problems/11/complaints/5/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 3105 | `/problems/11/complaints/5/combos/0/name` | `name` |  | string | 크라이오 + 인모드 |  |
| 3106 | `/problems/11/complaints/5/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 3107 | `/problems/11/complaints/5/combos/0/combo/0` | `(combo 원소)` | 0 | string | 크라이오 |  |
| 3108 | `/problems/11/complaints/5/combos/0/combo/1` | `(combo 원소)` | 1 | string | 인모드 |  |
| 3109 | `/problems/11/complaints/5/combos/0/reason` | `reason` |  | string | 지방파괴 + 피부타이트닝 |  |
| 3110 | `/problems/11/complaints/5/combos/0/evidence` | `evidence` |  | string | 지방 빼고 피부 조임 |  |
| 3111 | `/problems/11/complaints/5/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 3112 | `/problems/11/complaints/5/alternatives/0` | `(alternatives 원소)` | 0 | string | 운동·식단 병행 필수 |  |
| 3113 | `/problems/11/complaints/6` | `(complaints 원소)` | 6 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 3114 | `/problems/11/complaints/6/cc` | `cc` |  | string | 바디HIFU |  |
| 3115 | `/problems/11/complaints/6/cc_detail` | `cc_detail` |  | string | 리포소닉스 등 |  |
| 3116 | `/problems/11/complaints/6/cc_group` | `cc_group` |  | string | 지방감소 |  |
| 3117 | `/problems/11/complaints/6/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 3118 | `/problems/11/complaints/6/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) | OB-S12-01 |
| 3119 | `/problems/11/complaints/6/procedures/0/name` | `name` |  | string | 크라이오 |  |
| 3120 | `/problems/11/complaints/6/procedures/0/category` | `category` |  | string | M14 |  |
| 3121 | `/problems/11/complaints/6/procedures/0/role` | `role` |  | string | 지방 동결 파괴 |  |
| 3122 | `/problems/11/complaints/6/procedures/0/products` | `products` |  | array[0] | `[]` (빈 배열) |  |
| 3123 | `/problems/11/complaints/6/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 3124 | `/problems/11/complaints/6/procedures/1/name` | `name` |  | string | 인모드 |  |
| 3125 | `/problems/11/complaints/6/procedures/1/category` | `category` |  | string | M9 |  |
| 3126 | `/problems/11/complaints/6/procedures/1/role` | `role` |  | string | RF 타이트닝 |  |
| 3127 | `/problems/11/complaints/6/procedures/1/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 3128 | `/problems/11/complaints/6/procedures/1/products/0` | `(products 원소)` | 0 | string | 인모드 |  |
| 3129 | `/problems/11/complaints/6/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 3130 | `/problems/11/complaints/6/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 3131 | `/problems/11/complaints/6/combos/0/name` | `name` |  | string | 크라이오 + 인모드 |  |
| 3132 | `/problems/11/complaints/6/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 3133 | `/problems/11/complaints/6/combos/0/combo/0` | `(combo 원소)` | 0 | string | 크라이오 |  |
| 3134 | `/problems/11/complaints/6/combos/0/combo/1` | `(combo 원소)` | 1 | string | 인모드 |  |
| 3135 | `/problems/11/complaints/6/combos/0/reason` | `reason` |  | string | 지방파괴 + 피부타이트닝 |  |
| 3136 | `/problems/11/complaints/6/combos/0/evidence` | `evidence` |  | string | 지방 빼고 피부 조임 |  |
| 3137 | `/problems/11/complaints/6/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 3138 | `/problems/11/complaints/6/alternatives/0` | `(alternatives 원소)` | 0 | string | 운동·식단 병행 필수 |  |
| 3139 | `/problems/11/complaints/7` | `(complaints 원소)` | 7 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 3140 | `/problems/11/complaints/7/cc` | `cc` |  | string | 엠스컬프트 |  |
| 3141 | `/problems/11/complaints/7/cc_detail` | `cc_detail` |  | string | HIFEM | OB-S12-04 |
| 3142 | `/problems/11/complaints/7/cc_group` | `cc_group` |  | string | 근육강화 |  |
| 3143 | `/problems/11/complaints/7/procedures` | `procedures` |  | array[1] | (배열 · 1개) |  |
| 3144 | `/problems/11/complaints/7/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 3145 | `/problems/11/complaints/7/procedures/0/name` | `name` |  | string | HIFES | OB-S12-04 |
| 3146 | `/problems/11/complaints/7/procedures/0/category` | `category` |  | string | M10 |  |
| 3147 | `/problems/11/complaints/7/procedures/0/role` | `role` |  | string | 근육 자극 |  |
| 3148 | `/problems/11/complaints/7/procedures/0/products` | `products` |  | array[0] | `[]` (빈 배열) |  |
| 3149 | `/problems/11/complaints/7/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 3150 | `/problems/11/complaints/7/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 3151 | `/problems/11/complaints/7/combos/0/name` | `name` |  | string | HIFES 시리즈 |  |
| 3152 | `/problems/11/complaints/7/combos/0/combo` | `combo` |  | array[1] | (배열 · 1개) |  |
| 3153 | `/problems/11/complaints/7/combos/0/combo/0` | `(combo 원소)` | 0 | string | HIFES |  |
| 3154 | `/problems/11/complaints/7/combos/0/reason` | `reason` |  | string | 근육 강화로 탄탄한 몸 |  |
| 3155 | `/problems/11/complaints/7/combos/0/evidence` | `evidence` |  | string | 4~6회 시리즈 | OB-S12-06 |
| 3156 | `/problems/11/complaints/7/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 3157 | `/problems/11/complaints/7/alternatives/0` | `(alternatives 원소)` | 0 | string | 운동·식단 병행 필수 |  |
| 3158 | `/problems/11/complaints/8` | `(complaints 원소)` | 8 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 3159 | `/problems/11/complaints/8/cc` | `cc` |  | string | 바디써마지 |  |
| 3160 | `/problems/11/complaints/8/cc_detail` | `cc_detail` |  | string | RF 타이트닝 |  |
| 3161 | `/problems/11/complaints/8/cc_group` | `cc_group` |  | string | 바디탄력 |  |
| 3162 | `/problems/11/complaints/8/procedures` | `procedures` |  | array[1] | (배열 · 1개) |  |
| 3163 | `/problems/11/complaints/8/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 3164 | `/problems/11/complaints/8/procedures/0/name` | `name` |  | string | 인모드 |  |
| 3165 | `/problems/11/complaints/8/procedures/0/category` | `category` |  | string | M9 |  |
| 3166 | `/problems/11/complaints/8/procedures/0/role` | `role` |  | string | 바디 타이트닝 |  |
| 3167 | `/problems/11/complaints/8/procedures/0/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 3168 | `/problems/11/complaints/8/procedures/0/products/0` | `(products 원소)` | 0 | string | 인모드 |  |
| 3169 | `/problems/11/complaints/8/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 3170 | `/problems/11/complaints/8/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 3171 | `/problems/11/complaints/8/combos/0/name` | `name` |  | string | 바디 타이트닝 |  |
| 3172 | `/problems/11/complaints/8/combos/0/combo` | `combo` |  | array[1] | (배열 · 1개) |  |
| 3173 | `/problems/11/complaints/8/combos/0/combo/0` | `(combo 원소)` | 0 | string | 인모드 |  |
| 3174 | `/problems/11/complaints/8/combos/0/reason` | `reason` |  | string | RF로 피부 탄력 |  |
| 3175 | `/problems/11/complaints/8/combos/0/evidence` | `evidence` |  | string | 바디 전용 핸드피스 | OB-S12-06 |
| 3176 | `/problems/11/complaints/8/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 3177 | `/problems/11/complaints/8/alternatives/0` | `(alternatives 원소)` | 0 | string | 운동·식단 병행 필수 |  |
| 3178 | `/problems/11/complaints/9` | `(complaints 원소)` | 9 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 3179 | `/problems/11/complaints/9/cc` | `cc` |  | string | 바디인모드 |  |
| 3180 | `/problems/11/complaints/9/cc_detail` | `cc_detail` |  | string | RF+IR |  |
| 3181 | `/problems/11/complaints/9/cc_group` | `cc_group` |  | string | 바디탄력 |  |
| 3182 | `/problems/11/complaints/9/procedures` | `procedures` |  | array[1] | (배열 · 1개) |  |
| 3183 | `/problems/11/complaints/9/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 3184 | `/problems/11/complaints/9/procedures/0/name` | `name` |  | string | 인모드 |  |
| 3185 | `/problems/11/complaints/9/procedures/0/category` | `category` |  | string | M9 |  |
| 3186 | `/problems/11/complaints/9/procedures/0/role` | `role` |  | string | 바디 타이트닝 |  |
| 3187 | `/problems/11/complaints/9/procedures/0/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 3188 | `/problems/11/complaints/9/procedures/0/products/0` | `(products 원소)` | 0 | string | 인모드 |  |
| 3189 | `/problems/11/complaints/9/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 3190 | `/problems/11/complaints/9/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 3191 | `/problems/11/complaints/9/combos/0/name` | `name` |  | string | 바디 타이트닝 |  |
| 3192 | `/problems/11/complaints/9/combos/0/combo` | `combo` |  | array[1] | (배열 · 1개) |  |
| 3193 | `/problems/11/complaints/9/combos/0/combo/0` | `(combo 원소)` | 0 | string | 인모드 |  |
| 3194 | `/problems/11/complaints/9/combos/0/reason` | `reason` |  | string | RF로 피부 탄력 |  |
| 3195 | `/problems/11/complaints/9/combos/0/evidence` | `evidence` |  | string | 바디 전용 핸드피스 |  |
| 3196 | `/problems/11/complaints/9/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 3197 | `/problems/11/complaints/9/alternatives/0` | `(alternatives 원소)` | 0 | string | 운동·식단 병행 필수 |  |
| 3198 | `/problems/11/complaints/10` | `(complaints 원소)` | 10 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 3199 | `/problems/11/complaints/10/cc` | `cc` |  | string | 엔더몰로지 |  |
| 3200 | `/problems/11/complaints/10/cc_detail` | `cc_detail` |  | string | 흡입마사지 |  |
| 3201 | `/problems/11/complaints/10/cc_group` | `cc_group` |  | string | 셀룰라이트 |  |
| 3202 | `/problems/11/complaints/10/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 3203 | `/problems/11/complaints/10/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 3204 | `/problems/11/complaints/10/procedures/0/name` | `name` |  | string | 인모드 |  |
| 3205 | `/problems/11/complaints/10/procedures/0/category` | `category` |  | string | M9 |  |
| 3206 | `/problems/11/complaints/10/procedures/0/role` | `role` |  | string | 셀룰라이트 개선 |  |
| 3207 | `/problems/11/complaints/10/procedures/0/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 3208 | `/problems/11/complaints/10/procedures/0/products/0` | `(products 원소)` | 0 | string | 인모드 |  |
| 3209 | `/problems/11/complaints/10/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 3210 | `/problems/11/complaints/10/procedures/1/name` | `name` |  | string | HIFES |  |
| 3211 | `/problems/11/complaints/10/procedures/1/category` | `category` |  | string | M10 |  |
| 3212 | `/problems/11/complaints/10/procedures/1/role` | `role` |  | string | 근육 강화 |  |
| 3213 | `/problems/11/complaints/10/procedures/1/products` | `products` |  | array[0] | `[]` (빈 배열) |  |
| 3214 | `/problems/11/complaints/10/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 3215 | `/problems/11/complaints/10/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 3216 | `/problems/11/complaints/10/combos/0/name` | `name` |  | string | 인모드 + HIFES |  |
| 3217 | `/problems/11/complaints/10/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 3218 | `/problems/11/complaints/10/combos/0/combo/0` | `(combo 원소)` | 0 | string | 인모드 |  |
| 3219 | `/problems/11/complaints/10/combos/0/combo/1` | `(combo 원소)` | 1 | string | HIFES |  |
| 3220 | `/problems/11/complaints/10/combos/0/reason` | `reason` |  | string | 피부 + 근육 동시 개선 |  |
| 3221 | `/problems/11/complaints/10/combos/0/evidence` | `evidence` |  | string | 셀룰라이트 + 탄력 |  |
| 3222 | `/problems/11/complaints/10/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 3223 | `/problems/11/complaints/10/alternatives/0` | `(alternatives 원소)` | 0 | string | 운동·식단 병행 필수 |  |

## 잠정 관찰 (원문 칸과 분리)

| ID | 상태 | 위치 | 관찰 |
|---|---|---|---|
| OB-S12-01 | B | `/problems/11/complaints/0/procedures/0`<br>`/problems/11/complaints/1/procedures/0`<br>`/problems/11/complaints/2/procedures/0`<br>`/problems/11/complaints/3/procedures/0`<br>`/problems/11/complaints/4/procedures/0`<br>`/problems/11/complaints/5/procedures/0`<br>`/problems/11/complaints/6/procedures/0` | c0~c6 의 procedures(크라이오·인모드)·combos·alternatives 가 글자 그대로 같다. cc 는 쿨스컬프팅·지방분해주사(PPC/DC)·HPL주사·BNLS주사·브이올렛·컷슬린·바디HIFU 로 주사·장비가 서로 다른데, 주사·HIFU 는 procedures 에 없다(B-02 · I-03 같은 유형). |
| OB-S12-02 | I | `/problems/11/complaints/4/cc_detail`<br>`/problems/10/complaints/2/cc_detail` | 브이올렛의 허가 진술이 두 곳에서 다르다. S11 c2: 'FDA 승인 제품은 Kybella/벨카이라'. S12 c4: 'FDA 승인 제품은 미국 Kybella이며 동일 성분 Belkyra는 국가별 허가를 구분'. 같은 제품명이 '벨카이라'(한글)·'Belkyra'(로마자) 두 표기로 나온다. 허가 사실을 판정하지 않는다(I-09). |
| OB-S12-03 | P | `/problems/11/complaints/4/cc_detail`<br>`/problems/11/complaints/4/cc_group` | c4 cc_detail 은 '바디·체간 지방 사용은 허가 외' 라고 쓰면서 cc_group '지방감소'(problem '바디') 아래에 있다. 원문 배치와 진술을 그대로 보존하고 판단하지 않는다. |
| OB-S12-04 | I | `/problems/11/complaints/7/cc_detail`<br>`/problems/11/complaints/7/procedures/0/name` | cc_detail 'HIFEM' 과 procedures name 'HIFES' 가 다른 약어다. 같은 것을 가리키는지 원문에 근거가 없다(I-10). |
| OB-S12-05 | P | `/problems/11/complaints/0/procedures/1/name`<br>`/problems/11/complaints/0/procedures/1/products/0` | procedures name '인모드' 와 products 원소 '인모드' 가 같다 — procedure 이름에 제품명이 쓰였다. c8 cc '바디써마지' 도 products 는 '인모드' 다. |
| OB-S12-06 | P | `/problems/11/complaints/7/combos/0/evidence`<br>`/problems/11/complaints/8/combos/0/evidence` | evidence '4~6회 시리즈'(회차 범위), '바디 전용 핸드피스'(장비 구성) — evidence 칸이 근거가 아니라 일정·장비 정보다(F-06). |
| OB-S12-07 | P | `/problems/11/complaints/0/alternatives/0` | alternatives '운동·식단 병행 필수' 가 11개 complaint 전부에 있다. 생활 관리 필수 지시이며 대안 시술이 아니다(F-04). |
| OB-S12-08 | B | `/problems/11/complaints/1/cc` | cc '지방분해주사(PPC/DC)' 의 'PPC/DC' 는 괄호 안 약어이며 cc_detail '포스파티딜콜린/데옥시콜산' 과 순서상 대응해 보이나 원문이 대응을 명시하지 않는다. HPL·BNLS·HIFEM·HIFES·IR 도 풀이 없음(B-03 같은 유형). |

## 수동 복합 표현 (직접 읽기 · 출현별)

| 표현 | 위치(Pointer · 값 내 구간) | 관점(탐색용, 확정 분류 아님) |
|---|---|---|
| 냉각지방분해 | `/problems/11/complaints/0/cc_detail` [0,6) | 기전 표현, 붙여 쓴 복합어 |
| 지방분해주사(PPC/DC) | `/problems/11/complaints/1/cc` [0,14) | 시술명 표현, 괄호 보충, 약어, 기호(/) |
| 포스파티딜콜린/데옥시콜산 | `/problems/11/complaints/1/cc_detail` [0,13) | 성분 표현, 기호(/) |
| 고농도 지방분해 | `/problems/11/complaints/2/cc_detail` [0,8) | 정도 수식(고농도), 기전 표현 |
| 식물추출 지방분해 | `/problems/11/complaints/3/cc_detail` [0,9) | 재료 수식(식물추출), 기전 표현 |
| 턱밑 지방 전용 국내 허가(데옥시콜산) | `/problems/11/complaints/4/cc_detail` [0,21) | 허가 상태 진술, 한정(전용), 범위(국내), 부위 표현, 괄호 보충 |
| 바디·체간 지방 사용은 허가 외 | `/problems/11/complaints/4/cc_detail` [23,40) | 허가 상태 진술(허가 외), 부위 표현, 기호(·) |
| FDA 승인 제품은 미국 Kybella이며 동일 성분 Belkyra는 국가별 허가를 구분 | `/problems/11/complaints/4/cc_detail` [42,91) | 허가 상태 진술, 기관 약어(FDA), 범위(미국·국가별), 제품명 표현, 동일 성분 |
| 지방분해 주사 | `/problems/11/complaints/5/cc_detail` [0,7) | 시술명 표현 |
| 리포소닉스 등 | `/problems/11/complaints/6/cc_detail` [0,7) | 장비명 표현, 열린 목록(등) |
| 바디HIFU | `/problems/11/complaints/6/cc` [0,6) | 부위+시술명 표현, 혼합 표기 |
| HIFEM | `/problems/11/complaints/7/cc_detail` [0,5) | 약어(원문 풀이 없음) |
| RF 타이트닝 | `/problems/11/complaints/8/cc_detail` [0,7)<br>`/problems/11/complaints/0/procedures/1/role` [0,7)<br>`/problems/11/complaints/1/procedures/1/role` [0,7)<br>`/problems/11/complaints/2/procedures/1/role` [0,7)<br>`/problems/11/complaints/3/procedures/1/role` [0,7)<br>`/problems/11/complaints/4/procedures/1/role` [0,7)<br>`/problems/11/complaints/5/procedures/1/role` [0,7)<br>`/problems/11/complaints/6/procedures/1/role` [0,7) | 기전 약어(RF), 효과 표현 |
| RF+IR | `/problems/11/complaints/9/cc_detail` [0,5) | 약어, 기호(+ 공백 없음) |
| 흡입마사지 | `/problems/11/complaints/10/cc_detail` [0,5) | 기전 표현, 붙여 쓴 복합어 |
| 지방 동결 파괴 | `/problems/11/complaints/0/procedures/0/role` [0,8)<br>`/problems/11/complaints/1/procedures/0/role` [0,8)<br>`/problems/11/complaints/2/procedures/0/role` [0,8)<br>`/problems/11/complaints/3/procedures/0/role` [0,8)<br>`/problems/11/complaints/4/procedures/0/role` [0,8)<br>`/problems/11/complaints/5/procedures/0/role` [0,8)<br>`/problems/11/complaints/6/procedures/0/role` [0,8) | role 표현, 기전 표현 |
| 지방파괴 + 피부타이트닝 | `/problems/11/complaints/0/combos/0/reason` [0,13)<br>`/problems/11/complaints/1/combos/0/reason` [0,13)<br>`/problems/11/complaints/2/combos/0/reason` [0,13)<br>`/problems/11/complaints/3/combos/0/reason` [0,13)<br>`/problems/11/complaints/4/combos/0/reason` [0,13)<br>`/problems/11/complaints/5/combos/0/reason` [0,13)<br>`/problems/11/complaints/6/combos/0/reason` [0,13) | 기호(+), 결과 없는 공식형 |
| 지방 빼고 피부 조임 | `/problems/11/complaints/0/combos/0/evidence` [0,11)<br>`/problems/11/complaints/1/combos/0/evidence` [0,11)<br>`/problems/11/complaints/2/combos/0/evidence` [0,11)<br>`/problems/11/complaints/3/combos/0/evidence` [0,11)<br>`/problems/11/complaints/4/combos/0/evidence` [0,11)<br>`/problems/11/complaints/5/combos/0/evidence` [0,11)<br>`/problems/11/complaints/6/combos/0/evidence` [0,11) | 감소 표현, 병렬(-고), 효과 표현 |
| 운동·식단 병행 필수 | `/problems/11/complaints/0/alternatives/0` [0,11)<br>`/problems/11/complaints/1/alternatives/0` [0,11)<br>`/problems/11/complaints/2/alternatives/0` [0,11)<br>`/problems/11/complaints/3/alternatives/0` [0,11)<br>`/problems/11/complaints/4/alternatives/0` [0,11)<br>`/problems/11/complaints/5/alternatives/0` [0,11)<br>`/problems/11/complaints/6/alternatives/0` [0,11)<br>`/problems/11/complaints/7/alternatives/0` [0,11)<br>`/problems/11/complaints/8/alternatives/0` [0,11)<br>`/problems/11/complaints/9/alternatives/0` [0,11)<br>`/problems/11/complaints/10/alternatives/0` [0,11) | 병행, 필수 지시, 생활 관리, 기호(·) |
| HIFES 시리즈 | `/problems/11/complaints/7/combos/0/name` [0,9) | combo name(단독), 회차 표현(시리즈), 약어 |
| 근육 강화로 탄탄한 몸 | `/problems/11/complaints/7/combos/0/reason` [0,12) | 수단(-로)+결과, 증가 표현(강화), 수식(탄탄한) |
| 4~6회 시리즈 | `/problems/11/complaints/7/combos/0/evidence` [0,8) | 범위(~), 회차 |
| RF로 피부 탄력 | `/problems/11/complaints/8/combos/0/reason` [0,9)<br>`/problems/11/complaints/9/combos/0/reason` [0,9) | 수단(-로), 효과 표현 |
| 바디 전용 핸드피스 | `/problems/11/complaints/8/combos/0/evidence` [0,10)<br>`/problems/11/complaints/9/combos/0/evidence` [0,10) | 한정(전용), 장비 구성 |
| 바디 타이트닝 | `/problems/11/complaints/8/procedures/0/role` [0,7)<br>`/problems/11/complaints/9/procedures/0/role` [0,7)<br>`/problems/11/complaints/8/combos/0/name` [0,7)<br>`/problems/11/complaints/9/combos/0/name` [0,7) | 부위+효과 표현 |
| 피부 + 근육 동시 개선 | `/problems/11/complaints/10/combos/0/reason` [0,13) | 기호(+), 동시성(동시) |
| 셀룰라이트 + 탄력 | `/problems/11/complaints/10/combos/0/evidence` [0,10) | 기호(+), 증상·효과 표현 |
| 셀룰라이트 개선 | `/problems/11/complaints/10/procedures/0/role` [0,8) | role 표현, 증상 표현 |

## 이 구획에서 연 미결

- **I-09** (I) 같은 cc '브이올렛' 의 허가 진술이 두 problem 에서 다르고(FDA 승인 제품 범위), 제품명이 '벨카이라'/'Belkyra' 두 표기로 나온다. — 영향: 허가 정보를 합치면 서로 맞지 않는다. 사실 판정은 이 단계 범위 밖이며 원본 변경 제안은 후속 확인 후보.
- **I-10** (I) cc_detail 'HIFEM' 과 procedures name 'HIFES' 약어 불일치. — 영향: cc_detail 과 procedure 를 잇지 못한다.
