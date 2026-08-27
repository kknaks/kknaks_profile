---
type: content
id: C-010
date: 2026-05-11
duration: '2:37'
speaker: 해피AI | HAPPY AI
kind: study
youtubeId: 7XZoK_a7Fxg
title:
  en: 'LoRA Fine-Tuning: Efficient Model Adaptation with Low-Rank Matrices'
  ko: 'LoRA 파인튜닝: 저차원 행렬로 효율적으로 모델 조정하기'
summary:
  en: 'Master LoRA: update just 0.1–1% of parameters via low-rank matrices to efficiently fine-tune large language models without full retraining.'
  ko: 전체 파라미터가 아닌 0.1~1% 저차원 행렬만 학습해 모델을 효율적으로 파인튜닝하는 LoRA의 핵심 원리를 입문자 관점에서 설명한다.
tags:
- '#lora'
- '#fine-tuning'
- '#parameter-efficiency'
- '#low-rank-adaptation'
- '#llm'
- '#deep-learning'
---

## 요지

- LoRA는 복잡한 파라미터를 저차원의 간단한 구조로 근사하면서 효율적으로 조정하는 파인튜닝 기법이다.
- 기존 가중치는 완전히 고정하고 A×B 저차원 랭크 행렬만 추가해 그 부분만 학습한다.
- 기존 파라미터의 0.1~1%만 업데이트해도 전체 모델의 성능을 크게 향상시킬 수 있다.
- 건물 인테리어에서 조명이나 커튼 같은 핵심 요소만 바꿔도 전체 분위기가 달라지는 것처럼, 최소한의 조정으로 최대의 효과를 낸다.
- Full Fine-Tuning(전체 파라미터 업데이트)과 달리 LoRA는 메모리와 계산 비용을 극적으로 절감한다.

## 개요

LoRA(Low-Rank Adaptation)는 LLM과 같은 대규모 신경망을 파인튜닝할 때 전체 모델이 아닌 극히 일부 파라미터만 학습하는 기법이다. 왜 이것이 중요할까? 사전학습된 대규모 모델을 완전히 재학습하려면 수백 GB의 GPU 메모리와 막대한 계산 비용이 필요하다. LoRA를 사용하면 기존 파라미터의 0.1~1% 정도만 업데이트해도 모델의 성능을 크게 향상시킬 수 있다. 이는 개인 개발자나 소규모 팀도 70억 개 파라미터를 가진 대규모 모델을 자신의 데이터에 맞게 효율적으로 조정할 수 있게 해준다.

## 배경 / 사전 지식

### 파인튜닝(Fine-Tuning)
사전학습된 모델을 특정 태스크나 도메인에 맞게 재학습하는 과정이다. 초기값으로 학습된 가중치를 시작점으로 삼아 새로운 데이터에서 추가 학습을 진행한다. 처음부터 모델을 학습시키는 것(cold start)보다 훨씬 효율적이고 적은 데이터로도 좋은 성능을 낸다.

### 파라미터(Parameter)
신경망의 가중치(weight)와 편향(bias) 같은 학습 가능한 수치들이다. LLM의 경우 수십억~수천억 개의 파라미터를 가지며, 이들이 모델의 "지식"을 담고 있다고 할 수 있다. 파인튜닝은 이 파라미터들을 새로운 목표에 맞게 조정하는 과정이다.

### 랭크(Rank)
선형대수에서 행렬의 복잡도나 정보 함유량을 나타내는 지표이다. 낮은 랭크는 행렬이 단순한 구조를 가진다는 의미이고, 높은 랭크는 복잡하고 풍부한 정보를 담고 있다는 의미이다. 예를 들어 1×100 크기의 행렬은 랭크가 최대 1이지만, 100×100 크기의 정사각 행렬은 랭크가 최대 100이 될 수 있다.

### 저차원(Low-Dimension)
원래보다 적은 수의 차원으로 축약하거나 표현하는 상태를 의미한다. 고차원의 복잡한 정보를 저차원의 단순한 형태로 근사(approximation)하면 계산 효율성이 높아지고 메모리 사용량이 줄어든다.

