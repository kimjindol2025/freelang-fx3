# JSON 이름 호출 쌍 · json-stringify / json-try-parse

```text
AGENDA=JSON_PASSTHROUGH_PAIR
SERVER_STAR=NO
MARIADB=NO
FN_LOOP=NO
FIXTURE_05=NO
HOT_ALIAS=NO
RUNTIME=NO
LOWER=PASS
```

## 안건

app GAP 전면이 아니라, Core로 이름 그대로 호출할 수 있는 앱 함수 **한 쌍**만 `.fx3`/`.fl`로 남긴다.

## 쌍

| FX3 | 내린 호출 | 출처 |
|-----|-----------|------|
| `json-stringify` | `(json_stringify $x)` | fx-kv / fx-std 응답 본문 |
| `json-try-parse` | `(json_try_parse $s)` | fx-std `json-parse-safe` 본문 |

```text
F json-stringify[$x]{json_stringify($x)}
F json-try-parse[$s]{json_try_parse($s)}
```

## 검증

`python3 tools/check_corpus.py` → 두 케이스 모두 `lower~ref` PASS · host EXEC SKIP

## 넣지 않음

`server_*` · `mariadb` · `fn` · `loop`

## 한 줄

```text
JSON_PASSTHROUGH_PAIR=PASS
```
