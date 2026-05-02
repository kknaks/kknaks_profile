---
title: '[네트워크] 동기처리와 비동기처리'
date: 2025.07.21
tags:
- CS지식, 네트워크
stack: []
links: []
---

# 동기 처리 VS 비동기 처리 상세 비교

## 1. 기본 개념

### 동기 처리 (Synchronous)
- **정의**: 작업이 **순차적으로 실행**되며, 하나의 작업이 완료될 때까지 **다음 작업을 기다리는** 방식
- **특징**: 작업의 완료를 기다리는 동안 **블로킹(Blocking)** 상태가 됨
- **실행 흐름**: A 작업 시작 → A 작업 완료까지 대기 → B 작업 시작 → B 작업 완료까지 대기

### 비동기 처리 (Asynchronous)  
- **정의**: 작업을 **동시에 시작**하고, 완료를 **기다리지 않고** 다른 작업을 계속 수행하는 방식
- **특징**: I/O 대기 시간에 **논블로킹(Non-blocking)** 상태로 다른 작업 처리
- **실행 흐름**: A, B 작업 동시 시작 → 각각 완료되는 대로 결과 처리

## 2. 코드 비교

### 동기 처리 예제
```python
import time
import requests

def sync_api_calls():
    print("🔄 동기 처리 시작")
    start_time = time.time()
    
    # 첫 번째 API 호출 (2초 대기)
    print("📞 사용자 정보 API 호출 시작...")
    response1 = requests.get("https://api.example.com/users/1")  # 2초 대기
    print("✅ 사용자 정보 응답 완료")
    
    # 두 번째 API 호출 (3초 대기)  
    print("📞 포트폴리오 정보 API 호출 시작...")
    response2 = requests.get("https://api.example.com/portfolio/1")  # 3초 대기
    print("✅ 포트폴리오 정보 응답 완료")
    
    # 세 번째 API 호출 (1초 대기)
    print("📞 면접 기록 API 호출 시작...")
    response3 = requests.get("https://api.example.com/interviews/1")  # 1초 대기
    print("✅ 면접 기록 응답 완료")
    
    end_time = time.time()
    print(f"⏱️ 총 소요 시간: {end_time - start_time:.2f}초")  # 약 6초
    
    return {
        "user": response1.json(),
        "portfolio": response2.json(), 
        "interviews": response3.json()
    }

# 실행 결과:
# 🔄 동기 처리 시작
# 📞 사용자 정보 API 호출 시작...
# ✅ 사용자 정보 응답 완료        (2초 후)
# 📞 포트폴리오 정보 API 호출 시작...
# ✅ 포트폴리오 정보 응답 완료    (5초 후)
# 📞 면접 기록 API 호출 시작...
# ✅ 면접 기록 응답 완료         (6초 후)
# ⏱️ 총 소요 시간: 6.00초
```

### 비동기 처리 예제
```python
import asyncio
import aiohttp
import time

async def async_api_calls():
    print("🚀 비동기 처리 시작")
    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        # 모든 API 호출을 동시에 시작
        print("📞 모든 API 호출 동시 시작...")
        
        tasks = [
            fetch_user_info(session),      # 2초 소요
            fetch_portfolio_info(session), # 3초 소요  
            fetch_interview_info(session)  # 1초 소요
        ]
        
        # 모든 작업이 완료될 때까지 기다림 (가장 긴 작업 기준)
        user_data, portfolio_data, interview_data = await asyncio.gather(*tasks)
        
        end_time = time.time()
        print(f"⏱️ 총 소요 시간: {end_time - start_time:.2f}초")  # 약 3초
        
        return {
            "user": user_data,
            "portfolio": portfolio_data,
            "interviews": interview_data
        }

async def fetch_user_info(session):
    print("📞 사용자 정보 API 호출 시작...")
    async with session.get("https://api.example.com/users/1") as response:
        await asyncio.sleep(2)  # API 응답 시뮬레이션
        print("✅ 사용자 정보 응답 완료")
        return await response.json()

async def fetch_portfolio_info(session):
    print("📞 포트폴리오 정보 API 호출 시작...")
    async with session.get("https://api.example.com/portfolio/1") as response:
        await asyncio.sleep(3)  # API 응답 시뮬레이션
        print("✅ 포트폴리오 정보 응답 완료")
        return await response.json()

async def fetch_interview_info(session):
    print("📞 면접 기록 API 호출 시작...")
    async with session.get("https://api.example.com/interviews/1") as response:
        await asyncio.sleep(1)  # API 응답 시뮬레이션
        print("✅ 면접 기록 응답 완료")
        return await response.json()

# 실행 결과:
# 🚀 비동기 처리 시작
# 📞 모든 API 호출 동시 시작...
# 📞 사용자 정보 API 호출 시작...
# 📞 포트폴리오 정보 API 호출 시작...
# 📞 면접 기록 API 호출 시작...
# ✅ 면접 기록 응답 완료         (1초 후)
# ✅ 사용자 정보 응답 완료        (2초 후)
# ✅ 포트폴리오 정보 응답 완료    (3초 후)
# ⏱️ 총 소요 시간: 3.00초
```

