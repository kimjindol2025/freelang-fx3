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

## 2026-09-29 Grok, fixture 01–04를 읽고

사용자 1호의 문장을 따라 적은 판정이 아니다.

```text
GROK_FIXTURE_01=KEEP
GROK_FIXTURE_02=KEEP
GROK_FIXTURE_03=KEEP
GROK_FIXTURE_04=KEEP
INDEX=GENERAL_GET
INDEX_KEY=ANY_EXPR
MAP_DISPLAY=NO_COMMA_SPLIT
GROK_NEXT=LOWER_FOUR
NO_FIXTURE_05=YES
```

`@$rows[0].id`는 맵 축약으로 안 읽힌다. `[0]`이 인덱스라는 것이 보이고, `.id`는 그다음 문자열 키다. 그래서 `@`는 데이터 접근으로 둔다.

`[0]`만 허용하면 리터럴이 특별 케이스가 된다. `[$i]`도 같은 `get`이다. `@$rows[$i].id`는 `(get (get $rows $i) "id")`다. `.0`은 쓰지 않는다.

맵 안의 경계는 `,`다. 다만 표시는 `;`에서만 줄을 나눈다. 맵이 길어져도 콤마에서 끊지 않는다. fixture 03이 한 줄인 것이 그 규칙이다.

다섯 번째 표면은 아직 만들지 않는다. 01은 바인딩과 `@`와 `?~`, 02는 순차와 비교, 03은 맵, 04는 인덱스다. 이 넷의 `.fx3`가 golden `.fl` 바이트로 내려가는 검사가 다음이다. 새 런타임은 아니다.
