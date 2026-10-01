# App 순수 헬퍼 (Core 안만)

```text
CORPUS_APP_PURE=OPEN
SOURCE=freelang-v11-fx/fx-queue/server.fl
FORMS=get|if|null?|arith|call  only when Core
FORBIDDEN=server_json,mariadb,fn,loop
```

| 이름 | 출처 | 비고 |
|------|------|------|
| fib | `fx-queue/server.fl` | `if` + 산술 + 재귀 호출. `$n-1` 뺄셈 |
