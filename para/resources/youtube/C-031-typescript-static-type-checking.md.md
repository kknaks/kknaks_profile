# TypeScript 정적 타입 검사와 컴파일

> 출처: https://www.youtube.com/watch?v=zQnBQ4tB3ZA · Fireship · 2:25 · 2020-11-25

## 요지

- TypeScript는 JavaScript에 선택적인 타입 문법을 추가해 실행 전에 오류를 발견하도록 돕는다.
- TypeScript는 JavaScript의 상위 집합이므로 기존 JavaScript 코드도 유효한 TypeScript 코드로 사용할 수 있다.
- 컴파일러 `tsc`는 TypeScript 파일을 브라우저와 Node.js가 실행할 수 있는 JavaScript로 변환한다.
- 변수의 타입은 명시적으로 선언하거나 초기값을 바탕으로 추론할 수 있으며, 객체의 형태는 사용자 정의 타입과 인터페이스로 표현한다.
- 정적 타입 정보는 잘못된 값의 대입을 차단할 뿐 아니라 IDE의 자동 완성과 코드 탐색도 향상한다.

## 개요

JavaScript는 동적 타입 언어다. 변수와 객체의 타입이 실행 중에 결정되므로 빠르고 유연하게 코드를 작성할 수 있지만, 존재하지 않는 변수를 참조하거나 예상과 다른 형태의 객체를 사용한 오류가 실제 실행 시점까지 드러나지 않을 수 있다.

TypeScript는 JavaScript에 정적 타입 검사를 더해 이런 문제를 개발 단계에서 발견한다. 개발자는 변수, 배열, 함수 인자, 객체 속성의 타입을 기술할 수 있고, 컴파일러와 IDE는 그 정보를 이용해 잘못된 코드를 즉시 알려준다. 작성한 TypeScript 코드는 최종적으로 일반 JavaScript로 변환되어 실행된다.

## 배경 / 사전 지식

브라우저와 Node.js가 직접 실행하는 언어는 JavaScript다. JavaScript에서는 하나의 변수에 서로 다른 종류의 값을 대입할 수 있고, 객체가 특정 속성을 가지고 있는지도 실행 전에는 보장되지 않는다.

```javascript
let value = 10;
value = "ten";

const car = { brand: "Volvo" };
console.log(car.model.toUpperCase()); // 실행할 때 오류 발생
```

이러한 동적 특성은 작은 프로그램에서는 편리하지만, 코드가 커지고 여러 사람이 협업하면 함수가 어떤 값을 요구하는지와 객체가 어떤 형태여야 하는지를 추적하기 어려워진다. TypeScript의 정적 타입 검사는 코드를 실행하기 전에 타입 사이의 모순을 찾아 이 위험을 줄인다.

TypeScript를 사용하려면 일반적으로 Node.js 환경에서 `typescript` 패키지를 설치하고 `tsc` 명령으로 소스 코드를 컴파일한다. 프로젝트 설정은 `tsconfig.json`에 기록한다.

## 핵심 개념

### JavaScript의 상위 집합

TypeScript는 JavaScript의 엄격한 상위 집합이다. 따라서 유효한 JavaScript 문법은 TypeScript 파일에서도 사용할 수 있으며, 필요한 부분부터 점진적으로 타입을 추가할 수 있다. 타입 표기는 개발 과정에서 검사에 사용된 뒤 JavaScript로 변환될 때 제거된다.

### 명시적 타입

변수 이름 뒤에 콜론과 타입을 적어 허용할 값의 종류를 선언한다.

```typescript
let language: string = "TypeScript";
let stable: boolean = true;
let releaseYear: number = 2012;
```

이후 `releaseYear`에 문자열을 대입하는 것처럼 선언과 다른 타입을 사용하면 컴파일러가 오류를 보고한다.

### 타입 추론

타입을 직접 적지 않아도 초기값이 있으면 TypeScript가 타입을 추론한다.

```typescript
let score = 100; // number로 추론
score = "high";  // 타입 오류
```

명백한 타입을 매번 반복해서 적을 필요가 없으므로, 타입 추론을 활용하면 안전성과 간결함을 함께 얻을 수 있다.

### `any` 타입

`any`는 해당 값에 대한 타입 검사를 사실상 해제한다. 기존 JavaScript를 점진적으로 이전하거나 외부 데이터의 형태를 아직 알 수 없을 때 사용할 수 있지만, 오류 탐지와 자동 완성이라는 TypeScript의 장점도 함께 잃는다.

```typescript
let unchecked: any = 1;
unchecked = "one";
unchecked.missingMethod(); // 컴파일 단계에서 막지 못할 수 있음
```

### 배열 타입

배열 요소의 타입은 `타입[]` 형태로 지정한다.

```typescript
const prices: number[] = [10, 20, 30];
```

이 배열에 문자열을 추가하려 하면 타입 오류가 발생한다.

### 사용자 정의 타입과 인터페이스

객체가 가져야 할 속성과 각 속성의 타입은 `type` 또는 `interface`로 표현할 수 있다. 인터페이스를 적용하면 객체의 필수 속성이 빠졌거나 잘못된 타입이 들어간 경우를 실행 전에 확인할 수 있다.

