---
type: concept
id: thread-state
title: 쓰레드 상태 (Thread State)
aliases:
  - 쓰레드 상태
  - 스레드 상태
  - thread state
  - Thread.State
  - 쓰레드 생명주기
  - thread lifecycle
  - sleep
up:
  - 2024-08-05-Day48
tags:
  - java
  - 동시성
  - 운영체제
  - 디버깅
---

# 쓰레드 상태 (Thread State)

**만들어진 쓰레드가 끝날 때까지 지나가는 단계.** Day48 의 요지가 「쓰레드는 객체가 생성되서 바로 실행 되는 것이 아니라, CPU스케쥴링에 따라 시행된다」다 — `start()` 를 불렀다는 것이 「지금 돈다」가 아니라 **「돌 수 있는 줄에 섰다」**는 뜻이라는 것이 이 개념의 출발점이다 → [[thread]]

## 정의

Day48 은 다섯 개를 적었고, 자바가 실제로 갖고 있는 것(`Thread.State` 열거 타입)은 여섯 개다.

| Day48 | 실제 `Thread.State` | 무엇인가 |
|---|---|---|
| NEW | `NEW` | 객체만 만든 상태. 아직 `start()` 전 |
| RUNNABLE | `RUNNABLE` | 실행 가능 — **CPU 를 쥐고 도는 중도 여기다** |
| RUNNING | *(없다)* | 「CPU 를 지금 쥐고 있음」은 자바가 구별해 주지 않는다 |
| WATING | `WAITING` | 누가 깨워 줘야 한다 — `join()`·`wait()` |
| — | `TIMED_WAITING` | 시간이 지나면 스스로 깬다 — `sleep(ms)`·`join(ms)` |
| — | `BLOCKED` | 잠금(`synchronized`)이 풀리기만 기다린다 |
| TERMINATED | `TERMINATED` | `run()` 이 반환했거나 예외로 끝났다 |

상태를 옮기는 것은 대개 **자기 자신이 부른 메서드**다. 밖에서 남의 상태를 바꾸는 것은 `start()`·`interrupt()` 둘뿐이다.

```text
NEW --start()--> RUNNABLE --run() 반환/예외--> TERMINATED
                    │  ↑
        sleep(ms)   │  │ 시간 만료 · notify() · 상대 종료 · 잠금 획득
        join()      │  │
        잠금 대기    ↓  │
             TIMED_WAITING · WAITING · BLOCKED
```

**TERMINATED 에서 나가는 화살표가 없다.** 그래서 끝난 쓰레드는 되살릴 수 없다(아래 「경계와 오해」).

## 사용 예시

Day48 이 상태를 **읽는** 코드는 없고, **바꾸는** 코드가 하나 있다 — `sleep()` 으로 자기를 TIMED_WAITING 에 넣는 것이다.

```java
public class SleepExample {
    public static void main(String[] args) {
        Toolkit toolkit = Toolkit.getDefaultToolkit();
        for(int i=0; i<10; i++) {
            toolkit.beep();
            try {
              Thread.sleep(3000);
            } catch(InterruptedException e) {
            }
        }
    }
}
```

**`Thread.sleep()` 이 정적 메서드인 것이 이 문법의 성격을 말해 준다** — 남을 재우는 것이 아니라 **부른 쓰레드 자신**이 잠든다. 그래서 `thread.sleep(3000)` 이라고 써도 재워지는 것은 `thread` 가 아니라 그 줄을 실행한 쓰레드다 → [[static-member]]

단위는 밀리초라 `3000` 이 3초다. 잠든 쓰레드가 CPU 를 내놓으므로, 앞선 비프음 예제에서 두 흐름의 대기 시간이 겹칠 수 있었던 것도 이 성질이다.

## 왜 중요한가

**「멈췄다」를 진단할 수 있는 말이 생긴다.** 프로그램이 응답하지 않을 때 쓰레드마다 상태를 보면 원인이 갈린다 — `BLOCKED` 가 여럿이면 한 잠금에 줄을 선 것이고, `WAITING` 이면 깨워 줄 사람을 기다리는 것이고(그 사람이 이미 죽었을 수 있다), `RUNNABLE` 인데 느리면 CPU 가 부족하거나 코드가 실제로 오래 도는 것이다. **셋의 답이 전부 다르다** — 잠금을 줄이거나, 깨우는 쪽을 고치거나, 일을 줄인다.

