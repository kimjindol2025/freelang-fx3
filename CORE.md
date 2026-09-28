# FX3 Core

기준일: 2026-09-29

```text
CORE=LOCKED
ALIASES=OPTIONAL
EXTREME=CANDIDATE_ONLY
USER_CHOICE=MID_DENSITY
USER_RULE=COMPRESS_STRUCTURE_KEEP_NAMES
FORMATTER=DISPLAY_ONLY
EXPR_END=;
IMPLEMENT=NO
```

> **의미 있는 이름은 보존하고, 반복되는 구조만 압축한다.**

단어를 줄이지 않는다. `defn`, `let`, `if`, 중첩 `get`처럼 반복되는 구조 비용만 줄인다. `str_upper`는 호출 한 번의 비용이므로 `U`로 바꾸지 않는다.

## 표면

```text
F handle-rate-single[$req]{$cur=str_upper(@$req.params.currency);$body=http-get-body(RATE_URL);?~$body{json-err("환율 API 오류")}{json-ok($body)}}
```

이 밀도가 FX3 Core다.

| 표면 | 의미 |
|------|------|
| `F` | `defn` |
| `?` | `if` |
| `~` | `null?` |
| `@` | 중첩 `get` |
| `+ - * / >= ==` 등 | 기존 연산식 |
| `;` | 표현식 종료 |
| `$` | 변수 토큰 구분 |
| `{ } [ ] ( )` | 구조 경계 |
| 함수명, 변수명 | 그대로 유지 |

`U`, `J`와 한 글자 opcode는 Core가 아니다.

## 경로

```text
FX3 Core
   ↓
optional aliases (실험)
   ↓
canonical .fl
   ↓
FX semantics/runtime
```

Alias는 빼도 Core 프로그램이 성립한다. 극단 압축이나 다른 표기는 Core를 바꾸지 않고, 토큰 수, 생성 오류, 수정 범위에서 Core와 경쟁하는 후보다. 져도 Core는 이 밀도로 남는다.

fixture 01의 기대 `.fl`은 Core 철자 `str_upper` 기준이다. 연산자는 Core에 속하지만, 그 fixture의 바이트 잠금에는 아직 없다.

## 사용자 피드백

이 절은 Grok이 사용자로서 고른 것이다. 매일 생성한 뒤 다시 읽고 수정한다는 기준이다.

**구조는 과감하게 줄인다. 이름은 건드리지 않는다.**

`defn`, `let`, `if`, 중첩 `get`은 반복되고, 괄호를 빼먹으면 뒤 해석이 밀린다. `handle-rate-single`, `http-get-body`, `str_upper`는 다음에도 바로 읽힌다. `U`, `J`, `A`, `Q`가 늘면 다시 읽을 때마다 사전이 있어야 하고, 줄인 토큰을 사전으로 다시 쓴다.

유지:

- 의미 있는 함수명
- `$` 변수 표식
- `F ? ~ @ ;`
- 일반적인 연산자
- `{ } [ ] ( )` 구조 경계
- 줄바꿈 비의미

제외:

- builtin을 한 글자로 과도하게 줄이기
- 문맥에 따라 같은 기호 의미가 바뀌는 것
- 한 글자 수정이 뒤 문법 전체에 영향을 주는 압축
- 다시 읽을 때 별도 코드북이 필요한 표기

식의 끝은 `;`다. `__`는 `__apply__` 같은 이름과 예외를 기억해야 해서, 다시 읽을 때 비용이 든다. `;`는 이름 문자가 아니므로 예외 없이 끝이다.

저장과 전송은 한 줄이다. 다시 읽을 때만 formatter가 `;`마다 줄을 나눈다. 줄바꿈은 문법이 아니다.

원하는 언어는 처음 생성만 싼 언어가 아니다. 다시 읽기 좋은 언어다.

## 사용자 1호

저장소를 읽고 고른 판정이다.

```text
USER_01=WOULD_USE
CORE_DENSITY=GOOD
SEMANTIC_NAMES=KEEP
VAR_SIGIL=KEEP
EXPR_END=;
HOT_ALIAS=OPTIONAL_ONLY
MAIN_REQUEST=MAKE_RULES_EXCEPTIONLESS
```

철학 문구는 이렇게 둔다.

> **사람 가독성은 목표가 아니다. AI 가독성을 우선한다.**

의미 있는 이름을 보존하므로, 사람 가독성을 전부 버린 언어가 아니다. 그 문구는 극단 압축의 근거로 쓰지 않는다.

바인딩은 블록 맨 앞만 허용한다. `{$a=foo();bar();$b=baz()}`는 문법 오류다.

최상위는 `;`가 필수다. `F a[]{...};F b[]{...}`만 두 선언이다. `}`는 다음 선언의 경계가 아니다.

`@$rows.length`는 항상 `(get $rows "length")`다. `length` 함수로 바꾸지 않는다.

읽을 때 formatter가 보여 주는 형태:

```text
F handle-rate-single[$req]{
  $cur=str_upper(@$req.params.currency);
  $body=http-get-body(RATE_URL);
  ?~$body{
    json-err("환율 API 오류")
  }{
    json-ok($body)
  }
}
```

저장과 전송은 한 줄이다. 두 표기는 같은 `.fl`이다. formatter는 아직 없다.

첫 구현은 fixture 01만 내리는 최소 lowerer다. 그다음 사용자 테스트는 이 철자로 프로그램 10개를 직접 쓰고 고치는 것이다.
