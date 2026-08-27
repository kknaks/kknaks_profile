---
type: content
id: C-020
date: 2026.06.08
duration: '35:04'
speaker: Bloom AI
kind: study
youtubeId: yWyJKCZG990
title:
  en: 'GraphRAG & Knowledge Graphs: Overcoming RAG Limitations'
  ko: 'GraphRAG와 지식 그래프: RAG의 한계 극복하기'
summary:
  en: 'Master GraphRAG in 30 minutes: Understand how knowledge graphs overcome RAG limitations and build semantic search with Neo4j and LangChain.'
  ko: RAG의 청킹 문제와 Top-K 검색 한계를 지식 그래프로 해결하는 GraphRAG의 원리와 Neo4j 구현법을 30분 안에 습득합니다.
tags:
- '#graphrag'
- '#rag'
- '#knowledge-graph'
- '#neo4j'
- '#langchain'
- '#llm'
---

## 요지

- RAG는 유사도 기반 검색에 의존하므로 청킹 과정에서 문맥이 끊기고 필요한 정보가 Top-K 범위를 벗어날 수 있다.
- 지식 그래프는 노드(엔티티)·엣지(관계)·속성(메타데이터)으로 데이터를 구조화하여 의미 있는 연결을 표현한다.
- GraphRAG는 질문 관련 엔티티를 찾은 후 엣지를 따라 다중 홉 탐색을 수행하므로 단편적 검색보다 정확한 답변을 생성한다.
- Google Knowledge Graph(2012)부터 Palantir Ontology까지, 실무에서 증명된 기술로 2030년까지 시장이 6배 이상 성장할 전망이다.

## 개요

**GraphRAG(Graph Retrieval-Augmented Generation)**는 최근 AI 에이전트 분야에서 급부상하는 기술입니다. 기존 RAG 시스템이 유사도 기반으로 문서를 검색하면서 겪는 문맥 손실과 관계 누락 문제를 **지식 그래프(Knowledge Graph)**라는 구조화된 데이터 형태로 해결합니다. 

LLM에게 정확하고 맥락 있는 정보를 전달하려면 단순히 유사한 문서를 모으는 것만으로는 부족합니다. 데이터 간의 관계를 명시적으로 표현하고, 그 관계를 따라 탐색할 수 있어야 합니다. 이것이 GraphRAG가 중요한 이유이며, 이미 Google(2012), Palantier, 미래에셋 등 대규모 기업에서 실무에 적용하고 있습니다.

---

## 배경 / 사전 지식

### RAG(Retrieval-Augmented Generation)란?

RAG는 LLM이 학습 데이터에 없는 정보를 다루도록 외부 문서를 검색해서 제공하는 기법입니다. 기본 흐름은:

1. **사용자 질문** → 2. **유사 문서 검색** → 3. **질문 + 검색 결과를 프롬프트에 포함** → 4. **LLM이 답변 생성**

### 임베딩(Embedding)과 벡터 유사도

데이터를 기계가 이해할 수 있도록 **벡터(숫자 배열)**로 변환하는 과정을 임베딩이라 합니다. 문서와 질문 모두 벡터로 변환 후, 코사인 유사도 같은 수학적 거리를 계산하여 가장 유사한 문서를 찾습니다.

### 엔티티(Entity)와 관계(Relationship)

- **엔티티**: 명사, 구체적인 객체 (사람, 조직, 제품, 프로젝트 등)
- **관계**: 엔티티 간의 연결 (담당, 참여, 포함, 협력 등)

예: "김민수는 결제 시스템 리팩토링을 담당했다"
- 엔티티: 김민수, 결제 시스템 리팩토링
- 관계: 담당하다

---

## 핵심 개념

### 1. 기존 RAG의 한계

#### 문제 1: 청킹으로 인한 문맥 손실

문서를 일정 크기의 청크로 분할할 때, 중요한 조건이 서로 다른 청크에 흩어질 수 있습니다.

**예시:**
```
청크 1: "VIP 고객은 수수료 면제 대상입니다."
청크 2: "단, 해외송금 수수료는 면제 대상이 아닙니다."
청크 3: "2025년 3월 이후 가입자가 이 정책의 적용 대상입니다."
```

