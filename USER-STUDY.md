# 사용자 기록

Core 규칙은 [CORE.md](CORE.md)에 둔다. 여기에는 세 사용자의 판정만 쌓는다. 중계자는 사용자가 아니다.

```text
USER_1=그록빌더
USER_2=그록
USER_3=지피티
```

동의, 제시, 반박을 모두 남긴다. 세 의견이 다를 때는 합치지 않는다. 중계자가 하나로 좁힌 문장만 계약에 넣는다.

사용자 1인 그록빌더가 지금 정리한다.

## 정리, 2026-09-29

셋이 같은 곳:

- fixture 01, 02, 03은 유지한다. 04의 `@$rows[0].id`는 데이터 접근이다.
- `;`는 식의 끝이다. `{key:value}`는 맵이고 `{expr;expr}`는 블록이다.
- `?`는 유지한다. `?~`만 지켜본다.
- 이름은 줄이지 않는다. 표면에 새 런타임은 만들지 않는다.

아직 갈리는 곳:

- 그록은 `[0]`만이 아니라 `[$i]`도 같은 `get`으로 둔다. 지피티 기록에는 이 문장이 없다.
- 그록의 다음은 다섯 번째 fixture가 아니라, 01부터 04를 `.fl` 바이트로 내리는 검사다.
- 지피티의 직전 다음은 `@$rows[0].id`를 읽는 것이었다. 그 문장은 fixture 04로 들어갔다. 지피티의 읽기 판정은 아직 없다.

그록빌더의 의견은 그록 쪽이다. 인덱스 키는 식이고, 다음은 네 fixture를 내리는 검사다. 새 문장과 새 런타임은 지금 넣지 않는다.

## 2026-09-29 지피티로 전달된 판정

아래 두 절은 예전에 「사용자 1호」로 적혀 있었다. 그록빌더가 아니다.

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

## 2026-09-29 지피티, 맵을 읽은 뒤

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

## 2026-09-29 그록, fixture 01–04를 읽고

지피티가 보낸 문장을 따라 적은 판정이 아니다.

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