## 핵심 개념

### LoRA의 정의
LoRA는 "Low-Rank Adaptation"의 약자로, 복잡한 파라미터 변화를 저차원의 간단한 구조로 표현하면서 효율적으로 모델을 조정하는 파인튜닝 방식이다. 핵심 아이디어는 다음과 같다: 사전학습된 모델의 무거운 가중치 행렬 W 대신, 두 개의 가벼운 저차원 행렬 A와 B의 곱으로 필요한 변경사항을 표현한다는 것이다.

수식으로는 다음과 같이 표현할 수 있다:
- 기존 방식: 출력 = W·x
- LoRA 방식: 출력 = W·x + ΔW·x = W·x + (A·B)·x

여기서 W는 고정되고, A와 B만 학습된다.

### Full Fine-Tuning vs. LoRA

**Full Fine-Tuning**은 기존 모델의 모든 파라미터를 업데이트한다. 예를 들어 70억 개의 파라미터를 가진 모델이라면 70억 개 모두를 역전파를 통해 학습해야 한다. 이 방식은 다음과 같은 문제가 있다:
- 엄청난 메모리 필요: 최신 고사양 GPU도 감당하기 어려움
- 긴 학습 시간: 모든 파라미터를 업데이트해야 하므로 시간이 오래 걸림
- 높은 비용: 강력한 하드웨어를 오래 사용해야 함

**LoRA**는 다음과 같이 동작한다:
- 기존 가중치 W를 완전히 고정(freeze)시켜 업데이트하지 않음
- 그 위에 새로운 저차원 행렬 A(크기: m×r)와 B(크기: r×n)만 추가
- 오직 A와 B의 파라미터만 학습 대상으로 함
- 결과적으로 기존 파라미터의 0.1%~1% 정도만 업데이트

예시: 원래 가중치가 10,000×10,000 크기라면
- Full Fine-Tuning: 1억 개 파라미터 학습
- LoRA (r=64): 약 128만 개 파라미터만 학습 (약 1.3%)

### 저차원 구조의 원리

LoRA의 핵심은 "모든 필요한 변경이 저차원 구조로 표현될 수 있다"는 가정에 있다. 이는 수학적 배경이 다음과 같다:

파인튜닝 과정에서 나타나는 가중치의 변화(ΔW)가 높은 내재적 차원성(intrinsic dimensionality)을 가지지 않는다는 의미이다. 즉, 매우 큰 행렬이지만 실제로는 낮은 차원의 정보 구조로 표현할 수 있다는 것이다.

r을 "LoRA 랭크"라고 부르는데, 이는 저차원 공간의 크기를 결정한다:
- r이 작을수록: 메모리 효율적이지만 표현력이 떨어질 수 있음
- r이 클수록: 더 복잡한 변화를 표현할 수 있지만 효율성이 떨어짐
- 실제로는 r=8~64 범위에서 충분한 경우가 대부분

## 작동 원리

### 1단계: 모델 준비 및 동결
먼저 사전학습된 모델을 불러온다. 이 모델의 모든 기존 가중치를 동결하는데, 이는 파인튜닝 과정에서 이들이 변하지 않도록 `requires_grad = False` 설정을 통해 이루어진다.

### 2단계: LoRA 행렬 추가
동결된 가중치 W 위에 두 개의 작은 행렬을 추가한다:
- **행렬 A**: 크기 m×r, 가우시안 정규분포로 초기화
- **행렬 B**: 크기 r×n, 0으로 초기화 (초기에 변화가 0이 되도록)

ここで m은 입력 차원, n은 출력 차원, r은 LoRA 랭크(m, n보다 훨씬 작음)이다.

### 3단계: 순전파(Forward Pass)
모델의 입력 x에 대해 출력을 계산한다:
```
최종 출력 = W·x + α·A·B·x
```

α는 스케일링 인자로, LoRA의 영향력을 조절한다. 보통 α/r 형태로 정규화된다.

### 4단계: 역전파(Backward Pass)
손실함수로부터 그래디언트를 계산할 때, W의 그래디언트는 계산되지 않는다(동결되어 있으므로). 오직 A와 B의 그래디언트만 계산되고 업데이트된다.