**`start()` 와 「실행」이 다른 시점이라는 것이 코드에 영향을 준다.** `start()` 직후에 그 쓰레드가 이미 값을 채웠다고 가정하면 대개 맞고 가끔 틀린다 — RUNNABLE 은 「줄에 섰다」이지 「돌았다」가 아니다. 그래서 결과를 읽기 전에 `join()` 이 필요하다 → [[thread-join]]

**그리고 「기다림」이 한 종류가 아니라는 것을 알면 잠금 안에서 자면 안 되는 이유가 설명된다.** `sleep()` 은 잠금을 들고 잔다 — 그 동안 같은 잠금을 기다리는 쓰레드 전부가 `BLOCKED` 로 서 있는다. 「어차피 멈추는 건 같다」로 보면 프로그램 전체를 세우는 코드를 쓰게 된다.

## 경계와 오해

- **RUNNING 은 자바의 상태가 아니다** — Day48 이 「RUNNABLE : 실행 가능한 상태」와 「RUNNING : cpu에서 점유한 부분이 run() 메서드를 통해 실행 하는 상태」를 갈라 적었는데, `Thread.State` 에는 `RUNNING` 이 없고 **둘 다 `RUNNABLE`** 이다. 갈라 놓지 않은 이유가 있다 — 「지금 CPU 를 쥐고 있나」는 운영체제 스케줄러가 매 순간 바꾸는 값이라 **자바가 알려 준다 해도 읽은 순간 이미 옛 값**이다. 교과서 그림이 RUNNABLE 안에 RUNNING 을 넣어 그리는 것은 설명용이고, 코드로 확인할 수 있는 경계가 아니다. 「RUNNING 을 기다리자」 같은 코드가 안 써지는 이유다.
- **「WATING」은 오타이고, 그 한 칸에 실제로는 셋이 들어 있다** — Day48 의 「쓰레드가 실행할 수 없는 상태」는 결과만 맞다. 실제로는 `WAITING`(깨워 줄 사람이 있어야 한다) · `TIMED_WAITING`(시간이 지나면 스스로 깬다) · `BLOCKED`(잠금만 나면 된다)가 갈린다. **셋을 하나로 뭉치면 「왜 안 깨나」를 물을 수 없다** — 깨울 사람이 없는 것과 시간이 안 된 것과 잠금을 못 얻은 것은 고치는 방법이 전부 다르고, 교착 상태는 앞의 두 칸에서만 생긴다.
- **`sleep()` 은 잠금을 놓지 않는다 — `wait()` 는 놓는다** — 둘 다 「멈춘다」로 읽히지만 이것이 실무에서 가장 크게 갈리는 차이다. `synchronized` 블록 안에서 `sleep(3000)` 을 하면 3초 동안 그 잠금을 든 채로 자므로 **다른 쓰레드는 전부 `BLOCKED`** 다. Day48 이 「쓰레드 동기화」 절을 비워 둔 탓에 `wait()` 와 `sleep()` 이 나란히 놓이지 않았고, 그래서 이 차이가 이 회차에 드러날 자리가 없었다 → [[thread]]
- **`InterruptedException` 은 「실행 대기 중에 메서드가 호출되면」 나는 것이 아니다** — Day48 의 문장이 흐린데, 정확히는 **자고 있는 동안 다른 쓰레드가 이 쓰레드의 `interrupt()` 를 부르면** 던져진다. 즉 이 예외는 오류가 아니라 **「그만하고 나와라」는 신호**이고, 같은 노트의 비어 있는 「쓰레드 안전종료 - interrupt()메서드 이용」 절이 쓸 도구가 바로 이것이다. 그리고 **예외가 던져지는 순간 인터럽트 표시가 지워지므로**, `catch` 를 비워 두면 신호가 사라지고 쓰레드는 계속 돈다 — Day48 의 모든 `catch` 가 비어 있어 **안전종료가 성립하지 않는 상태**다 → [[exception-handling]]
- **`sleep(500)` 은 500밀리초를 보장하지 않는다** — 「최소 500밀리초」이고, 깨어난 뒤 CPU 를 다시 받아야 하므로 언제나 조금 더 걸린다. 그래서 비프음 예제의 5회가 정확히 2.5초가 아니고, `sleep` 을 여러 번 겹쳐 시간을 재면 오차가 쌓인다. **`sleep` 은 타이머가 아니다.**
- **`sleep` 을 「기다리는 도구」로 쓰면 조용히 틀린다** — 「1초면 끝나겠지」로 `sleep(1000)` 을 넣고 결과를 읽는 코드는 느린 기계에서 깨지고, 빠른 기계에서는 쓸데없이 1초를 쓴다. 게다가 시간이 충분해도 **다른 쓰레드가 쓴 값이 보인다는 보장 자체가 없다** — 그것을 주는 것은 `join()` 이다 → [[thread-join]]
- **NEW 로 돌아갈 수 없다** — 끝난 쓰레드를 다시 `start()` 하면 `IllegalThreadStateException` 이다. 상태 그림에서 `TERMINATED` 에 나가는 화살표가 없다는 것이 그 뜻이고, 그래서 **쓰레드는 「일꾼」이 아니라 「한 번 쓰는 일회용 흐름」**이다. 일꾼을 재사용하려면 쓰레드를 살려 둔 채 **작업만 바꿔 넣어야** 하고, 그것이 쓰레드 풀이 존재하는 이유다.
- **상태를 읽어 분기하지 않는다** — `getState()` 가 있지만 돌려받은 값은 **읽은 순간의 과거**다. `if (t.getState() == RUNNABLE)` 로 판단하면 그 줄을 실행하는 사이에 이미 바뀔 수 있다. 진단용(스레드 덤프·모니터링)이고 제어용이 아니며, 제어는 `join()`·`interrupt()`·잠금으로 한다.
- **TERMINATED 는 성공을 뜻하지 않는다** — `run()` 이 예외로 끝나도 상태는 같은 `TERMINATED` 다. **「끝났다」와 「해냈다」가 구별되지 않으므로** 결과를 담는 필드가 채워졌는지는 따로 확인해야 한다. 쓰레드에서 난 예외가 프로세스를 죽이지 않는 것과 겹쳐, **아무도 모르게 실패한 쓰레드**가 여기서 생긴다 → [[process]] · [[thread-join]]