질문: "2025년 4월에 가입한 VIP 고객의 해외송금 수수료는 면제되나요?"

청크 1만 검색되면 LLM은 "VIP는 면제된다"고 답하지만, 실제로는 해외송금은 제외됩니다. 문맥이 분산되어 있으면 올바른 답변이 불가능합니다.

#### 문제 2: Top-K 검색의 한계

검색은 가장 유사한 상위 K개(예: K=2)만 반환합니다. 하지만 **정답에 필요한 정보가 3, 4번째에 있을 수 있습니다.**

**예시:**
```
문서 1: "김민수는 결제 시스템 리팩토링을 담당했다."
문서 2: "결제 시스템 리팩토링은 장애율 개선을 위한 프로젝트다."
문서 3: "장애율 개선 프로젝트는 보안팀과 플랫폼팀이 공동으로 진행했다."
```

질문: "김민수와 보안팀은 어떤 관계인가?"

K=2로 설정하고 문서 1, 3이 검색되면, 문서 2가 없어서 **연결고리를 찾을 수 없습니다.** 김민수 → 결제 시스템 리팩토링 → 장애율 개선 → 보안팀 이라는 경로가 끊기는 것입니다.

#### 문제 3: 엔티티 간 관계 누락

유사도 기반 검색은 **문서 자체의 유사도**만 계산하지, **엔티티 간의 관계**는 명시적으로 추론하지 못합니다.

### 2. 지식 그래프(Knowledge Graph) 개념

지식 그래프는 현실의 개체들과 그들 간의 관계를 **구조화된 그래프 형태**로 표현합니다. 세 가지 핵심 요소로 구성됩니다:

#### 노드(Node)
- 현실의 개체, 보통 **명사**에 해당합니다
- 예: 사람(김민수), 조직(보안팀), 프로젝트(결제 시스템 리팩토링), 장소, 개념 등

#### 엣지(Edge)
- 노드 간의 **관계**, 보통 **동사나 서술**에 해당합니다
- 예: "담당하다", "포함된다", "협력한다", "위치한다" 등
- 방향이 있을 수 있습니다 (A → B)

#### 속성(Property/Attribute)
- 노드와 엣지의 **메타데이터**
- 노드의 속성: 나이, 부서, 상태 등
- 엣지의 속성: 시작 날짜, 출처 문서, 신뢰도 등

### 3. 지식 그래프 구축 예시

앞서 본 문장들을 지식 그래프로 표현하면:

```
노드:
  - 김민수 (속성: 나이=34, 주력언어=파이썬)
  - 결제시스템리팩토링 (속성: 상태=진행중)
  - 장애율개선프로젝트 (속성: 목표=가용성향상)
  - 보안팀 (속성: 역할=공동진행팀)
  - 플랫폼팀 (속성: 역할=공동진행팀)

엣지:
  - 김민수 --[담당한다]--> 결제시스템리팩토링 (출처=문서A)
  - 결제시스템리팩토링 --[포함된다]--> 장애율개선프로젝트 (출처=문서B)
  - 보안팀 --[공동진행한다]--> 장애율개선프로젝트 (출처=문서C)
  - 플랫폼팀 --[공동진행한다]--> 장애율개선프로젝트 (출처=문서C)
```

이제 "김민수와 보안팀의 관계"를 물으면:
- 김민수 → 담당 → 결제시스템리팩토링
- 결제시스템리팩토링 → 포함 → 장애율개선프로젝트
- 장애율개선프로젝트 → 공동진행 → 보안팀

AI는 이 **경로를 따라** "김민수는 결제 시스템 리팩토링을 담당했고, 이는 보안팀과 함께 진행한 장애율 개선 프로젝트에 포함되어 있다"는 답변을 생성할 수 있습니다.

### 4. GraphRAG의 핵심 차이

