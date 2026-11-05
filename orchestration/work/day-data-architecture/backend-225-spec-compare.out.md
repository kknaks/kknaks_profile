SPEC 테이블 51 · 모델 테이블 51 · SPEC 만 [] · 모델만 []

| 테이블 | SPEC 칸 | 보류(—) | 모델 칸 | 칸 차이 | 타입 | 필수 | PK | 유일 · FK · 비고 |
|---|---|---|---|---|---|---|---|---|
| `account` | 9 | 0 | 9 | 없음 | 맞음 | 맞음 | (id) | FK 0 |
| `account_brand_access` | 5 | 0 | 5 | 없음 | 맞음 | 맞음 | (account_id,brand_id) | FK 2 |
| `board_card_order` | 8 | 0 | 8 | 없음 | 맞음 | 맞음 | (hospital_id,board_date,visit_id) | FK 3 |
| `brand` | 7 | 0 | 7 | 없음 | 맞음 | 맞음 | (id) | UNIQUE (code) · FK 0 |
| `chat_attachment` | 15 | 0 | 15 | 없음 | 맞음 | 맞음 | (id) | FK 3 |
| `chat_member` | 12 | 0 | 12 | 없음 | 맞음 | 맞음 | (room_id,account_id) | FK 2 |
| `chat_message` | 12 | 0 | 12 | 없음 | 맞음 | 맞음 | (id) | UNIQUE (account_id,client_id) / (room_id,seq) · FK 3 |
| `chat_room` | 11 | 0 | 11 | 없음 | 맞음 | 맞음 | (id) | UNIQUE (direct_key) · FK 2 |
| `consultation` | 10 | 1 | 9 | 없음 | 맞음 | 맞음 | (id) | FK 3 · 보류 procedures |
| `consultation_procedure` | 13 | 0 | 13 | 없음 | 맞음 | 맞음 | (id) | FK 1 |
| `crm_connection` | 7 | 0 | 7 | 없음 | 맞음 | 맞음 | (hospital_id) | FK 1 |
| `customer` | 41 | 0 | 41 | 없음 | 맞음 | 맞음 | (id) | UNIQUE (hospital_id,chart_number) · FK 7 · gender=열린 enum→varchar |
| `customer_category` | 9 | 0 | 9 | 없음 | 맞음 | 맞음 | (id) | FK 1 |
| `customer_category_link` | 5 | 0 | 5 | 없음 | 맞음 | 맞음 | (customer_id,category_id) | FK 2 |
| `customer_type` | 6 | 0 | 6 | 없음 | 맞음 | 맞음 | (id) | FK 1 |
| `device` | 10 | 0 | 10 | 없음 | 맞음 | 맞음 | (id) | UNIQUE (install_id) · FK 1 |
| `display_request` | 15 | 0 | 15 | 없음 | 맞음 | 맞음 | (id) | FK 4 · kind=열린 enum→varchar |
| `doctor_call` | 9 | 0 | 9 | 없음 | 맞음 | 맞음 | (id) | FK 4 |
| `doctor_call_accept` | 8 | 0 | 8 | 없음 | 맞음 | 맞음 | (id) | FK 3 |
| `doctor_call_task` | 5 | 0 | 5 | 없음 | 맞음 | 맞음 | (call_id,task_id) | FK 2 |
| `event_log` | 8 | 0 | 9 | 없음 | 맞음 | 맞음 | (id) | FK 3 · 모델에만 deleted_at |
| `external_outbox` | 16 | 0 | 17 | 없음 | 맞음 | 맞음 | (id) | FK 2 · 모델에만 deleted_at |
| `external_ref` | 15 | 0 | 15 | 없음 | 맞음 | 맞음 | (id) | UNIQUE (hospital_id,vendor,entity_type,external_id) · FK 1 · entity_type=열린 enum→varchar |
| `external_session` | 8 | 0 | 8 | 없음 | 맞음 | 맞음 | (session_id) | FK 1 |
| `funnel` | 10 | 0 | 10 | 없음 | 맞음 | 맞음 | (id) | FK 2 |
| `funnel_category` | 8 | 0 | 8 | 없음 | 맞음 | 맞음 | (id) | FK 1 |
| `hospital` | 7 | 0 | 7 | 없음 | 맞음 | 맞음 | (id) | FK 1 |
| `id_photo` | 12 | 1 | 11 | 없음 | 맞음 | 맞음 | (id) | FK 3 · 보류 KOS 업로드 상태 · doc_type=열린 enum→varchar |
| `identity_check` | 12 | 0 | 12 | 없음 | 맞음 | 맞음 | (id) | FK 5 · method=열린 enum→varchar · status=열린 enum→varchar |
| `job_role` | 8 | 0 | 8 | 없음 | 맞음 | 맞음 | (id) | FK 1 |
| `job_role_permission` | 6 | 0 | 6 | 없음 | 맞음 | 맞음 | (job_role_id,permission_key) | FK 1 |
| `login_session` | 11 | 0 | 11 | 없음 | 맞음 | 맞음 | (id) | UNIQUE (token_hash) · FK 3 |
| `notice` | 7 | 0 | 7 | 없음 | 맞음 | 맞음 | (id) | FK 1 |
| `notification` | 12 | 0 | 12 | 없음 | 맞음 | 맞음 | (id) | FK 4 |
| `notification_setting` | 6 | 0 | 6 | 없음 | 맞음 | 맞음 | (account_id,kind) | FK 1 · kind=열린 enum→varchar |
| `push_log` | 16 | 0 | 17 | 없음 | 맞음 | 맞음 | (id) | FK 5 · 모델에만 deleted_at |
| `questionnaire_history` | 13 | 0 | 13 | 없음 | 맞음 | 맞음 | (id) | FK 4 |
| `reservation_group` | 9 | 0 | 9 | 없음 | 맞음 | 맞음 | (id) | FK 1 |
| `reservation_group_capacity` | 6 | 0 | 6 | 없음 | 맞음 | 맞음 | (group_id,zone_id) | FK 2 |
| `reservation_group_timetable` | 10 | 0 | 10 | 없음 | 맞음 | 맞음 | (group_id,weekday) | FK 1 |
| `room` | 8 | 0 | 8 | 없음 | 맞음 | 맞음 | (id) | FK 2 |
| `staff` | 14 | 0 | 14 | 없음 | 맞음 | 맞음 | (id) | FK 4 |
| `visit` | 32 | 3 | 29 | 없음 | 맞음 | 맞음 | (id) | FK 9 · 보류 purchase_ids,prescription_ids,reactions |
| `visit_anesthesia` | 9 | 0 | 9 | 없음 | 맞음 | 맞음 | (id) | FK 3 |
| `visit_flow_log` | 7 | 0 | 7 | 없음 | 맞음 | 맞음 | (id) | FK 2 |
| `visit_occupied_resource` | 11 | 1 | 10 | 없음 | 맞음 | 맞음 | (id) | FK 3 · 보류 doctor_ids |
| `visit_occupied_resource_doctor` | 5 | 0 | 5 | 없음 | 맞음 | 맞음 | (occupied_resource_id,staff_id) | FK 2 |
| `visit_requested_procedure` | 13 | 0 | 13 | 없음 | 맞음 | 맞음 | (id) | FK 1 |
| `visit_task` | 30 | 0 | 30 | 없음 | 맞음 | 맞음 | (id) | FK 2 · unit_type=열린 enum→varchar |
| `visit_task_staff` | 6 | 0 | 6 | 없음 | 맞음 | 맞음 | (task_id,staff_id,role) | FK 2 |
| `zone` | 8 | 0 | 8 | 없음 | 맞음 | 맞음 | (id) | FK 1 |

불일치 테이블 0