### 5단계: 파라미터 업데이트
옵티마이저(예: Adam)를 사용해 A와 B의 파라미터만 업데이트한다. 수만 번의 이터레이션 후, A와 B는 특정 태스크에 최적화된 값으로 변환된다.

### 6단계: 추론 및 배포
학습이 완료된 후에는 여러 방식으로 사용할 수 있다:
- **방식 1**: A와 B를 분리해서 관리. 필요할 때만 메모리에 로드해서 적용
- **방식 2**: A×B를 계산해서 W에 병합(merge)한 후 단일 모델 파일로 저장

병합하는 경우: W_final = W + α·A·B

## 코드 예시

### PyTorch를 사용한 LoRA 구현

```python
import torch
import torch.nn as nn

# LoRA가 적용된 선형 계층
class LoRALinear(nn.Module):
    def __init__(self, in_features, out_features, lora_rank=8, lora_alpha=16):
        super().__init__()
        
        # 기존 선형 계층 (동결됨)
        self.linear = nn.Linear(in_features, out_features)
        self.linear.weight.requires_grad = False  # 가중치 고정
        self.linear.bias.requires_grad = False
        
        # LoRA: 저차원 행렬 A와 B
        # A: in_features → lora_rank (차원 축소)
        self.lora_a = nn.Linear(in_features, lora_rank, bias=False)
        # B: lora_rank → out_features (차원 복구)
        self.lora_b = nn.Linear(lora_rank, out_features, bias=False)
        
        # A는 가우시안 초기화, B는 0으로 초기화
        nn.init.normal_(self.lora_a.weight, std=0.02)
        nn.init.zeros_(self.lora_b.weight)
        
        # 스케일링 인자 (학습 안정성 향상)
        self.lora_alpha = lora_alpha
        self.lora_rank = lora_rank
    
    def forward(self, x):
        # 기존 선형 변환 (고정)
        out = self.linear(x)
        
        # LoRA 변경사항 추가: (A × B) × x
        lora_out = self.lora_b(self.lora_a(x))
        
        # 스케일링을 적용해서 LoRA 영향력 조절
        scaling = self.lora_alpha / self.lora_rank
        out = out + scaling * lora_out
        
        return out

# 실제 사용 예시
if __name__ == "__main__":
    # 모델 생성
    lora_layer = LoRALinear(
        in_features=768,      # 임베딩 차원
        out_features=768,     # 출력 차원
        lora_rank=8,          # 저차원 크기
        lora_alpha=16         # 스케일링 인자
    )
    
    # 파라미터 개수 비교
    # 기존 가중치: 768 × 768 = 589,824개 (고정)
    # LoRA 추가: (768 × 8) + (8 × 768) = 12,288개 (학습)
    total_params = sum(p.numel() for p in lora_layer.parameters())
    trainable_params = sum(p.numel() for p in lora_layer.parameters() if p.requires_grad)
    
    print(f"전체 파라미터: {total_params:,}")
    print(f"학습 가능 파라미터: {trainable_params:,}")
    print(f"효율성: {100 * trainable_params / total_params:.2f}%")
    
    # 순전파
    x = torch.randn(4, 768)  # 배치 크기 4, 임베딩 크기 768
    output = lora_layer(x)
    print(f"\n입력 형태: {x.shape}")
    print(f"출력 형태: {output.shape}")
```

### Hugging Face PEFT를 사용한 LoRA 적용

더 실무적인 방식으로는 Hugging Face의 PEFT(Parameter-Efficient Fine-Tuning) 라이브러리를 사용한다:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import get_peft_model, LoraConfig, TaskType

# 기본 모델 불러오기
model_name = "meta-llama/Llama-2-7b"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# LoRA 설정
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=8,                          # LoRA 랭크
    lora_alpha=32,                # 스케일링 인자
    lora_dropout=0.05,            # 드롭아웃 (정규화)
    bias="none",                   # 편향은 학습하지 않음
    target_modules=["q_proj", "v_proj"],  # 어느 계층에 LoRA를 적용할지
)

