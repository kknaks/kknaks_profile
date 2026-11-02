---
type: concept
id: autoregressive-language-model
title: 자기회귀 언어모델 (Autoregressive Language Model)
aliases:
  - 자기회귀 언어모델
  - 자기회귀
  - 자동회귀
  - AR
  - autoregressive
  - causal language model
tags:
  - 생성
  - GPT
  - 다음 토큰 예측
up:
  - 2026-09-15-ai-engineering-ch1
  - C-052-how-llms-learn-and-generate-text
---

# 자기회귀 언어모델 (Autoregressive Language Model)

이전 토큰들만 보고 다음 토큰 하나를 예측하는 [[language-model]]이다. 뽑은 토큰을 입력 뒤에 붙이고 다시 다음 토큰을 예측하는 과정을 반복해 글을 만든다. GPT 계열이 대표적이다.

## 정의

뒤를 가린 채(causal mask) 다음 토큰만 맞히게 학습한다.

```text
입력   내가 가장 좋아하는 색상은 ___
예측   파란색 / 노란색 / … (색상 계열에 확률이 몰림)
```

모델은 `P(다음 토큰 | 지금까지의 토큰)`을 계산한다. 이 확률 계산과 토큰 선택은 별도 단계다. 최댓값 선택은 가장 확률이 높은 후보를 고르고, 샘플링은 확률에 따라 후보를 무작위로 뽑는다. 고정된 확률 분포에서도 샘플링 때문에 결과가 달라질 수 있다. 선택한 토큰을 입력에 붙여 반복하다가 종료 토큰이나 길이 제한에 도달하면 멈춘다.

[[transformer]]를 사용하는 경우, 정답 시퀀스가 주어진 훈련에서는 미래 토큰을 가린 채 여러 위치의 예측을 병렬 계산할 수 있다. 생성에서는 방금 선택한 토큰이 다음 예측의 조건이 되므로 단계 사이에 순차적 의존성이 남는다.

주류가 된 이유가 둘이다.

- **학습 목표와 사용 방식이 같다.** 학습도 「다음 토큰 맞히기」, 생성도 「다음 토큰 뽑기」다. 따로 생성용 장치를 붙일 필요가 없다.
- **모든 토큰이 학습 신호가 된다.** [[masked-language-model]]이 15%만 쓰는 데 비해 시퀀스의 모든 위치가 문제가 된다. 라벨도 필요 없어 인터넷 텍스트를 그대로 학습 데이터로 쓸 수 있다([[self-supervised-learning]]).

한계도 셋이다.

1. **뒤 문맥을 못 본다.**
2. **한 번 뽑은 토큰을 되돌릴 수 없다.** 오류가 뒤로 누적된다.
3. **느리다.** 토큰을 하나씩 순서대로 뽑는다.

## 사용 예시

출처의 작은 확률표 예시는 확률 계산과 토큰 선택을 분리한다. 실제 모델 대신 사람이 정한 표를 사용하고, 공백 단위 문자열을 토큰처럼 취급한다.

```python
import random

END = '<END>'
TABLE = {
    ('오늘',): {'눈이': 0.6, '비가': 0.4},
    ('오늘', '눈이'): {'내립니다.': 0.8, '쌓입니다.': 0.2},
    ('오늘', '비가'): {'내립니다.': 1.0},
}


def generate(prompt, sample=True, seed=0, max_new_tokens=10):
    rng = random.Random(seed)
    tokens = prompt.split()
    for _ in range(max_new_tokens):
        probabilities = TABLE.get(tuple(tokens), {END: 1.0})
        if sample:
            token = rng.choices(
                list(probabilities),
                weights=list(probabilities.values()),
                k=1,
            )[0]
        else:
            token = max(probabilities, key=probabilities.get)
        if token == END:
            break
        tokens.append(token)
    return ' '.join(tokens)


print(generate('오늘', sample=False))
for seed in range(3):
    print(generate('오늘', seed=seed))
```

최댓값 선택은 ‘오늘 눈이 내립니다.’를 만든다. 샘플링은 시드에 따라 다른 경로를 선택할 수 있으며, 이 예시에서는 같은 시드로 같은 결과를 재현한다. 실제 모델은 문맥별 확률표 대신 학습된 가중치로 확률을 계산한다.

## 왜 중요한가

세 번째 한계가 곧 운영 비용의 구조다. 토큰을 순차로 뽑기 때문에 출력이 길수록 시간이 선형으로 늘고, 비용은 학습 때가 아니라 **요청마다** 나간다([[inference-optimization]]). TTFT와 TPOT를 나눠 재는 이유도, 스트리밍이 체감 속도를 바꾸는 이유도 여기서 나온다([[inference-latency-metrics]]).

두 번째 한계는 품질 설계에 닿는다. 앞에서 한 번 잘못 뽑으면 그 전제 위에 계속 쌓이므로, 「틀리지 않게 하는 법」보다 「틀렸을 때 어떻게 되는가」를 같이 설계해야 한다([[human-in-the-loop]]).

## 경계와 오해

- **자기회귀 ≠ 생각하고 답한다** — 매 스텝 확률분포에서 하나를 뽑을 뿐이다. 전체 답을 먼저 정해 두고 출력하지 않는다.
- **느림 ≠ 모델이 커서** — 모델 크기와 별개로 순차 생성 자체가 병목이다. 배칭은 처리량을 올리지만 한 응답의 순차성은 남는다.
- **모든 토큰이 학습 신호 ≠ 더 좋은 모델** — 같은 데이터에서 얻는 신호량의 차이이고, 잘하는 일(생성 vs 이해)은 따로 갈린다.
- **최댓값 선택 ≠ 사실성 보장** — 문맥에서 그럴듯한 토큰이 사실과 일치한다는 보장은 없다. 샘플링의 다양성도 정확성과 별개다.
- **문맥 추가 ≠ 가중치 학습** — 일반적인 생성은 가중치를 고정한 채 입력을 늘린다. 가중치를 갱신하는 학습과 구분한다.

## 함께 보는 개념

- [[language-model]] — 두 갈래를 포함하는 상위 개념.
- [[masked-language-model]] — 앞뒤를 보고 가려진 자리를 맞히는 반대 갈래.
- [[self-supervised-learning]] — 라벨 없이 학습이 가능해진 근거.
- [[inference-optimization]] — 순차 생성의 비용을 줄이는 기법들.
- [[inference-latency-metrics]] — 첫 토큰과 토큰당 시간을 나눠 재는 이유.

## 출처

- [[2026-09-15-ai-engineering-ch1]] — 자기회귀의 정의와 학습 방식, 마스크 방식과의 학습 신호량 비교, 세 가지 한계와 추론 최적화가 필요한 이유를 정리한다.
- [[C-052-how-llms-learn-and-generate-text]] — 확률 계산과 샘플링의 구분, 확률표 기반 생성 예시, 훈련의 병렬성과 생성의 순차성을 설명한다.
