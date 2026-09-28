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

이 기록의 `NEXT_USER_TEST=MAP`은 fixture 03으로 끝났다. 현재 다음 표면은 아래 기록이다.

## 2026-09-29 사용자 1호, 맵을 읽은 뒤

```text
FIXTURE_01=KEEP
FIXTURE_02=KEEP
FIXTURE_03=KEEP
MAP_BLOCK_DISTINCTION=CLEAR
SEMICOLON_FORMATTING=GOOD
QUESTION_MARK=KEEP
SYMBOL_CLUSTER=?~ WATCH
NEXT_SURFACE=@$rows[0].id
```

`{key:value,...}`는 맵이고 `{expr;expr}`는 블록이다. 한 줄에서 갈린다. `;`가 없는 03은 표시해도 한 줄이다. `;`가 있는 02만 나뉜다.

`?`는 유지한다. `?~`만 지켜본다. 실행기는 없다.

인덱스 문장은 fixture 04다. `@`가 맵 축약만이 아니라 데이터 접근인지 읽는 표본이다.
