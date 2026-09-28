# FX3_LOWERING_CONTRACT_LOCK

기준일: 2026-09-29

```text
LOCK=FX3_LOWERING_CONTRACT_LOCK
PARSER=NONE
RUNTIME=NONE
LOWERER=NONE
GOLDEN=01
MATCH=EXACT_FL_BYTES
```

이 문서는 구현이 아니다. `GRAMMAR-V0.md`의 최소 표면이 항상 하나의 canonical `.fl`로만 내려간다는 계약이다.

같은 `.fx3` 의미는 공백과 줄바꿈을 어떻게 두어도 같은 `.fl` 바이트가 된다. 두 갈래로 내려가면 이 계약의 실패다.

## 잠그는 범위

이 잠금 안에 있는 표면만 계약이다.

| 표면 | canonical `.fl` |
|------|-----------------|
| `F name[$a,$b]{body}` | `(defn name [$a $b] body)` |
| `$x=expr` 가 `;`로 이어진 묶음 | 하나의 `(let [$x expr ...] body)` |
| `?cond{a}{b}` | `(if cond a b)` |
| `~primary` | `(null? primary)` |
| `@$x.a.b` | `(get (get $x "a") "b")` |
| `foo(a,b)` | `(foo a b)` |
| `$name` | `$name` |
| `;` | 식의 끝. `.fl`에 남지 않는다 |
| 공백, 줄바꿈 | 토큰 사이 여백. 의미 없음 |

맵, 벡터, `J`, `U`, `L`, `R`, `true`/`false`/`nil`의 짧은 표기는 이 잠금 밖이다.

## 식의 끝

`;`만 식을 끝낸다. 줄바꿈과 공백은 끝내지 않는다.

`;`는 이름 문자가 아니다. 문자열, raw literal, comment 안에서만 내용이고, 그 밖에서는 항상 식의 끝이다. `__apply__`, `currency__b` 같은 `__`는 이름의 일부이고 식이 끝나지 않는다.

`}` 바로 앞의 마지막 식은 `;`를 생략할 수 있다. 생략해도 같은 트리이고, 같은 `.fl`이다.

저장은 한 줄이다. 다시 읽을 때 formatter가 `;`마다 줄을 나눈다. 그 줄바꿈은 같은 `.fl`로 내려간다.

## 본문

`{...}` 안은 `;`로 나뉜 식의 나열이다.

1. 블록 맨 앞에서부터 `$이름=expr`가 연속된 구간만 바인딩이다. 그 묶음은 하나의 `let`이다. 중첩 `let`으로 나누지 않는다.
2. 첫 일반식이 나타난 뒤의 `$이름=expr`는 문법 오류다. `{$a=foo();bar();$b=baz()}`는 거부한다.
3. 바인딩 뒤의 식이 하나면 `let`의 본문이다.
4. 바인딩 뒤의 식이 둘 이상이면 본문은 `(do expr expr ...)`이다.
5. 바인딩이 없고 식이 둘 이상이면 본문 전체가 `(do ...)`이다.
6. 바인딩이 없고 식이 하나면 그 식이 본문이다.
7. 바인딩만 있고 본문 식이 없으면 이 계약의 식이 아니다.

## 최상위

프로그램은 선언과 식의 나열이다. 각 항목의 끝은 `;`다. `}`만으로는 선언이 끝나지 않는다.

```text
F a[]{...};F b[]{...};main()
```

`F a[]{...}F b[]{...}`는 문법 오류다. 파일 끝의 마지막 항목만 `;`를 생략할 수 있다. 생략해도 같은 트리다.

`F`의 인자 목록은 `$` 변수를 콤마로 나눈다. `.fl` 인자 벡터 안에서는 공백으로 나눈다.

## 호출과 경로

- 인자는 콤마로 나눈다. `foo()`는 `(foo)`다.
- 이름 그대로 호출한다. 이 잠금은 함수 이름을 줄이지 않는다.
- `~`는 바로 뒤의 primary 하나에 붙는다. primary는 `$` 변수, `@` 경로, 호출, 문자열, `(...)`다.
- `@`의 머리는 `$` 변수다. 그 뒤 `.이름` 조각마다 문자열 키가 된다.
  - `@$x.a` → `(get $x "a")`
  - `@$x.a.b` → `(get (get $x "a") "b")`
  - 조각이 없으면 이 계약의 식이 아니다.
- 문자열은 내용과 따옴표를 유지한 채 `(호출 "...")`의 인자가 된다.
- `$`가 없는 이름은 호출 자리가 아니면 그대로 심볼이다. 예: `RATE_URL`.

## Golden fixture 01

소스: [examples/handle-rate-single.fx3](examples/handle-rate-single.fx3)

기대값: [examples/handle-rate-single.fl](examples/handle-rate-single.fl)

판정은 기대 파일의 바이트와 같은지다. 실행하지 않는다. parser와 runtime은 이 잠금에 없다.

소스의 트리는 이것 하나다.

```text
(defn handle-rate-single [$req]
  (let [$cur (str_upper (get (get $req "params") "currency"))
        $body (http-get-body RATE_URL)]
    (if (null? $body)
      (json-err "환율 API 오류")
      (json-ok $body))))
```

위 트리의 canonical 표기는 fixture 파일 전체다. 같은 식을 여러 줄로 쓴 `.fx3`도 그 파일과 같은 바이트로 내려간다.

## 이 잠금의 PASS

다음 단계 `FX3_MINIMAL_LOWERER_STAGE1`은 이 계약과 fixture 01만 만족하면 된다. 그 전에 lowerer를 만들지 않는다.