| 구분 | 기존 RAG | GraphRAG |
|------|---------|---------|
| **검색 대상** | 유사한 문서/청크 | 관련 엔티티 + 연결관계 |
| **문맥 보존** | 청크 내에서만 가능 | 다중 홉 탐색으로 광범위 |
| **관계 추론** | 암묵적(LLM 추론) | 명시적(그래프 구조) |
| **확장성** | 새로운 문서마다 재임베딩 | 엔티티/관계 증분 추가 |

---

## 작동 원리

### RAG 시스템 구축 단계 (기존)

1. **데이터 로드**: 원본 문서 수집
2. **청킹(Chunking)**: 문서를 일정 크기로 분할 (예: 512 토큰)
3. **임베딩(Embedding)**: 각 청크를 벡터로 변환
4. **저장(Store)**: 벡터를 벡터 DB(Pinecone, Weaviate 등)에 저장
5. **검색(Retrieval)**: 사용자 쿼리를 임베딩한 후 유사도로 상위 K개 검색
6. **생성(Generation)**: 검색된 청크 + 쿼리를 프롬프트에 포함해 LLM이 답변 생성

### GraphRAG 구축 및 검색 단계

1. **문서 처리**: 원본 텍스트 수집
2. **엔티티 추출(Entity Extraction)**: 
   - LLM을 이용해 각 문장에서 명사/개체 추출
   - 예: "김민수", "결제 시스템 리팩토링"
   
3. **관계 추출(Relation Extraction)**:
   - LLM을 이용해 엔티티 간 관계 추출
   - 예: "김민수" --[담당]-- "결제 시스템 리팩토링"
   
4. **속성 추가(Property Assignment)**:
   - 각 노드와 엣지에 메타데이터 추가
   - 예: 엣지에 "출처=문서A" 추가
   
5. **그래프 저장**: Neo4j, ArangoDB 같은 그래프 DB에 저장

6. **질문 시 검색 프로세스**:
   - **질문 분석**: "김민수와 보안팀의 관계?"
   - **엔티티 인식(Entity Linking)**: "김민수", "보안팀" 식별
   - **그래프 탐색(Graph Traversal)**: 두 엔티티를 연결하는 경로 찾기
   - **경로 설명 생성**: 찾은 경로를 자연어로 해석해 LLM에 전달
   
7. **답변 생성**: LLM이 수집한 관계 정보를 바탕으로 최종 답변 작성

### 실제 검색 예시

질문: "2025년 4월에 가입한 VIP 고객의 해외송금 수수료는?"

**GraphRAG 검색 과정:**
```
1. 엔티티 인식: "VIP 고객", "해외송금 수수료", "2025년 4월 가입"
2. 그래프 탐색:
   VIP고객 --[수수료면제대상]--> 수수료카테고리
   수수료카테고리 --[포함]--> 일반송금수수료 (면제)
   수수료카테고리 --[제외]--> 해외송금수수료 (면제X)
   가입시기 --[적용범위]--> 2025년3월이후
3. 경로 종합: VIP는 면제 BUT 해외송금은 제외 AND 2025년3월 이후 = 조건 만족
4. 결론: 해외송금 수수료는 면제되지 않음
```

---

## 코드 예시

### 예제 1: Neo4j와 LangChain으로 기본 그래프 구축

