---
type: concept
id: tf-idf
title: TF-IDF
aliases:
  - TF-IDF
  - TFIDF
  - 단어 빈도 역문서 빈도
  - Term Frequency-Inverse Document Frequency
up:
  - C-051-tokenization-vectorization-and-embeddings
tags:
  - 자연어 처리
  - 어휘 가중치
  - 희소 벡터
  - 검색
---

# TF-IDF

TF-IDF는 문서 안에서의 단어 빈도와 전체 문서 집합에서의 희소성을 결합하는 가중치다. 여러 문서에 두루 등장하는 단어보다 특정 문서를 구분하는 데 유용한 단어를 강조한다.

## 정의

TF는 해당 문서에서 단어가 얼마나 등장하는지 나타낸다. IDF는 해당 단어가 등장하는 문서가 적을수록 커진다. 두 값을 결합해 문서별 어휘 가중치 벡터를 만든다.

`TF-IDF = 문서 내 빈도 × 역문서빈도`

실제 수치는 빈도에 대한 로그 적용, IDF 평활화, 벡터 정규화 등의 설정에 따라 달라진다. 어휘별 가중치를 나열한 문서 벡터는 보통 0이 많으므로 희소 행렬로 저장할 수 있다.

새 문서나 질문을 기존 문서와 비교하려면 기존 어휘 사전과 IDF를 재사용해야 한다. 질문만으로 다시 학습하면 좌표계와 가중치 기준이 달라진다.

## 사용 예시

다음 예시는 scikit-learn이 설치된 환경에서 실행한다.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

books = [
    "파이썬 데이터 분석 입문",
    "파이썬 데이터 분석 실전",
    "머신러닝 딥러닝 입문",
    "개발자를 위한 수학",
    "인공지능을 위한 수학",
]
vectorizer = TfidfVectorizer(
    tokenizer=str.split,
    token_pattern=None,
    lowercase=False,
)
documents = vectorizer.fit_transform(books)
query = vectorizer.transform(["파이썬 분석"])

if query.nnz == 0:
    print("질문에 어휘 사전의 단어가 없습니다.")
else:
    scores = cosine_similarity(query, documents).ravel()
    ranking = sorted(range(len(books)), key=lambda i: scores[i], reverse=True)
    for i in ranking:
        print(round(float(scores[i]), 3), books[i])
```

`fit_transform`은 어휘와 IDF를 학습하며, `transform`은 이를 새 질문에 적용한다. 첫 두 제목은 질문과 단어가 겹치므로 높은 점수를 얻는다. 공백 토큰화는 한국어 조사·어미를 분리하지 않는다.

## 왜 중요한가

TF-IDF는 외부 임베딩 모델 없이도 키워드 가중치와 문서 유사도를 계산하는 기준선이 된다. 각 좌표가 어휘에 대응하므로 어떤 단어 때문에 높은 점수가 나왔는지 설명하기도 쉽다.

임베딩을 도입할 때 이 기준선과 비교하면 의미적 표현의 이점이 실제 검색 결과에서도 나타나는지 확인할 수 있다.

## 경계와 오해

- **높은 TF-IDF ≠ 사람이 판단하는 중요도** — 문서를 통계적으로 구별하는 정도이며, 내용의 진실성이나 핵심성을 보장하지 않는다.
- **TF-IDF ≠ 학습된 의미 임베딩** — 같은 뜻이라도 단어가 겹치지 않으면 기본 표현만으로 관련성을 포착하기 어렵다.
- **TF-IDF에도 코사인 비교를 적용할 수 있다** — 코사인 유사도는 임베딩 전용 연산이 아니다.
- **어휘가 없는 질문 ≠ 관련 문서가 없는 질문** — OOV 질문의 영벡터는 현재 표현으로 비교할 근거가 없다는 뜻이다.
- **희소 행렬 ≠ 밀집 배열로 변환해야 계산 가능한 데이터** — 지원하는 연산에는 희소 행렬을 그대로 전달할 수 있다.

## 함께 보는 개념

- [[text-vectorization]] — TF-IDF를 포함하는 텍스트 수치화 과정이다.
- [[tokenization]] — 어떤 어휘가 빈도 계산의 대상이 되는지 정한다.
- [[cosine-similarity]] — TF-IDF 벡터의 방향을 비교한다.
- [[lexical-search]] — 용어 일치에 기반한 검색과 연결된다.
- [[text-embedding]] — 의미적 관계를 학습하는 대안적 표현이다.

## 출처

- [[C-051-tokenization-vectorization-and-embeddings]] — TF·IDF의 역할과 도서 제목 검색 예시, 동일한 어휘 사전을 재사용하는 방법을 설명한다.
