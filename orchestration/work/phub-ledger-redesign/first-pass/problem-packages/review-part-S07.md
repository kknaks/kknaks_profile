# S07 — /problems/6 P7 모공

[← review.md](review.md) · 범위 /problems/6 및 /problems/6/** 전체 · 소유 노드 223 · 말단 147 · 빈 값 0 · 직접 읽기 done

상위 문맥(공유, S00 소유): 루트 객체 → `/description` = taxonomy P1~P14 하위구조 기반 CC 자동 생성 → `/problems` 배열.

직접 읽기: reading/S07.txt 로 c0~c5 전부(procedures 15·combos 8·alternatives 7) 읽음.

## 원문 값 (문서 순서 · 전부)

| # | JSON Pointer | 원본 컬럼명 | 배열 순번 | 자료형 | 원문 값 | 관찰 참조 |
|---|---|---|---|---|---|---|
| 1764 | `/problems/6` | `(problems 원소)` | 6 | object{3} | (객체 · 키: `problem_id`, `problem`, `complaints`) |  |
| 1765 | `/problems/6/problem_id` | `problem_id` |  | string | P7 |  |
| 1766 | `/problems/6/problem` | `problem` |  | string | 모공 |  |
| 1767 | `/problems/6/complaints` | `complaints` |  | array[6] | (배열 · 6개) |  |
| 1768 | `/problems/6/complaints/0` | `(complaints 원소)` | 0 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 1769 | `/problems/6/complaints/0/cc` | `cc` |  | string | 스킨보톡스 | OB-S00-06, OB-S07-06 |
| 1770 | `/problems/6/complaints/0/cc_detail` | `cc_detail` |  | string | 피지↓ |  |
| 1771 | `/problems/6/complaints/0/cc_group` | `cc_group` |  | string | 피지과다형 |  |
| 1772 | `/problems/6/complaints/0/procedures` | `procedures` |  | array[4] | (배열 · 4개) |  |
| 1773 | `/problems/6/complaints/0/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1774 | `/problems/6/complaints/0/procedures/0/name` | `name` |  | string | 보톡스 |  |
| 1775 | `/problems/6/complaints/0/procedures/0/category` | `category` |  | string | M1 |  |
| 1776 | `/problems/6/complaints/0/procedures/0/role` | `role` |  | string | 진피내 피지선·입모근의 콜린성 신호 차단 |  |
| 1777 | `/problems/6/complaints/0/procedures/0/products` | `products` |  | array[3] | (배열 · 3개) |  |
| 1778 | `/problems/6/complaints/0/procedures/0/products/0` | `(products 원소)` | 0 | string | 보톡스 |  |
| 1779 | `/problems/6/complaints/0/procedures/0/products/1` | `(products 원소)` | 1 | string | 나보타 |  |
| 1780 | `/problems/6/complaints/0/procedures/0/products/2` | `(products 원소)` | 2 | string | 보툴렉스 |  |
| 1781 | `/problems/6/complaints/0/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) | OB-S07-01 |
| 1782 | `/problems/6/complaints/0/procedures/1/name` | `name` |  | string | 스킨부스터 |  |
| 1783 | `/problems/6/complaints/0/procedures/1/category` | `category` |  | string | M4 |  |
| 1784 | `/problems/6/complaints/0/procedures/1/role` | `role` |  | string | 피부 재생 |  |
| 1785 | `/problems/6/complaints/0/procedures/1/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1786 | `/problems/6/complaints/0/procedures/1/products/0` | `(products 원소)` | 0 | string | 리쥬란 HB+ |  |
| 1787 | `/problems/6/complaints/0/procedures/1/products/1` | `(products 원소)` | 1 | string | 쥬베룩 |  |
| 1788 | `/problems/6/complaints/0/procedures/2` | `(procedures 원소)` | 2 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1789 | `/problems/6/complaints/0/procedures/2/name` | `name` |  | string | 니들RF |  |
| 1790 | `/problems/6/complaints/0/procedures/2/category` | `category` |  | string | M11 |  |
| 1791 | `/problems/6/complaints/0/procedures/2/role` | `role` |  | string | 모공 수축 |  |
| 1792 | `/problems/6/complaints/0/procedures/2/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1793 | `/problems/6/complaints/0/procedures/2/products/0` | `(products 원소)` | 0 | string | 포텐자 |  |
| 1794 | `/problems/6/complaints/0/procedures/2/products/1` | `(products 원소)` | 1 | string | 시크릿 |  |
| 1795 | `/problems/6/complaints/0/procedures/3` | `(procedures 원소)` | 3 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) | OB-S07-01 |
| 1796 | `/problems/6/complaints/0/procedures/3/name` | `name` |  | string | 스킨부스터 |  |
| 1797 | `/problems/6/complaints/0/procedures/3/category` | `category` |  | string | M4 |  |
| 1798 | `/problems/6/complaints/0/procedures/3/role` | `role` |  | string | 콜라겐 재생 |  |
| 1799 | `/problems/6/complaints/0/procedures/3/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 1800 | `/problems/6/complaints/0/procedures/3/products/0` | `(products 원소)` | 0 | string | 쥬베룩 |  |
| 1801 | `/problems/6/complaints/0/combos` | `combos` |  | array[2] | (배열 · 2개) |  |
| 1802 | `/problems/6/complaints/0/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 1803 | `/problems/6/complaints/0/combos/0/name` | `name` |  | string | 보톡스 + 스킨부스터 |  |
| 1804 | `/problems/6/complaints/0/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 1805 | `/problems/6/complaints/0/combos/0/combo/0` | `(combo 원소)` | 0 | string | 보톡스 |  |
| 1806 | `/problems/6/complaints/0/combos/0/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 1807 | `/problems/6/complaints/0/combos/0/reason` | `reason` |  | string | 마이크로보톡스로 피지·모공 감소 + 스킨부스터로 피부 재생 보조 |  |
| 1808 | `/problems/6/complaints/0/combos/0/evidence` | `evidence` |  | string | 마이크로보톡스는 피지선의 콜린성 신호 차단으로 피지·모공을 감소시킴 |  |
| 1809 | `/problems/6/complaints/0/combos/1` | `(combos 원소)` | 1 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 1810 | `/problems/6/complaints/0/combos/1/name` | `name` |  | string | 니들RF + 스킨부스터 |  |
| 1811 | `/problems/6/complaints/0/combos/1/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 1812 | `/problems/6/complaints/0/combos/1/combo/0` | `(combo 원소)` | 0 | string | 니들RF |  |
| 1813 | `/problems/6/complaints/0/combos/1/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 1814 | `/problems/6/complaints/0/combos/1/reason` | `reason` |  | string | 열 수축 + 콜라겐 재생 | OB-S07-02 |
| 1815 | `/problems/6/complaints/0/combos/1/evidence` | `evidence` |  | string | 쥬베룩 PDLLA가 모공에 특화 | OB-S07-02 |
| 1816 | `/problems/6/complaints/0/alternatives` | `alternatives` |  | array[2] | (배열 · 2개) |  |
| 1817 | `/problems/6/complaints/0/alternatives/0` | `(alternatives 원소)` | 0 | string | 효과 부족 시 리프팅기기 추가 |  |
| 1818 | `/problems/6/complaints/0/alternatives/1` | `(alternatives 원소)` | 1 | string | MTS + 스킨부스터도 가벼운 대안 | OB-S07-03 |
| 1819 | `/problems/6/complaints/1` | `(complaints 원소)` | 1 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 1820 | `/problems/6/complaints/1/cc` | `cc` |  | string | 아그네스 | OB-S00-06, OB-S07-06 |
| 1821 | `/problems/6/complaints/1/cc_detail` | `cc_detail` |  | string | 피지선 파괴 |  |
| 1822 | `/problems/6/complaints/1/cc_group` | `cc_group` |  | string | 피지과다형 |  |
| 1823 | `/problems/6/complaints/1/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 1824 | `/problems/6/complaints/1/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1825 | `/problems/6/complaints/1/procedures/0/name` | `name` |  | string | 니들RF |  |
| 1826 | `/problems/6/complaints/1/procedures/0/category` | `category` |  | string | M11 |  |
| 1827 | `/problems/6/complaints/1/procedures/0/role` | `role` |  | string | 모공 수축 |  |
| 1828 | `/problems/6/complaints/1/procedures/0/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1829 | `/problems/6/complaints/1/procedures/0/products/0` | `(products 원소)` | 0 | string | 포텐자 |  |
| 1830 | `/problems/6/complaints/1/procedures/0/products/1` | `(products 원소)` | 1 | string | 시크릿 |  |
| 1831 | `/problems/6/complaints/1/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1832 | `/problems/6/complaints/1/procedures/1/name` | `name` |  | string | 스킨부스터 |  |
| 1833 | `/problems/6/complaints/1/procedures/1/category` | `category` |  | string | M4 |  |
| 1834 | `/problems/6/complaints/1/procedures/1/role` | `role` |  | string | 콜라겐 재생 |  |
| 1835 | `/problems/6/complaints/1/procedures/1/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 1836 | `/problems/6/complaints/1/procedures/1/products/0` | `(products 원소)` | 0 | string | 쥬베룩 |  |
| 1837 | `/problems/6/complaints/1/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 1838 | `/problems/6/complaints/1/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 1839 | `/problems/6/complaints/1/combos/0/name` | `name` |  | string | 니들RF + 스킨부스터 |  |
| 1840 | `/problems/6/complaints/1/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 1841 | `/problems/6/complaints/1/combos/0/combo/0` | `(combo 원소)` | 0 | string | 니들RF |  |
| 1842 | `/problems/6/complaints/1/combos/0/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 1843 | `/problems/6/complaints/1/combos/0/reason` | `reason` |  | string | 열 수축 + 콜라겐 재생 |  |
| 1844 | `/problems/6/complaints/1/combos/0/evidence` | `evidence` |  | string | 쥬베룩 PDLLA가 모공에 특화 |  |
| 1845 | `/problems/6/complaints/1/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 1846 | `/problems/6/complaints/1/alternatives/0` | `(alternatives 원소)` | 0 | string | MTS + 스킨부스터도 가벼운 대안 | OB-S07-03 |
| 1847 | `/problems/6/complaints/2` | `(complaints 원소)` | 2 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 1848 | `/problems/6/complaints/2/cc` | `cc` |  | string | 프락셔널레이저 | OB-S00-06, OB-S07-04 |
| 1849 | `/problems/6/complaints/2/cc_detail` | `cc_detail` |  | string | 콜라겐리모델링 |  |
| 1850 | `/problems/6/complaints/2/cc_group` | `cc_group` |  | string | 탄력저하형 |  |
| 1851 | `/problems/6/complaints/2/procedures` | `procedures` |  | array[3] | (배열 · 3개) |  |
| 1852 | `/problems/6/complaints/2/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1853 | `/problems/6/complaints/2/procedures/0/name` | `name` |  | string | 니들RF |  |
| 1854 | `/problems/6/complaints/2/procedures/0/category` | `category` |  | string | M11 |  |
| 1855 | `/problems/6/complaints/2/procedures/0/role` | `role` |  | string | 모공 수축 |  |
| 1856 | `/problems/6/complaints/2/procedures/0/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1857 | `/problems/6/complaints/2/procedures/0/products/0` | `(products 원소)` | 0 | string | 포텐자 |  |
| 1858 | `/problems/6/complaints/2/procedures/0/products/1` | `(products 원소)` | 1 | string | 시크릿 |  |
| 1859 | `/problems/6/complaints/2/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1860 | `/problems/6/complaints/2/procedures/1/name` | `name` |  | string | 스킨부스터 |  |
| 1861 | `/problems/6/complaints/2/procedures/1/category` | `category` |  | string | M4 |  |
| 1862 | `/problems/6/complaints/2/procedures/1/role` | `role` |  | string | 콜라겐 재생 |  |
| 1863 | `/problems/6/complaints/2/procedures/1/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 1864 | `/problems/6/complaints/2/procedures/1/products/0` | `(products 원소)` | 0 | string | 쥬베룩 |  |
| 1865 | `/problems/6/complaints/2/procedures/2` | `(procedures 원소)` | 2 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1866 | `/problems/6/complaints/2/procedures/2/name` | `name` |  | string | 리프팅기기 |  |
| 1867 | `/problems/6/complaints/2/procedures/2/category` | `category` |  | string | M9 |  |
| 1868 | `/problems/6/complaints/2/procedures/2/role` | `role` |  | string | 처짐 개선 | OB-S07-05 |
| 1869 | `/problems/6/complaints/2/procedures/2/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1870 | `/problems/6/complaints/2/procedures/2/products/0` | `(products 원소)` | 0 | string | 울쎄라 |  |
| 1871 | `/problems/6/complaints/2/procedures/2/products/1` | `(products 원소)` | 1 | string | 써마지FLX |  |
| 1872 | `/problems/6/complaints/2/combos` | `combos` |  | array[2] | (배열 · 2개) |  |
| 1873 | `/problems/6/complaints/2/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 1874 | `/problems/6/complaints/2/combos/0/name` | `name` |  | string | 니들RF + 스킨부스터 |  |
| 1875 | `/problems/6/complaints/2/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 1876 | `/problems/6/complaints/2/combos/0/combo/0` | `(combo 원소)` | 0 | string | 니들RF |  |
| 1877 | `/problems/6/complaints/2/combos/0/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 1878 | `/problems/6/complaints/2/combos/0/reason` | `reason` |  | string | 열 수축 + 콜라겐 재생 |  |
| 1879 | `/problems/6/complaints/2/combos/0/evidence` | `evidence` |  | string | 쥬베룩 PDLLA가 모공에 특화 |  |
| 1880 | `/problems/6/complaints/2/combos/1` | `(combos 원소)` | 1 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 1881 | `/problems/6/complaints/2/combos/1/name` | `name` |  | string | 니들RF + 리프팅기기 |  |
| 1882 | `/problems/6/complaints/2/combos/1/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 1883 | `/problems/6/complaints/2/combos/1/combo/0` | `(combo 원소)` | 0 | string | 니들RF |  |
| 1884 | `/problems/6/complaints/2/combos/1/combo/1` | `(combo 원소)` | 1 | string | 리프팅기기 |  |
| 1885 | `/problems/6/complaints/2/combos/1/reason` | `reason` |  | string | 수축 + 리프팅 = 처진 모공 해결 | OB-S07-05 |
| 1886 | `/problems/6/complaints/2/combos/1/evidence` | `evidence` |  | string | 원인(처짐)+결과(모공) 동시 치료 | OB-S07-05 |
| 1887 | `/problems/6/complaints/2/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 1888 | `/problems/6/complaints/2/alternatives/0` | `(alternatives 원소)` | 0 | string | MTS + 스킨부스터도 가벼운 대안 | OB-S07-03 |
| 1889 | `/problems/6/complaints/3` | `(complaints 원소)` | 3 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 1890 | `/problems/6/complaints/3/cc` | `cc` |  | string | 니들RF | OB-S00-06 |
| 1891 | `/problems/6/complaints/3/cc_detail` | `cc_detail` |  | string | 진피 타이트닝 |  |
| 1892 | `/problems/6/complaints/3/cc_group` | `cc_group` |  | string | 탄력저하형 |  |
| 1893 | `/problems/6/complaints/3/procedures` | `procedures` |  | array[3] | (배열 · 3개) |  |
| 1894 | `/problems/6/complaints/3/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1895 | `/problems/6/complaints/3/procedures/0/name` | `name` |  | string | 니들RF |  |
| 1896 | `/problems/6/complaints/3/procedures/0/category` | `category` |  | string | M11 |  |
| 1897 | `/problems/6/complaints/3/procedures/0/role` | `role` |  | string | 모공 수축 |  |
| 1898 | `/problems/6/complaints/3/procedures/0/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1899 | `/problems/6/complaints/3/procedures/0/products/0` | `(products 원소)` | 0 | string | 포텐자 |  |
| 1900 | `/problems/6/complaints/3/procedures/0/products/1` | `(products 원소)` | 1 | string | 시크릿 |  |
| 1901 | `/problems/6/complaints/3/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1902 | `/problems/6/complaints/3/procedures/1/name` | `name` |  | string | 스킨부스터 |  |
| 1903 | `/problems/6/complaints/3/procedures/1/category` | `category` |  | string | M4 |  |
| 1904 | `/problems/6/complaints/3/procedures/1/role` | `role` |  | string | 콜라겐 재생 |  |
| 1905 | `/problems/6/complaints/3/procedures/1/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 1906 | `/problems/6/complaints/3/procedures/1/products/0` | `(products 원소)` | 0 | string | 쥬베룩 |  |
| 1907 | `/problems/6/complaints/3/procedures/2` | `(procedures 원소)` | 2 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1908 | `/problems/6/complaints/3/procedures/2/name` | `name` |  | string | 리프팅기기 |  |
| 1909 | `/problems/6/complaints/3/procedures/2/category` | `category` |  | string | M9 |  |
| 1910 | `/problems/6/complaints/3/procedures/2/role` | `role` |  | string | 처짐 개선 |  |
| 1911 | `/problems/6/complaints/3/procedures/2/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1912 | `/problems/6/complaints/3/procedures/2/products/0` | `(products 원소)` | 0 | string | 울쎄라 |  |
| 1913 | `/problems/6/complaints/3/procedures/2/products/1` | `(products 원소)` | 1 | string | 써마지FLX |  |
| 1914 | `/problems/6/complaints/3/combos` | `combos` |  | array[2] | (배열 · 2개) |  |
| 1915 | `/problems/6/complaints/3/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 1916 | `/problems/6/complaints/3/combos/0/name` | `name` |  | string | 니들RF + 스킨부스터 |  |
| 1917 | `/problems/6/complaints/3/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 1918 | `/problems/6/complaints/3/combos/0/combo/0` | `(combo 원소)` | 0 | string | 니들RF |  |
| 1919 | `/problems/6/complaints/3/combos/0/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 1920 | `/problems/6/complaints/3/combos/0/reason` | `reason` |  | string | 열 수축 + 콜라겐 재생 |  |
| 1921 | `/problems/6/complaints/3/combos/0/evidence` | `evidence` |  | string | 쥬베룩 PDLLA가 모공에 특화 |  |
| 1922 | `/problems/6/complaints/3/combos/1` | `(combos 원소)` | 1 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 1923 | `/problems/6/complaints/3/combos/1/name` | `name` |  | string | 니들RF + 리프팅기기 |  |
| 1924 | `/problems/6/complaints/3/combos/1/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 1925 | `/problems/6/complaints/3/combos/1/combo/0` | `(combo 원소)` | 0 | string | 니들RF |  |
| 1926 | `/problems/6/complaints/3/combos/1/combo/1` | `(combo 원소)` | 1 | string | 리프팅기기 |  |
| 1927 | `/problems/6/complaints/3/combos/1/reason` | `reason` |  | string | 수축 + 리프팅 = 처진 모공 해결 |  |
| 1928 | `/problems/6/complaints/3/combos/1/evidence` | `evidence` |  | string | 원인(처짐)+결과(모공) 동시 치료 |  |
| 1929 | `/problems/6/complaints/3/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 1930 | `/problems/6/complaints/3/alternatives/0` | `(alternatives 원소)` | 0 | string | MTS + 스킨부스터도 가벼운 대안 | OB-S07-03 |
| 1931 | `/problems/6/complaints/4` | `(complaints 원소)` | 4 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 1932 | `/problems/6/complaints/4/cc` | `cc` |  | string | CO2프락셀 | OB-S07-04, OB-S07-07 |
| 1933 | `/problems/6/complaints/4/cc_detail` | `cc_detail` |  | string | 박피성 재생 |  |
| 1934 | `/problems/6/complaints/4/cc_group` | `cc_group` |  | string | 흉터형(열린모공) |  |
| 1935 | `/problems/6/complaints/4/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 1936 | `/problems/6/complaints/4/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1937 | `/problems/6/complaints/4/procedures/0/name` | `name` |  | string | 니들RF |  |
| 1938 | `/problems/6/complaints/4/procedures/0/category` | `category` |  | string | M11 |  |
| 1939 | `/problems/6/complaints/4/procedures/0/role` | `role` |  | string | 모공 수축 |  |
| 1940 | `/problems/6/complaints/4/procedures/0/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1941 | `/problems/6/complaints/4/procedures/0/products/0` | `(products 원소)` | 0 | string | 포텐자 |  |
| 1942 | `/problems/6/complaints/4/procedures/0/products/1` | `(products 원소)` | 1 | string | 시크릿 |  |
| 1943 | `/problems/6/complaints/4/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1944 | `/problems/6/complaints/4/procedures/1/name` | `name` |  | string | 스킨부스터 |  |
| 1945 | `/problems/6/complaints/4/procedures/1/category` | `category` |  | string | M4 |  |
| 1946 | `/problems/6/complaints/4/procedures/1/role` | `role` |  | string | 콜라겐 재생 |  |
| 1947 | `/problems/6/complaints/4/procedures/1/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 1948 | `/problems/6/complaints/4/procedures/1/products/0` | `(products 원소)` | 0 | string | 쥬베룩 |  |
| 1949 | `/problems/6/complaints/4/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 1950 | `/problems/6/complaints/4/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 1951 | `/problems/6/complaints/4/combos/0/name` | `name` |  | string | 니들RF + 스킨부스터 |  |
| 1952 | `/problems/6/complaints/4/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 1953 | `/problems/6/complaints/4/combos/0/combo/0` | `(combo 원소)` | 0 | string | 니들RF |  |
| 1954 | `/problems/6/complaints/4/combos/0/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 1955 | `/problems/6/complaints/4/combos/0/reason` | `reason` |  | string | 열 수축 + 콜라겐 재생 |  |
| 1956 | `/problems/6/complaints/4/combos/0/evidence` | `evidence` |  | string | 쥬베룩 PDLLA가 모공에 특화 |  |
| 1957 | `/problems/6/complaints/4/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 1958 | `/problems/6/complaints/4/alternatives/0` | `(alternatives 원소)` | 0 | string | MTS + 스킨부스터도 가벼운 대안 | OB-S07-03 |
| 1959 | `/problems/6/complaints/5` | `(complaints 원소)` | 5 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 1960 | `/problems/6/complaints/5/cc` | `cc` |  | string | 서브시전 | OB-S00-06, OB-S07-04 |
| 1961 | `/problems/6/complaints/5/cc_detail` | `cc_detail` |  | string | 유착 해제 |  |
| 1962 | `/problems/6/complaints/5/cc_group` | `cc_group` |  | string | 흉터형(열린모공) |  |
| 1963 | `/problems/6/complaints/5/procedures` | `procedures` |  | array[2] | (배열 · 2개) |  |
| 1964 | `/problems/6/complaints/5/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1965 | `/problems/6/complaints/5/procedures/0/name` | `name` |  | string | 니들RF |  |
| 1966 | `/problems/6/complaints/5/procedures/0/category` | `category` |  | string | M11 |  |
| 1967 | `/problems/6/complaints/5/procedures/0/role` | `role` |  | string | 모공 수축 |  |
| 1968 | `/problems/6/complaints/5/procedures/0/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 1969 | `/problems/6/complaints/5/procedures/0/products/0` | `(products 원소)` | 0 | string | 포텐자 |  |
| 1970 | `/problems/6/complaints/5/procedures/0/products/1` | `(products 원소)` | 1 | string | 시크릿 |  |
| 1971 | `/problems/6/complaints/5/procedures/1` | `(procedures 원소)` | 1 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 1972 | `/problems/6/complaints/5/procedures/1/name` | `name` |  | string | 스킨부스터 |  |
| 1973 | `/problems/6/complaints/5/procedures/1/category` | `category` |  | string | M4 |  |
| 1974 | `/problems/6/complaints/5/procedures/1/role` | `role` |  | string | 콜라겐 재생 |  |
| 1975 | `/problems/6/complaints/5/procedures/1/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 1976 | `/problems/6/complaints/5/procedures/1/products/0` | `(products 원소)` | 0 | string | 쥬베룩 |  |
| 1977 | `/problems/6/complaints/5/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 1978 | `/problems/6/complaints/5/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 1979 | `/problems/6/complaints/5/combos/0/name` | `name` |  | string | 니들RF + 스킨부스터 |  |
| 1980 | `/problems/6/complaints/5/combos/0/combo` | `combo` |  | array[2] | (배열 · 2개) |  |
| 1981 | `/problems/6/complaints/5/combos/0/combo/0` | `(combo 원소)` | 0 | string | 니들RF |  |
| 1982 | `/problems/6/complaints/5/combos/0/combo/1` | `(combo 원소)` | 1 | string | 스킨부스터 |  |
| 1983 | `/problems/6/complaints/5/combos/0/reason` | `reason` |  | string | 열 수축 + 콜라겐 재생 |  |
| 1984 | `/problems/6/complaints/5/combos/0/evidence` | `evidence` |  | string | 쥬베룩 PDLLA가 모공에 특화 |  |
| 1985 | `/problems/6/complaints/5/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 1986 | `/problems/6/complaints/5/alternatives/0` | `(alternatives 원소)` | 0 | string | MTS + 스킨부스터도 가벼운 대안 | OB-S07-03 |

## 잠정 관찰 (원문 칸과 분리)

| ID | 상태 | 위치 | 관찰 |
|---|---|---|---|
| OB-S07-01 | I | `/problems/6/complaints/0/procedures/1`<br>`/problems/6/complaints/0/procedures/3` | c0 에도 name '스킨부스터' 가 두 번(P1 '피부 재생' / P3 '콜라겐 재생') 나온다(I-07 같은 유형). S06 c4 와 구성이 같고 P2 니들RF products 만 '포텐자·시크릿'(S06 은 제니스 포함)으로 다르다. |
| OB-S07-02 | P | `/problems/6/complaints/0/combos/1/reason`<br>`/problems/6/complaints/0/combos/1/evidence`<br>`/problems/5/complaints/3/combos/0/reason` | 같은 combo '니들RF + 스킨부스터' 가 S06 에서는 reason '모공 수축 + 재생'·evidence '쥬베룩이 모공에 특화', S07 에서는 '열 수축 + 콜라겐 재생'·'쥬베룩 PDLLA가 모공에 특화' 다. problem 마다 문장 변형이 있다. '열 수축' 은 수축 기전 수식, 'PDLLA' 는 재질 약어. |
| OB-S07-03 | P | `/problems/6/complaints/0/alternatives/1`<br>`/problems/6/complaints/1/alternatives/0`<br>`/problems/6/complaints/2/alternatives/0`<br>`/problems/6/complaints/3/alternatives/0`<br>`/problems/6/complaints/4/alternatives/0`<br>`/problems/6/complaints/5/alternatives/0` | alternatives 'MTS + 스킨부스터도 가벼운 대안' — 'MTS' 는 procedures 에 없는 시술 표현이며 원문 풀이가 없다. '+' 로 함께 시술을, '도' 로 추가 선택지를, '가벼운' 으로 비교 정도를 나타낸다. |
| OB-S07-04 | I | `/problems/6/complaints/2/cc`<br>`/problems/6/complaints/4/cc`<br>`/problems/6/complaints/5/cc` | cc '프락셔널레이저'·'CO2프락셀'·'서브시전' 이 가리키는 시술이 procedures 에 없다(니들RF·스킨부스터·리프팅기기만). I-03 같은 유형. |
| OB-S07-05 | P | `/problems/6/complaints/2/procedures/2/role`<br>`/problems/6/complaints/2/combos/1/reason`<br>`/problems/6/complaints/2/combos/1/evidence` | '처짐 개선', '처진 모공 해결', '원인(처짐)+결과(모공) 동시 치료' — '처짐' 표기(F-07). evidence 는 괄호로 원인·결과 라벨을 붙인 공식형이다. |
| OB-S07-06 | P | `/problems/6/complaints/0/cc`<br>`/problems/5/complaints/4/cc`<br>`/problems/6/complaints/1/cc`<br>`/problems/5/complaints/3/cc` | cc '스킨보톡스'·'아그네스' 가 P6 여드름과 P7 모공 두 problem 에 모두 있다. cc_detail('피지↓' vs '피지↓ 모공↓', '피지선 파괴' vs '피지선 파괴 · 니들RF')과 cc_group 이 다르다. 같은 cc 의 다중 소속이 원문 구조상 사실이다. |
| OB-S07-07 | K | `/problems/6/complaints/4/cc` | 'CO2프락셀' 혼합 표기(로마자+숫자+한글). 형태소 분절 확인(K-04). |

## 수동 복합 표현 (직접 읽기 · 출현별)

| 표현 | 위치(Pointer · 값 내 구간) | 관점(탐색용, 확정 분류 아님) |
|---|---|---|
| 피지↓ | `/problems/6/complaints/0/cc_detail` [0,3) | 기호(↓), 감소 표현 |
| 피지선 파괴 | `/problems/6/complaints/1/cc_detail` [0,6) | 효과 표현, 기전 표현 |
| 콜라겐리모델링 | `/problems/6/complaints/2/cc_detail` [0,7) | 붙여 쓴 복합어, 기전 표현 |
| 진피 타이트닝 | `/problems/6/complaints/3/cc_detail` [0,7) | 층위(진피), 효과 표현 |
| 박피성 재생 | `/problems/6/complaints/4/cc_detail` [0,6) | 기전 수식(박피성), 효과 표현 |
| 유착 해제 | `/problems/6/complaints/5/cc_detail` [0,5) | 기전 표현 |
| 흉터형(열린모공) | `/problems/6/complaints/4/cc_group` [0,9)<br>`/problems/6/complaints/5/cc_group` [0,9) | 유형 표현, 괄호 보충 |
| 피지과다형 | `/problems/6/complaints/0/cc_group` [0,5)<br>`/problems/6/complaints/1/cc_group` [0,5) | 유형 표현, 정도(과다) |
| 탄력저하형 | `/problems/6/complaints/2/cc_group` [0,5)<br>`/problems/6/complaints/3/cc_group` [0,5) | 유형 표현, 감소 표현(저하) |
| CO2프락셀 | `/problems/6/complaints/4/cc` [0,6) | 시술명 표현, 혼합 표기 |
| 진피내 피지선·입모근의 콜린성 신호 차단 | `/problems/6/complaints/0/procedures/0/role` [0,22) | role 표현, 층위(진피내), 기전 표현 |
| 마이크로보톡스로 피지·모공 감소 + 스킨부스터로 피부 재생 보조 | `/problems/6/complaints/0/combos/0/reason` [0,35) | 기호(+), 수단(-로)+결과, 감소 표현, 보조 |
| 마이크로보톡스는 피지선의 콜린성 신호 차단으로 피지·모공을 감소시킴 | `/problems/6/complaints/0/combos/0/evidence` [0,37) | 기전 진술, 감소 표현 |
| 열 수축 + 콜라겐 재생 | `/problems/6/complaints/0/combos/1/reason` [0,13)<br>`/problems/6/complaints/1/combos/0/reason` [0,13)<br>`/problems/6/complaints/2/combos/0/reason` [0,13)<br>`/problems/6/complaints/3/combos/0/reason` [0,13)<br>`/problems/6/complaints/4/combos/0/reason` [0,13)<br>`/problems/6/complaints/5/combos/0/reason` [0,13) | 기호(+), 기전 수식(열) |
| 쥬베룩 PDLLA가 모공에 특화 | `/problems/6/complaints/0/combos/1/evidence` [0,17)<br>`/problems/6/complaints/1/combos/0/evidence` [0,17)<br>`/problems/6/complaints/2/combos/0/evidence` [0,17)<br>`/problems/6/complaints/3/combos/0/evidence` [0,17)<br>`/problems/6/complaints/4/combos/0/evidence` [0,17)<br>`/problems/6/complaints/5/combos/0/evidence` [0,17) | 제품명+재질 약어, 특화 주장 |
| 수축 + 리프팅 = 처진 모공 해결 | `/problems/6/complaints/2/combos/1/reason` [0,19)<br>`/problems/6/complaints/3/combos/1/reason` [0,19) | 공식형 문장, 기호(+), 기호(=), 상태 수식(처진) |
| 원인(처짐)+결과(모공) 동시 치료 | `/problems/6/complaints/2/combos/1/evidence` [0,19)<br>`/problems/6/complaints/3/combos/1/evidence` [0,19) | 괄호 라벨, 기호(+ 공백 없음), 동시성(동시), 원인·결과 |
| 처짐 개선 | `/problems/6/complaints/2/procedures/2/role` [0,5)<br>`/problems/6/complaints/3/procedures/2/role` [0,5) | role 표현, 증상 표현 |
| 효과 부족 시 리프팅기기 추가 | `/problems/6/complaints/0/alternatives/0` [0,16) | 조건(-시), 부족 표현, 추가 표현 |
| MTS + 스킨부스터도 가벼운 대안 | `/problems/6/complaints/0/alternatives/1` [0,19)<br>`/problems/6/complaints/1/alternatives/0` [0,19)<br>`/problems/6/complaints/2/alternatives/0` [0,19)<br>`/problems/6/complaints/3/alternatives/0` [0,19)<br>`/problems/6/complaints/4/alternatives/0` [0,19)<br>`/problems/6/complaints/5/alternatives/0` [0,19) | 대안 표현, 기호(+), 약어(MTS), 비교(가벼운), 추가(도) |

## 이 구획에서 연 미결

- 새로 연 미결 없음(관찰은 기존 미결 유형에 연결).