```python
from langchain.llms import OpenAI
from neo4j import GraphDatabase
from langchain.chains import GraphCypherQAChain

# Neo4j 연결
driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "password")
)

# 간단한 그래프 쿼리 (Cypher)
def create_knowledge_graph():
    """지식 그래프의 노드와 엣지 생성"""
    with driver.session() as session:
        # 노드 생성
        session.run("""
            CREATE (kim:Person {name: '김민수', age: 34, lang: 'Python'})
            CREATE (proj1:Project {name: '결제시스템리팩토링', status: '진행중'})
            CREATE (proj2:Project {name: '장애율개선프로젝트', goal: '가용성향상'})
            CREATE (team1:Team {name: '보안팀'})
            CREATE (team2:Team {name: '플랫폼팀'})
        """)
        
        # 엣지 생성 (관계)
        session.run("""
            MATCH (kim:Person {name: '김민수'}),
                  (proj1:Project {name: '결제시스템리팩토링'})
            CREATE (kim)-[:RESPONSIBLE_FOR {source: 'document_A'}]->(proj1)
        """)
        
        session.run("""
            MATCH (proj1:Project {name: '결제시스템리팩토링'}),
                  (proj2:Project {name: '장애율개선프로젝트'})
            CREATE (proj1)-[:INCLUDED_IN {source: 'document_B'}]->(proj2)
        """)
        
        session.run("""
            MATCH (team1:Team {name: '보안팀'}),
                  (team2:Team {name: '플랫폼팀'}),
                  (proj2:Project {name: '장애율개선프로젝트'})
            CREATE (team1)-[:COLLABORATES_ON {source: 'document_C'}]->(proj2)
            CREATE (team2)-[:COLLABORATES_ON {source: 'document_C'}]->(proj2)
        """)

# LangChain으로 그래프 쿼리 체인 구성
def query_graph(question: str):
    """자연어 질문을 Cypher로 변환하고 답변 생성"""
    llm = OpenAI(temperature=0)
    
    graph = GraphCypherQAChain.from_llm(
        llm=llm,
        graph=driver,  # Neo4j 드라이버 전달
        verbose=True
    )
    
    # 질문 처리
    result = graph.run(question)
    return result

# 실행 예시
if __name__ == "__main__":
    create_knowledge_graph()
    
    # 그래프 기반 질문
    answer = query_graph("김민수와 보안팀의 관계는?")
    print(f"답변: {answer}")
    # 출력: LangChain이 자동으로 Cypher 쿼리를 생성하고,
    # 그래프 탐색 결과를 바탕으로 자연어 답변 생성
```

**코드 설명:**
- `GraphDatabase.driver()`: Neo4j 데이터베이스 연결
- `CREATE (노드:레이블 {속성})`: 노드와 속성 생성
- `CREATE (노드1)-[:관계타입]->(노드2)`: 방향성 엣지 생성
- `GraphCypherQAChain`: LangChain이 자연어를 Cypher(그래프 쿼리 언어)로 자동 변환

### 예제 2: 엔티티 및 관계 자동 추출

```python
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List

# 추출 결과의 구조 정의
class Entity(BaseModel):
    name: str = Field(description="엔티티 이름")
    type: str = Field(description="엔티티 타입 (Person, Project, Team 등)")
    properties: dict = Field(description="속성 딕셔너리")

class Relationship(BaseModel):
    source: str = Field(description="출발 엔티티")
    target: str = Field(description="도착 엔티티")
    relation: str = Field(description="관계 타입")
    source_doc: str = Field(description="출처 문서")

class KnowledgeGraph(BaseModel):
    entities: List[Entity]
    relationships: List[Relationship]

def extract_graph_from_text(text: str) -> KnowledgeGraph:
    """
    텍스트에서 엔티티와 관계를 자동 추출
    """
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    parser = PydanticOutputParser(pydantic_object=KnowledgeGraph)
    
    prompt = PromptTemplate(
        template="""
        다음 텍스트에서 엔티티(개체)와 그들 간의 관계를 추출하세요.
        
        엔티티는 사람, 조직, 프로젝트, 팀 등의 명사입니다.
        관계는 엔티티 간의 동작이나 연결입니다 (예: 담당, 참여, 포함).
        
        텍스트:
        {text}
        
        {format_instructions}
        """,
        input_variables=["text"],
        partial_variables={
            "format_instructions": parser.get_format_instructions()
        }
    )
    
    chain = prompt | llm | parser
    result = chain.invoke({"text": text})
    return result

# 사용 예시
text = """
김민수는 결제 시스템 리팩토링을 담당했다.
결제 시스템 리팩토링은 장애율 개선을 위한 프로젝트였다.
이 장애율 개선 프로젝트는 보안팀과 플랫폼팀이 공동으로 진행했다.
"""

graph = extract_graph_from_text(text)

print("추출된 엔티티:")
for entity in graph.entities:
    print(f"  - {entity.name} ({entity.type}): {entity.properties}")

print("\n추출된 관계:")
for rel in graph.relationships:
    print(f"  - {rel.source} --[{rel.relation}]--> {rel.target}")
```