## 함께 보는 개념

- [[thread]] — 상태를 갖는 대상
- [[thread-join]] — 상대가 TERMINATED 가 될 때까지 내가 WAITING 이 되는 메서드
- [[process]] — 죽은 쓰레드가 프로세스를 죽이지 않는다는 경계
- [[exception-handling]] — `InterruptedException` 을 다루는 자리
- [[static-member]] — `Thread.sleep()` 이 정적 메서드인 이유
- [[method-overriding]] — `run()` 이 반환하면 TERMINATED 로 가는 그 메서드

## 출처

- [[2024-08-05-Day48]] — 「쓰레드는 객체가 생성되서 바로 실행 되는 것이 아니라, CPU스케쥴링에 따라 시행된다」로 `start()` 와 실행 시점을 갈랐고, 상태를 NEW·RUNNABLE·RUNNING·WATING·TERMINATED 다섯으로 적었다. `sleep()` 으로 스스로 멈추는 코드(`SleepExample`)가 이 회차에서 상태를 실제로 바꾸는 유일한 코드다. 다만 **`RUNNING` 은 `Thread.State` 에 없고**(RUNNABLE 이 둘을 덮는다), 「WATING」은 오타이며 그 한 칸에 `WAITING`·`TIMED_WAITING`·`BLOCKED` 셋이 뭉쳐 있다. `InterruptedException` 을 「실행 대기 중에 메서드가 호출되면」 난다고 적어 **누가 왜 던지는지**가 흐려졌고, `sleep()` 이 잠금을 들고 잔다는 것·끝난 쓰레드를 다시 시작할 수 없다는 것·`getState()` 로 읽은 값이 곧 과거라는 것은 다루지 않았다
