# FX3 구조 설계 초안

기준일: 2026-09-29

```text
STATUS=STRUCTURE_DRAFT
CORE=LOCKED
PRINCIPLE=KEEP_NAMES_COMPRESS_STRUCTURE
CORE_ALIAS_SPLIT=YES
IMPLEMENT=NO
```

Core 정본은 [CORE.md](CORE.md)다.

> **의미 있는 이름은 보존하고, 반복되는 구조만 압축한다.**

이미 잠긴 내리기 범위는 [LOWERING_CONTRACT.md](LOWERING_CONTRACT.md)다. 그 계약은 Core의 일부만 바이트로 고정한다. 이 초안의 연산자, 맵, 벡터, `L`, `try`, `loop`, Hot Alias는 아직 그 계약에 넣지 않는다.

## 1. 기본 철학

FX3는 새 의미론을 만들지 않는다.

```text
FX3 .fx3
   ↓ lowering
Canonical FX .fl
   ↓
기존 FX 실행 의미
```

목표:

- AI가 빠르게 읽고 생성한다
- 의미 있는 이름은 유지한다
- 반복 구조만 압축한다
- 공백과 줄바꿈은 의미가 없다
- 수정 영향은 지역적이다
- 항상 하나의 `.fl`로 변환한다

## 2. 세 층

```text
[1] STRUCTURE
F  ?  L  {}  []  ()  ;
연산자

[2] SEMANTIC SURFACE
함수명, 변수명, map key
try / catch, loop / recur

[3] HOT ALIAS
J, U 처럼 실험하는 축약
```

1번은 유지한다. 2번은 의미를 위해 보존한다. 3번은 측정이 나쁘면 제거한다.

```text
Core syntax
+
Hot aliases
```

`J`가 생성 오류를 높이면 `J`만 버린다. Core는 남는다.

## 3. 프로그램

프로그램은 선언과 표현식의 연속이다.

```text
F name[$a,$b]{...};F other[$x]{...};main(...)
```

줄바꿈은 없어도 된다.

## 4. 표현식 종료

`;`가 expression boundary다.

```text
$a=foo();
$b=bar($a);
print($b)
```

`;`는 이름 문자가 아니다. 문자열 안에서만 내용이고, 그 밖에서는 항상 식의 끝이다. `__apply__`, `currency__b`, `"hello__world"`의 `__`는 끝내지 않는다.

## 5. 함수

```text
F add[$a,$b]{$a+$b}
```

```lisp
(defn add [$a $b]
  (+ $a $b))
```

사용자 함수 이름은 줄이지 않는다.

## 6. Binding

```text
$x=foo();$y=bar($x);$x+$y
```

```lisp
(let [$x (foo)
      $y (bar $x)]
  (+ $x $y))
```

표면에서 `let`은 없다. 블록 앞쪽의 assignment만 lexical binding이다. 연속된 binding은 하나의 `let`이다.

## 7. 조건

```text
?$x>10{big($x)}{small($x)}
```

```lisp
(if (> $x 10)
  (big $x)
  (small $x))
```

else가 없으면:

```text
?$ok{save()}
```

```lisp
(if $ok (save))
```

FX `if`는 else가 없을 때 nil로 컴파일한다. canonical 형태는 else를 생략한 `(if cond then)` 하나다.

## 8. null

```text
~$x
```

```lisp
(null? $x)
```

반대:

```text
!~$x
```

```lisp
(not (null? $x))
```

## 9. 데이터 접근

Core에서 `.이름`은 항상 문자열 키 `get`이다. `[n]`은 인덱스 `get`이다.

```text
@$req.params.currency
```

```lisp
(get (get $req "params") "currency")
```

```text
@$rows[0].id
```

```lisp
(get (get $rows 0) "id")
```

`@$rows.length`를 `(length $rows)`로 읽는 규칙은 Core가 아니다. Core에서는 `(get $rows "length")`다. `length` 호출로 줄이려면 Hot Alias로 따로 둔다. 두 해석을 Core에 같이 두지 않는다.

## 10. 함수 호출

```text
http-get-body(RATE_URL)
json-err("API 오류")
parse-weather($body,$city)
```

함수명은 보존하고 FX 호출로 내린다.

## 11. 연산자

prefix 호출을 infix로 압축한다.

```text
$a+$b
$a-$b
$a*$b
$a/$b
$a==$b
$a!=$b
$a>$b
$a>=10
$a&&$b
$a||$b
!$a
```

우선순위는 이것만 고정한다.

```text
()
!
* /
+ -
< <= > >=
== !=
&&
||
```