**코드 설명:**
- `BaseModel` 기반의 구조화된 출력 정의로 LLM 결과를 자동 파싱
- LangChain의 `PydanticOutputParser`가 LLM 답변을 JSON으로 변환
- 이 구조화된 데이터를 Neo4j에 직접 저장 가능

### 예제 3: 그래프 기반 경로 탐색

```python
def find_relationship_path(start_entity: str, end_entity: str, max_hops: int = 3):
    """
    두 엔티티 간의 최단 경로 찾기
    """
    query = """
    MATCH path = shortestPath(
        (start)-[*1..{max_hops}]-(end)
    )
    WHERE start.name = $start_entity AND end.name = $end_entity
    RETURN path
    LIMIT 1
    """
    
    with driver.session() as session:
        result = session.run(
            query,
            start_entity=start_entity,
            end_entity=end_entity,
            max_hops=max_hops
        )
        
        for record in result:
            path = record["path"]
            # 경로를 자연어로 해석
            nodes = path.nodes
            rels = path.relationships
            
            explanation = f"{nodes[0]['name']}"
            for i, rel in enumerate(rels):
                explanation += f" --[{rel.type}]--> {nodes[i+1]['name']}"
            
            return explanation
    
    return "경로를 찾을 수 없습니다."

# 사용
path = find_relationship_path("김민수", "보안팀")
print(f"찾은 경로: {path}")
# 출력: 김민수 --[RESPONSIBLE_FOR]--> 결제시스템리팩토링 --[INCLUDED_IN]--> 장애율개선프로젝트 --[COLLABORATES_ON]--> 보안팀
```

---

## 함정·실수

### 1. 과도한 엔티티 추출로 인한 노이즈

**문제:** LLM에게 모든 명사를 엔티티로 추출하도록 하면, 중요하지 않은 것까지 노드로 생성됩니다.

예: "서울의 은행 지점에서 결제 시스템을 개선했다" 
- 과도 추출: 서울, 은행, 지점, 결제시스템, 개선 등 모두 노드화
- 결과: 그래프가 과도하게 복잡해지고 검색 성능 저하

**해결책:**
```python
# 도메인 특화 엔티티 타입만 추출하도록 제한
ENTITY_TYPES = ["Person", "Team", "Project", "Process"]  # 금융 도메인 기준

# 프롬프트에 명시
prompt = """
다음 타입의 엔티티만 추출하세요: {ENTITY_TYPES}
장소(도시, 주소)와 일반 동사는 제외하세요.
"""
```

### 2. 자동 추출의 일관성 부족

**문제:** 동일한 개체가 다른 이름으로 표현될 수 있습니다.

예: "김민수", "민수", "K. 민수", "엔지니어 김민수"

LLM이 이들을 다른 엔티티로 인식하면 그래프가 분산되어 탐색 실패.

**해결책:**
```python
# 엔티티 정규화(Canonicalization)
def normalize_entities(graph: KnowledgeGraph) -> KnowledgeGraph:
    """동일 개체의 별칭 통합"""
    
    # 유사도 기반 병합
    from difflib import SequenceMatcher
    
    entity_mapping = {}
    for i, e1 in enumerate(graph.entities):
        for e2 in graph.entities[i+1:]:
            ratio = SequenceMatcher(None, e1.name, e2.name).ratio()
            if ratio > 0.8:  # 80% 이상 유사
                # e2를 e1로 통합
                entity_mapping[e2.name] = e1.name
    
    # 통합된 이름으로 관계 업데이트
    for rel in graph.relationships:
        rel.source = entity_mapping.get(rel.source, rel.source)
        rel.target = entity_mapping.get(rel.target, rel.target)
    
    return graph
```

### 3. Top-K 설정 여전히 필요

**문제:** GraphRAG가 모든 엔티티를 탐색하지는 않습니다.

큰 그래프에서 모든 경로를 탐색하면 응답 시간이 급증합니다.

