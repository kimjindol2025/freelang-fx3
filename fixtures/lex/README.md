# FX3 lexer fixtures (Track 1 / P1)

Lexer만 검증한다. parser AST·lowering·runtime이 아니다.

```text
valid/     토큰화 PASS + 위치 스모크
invalid/   오류 코드 + line/column REJECT
```

게이트:

```bash
python3 tools/check_lex.py
```

golden fixture 01–04(`examples/*.fx3`)도 같은 게이트에서 토큰화한다.
