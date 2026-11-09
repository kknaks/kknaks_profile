# S04 — /problems/3 P4 항노화

[← review.md](review.md) · 범위 /problems/3 및 /problems/3/** 전체 · 소유 노드 222 · 말단 144 · 빈 값 3 · 직접 읽기 done

상위 문맥(공유, S00 소유): 루트 객체 → `/description` = taxonomy P1~P14 하위구조 기반 CC 자동 생성 → `/problems` 배열.

직접 읽기: reading/S04.txt 로 c0~c6 전부(procedures 15·combos 8·alternatives 9) 읽음.

## 원문 값 (문서 순서 · 전부)

| # | JSON Pointer | 원본 컬럼명 | 배열 순번 | 자료형 | 원문 값 | 관찰 참조 |
|---|---|---|---|---|---|---|
| 1027 | `/problems/3` | `(problems 원소)` | 3 | object{3} | (객체 · 키: `problem_id`, `problem`, `complaints`) |  |
| 1028 | `/problems/3/problem_id` | `problem_id` |  | string | P4 |  |
| 1029 | `/problems/3/problem` | `problem` |  | string | 항노화 |  |
| 1030 | `/problems/3/complaints` | `complaints` |  | array[7] | (배열 · 7개) |  |
| 1031 | `/problems/3/complaints/0` | `(complaints 원소)` | 0 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 1032 | `/problems/3/complaints/0/cc` | `cc` |  | string | 스킨부스터시술 |  |
| 1033 | `/problems/3/complaints/0/cc_detail` | `cc_detail` |  | string | 리쥬란/쥬베룩 등 | OB-S04-01 |
| 1034 | `/problems/3/complaints/0/cc_group` | `cc_group` |  | string | 피부재생/탄력 |  |
| 1035 | `/problems/3/complaints/0/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 1036 | `/problems/3/complaints/0/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1037 | `/problems/3/complaints/0/procedures/0/name` | `name` |  | string | 스킨부스터 |  |
| 1038 | `/problems/3/complaints/0/procedures/0/category` | `category` |  | string | M4 |  |
| 1039 | `/problems/3/complaints/0/procedures/0/role` | `role` |  | string | 피부 재생 |  |
| 1040 | `/problems/3/complaints/0/procedures/0/products` | `products` |  | array[3] | (배열 · 3개) |  |
| 1041 | `/problems/3/complaints/0/procedures/0/products/0` | `(products 원소)` | 0 | string | 리쥬란 힐러 |  |
| 1042 | `/problems/3/complaints/0/procedures/0/products/1` | `(products 원소)` | 1 | string | 쥬베룩 |  |
| 1043 | `/problems/3/complaints/0/procedures/0/products/2` | `(products 원소)` | 2 | string | 리쥬란 HB+ |  |
| 1044 | `/problems/3/complaints/0/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1045 | `/problems/3/complaints/0/procedures/1/name` | `name` |  | string | 리프팅기기 |  |
| 1046 | `/problems/3/complaints/0/procedures/1/category` | `category` |  | string | M9 |  |
| 1047 | `/problems/3/complaints/0/procedures/1/role` | `role` |  | string | 타이트닝 | OB-S04-11 |
| 1048 | `/problems/3/complaints/0/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1049 | `/problems/3/complaints/0/procedures/1/products/0` | `(products 원소)` | 0 | string | 써마지FLX |  |
| 1050 | `/problems/3/complaints/0/procedures/1/products/1` | `(products 원소)` | 1 | string | 울쎄라 |  |
| 1051 | `/problems/3/complaints/0/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 1052 | `/problems/3/complaints/0/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 1053 | `/problems/3/complaints/0/combos/0/name` | `name` |  | string | 스킨부스터 + 리프팅기기 |  |
| 1054 | `/problems/3/complaints/0/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 1055 | `/problems/3/complaints/0/combos/0/combo/0` | `(combo 원소)` | 0 | string | 스킨부스터 |  |
| 1056 | `/problems/3/complaints/0/combos/0/combo/1` | `(combo 원소)` | 1 | string | 리프팅기기 |  |
| 1057 | `/problems/3/complaints/0/combos/0/reason` | `reason` |  | string | 재생 + 타이트닝 |  |
| 1058 | `/problems/3/complaints/0/combos/0/evidence` | `evidence` |  | string | 피부 젊어짐 | OB-S04-10 |
| 1059 | `/problems/3/complaints/0/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 1060 | `/problems/3/complaints/0/alternatives/0` | `(alternatives 원소)` | 0 | string | 단계별 접근 추천 | OB-S04-07 |
| 1061 | `/problems/3/complaints/1` | `(complaints 원소)` | 1 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 1062 | `/problems/3/complaints/1/cc` | `cc` |  | string | 바이오스티뮬레이터시술 |  |
| 1063 | `/problems/3/complaints/1/cc_detail` | `cc_detail` |  | string | 스컬트라/엘란쎄 등 | OB-S04-01 |
| 1064 | `/problems/3/complaints/1/cc_group` | `cc_group` |  | string | 피부재생/탄력 |  |
| 1065 | `/problems/3/complaints/1/procedures` | `procedures` |  | array[1] | (배열 · 1개) |  |
| 1066 | `/problems/3/complaints/1/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1067 | `/problems/3/complaints/1/procedures/0/name` | `name` |  | string | 바이오스티뮬레이터/콜라겐부스터 | OB-S04-02 |
| 1068 | `/problems/3/complaints/1/procedures/0/category` | `category` |  | string | M3 |  |
| 1069 | `/problems/3/complaints/1/procedures/0/role` | `role` |  | string | 자가 콜라겐 생성 촉진 |  |
| 1070 | `/problems/3/complaints/1/procedures/0/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1071 | `/problems/3/complaints/1/procedures/0/products/0` | `(products 원소)` | 0 | string | 스컬트라 |  |
| 1072 | `/problems/3/complaints/1/procedures/0/products/1` | `(products 원소)` | 1 | string | 엘란쎄 |  |
| 1073 | `/problems/3/complaints/1/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 1074 | `/problems/3/complaints/1/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 1075 | `/problems/3/complaints/1/combos/0/name` | `name` |  | string | 바이오스티뮬레이터 | OB-S04-04 |
| 1076 | `/problems/3/complaints/1/combos/0/combo` | `combo` |  | array[1] | (배열 · 1개) |  |
| 1077 | `/problems/3/complaints/1/combos/0/combo/0` | `(combo 원소)` | 0 | string | 바이오스티뮬레이터/콜라겐부스터 | OB-S04-02 |
| 1078 | `/problems/3/complaints/1/combos/0/reason` | `reason` |  | string | PLLA/PCL 기반 콜라겐 생성 촉진 | OB-S04-05 |
| 1079 | `/problems/3/complaints/1/combos/0/evidence` | `evidence` |  | string | 즉각 볼륨보다 수개월에 걸친 자가 콜라겐 재생을 목표로 함 | OB-S04-06 |
| 1080 | `/problems/3/complaints/1/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 1081 | `/problems/3/complaints/1/alternatives/0` | `(alternatives 원소)` | 0 | string | 단계별 접근 추천 | OB-S04-07 |
| 1082 | `/problems/3/complaints/2` | `(complaints 원소)` | 2 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 1083 | `/problems/3/complaints/2/cc` | `cc` |  | string | PRP시술 |  |
| 1084 | `/problems/3/complaints/2/cc_detail` | `cc_detail` |  | string | 자가혈 재생 |  |
| 1085 | `/problems/3/complaints/2/cc_group` | `cc_group` |  | string | 피부재생/탄력 |  |
| 1086 | `/problems/3/complaints/2/procedures` | `procedures` |  | array[1] | (배열 · 1개) |  |
| 1087 | `/problems/3/complaints/2/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1088 | `/problems/3/complaints/2/procedures/0/name` | `name` |  | string | PRP | OB-S04-03 |
| 1089 | `/problems/3/complaints/2/procedures/0/category` | `category` |  | string | M5 | OB-S00-07 |
| 1090 | `/problems/3/complaints/2/procedures/0/role` | `role` |  | string | 자가혈 혈소판 성장인자 기반 재생 |  |
| 1091 | `/problems/3/complaints/2/procedures/0/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1092 | `/problems/3/complaints/2/procedures/0/products/0` | `(products 원소)` | 0 | string | 셀피아 |  |
| 1093 | `/problems/3/complaints/2/procedures/0/products/1` | `(products 원소)` | 1 | string | 리젠ACR |  |
| 1094 | `/problems/3/complaints/2/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 1095 | `/problems/3/complaints/2/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 1096 | `/problems/3/complaints/2/combos/0/name` | `name` |  | string | PRP | OB-S04-04 |
| 1097 | `/problems/3/complaints/2/combos/0/combo` | `combo` |  | array[1] | (배열 · 1개) |  |
| 1098 | `/problems/3/complaints/2/combos/0/combo/0` | `(combo 원소)` | 0 | string | PRP |  |
| 1099 | `/problems/3/complaints/2/combos/0/reason` | `reason` |  | string | 자가혈 유래 혈소판 성장인자로 조직 재생 보조 |  |
| 1100 | `/problems/3/complaints/2/combos/0/evidence` | `evidence` |  | string | 자가혈 PRP를 이용한 피부질감·회복 보조 |  |
| 1101 | `/problems/3/complaints/2/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 1102 | `/problems/3/complaints/2/alternatives/0` | `(alternatives 원소)` | 0 | string | 단계별 접근 추천 | OB-S04-07 |
| 1103 | `/problems/3/complaints/3` | `(complaints 원소)` | 3 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 1104 | `/problems/3/complaints/3/cc` | `cc` |  | string | 필러볼륨 |  |
| 1105 | `/problems/3/complaints/3/cc_detail` | `cc_detail` |  | string | 꺼진 부위 충전 |  |
| 1106 | `/problems/3/complaints/3/cc_group` | `cc_group` |  | string | 볼륨회복 |  |
| 1107 | `/problems/3/complaints/3/procedures` | `procedures` |  | array[3] | (배열 · 3개) |  |
| 1108 | `/problems/3/complaints/3/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1109 | `/problems/3/complaints/3/procedures/0/name` | `name` |  | string | 필러 |  |
| 1110 | `/problems/3/complaints/3/procedures/0/category` | `category` |  | string | M2 |  |
| 1111 | `/problems/3/complaints/3/procedures/0/role` | `role` |  | string | 볼륨 충전 |  |
| 1112 | `/problems/3/complaints/3/procedures/0/products` | `products` |  | array[3] | (배열 · 3개) |  |
| 1113 | `/problems/3/complaints/3/procedures/0/products/0` | `(products 원소)` | 0 | string | 쥬비덤 |  |
| 1114 | `/problems/3/complaints/3/procedures/0/products/1` | `(products 원소)` | 1 | string | 레스틸렌 |  |
| 1115 | `/problems/3/complaints/3/procedures/0/products/2` | `(products 원소)` | 2 | string | 이브아르 |  |
| 1116 | `/problems/3/complaints/3/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1117 | `/problems/3/complaints/3/procedures/1/name` | `name` |  | string | 보톡스 |  |
| 1118 | `/problems/3/complaints/3/procedures/1/category` | `category` |  | string | M1 |  |
| 1119 | `/problems/3/complaints/3/procedures/1/role` | `role` |  | string | 근이완 보조 |  |
| 1120 | `/problems/3/complaints/3/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1121 | `/problems/3/complaints/3/procedures/1/products/0` | `(products 원소)` | 0 | string | 보톡스 |  |
| 1122 | `/problems/3/complaints/3/procedures/1/products/1` | `(products 원소)` | 1 | string | 나보타 |  |
| 1123 | `/problems/3/complaints/3/procedures/2` | `(procedures 원소)` | 2 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1124 | `/problems/3/complaints/3/procedures/2/name` | `name` |  | string | 바이오스티뮬레이터/콜라겐부스터 |  |
| 1125 | `/problems/3/complaints/3/procedures/2/category` | `category` |  | string | M3 |  |
| 1126 | `/problems/3/complaints/3/procedures/2/role` | `role` |  | string | 장기 콜라겐 | OB-S04-11 |
| 1127 | `/problems/3/complaints/3/procedures/2/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1128 | `/problems/3/complaints/3/procedures/2/products/0` | `(products 원소)` | 0 | string | 스컬트라 |  |
| 1129 | `/problems/3/complaints/3/procedures/2/products/1` | `(products 원소)` | 1 | string | 엘란쎄 |  |
| 1130 | `/problems/3/complaints/3/combos` | `combos` |  | array[2] | (배열 · 2개) |  |
| 1131 | `/problems/3/complaints/3/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 1132 | `/problems/3/complaints/3/combos/0/name` | `name` |  | string | 필러 + 보톡스 |  |
| 1133 | `/problems/3/complaints/3/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 1134 | `/problems/3/complaints/3/combos/0/combo/0` | `(combo 원소)` | 0 | string | 필러 |  |
| 1135 | `/problems/3/complaints/3/combos/0/combo/1` | `(combo 원소)` | 1 | string | 보톡스 |  |
| 1136 | `/problems/3/complaints/3/combos/0/reason` | `reason` |  | string | 볼륨 + 근이완 = 시너지 |  |
| 1137 | `/problems/3/complaints/3/combos/0/evidence` | `evidence` |  | string | 보톡스가 근육 움직임 줄여 필러 유지력 향상 |  |
| 1138 | `/problems/3/complaints/3/combos/1` | `(combos 원소)` | 1 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 1139 | `/problems/3/complaints/3/combos/1/name` | `name` |  | string | 필러 + 바이오스티뮬레이터 |  |
| 1140 | `/problems/3/complaints/3/combos/1/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 1141 | `/problems/3/complaints/3/combos/1/combo/0` | `(combo 원소)` | 0 | string | 필러 |  |
| 1142 | `/problems/3/complaints/3/combos/1/combo/1` | `(combo 원소)` | 1 | string | 바이오스티뮬레이터 | OB-S00-05, OB-S04-02 |
| 1143 | `/problems/3/complaints/3/combos/1/reason` | `reason` |  | string | 즉각 볼륨 + 장기 재생 | OB-S04-06 |
| 1144 | `/problems/3/complaints/3/combos/1/evidence` | `evidence` |  | string | 필러가 브릿지, 바이오스티뮬레이터가 장기 효과 | OB-S04-12 |
| 1145 | `/problems/3/complaints/3/alternatives` | `alternatives` |  | array[2] | (배열 · 2개) |  |
| 1146 | `/problems/3/complaints/3/alternatives/0` | `(alternatives 원소)` | 0 | string | 바이오스티뮬레이터로 장기 관리 |  |
| 1147 | `/problems/3/complaints/3/alternatives/1` | `(alternatives 원소)` | 1 | string | 단계별 접근 추천 | OB-S04-07 |
| 1148 | `/problems/3/complaints/4` | `(complaints 원소)` | 4 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 1149 | `/problems/3/complaints/4/cc` | `cc` |  | string | 지방이식 |  |
| 1150 | `/problems/3/complaints/4/cc_detail` | `cc_detail` |  | string | 자연 볼륨 |  |
| 1151 | `/problems/3/complaints/4/cc_group` | `cc_group` |  | string | 볼륨회복 |  |
| 1152 | `/problems/3/complaints/4/procedures` | `procedures` |  | array[4] | (배열 · 4개) |  |
| 1153 | `/problems/3/complaints/4/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1154 | `/problems/3/complaints/4/procedures/0/name` | `name` |  | string | 지방이식 |  |
| 1155 | `/problems/3/complaints/4/procedures/0/category` | `category` |  | string | M6 |  |
| 1156 | `/problems/3/complaints/4/procedures/0/role` | `role` |  | string | 자가지방 이식 |  |
| 1157 | `/problems/3/complaints/4/procedures/0/products` | `products` |  | array[0] | `[]` (빈 배열) |  |
| 1158 | `/problems/3/complaints/4/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1159 | `/problems/3/complaints/4/procedures/1/name` | `name` |  | string | PRP/자가혈 | OB-S04-03 |
| 1160 | `/problems/3/complaints/4/procedures/1/category` | `category` |  | string | M5 |  |
| 1161 | `/problems/3/complaints/4/procedures/1/role` | `role` |  | string | 생착률 향상 |  |
| 1162 | `/problems/3/complaints/4/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1163 | `/problems/3/complaints/4/procedures/1/products/0` | `(products 원소)` | 0 | string | 셀피아 |  |
| 1164 | `/problems/3/complaints/4/procedures/1/products/1` | `(products 원소)` | 1 | string | 리젠ACR |  |
| 1165 | `/problems/3/complaints/4/procedures/2` | `(procedures 원소)` | 2 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1166 | `/problems/3/complaints/4/procedures/2/name` | `name` |  | string | 필러 |  |
| 1167 | `/problems/3/complaints/4/procedures/2/category` | `category` |  | string | M2 |  |
| 1168 | `/problems/3/complaints/4/procedures/2/role` | `role` |  | string | 볼륨 충전 |  |
| 1169 | `/problems/3/complaints/4/procedures/2/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1170 | `/problems/3/complaints/4/procedures/2/products/0` | `(products 원소)` | 0 | string | 쥬비덤 |  |
| 1171 | `/problems/3/complaints/4/procedures/2/products/1` | `(products 원소)` | 1 | string | 레스틸렌 |  |
| 1172 | `/problems/3/complaints/4/procedures/3` | `(procedures 원소)` | 3 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1173 | `/problems/3/complaints/4/procedures/3/name` | `name` |  | string | 바이오스티뮬레이터/콜라겐부스터 |  |
| 1174 | `/problems/3/complaints/4/procedures/3/category` | `category` |  | string | M3 |  |
| 1175 | `/problems/3/complaints/4/procedures/3/role` | `role` |  | string | 장기 콜라겐 |  |
| 1176 | `/problems/3/complaints/4/procedures/3/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1177 | `/problems/3/complaints/4/procedures/3/products/0` | `(products 원소)` | 0 | string | 스컬트라 |  |
| 1178 | `/problems/3/complaints/4/procedures/3/products/1` | `(products 원소)` | 1 | string | 엘란쎄 |  |
| 1179 | `/problems/3/complaints/4/combos` | `combos` |  | array[2] | (배열 · 2개) |  |
| 1180 | `/problems/3/complaints/4/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 1181 | `/problems/3/complaints/4/combos/0/name` | `name` |  | string | 지방이식 + PRP |  |
| 1182 | `/problems/3/complaints/4/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 1183 | `/problems/3/complaints/4/combos/0/combo/0` | `(combo 원소)` | 0 | string | 지방이식 |  |
| 1184 | `/problems/3/complaints/4/combos/0/combo/1` | `(combo 원소)` | 1 | string | PRP | OB-S00-05 |
| 1185 | `/problems/3/complaints/4/combos/0/reason` | `reason` |  | string | 자가지방 + 성장인자 = 생착률 향상 |  |
| 1186 | `/problems/3/complaints/4/combos/0/evidence` | `evidence` |  | string | PRP가 지방세포 생존율 높임 |  |
| 1187 | `/problems/3/complaints/4/combos/1` | `(combos 원소)` | 1 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 1188 | `/problems/3/complaints/4/combos/1/name` | `name` |  | string | 필러 + 바이오스티뮬레이터 |  |
| 1189 | `/problems/3/complaints/4/combos/1/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 1190 | `/problems/3/complaints/4/combos/1/combo/0` | `(combo 원소)` | 0 | string | 필러 |  |
| 1191 | `/problems/3/complaints/4/combos/1/combo/1` | `(combo 원소)` | 1 | string | 바이오스티뮬레이터 | OB-S00-05, OB-S04-02 |
| 1192 | `/problems/3/complaints/4/combos/1/reason` | `reason` |  | string | 즉각 볼륨 + 장기 재생 |  |
| 1193 | `/problems/3/complaints/4/combos/1/evidence` | `evidence` |  | string | 필러가 브릿지, 바이오스티뮬레이터가 장기 효과 |  |
| 1194 | `/problems/3/complaints/4/alternatives` | `alternatives` |  | array[2] | (배열 · 2개) |  |
| 1195 | `/problems/3/complaints/4/alternatives/0` | `(alternatives 원소)` | 0 | string | 필러가 간편한 대안 |  |
| 1196 | `/problems/3/complaints/4/alternatives/1` | `(alternatives 원소)` | 1 | string | 단계별 접근 추천 | OB-S04-07 |
| 1197 | `/problems/3/complaints/5` | `(complaints 원소)` | 5 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 1198 | `/problems/3/complaints/5/cc` | `cc` |  | string | NAD+수액 | OB-S04-08 |
| 1199 | `/problems/3/complaints/5/cc_detail` | `cc_detail` |  | string | 세포에너지 |  |
| 1200 | `/problems/3/complaints/5/cc_group` | `cc_group` |  | string | 전신항노화 |  |
| 1201 | `/problems/3/complaints/5/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 1202 | `/problems/3/complaints/5/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1203 | `/problems/3/complaints/5/procedures/0/name` | `name` |  | string | 수액 |  |
| 1204 | `/problems/3/complaints/5/procedures/0/category` | `category` |  | string | M16 |  |
| 1205 | `/problems/3/complaints/5/procedures/0/role` | `role` |  | string | 영양 공급 |  |
| 1206 | `/problems/3/complaints/5/procedures/0/products` | `products` |  | array[0] | `[]` (빈 배열) | OB-S04-09 |
| 1207 | `/problems/3/complaints/5/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1208 | `/problems/3/complaints/5/procedures/1/name` | `name` |  | string | 스킨부스터 |  |
| 1209 | `/problems/3/complaints/5/procedures/1/category` | `category` |  | string | M4 |  |
| 1210 | `/problems/3/complaints/5/procedures/1/role` | `role` |  | string | 피부 재생 |  |
| 1211 | `/problems/3/complaints/5/procedures/1/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 1212 | `/problems/3/complaints/5/procedures/1/products/0` | `(products 원소)` | 0 | string | 리쥬란 힐러 |  |
| 1213 | `/problems/3/complaints/5/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 1214 | `/problems/3/complaints/5/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 1215 | `/problems/3/complaints/5/combos/0/name` | `name` |  | string | 수액 + 스킨부스터 |  |
| 1216 | `/problems/3/complaints/5/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 1217 | `/problems/3/complaints/5/combos/0/combo/0` | `(combo 원소)` | 0 | string | 수액 |  |
| 1218 | `/problems/3/complaints/5/combos/0/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 1219 | `/problems/3/complaints/5/combos/0/reason` | `reason` |  | string | 전신 영양 + 피부 재생 |  |
| 1220 | `/problems/3/complaints/5/combos/0/evidence` | `evidence` |  | string | 안팎으로 동시 관리 | OB-S04-10 |
| 1221 | `/problems/3/complaints/5/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 1222 | `/problems/3/complaints/5/alternatives/0` | `(alternatives 원소)` | 0 | string | 단계별 접근 추천 | OB-S04-07 |
| 1223 | `/problems/3/complaints/6` | `(complaints 원소)` | 6 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 1224 | `/problems/3/complaints/6/cc` | `cc` |  | string | 항산화수액 |  |
| 1225 | `/problems/3/complaints/6/cc_detail` | `cc_detail` |  | string | 글루타치온/비타민C |  |
| 1226 | `/problems/3/complaints/6/cc_group` | `cc_group` |  | string | 전신항노화 |  |
| 1227 | `/problems/3/complaints/6/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 1228 | `/problems/3/complaints/6/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1229 | `/problems/3/complaints/6/procedures/0/name` | `name` |  | string | 수액 |  |
| 1230 | `/problems/3/complaints/6/procedures/0/category` | `category` |  | string | M16 |  |
| 1231 | `/problems/3/complaints/6/procedures/0/role` | `role` |  | string | 영양 공급 |  |
| 1232 | `/problems/3/complaints/6/procedures/0/products` | `products` |  | array[0] | `[]` (빈 배열) | OB-S04-09 |
| 1233 | `/problems/3/complaints/6/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1234 | `/problems/3/complaints/6/procedures/1/name` | `name` |  | string | 스킨부스터 |  |
| 1235 | `/problems/3/complaints/6/procedures/1/category` | `category` |  | string | M4 |  |
| 1236 | `/problems/3/complaints/6/procedures/1/role` | `role` |  | string | 피부 재생 |  |
| 1237 | `/problems/3/complaints/6/procedures/1/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 1238 | `/problems/3/complaints/6/procedures/1/products/0` | `(products 원소)` | 0 | string | 리쥬란 힐러 |  |
| 1239 | `/problems/3/complaints/6/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 1240 | `/problems/3/complaints/6/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 1241 | `/problems/3/complaints/6/combos/0/name` | `name` |  | string | 수액 + 스킨부스터 |  |
| 1242 | `/problems/3/complaints/6/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 1243 | `/problems/3/complaints/6/combos/0/combo/0` | `(combo 원소)` | 0 | string | 수액 |  |
| 1244 | `/problems/3/complaints/6/combos/0/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 1245 | `/problems/3/complaints/6/combos/0/reason` | `reason` |  | string | 전신 영양 + 피부 재생 |  |
| 1246 | `/problems/3/complaints/6/combos/0/evidence` | `evidence` |  | string | 안팎으로 동시 관리 |  |
| 1247 | `/problems/3/complaints/6/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 1248 | `/problems/3/complaints/6/alternatives/0` | `(alternatives 원소)` | 0 | string | 단계별 접근 추천 | OB-S04-07 |

## 잠정 관찰 (원문 칸과 분리)

| ID | 상태 | 위치 | 관찰 |
|---|---|---|---|
| OB-S04-01 | P | `/problems/3/complaints/0/cc_detail`<br>`/problems/3/complaints/1/cc_detail` | cc_detail 에 제품명 나열과 열린 목록 표지 '등' 이 쓰였다('리쥬란/쥬베룩 등', '스컬트라/엘란쎄 등'). 제품 표기는 products 원소('리쥬란 힐러'·'리쥬란 HB+')와 다르다. |
| OB-S04-02 | I | `/problems/3/complaints/1/procedures/0/name`<br>`/problems/3/complaints/1/combos/0/combo/0`<br>`/problems/3/complaints/3/combos/1/combo/1`<br>`/problems/3/complaints/4/combos/1/combo/1` | procedures name '바이오스티뮬레이터/콜라겐부스터' 를 c1 combo 원소는 그대로 쓰지만 c3·c4 combo 원소와 combo name 은 '바이오스티뮬레이터' 로 줄여 쓴다(I-01 같은 유형). |
| OB-S04-03 | I | `/problems/3/complaints/2/procedures/0/name`<br>`/problems/3/complaints/4/procedures/1/name` | 같은 category M5 의 procedures name 이 c2 는 'PRP', c4 는 'PRP/자가혈' 이다(I-01 같은 유형). |
| OB-S04-04 | P | `/problems/3/complaints/1/combos/0/name`<br>`/problems/3/complaints/2/combos/0/name` | combo 원소가 1개인 combo('바이오스티뮬레이터', 'PRP')가 있다. name 은 원소와 같거나 줄인 표기다. S01 의 '반영구 단독' 과 같은 단독 묶음. |
| OB-S04-05 | P | `/problems/3/complaints/1/combos/0/reason` | reason 'PLLA/PCL 기반 콜라겐 생성 촉진' — 재질 표현(PLLA/PCL)이 나온다. products(스컬트라·엘란쎄)와 재질의 대응은 원문에 없다(채우지 않음). |
| OB-S04-06 | P | `/problems/3/complaints/1/combos/0/evidence`<br>`/problems/3/complaints/3/combos/1/reason` | '즉각 볼륨보다 수개월에 걸친 자가 콜라겐 재생을 목표로 함' — 비교(보다)·기간(수개월에 걸친)·목표 표현. '수개월' 은 범위 없는 막연한 기간이며 수치로 바꾸지 않는다. c3 reason '즉각 볼륨 + 장기 재생' 도 즉각/장기 대비. |
| OB-S04-07 | B | `/problems/3/complaints/0/alternatives/0`<br>`/problems/3/complaints/1/alternatives/0`<br>`/problems/3/complaints/2/alternatives/0`<br>`/problems/3/complaints/3/alternatives/1`<br>`/problems/3/complaints/4/alternatives/1`<br>`/problems/3/complaints/5/alternatives/0`<br>`/problems/3/complaints/6/alternatives/0` | alternatives '단계별 접근 추천' 이 7개 complaint 전부에 같다. 어떤 단계인지 원문에 없다(B-07). |
| OB-S04-08 | K | `/problems/3/complaints/5/cc` | cc 'NAD+수액' — '+' 가 성분명 일부로 붙어 있다(K-03 같은 유형). 기호 규칙의 '함께' 가 아니다(원문 표면상). |
| OB-S04-09 | P | `/problems/3/complaints/5/procedures/0/products`<br>`/problems/3/complaints/6/procedures/0/products` | 수액 procedures 의 products 가 빈 배열. cc_detail '글루타치온/비타민C' 는 성분 표현이다(products 와 다른 칸). |
| OB-S04-10 | P | `/problems/3/complaints/0/combos/0/evidence`<br>`/problems/3/complaints/5/combos/0/evidence` | evidence '피부 젊어짐', '안팎으로 동시 관리' — 막연한 효과 진술. 근거 출처 없음. |
| OB-S04-11 | P | `/problems/3/complaints/0/procedures/1/role`<br>`/problems/3/complaints/3/procedures/2/role` | role 표기 변형: 리프팅기기 '타이트닝'(S02·S03 은 '피부 타이트닝'), 바이오스티뮬레이터 '장기 콜라겐'(c1 은 '자가 콜라겐 생성 촉진'). |
| OB-S04-12 | P | `/problems/3/complaints/3/combos/1/evidence` | '필러가 브릿지, 바이오스티뮬레이터가 장기 효과' — '브릿지' 는 비유. 시간적 연결(즉각→장기)로 읽을 수 있으나 확정하지 않는다. |

## 수동 복합 표현 (직접 읽기 · 출현별)

| 표현 | 위치(Pointer · 값 내 구간) | 관점(탐색용, 확정 분류 아님) |
|---|---|---|
| 리쥬란/쥬베룩 등 | `/problems/3/complaints/0/cc_detail` [0,9) | 제품명 표현, 기호(/), 열린 목록(등) |
| 스컬트라/엘란쎄 등 | `/problems/3/complaints/1/cc_detail` [0,10) | 제품명 표현, 기호(/), 열린 목록(등) |
| 자가혈 재생 | `/problems/3/complaints/2/cc_detail` [0,6) | 재료+효과 표현 |
| 꺼진 부위 충전 | `/problems/3/complaints/3/cc_detail` [0,8) | 상태 수식(꺼진), 부위 표현(일반), 기전 표현 |
| 자연 볼륨 | `/problems/3/complaints/4/cc_detail` [0,5) | 목표·효과 표현, 수식(자연) |
| 세포에너지 | `/problems/3/complaints/5/cc_detail` [0,5) | 붙여 쓴 복합어, 효과 표현 |
| 글루타치온/비타민C | `/problems/3/complaints/6/cc_detail` [0,10) | 성분 표현, 기호(/), 혼합 표기 |
| 피부재생/탄력 | `/problems/3/complaints/0/cc_group` [0,7)<br>`/problems/3/complaints/1/cc_group` [0,7)<br>`/problems/3/complaints/2/cc_group` [0,7) | 효과 표현, 기호(/) |
| NAD+수액 | `/problems/3/complaints/5/cc` [0,6) | 성분+시술 표현, 이름 안의 기호(+), 혼합 표기 |
| 바이오스티뮬레이터/콜라겐부스터 | `/problems/3/complaints/1/procedures/0/name` [0,16)<br>`/problems/3/complaints/3/procedures/2/name` [0,16)<br>`/problems/3/complaints/4/procedures/3/name` [0,16)<br>`/problems/3/complaints/1/combos/0/combo/0` [0,16) | 시술명 표현, 기호(/) |
| 자가 콜라겐 생성 촉진 | `/problems/3/complaints/1/procedures/0/role` [0,12) | role 표현, 기전 표현, 증가 표현(촉진) |
| PLLA/PCL 기반 콜라겐 생성 촉진 | `/problems/3/complaints/1/combos/0/reason` [0,21) | 재질 표현, 기호(/), 약어, 기전 표현 |
| PLLA/PCL | `/problems/3/complaints/1/combos/0/reason` [0,8) | 재질 표현, 기호(/), 약어 |
| 즉각 볼륨보다 수개월에 걸친 자가 콜라겐 재생을 목표로 함 | `/problems/3/complaints/1/combos/0/evidence` [0,32) | 비교(보다), 기간(수개월에 걸친), 목표 표현, 시간 대비(즉각/수개월) |
| 수개월에 걸친 | `/problems/3/complaints/1/combos/0/evidence` [8,15) | 수량·단위·시간(막연), 기간 |
| 자가혈 혈소판 성장인자 기반 재생 | `/problems/3/complaints/2/procedures/0/role` [0,18) | role 표현, 재료·기전 표현 |
| 자가혈 유래 혈소판 성장인자로 조직 재생 보조 | `/problems/3/complaints/2/combos/0/reason` [0,25) | 수단(-로)+결과, 보조(주/부 구분), 기전 표현 |
| 자가혈 PRP를 이용한 피부질감·회복 보조 | `/problems/3/complaints/2/combos/0/evidence` [0,23) | 수단(이용한), 기호(·), 보조 |
| 재생 + 타이트닝 | `/problems/3/complaints/0/combos/0/reason` [0,9) | 기호(+), 결과 없는 공식형 |
| 피부 젊어짐 | `/problems/3/complaints/0/combos/0/evidence` [0,6) | 효과 표현(막연) |
| 즉각 볼륨 + 장기 재생 | `/problems/3/complaints/3/combos/1/reason` [0,13)<br>`/problems/3/complaints/4/combos/1/reason` [0,13) | 기호(+), 시간 대비(즉각/장기) |
| 필러가 브릿지, 바이오스티뮬레이터가 장기 효과 | `/problems/3/complaints/3/combos/1/evidence` [0,25)<br>`/problems/3/complaints/4/combos/1/evidence` [0,25) | 비유(브릿지), 대조 병렬, 기간 표현(장기) |
| 장기 콜라겐 | `/problems/3/complaints/3/procedures/2/role` [0,6)<br>`/problems/3/complaints/4/procedures/3/role` [0,6) | role 표현, 기간 표현(장기), 축약 표현 |
| 볼륨 + 근이완 = 시너지 | `/problems/3/complaints/3/combos/0/reason` [0,14) | 공식형 문장, 기호(+), 기호(=) |
| 보톡스가 근육 움직임 줄여 필러 유지력 향상 | `/problems/3/complaints/3/combos/0/evidence` [0,24) | 인과·기전 진술 |
| 자가지방 + 성장인자 = 생착률 향상 | `/problems/3/complaints/4/combos/0/reason` [0,20) | 공식형 문장, 기호(+), 기호(=) |
| PRP가 지방세포 생존율 높임 | `/problems/3/complaints/4/combos/0/evidence` [0,16) | 기전 진술, 증가 표현 |
| 전신 영양 + 피부 재생 | `/problems/3/complaints/5/combos/0/reason` [0,13)<br>`/problems/3/complaints/6/combos/0/reason` [0,13) | 기호(+), 범위(전신) |
| 안팎으로 동시 관리 | `/problems/3/complaints/5/combos/0/evidence` [0,10)<br>`/problems/3/complaints/6/combos/0/evidence` [0,10) | 동시성(동시), 대조(안팎) |
| 단계별 접근 추천 | `/problems/3/complaints/0/alternatives/0` [0,9)<br>`/problems/3/complaints/1/alternatives/0` [0,9)<br>`/problems/3/complaints/2/alternatives/0` [0,9)<br>`/problems/3/complaints/3/alternatives/1` [0,9)<br>`/problems/3/complaints/4/alternatives/1` [0,9)<br>`/problems/3/complaints/5/alternatives/0` [0,9)<br>`/problems/3/complaints/6/alternatives/0` [0,9) | 권고(추천), 단계(내용 없음) |
| 필러가 간편한 대안 | `/problems/3/complaints/4/alternatives/0` [0,10) | 대안 표현, 비교(간편한) |
| 바이오스티뮬레이터로 장기 관리 | `/problems/3/complaints/3/alternatives/0` [0,16) | 시술명 표현, 기간 표현(장기) |

## 이 구획에서 연 미결

- **B-07** (B) alternatives '단계별 접근 추천' 에 단계 내용이 없다(전 원장 반복 위치는 구획 관찰 참조). — 영향: 대안·순서 정보로 쓸 수 없다.