**해결책:**
```python
# 최대 홉 수 제한 (3~5 홉 권장)
query = """
MATCH path = shortestPath(
    (start)-[*1..3]-(end)  -- 최대 3홉까지만
)
WHERE start.name = $entity AND length(path) < 10  -- 경로 길이도 제한
RETURN path
"""

# 관련성 스코어링으로 우선순위 결정
def score_path(path, query_context):
    """경로의 관련성 점수 계산"""
    score = 0
    for rel in path.relationships:
        # 엣지의 출처 신뢰도 확인
        if rel['source_doc'] in query_context.get('relevant_docs', []):
            score += 10
        # 관계 타입의 관련성
        if rel['type'] in query_context.get('important_relations', []):
            score += 5
    return score
```

### 4. 부정(Negation) 처리 누락

**문제:** "A는 B를 담당하지 않는다"는 관계도 명시적으로 저장해야 합니다.

자동 추출 시 부정은 보통 무시됩니다.

**예시 오류:**
```
"VIP 고객의 해외송금 수수료는 면제되지 않는다"
→ 자동 추출하면: VIP --[면제]--> 해외송금수수료 (부정이 손실)
```

**해결책:**
```python
# 관계에 명시적 속성 추가
session.run("""
    CREATE (vip:Customer {name: 'VIP'})-[:EXEMPTED {
        category: '수수료',
        exemption_type: '모든 수수료'
    }]->(fee:Category)
    CREATE (vip)-[:NOT_EXEMPTED {
        category: '수수료',
        specific_type: '해외송금'
    }]->(intl_fee:Category)
""")

# 검색 시 부정 관계도 확인
query = """
MATCH (customer)-[pos:EXEMPTED|NOT_EXEMPTED]->(fee)
WHERE customer.name = '2025년4월가입VIP'
RETURN pos.type, pos.specific_type
"""
```

---

## 베스트 프랙티스

### 1. 엔티티 추출 파이프라인 설계

```python
# 단계별 검증 프로세스
def robust_entity_extraction(text: str):
    """
    1단계: 초기 추출 (LLM)
    2단계: 도메인 필터링 (화이트리스트)
    3단계: 정규화 (정규식, 임베딩 기반)
    4단계: 중복 제거 및 병합
    5단계: 수동 검증 (중요 도메인)
    """
    
    # 1단계
    raw_entities = llm_extract(text)
    
    # 2단계: 도메인 관련 엔티티만 유지
    filtered = [e for e in raw_entities 
                if e.type in APPROVED_ENTITY_TYPES]
    
    # 3단계: 정규화
    normalized = [normalize_entity_name(e) for e in filtered]
    
    # 4단계: 임베딩 기반 중복 제거
    unique_entities = deduplicate_by_embedding(normalized)
    
    # 5단계: 검증
    if HIGH_STAKES_DOMAIN:
        unique_entities = human_review(unique_entities)
    
    return unique_entities
```

### 2. 점진적 그래프 구축

작은 규모로 시작해서 점진적으로 확장:

```python
# 단계 1: 핵심 엔티티만 (100-500개)
# 단계 2: 주요 관계 추가 (검증됨)
# 단계 3: 속성 풍부화
# 단계 4: 엣지 케이스 추가 (부정, 조건부, 시간적 관계)

def phased_graph_build(documents: List[str], phase: int = 1):
    if phase >= 1:
        # 핵심 엔티티
        extract_critical_entities(documents)
    if phase >= 2:
        # 주요 관계 (빈도 상위 10)
        extract_frequent_relations(documents)
    if phase >= 3:
        # 속성 추가
        enrich_entity_properties(documents)
    if phase >= 4:
        # 복잡한 관계 (부정, 조건)
        extract_complex_relations(documents)
```

### 3. 그래프 품질 모니터링