# LoRA를 모델에 적용
model = get_peft_model(model, lora_config)

# 모델 상태 확인
model.print_trainable_parameters()  # 학습 가능한 파라미터 출력

# 이제 일반적인 파인튜닝처럼 진행
# trainer = Trainer(...)
# trainer.train()
```

**코드 설명**:
- `LoRALinear`는 단일 선형 계층에 LoRA를 적용한 예시이다.
- `requires_grad = False`로 기존 가중치를 고정한다.
- A와 B는 가벼운 행렬이므로 메모리와 계산 시간이 극적으로 절감된다.
- PEFT 라이브러리는 실제 LLM의 특정 부분(예: Q, V 프로젝션)에만 LoRA를 선택적으로 적용한다.
- `lora_alpha`를 통해 LoRA의 영향력을 조절할 수 있다.

## 함정·실수

### 1. LoRA 랭크 설정 오류
**문제**: r(lora_rank)을 부적절하게 설정하는 경우
- r이 너무 작으면(예: r=1): 모델의 표현력이 부족해서 목표 태스크에 적응할 수 없다.
- r이 너무 크면(예: r=512): 효율성 이점이 사라지고 Full Fine-Tuning과 큰 차이가 없다.

**해결책**: 처음에는 r=8에서 시작해서 검증 성능을 보며 조정한다. 대부분의 경우 r=32 이상은 필요 없다.

### 2. 기존 가중치 실수로 학습하기
**문제**: 파인튜닝 설정에서 `requires_grad = False`를 빠뜨리거나, 혹은 나중에 실수로 활성화하는 경우

**결과**: 전체 모델의 모든 파라미터가 학습되어 LoRA의 효율성 이점이 완전히 사라진다. 또한 원래 지식을 잃어버릴 수 있다(catastrophic forgetting).

**해결책**: 
```python
# 반드시 이렇게 명시적으로 고정
for param in base_model.parameters():
    param.requires_grad = False
```

### 3. 학습률(Learning Rate) 설정 오류
**문제**: Full Fine-Tuning과 동일한 학습률을 사용하는 경우

LoRA 파라미터는 기존 가중치보다 훨씬 작고 초기에 0에 가깝기 때문에, 너무 큰 학습률을 사용하면 학습이 불안정해진다. 특히 초반에 손실이 발산(diverge)할 수 있다.

**해결책**: LoRA 파라미터용으로는 1e-4~1e-3 정도의 보수적인 학습률을 사용한다. Full Fine-Tuning의 학습률보다 10배 정도 작게 설정하는 것이 일반적이다.

### 4. 모델 저장 및 로드의 복잡성
**문제**: LoRA는 기본 모델과 A×B 행렬을 따로 관리해야 한다는 점이 운영상 복잡할 수 있다.

**해결책**:
- 개발 단계: A와 B를 따로 저장하고 필요할 때만 로드 (메모리 효율)
- 배포 단계: A×B를 기본 모델에 병합(merge)해서 단일 모델 파일로 저장 (배포 단순성)

```python
# 병합 예시 (PEFT)
merged_model = model.merge_and_unload()
merged_model.save_pretrained("./merged-model")
```

### 5. 작은 데이터셋에서의 오버피팅
**문제**: LoRA는 파라미터가 적어 정규화 효과가 있지만, 극히 작은 데이터셋(예: 수십 개 샘플)에서는 여전히 오버피팅할 수 있다.

**해결책**:
- 검증 데이터셋을 명확히 분리
- 조기 종료(early stopping) 사용
- LoRA 드롭아웃(dropout) 활성화
- 더 작은 r 값 사용

## 베스트 프랙티스

### 1. 랭크 크기 선택 가이드
**초기 선택**:
- 작은 모델(7B 파라미터 이하): r=8 시작
- 중간 모델(13B~30B): r=16 시작
- 큰 모델(70B 이상): r=32 시작

**조정 방법**:
1. 위의 초기값으로 학습
2. 검증 성능 확인
3. 성능이 부족하면 r을 8~16 증가
4. 성능 개선이 미미하면 그 전 r 값 사용

### 2. 학습률 조정 전략
**기본 설정**:
```python
lora_lr = 2e-4       # LoRA 파라미터용
base_lr = 5e-5       # 기본 모델 헤드용 (만약 학습한다면)
```

**동적 조정**:
- 초반 손실이 올라가면: 학습률을 절반으로 감소
- 수렴이 느리면: 학습률을 2배 증가 (주의해서 진행)

### 3. 여러 LoRA 어댑터 조합
같은 기본 모델 위에 여러 개의 LoRA를 독립적으로 학습할 수 있다. 이는 다양한 태스크를 지원하면서도 메모리 효율성을 유지하게 해준다.

```python
# 한국어 태스크용 LoRA
ko_lora = train_lora(model, korean_dataset)