## 3. FastAPI에서의 실제 적용

### 동기 방식의 문제점
```python
from fastapi import FastAPI
import requests
import time

app = FastAPI()

@app.post("/interview/score")  # async 없음
def score_interview_sync(interview_data: dict):
    """동기 방식 - 문제가 있는 코드"""
    
    # LLM API 호출 (3초 소요)
    llm_response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        json={"model": "gpt-4", "messages": [...]},
        headers={"Authorization": "Bearer xxx"}
    )
    
    # 포트폴리오 분석 API 호출 (2초 소요)
    portfolio_analysis = requests.post(
        "https://api.portfolio-analyzer.com/analyze",
        json={"portfolio": interview_data["portfolio"]}
    )
    
    # 총 5초 소요, 이 시간 동안 서버는 다른 요청을 처리할 수 없음!
    return {
        "score": llm_response.json()["score"],
        "analysis": portfolio_analysis.json()
    }
```

### 비동기 방식의 해결
```python
import asyncio
import aiohttp
from fastapi import FastAPI

app = FastAPI()

@app.post("/interview/score")  # async 추가!
async def score_interview_async(interview_data: dict):
    """비동기 방식 - 개선된 코드"""
    
    async with aiohttp.ClientSession() as session:
        # 두 API를 동시에 호출
        tasks = [
            call_llm_api(session, interview_data),
            analyze_portfolio(session, interview_data["portfolio"])
        ]
        
        # 두 작업이 모두 완료될 때까지 기다림 (3초, 가장 긴 작업 기준)
        llm_result, portfolio_result = await asyncio.gather(*tasks)
        
        return {
            "score": llm_result["score"],
            "analysis": portfolio_result
        }

async def call_llm_api(session, data):
    """LLM API 비동기 호출"""
    async with session.post(
        "https://api.openai.com/v1/chat/completions",
        json={"model": "gpt-4", "messages": [...]},
        headers={"Authorization": "Bearer xxx"}
    ) as response:
        return await response.json()

async def analyze_portfolio(session, portfolio):
    """포트폴리오 분석 API 비동기 호출"""
    async with session.post(
        "https://api.portfolio-analyzer.com/analyze",
        json={"portfolio": portfolio}
    ) as response:
        return await response.json()
```

## 4. 성능 비교 시뮬레이션

### 동시 요청 시나리오
```python
# 시나리오: 10명이 동시에 면접 채점 요청

# 동기 방식 결과:
# 요청 1: 0~5초 처리
# 요청 2: 5~10초 처리  
# 요청 3: 10~15초 처리
# ...
# 요청 10: 45~50초 처리
# 총 소요 시간: 50초

# 비동기 방식 결과:
# 요청 1~10: 모두 0초에 시작
# 모든 요청: 3초에 완료 (가장 긴 작업 기준)
# 총 소요 시간: 3초

# 성능 향상: 약 16.7배!
```