```typescript
interface Car {
  brand: string;
  model: string;
  year: number;
}

const car: Car = {
  brand: "Volvo",
  model: "XC40",
  year: 2020,
};
```

이 타입 정보는 IDE에도 전달되어 `car.`을 입력했을 때 `brand`, `model`, `year` 같은 속성을 자동 완성할 수 있게 한다.

## 작동 원리

1. 개발자가 `.ts` 파일에 JavaScript 코드와 선택적인 타입 표기를 작성한다.
2. TypeScript 컴파일러가 변수 대입, 함수 호출, 객체 속성 접근 등이 선언되거나 추론된 타입과 일치하는지 검사한다.
3. 타입이 맞지 않으면 컴파일러와 IDE가 실행 전에 진단 메시지를 제공한다.
4. 검사를 통과한 코드는 `tsc`에 의해 일반 JavaScript로 변환된다. 타입 표기와 인터페이스처럼 JavaScript 런타임에 존재하지 않는 정보는 결과에서 제거된다.
5. 생성할 JavaScript 버전과 모듈 형식 등은 `tsconfig.json`의 `target`, `module` 같은 옵션으로 조정한다. 오래된 실행 환경을 대상으로 하면서도 최신 JavaScript 문법으로 개발할 수 있다.
6. 생성된 JavaScript를 브라우저나 Node.js에서 실행한다. TypeScript 자체는 런타임이 아니라 개발 및 빌드 단계의 검사 도구로 동작한다.

## 코드 예시

다음 예시는 인터페이스, 배열 타입, 함수 매개변수 타입, 반환 타입을 함께 사용한다.

```typescript
interface Car {
  brand: string;
  model: string;
  year: number;
}

function describeCar(car: Car): string {
  return `${car.brand} ${car.model} (${car.year})`;
}

const cars: Car[] = [
  { brand: "Volvo", model: "XC40", year: 2020 },
  { brand: "Hyundai", model: "Ioniq 5", year: 2021 },
];

for (const car of cars) {
  console.log(describeCar(car));
}
```

`example.ts`로 저장한 뒤 다음과 같이 컴파일하고 실행할 수 있다.

```bash
npx tsc example.ts --target es2020
node example.js
```

실행 결과는 다음과 같다.

```text
Volvo XC40 (2020)
Hyundai Ioniq 5 (2021)
```

예를 들어 배열의 두 번째 객체에서 `year`를 문자열인 `"2021"`로 바꾸면 `tsc`가 `string`을 `number`에 할당할 수 없다는 오류를 보고한다. 객체가 사용되는 실행 경로에 도달하기 전에 문제를 확인할 수 있다는 점이 핵심이다.

## 함정·실수

- TypeScript가 모든 런타임 오류를 막아준다고 생각하기 쉽다. 타입 정보는 컴파일 후 사라지므로 API 응답, 사용자 입력, JSON처럼 프로그램 외부에서 들어오는 데이터는 런타임에 별도로 검증해야 한다.
- 편의를 위해 `any`를 넓게 사용하면 타입 검사가 우회되고 자동 완성도 약해진다. 타입을 모르는 값에는 `unknown`을 사용한 뒤 실제 형태를 확인해 좁히는 편이 안전하다.
- 타입 단언(`as`)은 값을 변환하거나 검증하지 않는다. 개발자가 컴파일러보다 타입을 더 잘 안다고 선언할 뿐이므로 잘못 사용하면 런타임 오류를 숨긴다.
- `tsconfig.json` 없이 파일마다 임의의 컴파일 옵션을 사용하면 개발 환경과 배포 환경의 결과가 달라질 수 있다. 프로젝트 단위 설정을 버전 관리해야 한다.
- 오래된 JavaScript를 대상으로 컴파일한다고 해서 모든 최신 런타임 API가 자동으로 제공되는 것은 아니다. 문법 변환과 필요한 폴리필은 별개의 문제다.

## 베스트 프랙티스

- 새 프로젝트에서는 `tsconfig.json`의 `strict` 옵션을 활성화해 엄격한 검사를 기본값으로 삼는다.
- 초기값만으로 타입이 명확한 지역 변수는 타입 추론에 맡기고, 함수의 공개 경계와 공유되는 객체 구조에는 명시적인 타입을 사용한다.
- `any` 대신 구체적인 타입을 정의하고, 타입을 확정할 수 없는 외부 값은 `unknown`으로 받은 뒤 타입 가드나 스키마 검증으로 확인한다.
- 반복해서 사용하는 객체 형태는 `interface`나 `type`으로 이름을 붙여 한곳에서 관리한다.
- 컴파일 검사를 IDE에만 의존하지 말고 CI에서 `tsc --noEmit`을 실행해 타입 오류가 포함된 변경을 차단한다.
- 프로젝트가 지원해야 할 브라우저와 Node.js 버전에 맞춰 `target`과 라이브러리 설정을 정하고, 팀 전체가 같은 `tsconfig.json`을 사용한다.

## 참고

- TypeScript 컴파일러 명령: `tsc`
- 프로젝트 컴파일러 설정 파일: `tsconfig.json`
- 영상에서 소개한 학습 서비스: Fireship Pro
