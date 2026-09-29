# 방언 목록 — FX3 Core만

기준일: 2026-09-29

```text
DIALECT=FX3_CORE
SCOPE=THIS_FILE_ONLY
OTHER_DIALECTS=NOT_IN_THIS_FILE
AFJ=EXCLUDED
FX_UNDERSCORE_INVENTORY=EXCLUDED
SCRIPT=EXCLUDED
FRONT=EXCLUDED
AFL_DB=EXCLUDED
CORE=LOCKED
MEANING_BASELINE=FX_.fl
RUNTIME=EXISTING_FX_ONLY
```

이 파일은 **FX3 Core**만 적는다. AFJ kebab 목록과 FX underscore 빌트인 목록을 여기 섞지 않는다. 의미의 기준 언어는 기존 FX `.fl`이고, 실행기는 FX3가 아니다.

근거: [CORE.md](CORE.md), [LOWERING_CONTRACT.md](LOWERING_CONTRACT.md), [MINIMUM_FROM_FX.md](MINIMUM_FROM_FX.md), [AI-ENTRY.md](AI-ENTRY.md), `tools/lower.py`, golden fixture 01–04.

---

## 확장자

| 항목 | 값 |
|------|-----|
| 소스 | `.fx3` |
| 내린 결과 | `.fl` (기존 FX canonical) |
| 표면 런타임 파일 | 없음 |

## 실행기

| 단계 | 도구 |
|------|------|
| 내리기 | `python3 tools/lower.py path.fx3` |
| 바이트 검사 | `python3 tools/lower.py --check` (fixture 01–04) |
| 실행 | 내린 `.fl`을 **기존 FX**로 실행. FX3 전용 런타임 없음 |
| 파서/VM | FX3 쪽에 없음 (`PARSER=NONE`, `RUNTIME=NONE`) |

## 함수 선언

| 표면 | 내린 FX |
|------|---------|
| `F name[$a,$b]{body}` | `(defn name [$a $b] body)` |

- 인자 목록은 `$` 변수를 콤마로 나눈다.
- 본문은 반드시 `{` `}`로 감싼다.
- 최상위에서 선언 끝은 `;`다. `}F`처럼 이어 쓰면 오류다. 파일 끝 마지막 항목만 `;` 생략 가능.

## 변수

| 표면 | 의미 |
|------|------|
| `$name` | 변수. `$`는 토큰 구분 |
| `$name=expr` | 블록 **맨 앞**에서만 바인딩. 식 끝 `;` 필수 |
| `$` 없는 이름 | 호출 자리가 아니면 심볼. 예: `RATE_URL` |

바인딩 규칙:

1. 블록 앞쪽의 `$이름=식` 연속만 하나의 `(let [...])`로 내린다.
2. 일반식이 나온 뒤의 `$이름=식`은 문법 오류다.
3. 바인딩만 있고 본문이 없으면 계약 밖이다.

## control flow

| 표면 | 내린 FX |
|------|---------|
| `?cond{a}{b}` | `(if cond a b)` |
| `{expr;expr;...}` (바인딩 없음, 식 ≥2) | `(do expr expr ...)` |
| 바인딩 + 본문 식 1개 | `(let [...] body)` |
| 바인딩 + 본문 식 ≥2 | `(let [...] (do ...))` |
| `;` | 식의 끝. `.fl`에 남지 않는다 |
| 줄바꿈·공백 | 의미 없음 |

Core에 없는 것: `loop` / `recur`, `fn`, `try` / `catch`, `future`. FX에 있어도 FX3 Core 표면에 아직 없다.

## data access

| 표면 | 내린 FX |
|------|---------|
| `@$x.a` | `(get $x "a")` |
| `@$x.a.b` | `(get (get $x "a") "b")` |
| `@$rows[0].id` | `(get (get $rows 0) "id")` |
| `@$rows[$i].id` | `(get (get $rows $i) "id")` |
| `{ok:true,data:$rows}` | 맵 리터럴. 이름 키 → 문자열 키 |
| `"..."` | 문자열 |
| 정수 리터럴 | 숫자 |
| `true` / `false` / `nil` | 같은 리터럴 (fixture 03) |

맵과 블록 구분: `:`·`,`가 있으면 맵, `;`로 식이 이어지면 블록이다.

## error