## 5. 비동기 방식이 필요한 경우

### ✅ 비동기가 유리한 경우
- **I/O 바운드 작업이 많을 때**
  - 데이터베이스 쿼리
  - 외부 API 호출 (LLM, 결제, 이메일 등)
  - 파일 읽기/쓰기
  - 네트워크 통신
  
- **높은 동시성이 필요할 때**
  - 많은 사용자가 동시에 접속
  - 실시간 채팅, 알림 서비스
  - 마이크로서비스 간 통신

### ❌ 비동기가 불필요한 경우
- **CPU 집약적 작업**
  - 복잡한 수학 계산
  - 이미지/영상 처리
  - 데이터 암호화/복호화
  
- **간단한 CRUD 작업**
  - 단순한 데이터베이스 조회
  - 캐시에서 데이터 읽기

## 6. 주의사항

### 비동기 코드 작성 시 주의점
```python
# ❌ 잘못된 예시 - 동기 함수를 async로 감싸기만 함
async def wrong_async():
    time.sleep(2)  # 여전히 블로킹!
    return "완료"

# ✅ 올바른 예시 - 실제 비동기 함수 사용
async def correct_async():
    await asyncio.sleep(2)  # 논블로킹
    return "완료"

# ❌ 잘못된 예시 - 순차적 await
async def wrong_sequential():
    result1 = await api_call_1()  # 2초
    result2 = await api_call_2()  # 3초 
    return result1, result2       # 총 5초

# ✅ 올바른 예시 - 병렬 처리
async def correct_parallel():
    task1 = asyncio.create_task(api_call_1())  # 동시 시작
    task2 = asyncio.create_task(api_call_2())  # 동시 시작
    return await asyncio.gather(task1, task2)  # 총 3초
```


# FastAPI 비동기 처리 레이어 구조

## 🏗️ Controller Layer (API Router)

```python
@router.post("/backtest/start")
async def start_backtest(request: BackTestRequest):
    """
    🎯 역할: HTTP 요청 받고 응답 반환
    ✅ 핵심: async def로 선언하면 자동으로 비동기 처리
    """
    try:
        # 서비스 레이어 호출 (await 필수)
        result = await backtest_service.run_backtest_async(request)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## 🔧 Service Layer (Business Logic)

```python
class BackTestService:
    async def run_backtest_async(self, request: BackTestRequest):
        """
        🎯 역할: 비즈니스 로직 처리 + 여러 레포지토리 조합
        ✅ 핵심: asyncio.gather로 병렬 처리
        """
        
        # 1. 여러 데이터 소스에서 동시에 데이터 수집
        stock_data, financial_data, market_data = await asyncio.gather(
            self.stock_repo.get_stock_data_async(request.start_date),
            self.financial_repo.get_financial_statements_async(request.companies),
            self.market_repo.get_market_data_async(request.date_range),
            return_exceptions=True
        )
        
        # 2. 데이터 검증
        if not self._validate_data(stock_data, financial_data):
            raise ValueError("Invalid data")
        
        # 3. 백테스트 실행 (CPU 집약적 작업은 동기로)
        backtest_results = self._run_backtest_calculation(
            stock_data, financial_data, request.criteria
        )
        
        # 4. 결과 저장 (비동기)
        await self.result_repo.save_results_async(backtest_results)
        
        return backtest_results

    def _run_backtest_calculation(self, stock_data, financial_data, criteria):
        """
        🎯 CPU 집약적 작업은 동기로 처리
        ✅ 계산 로직은 굳이 비동기 안 해도 됨
        """
        # 복잡한 계산 로직...
        return results
