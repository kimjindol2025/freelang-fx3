# APP_GAP_NARROW_01 · json 최소 표현

```text
AGENDA=APP_GAP_NARROW_01
FAMILY=json
EXAMPLE=json-ok-obj
EXPRESS_FULL_APP=NO
SERVER_STAR=NO
SQLITE=NO
LOWER_EQUIV=PASS
CORE_CUT=NO
```

## 안건

app GAP 중 `server_*` / `sqlite` / `json`에서 FX3 Core v1으로 옮길 수 있는 **최소 표현** 범위를 정하고 검증한다. 전면 앱 이식은 하지 않는다.

## 선택 (1개)

| 후보 | 선택 | 이유 |
|------|------|------|
| `server_*` | 아니오 | HTTP 호스트·라우트 묶음. 최소 예제에도 런타임 의존이 큼 |
| `sqlite` | 아니오 | DB 호스트 builtin 묶음 |
| **`json`** | **예** | FX 앱이 쓰는 `json_stringify` 호출+맵 리터럴을 Core v1 FX3가 이미 lower 가능. 호스트 EXEC 없이 **형태 동등** 검증 가능 |

## 예제

- FX3: [`corpus/app-gap/json-ok-obj.fx3`](../../../corpus/app-gap/json-ok-obj.fx3)
- ref: [`corpus/app-gap/json-ok-obj.fl`](../../../corpus/app-gap/json-ok-obj.fl)

```text
F json-ok-obj[]{json_stringify({ok:true})}
→
(defn json-ok-obj []
  (json_stringify {"ok" true}))
```

FX `fx-kv/server.fl`은 `(server_json (json_stringify {"ok" true …}))` 형태를 쓴다.  
이번 안건은 **`json_stringify` 절만** 옮긴다. `server_json`은 계속 GAP.

## 검증

```bash
python3 tools/check_corpus.py
# PASS json-ok-obj lower~ref
# CORPUS_APP_GAP_NARROW=PASS
```

- semantic_min / native: `json_stringify` host builtin → **SKIP** (이 안건 범위=lower 동등)
- 전면 앱·`server_*`·sqlite 표현: **안 함**

## 한 줄

```text
APP_GAP_NARROW_01=PASS
FAMILY=json
NEXT_OUTSIDE=server_*,sqlite,fn,loop,mariadb
```