```python
def quality_metrics():
    """그래프 품질 지표"""
    
    # 1. 엔티티 분포 균형
    entity_dist = graph.query("MATCH (n) RETURN labels(n), count(*)")
    
    # 2. 경로 가능성 확인
    disconnected = graph.query(
        "MATCH (n) WHERE NOT (n)--() RETURN count(n)"
    )
    
    # 3. 관계 타입 다양성
    relation_types = graph.query(
        "MATCH ()-[r]->() RETURN type(r), count(*)"
    )
    
    # 4. 속성 채워짐 비율
    property_fill_rate = graph.query(
        "MATCH (n) RETURN count(keys(n)) / count(*)"
    )
    
    print(f"고아 노드(고립된 노드): {disconnected}")
    print(f"관계 타입 수: {len(relation_types)}")
    print(f"평균 노드당 관계 수: {avg_degree}")
```

### 4. 하이브리드 검색

GraphRAG만으로 부족할 수 있으니 RAG와 병합:

```python
def hybrid_search(query: str):
    """
    그래프 기반 + 벡터 기반 검색 통합
    """
    
    # 1. 그래프 기반 검색 (구조적 정보)
    graph_results = graph_search(query)
    
    # 2. 벡터 기반 검색 (의미적 유사도)
    vector_results = vector_search(query)
    
    # 3. 결합
    combined = merge_and_rank([
        *graph_results,      # 신뢰도 높음
        *vector_results      # 보충
    ])
    
    # 4. LLM이 통합 정보 기반 답변
    answer = llm.generate(
        query=query,
        context=combined[:K]  # 상위 K개
    )
    return answer
```

### 5. 동적 업데이트

새로운 문서 추가 시 전체 재구축하지 말고 증분 업데이트:

```python
def incremental_update(new_document: str):
    """새 문서만 추출해서 그래프에 병합"""
    
    # 1. 새 엔티티/관계만 추출
    new_entities = extract_entities(new_document)
    new_relations = extract_relations(new_document)
    
    # 2. 기존 그래프와 병합
    for entity in new_entities:
        existing = find_similar_entity(entity)
        if existing:
            merge_entities(existing, entity)  # 속성 통합
        else:
            graph.create_node(entity)  # 신규 추가
    
    # 3. 새 관계 추가 (중복 확인)
    for relation in new_relations:
        if not graph.has_relation(relation):
            graph.create_edge(relation)
    
    # 4. 간단한 검증
    graph.validate_consistency()
```

---

## 참고

### 영상 내 언급 자료

1. **Google Knowledge Graph (2012)**
   - 구글에서 최초로 구축한 대규모 지식 그래프
   - 사용자 검색 시 우측에 표시되는 정보 카드의 기반
   - 현재 수십억 개 엔티티 관리

2. **Palantir Ontology**
   - Palantir Technologies의 데이터 통합 솔루션
   - 엔터프라이즈급 온톨로지 구축 플랫폼
   - 주가 상승으로 주목받으면서 그래프 기술의 가치 부상

3. **AWS Summit Seoul 2026 - 미래에셋 사례**
   - 미래에셋 증권의 금융 상품 검색 시스템
   - GraphRAG로 복잡한 상품 관계 구조화
   - 고객 및 직원의 정보 탐색 개선 사례

4. **시장 전망 (Gartner Hype Cycle)**
   - 2024년: 약 11억 달러 규모
   - 2030년: 약 69억 달러 규모 (연평균 45% 성장 예상)
   - 현재는 하이프 사이클의 성숙 단계로 진입 중

### 추가 학습 자료 (영상 내 명시 없음)

- **Neo4j 공식 문서**: https://neo4j.com/developer/
  - Cypher 쿼리 언어 튜토리얼
  - 그래프 데이터 모델링 가이드
  
- **LangChain GraphCypherQAChain**:
  - 자연어 → Cypher 자동 변환
  - LLM 기반 그래프 인터페이싱
  
- **엔티티/관계 추출 모델**:
  - SpaCy (오픈소스 NLP)
  - Hugging Face Transformers (사전학습 모델)
  - OpenAI Function Calling (상용)

### 실습 환경 구성

```bash
# Neo4j 설치 (Docker)
docker run --name neo4j -p 7687:7687 -p 7474:7474 \
  -e NEO4J_AUTH=neo4j/password \
  neo4j:latest

# Python 라이브러리
pip install langchain neo4j openai

# 테스트 연결
python -c "from neo4j import GraphDatabase; print('OK')"
```