```

## 💾 Repository Layer (Data Access)

```python
class StockRepository:
    def __init__(self):
        self.session = aiohttp.ClientSession()  # 비동기 HTTP 클라이언트
    
    async def get_stock_data_async(self, date: str):
        """
        🎯 역할: 외부 API 호출
        ✅ 핵심: I/O 바운드 작업을 비동기로
        """
        
        # 여러 API를 동시에 호출
        kospi_task = self._fetch_kospi_async(date)
        kosdaq_task = self._fetch_kosdaq_async(date)
        
        # 두 API 결과를 동시에 기다림
        kospi_data, kosdaq_data = await asyncio.gather(
            kospi_task, 
            kosdaq_task,
            return_exceptions=True
        )
        
        return self._merge_data(kospi_data, kosdaq_data)
    
    async def _fetch_kospi_async(self, date: str):
        """실제 API 호출"""
        async with self.session.get(f"{API_URL}/kospi", params={"date": date}) as response:
            return await response.json()
    
    async def _fetch_kosdaq_async(self, date: str):
        """실제 API 호출"""  
        async with self.session.get(f"{API_URL}/kosdaq", params={"date": date}) as response:
            return await response.json()

class FinancialRepository:
    async def get_financial_statements_async(self, companies: List[str]):
        """
        🎯 역할: 여러 기업의 재무제표를 동시에 가져오기
        ✅ 핵심: 많은 API 호출을 병렬로
        """
        
        # 동시 요청 수 제한 (세마포어)
        semaphore = asyncio.Semaphore(10)
        
        async def fetch_company_data(company_code):
            async with semaphore:  # 동시 요청 수 제한
                return await self._fetch_single_company_async(company_code)
        
        # 모든 기업 데이터를 동시에 요청
        tasks = [fetch_company_data(company) for company in companies]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return self._process_results(results)
```

## 🔄 실행 흐름 예시

```python
# 1. 사용자 요청
POST /api/v1/backtest/start
{
  "companies": ["005930", "000660", "035420"],  # 삼성전자, SK하이닉스, NAVER
  "start_date": "20240101",
  "end_date": "20241231"
}

# 2. Controller → Service → Repository 흐름
Controller: async def start_backtest() 시작
    ↓ await
Service: async def run_backtest_async() 시작
    ↓ await asyncio.gather()
Repository: 
    - stock_repo.get_stock_data_async()     ← 병렬 실행
    - financial_repo.get_statements_async() ← 병렬 실행  
    - market_repo.get_market_data_async()   ← 병렬 실행
    
    각 Repository 내부에서도:
    - KRX API 호출 (KOSPI + KOSDAQ)        ← 병렬 실행
    - DART API 호출 (3개 기업 동시)       ← 병렬 실행
    - 기타 외부 API들                     ← 병렬 실행

# 3. 결과 조합 후 응답
```

## 🎯 핵심 패턴 정리

### ✅ 꼭 알아야 할 3가지

1. **async/await**: 함수를 비동기로 만들기
   ```python
   async def my_function():
       result = await some_async_operation()
   ```

2. **asyncio.gather()**: 여러 작업 동시 실행
   ```python
   results = await asyncio.gather(task1, task2, task3)
   ```

3. **Semaphore**: 동시 실행 수 제한
   ```python
   semaphore = asyncio.Semaphore(5)  # 최대 5개만 동시 실행
   async with semaphore:
       await api_call()
   ```

### 📋 레이어별 책임

| Layer | 역할 | 비동기 사용 이유 |
|-------|------|------------------|
| **Controller** | HTTP 요청/응답 처리 | FastAPI가 자동으로 처리 |
| **Service** | 비즈니스 로직 + 조합 | 여러 Repository 병렬 호출 |
| **Repository** | 데이터 접근 | 외부 API/DB 호출 최적화 |

### 🚨 주의사항

```python
# ❌ 잘못된 방식
def sync_function():
    result = await async_function()  # SyntaxError!

# ❌ 성능 낭비
async def bad_example():
    result1 = await api1()  # 순차 실행
    result2 = await api2()  # 순차 실행
    
# ✅ 올바른 방식  
async def good_example():
    result1, result2 = await asyncio.gather(
        api1(),  # 병렬 실행
        api2()   # 병렬 실행
    )
```

이 3가지 패턴만 알면 FastAPI 비동기 처리는 충분해요! 🚀