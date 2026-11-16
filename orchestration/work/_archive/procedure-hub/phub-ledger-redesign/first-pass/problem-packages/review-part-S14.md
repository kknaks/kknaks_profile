# S14 — /problems/13 P14 기타

[← review.md](review.md) · 범위 /problems/13 및 /problems/13/** 전체 · 소유 노드 139 · 말단 83 · 빈 값 4 · 직접 읽기 done

상위 문맥(공유, S00 소유): 루트 객체 → `/description` = taxonomy P1~P14 하위구조 기반 CC 자동 생성 → `/problems` 배열.

직접 읽기: reading/S14.txt 로 c0~c6 전부(procedures 7·combos 6·alternatives 8) 읽음. c3 combos 빈 배열 확인.

## 원문 값 (문서 순서 · 전부)

| # | JSON Pointer | 원본 컬럼명 | 배열 순번 | 자료형 | 원문 값 | 관찰 참조 |
|---|---|---|---|---|---|---|
| 3517 | `/problems/13` | `(problems 원소)` | 13 | object{3} | (객체 · 키: `problem_id`, `problem`, `complaints`) |  |
| 3518 | `/problems/13/problem_id` | `problem_id` |  | string | P14 |  |
| 3519 | `/problems/13/problem` | `problem` |  | string | 기타 |  |
| 3520 | `/problems/13/complaints` | `complaints` |  | array[7] | (배열 · 7개) |  |
| 3521 | `/problems/13/complaints/0` | `(complaints 원소)` | 0 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 3522 | `/problems/13/complaints/0/cc` | `cc` |  | string | 점제거 |  |
| 3523 | `/problems/13/complaints/0/cc_detail` | `cc_detail` |  | string | CO2 레이저 |  |
| 3524 | `/problems/13/complaints/0/cc_group` | `cc_group` |  | string | 점/사마귀 |  |
| 3525 | `/problems/13/complaints/0/procedures` | `procedures` |  | array[1] | (배열 · 1개) |  |
| 3526 | `/problems/13/complaints/0/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 3527 | `/problems/13/complaints/0/procedures/0/name` | `name` |  | string | 레이저 |  |
| 3528 | `/problems/13/complaints/0/procedures/0/category` | `category` |  | string | M8 |  |
| 3529 | `/problems/13/complaints/0/procedures/0/role` | `role` |  | string | 병변 제거 |  |
| 3530 | `/problems/13/complaints/0/procedures/0/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 3531 | `/problems/13/complaints/0/procedures/0/products/0` | `(products 원소)` | 0 | string | CO2레이저 | OB-S14-06 |
| 3532 | `/problems/13/complaints/0/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 3533 | `/problems/13/complaints/0/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 3534 | `/problems/13/complaints/0/combos/0/name` | `name` |  | string | 레이저 제거 |  |
| 3535 | `/problems/13/complaints/0/combos/0/combo` | `combo` |  | array[1] | (배열 · 1개) |  |
| 3536 | `/problems/13/complaints/0/combos/0/combo/0` | `(combo 원소)` | 0 | string | 레이저 |  |
| 3537 | `/problems/13/complaints/0/combos/0/reason` | `reason` |  | string | 레이저로 정밀 제거 |  |
| 3538 | `/problems/13/complaints/0/combos/0/evidence` | `evidence` |  | string | CO2 레이저 사용 | OB-S14-06 |
| 3539 | `/problems/13/complaints/0/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 3540 | `/problems/13/complaints/0/alternatives/0` | `(alternatives 원소)` | 0 | string | 전문의 상담 필수 | OB-S14-08 |
| 3541 | `/problems/13/complaints/1` | `(complaints 원소)` | 1 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 3542 | `/problems/13/complaints/1/cc` | `cc` |  | string | 사마귀 |  |
| 3543 | `/problems/13/complaints/1/cc_detail` | `cc_detail` |  | string | 냉동/CO2 | OB-S14-05 |
| 3544 | `/problems/13/complaints/1/cc_group` | `cc_group` |  | string | 점/사마귀 |  |
| 3545 | `/problems/13/complaints/1/procedures` | `procedures` |  | array[1] | (배열 · 1개) |  |
| 3546 | `/problems/13/complaints/1/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 3547 | `/problems/13/complaints/1/procedures/0/name` | `name` |  | string | 레이저 |  |
| 3548 | `/problems/13/complaints/1/procedures/0/category` | `category` |  | string | M8 |  |
| 3549 | `/problems/13/complaints/1/procedures/0/role` | `role` |  | string | 병변 제거 |  |
| 3550 | `/problems/13/complaints/1/procedures/0/products` | `products` |  | array[1] | (배열 · 1개) |  |
| 3551 | `/problems/13/complaints/1/procedures/0/products/0` | `(products 원소)` | 0 | string | CO2레이저 |  |
| 3552 | `/problems/13/complaints/1/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 3553 | `/problems/13/complaints/1/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 3554 | `/problems/13/complaints/1/combos/0/name` | `name` |  | string | 레이저 제거 |  |
| 3555 | `/problems/13/complaints/1/combos/0/combo` | `combo` |  | array[1] | (배열 · 1개) |  |
| 3556 | `/problems/13/complaints/1/combos/0/combo/0` | `(combo 원소)` | 0 | string | 레이저 |  |
| 3557 | `/problems/13/complaints/1/combos/0/reason` | `reason` |  | string | 레이저로 정밀 제거 |  |
| 3558 | `/problems/13/complaints/1/combos/0/evidence` | `evidence` |  | string | CO2 레이저 사용 |  |
| 3559 | `/problems/13/complaints/1/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 3560 | `/problems/13/complaints/1/alternatives/0` | `(alternatives 원소)` | 0 | string | 전문의 상담 필수 |  |
| 3561 | `/problems/13/complaints/2` | `(complaints 원소)` | 2 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 3562 | `/problems/13/complaints/2/cc` | `cc` |  | string | 문신제거 |  |
| 3563 | `/problems/13/complaints/2/cc_detail` | `cc_detail` |  | string | 피코레이저 |  |
| 3564 | `/problems/13/complaints/2/cc_group` | `cc_group` |  | string | 문신제거 |  |
| 3565 | `/problems/13/complaints/2/procedures` | `procedures` |  | array[1] | (배열 · 1개) |  |
| 3566 | `/problems/13/complaints/2/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 3567 | `/problems/13/complaints/2/procedures/0/name` | `name` |  | string | 피코레이저 |  |
| 3568 | `/problems/13/complaints/2/procedures/0/category` | `category` |  | string | M8 |  |
| 3569 | `/problems/13/complaints/2/procedures/0/role` | `role` |  | string | 문신 색소 파괴 |  |
| 3570 | `/problems/13/complaints/2/procedures/0/products` | `products` |  | array[2] | (배열 · 2개) |  |
| 3571 | `/problems/13/complaints/2/procedures/0/products/0` | `(products 원소)` | 0 | string | 피코슈어 |  |
| 3572 | `/problems/13/complaints/2/procedures/0/products/1` | `(products 원소)` | 1 | string | 피코웨이 |  |
| 3573 | `/problems/13/complaints/2/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 3574 | `/problems/13/complaints/2/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 3575 | `/problems/13/complaints/2/combos/0/name` | `name` |  | string | 피코레이저 시리즈 |  |
| 3576 | `/problems/13/complaints/2/combos/0/combo` | `combo` |  | array[1] | (배열 · 1개) |  |
| 3577 | `/problems/13/complaints/2/combos/0/combo/0` | `(combo 원소)` | 0 | string | 피코레이저 |  |
| 3578 | `/problems/13/complaints/2/combos/0/reason` | `reason` |  | string | 피코초 레이저로 색소 분해 |  |
| 3579 | `/problems/13/complaints/2/combos/0/evidence` | `evidence` |  | string | 다회차 필요 | OB-S14-09 |
| 3580 | `/problems/13/complaints/2/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 3581 | `/problems/13/complaints/2/alternatives/0` | `(alternatives 원소)` | 0 | string | 전문의 상담 필수 |  |
| 3582 | `/problems/13/complaints/3` | `(complaints 원소)` | 3 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 3583 | `/problems/13/complaints/3/cc` | `cc` |  | string | 보톡스 |  |
| 3584 | `/problems/13/complaints/3/cc_detail` | `cc_detail` |  | string | 겨드랑이/손/발 |  |
| 3585 | `/problems/13/complaints/3/cc_group` | `cc_group` |  | string | 다한증 | OB-S14-02 |
| 3586 | `/problems/13/complaints/3/procedures` | `procedures` |  | array[1] | (배열 · 1개) |  |
| 3587 | `/problems/13/complaints/3/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 3588 | `/problems/13/complaints/3/procedures/0/name` | `name` |  | string | 보톡스 |  |
| 3589 | `/problems/13/complaints/3/procedures/0/category` | `category` |  | string | M1 |  |
| 3590 | `/problems/13/complaints/3/procedures/0/role` | `role` |  | string | 땀샘(한선) 신경전달 차단으로 발한 억제 | OB-S14-07 |
| 3591 | `/problems/13/complaints/3/procedures/0/products` | `products` |  | array[3] | (배열 · 3개) |  |
| 3592 | `/problems/13/complaints/3/procedures/0/products/0` | `(products 원소)` | 0 | string | 보톡스 |  |
| 3593 | `/problems/13/complaints/3/procedures/0/products/1` | `(products 원소)` | 1 | string | 나보타 |  |
| 3594 | `/problems/13/complaints/3/procedures/0/products/2` | `(products 원소)` | 2 | string | 보툴렉스 |  |
| 3595 | `/problems/13/complaints/3/combos` | `combos` |  | array[0] | `[]` (빈 배열) | OB-S14-01 |
| 3596 | `/problems/13/complaints/3/alternatives` | `alternatives` |  | array[2] | (배열 · 2개) |  |
| 3597 | `/problems/13/complaints/3/alternatives/0` | `(alternatives 원소)` | 0 | string | 효과 부족 시 리프팅기기 추가 | OB-S14-02 |
| 3598 | `/problems/13/complaints/3/alternatives/1` | `(alternatives 원소)` | 1 | string | 전문의 상담 필수 |  |
| 3599 | `/problems/13/complaints/4` | `(complaints 원소)` | 4 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 3600 | `/problems/13/complaints/4/cc` | `cc` |  | string | 미라드라이 |  |
| 3601 | `/problems/13/complaints/4/cc_detail` | `cc_detail` |  | string | 마이크로웨이브 · 영구적 | OB-S14-03 |
| 3602 | `/problems/13/complaints/4/cc_group` | `cc_group` |  | string | 다한증 |  |
| 3603 | `/problems/13/complaints/4/procedures` | `procedures` |  | array[1] | (배열 · 1개) |  |
| 3604 | `/problems/13/complaints/4/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 3605 | `/problems/13/complaints/4/procedures/0/name` | `name` |  | string | 미라드라이 |  |
| 3606 | `/problems/13/complaints/4/procedures/0/category` | `category` |  | string | M9 |  |
| 3607 | `/problems/13/complaints/4/procedures/0/role` | `role` |  | string | 영구적 한선 파괴 | OB-S14-03 |
| 3608 | `/problems/13/complaints/4/procedures/0/products` | `products` |  | array[0] | `[]` (빈 배열) |  |
| 3609 | `/problems/13/complaints/4/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 3610 | `/problems/13/complaints/4/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 3611 | `/problems/13/complaints/4/combos/0/name` | `name` |  | string | 미라드라이 |  |
| 3612 | `/problems/13/complaints/4/combos/0/combo` | `combo` |  | array[1] | (배열 · 1개) |  |
| 3613 | `/problems/13/complaints/4/combos/0/combo/0` | `(combo 원소)` | 0 | string | 미라드라이 |  |
| 3614 | `/problems/13/complaints/4/combos/0/reason` | `reason` |  | string | 마이크로파로 한선 영구 파괴 | OB-S14-03 |
| 3615 | `/problems/13/complaints/4/combos/0/evidence` | `evidence` |  | string | 1~2회로 영구 효과 | OB-S14-03 |
| 3616 | `/problems/13/complaints/4/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 3617 | `/problems/13/complaints/4/alternatives/0` | `(alternatives 원소)` | 0 | string | 전문의 상담 필수 |  |
| 3618 | `/problems/13/complaints/5` | `(complaints 원소)` | 5 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 3619 | `/problems/13/complaints/5/cc` | `cc` |  | string | 백반증 |  |
| 3620 | `/problems/13/complaints/5/cc_detail` | `cc_detail` |  | string | 엑시머 308nm |  |
| 3621 | `/problems/13/complaints/5/cc_group` | `cc_group` |  | string | 피부질환 |  |
| 3622 | `/problems/13/complaints/5/procedures` | `procedures` |  | array[1] | (배열 · 1개) |  |
| 3623 | `/problems/13/complaints/5/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 3624 | `/problems/13/complaints/5/procedures/0/name` | `name` |  | string | 레이저 | OB-S14-04 |
| 3625 | `/problems/13/complaints/5/procedures/0/category` | `category` |  | string | M8 |  |
| 3626 | `/problems/13/complaints/5/procedures/0/role` | `role` |  | string | 광선치료 |  |
| 3627 | `/problems/13/complaints/5/procedures/0/products` | `products` |  | array[0] | `[]` (빈 배열) |  |
| 3628 | `/problems/13/complaints/5/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 3629 | `/problems/13/complaints/5/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 3630 | `/problems/13/complaints/5/combos/0/name` | `name` |  | string | 광선치료 |  |
| 3631 | `/problems/13/complaints/5/combos/0/combo` | `combo` |  | array[1] | (배열 · 1개) |  |
| 3632 | `/problems/13/complaints/5/combos/0/combo/0` | `(combo 원소)` | 0 | string | 레이저 |  |
| 3633 | `/problems/13/complaints/5/combos/0/reason` | `reason` |  | string | 자외선 치료 | OB-S14-04 |
| 3634 | `/problems/13/complaints/5/combos/0/evidence` | `evidence` |  | string | 다회차 시리즈 | OB-S14-09 |
| 3635 | `/problems/13/complaints/5/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 3636 | `/problems/13/complaints/5/alternatives/0` | `(alternatives 원소)` | 0 | string | 전문의 상담 필수 |  |
| 3637 | `/problems/13/complaints/6` | `(complaints 원소)` | 6 | object{6} | (객체 · 키: `cc`, `cc_detail`, `cc_group`, `procedures`, `combos`, `alternatives`) |  |
| 3638 | `/problems/13/complaints/6/cc` | `cc` |  | string | 건선 |  |
| 3639 | `/problems/13/complaints/6/cc_detail` | `cc_detail` |  | string | UVB 광치료 | OB-S14-04 |
| 3640 | `/problems/13/complaints/6/cc_group` | `cc_group` |  | string | 피부질환 |  |
| 3641 | `/problems/13/complaints/6/procedures` | `procedures` |  | array[1] | (배열 · 1개) |  |
| 3642 | `/problems/13/complaints/6/procedures/0` | `(procedures 원소)` | 0 | object{4} | (객체 · 키: `name`, `category`, `role`, `products`) |  |
| 3643 | `/problems/13/complaints/6/procedures/0/name` | `name` |  | string | 레이저 |  |
| 3644 | `/problems/13/complaints/6/procedures/0/category` | `category` |  | string | M8 |  |
| 3645 | `/problems/13/complaints/6/procedures/0/role` | `role` |  | string | 광선치료 |  |
| 3646 | `/problems/13/complaints/6/procedures/0/products` | `products` |  | array[0] | `[]` (빈 배열) |  |
| 3647 | `/problems/13/complaints/6/combos` | `combos` |  | array[1] | (배열 · 1개) |  |
| 3648 | `/problems/13/complaints/6/combos/0` | `(combos 원소)` | 0 | object{4} | (객체 · 키: `name`, `combo`, `reason`, `evidence`) |  |
| 3649 | `/problems/13/complaints/6/combos/0/name` | `name` |  | string | 광선치료 |  |
| 3650 | `/problems/13/complaints/6/combos/0/combo` | `combo` |  | array[1] | (배열 · 1개) |  |
| 3651 | `/problems/13/complaints/6/combos/0/combo/0` | `(combo 원소)` | 0 | string | 레이저 |  |
| 3652 | `/problems/13/complaints/6/combos/0/reason` | `reason` |  | string | 자외선 치료 |  |
| 3653 | `/problems/13/complaints/6/combos/0/evidence` | `evidence` |  | string | 다회차 시리즈 |  |
| 3654 | `/problems/13/complaints/6/alternatives` | `alternatives` |  | array[1] | (배열 · 1개) |  |
| 3655 | `/problems/13/complaints/6/alternatives/0` | `(alternatives 원소)` | 0 | string | 전문의 상담 필수 |  |

## 잠정 관찰 (원문 칸과 분리)

| ID | 상태 | 위치 | 관찰 |
|---|---|---|---|
| OB-S14-01 | P | `/problems/13/complaints/3/combos` | 원장 전체에서 유일한 빈 combos 배열(c3 cc '보톡스', cc_group '다한증'). 조합 없음인지 미기재인지 원문에 정보가 없다(B-04 와 같은 성격). |
| OB-S14-02 | P | `/problems/13/complaints/3/alternatives/0`<br>`/problems/13/complaints/3/cc_group` | 다한증 보톡스 complaint 의 alternatives 에 '효과 부족 시 리프팅기기 추가' 가 있다. S01·S02 의 주름 템플릿 문장과 같고 다한증 문맥과의 관계가 원문에 없다(B-02 템플릿 반복). |
| OB-S14-03 | P | `/problems/13/complaints/4/cc_detail`<br>`/problems/13/complaints/4/procedures/0/role`<br>`/problems/13/complaints/4/combos/0/reason`<br>`/problems/13/complaints/4/combos/0/evidence` | 미라드라이는 cc_detail '마이크로웨이브 · 영구적', role '영구적 한선 파괴', reason '마이크로파로 한선 영구 파괴', evidence '1~2회로 영구 효과' 로 영구성 진술이 네 칸에 반복된다. '마이크로웨이브'·'마이크로파' 두 표기. 임상 사실로 승인하지 않는다. |
| OB-S14-04 | P | `/problems/13/complaints/5/procedures/0/name`<br>`/problems/13/complaints/5/combos/0/reason`<br>`/problems/13/complaints/6/cc_detail` | 백반증·건선 complaint 의 procedures name 은 '레이저'(M8), role '광선치료', reason '자외선 치료', cc_detail '엑시머 308nm'·'UVB 광치료' 다. name 과 다른 칸의 표현이 서로 다른 범주어를 쓴다. 동일성을 판단하지 않는다. |
| OB-S14-05 | I | `/problems/13/complaints/1/cc_detail` | cc_detail '냉동/CO2' 중 '냉동' 처치는 procedures 에 없다(I-03 같은 유형). |
| OB-S14-06 | P | `/problems/13/complaints/0/procedures/0/products/0`<br>`/problems/13/complaints/0/combos/0/evidence` | products 'CO2레이저' 는 장비 종류 표현이며 evidence 'CO2 레이저 사용' 은 띄어 쓴 같은 말이다. 근거 칸에 사용 장비가 적혀 있다(F-06). |
| OB-S14-07 | P | `/problems/13/complaints/3/procedures/0/role` | role '땀샘(한선) 신경전달 차단으로 발한 억제' — 괄호로 동의 표기(한선)를 병기한다. c4 는 '한선' 만 쓴다. |
| OB-S14-08 | P | `/problems/13/complaints/0/alternatives/0` | alternatives '전문의 상담 필수' — 7개 complaint 전부. 상담 지시이며 대안이 아니다(F-04). S01 '전문 시술자 필요' 와 표현이 다르다. |
| OB-S14-09 | B | `/problems/13/complaints/2/combos/0/evidence`<br>`/problems/13/complaints/5/combos/0/evidence` | '다회차 필요', '다회차 시리즈' — 회수 막연. 수치로 바꾸지 않는다. |

## 수동 복합 표현 (직접 읽기 · 출현별)

| 표현 | 위치(Pointer · 값 내 구간) | 관점(탐색용, 확정 분류 아님) |
|---|---|---|
| CO2 레이저 | `/problems/13/complaints/0/cc_detail` [0,7) | 장비 표현, 혼합 표기 |
| 냉동/CO2 | `/problems/13/complaints/1/cc_detail` [0,6) | 방법 표현, 기호(/), 혼합 표기 |
| 점/사마귀 | `/problems/13/complaints/0/cc_group` [0,5)<br>`/problems/13/complaints/1/cc_group` [0,5) | 병변 표현, 기호(/) |
| 겨드랑이/손/발 | `/problems/13/complaints/3/cc_detail` [0,8) | 부위 표현, 기호(/) |
| 마이크로웨이브 · 영구적 | `/problems/13/complaints/4/cc_detail` [0,13) | 기전 표현, 기호(· 띄어 씀), 정도 수식(영구적) |
| 엑시머 308nm | `/problems/13/complaints/5/cc_detail` [0,9) | 장비 표현, 수량·단위(nm) |
| UVB 광치료 | `/problems/13/complaints/6/cc_detail` [0,7) | 약어(UVB), 치료 표현 |
| 병변 제거 | `/problems/13/complaints/0/procedures/0/role` [0,5)<br>`/problems/13/complaints/1/procedures/0/role` [0,5) | role 표현 |
| 레이저로 정밀 제거 | `/problems/13/complaints/0/combos/0/reason` [0,10)<br>`/problems/13/complaints/1/combos/0/reason` [0,10) | 수단(-로), 정도 수식(정밀) |
| CO2 레이저 사용 | `/problems/13/complaints/0/combos/0/evidence` [0,10)<br>`/problems/13/complaints/1/combos/0/evidence` [0,10) | 장비 표현, 근거 칸의 사용 장비 |
| 레이저 제거 | `/problems/13/complaints/0/combos/0/name` [0,6)<br>`/problems/13/complaints/1/combos/0/name` [0,6) | combo name(단독) |
| 문신 색소 파괴 | `/problems/13/complaints/2/procedures/0/role` [0,8) | role 표현, 기전 표현 |
| 피코레이저 시리즈 | `/problems/13/complaints/2/combos/0/name` [0,9) | combo name(단독), 회차 표현(시리즈) |
| 피코초 레이저로 색소 분해 | `/problems/13/complaints/2/combos/0/reason` [0,14) | 단위 표현(피코초), 수단(-로), 기전 표현 |
| 다회차 필요 | `/problems/13/complaints/2/combos/0/evidence` [0,6) | 회차(막연), 필요 지시 |
| 땀샘(한선) 신경전달 차단으로 발한 억제 | `/problems/13/complaints/3/procedures/0/role` [0,22) | role 표현, 괄호 병기, 수단(-으로)+결과, 억제 표현 |
| 효과 부족 시 리프팅기기 추가 | `/problems/13/complaints/3/alternatives/0` [0,16) | 조건(-시), 부족 표현, 추가 표현 |
| 영구적 한선 파괴 | `/problems/13/complaints/4/procedures/0/role` [0,9) | role 표현, 정도 수식(영구적) |
| 마이크로파로 한선 영구 파괴 | `/problems/13/complaints/4/combos/0/reason` [0,15) | 수단(-로), 정도 수식(영구), 기전 표현 |
| 1~2회로 영구 효과 | `/problems/13/complaints/4/combos/0/evidence` [0,11) | 범위(~), 회차, 정도 수식(영구) |
| 광선치료 | `/problems/13/complaints/5/procedures/0/role` [0,4)<br>`/problems/13/complaints/6/procedures/0/role` [0,4)<br>`/problems/13/complaints/5/combos/0/name` [0,4)<br>`/problems/13/complaints/6/combos/0/name` [0,4) | 치료 표현 |
| 자외선 치료 | `/problems/13/complaints/5/combos/0/reason` [0,6)<br>`/problems/13/complaints/6/combos/0/reason` [0,6) | 치료 표현 |
| 다회차 시리즈 | `/problems/13/complaints/5/combos/0/evidence` [0,7)<br>`/problems/13/complaints/6/combos/0/evidence` [0,7) | 회차(막연) |
| 전문의 상담 필수 | `/problems/13/complaints/0/alternatives/0` [0,9)<br>`/problems/13/complaints/1/alternatives/0` [0,9)<br>`/problems/13/complaints/2/alternatives/0` [0,9)<br>`/problems/13/complaints/3/alternatives/1` [0,9)<br>`/problems/13/complaints/4/alternatives/0` [0,9)<br>`/problems/13/complaints/5/alternatives/0` [0,9)<br>`/problems/13/complaints/6/alternatives/0` [0,9) | 상담 지시, 필수 지시 |

## 이 구획에서 연 미결

- 새로 연 미결 없음(관찰은 기존 미결 유형에 연결).