`&&`는 `(and a b)`, `||`는 `(or a b)`, `!`는 `(not a)`다. 비교와 산술의 이름도 FX 연산자와 같다. 복잡하면 괄호를 쓴다.

이 연산자는 구조 설계에 있다. [LOWERING_CONTRACT.md](LOWERING_CONTRACT.md)의 fixture 01에는 아직 없다.

## 12. Map

```text
{ok:true,data:$rows}
```

```lisp
{"ok" true
 "data" $rows}
```

identifier key는 문자열 key다. 특수문자가 있으면 따옴표를 쓴다.

```text
{"content-type":"json"}
```

`{}` 안에 `key:value`가 있으면 맵이다. `;`로 식이 이어지면 블록이다.

## 13. Vector

```text
[1,2,$x,foo()]
```

FX vector / list의 canonical 형태 하나로만 내린다. 그 형태를 고르기 전에는 내리기 계약에 넣지 않는다.

## 14. Lambda

```text
L[$x]{$x+1}
```

```lisp
(fn [$x] (+ $x 1))
```

`L`은 Core 구조다. Hot Alias가 아니다. loop의 이름으로 `L`을 다시 쓰지 않는다.

## 15. 순차 실행

`do`는 표면에 없다. 블록이 sequence다.

```text
{a();b();c()}
```

```lisp
(do
  (a)
  (b)
  (c))
```

바인딩이 앞에 있으면 그 묶음은 `let`이고, 남은 식이 둘 이상일 때만 본문이 `do`다.

## 16. Hot Alias

고빈도 패턴만 별칭 테이블에 둔다.

```text
J{x}
```

```lisp
(server_json (json_stringify x))
```

`U(...)`처럼 builtin을 짧게 부르는 것도 이 테이블이다. Core 철자가 `str_upper(...)`이면 alias `U(...)`는 같은 `.fl`로 내린다. 측정이 나쁘면 테이블에서 지운다.

fixture 01의 정본 철자는 Core다. `str_upper`를 쓴다. `U`는 같은 프로그램의 alias 철자이고, 아직 계약의 필수 문자가 아니다.

## 17. 오류 처리

초기에는 줄이지 않는다.

```text
try{risky()}catch[$e]{log-error($e)}
```

빈도가 높아지면 그때 축약 경쟁으로 보낸다.

## 18. loop / recur

self-host의 핵심이라 명확한 철자를 유지한다.

```text
loop[$i=0,$acc=[]]{
  ?$i>=10{
    $acc
  }{
    recur[$i+1,conj($acc,$i)]
  }
}
```

극단 압축하지 않는다. `L`은 lambda만 뜻한다.

## 19. 변수

`$`를 유지한다.

```text
$user
$rows
$result
```

변수와 함수 이름의 경계다. 제거 여부는 측정 뒤에 정한다.

## 20. 공백

다음은 같은 코드다.

```text
F add[$a,$b]{
  $c=$a+$b;
  $c
}
```

```text
F add[$a,$b]{$c=$a+$b;$c}
```

formatter는 별도 도구다. 공백이 달라도 canonical `.fl` 바이트는 하나다.

## 21. 예시

FX:

```lisp
(defn handle-rate-single [$req]
  (let [$cur (str_upper (get (get $req "params") "currency"))
        $body (http-get-body RATE_URL)]
    (if (null? $body)
      (json-err "환율 API 오류")
      (json-ok $body))))
```

Core:

```text
F handle-rate-single[$req]{$cur=str_upper(@$req.params.currency);$body=http-get-body(RATE_URL);?~$body{json-err("환율 API 오류")}{json-ok($body)}}
```

Hot Alias를 켠 철자:

```text
F handle-rate-single[$req]{$cur=U(@$req.params.currency);$body=http-get-body(RATE_URL);?~$body{json-err("환율 API 오류")}{json-ok($body)}}
```

Core 철자는 fixture 01과 같고, 기대 `.fl`은 [examples/handle-rate-single.fl](examples/handle-rate-single.fl)이다. `U`를 쓰는 철자는 alias 테이블이 있을 때만 같은 파일로 내려간다.

## 22. 기준

FX3는 가장 짧은 언어가 아니다.

**의미 있는 이름은 유지하고, 반복되는 구조 비용만 제거한다.**

```text
AMBIGUOUS_PARSE=0
ROUNDTRIP_TO_FL=PASS
SEMANTIC_MATCH=PASS
TOKEN_REDUCTION=MEASURED
GENERATION_ERROR=MEASURED
EDIT_LOCALITY=PASS
```

판정 전에는 parser와 runtime을 만들지 않는다.
