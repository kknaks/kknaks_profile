---
type: concept
id: data-pipeline
title: 데이터 파이프라인 (Logstash)
aliases:
  - Logstash
  - 로그스태시
  - 데이터 파이프라인
  - pipeline.conf
  - 증분 동기화
up:
  - 2025-01-22-Day17
tags:
  - 데이터
  - 인프라
  - 동기화
---

# 데이터 파이프라인 (Logstash)

**한 저장소의 데이터를 주기적으로 읽어 다른 저장소로 옮기는 장치.** 읽고(input) · 다듬고(filter) · 내보내는(output) 세 단계가 설정 파일 하나에 적힌다.

## 정의

```ruby
input {
  jdbc {
    jdbc_connection_string => "jdbc:mysql://host.docker.internal:3306/es_dev"
    statement => "SELECT * FROM post"
    schedule => "*/30 * * * * *"          # 30초마다
    tracking_column => "id"               # 어디까지 읽었는지 추적할 컬럼
    use_column_value => true
    record_last_run => true               # 마지막 실행 위치를 기록
    last_run_metadata_path => "/usr/share/logstash/last_run_metadata"
  }
}

filter {
  mutate {
    remove_field => ["@version", "jdbc_user", "jdbc_password"]   # 내보내면 안 되는 것 제거
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "app1_posts"
    document_id => "%{id}"               # 같은 id 면 덮어쓴다
  }
  stdout { codec => rubydebug }          # 디버깅용
}
```

### 두 장치가 이 파이프라인을 쓸 만하게 만든다

- **`tracking_column` + `record_last_run`** — **마지막으로 읽은 위치를 기억**해 다음번에 그 뒤부터 읽는다(증분). 없으면 30초마다 전체를 다시 읽는다 → [[polling]] 의 커서와 같은 발상이다
- **`document_id => "%{id}"`** — 대상 쪽의 문서 id 를 원본의 기본키로 맞춘다. **같은 행을 두 번 넣어도 하나**가 된다 → [[primary-key]]

## 왜 중요한가

**저장소를 둘로 나눈 대가를 갚는 자리다.** 원본은 DB 에, 검색 색인은 검색 엔진에 두기로 한 순간 **둘을 맞추는 일**이 생기는데, 그것을 애플리케이션 코드에 넣으면 저장 로직마다 「색인도 갱신」이 붙는다. 파이프라인으로 빼면 **애플리케이션은 DB 만 알면 된다** → [[elasticsearch]] · [[service-layer]]

**그리고 「주기적으로 읽어 간다」는 방식의 성격이 드러난다.** 밀어 넣는(push) 것이 아니라 **끌어 오는(pull)** 것이라 — 애플리케이션은 아무것도 안 하고, 대신 **최대 주기만큼 늦다** → [[polling]]

## 경계와 오해

- **삭제는 이 방식으로 전해지지 않는다** — `SELECT * FROM post` 로 읽어 오는 것이라, **DB 에서 지운 행은 조회 결과에 아예 없다.** 색인에는 그대로 남아 **지운 글이 검색된다.** 소프트 삭제 컬럼을 두고 함께 넘기는 식의 처리가 따로 필요하다
- **`tracking_column => "id"` 는 수정을 못 따라간다** — id 는 새 행에서만 커지므로, **기존 행을 고쳐도 다시 안 읽는다.** 수정까지 따라가려면 `updated_at` 같은 시각 컬럼을 추적해야 한다 → [[date-time]]
- **30초는 「실시간 검색」이 아니다** — 검색 엔진 쪽이 실시간이어도 **들어오는 것이 30초마다**면 전체 지연은 그만큼이다. 진짜 즉시성이 필요하면 애플리케이션이 직접 색인해야 한다
- **비밀이 문서에 섞여 나갈 수 있다** — 필기가 `filter` 에서 `jdbc_user`·`jdbc_password` 를 지우는 이유다. **파이프라인이 붙인 메타데이터가 그대로 색인되면** 접속 정보가 검색된다 → [[externalized-configuration]]
- **드라이버를 볼륨으로 넣어 줘야 한다** — 컨테이너 안에 JDBC 드라이버가 없으므로 로컬 jar 를 마운트한다. 필기가 겪은 **권한 오류(`chmod 644`)**도 그 결과다 → [[container]] · [[jdbc]]
- **DB 에 30초마다 질의가 나간다** — 전체 조회라면 그것 자체가 부하다. **증분이 아니면 이 파이프라인이 원본을 괴롭힌다** → [[database-index]]

## 함께 보는 개념

- [[elasticsearch]] — 이 파이프라인이 채우는 곳
- [[polling]] — 주기적으로 끌어 오는 같은 방식
- [[jdbc]] — 원본에서 읽는 통로
- [[container]] — 드라이버·설정을 볼륨으로 넣는 자리
- [[primary-key]] — 중복을 막는 열쇠
- [[transaction]] — 두 저장소가 어긋날 수 있는 이유

## 출처

- [[2025-01-22-Day17]] — 「logstash 구현하기」 절이 **`pipeline.conf` 전문**을 싣고 각 설정에 주석을 달았다 — `input.jdbc` 의 접속 정보·`statement`·`schedule`·**`tracking_column`/`record_last_run`/`last_run_metadata_path`** 세트, `filter.mutate` 의 필드 제거, `output.elasticsearch` 의 `index` 와 **`document_id => "%{id}"`**. 마지막의 「logstash 구동 과정」 여섯 걸음이 파일을 읽는 것부터 ES 에 저장하는 것까지를 순서로 정리했다. 실전 함정 둘도 남았다 — JDBC 드라이버를 **볼륨 마운트로 컨테이너에 넣어 줘야** 한다는 것과, 그 jar 의 **읽기 권한(`chmod 644`)** 때문에 인식이 실패할 수 있다는 것. 다만 삭제가 전해지지 않는 문제, `id` 추적으로는 수정을 못 따라간다는 것은 다루지 않았다
