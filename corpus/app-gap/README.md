# app-gap 좁은 표현 (APP_GAP_NARROW_*)

Core v1 OUTSIDE인 앱 GAP 중 **한 가족만** 골라, FX3로 최소 표현을 검증한다.  
전면 앱 이식 금지. `server_*` / `sqlite` / `fn` / `loop` 전체를 열지 않는다.

| 안건 | 가족 | 예제 | 검증 |
|------|------|------|------|
| APP_GAP_NARROW_01 | **json** | `json-ok-obj` | lower ≡ ref `.fl` |
| JSON_PASSTHROUGH_PAIR | **json** 이름 호출 | `json-stringify` · `json-try-parse` | lower ≡ ref `.fl` |

`server_*` / `mariadb` / `fn` / `loop` 는 이 디렉터리에 넣지 않는다.