# 요약 태스크용 LoRA
summary_lora = train_lora(model, summary_dataset)

# 필요에 따라 선택적으로 로드
model = load_lora(model, ko_lora)      # 한국어 모드
model = load_lora(model, summary_lora) # 요약 모드
```

### 4. QLoRA와의 결합
LoRA는 모델 양자화 기법과 함께 사용할 수 있다(QLoRA). 4비트 양자화와 LoRA를 함께 사용하면:
- 메모리: 약 90% 절감
- 속도: 약간의 오버헤드 있음
- 품질: 거의 손실 없음

### 5. 파인튜닝 프로세스
**권장 진행 순서**:

1단계: 기본 검증
```python
# 작은 데이터셋(예: 100개 샘플)으로 빠르게 테스트
# LoRA 없이 기존 모델만으로 시작해서 기준 성능 파악
```

2단계: LoRA 적용
```python
# r=8로 시작, 작은 학습률(2e-4)
# 검증 손실을 모니터링하며 학습
```

3단계: 하이퍼파라미터 조정
```python
# 성능이 부족하면 r 증가 또는 학습률 조정
# 과적합 신호가 있으면 조기 종료
```

4단계: 최종 평가
```python
# 테스트 데이터셋에서 최종 성능 평가
# A×B를 W에 병합할지, 분리해서 관리할지 결정
```

### 6. 평가 및 모니터링
**주요 메트릭**:
- 검증 손실: 과적합 감지용
- 검증 정확도/F1: 실제 성능 지표
- 학습 곡선: 수렴 상황 확인

**모니터링 팁**:
- Tensorboard나 Weights & Biases 사용
- 매 에포크마다 검증 수행
- 성능 개선이 멈추면 조기 종료

### 7. 문제 해결 체크리스트

| 증상 | 원인 | 해결책 |
|------|------|--------|
| 손실이 발산 | 학습률 과대 | 학습률을 1/10로 감소 |
| 수렴이 너무 느림 | r이 너무 작음 | r을 2배 증가 |
| 과적합 신호 | 데이터 부족 또는 r이 과대 | 조기 종료, r 감소, 드롭아웃 증가 |
| 성능 개선 미미 | 부적절한 데이터 또는 하이퍼파라미터 | 데이터 확인, r 조정 재시도 |

## 참고

**영상 내 명시된 자료**:
- 강사: 해피AI 이진규
- 관련 강의: "맞춤형 LLM 만들기 – LoRA & QLoRA 파인튜닝 실습 입문" (https://inf.run/67NkD)
- 관련 강의: "처음 시작하는 분을 위한 RAG 실습가이드 : 기초 개념부터 멀티모달·Agent 등 다양한 실습으로 맞춤형 LLM 구축" (https://inf.run/J8j7p)

**권장 추가 학습 자료**:
- 원본 논문: "LoRA: Low-Rank Adaptation of Large Language Models" (Hu et al., 2021) — 수학적 배경과 실험 결과를 상세히 다룸
- Hugging Face PEFT 라이브러리 문서: https://huggingface.co/docs/peft — 실제 구현과 다양한 효율적 파인튜닝 기법 제공
- QLoRA 논문: "QLoRA: Efficient Finetuning of Quantized LLMs" (Dettmers et al., 2023) — LoRA와 양자화 결합
- Weights & Biases 튜토리얼: LoRA 실험 추적 및 하이퍼파라미터 최적화 방법