# FX / FX1에서 가져온 최소

기준 트리: `/home/kim/kim/platform/freelang-v11-fx`  
기준 커밋: `202c998`  
가져온 파일: 없음

FX/FX1은 의미의 기준이다. FX3 표면은 아래 형식으로만 내려간다. 이 목록 밖 기능은 아직 FX3의 언어가 아니다.

## 가져오는 형식

| Compact 표면 | 내려갈 FX `.fl` |
|--------------|-----------------|
| `F name[$args]{body}` | `(defn name [$args] body)` |
| `{$x=expr;body}` | `(let [$x expr] body)` |
| `{expr;expr}` | `(do expr expr)` |
| `?cond{a}{b}` | `(if cond a b)` |
| `~$x` | `(null? $x)` |
| `@$x.a.b` | `(get (get $x "a") "b")` |
| `foo(a,b)` | `(foo a b)` |
| `$name` | `$name` |
| `"..."` `{k:v}` `true` `false` `nil` | 같은 리터럴 |

함수 이름과 드문 builtin 이름은 줄이지 않는다. `$`는 유지한다. 식의 끝은 `;`다.

## 가져오지 않는 것

- C 런타임, `cgc`, `self/cgc-main.fl`, 빌드 스크립트
- `fx-*` 앱, stdlib 파일, 테스트 트리
- `server_json`, `json_stringify`, `fxb_sqlite_*`의 구현과 짧은 별칭. 별칭은 코퍼스 경쟁 전이다
- FX2 (`freelang-v11-fx2`, 참고 커밋 `73ebe1c`)의 runtime, library, interface
- 줄 수, 들여쓰기, 공백을 의미로 쓰는 규칙

한 겹 `(get X K)`, `fn`, `loop` / `recur`, `try`, `future`는 FX/FX1에 있으나 v0 축약으로 확정하지 않았다. 필요하면 형식을 문서로 추가한 뒤에만 표면에 올린다.
