---
type: concept
id: object-storage
title: 오브젝트 스토리지 (Object Storage)
aliases:
  - 오브젝트 스토리지
  - object storage
  - S3
  - 버킷
  - bucket
  - AmazonS3
up:
  - 2024-09-29-Day84
tags:
  - 클라우드
  - 저장
  - web
---

# 오브젝트 스토리지 (Object Storage)

**파일을 「경로가 있는 파일」이 아니라 「키로 찾는 객체」로 저장하는 저장소.** 디렉토리 트리가 아니라 **버킷 하나에 키-값**이고, 접근은 파일 API 가 아니라 **HTTP 요청**이다.

## 정의

세 가지가 한 벌이다.

| 것 | 무엇 |
|---|---|
| **버킷(bucket)** | 객체를 담는 최상위 그릇. 이름이 전역에서 유일해야 한다 |
| **키(key)** | 객체를 가리키는 이름. `board/2024/uuid-file.png` 처럼 `/` 를 쓰지만 **경로가 아니라 그냥 문자열**이다 |
| **객체(object)** | 바이트 덩어리 + 메타데이터(`Content-Type`·길이 등) |

접근에 필요한 것도 정해져 있다 — **엔드포인트 · 리전 · 액세스 키 · 시크릿 키.**

```properties
ncp.storage.endpoint=https://kr.object.ncloudstorage.com
ncp.storage.regionname=kr-standard
ncp.storage.bucketname=bitcamp-bucket96
ncp.accesskey=...
ncp.secretkey=...
```

**S3 API 가 사실상 표준이다.** 네이버 클라우드의 오브젝트 스토리지도 AWS 의 `aws-java-sdk-s3` 라이브러리로 붙는다 — 엔드포인트만 바꾸면 된다.

```groovy
implementation 'com.amazonaws:aws-java-sdk-s3:1.12.772'
```

### 세 가지 조작

```java
// 올리기 — 메타데이터 + 스트림
ObjectMetadata meta = new ObjectMetadata();
meta.setContentType((String) options.get(CONTENT_TYPE));
s3.putObject(new PutObjectRequest(bucketName, filePath, in, meta)
        .withCannedAcl(CannedAccessControlList.PublicRead));

// 지우기 — 버킷 + 키만 있으면 된다
s3.deleteObject(bucketName, filePath);

// 내려받기 — 객체에서 InputStream 을 얻어 복사한다
S3Object s3Object = s3.getObject(bucketName, filePath);
S3ObjectInputStream in = s3Object.getObjectContent();
byte[] buf = new byte[4096];
int len;
while ((len = in.read(buf)) != -1) {
  out.write(buf, 0, len);
}
in.close();
```

**읽고 쓰는 모양은 파일과 같다** — `InputStream`·`OutputStream` 이고, 4096 바이트 버퍼로 옮기는 그 루프다 → [[binary-io]] · [[io-stream]]

## 왜 중요한가

**서버의 디스크에 파일을 두지 않게 된다.** 업로드한 파일을 서버 로컬에 저장하면 세 가지가 묶인다 — 서버를 늘리면 파일이 한 대에만 있고, 서버를 다시 띄우면 사라지고, 용량이 서버 디스크에 갇힌다. 스토리지로 빼면 **애플리케이션 서버가 상태를 갖지 않는다** → [[web-application-deployment]] · [[distributed-processing]]

**그리고 파일 서빙을 애플리케이션이 안 해도 된다.** `PublicRead` 로 올린 객체는 URL 하나로 바로 열린다 — 이미지 요청이 우리 서버를 아예 지나지 않는다 → [[static-and-dynamic-content]]

## 경계와 오해

- **키의 `/` 는 디렉토리가 아니다** — 콘솔이 폴더처럼 보여 줄 뿐 실제로는 이름의 일부다. 필기의 「폴더 생성」 코드가 **길이 0 짜리 객체를 `application/x-directory` 로 올리는 것**인 이유가 이것이다 — 폴더라는 것이 없어서 폴더 흉내를 내는 것이다 → [[filesystem-path]]
- **`Content-Type` 을 안 넣으면 브라우저가 다운로드해 버린다** — 이미지를 올려도 타입이 없으면 화면에 안 보인다. 메타데이터가 **표시 방식을 정한다** → [[http-message]]
- **`PublicRead` 는 「누구나 볼 수 있다」는 뜻이다** — 첨부파일을 이렇게 올리면 **URL 을 아는 사람은 로그인 없이 본다.** 링크가 추측 가능하면 남의 파일도 열린다. 파일 이름에 UUID 를 쓰는 것이 그 완화책이지만 **권한 검사는 아니다** → [[http-session]]
- **키 이름을 사용자 파일명 그대로 쓰면 안 된다** — 같은 이름이 올라오면 덮어써진다(오브젝트 스토리지에는 「이미 있습니다」가 없다). 필기가 **UUID 를 키로 쓰고 원래 파일명을 DB 에 따로 저장**하는 것이 그 답이다 → [[primary-key]]
- **삭제는 되돌릴 수 없고 실패도 조용하다** — `deleteObject` 는 없는 키를 지워도 예외가 나지 않는다. 「지워졌는지」를 확인하려면 따로 봐야 한다
- **DB 와 스토리지는 한 트랜잭션이 아니다** — 글을 지우면서 파일도 지울 때, DB 롤백이 나도 스토리지에서 지운 파일은 안 돌아온다. **경계 밖의 부수효과**라 순서와 보정 절차를 따로 정해야 한다 → [[declarative-transaction]] · [[transaction]]
- **네트워크 너머라 느리고 실패한다** — 로컬 파일 쓰기와 달리 왕복이 있고 타임아웃이 있다. 필기의 예제가 `e.printStackTrace()` 로 끝나는데, **실패했는데 성공한 것처럼 이어지는** 모양이다 → [[exception-handling]]

## 함께 보는 개념

- [[multipart-form-data]] — 업로드된 파일이 여기까지 오는 경로
- [[binary-io]] · [[io-stream]] — 바이트를 옮기는 방법
- [[filesystem-path]] — 키와 경로가 갈리는 축
- [[externalized-configuration]] — 접근 키를 코드 밖에 두는 이유
- [[service-layer]] — 이 저장소를 감싸는 층
- [[remote-procedure-call]] — 네트워크 너머의 호출이라는 성격
- [[static-and-dynamic-content]] — 파일 서빙을 넘기는 자리

## 출처

- [[2024-09-29-Day84]] — 「Storage Object 설정하기」 절 전체. **NCP 의 오브젝트 스토리지를 AWS 의 `aws-java-sdk-s3` 로 붙인다**는 것(「ncp의 Starage Object는 aws의 s3라이브러리를 사용한다」)이 S3 API 가 표준 자리를 차지했음을 보인다. 엔드포인트·리전·버킷명·액세스 키·시크릿 키 다섯 값을 properties 로 빼고, `AmazonS3ClientBuilder` 로 클라이언트를 만드는 생성자 코드가 실려 있다. upload·delete·download 세 조작을 **NCP 가이드 코드 → 우리 코드 적용** 순으로 나란히 놓아, 가이드가 로컬 파일에 저장하던 것을 `OutputStream` 매개변수로 바꾸는 이행이 보인다. 「폴더 생성」이 길이 0 객체를 올리는 것이라는 점도 코드로 남았다. 다만 `PublicRead` 의 의미, 키 충돌, DB 와의 트랜잭션 불일치는 다루지 않았고, 예제 코드는 예외를 `printStackTrace()` 로만 처리한다
