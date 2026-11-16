# S03 — /problems/2 P3 쳐짐

[← review.md](review.md) · 범위 /problems/2 및 /problems/2/** 전체 · 소유 노드 236 · 말단 160 · 빈 값 1 · 직접 읽기 done

상위 문맥(공유, S00 소유): 루트 객체 → `/description` = taxonomy P1~P14 하위구조 기반 CC 자동 생성 → `/problems` 배열.

직접 읽기: reading/S03.txt 로 c0~c4 전부(procedures 16·combos 11·alternatives 5) 읽음.

## 원문 값 (문서 순서 · 전부)

| # | JSON Pointer | 원본 컬럼명 | 배열 순번 | 자료형 | 원문 값 | 관찰 참조 |
|---|---|---|---|---|---|---|
| 791 | `/problems/2` | `(problems 원소)` | 2 | object{3} | (객체 · 키: `problem_id`, `problem`, `complaints`) |  |
| 792 | `/problems/2/problem_id` | `problem_id` |  | string | P3 |  |
| 793 | `/problems/2/problem` | `problem` |  | string | 쳐짐 | OB-S03-01 |
| 794 | `/problems/2/complaints` | `complaints` |  | array[5] | (배열 · 5개) |  |
| 795 | `/problems/2/complaints/0` | `(complaints 원소)` | 0 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 796 | `/problems/2/complaints/0/cc` | `cc` |  | string | 볼쳐짐/불독살 | OB-S03-05 |
| 797 | `/problems/2/complaints/0/cc_detail` | `cc_detail` |  | string | 기기리프팅/실리프팅 |  |
| 798 | `/problems/2/complaints/0/cc_group` | `cc_group` |  | string | 얼굴 쳐짐 |  |
| 799 | `/problems/2/complaints/0/procedures` | `procedures` |  | array[3] | (배열 · 3개) |  |
| 800 | `/problems/2/complaints/0/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) | OB-S03-02 |
| 801 | `/problems/2/complaints/0/procedures/0/name` | `name` |  | string | 리프팅기기 |  |
| 802 | `/problems/2/complaints/0/procedures/0/category` | `category` |  | string | M9 |  |
| 803 | `/problems/2/complaints/0/procedures/0/role` | `role` |  | string | 피부 타이트닝 |  |
| 804 | `/problems/2/complaints/0/procedures/0/products` | `products` |  | array[3] | (배열 · 3개) |  |
| 805 | `/problems/2/complaints/0/procedures/0/products/0` | `(products 원소)` | 0 | string | 울쎄라 |  |
| 806 | `/problems/2/complaints/0/procedures/0/products/1` | `(products 원소)` | 1 | string | 써마지FLX |  |
| 807 | `/problems/2/complaints/0/procedures/0/products/2` | `(products 원소)` | 2 | string | 슈링크유니버스 |  |
| 808 | `/problems/2/complaints/0/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 809 | `/problems/2/complaints/0/procedures/1/name` | `name` |  | string | 실리프팅 |  |
| 810 | `/problems/2/complaints/0/procedures/1/category` | `category` |  | string | M7 |  |
| 811 | `/problems/2/complaints/0/procedures/1/role` | `role` |  | string | 물리적 거상 |  |
| 812 | `/problems/2/complaints/0/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 813 | `/problems/2/complaints/0/procedures/1/products/0` | `(products 원소)` | 0 | string | 민트리프트 |  |
| 814 | `/problems/2/complaints/0/procedures/1/products/1` | `(products 원소)` | 1 | string | 테스리프트 |  |
| 815 | `/problems/2/complaints/0/procedures/2` | `(procedures 원소)` | 2 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 816 | `/problems/2/complaints/0/procedures/2/name` | `name` |  | string | 스킨부스터 |  |
| 817 | `/problems/2/complaints/0/procedures/2/category` | `category` |  | string | M4 |  |
| 818 | `/problems/2/complaints/0/procedures/2/role` | `role` |  | string | 피부 재생 |  |
| 819 | `/problems/2/complaints/0/procedures/2/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 820 | `/problems/2/complaints/0/procedures/2/products/0` | `(products 원소)` | 0 | string | 리쥬란 힐러 |  |
| 821 | `/problems/2/complaints/0/procedures/2/products/1` | `(products 원소)` | 1 | string | 쥬베룩 |  |
| 822 | `/problems/2/complaints/0/combos` | `combos` |  | array[2] | (배열 · 2개) |  |
| 823 | `/problems/2/complaints/0/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 824 | `/problems/2/complaints/0/combos/0/name` | `name` |  | string | 리프팅기기 + 스킨부스터 |  |
| 825 | `/problems/2/complaints/0/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 826 | `/problems/2/complaints/0/combos/0/combo/0` | `(combo 원소)` | 0 | string | 리프팅기기 |  |
| 827 | `/problems/2/complaints/0/combos/0/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 828 | `/problems/2/complaints/0/combos/0/reason` | `reason` |  | string | 타이트닝 + 재생 |  |
| 829 | `/problems/2/complaints/0/combos/0/evidence` | `evidence` |  | string | 기기 후 2주 뒤 스킨부스터 | OB-S03-03 |
| 830 | `/problems/2/complaints/0/combos/1` | `(combos 원소)` | 1 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 831 | `/problems/2/complaints/0/combos/1/name` | `name` |  | string | 실리프팅 + 리프팅기기 |  |
| 832 | `/problems/2/complaints/0/combos/1/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 833 | `/problems/2/complaints/0/combos/1/combo/0` | `(combo 원소)` | 0 | string | 실리프팅 |  |
| 834 | `/problems/2/complaints/0/combos/1/combo/1` | `(combo 원소)` | 1 | string | 리프팅기기 |  |
| 835 | `/problems/2/complaints/0/combos/1/reason` | `reason` |  | string | 물리적 거상 + 열 타이트닝 |  |
| 836 | `/problems/2/complaints/0/combos/1/evidence` | `evidence` |  | string | 시술 2개월 간격 권장 | OB-S03-03 |
| 837 | `/problems/2/complaints/0/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 838 | `/problems/2/complaints/0/alternatives/0` | `(alternatives 원소)` | 0 | string | 바이오스티뮬레이터로 장기 관리 |  |
| 839 | `/problems/2/complaints/1` | `(complaints 원소)` | 1 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 840 | `/problems/2/complaints/1/cc` | `cc` |  | string | 턱선무너짐 | OB-S03-07 |
| 841 | `/problems/2/complaints/1/cc_detail` | `cc_detail` |  | string | 실리프팅/기기리프팅 |  |
| 842 | `/problems/2/complaints/1/cc_group` | `cc_group` |  | string | 얼굴 쳐짐 |  |
| 843 | `/problems/2/complaints/1/procedures` | `procedures` |  | array[3] | (배열 · 3개) |  |
| 844 | `/problems/2/complaints/1/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) | OB-S03-02 |
| 845 | `/problems/2/complaints/1/procedures/0/name` | `name` |  | string | 리프팅기기 |  |
| 846 | `/problems/2/complaints/1/procedures/0/category` | `category` |  | string | M9 |  |
| 847 | `/problems/2/complaints/1/procedures/0/role` | `role` |  | string | 피부 타이트닝 |  |
| 848 | `/problems/2/complaints/1/procedures/0/products` | `products` |  | array[3] | (배열 · 3개) |  |
| 849 | `/problems/2/complaints/1/procedures/0/products/0` | `(products 원소)` | 0 | string | 울쎄라 |  |
| 850 | `/problems/2/complaints/1/procedures/0/products/1` | `(products 원소)` | 1 | string | 써마지FLX |  |
| 851 | `/problems/2/complaints/1/procedures/0/products/2` | `(products 원소)` | 2 | string | 슈링크유니버스 |  |
| 852 | `/problems/2/complaints/1/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 853 | `/problems/2/complaints/1/procedures/1/name` | `name` |  | string | 실리프팅 |  |
| 854 | `/problems/2/complaints/1/procedures/1/category` | `category` |  | string | M7 |  |
| 855 | `/problems/2/complaints/1/procedures/1/role` | `role` |  | string | 물리적 거상 |  |
| 856 | `/problems/2/complaints/1/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 857 | `/problems/2/complaints/1/procedures/1/products/0` | `(products 원소)` | 0 | string | 민트리프트 |  |
| 858 | `/problems/2/complaints/1/procedures/1/products/1` | `(products 원소)` | 1 | string | 테스리프트 |  |
| 859 | `/problems/2/complaints/1/procedures/2` | `(procedures 원소)` | 2 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 860 | `/problems/2/complaints/1/procedures/2/name` | `name` |  | string | 스킨부스터 |  |
| 861 | `/problems/2/complaints/1/procedures/2/category` | `category` |  | string | M4 |  |
| 862 | `/problems/2/complaints/1/procedures/2/role` | `role` |  | string | 피부 재생 |  |
| 863 | `/problems/2/complaints/1/procedures/2/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 864 | `/problems/2/complaints/1/procedures/2/products/0` | `(products 원소)` | 0 | string | 리쥬란 힐러 |  |
| 865 | `/problems/2/complaints/1/procedures/2/products/1` | `(products 원소)` | 1 | string | 쥬베룩 |  |
| 866 | `/problems/2/complaints/1/combos` | `combos` |  | array[2] | (배열 · 2개) |  |
| 867 | `/problems/2/complaints/1/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 868 | `/problems/2/complaints/1/combos/0/name` | `name` |  | string | 리프팅기기 + 스킨부스터 |  |
| 869 | `/problems/2/complaints/1/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 870 | `/problems/2/complaints/1/combos/0/combo/0` | `(combo 원소)` | 0 | string | 리프팅기기 |  |
| 871 | `/problems/2/complaints/1/combos/0/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 872 | `/problems/2/complaints/1/combos/0/reason` | `reason` |  | string | 타이트닝 + 재생 |  |
| 873 | `/problems/2/complaints/1/combos/0/evidence` | `evidence` |  | string | 기기 후 2주 뒤 스킨부스터 |  |
| 874 | `/problems/2/complaints/1/combos/1` | `(combos 원소)` | 1 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 875 | `/problems/2/complaints/1/combos/1/name` | `name` |  | string | 실리프팅 + 리프팅기기 |  |
| 876 | `/problems/2/complaints/1/combos/1/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 877 | `/problems/2/complaints/1/combos/1/combo/0` | `(combo 원소)` | 0 | string | 실리프팅 |  |
| 878 | `/problems/2/complaints/1/combos/1/combo/1` | `(combo 원소)` | 1 | string | 리프팅기기 |  |
| 879 | `/problems/2/complaints/1/combos/1/reason` | `reason` |  | string | 물리적 거상 + 열 타이트닝 |  |
| 880 | `/problems/2/complaints/1/combos/1/evidence` | `evidence` |  | string | 시술 2개월 간격 권장 |  |
| 881 | `/problems/2/complaints/1/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 882 | `/problems/2/complaints/1/alternatives/0` | `(alternatives 원소)` | 0 | string | 바이오스티뮬레이터로 장기 관리 |  |
| 883 | `/problems/2/complaints/2` | `(complaints 원소)` | 2 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 884 | `/problems/2/complaints/2/cc` | `cc` |  | string | 이중턱 |  |
| 885 | `/problems/2/complaints/2/cc_detail` | `cc_detail` |  | string | 윤곽주사/크라이오/기기리프팅 | OB-S03-04 |
| 886 | `/problems/2/complaints/2/cc_group` | `cc_group` |  | string | 얼굴 쳐짐 |  |
| 887 | `/problems/2/complaints/2/procedures` | `procedures` |  | array[4] | (배열 · 4개) |  |
| 888 | `/problems/2/complaints/2/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) | OB-S03-02 |
| 889 | `/problems/2/complaints/2/procedures/0/name` | `name` |  | string | 리프팅기기 |  |
| 890 | `/problems/2/complaints/2/procedures/0/category` | `category` |  | string | M9 |  |
| 891 | `/problems/2/complaints/2/procedures/0/role` | `role` |  | string | 피부 타이트닝 |  |
| 892 | `/problems/2/complaints/2/procedures/0/products` | `products` |  | array[3] | (배열 · 3개) |  |
| 893 | `/problems/2/complaints/2/procedures/0/products/0` | `(products 원소)` | 0 | string | 울쎄라 |  |
| 894 | `/problems/2/complaints/2/procedures/0/products/1` | `(products 원소)` | 1 | string | 써마지FLX |  |
| 895 | `/problems/2/complaints/2/procedures/0/products/2` | `(products 원소)` | 2 | string | 슈링크유니버스 |  |
| 896 | `/problems/2/complaints/2/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 897 | `/problems/2/complaints/2/procedures/1/name` | `name` |  | string | 실리프팅 |  |
| 898 | `/problems/2/complaints/2/procedures/1/category` | `category` |  | string | M7 |  |
| 899 | `/problems/2/complaints/2/procedures/1/role` | `role` |  | string | 물리적 거상 |  |
| 900 | `/problems/2/complaints/2/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 901 | `/problems/2/complaints/2/procedures/1/products/0` | `(products 원소)` | 0 | string | 민트리프트 |  |
| 902 | `/problems/2/complaints/2/procedures/1/products/1` | `(products 원소)` | 1 | string | 테스리프트 |  |
| 903 | `/problems/2/complaints/2/procedures/2` | `(procedures 원소)` | 2 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 904 | `/problems/2/complaints/2/procedures/2/name` | `name` |  | string | 스킨부스터 |  |
| 905 | `/problems/2/complaints/2/procedures/2/category` | `category` |  | string | M4 |  |
| 906 | `/problems/2/complaints/2/procedures/2/role` | `role` |  | string | 피부 재생 |  |
| 907 | `/problems/2/complaints/2/procedures/2/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 908 | `/problems/2/complaints/2/procedures/2/products/0` | `(products 원소)` | 0 | string | 리쥬란 힐러 |  |
| 909 | `/problems/2/complaints/2/procedures/2/products/1` | `(products 원소)` | 1 | string | 쥬베룩 |  |
| 910 | `/problems/2/complaints/2/procedures/3` | `(procedures 원소)` | 3 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 911 | `/problems/2/complaints/2/procedures/3/name` | `name` |  | string | 크라이오 |  |
| 912 | `/problems/2/complaints/2/procedures/3/category` | `category` |  | string | M14 |  |
| 913 | `/problems/2/complaints/2/procedures/3/role` | `role` |  | string | 지방 감소 |  |
| 914 | `/problems/2/complaints/2/procedures/3/products` | `products` |  | array[0] | `[]` (빈 배열) |  |
| 915 | `/problems/2/complaints/2/combos` | `combos` |  | array[3] | (배열 · 3개) |  |
| 916 | `/problems/2/complaints/2/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 917 | `/problems/2/complaints/2/combos/0/name` | `name` |  | string | 리프팅기기 + 스킨부스터 |  |
| 918 | `/problems/2/complaints/2/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 919 | `/problems/2/complaints/2/combos/0/combo/0` | `(combo 원소)` | 0 | string | 리프팅기기 |  |
| 920 | `/problems/2/complaints/2/combos/0/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 921 | `/problems/2/complaints/2/combos/0/reason` | `reason` |  | string | 타이트닝 + 재생 |  |
| 922 | `/problems/2/complaints/2/combos/0/evidence` | `evidence` |  | string | 기기 후 2주 뒤 스킨부스터 |  |
| 923 | `/problems/2/complaints/2/combos/1` | `(combos 원소)` | 1 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 924 | `/problems/2/complaints/2/combos/1/name` | `name` |  | string | 실리프팅 + 리프팅기기 |  |
| 925 | `/problems/2/complaints/2/combos/1/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 926 | `/problems/2/complaints/2/combos/1/combo/0` | `(combo 원소)` | 0 | string | 실리프팅 |  |
| 927 | `/problems/2/complaints/2/combos/1/combo/1` | `(combo 원소)` | 1 | string | 리프팅기기 |  |
| 928 | `/problems/2/complaints/2/combos/1/reason` | `reason` |  | string | 물리적 거상 + 열 타이트닝 |  |
| 929 | `/problems/2/complaints/2/combos/1/evidence` | `evidence` |  | string | 시술 2개월 간격 권장 |  |
| 930 | `/problems/2/complaints/2/combos/2` | `(combos 원소)` | 2 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 931 | `/problems/2/complaints/2/combos/2/name` | `name` |  | string | 크라이오 + 리프팅기기 |  |
| 932 | `/problems/2/complaints/2/combos/2/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 933 | `/problems/2/complaints/2/combos/2/combo/0` | `(combo 원소)` | 0 | string | 크라이오 |  |
| 934 | `/problems/2/complaints/2/combos/2/combo/1` | `(combo 원소)` | 1 | string | 리프팅기기 |  |
| 935 | `/problems/2/complaints/2/combos/2/reason` | `reason` |  | string | 지방감소 + 타이트닝 |  |
| 936 | `/problems/2/complaints/2/combos/2/evidence` | `evidence` |  | string | 이중턱 원인(지방) 해결 | OB-S03-06 |
| 937 | `/problems/2/complaints/2/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 938 | `/problems/2/complaints/2/alternatives/0` | `(alternatives 원소)` | 0 | string | 바이오스티뮬레이터로 장기 관리 |  |
| 939 | `/problems/2/complaints/3` | `(complaints 원소)` | 3 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 940 | `/problems/2/complaints/3/cc` | `cc` |  | string | 눈꺼풀쳐짐 |  |
| 941 | `/problems/2/complaints/3/cc_detail` | `cc_detail` |  | string | 기기리프팅/실리프팅 |  |
| 942 | `/problems/2/complaints/3/cc_group` | `cc_group` |  | string | 눈가 쳐짐 |  |
| 943 | `/problems/2/complaints/3/procedures` | `procedures` |  | array[3] | (배열 · 3개) |  |
| 944 | `/problems/2/complaints/3/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) | OB-S03-02 |
| 945 | `/problems/2/complaints/3/procedures/0/name` | `name` |  | string | 리프팅기기 |  |
| 946 | `/problems/2/complaints/3/procedures/0/category` | `category` |  | string | M9 |  |
| 947 | `/problems/2/complaints/3/procedures/0/role` | `role` |  | string | 피부 타이트닝 |  |
| 948 | `/problems/2/complaints/3/procedures/0/products` | `products` |  | array[3] | (배열 · 3개) |  |
| 949 | `/problems/2/complaints/3/procedures/0/products/0` | `(products 원소)` | 0 | string | 울쎄라 |  |
| 950 | `/problems/2/complaints/3/procedures/0/products/1` | `(products 원소)` | 1 | string | 써마지FLX |  |
| 951 | `/problems/2/complaints/3/procedures/0/products/2` | `(products 원소)` | 2 | string | 슈링크유니버스 |  |
| 952 | `/problems/2/complaints/3/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 953 | `/problems/2/complaints/3/procedures/1/name` | `name` |  | string | 실리프팅 |  |
| 954 | `/problems/2/complaints/3/procedures/1/category` | `category` |  | string | M7 |  |
| 955 | `/problems/2/complaints/3/procedures/1/role` | `role` |  | string | 물리적 거상 |  |
| 956 | `/problems/2/complaints/3/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 957 | `/problems/2/complaints/3/procedures/1/products/0` | `(products 원소)` | 0 | string | 민트리프트 |  |
| 958 | `/problems/2/complaints/3/procedures/1/products/1` | `(products 원소)` | 1 | string | 테스리프트 |  |
| 959 | `/problems/2/complaints/3/procedures/2` | `(procedures 원소)` | 2 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 960 | `/problems/2/complaints/3/procedures/2/name` | `name` |  | string | 스킨부스터 |  |
| 961 | `/problems/2/complaints/3/procedures/2/category` | `category` |  | string | M4 |  |
| 962 | `/problems/2/complaints/3/procedures/2/role` | `role` |  | string | 피부 재생 |  |
| 963 | `/problems/2/complaints/3/procedures/2/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 964 | `/problems/2/complaints/3/procedures/2/products/0` | `(products 원소)` | 0 | string | 리쥬란 힐러 |  |
| 965 | `/problems/2/complaints/3/procedures/2/products/1` | `(products 원소)` | 1 | string | 쥬베룩 |  |
| 966 | `/problems/2/complaints/3/combos` | `combos` |  | array[2] | (배열 · 2개) |  |
| 967 | `/problems/2/complaints/3/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 968 | `/problems/2/complaints/3/combos/0/name` | `name` |  | string | 리프팅기기 + 스킨부스터 |  |
| 969 | `/problems/2/complaints/3/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 970 | `/problems/2/complaints/3/combos/0/combo/0` | `(combo 원소)` | 0 | string | 리프팅기기 |  |
| 971 | `/problems/2/complaints/3/combos/0/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 972 | `/problems/2/complaints/3/combos/0/reason` | `reason` |  | string | 타이트닝 + 재생 |  |
| 973 | `/problems/2/complaints/3/combos/0/evidence` | `evidence` |  | string | 기기 후 2주 뒤 스킨부스터 |  |
| 974 | `/problems/2/complaints/3/combos/1` | `(combos 원소)` | 1 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 975 | `/problems/2/complaints/3/combos/1/name` | `name` |  | string | 실리프팅 + 리프팅기기 |  |
| 976 | `/problems/2/complaints/3/combos/1/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 977 | `/problems/2/complaints/3/combos/1/combo/0` | `(combo 원소)` | 0 | string | 실리프팅 |  |
| 978 | `/problems/2/complaints/3/combos/1/combo/1` | `(combo 원소)` | 1 | string | 리프팅기기 |  |
| 979 | `/problems/2/complaints/3/combos/1/reason` | `reason` |  | string | 물리적 거상 + 열 타이트닝 |  |
| 980 | `/problems/2/complaints/3/combos/1/evidence` | `evidence` |  | string | 시술 2개월 간격 권장 |  |
| 981 | `/problems/2/complaints/3/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 982 | `/problems/2/complaints/3/alternatives/0` | `(alternatives 원소)` | 0 | string | 바이오스티뮬레이터로 장기 관리 |  |
| 983 | `/problems/2/complaints/4` | `(complaints 원소)` | 4 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 984 | `/problems/2/complaints/4/cc` | `cc` |  | string | 팔뚝/복부/허벅지 | OB-S03-05 |
| 985 | `/problems/2/complaints/4/cc_detail` | `cc_detail` |  | string | 바디리프팅 기기 |  |
| 986 | `/problems/2/complaints/4/cc_group` | `cc_group` |  | string | 바디 쳐짐 |  |
| 987 | `/problems/2/complaints/4/procedures` | `procedures` |  | array[3] | (배열 · 3개) |  |
| 988 | `/problems/2/complaints/4/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) | OB-S03-02 |
| 989 | `/problems/2/complaints/4/procedures/0/name` | `name` |  | string | 리프팅기기 |  |
| 990 | `/problems/2/complaints/4/procedures/0/category` | `category` |  | string | M9 |  |
| 991 | `/problems/2/complaints/4/procedures/0/role` | `role` |  | string | 피부 타이트닝 |  |
| 992 | `/problems/2/complaints/4/procedures/0/products` | `products` |  | array[3] | (배열 · 3개) |  |
| 993 | `/problems/2/complaints/4/procedures/0/products/0` | `(products 원소)` | 0 | string | 울쎄라 |  |
| 994 | `/problems/2/complaints/4/procedures/0/products/1` | `(products 원소)` | 1 | string | 써마지FLX |  |
| 995 | `/problems/2/complaints/4/procedures/0/products/2` | `(products 원소)` | 2 | string | 슈링크유니버스 |  |
| 996 | `/problems/2/complaints/4/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 997 | `/problems/2/complaints/4/procedures/1/name` | `name` |  | string | 실리프팅 |  |
| 998 | `/problems/2/complaints/4/procedures/1/category` | `category` |  | string | M7 |  |
| 999 | `/problems/2/complaints/4/procedures/1/role` | `role` |  | string | 물리적 거상 |  |
| 1000 | `/problems/2/complaints/4/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1001 | `/problems/2/complaints/4/procedures/1/products/0` | `(products 원소)` | 0 | string | 민트리프트 |  |
| 1002 | `/problems/2/complaints/4/procedures/1/products/1` | `(products 원소)` | 1 | string | 테스리프트 |  |
| 1003 | `/problems/2/complaints/4/procedures/2` | `(procedures 원소)` | 2 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1004 | `/problems/2/complaints/4/procedures/2/name` | `name` |  | string | 스킨부스터 |  |
| 1005 | `/problems/2/complaints/4/procedures/2/category` | `category` |  | string | M4 |  |
| 1006 | `/problems/2/complaints/4/procedures/2/role` | `role` |  | string | 피부 재생 |  |
| 1007 | `/problems/2/complaints/4/procedures/2/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1008 | `/problems/2/complaints/4/procedures/2/products/0` | `(products 원소)` | 0 | string | 리쥬란 힐러 |  |
| 1009 | `/problems/2/complaints/4/procedures/2/products/1` | `(products 원소)` | 1 | string | 쥬베룩 |  |
| 1010 | `/problems/2/complaints/4/combos` | `combos` |  | array[2] | (배열 · 2개) |  |
| 1011 | `/problems/2/complaints/4/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 1012 | `/problems/2/complaints/4/combos/0/name` | `name` |  | string | 리프팅기기 + 스킨부스터 |  |
| 1013 | `/problems/2/complaints/4/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 1014 | `/problems/2/complaints/4/combos/0/combo/0` | `(combo 원소)` | 0 | string | 리프팅기기 |  |
| 1015 | `/problems/2/complaints/4/combos/0/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 1016 | `/problems/2/complaints/4/combos/0/reason` | `reason` |  | string | 타이트닝 + 재생 |  |
| 1017 | `/problems/2/complaints/4/combos/0/evidence` | `evidence` |  | string | 기기 후 2주 뒤 스킨부스터 |  |
| 1018 | `/problems/2/complaints/4/combos/1` | `(combos 원소)` | 1 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 1019 | `/problems/2/complaints/4/combos/1/name` | `name` |  | string | 실리프팅 + 리프팅기기 |  |
| 1020 | `/problems/2/complaints/4/combos/1/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 1021 | `/problems/2/complaints/4/combos/1/combo/0` | `(combo 원소)` | 0 | string | 실리프팅 |  |
| 1022 | `/problems/2/complaints/4/combos/1/combo/1` | `(combo 원소)` | 1 | string | 리프팅기기 |  |
| 1023 | `/problems/2/complaints/4/combos/1/reason` | `reason` |  | string | 물리적 거상 + 열 타이트닝 |  |
| 1024 | `/problems/2/complaints/4/combos/1/evidence` | `evidence` |  | string | 시술 2개월 간격 권장 |  |
| 1025 | `/problems/2/complaints/4/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 1026 | `/problems/2/complaints/4/alternatives/0` | `(alternatives 원소)` | 0 | string | 바이오스티뮬레이터로 장기 관리 |  |

## 잠정 관찰 (원문 칸과 분리)

| ID | 상태 | 위치 | 관찰 |
|---|---|---|---|
| OB-S03-01 | P | `/problems/2/problem`<br>`/problems/1/complaints/3/combos/1/evidence` | problem 값 '쳐짐' 과 S02 evidence 의 '처짐 원인까지 해결' — 같은 증상으로 보이는 말이 두 표기로 나온다. 표기 통일 여부는 판단하지 않는다(F-07). |
| OB-S03-02 | P | `/problems/2/complaints/0/procedures/0`<br>`/problems/2/complaints/1/procedures/0`<br>`/problems/2/complaints/2/procedures/0`<br>`/problems/2/complaints/3/procedures/0`<br>`/problems/2/complaints/4/procedures/0` | 다섯 complaint 가 procedures 0~2(리프팅기기·실리프팅·스킨부스터)·products·combos 0~1·alternatives 를 글자 그대로 공유한다. c4 는 cc '팔뚝/복부/허벅지'·cc_group '바디 쳐짐'·cc_detail '바디리프팅 기기' 인데 procedures·products 가 얼굴 complaint 와 같다. 부위별 차이 정보가 원문에 없다(B-02). |
| OB-S03-03 | P | `/problems/2/complaints/0/combos/0/evidence`<br>`/problems/2/complaints/0/combos/1/evidence` | evidence 칸에 근거가 아니라 순서·간격 지시가 들어 있다: '기기 후 2주 뒤 스킨부스터', '시술 2개월 간격 권장'. '2개월 간격' 이 어느 시술 사이 간격인지 문장 안에 대상이 없다(B-06 · F-06). |
| OB-S03-04 | I | `/problems/2/complaints/2/cc_detail` | cc_detail '윤곽주사/크라이오/기기리프팅' 중 '윤곽주사' 는 c2 procedures 에 없다(I-03 같은 유형). |
| OB-S03-05 | P | `/problems/2/complaints/0/cc`<br>`/problems/2/complaints/4/cc` | cc 값 안에도 '/' 가 쓰였다: '볼쳐짐/불독살'(증상 둘), '팔뚝/복부/허벅지'(부위 셋). |
| OB-S03-06 | P | `/problems/2/complaints/2/combos/2/evidence` | '이중턱 원인(지방) 해결' — 괄호로 원인을 보충한다. 괄호 안 '지방' 이 원인이라는 원문 단정이며, 임상 사실로 승인하지 않는다. |
| OB-S03-07 | K | `/problems/2/complaints/1/cc` | '턱선무너짐' 붙여 쓴 복합 증상 표현. 형태소 분절 확인(K-02). |

## 수동 복합 표현 (직접 읽기 · 출현별)

| 표현 | 위치(Pointer · 값 내 구간) | 관점(탐색용, 확정 분류 아님) |
|---|---|---|
| 볼쳐짐/불독살 | `/problems/2/complaints/0/cc` [0,7) | 증상 표현, 기호(/) |
| 턱선무너짐 | `/problems/2/complaints/1/cc` [0,5) | 부위+증상 표현, 붙여 쓴 복합어 |
| 팔뚝/복부/허벅지 | `/problems/2/complaints/4/cc` [0,9) | 부위 표현, 기호(/) |
| 기기리프팅/실리프팅 | `/problems/2/complaints/0/cc_detail` [0,10)<br>`/problems/2/complaints/3/cc_detail` [0,10) | 시술명 표현, 기호(/) |
| 실리프팅/기기리프팅 | `/problems/2/complaints/1/cc_detail` [0,10) | 시술명 표현, 기호(/), 나열 순서 차이 |
| 윤곽주사/크라이오/기기리프팅 | `/problems/2/complaints/2/cc_detail` [0,15) | 시술명 표현, 기호(/) |
| 바디리프팅 기기 | `/problems/2/complaints/4/cc_detail` [0,8) | 시술명 표현, 부위 수식(바디) |
| 얼굴 쳐짐 | `/problems/2/complaints/0/cc_group` [0,5)<br>`/problems/2/complaints/1/cc_group` [0,5)<br>`/problems/2/complaints/2/cc_group` [0,5) | 부위+증상 표현 |
| 눈가 쳐짐 | `/problems/2/complaints/3/cc_group` [0,5) | 부위+증상 표현 |
| 바디 쳐짐 | `/problems/2/complaints/4/cc_group` [0,5) | 부위+증상 표현 |
| 타이트닝 + 재생 | `/problems/2/complaints/0/combos/0/reason` [0,9)<br>`/problems/2/complaints/1/combos/0/reason` [0,9)<br>`/problems/2/complaints/2/combos/0/reason` [0,9)<br>`/problems/2/complaints/3/combos/0/reason` [0,9)<br>`/problems/2/complaints/4/combos/0/reason` [0,9) | 기호(+), 결과 없는 공식형 |
| 기기 후 2주 뒤 스킨부스터 | `/problems/2/complaints/0/combos/0/evidence` [0,15)<br>`/problems/2/complaints/1/combos/0/evidence` [0,15)<br>`/problems/2/complaints/2/combos/0/evidence` [0,15)<br>`/problems/2/complaints/3/combos/0/evidence` [0,15)<br>`/problems/2/complaints/4/combos/0/evidence` [0,15) | 시간 순서(후·뒤), 수량·단위·시간, 순서 지시 |
| 2주 뒤 | `/problems/2/complaints/0/combos/0/evidence` [5,9)<br>`/problems/2/complaints/1/combos/0/evidence` [5,9)<br>`/problems/2/complaints/2/combos/0/evidence` [5,9)<br>`/problems/2/complaints/3/combos/0/evidence` [5,9)<br>`/problems/2/complaints/4/combos/0/evidence` [5,9) | 수량·단위·시간, 시간 순서(뒤) |
| 물리적 거상 + 열 타이트닝 | `/problems/2/complaints/0/combos/1/reason` [0,15)<br>`/problems/2/complaints/1/combos/1/reason` [0,15)<br>`/problems/2/complaints/2/combos/1/reason` [0,15)<br>`/problems/2/complaints/3/combos/1/reason` [0,15)<br>`/problems/2/complaints/4/combos/1/reason` [0,15) | 기호(+), 기전 수식(물리적·열) |
| 시술 2개월 간격 권장 | `/problems/2/complaints/0/combos/1/evidence` [0,12)<br>`/problems/2/complaints/1/combos/1/evidence` [0,12)<br>`/problems/2/complaints/2/combos/1/evidence` [0,12)<br>`/problems/2/complaints/3/combos/1/evidence` [0,12)<br>`/problems/2/complaints/4/combos/1/evidence` [0,12) | 수량·단위·시간, 간격, 권고(권장), 대상 생략 |
| 지방감소 + 타이트닝 | `/problems/2/complaints/2/combos/2/reason` [0,11) | 기호(+), 감소 표현 |
| 이중턱 원인(지방) 해결 | `/problems/2/complaints/2/combos/2/evidence` [0,13) | 원인 표현, 괄호 보충, 효과 강도(해결) |
| 지방 감소 | `/problems/2/complaints/2/procedures/3/role` [0,5) | role 표현, 감소 표현 |
| 바이오스티뮬레이터로 장기 관리 | `/problems/2/complaints/0/alternatives/0` [0,16)<br>`/problems/2/complaints/1/alternatives/0` [0,16)<br>`/problems/2/complaints/2/alternatives/0` [0,16)<br>`/problems/2/complaints/3/alternatives/0` [0,16)<br>`/problems/2/complaints/4/alternatives/0` [0,16) | 시술명 표현, 기간 표현(장기) |

## 이 구획에서 연 미결

- **B-06** (B) '시술 2개월 간격 권장' 에 간격의 앞뒤 시술이 명시되지 않았다(combo 실리프팅 + 리프팅기기 문맥만 있음). 순서도 없다. — 영향: 간격 규칙의 대상·방향을 확정할 수 없다.
- **F-06** (F) combos.evidence 에 근거 진술·기전·순서/간격 지시·시술자 요건 등 정보 종류가 섞여 있다. — 영향: evidence 를 '근거' 칸으로만 쓰면 일정 지시가 근거로 오분류된다.
- **F-07** (F) '쳐짐' / '처짐' 두 표기 공존(problem·cc_group 은 '쳐짐', evidence 는 '처짐'). — 영향: 문자열 일치 기반 연결에서 갈라진다. 표기 통일은 후속 결정 후보이며 지금 원본을 바꾸지 않는다.