| 층 | 내용 |
|----|------|
| 내리기 | `LowerError` — 예: `기대 '{'` , 잘못된 바인딩 위치 |
| 표면 | `try` / `catch` 없음 |
| 실행 | 내린 뒤의 오류는 **기존 FX**의 오류다 |
| 관용 호출 | fixture에 `json-err(...)` 같은 **이름 그대로인 FX 호출**이 있을 수 있다. 그건 FX3 문법 기호가 아니다 |

## IO

FX3 Core 문법에 IO 기호는 없다. IO는 호출 이름으로 기존 FX에 넘긴다.

golden fixture 01에 보이는 예:

- `http-get-body(RATE_URL)` → `(http-get-body RATE_URL)`

구현·권한·네트워크는 FX 쪽이다. FX3는 철자만 유지한다.

## builtin 목록

FX3 Core는 **닫힌 빌트인 라이브러리가 없다.** 구조 기호만 Core이고, 호출 이름은 줄이지 않은 채 FX로 내려간다.

### A. Core 표면 기호 (언어 본체)

| 기호 | 역할 |
|------|------|
| `F` | `defn` |
| `?` | `if` |
| `~` | `null?` (바로 뒤 primary 하나) |
| `@` | 중첩/`get` 경로 |
| `$` | 변수 |
| `;` | 식 종료 |
| `{ }` | 블록 또는 맵 |
| `[ ]` | 인자 목록 / 경로 인덱스 |
| `( )` | 호출·그룹 |
| `== != >= <= > < + - * /` | 연산 (lowerer가 FX 연산으로 내림) |

한 글자 opcode `U` `J` `L` `R`는 Core가 아니다.

### B. golden fixture 01–04에 등장하는 호출 이름 (통과 이름)

이 이름들은 FX3가 정의한 표준 라이브러리가 아니다. Core가 **줄이지 않고** 통과시키는 FX 쪽 이름이다.

| 이름 | 출처 fixture |
|------|----------------|
| `str_upper` | 01 handle-rate-single |
| `http-get-body` | 01 |
| `json-err` | 01 |
| `json-ok` | 01 |
| `log-start` | 02 check-and-log |
| `log-big` | 02 |
| `log-small` | 02 |
| `finish` | 02 |
| `result` | 03 make-result |
| `count` | 03 |
| `log-id` | 04 first-id |

### C. 이 파일에 넣지 않는 것

- AFJ kebab 빌트인 목록
- FX underscore 전체 빌트인 목록
- bench/expected·rust-stage1 참고용 호출 이름 전체 (코퍼스이지 Core 잠금이 아님)
- Hot Alias, 극단 압축, FX2 import

---

## 다른 방언과 공통인 것

(다른 방언 목록 파일은 아직 없다. 기준 의미만 FX로 적는다.)

- 의미가 최종적으로 **FX `.fl` S-expression**에 있다.
- 변수 `$name`을 유지한다.
- 함수·호출 **이름을 축약하지 않는다** (`str_upper` 유지).
- 실행은 기존 FX 한 줄이다.

## 이름만 다른 것

같은 FX 의미의 다른 철자.

| FX3 Core | FX `.fl` |
|----------|----------|
| `F name[...]{...}` | `(defn name [...] ...)` |
| `?cond{a}{b}` | `(if cond a b)` |
| `~primary` | `(null? primary)` |
| `@$x.a.b` | `(get (get $x "a") "b")` |
| `foo(a,b)` | `(foo a b)` |
| `$x=expr;...` 앞쪽 묶음 | `(let [$x expr ...] ...)` |
| `expr;expr` | `(do expr expr)` |

## 실제 의미가 다른 것

| 항목 | 내용 |
|------|------|
| 식 종료 | FX3는 `;`가 식의 끝이다. 줄바꿈은 끝이 아니다. |
| 바인딩 위치 | 블록 앞에서만 `$이름=식`이 바인딩이다. 뒤쪽 배정은 오류다. |
| 런타임 | FX3 표면은 VM이 없다. 틀린 표면은 lower에서 죽고, 실행 의미는 FX다. |
| 맵/블록 | 같은 `{ }`라도 `:`·`,`면 맵, `;`면 블록이다. |
| 밀도 목표 | 사람 가독성이 아니라 AI 재독·수정 국소성이다. |

---

## 관련 문서

- 생성 직전 최소 조각: [AI-ENTRY.md](AI-ENTRY.md)
- 밀도 잠금: [CORE.md](CORE.md)
- 바이트 내리기: [LOWERING_CONTRACT.md](LOWERING_CONTRACT.md)
- FX에서 가져온 형식 / 안 가져온 것: [MINIMUM_FROM_FX.md](MINIMUM_FROM_FX.md)
