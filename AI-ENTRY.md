# FX3 AI 진입 계약

기준일: 2026-09-29

```text
DIALECT=FX3_CORE
SURFACE=.fx3
MEANING=FX_.fl
RUNTIME=EXISTING_FX_ONLY
CORE=UNCHANGED
PURPOSE=FIRST_PASS_CONTRACT
```

AI가 FX3를 쓰기 전에 이 파일만 앞에 둔다. Core 밀도를 바꾸지 않는다. 새 기호를 만들지 않는다. 이미 잠긴 규칙과 fixture 01을 한곳에 모은 것이다.

실험 `bench/results/fx3-vs-python-timing/experiment-20260929-02`에서, 아래 두 규칙을 프롬프트에 넣자 첫 시도가 0/3에서 3/3이 됐다. 언어·lowerer는 바꾸지 않았다.

## 방언

지금 쓰는 언어는 **FX3 Core**다.

- 파일 확장자: `.fx3`
- 의미: 기존 FX `.fl`
- 실행: 기존 FX만. FX3 전용 런타임 없음
- AFJ kebab-case, FX underscore Lisp, FreeLangScript와 섞지 않는다

## 필수 규칙

1. 함수는 `F name[$a,$b]{본문}`이다. 본문은 반드시 `{` `}`로 감싼다.
2. 블록 맨 앞의 `$이름=식`만 바인딩이다. 각 바인딩 식 끝에는 `;`가 필요하다.
3. 일반식이 나온 뒤의 `$이름=식`은 오류다. 바인딩은 앞에만 둔다.
4. 식의 끝은 `;`다. 줄바꿈은 의미를 바꾸지 않는다.
5. 최상위 선언도 `;`로 끝낸다. `}F`처럼 바로 이어 쓰지 않는다. 파일 끝 마지막 항목만 `;` 생략 가능.
6. 이름은 줄이지 않는다. `str_upper`를 `U`로 쓰지 않는다.
7. 변수는 `$이름`이다. 맵·경로는 `@$x.a.b`다.
8. 조건은 `?cond{yes}{no}`다. `null?`는 `~primary`다.
9. 호출은 `foo(a,b)`다. 인자는 콤마다.

자세한 내리기는 [LOWERING_CONTRACT.md](LOWERING_CONTRACT.md)다. 밀도 잠금은 [CORE.md](CORE.md)다.

## 짧은 예제

fixture 01. 이 한 줄이 Core 밀도다.

```text
F handle-rate-single[$req]{$cur=str_upper(@$req.params.currency);$body=http-get-body(RATE_URL);?~$body{json-err("환율 API 오류")}{json-ok($body)}}
```

읽는 표시만 `;`에서 나눈 모습:

```text
F handle-rate-single[$req]{
$cur=str_upper(@$req.params.currency);
$body=http-get-body(RATE_URL);
?~$body{json-err("환율 API 오류")}{json-ok($body)}
}
```

원본: [examples/handle-rate-single.fx3](examples/handle-rate-single.fx3)  
기대 `.fl`: [examples/handle-rate-single.fl](examples/handle-rate-single.fl)

## 프롬프트에 붙일 최소 조각

작업 프롬프트 앞에 아래를 그대로 넣는다.

```text
DIALECT: FX3 Core (.fx3). Meaning lowers to existing FX .fl. No new runtime.
Rules:
- Function form: F name[$params]{body}. Body braces are required.
- Every leading binding `$name=expr` must end with `;`.
- Bindings only at the start of a block. Names stay full (no one-letter opcodes).
- Expression end is `;`. Newlines are not meaningful.
Example:
F handle-rate-single[$req]{$cur=str_upper(@$req.params.currency);$body=http-get-body(RATE_URL);?~$body{json-err("환율 API 오류")}{json-ok($body)}}
```

## 쓰지 않는 것

- AFJ / Front / FreeLangScript 문법
- FX2 import
- `U` `J` `L` `R` 등 Core 밖 한 글자 opcode를 필수로 쓰기
- FX3 전용 런타임
- 정답 예제를 작업마다 새로 창작하기. 위 fixture 01을 쓴다
