# 사용자 기록

Core 규칙은 [CORE.md](CORE.md)에 둔다. 여기에는 읽고 고친 뒤의 판정만 쌓는다.

## 2026-09-29 사용자 1호

```text
USER_01=CONTINUE
FIXTURE_01=KEEP
FIXTURE_02=KEEP
SEMICOLON=STRONG_KEEP
QUESTION_MARK=KEEP_FOR_NOW
SYMBOL_CLUSTER=?~ WATCH
NEXT_USER_TEST=MAP
```

바인딩은 블록 앞에서만 허용하는 쪽이 좋다. 최상위 `;`도 유지한다. `@$rows.length`는 항상 `get`이다.

fixture 02를 읽어 보니 `;`로 세 덩어리가 보인다. `;`는 `STRONG_KEEP`이다. 밀도는 01보다 02에서 더 무너지지 않았다.

`?` 자체는 두 fixture에서 익숙해졌다. 걸린 것은 `?`가 아니라 `?~`처럼 unary가 바로 붙는 경우다. 조건 표면은 바꾸지 않는다.

다음으로 읽은 것은 Map이다. `{ok:true,data:$rows}`와 `{a();b();c()}`가 한 줄에서 바로 갈리는지 보려는 표본이 fixture 03이다.

그 다음으로 보고 싶은 표면은 `@$rows[0].id`다. 아직 fixture로 넣지 않는다.
